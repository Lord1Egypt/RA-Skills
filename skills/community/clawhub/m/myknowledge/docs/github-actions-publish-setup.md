# GitHub Actions 自动发布配置指南

**目标**: 使用 GitHub Actions 自动发布 MyKnowledge 到 ClawHub 和 SkillHub，降低 Token 消耗。

---

## 配置步骤

### 1. 获取 ClawHub Token

**步骤**:
1. 打开终端，执行：
   ```bash
   clawhub login
   ```
2. 登录后，获取 Token：
   ```bash
   cat ~/.clawhub/token.json
   ```
3. 复制 Token（类似 `chub_xxx...`）

### 2. 获取 SkillHub Token

**步骤**:
1. 打开终端，执行：
   ```bash
   skillhub auth login --token skh_xxx
   ```
2. 登录后，获取 Token：
   ```bash
   skillhub auth token
   ```
3. 复制 Token（类似 `skh_xxx...`）

### 3. 配置 GitHub Secrets

**步骤**:
1. 打开浏览器，访问：https://github.com/CoderMoray/MyKnowledge/settings/secrets/actions
2. 点击"New repository secret"
3. 添加以下 Secrets：

| Name | Value | 说明 |
|------|-------|------|
| `CLAWHUB_TOKEN` | （ClawHub Token） | ClawHub 发布认证 |
| `SKILLHUB_TOKEN` | （SkillHub Token） | SkillHub 发布认证 |
| `SLACK_WEBHOOK_URL` | （可选） | Slack 通知 Webhook URL |

4. 点击"Add secret"保存

### 4. 测试 GitHub Actions

**手动触发**:
1. 打开浏览器，访问：https://github.com/CoderMoray/MyKnowledge/actions
2. 选择"Publish to ClawHub and SkillHub"工作流程
3. 点击"Run workflow"
4. 选择分支（如 `main`），点击"Run workflow"
5. 等待执行完成（约 5-10 分钟）

**推送标签触发**:
1. 打开终端，执行：
   ```bash
   git tag v1.4.87
   git push origin v1.4.87
   ```
2. GitHub Actions 会自动触发
3. 访问 https://github.com/CoderMoray/MyKnowledge/actions 查看执行日志

---

## 工作流程说明

### 触发条件

| 触发方式 | 条件 | 说明 |
|----------|------|------|
| **手动触发** | 在 GitHub Actions 页面点击"Run workflow" | 适用于测试或紧急发布 |
| **推送标签** | `git push origin v1.4.87` | 推荐方式，自动创建 GitHub Release |

### 执行步骤

1. **Checkout code**: 获取代码和完整 git 历史
2. **Setup Node.js**: 安装 Node.js（用于 ClawHub CLI）
3. **Setup Python**: 安装 Python（用于 SkillHub CLI）
4. **Install ClawHub CLI**: 全局安装 `clawhub`
5. **Install SkillHub CLI**: 安装 `skillhub`
6. **Build SkillHub zip**: 执行 `bash scripts/build-skillhub.sh`
7. **Publish to ClawHub**: 执行 `clawhub publish --no-input`
8. **Publish to SkillHub**: 执行 `skillhub publish releases/MyKnowledge-*.zip`
9. **Create GitHub Release**: 使用 `CHANGELOG.md` 创建 Release Notes
10. **Notify success/failure**: （可选）发送 Slack 通知

---

## 更新 `scripts/release.sh`

为了配合 GitHub Actions，需要更新 `scripts/release.sh`：

### 当前流程

```bash
# 我执行
bash scripts/release.sh 1.4.87
```

### 新流程

```bash
# 1. 我执行（只推送代码，不发布）
bash scripts/release.sh 1.4.87 --github-only

# 2. GitHub Actions 自动触发，执行发布
#    （或者你手动推送标签）
git tag v1.4.87
git push origin v1.4.87
```

### 更新 `scripts/release.sh`

让我更新 `scripts/release.sh`，添加 `--github-only` 参数：

```bash
#!/bin/bash

# 参数解析
GITHUB_ONLY=false
for arg in "${@:2}"; do
  case $arg in
    --github-only) GITHUB_ONLY=true ;;
    # ... 其他参数
  esac
done

# 发布到各渠道
if [ "$GITHUB_ONLY" = false ]; then
  # 发布到 ClawHub 和 SkillHub
  clawhub publish --no-input
  skillhub publish releases/MyKnowledge-*.zip
else
  echo "⏭️  跳过 ClawHub 和 SkillHub 发布（--github-only）"
fi

# 推送代码到 GitHub（总是执行）
git add -A
git commit -m "release: v${VERSION}"
git push origin main
git tag v${VERSION}
git push origin v${VERSION}
```

---

## 迁移计划

### 阶段 1：并行运行（推荐 🔥）

**目标**: 保持当前流程，同时测试 GitHub Actions

**步骤**:
1. 配置 GitHub Secrets（见上方"配置步骤"）
2. 推送 `.github/workflows/publish.yml` 到 main 分支
3. 手动触发 GitHub Actions，测试是否工作
4. 如果成功，开始使用 GitHub Actions 发布

**优点**:
- ✅ 安全：如果 GitHub Actions 失败，还可以用当前流程
- ✅ 渐进：逐步迁移，降低风险

### 阶段 2：完全迁移

**目标**: 只使用 GitHub Actions 发布

**步骤**:
1. 更新 `scripts/release.sh`，添加 `--github-only` 参数
2. 修改 `DEVELOPMENT.md`，说明新流程
3. 通知用户（如果有），新版本会自动发布

---

## 故障排查

### ClawHub 发布失败

**可能原因**:
- `CLAWHUB_TOKEN` 过期或无效
- `clawhub` CLI 版本不兼容

**解决方案**:
1. 重新获取 ClawHub Token
2. 更新 GitHub Secret
3. 在 GitHub Actions 日志中查看详细错误

### SkillHub 发布失败

**可能原因**:
- `SKILLHUB_TOKEN` 过期或无效
- `skillhub` CLI 安装失败

**解决方案**:
1. 重新获取 SkillHub Token
2. 更新 GitHub Secret
3. 检查 `scripts/build-skillhub.sh` 是否正常

### GitHub Release 创建失败

**可能原因**:
- `GITHUB_TOKEN` 权限不足
- `CHANGELOG.md` 格式错误

**解决方案**:
1. 检查 GitHub Actions 权限设置
2. 验证 `CHANGELOG.md` 格式

---

## 总结

**推荐方案**: 使用 GitHub Actions 自动发布

**优点**:
- ✅ 零 Token 消耗
- ✅ 自动化
- ✅ 可靠

**下一步**:
1. 配置 GitHub Secrets
2. 测试 GitHub Actions
3. 更新 `scripts/release.sh`
4. 完全迁移到 GitHub Actions

---

**文档版本**: 1.0  
**最后更新**: 2026-06-14  
**维护者**: AI Agent
