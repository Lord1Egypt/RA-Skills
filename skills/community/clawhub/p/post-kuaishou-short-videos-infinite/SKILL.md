---
name: post-kuaishou-short-videos-infinite
description: 在快手创作者平台发布短视频。触发场景：发布快手视频、上传快手视频、快手发布视频、发快手视频、发布快手短视频。
version: 1.0.0.0
---

# 发布快手短视频_无限

用于在快手创作者平台发布短视频，包含完整的视频上传、标题简介填写、封面设置、声明设置和权限配置流程。

## 触发场景

用户说：
- "发布快手视频"
- "上传快手视频"
- "快手发布视频"
- "发快手视频"
- "发布快手短视频"

## 重要注意事项

⚠️ **必须先启动 OpenClaw 浏览器！**
- 所有浏览器操作前，**必须先启动 OpenClaw 托管的 Chrome**
- 使用 `browser(action=start, target="host", profile="openclaw")` 启动浏览器
- 启动后再用 `browser(action=navigate, target="host", profile="openclaw", url=...)` 导航到目标 URL

⚠️ **浏览器控制核心原则：**
- `browser(action=start, target="host", profile="openclaw")` 用于启动浏览器
- `browser(action=navigate, target="host", profile="openclaw", url=...)` 用于导航页面
- **禁止使用 `profile="user"` 或 `profile="chrome-relay"`**（除非用户明确要求使用用户浏览器）
- **禁止使用 `browser(action=open, targetUrl=...)`**（会被 SSRF 策略拦截）
- **禁止硬编码 ref 值** — 每次页面加载后 ref 值会变化，必须通过快照获取当前 refs
- **使用 `type` 命令输入文本**，无需 JS evaluate

⚠️ **核心操作原则：**
- 除登录、支付、删除等核心操作外，**所有问题自己尝试解决，不指挥用户**
- 操作过程中如遇弹窗/提示，优先尝试自行关闭或确认，不凡事都问用户
- 每一步操作前先获取快照（snapshot），从快照中获取元素的 ref 值

## 操作流程

### 第零步：启动 OpenClaw 浏览器

1. 调用 `browser(action=start, target="host", profile="openclaw")` 启动浏览器
2. 若浏览器已在运行，跳过此步骤
3. 检查 `browser(action=status, target="host")` 确认状态

### 第一步：导航到上传页面

1. 导航到：`https://cp.kuaishou.com/article/publish/video?tabType=1`
2. 等待页面加载完成（可使用 `loadState="networkidle"`）
3. 获取页面快照，从快照中识别并点击相关按钮

### 第二步：上传视频文件

1. 从快照中找到**"上传视频"**按钮或上传区域的 ref
2. 点击上传按钮触发系统文件选择对话框
3. **使用 pyautogui 自动操作文件对话框选择视频文件：**

```python
# -*- coding: utf-8 -*-
import pyautogui
import time
import tkinter as tk

# 等待文件对话框出现
time.sleep(3)

# 按 Ctrl+L 聚焦地址栏
pyautogui.keyDown('ctrl')
pyautogui.keyDown('l')
pyautogui.keyUp('l')
pyautogui.keyUp('ctrl')

time.sleep(0.5)

# 全选并删除地址栏原有内容
pyautogui.keyDown('ctrl')
pyautogui.keyDown('a')
pyautogui.keyUp('a')
pyautogui.keyUp('ctrl')
time.sleep(0.2)
pyautogui.keyDown('delete')
pyautogui.keyUp('delete')
time.sleep(0.3)

# 使用 tkinter 复制文件夹路径到剪贴板（确保中文正确）
# ⚠️ 重要：必须使用原始字符串 r'' 或双反斜杠 \\ 来避免转义问题
# 错误：'E:\file\0素材' 中的 \f 会被转义为换页符，变成 'E:ile'
# 正确：r'E:\file\0素材' 或 'E:\\file\\0素材'
folder_path = r'文件夹路径'  # 例如：r'E:\file\0素材'
r = tk.Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(folder_path)
r.destroy()

# 粘贴路径
pyautogui.keyDown('ctrl')
pyautogui.keyDown('v')
pyautogui.keyUp('v')
pyautogui.keyUp('ctrl')

time.sleep(0.5)

# 按回车进入文件夹
pyautogui.keyDown('return')
pyautogui.keyUp('return')

time.sleep(2)

# 使用 tkinter 复制文件名到剪贴板
filename = u'视频文件名'  # 例如：u'AI超越人类.mp4'
r = tk.Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(filename)
r.destroy()

# 粘贴文件名
pyautogui.keyDown('ctrl')
pyautogui.keyDown('v')
pyautogui.keyUp('v')
pyautogui.keyUp('ctrl')

time.sleep(0.5)

# 按回车确认选择
pyautogui.keyDown('return')
pyautogui.keyUp('return')

time.sleep(2)
```

**关键要点：**
- 必须先按 Ctrl+A 全选并删除地址栏原有内容，再输入新路径
- 使用 `tkinter` 将中文路径复制到剪贴板，然后 Ctrl+V 粘贴，确保中文字符不丢失
- **路径格式必须使用原始字符串 r''**：如 `r'E:\file\0素材'`，避免 `\f` 等被转义
- 先输入文件夹路径，按回车进入文件夹
- 再输入文件名，按回车确认选择
- 等待视频上传完成（上传统钮变为已上传状态，或出现进度条）

### 第三步：填写视频信息

1. **填写作品描述**
   - 获取快照，找到作品描述输入框的 ref（如 textarea 或 input 元素 placeholder 包含"描述"或"作品描述"）
   - 使用 `type` 命令在描述输入框中按顺序输入：
     - 首先输入**标题**
     - 然后在标题后面追加**概述**内容
     - 最后在概述后面追加**话题或标签**（如 `#标签名`）
   
