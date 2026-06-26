from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable, Mapping, Protocol, cast

from eth_abi.abi import encode as abi_encode
from eth_account import Account
from pydantic import SecretStr
from predict_sdk import OrderBuilder, OrderBuilderOptions
from predict_sdk._internal.contracts import (
    get_conditional_tokens_contract,
    get_exchange_contract,
    get_neg_risk_adapter_contract,
)
from web3 import Web3

from .config import (
    ConfigError,
    PredictConfig,
    RuntimeEnv,
    WalletMode,
    mandated_vault_v1_unsupported_error,
)
from .mandated_mcp_bridge import (
    FactoryCreateVaultPrepareResult,
    MandatedVaultMcpBridge,
    MandatedVaultMcpError,
    VaultBootstrapResult,
    VaultHealthCheckResult,
)
from .session_storage import SessionStorage


OVERLAY_RPC_ENV_CANDIDATES = {
    56: ("BSC_MAINNET_RPC_URL", "BSC_RPC_URL", "ERC_MANDATED_RPC_URL"),
    97: ("BSC_TESTNET_RPC_URL", "BSC_RPC_URL", "ERC_MANDATED_RPC_URL"),
}
OVERLAY_PUBLIC_RPC_FALLBACKS = {
    56: "https://bsc-dataseed.bnbchain.org/",
    97: "https://data-seed-prebsc-1-s1.bnbchain.org:8545/",
}
ERC4626_ASSET_ABI = [
    {
        "stateMutability": "view",
        "type": "function",
        "name": "asset",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    }
]


@dataclass
class ApprovalSnapshot:
    standard_exchange_approval: bool
    standard_exchange_allowance: bool
    standard_neg_risk_exchange_approval: bool
    standard_neg_risk_exchange_allowance: bool
    standard_neg_risk_adapter_approval: bool
    yield_exchange_approval: bool
    yield_exchange_allowance: bool
    yield_neg_risk_exchange_approval: bool
    yield_neg_risk_exchange_allowance: bool
    yield_neg_risk_adapter_approval: bool

    @property
    def standard_ready(self) -> bool:
        return all(
            [
                self.standard_exchange_approval,
                self.standard_exchange_allowance,
                self.standard_neg_risk_exchange_approval,
                self.standard_neg_risk_exchange_allowance,
                self.standard_neg_risk_adapter_approval,
            ]
        )

    @property
    def yield_ready(self) -> bool:
        return all(
            [
                self.yield_exchange_approval,
                self.yield_exchange_allowance,
                self.yield_neg_risk_exchange_approval,
                self.yield_neg_risk_exchange_allowance,
                self.yield_neg_risk_adapter_approval,
            ]
        )

    @property
    def all_ready(self) -> bool:
        return self.standard_ready and self.yield_ready

    def to_dict(self) -> dict[str, object]:
        return {
            "standard": {
                "exchangeApproval": self.standard_exchange_approval,
                "exchangeAllowance": self.standard_exchange_allowance,
                "negRiskExchangeApproval": self.standard_neg_risk_exchange_approval,
                "negRiskExchangeAllowance": self.standard_neg_risk_exchange_allowance,
                "negRiskAdapterApproval": self.standard_neg_risk_adapter_approval,
                "ready": self.standard_ready,
            },
            "yieldBearing": {
                "exchangeApproval": self.yield_exchange_approval,
                "exchangeAllowance": self.yield_exchange_allowance,
                "negRiskExchangeApproval": self.yield_neg_risk_exchange_approval,
                "negRiskExchangeAllowance": self.yield_neg_risk_exchange_allowance,
                "negRiskAdapterApproval": self.yield_neg_risk_adapter_approval,
                "ready": self.yield_ready,
            },
            "allReady": self.all_ready,
        }


class WalletSdkProtocol(Protocol):
    @property
    def mode(self) -> WalletMode: ...

    @property
    def signer_address(self) -> str: ...

    @property
    def funding_address(self) -> str: ...

    @property
    def chain_name(self) -> str: ...

    def get_bnb_balance_wei(self) -> int: ...

    def get_usdt_balance_wei(self) -> int: ...

    def get_approval_snapshot(self) -> ApprovalSnapshot: ...

    def set_all_approvals(self) -> dict[str, Any]: ...


class MandatedVaultBridgeProtocol(Protocol):
    @property
    def available_tools(self) -> frozenset[str]: ...

    @property
    def missing_required_tools(self) -> frozenset[str]: ...

    @property
    def runtime_ready(self) -> bool: ...

    async def connect(self) -> None: ...

    async def close(self) -> None: ...

    async def predict_vault_address(
        self,
        *,
        factory: str | None,
        asset: str,
        name: str,
        symbol: str,
        authority: str,
        salt: str,
    ) -> Any: ...

    async def health_check(self, vault: str) -> VaultHealthCheckResult: ...

    async def prepare_create_vault(
        self,
        *,
        from_address: str,
        factory: str | None,
        asset: str,
        name: str,
        symbol: str,
        authority: str,
        salt: str,
    ) -> FactoryCreateVaultPrepareResult: ...

    async def vault_bootstrap(
        self,
        *,
        factory: str | None,
        asset: str,
        name: str,
        symbol: str,
        salt: str,
        signer_address: str | None = None,
        mode: Any = "plan",
        authority_mode: Any = None,
        authority: str | None = None,
        executor: str | None = None,
        create_account_context: bool | None = None,
        create_funding_policy: bool | None = None,
        account_context_options: Mapping[str, Any] | None = None,
        funding_policy_options: Mapping[str, Any] | None = None,
    ) -> VaultBootstrapResult: ...

    async def create_agent_account_context(
        self,
        *,
        agent_id: str,
        vault: str,
        authority: str,
        executor: str,
        asset_registry_ref: str | None = None,
        funding_policy_ref: str | None = None,
        defaults: dict[str, Any] | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
    ) -> Any: ...

    async def create_agent_funding_policy(
        self,
        *,
        policy_id: str,
        allowed_token_addresses: list[str] | None = None,
        allowed_recipients: list[str] | None = None,
        max_amount_per_tx: str | None = None,
        max_amount_per_window: str | None = None,
        window_seconds: int | None = None,
        expires_at: str | None = None,
        repeatable: bool | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
    ) -> Any: ...

    async def build_agent_fund_and_action_plan(
        self,
        *,
        account_context: dict[str, Any],
        funding_target: dict[str, Any],
        funding_context: dict[str, Any],
        follow_up_action: dict[str, Any],
        funding_policy: dict[str, Any] | None = None,
    ) -> Any: ...

    async def create_agent_fund_and_action_session(
        self,
        *,
        fund_and_action_plan: dict[str, Any],
        session_id: str | None = None,
        created_at: str | None = None,
    ) -> Any: ...

    async def next_agent_fund_and_action_session_step(
        self,
        *,
        session: dict[str, Any],
    ) -> Any: ...

    async def apply_agent_fund_and_action_session_event(
        self,
        *,
        session: Mapping[str, Any],
        event: Mapping[str, Any],
    ) -> Any: ...

    async def create_agent_follow_up_action_result(
        self,
        *,
        follow_up_action_plan: Mapping[str, Any],
        status: str,
        updated_at: str,
        started_at: str | None = None,
        completed_at: str | None = None,
        attempt: int | None = None,
        reference: Mapping[str, Any] | None = None,
        output: Mapping[str, Any] | None = None,
        error: Mapping[str, Any] | None = None,
    ) -> Any: ...

    async def create_vault_asset_transfer_result(
        self,
        *,
        asset_transfer_plan: Mapping[str, Any],
        status: str,
        updated_at: str,
        submitted_at: str | None = None,
        completed_at: str | None = None,
        attempt: int | None = None,
        chain_id: int | None = None,
        tx_hash: str | None = None,
        receipt: Mapping[str, Any] | None = None,
        output: Mapping[str, Any] | None = None,
        error: Mapping[str, Any] | None = None,
    ) -> Any: ...


