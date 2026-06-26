from __future__ import annotations

import os
import re
from enum import Enum
from pathlib import Path
from typing import Mapping

from eth_account import Account
from pydantic import BaseModel, ConfigDict, SecretStr, ValidationError, model_validator
from predict_sdk import ChainId


class RuntimeEnv(str, Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"
    TEST_FIXTURE = "test-fixture"


class WalletMode(str, Enum):
    READ_ONLY = "read-only"
    EOA = "eoa"
    PREDICT_ACCOUNT = "predict-account"
    MANDATED_VAULT = "mandated-vault"


class ConfigError(ValueError):
    """Raised when predict runtime configuration is invalid."""

    def to_dict(self) -> dict[str, object]:
        return {"message": str(self)}

    def format_lines(self) -> list[str]:
        return [str(self)]


class RouteConflictConfigError(ConfigError):
    def __init__(
        self,
        *,
        active_mode: str,
        active_route: str,
        recommended_mode: str,
        recommended_route: str,
        route_conflict_reason: str,
        detected_capabilities: dict[str, bool],
        next_step: str,
    ) -> None:
        self.error_code = "route-mode-conflict"
        self.active_mode = active_mode
        self.active_route = active_route
        self.recommended_mode = recommended_mode
        self.recommended_route = recommended_route
        self.route_conflict_reason = route_conflict_reason
        self.detected_capabilities = detected_capabilities
        self.next_step = next_step
        super().__init__(
            "Current active route is "
            f"{active_route} because PREDICT_WALLET_MODE={active_mode}, "
            "but Predict Account credentials are also configured. "
            f"If your goal is funding Predict Account, switch to PREDICT_WALLET_MODE={recommended_mode} "
            f"to use the {recommended_route} route."
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "errorCode": self.error_code,
            "message": str(self),
            "activeMode": self.active_mode,
            "activeRoute": self.active_route,
            "recommendedMode": self.recommended_mode,
            "recommendedRoute": self.recommended_route,
            "routeConflictReason": self.route_conflict_reason,
            "detectedCapabilities": self.detected_capabilities,
            "nextStep": self.next_step,
        }

    def format_lines(self) -> list[str]:
        return [
            str(self),
            f"Active Mode: {self.active_mode}",
            f"Active Route: {self.active_route}",
            f"Recommended Mode: {self.recommended_mode}",
            f"Recommended Route: {self.recommended_route}",
            f"Reason: {self.route_conflict_reason}",
            f"Next Step: {self.next_step}",
        ]


MANDATED_MCP_COMMAND_DEFAULT = "erc-mandated-mcp"
MANDATED_CONTRACT_VERSION_DEFAULT = "v0.3.0-agent-contract"
MANDATED_ALLOWED_ADAPTERS_ROOT_DEFAULT = "0x" + "11" * 32
MANDATED_FACTORY_ADDRESS_DEFAULT = "0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6"
MANDATED_VAULT_NAME_DEFAULT = "PredictClaw Vault"
MANDATED_VAULT_SYMBOL_DEFAULT = "pCLAW"
MANDATED_VAULT_SALT_DEFAULT = (
    "0x515efd8b3fb262cd01675c249fcdf91ce513efff6fed6c1e97d2a6d7f526c7f9"
)
MANDATED_VAULT_ASSET_ADDRESS_BY_CHAIN_ID = {
    56: "0x55d398326f99059fF775485246999027B3197955",
    97: "0xB32171ecD878607FFc4F8FC0bCcE6852BB3149E0",
}
MANDATED_VAULT_V1_UNSUPPORTED_CODE = "unsupported-in-mandated-vault-v1"
MANDATED_MODE_REQUIRED_ERROR = (
    "Mandated vault configuration requires an explicit PREDICT_WALLET_MODE "
    "(predict-account or mandated-vault). If you do not want vault overlay "
    "behavior, clear all ERC_MANDATED_* values."
)
HEX32_RE = re.compile(r"^0x[a-fA-F0-9]{64}$")
MANDATED_INPUT_ENV_NAMES = (
    "ERC_MANDATED_VAULT_ADDRESS",
    "ERC_MANDATED_FACTORY_ADDRESS",
    "ERC_MANDATED_VAULT_ASSET_ADDRESS",
    "ERC_MANDATED_VAULT_NAME",
    "ERC_MANDATED_VAULT_SYMBOL",
    "ERC_MANDATED_VAULT_AUTHORITY",
    "ERC_MANDATED_VAULT_SALT",
    "ERC_MANDATED_AUTHORITY_PRIVATE_KEY",
    "ERC_MANDATED_EXECUTOR_PRIVATE_KEY",
    "ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY",
    "ERC_MANDATED_ENABLE_BROADCAST",
    "ERC_MANDATED_CHAIN_ID",
    "ERC_MANDATED_ALLOWED_ADAPTERS_ROOT",
    "ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX",
    "ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW",
    "ERC_MANDATED_FUNDING_WINDOW_SECONDS",
)
MANDATED_DERIVATION_CORE_ENV_NAMES = (
    "ERC_MANDATED_VAULT_ASSET_ADDRESS",
    "ERC_MANDATED_VAULT_NAME",
    "ERC_MANDATED_VAULT_SYMBOL",
    "ERC_MANDATED_VAULT_AUTHORITY",
    "ERC_MANDATED_VAULT_SALT",
)


def redact_text(text: str, secrets: list[str | None]) -> str:
    redacted = text
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, "<redacted>")
    redacted = re.sub(r"Bearer\s+[A-Za-z0-9._-]+", "Bearer <redacted>", redacted)
    redacted = re.sub(r"0x[a-fA-F0-9]{64}", "0x<redacted>", redacted)
    return redacted


