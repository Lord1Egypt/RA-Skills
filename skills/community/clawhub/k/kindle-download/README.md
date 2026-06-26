# Kindle Download Skill

<p align="center">
  <strong>一个用于 OpenClaw 的 Kindle 电子书下载技能</strong>
</p>

<p align="center">
  自动从 Z-Library 搜索、下载电子书，并发送到你的 Kindle 设备
</p>

---

## ✨ 功能特性

- 🔍 **智能搜索**：支持按书名、作者、出版社、语言进行精准搜索
- 🔄 **自动镜像切换**：当某个镜像站不可用时，自动尝试下一个
- 💾 **登录态保存**：保存浏览器登录状态，避免重复登录
- 🖼️ **交互式选择**：当搜索结果有多个版本时，发送截图供用户选择
- 📧 **自动发送**：下载完成后自动通过邮件发送到 Kindle
- 📊 **进度报告**：实时报告每个步骤的执行进度
- 🖥️ **跨平台兼容**：支持 Linux、macOS、Windows
- 🔐 **安全配置**：敏感凭证存储在用户配置目录，不包含在技能目录中

---

## 📋 前置要求

> ⚠️ **重要**：本技能需要在**运行 OpenClaw 的服务器上**安装以下依赖。

### 1. OpenClaw 环境

本项目是一个 OpenClaw 的 Skill，需要先安装 OpenClaw。

### 2. Node.js 和 Playwright

需要在服务器上安装 Node.js (v18+) 和 Playwright。

**请系统管理员安装以下依赖：**
- Node.js (推荐 v18+)
- Playwright Chromium 浏览器

### 3. Python

需要 Python 3 用于发送邮件（大多数 Linux 系统已预装）。

### 4. Z-Library 账号

