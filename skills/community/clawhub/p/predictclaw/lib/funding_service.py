from __future__ import annotations

import asyncio
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Protocol, cast

from predict_sdk._internal.contracts import make_contract
from predict_sdk.abis import KERNEL_ABI
from web3 import Web3

from .config import (
    ConfigError,
    PredictConfig,
    WalletMode,
    mandated_vault_v1_unsupported_error,
)
from .mandated_mcp_bridge import MandatedVaultMcpBridge
from .session_storage import FundAndActionSessionRecord, SessionStorage
from .wallet_manager import (
    FixtureWalletSdk,
    MandatedVaultBridgeProtocol,
    PredictSdkWallet,
    VaultPermissionSummary,
    _overlay_address_guidance_payload,
    _build_mandated_permission_summary,
    WalletSdkProtocol,
    build_vault_to_predict_account_orchestration,
    load_wallet_bnb_balance_wei,
    load_wallet_usdt_balance_wei,
    make_wallet_sdk,
    resolve_mandated_vault,
)


TOKEN_DECIMALS = {"usdt": 18, "bnb": 18}
MIN_GAS_HEADROOM_WEI = 100_000_000_000_000
RPC_ENV_CANDIDATES = {
    56: ("BSC_MAINNET_RPC_URL", "BSC_RPC_URL", "ERC_MANDATED_RPC_URL"),
    97: ("BSC_TESTNET_RPC_URL", "BSC_RPC_URL", "ERC_MANDATED_RPC_URL"),
}
PUBLIC_RPC_FALLBACKS = {
    56: "https://bsc-dataseed.bnbchain.org/",
    97: "https://data-seed-prebsc-1-s1.bnbchain.org:8545/",
}
CUSTOM_ERROR_DATA_RE = re.compile(r"0x[a-fA-F0-9]{8,}")


def _utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _model_dump(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return cast(dict[str, Any], value.model_dump(by_alias=True))
    return cast(dict[str, Any], value)


ERC20_METADATA_ABI = [
    {
        "stateMutability": "view",
        "type": "function",
        "name": "name",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "symbol",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "decimals",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint8"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "balanceOf",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
    },
]

ERC4626_PREVIEW_ABI = ERC20_METADATA_ABI + [
    {
        "stateMutability": "view",
        "type": "function",
        "name": "asset",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "totalAssets",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "maxRedeem",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "maxWithdraw",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "previewRedeem",
        "inputs": [{"name": "shares", "type": "uint256"}],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        "stateMutability": "nonpayable",
        "type": "function",
        "name": "redeem",
        "inputs": [
            {"name": "shares", "type": "uint256"},
            {"name": "receiver", "type": "address"},
            {"name": "owner", "type": "address"},
        ],
        "outputs": [{"name": "", "type": "uint256"}],
    },
]


@dataclass
class DepositDetails:
    mode: str
    funding_address: str
    signer_address: str
    chain: str
    accepted_assets: list[str]
    bnb_balance_wei: int
    usdt_balance_wei: int
    active_route: str | None = None
    route_purpose: str | None = None
    vault_address_source: str | None = None
    vault_exists: bool | None = None
    create_vault_preparation: dict[str, object] | None = None
    bootstrap_preview: dict[str, object] | None = None
    permission_summary: dict[str, object] | None = None
    session_scope: str | None = None
    session_binding: dict[str, object] | None = None
    funding_route: str | None = None
    predict_account_address: str | None = None
    trade_signer_address: str | None = None
    vault_address: str | None = None
    funding_orchestration: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "mode": self.mode,
            "fundingAddress": self.funding_address,
            "signerAddress": self.signer_address,
            "chain": self.chain,
            "acceptedAssets": self.accepted_assets,
            "bnbBalanceWei": self.bnb_balance_wei,
            "usdtBalanceWei": self.usdt_balance_wei,
        }
        if self.active_route is not None:
            payload["activeRoute"] = self.active_route
        if self.route_purpose is not None:
            payload["routePurpose"] = self.route_purpose
        if self.vault_address_source is not None:
            payload["vaultAddressSource"] = self.vault_address_source
        if self.vault_exists is not None:
            payload["vaultExists"] = self.vault_exists
        if self.vault_exists is not None:
            payload["createVaultPreparation"] = self.create_vault_preparation
        elif self.create_vault_preparation is not None:
            payload["createVaultPreparation"] = self.create_vault_preparation
        if self.bootstrap_preview is not None:
            payload["bootstrapPreview"] = self.bootstrap_preview
        if self.permission_summary is not None:
            payload["permissionSummary"] = self.permission_summary
        if self.session_scope is not None:
            payload["sessionScope"] = self.session_scope
        if self.session_binding is not None:
            payload["sessionBinding"] = self.session_binding
        if self.funding_route is not None:
            payload["fundingRoute"] = self.funding_route
            payload["predictAccountAddress"] = self.predict_account_address
            payload["tradeSignerAddress"] = self.trade_signer_address
            payload["vaultAddress"] = self.vault_address
            payload["fundingOrchestration"] = self.funding_orchestration
            payload.update(
                _overlay_address_guidance_payload(
                    predict_account_address=self.predict_account_address,
                    vault_address=self.vault_address,
                )
            )
        return payload


