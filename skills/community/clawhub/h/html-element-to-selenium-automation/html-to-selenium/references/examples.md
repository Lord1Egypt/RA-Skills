# 操作步骤与 Selenium 方法示例

本文件记录每个有效操作的关键步骤及对应的 Selenium 方法, 作为代码生成的参考模板.

---

## 示例一: 公开页面 → 点击导航 → 搜索 → 查看详情

**场景:** 打开后台管理页面, 在左侧导航找到"用户管理", 在搜索框输入用户名"admin", 点击搜索, 再点击结果行的"查看"按钮.

### Step 1: 打开页面

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

driver = create_driver()
driver.get("https://example.com/admin/users")
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "user-table"))
)
```

**操作步骤记录:**
- 定位: `id="user-table"` — 通过 ID 确认页面已加载
- 方法: `driver.get()` → `WebDriverWait(...).until(EC.presence_of_element_located(...))`
- 结果: 页面加载成功, 表格元素已出现

### Step 2: 点击导航"用户管理"

```python
def real_click(driver, locator, timeout=10):
    if isinstance(locator, tuple):
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    else:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
    ActionChains(driver).move_to_element(element).click().perform()
    return element

# 展开导航菜单 (如有 hover 子菜单)
nav = driver.find_element(By.CSS_SELECTOR, ".sidebar-nav .nav-users")
ActionChains(driver).move_to_element(nav).pause(0.5).perform()

# 点击导航项
real_click(driver, ".sidebar-nav .nav-users a")
```

**操作步骤记录 (拆分):**
- 2.1: 定位侧边栏导航 → CSS selector → `.sidebar-nav .nav-users`
  - 方法: `ActionChains.move_to_element().pause()` 悬停展开子菜单
  - 结果: 子菜单已展开, 显示"用户管理"链接
- 2.2: 定位导航链接 → CSS selector → `.sidebar-nav .nav-users a`
  - 方法: `ActionChains.move_to_element().click()` 真实用户点击
  - 结果: 页面跳转到用户管理页, URL 变化

### Step 3: 在搜索框输入用户名

```python
from selenium.webdriver.common.keys import Keys

search_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='搜索用户名']"))
)
search_input.click()
search_input.send_keys(Keys.CONTROL + "a")
search_input.send_keys(Keys.DELETE)
search_input.send_keys("admin")
```

**操作步骤记录 (拆分):**
- 3.1: 定位搜索框 → CSS selector (placeholder 属性) → `input[placeholder='搜索用户名']`
  - 方法: `WebDriverWait(...).until(EC.element_to_be_clickable(...))` 等待可交互
  - 结果: 元素可交互状态
- 3.2: 聚焦并清空 → 发送 `Ctrl+A` → `Delete`
  - 方法: `.click()` → `.send_keys(Keys.CONTROL+"a")` → `.send_keys(Keys.DELETE)`
  - 结果: 输入框已清空
- 3.3: 输入搜索词 → `send_keys("admin")`
  - 方法: 直接 send_keys
  - 结果: "admin" 已填入, 触发前端搜索事件

### Step 4: 点击搜索按钮

```python
real_click(driver, (By.XPATH, "//button[contains(text(),'搜索')]"))
```

**操作步骤记录:**
- 定位: XPath 文本包含 → `//button[contains(text(),'搜索')]`
- 方法: `ActionChains.move_to_element().click()` 真实点击
- 结果: 列表刷新, 显示匹配"admin"的结果

### Step 5: 点击搜索结果中的"查看"按钮

```python
# 等待搜索结果加载
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".user-table tbody tr"))
)

# 点击第一行的"查看"按钮
first_row = driver.find_element(By.CSS_SELECTOR, ".user-table tbody tr:first-child")
view_btn = first_row.find_element(By.XPATH, ".//button[contains(text(),'查看')]")
real_click(driver, view_btn)
```

**操作步骤记录 (拆分):**
- 5.1: 等待搜索结果 → CSS selector → `.user-table tbody tr`
  - 方法: `WebDriverWait(...).until(EC.visibility_of_element_located(...))`
  - 结果: 至少一条结果出现
- 5.2: 定位第一行的查看按钮 → XPath 相对路径 → `.//button[contains(text(),'查看')]`
  - 方法: 从第一行元素内查找 → `ActionChains.move_to_element().click()`
  - 结果: 弹出详情弹窗或跳转到详情页

### Step 6: 截图保存 (before/after 对比)

```python
import os
from datetime import datetime

def screenshot(driver, name):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("screenshots", f"{name}_{ts}.png")
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(path)
    return path

screenshot(driver, "step5_after_view_click")
```

---

