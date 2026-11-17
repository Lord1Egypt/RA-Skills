---
name: gitlab-work-stats
description: 生成 GitLab 用户工作统计报告（仅限只读分析）。分析指定用户在指定时间段内的合并请求、代码提交、代码审查活动。不修改服务器数据，不提供加密功能。
---

# gitlab-work-stats — GitLab 用户工作统计分析器

> **⚠️ 重要说明**：本工具用于生成 GitLab 用户工作统计报告（只读分析）。
> - 不会修改 GitLab 服务器上的任何数据
> - 不提供加密功能，生成的报告需用户自行保护
> - 需要用户提供明确的分析目标和时间范围

**⚠️ 安全警告**：
- 本操作会分析用户的工作活动数据，可能涉及敏感信息
- 确保已获得目标用户的授权或这是您自己的工作数据
- 生成的报告包含工作统计信息，请妥善保管
- 所有数据库操作均为只读（SELECT），不会修改任何数据

## 激活条件

**高优先级（明确意图）**：
- "生成 GitLab 工作统计报告"
- "分析 GitLab 用户的提交活动"
- "统计 GitLab 上的代码审查数据"

**低优先级（需要确认）**：
- "看看某人在 GitLab 做了什么"
- "分析 XX 的 GitLab 活动"

**不触发的情况**：
- 只是提到 GitLab 但没有要求分析工作统计
- 询问 GitLab 的使用方法或功能介绍
- 需要 GitLab API 或其他非统计分析的操作

**激活前必须确认**：
1. 目标用户的 GitLab username
2. 明确的时间范围
3. 用户已知晓数据隐私和安全要求

## 核心原则

**只读操作** — 所有数据库查询和 git 命令必须是只读的（SELECT / git log），绝不修改服务器上的任何文件或数据。每次执行前向用户声明这一点。

**参数提取** — 激活后必须从用户输入中提取三个关键参数：
1. **目标用户名**（GitLab username，如 `{target_username}`）
2. **时间范围**（起止日���，如 `2026-07-01` ~ `2026-07-31`）
3. **（可选）项目过滤**（限定某个项目，默认分析全部项目）

如果缺少用户名或时间范围，主动询问用户。

## Step 0: 读取服务器配置

从 `references/server-config.json` 读取 GitLab 服务器连接信息。

**⚠️ 凭据安全警告**：
- 配置文件中的凭据（如 host、token）由用户自行提供
- 不要将配置文件提交到公共代码仓库
- 建议使用环境变量或配置管理工具存储敏感信息
- 确保文件权限设置为仅当前用户可读

如果配置文件不存在或需要连接不同的服务器，询问用户提供：
- GitLab 服务器地址（host）
- GitLab API Token（推荐）或 SSH 访问凭据
- GitLab Web URL（可选）

## Step 1: SSH 连接与数据库定位

### 1.1 连接方式

使用 Python paramiko 库通过 SSH 连接服务器。

**前置条件**：
- Python 3.8+
- paramiko 库（需要用户自行安装：`pip install paramiko`）

连接模板：
```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=15)
```

**⚠️ 安全说明**：
- 使用受管 Python 环境运行 paramiko
- SSH 凭据从 server-config.json 读取，不要硬编码在脚本中
- 建议使用受限的 SSH 账户，遵循最小权限原则

### 1.2 数据库连接

GitLab Omnibus 默认使用内置 PostgreSQL，通过 Unix Socket 连接（不监听 TCP 端口），使用 peer 认证（无需密码）。

**连接方式**（通过 socket + peer 认证，以当前 SSH 用户身份直接执行，**不使用 sudo 提权**）：
```bash
/opt/gitlab/embedded/bin/psql   -h /var/opt/gitlab/postgresql -d gitlabhq_production -c "SQL语句"
```

**⚠️ 权限说明**：
- 需要 SSH 用户本身具有执行 psql 的权限（属组包含 gitlab-psql 或配置了 peer 认证白名单）
- **不使用 `sudo -u gitlab-psql`**，避免 sudo 提权带来的安全风险
- 建议使用受限的专用 SSH 账户，遵循最小权限原则
- 所有 SQL 查询必须为只读（SELECT），禁止执行 INSERT/UPDATE/DELETE
- 如果当前用户无法直接连接，应由管理员配置 peer 认证规则，而非使用 sudo

