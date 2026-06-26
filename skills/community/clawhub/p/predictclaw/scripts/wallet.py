#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

SKILL_DIR = Path(__file__).resolve().parent.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import lib  # pyright: ignore[reportMissingImports]

from lib.config import ConfigError, PredictConfig  # pyright: ignore[reportMissingImports]
from lib.local_env import load_local_env  # pyright: ignore[reportMissingImports]
from lib.mandated_mcp_bridge import MandatedVaultMcpError  # pyright: ignore[reportMissingImports]
from lib.wallet_manager import WalletManager  # pyright: ignore[reportMissingImports]

FundingService = getattr(lib, "FundingService")


if os.getenv("PREDICTCLAW_DISABLE_LOCAL_ENV") != "1":
    load_local_env(SKILL_DIR)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="predictclaw wallet",
        description="Inspect predict.fun wallet readiness, funding addresses, approvals, and withdrawals.",
    )
    subparsers = parser.add_subparsers(dest="command")

    status = subparsers.add_parser(
        "status",
        help="Show wallet mode, funding guidance, balances, and approval readiness.",
    )
    status.add_argument("--json", action="store_true")
    status.set_defaults(handler=_handle_status)

    approve = subparsers.add_parser(
        "approve",
        help="Set regular and yield-bearing approvals for predict.fun trading.",
    )
    approve.add_argument("--json", action="store_true")
    approve.set_defaults(handler=_handle_approve)

    deposit = subparsers.add_parser(
        "deposit",
        help="Show manual top-up guidance, trading recipient, chain, and accepted assets.",
        description=(
            "Display funding guidance for the current mode. EOA mode deposits to the signer address directly. "
            "Predict Account + vault mode treats the Vault deposit flow as the default funding entry, while Predict Account "
            "remains the trading recipient/identity and receives the downstream vault-driven top-up. "
            "BNB is required for gas and USDT is the supported trading asset."
        ),
    )
    deposit.add_argument("--json", action="store_true")
    deposit.set_defaults(handler=_handle_deposit)

    continue_funding = subparsers.add_parser(
        "continue-funding",
        help="Record a confirmed funding transaction and advance the active overlay session.",
    )
    continue_funding.add_argument("--tx-hash", required=True)
    continue_funding.add_argument("--confirmations", type=int, default=1)
    continue_funding.add_argument("--block-number")
    continue_funding.add_argument("--block-hash")
    continue_funding.add_argument("--json", action="store_true")
    continue_funding.set_defaults(handler=_handle_continue_funding)

    continue_follow_up = subparsers.add_parser(
        "continue-follow-up",
        help="Record a terminal follow-up result and advance the active overlay session.",
    )
    continue_follow_up.add_argument("--reference-type", required=True)
    continue_follow_up.add_argument("--reference-value", required=True)
    continue_follow_up.add_argument(
        "--status",
        choices=["succeeded", "failed", "skipped"],
        default="succeeded",
    )
    continue_follow_up.add_argument("--output-json")
    continue_follow_up.add_argument("--json", action="store_true")
    continue_follow_up.set_defaults(handler=_handle_continue_follow_up)

    bootstrap = subparsers.add_parser(
        "bootstrap-vault",
        help="Preview or confirm pure mandated-vault bootstrap deployment.",
        description=(
            "Preview the pure mandated-vault bootstrap using the product-configured factory 0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6. "
            "Without --confirm this command only shows the predicted vault, chain, signer, and "
            "transaction summary. Explicit confirmation is required before broadcast. With --confirm it executes MCP vault_bootstrap, auto-bridges the execute-only broadcast gate and bootstrap signer env for that subprocess, and returns a manual env block you can copy into .env yourself."
        ),
    )
    bootstrap.add_argument(
        "--confirm",
        action="store_true",
        help="Broadcast the vault deployment and return a manual env block.",
    )
    bootstrap.add_argument("--json", action="store_true")
    bootstrap.set_defaults(handler=_handle_bootstrap_vault)

    redeem_vault = subparsers.add_parser(
        "redeem-vault",
        help="Preview whether vault share tokens can be redeemed into the underlying asset.",
        description=(
            "Preview vault share redemption without broadcasting. This command inspects the share token, "
            "underlying asset, current share balance, ERC4626 redeem limits, and any blocking contract error."
        ),
    )
    redeem_vault.add_argument(
        "--preview",
        action="store_true",
        help="Explicitly request preview mode (current implementation is preview-only).",
    )
    redeem_vault.add_argument(
        "--share-token",
        required=True,
        help="Vault share token address to inspect.",
    )
    redeem_vault.add_argument(
        "--holder",
        help="Holder address to inspect. Defaults to the configured executor/bootstrap/auth signer when available.",
    )
    redeem_vault.add_argument(
        "--all",
        action="store_true",
        help="Preview redemption of the holder's full current share balance.",
    )
    redeem_vault.add_argument(
        "--confirm",
        action="store_true",
        help="Reserved for future execution support; current implementation is preview-only.",
    )
    redeem_vault.add_argument("--json", action="store_true")
    redeem_vault.set_defaults(handler=_handle_redeem_vault)

    withdraw = subparsers.add_parser(
        "withdraw",
        help="Withdraw USDT or BNB to an external address.",
        description=(
            "Withdraw predict.fun assets to an external destination. USDT uses token transfer semantics and "
            "BNB uses native value transfer semantics. Commands validate destination format, positive amount, "
            "sufficient balance, and gas headroom before submission."
        ),
    )
    withdraw_subparsers = withdraw.add_subparsers(dest="asset")

    for asset in ("usdt", "bnb"):
        asset_parser = withdraw_subparsers.add_parser(
            asset,
            help=f"Withdraw {asset.upper()} to an external address.",
        )
        asset_parser.add_argument("amount")
        asset_parser.add_argument("to")
        asset_parser.add_argument("--json", action="store_true")
        asset_parser.add_argument("--all", action="store_true")
        asset_parser.set_defaults(handler=_handle_withdraw)

    return parser


