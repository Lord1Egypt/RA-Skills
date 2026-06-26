# GitHub PR 管理工作流

## 阶段 1：PR 初始化

### 信息收集
- 目标仓库：`owner/repo`
- 分支名：`feature-branch`
- PR 标题和描述
- 是否有对应 issue

### 执行步骤
1. 检查本地仓库是否存在
2. 如不存在，fork 并 clone
3. 创建 feature 分支
4. 应用代码修改
5. 提交 commit（带 signoff）
6. Push 到 fork
7. 创建 PR
8. 设置跟踪任务

## 阶段 2：CI 监控与修复

### 检查清单
- [ ] DCO 检查通过
- [ ] Lint/Format 检查通过
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 代码覆盖率满足要求

### 自动修复项

**DCO 失败**：
```bash
git commit --amend --signoff --no-edit
git push --force-with-lease origin <branch>
```

**Format 失败**（如有配置）：
```bash
# 根据项目配置执行 format
black .
# 或
pre-commit run --all-files
```

## 阶段 3：Review 处理

### Review 分类

| 类型 | 处理方式 |
|------|----------|
| 必须修改 (Required) | 立即修复并回复 |
| 建议修改 (Suggestion) | 评估后决定是否采纳 |
| 问题/疑问 (Question) | 回复澄清 |
| 赞赏 (Praise) | 礼貌感谢 |

### 处理流程

1. **获取 Review**：
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr}/reviews
   gh api repos/{owner}/{repo}/pulls/{pr}/comments
   ```

2. **分析每一条评论**：
   - 定位代码位置
   - 理解 reviewer 意图
   - 制定修复方案

3. **执行修复**：
   - 修改代码
   - 本地测试
   - 提交 commit
   - push 更新

4. **回复 Reviewer**：
   - 在对应行回复
   - 或在 PR 评论中统一回复
   - 标记为 resolved（如适用）

## 阶段 4：直到合入

### 合入条件检查
- [ ] 至少 1 个 approving review
- [ ] 所有 CI 检查通过
- [ ] 无冲突需要解决
- [ ] 满足分支保护规则

### 合入后操作
1. 通知用户 PR 已合入
2. 更新跟踪记录
3. 删除远程分支（可选）
4. 关闭相关 issue（如有）

## 常见问题

### Q: Reviewer 要求大幅重构怎么办？
A: 请示用户后再执行，评估工作量影响。

### Q: 多个 reviewer 意见冲突怎么办？
A: 发起讨论，请 reviewer 们达成一致。

### Q: CI 随机失败怎么办？
A: 检查是否为 flaky test，尝试 re-run，如持续失败需调查。

### Q: 长时间没 review 怎么办？
A: 礼貌 ping reviewer，或请社区其他成员帮忙 review。
