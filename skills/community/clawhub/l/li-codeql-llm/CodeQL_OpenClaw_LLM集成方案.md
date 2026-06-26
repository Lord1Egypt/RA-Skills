# CodeQL + OpenClaw LLM 集成方案

**制定时间**: 2026-03-19 07:35  
**目标**: 使用 OpenClaw SDK 调用 LLM 分析 CodeQL 扫描结果

---

## 🎯 集成目标

### 当前状态

- ✅ CodeQL 扫描完成
- ✅ 生成 SARIF 报告
- ✅ 生成 Markdown 报告
- ❌ **未使用 LLM 分析**

### 期望功能

使用 OpenClaw SDK 调用 LLM 对 CodeQL 结果进行智能分析：

1. **漏洞优先级排序**
2. **误报识别**
3. **修复建议生成**
4. **可利用性分析**
5. **结构化输出**

---

## 📚 OpenClaw SDK 学习内容

### 核心组件

```python
from openclaw_sdk import OpenClawClient, Agent

# 1. 连接到 OpenClaw Gateway
client = OpenClawClient.connect()

# 2. 获取 Agent
agent = client.get_agent("security-analyst")

# 3. 执行查询
result = await agent.execute("分析这个 CodeQL 报告")

# 4. 结构化输出
from pydantic import BaseModel

class VulnerabilityReport(BaseModel):
    critical: int
    high: int
    medium: int
    recommendations: list[str]

report = await agent.execute_structured(
    "分析 CodeQL 扫描结果",
    output_model=VulnerabilityReport
)
```

### 可用功能

| 功能 | 方法 | 说明 |
|------|------|------|
| 执行查询 | `agent.execute()` | 同步执行 |
| 流式输出 | `agent.execute_stream()` | 流式事件 |
| 结构化输出 | `agent.execute_structured()` | Pydantic 模型 |
| 状态检查 | `agent.get_status()` | Agent 状态 |
| 列出 Agents | `client.list_agents()` | 可用 Agents |

---

## 🔧 集成方案

### 方案 1: 扫描后自动分析（推荐）✨

**流程**:
```
CodeQL 扫描 → 生成报告 → OpenClaw LLM 分析 → 增强报告
```

**实现**:
```python
# 在 scanner.py 中添加
async def analyze_with_llm(sarif_file: str, report_file: str):
    """使用 OpenClaw LLM 分析报告"""
    
    from openclaw_sdk import OpenClawClient
    from pydantic import BaseModel
    
    # 定义输出模型
    class SecurityAnalysis(BaseModel):
        summary: str
        critical_count: int
        high_count: int
        medium_count: int
        false_positives: list[str]
        top_5_priority: list[str]
        remediation_plan: list[str]
    
    # 连接 OpenClaw
    async with OpenClawClient.connect() as client:
        agent = client.get_agent("security-analyst")
        
        # 读取 SARIF 报告
        with open(sarif_file) as f:
            sarif_content = f.read()
        
        # 执行分析
        analysis: SecurityAnalysis = await agent.execute_structured(
            f"""分析这个 CodeQL 安全扫描报告：
            
            {sarif_content[:50000]}  # 限制长度
            
            请提供：
            1. 漏洞摘要
            2. 按严重程度统计
            3. 可能的误报
            4. 优先级前 5 的漏洞
            5. 修复建议""",
            output_model=SecurityAnalysis
        )
        
        # 生成增强报告
        generate_enhanced_report(analysis, report_file)
```

### 方案 2: 独立分析脚本

**文件**: `analyze_with_llm.py`

```python
#!/usr/bin/env python3
"""使用 OpenClaw LLM 分析 CodeQL 结果"""

import asyncio
import json
from pathlib import Path
from openclaw_sdk import OpenClawClient
from pydantic import BaseModel


class VulnerabilityAnalysis(BaseModel):
    """漏洞分析结果"""
    summary: str
    total_vulnerabilities: int
    by_severity: dict[str, int]
    critical_issues: list[str]
    false_positives: list[str]
    top_priorities: list[str]
    remediation_steps: list[str]
    exploit_difficulty: str


async def analyze_sarif(sarif_file: str, output_file: str):
    """分析 SARIF 文件"""
    
    # 读取报告
    with open(sarif_file) as f:
        sarif_data = json.load(f)
    
    # 提取关键信息
    results = sarif_data.get('runs', [{}])[0].get('results', [])
    
    # 准备分析内容
    analysis_prompt = f"""
分析这个 CodeQL 安全扫描结果：

扫描文件数：{len(results)}
漏洞列表：
{json.dumps(results[:20], indent=2)}  # 前 20 个

请提供：
1. 漏洞摘要和统计
2. 按严重程度分类
3. 最关键的 5 个漏洞
4. 可能的误报
5. 修复建议（按优先级排序）
6. 利用难度评估
"""
    
    # 使用 OpenClaw 分析
    async with OpenClawClient.connect() as client:
        agent = client.get_agent("security-analyst")
        
        analysis: VulnerabilityAnalysis = await agent.execute_structured(
            analysis_prompt,
            output_model=VulnerabilityAnalysis
        )
    
    # 保存分析结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# CodeQL 漏洞分析报告（LLM 增强版）\n\n")
        f.write(f"## 摘要\n\n{analysis.summary}\n\n")
        f.write(f"## 统计\n\n")
        f.write(f"- 总漏洞数：{analysis.total_vulnerabilities}\n")
        for severity, count in analysis.by_severity.items():
            f.write(f"- {severity}: {count}\n")
        f.write(f"\n## 关键问题\n\n")
        for i, issue in enumerate(analysis.critical_issues, 1):
            f.write(f"{i}. {issue}\n")
        f.write(f"\n## 修复建议\n\n")
        for i, step in enumerate(analysis.remediation_steps, 1):
            f.write(f"{i}. {step}\n")
    
    print(f"✅ 分析完成：{output_file}")


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='LLM 分析 CodeQL 结果')
    parser.add_argument('sarif_file', help='SARIF 文件路径')
    parser.add_argument('-o', '--output', default='llm-analysis.md', help='输出文件')
    
    args = parser.parse_args()
    
    await analyze_sarif(args.sarif_file, args.output)


if __name__ == '__main__':
    asyncio.run(main())
```

