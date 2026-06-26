# 🚀 Node Connection Doctor - ClawHub 发布清单

**状态**: ✅ 准备就绪 (2026-03-26 10:30)

---

## 📦 技能文件结构

```
node-connection-doctor/
├── skills.json          # ClawHub 清单 (metadata)
├── SKILL.md             # 技能技术文档
├── README.md            # 用户友好文档
├── scripts/
│   └── diagnose.js      # 诊断脚本
└── screenshots/         # 截图 (可选)
    ├── demo-1.png
    └── demo-2.png
```

**所有文件已就绪**，位于: `skills/node-connection-doctor/`

---

## 🎯 发布步骤

### 1. 登录 ClawHub
- 访问 https://clawhub.com
- 登录你的账户 (或注册)

### 2. 创建新技能 listing
- 点击 **"Publish a Skill"** 或 **"Create Skill"**
- 填写以下信息:

**基本信息**:
- **Skill ID**: `node-connection-doctor` (与 skills.json 一致)
- **Name**: Node Connection Doctor
- **Short Description**: Automatically diagnose and fix OpenClaw node connection issues
- **Category**: Troubleshooting
- **Tags**: node, connection, diagnose, fix, gateway, tailscale

**详细描述**: 复制粘贴 `README.md` 内容 (已优化，可直接用)

**定价**:
- Single Diagnostic: $5 (one-time)
- Full Repair Service: $15 (one-time)
- Enterprise API: $50/month

**示例**: 复制 `skills.json` 中的 `examples` 部分

**Requirements**:
- OpenClaw >= 2026.3.23

### 3. 上传文件
打包技能目录：
```bash
cd skills
tar -czf node-connection-doctor.tar.gz node-connection-doctor/
```

在 ClawHub 表单中上传 `node-connection-doctor.tar.gz`

### 4. 截图 (可选但推荐)
运行截图脚本或手动截图：
```bash
node browser-agent.js title https://example.com  # 示例
```

建议截图:
- 诊断输出示例
- 修复命令示例
- 使用流程图解

### 5. 提交审核
- 勾选 "I confirm this skill works as described"
- 点击 **Submit for Review**
- 通常 1-3 天审核期

---

## 💰 定价策略

| Plan | Price | Target |
|------|-------|--------|
| Single Diagnostic | $5 | 轻度用户，单次问题 |
| Full Repair Service | $15 | 大多数用户 (推荐) |
| Enterprise API | $50/mo | 企业多节点 |

**预期收入**:
- 保守: 2 次诊断/周 = $40/月
- 乐观: 10 次诊断 + 2 次修复 = $110/月
- 被动 (API): 2 家企业 = $100/月

---

## 📢 推广渠道 (发布后)

- r/openclaw - 发帖介绍
- OpenClaw Discord - #skills 频道
- r/selfhosted - 如果相关
- 个人 Twitter/LinkedIn
- SEO 教程中推荐 (交叉推广)

---

## ⚠️ 注意事项

- 确保 `skills.json` 的 `id` 与 ClawHub 清单一致
- 定价以 USD 为单位
- 保持技能最小权限 (不需要外部网络)
- 提供清晰的错误处理
- 文档包含示例 YAML

---

**状态**: 所有文件已就绪，可随时打包上传

**预计发布时间**: 2026-03-26 (今日)

**期望首笔收入**: 3-7 天内

---