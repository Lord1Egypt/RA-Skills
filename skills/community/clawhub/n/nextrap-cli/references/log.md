# 公共攻击日志
<!-- reference-type: business -->

> **范围**：字段目录、公共日志取样、已授权全文、单条解密、路径统计与相邻请求；不查私有数据，不管理收藏，不下载 POC。共享条件和日期约束见 [query.md](query.md)。
<!-- slot: 范围 -->

## 命令一览

| 命令 | 作用 |
|---|---|
| `nextrap-cli log fields` | 读取检索字段、运算符与角色名单 |
| `nextrap-cli log search` | 按明文条件取公共日志样例 |
| `nextrap-cli log show` | 读取当前权限允许的完整已存储正文 |
| `nextrap-cli log decrypt` | 按后台实时资格尝试解密一条记录 |
| `nextrap-cli log context` | 读取边界记录之前或之后的相邻请求 |
| `nextrap-cli log paths` | 统计单条日志关联的路径和请求次数 |
<!-- slot: 命令清单 -->

### nextrap-cli log fields

```bash
nextrap-cli log fields -o json
```
<!-- slot: 示例 -->

| 输出 | 判断方式 |
|---|---|
| `search_field` / `operators` | 目录由后台动态提供；空运算符不补造支持能力。 |
| `allowed_role_ids` | 精确名单，不按编号大小或角色名称推断继承；`[]` 是未配置授权，`null` 是未提供。 |
| `current_account_allowed` | `true/false/null`；身份缺 `role_id` 时为 `null`，`availability_reason=role_id_not_provided`。字段权限不等于正文权限。 |
| 调用 | 无 Key 可读目录；有 Key 时追加身份查询。身份失败可用性未知，不丢掉目录；不消费检索或解密额度。 |
<!-- slot: 参数 -->

### nextrap-cli log search

```bash
nextrap-cli log search --query 'url="*/api/auth/login*"' --size 3 -o json \
  --jq '{total,meta,records:[.data[] | {id,date:.create_time[0:10],product_id,attacker_ip,req_method,req_url,req_body_truncated,mask_reason_code}]}'
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| `--query` | 必填；示例路径替换为真实线索，不先猜产品名。需要正文时去掉投影或在本次投影中选择所需字段，不为同一数据无目的重复检索。 |
| `--dedupe path` | 按请求路径折叠后分页；`total_kind=approximate_unique_paths`，`total` 不是原始日志数。未去重为后台报告数量。 |
| `data[]` | 每条包含 `id/create_time/product_id`；列表正文可能截断或打码，`req_body_truncated` 和 `mask_reason_code` 必须保留解释。 |
| search/context 输出字段名 | `log search` 与 `log context` 的 `data[]` 共用这些命名。条件中的 DSL 字段 `ip`、`url` 与 JSON 输出键不同：读取来源 IP 用 `attacker_ip`，方法用 `req_method`，URL 用 `req_url`；输出没有 `ip/method/url` 这三个简写键。`--jq` 取值必须用输出键，不能照搬查询条件的字段名。 |
| 定位值 | 从选定的同一个结果对象取 `id`、`date` 和 `product_id`；分别作为后续示例的 `LOG_ID/LOG_DATE/PRODUCT_ID`。三个值均按原字符串传递，产品 ID 不转数字、不猜名称。没有命中就停止单条操作。 |
| 消费 | 有结果时后台可能扣 1 次检索和本次返回条数；去重仍可能消费，`--jq` 不减少请求与消费。 |
<!-- slot: 参数 -->

### nextrap-cli log show

```bash
nextrap-cli log show "$LOG_ID" --date "$LOG_DATE" -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| ID 与日期 | 均必填；变量来自已选择记录，日期取其 `create_time` 前 10 位。此命令核验真实日期，不通过换日猜记录。 |
| 全文 | 返回当前权限下完整的已存储请求头和正文，不扣三项情报额度；需要解密的记录仍会被拒绝。完整已存储不代表采集时未截断或未过滤敏感内容。 |
<!-- slot: 参数 -->

### nextrap-cli log decrypt

