"""
Blueprint V1到V2迁移器

迁移旧蓝图到v2格式：
- 回填 blueprintIntent
- 回填 strategySelection
- 保持向后兼容（保留旧的category/layer字段）
"""

import json
from pathlib import Path
from typing import Dict, List


def infer_legacy_strategy(blueprint: Dict) -> Dict:
    """从旧蓝图推断意图和策略"""
    systems = blueprint.get("library", {}).get("systems", [])
    goals = blueprint.get("context", {}).get("goals", [])
    industry = blueprint.get("meta", {}).get("industry", "common")

    # 简单推断规则（Phase 0版本）
    # 1. 检查goals关键词
    product_keywords = ["产品", "能力", "功能", "价值", "产品规划"]
    technical_keywords = ["架构", "技术", "调用", "链路", "技术架构"]
    business_keywords = ["业务域", "CRM", "ERP", "OA", "业务"]

    goal_text = " ".join(goals)

    # 计算各视角得分
    scores = {
        "product": sum(1 for k in product_keywords if k in goal_text),
        "technical": sum(1 for k in technical_keywords if k in goal_text),
        "business": sum(1 for k in business_keywords if k in goal_text)
    }

    # 默认为product（最常见）
    if not goals or sum(scores.values()) == 0:
        primary = "product"
        confidence = 0.70
    else:
        primary = max(scores, key=scores.get)
        # 置信度基于关键词匹配比例
        max_score = scores[primary]
        confidence = min(max_score / len(goals), 0.85)

    # 2. 检测行业overlay
    secondary = None
    if industry == "finance":
        secondary = "finance"
        confidence = min(confidence + 0.1, 0.90)
    elif industry == "manufacturing":
        secondary = "manufacturing"
        confidence = min(confidence + 0.1, 0.90)
    elif industry == "retail":
        secondary = "retail"
        confidence = min(confidence + 0.1, 0.90)

    # 3. 确定策略
    strategy_map = {
        "product": "product-capability",
        "technical": "technical-architecture",
        "business": "business-domain"
    }

    strategy = strategy_map.get(primary, "product-capability")

    return {
        "blueprintIntent": {
            "primary": primary,
            "secondary": secondary,
            "mode": "auto"
        },
        "strategySelection": {
            "selected": strategy,
            "source": "migration",
            "reason": "migrated from v1 blueprint",
            "confidence": round(confidence, 2),
            "reviewNeeded": confidence < 0.75
        }
    }


def migrate_blueprint_v1_to_v2(blueprint: Dict) -> Dict:
    """迁移旧蓝图到v2格式"""
    # 深拷贝避免修改原数据
    migrated = json.loads(json.dumps(blueprint))

    # 确保editor字段存在
    migrated.setdefault("editor", {})

    # 迁移意图和策略
    if "blueprintIntent" not in migrated["editor"]:
        migration = infer_legacy_strategy(migrated)
        migrated["editor"]["blueprintIntent"] = migration["blueprintIntent"]
        migrated["editor"]["strategySelection"] = migration["strategySelection"]

    # 保留旧的category/layer字段（向后兼容）
    # 新系统会优先使用strategySelection，fallback到旧字段

    # 更新meta
    if "lastModifiedBy" not in migrated["meta"]:
        migrated["meta"]["lastModifiedBy"] = "migration"
        migrated["meta"]["lastModifiedAt"] = "2026-04-25T00:00:00Z"

    return migrated


def batch_migrate(input_dir: str, output_dir: str):
    """批量迁移蓝图"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    migrated_count = 0
    failed_count = 0

    for blueprint_file in input_path.glob("**/*.blueprint.json"):
        try:
            blueprint = json.load(open(blueprint_file))
            migrated = migrate_blueprint_v1_to_v2(blueprint)

            # 保存迁移后的蓝图
            output_file = output_path / blueprint_file.name
            json.dump(migrated, open(output_file, "w"), indent=2, ensure_ascii=False)

            migrated_count += 1
            print(f"✓ Migrated: {blueprint_file.name}")
        except Exception as e:
            failed_count += 1
            print(f"✗ Failed: {blueprint_file.name} - {str(e)}")

    print(f"\n迁移完成：{migrated_count} 成功，{failed_count} 失败")
    return {
        "migrated_count": migrated_count,
        "failed_count": failed_count
    }


if __name__ == "__main__":
    # 测试迁移
    import sys

    if len(sys.argv) > 2:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        batch_migrate(input_dir, output_dir)
    else:
        print("Usage: python v1_to_v2.py <input_dir> <output_dir>")