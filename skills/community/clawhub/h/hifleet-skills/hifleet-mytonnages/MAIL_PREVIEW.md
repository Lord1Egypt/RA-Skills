# 原始邮件预览（路由 A）

用户在前端点击 **「查看原邮件」** 时，有两种方式：

| 方式 | 字段 | 说明 |
|------|------|------|
| **A. 系统内预览**（推荐） | `preview_url` | 本地 HTTP 服务渲染 HTML，不依赖网页邮箱 |
| **B. 网页邮箱定位** | `webmail_url` | 在浏览器打开邮箱网页搜索深链，利用已登录会话定位原信 |
| **C. 邮件回复** | `reply_url` / `webmail_url` | 优先网页邮箱内回复；备选 SMTP（见 **`MAIL_REPLY.md`**） |

## 架构（方式 A）

```text
定时同步 mail_parse_loop
  → IMAP FETCH RFC822
  → mail_archive/{token}.eml + mail_index 表

前端按钮 preview_url
  → mail_preview_server HTTP
  → 优先读本地 .eml，缺失则 IMAP 按 Message-ID/UID 拉取
  → HTML 预览（正文 + 附件下载）
```

## 架构（方式 B）

```text
检索结果含 from_addr / subject / email_date_utc / message_id
  → webmail_locate 根据 imap_host 识别厂商（Gmail / Outlook / 163 / QQ …）
  → 按厂商能力生成多档搜索条件（由严到宽）
  → webmail_url = 第 0 档（最精确）；webmail_search_tiers = 全部档位
  → 浏览器打开；若搜不到，用户点下一档「放宽搜索」链接
```

### 搜索降级策略

各厂商语法不同，**不能**假定「发件人+主题+时间+Message-ID」同时有效：

| 厂商类型 | 代表 | 首选 | 搜不到时逐级放宽 |
|----------|------|------|------------------|
| 高级运算符 | Gmail、Outlook、Yahoo | Gmail 用 `rfc822msgid:` | 去掉日期 → 去掉发件人 → 仅主题 |
| 关键词搜索 | 163、QQ、阿里邮、企业邮 | **仅主题**（命中率最高） | 缩短主题 → 发件人邮箱 → 日期 |

返回 JSON 字段：

- `webmail_url`：默认打开第 0 档  
- `webmail_search_tiers[]`：`{level, query, method, label, url}` 全部档位  
- `webmail_fallback_count`：备用档位数  

CLI 指定档位：`--tier 2`（0=最精确，数字越大条件越少）。

**不能做的事**（技术限制）：

- 无法在服务端替用户自动输入密码登录网页邮箱。
- 无法用 Message-ID 生成各厂商「直达单封邮件」的通用 URL（仅 Gmail 的 `rfc822msgid` 较可靠）。
- 桌面客户端（Outlook/Thunderbird）无跨平台稳定深链，本方案以**网页邮箱**为主。

脚本：`python scripts/webmail_locate.py --message-id "<id>" --from-addr "..." --open`

## 1. 启动预览服务

与智能体同机部署（需能读 `config.json` 与 `mail_archive/`）：

```bash
cd hifleet-skills/hifleet-mytonnages
python scripts/mail_preview_server.py
# 或指定监听
python scripts/mail_preview_server.py --host 0.0.0.0 --port 8765
```

健康检查：`GET http://localhost:8765/health`

## 2. config.json

```json
{
  "imap_host": "imap.example.com",
  "imap_port": 993,
  "email": "user@example.com",
  "email_password": "app-password",
  "imap_mailbox": "INBOX",
  "mail_preview_host": "0.0.0.0",
  "mail_preview_port": 8765,
  "mail_preview_base_url": "http://your-server:8765",
  "mail_preview_token": "optional-shared-secret"
}
```

| 配置 | 说明 |
|------|------|
| `mail_preview_base_url` | 写入 `preview_url` 的公网/内网根地址（**前端按钮用此**） |
| `mail_preview_token` | 可选；设置后请求须带 `?auth=` 或头 `X-HIFLEET-Preview-Token` |

环境变量：`HIFLEET_MAIL_PREVIEW_HOST` / `PORT` / `BASE_URL` / `TOKEN`

## 3. 前端集成

### 方式 A：系统内预览（推荐）

`search` / `query-by-port` JSON 每行含 **`preview_url`**（及可选 **`webmail_url`**）：

```bash
python scripts/charter_facts_tool.py search "bulk carrier"
```