@dataclass
class WithdrawalResult:
    asset: str
    amount_wei: int
    destination: str
    result: Any

    def to_dict(self) -> dict[str, object]:
        return {
            "asset": self.asset,
            "amountWei": self.amount_wei,
            "destination": self.destination,
            "result": self.result,
        }


@dataclass
class VaultRedeemPreview:
    chain_id: int
    chain: str
    share_token: str
    holder: str
    share_token_name: str | None
    share_token_symbol: str | None
    share_token_decimals: int | None
    underlying_asset: str | None
    underlying_symbol: str | None
    underlying_decimals: int | None
    share_balance_wei: int
    requested_shares_wei: int
    total_assets_wei: int | None
    preview_redeem_wei: int | None
    max_redeem_wei: int | None
    max_withdraw_wei: int | None
    redeemable_now: bool
    blocking_reason: str | None
    contract_error: dict[str, object] | None
    recommended_next_action: str
    configured_roles: dict[str, str | None]
    holder_role_matches: dict[str, bool]

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "chainId": self.chain_id,
            "chain": self.chain,
            "shareToken": self.share_token,
            "holder": self.holder,
            "shareBalanceWei": self.share_balance_wei,
            "requestedSharesWei": self.requested_shares_wei,
            "redeemableNow": self.redeemable_now,
            "recommendedNextAction": self.recommended_next_action,
            "configuredRoles": self.configured_roles,
            "holderRoleMatches": self.holder_role_matches,
            "shareTokenMetadata": {
                "name": self.share_token_name,
                "symbol": self.share_token_symbol,
                "decimals": self.share_token_decimals,
            },
        }
        if self.underlying_asset is not None:
            payload["underlyingAsset"] = {
                "address": self.underlying_asset,
                "symbol": self.underlying_symbol,
                "decimals": self.underlying_decimals,
            }
        if self.total_assets_wei is not None:
            payload["totalAssetsWei"] = self.total_assets_wei
        if self.preview_redeem_wei is not None:
            payload["previewRedeemWei"] = self.preview_redeem_wei
        if self.max_redeem_wei is not None:
            payload["maxRedeemWei"] = self.max_redeem_wei
        if self.max_withdraw_wei is not None:
            payload["maxWithdrawWei"] = self.max_withdraw_wei
        if self.blocking_reason is not None:
            payload["blockingReason"] = self.blocking_reason
        if self.contract_error is not None:
            payload["contractError"] = self.contract_error
        return payload


class TransferCapableWallet(Protocol):
    @property
    def mode(self) -> object: ...

    @property
    def signer_address(self) -> str: ...

    @property
    def funding_address(self) -> str: ...

    @property
    def chain_name(self) -> str: ...

    def get_bnb_balance_wei(self) -> int: ...

    def get_usdt_balance_wei(self) -> int: ...


