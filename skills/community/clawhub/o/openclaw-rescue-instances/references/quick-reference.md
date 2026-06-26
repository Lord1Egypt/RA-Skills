# 快速参考卡

## 创建实例

```bash
# 创建单个（端口 19001）
~/.openclaw/skills/openclaw-rescue-instances/scripts/create-rescue-instance.sh 1 19001

# 创建 3 个（端口 19001, 20001, 30001）
~/.openclaw/skills/openclaw-rescue-instances/scripts/batch-create-rescue-instances.sh 1 3 19001
```

## 删除实例

```bash
# 删除 rescue1
~/.openclaw/skills/openclaw-rescue-instances/scripts/delete-rescue-instance.sh 1

# 删除 rescue2
~/.openclaw/skills/openclaw-rescue-instances/scripts/delete-rescue-instance.sh rescue2
```

## 状态检查

```bash
# 查看所有实例
launchctl list | grep openclaw.gateway

# 健康检查
for port in 8080 19001 20000 30000 40000; do
  curl -sk https://localhost:$port/health && echo " ($port)"
done
```

## 重启实例

```bash
# 重启单个
launchctl kickstart -k gui/$UID/ai.openclaw.gateway-rescue1

# 重启所有救援实例
for name in gateway-rescue1 gateway-rescue2 gateway-rescue3 gateway-rescue4; do
  launchctl kickstart -k gui/$UID/ai.openclaw.$name
done
```

## 日志查看

```bash
# 主实例
tail -f ~/.openclaw/logs/gateway.log

# 救援 1
tail -f ~/.openclaw-rescue1/logs/gateway.log
```

## 目录位置

| 类型 | 路径 |
|------|------|
| 配置文件 | `~/.openclaw-rescueN/openclaw.json` |
| 服务文件 | `~/Library/LaunchAgents/ai.openclaw.gateway-rescueN.plist` |
| 日志文件 | `~/.openclaw-rescueN/logs/` |
| 工作目录 | `~/.openclaw-rescueN/workspace/` |

## 默认端口分配

| 实例 | 端口 | 用途 |
|------|------|------|
| 主实例 | 8080 | 生产环境 |
| rescue1 | 19001 | 救援/测试 |
| rescue2 | 20000 | 救援/测试 |
| rescue3 | 30000 | 救援/测试 |
| rescue4 | 40000 | 救援/测试 |
