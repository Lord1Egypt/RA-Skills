# GitCode 仓库运营报表 Skill

将 GitCode 上配置的仓库运营数据整理成**日报**输出，支持关键指标统计、AI 摘要与 Markdown。本文档为设计说明与使用说明合一。（周报/月报待后续调试后发布。）

---

## 1. 设计原则

| 原则 | 说明 |
|------|------|
| **确定性流程在脚本内** | 数据拉取、指标计算、快照读写、报表 JSON 生成均由脚本完成，不依赖Agent做分步计算。 |
| **最少脚本调用** | 整份日报数据通过 **一次** 脚本调用完成；Agent仅负责解析用户意图、更新配置、调用脚本、根据报表数据生成摘要、渲染 Markdown。 |
| **脚本参数尽量少** | 脚本仅支持 **0～1 个** 可选参数（日期）；仓库列表与所有可调项均从 `config.json` 读取。 |
| **流程简单** | 用户提供「仓库（可选）+ 日期（可选）」→ 若提供仓库则写回 config → 执行脚本一次 → 根据输出生成摘要与日报。 |
| **通用性** | 支持单仓/多仓、今日/指定日期、中英文；输出格式与 schema 版本化，便于扩展。 |
| **易用性** | 未配置仓库时可用用户输入并保存到 config；默认时区与默认「今日」开箱即用。 |
| **准确性** | 指标口径在文档与脚本注释中固定；增量依赖 SQLite 历史快照；请求超时与重试可配置。 |

---

## 2. 整体架构

- **日报**：`generate_daily_report.py --type day` 调 GitCode API，计算当日指标，写 **snapshots** 与 **daily_metrics**；根据 `merged_prs_for_ai` 生成每仓摘要与全局摘要，再将摘要写成 JSON；渲染时脚本自动将摘要写入 **daily_summaries**。
- **脚本**：仅 **generate_daily_report.py**（生成报表 + 渲染 + 保存摘要）。

---

## 3. 脚本约定

- **generate_daily_report.py**：
  - **生成日报**：`--type day`（默认）、可选 `--date YYYY-MM-DD`、可选 `--repos "owner/repo,..."`。必选 GITCODE_TOKEN。结果自动写入 `temp_dir/report.json`（主通道），stdout 仅输出简短状态。必须从文件读取完整数据。
  - **保存摘要**：`--save-summaries`，从 summaries.json 读取摘要写入 DB（不调 API）。**`--render` 时已自动执行此操作**，通常无需单独调用。摘要 JSON 格式：`{ "period_type": "day", "date": "YYYY-MM-DD", "repos": [ {"repo": "owner/repo", "summary": "..."} ], "global": "全局摘要" }`。
  - **渲染报表**：`--render --output <PATH>` [--template <PATH>]。日报使用 **resources/daily_report.md** 模板。
- **resources/daily_report.md**：日报的固定模板，脚本根据 report JSON + 摘要 JSON 填充占位符，保证输出一致。
- **输入**：`config.json`、`resources/report.db`；日报还需 `GITCODE_TOKEN`。
- **输出**：生成报表时 stdout 单份 JSON；渲染时写入 `--output` 指定的 .md 文件。

---

## 4. 指标定义与数据来源

| 指标 | 口径 | 数据来源 |
|------|------|----------|
| Star/Fork 数 | 当前值 | `GET /repos/{owner}/{repo}` → stargazers_count / forks_count |
| Star/Fork 增量 | 今日相对昨日 | 昨日快照与当前 API 值做差；无昨日快照则为 null |
| 今日合并 PR 数 | 当日合并的 PR | `GET /repos/.../pulls?state=all` 分页，按 merged_at 在当日（timezone）过滤 |
| 今日关闭 PR 数 | 当日关闭的（合并+未合并） | 同上，按 closed_at 在当日过滤 |
| PR 合并率 | 当日合并数 / 当日关闭数 | 分母为 0 时 N/A |
| 今日新增/关闭 Issue | 当日创建/关闭 | `GET /repos/.../issues?state=all`，按 created_at/closed_at 过滤 |
| 活跃贡献者数 | 当日在该仓有 PR/Issue/评论行为的用户去重 | 从当日合并 PR、当日 Issue、评论中提取 user 去重 |
| 代码变更量（+/- 行） | 仅当日合并的 PR 的 additions/deletions 汇总 | 对当日合并的 PR 调 `GET /repos/.../pulls/{number}`，不拉 diff |
| 重大 PR | additions > 500 | 同上，单条 PR 的 additions |
| 热门 Issue | 今日评论数 ≥ 5 | 对当日有活动的 Issue 拉评论数 |
| 陈旧 Issue 数 | open 超过 30 天且标题不包含排除关键词 | 过滤 created_at < 今日-30 天、state=open；排除关键词见 config（不区分大小写） |
| 陈旧 PR 数 | open 超过 30 天 | 过滤 created_at < 今日-30 天、state=open |

时间边界：所有「当日」均为 config 的 `timezone` 下该日 00:00～23:59。请求：每次请求后 sleep 0.1s；单次超时 30s、失败重试 2 次、间隔 2s。

