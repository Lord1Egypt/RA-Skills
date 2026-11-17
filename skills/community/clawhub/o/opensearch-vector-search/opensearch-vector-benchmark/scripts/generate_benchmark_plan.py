#!/usr/bin/env python3
"""Generate a reproducible VectorDBBench command without executing it."""

from __future__ import annotations

import argparse
import json
import re
import shlex
from dataclasses import asdict, dataclass


SAFE_TOKEN = re.compile(r"^[A-Za-z0-9._:-]+$")


@dataclass(frozen=True)
class Plan:
    deployment: str
    host: str
    port: int
    region: str
    case_type: str
    db_label: str
    workflow: str
    phase: str
    metric: str
    engine: str
    quantization: str
    on_disk: bool
    oversample_factor: float
    shards: int
    replicas: int
    m: int
    ef_construction: int
    ef_search: int
    indexing_clients: int
    num_per_batch: int | None
    concurrency: str
    force_merge: bool
    segments: int
    refresh_interval: str
    client_instance: str
    warnings: tuple[str, ...]
    command: str


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be at least 0")
    return parsed


def safe_token(value: str) -> str:
    if not SAFE_TOKEN.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "use only letters, digits, dot, underscore, colon, and hyphen"
        )
    return value


def concurrency_list(value: str) -> str:
    try:
        values = [int(part) for part in value.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a comma-separated integer list") from exc
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("concurrency values must be positive")
    if values != sorted(set(values)):
        raise argparse.ArgumentTypeError("concurrency values must be unique and ascending")
    return ",".join(str(item) for item in values)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Generate, but do not run, an OpenSearch VectorDBBench command."
    )
    result.add_argument(
        "--deployment",
        choices=("managed", "serverless", "s3vector"),
        default="managed",
    )
    result.add_argument(
        "--host",
        required=True,
        type=safe_token,
        help="Host only; do not include https://",
    )
    result.add_argument("--port", type=positive_int, default=443)
    result.add_argument("--region", default="us-east-1", type=safe_token)
    result.add_argument("--case-type", default="Performance768D1M", type=safe_token)
    result.add_argument("--db-label", required=True, type=safe_token)
    result.add_argument(
        "--workflow", choices=("full", "load-only", "query-only"), default="full"
    )
    result.add_argument("--phase", choices=("dry-run", "run"), default="dry-run")
    result.add_argument("--metric", choices=("cosine", "l2", "ip"), default="cosine")
    result.add_argument("--quantization", choices=("fp32", "fp16", "bq"), default="fp32")
    result.add_argument("--on-disk", action="store_true")
    result.add_argument("--oversample-factor", type=float)
    result.add_argument("--shards", type=positive_int, default=1)
    result.add_argument("--replicas", type=nonnegative_int, default=0)
    result.add_argument("--m", type=positive_int, default=16)
    result.add_argument("--ef-construction", type=positive_int, default=200)
    result.add_argument("--ef-search", type=positive_int)
    result.add_argument("--indexing-clients", type=positive_int)
    result.add_argument("--num-per-batch", type=positive_int)
    result.add_argument(
        "--concurrency", type=concurrency_list, default="1,10,20,40,60,80"
    )
    result.add_argument("--segments", type=positive_int, default=1)
    result.add_argument("--refresh-interval", default="60s", type=safe_token)
    result.add_argument("--client-instance", default="4xlarge-class", type=safe_token)
    merge = result.add_mutually_exclusive_group()
    merge.add_argument("--force-merge", dest="force_merge", action="store_true")
    merge.add_argument("--no-force-merge", dest="force_merge", action="store_false")
    result.set_defaults(force_merge=True)
    result.add_argument("--format", choices=("shell", "json"), default="shell")
    return result


