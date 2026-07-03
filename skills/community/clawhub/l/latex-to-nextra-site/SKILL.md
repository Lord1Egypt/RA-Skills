---
version: "1.0.0"
name: "latex-to-nextra-site"
description: "将 project-cookbook-latex 生成的 LaTeX 工程转换为基于 Nextra 的中文电子文档网站，保留 PlantUML/drawio/Mermaid 图表、代码块、LaTeX 公式与表格，输出可上传 GitHub 并一键部署到 Vercel 或 Docker 的项目文件夹。"
---
> **Bilingual note**: This English edition mirrors `SKILL.zh-CN.md`. For the authoritative Chinese version, see `SKILL.zh-CN.md`.


# LaTeX to Nextra Site

本 Skill 用于把 `project-cookbook-latex` 等流程产出的**章节化中文 LaTeX 工程**自动转换为基于 **Nextra v3（Next.js 14 文档主题）** 的现代电子文档网站，交付一个可：

- `git init && git push` 上传 GitHub
- Vercel 上 Import + 零配置部署
- `docker compose up -d --build` 本地/服务器自托管

的完整项目目录。

> **本文档基于 `18-UML-SysML-CookBook` 项目（52 主体章 + 4 附录 + 42 张 PlantUML，约 18 万字）的实战经验编写**。所有"陷阱"小节都来自实际踩过的坑。

---



## ⚠️ Security & Side-Effects Disclosure

| Behaviour | Default | Rationale |
|---|---|---|
| Network access | OFF | Only fetch remote resources when user explicitly approves. |
| Host toolchain install | OFF / fail-closed | Never auto-run `pip install`, `npm install -g`, `apt install`, etc. Report missing deps and wait for manual confirmation. |
| LaTeX `-shell-escape` | OFF | Disabled by default; only enabled when user consents AND environment is sandboxed AND content is trusted. |

**Core principles:**

1. Offline by default — all side-effects require explicit user consent.
2. Fail closed on missing dependencies — never auto-install packages.
3. Never enable `-shell-escape` on untrusted input.
4. Pin remote fetches to release tags (never master/main) — require user approval before network access.

## ⚠️ 安全与副作用声明

| 行为 | 默认值 | 说明 |
|---|---|---|
| 网络访问 | 关闭 | 仅在用户明确同意后访问网络资源。 |
| 主机工具链安装 | 关闭 / 失败即止 | 不会自动运行 `pip install`、`npm install -g`、`apt install` 等。缺失依赖时报告给用户并等待手动确认。 |
| LaTeX `-shell-escape` | 关闭 | 默认不启用 `-shell-escape`；仅在用户明确同意、沙箱/容器化环境、受信内容三者同时满足时才可开启。 |

**核心原则：**

1. 默认离线，所有副作用需用户明确同意。
2. 缺失依赖时**失败即止**，不自动安装任何包。
3. 对不受信内容禁用 `-shell-escape`。
4. 远程获取资源时**固定版本/标签**，不追踪 master/main，并需用户批准。

## 灵活输入支持

本技能接受多种输入格式：

| 输入类型 | 说明 |
|---|---|
| Markdown / TXT 文件 | 最常见输入，直接处理。 |
| JSON 结构化数据 | 包含 `title`、`chapters[]`、`content` 字段时作为结构化大纲处理。 |
| 直接 LLM 上下文 | 当用户以对话方式提供内容时，自动从上下文提取大纲与正文。 |
| URL / 仓库地址 | 仅在用户明确同意后抓取远程内容。 |

## Trigger Conditions

当用户提出下列任一需求时，立即调用本 Skill：

- 把已有的 LaTeX CookBook / 电子书 / 论文项目转换成在线文档网站。
- 把 `project-cookbook-latex` 生成的工程（含 `latex/main.tex`、`chapters/*.tex`、`figures/`、`diagrams/`、`metadata/`）转换为可在网页上阅读的电子书。
- 要求基于 **Nextra v3**（或 Next.js 14 + React）搭建文档站，并要求支持**多语言切换、明暗模式、Markdown/PDF 导出、全文搜索**。
- 要求保留 LaTeX 工程中的 PlantUML / Draw.io / Mermaid 图表、代码块、公式、表格与图片。
- 要求最终输出可上传 GitHub、Vercel 零配置部署、或 Docker 自托管的项目文件夹。
- 要求生成中文为主、可选英文（或其他语言）切换的双语/多语文档站。

---

## Required Linked Skills

本 Skill 是**编排型 Skill**。执行时按需联动：

1. `project-cookbook-latex` —— 当用户尚未生成 LaTeX 工程时，先调用其产出标准化工程。
2. `plantuml` —— 把 `.puml` 渲染为 SVG + PNG。**优先使用 Docker（`plantuml/plantuml:latest`）而非 plantuml.jar**，因为：
   - 零安装，跨平台一致
   - **不要走 plantuml skill 自带的 PS1 脚本**：其在中文（GBK）locale 的 PowerShell 下会因带中文/特殊字符的字符串解析失败。本 Skill 直接调用 `docker run`。
3. `drawio` —— 把 `.drawio` 导出为 `.drawio.svg`。
4. `md-image-to-tos` —— 仅当用户要求将站点图片上传到对象存储（而非走仓库内 `public/`）时调用。

---

## Overall Goals

