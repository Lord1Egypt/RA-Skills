---
name: gitcode-pr-audit
description: "Quality audit for merged GitCode PRs: sample by time range or repo list, check compliance (labels, comments, tests, size, etc.), output table. Use when user asks to 抽检/质量检查 已合入的 PR 规范性、多仓库 PR、或 将结果整理成表格. Multi-repo (owner/repo). Python 3.7+ stdlib only."
metadata: {"openclaw": {"requires": {"env": ["GITCODE_TOKEN"]}, "primaryEnv": "GITCODE_TOKEN"}}
---

# GitCode 合入 PR 质量抽检

对指定时间范围内合入主分支的 PR 进行抽检，按多维度判断质量并输出表格。支持多仓库、可配置阈值与必选标签，输出可写为 Markdown 或 CSV。

## 何时使用

- 用户表达以下任一意图时使用本 skill：
  - **规范性抽检/质量抽检**：如「对已合入的 PR 进行质量抽检」「最近 30 天合入的 PR 抽检」「已合入 PR 规范性检查」；
  - **多仓库/仓库列表**：如「对以下仓库的 PR 抽检」「对owner组织下某几个仓库的 PR 检查」；
  - **输出形式**：如「将抽检结果整理成表格」「输出表格形式」。
- 需提供 **至少一个仓库**（格式 `owner/repo`）；可多仓库、可选时间（默认最近 30 天）与分支、可选抽检数量或「全部」检查。

## 认证

**GITCODE_TOKEN**：按以下优先级读取。

| 优先级 | 来源 |
|--------|------|
| 1 | 进程环境变量 `GITCODE_TOKEN` |
| 2 | Windows 用户级环境变量 |
| 3 | Windows 系统级环境变量 |

