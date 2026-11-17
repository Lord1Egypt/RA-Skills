#!/usr/bin/env python3
"""
IMRC 运营报告测试脚本

测试报告生成流程：
1. 加载 IMRC 数据
2. 加载美信消息
3. 生成整体介绍（第一页）
4. 生成分项报告
5. 导出完整报告
"""

import sys
import json
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from report_generator import (
    load_imrc_data,
    load_meixin_data,
    generate_summary,
    generate_section_report,
    generate_full_report,
    export_report
)


def test_load_imrc_data():
    """测试加载 IMRC 数据"""
    print("=" * 60)
    print("测试1: 加载 IMRC 数据")
    print("=" * 60)
    
    data = load_imrc_data("2026-07")
    
    if data:
        print(f"✅ 数据加载成功")
        print(f"   月份: {data.get('month', '-')}")
        print(f"   页面数: {len(data.get('pages', []))}")
    else:
        print(f"⚠️  数据为空（可能尚未提取）")
    
    return True


def test_load_meixin_data():
    """测试加载美信消息"""
    print("\n" + "=" * 60)
    print("测试2: 加载美信消息")
    print("=" * 60)
    
    data = load_meixin_data()
    
    if data:
        print(f"✅ 美信消息加载成功")
        print(f"   长度: {len(data)} 字符")
    else:
        print(f"⚠️  美信消息为空")
    
    return True


def test_generate_summary():
    """测试生成整体介绍（第一页）"""
    print("\n" + "=" * 60)
    print("测试3: 生成整体介绍（第一页）")
    print("=" * 60)
    
    imrc_data = load_imrc_data("2026-07")
    summary = generate_summary(imrc_data, "2026-07")
    
    if summary:
        print(f"✅ 整体介绍生成成功")
        print(f"   长度: {len(summary)} 字符")
        print(f"\n--- 前 500 字符 ---")
        print(summary[:500])
        print("...")
    else:
        print(f"❌ 整体介绍生成失败")
        return False
    
    return True


def test_generate_section_report():
    """测试生成分项报告"""
    print("\n" + "=" * 60)
    print("测试4: 生成分项报告")
    print("=" * 60)
    
    test_page = {
        "page_id": 1,
        "page_name": "项目运营情况",
        "url": "https://imrc.midea.com/analysis/projectOverviewOperations",
        "unit": "-",
        "extracted_at": "2026-07-13T07:00:00"
    }
    
    section = generate_section_report(test_page)
    
    if section:
        print(f"✅ 分项报告生成成功")
        print(f"   长度: {len(section)} 字符")
    else:
        print(f"❌ 分项报告生成失败")
        return False
    
    return True


def test_generate_full_report():
    """测试生成完整报告"""
    print("\n" + "=" * 60)
    print("测试5: 生成完整报告")
    print("=" * 60)
    
    report = generate_full_report("2026-07")
    
    if report:
        print(f"✅ 完整报告生成成功")
        print(f"   长度: {len(report)} 字符")
        print(f"   包含整体介绍: {'核心指标速览' in report}")
        print(f"   包含分项报告: {'分项报告' in report}")
        print(f"   包含美信消息: {'美信消息摘要' in report}")
    else:
        print(f"❌ 完整报告生成失败")
        return False
    
    return True


def test_export_report():
    """测试导出报告"""
    print("\n" + "=" * 60)
    print("测试6: 导出报告")
    print("=" * 60)
    
    report = generate_full_report("2026-07")
    output_path = Path(__file__).parent.parent / "test_output.md"
    
    try:
        saved_path = export_report(report, output_path)
        if saved_path.exists():
            print(f"✅ 报告导出成功")
            print(f"   路径: {saved_path}")
            print(f"   大小: {saved_path.stat().st_size} 字节")
            
            # 清理测试文件
            saved_path.unlink()
            print(f"   已清理测试文件")
        else:
            print(f"❌ 报告导出失败")
            return False
    except Exception as e:
        print(f"❌ 导出异常: {e}")
        return False
    
    return True


def main():
    print("\n" + "=" * 60)
    print("IMRC 运营报告测试套件")
    print("=" * 60)
    
    tests = [
        test_load_imrc_data,
        test_load_meixin_data,
        test_generate_summary,
        test_generate_section_report,
        test_generate_full_report,
        test_export_report
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"测试结果: {sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