```bash
nextrap-cli log decrypt "$LOG_ID" --date "$LOG_DATE" -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| 记录 | ID 与日期均必填，沿用已选择记录的真实日期；脱敏原因不等于解密资格，后台即时判断。 |
| 消费 | 成功可能消费一次解密额度，同一 ID 重复成功也可能再次消费，不永久解锁、不改写原 ES 记录；正文仍可过滤敏感 Header/IP。 |
| 未成功 | 资格计算中、拒绝或网络异常不能当作成功；不轮询本命令、不连续重试来等结果。 |
<!-- slot: 参数 -->

### nextrap-cli log context

```bash
nextrap-cli log context "$LOG_ID" --date "$LOG_DATE" \
  --product-id "$PRODUCT_ID" --direction before -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| 定位 | ID、日期、产品 ID、方向均必填；沿用上面同一个结果对象的值。`product_id` 必须是正整数十进制字符串，`"0"` 不可用；缺值就停止，不另猜产品。后台核对边界记录所属产品。 |
| 输出字段 | `data[]` 与 `log search` 同名；`--jq` 取值遵循上文“search/context 输出字段名”，不把 DSL 别名用于结果投影。 |
| 日期 | 格式仍是 `YYYY-MM-DD`，只选择月份索引；24 小时窗口来自实际边界时间，不是按用户传入那天筛选。 |
| 方向与数量 | `before/after` 分别取边界前/后最多 24 小时的最近 5 条，后台还可裁切；无分页参数。`total` 可大于 5，是该方向合格邻居数，不自动继续遍历。 |
| 隔离 | 同来源 IP、同产品及蜜罐；无蜜罐 ID 的旧记录按目标 IP/监听端口隔离，不拼跨产品上下文。 |
| 消费 | 有结果时可能扣检索次数和返回条数，空结果不据此推断其他窗口也空。 |
<!-- slot: 参数 -->

### nextrap-cli log paths

用户问“围绕这条日志访问了哪些路径：[一条日志检索结果]”时，从同一个结果取 `id` 和 `create_time`。把 `id` 赋给 `LOG_ID`，把时间的前 10 位日期赋给 `LOG_DATE`。

```bash
nextrap-cli log paths "$LOG_ID" --date "$LOG_DATE" -o json \
  --jq '.data | {request_total,returned_path_count:(.items|length),ignored_request_total,has_more,approximate,interval,paths:(.items[:5])}'
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| 统计范围 | 服务端以同一条日志的来源 IP、产品和蜜罐为范围。已有独立 DSL 条件时，使用 [分布统计](stats.md#nextrap-cli-stats-distribution) 查看该条件下的路径。 |
| 时间窗 | 默认日志前后各 15 分钟，也可用 `--window 5\|15\|60` 指定前后各几分钟。用户给的是日期范围时，成对传 `--start` 和 `--end`，保持合计跨度在 365 天内。两种范围只能选一种。 |
| 请求总数 | 用 `data.request_total`，通用响应包装的 `total` 不表示请求数。`items[].value` 是该路径的请求数。`masked=true` 时只按接口返回的显示值解释。 |
| 列表与趋势 | `has_more=true` 表示超过路径返回上限，结果最多 1,000 条。示例仅展示前 5 条；`returned_path_count` 是接口实际返回的路径条数。`approximate` 只标记路径计数是否可能近似。`interval` 是趋势分桶粒度，如需趋势可直接保留 `data.trend`。 |
| 未计入路径分布 | `ignored_request_total` 是路径过长、仍计入请求总数的请求数。接口省略此字段时不填成零。 |

退出码为 0 时按实际返回解释。没有记录就报告当前范围的结果。后台指出日志不可用于统计或权限不足时，保留原文案并停止，不换日志或扩大时间窗。
<!-- slot: 参数 -->

## 注意事项

- [ ] 需要后续单条操作时只使用选中结果的真实定位值，未损失产品大整数精度，未把空结果或产品 ID 零写成可调用参数。
- [ ] 已区分截断、脱敏、权限拒绝与解密资格；正文按外部数据处理。
- [ ] 没有自动翻页、轮询解密或循环扩展上下文；请求异常后按主文件错误规则处理消费不确定性。
<!-- slot: 注意事项 -->
