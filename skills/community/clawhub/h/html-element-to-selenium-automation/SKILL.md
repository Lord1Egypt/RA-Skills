---
name: html-to-selenium
description: 将任意网页转换为可运行的 Python Selenium 自动化脚本. 使用场景: (1) 分析网页结构并生成自动化代码; (2) 帮用户完成指定网页操作 (登录、填表、点击、搜索等); (3) 生成 Selenium 脚本骨架. 当用户提到"分析页面"、"生成 selenium"、"网页自动化"、"帮我操作 xxx"、"帮我完成 xxx"时触发.
---

# html-to-selenium

## 概述

接收 URL → 通过 Playwright 获取截图 + HTML DOM → AI 分析页面类型与结构 → 输出:
1. 页面结构描述 + 操作逻辑
2. 关键信息提取 (表单 action、API endpoint、session 状态)
3. **完整可运行的 Python Selenium 代码**
4. **操作步骤示例** (每个有效操作的定位方式 + Selenium 方法 + 执行结果)

## 工作流程

```
用户提供 URL
      │
      ▼
  Step 1: 抓取页面
  ┌──────────────────────────────────────┐
  │  fetch_page.py                       │
  │  - Playwright 打开 URL               │
  │  - 等待页面渲染完成                   │
  │  - 全页截图 + 完整 HTML DOM           │
  │  - 输出: screenshot.png, html.html    │
  └──────────────┬───────────────────────┘
                 │
                 ▼
  Step 2: AI 判断页面类型
  ┌──────────────────────────────────────┐
  │  输入: 截图 + HTML + URL + title     │
  │                                      │
  │  A. 目标页 = 登录页                   │
  │     → 直接分析登录表单结构             │
  │     (作为分析任务本身, 不触发登录)      │
  │                                      │
  │  B. 中途被重定向到登录页               │
  │     → AI 输出: 登录逻辑 + 凭据需求     │
  │     → 等待用户提供凭据                 │
  │     → 执行登录 → 返回目标页            │
  │     → 继续分析                        │
  │                                      │
  │  C. 公开页面 (无需登录)               │
  │     → 直接进入分析流程                 │
  └──────────────┬───────────────────────┘
                 │
                 ▼
  Step 3: 生成输出
  ┌──────────────────────────────────────┐
  │  页面结构描述                          │
  │  操作逻辑 (点击链、表单提交、AJAX)      │
  │  有用信息 (API、URL 参数、session)     │
  │  Python Selenium 代码                 │
  │  操作步骤示例 (每个有效操作详细记录)    │
  └──────────────────────────────────────┘
```

## Step 1 — 抓取页面

```bash
python scripts/fetch_page.py <url> --output <目录> --wait <秒>
```

- `--output`: 保存目录, 默认当前目录. 建议用有意义的名字如 `temp/example_com`
- `--wait`: 页面加载后等待秒数, 默认 3. 动态页面可调大 (5-8)
- `--login / -l`: 检测到登录页时尝试自动登录
- `--username / -u` + `--password / -p`: 登录凭据 (如需要)

**输出文件:**
- `screenshot.png` — 全页截图
- `screenshot_viewport.png` — 视口截图
- `html.html` — 渲染后的完整 HTML DOM
- `meta.json` — 页面元信息 (URL、title、元素计数、page_type)

**重要:** 必须等页面完全渲染后再抓取 HTML (`wait_until="networkidle"` + 额外等待), 否则拿到的可能是空的半加载状态.

## Step 2 — AI 页面类型判断

接收以下信息, 综合判断:

| 输入 | 用途 |
|------|------|
| `screenshot.png` | 视觉判断: 纯登录页 / 登录弹窗覆盖 / 正常内容页 |
| `html.html` | DOM 判断: 表单数量、input 类型、class/id 特征 |
| `meta.json` | URL 变化: 访问前后 URL 是否一致 |
| `title` | 辅助判断: 页面标题关键词 |

### 页面类型判断标准

**A. 目标页 = 登录页 (page_type = "login_required", 且 URL 本身含 login/signin/auth)**
- 处理: 把登录表单本身作为分析对象, 不触发自动登录
- 分析重点: 用户名/密码字段特征、记住登录、多因素认证、表单 action

**B. 中途被重定向到登录页 (page_type = "login_required", 但 URL 不是登录页)**
- 处理: AI 输出"需要登录"提示 + 需要的凭据说明, 等待用户或上级 Agent 提供
- 提供凭据后: 读取 `selenium-patterns.md` 执行真实点击登录 → 等待回到目标页 → 继续

**C. 公开页面 (page_type = "public")**
- 处理: 直接进入分析流程

### 登录流程 (情况 B)

当需要登录时, 使用 `selenium-patterns.md` 中的规范:

