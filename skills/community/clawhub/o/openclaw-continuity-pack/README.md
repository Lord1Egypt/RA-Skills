# OpenClaw Continuity Pack

这是一个可复用的 OpenClaw continuity / rollover 发布包，不是某台机器的完整运行现场。

它解决的问题是：

- 前台尽量保持同一个聊天 thread
- 后台在上下文压力升高时静默准备 continuity 元数据
- 必要时切到 successor session
- 把 hidden handoff 只留在后台 transcript，不泄露到用户可见历史
- 在失败时诚实降级，而不是假装已经无缝续接

它不是：

- 无限上下文
- 你的 `~/.openclaw` 完整快照
- 任何个人机器的密钥、日志、记忆或会话数据包

## 这包包含两层

### 1. 配置 / 规则层
适合不想改源码的人：

- `assets/workspace/AGENTS.md`
- `assets/workspace/SESSION_CONTINUITY.md`
- `plans/status/handoff` 模板
- `memory/temp` README
- 脱敏后的 `openclaw.example.json`

### 2. 源码补丁层
适合愿意自己编译部署 OpenClaw 的人：

- `assets/patch/thread-continuity.patch`
- install / deploy / verify / rollback 文档
- continuity upgrade doctor 脚本

## 已实现的能力

- memory / plans / status / handoff 热层闭环
- successor rollover
- hidden handoff
- same-thread UX
- honest degrade path
- 对 `totalTokens` 缺失场景的更稳压力回退
- 更早的 predictive rollover 触发

## 未承诺的能力

- 不保证真正无限上下文
- 不保证所有 OpenClaw 版本零改动套用
- 不保证所有 provider / gateway 结构都完全一致

## 使用者需要自己承担的事

- 自己填写模型、API、网关和密钥
- 自己先做备份
- 自己优先在测试环境验证
- Full continuity 安装时自己完成构建与部署

## 推荐阅读顺序

1. `references/overview.md`
2. `references/install.md`
3. `references/deploy-notes.md`
4. `references/verify.md`
5. `references/upgrade-maintenance.md`
6. `references/release-notes.md`
