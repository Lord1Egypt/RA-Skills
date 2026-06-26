# OpenClaw 安全检查清单

基于 [ZAST.AI OpenClaw Security Handbook](https://github.com/zast-ai/openclaw-security) 第九章。

## 🔴 CRITICAL — 必须立即处理

### T-ACCESS-004 / T-EXEC-005 / T-PERSIST-001 / T-EXFIL-003
**恶意 Skill 检测**

```bash
# 检查最近安装的 Skill
ls -lt ~/.openclaw/skills/ | head -20

# 危险模式扫描
grep -rEn "exec\(|spawn\(|child_process|eval\(|new Function\(|process\.env.*fetch|WebSocket" ~/.openclaw/skills/*/scripts/ 2>/dev/null
grep -rEn "xmrig|coinhive|base64.*decode|atob\(" ~/.openclaw/skills/ 2>/dev/null
```

### T-IMPACT-001
**任意命令执行风险**

检查项：
- [ ] `exec.mode` 是否为 `"ask"`（不是 `"allow"`）
- [ ] `sandbox.mode` 是否启用
- [ ] 是否在主力机器上运行（应使用独立 VM）

### T-EXEC-001
**直接提示注入**

检查项：
- [ ] 通道是否配置 `allowFrom` 白名单
- [ ] `dmPolicy` 是否为 `"pairing"`
- [ ] Bot 是否在群组中（不应在）

---

## 🟡 WARN — 建议处理

### 网关绑定
```bash
# 检查绑定地址（应为 loopback）
openclaw status 2>/dev/null | grep -i bind
ss -ltnp | grep 18789
```

### 认证模式
```bash
# 检查 auth.mode（应为 token，不是 none）
grep -A5 '"auth"' ~/.openclaw/openclaw.json
```

### 令牌强度
```bash
# 检查令牌长度（应为 64 字符 hex = 256 位）
grep -E "gateway.*token|OPENCLAW_GATEWAY_TOKEN" ~/.openclaw/.env
```

### 文件权限
```bash
# 检查权限（应为 600/700）
ls -la ~/.openclaw/
stat -c "%a %n" ~/.openclaw/openclaw.json ~/.openclaw/.env ~/.openclaw/credentials/
```

### 日志泄露
```bash
# 扫描明文密钥
grep -rEn "sk-|AKIA-|password|secret|token|private.key" ~/.openclaw/sessions/ 2>/dev/null
grep -rEn "sk-|password|secret|token" ~/.openclaw/logs/ 2>/dev/null
```

### Skill 版本
```bash
# 检查是否锁定版本（无自动更新）
find ~/.openclaw/skills/ -name "package.json" -exec grep '"version"' {} \; 2>/dev/null
```

### 附件权限
```bash
find ~/.openclaw/ -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.pdf" \) -perm +044 2>/dev/null
```

### Docker Socket
```bash
# 检查是否挂载了 Docker Socket（危险）
grep -r "docker.sock" ~/.openclaw/openclaw.json 2>/dev/null
docker inspect openclaw-sandbox 2>/dev/null | grep -i socket
```

### 沙箱网络
```bash
# 检查沙箱是否为 internal 网络
docker inspect openclaw-sandbox 2>/dev/null | grep NetworkMode
```

### OAuth 令牌
```bash
# 检查活跃的 OAuth 授权
ls -la ~/.openclaw/credentials/
```

### 记忆文件
```bash
# 检查记忆是否被篡改
cat ~/.openclaw/workspace/MEMORY.md | head -30
ls -la ~/.openclaw/workspace/memory/
```

---

## ℹ️ INFO — 参考项

### 端口暴露
```bash
# 网关 + 沙盒浏览器端口
ss -ltnp | grep -E "18789|18790|9222|5900|6080"
nmap -p 18789,18790,9222,5900 127.0.0.1 2>/dev/null
```

### Debug 模式
```bash
# 检查是否开启 debug
grep -i "debug\|verbose" ~/.openclaw/openclaw.json
```

### Telemetry
```bash
# 检查是否禁用遥测
echo $DISABLE_TELEMETRY
env | grep -iE "telemetry|analytic"
```

### Node.js 版本（Windows）
```bash
# Windows 用户检查 Node.js 版本
node --version  # 应 >= v20.11.1
```

### 模型 API 用量
```bash
# 检查 API 消费上限
# 访问 Anthropic Console: https://console.anthropic.com/settings/usage
```

---

## 快速诊断命令汇总

```bash
# 一行诊断命令（复制粘贴）
echo "=== 网关绑定 ===" && ss -ltnp | grep 18789
echo "=== 认证模式 ===" && grep -A3 '"auth"' ~/.openclaw/openclaw.json | head -10
echo "=== 文件权限 ===" && ls -la ~/.openclaw/ | head -15
echo "=== 端口暴露 ===" && ss -ltnp | grep -E "18789|9222|5900"
echo "=== 日志泄露 ===" && grep -rEn "sk-|password|secret" ~/.openclaw/sessions/ 2>/dev/null | head -5
echo "=== Skill 数量 ===" && ls ~/.openclaw/skills/ | wc -l
```
