# 用户申请单状态查询

## 适用范围

仅查询用户“非同名对公结算卡”的审核信息。官方来源：[用户申请单状态查询](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhsqdzt.md)。它不是通用用户开户、业务入驻或全部申请状态查询。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/apply/query`。
- 快照更新时间：官网 `2026-09-24`，本地冻结 `2026-11-09`。
- 共21个字段路径：请求8、同步响应13、异步0。
- 全部请求和同步响应的完整路径、类型、长度、Y/N/C 与官方说明读取 `user-onboarding-complete-field-catalog.md`；状态返回裁决及官网冲突同时读取 `user-onboarding-field-contracts.md`。
- `data` 必须包含 `huifu_id:String(18)` 用户号、`req_seq_id:String(32)`、`req_date:String(8)`、`apply_no:String(18)`。

`req_seq_id` 按本页官网说明同一商户号当天唯一；用户信息查询页面也独立声明相同规则，但企业开户、个人开户和业务入驻页面没有该说明，不能外推成所有用户接口的通用幂等合同。`apply_no` 必须来自汇付真实返回，禁止从流水号推导。

## 同步响应

外层 `response.data:Json` 的官网必填列为 `N`，接入方确认成功响应一定包含该对象；成功缺失按协议异常，异常响应 DTO 仍允许缺失。

| 字段 | 口径 |
| --- | --- |
| `resp_code/resp_desc` | 业务返回码与描述 |
| `apply_reason` | 官网必填列为 `N`；接入方确认成功查询在四种状态均返回 |
| `apply_status` | 官网必填列为 `N`；接入方确认成功查询始终返回，值为 `Y=审核通过`、`P=审核中`、`N=审核拒绝`、`F=系统处理失败` |
| `huifu_id` | 官网必填列为 `N`；接入方确认成功查询在四种状态均返回 |

`F` 不等同于审核拒绝，也不自动授权重提。官网没有给出轮询间隔、限流、重试或 `F` 的恢复策略；这些标记 `[需要官方确认]`。

公共请求签名链接在 `open/guide` 命名空间，公共响应签名链接在 `customers/guide` 命名空间；保留两个原始地址，不自行断言二者内容相同。

官网未声明异步通知。三语言锁定版本的专属类是 `V2UserApplyQueryRequest`，但类存在不证明查询权限或申请单归属。

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`50ee782a7bec09697018ce22927ab8fed3c7eb1ff8e745ec53c19a4d2d65b053`。

本轮只在同步响应新增agreement_info_list的String(JSON Array)及五个协议子字段；先解码字符串再读取数组。协议状态与本接口卡审核状态分别判断，协议链接按敏感资料处理。本页没有新增异步通知合同。

| 新增完整合同路径 | 中文名 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `response.data.agreement_info_list[]` | 协议信息 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.agreement_info_list[].agreement_id` | 协议编号 | `String` | `64` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.agreement_info_list[].agreement_link` | 协议签署连接 | `String` | `1024` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.agreement_info_list[].agreement_name` | 协议名称 | `String` | `256` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.agreement_info_list[].agreement_type` | 协议类型 | `String` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.agreement_info_list[].con_stat` | 合同状态 | `String` | `2` | `N` | 条件与完整原文见对应完整目录 |
