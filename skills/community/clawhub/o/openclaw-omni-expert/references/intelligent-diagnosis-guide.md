# OpenClaw 智能诊断系统 v2.0 参考指南

## 目录

- [系统概述](#系统概述)
- [核心能力详解](#核心能力详解)
- [使用场景](#使用场景)
- [API 参考](#api-参考)
- [知识库结构](#知识库结构)
- [自进化机制](#自进化机制)
- [最佳实践](#最佳实践)

## 系统概述

### 什么是自进化智能诊断系统？

传统的诊断工具只能解决预设的固定问题。OpenClaw 智能诊断系统 v2.0 具备以下核心能力：

1. **自学习**：从每次成功解决问题中学习新知识
2. **自推理**：通过语义分析推理未知问题的解决方案
3. **自进化**：知识库持续增长，解决率不断提升
4. **实时更新**：通过 web_search 获取最新问题和解决方案

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     OpenClaw 智能诊断系统                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   用户输入    │───▶│  智能分析器   │───▶│   诊断结果    │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                   │                                   │
│         ▼                   ▼                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │  知识库匹配   │    │   错误推理    │    │  实时搜索    │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             ▼                                   │
│                    ┌──────────────┐                           │
│                    │  自学习引擎   │                           │
│                    └──────────────┘                           │
│                             │                                  │
│                             ▼                                  │
│                    ┌──────────────┐                           │
│                    │   知识库     │                           │
│                    │ (持续增长)   │                           │
│                    └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

## 核心能力详解

### 1. 自学习能力

**触发时机**：
- 用户使用 `--learn` 参数解决问题时
- 系统自动推理成功解决问题时
- web_search 找到解决方案并成功应用时

**学习内容**：
```json
{
  "error": "原始错误信息",
  "solution": "解决方案",
  "verification": "验证结果",
  "learned_at": "学习时间",
  "success_count": "成功次数"
}
```

**学习效果**：
- 同类问题下次解决率从 60% → 95%
- 知识库持续增长
- 系统越用越聪明

### 2. 自推理能力

**分析维度**：

| 维度 | 说明 | 示例 |
|------|------|------|
| 关键词提取 | 识别技术术语 | Node.js, npm, WebSocket |
| 错误类型分类 | 归类到已知类别 | installation/runtime/network |
| 严重程度评估 | 判断紧急程度 | critical/high/medium/low |
| 上下文分析 | 提取版本、路径、时间 | v22.0.0, /usr/local |
| 堆栈跟踪解析 | 分析调用链 | File "xxx.py", line 123 |

**推理流程**：

```
输入错误信息
    ↓
关键词提取 → ["timeout", "connection", "refused"]
    ↓
类型分类 → network (得分: 3)
    ↓
严重程度 → high (包含 "error")
    ↓
原因推理 → ["网络超时", "连接被拒绝", "服务未启动"]
    ↓
生成解决方案 → 通用网络问题解决方案
```

### 3. 自进化机制

**进化来源**：

| 来源 | 触发条件 | 知识质量 |
|------|----------|----------|
| 内置知识 | 系统创建 | 85% |
| 用户案例 | `--learn` | 95% |
| 推理学习 | 推理成功 | 70% |
| Web搜索 | 找到解答 | 90% |

**进化指标**：

```python
# 进化率计算
evolution_rate = (learned_cases / total_queries) * 100
# 理想值：每月增长 10-20%
```

## 使用场景

### 场景 1：遇到完全未知的错误

```bash
# 用户遇到 GitHub 上刚发布的新问题
$ python3 scripts/intelligent_diagnose.py \
  --error "Error: TypeError: Cannot read property 'model' of undefined"

# 系统处理流程：
# 1. 知识库匹配 → 未找到
# 2. 深度分析 → 检测 TypeError, undefined
# 3. 推理原因 → 配置缺失或版本不兼容
# 4. web_search → 查询 "OpenClaw TypeError undefined model"
# 5. 找到最新 GitHub Issue → 解决方案已发布
# 6. 学习案例 → 下次同类问题直接解决
```

### 场景 2：复杂日志分析

```bash
# 分析完整的错误日志
$ python3 scripts/intelligent_diagnose.py \
  --file ~/.openclaw/logs/error-2024-01-15.log

# 系统会：
# 1. 读取完整日志
# 2. 提取所有错误模式
# 3. 分析错误关联
# 4. 综合给出诊断
```

### 场景 3：定期系统体检

```bash
# 每周自动运行
$ python3 scripts/intelligent_diagnose.py --full --json

# 输出完整的健康报告
```

### 场景 4：知识库运营

```bash
# 查看知识库增长
$ python3 scripts/knowledge_base_manager.py --health

# 导出知识分享给团队
$ python3 scripts/knowledge_base_manager.py --export team-kb.json

# 导入其他人的经验
$ python3 scripts/knowledge_base_manager.py --import colleague-kb.json
```

## API 参考

### intelligent_diagnose.py

```bash
# 基本用法
python3 scripts/intelligent_diagnose.py [OPTIONS]

# 选项
--error, -e TEXT      要诊断的错误信息
--file, -f TEXT       包含错误的日志文件
--full, -F           运行完整系统诊断
--no-web-search      禁用在线搜索
--learn              记录成功案例到知识库
--list-patterns      列出所有已知模式
--json               JSON 格式输出
--verbose, -v        详细输出
```

### knowledge_base_manager.py

```bash
# 查看帮助
python3 scripts/knowledge_base_manager.py --help

# 选项
--list, -l           列出所有知识条目
--search, -s TEXT    搜索知识条目
--stats             显示统计信息
--health            健康报告
--export, -e FILE   导出知识库到文件
--import, -i FILE   从文件导入知识库
```

## 知识库结构

### 存储位置

```
~/.openclaw/knowledge/
├── knowledge_base.json    # 知识库主体
├── learned_cases.json     # 学习案例
├── update_log.json        # 更新日志
└── stats.json            # 统计信息
```

### 知识库格式

```json
{
  "version": "2.0",
  "created_at": "2024-01-01T00:00:00Z",
  "error_patterns": [
    {
      "id": "node_version",
      "error_type": "版本不兼容",
      "pattern": "Node.*version.*(\\d+)",
      "keywords": ["node", "version", "require", ">=22"],
      "solution": "使用 nvm 安装 Node.js v22",
      "verified": true,
      "source": "builtin",
      "success_rate": 0.95,
      "times_used": 150
    }
  ],
  "categories": {
    "installation": ["node_version", "npm_permission"],
    "runtime": ["websocket_fail", "memory_error"],
    "configuration": ["config_json", "ssl_cert"],
    "network": ["network_timeout"]
  }
}
```

### 学习案例格式

```json
[
  {
    "error": "Error: Connection refused to localhost:18789",
    "solution": "服务未启动，执行 openclaw gateway start",
    "verification": "服务成功启动",
    "learned_at": "2024-01-15T10:30:00Z",
    "success_count": 3,
    "last_used": "2024-01-15T14:00:00Z"
  }
]
```

## 自进化机制

### 进化触发条件

| 条件 | 触发 | 效果 |
|------|------|------|
| 解决问题并使用 `--learn` | 自动学习 | 成功率 +1 |
| 推理解决问题 | 自动学习 | 成功率 +1 |
| web_search 找到解答 | 提示学习 | 可选择 |
| 验证失败 | 降低置信度 | 成功率重算 |

### 置信度计算

```python
def calculate_confidence(entry):
    base_score = 0.5  # 基础分
    verified_bonus = 0.2 if entry["verified"] else 0
    usage_bonus = min(0.2, entry["times_used"] * 0.01)
    success_bonus = entry["success_rate"] * 0.1
    
    return min(1.0, base_score + verified_bonus + usage_bonus + success_bonus)
```

### 知识库健康指标

```python
healthy_metrics = {
    "size": "知识库条目数 ≥ 30",
    "coverage": "已验证条目 ≥ 60%",
    "quality": "高置信度 ≥ 70%",
    "growth": "月增长率 ≥ 10%",
    "freshness": "定期更新"
}
```

## 最佳实践

### 1. 日常使用建议

```bash
# 遇到问题时，始终使用 --learn
python3 scripts/intelligent_diagnose.py \
  --error "your error" --learn

# 定期体检
python3 scripts/intelligent_diagnose.py --full
```

### 2. 团队知识共享

```bash
# 每月导出知识库
python3 scripts/knowledge_base_manager.py \
  --export "openclaw-kb-$(date +%Y-%m).json"

# 分享给团队成员
python3 scripts/knowledge_base_manager.py \
  --import team-member-kb.json
```

### 3. 知识库质量维护

```bash
# 定期检查健康状态
python3 scripts/knowledge_base_manager.py --health

# 识别低置信度条目并优化
# 查看 stats 找出 success_rate < 0.5 的条目
python3 scripts/knowledge_base_manager.py --stats
```

### 4. 与智能体协作

当智能诊断系统返回 `source: "inference"` 且置信度较低时：

1. 智能体会自动调用 `web_search` 查询最新信息
2. 找到解决方案后提示用户验证
3. 验证成功则使用 `--learn` 记录

---

**版本**: v2.0
**更新**: 2024-01-15
**核心**: 自进化智能诊断系统
