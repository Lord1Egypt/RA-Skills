#!/usr/bin/env python3
"""
保费计算工具
输入：年龄、性别、保额、保障期限、产品类型
输出：各产品年缴保费，支持不同缴费期对比

🆕 2026-10-27 停售产品过滤（I3）
   ── references/products.json 字段取值分布探查结论（2536 款，2026-10-27 实测）──
   is_active          : True 603 / False 1933（无缺失）
   validity_status    : '已停售' 1897 / 'DISCONTINUED' 80 / '在售新品' 222
                        / '在售老品' 176 / '在售常规' 116 / 'MODIFIED' 17
                        / 'VALID' 5 / 'SKIPPED' 4 / '信息缺失' 3 / 字段缺失 16
   delisting_time     : '已停售' 1880 / '仍在售' 454 / 日期串(YYYY 或 YYYY-MM) 57
                        / '待核实' 37 / 缺失或 null 108
   data_quality       : 'garbage' 37 / 其余无此字段
   is_duplicate       : True 56 / False 68 / 字段缺失 2412

   判定口径（基于上述真实分布，不臆造字段语义）：
     已停售/已下架 = is_active is False
                     或 validity_status ∈ {'已停售', 'DISCONTINUED'}
                     或 delisting_time == '已停售'
                     或 delisting_time 为日期串（YYYY / YYYY-MM / YYYY-MM-DD）
   三条信号并集 → 排除 2017 款；剩余 519 款再剔除 data_quality=='garbage' 37 款
   与 is_duplicate==True 1 款 → 481 款进入默认产品池。
   说明：'SKIPPED' / 'MODIFIED' / '信息缺失' 未被视为停售（它们表示状态未知或条款调整），
        但 is_active / delisting_time 的日期串仍会命中停售判定。

   行为：默认（include_discontinued=False）已停售/已下架产品不进入推荐与对比列表；
        它们仍计入"全部产品"总数口径，并在 _meta.disclaimers 中说明排除数量。
        在售产品的保费计算公式未做任何改动。
"""

import json
import os
import re
import sys

# 已停售判定：delisting_time 为日期串（2021-12 / 2025-02-14 / 2021 等）
_RE_DELIST_DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

# 视为"已停售/已下架"的 validity_status 取值（实测分布见文件头注释）
_DISCONTINUED_VALIDITY = ("已停售", "DISCONTINUED")


def _extract_quality_hints(product):
    """🆕 2026-08-20 quality-aware：从产品提取质量提示

    基于 P0/P1 数据处理引入的字段（产品库质量治理）：
    - data_quality="garbage" → skip_for_recommendation=True （37 个产品过滤）
    - coverage_period_quality="missing" → coverage_period 替换为"未明确"（112 个产品）
    - listing_time_quality=verified/estimated/missing/unknown → 各自对应 disclaimer
      （verified=541 / estimated=80 / missing=75 / unknown=1838）

    Returns:
        dict: {
            skip_for_recommendation: bool,
            disclaimers: list[str],
            coverage_period: str | None,
            data_quality: str | None,
            coverage_period_quality: str | None,
            listing_time_quality: str | None,
        }
    """
    result = {
        "skip_for_recommendation": False,
        "disclaimers": [],
        "coverage_period": product.get("coverage_period"),
        "data_quality": product.get("data_quality"),
        "coverage_period_quality": product.get("coverage_period_quality"),
        "listing_time_quality": product.get("listing_time_quality"),
    }

    # P0-1: garbage 数据不可信，跳过推荐
    if product.get("data_quality") == "garbage":
        result["skip_for_recommendation"] = True
        result["disclaimers"].append(
            "⚠️ 此产品信息未完全核实，请联系保险公司确认详情"
        )

    # P0-2 coverage_period: missing 提示 + 默认"未明确"
    if product.get("coverage_period_quality") == "missing":
        result["coverage_period"] = "未明确"
        result["disclaimers"].append(
            "⚠️ 保险期间未明确，建议联系保险公司确认"
        )

    # P0-2 listing_time: 分级 disclaimer（verified 不加提示）
    ltq = product.get("listing_time_quality")
    if ltq == "estimated":
        result["disclaimers"].append(
            "ℹ️ 上市时间为估算值（年/月推测），仅作参考"
        )
    elif ltq == "missing":
        result["disclaimers"].append(
            "ℹ️ 上市时间不详，建议咨询保险公司最新产品"
        )
    elif ltq == "unknown":
        result["disclaimers"].append(
            "ℹ️ 上市时间无法核实，建议联系保险公司确认"
        )

    return result


