# 🦀 ClawHub 发布快速指南

## 快速发布（3 步）

### Step 1: 确保登录

```bash
clawhub login
```

浏览器会打开，点击 "Authorize" 授权。

### Step 2: 发布技能

```bash
clawhub publish C:/Users/User/.openclaw/workspace/skills/prompt-router --slug prompt-router --name "Prompt-Router" --version 1.0.0
```

### Step 3: 验证发布

```bash
clawhub search prompt-router
```

看到技能信息即表示发布成功！

---

## 完整发布（带详细信息）

```bash
clawhub publish C:/Users/User/.openclaw/workspace/skills/prompt-router \
  --slug prompt-router \
  --name "Prompt-Router" \
  --version 1.0.0 \
  --changelog "Initial release - Fast routing engine with <10ms latency" \
  --tags "latest,routing,performance,optimization"
```

---

## 常见问题

### Q: 提示 "Not logged in"
**A:** 运行 `clawhub login` 重新登录

### Q: 提示 "Slug already exists"
**A:** 使用不同 slug 或更新现有技能：
```bash
clawhub publish ... --version 1.0.1  # 升级版本
```

### Q: 发布后找不到技能
**A:** 等待 1-2 分钟索引更新，然后搜索：
```bash
clawhub search prompt-router
```

---

## 发布后操作

### 1. 安装测试

```bash
# 在新目录测试安装
cd /tmp
clawhub install prompt-router
```

### 2. 分享链接

ClawHub 技能页面：
```
https://clawhub.ai/skills/prompt-router
```

### 3. 更新 README

添加安装徽章：
```markdown
[![ClawHub](https://img.shields.io/badge/ClawHub-prompt--router-orange.svg)](https://clawhub.ai/skills/prompt-router)
```

---

## 后续更新

### 修复 Bug（v1.0.1）

```bash
# 修改代码后
git commit -m "fix: 修复 XXX 问题"
git push

# 发布新版本
clawhub publish ./prompt-router --version 1.0.1 --changelog "Bug fixes"
```

### 新功能（v1.1.0）

```bash
# 添加新功能后
git commit -m "feat: 添加 XXX 功能"
git push

# 发布新版本
clawhub publish ./prompt-router --version 1.1.0 --changelog "New features: ..."
```

---

## 统计和监控

### 查看下载量

```bash
clawhub stats prompt-router
```

### 查看评价

访问：https://clawhub.ai/skills/prompt-router#reviews

---

*最后更新：2026-04-06 00:15*