- **内容来源**：用户指定的 LaTeX 工程。
- **内容形式**：每个 `chapters/*.tex` 对应一个 `.mdx` 页面。
- **语言策略**：默认中文（`zh`）为主语言；同步生成 `en/` 占位骨架。
- **主题特性**：明暗模式、本地全文搜索、多语言切换、KaTeX 公式、Mermaid、代码块高亮。
- **图表处理**：PlantUML / Draw.io 在**构建期**渲染；Mermaid 走 Nextra 内置客户端渲染。
- **表格处理**：宽表降级为 `<div className="overflow-x-auto">` 包裹的 HTML 表格。
- **代码处理**：`lstlisting` / `tcblisting` → 带语言标识的代码围栏。
- **公式处理**：`$...$` 与 `$$...$$` 保留，KaTeX 渲染。
- **章节编号**：当**阅读顺序 ≠ `\input` 顺序**时，必须执行重编号 + 跨章引用链接化（详见第 6 节）。
- **下载入口**：PDF / LaTeX zip 归档到 `public/downloads/`。
- **三路部署**：Vercel、Docker、自托管均可。

---

## Mandatory Quality Gates

生成完成前必须通过以下检查；不通过则继续修复：

1. **`npm run build` 成功**，不得有 MDX 解析 error（warning 允许）。
2. **首页 `/` 自动重定向到 `/zh`**（`middleware.js` 必须存在）。
3. **明暗模式切换可用**，所有图表在两种模式下均可读。
4. **多语言切换控件存在**（即便 `en` 内容为占位），`/zh/...` 与 `/en/...` 均可解析。
5. **侧边栏目录完整**，与设计的阅读顺序一致（**不一定等于文件名字典序，也不一定等于 `\input` 顺序**）。
6. **所有图表能加载**：HTTP 200，无 404。
7. **代码块带语言高亮**，无 LaTeX 残留。
8. **公式可见**：KaTeX 已注入。
9. **表格无 LaTeX 残留**（无 `\hline`、`\toprule`、裸 `&` 列分隔符）。
10. **章节编号一致**：侧边栏标号 = 正文 "第 N 章" 引用编号；所有跨章引用链接化为 `[第 N 章](/zh/chXX-...)`。
11. **Docker 镜像可启动**：`docker compose up -d --build` 后 `Up healthy`，`http://localhost:3000/zh` 返回 200。
12. **Vercel 兼容**：根目录存在 `package.json`、`next.config.mjs`、`theme.config.tsx`、`middleware.js`，Node 声明 `>=18.17.0`。

---

## Standard Output Structure

```text
<ProjectName>-site/
├── README.md                   # 项目说明、本地启动
├── DEPLOY.md                   # GitHub + Vercel + Docker 部署步骤
├── Dockerfile                  # 多阶段构建（deps → builder → runner）
├── docker-compose.yml          # 单服务 + healthcheck
├── .dockerignore
├── package.json
├── package-lock.json
├── .npmrc
├── next.config.mjs             # Nextra + i18n + KaTeX + standalone
├── theme.config.tsx            # Logo、暗黑模式、搜索、页脚
├── middleware.js               # / → /zh 重定向（必需）
├── tsconfig.json
├── .gitignore
├── vercel.json                 # 可选
├── public/
│   ├── figures/                # LaTeX 原始 figures + PlantUML/Drawio 渲染产物
│   ├── diagrams-src/           # 原始 .puml / .drawio
│   └── downloads/
│       ├── <ProjectName>.pdf
│       └── <ProjectName>-LaTeX.zip
├── pages/
│   ├── _meta.ts                # 顶层（zh / en 暴露为 page）
│   ├── _app.tsx
│   ├── zh/
│   │   ├── _meta.ts            # 中文侧边栏（含 separator 分组）
│   │   ├── index.mdx
│   │   ├── preface.mdx
│   │   ├── ch00-overview.mdx … ch48-arch-oo-ddd-bridge.mdx
│   │   ├── appendix-a-plantuml.mdx … appendix-d-references.mdx
│   │   └── downloads.mdx
│   └── en/
│       ├── _meta.ts
│       ├── index.mdx
│       └── ...（占位骨架）
├── components/
│   ├── PdfDownload.tsx
│   └── DiagramSource.tsx
├── styles/
│   └── globals.css             # callout / figure / 表格滚动 / KaTeX 微调
└── scripts/
    ├── tex2mdx.mjs             # LaTeX → MDX 转换器
    ├── render-plantuml.mjs     # Docker 批量渲染 .puml → .svg + .png
    ├── export-drawio.mjs       # 批量导出 .drawio → .drawio.svg
    ├── build-meta.mjs          # 由章节顺序生成 _meta.ts
    ├── renumber-content.mjs    # 跨章引用重编号 + 链接化
    ├── check-mdx.mjs           # MDX 语法预检（可选）
    └── check-yaml.mjs          # frontmatter YAML 预检（可选）
```

---

## Workflow

### 1. Input Identification & Location

至少识别：

- LaTeX 根目录（通常含 `main.tex` 与 `chapters/`）。
- 章节文件清单与顺序（**以 `main.tex` 中 `\input{chapters/...}` 顺序为准**）。
- **阅读顺序（reading order）**：当 `\part{}` 不与文件名字典序对齐时，**阅读顺序 ≠ `\input` 顺序**。例如 UML CookBook 项目中阅读顺序为 `ch00 → ch38 → ch39 → ch01 → ... → ch48 → ch40 → ch41 → ...`，**侧边栏标号必须按这个顺序而不是 ch## 数字**。务必询问用户**章节是否需要重编号**。
- 图表来源目录：`figures/`、`diagrams/`、可能的 `image/`。
- 编译产物：`dist/*.pdf`、`*.zip`，可作为下载资源。

如缺少关键输入，简洁询问：

- LaTeX 工程目录在哪里？
- 网站主语言是中文还是中英双语？是否需要英文骨架？
- 是否要在站点中提供 PDF 下载入口？
- 站点 Logo、网站名、GitHub 仓库 URL 是什么？
- **章节顺序：侧边栏阅读顺序与文件名字典序一致吗？若否，是否需要按阅读顺序重编号（影响所有 "第 N 章" 引用）？**
- **是否需要 Docker 部署？**（默认建议输出 Dockerfile + docker-compose.yml）。

