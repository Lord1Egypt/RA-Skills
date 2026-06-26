# MATLAB Simulation Optimizer

`matlab-simulation-optimizer` 是一个用于审计和优化 MATLAB 仿真程序的 Agent Skill。它会把本地 MATLAB 仿真源码与对应论文、规范或算法说明进行逐项对照，检查系统模型、算法流程、参数设置、迭代条件、停止准则、评价指标和实验结果映射是否一致，并在保持论文硬性条件不变的前提下直接优化源码。

该 skill 适合用于以下任务：

- 对照论文检查 MATLAB 仿真程序是否忠实复现论文模型、算法和实验设置。
- 修复论文与代码不一致的问题，例如参数、维度、噪声/SNR 映射、收敛条件、指标定义、基线算法或图表输出。
- 优化 MATLAB 程序运行速度，例如预分配数组、减少重复计算、避免不必要的矩阵求逆、缓存 Monte Carlo 不变量、移动循环内绘图或 I/O。
- 清理无用注释、死代码、旧绘图逻辑、重复结果输出、未使用函数和陈旧保存逻辑。
- 生成中文 `optimization_summary.md`，记录修改清单、论文条件核对、仿真结果与主函数映射、验证命令和剩余风险。

## 目录结构

```text
matlab-simulation-optimizer/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── matlab-audit-checklist.md
└── scripts/
    └── matlab_static_scan.py
```

关键文件说明：

- `SKILL.md`: skill 的核心说明，AI 工具会根据 frontmatter 中的 `name` 和 `description` 判断何时加载该 skill。
- `references/matlab-audit-checklist.md`: MATLAB 仿真审计检查表，用于细化论文-代码一致性核对。
- `scripts/matlab_static_scan.py`: MATLAB 静态扫描脚本，用于发现入口文件、函数调用、潜在性能热点和常见 MATLAB 风险模式。
- `agents/openai.yaml`: OpenAI/Codex 侧的界面元数据。

## 前置要求

- AI 工具需要能读取该 skill 文件夹。
- 如果要运行 MATLAB 仿真，需要本机安装 MATLAB；如果只做静态审计，则至少需要 MATLAB 源码和论文材料。
- 静态扫描脚本需要 Python 3。
- 安装时必须复制整个 `matlab-simulation-optimizer` 文件夹，而不是只复制 `SKILL.md`，否则引用文件和脚本会缺失。

## 下载或复制 Skill

如果该 skill 已经在本机：

```powershell
$SkillSource = "C:\Users\zhangxiuyu\.codex\skills\matlab-simulation-optimizer"
```

如果该 skill 放在 Git 仓库中，可以先克隆仓库，再复制其中的 skill 目录：

```bash
git clone <repo-url>
cd <repo-folder>
```

如果下载的是压缩包，解压后找到 `matlab-simulation-optimizer` 文件夹即可。最终目录中应当直接包含 `SKILL.md`，路径形如：

```text
matlab-simulation-optimizer/SKILL.md
```

## 安装到 Codex

Codex 会从用户级 skills 目录加载 skill。把整个文件夹复制到：

```text
Windows: %USERPROFILE%\.codex\skills\matlab-simulation-optimizer
macOS/Linux: ~/.codex/skills/matlab-simulation-optimizer
```

Windows PowerShell 示例：

```powershell
$Source = "C:\Users\zhangxiuyu\.codex\skills\matlab-simulation-optimizer"
$Target = "$env:USERPROFILE\.codex\skills\matlab-simulation-optimizer"
New-Item -ItemType Directory -Force (Split-Path $Target) | Out-Null
Copy-Item -Recurse -Force $Source $Target
```

安装后在 Codex 中可以这样触发：

```text
Use $matlab-simulation-optimizer to compare this MATLAB simulation folder with the paper, optimize the source code, and write the summary document.
```

中文触发示例：

```text
使用 matlab-simulation-optimizer，对照这篇论文审计并优化这个 MATLAB 仿真程序，保持论文算法条件不变，并生成中文优化总结。
```

## 安装到 Claude Code

Claude Code 的 skill 也是一个包含 `SKILL.md` 的文件夹。可以安装为用户级 skill，也可以安装为项目级 skill。

用户级安装路径：

```text
Windows: %USERPROFILE%\.claude\skills\matlab-simulation-optimizer
macOS/Linux: ~/.claude/skills/matlab-simulation-optimizer
```

项目级安装路径：

```text
<your-project>/.claude/skills/matlab-simulation-optimizer
```

Windows PowerShell 用户级安装示例：

```powershell
$Source = "C:\Users\zhangxiuyu\.codex\skills\matlab-simulation-optimizer"
$Target = "$env:USERPROFILE\.claude\skills\matlab-simulation-optimizer"
New-Item -ItemType Directory -Force (Split-Path $Target) | Out-Null
Copy-Item -Recurse -Force $Source $Target
```

macOS/Linux 示例：

```bash
mkdir -p ~/.claude/skills
cp -R ./matlab-simulation-optimizer ~/.claude/skills/
```

