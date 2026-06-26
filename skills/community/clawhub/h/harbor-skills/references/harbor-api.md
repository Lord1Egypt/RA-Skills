# Harbor API v2.0 参考

## 认证

### Basic Auth（默认）
```bash
curl -u "username:password" "https://harbor.example.com/api/v2.0/projects"
```

### Bearer Token（推荐）
```bash
# 1. 获取 Token
TOKEN=$(curl -s -X POST "https://harbor.example.com/api/v2.0/tokens" \
  -u "username:password" \
  -H "Content-Type: application/json" \
  -d '{"principal":"username","password":"password"}' | jq -r '.token')

# 2. 使用 Token
curl -H "Authorization: Bearer $TOKEN" "https://harbor.mycompany.com/api/v2.0/projects"
```

### Robot Account Token
```bash
curl -H "Authorization: Basic $(echo -n 'robot$project$account:TOKEN_SECRET' | base64)" \
  "https://harbor.mycompany.com/api/v2.0/projects"
```

## 基础信息

| 项目 | 地址 |
|------|------|
| Base URL | `{HARBOR_URL}/api/v2.0` |
| 健康检查 | `GET /health` |
| 系统统计 | `GET /statistics` |
| 版本 | `GET /version` |

## 项目 API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/projects` | 列出项目（`?name=xx&public=true`） |
| `POST` | `/projects` | 创建项目 |
| `GET` | `/projects/{id}` | 获取项目详情 |
| `PUT` | `/projects/{id}` | 更新项目 |
| `DELETE` | `/projects/{id}` | 删除项目（需先清空镜像） |
| `GET` | `/projects/{id}/metadatas` | 获取项目元数据 |
| `PUT` | `/projects/{id}/metadatas/{key}` | 更新单个元数据 |
| `POST` | `/projects/{id}/members` | 添加成员 |
| `GET` | `/projects/{id}/members` | 列出成员 |
| `DELETE` | `/projects/{id}/members/{mid}` | 删除成员 |
| `POST` | `/projects/{id}/robots` | 创建机器人账号 |
| `GET` | `/projects/{id}/robotAccounts` | 列出机器人账号 |
| `PUT` | `/projects/{id}/robotAccounts/{id}` | 更新机器人账号 |
| `DELETE` | `/projects/{id}/robotAccounts/{id}` | 删除机器人账号 |
| `POST` | `/projects/{id}/webhook` | 创建 Webhook |
| `GET` | `/projects/{id}/webhook` | 列出 Webhook |
| `DELETE` | `/projects/{id}/webhook/{wid}` | 删除 Webhook |

### 项目元数据 Key

| Key | 说明 | 示例值 |
|-----|------|--------|
| `public` | 是否公开 | `true` / `false` |
| `storage_quota` | 存储配额 | `500G` / `-1`（不限） |
| `retention_id` | 保留策略 ID | `1` |
| `auto_scan` | 自动扫描 | `true` / `false` |
| `severity` | 安全扫描级别 | `none` / `low` / `medium` / `high` / `critical` |
| `prevent_vulnerable_images` | 阻止漏洞镜像拉取 | `true` / `false` |
| `prevent_vulnerable_images_accept` | 允许拉取的最低漏洞等级 | `low` |

## 镜像（Artifact）API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/projects/{pid}/repositories` | 列出仓库 |
| `DELETE` | `/projects/{pid}/repositories/{repo}` | 删除仓库 |
| `GET` | `/projects/{pid}/repositories/{repo}/artifacts` | 列出制品（含标签） |
| `GET` | `/projects/{pid}/repositories/{repo}/artifacts?with_tag=true&with_scan_overview=true` | 含扫描摘要 |
| `DELETE` | `/projects/{pid}/repositories/{repo}/artifacts/{reference}` | 删除制品 |
| `GET` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/tags` | 列出标签 |
| `POST` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/tags` | 创建标签 |
| `DELETE` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/tags/{tag}` | 删除标签 |
| `POST` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/scan` | 触发扫描 |
| `GET` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/scan_report` | 获取扫描报告 |
| `GET` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/additions/vulnerabilities` | 漏洞详情 |
| `GET` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/additions/build_history` | 构建历史 |

**reference** 可以是：
- `sha256:xxxx`（Digest）
- `v1.2.3`（标签）

## 扫描 API

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/projects/{pid}/repositories/{repo}/artifacts/{ref}/scan` | 扫描指定镜像 |
| `POST` | `/projects/{pid}/scanAll` | 扫描项目所有镜像 |
| `GET` | `/projects/{pid}/scanner/capabilities` | 扫描器能力 |
| `GET` | `/system/scanAll/executions` | 全量扫描执行记录 |

## 复制 API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/replication/policies` | 列出复制策略 |
| `POST` | `/replication/policies` | 创建复制策略 |
| `PUT` | `/replication/policies/{id}` | 更新策略 |
| `DELETE` | `/replication/policies/{id}` | 删除策略 |
| `GET` | `/replication/executions` | 列出执行记录 |
| `POST` | `/replication/executions` | 触发执行 |
| `GET` | `/replication/executions/{id}/tasks` | 查看执行任务 |
| `POST` | `/replication/executions/{id}/stop` | 停止执行 |

### 复制过滤器

```json
{
  "filters": [
    {"type": "name", "value": "library/.*"},
    {"type": "tag", "value": "latest"},
    {"type": "label", "value": "env=prod"}
  ]
}
```

## 系统管理 API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/system/gc` | GC 执行记录 |
| `POST` | `/system/gc/schedule` | 触发 GC 或设置计划 |
| `GET` | `/system/gc/{id}` | GC 执行详情 |
| `GET` | `/system/garbagecollections/{id}` | GC 详情（新版 API） |
| `PUT` | `/system/gc/{id}/stop` | 停止 GC |
| `GET` | `/system/configurations` | 获取系统配置 |
| `PUT` | `/system/configurations` | 更新系统配置 |
| `GET` | `/audit-logs` | 全系统审计日志 |
| `GET` | `/projects/{pid}/logs` | 项目审计日志 |

### GC 调度类型

```json
// 手动触发
{"schedule": {"type": "Manual"}}

// 每日凌晨2点
{"schedule": {"type": "Daily", "trigger_settings": {"cron": "0 0 2 * * *"}}}

// 每周日
{"schedule": {"type": "Weekly", "trigger_settings": {"cron": "0 0 0 * * 0"}}}

// 关闭自动GC
{"schedule": {"type": "None"}}
```

## 错误码

| HTTP Status | 说明 |
|-------------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 冲突（如项目名已存在） |
| 412 | 前置条件失败（如删除有镜像的项目） |
| 500 | 服务器内部错误 |
