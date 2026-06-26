# -*- coding: utf-8 -*-
"""
NullChecker - 非空校验
检查 market_data.json 中所有必填字段是否存在且非 None。
支持结构：
  - 市场表现数值：price / change / volume
  - 经济数据数值
  - 政策/企业动态列表
  - 环球市场速览
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


class NullChecker:
    """
    规则 1：非空校验

    检查维度：
      1. 文件整体非空
      2. 顶层分类（市场表现、经济数据、政策动态、企业动态、环球市场速览）存在
      3. 市场表现中的数值字段（price/change）非 None
      4. 政策/企业动态列表非空（允许空列表）
      5. _meta.report_date 存在
    """

    MANDATORY_TOP_KEYS = [
        "_meta", "市场表现", "经济数据",
        "政策动态", "企业动态", "环球市场速览"
    ]

    MARKET_FIELDS = ["price", "change", "volume"]

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()

        # 规则 1-1：文件整体非空
        if not data:
            result.fail(
                rule="非空校验",
                category="整体",
                key="root",
                value=data,
                message="market_data.json 为空或解析失败"
            )
            return result

        # 规则 1-2：顶层分类存在
        for key in self.MANDATORY_TOP_KEYS:
            if key not in data:
                result.fail(
                    rule="非空校验",
                    category="顶层结构",
                    key=key,
                    value=None,
                    message=f"缺少必填顶层分类：{key}"
                )

        # 规则 1-3：_meta.report_date
        meta = data.get("_meta", {})
        if not meta.get("report_date"):
            result.fail(
                rule="非空校验",
                category="_meta",
                key="report_date",
                value=meta.get("report_date"),
                message="_meta.report_date 为空"
            )

        # 规则 1-4：市场表现数值检查
        market = data.get("市场表现", {})
        self._check_market_null(market, result)

        # 规则 1-5：政策/企业动态列表结构（列表存在即可，内容可空）
        for cat in ["政策动态", "企业动态"]:
            val = data.get(cat)
            if val is None:
                result.fail(
                    rule="非空校验",
                    category="结构",
                    key=cat,
                    value=None,
                    message=f"{cat} 字段缺失"
                )
            elif not isinstance(val, dict):
                result.fail(
                    rule="非空校验",
                    category="结构",
                    key=cat,
                    value=type(val).__name__,
                    message=f"{cat} 应为 dict，实际为 {type(val).__name__}"
                )

        # 规则 1-6：环球市场速览结构
        summary = data.get("环球市场速览", {})
        if summary is None:
            result.fail(
                rule="非空校验",
                category="结构",
                key="环球市场速览",
                value=None,
                message="环球市场速览 字段缺失"
            )
        elif isinstance(summary, dict) and not summary:
            result.fail(
                rule="非空校验",
                category="结构",
                key="环球市场速览",
                value={},
                message="环球市场速览 为空字典"
            )

        return result

    def _check_market_null(self, market: dict, result: CheckResult):
        """递归检查市场表现中的数值字段"""
        for region, items in market.items():
            if not isinstance(items, dict):
                continue
            for name, fields in items.items():
                if not isinstance(fields, dict):
                    continue
                for field in self.MARKET_FIELDS:
                    v = fields.get(field)
                    # price 必填，change 允许 None（如指数类），volume 可选
                    if field == "price" and (v is None or v == ""):
                        result.fail(
                            rule="非空校验",
                            category=region,
                            key=f"{name}.{field}",
                            value=v,
                            message=f"{name} 的 price 为空"
                        )