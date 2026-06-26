# Selenium 最佳实践

所有生成的 Selenium 代码必须遵循以下规范.

## 1. 真实用户点击（硬性要求）

**禁止使用 `driver.execute_script("arguments[0].click()")` 或 JS 注入方式模拟点击.**  
JS 点击不触发真实 DOM 事件 (mouseenter/mouseleave/hover 状态), 部分站点会检测并拒绝.

**正确方式: ActionChains + 可点击状态检测**

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def real_click(driver, locator, timeout=10):
    """
    模拟真实用户点击: 等待元素可点击 → hover → 点击.
    支持 tuple (By.ID, "id") 或 CSS selector 字符串.
    """
    if isinstance(locator, tuple):
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    else:
        # CSS selector
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, locator))
        )
    ActionChains(driver).move_to_element(element).click().perform()
    return element

def real_click_by_text(driver, text, timeout=10):
    """通过文本内容点击 (模糊匹配)."""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(),'{text}')]"))
    )
    ActionChains(driver).move_to_element(element).click().perform()
    return element
```

**场景化点击:**

```python
# 悬停后出现的菜单项
from selenium.webdriver.common.action_chains import ActionChains
menu = driver.find_element(By.CSS_SELECTOR, ".nav-dropdown")
ActionChains(driver).move_to_element(menu).pause(0.5).perform()
submenu = driver.find_element(By.CSS_SELECTOR, ".nav-dropdown .sub-item")
ActionChains(driver).move_to_element(submenu).click().perform()

# 下拉框选择
from selenium.webdriver.support.ui import Select
select_el = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='status']"))
)
Select(select_el).select_by_visible_text("已完成")

# iframe 切换
iframe = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "iframe_id"))
)
# ... 在 iframe 内操作 ...
driver.switch_to.default_content()  # 切回主文档
```

## 2. 等待策略

**禁止使用 `time.sleep()` 作为主要等待方式**, 仅用于调试或已知固定延迟.

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 显式等待 - 元素出现
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "content"))
)

# ✅ 显式等待 - 元素可见
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-row"))
)

# ✅ 显式等待 - 元素可点击
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='submit']"))
)

# ✅ 显式等待 - URL 变化
WebDriverWait(driver, 10).until(EC.url_changes(original_url))

# ✅ 显式等待 - 新窗口打开
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

# ✅ 显式等待 - JS 变量变化
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return window.appLoaded === true")
)

# ✅ 组合条件
from selenium.webdriver.support import expected_conditions as EC
WebDriverWait(driver, 10).until(
    EC.or_(
        EC.url_contains("success"),
        EC.visibility_of_element_located((By.CLASS_NAME, "error-msg"))
    )
)
```

## 3. 输入操作

```python
def safe_input(driver, locator, text, clear_first=True):
    """安全输入: 点击聚焦 → 清除 → 输入."""
    if isinstance(locator, tuple):
        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
    else:
        el = driver.find_element(By.CSS_SELECTOR, locator)
    
    el.click()
    if clear_first:
        el.clear()
        # Ctrl+A 全选后删除 (处理某些禁用 clear 的字段)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
    el.send_keys(text)
    return el
```

## 4. 截图对比

```python
import os
from datetime import datetime

def screenshot(driver, name, subdir="screenshots"):
    """按时间戳截图保存."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(subdir, f"{name}_{ts}.png")
    driver.save_screenshot(path)
    return path
```

## 5. 弹窗/对话框处理

```python
# Alert
alert = driver.switch_to.alert
alert.accept()          # 确认
alert.dismiss()         # 取消
alert.send_keys("text") # 输入文本

# Confirm 弹窗
driver.switch_to.alert.accept()  # 确定
driver.switch_to.alert.dismiss()  # 取消

# 模态框/自定义弹窗 (通常不在 alert 层)
# 等待元素出现
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay"))
)
# ... 操作 ...
driver.find_element(By.CSS_SELECTOR, ".modal-close").click()
```

## 6. 页面导航与状态检测

```python
# 等待页面完全加载
def wait_page_load(driver, timeout=30):
    state = driver.execute_script("return document.readyState")
    if state != "complete":
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

# 获取所有窗口句柄并切换
windows = driver.window_handles
driver.switch_to.window(windows[-1])  # 切换到新窗口

# 后退/前进
driver.back()
driver.forward()
```

## 7. Chrome 选项 (推荐配置)

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 ...")
    # 禁用图片加载 (提速)
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)  # 全局隐式等待
    return driver
```

## 8. 元素定位优先级

按稳定性从高到低:

1. **`id`** — 最稳定 (唯一)
2. **`data-*` 属性** — 业务属性, 通常不变
3. **`name`** — 表单字段常用
4. **`aria-label` / `aria-*`** — 无障碍属性, 较稳定
5. **XPath 文本匹配** — `//button[contains(text(),'确认')]`
6. **CSS class (精确)** — `.btn-primary.submit` (非模糊 class)
7. **CSS class (模糊)** — `[class*='login']` (备选)
8. **XPath 位置索引** — `//tr[3]/td[2]` (最后手段)

**避免:** XPath 绝对路径 `//html/body/div[3]/div[2]/span`, 极易失效.
