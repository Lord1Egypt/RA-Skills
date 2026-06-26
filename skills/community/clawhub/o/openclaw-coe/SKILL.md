---
name: openclaw-coe
description: OpenClaw 原生执行链（Chain of Execution, CoE）技能。让 OpenClaw 在处理复杂任务时，实时分步输出执行过程：拆解问题 → 选择 skill → 调用 skill → 调用模型 → 等待响应 → 拿到结果 → 最终汇总，完全贴合 OpenClaw 实际运行流程，让用户清楚看到每一步在做什么。
version: 1.0.0
author: 刘跃华 / OpenClaw community
triggers:
  - "执行链"
  - "分步执行"
  - "chain-of-execution"
  - "coe"
  - "一步一步"
  - "过程"
metadata: {"openclaw":{"emoji":"🔗","requires":{"bins":[],"env":[]}}}
---

# OpenClaw CoE (Chain of Execution)

OpenClaw 原生执行链追踪技能。让 OpenClaw 在处理复杂任务时，**实时分步输出执行过程**，完全贴合 OpenClaw 实际运行流程——"大模型提议 → 安全审批 → 龙虾执行"，每一步都同步给用户。

## 工作原理

这不是给大模型加 prompt 的"思维链"，而是 **OpenClaw 系统层面** 的执行过程同步：

1. **拆解问题**：收到复杂任务，先拆解成子任务，告诉用户
2. **选择 skill**：说明选哪个 skill / 哪个模型，为什么这么选
3. **调用 skill**：报告正在调用哪个 skill
4. **调用模型**：说明用哪个模型，大概做什么
5. **等待响应**：如果在等外部 API / 网页抓取，提前告诉用户"正在等响应，不会卡住"
6. **拿到结果**：报告 skill / 模型返回了什么
7. **思考推理**：给出推理过程，排除错误选项
8. **警告/错误**：出问题提前说，不会闷着卡住
9. **最终完成**：整合所有步骤，给出最终答案

## 使用方式

### 自动触发

当用户提问包含"分步"、"一步一步"、"执行过程"等关键词，自动启用 CoE。

### 手动启用

在会话中说"启用 openclaw-coe"，后续任务都会走执行链流程。说"关闭 openclaw-coe"关闭。

### API 调用

其他 skill 可以导入这个模块，手动触发分步输出：

```python
from skills.openclaw-coe.cot_tracker import CoETracker

tracker = CoETracker()
tracker.start("任务标题")
tracker.step("拆解问题", "把问题拆成三个子步骤...")
tracker.step("选择skill", "使用 wechat-article 提取文章...")
tracker.wait() # 等待外部响应
tracker.result("提取成功，获得 X 字符原文")
tracker.done("最终结论：...")
```

## 设计原则

- **低资源消耗**：只是输出过程文本，不额外调用大模型，token 消耗几乎为零
- **不改变原有逻辑**：只是在原有执行流程上加一层输出，不影响任何现有 skill 和模型
- **完全兼容**：所有现有 skill 都可以配合 CoE 使用，其他 skill 可以直接导入
- **贴合实际**：完全对齐 OpenClaw "大模型提议 → 安全审批 → 龙虾执行" 架构，每一步都对得上
- **提前预警**：遇到等待外部响应或者可能卡住的情况，提前告诉用户，不会闷着
- **简洁输出**：不说废话，每一步几句话讲清楚

## 配置

不需要环境变量或 API key，纯原生 skill。
