# FileBrowser API 参考

与 SKILL.md 配套的 API 说明，便于通过 API 操作 FileBrowser。

**安全**：账号密码、Token 仅通过环境变量或本地配置传递，不要写入代码或提交到版本库。**禁止上传** `kam-filebrowser-operator/config.json` 及 `.env` 到 FileBrowser 或任何远程。

## 认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/login` | Body: `{"username","password","recaptcha"}`，返回含 `token` 的 JSON。后续请求 Header: `X-Auth: <token>` |

## 资源（文件/目录）

| 方法 | 路径 / 用法 | 说明 |
|------|-------------|------|
| GET | `/api/resources?path=<路径>` | 列出该路径下文件与目录，`path` 默认 `/` |
| POST | `/api/resources/<路径>?override=true` | 上传文件。路径末尾加 `/` 且空 Body 表示创建目录：`/api/resources/<目录名>/?override=false` |
| GET | `/api/raw/<路径>` | 获取文件原始内容（下载） |
| DELETE | `/api/resources/<路径>` | 删除文件或目录 |
| PATCH | `/api/resources/<路径>` | 重命名等，Body 按实际 API 约定（通常不支持路径中含 `/` 的“移动到新路径”） |

**移动文件**（到新路径）：无单次“移动”接口时，可用：`GET /api/raw/<原路径>` 下载 → `POST /api/resources/<新路径>?override=true` 上传 → `DELETE /api/resources/<原路径>` 删除。

路径均为相对 FileBrowser 根目录。**本 skill 仅允许在 config 中 `scope` 所指定的目录下操作**，所有 `path` 须落在 `scope` 之内。

**查找目录与遍历文件名**：`GET /api/resources?path=<路径>` 返回 `items[]`，每项含 `name`、`isDir`、`path`。`isDir === true` 为子目录，`false` 为文件。遍历时对每个子目录再请求 `path=<当前路径>/<子项.name>`，递归即可得到该目录树下所有文件名（收集 `isDir === false` 的 `name` 或完整相对路径）。

## 用户管理（需管理员 token）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/users` | 用户列表 |
| POST | `/api/users` | 新建用户，Body 含 `username`、`password`（≥12 位）、`perm` 等 |
| PATCH | `/api/users/<id>` | 更新用户 |
| DELETE | `/api/users/<id>` | 删除用户 |

## 分享

| 方法 | 路径 / 用法 | 说明 |
|------|-------------|------|
| POST | `/api/share/<文件路径>` | 创建分享（**单数 share，路径在 URL 中**）。Body 空 `{}` 或 `{"expires":"3600","unit":"seconds"}`。响应含 `hash` |
| GET | `/share/<hash>` | 分享页（无需登录），用户在浏览器中打开即可下载 |
| GET | `/api/public/dl/<hash>` | 直接下载文件流（无需登录） |
| DELETE | `/api/share/<hash>` | 删除分享 |

> **注意**：端点是 `/api/share/`（单数），不是 `/api/shares`（复数）。复数端点会导致 `path` 被错误存储为 `"s"`，生成的链接无效。验证时用 GET（不要用 HEAD/`curl -I`，该端点不支持 HEAD）。

## 按订单类型整理

- 触发：用户说「对采购单进行整理」等。在 scope 内搜索/遍历名称含该类型（如「采购单」）的文件。
- 目标结构：`<类型>/<年份 YYYY>/<月份 MM>/`，例如 `采购单/2026/03/`。
- 年月解析：优先从文件名中的 `YYYYMMDD` 或 `YYYYMM` 取年月；否则用资源 `modified`。无法解析则视为无法整理并说明原因。
- 移动：下载 → 上传到 `类型/YYYY/MM/原文件名` → 删除原文件。无法移动的列出并说明原因（无法解析年月、目标已存在、接口报错等）。

## 其他常用

- **设置**：`GET/PATCH /api/settings`
- **搜索**：`/api/search?path=&query=`
- **Swagger**：部署内访问 `http://<base>/swagger/` 可查看完整 API（需 API 权限）

实际请求/响应格式以当前运行版本及 Swagger 为准。
