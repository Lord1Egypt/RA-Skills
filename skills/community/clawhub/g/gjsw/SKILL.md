---
name: gjsw
description: 国家税务总局 12366 纳税服务平台自动登录技能。支持图形验证码 OCR 识别、持久化会话、自动定位表单元素。当用户要求登录税务平台、12366、国家税务总局、国家税务局12366 、12366国家税务局 等登录场景时触发。关键判断：用户提供用户名、密码以及登录页面 URL（或已设置环境变量），希望自动完成登录流程。
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires":
          {
            "bins": ["python3", "google-chrome"]
          },
        "primaryEnv": "GJSW_LOGIN_URL"
      }
  }
---

# 国家税务总局 12366 自动登录

通过 `openclaw_login.py` 脚本，使用 Playwright 控制 Google Chrome 浏览器，自动填写账号、密码、识别图形验证码并提交登录。支持会话持久化（复用 Chrome 用户数据目录），下次运行可保持登录状态。

## 功能

1. **自动定位表单元素** - 智能识别用户名框、密码框、验证码图片、验证码输入框和登录按钮
2. **图形验证码 OCR** - 使用 ddddocr 识别验证码（自动过滤非数字字符）
3. **登录重试机制** - 最多重试 5 次，验证码错误会自动刷新重试，账号密码错误则立即停止
4. **持久化会话** - 使用独立 Chrome 用户数据目录 `./chrome_profile`，保存 Cookies 和登录态
5. **远程调试端口复用** - 固定使用端口 9222，多次运行可连接同一浏览器实例
6. **登录成功检测** - 通过 URL 跳转、页面关键词（个人中心、退出）和认证 Cookie 综合判断

## 前置要求

### 1. 安装依赖
```bash
pip install playwright ddddocr
playwright install chrome   # 安装 Playwright 浏览器内核（脚本实际使用 Chrome）
```
### 2. 安装 Google Chrome
* Windows / macOS / Linux 均需安装 Chrome 浏览器，并确保在 PATH 中
* 脚本会自动查找常见安装路径（如 macOS 的 /Applications/Google Chrome.app）
### 2. 设置环境变量（可选）
```bash
export GJSW_LOGIN_URL="https://12366.chinatax.gov.cn/login"   # Linux/macOS
# 或 Windows (CMD)
set GJSW_LOGIN_URL=https://12366.chinatax.gov.cn/login
```
* 如果未设置环境变量，每次运行时必须通过 --url 参数提供登录页 URL。

##  使用方法

### 基本命令
```bash
python3 {baseDir}/openclaw_login.py <用户名> <密码> [--url <登录页URL>] [--debug] [--window-size WIDTH,HEIGHT]
```
### 参数说明
| 参数 |说明|必填|
| --- | --- | --- | 
| 用户名 |登录账号| 是 |
| 密码 |登录密码| 是 |
| --url|登录页面的完整 URL（未提供则读取环境变量 GJSW_LOGIN_URL）|否 |
| --debug|开启调试模式，打印元素定位和识别过程|否 |
| --window-size|浏览器窗口大小，格式 宽度,高度，默认 1280,800|否 |
### 示例
```bash
# 使用命令行 URL
python3 openclaw_login.py myusername mypassword --url "https://12366.chinatax.gov.cn/usercenter/login/page"

# 使用环境变量中的 URL
python3 openclaw_login.py myusername mypassword

# 调试模式 + 大窗口
python3 openclaw_login.py myusername mypassword --debug --window-size 1920,1080
```