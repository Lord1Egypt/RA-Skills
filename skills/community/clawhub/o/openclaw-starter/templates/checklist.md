# OpenClaw 新手检查清单

## 安装前检查

- [ ] Node.js >= 18.0.0 已安装
- [ ] npm >= 8.0.0 已安装
- [ ] Python 3.x 已安装
- [ ] 网络连接正常

## 安装后检查

- [ ] OpenClaw CLI 已安装 (`openclaw --version`)
- [ ] Gateway 可启动 (`openclaw gateway start`)
- [ ] Workspace 目录存在 (`~/.openclaw/workspace`)
- [ ] 关键文件存在 (SOUL.md, AGENTS.md, TOOLS.md)

## 配置检查

- [ ] Gateway 配置安全（未暴露到公网）
- [ ] API Token 已妥善保管（未硬编码）
- [ ] 至少配置一个渠道（Telegram/WhatsApp/Discord/WebChat）

## Skills 安装

- [ ] 已安装基础 Skills（至少 3 个）
- [ ] Skills 可正常使用
- [ ] 了解如何更新 Skills (`clawhub update --all`)

## 渠道配置

### Telegram
- [ ] 已创建 Bot（通过 @BotFather）
- [ ] Token 已配置
- [ ] Bot 可响应消息

### WhatsApp
- [ ] 已扫描二维码
- [ ] 连接状态正常
- [ ] 可发送/接收消息

### Discord
- [ ] 已创建 Discord 应用
- [ ] Bot 已邀请到服务器
- [ ] Token 和 Channel ID 已配置

## 安全加固

- [ ] Gateway 未暴露到公网（bind: 127.0.0.1）
- [ ] 使用防火墙限制访问
- [ ] 定期更新 OpenClaw 和 Skills
- [ ] 备份重要配置文件

## 首次使用

- [ ] 发送第一条消息
- [ ] 测试一个 Skill（如天气查询）
- [ ] 查看帮助文档
- [ ] 加入 Discord 社区

---

**完成所有检查项后，你已经成功配置好 OpenClaw！** 🎉
