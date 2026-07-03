---
name: own-style-writer
description: |
  通用自有文风写作 skill。用于用户要求“按我的文章风格写”“学习某个目录里的文风”“把风格素材和本次写作素材分开处理”“从本地 PDF/DOCX/PPTX/Excel/HTML/文本等素材提炼文风并写文章”时。它会主动询问哪些目录用于学习写作风格、哪些材料只用于本次写作内容，优先在用户同意上传后用 MinerU 转换文档，也可回退内置 MarkItDown 离线转换；默认先生成风格画像、素材摘要和文章大纲，待确认后才写正文。
version: 1.3.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
        - py
        - wsl
    primaryEnv: MINERU_API_KEY
    envVars:
      - name: MINERU_API_KEY
        required: false
        description: Optional MinerU API key for precise document parsing. Get one from https://mineru.net/apiManage/docs.
      - name: MINERU_MODEL_VERSION
        required: false
        description: Optional MinerU precise model override. Defaults to vlm.
      - name: OWN_STYLE_WRITER_RUNTIME
        required: false
        description: Optional directory override for the reusable MarkItDown Python runtime.
      - name: AZURE_API_KEY
        required: false
        description: Optional variable referenced by vendored MarkItDown Azure converter; not used by the default workflow.
    skillKey: own-style-writer
    emoji: "✍️"
    homepage: https://github.com/snowles/own-style-writer
---

# Own Style Writer

Own Style Writer 是一个“学习指定文章风格，再按本次素材写作”的 skill。它不内置固定作者人格、固定口癖或默认语料。每次写作都必须以用户当次提供的风格素材为最高文风依据。

Inspired by khazix-writer, but contains no khazix-writer persona, corpus, prompts, or runtime dependency.

## First Ask

触发后先问清楚，不要把“风格素材”和“写作素材”混为一谈：

1. 哪一个目录是要学习文风的？
2. 哪些文件、目录、链接、粘贴内容或口述信息是本次写作用的素材？
3. 本次写作需求是什么：主题、目标读者、篇幅、输出语言、观点倾向、是否先给大纲？
4. 是否允许把本地文档上传到 MinerU 做高质量解析？
5. 是否已经设置 `MINERU_API_KEY`？
6. 是否已有历史 `写作复盘.md`，需要这次写作前读取？

如果用户没有 MinerU key，提示：

```text
如果你想使用 MinerU 精准解析，需要先获取 API Key：
https://mineru.net/apiManage/docs

没有 key 也可以继续：
1. 尝试 MinerU 轻量解析 API，适合 10MB / 20 页以内文件，受 IP 限频影响；
2. 或使用内置 MarkItDown 做本地离线转换。
```

## User Inputs

- **风格素材目录**：最好是一个文件夹，里面放用户想模仿文风的文章、PDF、Word、Markdown 等。只用于学习结构、节奏、语气、段落密度、开头结尾方式和表达禁忌。
- **写作素材**：可以是另一个文件夹、单个文件、链接、粘贴文本或用户口述需求。只用于事实、案例、数据、观点和背景信息，不自动学习其文风。
- **写作需求**：说明本次要写什么、写给谁、想多长、用什么语言、要不要保留某些观点或限制。

写作素材不参与文风学习，除非用户明确说“也参考这些素材的风格”。

## Conversion

优先转换策略：

1. 用户允许上传且设置了 `MINERU_API_KEY`：使用 MinerU 精准解析 API，默认模型 `vlm`，可用 `MINERU_MODEL_VERSION` 覆盖。
2. 用户允许上传但没有 key：尝试 MinerU 轻量解析 API，只适合 10MB / 20 页以内文件，受 IP 限频影响。
3. 用户不允许上传，或 MinerU 失败、超限、限频：使用内置 MarkItDown 本地离线转换。

转换入口：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_prepare_workspace.ps1 `
  -StyleDir "D:\writing\my-style-samples" `
  -ContentDir "D:\writing\topic-materials" `
  -OutputDir "D:\writing\workspace\.own-style-writer" `
  -Recursive
```

允许上传到 MinerU 时增加：

```powershell
-AllowUpload
```

macOS/Linux/WSL：

```bash
scripts/run_prepare_workspace.sh "/path/to/style-samples" "/path/to/topic-materials" --recursive --allow-upload
```

也可直接运行 Python：

```bash
python3 scripts/prepare_writing_workspace.py \
  --style-dir "/path/to/style-samples" \
  --content-dir "/path/to/topic-materials" \
  --output-dir "/path/to/output/.own-style-writer" \
  --converter auto \
  --recursive