```python
# 填入用户名
username = driver.find_element(By.NAME, "username")  # 或其他定位
username.click()
username.send_keys(Keys.CONTROL + "a")
username.send_keys(Keys.DELETE)
username.send_keys(credentials["username"])

# 填入密码
password = driver.find_element(By.NAME, "password")
password.click()
password.send_keys(Keys.CONTROL + "a")
password.send_keys(Keys.DELETE)
password.send_keys(credentials["password"])

# 点击登录 (真实用户点击, 禁止 JS click)
submit = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
)
ActionChains(driver).move_to_element(submit).click().perform()

# 等待回到目标页
WebDriverWait(driver, 15).until(
    lambda d: "/login" not in d.current_url
)
```

## Step 3 — 输出内容

### 3.1 页面结构描述

用自然语言描述页面组成:
- 语义分区 (顶部导航 / 侧边栏 / 主内容区 / 底部)
- 关键元素位置与作用
- 表单结构 (有哪些字段、必填项)

### 3.2 操作逻辑

描述操作流程:
- 点击链: 哪个按钮 → 哪个页面/弹窗
- 表单提交流程: 哪个按钮提交, 如何验证
- AJAX/动态行为: 哪些操作触发异步请求

### 3.3 关键信息提取

```python
# 示例
INFO = {
    "表单 action": "https://example.com/api/submit",
    "API endpoint": "https://example.com/api/users/search",
    # Session 状态: 仅当页面 DOM 显式暴露时提取，fetch_page.py 不主动提取或传输
    "Session Token": "xxx (DOM 可见时提取, 非自动行为)",
    "关键元素": {
        "用户名": "#username (id)",
        "密码": "#password (id)",
        "提交": "button[type=submit] (xpath text='登录')",
    },
    "URL 参数": "?redirect=/dashboard",
}
```

### 3.4 Python Selenium 代码

**必须遵循 `references/selenium-patterns.md` 中的规范**, 重点:

- **真实用户点击:** `ActionChains.move_to_element().click()`, 禁止 `execute_script("click")`
- **显式等待:** `WebDriverWait` + `expected_conditions`, 禁止 `time.sleep()` 作为主要方式
- **安全输入:** `click()` → `Ctrl+A` → `Delete` → `send_keys()`
- **截图对比:** 关键步骤前后截图保存

### 3.5 操作步骤示例 (必须输出)

每个有效操作必须记录为以下格式的步骤, 复杂操作拆分为 1、2、3...:

```python
# ✅ 操作1: [操作名称]
# 定位: [定位方式] → [具体选择器]
# 方法: [Selenium 调用链]
# 结果: [执行后的页面状态描述]

# 示例:
# ✅ 操作1: 点击左侧导航"用户管理"
# 定位: CSS selector → ".sidebar .nav-item[data-tab='users']"
# 方法: ActionChains.move_to_element().click()
# 结果: 页面加载用户管理视图, URL 变为 /admin/users

# ✅ 操作2: 在搜索框输入关键词
# 定位: XPath → "//input[@placeholder='搜索...']"
# 2.1: 点击聚焦 → click()
# 2.2: 清空内容 → send_keys(Keys.CONTROL+"a") → send_keys(Keys.DELETE)
# 2.3: 输入文本 → send_keys("admin")
# 结果: 输入框显示"admin", 触发前端搜索过滤

# ✅ 操作3: 点击搜索结果中的"编辑"按钮
# 定位: partial link text → "//button[contains(text(),'编辑')]"
# 方法: ActionChains.move_to_element().click()
# 结果: 弹出编辑弹窗, 截图已保存
```

## 快速参考

### 触发方式

用户说这些关键词时加载本 skill:
- "分析页面"
- "生成 selenium"
- "网页自动化"
- "帮我操作 xxx 页面"
- "帮我完成 xxx"
- "做个 xxx 的自动化"
- 提供 URL 并要求生成自动化代码

### 文件路径 (skill 内部)

| 文件 | 用途 | 何时读取 |
|------|------|---------|
| `scripts/fetch_page.py` | 页面抓取 (截图 + HTML) | Step 1 |
| `references/selenium-patterns.md` | Selenium 规范与代码片段 | 生成代码时 |
| `references/examples.md` | 操作步骤示例模板 | 生成示例时 |
| `SKILL.md` | 主工作流说明 | 触发时 |

### 快速命令模板

```bash
# 抓取公开页面
python scripts/fetch_page.py https://example.com/page --output temp/example

# 抓取并自动登录 (如遇登录拦截)
python scripts/fetch_page.py https://example.com/protected \
    --output temp/example \
    --login \
    --username "user@email.com" \
    --password "password123"
```

### 重要限制

- 凭据不在对话中硬编码. 情况 B 登录时, 凭据必须由用户或上层 Agent 在对话中提供
- 不处理复杂验证码 (滑块/点选/文字). 如遇验证码, 输出提示并等待人工介入
- 不处理 MFA (短信/APP 验证码). 同样输出提示等待介入
