# GitHub 发布步骤指南

## 准备工作（在本地执行）

### 1. 安装GitHub CLI（推荐）

**macOS:**
```bash
brew install gh
```

**Windows:**
```powershell
winget install --id GitHub.cli
```

**Linux:**
```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. 登录GitHub

```bash
gh auth login
```
- 按提示选择：GitHub.com → HTTPS → 浏览器登录
- 或选择Token方式（如果你生成了Personal Access Token）

---

## 发布步骤

### 方法1：使用GitHub CLI（推荐，最简单）

```bash
# 1. 进入项目目录
cd /path/to/mbti-master

# 2. 初始化git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial release v1.0.0"

# 5. 创建GitHub仓库并推送（一步完成）
gh repo create mbti-master --public --source=. --push

# 6. 创建Release版本
git tag v1.0.0
git push origin v1.0.0

# 7. 创建Release并上传打包文件
gh release create v1.0.0 --title "v1.0.0 - Initial Release" --notes "MBTI人格分析工具首个版本"
```

**打包并上传到Release：**
```bash
# 创建发布包
tar -czf mbti-master-v1.0.0.tar.gz --exclude='.git' --exclude='*.tar.gz' .

# 上传到Release
gh release upload v1.0.0 mbti-master-v1.0.0.tar.gz
```

---

### 方法2：使用传统Git命令

```bash
# 1. 进入项目目录
cd /path/to/mbti-master

# 2. 初始化git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial release v1.0.0 - MBTI personality analysis tool"

# 5. 在GitHub网页上创建仓库
# 访问 https://github.com/new
# 输入 Repository name: mbti-master
# 选择 Public
# 点击 Create repository

# 6. 关联远程仓库（替换yourusername为你的GitHub用户名）
git remote add origin https://github.com/yourusername/mbti-master.git

# 7. 推送代码
git branch -M main
git push -u origin main

# 8. 创建标签
git tag v1.0.0
git push origin v1.0.0
```

**在GitHub网页上创建Release：**
1. 访问 `https://github.com/yourusername/mbti-master/releases`
2. 点击 "Create a new release"
3. 选择标签 "v1.0.0"
4. 标题输入："v1.0.0 - Initial Release"
5. 内容复制：
   ```markdown
   ## MBTI Master v1.0.0
   
   首个正式版本发布！
   
   ### 功能特性
   - 4维度8题快速测试
   - 16型人格完整分析
   - 认知功能深度解析
   - 人格兼容性匹配
   - 趣味互动游戏
   
   ### 安装
   ```bash
   git clone https://github.com/yourusername/mbti-master.git
   cd mbti-master
   bash scripts/quick_test.sh
   ```
   
   ### 作者
   申建
   ```
6. 上传文件：`mbti-master-v1.0.0.tar.gz`
7. 点击 "Publish release"

---

## 验证发布

发布完成后，访问：
```
https://github.com/yourusername/mbti-master
```

确认：
- [ ] 代码已上传
- [ ] README正常显示
- [ ] License显示为MIT
- [ ] Release页面有v1.0.0
- [ ] 可下载tar.gz文件

---

## 分享给别人使用

发布后，别人可以通过以下方式安装：

```bash
# 方法1：Git克隆
git clone https://github.com/yourusername/mbti-master.git
cd mbti-master
bash scripts/quick_test.sh

# 方法2：下载Release
curl -L https://github.com/yourusername/mbti-master/releases/download/v1.0.0/mbti-master-v1.0.0.tar.gz -o mbti-master.tar.gz
tar -xzf mbti-master.tar.gz
cd mbti-master
bash scripts/quick_test.sh
```

---

## 后续更新

如果要发布新版本：

```bash
# 修改代码后
git add .
git commit -m "Update: 描述修改内容"
git push

# 创建新版本
git tag v1.1.0
git push origin v1.1.0

# 创建Release（使用CLI）
gh release create v1.1.0 --title "v1.1.0" --notes "更新说明"
```

---

## 常见问题

**Q: 提示权限错误？**  
A: 确认已登录 `gh auth login` 或使用HTTPS方式

**Q: 推送失败？**  
A: 确认GitHub仓库已创建，且用户名正确

**Q: 文件太大？**  
A: 检查.gitignore是否排除了node_modules等文件夹

---

**需要帮助？**  
GitHub文档：https://docs.github.com/zh/repositories