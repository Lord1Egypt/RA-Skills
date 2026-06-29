# 提交 MyKnowledge 到 agentskill.sh

**平台介绍**: [agentskill.sh](https://agentskill.sh) 是另一个 Agent Skills 目录平台，支持自动同步、所有权验证等功能。

---

## 提交步骤

### 1. 访问提交页面

打开浏览器，访问：https://agentskill.sh/submit

### 2. 输入 GitHub 仓库 URL

在输入框中填写 MyKnowledge 的 GitHub 仓库 URL：

```
https://github.com/CoderMoray/MyKnowledge
```

### 3. 点击"Import"

平台会自动扫描仓库中的所有 `SKILL.md` 文件，并导入技能。

### 4. （可选）绑定 GitHub 账号

如果需要验证技能归属、解锁数据分析功能：

1. 访问 [agentskill.sh 账户设置页面](https://agentskill.sh/settings)
2. 点击"Connect GitHub Account"
3. 授权后，你的仓库中的技能会自动被识别归属
4. 验证后，你的个人主页和对应技能页面会展示已验证标识

### 5. （可选）配置 Webhook 自动同步

如果需要在每次代码推送时自动更新技能：

1. 进入 GitHub 仓库 Settings → Webhooks → Add webhook
2. 配置以下信息：
   - **Payload URL**: `https://agentskill.sh/api/webhooks/github`
   - **Content type**: `application/json`
   - **Events**: 仅选择 `push` 事件
3. 点击"Add webhook"保存

---

## 自动同步规则

| 同步方式 | 说明 |
|----------|------|
| **每日自动同步** | 平台每 24 小时检查一次仓库变更，无需额外配置 |
| **Webhook 即时同步** | 配置 Webhook 后，每次 `git push` 都会触发更新 |
| **手动重新提交** | 访问 [agentskill.sh/submit](https://agentskill.sh/submit) 重新导入 |

---

## 验证提交成功

1. 访问 [agentskill.sh](https://agentskill.sh)
2. 搜索 `MyKnowledge` 或 `myknowledge`
3. 确认技能已出现在搜索结果中

---

## 更新 `scripts/release.sh`（待完成）

**当前状态**: agentskill.sh 可能没有公开的 API，无法程序化地提交。

**下一步**:
- [ ] 研究 agentskill.sh 是否有 API
- [ ] 如果有 API，更新 `scripts/release.sh` 自动提交
- [ ] 如果没有 API，保留本文档作为手动提交指南

---

**文档版本**: 1.0  
**最后更新**: 2026-06-14  
**维护者**: AI Agent