class PredictSdkWallet:
    def __init__(self, config: PredictConfig) -> None:
        self._config = config
        if config.wallet_mode == WalletMode.READ_ONLY:
            raise ConfigError(
                "Wallet actions require PREDICT_EOA_PRIVATE_KEY or Predict Account credentials."
            )

        if config.wallet_mode == WalletMode.PREDICT_ACCOUNT:
            assert config.privy_private_key_value is not None
            assert config.predict_account_address is not None
            self._builder = OrderBuilder.make(
                config.chain_id,
                config.privy_private_key_value,
                OrderBuilderOptions(predict_account=config.predict_account_address),
            )
        else:
            assert config.private_key_value is not None
            self._builder = OrderBuilder.make(config.chain_id, config.private_key_value)

    @property
    def mode(self) -> WalletMode:
        return self._config.wallet_mode

    @property
    def signer_address(self) -> str:
        if self._config.wallet_mode == WalletMode.PREDICT_ACCOUNT:
            assert self._config.privy_private_key_value is not None
            return Account.from_key(self._config.privy_private_key_value).address
        assert self._config.private_key_value is not None
        return Account.from_key(self._config.private_key_value).address

    @property
    def funding_address(self) -> str:
        return self._config.predict_account_address or self.signer_address

    @property
    def chain_name(self) -> str:
        return (
            "BNB Mainnet" if self._config.env == RuntimeEnv.MAINNET else "BNB Testnet"
        )

    def get_bnb_balance_wei(self) -> int:
        web3 = getattr(self._builder, "_web3", None)
        if web3 is None:
            raise ConfigError(
                "BNB balance requires an initialized Web3 signer context."
            )
        return int(web3.eth.get_balance(self.funding_address))

    def get_usdt_balance_wei(self) -> int:
        return int(self._builder.balance_of("USDT", self.funding_address))

    def get_approval_snapshot(self) -> ApprovalSnapshot:
        contracts = self._builder.contracts
        if contracts is None:
            raise ConfigError(
                "Approval checks require initialized predict.fun contracts."
            )

        owner = self.funding_address
        return ApprovalSnapshot(
            standard_exchange_approval=self._erc1155_approval(
                owner, is_neg_risk=False, is_yield_bearing=False
            ),
            standard_exchange_allowance=self._usdt_allowance(
                owner, is_neg_risk=False, is_yield_bearing=False
            ),
            standard_neg_risk_exchange_approval=self._erc1155_approval(
                owner, is_neg_risk=True, is_yield_bearing=False
            ),
            standard_neg_risk_exchange_allowance=self._usdt_allowance(
                owner, is_neg_risk=True, is_yield_bearing=False
            ),
            standard_neg_risk_adapter_approval=self._adapter_approval(
                owner, is_yield_bearing=False
            ),
            yield_exchange_approval=self._erc1155_approval(
                owner, is_neg_risk=False, is_yield_bearing=True
            ),
            yield_exchange_allowance=self._usdt_allowance(
                owner, is_neg_risk=False, is_yield_bearing=True
            ),
            yield_neg_risk_exchange_approval=self._erc1155_approval(
                owner, is_neg_risk=True, is_yield_bearing=True
            ),
            yield_neg_risk_exchange_allowance=self._usdt_allowance(
                owner, is_neg_risk=True, is_yield_bearing=True
            ),
            yield_neg_risk_adapter_approval=self._adapter_approval(
                owner, is_yield_bearing=True
            ),
        )

    def set_all_approvals(self) -> dict[str, Any]:
        return {
            "standard": self._builder.set_approvals(is_yield_bearing=False),
            "yieldBearing": self._builder.set_approvals(is_yield_bearing=True),
        }

    def _erc1155_approval(
        self, owner: str, *, is_neg_risk: bool, is_yield_bearing: bool
    ) -> bool:
        contracts = self._builder.contracts
        assert contracts is not None
        exchange = get_exchange_contract(
            contracts,
            is_neg_risk=is_neg_risk,
            is_yield_bearing=is_yield_bearing,
        )
        conditional_tokens = get_conditional_tokens_contract(
            contracts,
            is_neg_risk=is_neg_risk,
            is_yield_bearing=is_yield_bearing,
        )
        return bool(
            conditional_tokens.functions.isApprovedForAll(
                owner, exchange.address
            ).call()
        )

    def _adapter_approval(self, owner: str, *, is_yield_bearing: bool) -> bool:
        contracts = self._builder.contracts
        assert contracts is not None
        adapter = get_neg_risk_adapter_contract(
            contracts, is_yield_bearing=is_yield_bearing
        )
        conditional_tokens = get_conditional_tokens_contract(
            contracts,
            is_neg_risk=True,
            is_yield_bearing=is_yield_bearing,
        )
        return bool(
            conditional_tokens.functions.isApprovedForAll(owner, adapter.address).call()
        )

    def _usdt_allowance(
        self, owner: str, *, is_neg_risk: bool, is_yield_bearing: bool
    ) -> bool:
        contracts = self._builder.contracts
        assert contracts is not None
        exchange = get_exchange_contract(
            contracts,
            is_neg_risk=is_neg_risk,
            is_yield_bearing=is_yield_bearing,
        )
        allowance = contracts.usdt.functions.allowance(owner, exchange.address).call()
        return int(allowance) > 0


