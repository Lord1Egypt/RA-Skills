#!/usr/bin/env python3
"""
PaperMC插件升级框架使用示例
基于ViaVersion升级经验的最佳实践
"""

import json
from pathlib import Path
from plugin_upgrade_framework import PluginUpgradeFramework

def example1_viaversion_upgrade():
    """示例1: ViaVersion升级（基于实际经验）"""
    print("="*60)
    print("示例1: ViaVersion插件升级")
    print("基于2026-03-28实际升级经验")
    print("="*60)
    
    framework = PluginUpgradeFramework()
    
    # 模拟ViaVersion升级场景
    result = framework.method1_specific_plugin_upgrade(
        plugin_name="ViaVersion",
        target_version="5.8.0"  # 实际升级到的版本
    )
    
    print(f"\n升级结果:")
    print(f"  插件: {result.get('plugin')}")
    print(f"  当前版本: {result.get('current_version', 'unknown')}")
    print(f"  目标版本: {result.get('target_version', 'unknown')}")
    print(f"  成功: {result.get('success')}")
    
    if result.get("risk_assessment"):
        risk = result["risk_assessment"]
        print(f"\n风险评估:")
        print(f"  风险等级: {risk.get('risk_level')}")
        print(f"  风险因素: {', '.join(risk.get('risk_factors', []))}")
        print(f"  需要重启: {risk.get('restart_required')}")
        print(f"  建议测试: {risk.get('testing_recommended')}")
    
    if result.get("steps"):
        print(f"\n执行步骤:")
        for step in result["steps"]:
            print(f"  [{step.get('status', 'unknown')}] {step.get('step')}: {step.get('message', '')}")
    
    if result.get("restart_plan"):
        plan = result["restart_plan"]
        print(f"\n重启计划:")
        print(f"  建议时间: {plan.get('recommended_time')}")
        print(f"  预计停机: {plan.get('estimated_downtime')}")
    
    return result

def example2_scan_for_upgrades():
    """示例2: 扫描可升级插件"""
    print("\n" + "="*60)
    print("示例2: 扫描并评估插件升级")
    print("="*60)
    
    framework = PluginUpgradeFramework()
    
    # 扫描前20个热门插件
    result = framework.method2_scan_and_assess_upgrades(limit=20)
    
    print(f"\n扫描结果摘要:")
    summary = result.get("summary", {})
    print(f"  已安装插件: {result.get('installed_count', 0)}")
    print(f"  扫描插件数: {result.get('scanned_plugins', 0)}")
    print(f"  可升级候选: {summary.get('total_candidates', 0)}")
    print(f"  - 高风险: {summary.get('high_risk', 0)}")
    print(f"  - 中风险: {summary.get('medium_risk', 0)}")
    print(f"  - 低风险: {summary.get('low_risk', 0)}")
    print(f"  推荐升级: {summary.get('recommended', 0)}")
    
    # 显示推荐升级的插件
    candidates = result.get("upgrade_candidates", [])
    if candidates:
        print(f"\n推荐升级的插件:")
        for candidate in candidates:
            if candidate.get("recommendation") == "recommended":
                print(f"  - {candidate['plugin']}: {candidate['current_version']} → {candidate['latest_version']}")
                assessment = candidate.get("assessment", {})
                print(f"    风险等级: {assessment.get('risk_level')}")
                print(f"    下载URL: {candidate.get('download_url', '未获取')[:50]}...")
    
    # 显示需要谨慎的插件
    print(f"\n需要谨慎升级的插件:")
    for candidate in candidates:
        if candidate.get("recommendation") == "caution":
            print(f"  ⚠️  {candidate['plugin']}: {candidate['current_version']} → {candidate['latest_version']}")
            print(f"     风险因素: {', '.join(candidate['assessment'].get('risk_factors', []))}")
    
    return result

def example3_complete_upgrade_workflow():
    """示例3: 完整升级工作流（包含重启）"""
    print("\n" + "="*60)
    print("示例3: 完整升级工作流")
    print("包含准备、升级、重启全流程")
    print("="*60)
    
    framework = PluginUpgradeFramework()
    
    # 获取服务器信息
    server_info = framework.get_server_info()
    print(f"\n服务器信息:")
    print(f"  服务器目录: {server_info.get('server_dir')}")
    print(f"  Paper版本: {server_info.get('paper_version')}")
    print(f"  插件数量: {server_info.get('plugins_count')}")
    
    # 演示完整升级流程（不实际执行）
    print(f"\n完整升级流程演示:")
    print("1. 检查当前插件状态")
    print("2. 获取最新版本信息")
    print("3. 风险评估和预案制定")
    print("4. 备份当前版本")
    print("5. 下载新版本")
    print("6. 替换插件文件")
    print("7. 执行服务器重启")
    print("8. 验证升级结果")
    
    # 生成升级报告模板
    report_template = {
        "upgrade_report": {
            "server": server_info,
            "pre_upgrade_checklist": [
                "确认服务器备份完成",
                "通知玩家维护时间",
                "验证插件兼容性",
                "准备回滚方案"
            ],
            "upgrade_steps": [
                "停止服务器",
                "备份插件和世界数据",
                "下载新版本插件",
                "替换插件文件",
                "启动服务器",
                "验证功能正常"
            ],
            "post_upgrade_validation": [
                "检查服务器日志无错误",
                "验证核心功能正常",
                "测试插件特定功能",
                "监控服务器性能"
            ],
            "rollback_procedure": [
                "停止服务器",
                "恢复备份文件",
                "删除新版本文件",
                "重启服务器",
                "验证恢复状态"
            ]
        }
    }
    
    print(f"\n升级报告模板已生成")
    return report_template

