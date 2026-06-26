# Auto-Heal 配置示例

## 示例1：Nginx Web 服务

```json
{
  "services": [
    {
      "name": "nginx",
      "check": {
        "type": "port",
        "target": 80
      },
      "fix": "systemctl restart nginx",
      "rollback": "systemctl restart nginx",
      "timeout": 3
    }
  ]
}
```

## 示例2：HTTP API 健康检查

```json
{
  "services": [
    {
      "name": "myapi",
      "check": {
        "type": "http",
        "url": "https://api.example.com/health",
        "expected": "200"
      },
      "fix": "systemctl restart myapi && sleep 3",
      "rollback": "systemctl restart myapi",
      "timeout": 5
    }
  ]
}
```

## 示例3：Docker 容器

```json
{
  "services": [
    {
      "name": "redis-container",
      "check": {
        "type": "cmd",
        "command": "docker ps | grep -q redis"
      },
      "fix": "docker restart redis",
      "rollback": "docker start redis",
      "timeout": 5
    },
    {
      "name": "postgres-container",
      "check": {
        "type": "cmd",
        "command": "docker exec postgres pg_isready -U postgres"
      },
      "fix": "docker restart postgres",
      "rollback": "docker start postgres",
      "timeout": 5
    }
  ]
}
```

## 示例4：多服务综合监控

```json
{
  "services": [
    {
      "name": "nginx",
      "enabled": true,
      "check": { "type": "port", "target": 80 },
      "fix": "systemctl restart nginx",
      "timeout": 3
    },
    {
      "name": "mysql",
      "enabled": true,
      "check": {
        "type": "cmd",
        "command": "mysqladmin ping -u root -psecret 2>/dev/null"
      },
      "fix": "systemctl restart mysql",
      "timeout": 5
    },
    {
      "name": "redis",
      "enabled": true,
      "check": {
        "type": "cmd",
        "command": "redis-cli ping | grep -q PONG"
      },
      "fix": "systemctl restart redis",
      "timeout": 3
    },
    {
      "name": "web-api",
      "enabled": false,
      "check": {
        "type": "http",
        "url": "http://localhost:3000/health",
        "expected": "200"
      },
      "fix": "pm2 restart api",
      "timeout": 5
    }
  ]
}
```

## 示例5：带自动备份的配置变更

```json
{
  "services": [
    {
      "name": "app-config",
      "check": {
        "type": "http",
        "url": "http://localhost:8080/api/status",
        "expected": "200"
      },
      "fix": "cp /opt/app/config.json.new /opt/app/config.json && systemctl restart app",
      "rollback": "ls -1t /opt/app/backups/config_*.json | head -1 | xargs -I {} cp {} /opt/app/config.json && systemctl restart app",
      "backup_dir": "/opt/app/backups",
      "timeout": 5
    }
  ]
}
```

## 示例6：GitHub Actions Runner

```json
{
  "services": [
    {
      "name": "actions-runner",
      "check": {
        "type": "cmd",
        "command": "curl -s http://localhost:8080 > /dev/null"
      },
      "fix": "sudo systemctl restart actions-runner",
      "rollback": "sudo systemctl restart actions-runner",
      "timeout": 5
    }
  ]
}
```

## 高级用法

### 组合检测（端口 + HTTP）

如果需要双重验证（端口通且服务响应正常），可以写一个组合命令：

```json
{
  "name": "webapp",
  "check": {
    "type": "cmd",
    "command": "ss -tlnp | grep -q ':443 ' && curl -sf https://example.com/health > /dev/null"
  },
  "fix": "systemctl restart webapp",
  "timeout": 10
}
```

### 带通知的告警

在修复/回滚命令中调用通知脚本：

```json
{
  "name": "critical-api",
  "check": {
    "type": "http",
    "url": "https://api.example.com/health",
    "expected": "200"
  },
  "fix": "systemctl restart api && /opt/scripts/notify.sh 'API restarted'",
  "rollback": "/opt/scripts/rollback.sh && /opt/scripts/notify.sh 'API rolled back, manual check needed'",
  "timeout": 5
}
```
