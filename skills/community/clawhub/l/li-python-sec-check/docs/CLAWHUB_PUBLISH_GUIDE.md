# ClawHub 发布指南

## 🚀 发布 Li_python_sec_check 到 ClawHub

### 前置准备

1. **确认技能文件完整**
```bash
cd /root/.openclaw/workspace/skills/Li_python_sec_check
ls -la
```

**必需文件**：
- ✅ SKILL.md
- ✅ README.md
- ✅ _meta.json
- ✅ package.json
- ✅ scripts/python_sec_check.py
- ✅ LICENSE

2. **安装 clawhub CLI**（已安装）
```bash
clawhub --version
# v0.8.0
```

---

## 📋 发布步骤

### 步骤 1: 登录 ClawHub

```bash
# 登录（会打开浏览器）
clawhub login

# 或使用 Token 登录
clawhub auth login --token YOUR_API_TOKEN
```

### 步骤 2: 验证登录

```bash
clawhub whoami
```

**预期输出**：
```
Logged in as: your-username
Email: your@email.com
```

### 步骤 3: 发布技能

```bash
# 方式 1: 使用 CLI 发布
cd /root/.openclaw/workspace/skills
clawhub publish Li_python_sec_check

# 方式 2: 指定版本
clawhub publish Li_python_sec_check --version 2.1.0

# 方式 3: 发布为私有
clawhub publish Li_python_sec_check --visibility private
```

### 步骤 4: 验证发布

```bash
# 搜索技能
clawhub search Li_python_sec_check

# 查看技能详情
clawhub inspect Li_python_sec_check
```

---

## 🔧 发布配置

### package.json 配置

Li_python_sec_check 的 package.json 已配置：

```json
{
  "name": "Li_python_sec_check",
  "version": "2.1.0",
  "description": "Python 安全规范检查工具 - 基于 CloudBase 规范 + 腾讯安全指南 + LLM 智能分析",
  "author": "北京老李",
  "license": "MIT",
  "keywords": [
    "python",
    "security",
    "static-analysis",
    "devsecops",
    "code-quality",
    "privacy",
    "llm"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/your-repo/Li_python_sec_check.git"
  },
  "skill": {
    "entry": "scripts/python_sec_check.py",
    "category": "security",
    "tags": ["security", "python", "static-analysis", "devsecops"]
  },
  "publish": {
    "platform": "clawhub",
    "visibility": "public",
    "autoPublish": false
  }
}
```

### _meta.json 配置

```json
{
  "name": "Li_python_sec_check",
  "version": "2.1.0",
  "author": "北京老李",
  "category": "security",
  "tags": ["security", "python", "static-analysis", "devsecops", "privacy", "llm"]
}
```

---

## 📦 发布选项

### 版本管理

```bash
# 自动升级版本号
clawhub publish Li_python_sec_check --bump patch  # 2.1.0 -> 2.1.1
clawhub publish Li_python_sec_check --bump minor  # 2.1.0 -> 2.2.0
clawhub publish Li_python_sec_check --bump major  # 2.1.0 -> 3.0.0

# 指定版本号
clawhub publish Li_python_sec_check --version 2.1.0
```

### 可见性

```bash
# 公开发布（默认）
clawhub publish Li_python_sec_check --visibility public

# 私有发布
clawhub publish Li_python_sec_check --visibility private

# 仅团队成员可见
clawhub publish Li_python_sec_check --visibility team
```

### 发布说明

```bash
# 添加发布说明
clawhub publish Li_python_sec_check \
  --message "v2.1.0: 新增 LLM 智能分析、隐私和数据安全检查"
```

---

## 🧪 发布前检查清单

### 文件完整性
- [ ] SKILL.md 存在且格式正确
- [ ] README.md 存在且内容完整
- [ ] _meta.json 存在且版本正确
- [ ] package.json 存在且配置正确
- [ ] LICENSE 存在
- [ ] 主脚本文件存在（scripts/python_sec_check.py）

### 内容检查
- [ ] 版本号已更新（v2.1.0）
- [ ] 作者信息统一（北京老李）
- [ ] 无个人隐私泄露
- [ ] 无硬编码密钥
- [ ] CHANGELOG.md 已更新

### 功能测试
- [ ] 技能可以正常运行
- [ ] 所有检查项工作正常
- [ ] 测试通过

---

## 🎯 快速发布命令

```bash
# 一键发布（推荐）
cd /root/.openclaw/workspace/skills/Li_python_sec_check
clawhub publish . --version 2.1.0 --message "v2.1.0: LLM 智能分析 + 隐私安全检查"

# 验证发布
clawhub search Li_python_sec_check
```

---

## 📊 发布后验证

### 1. 搜索技能
```bash
clawhub search Li_python_sec_check
```

### 2. 查看详情
```bash
clawhub inspect Li_python_sec_check
```

### 3. 测试安装
```bash
# 在测试目录安装
cd /tmp
clawhub install Li_python_sec_check

# 验证安装
cd Li_python_sec_check
python scripts/python_sec_check.py --help
```

---

## 🔙 回滚（如有问题）

```bash
# 隐藏技能
clawhub hide Li_python_sec_check

# 删除技能
clawhub delete Li_python_sec_check

# 恢复技能
clawhub undelete Li_python_sec_check
```

---

## 📈 发布后操作

### 1. 分享技能
- ClawHub 技能页面链接
- GitHub 仓库链接
- 社交媒体分享

### 2. 收集反馈
- 关注 ClawHub 评论
- 回复用户问题
- 收集改进建议

### 3. 持续更新
- 修复 Bug
- 添加新功能
- 更新文档

---

## ❓ 常见问题

### Q: 发布失败怎么办？
**A**: 
1. 检查登录状态：`clawhub whoami`
2. 检查文件格式：确保 SKILL.md 等文件存在
3. 查看错误信息：根据提示修复

### Q: 如何更新已发布的技能？
**A**: 
```bash
# 升级版本号
clawhub publish Li_python_sec_check --bump patch

# 重新发布
clawhub publish Li_python_sec_check --version 2.1.1
```

### Q: 可以取消发布吗？
**A**: 可以，使用 `clawhub hide` 或 `clawhub delete`

### Q: 发布需要审核吗？
**A**: 根据 ClawHub 政策，可能需要审核，通常 24-48 小时

---

## 📞 支持

- **ClawHub 文档**: https://docs.clawhub.com
- **GitHub Issues**: https://github.com/your-repo/Li_python_sec_check/issues
- **邮件**: support@clawhub.com

---

**准备就绪！可以开始发布了！** 🚀
