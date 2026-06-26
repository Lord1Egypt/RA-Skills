# paper-matlab-reproduction

`paper-matlab-reproduction` 是一个用于“论文 MATLAB 仿真复现”的 AI 工具 skill。它面向需要根据论文 PDF、论文 URL、DOI 或 arXiv 链接自动梳理论文算法、提取仿真参数、生成 MATLAB 代码、运行仿真并对比论文结果的场景。

## Skill 描述

这个 skill 的目标不是简单地“读论文写代码”，而是建立一条可追溯的复现证据链：

1. 读取用户提供的论文文件地址。
2. 提取论文标题、系统模型、算法图表、仿真设置、结果图表和参考文献。
3. 根据论文中的算法图、算法表或流程图生成算法伪代码；有几个算法图表，就生成几个伪代码。
4. 按固定优先级查找参数：
   - 先查仿真结果或实验设置部分。
   - 再查图注、表注、算法描述和附录。
   - 再查被引用文献。
   - 如果仍找不到，则根据论文内容推断，并明确告知用户该参数是推断值。
5. 如果算法步骤引用其他论文中的操作，优先通过 Google Scholar 查找对应论文并读取所需操作定义。
6. 根据系统模型、算法伪代码和参数设置生成 MATLAB 仿真代码。
7. 将系统模型、仿真循环、对比指标和绘图逻辑放在 `main.m` 或多个 `main_<环境差异>.m` 中。
8. 一个算法伪代码对应一个 `.m` 函数文件。
9. 运行所有主函数，将仿真结果与论文结果对比。
10. 如果结果差异明显，最多自动诊断并优化 MATLAB 代码 3 次。
11. 输出 MATLAB 代码、中文说明文档、参数表、伪代码、引用操作说明、复现日志和相似度报告。

## 适用场景

适合这些请求：

- “帮我复现这篇论文的 MATLAB 仿真代码。”
- “根据这个 PDF 生成通信论文的仿真程序。”
- “把论文里的算法图转成伪代码和 MATLAB 函数。”
- “复现论文 Fig. 3 和 Fig. 4 的仿真结果。”
- “论文算法引用了其他文献，请把引用操作也补全后生成代码。”

## 输入要求

用户至少需要提供论文来源之一：

- 本地 PDF 路径
- 在线 PDF URL
- DOI
- arXiv 链接
- 已上传的论文文件

默认情况下，生成的 MATLAB 代码和中文说明文档会放在论文文件所在的文件夹中。如果 AI 工具无法识别论文所在文件夹，或该文件夹不可写，应先询问用户提供输出目录。

## 输出内容

默认输出结构类似：

```text
paper-title-reproduction/
├── main.m
├── main_<环境差异>.m
├── alg1_<算法名>.m
├── alg2_<算法名>.m
├── helpers/
├── data/
├── results/
│   ├── figures/
│   └── metrics/
├── paper_artifacts/
│   ├── pseudocode.md
│   ├── parameter_table.csv
│   ├── citation_operations.md
│   └── target_results.md
└── reproduction_log.md
```

所有面向用户的描述文档默认使用中文，包括伪代码说明、参数说明、引用文献操作说明、运行说明、复现日志和最终报告。

## 下载或安装到 AI 工具

### 方式一：复制整个 skill 文件夹

将整个 `paper-matlab-reproduction` 文件夹复制到目标 AI 工具的 skills 目录中。

当前 skill 目录结构应类似：

```text
paper-matlab-reproduction/
├── SKILL.md
├── README.md
├── evals/
└── references/
```

复制时要保留整个文件夹，而不是只复制 `SKILL.md`。

## 安装到 Codex

Codex 默认可以从下面的目录加载用户 skill：

```text
C:\Users\zhangxiuyu\.codex\skills
```

安装方式：

```powershell
Copy-Item -Recurse -Force `
  "path\to\paper-matlab-reproduction" `
  "C:\Users\zhangxiuyu\.codex\skills\paper-matlab-reproduction"
```

如果当前已经位于该目录，则无需重复安装。之后在 Codex 中可以这样调用：

```text
调用 paper-matlab-reproduction 复现论文 "D:\papers\example.pdf" 中的 MATLAB 仿真代码
```

或：

```text
使用 paper-matlab-reproduction，根据这篇论文生成 MATLAB 复现代码
```

## 安装到 Claude Code

Claude Code 的 skill 目录通常位于：

```text
~/.claude/skills
```

在 Windows PowerShell 中可以复制到：

```powershell
Copy-Item -Recurse -Force `
  "path\to\paper-matlab-reproduction" `
  "$env:USERPROFILE\.claude\skills\paper-matlab-reproduction"
```

在 macOS 或 Linux 中可以使用：

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/paper-matlab-reproduction ~/.claude/skills/
```

安装后，在 Claude Code 中可以用自然语言触发：

```text
Use paper-matlab-reproduction to reproduce this paper in MATLAB: /path/to/paper.pdf
```

中文也可以：

```text
调用 paper-matlab-reproduction，复现 /path/to/paper.pdf 的仿真代码
```

## 安装到 OpenCode

OpenCode 的 skill 支持方式可能随版本和配置不同而变化。常见做法是将 skill 放到 OpenCode 可读取的自定义 skill 或 agent instructions 目录中，并确保 `SKILL.md` 能被工具加载。

推荐方式：

1. 找到 OpenCode 的自定义 skill、agent 或 prompt 目录。
2. 将整个 `paper-matlab-reproduction` 文件夹复制进去。
3. 在 OpenCode 的配置文件中注册或引用该目录。
4. 在会话中明确要求使用该 skill。

示例提示词：

```text
Use the paper-matlab-reproduction skill. The paper path is /path/to/paper.pdf. Generate MATLAB reproduction code and Chinese documentation.
```

如果当前 OpenCode 版本没有原生 skill 机制，可以把 `SKILL.md` 内容作为项目级 instructions 或 agent prompt 引入。

## 安装到其他 AI 工具

对于支持“自定义技能、工具说明、项目规则、agent instructions、system prompt 扩展”的 AI 工具，通用安装方法是：

1. 创建一个名为 `paper-matlab-reproduction` 的 skill 或 instruction 目录。
2. 将 `SKILL.md` 放入该目录。
3. 保留 `references/` 和 `evals/`，方便工具读取补充说明和测试用例。
4. 在工具配置中启用该目录。
5. 使用时明确说明“调用 paper-matlab-reproduction”。

## 使用示例

```text
调用 paper-matlab-reproduction 复现论文 "F:\文献\URA.pdf" 中的仿真代码。
```

```text
使用 paper-matlab-reproduction，根据 arXiv:xxxx.xxxxx 生成 MATLAB 仿真代码，并对比论文 Fig. 2 和 Fig. 3。
```

```text
请用 paper-matlab-reproduction 读取这个 PDF，提取所有算法图表，生成伪代码和对应 MATLAB 函数。
```

## 注意事项

- 如果论文没有给出完整参数，skill 会按规则推断，并在报告中标明。
- 如果论文没有提供原始曲线数据，只能先做趋势级复现；点对点相似度需要用户提供原始数据或允许图像曲线数字化。
- 如果本机没有可用 MATLAB license，skill 会生成代码和运行说明，但不能完成本地仿真与自动修正。
- 如果需要读取 Google Scholar 或论文引用来源，AI 工具需要具备联网或浏览器检索能力。