def build_plan(args: argparse.Namespace) -> Plan:
    if args.host.startswith(("http://", "https://")):
        raise ValueError("--host must not include a URL scheme")
    if args.oversample_factor is not None and args.oversample_factor <= 0:
        raise ValueError("--oversample-factor must be greater than zero")
    if args.on_disk and args.deployment != "managed":
        raise ValueError("--on-disk is supported only for the managed deployment plan")
    if args.deployment in {"serverless", "s3vector"} and args.quantization != "fp32":
        raise ValueError(
            f"--quantization does not describe the {args.deployment} deployment plan"
        )
    if args.deployment == "s3vector" and args.oversample_factor is not None:
        raise ValueError("--oversample-factor does not apply to the s3vector engine")

    warnings: list[str] = []
    indexing_clients = args.indexing_clients
    num_per_batch = args.num_per_batch

    if args.deployment == "serverless":
        indexing_clients = indexing_clients or 1
        if indexing_clients != 1:
            warnings.append(
                "Serverless starts at one indexing client; validate scaling before increasing it."
            )
        if num_per_batch is not None:
            warnings.append(
                "Serverless controls ingestion behavior; NUM_PER_BATCH may not be honored."
            )
    else:
        indexing_clients = indexing_clients or 40
        num_per_batch = num_per_batch or 20000

    oversample_factor = args.oversample_factor
    if args.on_disk and oversample_factor is None:
        oversample_factor = 2.0
        warnings.append(
            "On-disk 32x defaulted to oversample factor 2 from the OpenSearch 3.7 "
            "100M 1-bit SQ baseline; remeasure for this dataset and version."
        )
    if oversample_factor is None:
        oversample_factor = 1.0
    ef_search = args.ef_search
    if ef_search is None:
        ef_search = 200 if args.on_disk else 100
        if args.on_disk:
            warnings.append(
                "On-disk 32x defaulted to ef_search 200 from the OpenSearch 3.7 "
                "100M 1-bit SQ baseline; also test 800 when recall is the priority."
            )

    if args.quantization == "bq" and not args.on_disk and args.oversample_factor is None:
        warnings.append(
            "Binary quantization uses oversample factor 1; include an explicit sweep for recall."
        )
    if args.client_instance == "4xlarge-class":
        warnings.append(
            "Record the exact EC2 instance type; use a 4xlarge-class or larger client."
        )

    force_merge = args.force_merge
    if args.workflow == "query-only" and force_merge:
        force_merge = False
        warnings.append("Query-only mode disables force merge to preserve the existing index.")

    engine = "s3vector" if args.deployment == "s3vector" else "faiss"
    command = build_command(
        args=args,
        engine=engine,
        indexing_clients=indexing_clients,
        num_per_batch=num_per_batch,
        oversample_factor=oversample_factor,
        ef_search=ef_search,
        force_merge=force_merge,
    )
    return Plan(
        deployment=args.deployment,
        host=args.host,
        port=args.port,
        region=args.region,
        case_type=args.case_type,
        db_label=args.db_label,
        workflow=args.workflow,
        phase=args.phase,
        metric=args.metric,
        engine=engine,
        quantization=args.quantization,
        on_disk=args.on_disk,
        oversample_factor=oversample_factor,
        shards=args.shards,
        replicas=args.replicas,
        m=args.m,
        ef_construction=args.ef_construction,
        ef_search=ef_search,
        indexing_clients=indexing_clients,
        num_per_batch=num_per_batch,
        concurrency=args.concurrency,
        force_merge=force_merge,
        segments=args.segments,
        refresh_interval=args.refresh_interval,
        client_instance=args.client_instance,
        warnings=tuple(warnings),
        command=command,
    )


def build_command(
    *,
    args: argparse.Namespace,
    engine: str,
    indexing_clients: int,
    num_per_batch: int | None,
    oversample_factor: float,
    ef_search: int,
    force_merge: bool,
) -> str:
    command = ["vectordbbench", "awsopensearch"]
    values = [
        ("--db-label", args.db_label),
        ("--host", args.host),
        ("--port", str(args.port)),
        ("--case-type", args.case_type),
        ("--number-of-shards", str(args.shards)),
        ("--number-of-replicas", str(args.replicas)),
        ("--engine", engine),
        ("--metric-type", args.metric),
        ("--number-of-indexing-clients", str(indexing_clients)),
        ("--number-of-segments", str(args.segments)),
        ("--refresh-interval", args.refresh_interval),
        ("--force-merge-enabled", str(force_merge).lower()),
        ("--num-concurrency", args.concurrency),
    ]

    if args.deployment == "serverless":
        command.extend(["--serverless", "--aws-region", args.region])
    else:
        command.extend(
            [
                "--user",
                "${OPENSEARCH_USER:?Set OPENSEARCH_USER}",
                "--password",
                "${OPENSEARCH_PASSWORD:?Set OPENSEARCH_PASSWORD}",
            ]
        )

    if engine != "s3vector":
        values.extend(
            [
                ("--m", str(args.m)),
                ("--ef-construction", str(args.ef_construction)),
                ("--ef-search", str(ef_search)),
                ("--quantization-type", args.quantization),
                ("--oversample-factor", format(oversample_factor, "g")),
            ]
        )
    if args.on_disk:
        command.append("--on-disk")
    if args.workflow == "load-only":
        command.extend(["--skip-search-serial", "--skip-search-concurrent"])
    elif args.workflow == "query-only":
        command.extend(["--skip-drop-old", "--skip-load"])
    if args.phase == "dry-run":
        command.append("--dry-run")

    for option, value in values:
        command.extend([option, value])

    rendered = " \\\n  ".join(shell_word(part) for part in command)
    if num_per_batch is not None:
        return f"export NUM_PER_BATCH={num_per_batch}\n{rendered}"
    return rendered


def shell_word(value: str) -> str:
    if value.startswith("${") and value.endswith("}"):
        return f'"{value}"'
    return shlex.quote(value)


def render_shell(plan: Plan) -> str:
    lines = [
        "# Generated plan only; inspect before execution.",
        f"# Deployment: {plan.deployment}; workflow: {plan.workflow}; phase: {plan.phase}",
        f"# Client: {plan.client_instance}",
    ]
    lines.extend(f"# WARNING: {warning}" for warning in plan.warnings)
    lines.append(plan.command)
    return "\n".join(lines)


def main() -> int:
    args = parser().parse_args()
    try:
        plan = build_plan(args)
    except ValueError as exc:
        parser().error(str(exc))

    if args.format == "json":
        print(json.dumps(asdict(plan), indent=2, sort_keys=True))
    else:
        print(render_shell(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
