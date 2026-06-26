#!/usr/bin/env python3
"""Unified entrypoint for OpenClaw + Feishu multi-agent scripts."""

from __future__ import annotations

import argparse

import apply_feishu_multi_agent
import audit_feishu_multi_agent
import render_feishu_multi_agent
import repair_feishu_group_sessions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="Render reusable artifacts from a roles file")
    render_parser.add_argument("--roles", required=True)
    render_parser.add_argument("--output-dir", required=True)
    render_parser.add_argument("--state-dir", default="~/.openclaw")

    audit_parser = subparsers.add_parser("audit", help="Audit existing openclaw.json against a roles file")
    audit_parser.add_argument("--roles", required=True)
    audit_parser.add_argument("--config", default="~/.openclaw/openclaw.json")

    repair_parser = subparsers.add_parser("repair", help="Audit or repair Feishu group session metadata")
    repair_parser.add_argument("--roles", required=True)
    repair_parser.add_argument("--group-id", required=True)
    repair_parser.add_argument("--state-dir", default="~/.openclaw")
    repair_parser.add_argument("--fix", action="store_true")
    repair_parser.add_argument("--backup", action="store_true")

    apply_parser = subparsers.add_parser("apply", help="Apply roles to ~/.openclaw semi-automatically")
    apply_parser.add_argument("--roles", required=True)
    apply_parser.add_argument("--state-dir", default="~/.openclaw")
    apply_parser.add_argument("--write", action="store_true")
    apply_parser.add_argument("--backup", action="store_true")
    apply_parser.add_argument("--apply-identities", action="store_true")

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Render, apply, and audit in sequence for a roles file",
    )
    bootstrap_parser.add_argument("--roles", required=True)
    bootstrap_parser.add_argument("--output-dir", required=True)
    bootstrap_parser.add_argument("--state-dir", default="~/.openclaw")
    bootstrap_parser.add_argument("--write", action="store_true")
    bootstrap_parser.add_argument("--backup", action="store_true")
    bootstrap_parser.add_argument("--apply-identities", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "render":
        return render_feishu_multi_agent.main(
            ["--roles", args.roles, "--output-dir", args.output_dir, "--state-dir", args.state_dir]
        )
    if args.command == "audit":
        return audit_feishu_multi_agent.main(["--roles", args.roles, "--config", args.config])
    if args.command == "repair":
        repair_args = ["--roles", args.roles, "--group-id", args.group_id, "--state-dir", args.state_dir]
        if args.fix:
            repair_args.append("--fix")
        if args.backup:
            repair_args.append("--backup")
        return repair_feishu_group_sessions.main(repair_args)
    if args.command == "apply":
        apply_args = ["--roles", args.roles, "--state-dir", args.state_dir]
        if args.write:
            apply_args.append("--write")
        if args.backup:
            apply_args.append("--backup")
        if args.apply_identities:
            apply_args.append("--apply-identities")
        return apply_feishu_multi_agent.main(apply_args)
    if args.command == "bootstrap":
        rc = render_feishu_multi_agent.main(
            ["--roles", args.roles, "--output-dir", args.output_dir, "--state-dir", args.state_dir]
        )
        if rc != 0:
            return rc
        apply_args = ["--roles", args.roles, "--state-dir", args.state_dir]
        if args.write:
            apply_args.append("--write")
        if args.backup:
            apply_args.append("--backup")
        if args.apply_identities:
            apply_args.append("--apply-identities")
        rc = apply_feishu_multi_agent.main(apply_args)
        if rc != 0:
            return rc
        if not args.write:
            print()
            print("Bootstrap finished in dry-run mode, so audit was skipped.")
            print("Re-run with --write if you want bootstrap to apply and audit the live config.")
            return 0
        return audit_feishu_multi_agent.main(["--roles", args.roles, "--config", f"{args.state_dir}/openclaw.json"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
