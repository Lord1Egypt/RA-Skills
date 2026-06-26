---
name: filebrowser-api
description: Operate FileBrowser via REST API—login, list/upload/download resources, manage users. Scan for 采购单 files in scope, prompt user to download by number or all, or provide download/browser link. Organize files by order type (e.g. 采购单) into 类型/年份/月份/ structure; report files that could not be organized and why. Use when automating FileBrowser, calling its API, or integrating with it.
---

# FileBrowser API 操作

通过 REST API 操作 FileBrowser：认证、文件列表/上传/下载、用户管理等。本技能适用于脚本、自动化或与其他系统集成。

## 首次使用：向用户确认配置

在通过本技能调用 FileBrowser API 或生成相关脚本之前，按以下顺序获取 Base URL、用户名、密码：

1. **优先**：若存在 `kam-filebrowser-operator/config.json`，从中读取 `baseUrl`、`username`、`password`、`scope`（该文件已加入 `.gitignore`，勿提交）。
2. **否则**：若项目根目录有 `.env` 或环境变量中有 `FB_BASE_URL`/`FB_USER`/`FB_PASSWORD`，可从中读取。
3. **否则**：**必须先向用户询问**：
   - **Base URL**：例如 `http://127.0.0.1:9888`
   - **用户名**：FileBrowser 登录账号
   - **密码**：至少 12 位

首次使用本 skill 时，可复制 `kam-filebrowser-operator/config.example.json` 为 `kam-filebrowser-operator/config.json` 并填写真实值；务必保证 `config.json` 不被提交到版本库，**且不得上传到 FileBrowser 或任何远程位置**。

## 安全：密码与凭证

- **禁止**在脚本、示例代码或本技能文档中写入真实密码；仅使用占位符（如 `你的密码`、`$FB_PASSWORD`）或从环境变量/配置文件读取。
- **禁止**将包含密码的文件提交到版本库。凭证存放在 `kam-filebrowser-operator/config.json`（已加入 `.gitignore`）或项目根目录 `.env` 中。
- **禁止上传 `kam-filebrowser-operator/config.json`**：该文件含登录凭证，不得通过本 skill、FileBrowser API 或任何方式上传到 FileBrowser 或其它远程；执行上传、同步、备份等操作时须排除该文件。
- **禁止**生成会读取 `.env` 或持久化凭证的上传/登录脚本（例如 `upload-to-filebrowser.sh` 等）。仅提供一次性命令（如 `curl`），由用户在已设置环境变量的终端中执行，或每次由用户临时提供 Base URL、用户名、密码。
- 使用本技能生成或修改脚本时：从环境变量（如 `FB_USER`、`FB_PASSWORD`）或受保护的配置读取账号密码，不要硬编码。
- Token 仅用于请求头，不要写入日志、错误信息或对外暴露。

## 可操作目录（scope）

- 在 `kam-filebrowser-operator/config.json` 中必须配置 **`scope`**，表示本 skill 仅允许在该 FileBrowser 目录下操作（如 `"/Qianlu"`）。
- **所有** 列出、上传、下载、创建目录、删除等操作，路径必须在 `scope` 之下；不得访问或操作 `scope` 以外的路径。
- **若 scope 对应目录不存在**：在执行列表、上传等操作前，应先调用创建目录接口（如 `POST /api/resources/<scope 名>/?override=false`，路径末尾带 `/`，不传 Body）建立该目录，再继续执行用户请求的操作。
- 若用户请求的路径超出 `scope`，须拒绝并说明仅支持在配置的目录内操作；若未配置 `scope`，须提示用户先在 config.json 中设置 `scope` 再执行操作。

## 基础配置

- **凭证来源**：优先使用 `kam-filebrowser-operator/config.json`（字段 `baseUrl`、`username`、`password`、`scope`）；若无则用项目 `.env` 或环境变量；再无则向用户询问。
- **Base URL**：默认 `http://127.0.0.1:9888`。可在 `config.json` 或 `.env` 中配置。
- **scope**：必填。本 skill 仅在此目录下操作，API 请求中的 path 均相对于此目录或填完整路径时也须落在 scope 内。
- **认证**：先调用登录接口获取 token，后续请求在 Header 中携带 `X-Auth: <token>`。

## 1. 登录获取 Token

