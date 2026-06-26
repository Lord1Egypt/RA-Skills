# -*- coding: utf-8 -*-
"""
DirectionChecker - 涨跌 / 收益率方向一致性校验
检查相关市场指标的方向是否与已知逻辑一致。
例如：
  - VIX 上涨 → 市场恐慌，股市通常下跌（正向关联场景）
  - 美债收益率与债券价格反向（可通过 change 符号推断）
  - 黄金与美元指数通常反向
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


# ── 一致性规则定义 ─────────────────────────────────
# 同向规则：两者变化方向应一致（同正或同负）
SAME_SIGN_RULES = [
    # 黄金与白银同向
    ("现货黄金(XAUUSD)", "现货白银(XAGUSD)"),
    ("COMEX黄金期货", "COMEX白银期货"),
    # A股各指数同向
    ("上证指数", "深证成指"),
    ("上证指数", "创业板指"),
    ("深证成指", "沪深300"),
    # 港股各指数同向
    ("恒生指数", "恒生科技指数"),
    ("恒生指数", "国企指数"),
    # 欧洲各指数同向
    ("德国DAX 30", "法国CAC 40"),
    ("德国DAX 30", "英国富时100"),
    # 亚太各指数同向
    ("日经225指数", "韩国综合指数"),
    ("日经225指数", "澳洲S&P/ASX 200"),
]

# 反向规则：两者变化方向应相反
OPPOSITE_SIGN_RULES = [
    # 黄金与美元指数反向
    ("现货黄金(XAUUSD)", "美元指数(DXY)"),
    ("COMEX黄金期货", "美元指数(DXY)"),
    # 美债收益率与债券价格反向（收益率下降 → 债券价格上涨）
    # 注意：change 记录的是收益率变化，非债券价格
    # 美债收益率与美股：收益率↑ → 股市承压（反向关联，但非严格反向）
]


def _sign(v):
    if v is None:
        return 0
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


class DirectionChecker:
    """
    规则 5：涨跌 / 收益率方向一致性校验

    对已知相关品种检查变化方向是否合理。
    仅发出警告，不直接拒绝（方向性问题属于软约束）。
    """

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()
        market = data.get("市场表现", {})

        # 建立名称→change 映射
        changes = {}
        for region, items in market.items():
            if not isinstance(items, dict):
                continue
            for name, fields in items.items():
                if isinstance(fields, dict):
                    ch = fields.get("change")
                    if ch is not None and isinstance(ch, (int, float)):
                        changes[name] = ch

        # 检查同向规则
        for name_a, name_b in SAME_SIGN_RULES:
            a_ch = changes.get(name_a)
            b_ch = changes.get(name_b)
            if a_ch is None or b_ch is None:
                continue

            sign_a = _sign(a_ch)
            sign_b = _sign(b_ch)
            if sign_a != 0 and sign_b != 0 and sign_a != sign_b:
                # 符号相反
                result.fail(
                    rule="方向一致性",
                    category="同向规则",
                    key=f"{name_a} vs {name_b}",
                    value=f"{a_ch}% vs {b_ch}%",
                    message=f"{name_a}({a_ch}%) 与 {name_b}({b_ch}%) 变化方向不一致（预期同向）"
                )

        # 检查反向规则
        for name_a, name_b in OPPOSITE_SIGN_RULES:
            a_ch = changes.get(name_a)
            b_ch = changes.get(name_b)
            if a_ch is None or b_ch is None:
                continue

            sign_a = _sign(a_ch)
            sign_b = _sign(b_ch)
            # 反向：符号应相反（同正或同负 → 违反规则）
            if sign_a != 0 and sign_b != 0 and sign_a == sign_b:
                result.fail(
                    rule="方向一致性",
                    category="反向规则",
                    key=f"{name_a} vs {name_b}",
                    value=f"{a_ch}% vs {b_ch}%",
                    message=f"{name_a}({a_ch}%) 与 {name_b}({b_ch}%) 变化方向相同（预期反向）"
                )

        return result