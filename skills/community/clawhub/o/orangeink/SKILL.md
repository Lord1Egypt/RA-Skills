---
name: orangeink
description: 橙墨（orangeink）公众号排版 skill。两种用法：① 按橙墨写作规范产出/审阅公众号 Markdown 文稿；② 把 Markdown 一键转成可直接发布微信公众号的内容——纯净合规 HTML（API 用）、一键复制页（浏览器打开→复制→粘贴）、公众号草稿箱 API 请求体 JSON，输出自带静态合规自检。触发词：橙墨排版、公众号排版、oimd、orangeink。不适用于一般写作、翻译、或知乎/头条等非公众号平台排版。本 skill 面向中文微信公众号场景，输出为简体中文。
license: MIT
compatibility: Node >= 18；换机部署后在 skill 目录执行 npm install 一次（jsdom / markdown-it 已精确锁版本声明在 package.json dependencies）
metadata:
  author: AladoooWu
  version: 1.2.8
  locale: zh-CN（微信公众号场景限定，产品定义即中文输出）
  permissions:
    fs-read: 仅读取用户在命令行显式传入的 Markdown 文件，及本 skill 目录内的自身文件
    fs-write: 仅写入用户在命令行显式指定的输出路径；不写任何其他位置
    network: 默认零网络访问。唯一例外：parity-check.mjs 在「同仓模板与 argv 模板均缺失」且用户显式设置环境变量 OIMD_REMOTE_TEMPLATE=1 时，才从官方仓 raw.githubusercontent.com/aladooo/orangeink 拉取 index.html 用于对拍
    exec: 仅当前 node 进程内执行；不调用 shell，不执行任何外部二进制
---

# 橙墨排版 Skill（orangeink · oimd）

把公众号文章从 Markdown 变成**可直接发布**的内容。核心价值：内置橙墨的**平台合规管线**（span leaf 包裹 / px 行高 / font-family 全剔除 / li section 包裹 / 分割线 nbsp 防剥 / 复制净化）——这些是 2026-09 对抗公众号「结构异常」弹窗实测踩坑的成果，通用 md2wechat 类工具不具备。

## 何时用我

1. **写稿**：用户要写公众号文章 → 先读 `references/writing-guide.md`，按橙墨规范产出标准 Markdown（扩展语法仅 `:::` 模块 / GFM 警告块 / `[^id]` 脚注，其余是标准 Markdown）
2. **排版**：用户有 `.md` 稿要发公众号 → 直接跑渲染命令
3. **审稿**：用户问「这篇稿排版上有什么问题」→ 渲染 + 自检，报告违规项与图片清单

**何时不适用**：一般写作 / 翻译 / 知乎、头条等非公众号平台排版——这些场景不要触发本 skill；用户明确要别的语言或别的平台时，交还通用能力。

## 权限与信任边界（安全声明）

- **文件访问**：只读输入 `.md` 与本 skill 目录自身文件；只写用户/agent 显式指定的输出路径（`-o/--copy-page/--draft/--meta`）。无其他文件系统访问
- **网络访问**：默认**零网络请求**。唯一的联网能力是 parity-check 的远端模板兜底，且默认关闭（须显式设 `OIMD_REMOTE_TEMPLATE=1`，见下）
- **代码执行边界**：parity-check 用 jsdom `runScripts: 'dangerously'` 执行浏览器版模板的内嵌脚本（对拍护栏原理）——**仅执行官方仓 `aladooo/orangeink` 的 `index.html`**（同仓检出或 argv 显式指定），绝不执行任何外部/用户来源的 HTML；`render.mjs` 本体不执行任何来自输入 Markdown 的代码

## 排版命令（核心，一条命令出全部产物）

```bash
node <skill目录>/scripts/render.mjs <文章.md> \
  -o 输出片段.html --copy-page 输出复制页.html --draft 草稿.json --meta 元数据.json
```

- 依赖：Node ≥18 + `jsdom` / `markdown-it`（均已在 package.json **精确锁版本**；换机部署后在 skill 目录 `npm install` 一次）
- `-o`：**纯净合规 HTML 片段**（`<section style="padding:0 14px…">` 起），给接公众号 API 的 skill 直接当 `content` 字段用
- `--copy-page`：**一键复制页**（自带「一键复制到公众号」按钮），浏览器打开 → 点按钮 → 公众号编辑器 Ctrl+V。这是**默认发布路径**
- `--draft`：公众号 `draft/add` API 请求体（title/author/digest/content），默认作者「登叔」，可用 `--title/--author/--digest` 覆盖
- `--meta`：字数（源文/公众号口径）/ 图片清单 / 自检结果 JSON
- 主题：`--theme orangeink|inkblue|pine|gold|haitang`（默认 orangeink 炭黑×亮橙）；`--zoom 0.94|1|1.06`；`--pad 0|14|22`
- 复制页自带**二次微调栏**：主题 / 字号 / 边距 / 深色（夜读配色）可即调即复制；「手机预览」**默认开启**（仅切 375px 预览不影响复制内容）。页面不展示 CLI 提示，「微调为快速近似」的说明只保留在本文件（agent 侧）：微调是浏览器端调色板映射的**快速近似**（切换主题时警告块底色等近似），精确效果用 `--theme/--zoom/--pad` 重新生成；深色为正文深底配色，公众号正文区两侧会露白边，交付前提示用户
- 复制页含**品牌位**：顶栏 `orangeink · oimd v<版本号>`、底部引流链接（github.com/aladooo/orangeink）——仅在复制页页面上，**不会进入复制到公众号的内容**
- 退出码：0=成功且自检 0 项；1=渲染失败；2=自检有 error 级违规

