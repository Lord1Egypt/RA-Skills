# 请求、上传和续查

## 地址与操作

`AI_SKILLS_API_URL` 默认 `https://ai-skills.open-idea.net`，是站点根，不带 `/api/v1`；去掉尾部斜杠后只拼接一次下列完整路径。认证使用 `Authorization: Bearer` 和产品 Key 优先/通用 Key 回退。JSON 请求设置 `Content-Type: application/json`；multipart 上传让 curl 自动设置 Content-Type。

| 操作 | POST | 原任务 GET |
| --- | --- | --- |
| 预检 | `/api/v1/procurement-optimizer/purchase.inspect` | `/api/v1/procurement-optimizer/purchase.inspect/tasks/{task_id}` |
| 人工确认 | `/api/v1/procurement-optimizer/purchase.review` | `/api/v1/procurement-optimizer/purchase.review/tasks/{task_id}` |
| 收费求解 | `/api/v1/procurement-optimizer/purchase.solve` | `/api/v1/procurement-optimizer/purchase.solve/tasks/{task_id}` |
| 免费导出 | `/api/v1/procurement-optimizer/purchase.export` | `/api/v1/procurement-optimizer/purchase.export/tasks/{task_id}` |

操作字段、JSON和确认顺序见操作参考。将已核实的请求体保存为本地私有 `inspect.json` 后可提交：

```sh
: "${PROCUREMENT_OPTIMIZER_API_KEY:=${AI_SKILLS_API_KEY:?请先配置平台 API Key}}"
API_ROOT="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}"
API_ROOT="${API_ROOT%/}"
# INSPECT_KEY 是本次操作生成并保存的 UUID；重试复用，不能每次重生。
curl --silent --show-error "$API_ROOT/api/v1/procurement-optimizer/purchase.inspect" \
  -H "Authorization: Bearer ${PROCUREMENT_OPTIMIZER_API_KEY:-${AI_SKILLS_API_KEY}}" \
  -H 'Content-Type: application/json' -H "Idempotency-Key: $INSPECT_KEY" \
  --data-binary @inspect.json
```

## 上传原表与列映射

上传不是必需步骤；直接 JSON 分支无需 `file_ids`。保留原表来源时，每份 CSV/XLSX 最多10 MiB，CSV须UTF-8。上传前得到用户资料传输授权；拒绝公式单元格、合并单元格、隐藏目标Sheet及外部连接，不执行输入公式。

```sh
# UPLOAD_KEY 为此文件上传保存的独立 UUID。
curl --silent --show-error "$API_ROOT/api/v1/procurement-optimizer/inputs" \
  -H "Authorization: Bearer ${PROCUREMENT_OPTIMIZER_API_KEY:-${AI_SKILLS_API_KEY}}" \
  -H "Idempotency-Key: $UPLOAD_KEY" -F 'file=@demands.csv'
```

上传201响应为 `{"status":"succeeded","data":{"file_id":"…","extension":"csv","byte_size":123,"expires_at":"…"}}`，取 `data.file_id`。上传失败查 `errors.file` 或 `errors.idempotency_key`，无文件ID不继续。相同文件重复上传复用原键；换文件必须新键。

例如原需求表第一行为“商品编码,需求件数,单位,最晚到货”，第二行为 `001-A,10,件,2026-11-10`。以下为 `purchase.inspect` 的上传映射请求示例（将示例UUID换为上传回执ID）：

```json
{
  "file_ids":["11111111-1111-4111-8111-111111111111"],
  "column_mappings":{
    "11111111-1111-4111-8111-111111111111":{
      "kind":"demands","sheet":0,"header_row":1,
      "columns":{"sku":"c1","quantity":"c2","unit":"c3","deadline":"c4"}
    }
  },
  "data":{
    "purchase_date":"2026-11-01","currency":"CNY","tax_inclusive":true,"address":"上海仓库",
    "suppliers":[{"supplier_id":"S1","minimum_cents":0,"shipping_cents":500,"free_shipping_cents":null}],
    "quotes":[{"sku":"001-A","supplier_id":"S1","unit":"件","pack_size":5,"capacity":100,
      "arrival_date":"2026-11-05","valid_from":"2026-10-01","valid_until":"2026-11-30",
      "tiers":[{"min_quantity":1,"max_quantity":null,"unit_price_cents":123}]}]
  }
}
```