def is_discontinued(product):
    """判断产品是否已停售/已下架。

    判定依据见文件头「字段取值分布探查结论」：
      - is_active is False
      - validity_status ∈ {'已停售', 'DISCONTINUED'}
      - delisting_time == '已停售' 或为日期串
    """
    if product.get("is_active") is False:
        return True
    if product.get("validity_status") in _DISCONTINUED_VALIDITY:
        return True
    delisting = str(product.get("delisting_time") or "").strip()
    if delisting == "已停售":
        return True
    if delisting and _RE_DELIST_DATE.match(delisting):
        return True
    return False


def is_eligible_for_pool(product, filter_garbage=True, include_discontinued=False):
    """产品是否可进入默认产品池（报价 / 对比 / 计数共用的**唯一**资格谓词）。

    ⚠️ 2026-11-08 整改（R7 · SDI-4）：原先 `load_products()` 与 `load_product_stats()`
    各写一套过滤条件，`load_products()` **漏了 is_duplicate 过滤**，
    导致报价池里仍混有重复记录，且 `eligible_products` != len(load_products())。
    现在两者共用本谓词，口径不会再漂移。

    过滤项：
      - data_quality == 'garbage'      → 数据不可信
      - is_duplicate is True            → 重复记录
      - 已停售/已下架（除非 include_discontinued=True）
    """
    if filter_garbage:
        if _extract_quality_hints(product)["skip_for_recommendation"] is not False:
            return False
    if product.get("is_duplicate") is True:
        return False
    if not include_discontinued and is_discontinued(product):
        return False
    return True