---

## 5. config.json

路径：技能根目录 `config.json`。键与默认值如下：

| 键 | 类型 | 说明 | 默认 |
|----|------|------|------|
| repos | string[] | 仓库列表 "owner/repo" | [] |
| timezone | string | 时区 | Asia/Shanghai |
| request_timeout_seconds | number | 单次 HTTP 超时（秒） | 30 |
| request_retry_times | number | 失败重试次数 | 2 |
| request_retry_interval_seconds | number | 重试间隔（秒） | 2 |
| request_sleep_seconds | number | 每次请求后 sleep（秒） | 0.1 |
| stale_days | number | 陈旧 Issue/PR 天数阈值 | 30 |
| stale_issue_exclude_keywords | string[] | 陈旧 Issue 标题排除词（不区分大小写） | ["RFC","CVE","Roadmap"] |
| major_pr_additions_threshold | number | 重大 PR：additions 超过该值 | 500 |
| hot_issue_comments_threshold | number | 热门 Issue：当日评论数 ≥ 该值 | 5 |
| max_repos_per_report | number | 最多处理仓库数 | 50 |
| merged_pr_body_max_chars | number | 供 AI 的 PR body 最大字符数 | 2000 |

用户本次指定仓库时，调用脚本时传 `--repos "owner/repo,..."`，脚本会写回 `config.json` 的 `repos`；未传时脚本从 config 读取。

---

## 6. 轻量存储（SQLite）

- **路径**：`{skill_root}/resources/report.db`
- **Schema 版本管理**：`schema_version` 表记录已应用的版本号。脚本启动时自动检查版本并执行渐进式迁移（`ALTER TABLE ADD COLUMN`），向后兼容旧 DB 文件。当前版本：**2**。
- **表**：
  - **schema_version**：`version` (INTEGER), `applied_at` (TEXT)；记录迁移历史。
  - **snapshots**：`date`, `repo`, `stars`, `forks`, `open_issues`；用于 Star/Fork 增量（昨日/周初/月初 vs 当前）。
  - **daily_metrics**：`date`, `repo`, `prs_merged`, `prs_closed`, `prs_opened`, `issues_opened`, `issues_closed`, `code_additions`, `code_deletions`, `active_contributors`, `stale_issues_count`, `stale_prs_count`, `major_prs_json`, `hot_issues_json`, `merged_prs_for_ai_json`；日报脚本在拉取当日 API 后写入。`INSERT OR REPLACE` 确保同日多次执行只保留最新数据。
  - **daily_summaries**：`date`, `repo`, `summary_text`；渲染时脚本自动从 summaries.json 写入；`repo = '__global__'` 为全局摘要。同日多次执行保留最新。

---

## 7. 报表 JSON Schema（脚本 stdout）

根级：`status`、`message`（仅 error）、`schema_version`、`generated_at`、`report`（仅 ok 时）。

**report**：`period_type`（day）、`date`、`timezone`、`global`、`repos`[]。每仓 `today` 内含：`issues_opened_today_list`、`issues_closed_today_list`（项为 `{ "number", "title" }`），渲染时新增 Issue 列为「#123 标题」。日报每仓含 `merged_prs_for_ai`，Agent据此生成每仓摘要与全局摘要。

---

## 8. 执行流程

1. **何时使用**：用户表达「生成日报」「仓库运营日报」「今日动态」等意图；可选提供仓库或日期；未提供仓库则用 config 的 repos。
2. **日报**：执行 `python scripts/generate_daily_report.py [--date YYYY-MM-DD] [--repos "owner/repo,..."]`（结果自动写入 temp_dir/report.json）→ 从文件读取数据，根据每仓 `merged_prs_for_ai` 生成摘要，写成 **summaries.json** → 执行 `python scripts/generate_daily_report.py --render --output <报告路径.md>` 渲染日报（渲染时**自动保存摘要到 DB**）。
3. **认证**：日报需要 GITCODE_TOKEN。

---

## 9. 报表 Markdown 结构（由模板唯一确定）

日报 **必须** 通过脚本的 `--render` 模式 + **resources/daily_report.md** 模板生成，以保证输出一致。结构：

1. **标题**（含 📊 emoji + 报表类型）
2. **一、仓库概览**：整体指标表（Star/Fork/PR/Issue + 增量）+ 全局一句话摘要
3. **二、分仓详情**：每仓指标 + 当日合并 PR 列表（可点击链接）+ 新开 PR 列表 + 新增/关闭 Issue 列表（可点击链接）+ 热门 Issue 明细 + 该仓小结
4. **三、行动建议**：基于数据自动识别陈旧 Issue/PR、热门 Issue、重大 PR 等需关注事项

完整样例见下方 **§ 样例报告**。

---

## 10. 样例报告

以下为一份**日报**的 Markdown 样例，由 `--render` 模式 + `resources/daily_report.md` 模板生成。