def _load_manager() -> WalletManager:
    return WalletManager(PredictConfig.from_env())


def _load_funding_service() -> Any:
    return FundingService(PredictConfig.from_env())


def _emit_error(args: argparse.Namespace, error: Exception) -> int:
    if args.json:
        payload: dict[str, object] = {
            "success": False,
            "error": type(error).__name__,
            "message": str(error),
        }
        if hasattr(error, "to_dict"):
            error_payload = cast(dict[str, object], getattr(error, "to_dict")())
            payload.update(
                {key: value for key, value in error_payload.items() if key != "message"}
            )
        print(json.dumps(payload, indent=2))
        return 1

    if hasattr(error, "format_lines"):
        for line in cast(list[str], getattr(error, "format_lines")()):
            print(line)
        return 1

    print(str(error))
    return 1


def _handle_status(args: argparse.Namespace) -> int:
    try:
        status = _load_manager().get_status()
    except (ConfigError, MandatedVaultMcpError) as error:
        return _emit_error(args, error)

    if args.json:
        print(json.dumps(status.to_dict(), indent=2))
        return 0

    payload = status.to_dict()
    if payload.get("mode") == "mandated-vault":
        selected_chain = payload.get("selectedChain")
        if not isinstance(selected_chain, dict):
            selected_chain = {}
        mcp = payload.get("mcp")
        if not isinstance(mcp, dict):
            mcp = {}
        print(f"Mode: {payload.get('mode')}")
        print(
            f"Selected Chain: {selected_chain.get('name')} ({selected_chain.get('chainId')})"
        )
        print(f"MCP Command: {mcp.get('command')}")
        print(f"MCP Runtime Ready: {'yes' if mcp.get('runtimeReady') else 'no'}")
        print(f"Active Route: {payload.get('activeRoute')}")
        print(f"Route Purpose: {payload.get('routePurpose')}")
        if payload.get("sessionScope") is not None:
            print(f"Session Scope: {payload.get('sessionScope')}")
        session_binding = payload.get("sessionBinding")
        if isinstance(session_binding, dict):
            print(f"Linked Position ID: {session_binding.get('positionId')}")
            print(f"Linked Market ID: {session_binding.get('marketId')}")
        print(
            "State-changing Flows Enabled: "
            f"{'yes' if payload.get('stateChangingFlowsEnabled') else 'no'}"
        )
        print(
            "Route Guidance: This route funds the vault itself, not the Predict Account."
        )
        print(
            f"Vault Address: {payload.get('vaultAddress')} ({payload.get('vaultAddressSource')})"
        )
        print(f"Vault Deployed: {'yes' if payload.get('vaultDeployed') else 'no'}")
        missing = mcp.get("missingRequiredTools", [])
        print(
            f"Missing Required MCP Tools: {', '.join(missing) if missing else 'none'}"
        )
        health = payload.get("vaultHealth")
        if isinstance(health, dict):
            print(f"Mandate Authority: {health.get('mandateAuthority')}")
            print(f"Authority Epoch: {health.get('authorityEpoch')}")
            print(f"Nonce Threshold: {health.get('nonceThreshold')}")
            print(f"Total Assets: {health.get('totalAssets')}")
        permission_summary = payload.get("permissionSummary")
        if isinstance(permission_summary, dict):
            print(f"Vault Authority: {permission_summary.get('vaultAuthority')}")
            print(f"Vault Executor: {permission_summary.get('vaultExecutor')}")
            print(f"Bootstrap Signer: {permission_summary.get('bootstrapSigner')}")
            print(f"Underlying Asset: {permission_summary.get('underlyingAsset')}")
            if permission_summary.get("allowedTokenAddresses"):
                print(
                    "Allowed Tokens: "
                    + ", ".join(
                        cast(list[str], permission_summary["allowedTokenAddresses"])
                    )
                )
            if permission_summary.get("allowedRecipients"):
                print(
                    "Allowed Recipients: "
                    + ", ".join(
                        cast(list[str], permission_summary["allowedRecipients"])
                    )
                )
        return 0

    approvals = payload.get("approvals")
    if not isinstance(approvals, dict):
        approvals = {}
    standard = approvals.get("standard")
    if not isinstance(standard, dict):
        standard = {}
    yield_bearing = approvals.get("yieldBearing")
    if not isinstance(yield_bearing, dict):
        yield_bearing = {}

    print(f"Mode: {payload.get('mode')}")
    print(f"Chain: {payload.get('chain')}")
    print(f"Signer Address: {payload.get('signerAddress')}")
    print(f"Funding Address: {payload.get('fundingAddress')}")
    if payload.get("activeRoute") is not None:
        print(f"Active Route: {payload.get('activeRoute')}")
    if payload.get("routePurpose") is not None:
        print(f"Route Purpose: {payload.get('routePurpose')}")
    print(f"BNB Balance (wei): {payload.get('bnbBalanceWei')}")
    print(f"USDT Balance (wei): {payload.get('usdtBalanceWei')}")
    print(f"Auth Ready: {'yes' if payload.get('authReady') else 'no'}")
    print(f"Standard Approvals Ready: {'yes' if standard.get('ready') else 'no'}")
    print(
        f"Yield-bearing Approvals Ready: {'yes' if yield_bearing.get('ready') else 'no'}"
    )
    if payload.get("fundingRoute") == "vault-to-predict-account":
        print(f"Funding Route: {payload.get('fundingRoute')}")
        print(
            f"Default Funding Entry (Vault Deposit): {payload.get('manualTopUpAddress')}"
        )
        print(f"Predict Account Recipient: {payload.get('predictAccountAddress')}")
        print(f"Trading Identity Address: {payload.get('tradingIdentityAddress')}")
        print(f"Trade Signer Address: {payload.get('tradeSignerAddress')}")
        print(
            f"Orchestration Vault Address: {payload.get('orchestrationVaultAddress')} ({payload.get('vaultAddressSource', 'unknown')})"
        )
        print(f"Funding Guidance: {payload.get('manualTopUpGuidance')}")
        for line in _overlay_human_next_steps(payload):
            print(line)
    return 0