### 2. Initialize Nextra Project

使用 **Nextra v3** + **Next.js 14（pages router）**。

`package.json` 关键依赖：

```json
{
  "name": "<project-name>-site",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "prepare:content": "node scripts/tex2mdx.mjs && node scripts/build-meta.mjs && node scripts/renumber-content.mjs",
    "prepare:diagrams": "node scripts/render-plantuml.mjs && node scripts/export-drawio.mjs",
    "convert": "npm run prepare:diagrams && npm run prepare:content"
  },
  "dependencies": {
    "next": "^14.2.15",
    "nextra": "^3.2.4",
    "nextra-theme-docs": "^3.2.4",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.12.12",
    "@types/react": "^18.3.3",
    "typescript": "^5.4.5"
  },
  "engines": { "node": ">=18.17.0" }
}
```

`next.config.mjs`（**与实战工程完全一致**）：

```js
import nextra from 'nextra'

const withNextra = nextra({
  theme: 'nextra-theme-docs',
  themeConfig: './theme.config.tsx',
  defaultShowCopyCode: true,
  latex: {
    renderer: 'katex',
    options: { strict: 'ignore', trust: true }
  },
  search: { codeblocks: false },
  mdxOptions: {
    rehypePrettyCodeOptions: { theme: 'github-dark-dimmed' }
  }
})

export default withNextra({
  output: 'standalone',         // 关键：Docker 镜像需要 standalone
  i18n: {
    locales: ['zh', 'en'],
    defaultLocale: 'zh'
  },
  reactStrictMode: true,
  images: { unoptimized: true } // 关键：让 Next.js 不强制走 Image Optimization
})
```

> **关键警告**：构建期会出现 `[nextra] Next.js doesn't support i18n by locale folder names.` 这是已知**告警**而非错误。Nextra v3 的 `pages/zh/` + `pages/en/` 文件夹布局与 Next.js 内置 i18n 同时存在，Nextra 自己处理路由；告警可忽略。

`theme.config.tsx` 关键项（中文优先）：

```tsx
import type { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span style={{ fontWeight: 700 }}>项目 CookBook</span>,
  project: { link: 'https://github.com/<user>/<repo>' },
  docsRepositoryBase: 'https://github.com/<user>/<repo>/tree/main',
  darkMode: true,
  i18n: [
    { locale: 'zh', name: '简体中文' },
    { locale: 'en', name: 'English' }
  ],
  search: { placeholder: '搜索文档…' },
  editLink: { content: '在 GitHub 上编辑此页 →' },
  feedback: { content: '问题或建议？' },
  footer: { content: '© 2026 项目 CookBook · 基于 Nextra 构建' },
  toc: { backToTop: true }
}
export default config
```

**`middleware.js`（强制）**——让根路径自动重定向到默认语言：

```js
import { NextResponse } from 'next/server'

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)']
}

export function middleware(req) {
  const { pathname } = req.nextUrl
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/zh', req.url))
  }
  return NextResponse.next()
}
```

`.npmrc`（屏蔽 pnpm 配置告警；如果用户用 npm 可忽略此文件）：

```
# pnpm 兼容；npm 会忽略未知项但会打印 warn，可以删除
auto-install-peers=true
shamefully-hoist=true
```

> **`npm warn Unknown project config "auto-install-peers"`** 是**非阻塞告警**。要么保留（用 pnpm）要么删除 `.npmrc`（纯 npm）。

### 3. 图表预处理

**先做图，后写正文**——否则 mdx 中的图片引用会全是 404。

#### 3.1 PlantUML —— Docker 渲染（推荐方案）

**关键经验**：

1. **使用 Docker，不要用 plantuml.jar**。`plantuml/plantuml:latest` 已包含 Java + plantuml.jar + 字体；零安装、跨平台一致。
2. **PlantUML 输出文件名由 `@startuml NAME` 决定，而不是输入文件名**。例如 `fig35-book-overview.puml` 含 `@startuml book-overview` → 输出是 `book-overview.svg`。**MDX 中既可能引用 `fig35-book-overview.svg` 也可能引用 `book-overview.svg`**，所以渲染脚本必须**同时产出两个文件名**（重命名或复制）。
3. **中文必须显式声明 CJK 字体**。每个 `.puml` 必须含：

   ```
   skinparam defaultFontName "WenQuanYi Micro Hei"
   ```

   否则中文渲染为豆腐方块 □□□（不会报错，但肉眼可见）。`plantuml/plantuml:latest` 镜像内自带这套字体。
4. **必须 UTF-8 charset**：`docker run ... -charset UTF-8`，否则非 ASCII 字符可能丢失。
5. **bundled plantuml skill 的 PS1 脚本不要用**：其在 GBK locale 的中文 PowerShell 下因带中文/特殊字符的字符串解析失败。**始终直接调用 `docker run`**。

`scripts/render-plantuml.mjs` 关键骨架：

```js
import { promises as fs } from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

const srcDir = path.resolve("public/diagrams-src");
const outDir = path.resolve("public/figures");
await fs.mkdir(outDir, { recursive: true });

const files = (await fs.readdir(srcDir)).filter(f => f.endsWith(".puml")).sort();
let ok = 0, fail = 0;

for (const file of files) {
  const figBase = file.replace(/\.puml$/, "");
  const firstLine = (await fs.readFile(path.join(srcDir, file), "utf8")).split(/\r?\n/, 1)[0];
  const m = firstLine.match(/@startuml\s+(\S+)/);
  const alias = m ? m[1] : null;
  try {
    for (const fmt of ["svg", "png"]) {
      const cmd =
        `docker run --rm -v "${srcDir}:/data" -v "${outDir}:/out" ` +
        `plantuml/plantuml:latest -charset UTF-8 -output /out -t${fmt} /data/${file}`;
      execSync(cmd, { stdio: ["ignore", "ignore", "pipe"], windowsHide: true });
    }
    const baseName = alias || figBase;
    if (baseName !== figBase) {
      // Produce BOTH names so any reference in mdx resolves.
      try { await fs.copyFile(path.join(outDir, baseName + ".svg"), path.join(outDir, figBase + ".svg")); } catch {}
      try { await fs.copyFile(path.join(outDir, baseName + ".png"), path.join(outDir, figBase + ".png")); } catch {}
    }
    ok++;
  } catch (e) { fail++; }
}
console.log(`Done. ${ok} ok, ${fail} fail.`);
process.exit(fail === 0 ? 0 : 1);
```

