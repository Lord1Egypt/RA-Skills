# Onboarding · 首次使用环境配置

本技能**默认即可用**：只要运行环境能把生成的单文件 HTML 写到本地目录，就能产出"文字 PRD + 可交互原型"。下面的发布与验证为**可选增强**，按需安装。

## 必需（默认即可用）
- 一个能写入本地文件的 Agent 运行环境（WorkBuddy / 其他支持 Agent Skills 的客户端 等）。技能会生成单文件 HTML 到本地目录。
- 浏览器：用于本地预览（用 `present_files` 打开，或直接双击生成的 `index.html`）。

## 可选：发布到静态托管（参见 references/deploy-github-pages.md）
- **`gh` CLI（静态托管命令行工具）**：
  - macOS：`brew install gh`
  - Linux：`apt install gh`（随官方文档安装）
  - Windows：随官方渠道安装 `gh`
- 登录：`gh auth login`，并确保对目标仓库有写权限。
- 发布流程见 `references/deploy-github-pages.md`（含 `.nojekyll`、cache-bust、`gh api` 更新、操作前确认）。

## 可选：实机验证（发布前推荐）
- **Playwright**（含系统 Chrome）：
  - `npm i -D playwright` 或 `pip install playwright`
  - 安装浏览器：`playwright install chromium`
- 用于确认原型无 JS 错误、布局 / 连接线 / 数据联动正确；不影响生成，仅提升发布质量。

## 可选：国内静态托管替代
- **Gitee Pages** / **腾讯云静态网站（CloudBase）** / **WorkBuddy CloudStudio 部署**。
- 详见 `references/deploy-github-pages.md` 第八节。

## 完成配置
- 仅生成本地预览：无需任何额外安装，开箱即用。
- 要发布 / 要验证：按上面安装对应工具后正常使用。
