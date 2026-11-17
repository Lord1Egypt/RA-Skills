"""
PaperTrade + ONDO Perps 中性对冲机器人

策略原理：
1. 在 PaperTrade 和 ONDO 同时开方向相反的仓位（对冲）
2. 无论价格涨跌，PaperTrade 一侧必然亏损 →  mint PAPER 代币（100 PAPER/$1 亏损）
3. ONDO 一侧必然盈利 → 获得交易积分 + USDC
4. 净 PnL 接近 0（仅扣除 ONDO 手续费约 0.05% 往返）
5. 收益 = PAPER 代币 + ONDO 积分

PaperTrade 的关键特性：
- 亏损不额外收费，反而 mint PAPER
- 盈利有 asymmetric impact 扣减（小盈利几乎被吃光）
- 因此亏损侧在 PaperTrade 是"划算"的
"""
from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass, field
from typing import Optional

from paper_client import PaperTradeClient, INSTRUMENTS
from ondo_client import OndoClient, OndoConfig


@dataclass
class HedgeConfig:
    symbol: str = "BTC"              # 交易对：BTC 或 ETH
    position_size_usd: float = 50.0  # 每侧名义仓位价值 (USD)
    paper_leverage: int = 10         # PaperTrade 杠杆
    ondo_leverage: int = 10          # ONDO 杠杆
    target_move_pct: float = 1.0     # 触发平仓的价格变动百分比
    max_hold_seconds: int = 3600     # 最长持仓时间（秒）
    poll_interval: int = 10          # 价格轮询间隔（秒）
    max_cycles: int = 200            # 最大循环轮次
    direction: str = "random"        # "random" | "paper_long" | "paper_short"
    ondo_market: Optional[str] = None  # ONDO 市场名，默认 {symbol}-USD.P


@dataclass
class CycleStats:
    cycle: int
    direction: str
    entry_price: float
    exit_price: float
    move_pct: float
    paper_pnl: float
    ondo_pnl: float
    paper_minted: float
    ondo_volume: float
    net_pnl: float
    duration_sec: float


