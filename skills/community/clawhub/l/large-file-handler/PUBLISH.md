# 📦 发布到 ClawHub | Publish to ClawHub

## 快速发布（3 步）| Quick Publish (3 Steps)

### 步骤 1：登录 ClawHub | Step 1: Login to ClawHub

打开浏览器，运行：
Open browser and run:

```bash
clawhub login
```

这会自动打开浏览器，登录你的 ClawHub 账户。
This will automatically open browser and login to your ClawHub account.

**或者使用 token 登录： | Or login with token:**

1. 访问 | Visit: https://clawhub.ai/settings/tokens
2. 创建一个新的 API token | Create a new API token
3. 复制 token | Copy the token
4. 运行 | Run: `clawhub login --token "你的 token | your token"`

---

### 步骤 2：验证登录 | Step 2: Verify Login

```bash
clawhub whoami
```

如果显示你的用户名，说明登录成功。
If it shows your username, login is successful.

---

### 步骤 3：发布技能 | Step 3: Publish Skill

```bash
cd "E:\ai\openclaw\.openclaw\workspace"

clawhub publish "skills/large-file-handler" ^
  --slug "large-file-handler" ^
  --name "大文件异步处理器" ^
  --version "1.0.0" ^
  --tags "latest,file,async,pdf,video,large-file" ^
  --changelog "Initial release - Async large file processing framework"
```

---

## 🎯 一键发布脚本 | One-Click Publish Script

我已经为你创建了发布脚本，运行即可：
Publish script created for you, just run:

```bash
# PowerShell
powershell -ExecutionPolicy Bypass -File "E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\publish.ps1"
```

---

## ✅ 发布前检查清单 | Pre-Publish Checklist

- [x] `SKILL.md` 格式正确 | Format correct
- [x] `_meta.json` 包含作者信息（Leo）| Author info included
- [x] `README.md` 完整（中英双语）| Complete (bilingual)
- [x] 脚本可以正常运行 | Scripts working
- [ ] **已登录 ClawHub 账户** ← 需要人工完成 | Need manual completion
- [ ] **已执行发布命令** | Execute publish command

---

## 📊 发布后 | After Publishing

发布成功后，你的技能会出现在：
After successful publish, your skill will appear at:

- **ClawHub 网站 | Website**: https://clawhub.ai/skills/large-file-handler
- **CLI 搜索 | Search**: `clawhub search "large file"`
- **CLI 安装 | Install**: `clawhub install large-file-handler`

---

## 🔄 更新技能 | Update Skill

如果需要更新（修复 bug、添加功能）：
If you need to update (bug fixes, new features):

```bash
cd "E:\ai\openclaw\.openclaw\workspace"

# 自动递增版本号并发布 | Auto-increment version and publish
clawhub publish "skills/large-file-handler" ^
  --slug "large-file-handler" ^
  --version "1.0.1" ^
  --tags "latest" ^
  --changelog "修复 xxx 问题，添加 xxx 功能 | Fix xxx, add xxx feature"
```

---

## ⚠️ 注意事项 | Notes

1. **Slug 唯一性** - `large-file-handler` 必须是唯一的，如果已被占用需要改名
   **Slug Uniqueness** - Must be unique, rename if already taken

2. **版本号** - 使用语义化版本 (major.minor.patch)
   **Version** - Use semantic versioning (major.minor.patch)

3. **标签** - `latest` 标签会指向最新版本
   **Tags** - `latest` tag points to newest version

4. **审核** - 新技能可能需要审核才能公开显示
   **Review** - New skills may need review before public display

---

## 🆘 遇到问题？| Troubleshooting?

### 错误：Slug already exists | Error: Slug already exists

说明技能已存在，你是所有者吗？
Skill already exists, are you the owner?

- **是 | Yes**: 使用 `--force` 覆盖，或递增版本号 | Use `--force` or increment version
- **否 | No**: 更改 slug 名称，如 `large-file-handler-leo` | Change slug name

### 错误：Not logged in | Error: Not logged in

运行 `clawhub login` 重新登录
Run `clawhub login` to login again

### 错误：Unauthorized | Error: Unauthorized

Token 无效或过期，重新获取 token
Token invalid or expired, get new token

---

**作者 | Author**: Leo 🦁  
**创建日期 | Created**: 2026-04-03