class FixtureWalletSdk:
    def __init__(self, config: PredictConfig) -> None:
        self._config = config
        if config.wallet_mode == WalletMode.READ_ONLY:
            raise ConfigError(
                "Wallet actions require PREDICT_EOA_PRIVATE_KEY or Predict Account credentials."
            )

    @property
    def mode(self) -> WalletMode:
        return self._config.wallet_mode

    @property
    def signer_address(self) -> str:
        if self._config.wallet_mode == WalletMode.PREDICT_ACCOUNT:
            assert self._config.privy_private_key_value is not None
            return Account.from_key(self._config.privy_private_key_value).address
        assert self._config.private_key_value is not None
        return Account.from_key(self._config.private_key_value).address

    @property
    def funding_address(self) -> str:
        return self._config.predict_account_address or self.signer_address

    @property
    def chain_name(self) -> str:
        return "BNB Testnet"

    def get_bnb_balance_wei(self) -> int:
        return 1_500_000_000_000_000_000

    def get_usdt_balance_wei(self) -> int:
        return 25_000_000_000_000_000_000

    def get_approval_snapshot(self) -> ApprovalSnapshot:
        return ApprovalSnapshot(
            standard_exchange_approval=True,
            standard_exchange_allowance=True,
            standard_neg_risk_exchange_approval=True,
            standard_neg_risk_exchange_allowance=True,
            standard_neg_risk_adapter_approval=True,
            yield_exchange_approval=True,
            yield_exchange_allowance=True,
            yield_neg_risk_exchange_approval=True,
            yield_neg_risk_exchange_allowance=True,
            yield_neg_risk_adapter_approval=True,
        )

    def set_all_approvals(self) -> dict[str, Any]:
        return {
            "standard": {"success": True, "mode": "fixture"},
            "yieldBearing": {"success": True, "mode": "fixture"},
        }


async def load_wallet_bnb_balance_wei(sdk: WalletSdkProtocol) -> int:
    return int(await asyncio.to_thread(sdk.get_bnb_balance_wei))


async def load_wallet_usdt_balance_wei(sdk: WalletSdkProtocol) -> int:
    return int(await asyncio.to_thread(sdk.get_usdt_balance_wei))


def make_wallet_sdk(config: PredictConfig) -> WalletSdkProtocol:
    if config.env == RuntimeEnv.TEST_FIXTURE:
        return FixtureWalletSdk(config)
    return PredictSdkWallet(config)


@dataclass
class WalletStatusSnapshot:
    mode: str
    signer_address: str
    funding_address: str
    chain: str
    bnb_balance_wei: int
    usdt_balance_wei: int
    auth_ready: bool
    approvals: ApprovalSnapshot
    active_route: str | None = None
    route_purpose: str | None = None
    funding_route: str | None = None
    predict_account_address: str | None = None
    trade_signer_address: str | None = None
    vault_address: str | None = None
    vault_address_source: str | None = None
    vault_exists: bool | None = None
    funding_orchestration: dict[str, object] | None = None
    permission_summary: dict[str, object] | None = None
    session_scope: str | None = None
    session_binding: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "mode": self.mode,
            "signerAddress": self.signer_address,
            "fundingAddress": self.funding_address,
            "chain": self.chain,
            "bnbBalanceWei": self.bnb_balance_wei,
            "usdtBalanceWei": self.usdt_balance_wei,
            "authReady": self.auth_ready,
            "approvals": self.approvals.to_dict(),
        }
        if self.active_route is not None:
            payload["activeRoute"] = self.active_route
        if self.route_purpose is not None:
            payload["routePurpose"] = self.route_purpose
        if self.funding_route is not None:
            payload.update(
                {
                    "fundingRoute": self.funding_route,
                    "predictAccountAddress": self.predict_account_address,
                    "tradeSignerAddress": self.trade_signer_address,
                    "vaultAddress": self.vault_address,
                    "vaultAddressSource": self.vault_address_source,
                    "vaultExists": self.vault_exists,
                    "fundingOrchestration": self.funding_orchestration,
                }
            )
            payload.update(
                _overlay_address_guidance_payload(
                    predict_account_address=self.predict_account_address,
                    vault_address=self.vault_address,
                )
            )
        if self.permission_summary is not None:
            payload["permissionSummary"] = self.permission_summary
        if self.session_scope is not None:
            payload["sessionScope"] = self.session_scope
        if self.session_binding is not None:
            payload["sessionBinding"] = self.session_binding
        return payload


@dataclass
class VaultPermissionSummary:
    permission_model: str
    vault_authority: str | None
    vault_executor: str | None
    bootstrap_signer: str | None
    underlying_asset: str | None
    share_token: str | None = None
    allowed_token_addresses: list[str] | None = None
    allowed_recipients: list[str] | None = None
    max_amount_per_tx: str | None = None
    max_amount_per_window: str | None = None
    window_seconds: int | None = None
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "permissionModel": self.permission_model,
            "vaultAuthority": self.vault_authority,
            "vaultExecutor": self.vault_executor,
            "bootstrapSigner": self.bootstrap_signer,
            "underlyingAsset": self.underlying_asset,
            "safetyNotes": self.safety_notes,
        }
        if self.share_token is not None:
            payload["shareToken"] = self.share_token
        if self.allowed_token_addresses is not None:
            payload["allowedTokenAddresses"] = self.allowed_token_addresses
        if self.allowed_recipients is not None:
            payload["allowedRecipients"] = self.allowed_recipients
        if self.max_amount_per_tx is not None:
            payload["maxAmountPerTx"] = self.max_amount_per_tx
        if self.max_amount_per_window is not None:
            payload["maxAmountPerWindow"] = self.max_amount_per_window
        if self.window_seconds is not None:
            payload["windowSeconds"] = self.window_seconds
        return payload


@dataclass
class VaultToPredictAccountFundingOrchestration:
    funding_route: str
    predict_account_address: str
    trade_signer_address: str
    vault_address: str
    vault_address_source: str
    vault_exists: bool
    account_context: dict[str, Any]
    funding_policy: dict[str, Any]
    funding_target: dict[str, Any]
    funding_plan: dict[str, Any]
    funding_session: dict[str, Any]
    funding_next_step: dict[str, Any]

    def to_dict(self) -> dict[str, object]:
        payload = {
            "fundingRoute": self.funding_route,
            "predictAccountAddress": self.predict_account_address,
            "tradeSignerAddress": self.trade_signer_address,
            "vaultAddress": self.vault_address,
            "vaultAddressSource": self.vault_address_source,
            "vaultExists": self.vault_exists,
            "accountContext": self.account_context,
            "fundingPolicy": self.funding_policy,
            "fundingTarget": self.funding_target,
            "fundingPlan": self.funding_plan,
            "fundingSession": self.funding_session,
            "fundingNextStep": self.funding_next_step,
        }
        payload.update(
            _overlay_address_guidance_payload(
                predict_account_address=self.predict_account_address,
                vault_address=self.vault_address,
            )
        )
        return payload