class FundingService:
    def __init__(
        self,
        config: PredictConfig,
        *,
        sdk_factory: Callable[[PredictConfig], TransferCapableWallet] = make_wallet_sdk,
        bridge_factory: Callable[
            [PredictConfig], MandatedVaultBridgeProtocol
        ] = MandatedVaultMcpBridge,
    ) -> None:
        self._config = config
        self._sdk_factory = sdk_factory
        self._bridge_factory = bridge_factory

    def get_deposit_details(self) -> DepositDetails:
        if self._config.wallet_mode.value == "mandated-vault":
            return self._get_mandated_deposit_details()

        sdk = self._require_sdk()
        if (
            self._config.wallet_mode == WalletMode.PREDICT_ACCOUNT
            and self._config.has_mandated_config_input
        ):
            return self._get_predict_account_overlay_deposit_details(sdk)

        return DepositDetails(
            mode=str(getattr(sdk.mode, "value", sdk.mode)),
            funding_address=sdk.funding_address,
            signer_address=sdk.signer_address,
            chain=sdk.chain_name,
            accepted_assets=["BNB", "USDT"],
            bnb_balance_wei=sdk.get_bnb_balance_wei(),
            usdt_balance_wei=sdk.get_usdt_balance_wei(),
        )

    def continue_funding(
        self,
        *,
        tx_hash: str,
        confirmations: int = 1,
        block_number: str | None = None,
        block_hash: str | None = None,
    ) -> dict[str, object]:
        record = self._require_active_session()
        task = cast(dict[str, Any], record.funding_next_step.get("task", {}))
        funding_plan = cast(
            dict[str, Any] | None,
            task.get("fundingPlan")
            or record.funding_plan
            or cast(
                dict[str, Any], record.funding_session.get("fundAndActionPlan", {})
            ).get("fundingPlan"),
        )
        if task.get("kind") not in {"submitFunding", "pollFundingResult"}:
            raise ConfigError(
                "Active session is not waiting for a funding continuation step."
            )
        if not isinstance(funding_plan, dict):
            raise ConfigError(
                "Active session did not expose a funding plan for continuation."
            )

        bridge = self._bridge_factory(self._config)

        async def _run_and_close() -> dict[str, object]:
            await bridge.connect()
            try:
                updated_at = _utc_timestamp()
                transfer = await bridge.create_vault_asset_transfer_result(
                    asset_transfer_plan=funding_plan,
                    status="confirmed",
                    updated_at=updated_at,
                    submitted_at=updated_at,
                    completed_at=updated_at,
                    attempt=1,
                    chain_id=int(self._config.chain_id),
                    tx_hash=tx_hash,
                    receipt={
                        "blockNumber": block_number,
                        "blockHash": block_hash,
                        "confirmations": confirmations,
                    },
                    output={"status": "ok"},
                )
                transfer_payload = _model_dump(transfer.assetTransferResult)
                applied = await bridge.apply_agent_fund_and_action_session_event(
                    session=record.funding_session,
                    event={
                        "type": "fundingConfirmed",
                        "updatedAt": updated_at,
                        "assetTransferResult": transfer_payload,
                    },
                )
                session_payload = _model_dump(applied.session)
                next_step = await bridge.next_agent_fund_and_action_session_step(
                    session=session_payload
                )
                next_step_payload = _model_dump(next_step)
                record.funding_session = session_payload
                record.funding_next_step = next_step_payload
                record.updated_at = updated_at
                SessionStorage(self._config.storage_dir).upsert(record)
                return {
                    "session": session_payload,
                    "assetTransferResult": transfer_payload,
                    "nextStep": next_step_payload,
                    "sessionBinding": record.binding_payload(),
                }
            finally:
                await bridge.close()

        return asyncio.run(_run_and_close())

    def continue_follow_up(
        self,
        *,
        reference_type: str,
        reference_value: str,
        status: str = "succeeded",
        output: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        record = self._require_active_session()
        task = cast(dict[str, Any], record.funding_next_step.get("task", {}))
        follow_up_action_plan = cast(
            dict[str, Any] | None,
            task.get("followUpActionPlan")
            or cast(
                dict[str, Any], record.funding_session.get("fundAndActionPlan", {})
            ).get("followUpActionPlan"),
        )
        if task.get("kind") not in {"submitFollowUp", "pollFollowUpResult"}:
            raise ConfigError(
                "Active session is not waiting for a follow-up continuation step."
            )
        if not isinstance(follow_up_action_plan, dict):
            raise ConfigError(
                "Active session did not expose a follow-up action plan for continuation."
            )

        bridge = self._bridge_factory(self._config)

        async def _run_and_close() -> dict[str, object]:
            await bridge.connect()
            try:
                updated_at = _utc_timestamp()
                follow_up_result = await bridge.create_agent_follow_up_action_result(
                    follow_up_action_plan=follow_up_action_plan,
                    status=status,
                    updated_at=updated_at,
                    completed_at=updated_at,
                    attempt=1,
                    reference={"type": reference_type, "value": reference_value},
                    output=output,
                )
                follow_up_payload = _model_dump(follow_up_result.followUpActionResult)
                applied = await bridge.apply_agent_fund_and_action_session_event(
                    session=record.funding_session,
                    event={
                        "type": "followUpResultReceived",
                        "followUpActionResult": follow_up_payload,
                    },
                )
                session_payload = _model_dump(applied.session)
                record.funding_session = session_payload
                record.funding_next_step = {"task": {"kind": "completed"}}
                record.updated_at = updated_at
                SessionStorage(self._config.storage_dir).upsert(record)
                return {
                    "session": session_payload,
                    "followUpActionResult": follow_up_payload,
                    "sessionBinding": record.binding_payload(),
                }
            finally:
                await bridge.close()

        return asyncio.run(_run_and_close())

    def _require_active_session(self) -> FundAndActionSessionRecord:
        predict_account_address = self._config.predict_account_address
        record = SessionStorage(self._config.storage_dir).get_active_session(
            predict_account_address=predict_account_address
        )
        if record is None:
            raise ConfigError("No active overlay funding session is available.")
        return record

    def _get_predict_account_overlay_deposit_details(
        self, sdk: TransferCapableWallet
    ) -> DepositDetails:
        bridge = self._bridge_factory(self._config)

        async def _load_and_close() -> DepositDetails:
            await bridge.connect()
            try:
                bnb_balance = await load_wallet_bnb_balance_wei(
                    cast(WalletSdkProtocol, sdk)
                )
                usdt_balance = await load_wallet_usdt_balance_wei(
                    cast(WalletSdkProtocol, sdk)
                )
                orchestration = await build_vault_to_predict_account_orchestration(
                    self._config,
                    bridge,
                    predict_account_address=sdk.funding_address,
                    trade_signer_address=sdk.signer_address,
                    current_usdt_balance_wei=usdt_balance,
                    wallet_sdk=sdk,
                )
                resolved_authority = cast(
                    str | None,
                    orchestration.account_context.get("authority"),
                )
                resolved_asset = cast(
                    str | None,
                    orchestration.funding_target.get("tokenAddress"),
                )
                session_record = SessionStorage(
                    self._config.storage_dir
                ).get_active_session(predict_account_address=sdk.funding_address)
                orchestration_payload = orchestration.to_dict()
                session_scope: str | None = None
                session_binding: dict[str, object] | None = None
                if session_record is not None:
                    session_scope = session_record.session_scope
                    session_binding = session_record.binding_payload()
                    orchestration_payload["fundingPlan"] = session_record.funding_plan
                    orchestration_payload["fundingSession"] = (
                        session_record.funding_session
                    )
                    orchestration_payload["fundingNextStep"] = (
                        session_record.funding_next_step
                    )
                return DepositDetails(
                    mode=str(getattr(sdk.mode, "value", sdk.mode)),
                    funding_address=orchestration.vault_address,
                    signer_address=sdk.signer_address,
                    chain=sdk.chain_name,
                    accepted_assets=["BNB", "USDT"],
                    bnb_balance_wei=bnb_balance,
                    usdt_balance_wei=usdt_balance,
                    active_route="vault-to-predict-account",
                    route_purpose="predict-account-top-up-and-trading",
                    vault_address_source=orchestration.vault_address_source,
                    vault_exists=orchestration.vault_exists,
                    funding_route=orchestration.funding_route,
                    predict_account_address=orchestration.predict_account_address,
                    trade_signer_address=orchestration.trade_signer_address,
                    vault_address=orchestration.vault_address,
                    funding_orchestration=orchestration_payload,
                    permission_summary=_build_mandated_permission_summary(
                        self._config,
                        permission_model="vault-to-predict-account-overlay",
                        vault_authority=resolved_authority,
                        underlying_asset=resolved_asset,
                        allowed_token_addresses=cast(
                            list[str] | None,
                            orchestration.funding_policy.get("allowedTokenAddresses"),
                        ),
                        allowed_recipients=cast(
                            list[str] | None,
                            orchestration.funding_policy.get("allowedRecipients"),
                        ),
                        max_amount_per_tx=cast(
                            str | None,
                            orchestration.funding_policy.get("maxAmountPerTx"),
                        ),
                        max_amount_per_window=cast(
                            str | None,
                            orchestration.funding_policy.get("maxAmountPerWindow"),
                        ),
                        window_seconds=cast(
                            int | None,
                            orchestration.funding_policy.get("windowSeconds"),
                        ),
                    ).to_dict(),
                    session_scope=session_scope,
                    session_binding=session_binding,
                )
            finally:
                await bridge.close()

        return asyncio.run(_load_and_close())

    def _get_mandated_deposit_details(self) -> DepositDetails:
        bridge = self._bridge_factory(self._config)

        async def _load_and_close() -> DepositDetails:
            await bridge.connect()
            try:
                resolution = await resolve_mandated_vault(
                    self._config,
                    bridge,
                    include_create_prepare=True,
                )
                preparation: dict[str, object] | None = None
                if (
                    not resolution.vault_deployed
                    and resolution.create_vault_prepare is not None
                    and resolution.bootstrap_preview is None
                ):
                    tx = resolution.create_vault_prepare.txRequest
                    preparation = {
                        "predictedVault": resolution.create_vault_prepare.predictedVault,
                        "txSummary": {
                            "from": tx.from_address,
                            "to": tx.to,
                            "data": tx.data,
                            "value": tx.value,
                            "gas": tx.gas,
                        },
                        "broadcast": "manual-only",
                    }
                bootstrap_preview = (
                    resolution.bootstrap_preview.to_dict()
                    if resolution.bootstrap_preview is not None
                    else None
                )

                return DepositDetails(
                    mode=self._config.wallet_mode.value,
                    funding_address=resolution.vault_address,
                    signer_address=self._config.mandated_vault_authority
                    or "not-required",
                    chain=(
                        "BNB Mainnet"
                        if self._config.env.value == "mainnet"
                        else "BNB Testnet"
                    ),
                    accepted_assets=["BNB", "USDT"],
                    bnb_balance_wei=0,
                    usdt_balance_wei=0,
                    active_route="vault-control-plane",
                    route_purpose="bootstrap-or-direct-vault-ops",
                    vault_address_source=resolution.vault_address_source,
                    vault_exists=resolution.vault_deployed,
                    create_vault_preparation=preparation,
                    bootstrap_preview=bootstrap_preview,
                    permission_summary=_build_mandated_permission_summary(
                        self._config,
                        permission_model="mandated-vault-v1",
                    ).to_dict(),
                )
            finally:
                await bridge.close()

        return asyncio.run(_load_and_close())

    def withdraw(
        self, asset: str, amount: str, destination: str, *, withdraw_all: bool = False
    ) -> WithdrawalResult:
        if self._config.wallet_mode == WalletMode.MANDATED_VAULT:
            raise mandated_vault_v1_unsupported_error("wallet withdraw")

        sdk = self._require_sdk()
        asset_key = asset.lower()
        if asset_key not in TOKEN_DECIMALS:
            raise ConfigError("Withdraw only supports BNB and USDT.")
        if not Web3.is_checksum_address(destination):
            raise ConfigError("Destination address must be a checksum address.")

        bnb_balance = sdk.get_bnb_balance_wei()
        usdt_balance = sdk.get_usdt_balance_wei()

        if withdraw_all:
            available = (
                usdt_balance
                if asset_key == "usdt"
                else max(bnb_balance - MIN_GAS_HEADROOM_WEI, 0)
            )
            amount_wei = available
        else:
            amount_wei = _parse_amount_to_wei(amount, TOKEN_DECIMALS[asset_key])

        if amount_wei <= 0:
            raise ConfigError("Withdrawal amount must be greater than zero.")
        if bnb_balance <= MIN_GAS_HEADROOM_WEI:
            raise ConfigError("Insufficient BNB gas headroom for withdrawal.")

        if asset_key == "usdt":
            if usdt_balance < amount_wei:
                raise ConfigError("Insufficient USDT balance for withdrawal.")
            result = _transfer_usdt(sdk, destination, amount_wei)
        else:
            if bnb_balance - MIN_GAS_HEADROOM_WEI < amount_wei:
                raise ConfigError(
                    "Insufficient BNB balance after reserving gas headroom."
                )
            result = _transfer_bnb(sdk, destination, amount_wei)

        return WithdrawalResult(
            asset=asset_key,
            amount_wei=amount_wei,
            destination=destination,
            result=result,
        )

    def preview_vault_redeem(
        self,
        *,
        share_token: str,
        holder: str | None = None,
        redeem_all: bool = False,
    ) -> VaultRedeemPreview:
        checksum_share_token = Web3.to_checksum_address(share_token)
        resolved_holder = _resolve_redeem_holder(self._config, holder)
        checksum_holder = Web3.to_checksum_address(resolved_holder)
        chain_id = self._config.mandated_chain_id or int(self._config.chain_id)
        chain_name = "BNB Mainnet" if chain_id == 56 else "BNB Testnet"
        rpc_url = _resolve_preview_rpc_url(chain_id)
        web3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 20}))
        share_contract = web3.eth.contract(
            address=checksum_share_token, abi=ERC4626_PREVIEW_ABI
        )

        share_token_name = cast(
            str | None, _safe_contract_call(share_contract.functions.name)
        )
        share_token_symbol = cast(
            str | None, _safe_contract_call(share_contract.functions.symbol)
        )
        share_token_decimals = cast(
            int | None, _safe_contract_call(share_contract.functions.decimals)
        )
        share_balance_wei = int(
            cast(int, share_contract.functions.balanceOf(checksum_holder).call())
        )
        underlying_asset = cast(
            str | None, _safe_contract_call(share_contract.functions.asset)
        )
        total_assets_wei = cast(
            int | None, _safe_contract_call(share_contract.functions.totalAssets)
        )
        max_redeem_wei = cast(
            int | None,
            _safe_contract_call(share_contract.functions.maxRedeem, checksum_holder),
        )
        max_withdraw_wei = cast(
            int | None,
            _safe_contract_call(share_contract.functions.maxWithdraw, checksum_holder),
        )
        requested_shares_wei = (
            share_balance_wei
            if redeem_all or max_redeem_wei is None
            else max_redeem_wei
        )
        preview_redeem_wei: int | None = None
        if requested_shares_wei > 0:
            preview_redeem_wei = cast(
                int | None,
                _safe_contract_call(
                    share_contract.functions.previewRedeem, requested_shares_wei
                ),
            )
        contract_error = None
        if requested_shares_wei > 0:
            contract_error = _simulate_redeem_call(
                web3=web3,
                share_contract=share_contract,
                holder=checksum_holder,
                requested_shares_wei=requested_shares_wei,
            )

        underlying_symbol = None
        underlying_decimals = None
        if underlying_asset is not None:
            underlying_contract = web3.eth.contract(
                address=Web3.to_checksum_address(underlying_asset),
                abi=ERC20_METADATA_ABI,
            )
            underlying_symbol = cast(
                str | None, _safe_contract_call(underlying_contract.functions.symbol)
            )
            underlying_decimals = cast(
                int | None, _safe_contract_call(underlying_contract.functions.decimals)
            )

        blocking_reason = _resolve_redeem_blocking_reason(
            share_balance_wei=share_balance_wei,
            requested_shares_wei=requested_shares_wei,
            max_redeem_wei=max_redeem_wei,
            contract_error=contract_error,
        )
        redeemable_now = blocking_reason is None
        recommended_next_action = _build_redeem_next_action(
            redeemable_now=redeemable_now,
            contract_error=contract_error,
        )
        configured_roles = {
            "vaultAuthority": self._config.mandated_vault_authority,
            "vaultExecutor": self._config.mandated_executor_address,
            "bootstrapSigner": self._config.mandated_bootstrap_signer_address,
        }
        holder_role_matches = {
            "vaultAuthority": checksum_holder.lower()
            == (self._config.mandated_vault_authority or "").lower(),
            "vaultExecutor": checksum_holder.lower()
            == (self._config.mandated_executor_address or "").lower(),
            "bootstrapSigner": checksum_holder.lower()
            == (self._config.mandated_bootstrap_signer_address or "").lower(),
        }
        return VaultRedeemPreview(
            chain_id=chain_id,
            chain=chain_name,
            share_token=checksum_share_token,
            holder=checksum_holder,
            share_token_name=share_token_name,
            share_token_symbol=share_token_symbol,
            share_token_decimals=share_token_decimals,
            underlying_asset=underlying_asset,
            underlying_symbol=underlying_symbol,
            underlying_decimals=underlying_decimals,
            share_balance_wei=share_balance_wei,
            requested_shares_wei=requested_shares_wei,
            total_assets_wei=total_assets_wei,
            preview_redeem_wei=preview_redeem_wei,
            max_redeem_wei=max_redeem_wei,
            max_withdraw_wei=max_withdraw_wei,
            redeemable_now=redeemable_now,
            blocking_reason=blocking_reason,
            contract_error=contract_error,
            recommended_next_action=recommended_next_action,
            configured_roles=configured_roles,
            holder_role_matches=holder_role_matches,
        )

    def _require_sdk(self) -> TransferCapableWallet:
        if self._config.auth_signer_address is None:
            raise ConfigError(
                "Wallet actions require signer configuration. Set PREDICT_EOA_PRIVATE_KEY or both PREDICT_ACCOUNT_ADDRESS and PREDICT_PRIVY_PRIVATE_KEY."
            )
        return self._sdk_factory(self._config)


