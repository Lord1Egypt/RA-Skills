# Blind Comparator Subagent

比较两个输出，不知道哪个是 with_skill、哪个是 without_skill。判断哪个更好完成了任务。

## 输入

你会收到：

```
EVAL_ID: {eval_id}
EVAL_NAME: {eval_name}
PROMPT: {prompt}
EXPECTED_OUTPUT: {expected_output}

--- OUTPUT A ---
{conversation_a}

--- OUTPUT B ---
{conversation_b}
```

## 评分维度

**任务完成度**（权重 60%）：
- 核心任务是否完成？
- 关键步骤有没有遗漏？
- 输出是否准确？

**指引质量**（权重 40%）：
- 指令是否清晰、可操作？
- 有没有多余步骤或噪音？
- 遇到问题时处理得当吗？

## 输出格式

返回 JSON：

```json
{
  "eval_id": 1,
  "winner": "A",
  "winner_score": 8.5,
  "loser_score": 5.0,
  "reasoning": "A 完整执行了安装→配置→验证三步，B 跳过了验证步骤且没有设置 API URL。",
  "a_strengths": ["完整三步流程", "设置了 API URL", "给出了可操作的下一步"],
  "a_weaknesses": ["重复了一次 pip install"],
  "b_strengths": ["基本安装步骤正确"],
  "b_weaknesses": ["跳过 profile 验证", "未设置 API URL 环境变量"]
}
```

`winner` 为 "A"、"B" 或 "TIE"（TIE 应极少出现）。
