---
name: gitcode-repo-daily
description: "Generate daily operations reports for GitCode repositories with key metrics, AI summaries and Markdown output. 将 GitCode 上配置的仓库运营数据整理成日报输出；支持关键指标统计、AI 摘要与 Markdown。Python 3.7+ standard library only, no pip dependencies."
metadata: {"openclaw": {"requires": {"env": ["GITCODE_TOKEN"]}, "primaryEnv": "GITCODE_TOKEN"}}
---

# GitCode 仓库运营报表（日报）

根据 config 或用户指定的仓库列表，生成运营日报（调 API + 写 DB）。**摘要根据报表数据生成后，渲染时自动写入 DB**。

## 何时使用

- 用户表达「生成日报」「仓库运营报表」「今日动态」「整理成日报」等意图。
- 可选：用户提供仓库链接或 owner/repo、日期；未提供则使用脚本从 **config.json** 读取的 `repos`（脚本负责读写 config）。
- 若用户本次指定了仓库，调用脚本时传入 `--repos "owner/repo,..."`，脚本会用于本次并写入 config，下次未指定时将使用此列表。
- 若 config 中 `repos` 为空且用户未指定仓库，则提示：「请本次对话中指定要统计的仓库（将保存为默认），或在 config.json 中配置 repos」。

## 认证

**GITCODE_TOKEN**：按以下优先级读取，任一处有值即用。

| 优先级 | 来源 | 适用平台 |
|--------|------|----------|
| 1 | 进程环境变量 `GITCODE_TOKEN` | 所有平台 |
| 2 | Windows 用户级环境变量 | Windows |
| 3 | Windows 系统级环境变量 | Windows |

- **Linux / macOS**：仅读进程环境变量。建议在 `~/.bashrc` 或 `~/.zshrc` 中添加 `export GITCODE_TOKEN="your_token"`。
- **Windows**：进程环境变量 → 用户级 → 系统级。
- **日报必选**（调 API 拉取当日数据）。

## 路径约定

- **技能根目录**（下称 `SKILL_ROOT`）：本 SKILL.md 所在的目录。脚本通过 `__file__` 定位自身，**不依赖工作目录**。
- **中间文件目录**：`SKILL_ROOT/temp_dir/`，脚本自动创建。
- 执行脚本时，统一使用**脚本绝对路径**，无需 cd 到特定目录。
- `--report-json` 和 `--summaries-file` 参数的相对路径会自动按 SKILL_ROOT 解析（也可传绝对路径），已有默认值无需每次指定。

## 固化流程（必须按此执行）

### 日报

1. **解析**：解析 **日期**（今日/昨天/YYYY-MM-DD）和 **仓库列表**（可选）。
2. **调用脚本**：若用户本次指定了仓库，传入 `--repos "owner/repo,..."`（逗号分隔）；否则不传。**config 由脚本读写，你无需写入 config。**
   `python <SKILL_ROOT>/scripts/generate_daily_report.py [--date YYYY-MM-DD] [--repos "owner/repo,..."]`（默认 --type day）。需 GITCODE_TOKEN。
3. **读取结果**：脚本成功时**自动写入** `SKILL_ROOT/temp_dir/report.json`（UTF-8 编码），同时也输出到 stdout。**优先从文件读取**（避免 Windows 管道编码乱码），若文件不存在再解析 stdout。
4. **错误**：若 `status == "error"`，提示 `message` 并结束。
5. **提示用户**：若脚本返回或 report.json 中含有 `repos_saved: true` 或 `repos_saved_message`，须用自然语言告知用户：「已保存为默认仓库列表，下次若不指定仓库将使用此列表。」不得向用户提及 config.json、--repos 等实现细节。
6. **成功**：
   - 读取 `SKILL_ROOT/temp_dir/report.json`（脚本已自动写入，无需手动保存）。
   - 对 `report.repos` 中每个无 `fetch_error` 的仓，根据 `merged_prs_for_ai`，**自行生成**该仓**今日摘要**；再根据各仓摘要生成**全局一句话摘要**。
     > **摘要要求**：1-2 句话，≤100 字，概括该仓当日主要变更方向。示例：「今日合并 3 个 PR，涉及 NPU 调度策略优化和单测补充。」
   - 将各仓摘要与全局摘要写成 `SKILL_ROOT/temp_dir/summaries.json`（使用 Write 工具），格式如下：
     ```json
     {
       "period_type": "day",
       "date": "2026-03-10",
       "repos": [
         {"repo": "owner/repo", "summary": "今日合并3个PR，涉及调度优化和单测补充。"}
       ],
       "global": "全局一句话摘要"
     }
     ```
   - **必须使用脚本渲染模式生成日报 Markdown**：
     `python <SKILL_ROOT>/scripts/generate_daily_report.py --render --output <用户指定的 .md 路径>`
     脚本自动从 temp_dir/report.json 和 temp_dir/summaries.json 读取，**渲染时同时自动将摘要写入 DB**。同一天多次执行时 DB 自动保留最新结果。报告结构由 **resources/daily_report.md** 唯一确定，不得自行改写模板结构或跳过渲染。

### 禁止

- 禁止在未得到脚本 stdout 输出前猜测或伪造数据。日报只调用 generate 一次。

## 脚本与路径

- **scripts/generate_daily_report.py**（唯一脚本）：
  - **生成日报**：`--type day`（默认）、`[--date YYYY-MM-DD]`、`[--repos "owner/repo,..."]`。仓库列表：未传 `--repos` 时从 config.json 读取；传了则用于本次并写入 config（下次未指定时使用）。结果自动写入 `temp_dir/report.json`。stdout 仅输出简短状态（文件路径），**必须从文件读取完整数据**。
  - **渲染报表**：`--render --output <PATH>` [--template <PATH>]。日报使用 **resources/daily_report.md** 模板。**渲染时自动将 summaries.json 中的摘要保存到 DB**。
  - **单独保存摘要**（可选）：`--save-summaries`，仅在不渲染但需写 DB 时使用。
- **resources/daily_report.md**：日报的固定模板，不得擅自改动。
- 配置：**config.json** 由脚本读写（无需写入）；存储：**resources/report.db**。
- 脚本通过 `__file__` 定位技能根目录，**不依赖工作目录**，Windows / Linux / macOS 均可使用绝对路径执行。

## 示例（供无歧义执行）

> 以下 `<S>` 代表 `<SKILL_ROOT>/scripts/generate_daily_report.py`，执行时替换为脚本绝对路径。

| 用户意图 | 命令 |
|----------|------|
| 生成今日日报 | `python <S>` |
| 生成 3 月 8 日日报 | `python <S> --date 2026-03-08` |
| 指定仓库生成日报（并保存为默认） | `python <S> --repos "owner/repo,owner2/repo2"` |
| 渲染报表到文件（同时自动保存摘要到 DB） | `python <S> --render --output 报告路径.md` |

## 报表内容结构（由模板唯一确定）

日报 **必须** 通过 `--render` 使用 **resources/daily_report.md** 模板生成，以保证输出格式一致。结构：标题（含 emoji）→ 一、仓库概览（整体指标表 + 全局一句话摘要）→ 二、分仓详情（含可点击 Issue/PR 链接、合并 PR 列表、热门 Issue 明细、该仓小结）→ 三、行动建议（基于数据自动识别的关注事项）。

## 参考

- 设计、config、DB 表、报表 Schema：**README.md**。

## 历史版本

**v1.0.0** (2026-03-11)
- 🎉 初始版本发布
- 📅 支持日报与摘要
