---
name: harbor-skills
description: Harbor 镜像仓库综合管理技能。用于 Harbor 日常运维、项目与镜像管理、安全扫描、清理策略、CI/CD 集成、GitOps、复制规则、存储管理、备份恢复、webhook 联动等所有 Harbor 相关操作。当用户提到 Harbor、镜像仓库管理、Docker 镜像、镜像安全扫描、CI/CD 镜像推送/拉取、GitOps 镜像策略、Harbor Webhook 时触发此技能。
user-invocable: true
auth-method: env
version: 1.1.1
env:
  HARBOR_URL:
    description: Harbor 地址（不含 /）
    example: https://harbor.mycompany.com
  HARBOR_TOKEN:
    description: Harbor API Token（Basic Auth 凭证，Base64 编码 user:pass）
    example: Basic YWRtaW46cGFzc3dvcmQ=
    required: true
  HARBOR_BACKUP_DIR:
    description: 备份目录（可选，默认 /data/harbor-backup）
    example: /data/harbor-backup
---

# Harbor Manager

Harbor 是企业级容器镜像仓库（CNCF 毕业项目）。

## 前置要求

### 必需环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `HARBOR_URL` | Harbor 地址（不含 /） | `https://harbor.mycompany.com` |
| `HARBOR_TOKEN` | Harbor API Token（推荐）或 Basic Auth 凭证 | `Basic base64(user:pass)` |

### 认证方式

**方式一：API Token（推荐）**
```bash
# 在 Harbor UI 创建 Robot Account 获取 token
export HARBOR_TOKEN="Basic $(echo -n 'robot$project$account:token' | base64)"
```

**方式二：用户密码**
```bash
export HARBOR_TOKEN="Basic $(echo -n 'username:password' | base64)"
```

### 必需系统工具

| 工具 | 用途 | 说明 |
|------|------|------|
| `curl` | 调用 Harbor API | 必需 |
| `python3` | 运行辅助脚本 | 可选，有脚本时需要 |
| `jq` | JSON 处理 | 建议安装 |

**Docker 相关操作**（备份恢复场景）需要：
- `docker` + `docker-compose`
- `pg_dump`（如安装 PostgreSQL 客户端）
- `rclone`（如需上传至对象存储）

## 快速诊断

```bash
# 检查 Harbor 健康状态
curl -s -H "Authorization: $HARBOR_TOKEN" "$HARBOR_URL/api/v2.0/health" | jq .

# 列出所有项目
curl -s -H "Authorization: $HARBOR_TOKEN" "$HARBOR_URL/api/v2.0/projects" | jq '.[].name'
```

## 项目管理

### 创建项目

```bash
curl -X POST "$HARBOR_URL/api/v2.0/projects" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "my-app",
    "public": false,
    "metadata": {"description": "业务镜像仓库", "storage_quota": "500G"}
  }'
```

### 修改存储配额（Python）

```python
# refs: references/harbor-api.md
import requests, os, base64

url = os.environ['HARBOR_URL']
token = os.environ['HARBOR_TOKEN']
auth = {'Authorization': token}

# 查找项目ID
proj = requests.get(f"{url}/api/v2.0/projects", params={"name": "my-app"}, headers=auth).json()[0]
pid = proj["project_id"]

# 更新配额（单位：bytes，500G = 500*1024^3）
requests.put(f"{url}/api/v2.0/projects/{pid}",
    headers=auth, json={"metadata": {"storage_quota": str(500*1024**3)}})
print(f"项目 {pid} 配额已更新为 500G")
```

## 镜像管理

### 列出镜像

```bash
# 按项目列出所有镜像
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories" | jq '.[].name'

# 查看某镜像的所有标签
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/tags" | jq '.[].name'

# 镜像详情（含大小、扫描状态）
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/artifacts?with_tag=true&with_scan_overview=true" \
  | jq '.[].{tags: .tag, size: .size, scan: .scan_summary}'
```

### 删除镜像（按标签）

