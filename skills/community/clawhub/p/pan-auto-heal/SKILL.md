---
name: auto-heal
description: "检测-修复-回滚" 自动守护框架，适用于任何服务（HTTP、进程、端口、容器等）。当服务异常时自动修复或回滚，防止级联故障。触发场景：服务频繁崩溃、变更后需要自动化保障、需要故障自愈能力。
---

# Auto-Heal 通用守护框架

## 核心机制

```
检测 → 修复 → 回滚 → 告警
```

**检测**：探活测试（HTTP/端口/进程/功能）
**修复**：重启/重试/切换
**回滚**：恢复到上一稳定状态
**告警**：记录并通知

## 快速开始

### 1. 定义要守护的服务

编辑 `services.json`：

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
      "timeout": 5
    },
    {
      "name": "web-api",
      "check": {
        "type": "http",
        "url": "https://api.example.com/health",
        "expected": "200"
      },
      "fix": "systemctl restart api && sleep 3",
      "rollback": "cp /etc/api/backup.json /etc/api/config.json && systemctl restart api",
      "backup_dir": "/etc/api/backups"
    }
  ]
}
```

### 2. 运行守护

```bash
./guard.sh services.json
```

### 3. 添加到 cron（每5分钟检查）

```bash
*/5 * * * * /path/to/guard.sh /path/to/services.json >> /var/log/guard.log 2>&1
```

## 检查类型

| 类型 | 配置 | 说明 |
|------|------|------|
| port | `{"type": "port", "target": 8080}` | 端口是否监听 |
| process | `{"type": "process", "name": "nginx"}` | 进程是否存在 |
| http | `{"type": "http", "url": "...", "expected": "200"}` | HTTP 状态码 |
| cmd | `{"type": "cmd", "command": "pgrep -x myapp"}` | 自定义命令（返回0=正常） |

## 框架流程

```
1. 解析配置文件
2. 遍历每个服务
3. 执行检测
   ├─ 正常 → 记录，跳过
   └─ 异常 → 进入修复流程
4. 修复
   ├─ 执行修复命令
   ├─ 重新检测
   │   ├─ 正常 → 恢复，记录"自愈成功"
   │   └─ 仍异常 → 回滚
5. 回滚
   ├─ 尝试回滚
   ├─ 重新检测
   │   ├─ 正常 → 恢复，记录"回滚成功"
   │   └─ 仍异常 → 告警（需人工介入）
```

## 配置字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | 服务名称（唯一标识） |
| check | ✅ | 检测配置 |
| fix | ✅ | 修复命令 |
| rollback | ❌ | 回滚命令（不填则跳过） |
| timeout | ❌ | 检测超时（秒），默认5 |
| backup_dir | ❌ | 自动备份目录（保留最近10份） |
| enabled | ❌ | true/false，默认true |

## 示例配置

详见 `references/examples.md`：
- Nginx 反向代理
- Docker 容器
- AI API 服务
- 数据库主从切换

## 日志格式

```
[2026-03-27 10:00:00] [nginx] 检测正常
[2026-03-27 10:05:00] [api] 检测失败 → 执行修复...
[2026-03-27 10:05:03] [api] 修复成功，自愈用时3秒
[2026-03-27 10:10:00] [db] 检测失败 → 执行修复... → 修复失败 → 回滚...
[2026-03-27 10:10:06] [db] 回滚成功
[2026-03-27 10:15:00] [cache] 检测失败 → 修复失败 → 回滚失败 → 告警：请人工介入
```