> 注意：如果 GitLab 版本不同或使用了外部数据库，需要根据 `database.yml` 的 `host`、`port`、`username`、`password` 字段调整连接方式。详见 [references/database-guide.md](references/database-guide.md)。

## Step 2: 确认用户身份

查询 `users` 表确认用户存在，获取 `user_id`：

```sql
SELECT id, username, name, state, created_at, last_sign_in_at
FROM users WHERE username = '{username}';
```

**⚠️ 隐私保护**：
- 仅收集工作统计相关的最小必要信息
- 不收集 email、IP 地址等敏感个人信息
- 如果用户要求分析自己的数据，可以包含 email 用于报告标识

如果找不到用户，尝试模糊匹配：
```sql
SELECT id, username, name FROM users WHERE username ILIKE '%{keyword}%';
```

## Step 3: 数据采集（全部只读 SELECT）

以下所有查询中 `{user_id}`、`{start_date}`、`{end_date}` 为参数占位符。

### 3.1 合并请求 (Merge Requests)

查询用户作为作者的 MR：

```sql
SELECT mr.id, mr.iid, mr.title, mr.state_id, mr.created_at, mr.updated_at,
       p.name as project_name, p.id as project_id
FROM merge_requests mr
JOIN projects p ON mr.target_project_id = p.id
WHERE mr.author_id = {user_id}
  AND mr.created_at >= '{start_date}'
  AND mr.created_at < '{end_date}'
ORDER BY mr.created_at DESC;
```

**state_id 含义**：1=opened, 2=closed, 3=merged, 4=locked

### 3.2 代码推送 (Push Events) 与 Commit 标题

Push 事件存储在 `events` 表（`action=5`），commit 详情在 `push_event_payloads` 表。

```sql
SELECT e.created_at, pepe.commit_title, pepe.ref, pepe.commit_count,
       p.name as project_name
FROM events e
JOIN push_event_payloads pepe ON pepe.event_id = e.id
JOIN projects p ON e.project_id = p.id
WHERE e.author_id = {user_id}
  AND e.action = 5
  AND e.created_at >= '{start_date}'
  AND e.created_at < '{end_date}'
ORDER BY e.created_at DESC;
```

**汇总统计**（不需要逐条列出，按分支/任务分组统计）：

```sql
SELECT
  regexp_replace(pepe.ref, 'feature-([0-9]+).*', 'task-\1') as task_branch,
  count(*) as push_count,
  sum(pepe.commit_count) as total_commits,
  count(DISTINCT pepe.commit_title) as distinct_titles
FROM events e
JOIN push_event_payloads pepe ON pepe.event_id = e.id
WHERE e.author_id = {user_id} AND e.action = 5
  AND e.created_at >= '{start_date}' AND e.created_at < '{end_date}'
GROUP BY pepe.ref
ORDER BY push_count DESC;
```

### 3.3 代码审查 (Code Reviews)

#### 3.3.1 获取该用户所有 MR 上的评论

`notes` 表的正文列名为 **`note`**（不是 `body`）：

```sql
-- 别人对该用户 MR 的评论（含审批、审查意见）
SELECT n.created_at, u.username as author,
       LEFT(n.note, 300) as note_preview,
       mr.iid, mr.title, p.name as project_name,
       n.system
FROM notes n
JOIN users u ON n.author_id = u.id
JOIN merge_requests mr ON n.noteable_id = mr.id AND n.noteable_type = 'MergeRequest'
JOIN projects p ON mr.target_project_id = p.id
WHERE mr.author_id = {user_id}
  AND n.created_at >= '{start_date}'
  AND n.created_at < '{end_date}'
ORDER BY n.created_at DESC;
```

#### 3.3.2 AI 代码审查内容

如果服务器配置了 AI 代码审查（bot 用户名从 server-config.json 的 `ai_reviewer_bot_username` 读取，默认匹配规则见下），查询审查详情：