@dataclass
class ApprovalRunSummary:
    standard: Any
    yield_bearing: Any

    def to_dict(self) -> dict[str, object]:
        return {
            "standard": self.standard,
            "yieldBearing": self.yield_bearing,
        }


MANDATED_FUNDING_TRANSFER_MAX_DRAWDOWN_BPS = "10000"
MANDATED_FUNDING_TRANSFER_MAX_CUMULATIVE_DRAWDOWN_BPS = "10000"


@dataclass
class MandatedVaultBootstrapSnapshot:
    mode: str
    chain_id: int
    chain_name: str
    factory: str
    signer_address: str
    predicted_vault: str
    deployed_vault: str
    vault_address_source: str
    vault_deployed: bool
    already_deployed: bool
    deployment_status: str
    confirmation_required: bool
    tx_summary: dict[str, object] | None
    env_block: str | None = None
    config_block: str | None = None
    backfill_env: dict[str, str] | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "mode": self.mode,
            "chainId": self.chain_id,
            "chain": self.chain_name,
            "factory": self.factory,
            "signerAddress": self.signer_address,
            "predictedVault": self.predicted_vault,
            "deployedVault": self.deployed_vault,
            "vaultAddressSource": self.vault_address_source,
            "vaultDeployed": self.vault_deployed,
            "alreadyDeployed": self.already_deployed,
            "deploymentStatus": self.deployment_status,
            "confirmationRequired": self.confirmation_required,
            "txSummary": self.tx_summary,
        }
        if self.env_block is not None:
            payload["envBlock"] = self.env_block
        if self.config_block is not None:
            payload["configBlock"] = self.config_block
        if self.backfill_env is not None:
            payload["backfillEnv"] = self.backfill_env
        return payload


@dataclass
class MandatedVaultResolution:
    vault_address: str
    vault_address_source: str
    vault_deployed: bool
    vault_health: VaultHealthCheckResult | None
    create_vault_prepare: FactoryCreateVaultPrepareResult | None
    bootstrap_preview: MandatedVaultBootstrapSnapshot | None = None


@dataclass
class MandatedWalletStatusSnapshot:
    mode: str
    selected_chain_name: str
    selected_chain_id: int
    mcp_command: str
    mcp_available_tools: list[str]
    mcp_missing_required_tools: list[str]
    mcp_runtime_ready: bool
    vault_address: str
    vault_address_source: str
    vault_deployed: bool
    vault_health: VaultHealthCheckResult | None
    state_changing_flows_enabled: bool
    active_route: str = "vault-control-plane"
    route_purpose: str = "bootstrap-or-direct-vault-ops"
    bootstrap_preview: MandatedVaultBootstrapSnapshot | None = None
    permission_summary: VaultPermissionSummary | None = None

    def to_dict(self) -> dict[str, object]:
        health_payload: dict[str, object] | None = None
        if self.vault_health is not None:
            health_payload = {
                "mandateAuthority": self.vault_health.mandateAuthority,
                "authorityEpoch": self.vault_health.authorityEpoch,
                "nonceThreshold": self.vault_health.nonceThreshold,
                "totalAssets": self.vault_health.totalAssets,
            }

        payload = {
            "mode": self.mode,
            "selectedChain": {
                "name": self.selected_chain_name,
                "chainId": self.selected_chain_id,
            },
            "activeRoute": self.active_route,
            "routePurpose": self.route_purpose,
            "mcp": {
                "command": self.mcp_command,
                "availableTools": self.mcp_available_tools,
                "missingRequiredTools": self.mcp_missing_required_tools,
                "runtimeReady": self.mcp_runtime_ready,
            },
            "vaultAddress": self.vault_address,
            "vaultAddressSource": self.vault_address_source,
            "vaultDeployed": self.vault_deployed,
            "vaultDeploymentState": "deployed" if self.vault_deployed else "undeployed",
            "vaultHealth": health_payload,
            "stateChangingFlowsEnabled": self.state_changing_flows_enabled,
        }
        if self.bootstrap_preview is not None:
            payload["bootstrapPreview"] = self.bootstrap_preview.to_dict()
        if self.permission_summary is not None:
            payload["permissionSummary"] = self.permission_summary.to_dict()
        return payload


def _overlay_address_guidance_payload(
    *,
    predict_account_address: str | None,
    vault_address: str | None,
) -> dict[str, object]:
    return {
        "manualTopUpAddress": vault_address,
        "manualTopUpGuidance": (
            "Use the vault deposit flow as the default funding entry; the Predict Account "
            "remains the trading identity and receives vault-driven top-ups afterward."
        ),
        "tradingIdentityAddress": predict_account_address,
        "orchestrationVaultAddress": vault_address,
    }


def has_mandated_vault_derivation(config: PredictConfig) -> bool:
    return all(
        [
            config.mandated_factory_address,
            config.mandated_vault_asset_address,
            config.mandated_vault_name,
            config.mandated_vault_symbol,
            config.mandated_vault_authority,
            config.mandated_vault_salt,
        ]
    )


def _supports_vault_bootstrap(bridge: MandatedVaultBridgeProtocol) -> bool:
    return "vault_bootstrap" in bridge.available_tools


def _bootstrap_create_vault_prepare(
    bootstrap: VaultBootstrapResult,
) -> FactoryCreateVaultPrepareResult | None:
    create_tx = bootstrap.createTx
    if create_tx is None or create_tx.txRequest is None:
        return None
    return FactoryCreateVaultPrepareResult(
        predictedVault=bootstrap.predictedVault,
        txRequest=create_tx.txRequest,
    )


def _selected_mandated_chain_id(config: PredictConfig) -> int:
    return config.mandated_chain_id or int(config.chain_id)


def _selected_mandated_chain_name(config: PredictConfig) -> str:
    return "BNB Mainnet" if _selected_mandated_chain_id(config) == 56 else "BNB Testnet"