- Linux/macOS：在 `~/.bashrc` 或 `~/.zshrc` 中 `export GITCODE_TOKEN="..."`。
- 未配置时：脚本报错并提示到 [GitCode 个人访问令牌](https://gitcode.com/setting/token-classic) 创建并设置环境变量。

## 路径与跨平台

- **技能根目录**（`SKILL_ROOT`）：本 SKILL.md 所在目录。脚本通过 `__file__` 定位，不依赖当前工作目录。
- 支持 **Linux / macOS / Windows**；执行时使用脚本**绝对路径**（如 `python <SKILL_ROOT>/scripts/pr_audit.py ...`）。

## 固化流程

1. **解析参数**：从用户输入提取 `--repo`（可多个）、`--pr`（可多个）、`--branch`、`--since`、`--until`、`--days`、`--all`、`--output` 等。
2. **调用脚本**：
   ```bash
   python <SKILL_ROOT>/scripts/pr_audit.py --repo owner/repo [--pr N] [--pr N2 ...] [--branch BRANCH] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--days N] [--all] [--output path.md|path.csv]
   ```
   - **指定 PR 时**：使用 `--pr N`（可多次）并**且仅指定一个** `--repo`，脚本只检查这些 PR，不按时间范围拉取。
   - 未指定 `--pr` 时：未指定时间则默认 **最近 30 天**（`--days 30`）；指定 `--since`/`--until` 则按用户时间。
   - 未指定分支时，每个仓库依次尝试 **master → develop → main**，都不存在则报错；指定则用指定分支，不存在则报错。
   - 未指定抽检数量时，**每个仓库**随机抽 **5～10 条**分析，不足 5 条则全部分析；用户明确「全部」或「所有」或传 `--all` 时，该时间范围内合入的 PR **全部**检查。
3. **读取结果**：脚本将**表格输出到 stdout**（Markdown 格式）；若指定 `--output` 则同时写入该文件（.md 或 .csv）。退出码非 0 或 stderr 有错误时，向用户展示错误并结束。
4. **成功**：将 stdout 表格呈现给用户；若写入了文件，说明路径。

## 脚本参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--repo` | 是（可多次） | 仓库，格式 `owner/repo`，可多次传入多仓库 |
| `--pr` | 否（可多次） | 指定 PR 编号；与时间范围二选一，使用时常需且仅需一个 `--repo` |
| `--branch` | 否 | 目标分支；未传时自动尝试 master → develop → main |
| `--since` | 否 | 起始日期 YYYY-MM-DD（含该日 00:00 上海时间） |
| `--until` | 否 | 结束日期 YYYY-MM-DD（含该日 24:00 前） |
| `--days` | 否 | 最近 N 天（默认 30）；与 since/until 二选一，未指定 since/until 时生效 |
| `--all` | 否 | 不抽样，该时间范围内合入的 PR 全部检查 |
| `--output` | 否 | 输出文件路径，扩展名 .md 或 .csv，UTF-8（CSV 带 BOM） |
| `--config` | 否 | 配置文件路径，未传则使用技能根目录下 config.json |

- **指定 PR**：传 `--pr N`（可多个）时仅检查这些 PR，需且仅需一个 `--repo`，不按时间筛选。
- 时间约定：仅用 `--days`、或仅用 `--since`/`--until`。若同时传，脚本按 `--since`/`--until` 优先。
- 多仓库时：**每个仓库**各自按上述规则抽样或全部检查（方案 A）。

## 分析维度（8 项）

| 维度 | 说明 | 判定 |
|------|------|------|
| 评论未解决 | 是否存在未解决的 diff 检视意见 | PR 评论中 `comment_type == "diff_comment"` 且 `resolved == false` 则记为「是」 |
| 流水线/标签 | 是否缺少必选标签（含流水线通过） | 配置的 `required_labels` 缺任一则「是」 |
| 缺必选标签 | 同上，与「流水线」合并为配置的必选标签集合 | 见 config.json `required_labels` |
| 新增超行数 | 新增代码行是否超过阈值 | 超过 `max_additions`（默认 1000）则「是」 |
| 无测试 | 修改文件是否包含测试 | 变更文件路径中均不包含 `test` 或 `ut` 则「是」 |
| 多 Issue | 是否关联超过 1 个 Issue | 关联 Issue 数 > 1 则「是」 |
| 缺检视 | 大 PR 是否缺乏检视意见 | 新增行数 > `review_lines_threshold`（默认 500）且 diff 评论数为 0 则「是」 |
| 标题/描述不清晰 | 标题与描述是否过短或过于笼统 | 标题长度 < `title_min_length`（默认 5）或描述长度 < `body_min_length`（默认 10）则「是」；满足长度后若标题/描述明显含糊（如仅「fix」「修改」无实质说明），则判为「是」 |

- **表格列**：仓库、**PR**（以 `#编号` 带链接，无单独链接列）、标题、各维度详情、问题汇总。
- **维度列为详情文案**：
  - 评论未解决：`否（已解决数/总 diff 评论数）` 或 `是（未解决数/总数）`，如 `否（1/10）`、`是（2/5）`。
  - 缺必选标签：`否` 或 `是（缺：label1、label2）`。
  - 新增超行数：`否（实际行数）` 或 `是（实际行数）`。
  - 多 Issue：`否（0）` 或 `是（N）`。
  - 缺检视：`否` 或 `是（新增 N 行，0 个检视）`。
  - 标题/描述不清晰：`否` 或 `是（原因，如标题过短、描述过短、描述笼统）`。
- 最后一列「问题汇总」为该项 PR 所有不通过维度的简短罗列。

## 配置（config.json）

位于技能根目录，或通过 `--config` 指定。字段说明：

| 字段 | 含义 | 默认 |
|------|------|------|
| `required_labels` | 必选标签列表（缺一即不通过） | `["ci-pipeline-passed", "approved", "lgtm"]` |
| `max_additions` | 新增行数阈值，超过记为「新增超行数」 | 1000 |
| `review_lines_threshold` | 超过此行数且无 diff 评论则记为「缺检视」 | 500 |
| `title_min_length` | 标题最小字符数 | 5 |
| `body_min_length` | 描述最小字符数 | 10 |
| `test_substrings` | 判定「含测试」时路径需包含的子串 | `["test", "ut"]` |

## 输出格式

- **表格列**：仓库、PR（`#编号` 带链接）、标题、评论未解决、缺必选标签、新增超行数、无测试、多 Issue、缺检视、标题/描述不清晰、问题汇总（无单独链接列，链接在 PR 列）。
- **stdout**：始终输出 Markdown 表格（便于控制台查看）。
- **--output .md**：与 stdout 相同的 Markdown 表格写入文件。
- **--output .csv**：同一内容写入 CSV，UTF-8 带 BOM，便于 Excel 打开。

## 禁止

- 禁止在未得到脚本输出前猜测或伪造数据。
- 禁止在用户未提供至少一个 `--repo` 时执行脚本。

## 示例

| 用户意图 | 命令 |
|----------|------|
| 最近 30 天单仓抽检 | `python <S> --repo owner/repo` |
| 指定 PR 检查 | `python <S> --repo owner/repo --pr 2905 --pr 2606` |
| 指定时间多仓抽检 | `python <S> --repo org/a --repo org/b --since 2026-02-01 --until 2026-03-10` |
| 全部检查不抽样 | `python <S> --repo owner/repo --days 7 --all` |
| 指定分支并写 CSV | `python <S> --repo owner/repo --branch main --output report.csv` |
| 自定义配置 | `python <S> --repo owner/repo --config /path/to/config.json` |

其中 `<S>` 为 `<SKILL_ROOT>/scripts/pr_audit.py` 的绝对路径。

## 历史版本

**v1.0.0** (2026-03-11)
- 🎉 初始版本发布
- 📊 支持按时间范围抽检、8 维度质量分析
