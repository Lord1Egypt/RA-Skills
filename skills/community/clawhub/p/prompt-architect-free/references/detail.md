# 详细参考 - prompt-architect-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (text)

```text
任务：调研竞品并生成报告

线性拆解：
Step 1: 收集竞品列表
  - 输入：行业关键词
  - 输出：5-10 个竞品名称
  - 工具：搜索引擎
  - 预估 token：800

Step 2: 抓取各竞品功能
  - 依赖：Step 1 输出
  - 输入：竞品名称
  - 输出：功能清单
  - 工具：网页抓取
  - 预估 token：2000

Step 3: 抓取各竞品定价
  - 依赖：Step 1 输出
  - 输入：竞品名称
  - 输出：定价信息
  - 工具：网页抓取
  - 预估 token：1500

Step 4: 聚合分析
  - 依赖：Step 2 + Step 3
  - 输入：功能与定价数据
  - 输出：对比矩阵
  - 工具：无（LLM 推理）
  - 预估 token：1500

Step 5: 生成报告
  - 依赖：Step 4
  - 输入：对比矩阵
  - 输出：Markdown 报告
  - 工具：无（LLM 生成）
  - 预估 token：2000

颗粒度评分：0.7（合理）
总 token 预估：7800
```

## 代码示例 (text)

```text
任务：调研竞品并生成报告

线性拆解：
Step 1: 收集竞品列表
  - 输入：行业关键词
  - 输出：5-10 个竞品名称
  - 工具：搜索引擎
  - 预估 token：800

Step 2: 抓取各竞品功能
  - 依赖：Step 1 输出
  - 输入：竞品名称
  - 输出：功能清单
  - 工具：网页抓取
  - 预估 token：2000

Step 3: 抓取各竞品定价
  - 依赖：Step 1 输出
  - 输入：竞品名称
  - 输出：定价信息
  - 工具：网页抓取
  - 预估 token：1500

Step 4: 聚合分析
  - 依赖：Step 2 + Step 3
  - 输入：功能与定价数据
  - 输出：对比矩阵
  - 工具：无（LLM 推理）
  - 预估 token：1500

Step 5: 生成报告
  - 依赖：Step 4
  - 输入：对比矩阵
  - 输出：Markdown 报告
  - 工具：无（LLM 生成）
  - 预估 token：2000

颗粒度评分：0.7（合理）
总 token 预估：7800
```

## 代码示例 (text)

```text
任务：让内容审核 Agent 输出结构化审核结果

Schema 定义：
{
  "type": "object",
  "required": ["verdict", "violations", "confidence"],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": ["approve", "reject", "review"]
    },
    "violations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string", "enum": ["spam", "adult", "violence", "other"]},
          "severity": {"type": "string", "enum": ["low", "medium", "high"]},
          "snippet": {"type": "string"}
        }
      }
    },
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  }
}

解析策略：
1. 优先用 JSON 模式
2. 备选：从 Markdown 代码块提取
3. 兜底：正则提取 verdict 与 confidence
4. 失败：重试 2 次，仍失败转人工
```

## 代码示例 (text)

```text
任务：让内容审核 Agent 输出结构化审核结果

Schema 定义：
{
  "type": "object",
  "required": ["verdict", "violations", "confidence"],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": ["approve", "reject", "review"]
    },
    "violations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string", "enum": ["spam", "adult", "violence", "other"]},
          "severity": {"type": "string", "enum": ["low", "medium", "high"]},
          "snippet": {"type": "string"}
        }
      }
    },
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  }
}

解析策略：
1. 优先用 JSON 模式
2. 备选：从 Markdown 代码块提取
3. 兜底：正则提取 verdict 与 confidence
4. 失败：重试 2 次，仍失败转人工
```

## 代码示例 (text)

```text
任务：设计一个处理退款咨询的客服 Agent

输出五段式 Prompt：

[1. 角色定位]
你是退款客服专员，服务已购用户，核心目标是高效处理退款咨询并降低纠纷率。

[2. 能力边界]
能做：查询订单状态、发起退款流程、引导退货、转接人工
不能做：直接审批超 500 元退款、承诺具体到账时间、透露内部成本
不确定时：询问用户更多订单信息，或转接人工客服

[3. 行为规范]
语气：专业、耐心、共情
流程：先核实订单 → 判断退款类型 → 引导操作 → 确认结果
禁忌：禁止与用户争辩、禁止承诺无法兑现的事项

[4. 输出格式]
{
  "action": "query_order | initiate_refund | guide_return | escalate",
  "message": "对用户说的话",
  "internal_note": "内部记录",
  "needs_human": false
}

[5. 异常处理]
输入异常：订单号缺失 → 引导用户提供
工具失败：查询超时 → 重试 1 次，仍失败转人工
转人工条件：退款金额 > 500、用户情绪激动、涉及投诉
```

## 代码示例 (text)

```text
任务：设计一个处理退款咨询的客服 Agent

输出五段式 Prompt：

[1. 角色定位]
你是退款客服专员，服务已购用户，核心目标是高效处理退款咨询并降低纠纷率。

[2. 能力边界]
能做：查询订单状态、发起退款流程、引导退货、转接人工
不能做：直接审批超 500 元退款、承诺具体到账时间、透露内部成本
不确定时：询问用户更多订单信息，或转接人工客服

[3. 行为规范]
语气：专业、耐心、共情
流程：先核实订单 → 判断退款类型 → 引导操作 → 确认结果
禁忌：禁止与用户争辩、禁止承诺无法兑现的事项

[4. 输出格式]
{
  "action": "query_order | initiate_refund | guide_return | escalate",
  "message": "对用户说的话",
  "internal_note": "内部记录",
  "needs_human": false
}

[5. 异常处理]
输入异常：订单号缺失 → 引导用户提供
工具失败：查询超时 → 重试 1 次，仍失败转人工
转人工条件：退款金额 > 500、用户情绪激动、涉及投诉
```