def _parse_amount_to_wei(raw_amount: str, decimals: int) -> int:
    try:
        amount = Decimal(raw_amount)
    except InvalidOperation as error:
        raise ConfigError("Withdrawal amount must be numeric.") from error

    if amount <= 0:
        return 0
    scale = Decimal(10) ** decimals
    return int(amount * scale)


def _resolve_preview_rpc_url(chain_id: int) -> str:
    for env_name in RPC_ENV_CANDIDATES.get(chain_id, ("ERC_MANDATED_RPC_URL",)):
        value = os.getenv(env_name)
        if value:
            return value
    fallback = PUBLIC_RPC_FALLBACKS.get(chain_id)
    if fallback is None:
        raise ConfigError(f"No RPC URL configured for chainId {chain_id}.")
    return fallback


def _resolve_redeem_holder(config: PredictConfig, holder: str | None) -> str:
    if holder is not None:
        return holder
    for candidate in (
        config.mandated_executor_address,
        config.mandated_bootstrap_signer_address,
        config.auth_signer_address,
    ):
        if candidate:
            return candidate
    raise ConfigError(
        "Redeem preview requires --holder or a configured executor/bootstrap/auth signer address."
    )


def _safe_contract_call(function_factory: Any, *args: Any) -> Any:
    try:
        if args:
            return function_factory(*args).call()
        return function_factory().call()
    except Exception:
        return None


