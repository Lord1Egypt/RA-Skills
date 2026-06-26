---
name: obsidian-quartz-blog-setup
description: >
  从零搭建 Quartz v4 + GitHub Pages 博客，将 Obsidian 知识库发布为静态网站。
  当用户提到"搭建 Quartz 博客"、"Obsidian 发布博客"、"部署 Obsidian 到 GitHub Pages"、
  "quartz setup"、"obsidian quartz blog"、"发布知识库到网站"、"搭建个人博客"、
  "把我的笔记部署到网上"、"obsidian to website"时触发此 skill。
  这是一个首次搭建的工作流——如果用户已经搭建好 Quartz 只是要推送更新，
  应该触发 obsidian-wiki-blog-push 而非本 skill。
---

# Obsidian Quartz Blog Setup

从零搭建 Quartz v4 + GitHub Pages，将 Obsidian 知识库发布为静态博客。

## 工作流总览

```
询问配置信息 → 环境检查 → 安装 Quartz → 初始化 → 同步笔记
→ 本地预览 → 配置 quartz.config.ts → GitHub 仓库指引
→ 绑定远程仓库 → 创建 deploy.yml → 推送到 GitHub
```

## Step 0: 收集配置信息

在开始任何操作之前，一次性询问用户以下所有信息：

1. **Obsidian 知识库路径** — vault 的绝对路径（如 `C:\Users\xxx\my-vault`）
2. **Quartz 项目目录** — 希望在哪里创建 Quartz 博客项目（如 `~/projects/my-blog`）
3. **GitHub 仓库地址** — 完整的远程仓库 URL（如 `https://github.com/username/repo.git`）。如果还没创建，提醒用户先去 GitHub 创建一个**空仓库**（不要添加 README、.gitignore 或 license）
4. **站点标题 (pageTitle)** — 博客的标题，显示在浏览器标签页和网站头部
5. **baseUrl** — GitHub Pages 的访问地址，不带 `https://`：
   - 用户站点：`username.github.io`
   - 项目站点：`username.github.io/repo`

将所有问题放在一条消息中，格式清晰，方便用户一次性回复。

## Step 1: 环境检查

检查以下工具是否可用：

```bash
git --version
node --version
npm --version
```

Quartz v4 需要 Node.js 20 或以上版本。如果版本过低，提示用户升级。

同时确认 Obsidian vault 目录存在：
```bash
ls "<vault-path>"
```

如果有工具缺失，指引用户安装：
- Git: https://git-scm.com/downloads
- Node.js (推荐 LTS): https://nodejs.org/

## Step 2: 安装 Quartz

先检查 Quartz 项目目录是否已存在 `quartz.config.ts`：

```bash
ls "<project-dir>/quartz.config.ts" 2>/dev/null && echo "EXISTS" || echo "NOT_EXISTS"
```

**如果 NOT_EXISTS**（首次安装）：
```bash
git clone https://github.com/jackyzha0/quartz.git "<project-dir>"
cd "<project-dir>"
npm install
```

如果 `npm install` 失败，常见原因：
- Node.js 版本太低（需要 20+）→ 升级 Node.js
- npm 缓存问题 → 执行 `npm cache clean --force` 后重试

**如果 EXISTS**（之前安装过）：
跳过 clone 和 npm install，直接进入 Step 3。输出提示：
> 检测到 Quartz 已安装，跳过安装步骤。

## Step 3: 初始化 Quartz

```bash
cd "<project-dir>"
npx quartz create
```

这是一个交互式命令，引导用户选择：
- 内容来源选 **"Obsidian"**
- 组织方式选 **"Copy the markdown files into the content folder"**（因为后续步骤会统一复制笔记）

## Step 4: 同步笔记到 Content 目录

将 Obsidian vault 中的所有 markdown 文件复制到 Quartz 的 content 目录。

**排除项**（不复制）：
- `.obsidian/` — Obsidian 配置目录
- `.trash/` — 回收站
- `.git/` — Git 仓库
- `node_modules/` — Node 依赖
- 隐藏文件（以 `.` 开头的文件）

**Windows (PowerShell) — 使用 robocopy**：
```powershell
robocopy "<vault-path>" "<project-dir>/content" *.md /S /XO /XD .obsidian .trash .git node_modules /XF ".*"
```

robocopy 退出码 0-7 均表示正常（0=无变更, 1=有复制, 2=有额外文件等），8+ 才是错误。

**macOS / Linux — 使用 rsync**：
```bash
rsync -av --update \
  --exclude='.obsidian/' --exclude='.trash/' --exclude='.git/' \
  --exclude='node_modules/' --exclude='.*' \
  --include='*.md' --include='*/' --exclude='*' \
  "<vault-path>/" "<project-dir>/content/"
```

如果 vault 中有附件目录（如 `attachments/`、`assets/`、`images/`），也一并复制。

## Step 5: 本地构建预览

启动本地开发服务器，让用户预览网站效果：

```bash
cd "<project-dir>"
npx quartz build --serve
```

