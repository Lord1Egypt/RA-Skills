# Multi-Agent Review — 多代理并行审查系统

> 借鉴 Claude Code pr-review-toolkit，同时 spawn 6 个专业代理并行审查代码，汇总为统一报告。

## 审查代理

| 代理 | 职责 | 关注点 |
|------|------|--------|
| architecture-critic | 架构批评家 | 模块划分、依赖关系、扩展性 |
| security-auditor | 安全审计员 | 漏洞、敏感信息、权限风险 |
| test-engineer | 测试工程师 | 覆盖率、边界条件、测试质量 |
| performance-analyst | 性能分析师 | 时间/空间复杂度、资源泄漏 |
| maintainability-reviewer | 可维护性审查员 | 代码清晰度、文档、命名 |
| documentation-checker | 文档检查员 | API 文档、注释完整性 |

## 并行审查流程

```
用户提交代码审查请求
  │
  ├─ 1. 解析目标代码（文件范围、语言、框架）
  │
  ├─ 2. 并行 spawn 6 个子代理
  │     ├→ architecture-critic
  │     ├→ security-auditor
  │     ├→ test-engineer
  │     ├→ performance-analyst
  │     ├→ maintainability-reviewer
  │     └→ documentation-checker
  │
  ├─ 3. 收集各代理结构化结果（JSON）
  │
  ├─ 4. 置信度过滤（≥80 分的发现才纳入报告）
  │
  ├─ 5. 冲突解决（多代理意见不一致时）
  │
  └─ 6. 生成汇总报告
```

## 编排逻辑

### Step 1：解析输入

从用户请求中提取：
- 目标文件/目录
- 审查范围（全量/增量）
- 特殊关注点（如有）

### Step 2：并行 spawn

```
对每个代理：
  sessions_spawn(
    model: "sonnet",
    system_prompt: <从 agents/*.yaml 读取>,
    task: "审查以下代码：[文件内容]\n\n重点关注：[代理职责]",
    tools: ["Read", "Grep", "Glob"]
  )
```

所有 spawn 同时发起，不等待前一个完成。

### Step 3：收集结果

每个代理返回 JSON 格式结果：

```json
{
  "agent": "architecture-critic",
  "findings": [
    {
      "severity": "high",
      "title": "模块耦合度过高",
      "location": "src/service.py:45",
      "description": "Service 类直接依赖 Database 实现",
      "suggestion": "引入 Repository 接口解耦",
      "confidence": 85
    }
  ],
  "score": 6,
  "summary": "架构存在耦合问题，建议重构"
}
```

### Step 4：置信度过滤

- 置信度 ≥ 80：纳入最终报告
- 置信度 60-79：标记为"待确认"
- 置信度 < 60：丢弃

### Step 5：冲突解决

当多个代理对同一位置有矛盾意见时：

1. **严重性优先**：取严重性更高的意见
2. **置信度加权**：置信度高的代理意见权重更大
3. **标注分歧**：在报告中同时展示不同观点
4. **人工裁决**：标记需要人工决策的冲突项

### Step 6：汇总报告

```markdown
# 多代理代码审查报告

## 概要
- 审查文件：X 个
- 参与代理：6 个
- 发现总数：X（Critical: X, High: X, Medium: X, Low: X）
- 整体评分：X/10

## 各维度评分
| 维度 | 评分 | 代理 |
|------|------|------|
| 架构 | X/10 | architecture-critic |
| 安全 | X/10 | security-auditor |
| 测试 | X/10 | test-engineer |
| 性能 | X/10 | performance-analyst |
| 可维护性 | X/10 | maintainability-reviewer |
| 文档 | X/10 | documentation-checker |

## 关键发现（按严重性排序）
[合并所有代理的发现，去重排序]

## 冲突项（需人工裁决）
[多代理意见不一致的发现]

## 建议行动
[按优先级排序的修复建议]
```

## 使用方法

### 全量审查

```
请审查 src/ 目录下的所有代码
```

### 指定代理

```
只做安全审查和性能分析
```

### 增量审查

```
审查最近 3 次 commit 的变更
```

## 文件结构

```
multi-agent-review/
├── SKILL.md                          # 本文件
├── agents/
│   ├── architecture-critic.yaml      # 架构批评家
│   ├── security-auditor.yaml         # 安全审计员
│   ├── test-engineer.yaml            # 测试工程师
│   ├── performance-analyst.yaml      # 性能分析师
│   ├── maintainability-reviewer.yaml # 可维护性审查员
│   └── documentation-checker.yaml    # 文档检查员
└── references/
    └── review-workflow.md            # 审查工作流详细文档
```