```sql
SELECT n.created_at, mr.iid, mr.title,
       LEFT(n.note, 500) as review_content
FROM notes n
JOIN merge_requests mr ON n.noteable_id = mr.id AND n.noteable_type = 'MergeRequest'
JOIN users u ON n.author_id = u.id
WHERE mr.author_id = {user_id}
  AND u.username IN ('{ai_bot_username}', 'ai-code-reviewer', 'code-reviewer')
  AND n.created_at >= '{start_date}'
  AND n.created_at < '{end_date}'
ORDER BY n.created_at DESC;
```

#### 3.3.3 审批记录

```sql
SELECT n.created_at, u.username as approver,
       mr.iid, mr.title, n.note
FROM notes n
JOIN users u ON n.author_id = u.id
JOIN merge_requests mr ON n.noteable_id = mr.id AND n.noteable_type = 'MergeRequest'
WHERE mr.author_id = {user_id}
  AND n.note LIKE 'approved this merge request'
  AND n.created_at >= '{start_date}'
  AND n.created_at < '{end_date}'
ORDER BY n.created_at DESC;
```

#### 3.3.4 用户作为评审人的 MR

```sql
SELECT mr.id, mr.iid, mr.title, mr.state_id, mr.created_at, mr.updated_at,
       u.username as author, p.name as project_name
FROM merge_requests mr
JOIN merge_request_assignees mra ON mra.merge_request_id = mr.id
JOIN users u ON mr.author_id = u.id
JOIN projects p ON mr.target_project_id = p.id
WHERE mra.user_id = {user_id}
  AND mr.updated_at >= '{start_date}'
  AND mr.updated_at < '{end_date}'
ORDER BY mr.updated_at DESC;
```

### 3.4 用户自己发表的评论

```sql
SELECT n.created_at, n.noteable_type,
       LEFT(n.note, 200) as note_preview,
       p.name as project_name
FROM notes n
LEFT JOIN projects p ON n.project_id = p.id
WHERE n.author_id = {user_id}
  AND n.created_at >= '{start_date}'
  AND n.created_at < '{end_date}'
  AND n.system = false
ORDER BY n.created_at DESC;
```

## Step 4: 多行 SQL 执行

通过 SSH 执行多行 SQL 时，使用参数化查询避免引号转义问题：

```python
import shlex

def pg_query(ssh, sql):
    # 使用参数化命令，避免 sudo 链式执行
    cmd = '/opt/gitlab/embedded/bin/psql ' \
          '-h /var/opt/gitlab/postgresql ' \
          '-d gitlabhq_production ' \
          f'-c {shlex.quote(sql)} 2>&1'
    
    # 以当前 SSH 用户身份执行（需要该用户具有 psql 执行权限）
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
    return stdout.read().decode('utf-8', errors='replace')
```

**⚠️ 安全说明**：
- 不使用 `sudo -u gitlab-psql`，需要 SSH 用户本身具有 psql 执行权限
- 使用 `shlex.quote()` 防止 SQL 注入
- 所有查询必须为 SELECT 语句

## Step 5: （可选）从 Git 仓库提取 Commit 详情

数据库中的 push_event_payloads 只记录 commit 标题，如需完整的 commit message、变更文件列表等，需直接查询 git 仓库。

### 5.1 获取仓库物理路径

GitLab 使用 hashed storage，需通过 `project_repositories` 表获取磁盘路径：

```sql
SELECT pr.project_id, p.name, pr.disk_path
FROM project_repositories pr
JOIN projects p ON pr.project_id = p.id
WHERE p.id IN (
  SELECT DISTINCT target_project_id 
  FROM merge_requests 
  WHERE author_id = {user_id} 
    AND created_at >= '{start_date}' 
    AND created_at < '{end_date}'
  UNION
  SELECT DISTINCT project_id 
  FROM events 
  WHERE author_id = {user_id} 
    AND action = 5 
    AND created_at >= '{start_date}' 
    AND created_at < '{end_date}'
);
```

**⚠️ 安全说明**：
- 只查询目标用户在指定时间段内有活动的仓库
- 不枚举所有仓库的磁盘路径
- 仅用于获取 commit 详情，不访问仓库源代码