def example4_batch_upgrade_planning():
    """示例4: 批量升级规划"""
    print("\n" + "="*60)
    print("示例4: 批量升级规划")
    print("基于风险评估的升级优先级排序")
    print("="*60)
    
    framework = PluginUpgradeFramework()
    
    # 获取可升级插件列表
    scan_result = framework.method2_scan_and_assess_upgrades(limit=30)
    candidates = scan_result.get("upgrade_candidates", [])
    
    if not candidates:
        print("未找到可升级插件")
        return
    
    # 按风险等级和推荐程度排序
    priority_order = {
        ("low", "recommended"): 1,    # 最高优先级
        ("medium", "recommended"): 2,
        ("low", "consider"): 3,
        ("medium", "consider"): 4,
        ("high", "consider"): 5,
        ("high", "caution"): 6        # 最低优先级
    }
    
    # 计算优先级
    for candidate in candidates:
        risk_level = candidate["assessment"]["risk_level"]
        recommendation = candidate["recommendation"]
        priority = priority_order.get((risk_level, recommendation), 99)
        candidate["priority"] = priority
    
    # 按优先级排序
    candidates.sort(key=lambda x: x["priority"])
    
    print(f"\n批量升级计划（按优先级排序）:")
    for i, candidate in enumerate(candidates[:10], 1):  # 显示前10个
        print(f"\n{i}. {candidate['plugin']}")
        print(f"   版本: {candidate['current_version']} → {candidate['latest_version']}")
        print(f"   优先级: {candidate['priority']}")
        print(f"   风险等级: {candidate['assessment']['risk_level']}")
        print(f"   建议: {candidate['recommendation']}")
        
        # 生成升级时间建议
        if candidate['priority'] <= 2:
            print(f"   升级时机: 下次维护窗口")
        elif candidate['priority'] <= 4:
            print(f"   升级时机: 下月维护窗口")
        else:
            print(f"   升级时机: 评估后决定")
    
    # 生成升级批次建议
    print(f"\n升级批次建议:")
    print(f"第一批（优先级1-2）: 低风险推荐升级，可立即执行")
    print(f"第二批（优先级3-4）: 中等风险，建议测试后升级")
    print(f"第三批（优先级5-6）: 高风险，需要详细评估")
    
    return candidates

def save_examples_to_file():
    """保存示例结果到文件"""
    print("\n" + "="*60)
    print("保存示例结果到文件")
    print("="*60)
    
    results = {}
    
    # 执行示例1
    print("\n执行示例1: ViaVersion升级演示...")
    results["example1_viaversion"] = example1_viaversion_upgrade()
    
    # 执行示例2
    print("\n执行示例2: 扫描升级演示...")
    results["example2_scan"] = example2_scan_for_upgrades()
    
    # 执行示例3
    print("\n执行示例3: 完整工作流演示...")
    results["example3_workflow"] = example3_complete_upgrade_workflow()
    
    # 执行示例4
    print("\n执行示例4: 批量规划演示...")
    results["example4_batch"] = example4_batch_upgrade_planning()
    
    # 保存到文件
    output_file = Path.home() / ".openclaw" / "workspace" / "papermc_upgrade_examples.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n所有示例结果已保存到: {output_file}")
    print(f"文件大小: {output_file.stat().st_size} 字节")
    
    return results

def main():
    """主函数：运行所有示例"""
    print("PaperMC插件升级框架 - 使用示例")
    print("基于ViaVersion升级经验的最佳实践")
    print("="*60)
    
    try:
        # 运行所有示例并保存结果
        results = save_examples_to_file()
        
        print("\n" + "="*60)
        print("示例执行完成！")
        print("="*60)
        
        # 显示关键统计
        total_candidates = 0
        if "example2_scan" in results and results["example2_scan"]:
            total_candidates = results["example2_scan"].get("summary", {}).get("total_candidates", 0)
        
        print(f"\n关键统计:")
        print(f"  • 可升级插件候选: {total_candidates}")
        print(f"  • ViaVersion升级演示: 完成")
        print(f"  • 完整工作流模板: 生成")
        print(f"  • 批量升级计划: 创建")
        
        print(f"\n下一步建议:")
        print(f"  1. 查看保存的示例文件了解详细信息")
        print(f"  2. 使用框架进行实际插件升级")
        print(f"  3. 根据服务器情况调整风险评估逻辑")
        print(f"  4. 建立定期升级检查机制")
        
    except Exception as e:
        print(f"\n执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return results

if __name__ == "__main__":
    main()