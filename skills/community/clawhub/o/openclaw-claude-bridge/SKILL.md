---
name: claude-bridge
description: Use when user asks about  Bridge to local Claude Code CLI - no API key required
metadata:
  openclaw:
    emoji: "🤖"
---

# Claude Code Bridge

无需 API Key 的 Claude Code 本地集成方案。
通过本地 CLI 调用已安装的 Claude Code，使用现有订阅。

## 前提条件

1. Claude Code 已安装: `which claude`
2. 已登录 Claude Code: `claude --version`
3. 有有效的 Claude 订阅

## 使用方法

### 1. 生成代码

```python
from skills.claude-bridge.claude_bridge import generate_code

# 创建代码生成任务
result = generate_code(
    description="Create a function to calculate RSI indicator",
    language="python"
)

print(f"Task ID: {result['task_id']}")
print(f"Script: {result['script_file']}")
```

### 2. 执行代码生成

```python
from skills.claude-bridge.claude_bridge import execute_task_local

# 执行任务
output = execute_task_local(result['task_id'])
print(output['output'])
```

### 3. 代码审查

```python
from skills.claude-bridge.claude_bridge import review_code

# 创建代码审查任务
result = review_code(['file1.py', 'file2.py'])

# 执行审查
output = execute_task_local(result['task_id'])
print(output['output'])
```

### 4. 数据分析

```python
from skills.claude-bridge.claude_bridge import analyze_data

# 创建分析任务
result = analyze_data(
    data_description="Stock price data for AAPL from 2024-01 to 2024-12",
    analysis_type="trend_analysis"
)

# 执行分析
output = execute_task_local(result['task_id'])
print(output['output'])
```

## 命令行使用

```bash
# 创建任务
python3 skills/claude-bridge/claude_bridge.py create "Generate a Python script to download stock data"

# 执行任务
python3 skills/claude-bridge/claude_bridge.py execute <task_id>

# 查看状态
python3 skills/claude-bridge/claude_bridge.py status <task_id>

# 列出所有任务
python3 skills/claude-bridge/claude_bridge.py list
```

## 工作流程

### 手动执行模式

```
OpenClaw
    ↓ 创建任务文件
生成 shell 脚本
    ↓ 人工执行
用户运行: bash tasks/task_xxx.sh
    ↓ 读取结果
OpenClaw 获取输出
```

### 自动执行模式

```
OpenClaw
    ↓ 调用 execute_task_local()
本地执行 Claude Code
    ↓ 等待完成
读取结果文件
    ↓
返回结果
```

## 注意事项

1. **需要登录**: Claude Code 必须已登录
2. **订阅有效**: 需要有有效的 Claude 订阅
3. **超时设置**: 默认 5 分钟超时
4. **结果文件**: 结果保存在 skills/claude-bridge/results/

## 与 OpenClaw Agent 集成

```python
# 在 AGENTS.md 中添加

def claude_code_generate(description):
    """使用 Claude Code 生成代码"""
    from skills.claude-bridge.claude_bridge import generate_code, execute_task_local
    
    # 创建任务
    result = generate_code(description)
    
    # 执行任务
    output = execute_task_local(result['task_id'])
    
    return output['output']

def claude_code_review(files):
    """使用 Claude Code 审查代码"""
    from skills.claude-bridge.claude_bridge import review_code, execute_task_local
    
    result = review_code(files)
    output = execute_task_local(result['task_id'])
    
    return output['output']
```

## 优势

- ✅ 无需 API Key
- ✅ 使用现有订阅
- ✅ 本地执行，数据安全
- ✅ 可人工介入
- ✅ 与 OpenClaw 无缝集成

## 限制

- ⚠️ 需要本地安装 Claude Code
- ⚠️ 需要有效订阅
- ⚠️ 执行时间较长（需等待 Claude 响应）
- ⚠️ 不适合高频调用
