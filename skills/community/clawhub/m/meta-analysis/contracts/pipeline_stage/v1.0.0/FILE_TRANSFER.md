# Meta-Analysis · 文件双向传输接口（上传 / 下载）

## 0. 结论一句话
**下载已具备通用通道（S3 预签名 GET + 本地通用下载器），只差“文档类产物”的显式返回字段；上传是空白，本次在契约中预留 `attachments`（请求侧=上传引用、响应侧=可下载产出）与 `request_upload` tool_card，采用与现有 S3 外置 + tool_card 范式对称的方案。两侧均 optional，老版本技能零影响。**

---

## 1. 现状盘点

### 1.1 下载（已实现）
- coze 端把 svg / R 脚本 / 完整 envelope 上传 S3，返回 `{storage:"s3", key, url}`（url 为预签名 GET，默认 3600s）。
- 本地 `coze_client.py` 已有 3 个通用下载器，均基于预签名 GET：
  - `_fetch_full_json`（GET 完整 envelope）
  - `_reassemble_from_manifest`（GET manifest 重组）
  - `_fill_external_svgs_legacy` / `_download_s3_ref`（GET figures[].url / repro.url / 任意 `{storage:"s3",url}`）
- ⚠️ 现状下载的载体是**计算结果**（svg/r/json），契约里**没有“文档类产物”字段**。Block C 生成的 docx 稿件若要下载，需在响应显式化 `attachments`（结构与现有 S3 引用完全一致）。

### 1.2 上传（空白）
- 老 `run_meta` 发送 `{task,data,params,figure,query_origin,request_id}`，`data` 是结构化 `{rows/csv_path}`，**无任何二进制/文件字段**。
- 新 per-stage 契约原 request schema 也无 `attachments`。
- coze 端无文件接收端点 / 预签名 PUT 机制。

---

## 2. 设计原则（对称 + 复用）
1. **S3 双向通道对称**：下载用预签名 GET，上传用预签名 PUT。同一 bucket / 命名空间，coze 端据 `key` 取。
2. **复用 tool_card 范式**：上传触发走 `request_upload` tool_card（与现有 `ct-literature` 委派同构），本地 adapter 代码层机械执行、结果回灌 `stage_context.tool_card_outputs`，**不回发 coze**。
3. **引用而非内联**：JSON 信封只传 `{storage,key,sha256,...}` 引用，二进制永远走 S3，避免大体积冲垮 JSON（现有 4000 字符截断防护已证明此路正确）。
4. **全 optional / 向后兼容**：`attachments` 在请求与响应侧均为 optional；老请求/响应不带不报错；新增 `request_upload` tool_card 类型老 adapter 不识别即忽略。

---

## 3. 上传接口（本地 → coze）

### 3.1 请求字段 `attachments`（request.schema.json）
```json
"attachments": [
  {"storage":"s3","key":"pipeline/<pid>/uploads/<sha256>.pdf",
   "filename":"Smith2020.pdf","mime":"application/pdf",
   "size_bytes":123456,"sha256":"<64hex>",
   "put_url":"https://s3/put?X-Amz-Signature=..."}
]
```
required：storage / key / filename / mime / size_bytes / sha256。

### 3.3 多文件同时上传与用途区分（关键）
- 一次请求可在 `attachments[]` 携带 **N 个文件**（数组），本地 adapter 对每个文件**并发 PUT** 到 S3（见 §7 落地清单的“并发”要求），实现“同时上传多个 PDF”。
- **同类型多文件**（如 5 篇文献全文）：coze 端无需区分类别，遍历 `attachments` 逐个解析即可。
- **混合类型多文件**（如 3 篇文献 + 1 份提取模板 + 1 张 RoB 截图）：每项 `AttachmentRef` 带可选 `purpose` 字段，coze 据 `purpose` 路由到对应解析器（文献→文本抽取，模板→提取 schema，截图→OCR）。`purpose` 为 optional，缺失时按同类型批量处理。
- 示例（已入 `test_contract.py §7.1b`）：
  ```json
  "attachments":[
    {"storage":"s3","key":"p1/uploads/lit1.pdf","purpose":"literature_fulltext", ...},
    {"storage":"s3","key":"p1/uploads/lit2.pdf","purpose":"literature_fulltext", ...},
    {"storage":"s3","key":"p1/uploads/tpl.pdf","purpose":"extraction_template", ...}
  ]
  ```

### 3.2 上传流程（两阶段，tool_card 驱动）
1. coze 编排在 `A2.literature_search` / `A4.data_extraction` 阶段，若需本地 PDF，返回：
   ```json
   {"tool_cards":[{"card_ref":"tc1","need_tool":"request_upload",
     "params":{"files":[{"accept":"application/pdf","required":true,"max_bytes":52428800}],"count":2},
     "sync":"blocking","timeout_sec":120}]}
   ```
2. 本地 `execute_tool_cards` 识别 `need_tool="request_upload"` → 对每个待传文件：
   a. 调 coze 的 `get_upload_ticket` 端点（或 tool_card.params 直接给 `put_url`）拿预签名 PUT URL；
   b. `_upload_file(path, put_url)`：PUT 文件到 S3，计算 sha256；
   c. 组装 AttachmentRef。
3. 结果回灌 `stage_context.tool_card_outputs[{card_ref:"tc1",status:"ok",result:{...AttachmentRefs}}]`。
4. 续跑请求在 `attachments` 携带这些引用（或 coze 端据 `tool_card_outputs` 内的 key 自取）。
5. coze 端按 `key` 取 PDF、解析（pdf 文本 / 数据提取）。

