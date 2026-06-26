"""
Phase 1准确率测试 - 修正版

修复Ground Truth标注，使用实际system ID和name
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from scripts.business_blueprint.intent_resolver import IntentResolver
from scripts.business_blueprint.rule_engine import RuleEngine, load_perspective, load_overlay
from scripts.business_blueprint.tests.metrics import intent_accuracy, weighted_layer_accuracy
from scripts.business_blueprint.tests.test_utils import load_test_set


# Ground truth标注 - 使用实际system ID和name（从blueprint读取）
GROUND_TRUTH_INTENT = {
    "common": {"primary": "product", "secondary": None, "strategy": "product-capability"},
    "finance": {"primary": "product", "secondary": "finance-regulatory", "strategy": "product-capability"},
    "manufacturing": {"primary": "product", "secondary": "manufacturing-supply-chain", "strategy": "product-capability"},
    "retail": {"primary": "product", "secondary": "retail-operations", "strategy": "product-capability"}
}

# 预期层级归属（基于system name关键词推断）
EXPECTED_LAYERS_FINANCE = {
    "客户端": "user-entry",
    "网关": "gateway",
    "风控": "risk-control",
    "CRM": "core-business",
    "信贷": "core-business",
    "反欺诈": "risk-control"
}

EXPECTED_LAYERS_MANUFACTURING = {
    "ERP": "supplier",
    "MES": "production",
    "WMS": "warehouse",
    "生产": "production",
    "仓库": "warehouse",
    "供应商": "supplier"
}


def match_system_to_expected_layer(system_name: str, expected_map: dict) -> str | None:
    """根据system name匹配预期层级"""
    for keyword, layer in expected_map.items():
        if keyword in system_name:
            return layer
    return None


def phase1_accuracy_test_fixed():
    """Phase 1准确率测试（修正版）"""
    print("=" * 80)
    print("Phase 1: Intent Inference & Layer Assignment Accuracy Test (Fixed)")
    print("=" * 80)

    fixtures = load_test_set("demos")
    print(f"\n1. 加载测试蓝图: {len(fixtures)} 个")

    # 意图推断测试
    print("\n2. 意图推断测试...")
    resolver = IntentResolver()
    intent_results = []

    for fixture in fixtures:
        name = fixture["name"].replace(".blueprint", "")
        blueprint = fixture["blueprint"]

        resolved = resolver.resolve_intent(blueprint)
        predicted_intent = resolved["blueprintIntent"]
        predicted_strategy = resolved["strategySelection"]["selected"]

        truth_intent = GROUND_TRUTH_INTENT.get(name, {})
        ground_truth_intent = {"primary": truth_intent.get("primary", "product"), "secondary": truth_intent.get("secondary")}
        ground_truth_strategy = truth_intent.get("strategy", "product-capability")

        accuracy = intent_accuracy(predicted_intent, ground_truth_intent)

        intent_results.append({
            "name": name,
            "predicted_intent": predicted_intent,
            "predicted_strategy": predicted_strategy,
            "ground_truth_intent": ground_truth_intent,
            "accuracy": accuracy
        })

        status = "✓" if accuracy >= 0.8 else "⚠"
        print(f"  {status} {name}: {predicted_intent['primary']} ({predicted_intent['confidence']})")

    overall_intent_accuracy = sum(r["accuracy"] for r in intent_results) / len(intent_results)
    print(f"\nIntent Accuracy: {overall_intent_accuracy:.2%}")

    # 层级归属测试（基于name匹配）
    print("\n3. 层级归属测试...")
    layer_results = []

    for fixture in fixtures:
        name = fixture["name"].replace(".blueprint", "")
        blueprint = fixture["blueprint"]
        systems = blueprint.get("library", {}).get("systems", [])

        if name == "finance":
            expected_map = EXPECTED_LAYERS_FINANCE
        elif name == "manufacturing":
            expected_map = EXPECTED_LAYERS_MANUFACTURING
        else:
            print(f"  - {name}: 无预期层级标注，跳过")
            continue

        intent_result = next(r for r in intent_results if r["name"] == name)
        perspective_id = intent_result["predicted_strategy"]
        overlay_id = intent_result["predicted_intent"]["secondary"]

        perspective = load_perspective(perspective_id)
        overlay = load_overlay(overlay_id)
        engine = RuleEngine(perspective, overlay)

        predicted_layers = {}
        expected_layers = {}

        for system in systems:
            system_id = system.get("id")
            system_name = system.get("name", "")

            # 推断预期层级（基于name匹配）
            expected_layer = match_system_to_expected_layer(system_name, expected_map)
            if expected_layer:
                expected_layers[system_id] = expected_layer

                # 规则引擎计算
                assignment = engine.assign_layer(system)
                predicted_layers[system_id] = assignment["layer"]

        if expected_layers:
            layer_order = perspective.get("layerOrder", list(set(expected_layers.values())))
            accuracy = weighted_layer_accuracy(predicted_layers, expected_layers, layer_order)

            layer_results.append({
                "name": name,
                "accuracy": accuracy,
                "predicted": predicted_layers,
                "expected": expected_layers
            })

            status = "✓" if accuracy >= 0.88 else "⚠"
            print(f"  {status} {name}: {accuracy:.2%}")

            for sys_id, pred in predicted_layers.items():
                exp = expected_layers.get(sys_id)
                match = "✓" if pred == exp else "✗"
                sys_name = next(s["name"] for s in systems if s["id"] == sys_id)
                print(f"    {match} {sys_name}: {pred} vs {exp}")

    overall_layer_accuracy = sum(r["accuracy"] for r in layer_results) / len(layer_results) if layer_results else 0.0
    print(f"\nLayer Accuracy: {overall_layer_accuracy:.2%}")

    # 自动选择成功率
    auto_success_count = sum(
        1 for r in intent_results
        if r["accuracy"] >= 0.8 and r["predicted_intent"]["confidence"] >= 0.75
    )
    auto_success_rate = auto_success_count / len(intent_results)
    print(f"\nAuto-Selection Success Rate: {auto_success_rate:.2%}")

    # 达标检查
    print("\n5. 达标检查...")
    thresholds = {"intent_accuracy": 0.85, "layer_accuracy": 0.88, "auto_success_rate": 0.70}

    pass_intent = overall_intent_accuracy >= thresholds["intent_accuracy"]
    pass_layer = overall_layer_accuracy >= thresholds["layer_accuracy"]
    pass_auto = auto_success_rate >= thresholds["auto_success_rate"]

    print(f"Intent Accuracy: {overall_intent_accuracy:.2%} >= {thresholds['intent_accuracy']:.0%} {'✓' if pass_intent else '✗'}")
    print(f"Layer Accuracy: {overall_layer_accuracy:.2%} >= {thresholds['layer_accuracy']:.0%} {'✓' if pass_layer else '✗'}")
    print(f"Auto-Selection Success: {auto_success_rate:.2%} >= {thresholds['auto_success_rate']:.0%} {'✓' if pass_auto else '✗'}")

    pass_status = pass_intent and pass_layer and pass_auto
    print(f"\n{'✓ Phase 1 测试通过' if pass_status else '✗ Phase 1 测试失败'}")

    # 生成报告
    report = {
        "test_phase": "Phase 1 (Fixed)",
        "test_date": "2026-04-25",
        "metrics": {
            "intent_inference_accuracy": (overall_intent_accuracy, thresholds["intent_accuracy"]),
            "layer_assignment_accuracy": (overall_layer_accuracy, thresholds["layer_accuracy"]),
            "auto_selection_success_rate": (auto_success_rate, thresholds["auto_success_rate"])
        },
        "pass_status": pass_status,
        "detailed_results": {"intent": intent_results, "layer": layer_results}
    }

    json.dump(report, open("reports/phase1_accuracy_report_fixed.json", "w"), indent=2, ensure_ascii=False)
    print(f"\n报告已保存: reports/phase1_accuracy_report_fixed.json")
    print("=" * 80)

    return report


if __name__ == "__main__":
    report = phase1_accuracy_test_fixed()