```json
{
  "message_id": "<abc@mail.example>",
  "subject": "OPEN TONNAGE",
  "from_addr": "broker@example.com",
  "email_date_utc": "2025-05-20T08:00:00Z",
  "preview_url": "http://your-server:8765/mail/preview/a1b2c3...",
  "webmail_url": "https://mail.google.com/mail/u/0/#search/rfc822msgid%3A%3Cabc%40mail.example%3E",
  "webmail_provider": "gmail",
  "webmail_method": "rfc822msgid",
  "webmail_hint": "将在浏览器打开 Gmail 并按 Message-ID 搜索...",
  "webmail_fallback_count": 3,
  "webmail_search_tiers": [
    {"level": 0, "method": "rfc822msgid", "label": "Message-ID（最精确）", "query": "...", "url": "..."},
    {"level": 1, "method": "composite", "label": "发件人 + 主题", "query": "...", "url": "..."}
  ]
}
```

前端可在主按钮旁增加「搜不到？放宽搜索」下拉，遍历 `webmail_search_tiers[1:]`。

按钮示例：

```html
<a href="{{ preview_url }}" target="_blank" rel="noopener noreferrer">
  查看原邮件（系统内）
</a>
<a href="{{ webmail_url }}" target="_blank" rel="noopener noreferrer"
   title="{{ webmail_hint }}">
  在网页邮箱中打开
</a>
```

### 方式 B：网页邮箱定位

```bash
python scripts/charter_facts_tool.py webmail-url \
  --message-id "<abc@mail.example>" \
  --from-addr "broker@example.com" \
  --subject "OPEN TONNAGE" \
  --email-date-utc "2025-05-20T08:00:00Z" \
  --open
```

`--open` 会用系统默认浏览器打开 `webmail_url`（须该浏览器已登录对应邮箱）。

### 方式 C：按 Message-ID 换 URL

```http
GET /api/mail/preview-url?message_id=%3Cabc%40mail.example%3E
```

响应：

```json
{
  "ok": true,
  "message_id": "<abc@mail.example>",
  "preview_token": "a1b2c3...",
  "preview_url": "http://your-server:8765/mail/preview/a1b2c3..."
}
```

CLI：

```bash
python scripts/charter_facts_tool.py preview-url --message-id "<abc@mail.example>"
```

## 4. HTTP 路由

| 路径 | 说明 |
|------|------|
| `GET /mail/preview/{token}` | **预览页**（前端按钮跳转目标） |
| `GET /mail/attachment/{token}/{index}` | 附件下载 |
| `GET /api/mail/preview-url?message_id=` | 生成 preview_url（可附带 from/subject/date 以生成 webmail_url） |
| `GET /api/mail/webmail-url?message_id=&from_addr=&subject=&email_date_utc=` | 仅生成网页邮箱定位链接 |
| `GET /api/mail/raw/{token}` | JSON 元数据+正文（供自定义 UI） |
| `GET /health` | 存活探测 |

`{token}` = `sha256(message_id)[:32]`（与 `preview_url` 路径一致）

## 5. 数据存储

| 位置 | 内容 |
|------|------|
| `mail_archive/*.eml` | 完整 RFC822 |
| SQLite `mail_index` | message_id、preview_token、imap_uid、archive_path |
| `cargo_plate` / `openvessel_plate` | 仅解析字段（**不含**正文） |

历史邮件若尚无 `.eml`，首次打开预览时会 **IMAP 按需拉取** 并写入归档。

## 6. Agent 规则

- 展示船盘/货盘列表时，若有 `preview_url`，向用户提供 **「查看原邮件」** 可点击链接。
- 若用户更习惯在 **自己的邮箱网页** 里看原文，且结果含 `webmail_url`，可提供 **「在网页邮箱中打开」**；说明须浏览器已登录。
- 对用户话术见 **`USER_WORDING.md`**（不说 IMAP/RFC822）。
- 预览服务须已启动；否则提示管理员运行 `mail_preview_server.py`。

## 7. 限制

- 邮件已删或移出 `imap_mailbox` 且本地无 `.eml` → 方式 A 404；方式 B 仍可在网页邮箱中搜到（若未删）。
- 无 `Message-ID` 的邮件（`generated-@local`）方式 A 可能无法 IMAP 搜索；方式 B 退化为发件人+主题+时间组合搜索。
- HTML 正文经简单消毒；复杂邮件版式可能略有差异。
- 方式 B 依赖各厂商搜索 URL 稳定性；163/QQ 等可能需用户多点一次打开邮件。
