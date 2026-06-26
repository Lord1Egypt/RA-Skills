#!/usr/bin/env python3
"""
使用 OpenClaw LLM 分析 CodeQL 扫描结果

使用方法:
    uv run python3 analyze_with_llm.py ./test-output/codeql-results.sarif -o llm-analysis.md
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from openclaw_sdk import OpenClawClient
    from pydantic import BaseModel
except ImportError:
    print("❌ 需要安装 OpenClaw SDK:")
    print("   pip install openclaw-sdk")
    print("   或：cd /root/source/openclaw-sdk && pip install -e .")
    sys.exit(1)


class VulnerabilityAnalysis(BaseModel):
    """漏洞分析结果模型"""
    summary: str
    total_vulnerabilities: int
    by_severity: dict[str, int]
    critical_issues: list[str]
    high_priority: list[str]
    false_positives: list[str]
    top_5_priorities: list[str]
    remediation_steps: list[str]
    exploit_difficulty: str
    confidence_score: float


async def analyze_sarif(sarif_file: str, output_file: str, agent_id: str = "security-analyst"):
    """
    分析 SARIF 文件
    
    Args:
        sarif_file: SARIF 文件路径
        output_file: 输出文件路径
        agent_id: OpenClaw Agent ID
    """
    
    print("=" * 60)
    print("  CodeQL LLM 分析工具")
    print("  使用 OpenClaw SDK")
    print("=" * 60)
    print()
    
    # 1. 读取 SARIF 文件
    print(f"📖 读取 SARIF 文件：{sarif_file}")
    
    if not Path(sarif_file).exists():
        print(f"❌ 文件不存在：{sarif_file}")
        return False
    
    with open(sarif_file, 'r', encoding='utf-8') as f:
        sarif_data = json.load(f)
    
    # 2. 提取关键信息
    print("📊 提取漏洞信息...")
    
    runs = sarif_data.get('runs', [{}])
    results = []
    
    for run in runs:
        run_results = run.get('results', [])
        results.extend(run_results)
    
    print(f"   发现 {len(results)} 个漏洞")
    
    # 3. 准备分析提示
    # 限制长度，避免超出 token 限制
    sarif_excerpt = json.dumps(results[:30], indent=2, ensure_ascii=False)
    
    analysis_prompt = f"""
你是一个专业的安全分析师。请分析这个 CodeQL 安全扫描结果：

## 扫描数据

{sarif_excerpt}

## 分析要求

请提供详细的分析报告，包括：

1. **摘要** - 200 字以内的整体评估
2. **统计** - 按严重程度分类统计
3. **关键问题** - 最危险的 3-5 个漏洞，说明原因
4. **高优先级** - 需要优先修复的问题
5. **误报识别** - 可能的误报（如测试代码、依赖包示例等）
6. **前 5 优先级** - 最应该优先修复的 5 个问题
7. **修复建议** - 具体可执行的修复步骤，按优先级排序
8. **利用难度** - 整体利用难度评估（低/中/高）
9. **置信度** - 0-100 分，表示分析的可信度

请以专业的安全报告格式输出。
"""
    
    # 4. 连接 OpenClaw 并执行分析
    print(f"\n🤖 连接 OpenClaw Gateway...")
    
    try:
        async with OpenClawClient.connect() as client:
            print(f"✅ 连接成功")
            
            print(f"\n🔍 调用 Agent: {agent_id}")
            agent = client.get_agent(agent_id)
            
            print(f"📝 执行 LLM 分析...")
            
            # 执行结构化分析
            analysis: VulnerabilityAnalysis = await agent.execute_structured(
                analysis_prompt,
                output_model=VulnerabilityAnalysis,
                timeout=120  # 2 分钟超时
            )
            
            print(f"✅ 分析完成")
            
            # 5. 生成报告
            print(f"\n📝 生成分析报告...")
            
            report_content = generate_report(analysis, sarif_file)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"✅ 报告已保存：{output_file}")
            
            # 6. 显示摘要
            print(f"\n" + "=" * 60)
            print("  分析摘要")
            print("=" * 60)
            print(f"\n{analysis.summary}")
            print(f"\n📊 统计:")
            for severity, count in analysis.by_severity.items():
                print(f"   {severity}: {count}")
            print(f"\n🎯 前 5 优先级:")
            for i, item in enumerate(analysis.top_5_priorities, 1):
                print(f"   {i}. {item}")
            print(f"\n💡 置信度：{analysis.confidence_score}%")
            
            return True
            
    except Exception as e:
        print(f"❌ 分析失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def generate_report(analysis: VulnerabilityAnalysis, sarif_file: str) -> str:
    """生成 Markdown 报告"""
    
    report = f"""# CodeQL 漏洞分析报告（LLM 增强版）

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**源文件**: {Path(sarif_file).name}
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
        report += f"| {severity} | {count} |\n"
    
    report += f"\n**总漏洞数**: {analysis.total_vulnerabilities}\n"
    report += f"**利用难度**: {analysis.exploit_difficulty}\n"
    
    report += f"""
---

## 🔴 关键问题

"""
    
    for i, issue in enumerate(analysis.critical_issues, 1):
        report += f"{i}. {issue}\n\n"
    
    report += f"""
---

## 🎯 优先修复清单（Top 5）

"""
    
    for i, item in enumerate(analysis.top_5_priorities, 1):
        report += f"{i}. {item}\n"
    
    report += f"""
---

## 🔧 修复建议

"""
    
    for i, step in enumerate(analysis.remediation_steps, 1):
        report += f"{i}. {step}\n"
    
    report += f"""
---

## ⚠️ 可能的误报

以下问题可能是误报，建议人工复核：

"""
    
    if analysis.false_positives:
        for i, fp in enumerate(analysis.false_positives, 1):
            report += f"{i}. {fp}\n"
    else:
        report += "未发现明显误报。\n"
    
    report += f"""
---

## 📋 高优先级问题

"""
    
    for i, item in enumerate(analysis.high_priority, 1):
        report += f"{i}. {item}\n"
    
    report += f"""
---

## ℹ️ 使用说明

### 立即行动

1. 优先修复 **前 5 优先级** 中的问题
2. 按照 **修复建议** 逐步改进
3. 对 **可能的误报** 进行人工复核

### 查看原始数据

- SARIF 文件：{sarif_file}
- 可用 SARIF Viewer 查看详细信息

### 重新分析

```bash
python3 analyze_with_llm.py {sarif_file} -o new-analysis.md
```

---

**报告生成**: CodeQL + OpenClaw LLM 融合扫描器
**版本**: 1.0.0
"""
    
    return report


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='使用 OpenClaw LLM 分析 CodeQL 扫描结果',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析 SARIF 文件
  python3 analyze_with_llm.py ./test-output/codeql-results.sarif
  
  # 指定输出文件
  python3 analyze_with_llm.py ./test-output/codeql-results.sarif -o llm-analysis.md
  
  # 使用不同的 Agent
  python3 analyze_with_llm.py ./test-output/codeql-results.sarif --agent security-expert
        """
    )
    
    parser.add_argument('sarif_file', help='SARIF 文件路径')
    parser.add_argument('-o', '--output', default='llm-analysis.md', help='输出文件路径')
    parser.add_argument('--agent', default='security-analyst', help='Agent ID')
    parser.add_argument('--timeout', type=int, default=120, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    success = await analyze_sarif(
        args.sarif_file,
        args.output,
        args.agent
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    asyncio.run(main())