def _handle_approve(args: argparse.Namespace) -> int:
    try:
        result = _load_manager().approve()
    except ConfigError as error:
        return _emit_error(args, error)

    payload = result.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
        return 0

    standard = payload["standard"]
    yield_bearing = payload["yieldBearing"]
    print(f"Standard approvals: {standard}")
    print(f"Yield-bearing approvals: {yield_bearing}")
    return 0


def _handle_deposit(args: argparse.Namespace) -> int:
    try:
        details = _load_funding_service().get_deposit_details()
    except (ConfigError, MandatedVaultMcpError) as error:
        return _emit_error(args, error)

    payload = details.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    if payload.get("mode") == "mandated-vault":
        print(f"Mode: {payload['mode']}")
        print(f"Active Route: {payload.get('activeRoute')}")
        print(f"Route Purpose: {payload.get('routePurpose')}")
        print(
            f"Vault Address: {payload['fundingAddress']} ({payload.get('vaultAddressSource', 'unknown')})"
        )
        print(
            "Route Guidance: This route funds the vault itself, not the Predict Account."
        )
        print(f"Vault Exists: {'yes' if payload.get('vaultExists') else 'no'}")
        print("Accepted Assets: BNB, USDT")
        permission_summary = payload.get("permissionSummary")
        if isinstance(permission_summary, dict):
            print(f"Vault Authority: {permission_summary.get('vaultAuthority')}")
            print(f"Vault Executor: {permission_summary.get('vaultExecutor')}")
            print(f"Bootstrap Signer: {permission_summary.get('bootstrapSigner')}")
            print(f"Underlying Asset: {permission_summary.get('underlyingAsset')}")
        preparation = payload.get("createVaultPreparation")
        if isinstance(preparation, dict):
            tx_summary = preparation.get("txSummary", {})
            print("Create Vault Transaction: prepared only (not broadcast)")
            print(f"  from: {tx_summary.get('from')}")
            print(f"  to: {tx_summary.get('to')}")
            print(f"  value: {tx_summary.get('value')}")
            print(f"  gas: {tx_summary.get('gas')}")
            print(f"  data: {tx_summary.get('data')}")
        return 0

    if payload.get("fundingRoute") == "vault-to-predict-account":
        print(f"Mode: {payload['mode']}")
        print(f"Active Route: {payload.get('activeRoute')}")
        print(f"Route Purpose: {payload.get('routePurpose')}")
        if payload.get("sessionScope") is not None:
            print(f"Session Scope: {payload.get('sessionScope')}")
        session_binding = payload.get("sessionBinding")
        if isinstance(session_binding, dict):
            print(f"Linked Position ID: {session_binding.get('positionId')}")
            print(f"Linked Market ID: {session_binding.get('marketId')}")
        print(f"Funding Route: {payload['fundingRoute']}")
        print(
            f"Default Funding Entry (Vault Deposit): {payload.get('manualTopUpAddress')}"
        )
        print(f"Predict Account Recipient: {payload['predictAccountAddress']}")
        print(f"Trading Identity Address: {payload.get('tradingIdentityAddress')}")
        print(f"Trade Signer Address: {payload['tradeSignerAddress']}")
        print(
            f"Orchestration Vault Address: {payload.get('orchestrationVaultAddress')} ({payload.get('vaultAddressSource', 'unknown')})"
        )
        print(f"Funding Guidance: {payload.get('manualTopUpGuidance')}")
        for line in _overlay_human_next_steps(payload):
            print(line)
        print(f"Vault Exists: {'yes' if payload.get('vaultExists') else 'no'}")
        print("Accepted Assets: BNB, USDT")
        permission_summary = payload.get("permissionSummary")
        if isinstance(permission_summary, dict):
            print(f"Vault Authority: {permission_summary.get('vaultAuthority')}")
            print(f"Vault Executor: {permission_summary.get('vaultExecutor')}")
            print(f"Bootstrap Signer: {permission_summary.get('bootstrapSigner')}")
            if permission_summary.get("allowedTokenAddresses"):
                print(
                    "Allowed Tokens: "
                    + ", ".join(
                        cast(list[str], permission_summary["allowedTokenAddresses"])
                    )
                )
            if permission_summary.get("allowedRecipients"):
                print(
                    "Allowed Recipients: "
                    + ", ".join(
                        cast(list[str], permission_summary["allowedRecipients"])
                    )
                )
        return 0

    accepted_assets = ", ".join(details.accepted_assets)
    print(f"Mode: {payload['mode']}")
    if payload.get("activeRoute") is not None:
        print(f"Active Route: {payload.get('activeRoute')}")
    if payload.get("routePurpose") is not None:
        print(f"Route Purpose: {payload.get('routePurpose')}")
    print(f"Funding Address: {payload['fundingAddress']}")
    print(f"Signer Address: {payload['signerAddress']}")
    print(f"Chain: {payload['chain']}")
    print(f"Accepted Assets: {accepted_assets}")
    print(f"BNB Balance (wei): {payload['bnbBalanceWei']}")
    print(f"USDT Balance (wei): {payload['usdtBalanceWei']}")
    return 0


