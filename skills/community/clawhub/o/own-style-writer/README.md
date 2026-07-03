# Own Style Writer

Own Style Writer 是一个“按你的参考文风写作”的 Agent Skill。它会把**要学习文风的材料**和**本次写作用的内容素材**分开处理：前者决定文章怎么写，后者决定文章写什么。

Inspired by khazix-writer, but contains no khazix-writer persona, corpus, prompts, or runtime dependency.

## 快速使用

把下面这段发给 Agent，把路径和需求换成你自己的：

```text
使用 own-style-writer。

风格素材目录：
D:\你的\风格文章目录

写作素材：
D:\你的\本次写作素材目录

写作需求：
请学习风格素材目录里的文风，但只使用写作素材里的事实和案例，帮我写一篇关于 XXX 的文章。先给文风总结和大纲，不要直接写正文。

转换方式：
如果我允许上传并且有 MINERU_API_KEY，就优先用 MinerU；否则用本地 MarkItDown。

写作复盘：
如果这个目录里有 写作复盘.md，请先读取，避免重复犯以前的问题。
```

简单理解：

- **风格素材**：想让文章“像谁”的材料。
- **写作素材**：这次文章“写什么”的材料。
- **MinerU**：PDF 转 Markdown 效果更好，但会上传文件，需要你同意。
- **MarkItDown**：本地离线转换，不上传文件。
- **写作复盘.md**：记录以前改稿时暴露的问题，下次写作前先读，避免重复犯错。
- 默认会先给你看大纲，确认后才写正文。

## 你需要准备什么

1. **风格素材目录**

   放你想让 Agent 学习文风的文章。最好是一个文件夹，里面可以有 PDF、Word、Markdown、TXT、PPT、Excel、HTML 等。这个目录只用来学习结构、节奏、语气、段落密度、开头结尾和表达习惯。

2. **写作素材**

   放本次文章要使用的事实、案例、数据、观点和背景资料。它可以是另一个文件夹、单个文件、链接、粘贴文本，或者你直接口述。默认不学习这些材料的文风。

3. **写作需求**

   说明主题、目标读者、篇幅、输出语言、观点倾向，以及是否先给大纲。

## MinerU API Key

PDF 解析优先使用 MinerU，效果通常比本地 MarkItDown 更好。使用 MinerU 精准解析需要 API Key：

https://mineru.net/apiManage/docs

设置方式：

PowerShell 临时设置：

```powershell
$env:MINERU_API_KEY="你的key"
```

Windows 持久设置：

```powershell
[Environment]::SetEnvironmentVariable("MINERU_API_KEY","你的key","User")
```

macOS / Linux / WSL：

```bash
export MINERU_API_KEY="你的key"
```

没有 key 也可以继续：

- 允许上传时，可尝试 MinerU 轻量解析 API，适合 10MB / 20 页以内文件，受 IP 限频影响。
- 不允许上传，或 MinerU 不可用时，会使用内置 MarkItDown 本地离线转换。

## 给 Agent 的使用示例

```text
使用 own-style-writer。

风格素材目录：
D:\writing\my-style-samples

写作素材目录：
D:\writing\topic-materials

写作需求：
帮我写一篇关于 XXX 的公众号长文，学习风格素材目录里的行文方式，但事实和案例只使用写作素材目录里的内容。先给文风总结和大纲，不要直接写正文。

MinerU：
我允许上传到 MinerU。
我已经设置 MINERU_API_KEY。
```

如果你没有 key，可以这样说：

```text
我没有 MINERU_API_KEY。可以先尝试 MinerU 轻量解析；不行就用 MarkItDown 本地转换。
```

如果你不想上传文件，可以这样说：

```text
不要上传到 MinerU，只用本地 MarkItDown 转换。
```

## 直接运行转换脚本

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_prepare_workspace.ps1 `
  -StyleDir "D:\writing\my-style-samples" `
  -ContentDir "D:\writing\topic-materials" `
  -OutputDir "D:\writing\workspace\.own-style-writer" `
  -Recursive
```

允许上传到 MinerU：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_prepare_workspace.ps1 `
  -StyleDir "D:\writing\my-style-samples" `
  -ContentDir "D:\writing\topic-materials" `
  -OutputDir "D:\writing\workspace\.own-style-writer" `
  -Recursive `
  -AllowUpload
```

macOS / Linux / WSL：

```bash
scripts/run_prepare_workspace.sh "/path/to/style-samples" "/path/to/topic-materials" --recursive --allow-upload
```

只用本地 MarkItDown：

```bash
scripts/run_prepare_workspace.sh "/path/to/style-samples" "/path/to/topic-materials" --recursive --converter markitdown
```

## 输出文件

转换后会生成：

- `style/converted/*.md`：风格素材转换结果。
- `style/corpus.md`：合并后的风格语料。
- `content/converted/*.md`：写作素材转换结果。
- `content/corpus.md`：合并后的写作素材语料。
- `manifest.json`：每个文件的来源、角色、转换器、状态和字符数。
- `conversion_errors.json`：失败项和具体错误。

Agent 后续会生成：

- `style_profile.md`：从风格语料提炼出的写作规则。
- `content_brief.md`：从写作素材提炼出的事实和观点摘要。
- `outline_review.md`：待确认大纲。
- `draft.md`：确认大纲后才生成的正文。
- `quality_report.md`：风格和事实检查。
- `写作复盘.md`：根据你的修改意见沉淀下次要避免的问题。

## 写作复盘

如果一篇稿子写出来不满意，后面改稿时可以让 Agent 把问题记到 `写作复盘.md`。下次再写时，Agent 先读这个文件，再生成大纲和正文。

你可以这样说：

```text
这次改稿意见请整理进 写作复盘.md：
1. 开头太绕，下次要直接切入主题。
2. 观点不够鲜明，下次先给核心判断。
3. 素材里的案例没有用足，下次每个重要判断后要跟一个具体例子。
```

复盘里只写可复用的避错规则，不要放完整正文、私人信息或未公开素材。模板见 `references/写作复盘模板.md`。

## 基本章法

文风可以学习你的参考文章，但一篇好文章仍然要有基本章法。Own Style Writer 会把标题、开头、正文、结尾和全文逻辑作为通用检查项：

- 标题要准确精练，点出主题和核心判断。
- 开头要尽快切入主题，不绕圈子。
- 正文要内容充实、层次清楚、重点突出。
- 结尾要干净有力，有结论、方向、建议、提醒或余味。
- 全文要前后照应，概念统一，详略得当，避免重复和一盘散沙。

你也可以直接要求：

```text
请在大纲和质检里同时按基本章法检查标题、开头、正文、结尾和逻辑。
```

## 安装

Codex 常见路径：

```powershell
git clone git@github.com:snowles/own-style-writer.git $env:USERPROFILE\.codex\skills\own-style-writer
```

macOS / Linux：

```bash
git clone git@github.com:snowles/own-style-writer.git ~/.codex/skills/own-style-writer
```

如果你的 Agent 支持从 GitHub 安装 skill，也可以让它安装：

```text
安装这个 skill：https://github.com/snowles/own-style-writer
```

## 注意事项

- MinerU 会把本地文档上传到第三方服务；Agent 应先明确征得你的同意。
- 写作素材默认只提供内容，不提供文风。
- MarkItDown 是内置离线 fallback，不依赖你本机另一个 MarkItDown 项目路径。
- 财经、医疗、法律等高风险内容需要人工核验关键事实。