def _resolve_overlay_rpc_url(config: PredictConfig) -> str:
    chain_id = _selected_mandated_chain_id(config)
    for env_name in OVERLAY_RPC_ENV_CANDIDATES.get(chain_id, ("ERC_MANDATED_RPC_URL",)):
        value = os.environ.get(env_name)
        if value:
            return value
    fallback = OVERLAY_PUBLIC_RPC_FALLBACKS.get(chain_id)
    if fallback:
        return fallback
    raise ConfigError(f"No RPC URL configured for chainId {chain_id}.")


def _load_explicit_vault_asset_address(
    config: PredictConfig, vault_address: str
) -> str:
    rpc_url = _resolve_overlay_rpc_url(config)
    web3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 20}))
    checksum_vault = Web3.to_checksum_address(vault_address)
    vault_contract = web3.eth.contract(address=checksum_vault, abi=ERC4626_ASSET_ABI)
    asset = vault_contract.functions.asset().call()
    return Web3.to_checksum_address(cast(str, asset))


def resolve_overlay_vault_runtime_metadata(
    config: PredictConfig,
    resolution: "MandatedVaultResolution",
) -> dict[str, str]:
    authority = config.mandated_vault_authority
    if authority is None and resolution.vault_health is not None:
        authority = resolution.vault_health.mandateAuthority

    asset_address = config.mandated_vault_asset_address
    if asset_address is None and resolution.vault_deployed:
        asset_address = _load_explicit_vault_asset_address(
            config, resolution.vault_address
        )

    if not resolution.vault_deployed:
        raise ConfigError(
            "predict-account + vault overlay needs a deployed vault first. Deploy or redeploy a vault with the pure mandated-vault bootstrap flow before using the overlay path."
        )
    if authority is None or asset_address is None:
        raise ConfigError(
            "predict-account + vault overlay could not resolve vault metadata from the configured vault. Deploy or redeploy a vault first, or provide the advanced manual vault metadata."
        )

    return {
        "vaultAuthority": authority,
        "vaultAssetAddress": asset_address,
    }


def _bootstrap_tx_summary(
    bootstrap: VaultBootstrapResult,
) -> dict[str, object] | None:
    create_tx = bootstrap.createTx
    if create_tx is None:
        return None
    payload: dict[str, object] = {}
    if create_tx.txRequest is not None:
        payload.update(
            {
                "from": create_tx.txRequest.from_address,
                "to": create_tx.txRequest.to,
                "data": create_tx.txRequest.data,
                "value": create_tx.txRequest.value,
                "gas": create_tx.txRequest.gas,
            }
        )
    if create_tx.txHash is not None:
        payload["txHash"] = create_tx.txHash
    if create_tx.receiptStatus is not None:
        payload["receiptStatus"] = create_tx.receiptStatus
    if create_tx.blockNumber is not None:
        payload["blockNumber"] = create_tx.blockNumber
    if create_tx.confirmations is not None:
        payload["confirmations"] = create_tx.confirmations
    return payload or None


def _parse_env_block(env_block: str | None) -> dict[str, str]:
    if not env_block:
        return {}
    payload: dict[str, str] = {}
    for raw_line in env_block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        payload[key.strip()] = value.strip()
    return payload


def _build_backfill_env(
    config: PredictConfig,
    bootstrap: VaultBootstrapResult,
) -> dict[str, str]:
    selected_chain_id = _selected_mandated_chain_id(config)
    payload = _parse_env_block(bootstrap.envBlock)
    payload.update(
        {
            "ERC_MANDATED_VAULT_ADDRESS": bootstrap.deployedVault,
            "ERC_MANDATED_FACTORY_ADDRESS": bootstrap.factory,
            "ERC_MANDATED_CHAIN_ID": str(selected_chain_id),
            "ERC_MANDATED_MCP_COMMAND": config.mandated_mcp_command,
            "ERC_MANDATED_CONTRACT_VERSION": config.mandated_contract_version,
            "ERC_MANDATED_VAULT_ASSET_ADDRESS": str(
                config.mandated_vault_asset_address
            ),
            "ERC_MANDATED_VAULT_NAME": str(config.mandated_vault_name),
            "ERC_MANDATED_VAULT_SYMBOL": str(config.mandated_vault_symbol),
            "ERC_MANDATED_VAULT_AUTHORITY": str(config.mandated_vault_authority),
            "ERC_MANDATED_VAULT_SALT": str(config.mandated_vault_salt),
        }
    )
    return payload


def _build_bootstrap_snapshot(
    config: PredictConfig,
    bootstrap: VaultBootstrapResult,
    *,
    vault_address_source: str,
    mode: str,
    include_backfill_env: bool,
) -> MandatedVaultBootstrapSnapshot:
    return MandatedVaultBootstrapSnapshot(
        mode=mode,
        chain_id=_selected_mandated_chain_id(config),
        chain_name=_selected_mandated_chain_name(config),
        factory=bootstrap.factory,
        signer_address=bootstrap.signerAddress,
        predicted_vault=bootstrap.predictedVault,
        deployed_vault=bootstrap.deployedVault,
        vault_address_source=vault_address_source,
        vault_deployed=bootstrap.alreadyDeployed,
        already_deployed=bootstrap.alreadyDeployed,
        deployment_status=bootstrap.deploymentStatus,
        confirmation_required=(not bootstrap.alreadyDeployed and mode == "plan"),
        tx_summary=_bootstrap_tx_summary(bootstrap),
        env_block=bootstrap.envBlock,
        config_block=bootstrap.configBlock,
        backfill_env=_build_backfill_env(config, bootstrap)
        if include_backfill_env
        else None,
    )


def _build_execute_bootstrap_config(config: PredictConfig) -> PredictConfig:
    bootstrap_private_key = config.mandated_bootstrap_private_key_value
    return config.model_copy(
        update={
            "mandated_enable_broadcast": (
                True
                if config.mandated_enable_broadcast is None
                else config.mandated_enable_broadcast
            ),
            "mandated_bootstrap_private_key": SecretStr(bootstrap_private_key)
            if bootstrap_private_key is not None
            else None,
        }
    )


