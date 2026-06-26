---
name: openclaw-uninstaller
description: "OpenClaw 卸载指南，帮你体面告别这只昂贵的龙虾"
---

# OpenClaw 卸载指南

如果你发现养龙虾的成本远超预期，或者 API 账单让你心惊肉跳，是时候和这只"龙虾"体面告别了。

## 快速卸载（推荐）

### 一键卸载

```bash
openclaw uninstall --all --yes --non-interactive
```

### 或使用 npx

```bash
npx -y openclaw uninstall --all --yes --non-interactive
```

## 手动卸载（分步执行）

### 第一步：停止网关服务

```bash
openclaw gateway stop
```

### 第二步：卸载网关

```bash
openclaw gateway uninstall
```

### 第三步：删除配置文件

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

### 第四步：删除 workspace（可选但建议）

```bash
rm -rf ~/.openclaw/workspace
```

### 第五步：卸载 CLI

根据安装方式选择：

```bash
# npm 安装的
npm rm -g openclaw

# pnpm 安装的
pnpm remove -g openclaw

# bun 安装的
bun remove -g openclaw
```

### macOS 桌面版

```bash
rm -rf /Applications/OpenClaw.app
```

## 系统服务清理

### macOS

```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Linux

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

## 注意事项

- **多 profile 用户**: 每个 profile 都有独立的状态目录 `~/.openclaw-<profile>`，需要逐一删除
- **远程模式**: 需要登录到网关主机执行清理操作
- **源码安装**: 必须先卸载网关服务，再删除仓库目录

## 卸载后的人生建议

✅ 恭喜你省下了一笔可观的 API 费用
✅ 你的电脑终于可以安静地休息了
✅ 不用再担心半夜收到天价账单
✅ 可以等下一代更稳定、更便宜的产品

记住：第一个吃螃蟹的人值得尊敬，但第一百个吃螃蟹的人，通常吃得更好，也更便宜。

## 参考文档与教程

### 官方资源
- 官方卸载指南: https://docs.openclaw.ai/install/uninstall
- GitHub Issues: https://github.com/openclaw/openclaw/issues

### 中文卸载教程
- 知乎搜索 "龙虾卸载指南"
- CSDN搜索 OpenClaw 完全卸载教程
- B站视频搜索"OpenClaw 卸载"
- 小红书搜索"OpenClaw 删除"

### 国外资源
- Reddit r/ollama: "How do I remove OpenClaw?"
- Stack Overflow OpenClaw 卸载问题
- YouTube 搜索"OpenClaw uninstall"

### 为什么这么多人要卸载？
- API 账单爆炸（月费破千美元）
- 安全风险（全球 10 万+实例暴露在公网）
- 配置复杂（Node.js 版本玄学）
- AI 脑过载（同时用 3 个以上 AI 工具生产力反降）

## 反悔了怎么办？

如果卸载后发现还是离不开龙虾，或者看到别人炫耀又心动了，请使用 **openclaw-installer** skill 重新开始这段昂贵的旅程。
