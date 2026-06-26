---
name: post-tiktok-short-videos-infinite
description: 在抖音创作者平台发布短视频。触发场景：发布抖音视频、上传抖音视频、抖音发布视频、发抖音视频。
version: 1.0.0.0
---

# 发布抖音短视频_无限

用于在抖音创作者平台发布短视频，包含完整的视频上传、标题简介填写、封面设置、合集选择和声明设置流程。

## 触发场景

用户说：
- "发布抖音视频"
- "发表抖音视频"
- "上传抖音视频"
- "抖音发布视频"
- "抖音发表视频"
- "发抖音视频"
- "发布抖音短视频"
- "发表抖音短视频"

## 重要注意事项

⚠️ **必须先启动 OpenClaw 浏览器！**
- 所有浏览器操作前，**必须先启动 OpenClaw 托管的 Chrome**
- 使用 `browser(action=start, target="host", profile="openclaw")` 启动浏览器
- 启动后再用 `browser(action=navigate, ...)` 导航到目标 URL

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

1. 导航到：`https://creator.douyin.com/creator-micro/content/upload`
2. 等待页面加载完成（可使用 `loadState="networkidle"`）
3. 获取页面快照，从快照中识别并点击相关按钮

### 第二步：上传视频文件

1. 从快照中找到**"高清发布"**按钮的 ref，点击它
2. 找到**"发布视频"**按钮的 ref，点击它
3. 找到**"上传视频"**相关按钮或上传区域的 ref
4. 点击上传按钮后，等待系统文件选择对话框出现
5. **使用 pyautogui 自动操作文件对话框选择视频文件：**

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
folder_path = r'文件夹路径'  # 例如：r'E:\file\0未来科技\AI'
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

1. **填写标题**
   - 获取快照，找到标题输入框的 ref（如 input 元素 placeholder 包含"标题"）
   - 使用 `type` 命令在标题输入框中输入视频标题

2. **填写简介**
   - 从快照中找到简介/描述输入框的 ref
   - 使用 `type` 命令输入视频简介/概述内容

3. **追加话题/标签**
   - **⚠️ 重要：不要删除已输入的简介内容，直接在简介末尾追加标签**
   - 在简介输入框的内容**后面直接追加**话题或标签（如 ` #标签名`）
   - 不要清空、删除或重新输入简介，只需在末尾追加标签
   - **⚠️ 重要：每追加一个标签或话题后，简介输入框下面会弹出一个下拉框**
   - **下拉框里面会显示同名的标签或话题选项**
   - **必须立即在这个下拉框里点击一下同名的标签或话题，确认选中**
   - **然后再追加下一个标签或话题，重复此过程**
   - **每个标签都要这样操作，不能跳过任何一个标签的下拉框确认步骤**
   - 不能跳过下拉框的点击确认步骤，否则标签可能无法正确添加

### 第四步：设置封面

1. 点击**"选择封面"**按钮
2. 点击右下角**"设置横封面"**按钮
3. 点击右下角**"完成"**按钮

就这三步，其他的不用管。

### 第五步：选择合集

1. 从快照中找到**"合集"**相关选项的 ref
2. 点击选择合集，从下拉列表中选择目标合集

### 第六步：设置权限

1. 找到**"保存权限"**或类似权限设置选项
2. 设置为**"不允许"**（或对应的不允许选项）

### 第七步：添加内容声明

1. 在页面右侧找到**"添加声明"**按钮，点击它
2. 在声明选项中选择**"内容由AI生成"**
3. 点击**"确定"**确认声明设置

### 第八步：暂存离开

1. 找到并点击**"暂存离开"**按钮（位于"发布"按钮旁边）
2. **⚠️ 重要：点击"暂存离开"而不是"发布"** — 这样可以将视频保存为草稿，而不是立即发布
3. 确认离开操作，完成暂存流程

## 关键元素参考

| 元素 | 描述 | 操作方式 |
|------|------|---------|
| 上传页面URL | https://creator.douyin.com/creator-micro/content/upload | navigate 导航 |
| 高清发布按钮 | 发布选项入口 | click + ref |
| 发布视频按钮 | 触发视频发布流程 | click + ref |
| 上传视频按钮 | 触发系统文件选择 | click + ref（需用户选择文件）|
| 标题输入框 | placeholder 包含"标题" | type 命令输入 |
| 简介输入框 | placeholder 包含"简介"或"描述" | type 命令输入 |
| 选择封面 | 封面设置入口 | click + ref |
| 设置横封面 | 横版封面选项 | click + ref |
| 完成按钮 | 确认封面设置 | click + ref |
| 合集选择 | 合集下拉选择 | click + ref → 选择 |
| 保存权限 | 权限设置选项 | 设置为不允许 |
| 添加声明 | 声明设置入口 | click + ref |
| 内容由AI生成 | AI声明选项 | click + ref 选中 |
| 确定按钮 | 确认声明 | click + ref |
| 暂存离开 | 保存草稿并离开 | click + ref |

## 技术要点总结

1. **先启动浏览器** — 使用 `browser(action=start, target="host", profile="openclaw")`
2. **用 navigate 导航** — `browser(action=navigate, target="host", profile="openclaw", url=...)`
3. **每步先快照获取 ref** — 禁止硬编码，必须实时从快照获取
4. **视频上传使用 pyautogui 自动操作文件对话框** — 使用 tkinter 复制中文路径到剪贴板，Ctrl+V 粘贴，避免中文乱码
5. **type 命令输入文本** — 直接使用 type 命令在输入框中输入内容
6. **追加话题在简介末尾添加** — 不替换简介内容，不删除已输入内容，直接在后面追加标签
7. **每个标签/话题都需要下拉框确认** — 每追加一个标签后，简介输入框下面会弹出下拉框，里面显示同名标签，必须立即点击确认，然后再追加下一个，每个标签都要这样操作
8. **设置封面三步法** — 点击"选择封面" → 点击右下角"设置横封面" → 点击右下角"完成"，就这三步，其他的不用管
9. **权限设置为不允许** — 注意找准权限设置选项
10. **声明选择"内容由AI生成"** — 在添加声明弹窗/选项中选择正确项
11. **暂存离开而不是发布** — 最后点击"暂存离开"按钮保存为草稿，而不是点击"发布"按钮

## 常见失败原因

- ❌ 浏览器未启动就调用 navigate → 应先 start
- ❌ 硬编码 ref 值 → 每次页面刷新 ref 会变化，必须快照获取
- ❌ 使用 profile="user" → 应使用 profile="openclaw"
- ❌ 使用 browser(action=open) → 应使用 browser(action=navigate)
- ❌ 使用 evaluate 执行 JS → 应使用 type 命令直接输入
- ❌ 使用 tkinter 路径未用原始字符串 r'' → `\f` 等会被转义，必须用 `r'E:\folder'` 格式
- ❌ 简介内容被覆盖 → 话题应追加到末尾，不是替换，不要删除已输入的简介内容
- ❌ 标签/话题未确认 → 每个标签都必须在简介输入框下面弹出的下拉框里点击同名标签确认，不能跳过任何一个标签
- ❌ 设置封面操作复杂 → 只需三步：点击"选择封面" → 点击右下角"设置横封面" → 点击右下角"完成"，其他的不用管
- ❌ 没有设置封面 → 必须同时设置竖封面和横封面，不能遗漏
- ❌ 权限设置错误 → 确认是"不允许"选项
- ❌ 声明未正确选择 → 确认选择"内容由AI生成"
- ❌ 点击"发布"而不是"暂存离开" → 应点击"暂存离开"保存为草稿，而不是立即发布
