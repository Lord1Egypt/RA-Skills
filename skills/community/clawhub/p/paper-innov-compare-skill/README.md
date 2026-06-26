# 多论文创新点对比 Skill

`multi-paper-innovation-comparator` 是一个用于批量阅读和对比多篇论文创新点的 AI agent skill。它适合处理一个论文文件夹中的多篇 PDF、Markdown 或文本论文，逐篇读取未处理过的论文，总结每篇论文的主要工作、创新点、实验结果和工作量，并持续与已读论文进行横向对比，最终生成一个 `summ.md` 文档。

该 skill 的核心目标是帮助研究者从一组相关论文中提炼：

- 每篇论文的研究问题、主要方法、创新点和工作量；
- 不同论文之间的相似处、差异和可互补之处；
- 需要回读两篇或多篇论文后才能判断的融合研究方向；
- 可用于开题、综述、论文选题或后续仿真的进一步创新点。

默认情况下，生成的 `summ.md`、`paper_summ_state.json` 和 `extracted_text/` 会放在用户提供的论文所在文件夹中。如果 AI agent 无法确定论文文件夹，应先询问用户提供论文文件夹路径。

## 文件结构

```text
multi-paper-innovation-comparator/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── paper_summ.py
```

## 使用方式

在支持 skills 的 AI 工具中，向 agent 提出类似请求：

```text
Use $multi-paper-innovation-comparator to compare innovations across papers in F:\文献\方向\NonStationary and produce a summ document.
```

或中文：

```text
使用 multi-paper-innovation-comparator skill，读取 F:\文献\方向\NonStationary 中的论文，逐篇总结创新点并生成 summ.md。
```

该 skill 会要求论文数量不超过 20 篇。支持的文件类型包括：

- `.pdf`
- `.txt`
- `.md`

## 安装到 Codex

Codex 默认会从用户的 skills 目录发现 skill。将整个 `multi-paper-innovation-comparator` 文件夹复制到：

```text
Windows: C:\Users\<用户名>\.codex\skills\multi-paper-innovation-comparator
macOS/Linux: ~/.codex/skills/multi-paper-innovation-comparator
```

安装后，重启 Codex 或开启新会话，使 skill 被重新发现。

如果你已经在本机创建了该 skill，当前路径通常是：

```text
C:\Users\zhangxiuyu\.codex\skills\multi-paper-innovation-comparator
```

## 安装到 Claude Code

Claude Code 的 skills 目录通常位于用户主目录下的 Claude 配置目录。将整个 `multi-paper-innovation-comparator` 文件夹复制到 Claude Code 可读取的 skills 目录，例如：

```text
Windows: C:\Users\<用户名>\.claude\skills\multi-paper-innovation-comparator
macOS/Linux: ~/.claude/skills/multi-paper-innovation-comparator
```

如果你的 Claude Code 使用项目级 skills，也可以将该文件夹放入项目中的 skills 目录，并在会话中明确要求：

```text
Use $multi-paper-innovation-comparator to analyze the papers in <paper-folder>.
```

安装后，重启 Claude Code 或开启新会话。

## 安装到 OpenCode

OpenCode 或其他兼容 agent 工具通常也可以通过本地 skills 目录加载 `SKILL.md`。将整个文件夹复制到对应工具的 skills 目录，例如：

```text
Windows: C:\Users\<用户名>\.opencode\skills\multi-paper-innovation-comparator
macOS/Linux: ~/.opencode/skills/multi-paper-innovation-comparator
```

如果 OpenCode 使用项目级配置，可将该文件夹放入项目的 `.opencode/skills/` 或工具文档指定的 skill 搜索路径中。

安装后，在新会话中调用：

```text
Use $multi-paper-innovation-comparator to compare papers in <paper-folder>.
```

## 手动运行脚本

该 skill 附带 `scripts/paper_summ.py`，用于管理论文列表、抽取文本、记录处理状态和写入 `summ.md`。

初始化论文文件夹：

```bash
python scripts/paper_summ.py init "<paper-folder>"
```

查看下一篇未处理论文：

```bash
python scripts/paper_summ.py next "<paper-folder>"
```

写入某篇论文总结：

```bash
python scripts/paper_summ.py add-paper "<paper-folder>" --paper-id P001 --summary-file "<summary.md>"
```

写入跨论文综合创新点：

```bash
python scripts/paper_summ.py add-synthesis "<paper-folder>" --title "<title>" --papers "P001,P002" --summary-file "<synthesis.md>"
```

检查完成状态：

```bash
python scripts/paper_summ.py finalize "<paper-folder>"
```

## 注意事项

- 论文文件夹中支持文件数量不能超过 20 篇。
- 默认输出文件会写入论文所在文件夹。
- 如果论文文件夹不可访问、路径不存在或未提供，agent 应先询问用户。
- PDF 文本抽取效果取决于 PDF 本身质量；扫描版 PDF 可能需要先 OCR。
- 最终 `summ.md` 应优先使用中文撰写，除非用户要求其他语言。
