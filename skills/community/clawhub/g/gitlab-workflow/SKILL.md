---
name: gitlab-workflow
description: GitLab 工作流助手，严格遵循团队规范。用于 MR 管理、代码审查、CI/CD 状态查询、分支管理和合并操作。通过 MorphixAI 代理安全访问 GitLab API。
metadata:
  openclaw:
    emoji: "🦊"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# GitLab 工作流

通过 `mx_gitlab` 工具管理 GitLab 项目。严格遵守团队规范。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 GitLab 账号，或通过 `mx_link` 工具链接（app: `gitlab`）

---

## 参数命名规范（重要）

`mx_gitlab` 工具所有 action 的参数命名：

| 参数 | 说明 |
|------|------|
| `project` | 项目 ID（数字字符串）或路径（`group/repo`），**不是** `project_id` |
| `mr_iid` | MR 在项目内的序号，**不是** `merge_request_iid` |
| `pipeline_id` | Pipeline 的全局 ID |

### description 字段换行格式

> ⚠️ `description` 字段**必须使用真实换行符**，不要使用 `\n` 字面量字符串。
>
> 错误示例（在 GitLab 上会显示为 `\n`）：
> ```
> description: "改动\n- 修复 bug\n- 新增功能"
> ```
>
> 正确示例（使用 YAML 多行字符串）：
> ```yaml
> description: |
>   ## 改动
>   - 修复 bug
>   - 新增功能
>
>   ## 测试
>   - 单元测试通过
> ```

---

## 代码审查策略（优先级顺序）

**获取 MR 代码变更时，按以下顺序尝试：**

### ✅ 优先：本地 git（推荐）

本地仓库 + git 命令是最可靠的代码审查方式：
- 无需额外认证（使用本地已有凭证）
- 无响应体大小限制（任意规模的 diff）
- 速度快，工具丰富（log、diff、show、blame）

**第一步：查找本地仓库路径**

```bash
# nodes.run — 在本机执行
find ~/www -maxdepth 4 -type d -name '<仓库名>'
# 例：find ~/www -maxdepth 4 -type d -name 'tanka-2b-web'
```

**第二步：fetch 最新数据**

```bash
# nodes.run — 工作目录切换到仓库路径
cd ~/www/<项目路径> && git fetch origin
```

**第三步：获取 MR 的 commits（需要知道源分支和目标分支）**

```bash
# 查看 MR 分支间的 commit 列表
git log origin/<target-branch>..origin/<source-branch> --oneline

# 示例（MR: feat/zoom-v2/main → uat-tanka-oh）
git log origin/uat-tanka-oh..origin/feat/zoom-v2/main --oneline
```

**第四步：获取文件变更统计**

```bash
git diff --stat origin/<target-branch>...origin/<source-branch>
# 示例
git diff --stat origin/uat-tanka-oh...origin/feat/zoom-v2/main
```

**第五步：获取具体文件的 diff**

```bash
# 全量 diff（大 MR 慎用，建议指定文件）
git diff origin/<target-branch>...origin/<source-branch>

# 指定文件 diff（推荐）
git diff origin/<target-branch>...origin/<source-branch> -- src/path/to/file.ts

# 只看特定目录
git diff origin/<target-branch>...origin/<source-branch> -- src/components/
```

---

### ⚠️ 备用：mx_link proxy（本地无仓库时使用）

当本地不存在仓库时，通过 MorphixAI 代理调用 GitLab API。
**注意：大型 MR 的 diff 可能因响应体过大返回 400，此时只能使用本地 git。**

```
mx_link:
  action: proxy
  account_id: <gitlab-account-id>
  method: GET
  url: https://gitlab.com/api/v4/projects/<project-id>/merge_requests/<mr-iid>/changes
```

可用的 MR 相关 API：
- `GET /api/v4/projects/{id}/merge_requests/{iid}` — MR 详情
- `GET /api/v4/projects/{id}/merge_requests/{iid}/changes` — 文件变更（可能因大小失败）
- `GET /api/v4/projects/{id}/merge_requests/{iid}/discussions` — Discussion 线程
- `GET /api/v4/projects/{id}/merge_requests/{iid}/notes` — 评论列表
- `POST /api/v4/projects/{id}/merge_requests/{iid}/notes` — 发表评论
- `GET /api/v4/projects/{id}/merge_requests/{iid}/approvals` — 审批状态