## 示例二: 登录拦截页面 → 自动登录 → 执行后续操作

**场景:** 访问 `https://example.com/dashboard`, 被重定向到登录页, 提供凭据登录后, 返回目标页继续操作.

### Step 1: 访问目标页 + AI 判断页面类型

(由 fetch_page.py 或 Playwright 完成后, AI 收到截图+HTML+URL 判定为"中途拦截登录页")

### Step 2: 填入登录表单

```python
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
username_field.click()
username_field.send_keys(Keys.CONTROL + "a")
username_field.send_keys(Keys.DELETE)
username_field.send_keys("admin@example.com")

password_field = driver.find_element(By.NAME, "password")
password_field.click()
password_field.send_keys(Keys.CONTROL + "a")
password_field.send_keys(Keys.DELETE)
password_field.send_keys("YourPassword123")
```

**操作步骤记录 (拆分):**
- 2.1: 定位用户名输入框 → name 属性 → `name="username"`
  - 方法: `WebDriverWait(...).until(EC.presence_of_element_located(...))` → `.click()` → `send_keys`
  - 结果: 用户名已填入
- 2.2: 定位密码输入框 → name 属性 → `name="password"`
  - 方法: 同上
  - 结果: 密码已填入

### Step 3: 点击登录按钮

```python
submit_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(),'登录')]"))
)
ActionChains(driver).move_to_element(submit_btn).click().perform()
```

**操作步骤记录:**
- 定位: XPath 组合条件 → `@type="submit"` + 文本包含"登录"
- 方法: `ActionChains.move_to_element().click()` 真实点击
- 结果: 登录请求发送, 页面跳转

### Step 4: 等待返回目标页

```python
# 等待 URL 变为目标页 (不再是 /login)
WebDriverWait(driver, 15).until(
    lambda d: "/login" not in d.current_url and "/dashboard" in d.current_url
)

# 或等待关键元素出现
WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.ID, "dashboard-content"))
)
```

**操作步骤记录:**
- 判断: URL 从 `/login` 变为 `/dashboard`, 确认登录成功
- 方法: `WebDriverWait(lambda d: ...)`.until
- 结果: 到达目标页面, 继续执行后续操作

---

## 示例三: 带下拉框 + 弹窗 + iframe 的复杂表单

### Step 3.1: 下拉框选择

```python
from selenium.webdriver.support.ui import Select

dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "category"))
)
Select(dropdown).select_by_visible_text("技术文档")
# 或按值选择
Select(dropdown).select_by_value("tech-docs")
```

**操作步骤记录:**
- 定位: name 属性 → `name="category"`
- 方法: `Select(...).select_by_visible_text("技术文档")`
- 结果: 下拉框选中"技术文档", 触发 onChange 事件

### Step 3.2: 填写富文本编辑器 (iframe 内)

```python
# 切换到富文本 iframe
iframe = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#editor_iframe"))
)
driver.switch_to.frame(iframe)

# 在 iframe 内输入
editor_body = driver.find_element(By.CSS_SELECTOR, "body")
editor_body.click()
editor_body.send_keys("这是文档内容。")

# 切回主文档
driver.switch_to.default_content()
```

**操作步骤记录 (拆分):**
- 3.2.1: 切换到 iframe → CSS selector → `#editor_iframe`
  - 方法: `WebDriverWait(...).until(EC.frame_to_be_available_and_switch_to_it(...))`
  - 结果: 已进入 iframe 上下文
- 3.2.2: 定位编辑器 body → CSS selector → `body`
  - 方法: `.click()` → `.send_keys(...)`
  - 结果: 内容已输入
- 3.2.3: 切回主文档 → `driver.switch_to.default_content()`
  - 结果: 已切回主文档, 可继续操作主文档元素

### Step 3.3: 点击确认按钮提交表单

```python
real_click(driver, (By.XPATH, "//button[contains(@class,'btn-submit')]"))
```

**操作步骤记录:**
- 定位: XPath + class 包含 → `//button[contains(@class,'btn-submit')]`
- 方法: `real_click()` — ActionChains 真实点击
- 结果: 表单提交, 服务器响应

### Step 3.4: 处理成功/失败弹窗

```python
# 等待成功提示出现
try:
    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".toast-success"))
    )
    print(f"操作成功: {success_msg.text}")
except Exception:
    # 检查是否有错误弹窗
    error_msg = driver.find_element(By.CSS_SELECTOR, ".toast-error")
    print(f"操作失败: {error_msg.text}")
```

**操作步骤记录:**
- 判断成功: CSS selector → `.toast-success` 可见
- 判断失败: CSS selector → `.toast-error` 可见
- 结果: 根据弹窗内容确认操作结果
