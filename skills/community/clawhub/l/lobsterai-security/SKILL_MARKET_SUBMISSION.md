# 🌐 Skill 社区提交指南

本指南说明如何将 LobsterAI Security SKILL 提交到各大 Skill 市场。

## 📊 支持的市场

| 平台 | URL | 状态 |
|------|-----|------|
| **Skillhub (clawhub.com)** | https://clawhub.com | ✅ 推荐 |
| **Skillhub (skills.sh)** | https://skills.sh | ✅ 推荐 |
| **LobsterAI 官方市场** | 待定 | ⏳ coming soon |

## 📦 提交前准备

### 1. 确保 SKILL 元数据完整

您的 SKILL 应包含以下文件：

```
security/
├── SKILL.md              # ✅ 主要文档（必须）
├── README.md             # ✅ 简介（必须）
├── setup.py              # ✅ Python 打包配置
├── MANIFEST.in           # ✅ 打包清单
├── authorizer.py         # ✅ 核心模块
├── audit_logger.py       # ✅ 核心模块
├── rbac_config.example.json  # ✅ 配置示例
├── tests.py              # ✅ 测试文件
├── scripts/              # ✅ 辅助脚本
│   ├── daily_code_scan.ps1
│   └── weekly_rbac_audit.ps1
└── .gitignore            # ✅ Git 忽略规则
```

### 2. 验证 SKILL.md Frontmatter

确保 SKILL.md 以正确的 YAML frontmatter 开头：

```yaml
---
name: security
description: Enterprise-grade security framework for LobsterAI with audit logging, RBAC, input validation, output sanitization, code scanning, and dependency vulnerability detection.
version: 1.0.0
author: LobsterAI Security Team
license: Proprietary
official: true
core: true
priority: 100
tags:
  - security
  - audit
  - rbac
  - compliance
  - validation
  - scanning
---
```

关键字段：
- `name`: 技能唯一 ID，小写字母和连字符
- `description`: 简洁描述（150 字以内）
- `version`: 语义化版本
- `official`: `true` 表示官方认证
- `core`: `true` 表示核心技能
- `tags`: 关键词，便于搜索

### 3. 准备 GitHub 仓库

确保代码已推送到 GitHub：

```bash
https://github.com/YOUR_USERNAME/lobsterai-security-skill
```

仓库应：
- ✅ 公开（Public）以便社区访问
- ✅ 包含完整的提交历史
- ✅ 有清晰的 README
- ✅ 已创建 Release（v1.0.0）

### 4. 创建发布包（可选）

```bash
cd security
python setup.py sdist bdist_wheel

# 生成的文件在 dist/ 目录：
# - lobsterai_security_skill-1.0.0-py3-none-any.whl
# - lobsterai-security-skill-1.0.0.tar.gz
```

## 🌍 Skillhub (clawhub.com) 提交

### 步骤 1: 注册/登录

1. 访问 https://clawhub.com
2. 点击 **Sign Up** 或 **Log In**
3. 使用 GitHub OAuth 或邮箱注册

### 步骤 2: 提交 Skill

1. 登录后，导航到 **Developers** → **Submit Skill**
2. 填写表单：

| 字段 | 值/说明 |
|------|---------|
| **Skill ID** | `security` |
| **Name** | `LobsterAI Security Framework` |
| **Short Description** | Enterprise-grade security with audit logging, RBAC, and scanning |
| **Full Description** | 从 SKILL.md 复制主要内容（保留格式） |
| **Repository URL** | `https://github.com/YOUR_USERNAME/lobsterai-security-skill` |
| **Version** | `1.0.0` |
| **License** | `Proprietary` |
| **Skillhub Category** | `Security` 或 `Core` |
| **Tags** | `security,audit,rbac,compliance,validation,scanning` |
| **Installation Command** | `pip install lobsterai-security-skill`（可选） |

3. 上传截图（可选）：
   - 审计日志示例截图
   - RBAC 配置界面截图（如有）
   - 扫描结果截图

4. 同意服务条款
5. 点击 **Submit for Review**

### 步骤 3: 等待审核

- 通常 1-3 个工作日
- 审核状态可在 Dashboard 查看
- 如有问题，社区会通过邮件或站内信反馈

### 步骤 4: 发布后

审核通过后：
1. Skill 将出现在 Skillhub 搜索结果中
2. 用户可以通过 `skill install security` 安装
3. 您可以收到下载量和使用统计

## 🌐 Skillhub (skills.sh) 提交

### 步骤 1: 访问平台

- 主站: https://skills.sh
- 国内镜像: 根据 https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/skillhub.md

### 步骤 2: 提交流程

流程与 clawhub.com 类似：

1. 登录/注册
2. 进入 **Publish** 或 **Add New Skill**
3. 填写相同的元数据
4. 提交审核

### 特殊要求

skills.sh 可能要求：
- 提供演示视频或 GIF（30 秒以内）
- 包含至少 3 个使用示例
- 提供测试报告

## 🔗 多平台同步建议

### 保持一致性

在所有平台使用相同的：
- Skill ID: `security`
- 版本号: `1.0.0` (递增)
- 描述文案（可适度调整）
- 标签/关键词

### 版本发布流程

```
1. 更新版本号 (SKILL.md, setup.py)
2. 更新 CHANGELOG.md
3. 提交并打 Git tag: git tag -a v1.0.0 -m "Release 1.0.0"
4. 推送到 GitHub: git push origin v1.0.0
5. 创建 GitHub Release
6. 在 Skill 市场提交更新（通常会自动检测）
```

### 监控反馈

- 定期查看各平台的问题反馈
- 及时回复用户评论
- 根据反馈迭代改进

## 📋 提交清单

提交前请检查：

- [ ] GitHub 仓库已创建并公开
- [ ] SKILL.md 格式正确，frontmatter 完整
- [ ] README.md 简洁明了
- [ ] 所有核心文件已提交（无遗漏）
- [ ] .gitignore 排除敏感文件
- [ ] tests.py 可以通过
- [ ] DEPLOYMENT.md 包含完整部署指南
- [ ] 版本号正确（建议从 1.0.0 开始）
- [ ] 许可证明确（Proprietary 或 OSS）
- [ ] 截图/演示材料准备（如需要）
- [ ] 已阅读平台具体规则

## 🆘 常见问题

### Q: 提交被拒绝怎么办？

A: 查看审核反馈，常见原因：
- 缺少必要文件（SKILL.md, README.md）
- 描述不清晰或夸大
- 包含敏感信息或恶意代码
- 不符合平台分类标准

修改后重新提交。

### Q: 可以提交到多个平台吗？

A: 完全可以！推荐在多个平台分发以增加曝光。

### Q: 如何处理用户问题？

A: 建议：
- 在 GitHub 开启 Issues
- 在各平台及时回复评论
- 创建 FAQ 文档

### Q: 如何更新已发布的 SKILL？

A:
1. 更新代码和文档
2. 增加版本号（如 1.0.1）
3. 创建新的 GitHub Release
4. 在 Skill 市场提交更新请求

---

**祝您发布成功！** 🎉

如有问题，请参考：
- [Skillhub 官方文档](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/skillhub.md)
- [LobsterAI 开发者指南](https://lobsterai.com/docs)
