# -*- coding: utf-8 -*-
"""
NaNChecker - 非 NaN / 非无穷大校验
检查 market_data.json 中所有数值字段是否为有限浮点数。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


class NaNChecker:
    """
    规则 2：非 NaN / 非无穷大校验

    检查所有 price / change / volume 数值字段：
      - 不能是 float('nan')
      - 不能是 float('inf') / float('-inf')
      - 不能是 math.nan / math.inf
    """

    MARKET_FIELDS = ["price", "change", "volume"]

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()
        market = data.get("市场表现", {})
        self._check_nan_inf(market, result)

        # 经济数据中的数值字段
        econ = data.get("经济数据", {})
        self._check_econ_nan(econ, result)

        return result

    def _check_nan_inf(self, market: dict, result: CheckResult):
        for region, items in market.items():
            if not isinstance(items, dict):
                continue
            for name, fields in items.items():
                if not isinstance(fields, dict):
                    continue
                for field in self.MARKET_FIELDS:
                    v = fields.get(field)
                    if v is None:
                        continue  # None 由 NullChecker 处理
                    if isinstance(v, (int, float)):
                        if math.isnan(v) or math.isinf(v):
                            result.fail(
                                rule="非NaN/非无穷大",
                                category=region,
                                key=f"{name}.{field}",
                                value=v,
                                message=f"{name}.{field} = {v}（NaN或无穷大）"
                            )
                    elif isinstance(v, str):
                        # 字符串形式的数值
                        try:
                            fv = float(v)
                            if math.isnan(fv) or math.isinf(fv):
                                result.fail(
                                    rule="非NaN/非无穷大",
                                    category=region,
                                    key=f"{name}.{field}",
                                    value=v,
                                    message=f"{name}.{field} = '{v}'（解析后为NaN或无穷大）"
                                )
                        except (ValueError, TypeError):
                            result.fail(
                                rule="非NaN/非无穷大",
                                category=region,
                                key=f"{name}.{field}",
                                value=v,
                                message=f"{name}.{field} = '{v}'（无法解析为数值）"
                            )

    def _check_econ_nan(self, econ: dict, result: CheckResult):
        """检查经济数据中的数值字段"""
        for region, data_dict in econ.items():
            if not isinstance(data_dict, dict):
                continue
            for key, val in data_dict.items():
                if isinstance(val, (int, float)):
                    if math.isnan(val) or math.isinf(val):
                        result.fail(
                            rule="非NaN/非无穷大",
                            category="经济数据",
                            key=f"{region}.{key}",
                            value=val,
                            message=f"经济数据 {region}.{key} = {val}"
                        )
                elif isinstance(val, dict):
                    for subkey, subval in val.items():
                        if isinstance(subval, (int, float)):
                            if math.isnan(subval) or math.isinf(subval):
                                result.fail(
                                    rule="非NaN/非无穷大",
                                    category="经济数据",
                                    key=f"{region}.{key}.{subkey}",
                                    value=subval,
                                    message=f"经济数据 {region}.{key}.{subkey} = {subval}"
                                )