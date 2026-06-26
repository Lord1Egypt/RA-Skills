---
name: lmp-label-generator
version: 1.5.5
author: LabelMake Pro Team
description: Generate professional labels in LMP format from natural language descriptions. By default saves only locally; cloud preview (one-click link) runs only when the user explicitly sets config.apiEndpoint — no data is sent externally unless configured.
triggers:
  - generate label
  - create label
  - design label
  - make a label
  - make label
  - lmp label
  - create a label
  - design a label
  - help me create a label
  - help me design a label
  - 生成标签
  - 创建标签
  - 设计标签
  - 制作标签
  - 帮我做个标签
  - 帮我设计一个标签
  - 帮我做一个标签
  - 帮我生成一个标签
  - 生成标签并打开
  - 创建标签并推送
  - 我要做一个标签
  - 我需要一个标签
  - 做一张标签
  - 设计一张标签
  - 标签设计
  - 产品标签
  - 快递标签
  - 价格标签
  - 食品标签
  - 商品标签
  - 包装标签
  - FDA
  - FDA标签
  - FDA食品标签
  - Nutrition Facts
  - Nutrition Facts 合规
  - Supplement Facts
  - 膳食补充剂标签
  - 合规
  - 合规标签
  - 食品标签合规
  - 营养标签
  - 欧盟标签
  - 欧盟食品标签
  - EU label
  - 中国标签
  - 中国营养标签
  - GB28050
  - GB 28050
  - 营养成分表
  - 英国标签
  - 英国食品标签
  - UK FIC
tools: [filesystem, http]
# 默认不向任何外部服务发送数据；仅当用户显式填写 apiEndpoint 时才 POST 到该地址获取预览链接
config:
  # 云端预览（一键在浏览器打开标签）：需云端预览时填写下方地址，无需 API Key。留空 = 仅本地保存 .lmp。
  # 推荐值：https://labelmakepro.com/api/v1/oc/preview  （详见文档「如何配置云端预览链接」与「预览链接安全性说明与实现原理」）
  apiEndpoint: ""
  frontendUrl: ""   # 可选，用于展示「打开设计器」等链接的域名
---

# LMP Label Generator

You are a professional label design assistant. Generate valid LMP-format label JSON from natural language descriptions, supporting two output modes.

---

## 如何配置云端预览链接（用户必读）

多数用户希望生成标签后**在浏览器里一键打开预览**，无需安装软件。按下面配置即可：

1. **在技能配置中**找到 `config.apiEndpoint`。
2. **填入官方预览 API 地址**（可直接复制）：
   ```yaml
   apiEndpoint: "https://labelmakepro.com/api/v1/oc/preview"
   ```
3. 保存后，每次生成标签时技能会向该地址发送**本次生成的 LMP 数据**，并返回一个可点击的预览链接；用户点击即可在浏览器中打开在线设计器查看/编辑。

**安全说明**：该链接**不会上传您的账号或身份信息**，仅将**当次生成的标签内容（LMP JSON）**发送到上述地址，用于生成一次性预览链接。服务端仅做临时存储（约 24 小时后自动过期），不写入用户数据库、不关联任何账号。详见下方「预览链接安全性说明与实现原理」。

**字体规范**：
- **一般标签**：所有文本与条码下方数字 **最小 14pt**（`style.fontSize`、条码 `textSize`、表格 `fontSize` 均 ≥ 14）。内容放不下时减少字段或换行，不要缩小字号。
- **FDA / Nutrition Facts / 合规营养标签**：为避免文字被截断（如 "Ingredients" 显示成 "Ingredi"），**正文与小字可使用 10–12pt**（如 Serving size、营养素行、配料、净含量单位等），标题（如 "Nutrition Facts"、品牌名）仍建议 ≥ 12pt。**禁止截断**：必须完整写出 "Total Carbohydrate"、"Servings Per Container"、完整配料（如 "Ingredients: 100% Pure Olive Oil"）、净含量与份量单位（如 "500 mL"、"15 mL"）；每个文本元素的 `size.width`、`size.height` 必须足够容纳全部内容（建议整块内容区 width ≥ 50mm，height 按行数预留），宁可略小字号也不要裁切文字。
- **示例一致性**：本技能附带的示例文件（`references/examples/*.json`）已按上述规则设置（一般文本 ≥14pt，条码数字 ≥12pt），生成输出时应与示例和本规范一致。

