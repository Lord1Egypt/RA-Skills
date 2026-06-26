"""
Phase 1准确率测试

验证意图解析和层级归属准确率：
- Intent Inference Accuracy >= 0.85
- Layer Assignment Accuracy >= 0.88
- Auto-Selection Success Rate >= 0.70
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from scripts.business_blueprint.intent_resolver import IntentResolver
from scripts.business_blueprint.rule_engine import RuleEngine, load_perspective, load_overlay
from scripts.business_blueprint.tests.metrics import intent_accuracy, weighted_layer_accuracy
from scripts.business_blueprint.tests.test_utils import load_test_set


# Ground truth标注（手动标注）
GROUND_TRUTH = {
    "common": {
        "intent": {"primary": "product", "secondary": None},
        "strategy": "product-capability"
    },
    "finance": {
        "intent": {"primary": "product", "secondary": "finance"},
        "strategy": "product-capability",
        "expected_layers": {
            "sys-client": "user-entry",
            "sys-gateway": "gateway",
            "sys-risk": "risk-control",
            "sys-service": "core-business"
        }
    },
    "manufacturing": {
        "intent": {"primary": "product", "secondary": "manufacturing"},
        "strategy": "product-capability",
        "expected_layers": {
            "sys-supplier": "supplier",
            "sys-production": "production",
            "sys-warehouse": "warehouse"
        }
    },
    "retail": {
        "intent": {"primary": "product", "secondary": "retail"},
        "strategy": "product-capability"
    }
}


def phase1_accuracy_test():
    """Phase 1准确率测试"""
    print("=" * 80)
    print("Phase 1: Intent Inference & Layer Assignment Accuracy Test")
    print("=" * 80)

    # 1. 加载测试蓝图
    fixtures = load_test_set("demos")
    print(f"\n1. 加载测试蓝图: {len(fixtures)} 个")

    # 2. 意图推断测试
    print("\n2. 意图推断测试...")
    resolver = IntentResolver()

    intent_results = []
    for fixture in fixtures:
        name = fixture["name"].replace(".blueprint", "")
        blueprint = fixture["blueprint"]

        # 推断意图
        resolved = resolver.resolve_intent(blueprint)
        predicted_intent = resolved["blueprintIntent"]
        predicted_strategy = resolved["strategySelection"]["selected"]

        # Ground truth
        truth = GROUND_TRUTH.get(name, {})
        ground_truth_intent = truth.get("intent", {"primary": "product"})
        ground_truth_strategy = truth.get("strategy", "product-capability")

        # 计算准确率
        accuracy = intent_accuracy(predicted_intent, ground_truth_intent)

        intent_results.append({
            "name": name,
            "predicted_intent": predicted_intent,
            "ground_truth_intent": ground_truth_intent,
            "predicted_strategy": predicted_strategy,
            "ground_truth_strategy": ground_truth_strategy,
            "accuracy": accuracy,
            "confidence": predicted_intent["confidence"]
        })

        status = "✓" if accuracy >= 0.8 else "⚠"
        print(f"  {status} {name}: {predicted_intent['primary']} ({predicted_intent['confidence']}) vs {ground_truth_intent['primary']}")

    # 3. 计算整体意图准确率
    overall_intent_accuracy = sum(r["accuracy"] for r in intent_results) / len(intent_results)
    print(f"\nIntent Accuracy: {overall_intent_accuracy:.2%}")

    # 4. 层级归属测试
    print("\n3. 层级归属测试...")
    layer_results = []

    for fixture in fixtures:
        name = fixture["name"].replace(".blueprint", "")
        blueprint = fixture["blueprint"]
        systems = blueprint.get("library", {}).get("systems", [])

        truth = GROUND_TRUTH.get(name, {})
        expected_layers = truth.get("expected_layers", {})

        if not expected_layers:
            print(f"  - {name}: 无expected_layers标注，跳过")
            continue

        # 加载策略
        intent_result = next(r for r in intent_results if r["name"] == name)
        perspective_id = intent_result["predicted_strategy"]
        overlay_id = intent_result["predicted_intent"]["secondary"]

        perspective = load_perspective(perspective_id)
        overlay = load_overlay(overlay_id)

        engine = RuleEngine(perspective, overlay)

        # 分配层级
        predicted_layers = {}
        for system in systems:
            system_id = system.get("id")
            if system_id in expected_layers:
                assignment = engine.assign_layer(system)
                predicted_layers[system_id] = assignment["layer"]

        # 计算准确率
        layer_order = perspective.get("layerOrder", list(expected_layers.values()))
        accuracy = weighted_layer_accuracy(predicted_layers, expected_layers, layer_order)

        layer_results.append({
            "name": name,
            "predicted_layers": predicted_layers,
            "expected_layers": expected_layers,
            "accuracy": accuracy
        })

        status = "✓" if accuracy >= 0.8 else "⚠"
        print(f"  {status} {name}: {accuracy:.2%}")
        for sys_id, pred_layer in predicted_layers.items():
            exp_layer = expected_layers.get(sys_id)
            match = "✓" if pred_layer == exp_layer else "✗"
            print(f"    {match} {sys_id}: {pred_layer} vs {exp_layer}")

    # 5. 计算整体层级准确率
    if layer_results:
        overall_layer_accuracy = sum(r["accuracy"] for r in layer_results) / len(layer_results)
        print(f"\nLayer Accuracy: {overall_layer_accuracy:.2%}")
    else:
        overall_layer_accuracy = 0.0
        print("\nLayer Accuracy: 无测试数据")

    # 6. 自动选择成功率
    print("\n4. 自动选择成功率...")
    auto_success_count = sum(
        1 for r in intent_results
        if r["accuracy"] >= 0.8 and r["confidence"] >= 0.75
    )
    auto_success_rate = auto_success_count / len(intent_results)
    print(f"Auto-Selection Success Rate: {auto_success_rate:.2%}")

    # 7. 达标检查
    print("\n5. 达标检查...")
    thresholds = {
        "intent_accuracy": 0.85,
        "layer_accuracy": 0.88,
        "auto_success_rate": 0.70
    }

    pass_status = (
        overall_intent_accuracy >= thresholds["intent_accuracy"] and
        overall_layer_accuracy >= thresholds["layer_accuracy"] and
        auto_success_rate >= thresholds["auto_success_rate"]
    )

    print(f"Intent Accuracy: {overall_intent_accuracy:.2%} >= {thresholds['intent_accuracy']:.0%} {'✓' if overall_intent_accuracy >= thresholds['intent_accuracy'] else '✗'}")
    print(f"Layer Accuracy: {overall_layer_accuracy:.2%} >= {thresholds['layer_accuracy']:.0%} {'✓' if overall_layer_accuracy >= thresholds['layer_accuracy'] else '✗'}")
    print(f"Auto-Selection Success: {auto_success_rate:.2%} >= {thresholds['auto_success_rate']:.0%} {'✓' if auto_success_rate >= thresholds['auto_success_rate'] else '✗'}")

    if pass_status:
        print("\n✓ Phase 1 测试通过")
    else:
        print("\n✗ Phase 1 测试失败")

    # 8. 生成报告
    report = {
        "test_phase": "Phase 1",
        "test_date": "2026-04-25",
        "metrics": {
            "intent_inference_accuracy": (overall_intent_accuracy, thresholds["intent_accuracy"]),
            "layer_assignment_accuracy": (overall_layer_accuracy, thresholds["layer_accuracy"]),
            "auto_selection_success_rate": (auto_success_rate, thresholds["auto_success_rate"])
        },
        "detailed_results": {
            "intent_results": intent_results,
            "layer_results": layer_results
        },
        "pass_status": pass_status,
        "failed_cases": [
            r for r in intent_results + layer_results
            if r.get("accuracy", 0) < 0.8
        ]
    }

    # 保存报告
    output_file = Path("reports/phase1_accuracy_report.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    json.dump(report, open(output_file, "w"), indent=2, ensure_ascii=False)

    print(f"\n报告已保存: {output_file}")
    print("=" * 80)

    return report


if __name__ == "__main__":
    report = phase1_accuracy_test()
    print("\n完整报告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))