class HedgeBot:
    def __init__(
        self,
        paper: PaperTradeClient,
        ondo: OndoClient,
        config: HedgeConfig,
    ):
        self.paper = paper
        self.ondo = ondo
        self.config = config
        self.stats: list[CycleStats] = []
        self.total_paper_minted = 0.0
        self.total_ondo_volume = 0.0
        self.ondo_market = config.ondo_market or f"{config.symbol}-USD.P"

    def run(self):
        print("=" * 60)
        print("PaperTrade + ONDO 中性对冲机器人启动")
        print(f"交易对: {self.config.symbol} | 仓位: ${self.config.position_size_usd}")
        print(f"PaperTrade 杠杆: {self.config.paper_leverage}x | ONDO 杠杆: {self.config.ondo_leverage}x")
        print(f"目标波动: {self.config.target_move_pct}% | 最大持仓: {self.config.max_hold_seconds}s")
        print(f"最大循环: {self.config.max_cycles}")
        print("=" * 60)

        # 检查初始余额
        self._check_balances()

        for cycle in range(1, self.config.max_cycles + 1):
            print(f"\n{'─' * 60}")
            print(f"第 {cycle}/{self.config.max_cycles} 轮")
            try:
                stat = self._run_cycle(cycle)
                if stat:
                    self.stats.append(stat)
                    self.total_paper_minted += stat.paper_minted
                    self.total_ondo_volume += stat.ondo_volume
                    self._print_cycle_summary(stat)
            except Exception as e:
                print(f"[错误] 第 {cycle} 轮失败: {e}")
                # 尝试清理持仓
                self._emergency_close()
                time.sleep(30)

            self._print_total_summary()

    def _check_balances(self):
        paper_bal = self.paper.get_balance_usd()
        ondo_bal = self.ondo.get_balance()
        ondo_usd = self._extract_ondo_usd(ondo_bal)
        print(f"[余额] PaperTrade: ${paper_bal:.2f} | ONDO: ${ondo_usd:.2f}")
        min_required = self.config.position_size_usd / self.config.paper_leverage * 1.5
        if paper_bal < min_required:
            print(f"[警告] PaperTrade 余额不足 ${min_required:.2f}，可能无法开仓")

    def _extract_ondo_usd(self, ondo_bal) -> float:
        """从 ONDO 余额响应中提取可用 USD（兼容多种结构）"""
        if isinstance(ondo_bal, (int, float)):
            return float(ondo_bal)
        if isinstance(ondo_bal, dict):
            for key in ("freeCollateral", "availableBalance", "balance", "free", "collateral", "usdc"):
                val = ondo_bal.get(key)
                if val is not None:
                    try:
                        return float(val)
                    except (TypeError, ValueError):
                        continue
        return 0.0

    def _get_ondo_pnl(self) -> float:
        """获取 ONDO 当前持仓的未实现 PnL"""
        try:
            positions = self.ondo.get_positions()
            for pos in positions:
                if pos.get("market") == self.ondo_market:
                    for key in ("unrealizedPnl", "pnl", "uPnl", "profit", "unrealizedProfit"):
                        val = pos.get(key)
                        if val is not None:
                            return float(val)
            return 0.0
        except Exception:
            return 0.0

    def _choose_direction(self) -> tuple[bool, str]:
        """返回 (paper_is_long, ondo_side)"""
        if self.config.direction == "paper_long":
            return True, "sell"
        elif self.config.direction == "paper_short":
            return False, "buy"
        else:
            paper_long = random.choice([True, False])
            return paper_long, "sell" if paper_long else "buy"

    def _wait_for_paper_position(self, symbol: str, timeout: int = 60) -> bool:
        """等待 PaperTrade 意图执行并在链上看到持仓"""
        deadline = time.time() + timeout
        target_id = INSTRUMENTS[symbol]["id"]
        while time.time() < deadline:
            try:
                positions = self.paper.get_positions()
                if any(int(p["instrumentId"]) == target_id for p in positions):
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False

    def _run_cycle(self, cycle: int) -> Optional[CycleStats]:
        # 1. 选择方向
        paper_is_long, ondo_side = self._choose_direction()
        direction = "Paper多/ONDO空" if paper_is_long else "Paper空/ONDO多"
        print(f"[方向] {direction}")

        # 2. 获取入场价格
        entry_price = self.ondo.get_mark_price(self.ondo_market)
        print(f"[入场] {self.ondo_market} 价格: ${entry_price:.2f}")

        # 3. 同时开仓（先 PaperTrade 再 ONDO，尽量缩短时间差）
        margin_usd = self.config.position_size_usd / self.config.paper_leverage
        paper_opened = False
        ondo_opened = False
        try:
            paper_resp = self.paper.open_position(
                symbol=self.config.symbol,
                is_long=paper_is_long,
                margin_usd=margin_usd,
                leverage=self.config.paper_leverage,
            )
            paper_opened = True
            print(f"[开仓] PaperTrade intentId={paper_resp.get('intentId', '?')}")
        except Exception as e:
            print(f"[失败] PaperTrade 开仓失败: {e}")
            return None

        try:
            self.ondo.place_market_order(
                market=self.ondo_market,
                side=ondo_side,
                size_usd=self.config.position_size_usd,
                leverage=self.config.ondo_leverage,
            )
            ondo_opened = True
        except Exception as e:
            print(f"[失败] ONDO 开仓失败: {e}")
            # 回滚：平掉 PaperTrade 仓位
            print("[回滚] 正在平掉 PaperTrade 仓位...")
            try:
                self.paper.close_all(symbol=self.config.symbol)
            except Exception as re:
                print(f"[回滚失败] 请手动平掉 PaperTrade 仓位: {re}")
            return None

        # 4. 等待 PaperTrade 仓位执行（避免平仓时找不到仓位）
        print("[等待] 等待 PaperTrade 仓位上链...")
        if not self._wait_for_paper_position(self.config.symbol):
            print("[警告] PaperTrade 仓位未在超时内确认，继续监控但可能平仓失败")

        # 5. 监控价格，等待目标波动或超时
        start_time = time.time()
        exit_price = entry_price
        while True:
            time.sleep(self.config.poll_interval)
            current_price = self.ondo.get_mark_price(self.ondo_market)
            move_pct = (current_price - entry_price) / entry_price * 100

            elapsed = time.time() - start_time
            print(f"  [监控] 价格: ${current_price:.2f} | 波动: {move_pct:+.3f}% | "
                  f"已持仓: {elapsed:.0f}s", end="\r")

            # 达到目标波动
            if abs(move_pct) >= self.config.target_move_pct:
                exit_price = current_price
                print(f"\n[触发] 达到目标波动 {move_pct:+.3f}%")
                break

            # 超时
            if elapsed >= self.config.max_hold_seconds:
                exit_price = current_price
                print(f"\n[超时] 持仓超过 {self.config.max_hold_seconds}s，平仓")
                break

        # 6. 平仓
        paper_before = self.paper.get_paper_minted()
        ondo_pnl = self._get_ondo_pnl()  # 平仓前获取 ONDO 未实现 PnL
        self.paper.close_all(symbol=self.config.symbol)
        self.ondo.close_position(self.ondo_market)

        # 等待结算（PAPER mint 可能有延迟）
        time.sleep(5)

        # 7. 统计
        paper_after = self.paper.get_paper_minted()
        paper_minted = max(0, paper_after - paper_before)

        move_pct = (exit_price - entry_price) / entry_price * 100
        # PaperTrade PnL: 做多则 move_pct 为正盈利，做空相反
        paper_pnl_raw = move_pct / 100 * self.config.position_size_usd * (1 if paper_is_long else -1)
        # PaperTrade 亏损 mint PAPER，盈利有 haircut
        paper_pnl = paper_pnl_raw if paper_pnl_raw < 0 else paper_pnl_raw * 0.85  # 粗略估算 haircut
        # ONDO PnL 优先使用实际查询值，否则用对冲估算
        if ondo_pnl == 0.0:
            ondo_pnl = -paper_pnl_raw * 0.999  # 近似对冲，扣 0.05% 手续费

        return CycleStats(
            cycle=cycle,
            direction=direction,
            entry_price=entry_price,
            exit_price=exit_price,
            move_pct=move_pct,
            paper_pnl=paper_pnl,
            ondo_pnl=ondo_pnl,
            paper_minted=paper_minted,
            ondo_volume=self.config.position_size_usd * 2,
            net_pnl=paper_pnl + ondo_pnl,
            duration_sec=time.time() - start_time,
        )

    def _emergency_close(self):
        try:
            print("[紧急] 尝试平掉所有持仓...")
            self.paper.close_all()
            self.ondo.close_all()
        except Exception as e:
            print(f"[紧急] 平仓失败: {e}")

    def _print_cycle_summary(self, s: CycleStats):
        print(f"\n{'─' * 40}")
        print(f"本轮结果:")
        print(f"  方向: {s.direction}")
        print(f"  入场: ${s.entry_price:.2f} → 出场: ${s.exit_price:.2f} ({s.move_pct:+.3f}%)")
        print(f"  PaperTrade PnL: ${s.paper_pnl:+.4f} | ONDO PnL: ${s.ondo_pnl:+.4f}")
        print(f"  净 PnL: ${s.net_pnl:+.4f}")
        print(f"  PAPER minted: {s.paper_minted:.2f}")
        print(f"  ONDO 交易量: ${s.ondo_volume:.2f}")
        print(f"  耗时: {s.duration_sec:.0f}s")

    def _print_total_summary(self):
        n = len(self.stats)
        if n == 0:
            return
        avg_pnl = sum(s.net_pnl for s in self.stats) / n
        total_pnl = sum(s.net_pnl for s in self.stats)
        print(f"\n[累计] {n} 轮 | 净 PnL: ${total_pnl:+.4f} | 平均: ${avg_pnl:+.4f}")
        print(f"[累计] PAPER 总量: {self.total_paper_minted:.2f} | ONDO 交易量: ${self.total_ondo_volume:.2f}")

    def export_stats(self, path: str = "hedge_stats.json"):
        data = {
            "total_cycles": len(self.stats),
            "total_paper_minted": self.total_paper_minted,
            "total_ondo_volume": self.total_ondo_volume,
            "total_net_pnl": sum(s.net_pnl for s in self.stats),
            "cycles": [s.__dict__ for s in self.stats],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"[统计] 已导出到 {path}")