> 备选“推模式”：本地已有 S3 写凭据时，可直传约定 bucket 后仅将引用放进 `attachments`，不经 tool_card。契约两种都支持（`put_url` 可选）。

---

## 4. 下载接口（coze → 本地）

### 4.1 响应字段 `attachments`（response.schema.json）
```json
"attachments":[
  {"storage":"s3","key":"pipeline/<pid>/outputs/manuscript.docx",
   "url":"https://s3/get?X-Amz-Signature=...","filename":"manuscript.docx",
   "mime":"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
   "size_bytes":54321,"sha256":"<64hex>"}
]
```
required：storage / key / url / filename / mime / size_bytes / sha256（**下载必须带 url**）。

### 4.2 下载流程（复用现有通道）
本地 adapter 收到 `attachments[]` → 对每个 `{storage:"s3",url}` 调已有 `_download_s3_ref` → 落盘本地 workdir（文件名取 `filename`，完整性 sha256 校验）。**无需新增下载器**，只新增“遍历 attachments 并落盘”的编排逻辑。

> 与 `stage_result.artifacts[].format ∈ {docx,xlsx}` 的关系：小体量结构化产物（<几 MB）仍可内联 `data`；大文件（docx/xlsx 整稿）走 `attachments` S3 外置，与现有 figures[].svg 外置一致。

---

## 5. AttachmentRef 字段语义（两侧共用 $defs）

| 字段 | 上传侧 required | 下载侧 required | 说明 |
|---|---|---|---|
| storage | ✅ | ✅ | 仅 "s3" |
| key | ✅ | ✅ | S3 对象 key（coze 命名空间） |
| url | ❌（put_url 可选） | ✅（GET） | 上传后 coze 据 key 自取；下载必须 |
| filename | ✅ | ✅ | 含扩展名，落盘命名 |
| mime | ✅ | ✅ | application/pdf 等 |
| size_bytes | ✅ | ✅ | 体积 |
| sha256 | ✅ | ✅ | 完整性校验 / 去重 |
| put_url | ❌ | — | 仅上传临时 PUT 凭证 |
| purpose | ❌ | ❌ | （可选）文件用途标识，一次上传多文件时区分类别：literature_fulltext / extraction_template / roi_screenshot / manuscript_draft / prisma_figure / grade_table 等。coze 据 purpose 路由解析；不填则视为同类批量。详见 §3.3 |

---

## 6. 向后兼容（与 BACKWARD_COMPAT.md R1–R5 一致）
- **请求侧**：`attachments` optional → 老 `run_meta` 不带，coze 双模路由（R1）判定 legacy 不受影响；老路径根本不碰该字段。
- **响应侧**：`attachments` optional → 老 coze 不返回，新 adapter 忽略（extra 字段被忽略）；老 adapter 不识别新字段即忽略。
- **新增 tool_card 类型 `request_upload`**：老 adapter 不处理 tool_cards（本就不支持），故无影响。
- **下载通道**：复用已有 S3 GET 下载器，老 adapter 下载 svg/r 的逻辑不变；新 `attachments` 下载是增量能力。

---

## 7. 本地 adapter 落地清单（下一阶段）
- [ ] `_upload_file(path, put_url) -> AttachmentRef`（PUT + sha256）。
- [ ] `_request_upload_ticket(spec) -> put_url`（调 coze `get_upload_ticket` 端点；或 tool_card.params 直接给）。
- [ ] `execute_tool_cards` 识别 `need_tool="request_upload"` → 批量上传 → 回灌 `tool_card_outputs`。
- [ ] `download_attachments(resp) -> list[local_path]`（遍历 `attachments`，复用 `_download_s3_ref`，sha256 校验）。
- [ ] 多文件：API 设计为数组，支持批量 + 并发 PUT（按 PDF 数）；超大文件（>100MB）走 S3 multipart（预留）。

---

## 8. coze 端落地清单（草稿，待重部署 state.py）
- [ ] 新增 `get_upload_ticket` 端点（或集成进 `/run` 的 tool_card 派发）返回预签名 PUT URL（限 key / TTL）。
- [ ] 编排在 A2/A4 阶段识别请求 `attachments`，据 `key` 取 PDF 解析。
- [ ] 响应产出 `attachments`（docx/xlsx 走 S3 外置，复用现有外置逻辑）。
- [ ] 上传安全：sha256 校验 + 文件类型白名单（pdf/docx/xlsx）+ 可选病毒扫描 + key TTL 清理。
- [ ] `state.py` 加 `attachments` 字段（extra='ignore' 已满足新字段容错）。

---

## 9. 风险与约束
- ⚠️ **预签名 URL TTL**：PUT（上传）与 GET（下载）均有时效，本地须在 TTL 内完成 PUT / 用户须在 TTL 内触发下载；过期则重新申请 ticket。
- ⚠️ **大文件**：单 PDF 数十 MB，S3 PUT 需稳；coze 端解析需资源隔离（避免 OOM）。
- ⚠️ **安全**：上传文件须做类型白名单 + sha256 去重 + 扫描；key 命名空间隔离防止越权读取他人 pipeline 文件。
- ⚠️ **coze 端 `extra='ignore'`**：仅保证“多字段不报错”，新字段要被消费仍须 `state.py` 加字段并重部署（见 §8）。

---

*本文件与 `SPEC.md §12`、`adapters/coze/coze_contract.md §10` 同步；属设计期产物，coze_contract.md 按 §16.7 不随技能发布。*
