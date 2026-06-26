from __future__ import annotations

from copy import deepcopy


NUTRIENT_FIELDS = [
    "kcal",
    "protein_g",
    "carbs_g",
    "fat_g",
    "fiber_g",
    "sugar_g",
    "sodium_mg",
    "water_ml",
    "caffeine_mg",
    "alcohol_g",
]

CSV_NUTRIENT_FIELDS = [
    "kcal",
    "protein_g",
    "carbs_g",
    "fat_g",
    "fiber_g",
    "sugar_g",
    "sodium_mg",
]

VALID_SOURCES = {"user_provided", "label_calculated", "estimated", "mixed"}
VALID_CONFIDENCE = {"high", "medium", "low"}


class NutritionError(ValueError):
    """Raised when structured nutrition input is invalid."""


def round_number(value):
    if value is None:
        return None
    rounded = round(float(value), 1)
    if rounded.is_integer():
        return int(rounded)
    return rounded


def round_nutrition(nutrition):
    return {
        field: round_number(nutrition.get(field))
        for field in NUTRIENT_FIELDS
        if field in nutrition
    }


def validate_nutrition_values(nutrition, *, allow_empty=True):
    if not isinstance(nutrition, dict):
        raise NutritionError("营养数据必须是对象。")
    if not nutrition and not allow_empty:
        raise NutritionError("营养数据不能为空。")

    for field, value in nutrition.items():
        if field not in NUTRIENT_FIELDS:
            raise NutritionError(f"不支持的营养字段：{field}")
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise NutritionError(f"{field} 必须是数字或 null。")
        if value < 0:
            raise NutritionError(f"{field} 不能为负数。")


def validate_positive_number(value, field_name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise NutritionError(f"{field_name} 必须是数字。")
    if value <= 0:
        raise NutritionError(f"{field_name} 必须大于 0。")


def calculate_per_100g(food, eaten_amount_g, nutrition_per_100g):
    validate_positive_number(eaten_amount_g, "eaten_amount_g")
    validate_nutrition_values(nutrition_per_100g, allow_empty=False)
    factor = float(eaten_amount_g) / 100
    nutrition = {
        field: value * factor
        for field, value in nutrition_per_100g.items()
        if value is not None
    }
    return {
        "food": food,
        "nutrition": round_nutrition(nutrition),
        "source": "label_calculated",
        "confidence": "high",
        "note": "根据用户提供的每100g营养标签计算。",
    }


def calculate_per_serving(food, servings_eaten, nutrition_per_serving):
    validate_positive_number(servings_eaten, "servings_eaten")
    validate_nutrition_values(nutrition_per_serving, allow_empty=False)
    nutrition = {
        field: value * float(servings_eaten)
        for field, value in nutrition_per_serving.items()
        if value is not None
    }
    return {
        "food": food,
        "nutrition": round_nutrition(nutrition),
        "source": "label_calculated",
        "confidence": "high",
        "note": "根据用户提供的每份营养标签计算。",
    }


def normalize_nutrition(nutrition):
    nutrition = nutrition or {}
    validate_nutrition_values(nutrition)
    normalized = {field: None for field in NUTRIENT_FIELDS}
    for field, value in nutrition.items():
        normalized[field] = round_number(value)
    return normalized


def normalize_item(item):
    if not isinstance(item, dict):
        raise NutritionError("每个食物条目必须是对象。")
    if not item.get("food"):
        raise NutritionError("食物条目缺少 food。")

    normalized = deepcopy(item)
    normalized["nutrition"] = normalize_nutrition(normalized.get("nutrition") or {})
    normalized["source"] = normalized.get("source") or "estimated"
    normalized["confidence"] = normalized.get("confidence") or "low"
    normalized["note"] = normalized.get("note") or ""
    normalized["amount_raw"] = normalized.get("amount_raw") or ""
    normalized["amount_g"] = round_number(normalized.get("amount_g"))

    if normalized["source"] not in VALID_SOURCES:
        raise NutritionError(f"不支持的数据来源：{normalized['source']}")
    if normalized["confidence"] not in VALID_CONFIDENCE:
        raise NutritionError(f"不支持的置信度：{normalized['confidence']}")
    if normalized["amount_g"] is not None and normalized["amount_g"] < 0:
        raise NutritionError("amount_g 不能为负数。")

    return normalized


def sum_nutrition(items):
    totals = {field: 0 for field in NUTRIENT_FIELDS}
    for item in items:
        nutrition = item.get("nutrition") or {}
        for field in NUTRIENT_FIELDS:
            value = nutrition.get(field)
            if value is not None:
                totals[field] += float(value)
    return round_nutrition(totals)


def missing_values_count(items):
    count = 0
    for item in items:
        nutrition = item.get("nutrition") or {}
        for field in CSV_NUTRIENT_FIELDS:
            if nutrition.get(field) is None:
                count += 1
    return count


def source_breakdown(entries):
    breakdown = {
        "user_provided": {field: 0 for field in NUTRIENT_FIELDS},
        "label_calculated": {field: 0 for field in NUTRIENT_FIELDS},
        "estimated": {field: 0 for field in NUTRIENT_FIELDS},
        "mixed": {field: 0 for field in NUTRIENT_FIELDS},
    }
    for entry in entries:
        for item in entry.get("items", []):
            source = item.get("source") if item.get("source") in breakdown else "estimated"
            nutrition = item.get("nutrition") or {}
            for field in NUTRIENT_FIELDS:
                value = nutrition.get(field)
                if value is not None:
                    breakdown[source][field] += float(value)
    return {source: round_nutrition(values) for source, values in breakdown.items()}
