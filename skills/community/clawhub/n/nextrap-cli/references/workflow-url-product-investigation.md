# 从 URL 或产品名称调查请求
<!-- reference-type: workflow -->

> **范围**：把用户给出的 URL、接口片段或产品名称转为公共日志调查，按问题补充规模、分布或单条前后文；不管理产品、不猜产品 ID、不生成漏洞利用结论。
<!-- slot: 范围 -->

## 前置条件

- [ ] 使用主文件确认的同一实际 CLI 路径和环境；示例变量在每次独立 shell 中明确带入。
- [ ] 已有真实 URL / 路径片段 / 产品名称及所需日期。例：“看这个产品这两天收到什么请求，有多少不同来源，挑一条看看前后动作。”只问数量时直接做步骤 3 所需统计，不先取样。
- [ ] 条件写法见 [query.md](query.md)；保留用户原意，区分包含名称、精确名称与产品编号。
<!-- slot: 前置条件 -->

### 步骤 1：固定线索及窗口

URL 片段与产品名称是两种可选入口；不要把示例产品当用户目标，也不要默认把两种条件一起加上。已有用户表达式时保留其逻辑。下面展示产品入口，URL 入口改用 query.md 中的 URL 条件：

```bash
BASE_QUERY='product="Crocus"'
START_DATE='2026-11-13'
END_DATE='2026-11-14'
```

名称片段可能对应多个产品，不能在查询前自行选一个 ID。若用户同时给 URL 和产品，才把两项按原意组合。字段不确定时先查看 `log fields`；账号可用性未知由后台对已授权查询判定，明确拒绝则停止该分支。
<!-- slot: 步骤 -->

### 步骤 2：需要请求行为时取少量样例

下面保留方法/URL层面的证据；用户问题已需要载荷时，首次调用就按需加入 `req_body/req_header` 或保留原始结构，保留打码原因，不为修补自己丢弃的字段自动重查。最终答复去除敏感内容。

```bash
nextrap-cli log search --query "${BASE_QUERY:?使用步骤1的真实线索}" \
  --start "${START_DATE:?使用原开始日期}" --end "${END_DATE:?使用原结束日期}" \
  --size 3 -o json \
  --jq '{total,meta,records:[.data[] | {id,create_time,product_id,product_name,attacker_ip,req_method,req_url,attack_type_name,req_body_truncated,mask_reason_code,mask_reason}]}'
```

先核对退出码，再从实际方法、URL、来源、产品名称与时间描述请求。名称匹配包含多个产品时说明这一范围，逐条保留真实 ID；这些请求只是样例，不能据此概括所有流量的占比或确认产品存在某个漏洞。没有样例就说明当前条件下未返回，不换产品名、日期或去重方式碰运气。

仅要样例时到此停止；用户只要统计可以跳过本步 API，但必须保留步骤 1 输入。请求量、对象数和分布各自含义见 [stats.md](stats.md)。
<!-- slot: 步骤 -->

### 步骤 3：只为尚未回答的规模问题补统计

问题还需要“多少个不同来源 IP”时，用相同条件和窗口取得去重数；不能拿样例的 IP 去重后当全量：

```bash
nextrap-cli stats unique-count --query "${BASE_QUERY:?保留原条件}" --field ip \
  --start "${START_DATE:?保留原开始日期}" --end "${END_DATE:?保留原结束日期}" -o json
```

如果问题是“主要请求哪些路径”，选择下面的分布，而非为了完整感把所有维度都查一遍；确实同时要求两项时才两项都做：

```bash
nextrap-cli stats distribution --query "${BASE_QUERY:?保留原条件}" --by path \
  --start "${START_DATE:?保留原开始日期}" --end "${END_DATE:?保留原结束日期}" --size 5 -o json
```

解释桶名、桶内请求数、近似性和本页范围，不把桶种类数当请求数。若还需从分布找具体请求，按 [分布下钻流程](workflow-distribution-drilldown.md) 的资格判断；路径桶不自动回填完整 URL。
<!-- slot: 步骤 -->

### 步骤 4：需要连续动作时才取同条上下文

从步骤 2 已选记录取得 `LOG_ID=id`、`LOG_DATE=create_time` 的日期部分、`PRODUCT_ID=product_id`。用户指定某条就用该条；未选定且不同样例会导致不同结论时，说明候选而不擅自混用定位值。无法取得有效产品编号时停止上下文分支。

```bash
nextrap-cli log context "${LOG_ID:?从同一选定记录取得}" \
  --date "${LOG_DATE:?从同条真实时间取得日期}" \
  --product-id "${PRODUCT_ID:?从同条取得有效非零产品编号}" --direction before -o json
```

方向按用户问题选 `before` 或 `after`，都需要才查两边。上下文依据边界记录和邻居规则，不继续套用原 URL / 产品名称条件，也不假定邻居只能落在原检索日期内。全文与截断、打码分支见 [business.md](business.md)，具体定位限制见 [log.md](log.md)。

最后把“输入线索及其匹配范围 → 实际样例行为 → 所需统计 → 同条前后证据”串成答复；未执行的部分不写成已验证事实。
<!-- slot: 步骤 -->

## 注意事项

- [ ] 三类线索中的 URL 与产品都能进入现有日志和统计命令，没有发明产品子命令或产品编号检索字段。
- [ ] 全程保留原条件、环境与检索窗口；上下文的边界窗口另行解释，多个接口不承诺同一快照。
- [ ] 没有把样例、不同来源数量、请求数和桶种类数混用；没有猜名称到 ID 或日志到漏洞的映射。
- [ ] 仅执行本次问题需要的分支，达到目标即停止；不自动解密、翻页或为展示格式重复检索。
<!-- slot: 注意事项 -->