```bash
# 删除指定标签（保留其他标签）
curl -X DELETE \
  -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/tags/v1.2.3"

# 批量删除（用 jq 生成）
TAGS=$(curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/tags" \
  | jq -r '.[].name | select(startswith("v0"))')
for tag in $TAGS; do
  echo "删除: $tag"
  curl -X DELETE -H "Authorization: $HARBOR_TOKEN" \
    "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/tags/$tag"
done
```

### 删除不留用的镜像（Python）

```python
# refs: references/cleanup-policy.md
import requests, os

def delete_artifact(project, repo, reference, dry_run=True):
    url = f"{os.environ['HARBOR_URL']}/api/v2.0/projects/{project}/repositories/{repo}/artifacts/{reference}"
    auth = {'Authorization': os.environ['HARBOR_TOKEN']}
    if dry_run:
        print(f"[演练] 应删除: {url}")
    else:
        r = requests.delete(url, headers=auth)
        print(f"[已删除] {reference}" if r.status_code == 200 else f"[失败] {r.status_code}")
```

**注意**：Harbor GC 需要手动触发，删除后运行垃圾回收。

## 清理策略

### 配置保留策略

策略规则在 `references/cleanup-policy.md` 中有详细说明。

典型场景：

| 场景 | 规则 |
|------|------|
| 保留最近 N 个版本 | `kept_tags >= N`（按 push 时间排序） |
| 删除 N 天前镜像 | `pushed_time < now - N days` |
| 保留带有特定前缀的标签 | `tag =~ ^release-` |
| 清理快照版本 | `tag =~ ^snap-` |

### 演练模式（评估影响）

```bash
python3 /root/.openclaw/workspace/skills/harbor-skills/scripts/cleanup_dryrun.py \
  --project my-app --repo my-app--api --policy "保留最近5个" --url "$HARBOR_URL"
```

### 清理策略推荐 YAML 格式

```yaml
# 清理策略示例（用于自动化脚本生成）
project: my-app
repo: my-app--api
rules:
  - action: delete
    condition: tag not in recent(5)
    exclude:
      tags: ["latest", "stable", "release-*"]
  - action: delete
    condition: pushed_time < days_ago(30)
    exclude:
      tags: ["latest"]
```

## 垃圾回收（GC）

```bash
# 1. 触发 GC
curl -X POST "$HARBOR_URL/api/v2.0/system/gc/schedule" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"schedule":{"type":"manual"}}'

# 2. 查看 GC 状态
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/system/gc" | jq '.[] | {id: .id, status: .job_status, start: .start_time}'

# 3. GC 完成后清理孤儿 Blob
curl -X POST "$HARBOR_URL/api/v2.0/system/gc/schedule" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"schedule":{"type":"none"}, "dry_run": false}'
```

> ⚠️ GC 期间 Harbor 会进入维护模式，建议在低峰期执行。

## 存储使用情况

```bash
# 查看项目存储使用
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app" | jq '{name: .name, storage: .metadata.storage_quota, used: .metadata.storage_quota_used}'

# 查看系统总体存储
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/statistics" | jq '{total: .total_storage, used: .used_storage, free: .free_storage}'
```

## 复制管理

### 创建复制规则

```bash
curl -X POST "$HARBOR_URL/api/v2.0/replication/policies" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "backup-to-dr-site",
    "src_registry": {"id": 1, "name": "local"},
    "dest_registry": {"id": 2, "name": "dr-harbor"},
    "filters": [
      {"type": "name", "value": "my-app/.*"},
      {"type": "tag", "value": ".*"}
    ],
    "trigger": {"type": "scheduled", "trigger_settings": {"cron": "0 2 * * * *"}},
    "deletion": true,
    "override": true
  }'
```

### 触发立即执行

```bash
curl -X POST "$HARBOR_URL/api/v2.0/replication/executions" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"policy_id": 3}'

# 查看执行状态
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/replication/executions?policy_id=3" \
  | jq '.[] | {id: .id, status: .status, summary: .status_ext}'
```

## 代理缓存（Proxy Cache）

### 创建代理缓存项目