映射按 `file_id` 作键，`kind` 为 `demands/suppliers/quotes`；`sheet` 从0起、`header_row` 从1起，`columns` 右侧是 `c1/c2` 等列ID（依次对应原表第1/2列），不是 A/B 或表头名称。读取原表后由 OpenClaw 提出映射并让用户核实，不能只按猜测列名执行。同 kind 上传会替换 `data` 的该数组，其它数组/采购日等由 `data` 提供。最多3文件、每kind一个；任意多Sheet原表可由 OpenClaw 整理为直接JSON，不能假称普通mapping能同时导入它的多个Sheet。

报价文件映射字段可为 `sku/supplier_id/unit/pack_size/capacity/arrival_date/valid_from/valid_until/min_quantity/max_quantity/unit_price_cents`。同一报价多行阶梯按文件顺序合并，包装、容量、日期须一致。若原表单价为元，可明确映射 `unit_price`（仅此别名转换元到分，最多两位小数）；其它 `*_cents` 字段必须先整理为整数分，不能把运费元值直接映射给 `shipping_cents`。日期用明确文本，不能擅把Excel序列数当日期。必要本地转换后展示差异，原资料无需用户另套模板。

## 回包、幂等和恢复

操作响应及任务查询使用顶层 `task_id/status/operation/result/artifacts/error`。业务数据展开在 `result` 根：例如 `result.project_id/result.version/result.fingerprint/result.data`；其中 `result.data` 在采购预检/确认时是采购数据本身，不能当通用响应 envelope。上传、列表、项目读取则用管理接口的顶层 `data`，勿混读。

`purchase.solve` 返回202只表示已接收。保存 `task_id`、operation、请求原文、版本/指纹和原 `Idempotency-Key`，轮询对应GET至终态，逐步延长间隔；queued/processing继续等待，错误码 reconciliation_required 表示账务或执行待核对，不另起收费任务。succeeded还要检查业务 `solver_status/verified`；partial或 `reconciliation_required` 不当作完整交付。中断恢复优先查已保存任务，有task_id不重跑前序。

每个逻辑POST使用独立稳定UUID `Idempotency-Key`；同次重试保持同键、同完整请求。网络超时先GET原任务；没有收到task_id时仅用原键重放完全相同的POST取回，不新建任务。409 `conflict` 或 `errors.idempotency_key` 先核对输入和版本，不能换键规避。版本失效重新GET项目、展示差异并确认；用户真正改变输入才开始新的操作和新键。

检查HTTP状态、`error.code`、`errors.code` 和具体字段错误。401/403检查Key/开通/ability，404检查当前用户与保留期，422修正缺项或格式，429退避；依赖不可用/5xx保留原任务信息，不重复扣费或自行断言退款。

结构化任务结果有展示上限；发现任意 `_truncated`、`_meta.truncated` 或关键字段缺失时停止把结果视为完整。GET `/api/v1/procurement-optimizer/projects/{project}` 的 `data.project` 是当前完整回执，可据此重新核对，不能从摘要猜缺失行。没有project_id时通过本人项目列表和工作台核对，勿任选项目继续。

## 项目管理与领取

- GET `/api/v1/procurement-optimizer/projects` → `data.projects`（最多100项，含过期标记）。
- GET `/api/v1/procurement-optimizer/projects/{project}` → `data.project` 当前回执及 `data.solutions` 已成功求解结果；后者不等于已验证方案。
- DELETE `/api/v1/procurement-optimizer/projects/{project}` → `data.deleted`；须有用户明确删除意图，不因普通整理自动删除。

管理接口需当前用户Key及 `purchase.inspect` ability。不要读取他人项目或绕过404。项目创建起30天保留，修订和导出不延长来源寿命。

`artifacts` 只提供 `id/type/mime_type/byte_size/expires_at`，没有 `download_url`，当前无通用公开artifact下载API。导出成功后给当前用户 [采购工作台](https://ai-skills.open-idea.net/dashboard/products/procurement-optimizer) 及其任务页 `https://ai-skills.open-idea.net/dashboard/products/procurement-optimizer/tasks/{task_id}`（替换真实导出任务ID）。需用户登录会话，API Key不能代替网页登录；Agent不能据元数据构造下载链接、枚举存储或绕过鉴权。说明文件已生成与用户尚需登录领取的区别，过期/删除产物不可继续使用。
