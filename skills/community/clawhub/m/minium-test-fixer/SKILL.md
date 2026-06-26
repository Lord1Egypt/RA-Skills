---
name: minium-test-fixer
description: Minium 测试用例修复工具。自动修复测试中的元素定位错误，分析错误日志、读取 WXML 快照、找到正确元素定位并修复代码。当测试报错"找不到元素"、需要优化元素定位、或分析 WXML 结构时使用此技能。支持本地运行日志和云测平台报告。
---

# Minium 测试用例修复技能

## 📖 描述

自动修复 Minium 测试用例中的元素定位错误。当测试用例因元素找不到而失败时，本技能自动分析错误日志、读取 WXML 快照、找到正确的元素定位并修复代码。

**核心能力**:
- ✅ 分析 WXML 找到正确元素
- ✅ 修复元素定位问题
- ✅ 验证修复后测试通过

---

## 🎯 触发条件

**核心触发场景**：用户提供 Minium 测试错误报告，要求修复用例

**触发词**：
- "修复用例"
- "测试报错了"
- "元素找不到"
- "帮我看看这个错误"
- 直接粘贴错误日志/错误报告

**支持的报告格式**：
1. **本地运行日志** - 直接粘贴终端输出
2. **云测平台报告** - 粘贴云测平台的错误日志
3. **错误截图** - 描述错误信息

---

## ⚡ 核心规则（必须遵守！）

### 🚨 规则 1：先运行测试，获取最新 WXML

**当用户提供错误报告时，禁止直接修复！**

**正确流程**：
```
第 1 步：运行测试用例
→ minitest -m <模块名> --case <用例名> -c config.json -g
→ 等待测试失败，自动生成 error_wxml/error_page.xml

第 2 步：读取错误日志
→ 找到失败的元素定位（如 self.tap(self.xxx)）
→ 记录元素变量名（如 xxx）

第 3 步：在 WXML 中搜索正确元素
→ 搜索元素文本或 class
→ 找到正确的定位方式

第 4 步：提供修复方案给用户确认
→ 展示当前定位和正确定位
→ 等待用户确认

第 5 步：更新代码
→ 修改对应的 Page Object 文件
```

**错误示范（禁止！）**：
- ❌ 用户给错误报告 → 直接修改代码（未运行测试）
- ❌ 假设元素定位（未查看 WXML）
- ❌ 覆盖用户原有代码（未确认）

---

### 🚨 规则 2：页面有多个相同元素时，使用 get_elements()[0]

**核心问题**：页面里有多个同样的元素，直接点击会失败

**正确做法**：
```python
# ❌ 错误做法（会失败）
self.tap_icon(self.element_name)

# ✅ 正确做法（获取第一个元素）
self.get_elements(self.element_name)[0].tap()
```

**适用场景**：
- feed 列表中的多个相同按钮
- 商品列表中的多个相同操作按钮
- 任何重复出现的元素

---

### 🚨 规则 3：优先使用文本定位，避免长 XPath

**核心问题**：长 XPath 依赖页面结构索引，页面结构变化就会失效

**对比**：
```python
# ❌ 错误做法（长 XPath，不稳定）
element_name = "/page-wrapper/view/view/view[1]/view[3]/view[4]/view[3]/view[1]/home-sequence-list/view/view/view[6]/view[1]/view[2]"

# ✅ 正确做法（文本定位，稳定）
element_name = "//*[text()='按钮文本']"
```

**定位优先级**：
1. **文本定位**（最稳定）：`//*[text()='按钮文本']`
2. **CSS selector**（较稳定）：`view.class-name`
3. **XPath 属性**（中等）：`//view[@data-key='xxx']`
4. **长 XPath**（最不稳定，禁止使用）

---

### 🚨 规则 4：无法识别时直接问

**当以下情况无法确定元素时**：

1. 原定位路径在 WXML 中找不到
2. 变量名无意义（如 `element_1`）
3. 没有注释说明元素用途
4. WXML 中有多个相似元素

