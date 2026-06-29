"""读取 policies.yaml，对每个 action 执行三级权限检查。"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml
import structlog

CONFIG_DIR = Path(__file__).parent.parent / "config"
logger = structlog.get_logger(__name__)


class PolicyViolationError(Exception):
    """当 action 被 forbidden 策略拒绝时抛出。"""


class ConfirmationRequiredError(Exception):
    """当 action 需要用户确认时抛出，携带执行计划供上层展示。"""

    def __init__(self, action: str, plan: dict | None = None) -> None:
        self.action = action
        self.plan = plan or {}
        super().__init__(f"Action '{action}' requires confirmation before execution.")


class PolicyEngine:
    def __init__(self, config_dir: Path = CONFIG_DIR) -> None:
        self._config_dir = config_dir
        self._policies: dict = {}
        self._loaded = False

    def load(self) -> None:
        path = self._config_dir / "policies.yaml"
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self._policies = data.get("policies", {})
        self._loaded = True

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def _resolve_policy(self, environment: str) -> dict[str, set[str]]:
        """合并 default + environment 特定策略，返回三个 set。"""
        self._ensure_loaded()
        default = self._policies.get("default", {})
        env_policy = self._policies.get(environment, {})

        readonly = set(default.get("readonly_allowed", []))
        confirm = set(default.get("confirmation_required", []))
        forbidden = set(default.get("forbidden", []))

        # 应用环境扩展
        readonly |= set(env_policy.get("readonly_allowed_extra", []))
        readonly -= set(env_policy.get("readonly_allowed_remove", []))
        confirm |= set(env_policy.get("confirmation_required_extra", []))
        confirm -= set(env_policy.get("confirmation_required_remove", []))

        return {"readonly": readonly, "confirm": confirm, "forbidden": forbidden}

    def check(self, action: str, environment: str = "test", plan: dict | None = None) -> None:
        """
        检查 action 是否允许执行。

        - forbidden：抛出 PolicyViolationError（记录审计日志）
        - confirmation_required：抛出 ConfirmationRequiredError（上层展示计划，等待确认）
        - readonly_allowed：正常通过
        - 未知 action：默认当作 confirmation_required 处理
        """
        policy = self._resolve_policy(environment)

        if action in policy["forbidden"]:
            logger.warning(
                "policy_violation",
                action=action,
                environment=environment,
                reason="action is in forbidden list",
            )
            raise PolicyViolationError(
                f"操作 '{action}' 已被安全策略禁止，无法执行。"
                f"（环境：{environment}）"
            )

        if action in policy["confirm"]:
            logger.info("confirmation_required", action=action, environment=environment)
            raise ConfirmationRequiredError(action=action, plan=plan)

        if action in policy["readonly"]:
            logger.debug("policy_allowed", action=action, environment=environment)
            return

        # 未知 action 保守处理
        logger.info(
            "unknown_action_requires_confirmation",
            action=action,
            environment=environment,
        )
        raise ConfirmationRequiredError(action=action, plan=plan)

    def is_readonly(self, action: str, environment: str = "test") -> bool:
        policy = self._resolve_policy(environment)
        return action in policy["readonly"]

    def is_forbidden(self, action: str, environment: str = "test") -> bool:
        policy = self._resolve_policy(environment)
        return action in policy["forbidden"]
