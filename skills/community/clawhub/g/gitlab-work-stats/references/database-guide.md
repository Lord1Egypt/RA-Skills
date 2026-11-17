# GitLab PostgreSQL 数据库结构与查询指南

> 本文档记录 GitLab Omnibus 内置 PostgreSQL 的关键表结构、连接方法和常用分析查询。

---

## 一、数据库连接

### Omnibus 默认连接方式

GitLab Omnibus 内置 PostgreSQL，默认不监听 TCP 端口，仅通过 Unix Socket + peer 认证连接。

**⚠️ 权限要求**：
- 需要 SSH 用户具有执行 psql 命令的权限
- 建议使用受限账户，遵循最小权限原则
- 所有查询必须为只读（SELECT）

**认证原理**：
- peer 认证 = 通过操作系统用户名匹配数据库用户名，无需密码
- 只有具有相应权限的用户才能连接

### 非 Omnibus / 外部数据库

如果 GitLab 使用外部 PostgreSQL，需要配置相应的连接参数。

---

## 二、核心表结构

### users 表

| 列名 | 类型 | 说明 | 统计报告是否需要 |
|------|------|------|------------------|
| id | integer | 用户ID（主键） | ✅ 是 |
| username | varchar | 登录用户名 | ✅ 是 |
| name | varchar | 显示名称 | ✅ 是 |
| state | varchar | 状态（active/locked） | ✅ 是 |
| created_at | timestamp | 创建时间 | ✅ 是 |
| email | varchar | 邮箱 | ❌ **不应收集** |
| admin | boolean | 是否管理员 | ❌ **不应收集** |
| last_sign_in_at | timestamp | 最后登录时间 | ❌ **不应收集** |
| current_sign_in_ip | varchar | 当前登录IP | ❌ **不应收集** |

> **⚠️ 隐私保护**：工作统计报告只需 `id`、`username`、`name`、`state`、`created_at` 字段。
> **禁止收集** `email`、`admin`、`last_sign_in_at`、`current_sign_in_ip` 等敏感个人信息——这些字段与工作统计无关，收集它们会导致隐私风险。

### projects 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | integer | 项目ID |
| name | varchar | 项目名 |
| path | varchar | 项目路径 |
| namespace_id | integer | 命名空间ID |
| description | text | 描述 |
| visibility_level | integer | 可见性（0=私有,10=内部,20=公开） |
| creator_id | integer | 创建者ID |
| archived | boolean | 是否归档 |

### namespaces 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | integer | 命名空间ID |
| name | varchar | 名称 |
| path | varchar | 路径 |
| type | varchar | 类型（Group/User） |
| parent_id | integer | 父级ID |

### merge_requests 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | integer | MR全局ID |
| iid | integer | 项目内序号 |
| title | text | 标题 |
| description | text | 描述 |
| state_id | integer | **状态ID**（不是 state 列） |
| author_id | integer | 作者ID |
| assignee_id | integer | 指派人ID（旧版） |
| target_project_id | integer | 目标项目ID |
| source_branch | text | 源分支 |
| target_branch | text | 目标分支 |
| created_at | timestamp | 创建时间 |
| updated_at | timestamp | 更新时间 |
| merged_at | timestamp | 合并时间 |

**state_id 值映射**：
- 1 = opened
- 2 = closed
- 3 = merged
- 4 = locked

### notes 表（评论/笔记）

> **重要**：正文列名是 `note`，不是 `body`

| 列名 | 类型 | 说明 |
|------|------|------|
| id | integer | 评论ID |
| note | text | **评论正文** |
| noteable_type | varchar | 关联类型（MergeRequest/Issue/Commit等） |
| noteable_id | integer | 关联对象ID |
| author_id | integer | 评论作者ID |
| project_id | integer | 项目ID |
| system | boolean | 是否系统自动生成 |
| created_at | timestamp | 创建时间 |
| discussion_id | varchar | 讨论组ID |
| resolved_at | timestamp | 解决时间 |

### events 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | integer | 事件ID |
| action | integer | **动作类型** |
| author_id | integer | 操作者ID |
| project_id | integer | 项目ID |
| target_type | varchar | 目标类型 |
| target_id | integer | 目标ID |
| created_at | timestamp(含时区) | 创建时间 |