**正确做法**：
```
这个元素的定位路径失效了，变量名是 `feed_follow_leader`。

在最新 WXML 中没找到唯一匹配的元素。

请问这个元素应该显示什么文本？或者截个图告诉我它是哪个按钮？
```

**错误做法**：
- ❌ 瞎猜一个文本
- ❌ 随便选一个相似的
- ❌ 不确认就直接修改

---

### 🚨 规则 5：已存在目录 → 先阅读现有代码结构！

**当修复用例时，禁止直接修改！**

**正确流程**：
```
第 1 步：读取现有 Page Object 文件
→ 查看元素定义风格（CSS selector 还是 xpath）
→ 查看方法命名规范

第 2 步：总结现有规则
→ Page Object 命名规则
→ 元素定位规则
→ 测试用例结构

第 3 步：按现有规则修复
→ 新 Page Object 遵循已有命名和结构
→ 新测试用例遵循已有风格和格式
→ 不引入与现有代码冲突的规范
```

---

### 🚨 规则 6：先阅读用户基类代码，再决定使用什么方法！

**Page Object 核心规则**：

1. **先阅读用户的基类代码**（如 basedef.py）
   - 检查用户是否封装了点击、输入等方法
   - 如果有封装 → 使用用户的封装方法
   - 如果没有封装 → 生成封装方法并使用

2. **检查用户的封装方式**
   - 点击方法：可能是 `tap()`, `click()`, `click_element()`, `tap_icon()` 等
   - 输入方法：可能是 `send_key()`, `input_text()`, `type()` 等
   - 滚动方法：可能是 `scroll_to()`, `scroll()` 等

3. **不要照搬录制脚本的等待时间！**
   - 录制脚本中的 `self.page.wait_for(x)` 是录制工具自动生成的
   - 用户的基类方法（如 `tap()`, `send_key()`）内部已有等待逻辑
   - **禁止生成多余的 `sleep()` 或 `wait_for()`**

---

### 🚨 规则 7：修复后必须在本地验证！

**核心原则**：改完之后一定要在本地先自己跑一遍确认没有报错

**正确流程**：
```
第 1 步：修复元素定位
→ 修改 Page Object 文件

第 2 步：本地运行测试
→ 激活微信开发者工具（AppActivate）
→ minitest -m <模块名> --case <用例名> -c config.json -g

第 3 步：确认测试结果
→ 看到 "case num:1, failed num:0, error num:0" 才算成功
→ 如果还有报错 → 继续修复其他元素

第 4 步：报告用户
→ 本地验证通过后再告知用户
→ 云测平台的用例让用户重新运行
```

**错误示范（禁止！）**：
- ❌ 修改代码后不验证就直接报告完成
- ❌ 只依赖云测平台验证（来回浪费时间）
- ❌ 假设修复成功（不运行测试）

**正确示范**：
```
✅ 修复完成！
本地验证结果：
====================case num:1, failed num:0, error num:0====================

主人，本地测试已通过！你可以在云测平台重新运行了！
```


---

## 📋 完整修复流程

### 步骤 1：运行测试用例（开发者工具保持前台）

**方法 A：使用窗口标题激活（推荐）**
```powershell
# 通过窗口标题激活微信开发者工具
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate("微信开发者工具")

# 运行测试用例
minitest -m <模块路径> --case <用例名> -c config.json -g
```

**方法 B：使用进程名激活**
```powershell
# 通过进程名激活
Add-Type -AssemblyName System.Windows.Forms
$proc = Get-Process | Where-Object { $_.ProcessName -like "*wechat*" -or $_.MainWindowTitle -like "*开发者工具*" }
if($proc) {
 [System.Windows.Forms.SendKeys]::SendWait("%{TAB}")
 Start-Sleep -Milliseconds 500
}

# 运行测试
minitest -m <模块路径> --case <用例名> -c config.json -g
```

