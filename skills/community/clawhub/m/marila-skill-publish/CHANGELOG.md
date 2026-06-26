# Changelog

## [1.0.8] - 2026-03-11

### 新增
- 补充 ClawHub CLI 发布兼容坑：`SKILL.md required` 与 `acceptLicenseTerms: invalid value` 的联合排查逻辑
- 补充手工调用 `https://clawhub.ai/api/v1/skills` 的 API 发布兜底方案
- 补充 `metadata mismatch` 审核反馈的修复流程
- 明确 GitHub Release 成功但 ClawHub CLI 失败时，不要盲重试，优先判断是否为 CLI payload bug
- 同步修正版本元数据不一致：`SKILL.md` / `package.json` 对齐到 `1.0.8`

## [1.0.7] - 2026-03-07

### 修复
- ✅ description 去掉本地目录路径表述，避免把技能用途绑死到特定机器路径
- ✅ 删除 TLS bypass 和直接读取本地凭证文件的排障建议
- ✅ 将 agent workspace 同步改为受信任环境下的显式敏感操作说明
- ✅ checklist 新增安全审查项：本地目录路径、TLS 绕过、凭证文件读取、敏感写操作标注

## [1.0.6] - 2026-03-07

### 更新
- ✅ 将 `references/clawhub-review-checklist.md` 正式纳入发布流程
- ✅ SKILL.md 和 README.md 明确要求：发布前必须先过 checklist

## [1.0.5] - 2026-03-07

### 更新
- ✅ 补充 Git / GitHub CLI 安装检查步骤
- ✅ 补充 GitHub 鉴权、Git 身份配置、remote 配置说明
- ✅ 元数据补充 `gh` 依赖，避免技能声明与实际使用不一致

## [1.0.4] - 2026-03-07

### 更新
- ✅ 优化技能 description，明确覆盖“发布技能”“发到 ClawHub”“发布这个 skill”“写完就发布”“上线这个技能”等触发表达
- ✅ package.json 和 README.md 同步更新描述文案，减少触发歧义

## [1.0.3] - 2026-03-07

### 更新
- ✅ 新增硬规则：发布 OpenClaw 技能时，ClawHub 发布必须同步创建 GitHub Release
- ✅ 版本更新流程补充为：先 push + GitHub Release，再发布到 ClawHub

## [1.0.2] - 2026-03-05

### 更新
- ✅ 发布流程新增第 5 步：发布后必须同步 SKILL.md 到 agent 工作空间

## [1.0.1] - 2026-03-05

### 更新
- ✅ 新增"发布顺序"章节：明确 4 步发布流程顺序（版本号 → CHANGELOG → GitHub Release → ClawHub）

## [1.0.0] - 2026-02-27

### 新增
- 完整的 ClawHub 技能发布流程文档
- 常见问题与解决方案汇总
- 元数据规范说明
- 版本更新流程
- 安全注意事项
- 最佳实践建议

### 来源
基于发布 `dingtalk-ai-table` 技能的实际经验总结，包括：
- 学习 ClawHub 官方规范（skill-format.md, security.md）
- 修复元数据不一致问题（requires.env, requires.bins）
- 解决 CLI 超时和认证问题
- 成功发布 v0.3.3 版本