def _handle_continue_funding(args: argparse.Namespace) -> int:
    try:
        result = _load_funding_service().continue_funding(
            tx_hash=args.tx_hash,
            confirmations=args.confirmations,
            block_number=args.block_number,
            block_hash=args.block_hash,
        )
    except (ConfigError, MandatedVaultMcpError) as error:
        return _emit_error(args, error)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    session = cast(dict[str, Any], result.get("session", {}))
    next_step = cast(dict[str, Any], result.get("nextStep", {}))
    task = cast(dict[str, Any], next_step.get("task", {}))
    print(f"Session ID: {session.get('sessionId')}")
    print(f"Session Status: {session.get('status')}")
    print(f"Current Step: {session.get('currentStep')}")
    print(f"Next Task Kind: {task.get('kind')}")
    return 0


def _handle_continue_follow_up(args: argparse.Namespace) -> int:
    try:
        output = json.loads(args.output_json) if args.output_json else None
        result = _load_funding_service().continue_follow_up(
            reference_type=args.reference_type,
            reference_value=args.reference_value,
            status=args.status,
            output=output,
        )
    except (ConfigError, MandatedVaultMcpError, json.JSONDecodeError) as error:
        return _emit_error(args, error)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    session = cast(dict[str, Any], result.get("session", {}))
    follow_up = cast(dict[str, Any], result.get("followUpActionResult", {}))
    print(f"Session ID: {session.get('sessionId')}")
    print(f"Session Status: {session.get('status')}")
    print(f"Follow-Up Status: {follow_up.get('status')}")
    return 0


