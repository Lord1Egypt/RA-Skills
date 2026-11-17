# 部署单文件 HTML 到静态托管

> ⚠️ 本文件**仅在用户明确确认要发布后**才执行（对应 SKILL.md 工作流第 7 步）。默认只生成本地预览（用 `present_files` 打开），**不主动推送任何远端**。只有在用户说"要发布 / 要个链接"时才进入下面的流程，且覆盖远端文件前必须再次确认。

本文说明如何把 PRD 原型（单文件 HTML）发布为可访问的静态站点，并规避常见的"线上某页不显示 / 缓存不刷新"问题。文中命令、工具名为英文专有名词（如 GitHub Pages、Jekyll、`gh api`、`curl`），其余说明统一用中文。

## 一、仓库准备（GitHub Pages）

- 仓库根目录放 `index.html`（单文件自包含，图片 base64 内嵌，无外部依赖）。
- **必须**在仓库根放一个空的 `.nojekyll` 文件。GitHub Pages 默认用 Jekyll 处理，可能改写 / 吞掉含特定字符的内容，导致"后台管理页展示不出来"等诡异问题；`.nojekyll` 禁用 Jekyll。提交它会触发 Pages 重建。
- 开启 Pages：仓库 Settings → Pages → Source 选 `main` 分支根目录。

## 二、更新文件（gh CLI / GitHub 内容接口）

单次更新用 `gh api` 的 PUT 请求 `repos/<owner>/<repo>/contents/index.html`，需要：

- `content`：文件 base64 编码
- `sha`：**每次先 GET** 拿到远程当前 blob 的 SHA 值（SHA 会随每次提交变化，不要硬编码旧值）
- `message`：提交信息

Python 流程：

1. `gh api repos/<o>/<r>/contents/index.html` → 取 `sha` 与 `content`
2. 用本地最新文件内容覆盖
3. 在 `</head>` 前注入 `<!-- deploy-cache-bust:YYYY-MM-DDTHH:MM:SS -->` 注释（时间戳每次不同 → 内容变 → ETag 变）
4. base64 编码 → PUT

## 三、cache-bust 为什么必要（关键）

- 仅"重新部署"若文件**内容字节完全相同**，GitHub Pages 的 ETag 不变。浏览器硬刷新时发条件请求拿到 `304`，继续用旧的（可能是损坏前）缓存——这就是"硬刷新也打不开"的根因。
- 改变文件内容（哪怕只改一个注释时间戳）→ ETag 变化 → 浏览器条件请求拿到 `200` 新内容。
- 因此**每次部署都注入新时间戳**是最可靠的缓存失效手段。

## 四、验证线上已生效

轮询直到满足其一：

- `curl -sI <url>` 的 `etag` 变化，或
- `curl -s <url> | grep deploy-cache-bust` 的时间戳为新值

GitHub Pages 重建通常 1–3 分钟。轮询脚本注意 HTTP 响应头行尾 `\r` 会干扰字符串比较，用 `tr -d '\r'` 处理。示例：

```bash
OLD_TS='deploy-cache-bust:2026-07-21T14:15:04'
for i in $(seq 1 24); do
  ts=$(curl -s "<url>" 2>/dev/null | grep -o "deploy-cache-bust:[^\"]*" | tr -d '\r' | head -1)
  if [ "$ts" != "$OLD_TS" ] && [ -n "$ts" ]; then echo "✅ 已生效 ($i)"; break; fi
  sleep 15
done
```

## 五、用户侧兜底清缓存

若仍异常，让用户访问 `chrome://settings/clearBrowserData` → 时间范围"所有时间" → 仅勾"缓存的图片和文件" → 清除数据，再重开站点。

## 六、实机验证（发布前）

- 用 Playwright-core + 系统 Chrome（`executablePath: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome`）渲染，检查无 JS 错误（`pageerror` / `console error`）。
- div 平衡校验：标准 HTML 解析器统计未闭合 / 额外闭合标签应为 0。
- 切换每个 tab / 页面，验证连接线点位、圆角、数据联动正确。

## 七、操作前必须确认（重要）

**执行部署前，必须明确告知用户："此操作会覆盖仓库远端的 `index.html`（以及触发 Pages 重建），是否继续？" 在用户确认前不要执行任何写入远端的命令。**

覆盖是破坏性操作，一旦推错内容可能影响线上正在评审的链接，务必先确认。

## 八、国内访问替代方案

GitHub Pages 在部分地区访问不稳定。若用户主要在境内访问，优先选择以下之一：

- **Gitee Pages**：与 GitHub Pages 类似的静态托管，推送仓库后开启 Pages 服务即可生成境内可访问链接。流程与本文一致（同样需要 `.nojekyll` 与 cache-bust）。
- **腾讯云静态网站托管 / CloudBase**：把 `index.html` 上传到对象存储或静态托管，生成国内 CDN 链接，访问稳定、速度快。
- **WorkBuddy CloudStudio 部署**：使用 `workbuddy_cloudstudio_deploy` 工具直接把本地目录发布为沙箱站点，适合快速分享评审，无需自建仓库。

选择哪种方式取决于用户是否有对应平台的账号与仓库权限；无明确偏好时默认 GitHub Pages。
