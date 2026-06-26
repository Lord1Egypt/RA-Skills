# 📤 上传到 GitHub 指南

## 方法一：使用 GitHub CLI（推荐）

### 1. 登录 GitHub

```bash
gh auth login
```

按照提示完成登录。

### 2. 创建远程仓库

```bash
cd C:\Windows\System32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian

gh repo create openclaw-gateway-guardian --public --source=. --push
```

### 3. 验证

访问：https://github.com/davidme6/openclaw-gateway-guardian

---

## 方法二：使用 Git 命令

### 1. 创建 GitHub 仓库

在 GitHub 网站上：
1. 访问 https://github.com/new
2. 仓库名：`openclaw-gateway-guardian`
3. 描述：`OpenClaw Gateway Guardian - 网关守护神`
4. 选择 **Public**
5. **不要** 勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 2. 添加远程仓库

```bash
cd C:\Windows\System32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian

git remote add origin https://github.com/davidme6/openclaw-gateway-guardian.git
```

### 3. 推送代码

```bash
git branch -M main
git push -u origin main
```

### 4. 验证

访问：https://github.com/davidme6/openclaw-gateway-guardian

---

## 方法三：使用 GitHub Desktop

### 1. 安装 GitHub Desktop

下载：https://desktop.github.com/

### 2. 添加本地仓库

1. 打开 GitHub Desktop
2. File → Add Local Repository
3. 选择：`C:\Windows\System32\UsersAdministrator.openclawworkspace\github\davidme6\openclaw-gateway-guardian`
4. 点击 "Add repository"

### 3. 发布到 GitHub

1. File → Publish repository
2. 名称：`openclaw-gateway-guardian`
3. 描述：`OpenClaw Gateway Guardian - 网关守护神`
4. 勾选 "Keep this code private"（如果需要私有）
5. 点击 "Publish repository"

---

## ✅ 验证上传

上传成功后，访问：
https://github.com/davidme6/openclaw-gateway-guardian

应该能看到：
- ✅ README.md
- ✅ SKILL.md
- ✅ requirements.txt
- ✅ scripts/gateway_guardian.py

---

## 📝 后续更新

```bash
# 修改代码后
git add .
git commit -m "fix: 修复 XXX 问题"
git push
```

---

## 🎉 完成！

上传成功后，其他人就可以通过以下方式使用：

```bash
git clone https://github.com/davidme6/openclaw-gateway-guardian.git
cd openclaw-gateway-guardian
pip install -r requirements.txt
python scripts/gateway_guardian.py init
python scripts/gateway_guardian.py start
```