#### 3.2 Draw.io → SVG

- 输入：`<latex-root>/diagrams/*.drawio`
- 推荐输出：`public/figures/*.drawio.svg`
- 工具：`drawio-desktop` CLI 或 Docker `rlespinasse/drawio-desktop-headless`。

#### 3.3 Mermaid

LaTeX 工程通常不直接使用 Mermaid。若用户在源 Markdown 笔记中用过，在 MDX 中保留 ` ```mermaid ` 代码围栏即可——Nextra v3 客户端会自动渲染。

#### 3.4 LaTeX 原生图（TikZ/PGFPlots/figures 目录）

直接拷贝 `figures/*.{png,svg,jpg}` 到 `public/figures/`。`.pdf` 矢量图用 `pdf2svg` 或 `inkscape --export-type=svg` 转换。

---

### 4. LaTeX → MDX 转换（`scripts/tex2mdx.mjs`）

本 Skill 的核心。**正确性高于速度**。可基于 `unified` + `mdast` 自写，或用 `pandoc --from=latex --to=gfm` 打底 + 后处理。

**推荐策略：自写解析器（更可控）**。原因：

- pandoc 对 `tcolorbox`、`xltabular`、ElegantBook 自定义环境（`definition` / `theorem` / `keypoints` 块）支持极差。
- 自定义环境往往要转成 `<div className="callout xxx">` 这种带样式的 JSX。
- 数学宏的 KaTeX 展开需要细粒度控制。

**关键转换映射表**：

| LaTeX 结构 | 转换目标 | 处理规则 |
|---|---|---|
| `\chapter{...}` | frontmatter `title:` + 不输出顶层 H1 | Nextra 用 frontmatter title 渲染页头 |
| `\section{...}` | `## ...` | 同时是右侧 TOC 节点 |
| `\subsection{...}` | `### ...` | |
| `\textbf{x}` / `\emph{x}` | `**x**` / `*x*` | |
| `\href{url}{text}` | `[text](url)` | |
| `\includegraphics[...]{figures/x}` | `<img src="/figures/x.svg" />` | 路径补 `/figures/`；扩展名优先 svg 回退 png |
| `\begin{figure} ... \caption{} \label{fig:x}` | `<figure id="fig-x">` 包裹 `<img/>` + `<figcaption/>` | **`\label{fig:x}` 必须转为 `id="fig-x"`** 否则跨页锚点 404 |
| `\begin{tabular} ... \caption{} \label{tab:y}` | `<figure id="tab-y">` 包裹 `<table/>` | 表号同样需要 id |
| `\ref{fig:x}` / `\autoref{fig:x}` | `[图 X](#fig-x)` | mdx 中显示为可点击锚点 |
| `\toprule / \midrule / \bottomrule / \hline` | 表格分隔符 `---` | 直接移除 LaTeX 命令 |
| 含合并单元格 / 多行表头 / 超 5 列 | `<div className="overflow-x-auto"><table>...</table></div>` | 必须包 overflow 容器 |
| `\begin{lstlisting}[language=Python]` | 三个反引号 + `python` 围栏 | 语言名映射；文件名保留为代码注释 |
| `\begin{tcblisting}{...}` | 代码围栏 | title 保留为第一行注释 |
| `$...$` / `$$...$$` | 原样保留 | Nextra latex 接管 |
| `\cite{key}` | `[[key]]` 或链接到 references 页 | |
| `\input{chapters/xxx}` | 拆分文件 | 由 `main.tex` input 顺序生成侧边栏 |
| 自定义 `\begin{tcolorbox}[colback=...]` | `<div className="callout xxx">...</div>` | 见下方 callout 约定 |

**Callout 约定**（与 globals.css 配合）：

```mdx
<div className="callout chapteroutline">

#### 📘 本章大纲

本章建立...

</div>

<div className="callout keypoints">

#### ✅ 核心要点

</div>

<div className="callout recipe">

#### 🍳 Recipe: ...

</div>

<div className="callout pitfall">

#### ⚠️ 常见陷阱

</div>
```

**关键陷阱（实战踩坑）**：

- **MDX 对 `<`、`>`、`{`、`}` 极敏感**：正文中的裸 `<` / `>` 必须转义为 `&lt;` / `&gt;`，或包裹在反引号代码中。
- **百分号 `%` 与数字相邻**：mdx 中 `5%` 在某些组合下被识别异常；保险做法是用 `5&#37;`。
- **中文段落不要被 pandoc 拆词**：若用 pandoc，后处理需把 CJK 字符之间的换行/单空格收紧，保留段落空行。
- **注释 `% ...` 必须丢弃**，不能进入 MDX（会被识别为 JSX props 或文本噪声）。
- **LaTeX `~` 不间断空格** → 半角空格或 `&nbsp;`。
- **frontmatter 必须有 `title:`**：Nextra 用它做面包屑与 `<title>`。
- **`<` 紧跟字母或数字**会被 MDX 当成 JSX 标签开始：例如 `<5 分钟` 这种文本必须写成 `&lt;5 分钟`。

---

### 5. 章节文件与 `_meta.ts` 生成

**关键**：Nextra v3 用 **`_meta.ts`**（TypeScript 默认导出对象）**而不是 `_meta.json`**。后者虽兼容但**不支持 `type: 'separator'` 分组**，强烈不推荐。

`pages/zh/_meta.ts` 示例（含 separator 分组、reading-order 编号）：

```ts
// 自动生成 - 请勿手工编辑（修改 scripts/build-meta.mjs）
export default {
  index: "🏠 首页",
  '---sep-0': { type: 'separator', title: "📖 前言" },
  "preface": "前言",
  '---sep-1': { type: 'separator', title: "I · 总论" },
  "ch00-overview": "0. 总论与本书地图",
  "ch38-sw-design-principles": "1. 软件设计基本原则",  // reading-order 编号
  "ch39-sdlc-methodologies": "2. SDLC 与方法论演进",
  '---sep-2': { type: 'separator', title: "II · UML 2.5" },
  "ch01-modeling": "3. 建模认识论",
  // ...
  "appendix-a-plantuml": "附录 A：PlantUML 速查",
  "downloads": "📥 下载",
}
```

**注意点**：

- key 必须与 `.mdx` 文件名（不含扩展名）一致。
- separator 用前缀 `---sep-N` 命名以保持稳定排序（短横线确保 JS 对象内键有序遍历）。
- **value 中的编号是 reading order（阅读顺序）序号，不一定是文件名里的 `chXX`**。如示例中 `ch38-sw-design-principles` 的展示名是 `"1. 软件设计基本原则"`。
- 顶层 `pages/_meta.ts` 用于把 `zh` 与 `en` 暴露为 page：

  ```ts
  export default {
    zh: { title: '简体中文', type: 'page' },
    en: { title: 'English', type: 'page' }
  }
  ```

- 英文目录 `pages/en/_meta.ts` 至少建立同结构骨架。

---

### 6. 章节重编号 + 跨章引用链接化（实战新增章节）

**问题场景**：当 `pages/zh/_meta.ts` 的阅读顺序与文件名字典序不一致（这在重排后的 CookBook 中极常见），就出现两层不匹配：

- **侧边栏标号 vs 文件名**：`ch38-sw-design-principles` 在侧边栏显示为 `"1. ..."`。
- **正文跨章引用 vs 侧边栏标号**：正文中 LaTeX `\ref` 输出的 "第 38 章" 还是老编号，与侧边栏 "1. ..." 不一致。

**解决方案**：在 `scripts/tex2mdx.mjs` 跑完后，**再跑一遍 `scripts/renumber-content.mjs`**，对 MDX 正文里的所有 "第 N 章" 引用做智能改写：

```js
// scripts/renumber-content.mjs 核心逻辑（精简版）
//
// 1. READING_ORDER 数组按阅读顺序声明所有章节 slug。
// 2. 建 oldNum → newNum 与 oldNum → slug 两张映射表。
// 3. 用正则匹配 "第 <expr> 章" 整体，<expr> 是数字 / 范围 / 列表 / 混合。
// 4. 解析 expr，把每个 OLD 编号映射为 NEW 编号。
// 5. NEW 编号排序、合并连续区间，渲染为 "[第 a–b、c 章](/zh/<slug-of-min-new>)"。
// 6. 链接目标 = NEW 编号最小者对应的 slug（保证点击后第一眼就到本范围）。
// 7. 跳过：frontmatter、代码块、行内代码、已有 markdown 链接、HTML 属性值。

const READING_ORDER = [
  "ch00-overview",
  "ch38-sw-design-principles",
  "ch39-sdlc-methodologies",
  "ch01-modeling",
  // ... 完整顺序，按 _meta.ts 顺序
];

const oldToNew = new Map();
const oldToSlug = new Map();
for (let i = 0; i < READING_ORDER.length; i++) {
  const m = READING_ORDER[i].match(/^ch(\d+)/);
  if (!m) continue;
  oldToNew.set(parseInt(m[1], 10), i);
  oldToSlug.set(parseInt(m[1], 10), READING_ORDER[i]);
}

// 正则要覆盖：第 N 章 / 第 N-M 章 / 第 N、M 章 / 第 N 与 M 章 / 第 N-M、K 章
const re = new RegExp(
  "第\\s*((?:\\d+)(?:\\s*(?:[-\u2013\u2014\u3001,\uFF0C]|\u4E0E|\u548C)\\s*\\d+)*)\\s*章",
  "g",
);
```

**规则要点**：

1. **必须 skip mask**：frontmatter（`---...---`）、fenced code（` ``` ` 之间）、inline code（单反引号之间）、existing markdown link（`[...](...)`）、HTML 属性值（`href=`、`src=`、`id=`、`alt=`、`title=`、`className=`）。
2. **链接目标 = NEW 编号最小者对应的 slug**，不是 OLD 编号最小者；这样 `[第 9–11、17 章]` 点击会跳到 reading-order 第 9 章（实际文件 `ch45-practical-oo.mdx`）。
3. **连续区间合并**：`第 9、10、11、17 章` → `第 9–11、17 章`。
4. **idempotency（幂等性）注意**：因为 skip mask 包含 existing markdown link，**第二次运行不会再改已链接化的引用**，可重复执行。
5. **执行顺序**：必须**先 `tex2mdx.mjs`（保留 OLD 编号）再 `renumber-content.mjs`**。直接对手工编辑后的文件二次运行会跳过已链接化部分（按 idempotency 是 OK 的）。

参考实战完整脚本：`18-UML-SysML-CookBook/UML-SysML-CookBook-site/scripts/renumber-content.mjs`。

---

### 7. 公式渲染

- `next.config.mjs` 中 `latex: { renderer: 'katex', options: { strict: 'ignore', trust: true } }`。
- 行内 `$E=mc^2$`、块级 `$$\int_0^1 f(x) dx$$` 原样保留。
- 自定义宏（`\newcommand`）必须在 `tex2mdx.mjs` 阶段就展开成 KaTeX 支持的语法；维护一份"宏展开映射表"。
- `strict: 'ignore'` 让 KaTeX 不抛出对未识别命令的错误（避免单个公式打挂整页）。

---

### 8. 多语言策略

- **中文优先**：`pages/zh/` 是事实标准内容源；`middleware.js` 让根路径自动重定向到 `/zh`。
- **英文骨架**：`pages/en/` 至少建立与 `zh` 同结构的占位文件，每个加：

  ```mdx
  ---
  title: <对应英文标题>
  ---

  > 🚧 English translation is in progress. Contributions welcome.
  ```

- `theme.config.tsx` `i18n` 中 `zh` 排在前。

---

### 9. PDF / 原始 LaTeX 下载入口

- `dist/<Project>.pdf` → `public/downloads/<Project>.pdf`
- `dist/<Project>-LaTeX.zip` → `public/downloads/`
- `components/PdfDownload.tsx`：

  ```tsx
  export default function PdfDownload({ href, label }: { href: string; label: string }) {
    return (
      <a className="download-btn" href={href} download>⬇️ {label}</a>
    )
  }
  ```

- `pages/zh/downloads.mdx` 提供下载页（侧边栏底部 separator 之后）。

---

### 10. styles/globals.css（实战推荐最小集）

```css
/* Callout 卡片 —— 章节大纲 / 核心要点 / Recipe / Pitfall */
.callout {
  border-left: 4px solid;
  padding: 0.75em 1em;
  margin: 1em 0;
  border-radius: 4px;
}
.callout h4 { margin-top: 0; }
.callout.chapteroutline { background: rgba(59,130,246,0.08); border-color: #3b82f6; }
.callout.keypoints      { background: rgba(34,197,94,0.08);  border-color: #22c55e; }
.callout.recipe         { background: rgba(245,158,11,0.08); border-color: #f59e0b; }
.callout.pitfall        { background: rgba(239,68,68,0.08);  border-color: #ef4444; }

/* 暗色模式微调 */
.dark .callout.chapteroutline { background: rgba(59,130,246,0.16); }
.dark .callout.keypoints      { background: rgba(34,197,94,0.16); }
.dark .callout.recipe         { background: rgba(245,158,11,0.16); }
.dark .callout.pitfall        { background: rgba(239,68,68,0.16); }

/* figure + caption */
figure { margin: 1.25em 0; text-align: center; }
figure img { max-width: 100%; height: auto; }
figcaption {
  font-size: 0.875em;
  color: var(--nx-color-fg-default, #6b7280);
  margin-top: 0.5em;
}

/* 表格横向滚动（防止超宽表撑破移动端布局） */
.overflow-x-auto { overflow-x: auto; }
.overflow-x-auto > table { min-width: 540px; }

/* 下载按钮 */
.download-btn {
  display: inline-block;
  padding: 0.5em 1em;
  margin-right: 0.5em;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  text-decoration: none;
}
.download-btn:hover { background: #1d4ed8; }
.download-btn.secondary { background: #6b7280; }
.download-btn.secondary:hover { background: #4b5563; }

/* 封面网格 */
.cover-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.5em;
  align-items: start;
  margin: 1em 0 2em;
}
@media (max-width: 640px) {
  .cover-grid { grid-template-columns: 1fr; }
}
```

`pages/_app.tsx`：

```tsx
import type { AppProps } from 'next/app'
import '../styles/globals.css'
export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

---

### 11. Docker 部署（实战完整方案）

提供本地/服务器自托管能力，与 Vercel 并列为推荐部署方式。

`Dockerfile`（三阶段构建）：

```dockerfile
# ===== 阶段 1: 依赖安装 =====
FROM node:18-alpine AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json* .npmrc* ./
RUN if [ -f package-lock.json ]; then \
      npm ci --no-audit --no-fund; \
    else \
      npm install --no-audit --no-fund; \
    fi

# ===== 阶段 2: 构建 =====
FROM node:18-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ===== 阶段 3: 运行时 =====
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

# 关键：Next.js standalone 输出
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

> **关键点**：必须在 `next.config.mjs` 中开启 `output: 'standalone'`，否则 `.next/standalone/server.js` 不会生成。

`docker-compose.yml`：

```yaml
services:
  cookbook:
    build:
      context: .
      dockerfile: Dockerfile
    image: <project-name>-site:latest
    container_name: <project-name>
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - HOSTNAME=0.0.0.0
      - NEXT_TELEMETRY_DISABLED=1
    healthcheck:
      test: ["CMD-SHELL", "wget -q -O - http://127.0.0.1:3000/zh > /dev/null 2>&1 || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

`.dockerignore`（关键：避免拷贝 `node_modules` / `.next` / git 等大文件）：

```
node_modules
.next
.vercel
out
dist
.git
.gitignore
.dockerignore
Dockerfile
docker-compose.yml
README.md
DEPLOY.md
*.log
.DS_Store
.env*.local
coverage
.idea
.vscode
*.tsbuildinfo
```

**一键启动**：

```bash
docker compose up -d --build
# 容器会自动 healthcheck，约 30 秒后 Up healthy
# 浏览器打开 http://localhost:3000  → 自动跳转 /zh
```

**镜像体积参考**：Alpine + Node 18 + Next standalone ≈ **250–270 MB**。

**Docker 部署验证清单**：

```bash
docker ps --filter "name=<project-name>"
# 期望：STATUS = Up X seconds (healthy)

docker logs -f <project-name>
# 期望：Ready in NNNms

curl -sI http://127.0.0.1:3000/                       # 期望 308 → /zh
curl -sI http://127.0.0.1:3000/zh                     # 期望 200
curl -sI http://127.0.0.1:3000/zh/ch00-overview       # 期望 200
curl -sI http://127.0.0.1:3000/figures/<some-fig>.svg # 期望 200
```

---

### 12. 上传 GitHub + 部署 Vercel

`DEPLOY.md` 指引：

```markdown
## 上传到 GitHub

cd <ProjectName>-site
git init && git add . && git commit -m "feat: init nextra docs from latex"
gh repo create <user>/<repo> --public --source=. --remote=origin --push

## 部署到 Vercel

1. 打开 https://vercel.com/new
2. Import Git Repository → 选择刚才的仓库
3. Framework Preset：Next.js（自动识别）
4. Build Command：next build（默认）
5. Output Directory：.next（默认）
6. Node.js Version：18.x 或 20.x
7. 点击 Deploy
```

可选生成 `vercel.json`（一般无需）：

```json
{ "framework": "nextjs", "buildCommand": "next build", "installCommand": "npm install" }
```

---

### 13. `.gitignore`

```
node_modules
.next
.vercel
dist
*.log
.DS_Store
.env*.local
```

注意 `public/figures/` **不能**被 ignore——这是站点资源。

---

## 推荐执行清单

```text
0.  询问关键参数：LaTeX 路径、主语言、Logo、GitHub URL、是否需要 Docker、是否需要按阅读顺序重编号
1.  定位 LaTeX 工程，识别 main.tex 的 \input 顺序，列出全部 chapters/*.tex
2.  与用户确认 reading order（侧边栏阅读顺序），保存为 READING_ORDER 数组
3.  扫描 diagrams/ 与 figures/，建立"图表清单 + 来源 + 目标路径"
4.  渲染 PlantUML：docker run plantuml/plantuml:latest 批量产 .svg + .png + 双别名
5.  渲染 Draw.io：drawio-desktop 或 Docker drawio-headless 批量产 .drawio.svg
6.  拷贝 LaTeX figures/* 到 public/figures/；.pdf 矢量图先转 svg
7.  初始化 Nextra 工程：package.json + next.config.mjs (output: standalone) + theme.config.tsx + middleware.js
8.  写 styles/globals.css（callout / figure / overflow-x-auto / 下载按钮）
9.  写 scripts/tex2mdx.mjs：自写解析器或 pandoc + 后处理
10. 批量转换 chapters/*.tex → pages/zh/*.mdx（含 frontmatter title、figure id 锚点、callout 包装）
11. 生成英文骨架 pages/en/*.mdx（仅 frontmatter + TODO 提示）
12. 写 scripts/build-meta.mjs，生成 pages/zh/_meta.ts 和 pages/en/_meta.ts（含 separator）
13. （reading order ≠ \input order 时）写 scripts/renumber-content.mjs，把跨章引用链接化
14. 拷贝 PDF / LaTeX zip 到 public/downloads/，写 PdfDownload 组件 + downloads.mdx
15. npm install && npm run build —— 验证生产构建（warning 允许，error 必须为零）
16. 写 Dockerfile + docker-compose.yml + .dockerignore；docker compose up -d --build 验证 healthy
17. 写 README.md（介绍 + 本地启动）与 DEPLOY.md（GitHub + Vercel + Docker 三路）
18. 输出最终目录链接 + 验证报告
```

---

## 常见失败点与优化策略（来自实战）

### 失败点：PlantUML 中文显示为方块 □□□

**原因**：`.puml` 未指定 CJK 字体。
**优化**：每个 `.puml` 加 `skinparam defaultFontName "WenQuanYi Micro Hei"`；`render-plantuml.mjs` 启动时校验"含 CJK 字符但无 CJK 字体声明"。

### 失败点：PlantUML 图引用 404（`fig35-x.svg` 不存在）

**原因**：PlantUML 输出名跟随 `@startuml NAME`，与文件名 `fig35-x.puml` 不一致。
**优化**：渲染脚本必须**同时产出两个文件名**（一份按文件名 figXX，一份按 alias）。

### 失败点：bundled plantuml skill PS1 脚本报 ParserError

**原因**：脚本中 `$($var:foo)x$($var:bar)` 在中文 GBK PowerShell 下解析失败。
**优化**：**绕开 PS1，直接 `docker run plantuml/plantuml:latest`**。

### 失败点：MDX 解析报错 "Unexpected character `<`"

**原因**：LaTeX 正文里的裸 `<`、`>` 被 MDX 当作 JSX 标签开始。
**优化**：转换阶段全局转义裸 `<`/`>` 为 `&lt;`/`&gt;`，或包裹在反引号代码中。

### 失败点：中文段落被空格断裂

**原因**：pandoc 默认按词换行，中文遇空格被切。
**优化**：转换后用正则把 CJK 字符之间的换行/空格收紧（保留段落空行）。

### 失败点：跨章引用编号与侧边栏不一致

**原因**：reading order ≠ 文件名字典序，只改了 `_meta.ts` 没跑 `renumber-content.mjs`。
**优化**：每次改阅读顺序后必须重跑 `node scripts/renumber-content.mjs`。

### 失败点：跨章引用链接化后再次运行被破坏

**原因**：脚本不幂等，二次运行把已是 NEW 编号的链接又按 OLD 编号映射一次。
**优化**：skip mask 必须包含 existing markdown links；先在干净的 MDX（刚 tex2mdx 完）上跑。**如果必须二次运行，唯一安全做法是先 `node scripts/tex2mdx.mjs` 把 MDX 回滚到 OLD 编号状态再重跑**。

### 失败点：Docker 构建后容器秒挂

**原因**：`next.config.mjs` 未设 `output: 'standalone'`，`.next/standalone/server.js` 不存在；或 `public/` 没拷贝。
**优化**：检查 `next.config.mjs` 配置；Dockerfile 中 `COPY --from=builder /app/public ./public` 必须存在。

### 失败点：i18n 切换后 404

**原因**：英文目录缺少同名文件。
**优化**：构建 `pages/en/` 时严格镜像 `pages/zh/` 的文件名结构；缺失页面生成占位 mdx。

### 失败点：构建警告 "[nextra] Next.js doesn't support i18n by locale folder names"

**原因**：Nextra v3 的 `pages/zh/` + `pages/en/` 文件夹布局与 Next.js 内置 i18n 同时存在。
**优化**：**这是非阻塞告警**，Nextra 自己接管路由，可忽略。

### 失败点：npm warn "Unknown project config 'auto-install-peers'"

**原因**：`.npmrc` 含 pnpm 专属配置项。
**优化**：要么删除 `.npmrc`（纯 npm），要么忽略（用 pnpm）。**非阻塞**。

### 失败点：Mermaid 在暗色模式下不可读

**原因**：默认 Mermaid 主题与暗背景对比度低。
**优化**：在 `theme.config.tsx` 中通过 Nextra 的 mermaid 主题配置切换 `default` / `dark`。

### 失败点：表格在窄屏溢出

**原因**：宽表未加滚动容器。
**优化**：所有 HTML 表格统一包裹 `<div className="overflow-x-auto">`；`styles/globals.css` 给 `table` 设 `min-width: 540px`。

### 失败点：公式不渲染

**原因**：未启用 `latex: { renderer: 'katex' }`，或自定义宏 KaTeX 不支持。
**优化**：检查 `next.config.mjs`；维护宏展开映射表；`strict: 'ignore'` 容错。

### 失败点：Vercel 构建失败 "Module not found: nextra-theme-docs"

**原因**：依赖未声明 / `next.config.mjs` 引入路径不对。
**优化**：确认 `dependencies` 里有 `nextra` 与 `nextra-theme-docs`，且版本兼容（v3.x + Next.js 14.x）。

### 失败点：仓库太大上传 GitHub 失败

**原因**：把 `node_modules` 或大量 PDF 一并提交。
**优化**：完善 `.gitignore`；若 PDF > 50MB，移出仓库改放对象存储。

### 失败点：tex2mdx.mjs 路径硬编码到旧 LaTeX 工程位置

**原因**：脚本顶部 `const SRC_LATEX = 'D:/old-path/latex'` 没跟着项目迁移更新。
**优化**：脚本第一行的 `SRC_LATEX` 必须随项目搬迁同步更新；推荐改为读取环境变量 `process.env.SRC_LATEX || default`。

### 失败点：Windows 路径在 docker run 命令里有空格或特殊字符

**原因**：`-v` 挂载路径未加引号。
**优化**：始终用 `-v "${path}:/data"` 包双引号；用 Node 的 `path.resolve()` 确保绝对路径。

---

## 重生成命令（用户文档片段）

LaTeX 源 / 章节顺序 / 图表更新后的标准刷新流程：

```bash
# 1. 重渲所有 PlantUML（需 Docker）
node scripts/render-plantuml.mjs

# 2. LaTeX → MDX（覆盖式重生，保留 OLD 编号）
node scripts/tex2mdx.mjs

# 3. 重写侧边栏标签（reading-order 编号）
node scripts/build-meta.mjs

# 4. 把正文中的 "第 N 章" 跨章引用链接化为 NEW 编号
node scripts/renumber-content.mjs

# 5. 验证
npm run build

# 6. 部署
docker compose up -d --build      # 自托管
# 或 git push && Vercel 自动 redeploy
```

---

## 示例用户请求

```
请把 d:\TARE-WORK\11-信息论 工程转换成基于 Nextra 的中文电子文档网站，
保留 PlantUML 图表和封面图，支持明暗模式切换，并打包成可上传 GitHub、
可一键部署到 Vercel 与 Docker 的项目文件夹。
侧边栏需要按阅读顺序重编号。
```

执行步骤：

1. 读取 `d:\TARE-WORK\11-信息论\main.tex` 与 `chapters/`、`diagrams/*.puml`、`figures/*`。
2. 询问用户确认 reading order，构建 `READING_ORDER` 数组。
3. **直接 `docker run plantuml/plantuml:latest` 渲染 `.puml` 为 SVG + PNG**（不走 plantuml skill 的 PS1 脚本）。
4. 在 `d:\TARE-WORK\信息论-site/` 下生成 Nextra 工程。
5. 章节按 `main.tex` 顺序 `tex2mdx.mjs` 生成 `pages/zh/*.mdx`（保留 OLD 编号）。
6. 生成英文骨架与 `_meta.ts`（含 separator 分组）。
7. **跑 `renumber-content.mjs`，把所有 "第 N 章" 跨章引用按 reading order 重编号并链接化**。
8. 拷贝 PDF 到 `public/downloads/`。
9. 写 `Dockerfile`、`docker-compose.yml`、`.dockerignore`、`middleware.js`、`styles/globals.css`。
10. `npm run build` 验证；`docker compose up -d --build` 验证 healthy。
11. 输出 `README.md` 与 `DEPLOY.md`。
12. 给用户提供文件夹链接、端口、HTTP 探针证据。

---

## 示例最终回复要点

最终交付时应包含：

- 项目文件夹的 `computer://` 链接。
- 已转换的章节数 / 图表数 / 表格数 / 代码块数。
- 已生成的下载资源（PDF / LaTeX zip）链接。
- 本地启动命令（`npm install && npm run dev`）。
- GitHub 上传与 Vercel 部署的两条关键命令 / 步骤。
- **Docker 一键启动命令**（`docker compose up -d --build`）+ 容器健康状态截图/输出。
- **HTTP 探针验证**：根、`/zh`、典型章节、PlantUML SVG 均返回 200。
- 如有未完成项（例如英文章节仅占位、某些 TikZ 图未能转 SVG），明确列出。