def _build_mandated_permission_summary(
    config: PredictConfig,
    *,
    permission_model: str,
    vault_authority: str | None = None,
    underlying_asset: str | None = None,
    allowed_token_addresses: list[str] | None = None,
    allowed_recipients: list[str] | None = None,
    max_amount_per_tx: str | None = None,
    max_amount_per_window: str | None = None,
    window_seconds: int | None = None,
    share_token: str | None = None,
) -> VaultPermissionSummary:
    safety_notes = [
        "Authority controls vault mandate authority state.",
        "Bootstrap signer can differ from authority and is only used for deployment/bootstrap execution.",
    ]
    if allowed_token_addresses or allowed_recipients:
        safety_notes.append(
            "Funding policy restricts asset movement to listed tokens/recipients and configured window caps."
        )
    else:
        safety_notes.append(
            "No overlay funding policy is active; bootstrap alone does not grant generalized transfer permissions."
        )
    if permission_model == "mandated-vault-v1":
        safety_notes.append(
            "Pure mandated-vault v1 still blocks generic wallet approve/withdraw trading parity flows."
        )
    return VaultPermissionSummary(
        permission_model=permission_model,
        vault_authority=vault_authority or config.mandated_vault_authority,
        vault_executor=config.mandated_executor_address,
        bootstrap_signer=config.mandated_bootstrap_signer_address,
        underlying_asset=underlying_asset
        or (
            str(config.mandated_vault_asset_address)
            if config.mandated_vault_asset_address
            else None
        ),
        share_token=share_token,
        allowed_token_addresses=allowed_token_addresses,
        allowed_recipients=allowed_recipients,
        max_amount_per_tx=max_amount_per_tx,
        max_amount_per_window=max_amount_per_window,
        window_seconds=window_seconds,
        safety_notes=safety_notes,
    )


async def resolve_mandated_vault(
    config: PredictConfig,
    bridge: MandatedVaultBridgeProtocol,
    *,
    include_create_prepare: bool,
) -> MandatedVaultResolution:
    if config.mandated_vault_address:
        vault_address = config.mandated_vault_address
        vault_address_source = "explicit"
    else:
        if not has_mandated_vault_derivation(config):
            raise ConfigError(
                "mandated-vault mode requires ERC_MANDATED_VAULT_ADDRESS or full derivation inputs."
            )

        if _supports_vault_bootstrap(bridge):
            assert config.mandated_vault_authority is not None
            assert config.mandated_bootstrap_signer_address is not None
            bootstrap = await bridge.vault_bootstrap(
                factory=config.mandated_factory_address,
                asset=str(config.mandated_vault_asset_address),
                name=str(config.mandated_vault_name),
                symbol=str(config.mandated_vault_symbol),
                salt=str(config.mandated_vault_salt),
                signer_address=str(config.mandated_bootstrap_signer_address),
                mode="plan",
                authority_mode="single_key",
                authority=str(config.mandated_vault_authority),
                create_account_context=False,
                create_funding_policy=False,
            )
            vault_address = bootstrap.deployedVault
            vault_address_source = "predicted"
            vault_deployed = bootstrap.alreadyDeployed
            vault_health = bootstrap.vaultHealth
            if vault_deployed and vault_health is None:
                vault_health = await bridge.health_check(vault_address)
            bootstrap_preview = None
            if not vault_deployed:
                bootstrap_preview = _build_bootstrap_snapshot(
                    config,
                    bootstrap,
                    vault_address_source=vault_address_source,
                    mode="plan",
                    include_backfill_env=False,
                )

            return MandatedVaultResolution(
                vault_address=vault_address,
                vault_address_source=vault_address_source,
                vault_deployed=vault_deployed,
                vault_health=vault_health,
                create_vault_prepare=(
                    _bootstrap_create_vault_prepare(bootstrap)
                    if include_create_prepare and not vault_deployed
                    else None
                ),
                bootstrap_preview=bootstrap_preview,
            )

        predicted = await bridge.predict_vault_address(
            factory=config.mandated_factory_address,
            asset=str(config.mandated_vault_asset_address),
            name=str(config.mandated_vault_name),
            symbol=str(config.mandated_vault_symbol),
            authority=str(config.mandated_vault_authority),
            salt=str(config.mandated_vault_salt),
        )
        vault_address = str(getattr(predicted, "predictedVault"))
        vault_address_source = "predicted"

    vault_health: VaultHealthCheckResult | None = None
    vault_deployed = False
    try:
        vault_health = await bridge.health_check(vault_address)
        vault_deployed = True
    except MandatedVaultMcpError as error:
        if not _is_expected_undeployed_health_error(error):
            raise
        vault_health = None

    create_vault_prepare: FactoryCreateVaultPrepareResult | None = None
    if (
        include_create_prepare
        and not vault_deployed
        and has_mandated_vault_derivation(config)
    ):
        assert config.mandated_vault_authority is not None
        create_vault_prepare = await bridge.prepare_create_vault(
            from_address=config.mandated_vault_authority,
            factory=config.mandated_factory_address,
            asset=str(config.mandated_vault_asset_address),
            name=str(config.mandated_vault_name),
            symbol=str(config.mandated_vault_symbol),
            authority=str(config.mandated_vault_authority),
            salt=str(config.mandated_vault_salt),
        )

    return MandatedVaultResolution(
        vault_address=vault_address,
        vault_address_source=vault_address_source,
        vault_deployed=vault_deployed,
        vault_health=vault_health,
        create_vault_prepare=create_vault_prepare,
        bootstrap_preview=None,
    )


def _is_expected_undeployed_health_error(error: MandatedVaultMcpError) -> bool:
    message = str(error).upper()
    undeployed_markers = (
        "VAULT_NOT_DEPLOYED",
        "VAULT_UNDEPLOYED",
        "VAULT_NOT_FOUND",
        "NO_CONTRACT_CODE",
        "NOT DEPLOYED",
        "RETURNED NO DATA",
        "ADDRESS IS NOT A CONTRACT",
    )
    return any(marker in message for marker in undeployed_markers)


def _has_predict_account_overlay(config: PredictConfig) -> bool:
    return (
        config.wallet_mode == WalletMode.PREDICT_ACCOUNT
        and config.has_mandated_config_input
    )


def _result_dict(result: Any, *, field: str, operation: str) -> dict[str, Any]:
    payload = result.model_dump() if hasattr(result, "model_dump") else result
    if not isinstance(payload, dict):
        raise ConfigError(f"Malformed {operation} response: expected object payload.")
    nested = payload.get(field)
    if not isinstance(nested, dict):
        raise ConfigError(
            f"Malformed {operation} response: expected `{field}` object in payload."
        )
    return nested