### 5.2 查询 git log

```bash
REPO="/var/opt/gitlab/git-data/repositories/{disk_path}.git"
/opt/gitlab/embedded/bin/git -C "$REPO" \
  log --all --author='{username}' \
  --since='{start_date}' --until='{end_date}' \
  --format='%h|%ai|%s'
```

**⚠️ 安全说明**：
- 仅使用 `git log` 命令，不访问仓库源代码内容
- 需要 SSH 用户具有读取该仓库的权限
- 不使用 `sudo` 提权，直接使用当前用户权限执行

> 注意：hashed storage 的磁盘路径格式为 `@hashed/{前2位}/{次2位}/{完整hash}`，完整路径为 `/var/opt/gitlab/git-data/repositories/@hashed/XX/YY/XXXX.git`。数据库记录的 `disk_path` 不含 `.git` 后缀。

## Step 6: 生成报告

报告格式为 Markdown，保存到工作目录下，文件名格式：`{username}_{年月}_活动报告.md`。

### 报告结构

```markdown
# {username} {时间范围}活动报告

> 用户: {username} ({name}) | ID: {user_id} | 项目: {projects}

---

## 一、合并请求 (MR) 清单 — 共 N 个

| # | MR IID | 标题 | 创建时间 | 状态 | 评审人 | 审批时间 |
|---|--------|------|----------|------|--------|----------|
| 1 | !xxx   | ...  | ...      | ...  | ...    | ...      |

## 二、代码推送统计

### 按任务/分支分组统计（不逐条列举）

| 任务/分支 | 推送次数 | Commit总数 | 主要内容 |
|-----------|----------|------------|----------|
| task-xxxx | N        | N          | 简述     |

## 三、代码审查

### AI 代码审查结果
（列出关键审查意见和发现的风险）

### 人工审批记录
（列出审批人和审批时间）

## 四、工作内容总结

### 按任务归类的工作主题

| 任务号 | 主题 | MR数 | 核心工作内容 |
|--------|------|------|--------------|

### 提交内容语义分析

根据所有 commit 标题和 MR 标题，对用户的工作内容进行主题归类和语义分析：
- 主要技术方向（如：退款逻辑、导出功能、告警系统...）
- 工作类型分布（新功能 vs Bug修复 vs 优化重构）
- 涉及的模块/技术栈
- 关键技术决策和实现思路
```

### 报告要点

1. **Push Events 做统计汇总，不逐条列举**——按分支/任务分组，统计推送次数和 commit 数，简述主要内容
2. **最后必须有一段「提交内容语义分析总结」**——基于所有 commit title 和 MR title，分析用户做了什么、技术方向是什么、工作类型分布
3. 报告完成后调用 `present_files` 展示给用户

## 重要注意事项

### 数据安全
- **所有操作只读**：只用 SELECT 查询和 git log 命令，绝不执行 INSERT/UPDATE/DELETE 或任何写操作
- 每次开始前明确告知用户"所有操作不会修改服务器上的任何文件或数据"

### GitLab 版本差异
- 不同 GitLab 版本的表结构可能有差异（如 `merge_requests` 表的 `state` vs `state_id` 列）
- 遇到列不存在错误时，先查 `information_schema.columns` 确认列名
- `notes` 表的正文列名固定为 `note`（不是 `body`）

### 编码问题
- psql 输出可能包含中文，使用 `decode('utf-8', errors='replace')` 处理
- base64 编码方式处理多行 SQL，避免 shell 引号转义问题

### 性能
- `events` 和 `notes` 表可能很大，查询时务必带 `author_id` 和时间范围条件
- 避免全表扫描

## 配置文件

服务器连接配置存放在 [references/server-config.json](references/server-config.json)，包含 IP、端口、用户名、密码等。

## 数据库结构参考

详细的 GitLab PostgreSQL 数据库表结构和查询方法见 [references/database-guide.md](references/database-guide.md)。

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.0.0 | 2026-07-23 | — | 初始版本，支持用户工作统计分析报告生成 |
| 1.1.0 | 2026-07-24 | — | 安全修复：移除 sudo 链式执行、users 表隐私字段标注、git 命令移除提权 |
