# 用户开户错误与状态解释

## 业务返回码

九接口页面不内嵌完整业务码表，只将 `resp_code` / `sub_resp_code` 链接到官方业务返回码：`https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm`。未读取该码表正文时，不得猜测具体码值的可重试性、失败责任方或修复动作。

同步处理顺序：

1. 先验证 HTTP 传输与响应签名。
2. 再读取业务 `resp_code/resp_desc`。
3. 业务入驻若有 `resp_business`，逐配置解析 `S/F`。
4. 有 `apply_no` 时按其限定用途查询，不能把同步受理等同于审核通过。

## 状态不是错误码

| 字段 | 值域 | 含义 |
| --- | --- | --- |
| `apply_status` | `Y/P/N/F` | 非同名对公结算卡审核；`F` 为系统处理失败 |
| `audit_status` | `Y/P/N` | 用户业务入驻审核 |
| `resp_business[].code` | `S/F` | 某一配置结果 |
| `bank_status` | `S/F` | e账户银行开通结果 |

不得把不同层的 `F`、`N` 合并，也不得把 `P` 当可交易。未知轮询间隔、重试窗口和失败恢复方式统一标记 `[需要官方确认]`。

申请状态查询的三个字段在官网必填列仍为 `N`；接入方确认成功查询时 `apply_reason/apply_status/huifu_id` 在 `Y/P/N/F` 四种状态均返回。该结论不定义 `F` 的重提、恢复或轮询策略。

## 文档异常

官方类型/示例冲突不是运行时错误码。用户详情的 `resp_code` 当前已修正为 `String(8)`；String(JSON)/Object 按 `user-onboarding-platform-contracts.md` 的 wire 矩阵解析，不能在业务层伪造成功码或吞掉解析异常。