async def build_vault_to_predict_account_orchestration(
    config: PredictConfig,
    bridge: MandatedVaultBridgeProtocol,
    *,
    predict_account_address: str,
    trade_signer_address: str,
    current_usdt_balance_wei: int,
    wallet_sdk: Any | None = None,
) -> VaultToPredictAccountFundingOrchestration:
    resolution = await resolve_mandated_vault(
        config, bridge, include_create_prepare=False
    )
    metadata = resolve_overlay_vault_runtime_metadata(config, resolution)
    resolved_authority = metadata["vaultAuthority"]
    resolved_asset_address = metadata["vaultAssetAddress"]
    timestamp = (
        datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    agent_id = f"predict-account:{predict_account_address.lower()}"
    policy_id = f"vault-to-predict-account:{predict_account_address.lower()}"
    funding_executor_address = config.mandated_executor_address or resolved_authority
    if not funding_executor_address:
        raise ConfigError(
            "predict-account + vault overlay requires an authorized funding executor address."
        )
    allowed_adapters_root = _resolve_transfer_allowed_adapters_root(
        token_address=resolved_asset_address,
        wallet_sdk=wallet_sdk,
        fallback_root=config.mandated_allowed_adapters_root,
    )
    mandate_defaults = {
        "allowedAdaptersRoot": allowed_adapters_root,
        "maxDrawdownBps": MANDATED_FUNDING_TRANSFER_MAX_DRAWDOWN_BPS,
        "maxCumulativeDrawdownBps": MANDATED_FUNDING_TRANSFER_MAX_CUMULATIVE_DRAWDOWN_BPS,
        "payloadBinding": "actionsDigest",
        "extensions": "0x",
    }

    context_result = await bridge.create_agent_account_context(
        agent_id=agent_id,
        vault=resolution.vault_address,
        authority=resolved_authority,
        executor=funding_executor_address,
        funding_policy_ref=policy_id,
        defaults=dict(mandate_defaults),
        created_at=timestamp,
        updated_at=timestamp,
    )
    account_context = _result_dict(
        context_result,
        field="accountContext",
        operation="agent_account_context_create",
    )

    policy_result = await bridge.create_agent_funding_policy(
        policy_id=policy_id,
        allowed_token_addresses=[resolved_asset_address],
        allowed_recipients=[predict_account_address],
        max_amount_per_tx=config.mandated_funding_max_amount_per_tx,
        max_amount_per_window=config.mandated_funding_max_amount_per_window,
        window_seconds=config.mandated_funding_window_seconds,
        repeatable=True,
        created_at=timestamp,
        updated_at=timestamp,
    )
    funding_policy = _result_dict(
        policy_result,
        field="fundingPolicy",
        operation="agent_funding_policy_create",
    )

    minimum_target_balance_wei = 5 * (10**18)
    required_amount_raw = str(
        max(minimum_target_balance_wei - max(current_usdt_balance_wei, 0), 0)
    )
    funding_target = {
        "label": "predict-account-usdt",
        "recipient": predict_account_address,
        "tokenAddress": resolved_asset_address,
        "requiredAmountRaw": required_amount_raw,
        "currentBalanceRaw": str(max(current_usdt_balance_wei, 0)),
        "balanceSnapshot": {
            "snapshotAt": timestamp,
            "maxStalenessSeconds": 120,
            "source": "predict-wallet-status",
        },
    }
    funding_context = {
        "nonce": "0",
        "deadline": "0",
        "authorityEpoch": (
            resolution.vault_health.authorityEpoch if resolution.vault_health else "0"
        ),
        **mandate_defaults,
    }
    follow_up_action = {
        "kind": "predict-order-submission",
        "target": "predict-api",
        "payload": {
            "status": "deferred",
            "reason": "buy-orchestration-not-enabled-in-this-task",
        },
    }
    plan_result = await bridge.build_agent_fund_and_action_plan(
        account_context=account_context,
        funding_policy=funding_policy,
        funding_target=funding_target,
        funding_context=funding_context,
        follow_up_action=follow_up_action,
    )
    funding_plan = (
        plan_result.model_dump() if hasattr(plan_result, "model_dump") else plan_result
    )
    if not isinstance(funding_plan, dict):
        raise ConfigError(
            "Malformed agent_build_fund_and_action_plan response: expected object payload."
        )

    session_result = await bridge.create_agent_fund_and_action_session(
        fund_and_action_plan=funding_plan,
        created_at=timestamp,
    )
    funding_session = _result_dict(
        session_result,
        field="session",
        operation="agent_fund_and_action_session_create",
    )

    next_step_result = await bridge.next_agent_fund_and_action_session_step(
        session=funding_session,
    )
    funding_next_step = (
        next_step_result.model_dump()
        if hasattr(next_step_result, "model_dump")
        else next_step_result
    )
    if not isinstance(funding_next_step, dict):
        raise ConfigError(
            "Malformed agent_fund_and_action_session_next_step response: expected object payload."
        )
    task_payload = funding_next_step.get("task")
    if not isinstance(task_payload, dict):
        raise ConfigError(
            "Malformed agent_fund_and_action_session_next_step response: expected `task` object in payload."
        )

    return VaultToPredictAccountFundingOrchestration(
        funding_route="vault-to-predict-account",
        predict_account_address=predict_account_address,
        trade_signer_address=trade_signer_address,
        vault_address=resolution.vault_address,
        vault_address_source=resolution.vault_address_source,
        vault_exists=resolution.vault_deployed,
        account_context=account_context,
        funding_policy=funding_policy,
        funding_target=funding_target,
        funding_plan=funding_plan,
        funding_session=funding_session,
        funding_next_step=funding_next_step,
    )


def _resolve_transfer_allowed_adapters_root(
    *,
    token_address: str,
    wallet_sdk: Any | None,
    fallback_root: str,
) -> str:
    builder = getattr(wallet_sdk, "_builder", None)
    web3 = getattr(builder, "_web3", None)
    if web3 is None:
        return fallback_root

    checksum_token = Web3.to_checksum_address(token_address)
    try:
        token_code = web3.eth.get_code(checksum_token)
    except Exception as error:  # pragma: no cover - defensive live-path guard
        raise ConfigError(
            f"Unable to load token code for mandated funding adapter root: {checksum_token}"
        ) from error
    if len(token_code) == 0:
        raise ConfigError(
            f"Mandated funding token address has no deployed code: {checksum_token}"
        )

    codehash = Web3.keccak(token_code)
    leaf_root = Web3.keccak(
        abi_encode(["address", "bytes32"], [checksum_token, codehash])
    )
    return "0x" + leaf_root.hex()


class WalletManager:
    def __init__(
        self,
        config: PredictConfig,
        *,
        sdk_factory: Callable[[PredictConfig], WalletSdkProtocol] = make_wallet_sdk,
        bridge_factory: Callable[
            [PredictConfig], MandatedVaultBridgeProtocol
        ] = MandatedVaultMcpBridge,
    ) -> None:
        self._config = config
        self._sdk_factory = sdk_factory
        self._bridge_factory = bridge_factory

    def get_status(self) -> WalletStatusSnapshot | MandatedWalletStatusSnapshot:
        if self._config.wallet_mode == WalletMode.MANDATED_VAULT:
            return self._get_mandated_status()

        sdk = self._require_sdk()
        if _has_predict_account_overlay(self._config):
            return self._get_predict_account_overlay_status(sdk)

        return WalletStatusSnapshot(
            mode=sdk.mode.value,
            signer_address=sdk.signer_address,
            funding_address=sdk.funding_address,
            chain=sdk.chain_name,
            bnb_balance_wei=sdk.get_bnb_balance_wei(),
            usdt_balance_wei=sdk.get_usdt_balance_wei(),
            auth_ready=bool(self._config.auth_signer_address),
            approvals=sdk.get_approval_snapshot(),
        )

    def bootstrap_vault(self, *, confirm: bool) -> MandatedVaultBootstrapSnapshot:
        if self._config.wallet_mode != WalletMode.MANDATED_VAULT:
            raise ConfigError(
                "wallet bootstrap-vault only supports mandated-vault mode."
            )

        bootstrap_config = (
            _build_execute_bootstrap_config(self._config) if confirm else self._config
        )
        bridge = self._bridge_factory(bootstrap_config)

        async def _run_and_close() -> MandatedVaultBootstrapSnapshot:
            await bridge.connect()
            try:
                if not _supports_vault_bootstrap(bridge):
                    raise MandatedVaultMcpError(
                        "Mandated-vault MCP cannot perform bootstrap execute; missing required tool: vault_bootstrap."
                    )
                assert bootstrap_config.mandated_vault_authority is not None
                assert bootstrap_config.mandated_bootstrap_signer_address is not None
                bootstrap = await bridge.vault_bootstrap(
                    factory=bootstrap_config.mandated_factory_address,
                    asset=str(bootstrap_config.mandated_vault_asset_address),
                    name=str(bootstrap_config.mandated_vault_name),
                    symbol=str(bootstrap_config.mandated_vault_symbol),
                    salt=str(bootstrap_config.mandated_vault_salt),
                    signer_address=str(
                        bootstrap_config.mandated_bootstrap_signer_address
                    ),
                    mode="execute" if confirm else "plan",
                    authority_mode="single_key",
                    authority=str(bootstrap_config.mandated_vault_authority),
                    create_account_context=False,
                    create_funding_policy=False,
                )
                return _build_bootstrap_snapshot(
                    bootstrap_config,
                    bootstrap,
                    vault_address_source=(
                        "explicit"
                        if bootstrap_config.mandated_vault_address
                        else "predicted"
                    ),
                    mode="execute" if confirm else "plan",
                    include_backfill_env=confirm,
                )
            finally:
                await bridge.close()

        return asyncio.run(_run_and_close())

    def _get_predict_account_overlay_status(
        self, sdk: WalletSdkProtocol
    ) -> WalletStatusSnapshot:
        bridge = self._bridge_factory(self._config)

        async def _load_and_close() -> WalletStatusSnapshot:
            await bridge.connect()
            try:
                bnb_balance = await load_wallet_bnb_balance_wei(sdk)
                usdt_balance = await load_wallet_usdt_balance_wei(sdk)
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
                session_scope = "generic-balance-top-up"
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
                return WalletStatusSnapshot(
                    mode=sdk.mode.value,
                    signer_address=sdk.signer_address,
                    funding_address=orchestration.vault_address,
                    chain=sdk.chain_name,
                    bnb_balance_wei=bnb_balance,
                    usdt_balance_wei=usdt_balance,
                    auth_ready=bool(self._config.auth_signer_address),
                    approvals=sdk.get_approval_snapshot(),
                    active_route="vault-to-predict-account",
                    route_purpose="predict-account-top-up-and-trading",
                    funding_route=orchestration.funding_route,
                    predict_account_address=orchestration.predict_account_address,
                    trade_signer_address=orchestration.trade_signer_address,
                    vault_address=orchestration.vault_address,
                    vault_address_source=orchestration.vault_address_source,
                    vault_exists=orchestration.vault_exists,
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

    def approve(self) -> ApprovalRunSummary:
        if self._config.wallet_mode == WalletMode.MANDATED_VAULT:
            raise mandated_vault_v1_unsupported_error("wallet approve")

        sdk = self._require_sdk()
        results = sdk.set_all_approvals()
        return ApprovalRunSummary(
            standard=results["standard"],
            yield_bearing=results["yieldBearing"],
        )

    def _require_sdk(self) -> WalletSdkProtocol:
        if self._config.auth_signer_address is None:
            raise ConfigError(
                "Wallet actions require signer configuration. Set PREDICT_EOA_PRIVATE_KEY or both PREDICT_ACCOUNT_ADDRESS and PREDICT_PRIVY_PRIVATE_KEY."
            )
        return self._sdk_factory(self._config)

    def _get_mandated_status(self) -> MandatedWalletStatusSnapshot:
        bridge = self._bridge_factory(self._config)

        async def _load_and_close() -> MandatedWalletStatusSnapshot:
            await bridge.connect()
            try:
                resolution = await resolve_mandated_vault(
                    self._config,
                    bridge,
                    include_create_prepare=False,
                )
                return MandatedWalletStatusSnapshot(
                    mode=self._config.wallet_mode.value,
                    selected_chain_name=self._chain_name(),
                    selected_chain_id=self._selected_chain_id(),
                    mcp_command=self._config.mandated_mcp_command,
                    mcp_available_tools=sorted(bridge.available_tools),
                    mcp_missing_required_tools=sorted(bridge.missing_required_tools),
                    mcp_runtime_ready=bridge.runtime_ready,
                    vault_address=resolution.vault_address,
                    vault_address_source=resolution.vault_address_source,
                    vault_deployed=resolution.vault_deployed,
                    vault_health=resolution.vault_health,
                    state_changing_flows_enabled=bridge.runtime_ready,
                    bootstrap_preview=resolution.bootstrap_preview,
                    permission_summary=_build_mandated_permission_summary(
                        self._config,
                        permission_model="mandated-vault-v1",
                    ),
                )
            finally:
                await bridge.close()

        return asyncio.run(_load_and_close())

    def _chain_name(self) -> str:
        return (
            "BNB Mainnet" if self._config.env == RuntimeEnv.MAINNET else "BNB Testnet"
        )

    def _selected_chain_id(self) -> int:
        return self._config.mandated_chain_id or int(self._config.chain_id)
