# 发布指南

**发布到 GitHub + ClawHub**

---

## 📦 方式 1：手动发布（推荐）

### 步骤 1：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`investment-buddy-pet`
3. 描述：投资宠物技能 - 12 只宠物陪伴你投资成长
4. 可见性：Public
5. 点击 "Create repository"

### 步骤 2：推送代码

```bash
cd /home/admin/.openclaw/workspace/projects/investment-buddy-pet

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin git@github.com:lj22503/investment-buddy-pet.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 3：发布到 ClawHub

```bash
# 安装 ClawHub CLI（如果未安装）
npm install -g clawhub

# 登录 ClawHub
clawhub login

# 发布技能
cd /home/admin/.openclaw/workspace/projects/investment-buddy-pet
clawhub publish
```

### 步骤 4：验证发布

```bash
# 测试安装
clawhub install investment-buddy-pet

# 验证文件
ls -la ~/.openclaw/skills/investment-buddy-pet/
```

---

## 🚀 方式 2：GitHub Actions 自动发布

### 创建工作流

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to ClawHub

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install ClawHub CLI
        run: npm install -g clawhub
      
      - name: Login to ClawHub
        run: clawhub login --token ${{ secrets.CLAWHUB_TOKEN }}
      
      - name: Publish to ClawHub
        run: clawhub publish
```

### 配置 Secrets

1. GitHub 仓库 → Settings → Secrets and variables → Actions
2. 添加 `CLAWHUB_TOKEN`（从 ClawHub 获取）

---

## 📝 发布前检查清单

### 代码质量

- [x] 合规检查器测试通过（6/6）
- [x] 话术生成器测试通过
- [x] 心跳引擎集成合规检查
- [ ] GitHub 仓库创建
- [ ] 代码推送到 GitHub

### 文档完整

- [x] SKILL.md（技能核心文档）
- [x] README.md（使用说明）
- [x] COMPLIANCE_DESIGN.md（合规设计）
- [x] BODY_DESIGN.md（Body 设计规范）
- [x] clawhub.json（ClawHub 配置）

### 合规检查

- [x] 不推荐具体产品
- [x] 不承诺收益
- [x] 不提供择时建议
- [x] 用户数据本地存储
- [x] 合规检查器集成
- [x] 投资者教育说明

### H5 对接

- [x] 结果页添加投资者教育说明
- [x] 合规承诺展示
- [x] 有趣话术（SSBTI 风格）
- [ ] 部署到 Vercel
- [ ] 绑定域名

---

## 🎯 版本管理

### 语义化版本

```
主版本。次版本。修订号
  ↑      ↑      ↑
 重大变更  新功能  修复

### 发布流程

1. 更新版本号（`clawhub.json` 和 `SKILL.md`）
2. 编写变更日志（CHANGELOG.md）
3. 提交并打标签
4. 推送到 GitHub
5. 发布到 ClawHub

```bash
# 更新版本号
vim clawhub.json  # version: "1.0.0"

# 提交
git add .
git commit -m "release: v1.0.0 - 初始版本"
git tag v1.0.0
git push origin main --tags

# 发布
clawhub publish
```

---

## 📊 发布后验证

### 测试安装

```bash
# 从 ClawHub 安装
clawhub install investment-buddy-pet

# 验证文件
ls -la ~/.openclaw/skills/investment-buddy-pet/

# 测试运行
cd ~/.openclaw/skills/investment-buddy-pet
python3 scripts/compliance_checker.py
```

### 测试宠物启动

```bash
# 启动松果
python3 scripts/heartbeat_engine.py start \
  --user-id test_user \
  --pet-type songguo

# 验证输出
# 🚀 心跳引擎启动（用户：test_user）
# 🐾 宠物：松果 (🐿️)
# ✅ 合规检查器已加载
```

---

## 🔗 相关链接

- GitHub 仓库：https://github.com/lj22503/investment-buddy-pet
- ClawHub 页面：https://clawhub.com/skills/investment-buddy-pet
- H5 测试页：https://mangofolio.vercel.app
- 问题反馈：https://github.com/lj22503/investment-buddy-pet/issues

---

**创建时间**：2026-04-10  
**版本**：v1.0.0  
**状态**：待发布
