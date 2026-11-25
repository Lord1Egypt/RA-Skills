# 身份与情报额度
<!-- reference-type: business -->

> **范围**：读取当前凭证对应的账号身份与三项情报额度；不查询产品画像、IP画像、节点或蜜罐额度，不修改账号。
<!-- slot: 范围 -->

## 命令一览

| 命令 | 作用 |
|---|---|
| `nextrap-cli status` | 读取身份与检索次数、结果条数、解密次数余额 |
<!-- slot: 命令清单 -->

### nextrap-cli status

```bash
nextrap-cli status -o json --jq '.data | {role_name, info_search_query_remaining, info_search_result_remaining, info_search_decrypt_remaining}'
```
<!-- slot: 示例 -->

| 输出 | 含义 |
|---|---|
| `data.role_name` | 后台返回的角色名称，不从名称反推出字段权限或无限额度。 |
| 三个 `*_remaining` | 后台实际余额；缺失值为 `null`，真实 `0` 为零余额，不写死各会员的默认额度。 |
| 调用范围 | 身份与额度两个接口均成功才输出结果；本命令不扣检索或解密额度，没有日期或 scope 参数。 |
<!-- slot: 参数 -->

## 注意事项

- [ ] 只向用户展示本任务需要的身份字段；不在报告复制邮箱、账号 ID 等多余个人信息。
- [ ] 余额是查询时的状态，并发使用或重置可能改变它，不能据此承诺下一次操作必然成功。
<!-- slot: 注意事项 -->