### 方案 3: Jenkins Pipeline 集成

**修改 Jenkinsfile**:

```groovy
stage('LLM 分析 / LLM Analysis') {
    steps {
        script {
            echo "🤖 使用 OpenClaw LLM 分析..."
            
            sh """
                cd ${SCANNER_DIR}
                export OPENCLAW_GATEWAY_WS_URL=ws://localhost:18789/gateway
                python3 analyze_with_llm.py \\
                    ${params.OUTPUT_DIR}/codeql-results.sarif \\
                    -o ${params.OUTPUT_DIR}/llm-analysis.md
            """
        }
    }
}

stage('发布 LLM 报告 / Publish LLM Report') {
    steps {
        publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: params.OUTPUT_DIR,
            reportFiles: 'llm-analysis.md',
            reportName: 'LLM Security Analysis'
        ])
    }
}
```

---

## 📋 实施步骤

### 步骤 1: 安装 OpenClaw SDK

```bash
cd /root/source/openclaw-sdk
pip install -e .
```

### 步骤 2: 创建分析脚本

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
cat > analyze_with_llm.py << 'EOF'
# （上面的代码）
EOF
chmod +x analyze_with_llm.py
```

### 步骤 3: 测试分析

```bash
python3 analyze_with_llm.py ./test-output/codeql-results.sarif -o llm-analysis.md
```

### 步骤 4: 集成到扫描流程

修改 `scanner.py` 添加可选的 LLM 分析：

```python
if config.get_bool('LLM_AUTO_ANALYZE', False):
    print("🤖 运行 LLM 分析...")
    asyncio.run(analyze_with_llm(sarif_file, report_file))
```

### 步骤 5: 更新 Jenkins Pipeline

添加 LLM 分析阶段（见上方）

---

## 🔧 配置项

### .env 添加

```ini
# LLM 分析配置
LLM_AUTO_ANALYZE=true
LLM_ANALYSIS_AGENT=security-analyst
OPENCLAW_GATEWAY_WS_URL=ws://localhost:18789/gateway
```

---

## 📊 输出示例

### LLM 分析报告

```markdown
# CodeQL 漏洞分析报告（LLM 增强版）

## 摘要

本次扫描发现 41 个安全问题，主要集中在信息泄露和注入漏洞。
建议优先修复 SQL 注入和代码注入问题。

## 统计

- 总漏洞数：41
- 严重：6
- 高危：10
- 中危：25

## 关键问题

1. SQL 注入 - vulnerable_app.py:44
   可利用性：高，建议立即修复

2. 代码注入 - vulnerable_app.py:138
   可导致远程代码执行

3. ...

## 修复建议

1. **立即修复** - SQL 注入（44 行）
   使用参数化查询替代字符串拼接

2. **高优先级** - 代码注入（138 行）
   移除 eval() 调用

3. ...

## 误报分析

以下问题可能是误报：
- 依赖包中的示例代码（非生产代码）
- 测试文件中的硬编码密码

## 利用难度

整体利用难度：中等

需要访问权限的漏洞：15
可远程利用的漏洞：8
```

---

## ✅ 验收清单

- [ ] OpenClaw SDK 已安装
- [ ] 分析脚本已创建
- [ ] 测试运行成功
- [ ] 集成到扫描流程
- [ ] Jenkins Pipeline 更新
- [ ] LLM 报告生成
- [ ] 配置项完整

---

## 🎯 下一步

1. **安装 OpenClaw SDK**
2. **创建分析脚本**
3. **测试运行**
4. **集成到现有流程**

需要我开始实施吗？
