# OpenClaw Continuity Pack

这是一个可复用的 OpenClaw continuity / rollover 发布包，不是某台机器的完整运行现场快照。

它解决的问题是：
- 前台尽量保持“同一个聊天 thread”的体验
- 后台在上下文压力升高时**静默刷新 durable state**，并在需要时切到 successor session
- successor 中保留 hidden handoff，但不把 handoff 泄露到用户可见历史
- 普通聊天页**不再渲染 continuity/context 两类提示**，避免用户侧看到显式“快满了/准备压缩”的提示条
- 当 token 缺失、successor 创建失败、handoff 注入失败时，诚实降级，不伪装成“已经无缝续接成功”

它不是：
- 真正的无限上下文
- 你的完整 `~/.openclaw` 目录快照
- 任何人的现网配置、密钥、日志、渠道设置或个人记忆数据包

## 这包包含两层内容

1. 规则/模板层  
适合不想改源码的人。它提供一套可直接复用的 continuity workspace 模板：
- `AGENTS.md`
- `SESSION_CONTINUITY.md`
- `plans/status/handoff` 模板
- `memory/temp` 说明文件
- 一份脱敏后的 `openclaw.example.json`

2. 源码补丁层  
适合愿意自己编译部署的人。它提供：
- 仅包含正式运行时代码与 source-side 对齐测试的 `thread-continuity.patch`
- 正式运行时代码文件清单
- 构建、部署、回滚、验证说明

## 已实现的能力

- 热层 `memory / plans / status / handoff` 连续性闭环
- successor rollover
- hidden handoff
- 普通聊天页无 continuity/context 提示的 same-thread UX
- 80% / 85% / 88% / 90% 上下文压力策略：静默 durability refresh / compact_prepare / 预测切换 / rollover_required
- 诚实降级

## 未承诺的能力

- 不承诺真正无限上下文
- 不承诺所有 OpenClaw 版本都能零改动套用
- 不承诺所有 provider / gateway / UI 打包方式都完全一致

## 使用者需要自己承担的事情

- 自己配置模型、API、网关 token、渠道和 secrets
- 自己先做备份
- 自己优先在测试环境验证
- 如果要部署源码补丁，自己执行构建与上线/回滚

## 目录说明

- `assets/workspace/`：可复用热层规则与模板
- `assets/config/openclaw.example.json`：脱敏示例配置
- `assets/patch/thread-continuity.patch`：正式运行时代码补丁
- `references/files-to-replace.md`：正式运行时代码清单与排除清单
- `references/deploy-notes.md`：补丁构建与部署说明
- `references/install.md`：安装方法
- `references/rollback.md`：回滚方法
- `references/verify.md`：最小验证步骤
- `references/release-notes.md`：发布说明
- `references/changelog.md`：变更记录

## 适用范围

建议用于：
- 想在 OpenClaw 上实现“同一 thread 体验 + 后台自动续接”的用户
- 已经有现成 continuity 热层基础，希望补上 runtime / UI continuity 的用户
- 愿意自己编译 OpenClaw 并部署到测试环境的用户

## 不包含的内容

这个包**刻意不包含**：
- 真实 `memory/*.md`
- 真实 `plans/ status/ handoff/` 实例文件
- 真实 `openclaw.json`
- 任意 token / API key / OAuth / channel secret
- `.bak_*`
- `.tmp/`
- 验收脚本
- 临时故障注入代码
- 部署备份目录

先读 [install.md](./install.md) 再决定走“仅规则包”还是“规则包 + 源码补丁”。