def _build_predict_account_overlay_route_conflict() -> RouteConflictConfigError:
    return RouteConflictConfigError(
        active_mode=WalletMode.MANDATED_VAULT.value,
        active_route="vault-control-plane",
        recommended_mode=WalletMode.PREDICT_ACCOUNT.value,
        recommended_route="vault-to-predict-account",
        route_conflict_reason=(
            "mandated-vault mode selects the pure vault control-plane path, "
            "while the configured Predict Account credentials indicate an overlay funding workflow"
        ),
        detected_capabilities={
            "predictAccountCredentials": True,
            "mandatedVaultConfig": True,
            "predictAccountOverlayCandidate": True,
        },
        next_step=(
            "Set PREDICT_WALLET_MODE=predict-account and keep the current ERC_MANDATED_* settings "
            "if your goal is topping up Predict Account."
        ),
    )


def _default_api_base_url(runtime_env: RuntimeEnv) -> str:
    if runtime_env == RuntimeEnv.MAINNET:
        return "https://api.predict.fun"
    return "https://api-testnet.predict.fun"


class PredictConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    env: RuntimeEnv = RuntimeEnv.MAINNET
    storage_dir: Path = Path("~/.openclaw/predict").expanduser()
    wallet_mode_override: WalletMode | None = None
    api_key: SecretStr | None = None
    private_key: SecretStr | None = None
    predict_account_address: str | None = None
    privy_private_key: SecretStr | None = None
    mandated_vault_address: str | None = None
    mandated_factory_address: str | None = None
    mandated_vault_asset_address: str | None = None
    mandated_vault_name: str | None = None
    mandated_vault_symbol: str | None = None
    mandated_vault_authority: str | None = None
    mandated_vault_salt: str | None = None
    mandated_authority_private_key: SecretStr | None = None
    mandated_executor_private_key: SecretStr | None = None
    mandated_bootstrap_private_key: SecretStr | None = None
    mandated_enable_broadcast: bool | None = None
    mandated_mcp_command: str = MANDATED_MCP_COMMAND_DEFAULT
    mandated_contract_version: str = MANDATED_CONTRACT_VERSION_DEFAULT
    mandated_chain_id: int | None = None
    mandated_allowed_adapters_root: str = MANDATED_ALLOWED_ADAPTERS_ROOT_DEFAULT
    mandated_funding_max_amount_per_tx: str | None = None
    mandated_funding_max_amount_per_window: str | None = None
    mandated_funding_window_seconds: int | None = None
    has_mandated_config_input: bool = False
    has_mandated_explicit_vault_input: bool = False
    has_any_mandated_derivation_input: bool = False
    has_all_mandated_derivation_input: bool = False
    openrouter_api_key: SecretStr | None = None
    model_name: str | None = None
    api_base_url: str = "https://api.predict.fun"
    http_timeout_seconds: float = 15.0
    retry_attempts: int = 3
    retry_backoff_seconds: float = 0.25

    @model_validator(mode="after")
    def validate_runtime_contract(self) -> "PredictConfig":
        if self.env == RuntimeEnv.MAINNET and not self.api_key:
            raise ValueError(
                "PREDICT_API_KEY is required for mainnet. "
                "Use test-fixture for secret-free verification, or set a non-mainnet "
                "environment explicitly if you intentionally need it."
            )

        has_eoa = self.private_key is not None
        has_predict_account_address = bool(self.predict_account_address)
        has_privy_key = self.privy_private_key is not None
        has_predict_account_credentials = has_predict_account_address or has_privy_key
        has_predict_account_pair = has_predict_account_address and has_privy_key
        has_bootstrap_signer = has_eoa
        has_mandated_vault_address = self.has_mandated_explicit_vault_input
        has_any_mandated_derivation = self.has_any_mandated_derivation_input
        has_all_mandated_derivation = self.has_all_mandated_derivation_input

        def validate_mandated_overlay_inputs() -> None:
            if not self.has_mandated_config_input:
                return
            if has_any_mandated_derivation and not has_all_mandated_derivation:
                raise ValueError(
                    "mandated-vault mode requires ERC_MANDATED_VAULT_ADDRESS or all mandated vault derivation inputs."
                )
            if not has_mandated_vault_address and not has_all_mandated_derivation:
                raise ValueError(
                    "mandated-vault mode requires ERC_MANDATED_VAULT_ADDRESS or all mandated vault derivation inputs."
                )

        if not HEX32_RE.fullmatch(self.mandated_allowed_adapters_root):
            raise ValueError(
                "ERC_MANDATED_ALLOWED_ADAPTERS_ROOT must be a 32-byte hex string."
            )

        if self.wallet_mode_override is None:
            if self.has_mandated_config_input:
                raise ValueError(MANDATED_MODE_REQUIRED_ERROR)

            if has_predict_account_address != has_privy_key:
                raise ValueError(
                    "Predict Account mode requires both PREDICT_ACCOUNT_ADDRESS and PREDICT_PRIVY_PRIVATE_KEY."
                )

            if has_eoa and has_predict_account_credentials:
                raise ValueError(
                    "Use either PREDICT_EOA_PRIVATE_KEY for EOA mode or the Predict Account pair, not both."
                )

            return self

        if self.wallet_mode_override == WalletMode.READ_ONLY:
            if (
                has_eoa
                or has_predict_account_credentials
                or self.has_mandated_config_input
            ):
                raise ValueError(
                    "read-only mode does not allow EOA, Predict Account, or mandated-vault configuration."
                )
            return self

        if self.wallet_mode_override == WalletMode.EOA:
            if not has_eoa:
                raise ValueError("EOA mode requires PREDICT_EOA_PRIVATE_KEY.")
            if has_predict_account_credentials or self.has_mandated_config_input:
                raise ValueError(
                    "EOA mode does not allow Predict Account or mandated-vault configuration."
                )
            return self

        if self.wallet_mode_override == WalletMode.PREDICT_ACCOUNT:
            if has_predict_account_address != has_privy_key:
                raise ValueError(
                    "Predict Account mode requires both PREDICT_ACCOUNT_ADDRESS and PREDICT_PRIVY_PRIVATE_KEY."
                )
            if not has_predict_account_pair:
                raise ValueError(
                    "Predict Account mode requires both PREDICT_ACCOUNT_ADDRESS and PREDICT_PRIVY_PRIVATE_KEY."
                )
            if has_eoa:
                raise ValueError("Predict Account mode does not allow EOA credentials.")
            validate_mandated_overlay_inputs()
            return self

        if has_predict_account_credentials:
            raise ValueError(
                "mandated-vault mode does not allow Predict Account credentials."
            )
        if has_any_mandated_derivation and not has_all_mandated_derivation:
            raise ValueError(
                "mandated-vault mode requires PREDICT_EOA_PRIVATE_KEY, ERC_MANDATED_VAULT_ADDRESS, or full derivation inputs."
            )
        if (
            not has_bootstrap_signer
            and not has_mandated_vault_address
            and not has_all_mandated_derivation
        ):
            raise ValueError(
                "mandated-vault mode requires PREDICT_EOA_PRIVATE_KEY, ERC_MANDATED_VAULT_ADDRESS, or full derivation inputs."
            )

        return self

    @property
    def wallet_mode(self) -> WalletMode:
        if self.wallet_mode_override is not None:
            return self.wallet_mode_override
        if self.predict_account_address and self.privy_private_key:
            return WalletMode.PREDICT_ACCOUNT
        if self.private_key:
            return WalletMode.EOA
        return WalletMode.READ_ONLY

    @property
    def chain_id(self) -> ChainId:
        if self.env == RuntimeEnv.MAINNET:
            return ChainId.BNB_MAINNET
        return ChainId.BNB_TESTNET

    @property
    def private_key_value(self) -> str | None:
        return self.private_key.get_secret_value() if self.private_key else None

    @property
    def privy_private_key_value(self) -> str | None:
        return (
            self.privy_private_key.get_secret_value()
            if self.privy_private_key
            else None
        )

    @property
    def mandated_authority_private_key_value(self) -> str | None:
        if self.mandated_authority_private_key is not None:
            return self.mandated_authority_private_key.get_secret_value()
        if self.wallet_mode == WalletMode.MANDATED_VAULT:
            return self.private_key_value
        return None

    @property
    def mandated_executor_private_key_value(self) -> str | None:
        if self.mandated_executor_private_key is not None:
            return self.mandated_executor_private_key.get_secret_value()
        return self.mandated_authority_private_key_value

    @property
    def mandated_bootstrap_private_key_value(self) -> str | None:
        if self.mandated_bootstrap_private_key is not None:
            return self.mandated_bootstrap_private_key.get_secret_value()
        if (
            self.wallet_mode == WalletMode.MANDATED_VAULT
            and self.private_key_value is not None
        ):
            return self.private_key_value
        return self.mandated_authority_private_key_value

    @property
    def mandated_bootstrap_signer_address(self) -> str | None:
        if self.mandated_bootstrap_private_key_value is not None:
            return Account.from_key(self.mandated_bootstrap_private_key_value).address
        return self.mandated_vault_authority

    @property
    def mandated_executor_address(self) -> str | None:
        if self.mandated_executor_private_key_value:
            return Account.from_key(self.mandated_executor_private_key_value).address
        return self.mandated_vault_authority

    @property
    def auth_signer_address(self) -> str | None:
        if self.wallet_mode == WalletMode.PREDICT_ACCOUNT:
            return self.predict_account_address
        if self.wallet_mode == WalletMode.EOA and self.private_key_value:
            return Account.from_key(self.private_key_value).address
        return None

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "PredictConfig":
        source = env or os.environ
        runtime_env = RuntimeEnv(source.get("PREDICT_ENV", RuntimeEnv.MAINNET.value))
        wallet_mode_override = _wallet_mode_or_none(source.get("PREDICT_WALLET_MODE"))
        private_key = _secret_or_none(source.get("PREDICT_EOA_PRIVATE_KEY"))
        predict_account_address = _value_or_none(source.get("PREDICT_ACCOUNT_ADDRESS"))
        privy_private_key = _secret_or_none(source.get("PREDICT_PRIVY_PRIVATE_KEY"))
        mandated_chain_id = _int_or_none(source.get("ERC_MANDATED_CHAIN_ID"))
        mandated_vault_address = _value_or_none(
            source.get("ERC_MANDATED_VAULT_ADDRESS")
        )
        mandated_factory_address = (
            _value_or_none(source.get("ERC_MANDATED_FACTORY_ADDRESS"))
            or MANDATED_FACTORY_ADDRESS_DEFAULT
        )
        raw_mandated_vault_asset_address = _value_or_none(
            source.get("ERC_MANDATED_VAULT_ASSET_ADDRESS")
        )
        raw_mandated_vault_name = _value_or_none(source.get("ERC_MANDATED_VAULT_NAME"))
        raw_mandated_vault_symbol = _value_or_none(
            source.get("ERC_MANDATED_VAULT_SYMBOL")
        )
        raw_mandated_vault_authority = _value_or_none(
            source.get("ERC_MANDATED_VAULT_AUTHORITY")
        )
        raw_mandated_vault_salt = _value_or_none(source.get("ERC_MANDATED_VAULT_SALT"))

        mandated_vault_asset_address = raw_mandated_vault_asset_address
        mandated_vault_name = raw_mandated_vault_name
        mandated_vault_symbol = raw_mandated_vault_symbol
        mandated_vault_authority = raw_mandated_vault_authority
        mandated_vault_salt = raw_mandated_vault_salt
        has_mandated_config_input = any(
            _value_or_none(source.get(env_name)) is not None
            for env_name in MANDATED_INPUT_ENV_NAMES
        )

        if (
            wallet_mode_override == WalletMode.MANDATED_VAULT
            and predict_account_address is not None
            and privy_private_key is not None
            and has_mandated_config_input
        ):
            raise _build_predict_account_overlay_route_conflict()

        if (
            wallet_mode_override == WalletMode.MANDATED_VAULT
            and mandated_vault_address is None
        ):
            if mandated_vault_asset_address is None:
                mandated_vault_asset_address = _default_mandated_vault_asset_address(
                    runtime_env, mandated_chain_id
                )
            if mandated_vault_name is None:
                mandated_vault_name = MANDATED_VAULT_NAME_DEFAULT
            if mandated_vault_symbol is None:
                mandated_vault_symbol = MANDATED_VAULT_SYMBOL_DEFAULT
            if mandated_vault_salt is None:
                mandated_vault_salt = MANDATED_VAULT_SALT_DEFAULT
            if mandated_vault_authority is None and private_key is not None:
                mandated_vault_authority = Account.from_key(
                    private_key.get_secret_value()
                ).address

        try:
            return cls(
                env=runtime_env,
                storage_dir=Path(
                    source.get("PREDICT_STORAGE_DIR", "~/.openclaw/predict")
                ).expanduser(),
                wallet_mode_override=wallet_mode_override,
                api_key=_secret_or_none(source.get("PREDICT_API_KEY")),
                private_key=private_key,
                predict_account_address=predict_account_address,
                privy_private_key=privy_private_key,
                mandated_vault_address=mandated_vault_address,
                mandated_factory_address=mandated_factory_address,
                mandated_vault_asset_address=mandated_vault_asset_address,
                mandated_vault_name=mandated_vault_name,
                mandated_vault_symbol=mandated_vault_symbol,
                mandated_vault_authority=mandated_vault_authority,
                mandated_vault_salt=mandated_vault_salt,
                mandated_authority_private_key=_secret_or_none(
                    source.get("ERC_MANDATED_AUTHORITY_PRIVATE_KEY")
                ),
                mandated_executor_private_key=_secret_or_none(
                    source.get("ERC_MANDATED_EXECUTOR_PRIVATE_KEY")
                ),
                mandated_bootstrap_private_key=_secret_or_none(
                    source.get("ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY")
                ),
                mandated_enable_broadcast=_bool_or_none(
                    source.get("ERC_MANDATED_ENABLE_BROADCAST")
                ),
                mandated_mcp_command=_value_or_none(
                    source.get("ERC_MANDATED_MCP_COMMAND")
                )
                or MANDATED_MCP_COMMAND_DEFAULT,
                mandated_contract_version=_value_or_none(
                    source.get("ERC_MANDATED_CONTRACT_VERSION")
                )
                or MANDATED_CONTRACT_VERSION_DEFAULT,
                mandated_chain_id=mandated_chain_id,
                mandated_allowed_adapters_root=_value_or_none(
                    source.get("ERC_MANDATED_ALLOWED_ADAPTERS_ROOT")
                )
                or MANDATED_ALLOWED_ADAPTERS_ROOT_DEFAULT,
                mandated_funding_max_amount_per_tx=_value_or_none(
                    source.get("ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX")
                ),
                mandated_funding_max_amount_per_window=_value_or_none(
                    source.get("ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW")
                ),
                mandated_funding_window_seconds=_int_or_none(
                    source.get("ERC_MANDATED_FUNDING_WINDOW_SECONDS")
                ),
                has_mandated_config_input=has_mandated_config_input,
                has_mandated_explicit_vault_input=mandated_vault_address is not None,
                has_any_mandated_derivation_input=any(
                    _value_or_none(source.get(env_name)) is not None
                    for env_name in MANDATED_DERIVATION_CORE_ENV_NAMES
                ),
                has_all_mandated_derivation_input=all(
                    _value_or_none(source.get(env_name)) is not None
                    for env_name in MANDATED_DERIVATION_CORE_ENV_NAMES
                ),
                openrouter_api_key=_secret_or_none(source.get("OPENROUTER_API_KEY")),
                model_name=_value_or_none(source.get("PREDICT_MODEL")),
                api_base_url=_value_or_none(source.get("PREDICT_API_BASE_URL"))
                or _default_api_base_url(runtime_env),
            )
        except (ValidationError, ValueError) as error:
            raise ConfigError(
                redact_text(
                    str(error),
                    [
                        source.get("PREDICT_API_KEY"),
                        source.get("PREDICT_EOA_PRIVATE_KEY"),
                        source.get("PREDICT_PRIVY_PRIVATE_KEY"),
                        source.get("ERC_MANDATED_AUTHORITY_PRIVATE_KEY"),
                        source.get("ERC_MANDATED_EXECUTOR_PRIVATE_KEY"),
                        source.get("ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY"),
                        source.get("OPENROUTER_API_KEY"),
                    ],
                )
            ) from error


