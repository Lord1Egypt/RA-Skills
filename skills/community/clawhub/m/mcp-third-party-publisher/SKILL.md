---
name: mcp-third-party-publisher
description: Use when publishing or submitting an MCP server to third-party MCP directories and marketplaces including Glama, mcp.so, Smithery, and MCP Market, especially when Codex must use Computer Use, Browser, or Chrome to open websites, fill submission forms, verify listing pages, and stop before final external submission.
---

# MCP 三方平台发布 Skill

## 核心流程

使用该 Skill 时，先读取发布工具生成的 `skill_inputs`：

- `platform`：目标平台，取值 `glama`、`mcp.so`、`smithery`、`mcp-market`。
- `server`：标准化 MCP 元数据，包含 `id`、`name`、`description`、`repo_url`、`license`、`transport`、`install_config` 等。
- `payload`：平台提交材料。
- `form`：需要填写到网页表单的字段。
- `public_url`：预期上架后的公开访问链接。

执行顺序：

1. 打开目标平台入口。
2. 按平台章节填写或验证页面。
3. 上传、提交、登录、付费、验证码、最终 Submit 之前必须 `stop_before_submit`，向用户确认。
4. 用户确认后才可点击最终提交。
5. 提交后打开或记录 `public_url`，无法访问时记录为待审核而不是失败。

## Computer Use 规则

- 默认优先使用 Chrome 打开三方平台页面；只有用户明确要求应用内 Browser/Computer Use 时才切换。
- 每次打开、点击、填写后读取页面可见状态，确认页面确实进入下一步。
- 表单字段名不完全匹配时，使用语义匹配：例如 `URL`、`Repository`、`GitHub URL` 都可对应 `repo_url`。
- 不要绕过登录、验证码、付费墙、风控或审核流程。
- 任何会向三方平台发送数据的最终提交动作，都必须先停下并说明将提交的平台、账号页面和字段。
- 如果页面结构变化，使用页面可见文本和表单 label 重新定位，不要盲点。

## Glama

平台入口：

- 目录首页：`https://glama.ai/mcp`
- 预期公开链接：`https://glama.ai/mcp/servers/{owner}/{server_id}`

操作方案：

1. 打开 `https://glama.ai/mcp`。
2. 搜索 MCP 名称、仓库名或 owner，确认是否已被索引。
3. 如果已存在，打开 `public_url` 并记录为已可访问。
4. 如果不存在，确认仓库内是否已有 `glama.json`。发布工具的 `payload["glama.json"]` 是建议内容。
5. Glama 通常以 GitHub 仓库和 `glama.json` 索引为主；如果页面提供提交入口，填写 `repo_url` 并提交前 `stop_before_submit`。

字段映射：

- Repository/GitHub URL：`server.repo_url`
- Name：`server.name`
- Description：`server.description`
- Config：`payload["glama.json"]`

## mcp.so

平台入口：

- 提交页：`https://mcp.so/submit`
- 预期公开链接：`https://mcp.so/server/{server_id}/{owner}`

操作方案：

1. 打开 `https://mcp.so/submit`。
2. 选择 Type 为 `Server`。
3. 填写 `form` 中字段：
   - `Type`
   - `Name`
   - `URL`
   - `Server Config`
   - `Description`
4. 如果页面要求登录、验证码或最终提交，执行 `stop_before_submit`。
5. 提交后记录页面提示；若进入审核流程，状态保持 `needs_human`。

字段映射：

- Type：`form["Type"]`
- Name：`form["Name"]`
- URL：`form["URL"]`
- Server Config：`form["Server Config"]`
- Description：`form["Description"]`

## Smithery

### PatSnap GitHub MCP Selection Gate

When publishing from `https://github.com/patsnap/mcp`, Do not use the root repository name `mcp` as the Smithery Server ID.

Before filling Smithery:

1. Run `python -m mcp_publisher github-mcp-cache --cache-dir .cache`.
2. Read `.cache/patsnap-mcp-github-main.md` and show the cached MCP list to the human.
3. Confirm `.cache/patsnap-mcp-github-main.json` was written and contains the same entry set.
4. Ask the human to select the exact GitHub MCP directory name, for example `patsnap-advanced-patent-search`.
5. Use that exact directory name for `Server ID*`.
6. Use the selected entry's `mcp_server_url` for `MCP Server URL*`.
7. If the selected entry has no `mcp_server_url`, stop and ask the human for the real Streamable HTTP MCP endpoint.
8. Stop before clicking `Continue`.

Server ID* must be the exact GitHub MCP directory name. Do not shorten `patsnap-advanced-patent-search` to `advanced-patent-search`.

### PatSnap Smithery Ordered Upload And Cache Update

When the human asks to upload PatSnap MCPs to Smithery in order:

1. Use `.cache/patsnap-mcp-github-main.json` as the ordered source list.
2. Treat `patsnap-advanced-patent-search` and `patsnap-deep-patent-mining` as already uploaded when the human explicitly says they are successful.
3. Store platform status in this exact shape:

```json
"platform": {"smithery": {"success": true, "public_url": "https://smithery.ai/servers/openpatsnap/<server_id>", "updated_at": "<iso timestamp>"}}
```

4. For failures, use the same shape with `success: false`, empty `public_url`, `updated_at`, and a `reason` field.
5. For each MCP, open `https://smithery.ai/servers/new`, fill:
   - `Server ID*`: exact GitHub directory name, for example `patsnap-advanced-patent-search`
   - `MCP Server URL*`: the selected entry's Streamable HTTP endpoint without the `?apikey=YOUR_API_KEY` placeholder when uploading without credentials
