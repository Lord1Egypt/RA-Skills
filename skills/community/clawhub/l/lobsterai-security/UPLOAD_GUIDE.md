# 🚀 GitHub 上传指南

此指南帮助您将 LobsterAI Security SKILL 上传到 GitHub 和其他 Skill 社区。

## 📦 前置准备

### 1. 确保安全 SKILL 已打包

SKILL 位置：
```
C:\Users\Administrator\AppData\Local\Programs\LobsterAI\resources\SKILLs\security\
```

必要文件：
- ✅ `SKILL.md` - 主要文档
- ✅ `README.md` - 简介
- ✅ `setup.py` - Python 打包配置
- ✅ `MANIFEST.in` - 打包清单
- ✅ `authorizer.py`, `audit_logger.py`, 等核心模块
- ✅ `.gitignore` - Git 忽略规则

### 2. 创建 GitHub 账号（如无）

访问 https://github.com/join

### 3. 生成 Personal Access Token (PAT)

1. 登录 GitHub
2. 进入 **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. 点击 **Generate new token** → **Generate new token (classic)**
4. 配置：
   - **Note:** LobsterAI Security SKILL Upload
   - **Expiration:** No expiration (或选择期限)
   - **Scopes:** ✅ `repo` (Full control of private repositories)
5. 点击 **Generate token**
6. **复制并保存** Token（只显示一次）

## 📤 上传方式

### 方式一：使用 GitHub CLI（推荐，无需 PAT）

1. **安装 GitHub CLI**

   **Windows (PowerShell):**
   ```powershell
   winget install --id GitHub.cli
   # 或下载安装包: https://cli.github.com/
   ```

   **macOS:**
   ```bash
   brew install gh
   ```

   **Linux:**
   ```bash
   sudo apt install gh  # Debian/Ubuntu
   ```

2. **登录 GitHub**

   ```powershell
   gh auth login
   # 选择: GitHub.com
   # 选择: HTTPS
   # 选择: Yes, authenticate with GitHub
   # 浏览器会打开，授权即可
   ```

3. **创建仓库并推送**

   ```powershell
   cd "C:\Users\Administrator\AppData\Local\Programs\LobsterAI\resources\SKILLs\security"

   # 创建公开仓库
   gh repo create lobsterai-security-skill `
     --description "Enterprise-grade security framework for LobsterAI" `
     --public `
     --source . `
     --push

   # 或创建私有仓库
   gh repo create lobsterai-security-skill --private --source . --push
   ```

### 方式二：使用提供的 PowerShell 脚本

我已经创建了自动化脚本：
```
C:\Users\Administrator\lobsterai\project\security\scripts\upload_to_github.ps1
```

**使用方法：**

```powershell
# 基本用法（会提示输入）
cd "C:\Users\Administrator\lobsterai\project\security\scripts"
.\upload_to_github.ps1

# 使用参数（非交互）
.\upload_to_github.ps1 -RepoName "lobsterai-security-skill" -GitHubUsername "your-username" -Pat "your-pat"
```

### 方式三：手动操作

如果上述方法都不行，可以手动完成：

1. **创建 GitHub 仓库**

   - 访问 https://github.com/new
   - Repository name: `lobsterai-security-skill`
   - Description: `Enterprise-grade security framework for LobsterAI with audit logging, RBAC, input validation, and scanning`
   - 选择 **Public**（推荐开源）或 **Private**
   - ❌ **不要**勾选 "Initialize this repository with a README"
   - 点击 **Create repository**

2. **推送本地代码**

   ```powershell
   cd "C:\Users\Administrator\AppData\Local\Programs\LobsterAI\resources\SKILLs\security"

   # 如果提示 fatal: remote origin already exists，先删除：
   git remote remove origin

   # 添加 remote（替换 YOUR_USERNAME）
   git remote add origin https://github.com/YOUR_USERNAME/lobsterai-security-skill.git

   # 设置主分支并推送
   git branch -M main
   git push -u origin main
   ```

3. **验证**

   访问 `https://github.com/YOUR_USERNAME/lobsterai-security-skill` 查看代码是否已推送。

## 🔗 提交到 Skill 市场

### Skillhub (clawhub.com)

1. 访问 https://clawhub.com 或 https://skills.sh
2. 注册/登录账号（通常使用 GitHub OAuth）
3. 点击 **Submit Skill** 或 **Add Skill**
4. 填写信息：
   - **Skill ID:** `security`
   - **Name:** `LobsterAI Security Framework`
   - **Repository URL:** `https://github.com/YOUR_USERNAME/lobsterai-security-skill`
   - **Version:** `1.0.0`
   - **License:** Proprietary
   - **Tags:** security, audit, rbac, compliance, validation, scanning
5. 提交审核

### 其他社区

根据您学习的 Skillhub 安装文档，其他平台可能包括：
- LobsterAI 官方技能市场（如果有）
- OpenCLAW 社区（如提到）

## 🏷️ 仓库设置建议

推送成功后，建议在 GitHub 上进行以下设置：

1. **添加主题 (Topics)**
   ```
   lobsterai security audit rbac compliance validation scanning
   ```

2. **启用 GitHub Pages**（可选，用于文档托管）
   - Settings → Pages → Source: `main` branch `/docs` folder
   - 然后可以将 SKILL.md 转换为 HTML 部署

3. **添加徽章**
   ```markdown
   [![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)](https://github.com/YOUR_USERNAME/lobsterai-security-skill)
   [![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/YOUR_USERNAME/lobsterai-security-skill/releases)
   [![License](https://img.shields.io/badge/license-Proprietary-red)](LICENSE)
   ```

4. **创建 Release**
   ```bash
   git tag -a v1.0.0 -m "First stable release"
   git push origin v1.0.0
   ```

5. **设置保护规则**（如果是开源且希望协作）
   - Settings → Branches → Add rule
   - Require pull request reviews
   - Require status checks

## 🔐 安全注意事项

- ✅ **不要**在仓库中提交任何真实的敏感配置（`rbac_config.json` 已 .gitignore）
- ✅ **不要**提交 `LOBSTERAI_AUDIT_SECRET` 或任何密钥
- ✅ **检查** `.gitignore` 是否包含 `logs/`, `.secret/`, `rbac_config.json`
- ✅ **推荐**使用 GitHub Secrets 存储 CI/CD 所需密钥

## 📝 下一步

1. ✅ 上传到 GitHub
2. ✅ 提交到 Skill 市场（clawhub.com, skills.sh）
3. 🔄 创建 GitHub Release
4. 🔄 添加详细的贡献指南 (CONTRIBUTING.md)
5. 🔄 添加代码 of conduct（可选）
6. 🔄 设置自动化测试 CI（如 GitHub Actions）

## 💡 获取帮助

- GitHub 文档: https://docs.github.com/
- GitHub CLI 文档: https://cli.github.com/manual/
- Skillhub 安装指南: https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/skillhub.md

---

**祝您部署顺利！** 🎉