def _extract_custom_error_data(error: Exception) -> str | None:
    matches = CUSTOM_ERROR_DATA_RE.findall(str(error))
    for match in matches:
        if len(match) >= 10:
            return match
    return None


def _decode_custom_error(error_data: str | None) -> dict[str, object] | None:
    if not error_data or len(error_data) < 10:
        return None
    selector = error_data[2:10].lower()
    body = bytes.fromhex(error_data[10:])
    if selector == "b94abeec":
        payload: dict[str, object] = {"code": "ERC4626ExceededMaxRedeem"}
        if len(body) >= 96:
            owner = "0x" + body[12:32].hex()
            shares = int.from_bytes(body[32:64], "big")
            max_redeem = int.from_bytes(body[64:96], "big")
            payload.update(
                {
                    "owner": Web3.to_checksum_address(owner),
                    "requestedSharesWei": shares,
                    "maxRedeemWei": max_redeem,
                }
            )
        return payload
    if selector == "fe9cceec":
        payload = {"code": "ERC4626ExceededMaxWithdraw"}
        if len(body) >= 96:
            owner = "0x" + body[12:32].hex()
            assets = int.from_bytes(body[32:64], "big")
            max_withdraw = int.from_bytes(body[64:96], "big")
            payload.update(
                {
                    "owner": Web3.to_checksum_address(owner),
                    "requestedAssetsWei": assets,
                    "maxWithdrawWei": max_withdraw,
                }
            )
        return payload
    return {"code": "UNKNOWN_CUSTOM_ERROR", "data": error_data}


