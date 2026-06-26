#!/usr/bin/env python3
"""
CodeQL + LLM 一键扫描分析工具

使用方法:
    uv run python3 codeql_llm_scan.py /path/to/project

功能:
    1. CodeQL 扫描
    2. LLM 智能分析
    3. 生成报告
    4. 自动打开报告
"""

import asyncio
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# 检查依赖
try:
    from openclaw_sdk import OpenClawClient
    from pydantic import BaseModel
except ImportError:
    print("❌ 需要安装 OpenClaw SDK")
    print("   运行：cd /root/source/openclaw-sdk && uv pip install -e .")
    sys.exit(1)


class SecurityAnalysis(BaseModel):
    """安全分析结果"""
    summary: str
    total_vulnerabilities: int
    by_severity: dict[str, int]
    critical_issues: list[str]
    top_5_priorities: list[str]
    false_positives: list[str]
    remediation_steps: list[str]
    exploit_difficulty: str
    confidence_score: float


def check_codeql():
    """检查 CodeQL 是否安装"""
    try:
        result = subprocess.run(
            ["codeql", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.split('\n')[0]
    except Exception as e:
        return False, str(e)


def create_database(source_root: str, db_path: str):
    """创建 CodeQL 数据库"""
    print("📦 创建 CodeQL 数据库...")
    
    cmd = [
        "codeql", "database", "create", db_path,
        "--language", "python",
        "--source-root", source_root,
        "--overwrite"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 数据库创建成功")
        return True
    else:
        print(f"❌ 数据库创建失败：{result.stderr}")
        return False


def run_analysis(db_path: str, output_sarif: str):
    """运行 CodeQL 分析"""
    print("🔍 运行 CodeQL 安全分析...")
    
    # 下载查询包
    subprocess.run(
        ["codeql", "pack", "download", "codeql/python-queries"],
        capture_output=True
    )
    
    # 查找查询套件
    home = Path.home()
    suite_path = home / ".codeql/packages/codeql/python-queries/*/codeql-suites/python-security-extended.qls"
    
    import glob
    matches = glob.glob(str(suite_path))
    if not matches:
        print("❌ 未找到查询套件")
        return False
    
    query_suite = matches[0]
    
    # 运行分析
    cmd = [
        "codeql", "database", "analyze", db_path,
        query_suite,
        "--format=sarif-latest",
        "--output", output_sarif
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 分析完成")
        return True
    else:
        print(f"❌ 分析失败：{result.stderr}")
        return False


async def analyze_with_llm(sarif_file: str) -> SecurityAnalysis:
    """使用 OpenClaw LLM 分析 SARIF 结果"""
    print("\n🤖 使用 OpenClaw LLM 分析...")
    
    # 读取 SARIF
    with open(sarif_file, 'r', encoding='utf-8') as f:
        sarif_data = json.load(f)
    
    results = sarif_data.get('runs', [{}])[0].get('results', [])
    
    # 准备分析内容
    sarif_excerpt = json.dumps(results[:30], indent=2, ensure_ascii=False)
    
    analysis_prompt = f"""
你是一个专业的安全分析师。请分析这个 CodeQL 安全扫描结果：

## 扫描数据

{sarif_excerpt}

## 分析要求

请提供：
1. **摘要** - 200 字以内的整体评估
2. **统计** - 按严重程度分类
3. **关键问题** - 最危险的 3-5 个漏洞
4. **前 5 优先级** - 最应该优先修复的 5 个问题
5. **误报识别** - 可能的误报
6. **修复建议** - 具体可执行的修复步骤
7. **利用难度** - 低/中/高
8. **置信度** - 0-100 分
"""
    
    try:
        async with OpenClawClient.connect() as client:
            agent = client.get_agent("security-analyst")
            
            print("📝 执行 LLM 分析...")
            
            analysis: SecurityAnalysis = await agent.execute_structured(
                analysis_prompt,
                output_model=SecurityAnalysis,
                timeout=120
            )
            
            print("✅ LLM 分析完成")
            return analysis
            
    except Exception as e:
        print(f"⚠️ LLM 分析失败：{e}")
        print("   将生成基础报告（无 LLM 增强）")
        
        # 返回基础分析
        return SecurityAnalysis(
            summary=f"CodeQL 扫描发现 {len(results)} 个安全问题",
            total_vulnerabilities=len(results),
            by_severity={"none": len(results)},
            critical_issues=[],
            top_5_priorities=[],
            false_positives=[],
            remediation_steps=["查看完整报告了解详细信息"],
            exploit_difficulty="未知",
            confidence_score=0.0
        )


def generate_report(analysis: SecurityAnalysis, sarif_file: str, output_md: str):
    """生成 Markdown 报告"""
    print(f"\n📝 生成分析报告...")
    
    report = f"""# CodeQL 安全扫描报告（LLM 增强版）

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**扫描目标**: {Path(sarif_file).parent.name}
**分析引擎**: OpenClaw LLM
**置信度**: {analysis.confidence_score}%

---

## 📊 执行摘要

{analysis.summary}

---

## 📈 漏洞统计

| 严重程度 | 数量 |
|----------|------|
"""
    
    for severity, count in analysis.by_severity.items():
        emoji = {"error": "🔴", "warning": "🟠", "note": "🟡", "none": "⚪"}.get(severity.lower(), "⚪")
        report += f"| {emoji} {severity} | {count} |\n"
    
    report += f"\n**总漏洞数**: {analysis.total_vulnerabilities}\n"
    report += f"**利用难度**: {analysis.exploit_difficulty}\n"
    
    if analysis.critical_issues:
        report += f"""
---

## 🔴 关键问题

"""
        for i, issue in enumerate(analysis.critical_issues, 1):
            report += f"{i}. {issue}\n\n"
    
    if analysis.top_5_priorities:
        report += f"""
---

## 🎯 优先修复清单（Top 5）

"""
        for i, item in enumerate(analysis.top_5_priorities, 1):
            report += f"{i}. {item}\n"
    
    if analysis.remediation_steps:
        report += f"""
---

## 🔧 修复建议

"""
        for i, step in enumerate(analysis.remediation_steps, 1):
            report += f"{i}. {step}\n"
    
    report += f"""
---

## ⚠️ 可能的误报

"""
    if analysis.false_positives:
        for i, fp in enumerate(analysis.false_positives, 1):
            report += f"{i}. {fp}\n"
    else:
        report += "未发现明显误报。\n"
    
    report += f"""
---

## 📁 原始数据

- **SARIF 文件**: {sarif_file}
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

**报告生成**: CodeQL + OpenClaw LLM 融合扫描器
"""
    
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{output_md}")
    return report


def open_file(file_path: str):
    """尝试打开文件"""
    print(f"\n📖 尝试打开报告...")
    
    # 尝试使用 xdg-open（Linux）
    try:
        subprocess.run(["xdg-open", file_path], check=True)
        print(f"✅ 已在浏览器中打开：{file_path}")
        return
    except:
        pass
    
    # 尝试使用默认编辑器
    editor = os.environ.get('EDITOR', 'vim')
    print(f"💡 使用 {editor} 打开报告")
    subprocess.run([editor, file_path])


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  {sys.argv[0]} /path/to/project")
        print("\n示例:")
        print(f"  {sys.argv[0]} /root/devsecops-python-web")
        sys.exit(1)
    
    target = sys.argv[1]
    output_dir = Path(f"./scan-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    output_dir.mkdir(exist_ok=True)
    
    sarif_file = output_dir / "codeql-results.sarif"
    report_file = output_dir / "llm-analysis.md"
    db_path = output_dir / "codeql-db"
    
    print("=" * 60)
    print("  CodeQL + LLM 一键扫描分析")
    print("=" * 60)
    print()
    
    # 1. 检查 CodeQL
    print("🔍 检查 CodeQL...")
    codeql_installed, version = check_codeql()
    
    if not codeql_installed:
        print(f"❌ CodeQL 未安装：{version}")
        print("   请安装 CodeQL")
        sys.exit(1)
    
    print(f"✅ CodeQL 已安装：{version}")
    print()
    
    # 2. 创建数据库
    if not create_database(target, str(db_path)):
        sys.exit(1)
    print()
    
    # 3. 运行分析
    if not run_analysis(str(db_path), str(sarif_file)):
        sys.exit(1)
    print()
    
    # 4. LLM 分析
    analysis = await analyze_with_llm(str(sarif_file))
    print()
    
    # 5. 生成报告
    generate_report(analysis, str(sarif_file), str(report_file))
    print()
    
    # 6. 显示摘要
    print("=" * 60)
    print("  分析摘要")
    print("=" * 60)
    print(f"\n{analysis.summary}")
    print(f"\n📊 统计:")
    for severity, count in analysis.by_severity.items():
        print(f"   {severity}: {count}")
    
    if analysis.top_5_priorities:
        print(f"\n🎯 前 5 优先级:")
        for i, item in enumerate(analysis.top_5_priorities, 1):
            print(f"   {i}. {item}")
    
    print(f"\n💡 置信度：{analysis.confidence_score}%")
    print()
    
    # 7. 打开报告
    open_file(str(report_file))
    
    print("\n" + "=" * 60)
    print("  ✅ 扫描分析完成！")
    print("=" * 60)
    print(f"\n📁 输出目录：{output_dir}")
    print(f"📄 报告文件：{report_file}")
    print(f"📊 SARIF 文件：{sarif_file}")
    print()


if __name__ == '__main__':
    asyncio.run(main())
