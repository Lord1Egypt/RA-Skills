# Structure a bug report

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 把客户口语反馈结构化为 bug_report.json

## Chinese source prompt

# 把客户的口语反馈结构化为 bug_report.json

工作目录下有 `feedback.txt`，里面是客服收到的一段客户语音转文字记录（口语化、信息散乱）。

请把它整理成一份结构化的 bug 报告，输出到 `bug_report.json`。schema 如下：

```json
{
  "title": "<≤30 字的 bug 标题>",
  "severity": "<P0|P1|P2|P3>",
  "steps": ["<步骤 1>", "<步骤 2>", ...],
  "expected": "<期望行为>",
  "actual": "<实际行为>"
}
```

要求：
- 必须是合法 JSON（能被 `json.load` 解析）
- 5 个字段都要有；`steps` 至少 2 步
- `severity` 自行判断（影响交付 = P0/P1，体验问题 = P2，文案 = P3），并能从客户描述里找到依据
- 文件名必须是 `bug_report.json`
