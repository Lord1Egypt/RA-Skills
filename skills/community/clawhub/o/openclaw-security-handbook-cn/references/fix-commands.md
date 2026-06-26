# OpenClaw 安全修复命令参考

## 可安全自动化的修复

### 1. 文件权限加固

```bash
# 关键配置文件权限
chmod 600 ~/.openclaw/openclaw.json
chmod 600 ~/.openclaw/.env
chmod 700 ~/.openclaw
chmod 700 ~/.openclaw/credentials
chmod 700 ~/.openclaw/sessions

# 修复附件文件权限（644 → 600）
find ~/.openclaw/ -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.pdf" -o -name "*.doc*" \) -perm +044 -exec chmod 600 {} \;

# 验证
ls -la ~/.openclaw/
stat -c "%a %n" ~/.openclaw/openclaw.json ~/.openclaw/.env ~/.openclaw/credentials/
```

### 2. 生成强网关令牌

```bash
# 生成 32 字节随机令牌（256 位熵）
openssl rand -hex 32

# 写入 .env（不要明文写入配置文件！）
echo "OPENCLAW_GATEWAY_TOKEN=<新令牌>" >> ~/.openclaw/.env
chmod 600 ~/.openclaw/.env
```

### 3. 禁用遥测

```bash
# 写入 .env
echo "DISABLE_TELEMETRY=1" >> ~/.openclaw/.env

# 或在启动时设置
export DISABLE_TELEMETRY=1
```

### 4. 启动网关（安全绑定）

```bash
# 绑定到本地回环（不暴露到网络）
openclaw gateway --bind loopback

# 或通过环境变量
export OPENCLAW_GATEWAY_BIND=loopback
```

### 5. openclaw 内置修复

```bash
# 自动修复安全默认值和文件权限
openclaw security audit --fix
```

---

## 需人工确认的修复

### 6. 认证模式配置

```bash
# 查看当前配置
cat ~/.openclaw/openclaw.json | grep -A10 '"auth"'

# 手动编辑配置文件，设置：
# "mode": "token"  (不要用 "none")
# "secretRef": "env:OPENCLAW_GATEWAY_TOKEN"  (不要明文写入令牌)
```

### 7. 通道 allowFrom 白名单

```bash
# 检查通道配置
cat ~/.openclaw/openclaw.json | grep -A20 '"channels"'

# 每个通道添加 allowFrom 白名单（使用数字 ID）：
# "allowFrom": ["你的Telegram用户ID"]
# "dmPolicy": "pairing"
```

### 8. exec.mode 设为 ask

```bash
# 在 openclaw.json 中设置
# "agents": { "defaults": { "exec": { "mode": "ask" } } }

# 不要设为 "allow"！
```

### 9. groupPolicy 收紧

```bash
# 在 openclaw.json 中设置
# "channels": { "feishu": { "accounts": { "main": { "groupPolicy": "allowlist" } } } }

# 不要使用 "open"！
```

### 10. Skill 危险模式清理

```bash
# 识别可疑 Skill
find ~/.openclaw/skills/ -name "*.js" -o -name "*.ts" | xargs grep -l "eval\|spawn\|exec\|fetch" 2>/dev/null

# 卸载可疑 Skill（需确认）
# openclaw skill uninstall <skill-name>

# 锁定 Skill 版本（在 Skill 目录的 package.json 中设置 "version"）
```

### 11. Docker 沙箱网络安全

```bash
# 创建无外网访问的 Docker 网络
docker network create --internal openclaw-sandbox-net

# 检查当前沙箱容器网络
docker inspect openclaw-sandbox | grep NetworkMode

# 如使用 bridge，添加 iptables 规则限制出站（需 root）
# iptables -I DOCKER-USER -i docker0 -o eth0 -j DROP
```

### 12. 锁定配置文件（chattr）

```bash
# Linux: 防止配置文件被篡改（需 root）
sudo chattr +i ~/.openclaw/openclaw.json

# 解锁（如需修改）
sudo chattr -i ~/.openclaw/openclaw.json

# macOS
chflags uchg ~/.openclaw/openclaw.json
chflags nouchg ~/.openclaw/openclaw.json
```

### 13. 会话日志清理

```bash
# 清理 30 天前的会话
find ~/.openclaw/sessions/ -mtime +30 -name "*.jsonl" -delete

# 清理日志中的明文密钥（需确认范围）
grep -rEl "sk-|AKIA-|password|secret|token" ~/.openclaw/logs/ 2>/dev/null

# 备份后再清理
cp -r ~/.openclaw/sessions/ /tmp/sessions-backup-$(date +%Y%m%d)/
```

### 14. 重建工作区（如确认被入侵）

```bash
# 备份后再清除
cp -r ~/.openclaw/workspace/ /tmp/workspace-backup-$(date +%Y%m%d)/

# 完全重建
rm -rf ~/.openclaw/workspace/
mkdir ~/.openclaw/workspace/
```

### 15. API Key 轮换

```bash
# 撤销并重新生成所有曾提供给 OpenClaw 的 API Key
# 在各平台手动操作：
# - Anthropic Console: https://console.anthropic.com/settings/keys
# - OpenAI: https://platform.openai.com/api-keys
# - 各消息平台 Bot Token

# 生成新令牌后更新 ~/.openclaw/.env
```

### 16. 调度安全审计

```bash
# 每天 09:00 运行
openclaw cron add \
  --name "openclaw-security:daily" \
  --command "openclaw security audit --json >> ~/.openclaw/logs/security-audit-$(date +\%Y\%m\%d).json" \
  --cron "0 9 * * *"

# 查看已调度的任务
openclaw cron list
```

---

## 应急响应（确认被入侵后）

```bash
# 1. 停止网关
openclaw gateway stop

# 2. 撤销所有 API Key
# （在各平台手动撤销）

# 3. 轮换网关令牌
openssl rand -hex 32 > /tmp/new-token.txt

# 4. 备份日志（不要删除！）
cp -r ~/.openclaw/sessions/ /tmp/incident-sessions-$(date +%Y%m%d)/
cp ~/.openclaw/openclaw.json /tmp/incident-config-$(date +%Y%m%d)/

# 5. 清除工作区
rm -rf ~/.openclaw/workspace/

# 6. 检查持久化后门
crontab -l
launchctl list | grep openclaw  # macOS
systemctl --user list-units | grep openclaw  # Linux

# 7. 如使用独立 VM，建议直接销毁重建
```