**注意**：
- 运行测试前，确保微信开发者工具已打开
- 使用 `AppActivate` 直接激活指定窗口（比 Alt+Tab 更可靠）
- 测试运行期间不要切换到其他窗口

---

### 步骤 2：读取错误日志

测试失败后，查看错误堆栈：

```python
File "cases/case/pages/pages/xxx/xxx.py", line 399, in test_method
 self.tap(self.element_name)
```

**提取关键信息**：
- 失败文件：`pages/pages/xxx/xxx.py`
- 失败行号：399
- 失败元素：`self.element_name`

---

### 步骤 3：查找当前元素定义

```bash
Select-String -Path "<文件路径>" -Pattern "element_name\s*="
```

**示例输出**：
```python
element_name = "//*[text()='按钮文本']"
```

---

### 步骤 4：读取 WXML 文件

```bash
Get-ChildItem "error_wxml\error_page.xml" | Select-Object LastWriteTime
```

**在 WXML 中搜索正确元素**：

```bash
# 搜索文本
Select-String -Path "error_wxml\error_page.xml" -Pattern "按钮文本"

# 搜索 class
Select-String -Path "error_wxml\error_page.xml" -Pattern "operate-btn|more"

# 搜索 custom-modal/popup
Select-String -Path "error_wxml\error_page.xml" -Pattern "custom-modal|popup"
```

---

### 步骤 5：提供修复方案

**向用户展示**：

```markdown
## 📊 分析结果

**当前元素定义**：
```python
element_name = "//*[text()='按钮文本']"
```

**WXML 中实际结构**：
```xml
<view class="actionsheet--sheet-item">按钮文本</view>
```

**建议修复方案**：

**方案 1**：使用 class 定位
```python
element_name = "view.class='actionsheet--sheet-item'"
```

**方案 2**：使用 text 包含
```python
element_name = "//*[contains(text(),'按钮')]"
```

---

**主人，确认这个修改吗？** 🔧
```

---

### 步骤 6：用户确认后更新代码

```python
# 使用 edit 工具精确替换
edit(
 path="<文件路径>",
 oldText='element_name = "//*[text()=\'按钮文本\']"',
 newText='element_name = "view.class=\'actionsheet--sheet-item\'"'
)
```

---

### 步骤 7：重新运行测试验证（必须！）

**⚠️ 重要：修复后必须在本地验证！**

```bash
# 激活微信开发者工具
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate("微信开发者工具")

# 运行测试
minitest -m <模块路径> --case <用例名> -c config.json -g
```

**确认测试通过**：
```
====================case num:1, failed num:0, error num:0====================
```

**只有看到上述输出才算修复完成！**

如果还有报错：
1. 读取新的错误日志
2. 继续修复下一个元素
3. 重新运行测试
4. 直到完全通过

---

## 💡 踩坑总结

### 坑 1：页面有多个相同元素

**现象**：元素定位正确，但点击失败

**原因**：页面里有多个同样的元素，`tap_icon()` 不知道点哪个

**解决**：使用 `get_elements()[0].tap()` 获取第一个

**案例**：
```python
# feed_statistic 等按钮在 feed 列表中重复出现
self.get_elements(self.feed_statistic)[0].tap()
self.get_elements(self.feed_order_manage)[0].tap()
self.get_elements(self.feed_wait_thaw_payment)[0].tap()
```

---

### 坑 2：长 XPath 定位不稳定

**现象**：今天能跑，明天就失败

**原因**：XPath 依赖页面结构索引，页面结构一变就失效

**解决**：使用文本定位 `//*[text()='按钮文本']`

**案例**：
```python
# ❌ 错误做法
element_name = "/page-wrapper/view/view/view[1]/view[3]/view[4]/view[3]/view[1]/home-sequence-list/view/view/view[6]/view[1]/view[2]"

# ✅ 正确做法
element_name = "//*[text()='按钮文本']"
```

