---
name: indexnow
description: |
  通过 IndexNow 协议向搜索引擎（Bing、Yandex、Naver 等）提交 URL，加速页面收录。使用场景：
  (1) 用户想要提交新页面或更新的页面给搜索引擎
  (2) 用户说"提交收录"、"indexnow"、"提交给 Bing"、"加速收录"
  (3) 用户需要从 sitemap 批量提交所有 URL
  (4) 用户需要生成 IndexNow API key 或部署验证文件
  触发词：indexnow、提交收录、submit url、bing 收录、加速收录、搜索引擎提交、submit to search engine
---

# IndexNow

通过 IndexNow 协议向 Bing、Yandex、Naver、Seznam 等搜索引擎提交 URL，加速页面收录。提交到 `api.indexnow.org` 会自动分发给所有支持的搜索引擎。

## 前置条件

- 网站已部署上线（搜索引擎需要访问验证文件）
- 系统有 `curl`（macOS/Linux 内置）
- 项目有 `public/` 目录

## 工作流程

### Step 1: 检查 API Key

检查项目根目录是否存在 `.indexnow-key` 文件：

- **存在**: 读取 key 值，继续下一步
- **不存在**: 执行脚本生成 key：
  ```bash
  ${CLAUDE_SKILL_ROOT}/scripts/indexnow.sh generate-key
  ```
  脚本会生成随机 key，保存到 `.indexnow-key`，并在 `public/` 目录创建 `{key}.txt` 验证文件。

### Step 2: 确认验证文件

检查 `public/{key}.txt` 是否存在且内容正确。提醒用户：验证文件需要随项目部署后，搜索引擎才能验证 key。

### Step 3: 提交 URL

根据用户需求选择提交方式：

**提交单个或多个 URL:**
```bash
${CLAUDE_SKILL_ROOT}/scripts/indexnow.sh submit https://example.com/page1 https://example.com/page2
```

**从本地 sitemap.xml 提取并提交:**
```bash
${CLAUDE_SKILL_ROOT}/scripts/indexnow.sh submit-sitemap [path]
```
默认读取 `public/sitemap.xml`。

**从远程 sitemap URL 提取并提交:**
```bash
${CLAUDE_SKILL_ROOT}/scripts/indexnow.sh submit-sitemap-url https://example.com/sitemap.xml
```

### Step 4: 验证结果

脚本会输出每个 URL 的提交结果。响应码含义：

| 响应码 | 含义 | 处理方式 |
|--------|------|----------|
| 200 | 提交成功 | 无需操作 |
| 202 | 已接收，待验证 | 确认验证文件已部署 |
| 400 | 格式错误 | 检查 URL 格式 |
| 403 | key 无效 | 重新生成 key 并部署 |
| 422 | URL 不匹配 | 确认 URL 域名正确 |
| 429 | 请求过多 | 等待后重试 |

## 脚本命令参考

脚本位置: `${CLAUDE_SKILL_ROOT}/scripts/indexnow.sh`

| 命令 | 说明 |
|------|------|
| `generate-key` | 生成 API key 和验证文件 |
| `submit <url1> [url2...]` | 提交一个或多个 URL |
| `submit-sitemap [path]` | 从本地 sitemap 提取并提交 |
| `submit-sitemap-url <url>` | 从远程 sitemap 提取并提交 |
| `status` | 显示当前配置状态 |

## 注意事项

- 单次批量提交最多 10,000 个 URL，超过自动分批
- `.indexnow-key` 文件建议加入 `.gitignore`
- `public/{key}.txt` 验证文件需提交到版本控制并部署
- 提交不保证被收录，但会通知搜索引擎尽快爬取

## 更多信息

更多 AI SEO 技能详见：https://domainrank.app/ai-seo-skills
