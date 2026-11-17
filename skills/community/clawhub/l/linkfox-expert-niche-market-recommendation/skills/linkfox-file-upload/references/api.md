# 文件上传底层说明

本 skill 不直接调业务网关端点，而是复用同目录 `scripts/linkfox_paths.py` 的两个函数。

## get_sts_voucher()

- 调 `POST {LINKFOX_TOOL_GATEWAY}/oss/getStsVoucherByAPI`（缺省 `https://tool-gateway.linkfox.com`），`Authorization` 头取 `LINKFOX_AGENT_API_KEY`。
- 返回临时上传凭证（accessKeyId / accessKeySecret / securityToken / expiration）+ OSS 信息（endpoint / bucketName / dir / region）+ 约束（supportedTypes / maxFileSize / maxFileCount）。
- 最多重试 3 次、指数退避（1s→2s），仅对 408/429/5xx 重试；errcode≠200 直接抛错。

## upload_file(local_path, *, slug=None, ts=None, voucher=None)

- 用 `oss2` 以 STS 凭证上传到 `{dir}/{YYYY/MM}/{uuid}.{ext}`。
- 上传前校验：文件大小 ≤ `maxFileSize`、扩展名 ∈ `supportedTypes`，超限抛 `RuntimeError`。
- 上传时显式声明 `Content-Type`，文本类一律带 `charset=utf-8`（见下节）。
- 成功后把 URL 登记进会话 `_meta.json` 的 `deliverables`。

### Content-Type 与编码

文本类文件必须带 `charset=utf-8`，否则按 HTTP 规范，解码方在 `text/*` 缺 charset 时会回退到"本地传统编码"——中文 Windows 上按 GBK 解 UTF-8 正文，汉字直接乱码。所以不依赖 oss2 按文件名推断，而是显式给出：

| 扩展名 | 声明的 Content-Type | 为什么不交给 oss2 |
|--------|--------------------|------------------|
| `md`   | `text/markdown; charset=utf-8` | 它给 `text/markdown`，缺 charset |
| `csv`  | `text/csv; charset=utf-8` | 它猜成 `application/vnd.ms-excel`，类型错且缺 charset |
| `json` | `application/json; charset=utf-8` | 缺 charset |
| `webp` | `image/webp` | 它返回 `None`，等于上传后没有 Content-Type |
| `txt` / `html` | `text/plain` / `text/html`，均带 `charset=utf-8` | 缺 charset。但这两种当前**不在** OSS 白名单内，会在上传前就被拒；表里保留是为白名单放开后即时生效 |

未列出的扩展名（`png` / `jpg` / `jpeg` / `pdf` / `mp4` / `xlsx` / `zip`）交给 oss2 推断，它推得对。

**不写 UTF-8 BOM**：BOM 能讨好本地双击打开的 Excel，但会污染文件字节、破坏 md 首行标题解析、也让按 URL 取内容的下游读到 `﻿`。需要 Excel 直接打开的交付走 `.xlsx`，不要用 CSV。

注意 charset 只随 HTTP 响应头走。文件下载到本地后响应头就没了，编辑器仍按自己的默认编码猜——这是本 skill 无法覆盖的边界。

### OSS 凭证约束（实测值）

`get_sts_voucher()` 返回的约束，2026-09-08 实测：

| 约束 | 值 |
|------|-----|
| `supportedTypes` | `xlsx` `csv` `jpg` `jpeg` `webp` `png` `pdf` `zip` `json` `md` `mp4` |
| `maxFileSize` | 52428800（50 MB）|
| `maxFileCount` | 10 |

**白名单里没有 `txt` / `html` / `docx`**——传这些会在上传前被 `upload_file()` 拒掉并返回结构化错误（不是崩栈）。要交付纯文本，改用 `.md`。以上是服务端下发的动态值，可能调整，代码里不要硬编码，以 `voucher` 实际返回为准。

返回：

| 字段 | 含义 |
|------|------|
| `url`  | 可公开访问的 HTTPS URL |
| `path` | OSS 对象键（如 `tmp/2026/06/abc123.png`） |
| `name` | 原始文件名 |
| `size` | 文件大小（字节） |
| `ext`  | 扩展名（不含点） |

## 依赖与环境

- `pip install oss2`
- `LINKFOX_AGENT_API_KEY`（必需）；`LINKFOX_TOOL_GATEWAY`（可选，覆盖 tool-gateway 地址）。