```http
POST /api/login
Content-Type: application/json

{
  "username": "Username",
  "password": "你的密码",
  "recaptcha": ""
}
```

成功响应体为 JSON，其中包含 `token` 字段。后续所有 API 请求需添加：

```http
X-Auth: <token>
```

## 2. 资源（文件/目录）接口

### 列出目录

```http
GET /api/resources?path=<scope>
GET /api/resources?path=<scope>/子目录
```

Query 参数 `path` 必须在 config 的 **scope** 之下（如 `scope` 为 `/Qianlu` 时，用 `Qianlu` 或 `Qianlu/子目录`；部分环境 `path` 带前导 `/` 如 `/Qianlu`）。响应为 JSON，形如：

```json
{
  "items": [
    { "name": "文件名.txt", "path": "相对路径", "isDir": false, "size": 123, "extension": ".txt" },
    { "name": "子目录", "path": "子目录", "isDir": true, ... }
  ],
  "numDirs": 1,
  "numFiles": 1
}
```

- **查找目录**：`items` 中 `isDir === true` 的项为子目录，`isDir === false` 的为文件。
- **path 用法**：列出某目录时，`path` 为相对于根或 scope 的路径（如 `Qianlu`、`Qianlu/采购单`），下一层子项在 `items[].name` 或 `items[].path` 中。

### 遍历目录并获取文件名称

1. **单层**：`GET /api/resources?path=<目录路径>`，从响应 `items` 中取每项的 `name`（即该层下的文件名与子目录名）。
2. **递归遍历**：
   - 先请求 `path=<scope>` 得到根层 `items`；
   - 对每个 `item`：若 `item.isDir === true`，再请求 `path=<当前路径>/<item.name>`（当前路径首层为 scope 名，如 `Qianlu`），得到该子目录下的 `items`；
   - 重复上述步骤直到没有子目录，或达到所需层级；
   - 收集所有 `isDir === false` 的 `item.name` 即为该目录树下的全部文件名（可同时保留相对路径：当前路径 + `/` + `item.name`）。
3. **路径约定**：`path` 使用与 API 一致的格式（多数为 `scope` 或 `scope/子路径`，无前导 `/`），遍历时用「当前 path + `/` + 子项 name」拼出子路径。

### 上传文件

```http
POST /api/resources/<文件路径>?override=true
X-Auth: <token>
Content-Type: application/octet-stream
# 或具体类型，如 text/plain、application/json

<文件二进制或文本内容作为 Body>
```

- `<文件路径>` 必须在 config 的 **scope** 之下，且**必须带 scope 前缀**才会进入 scope 目录内（如 scope 为 `/Qianlu` 时，用 `Qianlu/文件名`，不要只用 `文件名`，否则会落在根目录）。子路径示例：`Qianlu/doc.txt`、`Qianlu/子目录/file.txt`。
- `override=true` 表示覆盖已存在文件；不传或 `false` 则存在时可能报错。
- Body 为文件原始内容，不要用 multipart/form-data。
- **禁止上传**：`kam-filebrowser-operator/config.json`、`.env` 及任何含凭证的文件不得通过本接口上传。

### 下载 / 原始文件

```http
GET /api/raw/<文件路径>
X-Auth: <token>
```

`<文件路径>` 必须在 **scope** 之下。返回文件原始内容，用于下载或直接读取。

### 采购单扫描与下载流程

在 scope 内**扫描出采购单相关文件**（如通过搜索「采购单」或遍历目录筛选名称）后，按以下步骤与用户交互：

1. **列出清单并编号**  
   将结果整理为带编号的列表，例如：  
   `1. 采购单-RFQ0311.xlsx`、`2. 采购单-XXX.xlsx`  
   或使用文件名、编号等便于区分的标识。

2. **提示是否下载**  
   明确询问用户：**是否需要下载？可回复对应编号（如 1、2）或「全部」**。  
   未选择则视为不需要下载。

