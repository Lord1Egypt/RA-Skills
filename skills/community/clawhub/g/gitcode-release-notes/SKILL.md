---
name: gitcode-release-notes
description: "Generate release notes for GitCode repositories from commits (by tag range or since-date), grouped as feat/fix/docs/other, output Markdown for Release pages. 按 tag 区间或日期拉取提交并生成版本发布公告 Markdown。Python 3.7+ standard library only."
metadata: {"openclaw": {"requires": {"env": ["GITCODE_TOKEN"]}, "primaryEnv": "GITCODE_TOKEN"}}
---

# GitCode 版本发布公告（Release Notes）

根据 **GitCode API** 拉取仓库在指定区间内的提交。**脚本仅负责获取 commit 与简单过滤**；**你**根据脚本输出的 JSON **总结、归类、润色并生成最终 release note**，输出为 **Markdown 格式**，使阅读清晰、像人写的发布说明。

## 何时使用

- 用户表达「生成 release notes」「版本发布说明」「从 v1.0 到现在的更新日志」「从某日期到现在的提交记录」等意图。
- **必须**在本次对话中提供 **`--repo owner/repo`**（必传）；可选提供 `--branch`、`--from`、`--to`、`--since-date`。

## 认证

**GITCODE_TOKEN**：按以下优先级读取。

| 优先级 | 来源 |
|--------|------|
| 1 | 进程环境变量 `GITCODE_TOKEN` |
| 2 | Windows 用户级环境变量 |
| 3 | Windows 系统级环境变量 |