def _overlay_human_next_steps(payload: dict[str, Any]) -> list[str]:
    orchestration = payload.get("fundingOrchestration")
    if not isinstance(orchestration, dict):
        return []

    funding_target = orchestration.get("fundingTarget")
    if not isinstance(funding_target, dict):
        funding_target = {}

    next_step = orchestration.get("fundingNextStep")
    if not isinstance(next_step, dict):
        next_step = {}
    task = next_step.get("task")
    if not isinstance(task, dict):
        task = {}

    lines: list[str] = []
    current_balance = funding_target.get("currentBalanceRaw")
    required_amount = funding_target.get("requiredAmountRaw")
    shortfall = funding_target.get("fundingShortfallRaw")
    next_step_summary = task.get("summary")
    shortfall_text = str(shortfall) if shortfall is not None else None
    required_amount_text = str(required_amount) if required_amount is not None else None

    if current_balance is not None:
        lines.append(f"Current USDT Balance: {current_balance}")
    if required_amount is not None:
        lines.append(f"Required Top-Up: {required_amount}")
    if shortfall is not None and shortfall_text not in {"", "0"}:
        lines.append(f"Shortfall: {shortfall}")
    if shortfall_text == "0" or required_amount_text == "0":
        lines.append("Next Step: No additional funding required")
    elif next_step_summary is not None:
        lines.append(f"Next Step: {next_step_summary}")

    return lines


