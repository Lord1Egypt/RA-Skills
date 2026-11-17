#!/usr/bin/env python3
"""Stream Hardware Inspector to an SSH host or Kubernetes pod."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

VERSION = "0.1.0"
MAX_REPORT_BYTES = 10 * 1024 * 1024
SSH_TARGET_RE = re.compile(r"^[A-Za-z0-9_.:@%+\-\[\]]+$")
REMOTE_PYTHON_RE = re.compile(r"^(?:[A-Za-z0-9_.-]+|/[A-Za-z0-9_./-]+)$")
KUBERNETES_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?$")
KUBERNETES_CONTEXT_RE = re.compile(r"^[A-Za-z0-9_.:/@+\-]+$")


class RemoteInspectionError(RuntimeError):
    """A safe, user-facing remote inspection failure."""


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def port_number(value: str) -> int:
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("must be between 1 and 65535")
    return port


def validate_ssh_target(value: str) -> str:
    if not value or value.startswith("-") or not SSH_TARGET_RE.fullmatch(value):
        raise RemoteInspectionError(
            "SSH target must be a host, alias, IP, or user@host without whitespace or options"
        )
    return value


def validate_remote_python(value: str) -> str:
    if (
        not value
        or value.startswith("-")
        or not REMOTE_PYTHON_RE.fullmatch(value)
        or ".." in Path(value).parts
    ):
        raise RemoteInspectionError(
            "remote Python must be a command name or absolute POSIX path"
        )
    return value


def validate_kubernetes_name(label: str, value: str) -> str:
    if not value or value.startswith("-") or not KUBERNETES_NAME_RE.fullmatch(value):
        raise RemoteInspectionError(
            "{} must be a Kubernetes DNS-style name".format(label)
        )
    return value


def validate_kubernetes_context(value: str) -> str:
    if not value or value.startswith("-") or not KUBERNETES_CONTEXT_RE.fullmatch(value):
        raise RemoteInspectionError(
            "Kubernetes context contains unsupported characters"
        )
    return value


def checked_local_path(label: str, value: Optional[Path]) -> Optional[Path]:
    if value is None:
        return None
    path = value.expanduser()
    if not path.is_file():
        raise RemoteInspectionError("{} does not exist: {}".format(label, path))
    return path


def collector_command(args: argparse.Namespace) -> List[str]:
    command = [
        validate_remote_python(args.remote_python),
        "-",
        "--format",
        args.format,
        "--timeout",
        str(args.probe_timeout),
    ]
    if args.full:
        command.append("--full")
    if args.no_redact:
        command.append("--no-redact")
    return command


def build_ssh_command(args: argparse.Namespace) -> List[str]:
    target = validate_ssh_target(args.target)
    command = [
        "ssh",
        "-T",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout={}".format(args.connect_timeout),
    ]
    if args.port is not None:
        command.extend(["-p", str(args.port)])
    identity = checked_local_path("SSH identity file", args.identity_file)
    if identity is not None:
        command.extend(["-i", str(identity)])
    command.append(target)
    command.extend(collector_command(args))
    return command


def build_kubernetes_command(args: argparse.Namespace) -> List[str]:
    pod = validate_kubernetes_name("pod", args.pod)
    command = ["kubectl"]
    kubeconfig = checked_local_path("kubeconfig", args.kubeconfig)
    if kubeconfig is not None:
        command.append("--kubeconfig={}".format(kubeconfig))
    if args.context:
        command.append("--context={}".format(validate_kubernetes_context(args.context)))
    if args.namespace:
        command.append(
            "--namespace={}".format(
                validate_kubernetes_name("namespace", args.namespace)
            )
        )
    command.extend(["exec", "-i", pod])
    if args.container:
        command.extend(["-c", validate_kubernetes_name("container", args.container)])
    command.append("--")
    command.extend(collector_command(args))
    return command


def read_collector_source() -> str:
    collector = Path(__file__).resolve().with_name("hardware_report.py")
    try:
        return collector.read_text(encoding="utf-8")
    except OSError as error:
        raise RemoteInspectionError(
            "cannot read bundled collector {}: {}".format(collector, error)
        ) from error


def execute_transport(
    command: Sequence[str], collector_source: str, timeout: float
) -> subprocess.CompletedProcess[str]:
    executable = shutil.which(command[0])
    if not executable:
        raise RemoteInspectionError(
            "required transport executable is not installed: {}".format(command[0])
        )
    effective_command = list(command)
    effective_command[0] = executable
    try:
        return subprocess.run(
            effective_command,
            input=collector_source,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RemoteInspectionError(
            "remote inspection exceeded the transport timeout of {} seconds".format(
                timeout
            )
        ) from error
    except OSError as error:
        raise RemoteInspectionError(
            "transport failed to start: {}".format(error)
        ) from error


def transport_metadata(kind: str) -> Dict[str, Any]:
    return {
        "kind": kind,
        "network_connection": True,
        "collector_streamed_via_stdin": True,
        "remote_file_created": False,
        "target_identifier_included": False,
    }


def annotate_output(output: str, output_format: str, kind: str) -> str:
    metadata = transport_metadata(kind)
    if output_format == "json":
        try:
            report = json.loads(output)
        except json.JSONDecodeError as error:
            raise RemoteInspectionError(
                "remote collector returned invalid JSON: {}".format(error)
            ) from error
        if not isinstance(report, dict) or report.get("schema_version") != "1.0":
            raise RemoteInspectionError(
                "remote collector returned an unsupported report contract"
            )
        report["transport"] = metadata
        return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    note = (
        "> Remote transport: **{}** used a network connection. The streamed "
        "collector itself made no network requests and created no remote file."
    ).format(kind)
    lines = output.rstrip().splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join([lines[0], "", note, ""] + lines[1:]).rstrip() + "\n"
    return note + "\n\n" + output.rstrip() + "\n"


def ensure_output_size(output: str) -> None:
    size = len(output.encode("utf-8"))
    if size > MAX_REPORT_BYTES:
        raise RemoteInspectionError(
            "remote report is {} bytes, exceeding the {} byte safety limit".format(
                size, MAX_REPORT_BYTES
            )
        )


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--output", type=Path, help="Write the remote report to a local file."
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include slower peripheral and ML framework probes; frameworks may initialize accelerators.",
    )
    parser.add_argument(
        "--probe-timeout",
        type=positive_float,
        default=8.0,
        help="Default timeout for each remote probe (default: 8 seconds).",
    )
    parser.add_argument(
        "--transport-timeout",
        type=positive_float,
        default=120.0,
        help="Overall SSH or kubectl timeout (default: 120 seconds).",
    )
    parser.add_argument(
        "--python",
        dest="remote_python",
        default="python3",
        help="Python 3.9+ executable on the target (default: python3).",
    )
    parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Disable collector redaction. Review the result before sharing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the transport command without connecting.",
    )


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a remote machine without installing the skill there."
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    subparsers = parser.add_subparsers(dest="transport", required=True)

    ssh_parser = subparsers.add_parser(
        "ssh", help="Stream the collector to a host through OpenSSH."
    )
    ssh_parser.add_argument("target", help="SSH host, alias, IP, or user@host.")
    ssh_parser.add_argument("--port", type=port_number)
    ssh_parser.add_argument("--identity-file", type=Path)
    ssh_parser.add_argument(
        "--connect-timeout",
        type=positive_int,
        default=10,
        help="SSH connection timeout (default: 10 seconds).",
    )
    add_common_options(ssh_parser)
    ssh_parser.set_defaults(command_builder=build_ssh_command, transport_kind="ssh")

    kubernetes_parser = subparsers.add_parser(
        "kubernetes",
        aliases=["k8s"],
        help="Stream the collector into a running Kubernetes pod.",
    )
    kubernetes_parser.add_argument("pod", help="Running pod name.")
    kubernetes_parser.add_argument("--namespace", "-n")
    kubernetes_parser.add_argument("--context")
    kubernetes_parser.add_argument("--container", "-c")
    kubernetes_parser.add_argument("--kubeconfig", type=Path)
    add_common_options(kubernetes_parser)
    kubernetes_parser.set_defaults(
        command_builder=build_kubernetes_command, transport_kind="kubernetes"
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        command = args.command_builder(args)
        if args.dry_run:
            sys.stdout.write(shlex.join(command) + "\n")
            return 0

        collector_source = read_collector_source()
        completed = execute_transport(command, collector_source, args.transport_timeout)
        if completed.returncode != 0:
            sys.stderr.write(
                "Remote transport exited with status {}.\n".format(completed.returncode)
            )
            if completed.stderr:
                sys.stderr.write(completed.stderr.rstrip() + "\n")
            if completed.stdout:
                sys.stderr.write("Remote stdout:\n" + completed.stdout.rstrip() + "\n")
            return 1

        if completed.stderr:
            sys.stderr.write(completed.stderr)
        rendered = annotate_output(completed.stdout, args.format, args.transport_kind)
        ensure_output_size(rendered)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0
    except RemoteInspectionError as error:
        sys.stderr.write("Remote inspection failed: {}\n".format(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