3. **执行下载或提供链接**  
   - **能直接提供文件时**：按用户选择的编号或「全部」，用 `GET /api/raw/<路径>` 拉取文件，在对话中提供或说明已准备好（视环境是否支持传输文件）。  
   - **用户要求直接下载链接或无法在对话中提供文件时**：按下方「分享链接（直接下载链接）」流程生成链接；若不可用则用方式二。  
   - **方式二（备用）**：提供 **FileBrowser 内下载说明**：在浏览器打开 baseUrl，登录后进入对应路径（如 `Qianlu/采购单-xxx.xlsx`）即可下载。并提示：可在 FileBrowser Web 界面对该文件点击「分享」自行生成有效链接。  
   - 提供链接时注明：分享链接有效期视服务端配置（expire 为 0 通常表示长期有效），若失效可再次请求生成。

### 分享链接（与网页流程一致）

用于生成**无需登录即可打开分享页并下载**的链接，用户要求「分享链接」时使用。

> **关键：端点是 `/api/share/<文件路径>`（单数 share，路径在 URL），不是 `/api/shares`（复数）。复数端点会导致 path 被存为 `"s"`，生成的链接无效。**

1. **创建分享**

   ```http
   POST /api/share/<scope内文件路径>
   X-Auth: <token>
   Content-Type: application/json

   {}
   ```

   - **文件路径放在 URL 中**，如 `POST /api/share/Qianlu/采购单-RFQ0311.xlsx`（路径须在 scope 内）。
   - Body 为空 JSON `{}`。若需设置**有效期**，Body 传 `{"expires":"<秒数>","unit":"seconds"}`，例如 1 小时：`{"expires":"3600","unit":"seconds"}`。不传则长期有效（expire = 0）。
   - 响应示例：`{"hash":"0wod80NP","path":"/Qianlu/采购单-RFQ0311.xlsx","userID":1,"expire":0}`，取 `hash`。

2. **拼出分享链接**
   - **分享页**（与网页「复制链接」一致）：`baseUrl/share/<hash>`
     - 示例：`http://127.0.0.1:9888/share/0wod80NP`
     - 用户在浏览器中打开即可查看/下载（无需登录）。
   - **直接下载**（同一 hash）：`baseUrl/api/public/dl/<hash>`

3. **验证**
   - 创建后检查响应中的 `path` 是否与请求路径一致（如 `/Qianlu/采购单-RFQ0311.xlsx`）。若 `path` 异常（如 `"s"` 或与请求不符），说明使用了错误端点，须检查 URL 是否为 `/api/share/<路径>`（单数）。
   - 可用 `curl -s -o /dev/null -w "%{http_code}" <baseUrl>/api/public/dl/<hash>` 验证链接是否可下载（应返回 200）。注意：不要用 HEAD（`curl -I`）验证，该端点不支持 HEAD 方法。

4. **删除分享**
   - `DELETE /api/share/<hash>`，Header `X-Auth: <token>`。

### 按订单类型整理（如「对采购单进行整理」）

当用户提出对某类订单文件进行整理（例如「对采购单进行整理」）时，按以下流程执行，并在结束时明确告知：已整理到哪些路径、哪些文件无法整理及原因。

1. **确定订单类型与范围**
   - 从用户表述中识别订单类型名称（如「采购单」），及是否限定扩展名（默认可限定为 `.xlsx` 等常见表格格式，或不做扩展名限制）。
   - 在 **scope** 内通过搜索或递归列出目录，收集**名称包含该类型关键词**且为文件的项（如名称含「采购单」）。只处理 scope 下的文件，不处理已在「类型/年份/月份」子目录下且已按规则命名的文件（可选：避免重复整理）。

2. **解析年月**
   - 对每个文件，尝试解析**年份（YYYY）和月份（MM）**，用于生成目标路径 `类型/YYYY/MM/`（例如 `采购单/2026/03/`）。
   - **优先从文件名解析**：若文件名中存在连续 8 位数字且形如 `YYYYMMDD`（如 `20260312`），取前 4 位为年、第 5–6 位为月；若为 6 位 `YYYYMM`，则取前 4 位为年、后 2 位为月。
   - **若无则用修改时间**：使用该文件在 API 返回的 `modified` 字段（若存在），转换为本地或 UTC 的年份与月份。
   - **若仍无法得到年月**：该文件**不移动**，归入「无法整理」列表，原因写为「无法从文件名或修改时间解析年月」。

3. **创建目录结构**
   - 在 scope 下创建目录：`<类型>/<YYYY>/<MM>/`（如 `Qianlu/采购单/2026/03/`）。对涉及的所有 (YYYY, MM) 组合逐层创建，使用 `POST /api/resources/<目录路径>/?override=false`，路径末尾带 `/`，不传 Body。

