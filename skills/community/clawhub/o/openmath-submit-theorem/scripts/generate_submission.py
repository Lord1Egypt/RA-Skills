#!/usr/bin/env python3
"""Generate OpenMath proof submission commands for direct or authz-based flows."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path

from calculate_proof_hash import calculate_proof_hash
from submission_config import (
    DEFAULT_SHENTU_CHAIN_ID,
    DEFAULT_SHENTU_NODE_URL,
    KEYRING_BACKEND,
    SubmissionConfig,
    SubmissionConfigError,
    load_submission_config,
)


DEFAULT_WAIT_SECONDS = 6
DEFAULT_MODE = os.environ.get("OPENMATH_SUBMISSION_MODE", "authz")
DEFAULT_INNER_TX_FEES = os.environ.get("OPENMATH_INNER_TX_FEES", "5000uctk")
DEFAULT_INNER_TX_GAS = os.environ.get("OPENMATH_INNER_TX_GAS", "200000")


def shell_quote(value: object) -> str:
    return shlex.quote(str(value))


def read_proof_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Proof file not found: {file_path}")
    return path.read_text(encoding="utf-8")


def outer_gas_flags(
    shentu_chain_id: str = DEFAULT_SHENTU_CHAIN_ID,
    shentu_node_url: str = DEFAULT_SHENTU_NODE_URL,
) -> str:
    return (
        f"--gas auto --gas-adjustment 2.0 --gas-prices 0.025uctk "
        f"--keyring-backend {shell_quote(KEYRING_BACKEND)} "
        f"--chain-id {shell_quote(shentu_chain_id)} "
        f"--node {shell_quote(shentu_node_url)} -y"
    )


def inner_generate_only_flags(
    shentu_chain_id: str = DEFAULT_SHENTU_CHAIN_ID,
) -> str:
    return (
        f"--fees {shell_quote(DEFAULT_INNER_TX_FEES)} "
        f"--gas {shell_quote(DEFAULT_INNER_TX_GAS)} "
        f"--chain-id {shell_quote(shentu_chain_id)} "
        f"--keyring-backend {shell_quote(KEYRING_BACKEND)} "
        "--generate-only -o json"
    )


def post_broadcast_hint(command: str) -> None:
    print("\nAfter broadcasting and receiving a txhash, wait about 5-10 seconds for block inclusion.")
    print("Recommended follow-up:")
    print(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate shentud commands for OpenMath proof submission.",
    )
    parser.add_argument(
        "--mode",
        choices=["authz", "direct"],
        default=DEFAULT_MODE,
        help=f"Submission mode (default: {DEFAULT_MODE})",
    )
    parser.add_argument(
        "--config",
        default=None,
        help=(
            "Shared config path (resolution: --config, then OPENMATH_ENV_CONFIG, "
            "then ./.openmath-skills/openmath-env.json, then ~/.openmath-skills/openmath-env.json)."
        ),
    )
    subparsers = parser.add_subparsers(dest="mode_name", required=True)

    hash_parser = subparsers.add_parser("hash", help="Generate the stage 1 proof-hash command.")
    hash_parser.add_argument("theorem_id", type=int, help="OpenMath theorem ID")
    hash_parser.add_argument("proof_path", help="Path to the proof file")
    hash_parser.add_argument(
        "prover_from",
        help="Original prover key or OpenMath wallet address for direct mode. Retained for compatibility; authz mode uses prover_address from config.",
    )
    hash_parser.add_argument("prover_addr", help="OpenMath wallet address on Shentu")
    hash_parser.add_argument(
        "--tx-json",
        default="proofhash.json",
        help="Output tx JSON filename for authz mode (default: proofhash.json)",
    )

    detail_parser = subparsers.add_parser(
        "detail",
        help="Generate the stage 2 proof-detail command.",
    )
    detail_parser.add_argument(
        "proof_id",
        help="On-chain proof ID returned after stage 1. On Yulei this is the proof hash string.",
    )
    detail_parser.add_argument("proof_path", help="Path to the proof file")
    detail_parser.add_argument(
        "prover_from",
        help="Original prover key or OpenMath wallet address for direct mode. Retained for compatibility; authz mode uses prover_address from config.",
    )
    detail_parser.add_argument(
        "--tx-json",
        default="proofdetail.json",
        help="Output tx JSON filename for authz mode (default: proofdetail.json)",
    )

    return parser


def load_authz_config_or_exit(config_path: str) -> SubmissionConfig:
    try:
        return load_submission_config(config_path)
    except SubmissionConfigError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)


def print_authz_preamble(config: SubmissionConfig) -> None:
    print("Mode: authz")
    print("Config:", config.config_path)
    print("Prover Addr:", config.prover_address)
    print("Agent Key:", config.agent_key_name)
    print("Agent Addr:", config.agent_address)
    print("Fee Granter (derived):", config.fee_granter_address)
    print("\nPre-check:")
    print(f"python3 scripts/check_authz_setup.py --config {shell_quote(config.config_path)}")


def print_direct_preamble() -> None:
    print("Mode: direct")


def enforce_authz_gate(config: SubmissionConfig) -> None:
    script_path = Path(__file__).with_name("check_authz_setup.py")
    command = [
        sys.executable,
        str(script_path),
        "--config",
        str(config.config_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        print(
            "\nFirst-run gate: stop here. Do not generate submission commands until "
            "`check_authz_setup.py` returns `Status: ready`."
        )
        raise SystemExit(1)


def authz_hash_generate_command(
    theorem_id: int,
    proof_hash: str,
    prover_addr: str,
    tx_json: str,
    config: SubmissionConfig,
) -> str:
    return (
        "shentud tx bounty proof-hash "
        f"--theorem-id {shell_quote(theorem_id)} "
        f"--hash {shell_quote(proof_hash)} "
        "--deposit 1000000uctk "
        f"--from {shell_quote(prover_addr)} "
        f"{inner_generate_only_flags(config.shentu_chain_id)} > {shell_quote(tx_json)}"
    )


def authz_detail_generate_command(
    proof_id: str,
    detail_content: str,
    prover_addr: str,
    tx_json: str,
    config: SubmissionConfig,
) -> str:
    return (
        "shentud tx bounty proof-detail "
        f"--proof-id {shell_quote(proof_id)} "
        f"--detail {shell_quote(detail_content)} "
        f"--from {shell_quote(prover_addr)} "
        f"{inner_generate_only_flags(config.shentu_chain_id)} > {shell_quote(tx_json)}"
    )


def authz_exec_command(tx_json: str, config: SubmissionConfig) -> str:
    return (
        "shentud tx authz exec "
        f"{shell_quote(tx_json)} "
        f"--from {shell_quote(config.agent_key_name)} "
        f"--fee-granter {shell_quote(config.fee_granter_address)} "
        f"{outer_gas_flags(config.shentu_chain_id, config.shentu_node_url)}"
    )


def direct_hash_command(theorem_id: int, proof_hash: str, prover_from: str) -> str:
    return (
        "shentud tx bounty proof-hash "
        f"--theorem-id {shell_quote(theorem_id)} "
        f"--hash {shell_quote(proof_hash)} "
        "--deposit 1000000uctk "
        f"--from {shell_quote(prover_from)} "
        f"{outer_gas_flags()}"
    )


def direct_detail_command(proof_id: str, detail_content: str, prover_from: str) -> str:
    return (
        "shentud tx bounty proof-detail "
        f"--proof-id {shell_quote(proof_id)} "
        f"--detail {shell_quote(detail_content)} "
        f"--from {shell_quote(prover_from)} "
        f"{outer_gas_flags()}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])
    config: SubmissionConfig | None = None

    if args.mode == "authz":
        config = load_authz_config_or_exit(args.config)
        enforce_authz_gate(config)

    try:
        detail_content = read_proof_file(args.proof_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.mode_name == "hash":
        proof_hash = calculate_proof_hash(args.theorem_id, args.prover_addr, detail_content)
        print("\n--- Stage 1: Submit Proof Hash (Commitment) ---")
        print("Theorem ID:", args.theorem_id)
        print("Prover Addr:", args.prover_addr)
        print("Verified Proof Hash (SHA256):", proof_hash)
        print("Stage 2 Proof ID:", proof_hash)

        if args.mode == "authz":
            assert config is not None
            if config.prover_address != args.prover_addr:
                print(
                    "Error: config prover_address does not match the CLI prover address.",
                    file=sys.stderr,
                )
                print(f"Config: {config.prover_address}", file=sys.stderr)
                print(f"CLI:    {args.prover_addr}", file=sys.stderr)
                return 1

            print()
            print_authz_preamble(config)
            print("\nGenerate inner tx JSON:")
            print(
                authz_hash_generate_command(
                    args.theorem_id,
                    proof_hash,
                    config.prover_address,
                    args.tx_json,
                    config,
                )
            )
            print("\nBroadcast via authz + feegrant:")
            print(authz_exec_command(args.tx_json, config))
        else:
            print()
            print_direct_preamble()
            print("\nCommand:")
            print(direct_hash_command(args.theorem_id, proof_hash, args.prover_from))

        post_broadcast_hint(
            "python3 scripts/query_submission_status.py "
            f"tx <txhash> --wait-seconds {DEFAULT_WAIT_SECONDS}"
        )
        return 0

    if args.mode_name == "detail":
        print("\n--- Stage 2: Submit Proof Detail (Reveal) ---")
        print("Proof ID:", args.proof_id)

        if args.mode == "authz":
            assert config is not None
            print()
            print_authz_preamble(config)
            print("\nGenerate inner tx JSON:")
            print(
                authz_detail_generate_command(
                    args.proof_id,
                    detail_content,
                    config.prover_address,
                    args.tx_json,
                    config,
                )
            )
            print("\nBroadcast via authz + feegrant:")
            print(authz_exec_command(args.tx_json, config))
        else:
            print()
            print_direct_preamble()
            print("\nCommand:")
            print(direct_detail_command(args.proof_id, detail_content, args.prover_from))

        post_broadcast_hint(
            "python3 scripts/query_submission_status.py "
            f"theorem <theoremId> --wait-seconds {DEFAULT_WAIT_SECONDS}"
        )
        return 0

    parser.error(f"unsupported mode: {args.mode_name}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