6. If Smithery shows `Configure connection settings` and the human requested no credentials, click `Skip`.
7. After creation or when the server already exists, open `https://smithery.ai/servers/openpatsnap/<server_id>/settings`.
8. Fill and save these Settings fields from the cache:
   - `Description`: `entry.description`
   - `Homepage`: `entry.homepage`
   - `GitHub Repository`: `https://github.com/patsnap/mcp`
9. Click `Save Settings`.
10. Only after Settings are saved or already match, update `.cache/patsnap-mcp-github-main.json` with `platform.smithery.success = true`.
11. After every successful upload/cache update, sleep 5 seconds before starting the next MCP.
12. If any upload or Settings save fails, update the cache with `success: false` and `reason`, then stop immediately. Do not continue to later MCPs.
13. If the human says to resume failed uploads, start from the first cache entry where `platform.smithery.success` is `false`.

平台入口：

- 首页：`https://smithery.ai/`
- 发布页：`https://smithery.ai/servers/new`
- 预期公开链接：`https://smithery.ai/servers/{owner}/{server_id}`
- 旧格式可能重定向：`https://smithery.ai/server/{owner}/{server_id}`
- openpatsnap 默认 namespace：`openpatsnap`
- openpatsnap 默认账号：`openpatsnap@gmail.com`

操作方案：

1. 打开 `https://smithery.ai/`。
2. 搜索 MCP 名称、owner 或仓库 URL，确认是否已经存在。
3. 如果已存在，打开 `public_url` 并记录为已可访问。
4. 如果需要发布，优先使用 `payload["commands"]` 中的 Smithery CLI 命令；网页只用于登录、验证和确认结果。
5. 如果用户要求网页发布，默认用 Chrome 打开 `https://smithery.ai/servers/new`，确认页面标题为 `Publish an MCP Server`，并确认已登录账号。
6. 在发布页填写：
   - `Server ID*`：使用短横线 slug，例如 `patsnap-pharma-intelligence`。
   - `MCP Server URL*`：优先使用真实 Streamable HTTP MCP endpoint；如果用户明确给出 Marketplace 页面 URL，也按用户输入填写，但说明可能只是 HTML 页面。
7. 点击 `Continue` 前执行 `stop_before_submit`；用户确认后才点击。
8. 如果进入 `Configure connection settings` 页面：
   - 有 API key、token、headers 等用户连接参数时，先 `Add Parameter` 并确认字段。
   - 用户明确要求 `Skip` 时，点击 `Skip` 继续。
9. 发布后打开或记录 `https://smithery.ai/servers/{owner}/{server_id}`。如果页面显示 `This server is unlisted and won't appear in search results`，状态记录为 `submitted` 或 `needs_human`，并提示可在 Settings/verification 中处理公开可见性。
10. 在 Releases 日志中检查能力发现结果：
    - `WORKING` 表示 release 已创建，不等于 MCP 能力一定可用。
    - 如果日志出现 `Unexpected content type: text/html`、`No capabilities found`、`Failed to list tools/resources/prompts/triggers`，说明填写的是网页 URL 或非 MCP HTTP 响应；记录公开链接，同时提示后续应改成真实 Streamable HTTP MCP endpoint。

字段映射：

- Repository：`server.repo_url`
- Name：`server.name`
- Description：`server.description`
- Server Card：`payload["server_card"]`
- CLI：`payload["commands"]`
- Server ID：`form["Server ID"]` 或 slug 化后的 `server.id`
- MCP Server URL：`form["MCP Server URL"]` 或用户明确提供的 URL

## MCP Market

平台入口：

- 提交页：`https://mcpmarket.com/submit`
- 预期公开链接：`https://mcpmarket.com/server/{server_id}`
- 默认邮箱：`openpatsnap@gmail.com`
- 默认上架方式：使用页面推荐的 `Get Listed Now` / `RECOMMENDED` / `$29` / `OFFICIAL` 方案。

操作方案：

1. 打开 `https://mcpmarket.com/submit`。
2. 填写 GitHub 仓库 URL。页面字段通常显示为 `https://github.com/username/mcp-server`，对应 `form["Repository URL"]` 或 `server.repo_url`。
3. 填写邮箱 `openpatsnap@gmail.com`，除非用户在本次请求中明确给出其他邮箱。
4. 上架方式默认选择页面标记为 `RECOMMENDED` 的 `Get Listed Now` 方案，通常显示为 `$29`、`OFFICIAL`、Listed within 24 hours。
5. 如果页面提供 Try Now link 且没有用户明确给出链接，保持为空。
6. 点击最终 `Get listed now` 前执行 `stop_before_submit`，明确说明将提交 GitHub 仓库、邮箱和推荐付费/官方上架方案。
7. 用户确认后才可点击最终按钮。
8. 提交后记录审核状态；未立即公开时保持 `needs_human`。

字段映射：

- Repository URL：`form["Repository URL"]`
- Name：`form["Name"]`
- Description：`form["Description"]`
- Category：`form["Category"]`
- License：`form["License"]`
- Email：`openpatsnap@gmail.com`
- Listing mode：`Get Listed Now` / `RECOMMENDED` / `$29` / `OFFICIAL`

## 结果回填

完成操作后返回：

- `platform`
- `status`：`listed`、`submitted`、`needs_human` 或 `failed`
- `public_url`
- 页面提示、审核信息或失败原因

如果只是完成表单填写但未得到用户最终提交确认，状态必须保持 `needs_human`。
