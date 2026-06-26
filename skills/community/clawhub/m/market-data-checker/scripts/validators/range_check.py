# -*- coding: utf-8 -*-
"""
RangeChecker - 业务范围合理性校验
检查各市场指标的数值是否在合理范围内（如债券收益率 ±10%、汇率 ±50 等）。
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


# ── 各品种合理范围定义 ─────────────────────────────────
RANGE_RULES = {
    # 市场表现 - 美国股市
    "标普500指数":        {"price": (1000, 10000), "change": (-15, 15)},
    "纳斯达克综合指数":   {"price": (5000, 60000), "change": (-15, 15)},
    "道琼斯工业平均指数": {"price": (20000, 60000), "change": (-15, 15)},
    "VIX恐慌指数":        {"price": (5, 100), "change": (-50, 50)},
    "罗素2000指数":       {"price": (500, 5000), "change": (-20, 20)},

    # 美国债券与外汇
    "10年期美债收益率":   {"price": (0, 15), "change": (-50, 50), "unit": "%"},
    "2年期美债收益率":    {"price": (0, 15), "change": (-50, 50), "unit": "%"},
    "美元指数(DXY)":      {"price": (80, 130), "change": (-5, 5)},
    "美国国债收益率利差": {"price": (-2, 5), "change": (-50, 50)},

    # 美国大宗商品
    "WTI原油期货":        {"price": (20, 200), "change": (-15, 15)},
    "布伦特原油":         {"price": (20, 200), "change": (-15, 15)},
    "COMEX黄金期货":      {"price": (1000, 6000), "change": (-15, 15)},
    "现货黄金(XAUUSD)":   {"price": (1000, 6000), "change": (-15, 15)},
    "COMEX白银期货":      {"price": (10, 100), "change": (-20, 20)},
    "现货白银(XAGUSD)":   {"price": (10, 100), "change": (-20, 20)},

    # A股
    "上证指数":           {"price": (1500, 8000), "change": (-15, 15)},
    "深证成指":           {"price": (3000, 20000), "change": (-15, 15)},
    "创业板指":           {"price": (500, 5000), "change": (-20, 20)},
    "沪深300":            {"price": (1000, 8000), "change": (-15, 15)},
    "科创50":             {"price": (500, 4000), "change": (-20, 20)},
    "上证50":             {"price": (1000, 20000), "change": (-15, 15)},

    # 港股
    "恒生指数":           {"price": (10000, 50000), "change": (-15, 15)},
    "恒生科技指数":       {"price": (1000, 15000), "change": (-25, 25)},
    "国企指数":           {"price": (3000, 20000), "change": (-15, 15)},
    "恒生中国":           {"price": (3000, 20000), "change": (-15, 15)},

    # 欧洲股市
    "德国DAX 30":         {"price": (5000, 25000), "change": (-15, 15)},
    "法国CAC 40":          {"price": (3000, 12000), "change": (-15, 15)},
    "英国富时100":        {"price": (4000, 12000), "change": (-15, 15)},
    "欧洲斯托克600":      {"price": (200, 1000), "change": (-15, 15)},

    # 亚太
    "日经225指数":        {"price": (5000, 70000), "change": (-15, 15)},
    "韩国综合指数":       {"price": (1000, 6000), "change": (-15, 15)},
    "澳洲S&P/ASX 200":    {"price": (3000, 12000), "change": (-15, 15)},

    # 外汇（汇率通常 0.x ~ 200）
    "USD/CNY":            {"price": (6.0, 10.0), "change": (-5, 5)},
    "EUR/USD":            {"price": (0.5, 2.0), "change": (-5, 5)},
    "GBP/USD":            {"price": (0.5, 2.5), "change": (-5, 5)},
    "AUD/USD":            {"price": (0.4, 2.0), "change": (-5, 5)},
    "USD/JPY":            {"price": (50, 250), "change": (-5, 5)},
    "USD/KRW":            {"price": (500, 2500), "change": (-5, 5)},
    "USD/HKD":            {"price": (7.0, 8.5), "change": (-1, 1)},

    # 贵金属
    "现货黄金(XAUUSD)":   {"price": (1000, 3000), "change": (-8, 8)},
}


class RangeChecker:
    """
    规则 4：业务范围合理性校验

    对已知品种检查 price/change 是否在合理区间内。
    未知品种记录但不报错。
    """

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()
        market = data.get("市场表现", {})

        for region, items in market.items():
            if not isinstance(items, dict):
                continue
            for name, fields in items.items():
                if not isinstance(fields, dict):
                    continue

                rules = RANGE_RULES.get(name)
                if rules is None:
                    # 未知品种，不做范围检查
                    continue

                for field in ["price", "change"]:
                    v = fields.get(field)
                    if v is None:
                        continue
                    range_conf = rules.get(field)
                    if range_conf is None:
                        continue

                    lo, hi = range_conf
                    if not (lo <= v <= hi):
                        result.fail(
                            rule="业务范围合理性",
                            category=region,
                            key=f"{name}.{field}",
                            value=v,
                            message=f"{name}.{field} = {v}，超出合理范围 [{lo}, {hi}]"
                        )

        return result