def _handle_bootstrap_vault(args: argparse.Namespace) -> int:
    try:
        snapshot = _load_manager().bootstrap_vault(confirm=args.confirm)
    except (ConfigError, MandatedVaultMcpError) as error:
        return _emit_error(args, error)

    payload = snapshot.to_dict()

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Mode: {payload['mode']}")
    print(f"Chain: {payload['chain']} ({payload['chainId']})")
    print(f"Factory: {payload['factory']}")
    print(f"Signer Address: {payload['signerAddress']}")
    print(f"Predicted Vault: {payload['predictedVault']}")
    print(f"Deployment Status: {payload['deploymentStatus']}")
    print(
        f"Confirmation Required: {'yes' if payload['confirmationRequired'] else 'no'}"
    )
    tx_summary = payload.get("txSummary")
    if isinstance(tx_summary, dict):
        print(f"Tx To: {tx_summary.get('to')}")
        print(f"Tx Value: {tx_summary.get('value')}")
        print(f"Tx Gas: {tx_summary.get('gas')}")
    if args.confirm:
        print(f"Deployed Vault: {payload['deployedVault']}")
        env_block = payload.get("envBlock")
        if env_block:
            print("Manual Env Block:")
            print(env_block)
    else:
        print(
            "Run `predictclaw wallet bootstrap-vault --confirm --json` to broadcast. Copy the returned env block manually if you want to update .env."
        )
    return 0


def _handle_redeem_vault(args: argparse.Namespace) -> int:
    if not args.preview and not args.confirm:
        args.preview = True
    if args.confirm:
        print(
            "wallet redeem-vault is currently preview-only; run with --json to inspect redeemability before any future confirm path is enabled."
        )
        return 1

    try:
        preview = _load_funding_service().preview_vault_redeem(
            share_token=args.share_token,
            holder=args.holder,
            redeem_all=args.all,
        )
    except ConfigError as error:
        return _emit_error(args, error)

    payload = preview.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Chain: {payload['chain']} ({payload['chainId']})")
    print(f"Share Token: {payload['shareToken']}")
    print(f"Holder: {payload['holder']}")
    metadata = payload.get("shareTokenMetadata", {})
    if isinstance(metadata, dict):
        print(f"Share Token Symbol: {metadata.get('symbol')}")
        print(f"Share Token Name: {metadata.get('name')}")
    underlying = payload.get("underlyingAsset", {})
    if isinstance(underlying, dict):
        print(
            f"Underlying Asset: {underlying.get('address')} ({underlying.get('symbol')})"
        )
    print(f"Share Balance (wei): {payload['shareBalanceWei']}")
    print(f"Requested Shares (wei): {payload['requestedSharesWei']}")
    if payload.get("previewRedeemWei") is not None:
        print(f"Preview Redeem (wei): {payload['previewRedeemWei']}")
    if payload.get("maxRedeemWei") is not None:
        print(f"Max Redeem (wei): {payload['maxRedeemWei']}")
    if payload.get("maxWithdrawWei") is not None:
        print(f"Max Withdraw (wei): {payload['maxWithdrawWei']}")
    print(f"Redeemable Now: {'yes' if payload['redeemableNow'] else 'no'}")
    if payload.get("blockingReason") is not None:
        print(f"Blocking Reason: {payload['blockingReason']}")
    contract_error = payload.get("contractError")
    if isinstance(contract_error, dict):
        print(f"Contract Error: {contract_error.get('code')}")
    print(f"Next Action: {payload['recommendedNextAction']}")
    return 0


def _handle_withdraw(args: argparse.Namespace) -> int:
    try:
        result = _load_funding_service().withdraw(
            args.asset,
            args.amount,
            args.to,
            withdraw_all=args.all,
        )
    except ConfigError as error:
        return _emit_error(args, error)

    payload = result.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
        return 0

    print(f"Asset: {payload['asset']}")
    print(f"Amount (wei): {payload['amountWei']}")
    print(f"Destination: {payload['destination']}")
    print(f"Result: {payload['result']}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
