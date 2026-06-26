"""
Initialize pmbuysell config files for agents/users.

This CLI creates `pmbuysell/.env` from `pmbuysell/.env.example` (or a minimal template)
so that an AI agent has a deterministic command to run and a deterministic path to edit.

Usage:
  python -m pmbuysell.skills.init_cli
  python -m pmbuysell.skills.init_cli --force
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def _minimal_env_template() -> str:
    return "\n".join(
        [
            "# pmbuysell .env (generated)",
            "# 账号配置（二选一：推荐用 PM_ACCOUNT_IDS + ACCx_*）",
            "PM_ACCOUNT_IDS=ACC1",
            "ACC1_PRIVATE_KEY=0xYOUR_PRIVATE_KEY",
            "ACC1_FUNDER=0xYOUR_FUNDER_ADDRESS",
            "",
            "# 可选：CLOB / chain",
            "CLOB_HOST=https://clob.polymarket.com",
            "CHAIN_ID=137",
            "",
            "# 可选：amount=0 自动下注",
            "AUTO_BUY_MIN_AMOUNT=1",
            "AUTO_BUY_MAX_AMOUNT=50",
            "BALANCE_CACHE_TTL_SEC=10",
            "",
            "# 可选：自动结算（redeem）— 付费模块 pmbuysell_redeem 所需",
            "# RELAYER_URL=https://relayer-v2.polymarket.com/",
            "# ACC1_BUILDER_API_KEY=your_builder_api_key",
            "# ACC1_BUILDER_SECRET=your_builder_secret",
            "# ACC1_BUILDER_PASSPHRASE=your_builder_passphrase",
            "",
        ]
    ) + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description="Initialize pmbuysell/.env from template")
    p.add_argument("--force", action="store_true", help="覆盖已存在的 .env（谨慎）")
    args = p.parse_args()

    base_dir = Path(__file__).resolve().parents[1]  # .../pmbuysell
    env_path = base_dir / ".env"
    example_path = base_dir / ".env.example"

    if env_path.exists() and not args.force:
        print(f"SKIP: {env_path} 已存在（如需覆盖请加 --force）")
        sys.exit(0)

    if example_path.exists():
        content = example_path.read_text(encoding="utf-8")
        if not content.strip():
            content = _minimal_env_template()
        env_path.write_text(content, encoding="utf-8")
        print(f"OK: 已从 {example_path.name} 生成 {env_path}")
        sys.exit(0)

    env_path.write_text(_minimal_env_template(), encoding="utf-8")
    print(f"OK: 已生成 {env_path}（minimal template）")
    sys.exit(0)


if __name__ == "__main__":
    main()

