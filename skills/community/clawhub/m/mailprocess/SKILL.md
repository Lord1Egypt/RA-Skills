---
name: mali-builder
description: 自动调用码力搭建平台完成应用搭建。触发词：码力搭建、mali、低代码搭建、搭建应用、创建应用、管理系统、数据看板、表单系统。自动打开Chrome填充需求并点击发送。适合内部工具、数据展示、表单收集、快速原型开发。
---

# 码力搭建 Skill

## 功能说明
该 Skill 用于调用码力搭建平台（Mali App Builder），自动化完成以下操作：
1. 在用户的 Chrome 浏览器中打开码力搭建平台
2. 确保用户已登录
3. 将用户的搭建需求自动填入对话框
4. 触发搭建流程

## 触发条件
- 用户明确要求使用"码力搭建"、"Mali"或"低代码搭建"
- 用户提出应用搭建需求，且适合使用低代码平台实现

## 操作流程

### 步骤 1: 打开码力搭建平台
使用 AppleScript（macOS）或其他系统命令打开 Chrome 浏览器并导航到码力搭建平台：

```bash
# macOS 使用 AppleScript
osascript -e 'tell application "Google Chrome"
    activate
    open location "https://lowcode.baidu-int.com/ai-coding"
end tell'

# Linux 使用 xdg-open
xdg-open "https://lowcode.baidu-int.com/ai-coding"

# Windows 使用 start
start chrome "https://lowcode.baidu-int.com/ai-coding"
```

### 步骤 2: 等待页面加载
等待 3-5 秒确保页面完全加载，并检查用户登录状态。

### 步骤 3: 注入需求并触发搭建
使用 Chrome DevTools Protocol 或 JavaScript 注入来填充搭建需求：

```javascript
// 通过 Chrome DevTools Protocol 执行
// 1. 找到输入框并填入需求
const inputBox = document.querySelector('textarea[placeholder*="描述"], input[type="text"]');
if (inputBox) {
    inputBox.value = "用户的搭建需求内容";
    inputBox.dispatchEvent(new Event('input', { bubbles: true }));
}

// 2. 找到发送按钮并点击
const sendButton = document.querySelector('button[type="submit"], button.send-btn');
if (sendButton) {
    sendButton.click();
}
```

### 步骤 4: 确认执行状态
- 验证请求已发送
- 监控搭建进度
- 向用户反馈当前状态

## 输出格式

执行完成后返回：

```
✅ 码力搭建已启动！

🌐 浏览器: Chrome
📍 平台地址: https://lowcode.baidu-int.com/ai-coding

📋 提交的需求:
{用户的原始需求}

⏳ 请在浏览器中查看搭建进度...
```

## 错误处理

### 浏览器未安装
```
❌ 未找到 Chrome 浏览器
💡 建议: 请安装 Chrome 浏览器后重试
```

### 登录状态异常
```
⚠️ 检测到未登录状态
💡 建议: 请先在浏览器中登录码力搭建平台
🔗 登录地址: https://lowcode.baidu-int.com/ai-coding
```

### 页面加载失败
```
❌ 页面加载失败
💡 建议: 
1. 检查网络连接
2. 确认是否在公司内网环境
3. 手动访问平台进行搭建
```

## 技术实现

### 方案 A: AppleScript + Chrome (推荐 macOS)
```applescript
tell application "Google Chrome"
    activate
    set myTab to make new tab at end of tabs of window 1
    set URL of myTab to "https://lowcode.baidu-int.com/ai-coding"
    delay 3
    execute myTab javascript "
        const input = document.querySelector('textarea, input[type=\"text\"]');
        if (input) {
            input.value = '用户需求内容';
            input.dispatchEvent(new Event('input', {bubbles: true}));
            const btn = document.querySelector('button[type=\"submit\"]');
            if (btn) btn.click();
        }
    "
end tell
```

### 方案 B: Python + Selenium (跨平台)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def launch_mali_builder(user_requirement):
    driver = webdriver.Chrome()
    driver.get('https://lowcode.baidu-int.com/ai-coding')
    
    # 等待页面加载
    time.sleep(3)
    
    # 查找输入框
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea, input[type='text']"))
        )
        input_box.send_keys(user_requirement)
        
        # 查找发送按钮
        send_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        send_btn.click()
        
        print("✅ 搭建需求已提交")
    except Exception as e:
        print(f"❌ 操作失败: {str(e)}")
```

### 方案 C: 纯命令行 (最简单)
```bash
#!/bin/bash
# 简单地打开浏览器到指定页面
# 用户需要手动输入需求

MALI_URL="https://lowcode.baidu-int.com/ai-coding"

case "$(uname -s)" in
    Darwin*)
        open -a "Google Chrome" "$MALI_URL"
        ;;
    Linux*)
        xdg-open "$MALI_URL" || google-chrome "$MALI_URL"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        start chrome "$MALI_URL"
        ;;
esac

echo "✅ 已在浏览器中打开码力搭建平台"
echo "📍 $MALI_URL"
echo ""
echo "📋 请手动输入以下需求："
echo "$1"
```

## 使用示例

### 示例 1: 简单应用搭建
```
用户: 帮我用码力搭建一个任务管理应用
助手: [执行 mali-builder skill]
      ✅ 码力搭建已启动！
      📋 提交的需求: 任务管理应用
```

### 示例 2: 复杂需求搭建
```
用户: 使用码力搭建创建一个包含用户登录、数据看板、报表导出的管理系统
助手: [执行 mali-builder skill]
      ✅ 码力搭建已启动！
      📋 提交的需求: 包含用户登录、数据看板、报表导出的管理系统
```

## 注意事项

1. **网络要求**: 需要在公司内网或 VPN 环境下使用
2. **浏览器要求**: 推荐使用 Chrome 浏览器（最新版本）
3. **登录状态**: 首次使用需要手动登录一次
4. **权限要求**: 需要系统允许脚本控制浏览器的权限
5. **自动化限制**: 部分页面可能有反自动化机制，需要用户手动确认

## 兼容性

| 操作系统 | Chrome | Safari | Firefox | Edge |
|---------|--------|--------|---------|------|
| macOS   | ✅     | ✅     | ⚠️      | ❌   |
| Linux   | ✅     | ❌     | ⚠️      | ❌   |
| Windows | ✅     | ❌     | ⚠️      | ✅   |

✅ 完全支持  ⚠️ 部分支持  ❌ 不支持