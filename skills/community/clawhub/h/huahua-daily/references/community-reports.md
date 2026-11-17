# 社区、JCTI 与个人报告

## 社区

- 排行榜、个人排名、用户详情、关注列表和搜索均使用对应 MCP 工具。
- 授权、撤销授权和关注会改变状态；只在用户明确要求后执行。
- `follow_community_user` 是非幂等切换操作，失败或结果不明时不要自动重试。
- 社区收益使用后端统一 G 日口径；不自行平移 QDII 日期。

## JCTI

只有用户明确要求人格分析并提供必要答案时调用 `analyze_jcti`。结果是辅助解释，不是风险承受能力或投资适当性的替代品。

## 个人报告

- 用户明确要求生成并保存报告时才调用 `submit_personal_strategy_report`。
- 报告只能投递到当前 Agent Token 所属用户，不能指定其他用户或广播。
- 同一报告重试复用 `client_message_id`；同一 ID 不得携带不同内容。
- 普通大小报告走 MCP；已经存在的大型 JSON 报告文件走 `huahua report submit --file ...`。
- 不调用 `/api/hermes/reports`，该接口不属于公开用户 Agent。
