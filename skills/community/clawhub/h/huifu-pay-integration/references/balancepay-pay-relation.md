# 付款关系提交

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acct_fkgxtj.md>；快照 `2026-11-04`，官网更新时间 `2025-02-25`。

接口：`POST /v2/trade/payrelation/apply`。仅适用于须预先维护付款关系才能正常余额支付的商户；完整24个字段路径见 `payment-complete-field-catalog.md` 的“付款关系提交”。

## 请求

必填 `out_huifu_id:String(32)`、`req_date:String(8)`、`req_seq_id:String(128)`、`pay_relations:String(JSON Array)`。数组项 `in_huifu_id:String(32) Y` 是入账方，`apply_type:String(3) Y` 仅 `ADD/DEL`。先序列化明细数组一层；不能把数组直接发送或改成包含明细的 JSON 对象。

本接口没有请求 `huifu_id`，不为了补 SDK 来源头虚构业务字段；SDK未从出款号生成商户头也不是替换出款号的依据。

## 提交与确认

分别检查顶层 `resp_code` 和逐项 `apply_stat=S/F`、`apply_desc`；一项成功不等于全部成功。可返回 `confirm_url:String(128) N`，成功示例描述“等待确认”，不得把提交成功直接判关系已生效。跳转 URL 属于运行时返回值，不使用官网示例 URL 作为默认地址。本页未声明确认查询接口或异步通知，未知确认机制留适配点。

## 返回编码待确认

正式响应 `pay_relations:String Y` 的描述误拼 `jsonArry`，示例为 JSON 数组字符串。保留正式原文与示例差异；目录保留独立子字段，wire 只到 `response.data.pay_relations`，响应数组形态和严格解码留 `[需要官方确认]`。请求侧明确为 jsonArray，不受此响应冲突影响。