- Linux/macOS：建议在 `~/.bashrc` 或 `~/.zshrc` 中 `export GITCODE_TOKEN="..."`。
- 未配置时：脚本报详细错误，提示到 [GitCode 个人访问令牌](https://gitcode.com/setting/token-classic) 创建并设置环境变量。

## 路径约定

- **技能根目录**（`SKILL_ROOT`）：本 SKILL.md 所在目录。脚本通过 `__file__` 定位，**不依赖当前工作目录**。
- 支持 **Linux / macOS / Windows**；执行时使用脚本**绝对路径**。

## 固化流程

1. **解析参数**：从用户输入或对话中提取 `--repo`（必传）、`--branch`、`--from`、`--to`、`--since-date`。
2. **调用脚本（输出 JSON）**：
   ```bash
   python <SKILL_ROOT>/scripts/release_notes.py --repo owner/repo --json [--branch BRANCH] [--from TAG] [--to TAG] [--since-date YYYY-MM-DD]
   ```
   - **必须带 `--json`**：脚本只做拉取与简单过滤，向 stdout 输出 **JSON**，不生成最终 Markdown。
   - 区间三选一：`--since-date`（从该日 00:00 上海时间至今）、`--from`（从某 tag 至今）、或 `--from` + `--to`（两 tag 之间）。
   - `--branch` 未传时：脚本依次尝试 **master → develop → main**，都不存在则报错并提示使用 `--branch`。
3. **读取 JSON**：从 stdout 解析 JSON。若退出码非 0 或 stderr 有错误信息，向用户展示**详细错误**并结束。
4. **生成最终 release note**：
   - 根据 JSON 中的 `commits` 做**归类**（新特性 / 修复 / 文档 / 其他）、**总结**（每条或每组用简要概括，不要直接贴 commit 原文）、**润色**（统一语言、合并同类、去掉无信息量项），生成干净、专业、可对外发布的 release note。
   - 按 **「最终 release note 输出格式」** 与 **「撰写原则」** 写出 Markdown（标题、四小节、每条仅写简要说明；不展示 commit 信息；不展示合并条数/测试/合规等无价值信息）。
   - 交付给用户（可保存为文件或粘贴到 GitCode Release）。
5. **禁止**：不得在未得到脚本 JSON 前猜测或伪造数据；不得将 commit 列表原样当作最终 release note 交付，**须经总结与润色后**再交付。其余禁止事项见「禁止」一节。

## 脚本参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--repo` | 是 | 仓库，格式 `owner/repo` |
| `--json` | 必带（本技能调用时） | 脚本输出 JSON（仅拉取+简单过滤），由你总结并生成最终 release note |
| `--branch` | 否 | 分支；未传时自动尝试 master → develop → main |
| `--since-date` | 否 | 从该日期 00:00（Asia/Shanghai）至今的提交 |
| `--from` | 否 | 起始 tag（到当前 HEAD 或到 `--to`） |
| `--to` | 否 | 结束 tag，与 `--from` 一起表示区间 |
| `--max-per-category` | 否 | 仅在不使用 `--json` 时生效，每类最多展示条数，默认 10 |

- 区间约定：仅用 `--since-date`、或仅用 `--from`、或 `--from` + `--to`。若同时传多种，脚本按 `--since-date` > `--from/--to` 优先级处理。
- 本技能流程下**须带 `--json`**（以获取 JSON 供你总结）；**不带 `--json` 时脚本会直接输出 Markdown**，不经过本技能总结步骤。

## 脚本 --json 输出与你的职责

- **脚本**：仅获取 commit 与简单过滤（排除空 message、纯 merge），向 stdout 输出 JSON；不做归类、不写总结。
- **你**：从 stdout 解析 JSON，根据 `commits` 与 `stats` 做归类、简要概括、润色，按「最终 release note 输出格式」与「撰写原则」写出 Markdown；不得原样罗列 commit。

## 最终 release note 输出格式（须统一遵守）

生成 Markdown 时**必须**按以下格式；每条条目的**简要说明**根据 commit 进行归纳。

1. **标题**：`# owner/repo Release Notes（版本区间）`，或使用 JSON 中的 `title_line` 作为二级标题（如 `## v1.1.0 (YYYY-MM-DD)`）时，一级标题可为 `# owner/repo Release Notes`。
2. **小节顺序与标题**（有内容的才输出，顺序不可调换）：
   - `### 🚀 新特性`
   - `### 🐛 修复`
   - `### 📚 文档`
   - `### 🔧 其他更改`
3. **每条条目格式**：`- 简要说明`。简要说明由你根据该 commit 归纳；**不展示 commit 哈希或链接**。
4. **其他更改**：仅保留对用户/使用方有感知的架构或能力类变更；**不展示**「合并与依赖更新（共 N 条）」；若无实质内容可省略该小节或仅 1～2 条。
5. **每类条数**：新特性、修复、文档、其他更改**每类最多 10 条**；优先保留对用户价值最高、最易理解的条目，超出时合并同类或略去次要项。
6. **语言**：小节标题与条目说明统一用中文；专有名词、仓库名可保留英文。

## 撰写原则（保证输出质量）

面向非核心研发（测试、产品、运维等）可快速抓取重点，避免信息过载与内部黑话。

- **精简粒度**：按能力/模块合并同类项，单条不堆砌多个无关功能；新特性可按「硬件与拓扑 / 调度 / 设备与插件 / 高可用 / 推理与运维」等维度归纳；修复中不同问题应拆条或按类合并，避免一条里混杂多个无关 bug。
- **术语统一**：同一概念全文统一表述（同一术语不混用不同拼写）；专业缩写首次出现时可加括号简要说明；避免仅内部使用的缩写直接出现在对外 release note 中。
- **不展示无价值信息**：不展示「合并与依赖更新（共 N 条）」；不体现测试用例、用例补充；不体现合规；不体现内部细节（如 cleancode、codecheck、DT、若干内部 bug 修复）。
- **聚焦价值**：只保留对用户/使用方有意义的变更；模糊表述（如仅写「逻辑优化」）应并入具体能力描述或略去；长句适当缩短，条目分行清晰。
- **每条简短可扫读**：每条尽量**一句话、一个要点**，避免用分号/顿号在一句里堆砌多个功能或修复；可参考成熟开源社区（如 Kubernetes、VS Code）的 release note 风格——简短、易扫读，读者几秒内能抓重点。

## 输出示例（Markdown）

```markdown
# owner/repo Release Notes（v1.0.0 → v1.1.0）

### 🚀 新特性
- 新增 XXX 支持，兼容 A 与 B 场景。
- 支持从配置文件加载集群拓扑。

### 🐛 修复
- 修复 namespace 与任务名相同时的匹配错误。
- 修复日志打印重复与级别丢失问题。
- 修复包含 init 容器时的配置生成问题。

### 📚 文档
- 更新依赖源说明。

### 🔧 其他更改
- 设备 ID 体系与资源管理实现与重构。
- 故障码与知识库、路径诊断等能力补充与优化。
```

## 禁止

- 禁止在未得到脚本输出（JSON）前猜测或伪造数据。
- 禁止在未配置 `--repo` 时执行脚本（必须提示用户提供 `--repo`）。
- 禁止将脚本 JSON 中的 commit 列表原样当作最终 release note 交付（须经你总结、归类、润色后输出 Markdown）。
- 禁止直接复制 commit 原文，必须重新总结、改写。
- 禁止出现任何 commit 链接、commit ID、git 地址。
- 禁止罗列零散 fix，同类问题必须合并成一条。
- 只保留对用户/使用方有意义的内容，去掉内部调试、分支合并、过于细碎的文档改动等无关信息。
- 禁止展示「合并与依赖更新（共 N 条）」；禁止体现测试用例、出海与合规、cleancode/codecheck/DT/内部 bug 等内部细节。

## 示例

| 用户意图 | 命令（须带 --json） |
|----------|---------------------------|
| 从 v1.0.0 到当前 | `python <S> --repo owner/repo --json --from v1.0.0` |
| 从 v1.0.0 到 v1.1.0 | `python <S> --repo owner/repo --json --from v1.0.0 --to v1.1.0` |
| 从 2026-01-08 至今（上海时间） | `python <S> --repo owner/repo --json --since-date 2026-01-08` |
| 指定分支 | `python <S> --repo owner/repo --json --since-date 2026-01-08 --branch main` |

其中 `<S>` 为 `<SKILL_ROOT>/scripts/release_notes.py` 的绝对路径。不带 `--json` 时脚本会直接输出 Markdown，不经过本技能总结步骤。

## 历史版本

**v1.0.0** (2026-03-11)
- 🎉 初始版本发布
- 📖 支持按 tag/日期生成 Release Notes Markdown