---

## 分支命名

- `feature/JIRA-{ID}-{简短描述}` — 新功能
- `fix/JIRA-{ID}-{简短描述}` — bug 修复
- `release/v{X.Y.Z}` — 发布分支
- `hotfix/v{X.Y.Z}-{描述}` — 生产热修复

## Commit Message 格式

`{Scope}: {action} {description}`

- Scope：模块名（SDK、CLI、Gateway、Bot 等）
- Actions：add / update / fix / remove / refactor
- 示例：`SDK: add message retry logic`
- 相关改动一个 commit，绝不混杂无关重构

---

## 核心操作（mx_gitlab）

### 查看当前用户

```
mx_gitlab:
  action: get_user
```

### 列出项目

```
mx_gitlab:
  action: list_projects
  per_page: 10
```

### 查看项目详情

```
mx_gitlab:
  action: get_project
  project: "12345"
```

### MR 操作

**列出 MR：**
```
mx_gitlab:
  action: list_merge_requests
  project: "12345"
  state: "opened"
```

**创建 MR：**
```
mx_gitlab:
  action: create_merge_request
  project: "12345"
  source_branch: "feature/JIRA-123-user-login"
  target_branch: "main"
  title: "[JIRA-123] 实现用户登录功能"
  description: "## 改动\n- 实现 JWT 登录\n\n## 测试\n- 单元测试通过\n\n## 关联\n- JIRA-123"
```

**审批 MR：**
```
mx_gitlab:
  action: approve_merge_request
  project: "12345"
  mr_iid: 42
```

**查看单条 MR 详情（含合并就绪状态）：**
```
mx_gitlab:
  action: get_merge_request
  project: "12345"
  mr_iid: 42
```
返回关键字段：
- `detailed_merge_status`: `mergeable`（可合并）/ `preparing`（准备中，需等待）/ `checking`（检查中）/ `ci_must_pass`（CI 未通过）/ `not_approved`（未获批准）/ `discussions_not_resolved`（有未解决讨论）
- `has_conflicts`: 是否有冲突
- `blocking_discussions_resolved`: 阻塞性讨论是否已解决
- `pipeline`: 最新 Pipeline 状态

**合并前必须先检查状态（重要）：**

> ⚠️ 直接调用 `merge_merge_request` 而不检查状态会导致 500 错误（MR 未就绪时 GitLab 拒绝合并）

```
# 正确流程：
1. mx_gitlab: get_merge_request → 确认 detailed_merge_status === "mergeable"
2. 如果是 "preparing" 或 "checking" → 等待后重试 get_merge_request
3. 如果是 "ci_must_pass" → CI 未通过，不能合并
4. 如果是 "not_approved" → 需要审批，先 approve_merge_request
5. 确认 mergeable 后 → mx_gitlab: merge_merge_request
```

**合并 MR：**
```
mx_gitlab:
  action: merge_merge_request
  project: "12345"
  mr_iid: 42
```

> ✅ `merge_merge_request` 会自动检查 `detailed_merge_status`，若 MR 未就绪会直接返回错误和原因，无需手动 pre-check。

**更新 MR（设置 Reviewer / Assignee / 标签等）：**
```
# 先搜索 GitLab 用户 ID
mx_gitlab:
  action: search_users
  search: "username_or_name"

# 再设置 reviewer（使用搜索结果中的 id 字段）
mx_gitlab:
  action: update_merge_request
  project: "12345"
  mr_iid: 42
  reviewer_ids: [12345]
```

### CI/CD 操作

**查看 Pipeline：**
```
mx_gitlab:
  action: list_pipelines
  project: "12345"
  per_page: 5
```

**重试失败的 Pipeline：**
```
mx_gitlab:
  action: retry_pipeline
  project: "12345"
  pipeline_id: 67890
```

### Issue 操作

**列出 Issue：**
```
mx_gitlab:
  action: list_issues
  project: "12345"
  state: "opened"
```

**创建 Issue：**
```
mx_gitlab:
  action: create_issue
  project: "12345"
  title: "Bug: 登录页面白屏"
  description: "## 问题\n在 Safari 下登录页面白屏\n\n## 复现\n1. 打开 Safari\n2. 访问 /login"
  labels: ["bug", "frontend"]
```

### 分支操作