服务器默认运行在 http://localhost:8080。提示用户：
> 本地预览服务器已启动，可以在浏览器中打开 http://localhost:8080 查看效果。
> 确认无误后，按 Ctrl+C 停止服务器，我们继续后续配置。

## Step 6: 配置 quartz.config.ts

打开 `<project-dir>/quartz.config.ts`，修改以下配置项：

```typescript
const config: QuartzConfig = {
  configuration: {
    pageTitle: "<用户提供的站点标题>",
    baseUrl: "<用户提供的 baseUrl>",
    // ... 其余配置保持默认
  },
}
```

向用户解释：
- `pageTitle` — 显示在浏览器标签页和网站头部标题
- `baseUrl` — 用于生成正确的页面链接和资源路径，**不要**带 `https://`，**不要**末尾加 `/`

## Step 7: GitHub 仓库设置指引

这是**提示用户手动操作**的步骤，不在本地执行。向用户展示以下指引：

> **请在 GitHub 上完成以下操作：**
>
> 1. 访问 https://github.com/new 创建一个新的空仓库
>    - **重要**：仓库必须是**完全空的**——不要勾选 "Add a README file"、".gitignore" 或 "license"
> 2. 创建完成后，进入仓库的 **Settings → Pages**
> 3. 在 "Build and deployment" 部分，将 **Source** 设置为 **GitHub Actions**
>
> 完成后请告诉我，我将继续配置自动部署。

等待用户确认后继续。

## Step 8: 绑定远程仓库

将 Quartz 项目的 origin 从官方仓库改为用户的 GitHub 仓库：

```bash
cd "<project-dir>"
git remote set-url origin <用户的-github-仓库地址>
git remote -v
```

验证 `origin` (fetch) 和 `origin` (push) 都指向用户的仓库。

## Step 9: 创建 GitHub Actions 部署工作流

创建 `.github/workflows/deploy.yml`：

```bash
mkdir -p "<project-dir>/.github/workflows"
```

写入以下内容到 `<project-dir>/.github/workflows/deploy.yml`：

```yaml
name: Deploy Quartz site to GitHub Pages

on:
  push:
    branches:
      - v4
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install Dependencies
        run: npm ci

      - name: Build Quartz
        run: npx quartz build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public

  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**`workflow_dispatch`** 允许手动触发部署，作为 push 触发失败时的后备方案。

### 清理继承的 Quartz 模板 Workflow

Quartz 官方仓库自带多个 workflow（`ci.yaml`、`build-preview.yaml`、`deploy-preview.yaml`、`docker-build-push.yaml`），它们包含 `if: github.repository == 'jackyzha0/quartz'` 条件，在用户的仓库中永远不会执行，只会在 Actions 页面产生多余的 skipped 记录。

创建 deploy.yml 后，删除这些无用 workflow：

```bash
rm "<project-dir>/.github/workflows/ci.yaml"
rm "<project-dir>/.github/workflows/build-preview.yaml"
rm "<project-dir>/.github/workflows/deploy-preview.yaml"
rm "<project-dir>/.github/workflows/docker-build-push.yaml"
```

向用户说明：每次推送到 `v4` 分支时，GitHub Actions 会自动构建并部署网站到 GitHub Pages。

## Step 10: 推送到 GitHub

```bash
cd "<project-dir>"
git add .
git commit -m "init quartz blog"
git branch -M v4
git push -u origin v4
```

推送成功后，向用户报告：
- 提交信息
- 推送到的分支
- 部署状态查看地址：`https://github.com/<username>/<repo>/actions`
- 首次部署通常需要 1-3 分钟
- 部署完成后网站将在 GitHub Pages URL 上线

### 首次推送后 Actions 未触发的处理

GitHub Actions 有一个已知问题：首次推送包含 workflow 文件的提交时，workflow 可能不会被触发。如果推送后在 Actions 页面看不到运行记录：

1. **先等待 1-2 分钟**，GitHub 有时需要时间处理
2. **手动触发**：进入 Actions → 选择 deploy workflow → 点击 "Run workflow" → 选择 v4 分支运行
3. **再推一个小改动**触发 push 事件：
   ```bash
   cd "<project-dir>"
   git commit --allow-empty -m "chore: trigger deploy"
   git push origin v4
   ```

## 后续更新

当用户需要更新博客内容时，应触发 `obsidian-wiki-blog-push` skill（而非本 skill）来完成增量同步和推送。本 skill 仅用于首次搭建。

## 安全规则

- **绝不删除**用户 Obsidian vault 中的任何文件
- **覆盖前确认** — 覆盖已有的 Git 仓库或配置文件前，征得用户明确同意
- **修改 Git remote 前确认**
- 执行每一条命令前，向用户简要解释其作用
- 针对用户的操作系统给出对应命令（Windows PowerShell vs macOS/Linux bash）

## 自我进化机制
每次执行完本 Skill 后：
1. 评估输出是否达成目标（pass / fail）
2. fail 时反思失败原因，在 diary/YYYY-MM-DD.md 追加「失败案例 + 修复建议」
3. 某条修复建议在最近 3 次执行中被反复提及时，提炼为正式规则，提交 PR 修改本 SKILL.md