---

### 坑 3：开发者工具不在前台

**现象**：页面跳转超时 `WaitTimeoutError`

**原因**：微信开发者工具在后台，页面加载慢或卡住

**解决**：运行测试前用 `AppActivate` 激活开发者工具

**案例**：
```powershell
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate("微信开发者工具")
Start-Sleep -Milliseconds 2000
```

---

### 坑 4：元素定义乱码

**现象**：修改后元素定义变成乱码

**原因**：PowerShell 字符串转义问题

**解决**：使用 Python 脚本修改文件

**案例**：
```python
# fix_elements.py
import re
content = open('file.py', 'r', encoding='utf8').read()
content = re.sub(r'element_name = ".*?"', 'element_name = "//*[text()=\'按钮文本\']"', content)
open('file.py', 'w', encoding='utf8').write(content)
```

---

## 🧪 使用示例

### 示例 1：用户提供错误报告

**用户**：
```
测试用例 test_xxx 报错了
Error Log:
File "pages/xxx.py", line 399
 self.tap(self.element_name)
RuntimeError: 找不到元素
```

**技能响应**：
```
🦞 收到，我来帮你修复！

**第 1 步：运行测试获取最新 WXML**
```bash
minitest -m testcase.xxx --case test_xxx -c config.json -g
```

[运行测试...]

**第 2 步：分析错误**
- 失败元素：`element_name`
- 当前定位：`//*[text()='按钮文本']`

**第 3 步：查找 WXML**
[搜索 WXML...]

**第 4 步：修复方案**
[提供方案...]

主人，确认修改吗？
```

---

### 示例 2：云测平台报告

**用户**：
```
测试用例
(testcase.xxx.TestXxx)test_xxx
测试结果
未通过
Error Log:
Traceback (most recent call last):
 File "/home/runtest/minium/framework/libs/unittest/case.py", line 266, in testPartExecutor
 yield
 File "/home/runtest/minium/framework/libs/unittest/case.py", line 351, in run
 self._callTestMethod(testMethod)
 File "/home/runtest/minium/framework/minitest.py", line 1071, in _callTestMethod
 method()
 File "cases/case/testcase/xxx/xxx.py", line 49, in test_xxx
 self.xxx_page.xxx_method()
 File "cases/case/pages/pages/xxx/xxx.py", line 169, in xxx_method
 self.tap(self.element_name)
```

**技能响应**：
```
🦞 收到云测报告，我来帮你修复！

**分析云测报告**：
- 失败文件：`pages/pages/xxx/xxx.py`
- 失败行号：169
- 失败方法：`xxx_method`
- 失败元素：`self.element_name`

**第 1 步：本地运行测试获取 WXML**
```bash
minitest -m testcase.xxx --case test_xxx -c config.json -g
```

[运行测试...]

**第 2 步：在 WXML 中搜索元素**
[搜索 WXML...]

**第 3 步：提供修复方案**
[提供方案...]

主人，确认修改吗？
```

---

### 示例 3：用户说"修复用例"

**用户**：
```
修复用例 testcase.xxx
```

**技能响应**：
```
🦞 好的，我来运行测试并修复！

**运行测试**：
```bash
minitest -m testcase.xxx --case test_xxx -c config.json -g
```

[等待测试失败 → 读取错误 → 查找 WXML → 提供方案]
```

---

## 📊 技能统计

| 指标 | 数值 |
|------|------|
| 支持的错误类型 | 元素找不到、元素定位过期、页面结构变化、多元素冲突 |
| 支持的定位方式 | 文本定位、CSS selector、XPath 属性、get_elements |
| 修复流程步骤 | 7 步 |
| 平均修复时间 | 2-5 分钟 |

---

## 🚀 快速开始

当你有 Minium 测试用例报错时，直接说：

```
修复用例 <用例名>
```

或者粘贴错误日志，我会自动帮你分析修复！