def _simulate_redeem_call(
    *,
    web3: Web3,
    share_contract: Any,
    holder: str,
    requested_shares_wei: int,
) -> dict[str, object] | None:
    if requested_shares_wei <= 0:
        return None
    try:
        share_contract.functions.redeem(
            requested_shares_wei,
            holder,
            holder,
        ).call({"from": holder})
        return None
    except Exception as error:
        decoded = _decode_custom_error(
            _extract_custom_error_data(cast(Exception, error))
        )
        if decoded is not None:
            return decoded
        return {
            "code": type(error).__name__,
            "message": str(error),
        }


def _resolve_redeem_blocking_reason(
    *,
    share_balance_wei: int,
    requested_shares_wei: int,
    max_redeem_wei: int | None,
    contract_error: dict[str, object] | None,
) -> str | None:
    if share_balance_wei <= 0:
        return "no-shares"
    if requested_shares_wei <= 0:
        return "no-requested-shares"
    if contract_error is not None:
        code = contract_error.get("code")
        if code == "ERC4626ExceededMaxRedeem":
            return "erc4626-max-redeem-blocked"
        if code == "ERC4626ExceededMaxWithdraw":
            return "erc4626-max-withdraw-blocked"
        return "redeem-call-blocked"
    if max_redeem_wei is not None and requested_shares_wei > max_redeem_wei:
        return "requested-shares-exceed-max-redeem"
    return None


