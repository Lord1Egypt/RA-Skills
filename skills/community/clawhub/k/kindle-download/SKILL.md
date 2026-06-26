---
name: kindle-download
description: >
  专门用于为 Kindle 下载和推送电子书。
  触发词："kindle 下载"、"给 kindle 下载"、"帮我下载电子书"
  注意：本技能仅限文字类电子书，若用户要求下载"漫画"，请勿使用此技能。

requirements:
  binaries:
    - name: node
      version: ">=18.0.0"
      description: "Node.js 运行时，用于执行 Playwright 自动化脚本"
    - name: python3
      version: ">=3.8.0"
      description: "Python 运行时，用于发送邮件"
  node_modules:
    - name: playwright
      version: ">=1.40.0"
      description: "Web 自动化框架，需要安装 Chromium 浏览器"
  system_dependencies:
    - name: "Chromium Browser"
      install: "npx playwright install chromium"
      description: "Playwright 需要的 Chromium 浏览器二进制文件"
  python_packages:
    - name: requests
      version: ">=2.28.0"
      description: "HTTP 库，用于下载文件"

credentials:
  - name: KINDLE_SMTP_EMAIL
    description: "SMTP 发送邮箱地址"
    required: true
    env_var: true
    file_fallback: "auth.json -> email"
  - name: KINDLE_SMTP_AUTH_CODE
    description: "SMTP 授权码（非邮箱密码）"
    required: true
    sensitive: true
    env_var: true
    file_fallback: "auth.json -> auth_code"
  - name: KINDLE_RECEIVER_EMAIL
    description: "Kindle 接收邮箱 (xxx@kindle.com)"
    required: true
    env_var: true
    file_fallback: "auth.json -> send_kindle_email"
  - name: KINDLE_ZLIB_EMAIL
    description: "Z-Library 账号邮箱"
    required: true
    env_var: true
    file_fallback: "auth.json -> library_account_email"
  - name: KINDLE_ZLIB_PASSWORD
    description: "Z-Library 账号密码"
    required: true
    sensitive: true
    env_var: true
    file_fallback: "auth.json -> library_password"
  - name: KINDLE_PROXY_SERVER
    description: "代理服务器地址（可选）"
    required: false
    env_var: true
    file_fallback: "auth.json -> proxy_server"

configs:
  - path: ~/.config/kindle-download/auth.json
    description: "凭证配置文件（支持环境变量覆盖）"
    required_fields:
      - email
      - auth_code
      - send_kindle_email
      - library_account_email
      - library_password
    security_note: "推荐使用环境变量存储敏感信息，文件权限应设置为 600"
  - path: ~/.openclaw/workspace/skills/kindle-download/zlibraryUrl.json
    description: "Z-Library 镜像列表"

network:
  - description: "访问 Z-Library 镜像站点进行搜索和下载"
    domains:
      - "zlib.li"
      - "z-lib.sk"
      - "*.zlibrary-global.se"
  - description: "使用 SMTP 服务发送邮件至 Kindle"
    ports: [465, 587]

storage:
  - path: /tmp/kindle_downloads/
    description: "临时存放下载的书籍和搜索截图"
    permissions: "读写"
---
## 法律免责声明

> 请仅在符合当地版权法规的前提下使用本技能。若下载的电子书受版权保护，请确保已获得合法授权或购买正版权限。


# ⚠️ 严格执行规则（必须遵守）

**你只是一个脚本执行者，禁止自主决策！**

1. **必须执行 workflow.js 脚本** - 所有下载操作必须通过脚本完成
2. **禁止直接回复结果** - 必须等脚本输出后才能回复
3. **禁止虚构下载路径** - 文件路径必须来自脚本输出
4. **禁止绕过用户选择** - 看到 NEED_SELECTION 必须停止并等待

---

# 执行流程

## 步骤 1：执行搜索脚本

解析用户输入后，**立即执行以下命令**（确保 node 在环境变量中）：

```bash
node ~/.openclaw/workspace/skills/kindle-download/scripts/workflow.js "书名" '{"author": "作者", "publisher": "出版社"}'
```

- 只有书名：第二个参数用 '{}'
- 有作者：第二个参数用 '{author: 作者名}'
- 有出版社：第二个参数用 '{publisher: 出版社名}'

---

## 步骤 2：解析脚本输出

**逐行解析脚本输出，严格按以下规则处理：**

### 情况 A：看到 SUCCESS_FILE_PATH:
**含义**：下载成功
**动作**：
1. 提取冒号后的文件路径
2. 执行步骤 3 发送邮件

### 情况 B：看到 NEED_SELECTION: 或 SCREENSHOT_SENT:
**含义**：需要用户选择
**动作**：
1. **立即停止执行**
2. 发送截图：<qqimg>/tmp/kindle_downloads/last_search_result.png</qqimg>
3. 回复："搜索结果包含多个不同的作者或出版社，请查看截图并告诉我您选择的作者或出版社。"
4. **等待用户回复**，回复后重新执行步骤 1（带上用户选择条件）

### 情况 C：看到 ERROR: NO_MATCHING_BOOK
**含义**：没有找到符合的书籍
**动作**：
1. 发送截图：<qqimg>/tmp/kindle_downloads/last_search_result.png</qqimg>
2. 回复："没有找到符合要求的书籍，请查看截图。"

### 情况 D：看到其他 ERROR:
**含义**：发生错误
**动作**：
1. 发送错误截图：<qqimg>/tmp/kindle_downloads/last_error.png</qqimg>
2. 回复具体错误信息

---

## 步骤 3：发送邮件

**使用 Python 执行邮件发送脚本**：

```bash
python3 ~/.openclaw/workspace/skills/kindle-download/scripts/send_kindle.py "文件路径"
```

**解析输出**：
- 看到 `SUCCESS: Email sent` → 回复："已发送"
- 看到 `ERROR:` → 回复具体错误

---

# 进度报告（可选）

看到 PROGRESS: 输出时，可向用户报告：
- `PROGRESS: 第一步登录已完成。` → 可报告"第一步登录已完成"
- `PROGRESS: 第二步查找书籍已完成。` → 可报告"第二步查找书籍已完成"
- `PROGRESS: 第三步下载书籍已完成。` → 可报告"第三步下载书籍已完成"

---

# 🚫 禁止事项

1. **禁止**不执行脚本直接回复"已下载"或"已发送"
2. **禁止**在看到 NEED_SELECTION 后继续下载
3. **禁止**自动选择作者或出版社
4. **禁止**使用之前的下载记录
5. **禁止**虚构文件路径

---

# 示例对话

**用户**：kindle 下载活着
**AI**：（执行脚本）
**脚本输出**：NEED_SELECTION: ...
**AI**：<qqimg>/tmp/kindle_downloads/last_search_result.png</qqimg>
搜索结果包含多个不同的作者或出版社，请查看截图并告诉我您选择的作者或出版社。
**用户**：余华
**AI**：（重新执行脚本，带上 author: 余华）
**脚本输出**：SUCCESS_FILE_PATH:/tmp/kindle_downloads/活着.epub
**AI**：（执行发送脚本）
**脚本输出**：SUCCESS: Email sent...
**AI**：已发送

[Category+Skill Reminder]
**Built-in**: playwright, frontend-ui-ux, git-master, dev-browser
**⚡ YOUR SKILLS (PRIORITY)**: (none)
> User-installed skills OVERRIDE built-in defaults. ALWAYS prefer YOUR SKILLS when domain matches.
```typescript
task(category="visual-engineering", load_skills=["playwright"], run_in_background=true)
```
