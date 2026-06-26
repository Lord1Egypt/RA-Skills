"""长桥 OpenAPI 配置初始化"""
import os
from pathlib import Path

import click
from longbridge.openapi import Config


# ---------------------------------------------------------------------------
# .env 加载（CLI 包自包含，不依赖 trader 包）
# ---------------------------------------------------------------------------

def _load_dotenv_for_profile(profile: str | None = None) -> None:
    """Load .env (or .{profile}.env) into os.environ.

    查找顺序: cwd → home dir。
    profile=None + 文件不存在 → 静默跳过（向后兼容）。
    profile 非空 + 文件不存在 → 抛 FileNotFoundError。
    已存在的环境变量不会被覆盖。
    """
    filename = f".{profile}.env" if profile else ".env"
    env_path: Path | None = None
    for base in [Path.cwd(), Path.home()]:
        candidate = base / filename
        if candidate.is_file():
            env_path = candidate
            break

    if env_path is None:
        if profile is not None:
            raise FileNotFoundError(
                f"Profile '{profile}' 的 env 文件未找到。"
                f"请在当前目录或主目录创建 {filename}"
            )
        return

    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


# 下单权限控制：设置 LONGBRIDGE_TRADE_ENABLED=true 才允许 buy/sell/cancel
_TRADE_ENV_VAR = "LONGBRIDGE_TRADE_ENABLED"


def is_trade_enabled() -> bool:
    """返回是否已开启交易权限（默认关闭，只读模式）"""
    return os.environ.get(_TRADE_ENV_VAR, "").strip().lower() == "true"


def require_trade_enabled() -> None:
    """若未开启交易权限，抛出友好错误并提示配置方式"""
    if not is_trade_enabled():
        raise click.ClickException(
            "当前为只读模式，下单/撤单操作已禁用。\n"
            f"如需开启交易权限，请设置环境变量：\n"
            f"  export {_TRADE_ENV_VAR}=true\n"
            "⚠️  开启后请确保操作正确，下单指令将直接提交至长桥交易系统。"
        )


def get_config(profile: str | None = None) -> Config:
    """从环境变量初始化长桥配置。支持 --profile 切换账户。

    需要设置以下环境变量：
        LONGBRIDGE_APP_KEY
        LONGBRIDGE_APP_SECRET
        LONGBRIDGE_ACCESS_TOKEN
    """
    _load_dotenv_for_profile(profile)
    try:
        return Config.from_apikey_env()
    except Exception as e:
        raise click.ClickException(
            "无法初始化长桥配置，请确认已设置以下环境变量：\n"
            "  LONGBRIDGE_APP_KEY\n"
            "  LONGBRIDGE_APP_SECRET\n"
            "  LONGBRIDGE_ACCESS_TOKEN\n"
            f"错误详情：{e}"
        )