def _build_redeem_next_action(
    *, redeemable_now: bool, contract_error: dict[str, object] | None
) -> str:
    if redeemable_now:
        return "Redeem preview succeeded; a future confirm path can use this amount if execution support is added."
    code = contract_error.get("code") if contract_error is not None else None
    if code == "ERC4626ExceededMaxRedeem":
        return "Vault shares are currently not redeemable through a direct full redeem call. Check cooldown, queue, unlock, or vault-specific withdrawal rules before attempting a real transaction."
    if code == "ERC4626ExceededMaxWithdraw":
        return "Vault withdrawals are currently capped below the requested amount. Inspect vault-specific withdrawal limits before attempting a real transaction."
    return "Redeem preview is blocked. Inspect the contract error and vault rules before attempting any real redeem transaction."


def _transfer_usdt(
    sdk: TransferCapableWallet, destination: str, amount_wei: int
) -> Any:
    if hasattr(sdk, "transfer_usdt"):
        return cast(Any, getattr(sdk, "transfer_usdt"))(destination, amount_wei)

    if isinstance(sdk, FixtureWalletSdk):
        return {"success": True, "txHash": "0xfixture-usdt"}

    if not isinstance(sdk, PredictSdkWallet):
        raise ConfigError("Wallet SDK does not support USDT withdrawals.")

    builder = sdk._builder
    contracts = builder.contracts
    if contracts is None:
        raise ConfigError("USDT withdrawal requires initialized predict.fun contracts.")

    checksum_to = Web3.to_checksum_address(destination)
    if sdk.mode.value == "predict-account":
        encoded = contracts.usdt.encode_abi(
            abi_element_identifier="transfer",
            args=[checksum_to, amount_wei],
        )
        calldata = builder._encode_execution_calldata(
            contracts.usdt.address, encoded, value=0
        )
        web3 = getattr(builder, "_web3", None)
        predict_account = getattr(builder, "_predict_account", None)
        execution_mode = getattr(builder, "_execution_mode", None)
        if web3 is None or predict_account is None or execution_mode is None:
            raise ConfigError(
                "Predict Account withdrawal requires initialized Kernel execution state."
            )
        kernel = make_contract(web3, predict_account, KERNEL_ABI)
        return builder._run_async(
            builder._handle_transaction_async(
                kernel, "execute", execution_mode, calldata
            )
        )

    return builder._run_async(
        builder._handle_transaction_async(
            contracts.usdt, "transfer", checksum_to, amount_wei
        )
    )


