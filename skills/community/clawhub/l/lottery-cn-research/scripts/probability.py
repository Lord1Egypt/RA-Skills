# -*- coding: utf-8 -*-
"""
probability.py — 各彩种中奖概率与期望收益(EV)计算

用法:
  python probability.py --game ssq
  python probability.py --game dlt --jackpot 10000000   # 设定一等奖估算奖池(元)
  python probability.py --all                            # 列出全部彩种概要

计算方式:
  - 双色球/大乐透: 超几何分布精确计算各奖级概率
  - 3D/排列3/排列5/七星彩/快乐8/七乐彩: 组合数精确计算
  - 期望收益 = Σ(奖金额 × 中奖概率) − 单注成本
  - 浮动奖(一/二等奖)使用估算值: 一等奖由 --jackpot 控制, 二等奖用典型值

说明: 浮动奖的"典型值"仅为研究估算, 实际随奖池与中奖人数浮动。返奖率固定,
单注期望长期为负。本工具用于理解概率, 非购彩建议。
依赖: 仅标准库 + lottery_core.py
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lottery_core as core

# 浮动二等奖的"典型估算值"(仅研究参考, 实际浮动)
SECOND_EST = {"ssq": 150_000, "dlt": 300_000, "qlc": 50_000, "qxc": 80_000}
# 各彩种一等奖默认估算奖池(元)。双色球/大乐透可达千万级; 七乐彩/七星彩/快乐8 较小。
DEFAULT_JACKPOT = {"ssq": 8_000_000, "dlt": 8_000_000, "qlc": 1_000_000,
                   "qxc": 5_000_000, "kl8": 5_000_000}


def prob_dual(Nr, cr, Nb, cb, k, b):
    """双池彩: 红球(前区)中 k 个, 蓝球(后区)中 b 个的概率。"""
    return core.hypergeom(Nr, cr, cr, k) * core.hypergeom(Nb, cb, cb, b)


def ssq_tiers(jackpot):
    t = []
    t.append(("一等奖", prob_dual(33, 6, 16, 1, 6, 1), jackpot, "浮动(基本最高1000万)"))
    t.append(("二等奖", prob_dual(33, 6, 16, 1, 6, 0), SECOND_EST["ssq"], "浮动(典型值)"))
    t.append(("三等奖", prob_dual(33, 6, 16, 1, 5, 1), 3000, "固定"))
    t.append(("四等奖", prob_dual(33, 6, 16, 1, 5, 0) + prob_dual(33, 6, 16, 1, 4, 1), 200, "固定"))
    t.append(("五等奖", prob_dual(33, 6, 16, 1, 4, 0) + prob_dual(33, 6, 16, 1, 3, 1), 10, "固定"))
    t.append(("六等奖", prob_dual(33, 6, 16, 1, 2, 1) + prob_dual(33, 6, 16, 1, 1, 1)
              + prob_dual(33, 6, 16, 1, 0, 1), 5, "固定"))
    return t, 2, core.combinations(33, 6) * 16


def dlt_tiers(jackpot):
    # 大乐透 9 奖级(2019 升级后现行规则, 来源: 中国体彩网 / Wikiwand)
    # 中奖条件 = (前区命中数 + 后区命中数)。任一注只兑最高奖级。
    def p(k, m):
        return prob_dual(35, 5, 12, 2, k, m)
    t = []
    t.append(("一等奖", p(5, 2), jackpot, "浮动(基本最高1000万, 追加+80%)"))
    t.append(("二等奖", p(5, 1), SECOND_EST["dlt"], "浮动(典型值, 追加+80%)"))
    t.append(("三等奖", p(5, 0), 10000, "固定"))
    t.append(("四等奖", p(4, 2), 3000, "固定"))
    t.append(("五等奖", p(4, 1), 300, "固定"))
    t.append(("六等奖", p(3, 2), 200, "固定"))
    t.append(("七等奖", p(4, 0), 100, "固定"))
    t.append(("八等奖", p(3, 1) + p(2, 2), 15, "固定"))
    t.append(("九等奖", p(3, 0) + p(2, 1) + p(1, 2) + p(0, 2), 5, "固定"))
    return t, 2, core.combinations(35, 5) * core.combinations(12, 2)


def simple_tiers(game, jackpot):
    # 以下为"不同投注方式", 彼此互斥(一注只选一种方式), 故 EV 须按方式分别算
    if game in ("fc3d", "pl3"):
        total = 1000
        t = [
            ("直选", 1 / 1000, 1040, "固定(百位=十位=个位顺序全中)"),
            ("组选三", 3 / 1000, 346, "固定(押注含两同的三数字, 3种排列中奖)"),
            ("组选六", 6 / 1000, 173, "固定(押注全不同的三数字, 6种排列中奖)"),
        ]
        return t, 2, total, "bets"
    if game == "pl5":
        total = 100000
        return [("直选", 1 / 100000, 100000, "固定(五位顺序全中)")], 2, total, "bets"
    if game == "qxc":
        total = 10 ** 7
        return [("一等奖(7位)", 1 / total, jackpot, "浮动(最高500万)"),
                ("二等奖(连续6位)", 1 / (10 ** 6), SECOND_EST["qxc"], "浮动(典型值)")], 2, total, "bets"
    if game == "kl8":
        total = core.combinations(80, 20)
        # 选十: 中k个 = C(20,k) * C(60,10-k) / C(80,20)
        t = [
            ("选十中十", core.combinations(20, 10) / total, jackpot, "浮动(最高500万)"),
            ("选十中九", core.combinations(20, 9) * core.combinations(60, 1) / total, 8000, "固定"),
            ("选十中八", core.combinations(20, 8) * core.combinations(60, 2) / total, 200, "固定"),
        ]
        return t, 2, total, "bets"
    if game == "qlc":
        total = core.combinations(30, 7)
        t = [
            ("一等奖(7基本)", 1 / total, jackpot, "浮动(典型值)"),
            ("二等奖(6+特别)", 7 / total, SECOND_EST["qlc"], "浮动(典型值)"),
        ]
        return t, 2, total, "outcome"
    return None, 2, 0, "outcome"


def compute_ev(tiers, cost):
    ev = 0.0
    for name, p, prize, kind in tiers:
        ev += prize * p
    return_ev = ev / cost
    return ev, return_ev


def render(game, tiers, cost, total, jackpot, mode):
    cfg = core.GAME_CONFIG[game]
    lines = []
    lines.append("=" * 64)
    lines.append("%s (%s) 概率与期望分析" % (cfg["name"], game))
    lines.append("总组合数: %s   单注: %d元   官方返奖率: %.0f%%"
                 % (format(total, ",d"), cost, cfg["payout_ratio"] * 100))
    lines.append("=" * 64)
    lines.append("%-12s %-20s %-12s %s" % ("奖级/方式", "中奖概率", "奖金(元)", "类型"))
    lines.append("-" * 64)
    for name, p, prize, kind in tiers:
        pstr = ("1/%s" % format(round(1 / p), ",d")) if p > 0 else "0"
        pstr = ("≈%.2e" % p) if (p > 0 and p < 1e-4) else pstr
        prize_str = format(int(prize), ",d")
        lines.append("%-12s %-20s %-12s %s" % (name, pstr, prize_str, kind))
    if mode == "outcome":
        ev, return_ev = compute_ev(tiers, cost)
        lines.append("-" * 64)
        lines.append("期望返还: %.4f 元/注  →  返奖率 %.2f%%" % (ev, return_ev * 100))
        lines.append("期望净收益: %.4f 元/注 (长期必为负)" % (ev - cost))
    else:
        # 不同投注方式互斥: 分别列出各方式返奖率
        lines.append("-" * 64)
        lines.append("各投注方式独立, 以下为单方式期望返还:")
        for name, p, prize, kind in tiers:
            r = prize * p / cost * 100
            rstr = ("%.2f%%" % r) if r >= 0.01 else ("≈%.4f%%" % r)
            lines.append("  %-12s 返奖率 %s" % (name, rstr))
        lines.append("任一方式期望净收益均为负(返奖率恒<100%%)")
    lines.append("")
    return "\n".join(lines)


def get_tiers(game, jackpot):
    if game == "ssq":
        return ssq_tiers(jackpot) + ("outcome",)
    if game == "dlt":
        return dlt_tiers(jackpot) + ("outcome",)
    return simple_tiers(game, jackpot)


def main():
    ap = argparse.ArgumentParser(description="彩票概率与期望计算")
    ap.add_argument("--game", default="ssq")
    ap.add_argument("--all", action="store_true", help="列出全部彩种概要")
    ap.add_argument("--jackpot", type=float, default=None, help="一等奖估算奖金额(元), 不填则用该彩种默认值")
    args = ap.parse_args()

    if args.all:
        for g in core.GAME_CONFIG:
            jp = args.jackpot if args.jackpot is not None else DEFAULT_JACKPOT.get(g, 8_000_000)
            tiers, cost, total, mode = get_tiers(g, jp)
            print(render(g, tiers, cost, total, jp, mode))
        return

    game = core.resolve_game(args.game)
    jp = args.jackpot if args.jackpot is not None else DEFAULT_JACKPOT.get(game, 8_000_000)
    tiers, cost, total, mode = get_tiers(game, jp)
    print(render(game, tiers, cost, total, jp, mode))


if __name__ == "__main__":
    main()