```bash
curl -X POST "$HARBOR_URL/api/v2.0/projects" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "proxy-cache-dockerhub",
    "public": false,
    "metadata": {
      "proxy_cache_name": "dockerhub",
      "description": "Docker Hub 代理缓存"
    }
  }'
```

### 使用代理缓存拉取镜像

```bash
# Pod 层面配置代理（通过 /etc/docker/daemon.json）
{
  "registry-mirrors": ["https://proxy-cache-dockerhub.harbor.mycompany.com"]
}

# 或手动拉取
docker pull proxy-cache-dockerhub.library/nginx:latest
```

## 漏洞扫描

### 触发全量扫描

```bash
# 扫描单个镜像
curl -X POST \
  -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/artifacts/sha256:abc123.../scan"

# 扫描整个项目所有镜像
curl -X POST \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  "$HARBOR_URL/api/v2.0/projects/my-app/scanAll" \
  -d '{"selector":"all"}'
```

### 获取扫描报告

```bash
# 获取镜像扫描摘要
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/artifacts/v1.2.3?with_scan_summary=true" \
  | jq '{scan: .scan_summary}'

# 导出详细扫描报告（CSV格式）
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/repositories/my-app--api/artifacts/v1.2.3/scan_report?accept=text/csv"
```

### 自动扫描策略

```bash
# 设置自动化扫描：镜像推送后自动触发扫描
curl -X PUT "$HARBOR_URL/api/v2.0/projects/my-app" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"auto_scan": true}'
```

## 镜像签名（Notary）

```bash
# 1. 启用 Notary（需在 Harbor 部署时配置）
# 2. 对镜像签名（需安装 docker content trust 相关工具）
DOCKER_CONTENT_TRUST=1
DOCKER_CONTENT_TRUST_SERVER="$HARBOR_URL"
docker pull my-app/my-app--api:v1.2.3
docker tag my-app/my-app--api:v1.2.3 harbor.mycompany.com/my-app/my-app--api:v1.2.3
docker push harbor.mycompany.com/my-app/my-app--api:v1.2.3

# 3. 验证签名
DOCKER_CONTENT_TRUST=1
docker pull harbor.mycompany.com/my-app/my-app--api:v1.2.3
```

## 机器人账号（Robot Account）

### 创建项目机器人账号

```bash
curl -X POST "$HARBOR_URL/api/v2.0/projects/my-app/robots" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ci-pipeline",
    "description": "CI/CD流水线使用",
    "access": [
      {"resource": "/project/my-app/repository", "action": "push"},
      {"resource": "/project/my-app/repository", "action": "pull"}
    ],
    "expires_at": 0  # 永不过期
  }'
```

### CI 使用机器人账号

```bash
# 获取机器人 token（创建时返回的 credentials.secret）
docker login "$HARBOR_URL" -u "robot$my-app$ci-pipeline" -p "$ROBOT_TOKEN"
```

## RBAC 权限管理

```bash
# 添加项目成员
curl -X POST "$HARBOR_URL/api/v2.0/projects/my-app/members" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member_user": {"username": "dev-user"}, "role_id": 2}'  # 2=开发者

# 角色ID说明：1=项目管理员, 2=开发者, 3=访客, 4=维护者
```

## Webhook

### 创建 Webhook

```bash
curl -X POST "$HARBOR_URL/api/v2.0/projects/my-app/webhook" \
  -H "Authorization: $HARBOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ci-trigger",
    "targets": [{
      "type": "http",
      "address": "https://ci.mycompany.com/webhook/harbor",
      "skip_cert_verify": true,
      "auth_header": "Bearer xxxxx"
    }],
    "event_types": ["SCANNING_COMPLETED", "PUSH_ARTIFACT", "DELETE_ARTIFACT"]
  }'
```

Webhook payload 示例：
```json
{
  "type": "PUSH_ARTIFACT",
  "occur_at": 1700000000,
  "artifact": {
    "media_type": "application/vnd.docker.distribution.manifest.v2+json",
    "digest": "sha256:abc123",
    "tags": ["v1.2.3"]
  },
  "project": {"id": 1, "name": "my-app"},
  "repository": {"name": "my-app--api"}
}
```