运行后**必须向用户报告**：自检结果行 + 图片清单（如有）。退出码 2 时先修稿再交付。

## 对拍护栏（改了 render.mjs 或 orangeink 升版后必跑）

```bash
node <skill目录>/scripts/parity-check.mjs <文章.md> [orangeink/index.html 路径]
```

原理：把浏览器版 index.html 原脚本放进 jsdom 执行，调其 `__tool.copyHTML()` 与 CLI 输出比对，**输出必须逐字节一致**（已验证：2026-09-28，sample + 07~20 期共 15 篇全过）。不一致 = 移植版漂移，禁止发布。

模板解析三级回退：argv 显式路径 → 同仓检出 `../../index.html` → 远端拉取。**远端拉取默认关闭**（会命中平台安全审计的 Remote Payload Retrieval 模式）：仅当环境变量 `OIMD_REMOTE_TEMPLATE=1` 时才从 `raw.githubusercontent.com/aladooo/orangeink/main` 拉取并缓存 1 小时；审核/沙箱环境请勿开启。

## 合规边界（诚实声明）

CLI 自检覆盖**静态规则**：无单位行高 / text-align:start / font-family / 块级直接文本 / 固定宽度溢出 / 嵌套深度>15 / 表格>4 列 / pre 滥用 / 空链接。
**不覆盖布局类**（官方「实测口径」叠字检测需真实渲染）——橙墨输出因 `<span leaf>` 包裹该检测恒 0，且浏览器版自检器与 probe.py 仍在兜底。首次用新主题/新语法时，建议用户在浏览器版排版台里点一次「自检」复核。

## 图片（重要，发布前必看）

- **复制页路径**（默认）：粘贴进公众号编辑器时微信自动转存外链图片，一般无需处理
- **API 路径**（draft.json）：`draft/add` 的 content 中**外链图片会被过滤**——须先调 `uploadimg` 传素材库换永久链接（本 skill 不做上传，属用户自有 API 凭据的职责边界）。图片清单在 `--meta` 输出里

## 文件结构

```
SKILL.md                      本文件
scripts/render.mjs            headless 渲染器（逻辑源：orangeink v1.1.0，函数级移植）
scripts/parity-check.mjs      对拍护栏
references/writing-guide.md   橙墨写作规范（写稿前必读）
references/wechat-rules.md    微信合规规则与历史坑位表
references/wechat-api.md      草稿箱 API 注意事项
package.json / node_modules   jsdom 29.1.1 + markdown-it 14.3.2（npm 精确锁版本；打包发布时排除 node_modules）
tests/sample.md               全语法测试稿
tests/test-copypage.mjs       复制页微调栏冒烟测试（node test-copypage.mjs <复制页.html>）
```

## 逻辑基准与同步纪律

- 逻辑源 = **orangeink v1.1.0** `src/template.html`（GitHub: aladooo/orangeink，MIT）
- orangeink 发新版后：① 重跑 parity-check；② 如失败，按 diff 同步 render.mjs；③ 更新本文件基准版本号
- 不要在 render.mjs 里「顺手优化」样式逻辑——对拍一致是唯一真理
- skill 版本：**oimd v1.2.4**（2026-10-09：vendor 转 npm 精确锁依赖、远端模板拉取默认关闭、权限与信任边界声明；正文渲染逻辑未动，对拍护栏仍以 v1.1.0 为基准）

## 跨 agent 兼容与打包（SkillHub / OpenClaw / Codex）

- **结构合规**：本 skill 即 Claude Agent Skills 通用规范布局（`SKILL.md` + `scripts/` + `references/` + `tests/`），frontmatter 仅用通用字段（name / description / license / metadata）——**OpenClaw 完全兼容 Claude Skills 格式**，目录拷贝即用；WorkBuddy 原生支持（触发词「橙墨排版」）；Codex 无 skill 机制，把 SKILL.md 当指令文档 + 直接跑 render.mjs CLI
- **frontmatter 自查**（skills.sh / SkillHub 校验口径）：`name: orangeink` 为 kebab-case、≤64 字符、与目录同名 ✓；`description` 单行、≤1024 字符、含触发词 ✓
- **打包发布注意（重要）**：SkillHub 类平台限 100 文件 / 10MB / 单文件 1MB，**打包时必须排除 `node_modules/`**，改为在 SKILL.md 声明依赖（`compatibility: Node >= 18`）；换机部署后在 skill 目录执行 `npm install` 一次即可。依赖全部走 npm 精确锁版本（jsdom 29.1.1 / markdown-it 14.3.2），**包内不含任何 vendor 发行版文件**
- 微调栏/自检等页面脚本为自包含内联 JS，无运行时外部依赖；skill 内所有命令均用相对路径，Windows / macOS / Linux 通用
