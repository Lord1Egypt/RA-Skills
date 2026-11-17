# 用户开户请求字段保真规则

## ID 角色

- 领域模型使用 `userHuifuId` 表示 `/v2/user/*` 的目标用户，用 `merchantHuifuId` / `channelHuifuId` 表示调用主体或上级。
- wire 层按官方字段名映射：用户业务入驻的 `data.huifu_id=userHuifuId`，`data.upper_huifu_id=merchantHuifuId|channelHuifuId`。
- 企业/个人用户开户没有 `data.huifu_id` 和 `upper_huifu_id`；禁止添加空值、占位或当前调用主体。
- `sys_id` 保持调用主体角色，不得替换为刚创建的用户号。

## 调用方字段

- 调用方给出的 `req_date`、`req_seq_id`、`apply_no`、真实 ID、费率、卡类型和材料标识应原样进入校验；缺失或非法时报错，不自行“修复”。
- 申请状态查询和用户信息查询页面都明确写明 `req_seq_id` 在同一商户号当天唯一；分别在对应查询请求中校验。开户和业务入驻页面没有该说明，不得外推成所有用户接口的通用幂等规则。
- 网络不确定时不能自动更换流水重提。业务幂等、查询补偿和重试语义未获官方确认时标记 `[需要官方确认]`。

## 嵌套与 String(JSON)

- 按完整父路径保留同名字段；例如基础信息省市、结算卡省市、e账户银行卡省市各自独立。
- 先在业务对象层校验所有叶字段，再按 `user-onboarding-platform-contracts.md` 的 wire 矩阵逐层序列化；嵌套 String(JSON) 各自只序列化所在层一次。
- 响应先验签，再按矩阵逐层解码；`elec_acct_config.elec_card_list` 等明确双层边界需要按父、子各解一次，禁止递归猜解和跨对象扁平化。
- 官网类型列与说明/示例冲突继续记录；已由接入方按说明裁决的 wire 不再回退为未知。

## 图片材料

用户开户和业务入驻可引用图片上传返回的 `file_id`，但图片上传 `data.huifu_id` 只支持直属商户号。不得将 `userHuifuId` 作为上传字段或来源头；无法确认上传主体时硬停。
