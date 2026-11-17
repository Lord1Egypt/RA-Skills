# zengzhi.life Agent API 参考（技能随附，写死的部分是稳定契约；动态部分一律以 meta 为准）

> 口径对齐：2026-10-02，对应线上 meta v2.0（auth v2：密码登录 + Bearer API Key，scope 分级/设备授权/一次性确认码已退役）。

Base：`https://zengzhi.life/api/v1`　认证：请求头 `Authorization: Bearer <API Key>`
引导词与权限的唯一事实源：`GET /agent/meta`（免认证）。行为规范全文：`GET /agent/code-of-conduct`（免认证）。密钥自检与配额快照：`GET /agent/ping`。

## 密钥的取得与轮换（auth v2；1 user = 1 key，key 即持有人本人身份）

1. **首次取得**：主人注册 `POST /api/v1/auth/register`（邮箱+密码+展示名，Agent 可代办）→ 注册邮件下发**激活码 + API Key 明文（仅此一次）** → 主人在页面输激活码完成邮箱验证、把 key 转交 Agent
2. **丢失/轮换**：主人登录后在 https://zengzhi.life/agent-authorize.html 轮换，新明文发主人邮箱；旧 key 立即失效
3. **动作留痕**：`GET /agent/actions` 可逐条查看 Agent 做过什么（与主人页流水互相印证）；吊销＝轮换 key
4. 配额按 **Bearer key（机器身份）** 计数，主人本人会话登录不受这层限制

申请"上架类"权限不存在——上架、挂牌、签委托书等只认本人，不设 scope。

## 端点速查（模式 B 用到的）

| 步骤 | 端点 | 要点 |
|---|---|---|
| 对齐 | `GET /agent/meta` | 引导词 workflow_seller/buyer、决策四档、配额、human_only 清单、publish_prerequisites |
| 自检 | `GET /agent/ping` | 拿到 key 先调一次确认可用；`quotas.{key}.limit/used/remaining` 是配额快照 |
| 建单 | `POST /report/orders` | body：`cats`(1–3)、`ownership{q1,q2,q3,note}`（三句必须如实全 true 才能递交；Agent 代填会永久留痕 `via=agent`。展示页公开**不再要求本人先保存**——2026-09-13 已取消该门，但主人没保存过时，对外承诺记的就是你填的那份，交付时应如实提醒一句）、`mode:"free"`、`auto_generate` |
| step0 | `GET /report/orders/{id}/step0` → `POST .../step0/answers` | 建单后平台可能追问 step0 问题（先 `POST .../step0/ask` 取题）；是否必答以 meta `workflow_seller` 与单据状态为准 |
| 素材 | `POST /report/orders/{id}/materials` | **multipart/form-data，字段名 `files`**，可多件；文本 .txt/.md，图片 jpg/png/webp/gif ≤5MB；空 body/错字段名/JSON 提交一律 422（会回显你实际发来的 content_type 与字段名） |
| 软删 | `POST .../materials/{mid}/void` | body `{"void": true}`；误传可 `{"void": false}` 恢复；全作废后 generate 会被 422 拦 |
| 生成 | `POST /report/orders/{id}/generate` | 需 ≥1 件有效素材；后台异步 |
| 轮询 | `GET /report/orders/{id}` | status：submitted → processing → generated / needs_reinforcement / failed；响应含 `report`（grounding 通过率、attest_no 存证号）、`page`、`advice`（平台建议）、`advice_history` |
| 改稿 | `PUT /report/reports/{report_id}/draft` | 服务端必重算 grounding——改稿后证据分会如实下降 |
| 展示页 | `GET /report/pages/{id}`；`PUT /report/pages/{id}/title`（≤60）；`PUT .../brief`（≤300）；`PUT .../valuation`（0–1e8） | brief 三要素：金额（或"未标价/面议"）+ 主体性质（个人/工作室/公司…）+ 可点开出处（网址或 RP/ZC 编号）；`valuation` 是持有人自报价，非平台鉴定 |
| 公开读 | `GET /directory`、`GET /pages/{id}/public` | 游客可读；只出笔名，缺依据句在公开页替换为占位 |

## 建议与复核（2026-09-28/29 口径）

- 建议的产出节点＝**报告生成完**：`GET /report/orders/{id}` 的 `report.advice` 是"平台建议与风险提示"，**只引导、不阻拦、不审核**——合格与否由持有人本人判断。
- `report.advice_history` 是历次快照；点公开展示时会与当前内容复核，已提示且仍未处理的标注原日期（「（YYYY-MM-DD 报告生成时已提示，仍未处理）」），处理掉的不再出现。
- 权属三句可由本人就地改：`POST /report/orders/{id}/ownership/confirm`（body 可带 `q1/q2/q3/note`；只认本人，Agent 调 403）——"能改即确认"。

## 配额与限流（按 Bearer key 计数，北京 0 点恢复）

| 前缀 | 上限/日 |
|---|---|
| `GET /api/v1/*`（read） | 300 |
| 建单/素材/生成等（draft） | 60 |
| generate | 5 |
| rerun | 3 |
| 意向（intent） | 10 |
| 申报（declare） | 5 |

- 只对 **Bearer key（机器身份）** 计数；主人本人会话登录不受这层限制
- **调用即计数**——被 404/409/422 等前置门拦下的调用也算（否则一次失败可无限重试）
- 配额快照：`GET /agent/ping → quotas.{key}.limit/used/remaining`（三字段，Agent 不必撞 429 才知道限额）
- 429 带 `Retry-After` 与 `detail.quota`；数值以 meta `quotas.limits` 为准

## 错误语义（每个错误都自带下一步）

- `401` 未认证：key 无效/已被主人轮换/尚未领取——向主人要新 key（注册邮件或轮换邮件里，明文仅一次），不要硬试
- `403` 触碰"只认本人"动作（或操作他人资源）：按 `detail`/`next_action` 的中文说明把入口递给主人本人——**不要换写法绕过**
- `422` 入参问题：`detail` 为数组时逐条给字段级中文说明（如 `cats：请提供 1-3 个`）；multipart 上传错误回显 `received.content_type`、`other_form_keys`、`allowed_ext`
- `429` 配额：`quota.remaining=0`，北京 0 点恢复
- `404` 资源不存在或不属于你

## "只认本人"端点清单（Agent 调用一律 403，不要代点）

`POST /report/pages/{id}/publish`（公开展示/上架）· `POST /api/v1/listings`（挂牌）· `POST /api/v1/listings/{id}/off`（下线）· `POST /api/v1/listings/{id}/intent`（提交购买意向——含"用途合规"承诺，须主人本人勾）· `POST|DELETE /api/v1/deeds/sell`（卖方委托书）· `POST|DELETE /api/v1/deeds/buy`（买方寻购委托书）· `POST /deals/{id}/confirm`（确认对方成交）· `POST /report/orders/{id}/ownership/confirm`（保存权属三句）· `DELETE /report/orders/{id}`（删单）· `DELETE /report/pages/{id}/comments/{comment_id}`（隐藏评论）

完整清单以 `GET /agent/meta → human_only_endpoints` 为准。

## 建展示页后的固定话术（原样复述给用户）

「已建立数字资产，请主人修正内容，是否公开展示和上架销售，请主人亲自操作。」
并附：页面 id／标题／简介／自报价／证据分／还缺哪几项（来自 `advice`）。