def _value_or_none(raw: str | None) -> str | None:
    if raw is None:
        return None
    value = raw.strip()
    return value or None


def _secret_or_none(raw: str | None) -> SecretStr | None:
    value = _value_or_none(raw)
    return SecretStr(value) if value else None


def _wallet_mode_or_none(raw: str | None) -> WalletMode | None:
    value = _value_or_none(raw)
    return WalletMode(value) if value else None


def _int_or_none(raw: str | None) -> int | None:
    value = _value_or_none(raw)
    return int(value) if value else None


def _bool_or_none(raw: str | None) -> bool | None:
    value = _value_or_none(raw)
    if value is None:
        return None
    normalized = value.lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(
        "ERC_MANDATED_ENABLE_BROADCAST must be one of: 1, 0, true, false, yes, no, on, off."
    )


def _default_mandated_vault_asset_address(
    runtime_env: RuntimeEnv, mandated_chain_id: int | None
) -> str:
    selected_chain_id = mandated_chain_id
    if selected_chain_id is None:
        selected_chain_id = int(
            ChainId.BNB_MAINNET
            if runtime_env == RuntimeEnv.MAINNET
            else ChainId.BNB_TESTNET
        )
    asset_address = MANDATED_VAULT_ASSET_ADDRESS_BY_CHAIN_ID.get(selected_chain_id)
    if asset_address is None:
        raise ValueError(
            "No default ERC_MANDATED_VAULT_ASSET_ADDRESS is configured for the selected chain."
        )
    return asset_address


def mandated_vault_v1_unsupported_error(flow: str) -> ConfigError:
    return ConfigError(
        f"{flow}: {MANDATED_VAULT_V1_UNSUPPORTED_CODE}. "
        "mandated-vault v1 currently covers protected funding/control-plane operations "
        "and does not provide predict.fun trading parity."
    )
