---
name: pr-comment-fix
description: "按 GitCode PR 检视意见修改代码。需 GITCODE_TOKEN。Use when 用户要修改 PR 检视意见。"
metadata: {"openclaw": {"requires": {"env": ["GITCODE_TOKEN"]}, "primaryEnv": "GITCODE_TOKEN", "optional": true}}
---

# GitCode PR 检视意见修复

**执行顺序**：`fetch` 写出 JSON → 按模板汇总并请用户选范围 → 确认后再改代码 → 本地验证并输出修复总结表 → 用户需要时再 `reply` / `resolve`。

## 何时使用

- 用户希望 **根据 PR 上的代码检视意见改本地代码**（不是「检视 PR 出报告」一类只读检视）。
- **须由用户提供 GitCode PR 页面链接**（`--pr-url`）；**不支持**仅填 owner/repo/编号，**不做**基于 git 的自动匹配。

## 认证

- **Token**：`GITCODE_TOKEN` 环境变量，或用户消息中提供；也可用脚本参数 `--token`。
- 请求头：`PRIVATE-TOKEN`（与现有 GitCode skills 一致）。
- 未配置时提示前往 [GitCode 个人访问令牌](https://gitcode.com/setting/token-classic) 创建并设置变量。

## 依赖

- **Python 3.7+**，仅标准库（脚本 `scripts/pr_comment_fix_tool.py`）。
- 工作区应能打开 **待修改的仓库**（与 PR 变更一致）。

---

## 流程（严格顺序）

### 1. 拉取上下文 JSON（必须先做）

**SKILL_ROOT**：本 `SKILL.md` 所在目录。

```bash
python <SKILL_ROOT>/scripts/pr_comment_fix_tool.py fetch -o "<路径>/pr_comment_fix_context.json" --pr-url "<GitCode PR 完整 URL>"
```

- **`fetch` 仅接受 `--pr-url`**：URL 路径含 `/pull/`、`/pulls/` 或 `merge_requests/` 均可解析。请从浏览器复制 **PR 所在仓库** 的页面链接（fork 场景下一般打开上游仓库里的 PR）。

脚本写出 **`pr_comment_fix_context.json`**（或打印到 stdout），其中包含：

- `owner`、`repo`、`pr_number`、`pr_html_url`
- **`unresolved_diff_comments`**：每条含 **`seq`**、`discussion_id`、`body`、`diff_file`、`resolved` 等 API 原始字段（**须保留 `discussion_id` 供后续回复/改状态**）
- **`by_file`**：按文件分组，同一文件内评论已按 **行号相关字段从大到小** 排序（便于从文件末尾往前改）

**筛选规则**：仅包含 **未解决** 行评（`resolved` 不为真；缺省视为未解决）。

若 JSON 含 **`warnings`**（如缺少 `discussion_id`），须告知用户：对应条目 **无法** 使用脚本的 `reply` / `resolve`。

- **停步点**：`fetch` 成功并已有 `pr_comment_fix_context.json` 后，**下一步只能是步骤 2**（汇总并按模板输出、再询问用户）。**不得**直接进入读文件、打补丁或「顺手改一处」。

---

### 2. 汇总并按模板输出、再确认范围（未收到明确答复前不得改代码）

1. 读取 JSON：以 **`unresolved_diff_comments`** 为准（可与 **`by_file`** 对照），统计条数 **N**。
2. **必须先**用下面表格向用户展示全部待处理项（**序号**与 JSON 中 **`seq`** 一致；**行号**取自接口字段，如 `line` / `original_line` / `position` 等，无则写「见讨论/无行号」；**问题**用 `body` 的简要概括或首行，勿整段粘贴）：

   | 序号 | 文件 | 行号 | 问题 |
   |------|------|------|------|
   | 1 | `diff_file` | … | … |
   | … | … | … | … |

3. 询问用户处理范围：`全部`/`是`、部分序号如 `1,3`、`不修`/`跳过`。
4. 用户回复可解析后再进入步骤 3；不明则再问。发出表格与询问后**须等待用户下一条消息**，在此之前**不得**编辑代码。
5. 「不修」→ 结束，不改代码。

---

### 3. 按文件修复（仅在步骤 2 确认后执行）

依据 **`pr_comment_fix_context.json`** 中的 **`by_file`** 与 **`unresolved_diff_comments`** 修复：

1. **顺序**：以 **`by_file`** 为准；**同一文件内** 按数组顺序（已 **从后往前**）逐条处理，减少行号漂移。
2. **定位**：以 API 行号相关字段与 **`diff_file`** 为准；修改前 **先读当前文件对应行**，勿盲信过时行号。
3. **路径**：`diff_file` 相对仓库根解析；若找不到，再尝试去前缀或让用户确认根目录。
4. **大改**：单条预估改动 **>20 行**、或 **改签名/结构**、或 **跨 ≥2 个文件** → 先给 **修改方案**，用户确认后再动代码。
5. **合并同一次修改**：同一文件、同一意图的多条意见尽量合并为一次编辑。

---

### 4. 本地验证与修复总结

每批或全部修改完成后：

- **语法/解析**：对改动过的文件做可行检查（如 `python -m py_compile`）。
- **导入与符号**：无未定义引用。
- **范围**：仅动用户确认范围内的代码。
- 若项目有固定检查命令（`ruff` / `eslint` / `make test` 等），在可行时执行。

**必须先输出「修复总结表」**（与步骤 2 中条目对应；**处理方式**写本次实际做了什么；未动的项不要编造）：

| 序号 | 文件 | 行号 | 问题 | 处理方式 |
|------|------|------|------|----------|
| 1 | … | … | （与步骤 2 对应） | （简述：如何改、是否仅说明未改） |
| … | … | … | … | … |

---

### 5. 修后闭环（仅当用户需要时）

**顺序固定为：**

1. **修改与验证完成后**，询问是否 **生成回复草稿**（针对已处理的条目）。
2. 若需要 → 生成草稿 → 用户确认 → 询问是否 **发送**。
3. 若发送 → 使用脚本 **`reply`**（见下）调用官方接口：[回复 Pull Request 评论](https://docs.gitcode.com/docs/apis/post-api-v-5-repos-owner-repo-pulls-number-discussions-discussions-id-comments)。
4. **发送完成后**，询问是否 **修改检视解决状态**；若需要 → 使用 **`resolve`** 子命令：[修改检视意见解决状态](https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-pulls-number-comments-discussions-id)。

**不得**在未获用户确认时代为发送评论或修改远端状态。

#### 回复单条讨论

```bash
python <SKILL_ROOT>/scripts/pr_comment_fix_tool.py reply -c "<pr_comment_fix_context.json>" --seq <seq> --body "<正文>"
# 或 --discussion-id <id> --body "..."
```

#### 将讨论标为已解决

```bash
python <SKILL_ROOT>/scripts/pr_comment_fix_tool.py resolve -c "<pr_comment_fix_context.json>" --seq <seq> --resolved 1
```

若 `resolve` 报错，对照官方文档核对请求体。

---

## 脚本子命令一览

| 子命令 | 作用 |
|--------|------|
| `fetch` | 拉取未解决 `diff_comment`，写上下文 JSON |
| `reply` | `POST .../pulls/{n}/discussions/{discussion_id}/comments` |
| `resolve` | `PUT .../pulls/{n}/comments/discussions/{id}` |

完整参数见：`python scripts/pr_comment_fix_tool.py --help`。
