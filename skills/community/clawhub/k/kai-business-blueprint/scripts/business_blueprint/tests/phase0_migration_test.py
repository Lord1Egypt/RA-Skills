"""
Phase 0 迁移验证测试

验证迁移后蓝图输出与旧输出的一致性
"""

import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from scripts.business_blueprint.tests.metrics import (
    parse_svg_structure,
    compare_svg_structure,
    migration_consistency_rate,
    generate_metrics_report
)
from scripts.business_blueprint.tests.test_utils import (
    load_golden_fixtures,
    run_export_command,
    copy_output_to_fixture,
    save_test_result
)
from scripts.business_blueprint.migrations.v1_to_v2 import (
    migrate_blueprint_v1_to_v2,
    batch_migrate
)


def phase0_migration_test():
    """Phase 0测试：迁移验证"""
    print("=" * 80)
    print("Phase 0: Migration Consistency Test")
    print("=" * 80)

    # 1. 准备Golden Fixtures
    fixtures_dir = "demos"
    fixtures = load_golden_fixtures(fixtures_dir)

    print(f"\n1. 加载Golden Fixtures: {len(fixtures)} 个蓝图")

    if not fixtures:
        print("✗ 无测试数据，测试失败")
        return {
            "test_phase": "Phase 0",
            "pass_status": False,
            "error": "No test fixtures found"
        }

    # 2. 导出旧版本输出（baseline）
    print("\n2. 导出旧版本输出作为baseline...")

    fixture_baseline_dir = Path("scripts/business_blueprint/fixtures/golden_v1")
    fixture_baseline_dir.mkdir(parents=True, exist_ok=True)

    baseline_outputs = []
    for fixture in fixtures:
        blueprint_path = fixture["path"]
        name = fixture["name"]

        print(f"  - 导出 {name}...")
        result = run_export_command(blueprint_path, str(fixture_baseline_dir))

        if result["success"]:
            # 复制输出到baseline目录
            copy_output_to_fixture(
                result["exports_dir"],
                str(fixture_baseline_dir),
                name
            )
            baseline_outputs.append({
                "name": name,
                "path": blueprint_path,
                "exports_dir": result["exports_dir"]
            })
            print(f"    ✓ baseline保存: {name}.svg")
        else:
            print(f"    ✗ 导出失败: {name}")

    print(f"Baseline输出: {len(baseline_outputs)} 个")

    # 3. 迁移所有fixtures
    print("\n3. 迁移所有蓝图到v2格式...")

    migrated_dir = Path("test_data/migrated_blueprints")
    migrated_dir.mkdir(parents=True, exist_ok=True)

    migration_result = batch_migrate(fixtures_dir, str(migrated_dir))
    print(f"迁移完成: {migration_result['migrated_count']} 成功")

    # 4. 导出迁移后版本
    print("\n4. 导出迁移后蓝图...")

    migrated_outputs = []
    for fixture in fixtures:
        blueprint_path = fixture["path"]
        name = fixture["name"]

        # 加载迁移后的蓝图
        migrated_blueprint_path = migrated_dir / Path(blueprint_path).name

        if migrated_blueprint_path.exists():
            print(f"  - 导出 {name} (v2)...")
            result = run_export_command(str(migrated_blueprint_path), str(fixture_baseline_dir))

            if result["success"]:
                migrated_outputs.append({
                    "name": name,
                    "path": str(migrated_blueprint_path),
                    "exports_dir": result["exports_dir"]
                })
                print(f"    ✓ v2导出成功")
            else:
                print(f"    ✗ v2导出失败: {result.get('error', 'Unknown')}")

    print(f"V2输出: {len(migrated_outputs)} 个")

    # 5. 双跑比对
    print("\n5. 双跑比对（baseline vs v2）...")

    comparison_results = []
    for baseline in baseline_outputs:
        name = baseline["name"]

        # 找到对应的migrated输出
        migrated = next(
            (m for m in migrated_outputs if m["name"] == name),
            None
        )

        if not migrated:
            print(f"  - {name}: 无migrated输出")
            continue

        # 解析SVG结构
        baseline_svg_path = fixture_baseline_dir / f"{name}.svg"
        migrated_svg_path = Path(migrated["exports_dir"]) / f"{name}.svg"

        if baseline_svg_path.exists() and migrated_svg_path.exists():
            old_svg = parse_svg_structure(baseline_svg_path)
            new_svg = parse_svg_structure(migrated_svg_path)

            diff = compare_svg_structure(old_svg, new_svg)

            comparison_results.append({
                "name": name,
                "difference": diff,
                "old_svg": old_svg,
                "new_svg": new_svg
            })

            # 输出比对结果
            status = "✓" if not diff.route_change and diff.layer_changes < 0.2 else "✗"
            print(f"  - {name}: {status}")
            print(f"    路由: {old_svg['route']} → {new_svg['route']}")
            print(f"    层级变化: {diff.layer_changes:.2%}")

    # 6. 计算Migration Consistency Rate
    print("\n6. 计算Migration Consistency Rate...")

    if comparison_results:
        consistency_rate = migration_consistency_rate(
            [r["difference"] for r in comparison_results]
        )
        print(f"Migration Consistency Rate: {consistency_rate:.2%}")
    else:
        consistency_rate = 0.0
        print("✗ 无比对结果")

    # 7. 检查是否达标
    threshold = 0.95
    pass_status = consistency_rate >= threshold

    print(f"\n7. 达标检查: {consistency_rate:.2%} >= {threshold:.0%}")
    if pass_status:
        print("✓ Phase 0 测试通过")
    else:
        print("✗ Phase 0 测试失败")

    # 8. 统计失败案例
    failed_cases = [
        {
            "name": r["name"],
            "route_change": r["difference"].route_change,
            "layer_changes": r["difference"].layer_changes
        }
        for r in comparison_results
        if r["difference"].route_change or r["difference"].layer_changes >= 0.2
    ]

    # 9. 生成报告
    report = generate_metrics_report(
        "Phase 0",
        {
            "migration_consistency_rate": (consistency_rate, threshold)
        },
        failed_cases
    )

    # 10. 保存报告
    save_test_result(report, "reports/phase0_migration_report.json")

    print(f"\n报告已保存: reports/phase0_migration_report.json")
    print("=" * 80)

    return report


if __name__ == "__main__":
    report = phase0_migration_test()

    # 输出完整报告
    print("\n完整报告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))