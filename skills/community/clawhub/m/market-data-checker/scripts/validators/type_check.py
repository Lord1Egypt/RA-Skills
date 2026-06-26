# -*- coding: utf-8 -*-
"""
TypeChecker - 数值类型强校验
检查 price / change / volume 等字段的类型是否符合预期。
price: float | int (正数)
change: float | int (可正可负)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


class TypeChecker:
    """
    规则 3：数值类型强校验

    期望类型：
      - price:   float | int，必须 > 0
      - change:  float | int，可正可负
      - volume:  float | int，可为 0

    以下均为错误：
      - str 类型（"N/A", "null", "" 等）
      - bool 类型
      - list / dict 类型
      - price <= 0
    """

    MARKET_NUMERIC_FIELDS = ["price", "change", "volume"]
    ALLOWED_TYPES = (int, float)

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()
        market = data.get("市场表现", {})

        for region, items in market.items():
            if not isinstance(items, dict):
                continue
            for name, fields in items.items():
                if not isinstance(fields, dict):
                    continue
                for field in self.MARKET_NUMERIC_FIELDS:
                    v = fields.get(field)
                    if v is None:
                        continue  # NullChecker 处理

                    # 类型检查
                    if not isinstance(v, self.ALLOWED_TYPES):
                        result.fail(
                            rule="数值类型强校验",
                            category=region,
                            key=f"{name}.{field}",
                            value=f"{type(v).__name__}: {repr(v)[:50]}",
                            message=f"{name}.{field} 类型应为 int/float，实际为 {type(v).__name__}"
                        )
                        continue

                    # price 范围检查
                    if field == "price" and v <= 0:
                        result.fail(
                            rule="数值类型强校验",
                            category=region,
                            key=f"{name}.{field}",
                            value=v,
                            message=f"{name}.{field} = {v}，price 必须 > 0"
                        )

                    # change 合理性（允许 0，上下限 ±50%）
                    if field == "change" and abs(v) > 50:
                        result.fail(
                            rule="数值类型强校验",
                            category=region,
                            key=f"{name}.{field}",
                            value=v,
                            message=f"{name}.{field} = {v}%，单日涨跌幅超出 ±50%，疑似数据异常"
                        )

                    # volume 非负
                    if field == "volume" and v < 0:
                        result.fail(
                            rule="数值类型强校验",
                            category=region,
                            key=f"{name}.{field}",
                            value=v,
                            message=f"{name}.{field} = {v}，volume 不能为负"
                        )

        return result