```markdown
# 📊 开源代码仓库运营日报

**报表日期**：2026-03-10（Asia/Shanghai）  
**仓库总数**：2　**活跃仓库数**：2

---

## 📋 一、仓库概览

| 指标 | 数值 |
|------|------|
| ⭐ 总 Star | 876 |
| 📈 Star 增量（较昨日） | +9 |
| 🍴 总 Fork | 310 |
| 📈 Fork 增量（较昨日） | +4 |
| 🔀 今日合并 PR | 3 |
| 🆕 今日新开 PR | 2 |
| 📌 今日新增 Issue | 2 |
| ✅ 今日关闭 Issue | 1 |
| ⚠️ 异常速览 | 陈旧 Issue 4 个；陈旧 PR 1 个 |

**💬 一句话摘要（全局）**：两仓今日共合并 3 个 PR，sample 完成多机调度策略重构，example 修复推理精度问题；整体活跃度良好。（示例中仓库名仅为占位，可替换为实际 owner/repo。）

---

## 📁 二、分仓详情

### 📦 org/sample

- **Star**：620（+6）　**Fork**：210（+3）
- **今日合并 PR**：2　**今日新开 PR**：1　**PR 合并率**：100%
- **今日新增 Issue**：1　**今日关闭 Issue**：1
- **代码变更（当日合并 PR）**：+480 / -120 行　**活跃贡献者**：4
- **陈旧 Issue**：3　**陈旧 PR**：1

**🔀 当日合并 PR**

- [#356](https://gitcode.com/org/sample/pulls/356) 重构多机调度策略以支持异构集群（⚡ +520 行）
- [#361](https://gitcode.com/org/sample/pulls/361) 修复通信超时在 8 卡场景下的偶发失败

**🆕 当日新开 PR**

- [#365](https://gitcode.com/org/sample/pulls/365) feat: 支持某型号弹性调度

**📌 当日新增 Issue**

- [#189](https://gitcode.com/org/sample/issues/189) 集群训练在 16 卡拓扑下 AllReduce 性能下降

**✅ 当日关闭 Issue**

- [#180](https://gitcode.com/org/sample/issues/180) HCCL 链路检测误报已修复

**🔥 热门 Issue（当日评论较多）**

- [#150](https://gitcode.com/org/sample/issues/150) RFC: 下一代弹性训练容错机制设计（8 条评论）

**💬 该仓小结**：今日合并 2 个 PR，其中 #356 为多机调度重构（+520 行）；社区对弹性训练 RFC 讨论活跃。

---

### 📦 org/example

- **Star**：256（+3）　**Fork**：100（+1）
- **今日合并 PR**：1　**今日新开 PR**：1　**PR 合并率**：100%
- **今日新增 Issue**：1　**今日关闭 Issue**：0
- **代码变更（当日合并 PR）**：+95 / -30 行　**活跃贡献者**：2
- **陈旧 Issue**：1　**陈旧 PR**：0

**🔀 当日合并 PR**

- [#78](https://gitcode.com/org/example/pulls/78) 修复 FP16 推理在特定 batch size 下的精度偏差

**🆕 当日新开 PR**

- [#80](https://gitcode.com/org/example/pulls/80) feat: 新增稀疏特征 embedding 量化方案

**📌 当日新增 Issue**

- [#42](https://gitcode.com/org/example/issues/42) 推荐模型导出 ONNX 时 dynamic axes 配置报错

**💬 该仓小结**：今日合并 1 个 PR 修复推理精度问题，新开 1 个量化方案 PR，进展平稳。

---

## 🎯 三、行动建议

基于当日数据自动识别的关注事项：

- ⏳ **org/sample** 有 3 个陈旧 Issue（open 超 30 天），建议评审清理
- ⏳ **org/sample** 有 1 个陈旧 PR（open 超 30 天），建议评审或关闭
- 🔥 **org/sample** [#150](https://gitcode.com/org/sample/issues/150) RFC: 下一代弹性训练容错机制设计 今日 8 条评论，建议跟进
- ⚡ **org/sample** [#356](https://gitcode.com/org/sample/pulls/356) 重构多机调度策略以支持异构集群（+520 行），建议重点 review
- ⏳ **org/example** 有 1 个陈旧 Issue（open 超 30 天），建议评审清理

**📊 整体**：两仓今日共合并 3 个 PR，sample 完成多机调度策略重构，example 修复推理精度问题；整体活跃度良好。（示例中 org/sample、org/example 为占位，可替换为实际仓库。）
```

---

## 11. 错误与安全

- 未配置/无效 Token、repos 为空：脚本输出 status=error、message 提示；不暴露 Token。
- 某仓超时或 API 失败：该仓设 fetch_error，其余仓继续；全局 fetch_errors 汇总。
- 无昨日快照：Star/Fork 增量为 null。日报中链接仅用公开 URL，不带 token。

---

## 12. 依赖与使用方式

- **依赖**：日报必配 **GITCODE_TOKEN**。Python 3.7+。
- **使用**：在 `config.json` 中配置 `repos`，或对话中指定仓库（脚本可写回 config）；对Agent说「生成今日日报」等，Agent执行一次 generate 脚本后根据输出生成摘要并渲染 Markdown。