**action 值映射**：
- 1 = created
- 5 = pushed
- 7 = commented
- 12 = merged
- 其他值需根据 GitLab 版本确认

### push_event_payloads 表

| 列名 | 类型 | 说明 |
|------|------|------|
| event_id | integer | 关联 events.id |
| action | smallint | 推送动作 |
| ref_type | smallint | 引用类型 |
| commit_from | bytea | 推送前 commit SHA |
| commit_to | bytea | 推送后 commit SHA |
| ref | text | **分支名** |
| commit_title | varchar | **最新 commit 标题** |
| commit_count | bigint | **推送的 commit 数量** |

> 注意：`commit_from` 和 `commit_to` 是 bytea 类型，显示为十六进制 `\x...`

### project_repositories 表（仓库磁盘路径）

| 列名 | 类型 | 说明 |
|------|------|------|
| id | integer | 仓库记录ID |
| shard_id | integer | 存储分片ID |
| disk_path | text | **磁盘路径**（如 `@hashed/19/58/1958...`） |
| project_id | integer | 关联项目ID |

### merge_request_assignees 表（多对多评审人）

| 列名 | 类型 | 说明 |
|------|------|------|
| merge_request_id | integer | MR ID |
| user_id | integer | 评审人ID |

---

## 三、常用分析查询

### 3.1 用户概览统计

```sql
SELECT 'users' as entity, count(*) FROM users
UNION ALL SELECT 'projects', count(*) FROM projects
UNION ALL SELECT 'groups', count(*) FROM namespaces WHERE type='Group'
UNION ALL SELECT 'merge_requests', count(*) FROM merge_requests
UNION ALL SELECT 'issues', count(*) FROM issues
UNION ALL SELECT 'webhooks', count(*) FROM web_hooks;
```

### 3.2 数据库大小 Top 表

```sql
SELECT schemaname||'.'||relname AS table_name,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
       n_live_tup AS row_count
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC LIMIT 20;
```

### 3.3 用户活跃度排行

```sql
SELECT u.username, u.name,
       count(DISTINCT mr.id) as mr_count,
       count(DISTINCT e.id) as event_count
FROM users u
LEFT JOIN merge_requests mr ON mr.author_id = u.id
  AND mr.created_at >= '{start}' AND mr.created_at < '{end}'
LEFT JOIN events e ON e.author_id = u.id
  AND e.created_at >= '{start}' AND e.created_at < '{end}'
GROUP BY u.id, u.username, u.name
ORDER BY mr_count DESC NULLS LAST LIMIT 20;
```

---

## 四、GitLab Hashed Storage 路径规则

GitLab 12+ 默认使用 hashed storage，仓库物理路径不再使用 `namespace/project.git` 格式。

**路径规则**：
```
/var/opt/gitlab/git-data/repositories/@hashed/{前2位}/{次2位}/{完整SHA256}.git
```

**SHA256 计算方式**：对项目ID进行 SHA256 哈希。

**获取方式**：
```sql
SELECT disk_path FROM project_repositories WHERE project_id = {id};
```

**Git 操作**（只读，以当前 SSH 用户身份执行，不使用 sudo 提权）：
```bash
/opt/gitlab/embedded/bin/git \
  -C /var/opt/gitlab/git-data/repositories/@hashed/XX/YY/XXXX.git \
  log --all --author='{username}' --since='{start}' --format='%h|%ai|%s'
```

> **⚠️ 安全说明**：不使用 `sudo -u git` 提权，直接以当前 SSH 用户身份执行只读 `git log`。需要 SSH 用户具有读取目标仓库目录的权限。仅用于提取 commit 元数据（hash/日期/标题），不访问源代码内容。

---

## 五、注意事项

1. **列名差异**：不同 GitLab 版本的列名可能变化，遇到 "column does not exist" 时先查 `information_schema.columns`
2. **时间范围**：`events.created_at` 带时区（timestamp with time zone），其他表多为 timestamp without time zone，查询时注意时区
3. **系统笔记**：`notes.system = true` 的是自动生成的（如"assigned to @xxx"），`false` 的是用户手写评论
4. **大表性能**：`events`、`notes`、`push_event_payloads` 表可能百万级，务必带 author_id + 时间范围过滤