需要一个 Z-Library 账号用于登录下载。可以在 [Z-Library](https://zlibrary-global.se/) 注册。

### 5. Kindle 邮箱设置

1. 登录 [Amazon 账户](https://www.amazon.com/myk)
2. 在"设置" -> "个人文档设置"中添加你的发送邮箱
3. 记下你的 Kindle 邮箱地址（格式：`yourname@kindle.com`）

---

## 🚀 安装

将本项目复制到 OpenClaw 的 skills 目录：

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/xiehaixin/kindle-download.git
```

---

## ⚙️ 配置

### 1. 创建配置目录并配置 auth.json

配置文件存储在用户主目录下，不包含在技能目录中，提高了安全性。

```bash
mkdir -p ~/.config/kindle-download
cp ~/.openclaw/workspace/skills/kindle-download/auth.json.example ~/.config/kindle-download/auth.json
```

编辑 `~/.config/kindle-download/auth.json` 文件：

```json
{
  "email": "your_email@163.com",
  "auth_code": "your_smtp_authorization_code",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "send_kindle_email": "yourname@kindle.com",
  "library_account_email": "your_zlibrary_email@example.com",
  "library_password": "your_zlibrary_password",
  "proxy_server": ""
}
```

#### 配置项说明

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `email` | 用于将下载到本地的电子书自动发送到kindle接收邮箱的邮箱 | ✅ |
| `auth_code` | SMTP 授权码（email的SMTP授权码，不是邮箱密码） | ✅ |
| `smtp_server` | SMTP 服务器地址（例：smtp.qq.com） | ✅ |
| `smtp_port` | SMTP 服务器端口 （例如：465）| ✅ |
| `send_kindle_email` | Kindle 接收电子书的邮箱（`xxx@kindle.com`） | ✅ |
| `library_account_email` | Z-Library 注册的账号邮箱（只存本地，自己填入，用于自动登录Z-Library下载电子书） | ✅ |
| `library_password` | Z-Library 注册的账号密码（只存本地，自己填入） | ✅ |
| `proxy_server` | 代理服务器地址（如需要） | ❌ |

#### 常用邮箱 SMTP 配置

| 邮箱 | SMTP 服务器 | 端口 |
|------|-------------|------|
| 163 邮箱 | smtp.163.com | 465 |
| QQ 邮箱 | smtp.qq.com | 465 |
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp.office365.com | 587 |

### 2. 配置镜像站（可选）

默认已配置多个 Z-Library 镜像站，可在技能目录下的 `zlibraryUrl.json` 中修改。

### 3. 配置代理（可选）

如果服务器无法直接访问 Z-Library，在 `auth.json` 中配置代理：

```json
{
  "proxy_server": "http://127.0.0.1:7890"
}
```

---

## 📖 使用方法

### 在 OpenClaw 中使用

安装并配置后，在 OpenClaw 中可以使用以下指令：

#### 基本用法

```
kindle 下载 三体
```

#### 指定作者

```
kindle 下载 三体，作者刘慈欣
```

#### 指定出版社

```
kindle 下载 三体，重庆出版社
```

#### 组合条件

```
kindle 下载 三体，作者刘慈欣，出版社重庆出版社
```

### 交互式选择

当搜索结果有多个不同版本时，系统会发送截图让你选择：

```
AI: 搜索结果包含多个不同的作者或出版社，请查看截图并告诉我您选择的作者或出版社。
<截图>

你: 我选择机械工业出版社

AI: 第一步登录已完成。
第二步查找书籍已完成。
第三步下载书籍已完成。
第四步发送已完成。已发送
```

---

## 📁 项目结构

```
kindle-download/
├── README.md           # 项目说明文档
├── SKILL.md            # OpenClaw Skill 定义文件
├── auth.json.example   # 配置文件示例
├── zlibraryUrl.json    # Z-Library 镜像站列表
└── scripts/
    ├── workflow.js     # 主要下载流程脚本
    ├── send_kindle.py  # 邮件发送脚本
    └── download_book.py # HTTP 下载脚本
```

> 注意：`auth.json` 存储在 `~/.config/kindle-download/` 目录下，不包含在项目中，提高了安全性。

---

## 🖥️ 跨平台兼容性

本项目支持以下平台：

| 平台 | 支持 | 备注 |
|------|------|------|
| Linux | ✅ | 主要测试平台 |
| macOS | ✅ | 需要 Intel 或 Apple Silicon |
| Windows | ✅ | 需要 WSL 或 Git Bash |

### 自动检测

- **Chromium 浏览器**：脚本会自动检测系统中的 Chromium/Chrome 浏览器
- **下载目录**：使用系统临时目录（Linux: `/tmp`，macOS: `/tmp`，Windows: `%TEMP%`）
- **Node.js**：使用系统 PATH 中的 `node` 命令

---

## 🔄 工作流程

```
┌─────────────────┐
│  用户发起请求    │
└────────┬────────┘
         ▼
┌─────────────────┐
│  第一步：登录    │
│   Z-Library     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  第二步：查找    │
│   搜索书籍      │
└────────┬────────┘
         ▼
┌─────────────────┐
│  第三步：下载    │
│   获取电子书    │
└────────┬────────┘
         ▼
┌─────────────────┐
│  第四步：发送    │
│  发送到 Kindle  │
└─────────────────┘
```

> 如果搜索结果有多个版本，会在第二步后暂停，等待用户选择。

---

## ⚠️ 注意事项

1. **仅限个人学习使用**：请尊重版权，下载的电子书仅供个人学习使用
2. **不支持漫画**：本技能仅支持文字类电子书，漫画类请勿使用
3. **邮箱白名单**：确保发送邮箱已添加到 Kindle 的认可发件人列表
4. **网络环境**：如果无法访问 Z-Library，请配置代理
5. **配置安全**：敏感凭证存储在 `~/.config/kindle-download/` 目录，请妥善保管

---

## 🛠️ 故障排除

### 找不到书籍
- 检查书名是否正确
- 尝试只使用书名搜索，不要带作者
- 查看截图确认搜索结果

### 发送失败
- 检查 `~/.config/kindle-download/auth.json` 配置是否正确
- 确认 SMTP 授权码有效（不是邮箱密码）
- 确认发送邮箱已添加到 Kindle 白名单

### 登录失败
- 检查 Z-Library 账号密码是否正确
- 尝试手动登录 Z-Library 确认账号状态

### 找不到 node 命令
- 确保 Node.js 已正确安装
- 检查 PATH 环境变量是否包含 Node.js 路径

### Chromium 找不到
请联系系统管理员安装 Playwright Chromium 浏览器。

---

## 📄 许可证

本项目仅供学习和研究使用。使用本项目下载的电子书请遵守相关版权法律。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📧 联系方式

如有问题，请提交 [Issue](https://github.com/xiehaixin/kindle-download/issues)。
