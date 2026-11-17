# 操作字段与规则

## 从原资料选择输入分支

- 用户给出文字、报价截图的已核实文字或聊天记录：OpenClaw 提取需求/供应商/报价，建立来源与缺项清单，整理为 `data`，无需上传文件或套模板。图片/PDF/DOCX 不是采购上传接口支持的格式；能可靠读取时在本地提取并让用户核实关键值，不能读清时只索取必要内容。
- 原 CSV/XLSX 可直接读取：OpenClaw 检查表头、单位和金额口径，选择直接 JSON；需要平台保留文件来源时用上传+列映射。最多三个文件，同一 kind 仅一份；普通映射每文件选一个可见 Sheet，不支持把任意三工作表文件当模板。现有平台模板只是可选输入，不是用户前置工作。
- 已有项目：GET 项目读取当前回执；只续查原任务不重新创建。修改输入用 `purchase.inspect` 带 `project_id`、`expected_version`，或在 `purchase.review` 提交完整修正 `data`；两者均产生新版本，再确认后求解。

## 最小正确直接 JSON

下例为 POST `/api/v1/procurement-optimizer/purchase.inspect` 请求体，日期仅作示例，实际使用用户确认日期。示例需求10件，单价123分，运费500分；不能把未知运费填成0。

```json
{
  "title": "采购试算",
  "data": {
    "purchase_date": "2026-11-01",
    "currency": "CNY",
    "tax_inclusive": true,
    "address": "上海仓库",
    "demands": [{"sku":"001-A","quantity":10,"unit":"件","deadline":"2026-11-10"}],
    "suppliers": [{"supplier_id":"S1","minimum_cents":0,"shipping_cents":500,"free_shipping_cents":null}],
    "quotes": [{
      "sku":"001-A","supplier_id":"S1","unit":"件","pack_size":5,"capacity":100,
      "arrival_date":"2026-11-05","valid_from":"2026-10-01","valid_until":"2026-11-30",
      "tiers":[{"min_quantity":1,"max_quantity":null,"unit_price_cents":123}]
    }]
  }
}
```

`data` 顶层仅允许 `purchase_date/demands/suppliers/quotes/locks/baseline/currency/tax_inclusive/address`。不要把回执中的 `schema_version` 原样回传。`title` 最长120字符，整体请求不超过4 MiB。日期均为 `YYYY-MM-DD`，采购日不得晚于需求期限；报价有效期必须覆盖采购日，到货日不得早于采购日。

需求必需 `sku/quantity/unit/deadline`；供应商必需 `supplier_id`，明确确认后提供 `minimum_cents/shipping_cents/free_shipping_cents`。报价必需 `sku/supplier_id/unit/pack_size/capacity/arrival_date/valid_from/valid_until/tiers`。SKU、单位和供应商编码保留文本，前导零不丢失；编码最长64字符，由字母、数字、点、下划线、连字符组成，首位为字母或数字。需求 SKU、供应商编码各自唯一；报价必须引用存在的需求与供应商，同供应商/SKU 只能一条（阶梯合并到 tiers）。可用 `source` 保存来源行；直接整理来源要可追溯，不伪造上传 file_id。

数量、包装和容量均为需求单位的整数；数量1–1000000，包装1–1000000，容量0–1000000。需求/报价单位必须相同；“箱→件”换算先由用户明确，再统一包装、容量、阶梯数量、单价，不能仅改单位名称。最多100个需求、20个供应商、2000条报价，每条最多50档。

金额全部为 CNY 整数分（如1.23元→123）；统一含税，不自动税率换算、汇率转换或浮点舍入。单价0–1000000000分；其它金额及总成本安全上限1000000000000分。`free_shipping_cents:null` 表示不免运，0表示达到0即免运，语义不同。最小采购额及免运门槛仅按该供应商商品额计算，商品额加运费才是总额。

阶梯为整单数量定价，不是分段累进；区间 `[min_quantity,max_quantity)` 从1连续无重叠，末档 `max_quantity:null`。例如1–9件/10件起，对应 `[1,10)` 与 `[10,null)`。不能把“含10”写成排除10的上界。

可选 `locks` 为 `[{"sku":"001-A","supplier_id":"S1"}]` 锁供应商；加 `quantity` 锁该供应商确切数量（0可禁用，须满足包装/容量/交期）。`baseline` 为同形的 `sku/supplier_id/quantity` 分配列表，仅通过当前约束复核的基准才有节省额；没有有效基准不编造节省率。

## 确认、求解与导出

预检回执含 `project_id/version/confirmed/fingerprint/issues/data/expires_at`，回执字段展开在 `result` 根，采购内容数组位于 `result.data`。有 `issues` 先解决，不将预检成功等同确认成功。人工确认摘要应列出来源、采购日/地址、SKU数量与单位、报价/税币种、包装容量/交期、阶梯/起订/运费、锁定和基准、缺项处理及费用。

用户确认后，`purchase.review` 请求最小为：

```json
{"project_id":"11111111-1111-4111-8111-111111111111","expected_version":1}
```

UUID仅为占位，换成预检原值；可选 `data` 是完整修正数据，不是局部 patch。review 生成新版本，不沿用预检旧版本。取 review 的 `result.project_id/result.version/result.fingerprint`，确认 `confirmed=true` 后，`purchase.solve` 请求为：

```json
{"project_id":"11111111-1111-4111-8111-111111111111","version":2,"fingerprint":"<review返回的64位十六进制指纹>"}
```

指纹占位必须替换为回执原值，不自行计算或编造；费用授权需覆盖此版本。求解异步，续查见请求参考。检查 `result.solver_status` 与 `verified`：OPTIMAL且verified表示已证明最优，FEASIBLE且verified仅表示可行；INFEASIBLE为当前约束无解，UNKNOWN为时限内无方案，MODEL_INVALID/复核失败为错误。不能擅改约束换取结果。

`purchase.export` 请求 `{"source_task_id":"<成功且已验证的purchase.solve任务UUID>"}`；来源必须属于当前用户。导出 XLSX分配表、JSON成本及Markdown说明，返回 artifacts 元数据，实际领取方式见请求参考。