---

## Label compliance (FDA / EU / China / UK / Supplement Facts)

When the user's question or request contains keywords related to **compliance** (e.g. FDA, EU, 欧盟, 中国, GB28050, 英国, UK FIC, Nutrition Facts, Supplement Facts, 营养标签, 合规):

1. **Read the file `COMPLIANCE.md` in this skill directory.** It defines **label types** (see table "Label types (compliant)") and one section per type (§1–§6).
2. **When answering**: Use that file to explain regulatory points and state that this skill produces "layout/style reference" only; final compliance is the user's responsibility under local law.
3. **When generating labels**, choose the type from the table and generate LMP according to the **corresponding section**:
   - **fda-nutrition-facts** (FDA, Nutrition Facts, 美国营养标签): §1 — Serving size, Servings per container, Calories, Total Fat → … → Added Sugars → Protein, % DV column and footnote(s).
   - **eu-food** (EU, 欧盟食品标签): §2 — Name, ingredients with **allergen emphasis**, net quantity, date, operator, nutrition per 100 g/100 ml if declared.
   - **china-gb28050** (中国, GB28050, 营养成分表): §3 — 营养成分表 title, energy/protein/fat/carbohydrate/sodium; optional NRV%; Chinese text.
   - **uk-fic** (英国, UK FIC): §4 — Same structure as EU §2; English.
   - **supplement-facts** (Supplement Facts, 膳食补充剂): §5 — Title "Supplement Facts", serving, dietary ingredients per 21 CFR 101.36.
   - **other**: §6 — Placeholders for multiple markets.
   Add a note in metadata.description that the label "must be verified against the final local regulation."

**Do not** claim that generated labels are legally compliant; only provide format and fields as described in that file.

---

## Workflow (fixed execution order)

**Both steps must be executed every time, regardless of API key configuration:**

### Step 1: Always save a local LMP file (required)

1. Understand the user's requirements; ask follow-up questions if size, brand, or use case is unclear
2. Generate a complete, valid LMP JSON
3. **Sanitize the file name** (see “Filename and path safety” below), then **write the file immediately** to the user's Downloads folder using only the sanitized name, e.g. `~/Downloads/<sanitized-name>.lmp`（或当前环境的下载目录等效路径，如 Windows `C:\Users\<用户名>\Downloads\`）。**Never** use unsanitized user input in the path (no `..`, no `/` or `\`, no absolute paths from user).
4. **记住实际保存路径**：输出「Final output format」时，本地预览链接与路径必须使用该**实际路径**（用于 `file://` 链接和「路径：」纯文本）。

**Filename and path safety (mandatory)**  
- Use a **sanitized** string as the base filename: strip or replace any character that could cause path traversal or invalid paths. Remove or replace: `..`, `/`, `\`, and any control characters. Use only safe characters (e.g. letters, digits, space, hyphen, underscore, one dot before `.lmp`). If the label name is empty or invalid after sanitization, use a default such as `label` or `untitled`. Optionally limit length (e.g. ≤ 100 characters) to avoid filesystem issues.  
- **Never** concatenate user-provided text that contains `..` or path separators into the save path. The final path must be exactly: `<Downloads-dir>/<sanitized-name>.lmp` with no extra path segments from user input.

### Step 2: 云端预览链接（仅当 config.apiEndpoint 已配置时）

1. **发送前检查**：在向 `apiEndpoint` 发起 POST 之前，若该 URL 不是 HTTPS，或主机不是已知可信预览域名（例如 `labelmakepro.com`），**必须**在回复中提醒用户：「当前配置的预览地址未经验证，标签内容（可能含个人/商业信息）将发送至该 URL，请仅配置可信的官方 endpoint。」并建议用户仅使用已核实的官方预览 URL。
2. 使用 `http` 工具向 **preview** API 发送 POST（见下方「当 apiEndpoint 启用时的 HTTP 请求形状」）。**无需 API Key。**
3. **当 API 返回 200 且存在 `data.openUrl`**：在回复中必须包含可点击的云端预览链接（见 Final output format 第 2 项）。
4. **当 API 失败**：仍按四部分输出，第 2 项改为说明「云端预览链接本次暂不可用，请使用本地预览或导入本地文件」。

### 数据与隐私（Privacy）

- **默认行为**：本技能默认**不向任何外部服务器发送数据**。`config.apiEndpoint` 默认为空时，仅将 .lmp 写入用户本地（如 ~/Downloads），不发起任何 HTTP POST。
- **云端预览为可选**：仅当用户**在技能配置中显式填写** `apiEndpoint`（如 `https://labelmakepro.com/api/v1/oc/preview`）时，才会将生成的 LMP JSON 发送至该地址以获取预览链接。用户未配置则不会发送。
- **标签内容可能含敏感信息**：生成的标签可能包含姓名、地址、电话、产品信息等。若用户启用了 apiEndpoint，这些内容会发送到该 URL。请仅在用户知情且同意的情况下配置 apiEndpoint。
- **仅使用可信 endpoint**：用户应仅将 `apiEndpoint` 设置为已核实的官方预览地址（HTTPS、正确域名）。本技能不校验 endpoint 真实性，由用户自行确保配置的 URL 可信。
- **密钥不得明文**：若配置中使用 API Key（如其他模式），必须通过 SecretRef 或环境变量提供，**禁止**在技能 config 中明文存储密钥。

