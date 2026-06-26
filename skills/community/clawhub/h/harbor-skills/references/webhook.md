# Webhook 事件类型与使用指南

## 支持的事件类型

| 事件类型 | 触发时机 |
|---------|---------|
| `PUSH_ARTIFACT` | 镜像/制品被推送 |
| `PULL_ARTIFACT` | 镜像/制品被拉取 |
| `DELETE_ARTIFACT` | 镜像/制品被删除 |
| `SCANNING_FAILED` | 漏洞扫描失败 |
| `SCANNING_COMPLETED` | 漏洞扫描完成 |
| `TAG_RETENTION` | 保留策略执行完成 |
| `REPLICATION` | 复制任务完成 |
| `QUOTA_EXCEED` | 存储配额超限 |
| `CONFIG_CHANGE` | 项目配置变更 |

## Webhook Payload 结构

```json
{
  "type": "PUSH_ARTIFACT",
  "occur_at": 1700000000,
  "operator": "admin",
  "project": {
    "id": 1,
    "name": "my-app",
    "public": false
  },
  "repository": {
    "name": "my-app--api",
    "namespace": "my-app",
    "full_name": "my-app/my-app--api",
    "artifact_count": 42
  },
  "artifact": {
    "id": 12345,
    "type": "IMAGE",
    "media_type": "application/vnd.docker.distribution.manifest.v2+json",
    "digest": "sha256:abc123def456...",
    "size": 52428800,
    "tags": ["v1.2.3", "latest"],
    "created": "2024-01-01T00:00:00Z",
    "labels": [],
    "scan_overview": {
      "scan_completed_at": "2024-01-01T00:01:00Z",
      "severity": "high",
      "complete_percent": 100,
      "summary": {
        "critical": 2,
        "high": 5,
        "medium": 10,
        "low": 20,
        "unknown": 3
      }
    }
  }
}
```

## 各事件类型 Payload 差异

### PUSH_ARTIFACT
```json
{
  "type": "PUSH_ARTIFACT",
  "operator": "robot$my-app$ci",
  "artifact": { "digest": "...", "tags": ["v1.2.3"] }
}
```

### SCANNING_COMPLETED
```json
{
  "type": "SCANNING_COMPLETED",
  "operator": "system",
  "artifact": {
    "digest": "sha256:...",
    "scan_overview": {
      "severity": "high",
      "summary": { "critical": 1, "high": 3 }
    }
  }
}
```

### REPLICATION
```json
{
  "type": "REPLICATION",
  "operator": "system",
  "payload": {
    "policy_id": 3,
    "policy_name": "backup-to-dr",
    "execution_id": 15,
    "status": "success",
    "resources_total": 10,
    "resources_failed": 0
  }
}
```

## CI/CD 集成示例

### 方式1：通用 HTTP Webhook（推荐）

配置 Webhook 指向 CI 系统：
```
https://ci.mycompany.com/webhooks/harbor?token=xxxxx
```

### 方式2：企业微信/钉钉通知

```python
# Webhook 转发服务示例
def handle_webhook(payload):
    event = payload['type']
    artifact = payload.get('artifact', {})

    if event == 'SCANNING_COMPLETED':
        severity = artifact['scan_overview']['summary']
        msg = f"镜像扫描完成: {payload['repository']['full_name']}"
        if severity['critical'] > 0:
            send_alert(f"🔴 严重漏洞: {severity['critical']} 个\n{msg}")
        elif severity['high'] > 0:
            send_alert(f"🟠 高危漏洞: {severity['high']} 个\n{msg}")

    elif event == 'PUSH_ARTIFACT':
        tags = artifact.get('tags', [])
        notify(f"✅ 新镜像推送: {payload['repository']['full_name']}:{tags[-1]}")

    elif event == 'REPLICATION':
        status = payload['payload']['status']
        notify(f"🔄 复制{'成功' if status=='success' else '失败'}: {payload['payload']['policy_name']}")
```

### 方式3：Argo CD 镜像更新触发

```bash
# Argo CD Image Updater 配置
# /etc/argocd-image-updater.conf
argocd-image-updater:
  log-level: info
  registries:
    - name: Harbor
      api_url: https://harbor.mycompany.com/
      credentials: pullsecret:harbor/harbor-secret
      skip: false
```

Argo CD Image Updater 可以监听 Harbor Webhook `PUSH_ARTIFACT` 事件，自动更新 Deployment 镜像版本。

## Webhook 可靠性配置

```json
{
  "targets": [
    {
      "type": "http",
      "address": "https://your-webhook-endpoint.com/hook",
      "skip_cert_verify": false,
      "auth_header": "Bearer your-token-here",
      "retry_times": 3,
      "retry_duration": "5s",
      "timeout": 30
    }
  ],
  "event_types": ["PUSH_ARTIFACT", "SCANNING_COMPLETED", "REPLICATION"]
}
```

> 💡 建议在接收端做幂等处理（相同的 event 重复发送时不重复操作），因为 Harbor 在未收到 200 响应时会重试。
