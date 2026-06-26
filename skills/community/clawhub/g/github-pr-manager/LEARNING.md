# Skill 学习日志 - github-pr-manager

## 学习机制

每次执行 PR 管理任务时，记录：
1. 遇到的问题和解决方案
2. 用户反馈和建议
3. 可以改进的地方
4. 新场景的处理方式

定期（每月或每季度）回顾并更新 SKILL.md。

---

## 2026-03-14 - PR #1880 实战记录

### 场景
帮助用户提交 PR 到 vllm-project/vllm-omni，修复 tea_cache + cpu-offload 问题。

### 执行过程
1. **Fork & Clone** - 用户已有 fork，直接 clone
2. **DCO 修复** - Commit 缺少 signoff，使用 `git commit --amend --signoff` 修复
3. **GitHub CLI 配置** - 找到已安装的 gh CLI，配置 token 登录
4. **Push 修复** - Force push 更新 commit
5. **Issue 回复** - 使用 API 回复 issue #1868，解决 assign 请求
6. **设置跟踪** - 创建 cron 任务每 2 小时检查 PR 状态

### 遇到的问题
- GitHub 已禁用 token 直接认证，必须通过 gh CLI
- Windows PowerShell 的语法与 Bash 不同（用 `;` 而不是 `&&`）
- Gateway 服务不稳定，需要多次重试

### 用户反馈
- 希望 skill 能持续学习更新
- 需要自动处理 review 意见直到 PR 合入

### 改进点
1. ✅ 已添加 Windows PowerShell 命令适配
2. ✅ 已添加 gh CLI 自动检测和配置流程
3. ⏳ 需要添加更多错误重试机制
4. ⏳ 需要添加 review 意见自动分类和处理

### 新增模板
- 回复 issue assign 请求："Done! I've replied to issue #XXX..."

---

## 待学习场景

- [ ] 处理需要代码修改的 review 意见
- [ ] 解决 PR 冲突
- [ ] 多个 reviewer 意见冲突时的处理
- [ ] CI 随机失败（flaky test）的处理
- [ ] 长时间未 review 的跟进策略
