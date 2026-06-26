# 通用排错指南

## 快速分类流程
```bash
openclaw status              # 1. 快速概览
openclaw status --all        # 2. 完整诊断(可安全分享)
openclaw status --deep       # 3. 含提供商探测
openclaw gateway status      # 4. 服务状态+最后错误
openclaw logs --follow       # 5. 实时日志(最佳信号)
openclaw doctor              # 6. 自动诊断
openclaw doctor --fix        # 7. 自动修复
```

## 配置无效导致无法启动
```bash
openclaw doctor              # 报告每个无效条目
openclaw doctor --fix        # 自动修复+重写配置
# 注意: logs/health/status/gateway status 即使配置无效也能运行
```

## "All models failed"
1. 检查凭证: `openclaw models status`
2. 确认模型路由: `agents.defaults.model.primary` + fallbacks
3. 查看日志: `openclaw logs --follow`
4. 聊天内: `/model status`

## No API key found for provider
认证是每个智能体独立的，新智能体不继承主智能体密钥。
```bash
openclaw models auth setup-token --provider anthropic  # 粘贴token
openclaw models status                                  # 验证
```

## OAuth token refresh failed
切换到 setup-token (更可靠):
```bash
openclaw models auth setup-token --provider anthropic
openclaw models status
```

## "Gateway start blocked: set gateway.mode=local"
```bash
openclaw config set gateway.mode local    # 本地模式
# 或
openclaw configure                         # 交互式设置
```

## 服务已安装但没运行
```bash
openclaw gateway status     # 查看PID/退出状态
openclaw doctor             # 审计服务配置
openclaw logs --follow      # 查看错误原因
```

## 端口被占用 (Address in use)
```bash
openclaw gateway status                    # 显示监听器
lsof -nP -iTCP:18789 -sTCP:LISTEN        # 查找占用进程
kill -TERM <PID>                           # 优雅停止
```

## 服务运行但端口未监听
- 确认 `gateway.mode` 为 `local`
- 非loopback绑定需要 `gateway.auth.token`
- `openclaw gateway status` 查看配置不匹配
- `openclaw gateway install --force` 修复服务配置

## 消息未触发
1. 发送者在白名单? `openclaw status` 查看 AllowFrom
2. 群聊需要提及? 检查 mentionPatterns
3. 查看日志: `openclaw logs --follow | grep "blocked\|skip\|unauthorized"`

## WhatsApp 断开连接
```bash
openclaw status --deep                     # 检查连接状态
openclaw gateway restart                   # 通常自动重连
# 如果已登出:
openclaw channels logout
openclaw channels login --verbose          # 重新扫描二维码
```

## 智能体超时
默认30分钟。调整:
```json5
{ reply: { timeoutSeconds: 3600 } }  // 1小时
```

## "Agent was aborted"
用户发送了stop/abort/esc，或超时。发送新消息即可继续。

## "Model is not allowed"
模型不在白名单中:
- 添加到 `agents.defaults.models`
- 或删除 `agents.defaults.models` 清除白名单
- 或从 `/model list` 选择

## 会话未恢复
1. 检查会话文件: `ls ~/.openclaw/agents/<agentId>/sessions/`
2. 检查重置窗口是否太短
3. 是否有人发送了 `/new` `/reset`

## 高内存使用
```json5
{ session: { historyLimit: 100 } }  // 限制消息数
```
或定期重启网关。

## macOS: Gateway卡在Starting
```bash
openclaw gateway stop                      # 先停服务
lsof -nP -iTCP:18789 -sTCP:LISTEN        # 检查端口
kill -TERM <PID>                           # 杀占用进程
```

## macOS: 权限提示导致崩溃
```bash
tccutil reset All bot.molt.mac.debug
```

## Linux: 浏览器无法启动
安装 Google Chrome 替代 Snap Chromium:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```
配置: `browser.executablePath: "/usr/bin/google-chrome-stable"`

## Discord 不回复
1. `channels.discord.groupPolicy` 默认 allowlist，需添加 guild
2. `channels.discord.guilds.<guildId>.channels` 用数字频道ID
3. `requireMention` 放在 guilds 下面
4. 确保 Message Content Intent 已开启

## Telegram 分块流式不工作
1. `agents.defaults.blockStreamingDefault` 设为 `"on"`
2. `channels.telegram.streamMode` 设为 `"off"` (禁用草稿流式)
3. 调低 minChars/coalesce 阈值

## 沙箱中 Skill 缺少 API 密钥
沙箱不继承主机环境变量:
```json5
{ agents: { defaults: { sandbox: { docker: { env: { MY_KEY: "..." } } } } } }
```
然后: `openclaw sandbox recreate --all`

## 核选项: 重置所有
```bash
openclaw gateway stop
trash ~/.openclaw
openclaw channels login      # 重新配对
openclaw gateway restart
```
⚠️ 丢失所有会话，需重新配对渠道

## 获取帮助
1. 查日志: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
2. 搜 GitHub issues
3. 提交 issue 时包含: 版本、日志、重现步骤、配置(隐藏密钥)