def load_products(filter_garbage=True, include_discontinued=False):
    """加载产品数据。

    Args:
        filter_garbage: True=跳过 data_quality=garbage 的产品（默认）。
        include_discontinued: False=跳过已停售/已下架产品（默认）；
                              True=保留它们（显式查询停售产品时使用）。

    Returns:
        list[dict]: 产品列表（已过滤 garbage、重复记录与停售产品）
    """
    product_file = os.path.join(os.path.dirname(__file__), "../references/products.json")
    with open(product_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    products = [
        p for p in data["products"]
        if is_eligible_for_pool(p, filter_garbage=filter_garbage,
                                include_discontinued=include_discontinued)
    ]
    return products


def load_product_stats(include_discontinued=False):
    """产品池计数口径（含"全部产品"总数与停售排除数）。

    Returns:
        dict: {
            total_products: int,          # 产品库总数（"全部产品"口径）
            garbage_excluded: int,
            duplicate_excluded: int,
            discontinued_excluded: int,   # 默认被排除的停售/下架数量
            eligible_products: int,       # 默认返回列表长度
            include_discontinued: bool,
        }
    """
    product_file = os.path.join(os.path.dirname(__file__), "../references/products.json")
    with open(product_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_products = data["products"]

    garbage = [p for p in all_products if p.get("data_quality") == "garbage"]
    duplicates = [p for p in all_products if p.get("is_duplicate") is True]
    discontinued = [p for p in all_products if is_discontinued(p)]

    # ⚠️ 2026-11-08 整改（R7 · SDI-4）：与 load_products() 共用同一资格谓词，
    #    保证 eligible_products == len(load_products())。
    eligible = [
        p for p in all_products
        if is_eligible_for_pool(p, filter_garbage=True,
                                include_discontinued=include_discontinued)
    ]
    return {
        "total_products": len(all_products),
        "garbage_excluded": len(garbage),
        "duplicate_excluded": len(duplicates),
        "discontinued_excluded": len(discontinued),
        "eligible_products": len(eligible),
        "include_discontinued": include_discontinued,
    }


def _pool_disclaimers(stats):
    """产品池口径说明（进入结果的 _meta.disclaimers）。"""
    disclaimers = []
    if stats["include_discontinued"]:
        disclaimers.append(
            f"ℹ️ 本次显式包含已停售/已下架产品（产品库共 {stats['total_products']} 款，"
            f"其中 {stats['discontinued_excluded']} 款已停售/已下架），"
            f"这些产品不可投保，仅供历史查询参考"
        )
    elif stats["discontinued_excluded"]:
        disclaimers.append(
            f"ℹ️ 已排除 {stats['discontinued_excluded']} 款已停售/已下架产品"
            f"（产品库全部 {stats['total_products']} 款，"
            f"本次可对比 {stats['eligible_products']} 款）；"
            f"如需查询停售产品请显式传 include_discontinued=true"
        )
    if stats["garbage_excluded"]:
        disclaimers.append(
            f"ℹ️ 已排除 {stats['garbage_excluded']} 款数据质量不达标（data_quality=garbage）的产品"
        )
    if stats["duplicate_excluded"]:
        disclaimers.append(
            f"ℹ️ 已排除 {stats['duplicate_excluded']} 款重复记录（is_duplicate=true）"
        )
    return disclaimers


def calculate_premium(product, age, gender, coverage_amount, payment_term=None, coverage_year=None):
    """计算单一产品保费"""
    product_type = product.get("type")

    # 基础费率调整系数
    age_factor = 1.0
    if age >= 18 and age <= 30:
        age_factor = 0.8
    elif age >= 31 and age <= 40:
        age_factor = 1.0
    elif age >= 41 and age <= 50:
        age_factor = 1.3
    elif age >= 51 and age <= 55:
        age_factor = 1.6
    elif age > 55:
        age_factor = 2.0

    gender_factor = 1.0
    if gender in ["女", "女性"]:
        gender_factor = 0.85
    elif gender in ["男", "男性"]:
        gender_factor = 1.0

    # 缴费期系数
    payment_term_factor = 1.0
    if product_type in ["重疾险", "定期寿险", "储蓄险"]:
        if payment_term == "趸交":
            payment_term_factor = 0.85
        elif payment_term == "3年":
            payment_term_factor = 0.95
        elif payment_term == "5年":
            payment_term_factor = 1.0
        elif payment_term == "10年":
            payment_term_factor = 1.05
        elif payment_term == "20年":
            payment_term_factor = 1.15
        elif payment_term == "30年":
            payment_term_factor = 1.25

    # 医疗险和意外险按固定费率（与年龄相关）
    if product_type == "医疗险":
        if age <= 30:
            annual_premium = coverage_amount * 0.0003
        elif age <= 40:
            annual_premium = coverage_amount * 0.0004
        elif age <= 50:
            annual_premium = coverage_amount * 0.0006
        elif age <= 60:
            annual_premium = coverage_amount * 0.001
        else:
            annual_premium = coverage_amount * 0.0015
        return max(annual_premium, 200)  # 最低保费200元

    if product_type == "意外险":
        annual_premium = coverage_amount * 0.001
        return max(annual_premium, 100)  # 最低保费100元

    # 重疾险、定期寿险、储蓄险
    premium_val = product.get("premium_per_10k")
    if premium_val is not None:
        # 处理字符串值，如 "约280" 或 "280"
        if isinstance(premium_val, str):
            nums = re.findall(r'[\d.]+', premium_val)
            premium_val = float(nums[0]) if nums else 0
        base_premium = (coverage_amount / 10000) * float(premium_val)
    else:
        base_premium = coverage_amount * 0.01

    total_premium = base_premium * age_factor * gender_factor * payment_term_factor

    return round(total_premium, 2)


def calculate_all_premiums(age, gender, coverage_amount, product_types=None, payment_term=None,
                           coverage_year=None, include_discontinued=False):
    """计算所有符合条件的产品的保费（quality-aware + 停售过滤）

    Args:
        include_discontinued: False=默认不返回已停售/已下架产品；
                              True=显式查询停售产品（含在结果中并标注）。
    """
    products = load_products(include_discontinued=include_discontinued)
    stats = load_product_stats(include_discontinued=include_discontinued)
    pool_disclaimers = _pool_disclaimers(stats)

    results = {}
    for product in products:
        # 按类型筛选
        if product_types:
            if product.get("type") not in product_types:
                continue

        # 年龄筛选
        if age > 55 and product.get("type") in ["定期寿险", "储蓄险"]:
            continue  # 定期寿险55岁以上不推荐
        if age > 60 and product.get("type") == "意外险":
            continue

        # 计算保费
        premiums_by_term = {}
        available_terms = product.get("payment_terms", ["年交"])

        for term in available_terms:
            if product.get("type") in ["医疗险", "意外险"]:
                term_premium = calculate_premium(product, age, gender, coverage_amount, "年交")
            else:
                term_premium = calculate_premium(product, age, gender, coverage_amount, term)

            # 标准化缴费期名称
            term_name = term
            premiums_by_term[term_name] = term_premium

        # 🆕 2026-08-20 quality-aware：获取 disclaimers 和数据质量标记
        hints = _extract_quality_hints(product)
        product_disclaimers = list(hints["disclaimers"])
        if is_discontinued(product):
            product_disclaimers.append(
                "⚠️ 该产品已停售/已下架（仅在显式查询停售产品时返回），不可投保"
            )

        # 如果指定了缴费期，只返回该缴费期
        if payment_term and payment_term in premiums_by_term:
            results[product.get("id")] = {
                "name": product.get("name"),
                "company": product.get("company"),
                "type": product.get("type"),
                "annual_premium": premiums_by_term[payment_term],
                "payment_term": payment_term,
                "coverage_amount": coverage_amount,
                "coverage_period": hints["coverage_period"],  # 🆕 缺失时为"未明确"
                "waiting_period": product.get("waiting_period"),
                "core_coverage": ", ".join(product.get("key_benefits", [])) if isinstance(product.get("key_benefits"), list) else product.get("core_coverage", ""),
                "notes": product.get("notes", ""),
                # 🆕 质量提示（SKILL 用来给客户附 disclaimer）
                "data_quality": hints["data_quality"],
                "coverage_period_quality": hints["coverage_period_quality"],
                "listing_time_quality": hints["listing_time_quality"],
                "disclaimers": product_disclaimers,
                "is_discontinued": is_discontinued(product),
            }
        else:
            # 返回所有可用缴费期
            results[product.get("id")] = {
                "name": product.get("name"),
                "company": product.get("company"),
                "type": product.get("type"),
                "premiums_by_term": premiums_by_term,
                "coverage_amount": coverage_amount,
                "coverage_period": hints["coverage_period"],  # 🆕 缺失时为"未明确"
                "waiting_period": product.get("waiting_period"),
                "core_coverage": ", ".join(product.get("key_benefits", [])) if isinstance(product.get("key_benefits"), list) else product.get("core_coverage", ""),
                "notes": product.get("notes", ""),
                # 🆕 质量提示（SKILL 用来给客户附 disclaimer）
                "data_quality": hints["data_quality"],
                "coverage_period_quality": hints["coverage_period_quality"],
                "listing_time_quality": hints["listing_time_quality"],
                "disclaimers": product_disclaimers,
                "is_discontinued": is_discontinued(product),
            }

    # 🆕 I3：全部产品计数口径 + 停售排除说明（不影响单产品保费公式）
    results["_meta"] = {
        "total_products": stats["total_products"],
        "eligible_products": stats["eligible_products"],
        "returned_products": len([k for k in results if k != "_meta"]),
        "discontinued_excluded": stats["discontinued_excluded"],
        "garbage_excluded": stats["garbage_excluded"],
        "duplicate_excluded": stats["duplicate_excluded"],
        "include_discontinued": include_discontinued,
        "disclaimers": pool_disclaimers,
    }

    return results


def compare_payment_terms(products_list, age, gender, coverage_amount, include_discontinued=False):
    """对比不同缴费期的保费"""
    products = load_products(include_discontinued=include_discontinued)
    comparison = []

    for product in products:
        if product.get("id") not in products_list:
            continue

        row = {
            "product_id": product.get("id"),
            "name": product.get("name"),
            "company": product.get("company"),
            "type": product.get("type")
        }

        for term in product.get("payment_terms", []):
            if product.get("type") in ["医疗险", "意外险"]:
                annual = calculate_premium(product, age, gender, coverage_amount, "年交")
            else:
                annual = calculate_premium(product, age, gender, coverage_amount, term)
            row[term] = annual

        comparison.append(row)

    return comparison


# 示例档案（仅在 stdin 未提供输入时作为演示数据打印，并明确标注来源）
EXAMPLE_PREMIUM_INPUT = {
    "age": 35,
    "gender": "男",
    "coverage_amount": 500000,
    "product_types": None,
    "payment_term": "20年",
    "coverage_year": None
}


def _read_stdin_text():
    """读取 stdin 文本；TTY（无管道输入）返回空串。"""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return ""
        return sys.stdin.read() or ""
    except Exception:
        return ""


def main():
    raw = _read_stdin_text().strip()
    if not raw:
        # 未提供输入：明确标注示例数据，不静默把示例档案当作正式结果
        sys.stderr.write("⚠️ 未提供输入，以下为示例数据（示例档案，非真实客户数据）：\n")
        sys.stderr.write(json.dumps(EXAMPLE_PREMIUM_INPUT, ensure_ascii=False, indent=2) + "\n")
        params = EXAMPLE_PREMIUM_INPUT
    else:
        try:
            params = json.loads(raw)
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            return 0
    try:
        results = calculate_all_premiums(
            params.get("age", 35),
            params.get("gender", "男"),
            params.get("coverage_amount", 500000),
            params.get("product_types"),
            params.get("payment_term"),
            params.get("coverage_year"),
            params.get("include_discontinued", False)
        )
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 0
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