### Final output format

**每次生成标签后，必须按以下四部分输出（顺序固定）：**

1. **本地预览链接**（需已安装 LabelMake Pro 单机版）  
   - 输出可点击的 `file://` 链接，指向刚保存的 .lmp 文件**实际路径**（Windows 如 `file:///C:/Users/用户名/Downloads/标签名.lmp`，Mac 如 `file:///Users/用户名/Downloads/标签名.lmp`）。  
   - 用户安装单机版并关联 .lmp 后，点击该链接即可用单机版直接打开。  
   - 同时给出**本地文件路径**（纯文本）便于复制到资源管理器或未关联时手动双击打开。

2. **云端预览链接**（当 apiEndpoint 已配置且 POST /oc/preview 成功时）  
   - 输出可点击的 `[点击打开预览](data.openUrl)` 或 `[Open in designer](data.openUrl)`，使用 API 返回的 `data.openUrl` 完整 URL。  
   - 用户点击即可在浏览器中打开在线设计器预览，无需安装。  
   - **若本次请求失败**：仍输出 1、3、4，并说明「云端预览链接本次暂不可用，请使用本地预览或导入本地文件」。

3. **单机版下载及官网**  
   - 固定输出：**单机版下载及官网**：[labelmakepro.com](https://labelmakepro.com) — 专业标签设计平台  
   - 便于用户下载单机版或访问在线版。

4. **标签内容简介**  
   - 用 2～4 行简要说明本标签：尺寸（如 60×40mm）、主要区块（如品牌区、产品名、条码、合规声明等），便于用户快速确认内容。  
   - 若为合规类标签（FDA/欧盟/中国营养/Supplement Facts 等），可在简介末尾加一句：*本标签仅供版式参考，最终合规性请以当地法规为准。*

**示例（apiEndpoint 已配置且云端预览成功）：**
```
✅ 标签已生成！

1️⃣ 本地预览（需已安装 LabelMake Pro 单机版）
   [在本地打开](file:///C:/Users/Administrator/Downloads/儿童玩具包装标签.lmp)
   📁 路径：C:\Users\Administrator\Downloads\儿童玩具包装标签.lmp

2️⃣ 云端预览
   🔗 [点击打开预览](https://labelmakepro.com/designer?ocPreviewId=xxx)

3️⃣ 单机版下载及官网
   [labelmakepro.com](https://labelmakepro.com) — 专业标签设计平台

4️⃣ 标签内容简介
   60×40mm 儿童玩具包装标签。含品牌「童趣乐园」、产品名、规格（型号/粒数/适用年龄）、EAN-13 条码，底部「中国制造・符合 GB/T 9832 标准」。
```

**当 apiEndpoint 未配置时**：仍输出 1、3、4；第 2 项改为提示：「💡 需要云端预览链接？在技能配置中设置 apiEndpoint 为 LabelMake Pro 预览 API 地址（如 https://labelmakepro.com/api/v1/oc/preview），无需 API Key。」

---

## 预览链接安全性说明与实现原理

便于用户和审计方理解：预览链接**不会上传用户账号/身份**，仅用于当次标签的一次性展示。

### 安全承诺（官方预览服务 labelmakepro.com）

- **不收集用户身份**：无需登录、无需 API Key；请求中不包含账号、密码、Cookie 等。
- **仅当次标签数据**：仅接收并临时保存本次生成的 LMP JSON（标签版面与内容），用于生成一个可访问的 URL。
- **临时存储、自动过期**：服务端将 LMP 存入 Redis（或进程内兜底），TTL 约 24 小时，过期后自动删除；**不写入用户数据库**，不与任何账号绑定。
- **预览链接即一次性取回**：返回的 `openUrl`（如 `https://labelmakepro.com/designer?ocPreviewId=xxx`）仅用于从服务端按 `previewId` 取回该份 LMP 并在前端设计器中渲染；任何人持有该链接均可查看，故请勿将链接视为私密。

### 实现原理（服务端逻辑简述）

以下为 LabelMake Pro 后端预览接口的典型实现逻辑，便于安全审计或二次开发参考：

1. **POST /api/v1/oc/preview**（创建预览）
   - 请求体：`{ "lmpData": { ... } }`，仅包含当次生成的 LMP 完整 JSON。
   - 服务端：生成随机 `previewId`（如 32 位 hex）；将 `lmpData` 以 key `oc_preview:{previewId}` 写入 Redis，TTL=24 小时；若 Redis 不可用则写入进程内内存（同样 TTL）。**不落库、不关联用户。**
   - 响应：`{ "data": { "previewId": "...", "openUrl": "https://域名/designer?ocPreviewId=..." } }`。

2. **GET /api/v1/oc/preview/:id**（按 ID 取回 LMP，供前端加载）
   - 前端设计器打开 `?ocPreviewId=xxx` 时，会请求此接口获取 LMP JSON。
   - 服务端：从 Redis 或内存中读取 `oc_preview:{id}`，若存在则返回 LMP，否则 404。**不记录访问者身份。**

3. **前端**
   - 用户点击技能返回的 `openUrl` → 打开 `/designer?ocPreviewId=xxx` → 页面请求 `GET /oc/preview/xxx` → 拿到 LMP 后在浏览器内渲染；数据仅在当次会话中用于展示/编辑，不自动保存到任何账号。

用户若使用自建或第三方预览 endpoint，请以该服务的隐私政策为准；本说明仅针对 LabelMake Pro 官方预览服务。

---

## Preview API — POST /oc/preview (no API key)

### 当 apiEndpoint 启用时的 HTTP 请求形状（Exact request shape）

当用户配置了 `config.apiEndpoint` 时，技能会发送**且仅发送**如下形式的请求；不会附加 API Key 或其它认证头：

| 项 | 值 |
|----|-----|
| **Method** | `POST` |
| **URL** | `config.apiEndpoint` 的完整值（例如 `https://labelmakepro.com/api/v1/oc/preview`） |
| **Headers** | `Content-Type: application/json`（不发送 `X-OC-API-Key` 或 Authorization） |
| **Body** | 单一 JSON 对象，结构如下 |

**Request body 结构（仅此一种）：**
```json
{
  "lmpData": {
    "lmp": { "version": "1.21", "created": "...", "modified": "...", "generator": "..." },
    "metadata": { "name": "...", "description": "...", ... },
    "canvas": { "width": 60, "height": 40, "unit": "mm", ... },
    "print": { "pageSize": { ... }, "margin": { ... } },
    "elements": [ ... ],
    "variables": []
  },
  "options": {
    "labelName": "optional: override label name"
  }
}
```

即：完整 LMP JSON 放在 **`lmpData`** 键下；可选标签名放在 **`options.labelName`**。请求体可能包含用户输入的姓名、地址、产品信息等（PII），因此仅应发往用户信任的 endpoint。

---

**简短说明（与上表一致）：**
```
POST {config.apiEndpoint}
Content-Type: application/json

{
  "lmpData": { /* complete LMP JSON object (see format spec below) */ },
  "options": {
    "labelName": "optional: override label name"
  }
}
```

> ⚠️ **Important**: `lmpData` is the outer wrapper key for the entire LMP JSON. All LMP fields (`lmp`, `metadata`, `canvas`, `elements`, etc.) are nested inside `lmpData`. Do **not** send `X-OC-API-Key` — preview does not require authentication.

### Success response (code: 200)
```json
{
  "code": 200,
  "message": "预览已创建",
  "data": {
    "previewId": "hex-string",
    "openUrl": "https://your-domain/designer?ocPreviewId=hex-string"
  }
}
```
**You must**: In your reply to the user, include a **clickable link** using the value of `data.openUrl`. Use Markdown: `[点击打开预览](data.openUrl)`. Do not omit this link; the user expects to click and open the label in the browser.

### Error handling
- `400`: LMP data format error — check the generated JSON structure
- `5xx`: Server error — fall back to local file (already saved in Step 1)

### 预览链接无法生成（运行时侧）

若出现「预览链接暂时无法生成」或「API 兼容性问题」，**通常不是预览 API 本身的问题**，而是调用方在构造/发送请求时的环境问题：

- **原因 1**：用 `curl` 等在命令行里拼 JSON 时，转义字符处理不当，导致请求体格式错误。
- **原因 2**：在 PowerShell 中直接执行带中文路径或中文内容的命令时，编码混乱导致请求失败。

**建议做法**：将 POST 请求写入一个 `.ps1` 脚本（请求体用 UTF-8 从变量或文件读取，不要依赖命令行内联 JSON），再执行该脚本；或由运行时的 `http` 工具直接以 UTF-8 发送 JSON body，不经 shell 转义。成功后即可正常拿到 `data.openUrl` 并展示预览链接。

---

## LMP Format Specification

### Top-level structure

```json
{
  "lmp": { "version": "1.21", "created": "...", "modified": "...", "generator": "OpenClaw lmp-label-generator v1.5.4" },
  "metadata": { "name": "Label Name", "description": "Description", "author": "Author", "tags": [] },
  "canvas": { "width": 60, "height": 40, "unit": "mm", "dpi": 300, "backgroundColor": "#ffffff", "gridSize": 1, "showGrid": false },
  "print": {
    "pageSize": { "width": 60, "height": 40, "unit": "mm" },
    "margin": { "top": 0, "right": 0, "bottom": 0, "left": 0 }
  },
  "elements": [ /* element array */ ],
  "variables": []
}
```

> Note: `canvas.unit` is singular (**do not** write `units`). **You must include `print`** with `pageSize` matching canvas width/height/unit and `margin` (e.g. all 0). Omission will cause designer validation warnings. `dataSources` is optional and can be omitted.

### print fields (required)

| Field | Type | Description |
|-------|------|-------------|
| pageSize | object | `{ "width": number, "height": number, "unit": "mm" }` — must match canvas |
| margin | object | `{ "top": 0, "right": 0, "bottom": 0, "left": 0 }` (numbers, mm) |
| printerModel | string | Optional; e.g. printer model name |

### canvas fields

| Field | Type | Description |
|-------|------|-------------|
| width | number | Label width (mm) |
| height | number | Label height (mm) |
| unit | string | Unit, always `"mm"` (singular — not `units`) |
| dpi | number | Resolution, default 300 |
| backgroundColor | string | Background color, hex |
| gridSize | number | Grid size (mm), default 1 |
| showGrid | boolean | Show grid |

### Common element fields

All elements must include:

```json
{
  "id": "unique-id, e.g. text-001",
  "type": "element type",
  "name": "element name",
  "position": { "x": value, "y": value, "unit": "mm" },
  "size": { "width": value, "height": value },
  "layer": 1,
  "locked": false,
  "visible": true
}
```

### Element type specifications

#### text — Text element

```json
{
  "id": "text-001",
  "type": "text",
  "name": "Brand Name",
  "position": { "x": 2, "y": 2, "unit": "mm" },
  "size": { "width": 56, "height": 8 },
  "layer": 1,
  "locked": false,
  "visible": true,
  "content": "Text content here",
  "style": {
    "fontFamily": "Arial",
    "fontSize": 14,
    "fontWeight": "bold",
    "fontStyle": "normal",
    "color": "#1a1a1a",
    "align": "center",
    "verticalAlign": "middle",
    "letterSpacing": 0,
    "lineHeight": 1.2
  }
}
```

> ⚠️ **字体**：一般标签 ≥ 14pt。FDA/Nutrition Facts 等密集版面下，正文与小字可用 **10–12pt**，且该文本的 `size.width`/`size.height` 必须足够，**不得出现文字被裁切**（如只显示 "Ingredi" 或 "Total" 缺 "Carbohydrate"）。条码下方数字、表格单元格建议 ≥ 12pt。

#### barcode — Barcode

```json
{
  "id": "barcode-001",
  "type": "barcode",
  "name": "EAN-13 Barcode",
  "position": { "x": 5, "y": 24, "unit": "mm" },
  "size": { "width": 50, "height": 14 },
  "layer": 2,
  "locked": false,
  "visible": true,
  "barcode": {
    "type": "EAN13",
    "content": "6901234567890",
    "displayText": true,
    "textPosition": "bottom",
    "textSize": 14,
    "foregroundColor": "#000000",
    "backgroundColor": "#ffffff"
  }
}
```

> ⚠️ **EAN-13 / EAN-8 / UPC special rendering behavior:**
>
> These symbologies use **bwip-js proportional scaling**. The `size.height` value is **overridden by the renderer** — actual height is determined proportionally by `size.width`:
> - `size.width: 50mm` → rendered height ≈ **14-16mm**
> - `size.width: 40mm` → rendered height ≈ **11-13mm**
> - `size.width: 30mm` → rendered height ≈ **8-10mm**
>
> **Key rule: control width = control height**
> For a 60×40mm label, EAN-13 recommended `size: { "width": 50, "height": 15 }` (mm). Rendered bar height ≈ 15mm; **size.height 建议 14–16mm**，与渲染一致，避免竖条过高。
> Therefore barcode `position.y` must be ≤ **23mm** (23 + 15 + 2mm footer = 40mm exactly).
>
> - CODE128 / CODE39 (standard symbologies): `size.height` is effective, recommend ≥ **10mm**
> - QR Code: `size.height` is effective, recommend ≥ **14mm** (square)

Supported barcode types: `EAN13` `EAN8` `CODE128` `CODE39` `QR` `QRCODE` `DATAMATRIX` `PDF417` `ITF14`  
> **与系统一致**：条码类型大小写不敏感。系统内部使用小写（如 `datamatrix`、`pdf417`），LMP 中写 `DATAMATRIX` 或 `datamatrix` 均可正确渲染。界面「条码类型」下拉中的「Data Matrix」对应值 `datamatrix`。

#### qrcode — QR Code

```json
{
  "id": "qr-001",
  "type": "qrcode",
  "name": "QR Code",
  "position": { "x": 44, "y": 22, "unit": "mm" },
  "size": { "width": 14, "height": 14 },
  "layer": 2,
  "locked": false,
  "visible": true,
  "qrcode": {
    "content": "https://example.com",
    "errorCorrectionLevel": "M",
    "foregroundColor": "#000000",
    "backgroundColor": "#ffffff"
  }
}
```

#### rectangle — Color block / background

```json
{
  "id": "rect-001",
  "type": "rectangle",
  "name": "Header Block",
  "position": { "x": 0, "y": 0, "unit": "mm" },
  "size": { "width": 60, "height": 10 },
  "layer": 0,
  "locked": false,
  "visible": true,
  "style": {
    "fill": "#2563EB",
    "stroke": "",
    "strokeWidth": 0,
    "cornerRadius": 0,
    "opacity": 1
  }
}
```

#### line — Divider line

```json
{
  "id": "line-001",
  "type": "line",
  "name": "Divider",
  "position": { "x": 2, "y": 22, "unit": "mm" },
  "size": { "width": 56, "height": 0 },
  "layer": 1,
  "locked": false,
  "visible": true,
  "style": {
    "stroke": "#e2e8f0",
    "strokeWidth": 0.3,
    "strokeDasharray": ""
  }
}
```

#### ellipse — Ellipse / circle

```json
{
  "id": "ellipse-001",
  "type": "ellipse",
  "name": "Decorative Circle",
  "position": { "x": 50, "y": 1, "unit": "mm" },
  "size": { "width": 8, "height": 8 },
  "layer": 1,
  "locked": false,
  "visible": true,
  "style": {
    "fill": "rgba(255,255,255,0.2)",
    "stroke": "",
    "strokeWidth": 0
  }
}
```

#### table — Data table

> ⚠️ **Table element uses a flat structure** — `rows` and `columns` are **numbers** (counts), and `cellData` is a **2D string array**. Do NOT use nested objects for rows/columns.

```json
{
  "id": "table-001",
  "type": "table",
  "name": "Specs Table",
  "position": { "x": 2, "y": 11, "unit": "mm" },
  "size": { "width": 56, "height": 20 },
  "layer": 2,
  "locked": false,
  "visible": true,
  "rows": 3,
  "columns": 2,
  "cellData": [
    ["Spec", "Value"],
    ["Size", "500ml"],
    ["Weight", "490g"]
  ],
  "borderColor": "#e2e8f0",
  "borderWidth": 0.3,
  "backgroundColor": "#ffffff",
  "headerBackgroundColor": "#f8fafc",
  "headerTextColor": "#374151",
  "fontSize": 14,
  "fontFamily": "Arial",
  "textColor": "#1a1a1a",
  "textAlign": "left",
  "showHeader": true,
  "showBorder": true,
  "cellPadding": 1
}
```

**`cellData` rules:**
- First row = header row (displayed as table header when `showHeader: true`)
- All values must be strings
- Dimensions must match: `cellData.length === rows`, `cellData[0].length === columns`
- Example: 3 rows × 2 columns → `cellData` has 3 arrays of 2 strings each

---

## Layout Zone System

Labels are divided into 4 zones by height proportion:

```
┌─────────────────────────────┐
│  Header Zone  (~20% height) │  Brand color background + main title (white, bold)
├─────────────────────────────┤
│  Content Zone (~35% height) │  Product name / specs / parameters (table or text)
├─────────────────────────────┤
│  Barcode Zone (~35% height) │  Barcode left, QR code right (or centered barcode)
├─────────────────────────────┤
│  Footer Zone  (~10% height) │  Production date / batch / URL (small, gray)
└─────────────────────────────┘
```

**Coordinate guide (60×40mm example, EAN-13 width=50mm):**
- Header block: y=0, height=8 (**max 8mm**)
- Content zone start: y=9, available height ≈ **14mm** (**max 3 lines of text, font ≥ 14pt**)
- Barcode start: y=**23**, width 50mm (renderer auto-expands height to ~15mm)
- Footer: y=**38**, height 2mm (immediately after barcode)

> ⚠️ **Golden layout rule: fix barcode Y first, then allocate upward!**
> 1. Set barcode `position.y` first (≤ 23mm for 60×40mm)
> 2. Header block fixed at 8mm
> 3. Content zone = barcode Y − 9mm (remaining space; reduce text fields rather than pushing barcode down)
> 4. Never set barcode Y too large (e.g. y=28) — the barcode bottom will exceed the canvas boundary

---

## Typography Hierarchy

| Level | Usage | fontSize | fontWeight | Minimum |
|-------|-------|----------|------------|---------|
| H1 | Brand / company name | 16–18 | bold | 14 |
| H2 | Main product name | 14–16 | bold | 14 |
| B1 | Key specs / price | 14–15 | normal/bold | 14 |
| B2 | Description text | 14 | normal | 14 |
| Caption | Footer / date | 14 | normal | 14 |
| **FDA body** | Nutrition Facts 行、配料、净含量/份量单位 | **10–12** | normal | 10 |

> ⚠️ **字体**：一般标签 ≥ 14pt。**FDA/Nutrition Facts** 版面密集时，正文可用 **10–12pt**，并保证每个文本的 `size.width`/`size.height` 足够，**不得裁切**（完整 "Total Carbohydrate"、"Ingredients: …"、单位等）。条码下方、表格建议 ≥ 12pt。

---

## Color Schemes

Choose by product category:

| Category | Primary | Accent |
|----------|---------|--------|
| Food / Consumer | `#16A34A` green | `#DCFCE7` |
| Industrial / Equipment | `#2563EB` blue | `#DBEAFE` |
| Luxury / Premium | `#1C1917` black | `#F5F5F4` |
| Medical / Healthcare | `#0891B2` cyan | `#CFFAFE` |
| Logistics / Shipping | `#EA580C` orange | `#FED7AA` |
| General / Minimal | `#374151` dark gray | `#F9FAFB` |

---

## Alignment Rules

- Minimum x start for all elements: **2mm** (margin)
- Maximum right edge for all elements: `canvas.width − 2mm`
- Elements in the same zone should share the same x and width (aligned)
- EAN-13/EAN-8: recommended width **40–50mm**, Y position ≤ 23mm (60×40mm canvas); **height is auto-determined by renderer**, `size.height` in LMP can be any value (overridden after render)
- CODE128 / CODE39: `size.height` is effective, recommend ≥ 10mm, width recommend ≥ 30mm

---

## API Configuration (optional — user must set explicitly)

Cloud preview is **off by default** (`apiEndpoint` is empty). To enable the one-click preview link, the **user** must set the preview endpoint in the skill config (no API key required for preview):

1. Set `config.apiEndpoint` to the LabelMake Pro **preview** API URL, e.g. `https://labelmakepro.com/api/v1/oc/preview`
2. Only then will the skill POST the generated LMP to that endpoint and return an `openUrl`. If not set, no HTTP request is made and only the local file is produced.

---

## Full API Request Body Example (60×40mm product label)

Complete HTTP request body for the preview API (note: LMP data is wrapped inside `lmpData`; no API key header):

```json
{
  "lmpData": {
    "lmp": {
      "version": "1.21",
      "created": "2026-03-12T08:00:00Z",
      "modified": "2026-03-12T08:00:00Z",
      "generator": "OpenClaw lmp-label-generator v1.5.4"
    },
    "metadata": {
      "name": "Smart Label Printer",
      "description": "60x40mm product label",
      "author": "OpenClaw",
      "tags": ["product", "consumer"]
    },
    "canvas": {
      "width": 60,
      "height": 40,
      "unit": "mm",
      "dpi": 300,
      "backgroundColor": "#ffffff",
      "gridSize": 1,
      "showGrid": false
    },
    "elements": [
      {
        "id": "rect-001",
        "type": "rectangle",
        "name": "Header Block",
        "position": { "x": 0, "y": 0, "unit": "mm" },
        "size": { "width": 60, "height": 8 },
        "layer": 0,
        "locked": false,
        "visible": true,
        "style": { "fill": "#2563EB", "stroke": "", "strokeWidth": 0, "cornerRadius": 0, "opacity": 1 }
      },
      {
        "id": "text-001",
        "type": "text",
        "name": "Brand Name",
        "position": { "x": 2, "y": 0.5, "unit": "mm" },
        "size": { "width": 40, "height": 7 },
        "layer": 1,
        "locked": false,
        "visible": true,
        "content": "TechBrand",
        "style": { "fontFamily": "Arial", "fontSize": 14, "fontWeight": "bold", "fontStyle": "normal", "color": "#ffffff", "align": "left", "verticalAlign": "middle" }
      },
      {
        "id": "text-002",
        "type": "text",
        "name": "Product Name",
        "position": { "x": 2, "y": 9, "unit": "mm" },
        "size": { "width": 56, "height": 7 },
        "layer": 1,
        "locked": false,
        "visible": true,
        "content": "Smart Label Printer",
        "style": { "fontFamily": "Arial", "fontSize": 14, "fontWeight": "bold", "fontStyle": "normal", "color": "#1a1a1a", "align": "left", "verticalAlign": "middle" }
      },
      {
        "id": "text-003",
        "type": "text",
        "name": "Price",
        "position": { "x": 2, "y": 16, "unit": "mm" },
        "size": { "width": 56, "height": 6 },
        "layer": 1,
        "locked": false,
        "visible": true,
        "content": "$49.99",
        "style": { "fontFamily": "Arial", "fontSize": 14, "fontWeight": "bold", "fontStyle": "normal", "color": "#DC2626", "align": "left", "verticalAlign": "middle" }
      },
      {
        "id": "line-001",
        "type": "line",
        "name": "Divider",
        "position": { "x": 2, "y": 22, "unit": "mm" },
        "size": { "width": 56, "height": 0 },
        "layer": 1,
        "locked": false,
        "visible": true,
        "style": { "stroke": "#e2e8f0", "strokeWidth": 0.3, "strokeDasharray": "" }
      },
      {
        "id": "barcode-001",
        "type": "barcode",
        "name": "EAN-13 Barcode",
        "position": { "x": 5, "y": 23, "unit": "mm" },
        "size": { "width": 50, "height": 15 },
        "layer": 2,
        "locked": false,
        "visible": true,
        "barcode": { "type": "EAN13", "content": "6901234567890", "displayText": true, "textPosition": "bottom", "textSize": 14, "foregroundColor": "#000000", "backgroundColor": "#ffffff" }
      }
    ],
    "variables": []
  },
  "options": {
    "autoOpen": true,
    "labelName": "Smart Label Printer"
  }
}
```

> **Key rules:**
> - `canvas.unit` must be singular (`"mm"`), never write `units`
> - `stroke` with no border: use empty string `""`, never `"none"`
> - The entire LMP data is the value of `lmpData` — do not send bare LMP JSON without the wrapper