```

## Outputs

转换脚本保留可复查产物：

- `style/converted/*.md`
- `style/corpus.md`
- `content/converted/*.md`
- `content/corpus.md`
- `style_corpus.md`
- `content_corpus.md`
- `manifest.json`
- `conversion_errors.json`

`manifest.json` 每条记录包含 `role`、`source`、`output`、`status`、`extension`、`bytes`、`characters`、`converter`、`converter_mode`、`error`。

后续由 Agent 生成：

- `style_profile.md`：只从 `style/corpus.md` 提炼文风。
- `content_brief.md`：只从 `content/corpus.md` 和用户粘贴/口述内容提炼事实素材。
- `outline_review.md`：结合文风画像和写作素材生成待确认大纲。
- `draft.md`：用户确认大纲后才生成。
- `quality_report.md`：检查文风贴合、素材使用和事实风险。
- `写作复盘.md`：根据用户后续修改意见沉淀可复用避错规则。

## Workflow

1. 确认风格素材、写作素材、写作需求、MinerU 上传许可和 key 状态。
2. 运行转换脚本，保留所有中间产物。
3. 阅读 `manifest.json`，确认转换成功率和失败项。
4. 阅读 `style/corpus.md`，参考 `references/style_profile_template.md` 生成 `style_profile.md`。
5. 阅读 `content/corpus.md`，参考 `references/content_brief_template.md` 生成 `content_brief.md`。
6. 阅读 `references/writing_principles.md`，把通用章法原则翻译成当前题材可用的结构建议。
7. 如果输出目录或用户提供路径中已有 `写作复盘.md`，先读取并提取本次需要避免的问题。
8. 参考 `references/outline_review_template.md` 生成 `outline_review.md`，展示给用户确认。
9. 用户确认后，再根据 `style_profile.md`、`content_brief.md`、`写作复盘.md` 和已确认大纲写 `draft.md`。
10. 参考 `references/quality_check_template.md` 生成 `quality_report.md`。
11. 如果用户后续提出修改意见，参考 `references/写作复盘模板.md` 更新 `写作复盘.md`。

默认停在大纲确认阶段，不要第一轮直接写完整正文，除非用户明确说“跳过大纲确认，直接写”。

## General Writing Principles

无论参考风格是什么，写作时都要保留基本章法和逻辑底线。生成 `outline_review.md` 前阅读 `references/writing_principles.md`，并检查：

- 标题是否准确、精练、醒目，能反映主题和核心判断。
- 开头是否开门见山，尽快交代基本意图或核心问题。
- 正文是否内容充实、层次清楚，围绕主题分段展开。
- 结尾是否干净利索，有方向性、结论性、建议性、鼓励性或希望性。
- 全文是否前后照应，详略得当，概念统一，重点突出。
- 文风是否做到短、新、实、特：简短、有新意、具体实在、有辨识度。

这些原则是写作质量建议，不是固定文风。不要把所有文章写成机关文稿；要把原则转译为当前题材、用户需求和风格语料适用的表达方式。如果风格语料故意采用特殊结构，优先尊重用户风格，同时在大纲或质检里提示它可能带来的结构风险。

## Writing Review Memory

`写作复盘.md` 是用户自己的长期避错清单。它用于记录“这次哪里写得不好、用户怎么改、下次如何避免”，帮助后续写作不重复犯错。

- 如果用户提供了 `写作复盘.md`，生成大纲和正文前必须先读。
- 如果当前输出目录里已经有 `写作复盘.md`，默认读取它。
- 如果没有复盘文件，但用户在改稿时给了明确修改意见，创建 `写作复盘.md`。
- 复盘只记录可复用问题，例如标题空泛、开头绕、事实没用足、语气不像、段落太散、观点不够鲜明。
- 不要把一次性素材、私人信息、客户未公开要求或完整正文大量写入复盘；只记录抽象后的避错规则。
- 复盘不能覆盖当次风格素材。如果复盘规则与当前风格语料冲突，在 `outline_review.md` 里说明冲突，让用户确认。
- `references/写作复盘模板.md` 是模板；实际复盘文件应放在用户的输出目录或长期写作目录中。

## Style Extraction

提炼文风时不要只总结主题内容，要写成可执行约束。重点观察：

- 开头如何启动：叙事、判断、问题、场景、金句、新闻事实，还是直接抛结论。
- 文章结构：线性推进、分节论证、清单式、故事弧、评论式、研究式、问答式。
- 段落密度：长段还是短段，单句成段是否高频。
- 句式节奏：长短句比例、停顿方式、转折方式、是否爱用反问。
- 论证方式：案例、数据、经验、类比、引用、复盘、情绪判断。
- 视角和姿态：旁观者、亲历者、导师、朋友、研究员、评论员、交易员、编辑部口吻。
- 用词习惯：高频词、口头禅、行业术语、情绪词、连接词。
- 格式习惯：标题层级、编号、加粗、引用、表格、括号、标点。
- 禁忌：参考文章明显不用或很少用的表达方式。
- 结尾方式：回扣开头、给判断、留悬念、行动建议、风险提示、情绪收束。

不要写“语言生动”这种泛泛评价；要写“每个核心判断后通常跟一个短句解释，并用口语转折把节奏拉回来”这类可执行规则。

## Drafting Rules

写正文时严格依据 `style_profile.md`、`content_brief.md` 和已确认的 `outline_review.md`：

- 不套用任何固定作者人格。
- 不继承旧 skill 的固定口癖、固定尾巴或固定价值观。
- 不把写作素材的风格误当成目标文风。
- 不编造第一手经历、数据、引用或具体事实。
- 用户没有提供的信息，用“需要补充”或保守表达处理。
- 如果素材涉及财经、医疗、法律等高风险领域，避免给出确定性操作指令，并提醒用户核验关键事实。
- 如果用户要求直接发布稿，仍要附简短 `quality_report.md`，说明哪些风格特征已对齐、哪些事实仍需人工确认。

## Runtime Notes

MinerU 精准解析需要 `MINERU_API_KEY`。设置示例：

```powershell
$env:MINERU_API_KEY="你的key"
[Environment]::SetEnvironmentVariable("MINERU_API_KEY","你的key","User")
```

```bash
export MINERU_API_KEY="你的key"
```

内置 MarkItDown 位于 `vendor/markitdown`。首次需要 fallback 到 MarkItDown 时，`scripts/bootstrap_markitdown.py` 会自动创建可复用 Python runtime，并按文件类型安装所需依赖。

默认 runtime 位置：

- Windows: `%LOCALAPPDATA%\own-style-writer\runtime`
- Linux/WSL/macOS: `~/.cache/own-style-writer/runtime`

如果不能写用户缓存目录，设置 `OWN_STYLE_WRITER_RUNTIME` 到一个可写目录。