安装后重新打开 Claude Code，或在新会话中使用与 skill 描述匹配的请求。Claude Code 会在相关任务中自动加载该 skill，也可以在提示词中明确写：

```text
Use the matlab-simulation-optimizer skill to audit and optimize this MATLAB simulation against the attached paper.
```

## 安装到 OpenCode

OpenCode 支持 `SKILL.md` 风格的 Agent Skills。把整个文件夹复制到以下任一位置：

```text
全局 OpenCode: ~/.config/opencode/skills/matlab-simulation-optimizer
项目级 OpenCode: <your-project>/.opencode/skills/matlab-simulation-optimizer
全局 Claude 兼容: ~/.claude/skills/matlab-simulation-optimizer
项目级 Claude 兼容: <your-project>/.claude/skills/matlab-simulation-optimizer
全局 Agents 兼容: ~/.agents/skills/matlab-simulation-optimizer
项目级 Agents 兼容: <your-project>/.agents/skills/matlab-simulation-optimizer
```

macOS/Linux 全局安装示例：

```bash
mkdir -p ~/.config/opencode/skills
cp -R ./matlab-simulation-optimizer ~/.config/opencode/skills/
```

Windows PowerShell 示例：

```powershell
$Source = "C:\Users\zhangxiuyu\.codex\skills\matlab-simulation-optimizer"
$Target = "$env:USERPROFILE\.config\opencode\skills\matlab-simulation-optimizer"
New-Item -ItemType Directory -Force (Split-Path $Target) | Out-Null
Copy-Item -Recurse -Force $Source $Target
```

OpenCode 中可以这样使用：

```text
Use the matlab-simulation-optimizer skill to compare this MATLAB project with the paper and optimize it.
```

如果你更想把它做成可手动选择的 OpenCode agent，也可以创建 Markdown agent 文件，让 agent 的提示词引用该 skill。

用户级 agent 目录为：

```text
macOS/Linux: ~/.config/opencode/agents/
Windows: %APPDATA%\opencode\agents\ 或 %USERPROFILE%\.config\opencode\agents\
```

项目级 agent 目录通常为：

```text
<your-project>/.opencode/agents/
```

可以创建一个 `matlab-simulation-optimizer.md`：

```markdown
---
description: Audit and optimize MATLAB simulation programs against papers while preserving paper-mandated algorithm logic and parameters.
mode: primary
tools:
  write: true
  edit: true
---

You are a MATLAB simulation optimization agent.

Follow the workflow in the matlab-simulation-optimizer skill. When available, read:
- <path-to-skill>/SKILL.md
- <path-to-skill>/references/matlab-audit-checklist.md

Use <path-to-skill>/scripts/matlab_static_scan.py for static scanning when useful.

Always preserve paper-mandated model, algorithm, parameters, iteration rules, stopping criteria, metrics, and simulation settings. Write a Chinese optimization_summary.md in the MATLAB source root.
```

把 `<path-to-skill>` 替换成实际路径，例如：

```text
C:\Users\zhangxiuyu\.codex\skills\matlab-simulation-optimizer
```

## 验证安装

安装后，向 AI 工具发送一个小型检查请求：

```text
请确认你能看到 matlab-simulation-optimizer skill，并概述它需要哪些输入材料。不要修改文件。
```

期望回答应包含：

- 需要论文或规范材料。
- 需要 MATLAB 程序目录或 `.m` 文件。
- 会对照论文硬性条件和代码实现。
- 会区分正确性修复、性能优化、清理和可复现性改动。
- 默认生成中文 `optimization_summary.md`。

## 使用建议

为了让该 skill 更稳定地工作，建议一次性提供：

- 论文 PDF、DOI、URL 或正文。
- MATLAB 源码根目录。
- 需要复现或优化的论文图、表、指标。
- MATLAB 是否可用、是否允许 Octave、是否有 Parallel Toolbox 或 GPU。
- 当前最慢的脚本、报错信息或运行日志。

示例请求：

```text
使用 matlab-simulation-optimizer，对照 paper.pdf 审计 C:\work\sim 里的 MATLAB 仿真程序。
请修复与论文不一致的地方，优化运行速度，但不要改变论文规定的 Monte Carlo 次数、SNR 网格、迭代停止条件和指标定义。
最后在源码目录写一份中文 optimization_summary.md。
```

## 注意事项

- 不要为了提速擅自降低 Monte Carlo 次数、缩短 SNR 网格、改变最大迭代次数或放宽收敛阈值。
- 不要把论文算法替换成其他算法；只有数学等价的优化才应直接合入。
- 删除代码前必须确认它不参与任何论文结果、验证路径或共享函数调用。
- 如果 MATLAB 不可用，skill 应进行静态验证，并给出用户可运行的 MATLAB 命令。

## 参考文档

- Claude Code Skills: https://docs.claude.com/en/docs/claude-code/skills
- Claude Code SDK Skills discovery: https://code.claude.com/docs/en/agent-sdk/skills
- OpenCode Agent Skills: https://opencode.ai/docs/skills/
- OpenCode agents: https://opencode.ai/docs/agents/
- OpenCode config: https://opencode.ai/docs/config/
