# Source Audit

## 这个 skill 的发布原则

这不是完整运行现场快照，而是一个**公开可迁移层**：
- 可复用 workspace 模板
- continuity 规则
- 脱敏示例配置
- 正式运行时代码补丁
- 安装 / 部署 / 验证 / 回滚文档

## 明确保留的内容

- `LICENSE`
- `SKILL.md`
- `agents/openai.yaml`
- `scripts/install_continuity_pack.py`
- `scripts/bootstrap_workspace.py`
- `scripts/apply_runtime_patch.py`
- `assets/workspace/`
- `assets/config/openclaw.example.json`
- `assets/patch/thread-continuity.patch`
- `references/` 下的公开说明文档

## 明确排除的内容

以下内容不应进入发布包：
- 真实 `memory / plans / status / handoff` 实例
- 真实 `openclaw.json`
- token / API key / OAuth / channel secret
- `.bak_*`
- `.tmp/`
- 验收脚本
- 临时故障注入代码
- deploy-backups
- 写死的个人路径、用户名、会话名

## 发布前清洁检查

发布前至少再核一遍：
- `assets/` 里没有日志、密钥、个人数据
- `scripts/` 里没有临时验收或故障注入脚本
- `references/` 里没有本机路径和一次性现场说明
- patch 只包含正式运行时代码，不含测试辅助物
- source 目录里没有 `__pycache__`、`.pyc` 或其他本地测试残留

## 2026-03-29 复验结论

本轮针对 source 目录、ClawHub 安装后的隔离副本以及 `.skill` 打包产物做了额外检索，重点检查：
- 本机路径
- 用户名 / 控制台标签
- QQ / 聊天 ID
- token / API key / OAuth 凭据形态
- 发布后安装落盘的 registry 元数据

结论：
- 未发现用户真实路径、用户名、QQ、token、API key、channel secret、真实 memory/plan/status/handoff 数据
- 安装后的 `.clawhub/origin.json` 仅包含 registry、slug、已装版本与安装时间，不含发布者用户名或 token
- 检出的数字仅是模板文档中的示例时间戳，不是个人身份信息
