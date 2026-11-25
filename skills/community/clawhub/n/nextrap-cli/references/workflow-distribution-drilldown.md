# 从请求分布定位日志样例
<!-- reference-type: workflow -->

> **范围**：按用户给出的 URL、产品名称或其他真实条件查看一种请求分布，并在有可靠 IP 桶时定位少量日志；不自动遍历分布，不猜路径、类型或产品标签的检索映射，不做产品管理。
<!-- slot: 范围 -->

## 前置条件

- [ ] 已确认当前 CLI 身份和目标环境，后续始终使用同一实际可执行文件。
- [ ] 已取得原始线索、日期窗口和要回答的维度。例：“看看这段登录 URL 线索在 11 月 13 日至 14 日主要来自哪些 IP；从一个可用 IP 取三条请求核对。”产品名称或 URL 的条件写法见 [query.md](query.md)，不要把名称当作产品 ID。
- [ ] 已读取 [stats.md](stats.md) 的桶与计数契约；只有还要具体请求时才进入日志步骤。只问不同对象有多少时，使用该文档的 `unique-count`，不为了计数额外跑完整分布。
<!-- slot: 前置条件 -->

### 步骤 1：直接查询问题所需的一种分布

把用户线索组为 `BASE_QUERY`，后续保留它及日期。下面用 URL 线索演示 IP 分布；替换为用户提供的真实输入。用户问路径、类型或产品时按 [stats.md](stats.md) 选择相应维度，不为凑概览再请求其他三种分布，也不先跑一遍日志。

```bash
BASE_QUERY='url="*/api/auth/login*"'
START_DATE='2026-11-13'
END_DATE='2026-11-14'
nextrap-cli stats distribution --query "$BASE_QUERY" --by ip \
  --start "$START_DATE" --end "$END_DATE" --size 5 -o json \
  --jq '{total,meta,buckets:[.data[] | {dimension,name,name_label,value,masked,can_filter,filter_value,filter_reason}]}'
```

退出码为 0 后，用每个桶的 `name` 说明“谁/哪一类”，用 `value` 说明桶内请求数，结合打码信息解释可识别程度。`total` 是桶种类数，不是请求数；当前页也不是全部分布，不拿页内求和生成全量比例。具体近似、窗口与字段含义沿用 [stats.md](stats.md) 和 [output.md](output.md)。

只有分布问题就回答并停止。`buckets: []` 表示本页没有桶，即便 `total` 仍大于零也不自动翻页。业务拒绝、未知或已脱敏标签不通过换账号、猜值或扩大窗口来补齐。
<!-- slot: 步骤 -->

### 步骤 2：仅从可回填的 IP 桶检索样例

用户还需要具体请求时，选定上一步一个 IP 桶；必须同时满足 `dimension="ip"`、`masked=false`、`can_filter=true`，并确认 `filter_value` 是合法且非空的 IPv4/IPv6。`null` 不是 `false`，`can_filter` 也不是账号权限证明。把该桶原样提供的 `filter_value` 传给 `FILTER_IP`；不从打码 `name` 还原地址，不换用别的桶蒙混。

下列投影供方法/URL层面核对；任务已需要载荷时首次就按需保留 `req_body/req_header` 或原始结构，同时保留打码原因。不要丢弃所需证据后再靠额外请求补回来，答复只摘任务必要且已脱敏的内容。

```bash
DRILL_QUERY="(${BASE_QUERY:?保留步骤1的原始条件}) && ip==\"${FILTER_IP:?取已确认可回填桶的 filter_value}\""
nextrap-cli log search --query "$DRILL_QUERY" \
  --start "${START_DATE:?沿用步骤1开始日期}" \
  --end "${END_DATE:?沿用步骤1结束日期}" --size 3 -o json \
  --jq '{total,meta,records:[.data[] | {id,create_time,product_id,attacker_ip,req_method,req_url,req_body_truncated,mask_reason_code,mask_reason}]}'
```

这里的 `&&` 是逻辑 AND：新条件是“原条件 **并且** 该精确 IP”，不能把原条件丢掉后只查 IP；原条件加括号保留原有 OR 组合的含义。检索沿用同一请求窗口和公共范围，但各接口不是同一快照，后台也可能按权限裁切，不能要求样例数与桶数量完全一致。

退出码为 0 且有记录后，用 `attacker_ip/req_method/req_url` 解释这些样例如何支持原问题，并保留真实 `id/create_time/product_id` 供已授权的单条跟进。字段与定位规则见 [log.md](log.md)。若没有命中，报告“该条件下未取到样例”，保留此前分布的观察，不反过来宣称该桶造假或自动重跑。

对于 `path/type/product` 桶，在分布答复后停止自动下钻：路径标签不是完整 URL，类型编号不是检索枚举，产品名称可能重名；即使某桶提供了产品 ID，也不是可直接回填的公共检索字段。确需继续时，只使用用户另行提供或已有权威数据确认的检索条件，按 [query.md](query.md) 另行组条件，不把这种查询声称为与原桶严格等价。

最终答复保留“原条件与窗口 → 桶标签和请求数及打码状态 → 是否下钻、所选真实 IP → 少量请求证据”的关系。足以回答时即停止，不默认进入全文、上下文或解密。
<!-- slot: 步骤 -->

## 注意事项

- [ ] 桶标签 `name` 与请求数 `value` 一起解释，没有只报几个数或把 `total` 当作请求总数。
- [ ] 下钻资格全部明确；IP 来自该桶 `filter_value`，原条件、日期和公共范围均保留，括号未改变原条件的逻辑。
- [ ] 路径、类型和产品桶没有被猜测映射；产品名称与 ID、过滤值可用性与账号权限保持区分。
- [ ] 只取已授权数量的样例。日志检索有结果时可能消费检索次数及返回条数；异常后先按主文件错误规则判断，不直接重跑或自动翻页。
<!-- slot: 注意事项 -->
