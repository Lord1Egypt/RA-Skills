# 常见问题解答 (FAQ)

## 安装相关

### Q: OpenClaw 如何安装？
A: 运行以下命令：
```bash
npm install -g openclaw
```

### Q: 安装失败怎么办？
A: 检查 Node.js 版本（需要 >= 18.0.0）：
```bash
node --version
```
如版本过低，请升级 Node.js。

### Q: 如何更新 OpenClaw？
A: 运行：
```bash
npm update -g openclaw
```

---

## Gateway 相关

### Q: Gateway 无法启动？
A: 检查日志：
```bash
openclaw gateway status
```
常见原因：
- 端口被占用
- 配置文件错误
- 缺少依赖

### Q: 如何重启 Gateway？
A: 运行：
```bash
openclaw gateway restart
```

### Q: Gateway 日志在哪里？
A: 查看 Gateway 状态时会显示日志路径。

---

## Skills 相关

### Q: 如何安装 Skill？
A: 运行：
```bash
clawhub install <skill-name>
```

### Q: 如何查看已安装的 Skills？
A: 运行：
```bash
clawhub list
```

### Q: 如何更新 Skills？
A: 运行：
```bash
clawhub update --all
```

### Q: Skill 安装失败？
A: 检查：
1. 网络连接
2. Skill 名称是否正确
3. 是否有足够权限

---

## 渠道相关

### Q: Telegram Bot 没有响应？
A: 检查：
1. Gateway 是否运行
2. Token 是否正确
3. Bot 是否被禁用

### Q: WhatsApp 连接断开？
A: 重新扫描配置二维码：
```bash
openclaw configure --section whatsapp
```

### Q: Discord Bot 无法发送消息？
A: 检查 Bot 权限，确保有 `Send Messages` 权限。

---

## 使用相关

### Q: 如何查看帮助？
A: 运行：
```bash
openclaw help
```

### Q: 如何查看状态？
A: 运行：
```bash
openclaw status
```

### Q: 工作目录在哪里？
A: 默认在 `~/.openclaw/workspace`

### Q: 如何备份配置？
A: 备份以下目录：
- `~/.openclaw/workspace`
- Gateway 配置文件

---

## 安全相关

### Q: 如何保护 API Token？
A: 
- 不要分享到公开场合
- 使用环境变量存储
- 定期更换 Token

### Q: Gateway 可以暴露到公网吗？
A: 不建议。如需远程访问，请使用：
- SSH 隧道
- Tailscale 等内网穿透
- 反向代理 + 认证

### Q: 如何检查安全配置？
A: 使用安全审计工具：
```bash
# 待开发的安全审计 skill
openclaw security-audit
```

---

## 其他问题

### Q: 在哪里获取帮助？
A: 
- 官方文档：https://docs.openclaw.ai
- Discord 社区：https://discord.com/invite/clawd
- GitHub Issues: https://github.com/openclaw/openclaw/issues

### Q: 如何反馈问题？
A: 在 GitHub 提交 Issue，描述清楚：
1. 问题现象
2. 复现步骤
3. 环境信息（系统、Node.js 版本等）
4. 日志输出

---

**没有找到答案？** 欢迎在 Discord 社区提问或提交 Issue。