2. **⚠️ 重要：话题/标签处理**
   - **快手最多只能设置 4 个话题或标签**
   - 如果用户提供了超过 4 个标签，**必须删除多余的标签**，只保留前 4 个
   - 每追加一个话题或标签后，描述输入框下面会弹出一个下拉框
   - 下拉框里面会显示同名的标签或话题选项
   - **必须立即在这个下拉框里点击一下同名的标签或话题，确认选中**
   - 然后再追加下一个标签或话题，重复此过程
   - 每个标签都要这样操作，不能跳过任何一个标签的下拉框确认步骤
   - **超过 4 个标签时发布会失败**

### 第四步：设置 PK 封面

**PK 封面设置三步法：**

1. **打开 PK 封面开关**
   - 从快照中找到**"PK 封面"**滑动开关（通常是 `switch` 元素）
   - 点击开关将其打开（状态变为 `checked`）

2. **点击 PK 封面按钮打开封面选择对话框**
   - 找到 PK 封面所在行的按钮（通常是 `PK封面` 文本旁边的可点击元素）
   - 点击后弹出封面选择对话框

3. **在封面选择对话框中确认**
   - 对话框中会显示视频帧缩略图（`img "background"` 元素）
   - 直接点击**"确认"**按钮使用默认封面
   - 等待对话框关闭，PK 封面设置完成

**关键要点：**
- 必须先打开 PK 封面开关，再点击 PK 封面按钮
- 封面选择对话框中的确认按钮通常是 `button "确认"`
- 设置完成后对话框会自动关闭

### 第五步：添加作者声明

1. 在页面中找到**"作者声明"**相关选项
2. 选择**"内容为 AI 生成"**选项
3. 如有确认按钮，点击确认

### 第六步：设置下载权限

1. 找到**"允许下载此作品"**选项（通常是复选框）
2. **取消勾选**此选项（确保前面的勾被去掉）

**正确取消方法：**
- 使用快照获取"允许下载此作品"复选框的 ref（如 `e321`）
- 使用 `browser(action=click, ref="e321")` 点击复选框
- 再次获取快照确认复选框状态变为 `active` 或 `unchecked`
- 如果一次点击未取消，可再次点击

**注意：** 不要直接使用 JavaScript 操作 checkbox，应通过点击事件来切换状态

### 第七步：保存并发布

1. 找到并点击**"发布"**按钮（或类似的保存/提交按钮）
2. 确认发布操作，完成发布流程

## 关键元素参考

| 元素 | 描述 | 操作方式 |
|------|------|---------|
| 上传页面 URL | https://cp.kuaishou.com/article/publish/video?tabType=1 | navigate 导航 |
| 上传视频按钮 | 触发系统文件选择 | click + ref，然后用 pyautogui 自动选择文件 |
| 作品描述输入框 | placeholder 包含"描述"或"作品描述" | type 命令输入（标题 + 概述 + 标签）|
| PK 封面开关 | 封面设置区域的滑动开关 | click + ref 打开 |
| 封面设置 + 号 | 封面设置所在行的添加按钮 | click + ref |
| 确认按钮 | 封面弹出对话框的确认 | click + ref |
| 作者声明 | AI 生成内容选项 | click + ref 选中 |
| 允许下载 | 下载权限复选框 | click + ref 取消勾选 |
| 发布按钮 | 保存并发布视频 | click + ref |

## 技术要点总结

1. **先启动浏览器** — 使用 `browser(action=start, target="host", profile="openclaw")`
2. **用 navigate 导航** — `browser(action=navigate, target="host", profile="openclaw", url=...)`
3. **每步先快照获取 ref** — 禁止硬编码，必须实时从快照获取
4. **视频上传使用 pyautogui 自动操作文件对话框** — 使用 tkinter 复制中文路径到剪贴板，Ctrl+V 粘贴，避免中文乱码
5. **type 命令输入文本** — 直接使用 type 命令在输入框中输入内容
6. **作品描述格式** — 按顺序输入：标题 → 概述 → 话题标签，不要删除已输入内容
7. **每个标签/话题都需要下拉框确认** — 每追加一个标签后，描述输入框下面会弹出下拉框，里面显示同名标签，必须立即点击确认，然后再追加下一个，每个标签都要这样操作
8. **PK 封面设置三步法** — 点击"PK 封面开关" → 点击封面行"+"号 → 点击"确认"
9. **作者声明选择 AI 生成** — 在作者声明选项中选择"内容为 AI 生成"
10. **取消允许下载** — 确保"允许下载此作品"选项未勾选

## 常见失败原因

- ❌ 浏览器未启动就调用 navigate → 应先 start
- ❌ 硬编码 ref 值 → 每次页面刷新 ref 会变化，必须快照获取
- ❌ 使用 profile="user" → 应使用 profile="openclaw"
- ❌ 使用 browser(action=open) → 应使用 browser(action=navigate)
- ❌ 使用 evaluate 执行 JS → 应使用 type 命令直接输入
- ❌ 描述内容格式错误 → 应按顺序输入：标题 + 概述 + 标签，不要遗漏任何部分
- ❌ 标签/话题未确认 → 每个标签都必须在描述输入框下面弹出的下拉框里点击同名标签确认，不能跳过任何一个标签
- ❌ PK 封面设置不完整 → 必须完成三步：打开开关 → 点击 + 号 → 点击确认
- ❌ 作者声明未正确选择 → 确认选择"内容为 AI 生成"
- ❌ 下载权限未取消 → 确认"允许下载此作品"未勾选