4. **移动文件**
   - 目标路径为：`<类型>/<YYYY>/<MM>/<原文件名>`（如 `采购单/2026/03/采购单-xxx-20260312.xlsx`），须在 scope 内。
   - FileBrowser 无「移动到新路径」的单次 API，采用：**GET /api/raw/<原路径>** 下载内容 → **POST /api/resources/<目标路径>?override=true** 上传 → **DELETE /api/resources/<原路径>** 删除原文件。若目标已存在且用户未要求覆盖，可视为「目标已存在，未移动」，归入无法整理并说明原因。
   - 若下载、上传或删除任一步失败：该文件留在原位置，归入「无法整理」列表，原因写为「移动失败」并尽量附带接口返回信息（如权限不足、目标已存在等）。

5. **汇总并提示用户**
   - **已整理**：列出已成功移动到 `类型/年份/月份/` 下的文件及目标路径（如 `采购单/2026/03/采购单-xxx.xlsx`）。
   - **未整理（留在原位置）**：列出每个文件的当前路径（或文件名）及**原因**，例如：
     - 「无法从文件名或修改时间解析年月」
     - 「目标路径已存在，未覆盖」
     - 「移动失败：<简短错误原因>」

6. **约定**
   - 所有路径均在 **scope** 之下；类型子目录（如 `采购单`）建在 scope 根下，即 `scope名/采购单/2026/03/`。
   - 若某文件已位于 `类型/YYYY/MM/` 下且名称符合当前命名规则，可视为已整理，无需再次移动；若用户希望「重新整理」再按上述规则执行并覆盖或跳过由实现决定（建议默认不覆盖已存在目标，并归入无法整理说明原因）。

### 创建目录

```http
POST /api/resources/<目录路径>/?override=false
X-Auth: <token>
```

- **路径末尾必须带 `/`**，否则会创建成空文件而非目录。例如创建目录 `Qianlu` 用 `Qianlu/`，创建 `Qianlu/子目录` 用 `Qianlu/子目录/`。
- 不传 Body 或传空 Body，不要传 `{}`。
- `<目录路径>` 必须在 **scope** 之下。

### 删除

```http
DELETE /api/resources/<路径>
X-Auth: <token>
```

删除文件或目录；路径必须在 **scope** 之下。

## 3. 用户管理（需管理员权限）

- **列出用户**：`GET /api/users`，Header 需带 `X-Auth`。
- **新建用户**：`POST /api/users`，Body 为 JSON，包含 `username`、`password`（至少 12 位）、`perm` 等。
- **更新用户**：`PATCH /api/users/<id>` 或按实际 API 约定。
- **删除用户**：`DELETE /api/users/<id>`。

具体字段以实际 Swagger/文档为准；部署内可访问 `http://<base>/swagger/` 查看（若已开启）。

## 4. 调用示例（curl）

凭证从环境变量读取，**勿在脚本中写明文密码**：

```bash
# 从 .env 或环境变量读取（FB_USER、FB_PASSWORD 勿提交到 Git）
BASE="${FB_BASE_URL:-http://127.0.0.1:9888}"
TOKEN=$(curl -s -X POST "$BASE/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$FB_USER\",\"password\":\"$FB_PASSWORD\",\"recaptcha\":\"\"}" \
  | jq -r '.token')

# 列根目录
curl -s -H "X-Auth: $TOKEN" "$BASE/api/resources?path=/"

# 上传
echo "hello" | curl -s -X POST "$BASE/api/resources/hello.txt?override=true" \
  -H "X-Auth: $TOKEN" -H "Content-Type: text/plain" --data-binary @-

# 下载
curl -s -H "X-Auth: $TOKEN" "$BASE/api/raw/hello.txt"
```

## 5. 错误与注意

- 未带 `X-Auth` 或 token 无效会返回 401。
- 路径不存在或权限不足会返回 4xx，根据响应体调整 path 或权限。
- 密码需至少 12 位（与 Web 端一致）。
- **再次强调**：密码、Token 仅通过环境变量或本地 `.env`（且已加入 .gitignore）传递，不写入代码、不提交、不暴露。

更多接口说明见 [reference.md](reference.md)。
