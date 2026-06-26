"""
Supabase 客户端 — 可选，用于巨鲸数据持久化去重
如果没有配置 SUPABASE_URL / SUPABASE_KEY 则所有方法静默跳过
"""

from __future__ import annotations

from config.settings import settings


class SupabaseClient:

    def __init__(self):
        self.client = None
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                from supabase import create_client

                self.client = create_client(
                    settings.SUPABASE_URL, settings.SUPABASE_KEY
                )
            except Exception:
                self.client = None

    @property
    def available(self) -> bool:
        return self.client is not None

    def get_existing_trade_hashes(self) -> set[str]:
        if not self.client:
            return set()
        try:
            resp = (
                self.client.table("whale_trades")
                .select("transaction_hash")
                .execute()
            )
            return {r["transaction_hash"] for r in (resp.data or [])}
        except Exception:
            return set()

    def insert_whale_trades(self, trades: list[dict]) -> int:
        if not self.client or not trades:
            return 0
        try:
            self.client.table("whale_trades").insert(trades).execute()
            return len(trades)
        except Exception:
            return 0