**列出分支：**
```
mx_gitlab:
  action: list_branches
  project: "12345"
  search: "feature/"
```

---

## MR 创建规范

标题：`[JIRA-{ID}] {描述}`

描述必须包含：
1. 改了什么，为什么改
2. 如何测试
3. 关联的 Jira Issue 链接

至少指定 1 个 Reviewer。单个 MR 最多 500 行变更。

## Code Review 检查清单

Review MR 时，按顺序检查所有项目：
1. 分支命名符合规范
2. Commit message 清晰且有 scope
3. 代码符合团队风格指南
4. 有对应的测试用例
5. CI pipeline 全绿
6. 无未解决的 Discussion
7. 无硬编码的 secret 或 token
8. 破坏性变更有文档说明

所有项通过才能 approve。评论具体问题时引用行号。

---

## 常见工作流

### 审查指定 MR（完整流程）

```
1. mx_gitlab: list_merge_requests, project: "<id>", state: "opened"
     → 获取 MR 信息（source_branch, target_branch, mr_iid）

2. nodes.run: find ~/www -maxdepth 4 -type d -name '<repo>'
     → 查找本地仓库路径

3. nodes.run: cd <repo-path> && git fetch origin
     → 更新远端分支数据

4. nodes.run: git log origin/<target>..origin/<source> --oneline
     → 查看 commit 列表

5. nodes.run: git diff --stat origin/<target>...origin/<source>
     → 查看文件变更统计

6. nodes.run: git diff origin/<target>...origin/<source> -- <关键文件>
     → 深入审查关键文件的 diff

7. mx_gitlab: list_pipelines, project: "<id>" → 确认 CI 状态

8. mx_gitlab: approve_merge_request, project: "<id>", mr_iid: <iid>（审查通过后）
```

### 查看我的待处理 MR

```
1. mx_gitlab: get_user → 获取用户名
2. mx_gitlab: list_merge_requests, project: "<id>", state: "opened"
     → 列出 open 状态的 MR
3. mx_gitlab: list_pipelines, project: "<id>" → 检查 CI 状态
```

### 创建并合并 Feature MR

```
1. mx_gitlab: create_merge_request
     project: "<id>", source_branch: "feature/xxx", target_branch: "main"
     title: "[JIRA-xxx] desc"
2. mx_gitlab: get_merge_request, project: "<id>", mr_iid: <iid>
     → 等待 detailed_merge_status 变为 "mergeable"
     (刚创建后状态为 "preparing"，需要等待 GitLab 完成检查)
3. mx_gitlab: list_pipelines, project: "<id>" → 确认 CI 通过
4. mx_gitlab: merge_merge_request, project: "<id>", mr_iid: <iid> → 合并
```

### CI 失败处理

```
1. mx_gitlab: list_pipelines, project: "<id>", status: "failed"
2. mx_gitlab: retry_pipeline, project: "<id>", pipeline_id: <id>
```

### 设置 MR Reviewer（完整流程）

```
1. mx_gitlab: search_users, search: "reviewer_name"
     → 从结果中找到目标用户的 id（数字）
2. mx_gitlab: update_merge_request
     project: "<id>", mr_iid: <iid>, reviewer_ids: [<user_id>]
```

### Pipeline 监控（等待 Pipeline 完成）

> ⚠️ 心跳（HEARTBEAT）默认间隔 30m，Anthropic setup-token 下为 1h，不适合实时监控。
>
> 推荐做法：将监控任务写入 `HEARTBEAT.md`，心跳触发时自动检查：
> ```md
> ## 待监控
> - Pipeline #10164 (project: tanka-electron)：等待完成，完成后通知用户
> ```
>
> 或用户要求"立即检查"时，直接调用：
> ```
> mx_gitlab: list_pipelines, project: "<id>", per_page: 5
> ```
> 对比 pipeline id 和状态，判断是否完成。

---

## 注意事项

- `project` 参数：数字 ID（如 `"12345"`）或路径（如 `"my-group/my-project"`），通过 `list_projects` 或 `get_project` 获取
- `mr_iid` 是 MR 在项目内的序号（非全局 ID），从 `list_merge_requests` 或 `create_merge_request` 返回结果中获取
- `account_id` 参数通常省略，工具自动检测已链接的 GitLab 账号
- `mx_link proxy` 获取 MR diff 可能因响应体过大返回 400，优先使用本地 git
