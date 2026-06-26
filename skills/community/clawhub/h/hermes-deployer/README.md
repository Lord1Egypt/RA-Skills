# hermes-deployer

在 Linux 服务器上安装、配置、部署和运维 [Hermes Agent](https://github.com/NousResearch/hermes-agent)（Nous Research 出品的自我改进 AI Agent）的 Skill。

## 适用场景

- 从零在 Linux 服务器上部署 Hermes Agent
- 配置 LLM Provider（OpenAI / Anthropic / 智谱 / 腾讯云 LKEAP / 自定义接口）
- 接入消息平台（微信 / 企业微信 / Telegram / Discord）
- systemd 服务化部署，开机自启、自动恢复
- 日常运维、升级、排障

## 快速使用

安装到 WorkBuddy / CodeBuddy 后，直接对 AI 说：

- "帮我在服务器上装个 hermes"
- "hermes gateway 挂了，帮我排查"
- "帮我给 hermes 配置微信接入"
- "hermes 怎么切换模型"

AI 会自动加载本 Skill 并按照标准流程执行。

## 包含内容

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 完整的部署指南 + 配置参考 + 排障手册 |

## 覆盖知识

- ✅ 5 阶段部署流程（环境准备 → LLM 配置 → 平台接入 → 测试 → 服务化）
- ✅ Provider 配置（含 custom provider 正确写法和常见错误）
- ✅ 微信 / 企微 / Telegram 接入模板
- ✅ systemd service 最佳实践
- ✅ 踩坑经验（残留进程、端口冲突、Requires vs Wants、PID 文件等）

## 安装方式

### WorkBuddy / CodeBuddy

下载 ZIP 后通过"导入 Skills"安装。

### 手动安装

```bash
# 用户级（所有项目可用）
cp -r hermes-deployer ~/.workbuddy/skills/

# 项目级
cp -r hermes-deployer .workbuddy/skills/
```

## License

MIT
