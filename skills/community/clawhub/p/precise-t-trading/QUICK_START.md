# 🚀 快速发布指南

> 5分钟将你的 Skill 发布到 ClawHub

---

## 📋 前置要求

- [x] Node.js 已安装
- [ ] GitHub 账号（用于登录 ClawHub）
- [x] Skill 文件已准备好

---

## 🎯 发布步骤（超简单）

### 步骤1: 打开发布脚本目录

```bash
cd I:\OpenClawWorkspace\skills\precise-t-trading
```

### 步骤2: 运行发布脚本

**Windows PowerShell**（推荐）:
```powershell
.\publish.ps1
```

**或者 CMD**:
```cmd
publish.bat
```

### 步骤3: 按提示操作

脚本会自动：
1. ✅ 检查 Node.js
2. ✅ 安装 ClawHub CLI（如果未安装）
3. ⏸️ **暂停，提示你手动登录** ← 这里需要你操作
4. ✅ 验证登录状态
5. ✅ 自动发布 Skill

---

## 🔑 手动登录步骤（只需1次）

当脚本提示时：

1. **打开浏览器**
2. **访问**: https://clawhub.ai
3. **点击** "Sign In"
4. **选择** "Continue with GitHub"（推荐）或邮箱登录
5. **完成授权**
6. **回到脚本**，按回车继续

---

## ✅ 发布成功验证

发布完成后，运行：

```bash
clawhub search "precise-t-trading"
```

应该能看到你的 Skill！

---

## 🌐 查看你的 Skill

访问: https://clawhub.com/skills/precise-t-trading

---

## ⚠️ 常见问题

### Q1: "clawhub: command not found"
**解决**: 运行 `npm install -g clawhub`

### Q2: "Login failed"
**解决**: 
1. 确认已在浏览器登录
2. 运行 `clawhub login` 重新登录

### Q3: "Slug already exists"
**解决**: 修改 `_meta.json` 中的 slug，例如 `precise-t-trading-v2`

### Q4: "Network error"
**解决**: 检查网络连接，可能需要科学上网

---

## 📞 需要帮助？

运行脚本遇到问题？告诉我错误信息，我帮你解决！🐙
