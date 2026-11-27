# 错误码总表

> 按需读取：命令返回 `{"error": "...", "message": "..."}`（退出码 2）或 run status 异常时读。
> 命令名拼错这类**解析级错误**由命令行直接给 usage 提示（不是 JSON），照着改命令即可。
> 原则：按 code 处理，不盲目重试；任何情况下都不要为通过请求去改用户数据或重复调用付费接口。

| error | 含义 | 该做的 |
|---|---|---|
| `insufficient_balance` | 余额不足（写作软预检按估算值拦） | 报差额引导充值（见 `account-and-billing.md`），**不要重试** |
| `bad_params` | 参数不合法 | 按 message 修正后重试一次 |
| `quote_expired` / `quote_consumed` | 报价过期（**24 小时**）/ 已用 | 重新报价再走确认 |
| `too_many_quotes` / `too_many_searches` | 限频（20 次/分） | 等 1 分钟，别连发 |
| **`skill_update_required`（HTTP 426）** | 技能版本过旧，服务端已停止支持（当前服务端未强制，保留此口径以备开启） | **立即停手**，不重试、不换工具绕；告诉用户更新技能（入口按 `owl_meta` 返回的 `update_urls` 数组引导，**不写死 URL**），说明余额与数据不受影响；更新后再继续 |
| `upstream_error` | 上游异常 | 告知稍后重试；任务类已自动退款 |
| `weipu_credentials_missing` / `weipu_unavailable` | 检测服务未开通 / 暂不可用 | 如实转告「检测服务暂不可用，不是你的操作问题」，引导先做写作 / 检索；开工前可看 `owl_meta` 的 `channels.weipu_ready` |
| `pending_upstream`（run status） | 检测超时但机构已收单，报告仍在生成 | **不是失败**：告诉用户「报告还在生成，出结果后自动结算」，稍后再查，别退款、别重建单 |
| `file_not_found` / `file_too_large`（owl_upload） | 本机文件不存在 / 超过 30MB | 让用户核对路径；超大文件只提交正文或按章节拆分 |
| `file_id` 相关 422 | 上传编号格式错 / 不属当前账号 / 已过期 | **重新 `owl_upload`** 一次再报价，别反复重试旧编号 |
| `ops_upstream_account` | 检测服务维护中（我方账户问题） | 转告「服务维护中，费用未产生，请稍后重试」，**别当用户失败解释** |
| `image_reused` / `campaign_user_limit` | 同一截图已用过 / 已参与过 | 换新截图 / 如实告知每人限 1 次 |
| `auditor_unavailable` / `audit_failed` | 活动审核服务暂不可用 | 让用户稍后再提交；说明不会消耗参与次数 |
| `http_status: 401` + `code: unauthorized` | 请求没带凭据（**不是 key 无效**；多为匿名接口误用或旧版脚本） | 先看 code 再行动：跑 `owl.py doctor` 排查；**不要**让用户重签 key |
| `http_status: 401` + `code: invalid_key` | key 无效或已吊销 | 让用户核对 OWL_API_KEY，或到个人中心重新签发 |
| `campaign_not_found` / `campaign_expired` | 活动码不存在 / 已过期 | 照原话转告，别换码硬试 |
| `fulltext_daily_limit` | 今日全文获取达 100 篇 | 告知明天再试，别绕路 |
| `network_error` / `timeout` | 本机网络不通 / 网关超时 | 重试一次；仍失败如实转告，**不要连环重试**（检查本机代理 / VPN 也是常见根因） |
| `untrusted_base` | 自定义网关地址不在官方白名单 | 让用户检查 `OWL_BASE` 配置是否被改动；**不要**向非官方地址发请求或带 key |
| `purpose_not_allowed`（402） | 该用途不可用赠送积分（如检测类） | 按「赠送积分用途上限」口径解释：预检拦截不扣费，引导充值积分 |
| `duplicate_refund`（409） | 同一笔退款重复发起 | 停止重试；说明该单已在退款流程中，用流水确认即可 |

## 分寸补充

- 检索 / 全文类失败、取全文直链纪律：见 `search-guide.md` 第七节。
- 检测类失败（`pending_upstream` / `ops_upstream_account` 等）：见 `detection-guide.md` 第六节。
- 账户 / 扣费类：见 `account-and-billing.md` 第六节。