## 审计日志

```bash
# 查看项目审计日志
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/logs?page=1&page_size=20" | jq '.'

# 导出为 CSV
curl -s -H "Authorization: $HARBOR_TOKEN" \
  "$HARBOR_URL/api/v2.0/projects/my-app/logs?page=1&page_size=100&sort=op_time_desc" \
  | jq -r '.[] | [.op_time, .username, .resource, .operation] | @csv'
```

## 备份与恢复

> ⚠️ 备份恢复需要 Docker 和相关工具，请在有权限的环境中使用。

### 备份（Harbor 数据）

```bash
# 备份清单（推荐 cron 定期执行）
# refs: references/backup-recovery.md
BACKUP_DIR="${HARBOR_BACKUP_DIR:-/data/harbor-backup}"
DATE=$(date +%Y%m%d_%H%M%S)

# 1. 备份数据库（如有 docker 环境）
# docker exec -t harbor-db pg_dump -U postgres registry > "$BACKUP_DIR/harbor-db-$DATE.sql"

# 2. 备份核心配置
# tar czf "$BACKUP_DIR/harbor-config-$DATE.tar.gz" /data/harbor/redis /data/harbor/registry

# 3. 上传至对象存储（如有 rclone）
# rclone sync "$BACKUP_DIR/" "s3:my-bucket/harbor-backups/"

echo "备份完成: $DATE"
```

### 恢复

```bash
# 1. 停止 Harbor
cd /opt/harbor && docker-compose down

# 2. 恢复数据库
# docker exec -i harbor-db psql -U postgres registry < "$BACKUP_DIR/harbor-db-$DATE.sql"

# 3. 恢复配置文件
# tar xzf "$BACKUP_DIR/harbor-config-$DATE.tar.gz" -C /

# 4. 重启 Harbor
docker-compose up -d
```

## 合规性检查

```bash
# 等保 2.0 / GDPR 检查项（详见 references/compliance.md）
python3 /root/.openclaw/workspace/skills/harbor-skills/scripts/compliance_check.py \
  --harbor-url "$HARBOR_URL" --auth "$HARBOR_TOKEN" \
  --standard "等保2级" --output /tmp/harbor-compliance-report.html
```

检查项包括：
- ✅ 匿名访问是否关闭
- ✅ Robot Account 是否有过期设置
- ✅ 镜像扫描覆盖率
- ✅ CVE 漏洞是否在可接受阈值内
- ✅ 审计日志保留时长
- ✅ HTTPS 强制开启
- ✅ 密码策略配置

## CI/CD 集成速查

| 工具 | 集成方式 |
|------|---------|
| **Jenkins** | `withCredentials([string(credentialsId: 'harbor', variable: 'HARBOR_TOKEN')])` + `docker login` |
| **GitLab CI** | `image: docker:latest` + `before_script` 登录 |
| **GitHub Actions** | `uses: docker/login-action@v3` |
| **Argo CD** | Application YAML 中引用 Image Updater 或使用 Argo CD Image Updater |
| **Tekton** | `Task` 中用 `dockerauth` secret 登录后 `docker push` |

## GitOps 配置管理

参考 `references/gitops.md` 了解更多 GitOps 工具与 Harbor 的集成方式。

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/harbor-api.md` | 完整 Harbor API v2.0 参考（认证、请求格式、错误码） |
| `references/cleanup-policy.md` | 镜像清理策略详细规则与演练脚本 |
| `references/webhook.md` | Webhook 事件类型与 payload 格式说明 |
| `references/backup-recovery.md` | 备份恢复详细步骤与灾难恢复预案 |
| `references/gitops.md` | GitOps 集成（Argo CD / Flux / Helm） |
| `references/compliance.md` | 等保2.0 / GDPR 合规检查项说明 |
| `scripts/cleanup_dryrun.py` | 清理演练脚本 |
| `scripts/compliance_check.py` | 合规性检查脚本 |
| `scripts/robot_account.py` | 机器人账号创建与轮换脚本 |
