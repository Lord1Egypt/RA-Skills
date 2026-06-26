# 🚀 Gateway Guardian 发布指南

**目标：** 将技能发布到 GitHub 和 ClawHub

---

## ⚠️ 需要认证

由于 GitHub 和 ClawHub 都需要浏览器登录认证，请按以下步骤操作：

---

## 📤 步骤 1：发布到 GitHub

### 方法 A：使用 GitHub Desktop（最简单）

1. **打开 GitHub Desktop**
   - 如果未安装，下载：https://desktop.github.com/

2. **添加本地仓库**
   - 点击 `File` → `Add Local Repository`
   - 选择目录：
     ```
     C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian
     ```
   - 点击 `Add repository`

3. **发布到 GitHub**
   - 点击 `File` → `Publish repository`
   - 名称：`openclaw-gateway-guardian`
   - 描述：`OpenClaw Gateway Guardian - 自动监控、保护和重启 OpenClaw 网关服务`
   - 勾选 `Public`
   - 点击 `Publish repository`

4. **验证**
   - 访问：https://github.com/davidme6/openclaw-gateway-guardian
   - 应该能看到所有文件

---

### 方法 B：使用浏览器手动创建

1. **访问 GitHub**
   - 打开：https://github.com/new

2. **创建仓库**
   - 仓库名：`openclaw-gateway-guardian`
   - 描述：`OpenClaw Gateway Guardian - 自动监控、保护和重启 OpenClaw 网关服务`
   - 选择 `Public`
   - **不要** 勾选 "Initialize this repository with a README"
   - 点击 `Create repository`

3. **上传文件**
   - 点击 `uploading an existing file`
   - 拖拽以下文件到浏览器：
     ```
     README.md
     SKILL.md
     DEPLOY.md
     DEPLOYMENT.md
     STATUS.md
     requirements.txt
     scripts/gateway_guardian.py
     scripts/install_guardian.ps1
     ```
   - 点击 `Commit changes`

---

### 方法 C：使用 Git 命令（需要 Token）

1. **获取 GitHub Token**
   - 访问：https://github.com/settings/tokens
   - 点击 `Generate new token (classic)`
   - 勾选 `repo` 权限
   - 生成并复制 Token

2. **推送代码**
   ```bash
   cd C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian
   
   # 替换 YOUR_TOKEN 为你的 GitHub Token
   git push https://YOUR_TOKEN@github.com/davidme6/openclaw-gateway-guardian.git main
   ```

---

## 📦 步骤 2：发布到 ClawHub

### 方法 A：使用浏览器登录（推荐）

1. **打开浏览器**
   - 访问：https://clawhub.ai/cli/auth

2. **登录 ClawHub**
   - 使用你的账号登录
   - 复制 Token

3. **存储 Token**
   ```bash
   clawhub login --token YOUR_TOKEN
   ```

4. **发布技能**
   ```bash
   cd C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian
   clawhub publish .
   ```

5. **验证**
   - 访问：https://clawhub.com/skills/openclaw-gateway-guardian

---

### 方法 B：自动登录（会打开浏览器）

1. **运行登录命令**
   ```bash
   clawhub login
   ```

2. **在浏览器中完成登录**
   - 会自动打开浏览器
   - 点击 `Authorize`

3. **发布技能**
   ```bash
   cd C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian
   clawhub publish .
   ```

---

## ✅ 验证清单

### GitHub
- [ ] 仓库已创建：https://github.com/davidme6/openclaw-gateway-guardian
- [ ] 所有文件已上传
- [ ] README.md 显示正常

### ClawHub
- [ ] 技能已发布：https://clawhub.com/skills/openclaw-gateway-guardian
- [ ] 技能描述正确
- [ ] 可以安装

---

## 🔧 快速验证命令

```bash
# 检查 GitHub 仓库
curl https://api.github.com/repos/davidme6/openclaw-gateway-guardian

# 检查 ClawHub 技能
clawhub inspect openclaw-gateway-guardian

# 测试安装
clawhub install openclaw-gateway-guardian
```

---

## 📝 文件清单

确保以下文件已上传：

- [x] `README.md` - 项目说明
- [x] `SKILL.md` - ClawHub 技能描述
- [x] `DEPLOY.md` - GitHub 部署指南
- [x] `DEPLOYMENT.md` - 完整部署指南
- [x] `STATUS.md` - 当前状态报告
- [x] `PUBLISH_GUIDE.md` - 本文件
- [x] `requirements.txt` - Python 依赖
- [x] `scripts/gateway_guardian.py` - 主程序（29KB）
- [x] `scripts/install_guardian.ps1` - Windows 安装脚本

---

## 🎯 一键发布脚本（可选）

创建一个 PowerShell 脚本 `publish.ps1`：

```powershell
# 发布到 GitHub（使用 GitHub Desktop）
Write-Host "Opening GitHub Desktop..."
Start-Process "github"

# 发布到 ClawHub
Write-Host "Logging in to ClawHub..."
clawhub login

Write-Host "Publishing to ClawHub..."
cd C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian
clawhub publish .

Write-Host "Done!"
```

---

## 📞 需要帮助？

如果遇到任何问题：

1. **GitHub 问题** - 检查网络连接，确认账号登录
2. **ClawHub 问题** - 检查 Token 是否有效
3. **文件缺失** - 确认所有文件都在目录中

---

**发布完成后，技能将可供全球用户安装使用！🎉**