def _transfer_bnb(sdk: TransferCapableWallet, destination: str, amount_wei: int) -> Any:
    if hasattr(sdk, "transfer_bnb"):
        return cast(Any, getattr(sdk, "transfer_bnb"))(destination, amount_wei)

    if isinstance(sdk, FixtureWalletSdk):
        return {"success": True, "txHash": "0xfixture-bnb"}

    if not isinstance(sdk, PredictSdkWallet):
        raise ConfigError("Wallet SDK does not support BNB withdrawals.")

    builder = sdk._builder
    checksum_to = Web3.to_checksum_address(destination)
    if sdk.mode.value == "predict-account":
        web3 = getattr(builder, "_web3", None)
        predict_account = getattr(builder, "_predict_account", None)
        execution_mode = getattr(builder, "_execution_mode", None)
        if web3 is None or predict_account is None or execution_mode is None:
            raise ConfigError(
                "Predict Account withdrawal requires initialized Kernel execution state."
            )
        calldata = builder._encode_execution_calldata(
            checksum_to, "0x", value=amount_wei
        )
        kernel = make_contract(web3, predict_account, KERNEL_ABI)
        return builder._run_async(
            builder._handle_transaction_async(
                kernel, "execute", execution_mode, calldata
            )
        )

    web3 = getattr(builder, "_web3", None)
    signer = getattr(builder, "_signer", None)
    if web3 is None or signer is None or not sdk._config.private_key_value:
        raise ConfigError("EOA BNB withdrawal requires initialized signer state.")

    tx = {
        "from": signer.address,
        "to": checksum_to,
        "value": amount_wei,
        "nonce": web3.eth.get_transaction_count(signer.address),
        "gasPrice": web3.eth.gas_price,
        "chainId": web3.eth.chain_id,
    }
    estimated_gas = web3.eth.estimate_gas(tx)
    tx["gas"] = (estimated_gas * 125) // 100
    signed = web3.eth.account.sign_transaction(tx, sdk._config.private_key_value)
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return {"success": True, "txHash": tx_hash.hex(), "receipt": dict(receipt)}
