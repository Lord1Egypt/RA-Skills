from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .auth import SetupRequiredError, resolve_credentials, setup_required_payload
from .archive import build_report, list_month_messages, pack_month, run_doctor, sync_month
from .config import RuntimeConfig, default_config_path
from .providers import known_mail_provider_ids, list_mail_providers
from .setup_wizard import run_setup


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read supported mailbox providers and archive invoice attachments.")
    parser.add_argument("--config", type=Path, default=None, help="Optional TOML config path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human text.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    providers = subparsers.add_parser("providers", help="List supported mailbox providers.")
    providers.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    providers.set_defaults(handler=cmd_providers)

    doctor = subparsers.add_parser("doctor", help="Check credential storage, IMAP, and runtime settings.")
    doctor.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    doctor.set_defaults(handler=cmd_doctor)

    setup = subparsers.add_parser("setup", help="Configure credential storage for the current machine.")
    setup.add_argument("--provider", choices=["system", "env", "config", "prompt"], default=None)
    setup.add_argument("--mail-provider", choices=list(known_mail_provider_ids(include_auto=True)), default=None)
    setup.add_argument("--email", default=None)
    setup.add_argument("--secret", default=None)
    setup.add_argument("--service", default=None)
    setup.add_argument("--env-email-var", default=None)
    setup.add_argument("--env-secret-var", default=None)
    setup.add_argument("--non-interactive", action="store_true")
    setup.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    setup.set_defaults(handler=cmd_setup)

    lst = subparsers.add_parser("list", help="List month messages without downloading attachments.")
    lst.add_argument("--month", required=True)
    lst.add_argument("--limit", type=int, default=None)
    lst.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    lst.set_defaults(handler=cmd_list)

    sync = subparsers.add_parser("sync", help="Download likely invoice attachments for a month.")
    sync.add_argument("--month", required=True)
    sync.add_argument("--limit", type=int, default=None)
    sync.add_argument("--no-follow-links", action="store_true")
    sync.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    sync.set_defaults(handler=cmd_sync)

    report = subparsers.add_parser("report", help="Build a month summary from the local index.")
    report.add_argument("--month", required=True)
    report.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    report.set_defaults(handler=cmd_report)

    pack = subparsers.add_parser("pack", help="Build zip and summary files for a month.")
    pack.add_argument("--month", required=True)
    pack.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    pack.set_defaults(handler=cmd_pack)

    deliver = subparsers.add_parser("deliver", help="Prepare a month package for chat delivery.")
    deliver.add_argument("--month", required=True)
    deliver.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    deliver.set_defaults(handler=cmd_deliver)
    return parser


def resolve_runtime(config_path: Path | None, *, allow_missing_setup: bool = False) -> tuple[RuntimeConfig, str, str]:
    path = config_path or default_config_path()
    if not path.exists():
        if allow_missing_setup:
            raise SetupRequiredError(path)
        raise SetupRequiredError(path)
    config = RuntimeConfig.load(path)
    credentials = resolve_credentials(config, config_path=path)
    if not config.email_address:
        config.email_address = credentials.email
    return config, credentials.email, credentials.secret


def cmd_providers(args: argparse.Namespace) -> dict[str, object]:
    return {"providers": list_mail_providers()}


def cmd_doctor(args: argparse.Namespace) -> dict[str, object]:
    try:
        config, account, password = resolve_runtime(args.config, allow_missing_setup=True)
    except SetupRequiredError as exc:
        return setup_required_payload(exc.config_path)
    return run_doctor(config, account, password)


def cmd_setup(args: argparse.Namespace) -> dict[str, object]:
    return run_setup(
        config_path=args.config,
        mail_provider=args.mail_provider,
        provider=args.provider,
        email=args.email,
        secret=args.secret,
        service=args.service,
        env_email_var=args.env_email_var,
        env_secret_var=args.env_secret_var,
        interactive=not args.non_interactive,
    )


def cmd_list(args: argparse.Namespace) -> list[dict[str, object]]:
    config, account, password = resolve_runtime(args.config)
    return list_month_messages(config, account, password, args.month, limit=args.limit)


def cmd_sync(args: argparse.Namespace) -> dict[str, object]:
    config, account, password = resolve_runtime(args.config)
    result = sync_month(
        config,
        account,
        password,
        args.month,
        limit=args.limit,
        follow_links=not args.no_follow_links,
    )
    return {
        "month": result.month,
        "scanned_messages": result.scanned_messages,
        "canonical_saved": result.canonical_saved,
        "duplicates": result.duplicates,
        "conflicts": result.conflicts,
        "failures": result.failures,
        "link_failures": result.link_failures,
        "saved_paths": result.saved_paths,
    }


def cmd_report(args: argparse.Namespace) -> dict[str, object]:
    config = RuntimeConfig.load(args.config)
    return build_report(config, args.month)


def cmd_pack(args: argparse.Namespace) -> dict[str, object]:
    config = RuntimeConfig.load(args.config)
    result = pack_month(config, args.month)
    return {
        "month": result.month,
        "zip_path": result.zip_path,
        "summary_path": result.summary_path,
        "summary_json_path": result.summary_json_path,
    }


def cmd_deliver(args: argparse.Namespace) -> dict[str, object]:
    config = RuntimeConfig.load(args.config)
    result = pack_month(config, args.month)
    return {
        "month": result.month,
        "delivery_channel": config.chat_delivery_channel,
        "attachment_path": result.zip_path,
        "summary_path": result.summary_path,
        "summary_json_path": result.summary_json_path,
        "instructions": (
            "Attach the zip file to the current chat, paste the markdown summary, "
            "and call out high-value invoices plus any failures."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = args.handler(args)
    except SetupRequiredError as exc:
        payload = setup_required_payload(exc.config_path)
    except RuntimeError as exc:
        payload = {"error": str(exc)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if "error" not in payload else 1


if __name__ == "__main__":
    raise SystemExit(main())
