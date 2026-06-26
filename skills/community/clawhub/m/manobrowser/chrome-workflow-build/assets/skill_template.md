---
name: xiaohongshu-post
description: 在小红书创作者平台发布图文笔记，支持上传图片、填写标题和正文内容，并完成发布操作
version: 1.0.0
---

# 小红书图文笔记发布

## 概述

本 Skill 用于在小红书创作者平台自动发布图文笔记。通过自动化流程，支持上传图片、填写标题和正文内容，并完成发布操作，帮助用户快速创建小红书内容。

**主要功能**：
- 自动导航到小红书创作者发布页面
- 上传指定URL的图片文件
- 填写笔记标题和正文内容
- 一键完成发布操作

**适用场景**：
- 批量发布小红书笔记
- 自动化内容发布流程
- 定时发布内容

## 快速开始

用户示例：
```
使用 xiaohongshu-post 发布一篇笔记，图片是 https://example.com/photo.jpg，
标题为"美食推荐"，内容为"今天发现了一家超好吃的餐厅"
```

## 必需参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **image_url** | string | 要上传的图片URL地址 | `http://192.168.215.200:8080/xhs.jpg` |
| **note_title** | string | 笔记标题内容（≤20字符） | `求滑雪搭子` |
| **note_content** | string | 笔记正文内容（≤1000字符） | `求望京滑雪搭子` |

## 执行流程

### 步骤1：导航到发布页面

**工具**：`mcp__chrome-server__chrome_navigate`

**参数**：
- `url`: `https://creator.xiaohongshu.com/publish/publish?source=official&from=menu&target=image`

**说明**：直接导航到小红书创作者发布页面，进入图文笔记发布界面。这是官方提供的创作者发布入口，跳过了从首页寻找入口的步骤。

---

### 步骤2：上传图片

**工具**：`mcp__chrome-server__chrome_input_upload_file`

**参数**：
- `sourceType`: `"url"`
- `multiple`: `true`
- `files`: `[{"sourceType": "url", "url": "{image_url}"}]`
- `inputSelector`: `"input[type='file']"`
- `timeout`: `10000`

**说明**：使用 chrome_input_upload_file 工具上传指定的图片文件。图片来源支持URL方式，工具会自动下载并上传到小红书。上传成功后页面会显示图片预览。

**参数占位符**：
- `{image_url}`：会被替换为用户提供的图片URL

---

### 步骤3：点击标题输入框

**工具**：`mcp__chrome-server__chrome_click_element`

**参数**：
- `selector`: `".title-container .d-input .d-text"`

**说明**：点击标题输入框使其获得焦点，为后续填写标题做准备。这一步确保输入框处于激活状态。

---

### 步骤4：填写标题

**工具**：`mcp__chrome-server__chrome_fill_or_select`

**参数**：
- `selector`: `".title-container .d-input .d-text"`
- `value`: `"{note_title}"`

**说明**：在标题输入框中填写笔记标题。小红书标题限制为20个字符，超出部分会被截断。

**参数占位符**：
- `{note_title}`：会被替换为用户提供的标题内容

---

### 步骤5：点击正文编辑区域

**工具**：`mcp__chrome-server__chrome_click_element`

**参数**：
- `selector`: `".tiptap.ProseMirror"`

**说明**：点击正文编辑区域使其获得焦点。正文编辑器使用的是 TipTap 富文本编辑器，需要先点击激活。

---

### 步骤6：填写正文内容

**工具**：`mcp__chrome-server__chrome_fill_or_select`

**参数**：
- `selector`: `"div[contenteditable=\"true\"][role=\"textbox\"].tiptap.ProseMirror"`
- `value`: `"{note_content}"`

**说明**：在正文编辑区域填写笔记内容。使用更精确的 selector 定位到可编辑的 div 元素。小红书正文限制为1000个字符。

**参数占位符**：
- `{note_content}`：会被替换为用户提供的正文内容

---

### 步骤7：发布笔记

**工具**：`mcp__chrome-server__chrome_click_element`

**参数**：
- `selector`: `"button.d-button.publishBtn"`

**说明**：点击发布按钮完成笔记发布。发布成功后页面会跳转到创作中心，显示发布的笔记。这是整个流程的最终步骤。

**最终结果**：此步骤完成后，笔记发布成功。

---

### 步骤8：获取发布结果数据

**工具**：`web-data-extractor` skill

**调用方式**：
调用 web-data-extractor skill 提取发布笔记后页面显示的数据信息

## 注意事项

### 平台特性

1. **账号登录要求**
   - 必须已登录小红书创作者账号
   - 建议使用 chrome-server 的持久化 session 保持登录状态

2. **内容限制**
   - 图片格式：jpg、png、webp
   - 图片大小：单张 < 20MB
   - 标题长度：≤ 20 字符
   - 正文长度：≤ 1000 字符

3. **发布频率**
   - 避免短时间内频繁发布
   - 建议间隔至少 5 分钟
   - 过于频繁可能触发平台限制

4. **页面稳定性**
   - 小红书创作者平台会定期更新
   - selector 可能因页面改版而失效
   - 如遇失效，需要更新对应的 selector

### 常见问题

#### 问题1：图片上传失败

**症状**：
- chrome_input_upload_file 执行成功但页面无图片预览
- 或报错 "File upload operation failed"

**解决方案**：
1. 检查图片URL是否可访问（在浏览器中打开测试）
2. 确认图片格式符合要求（jpg/png/webp）
3. 检查图片大小是否超过20MB
4. 如果是网络问题，增加 timeout 参数（如 30000）

---

#### 问题2：标题或正文填写失败

**症状**：
- chrome_fill_or_select 执行成功但输入框仍为空
- 或内容被截断

**解决方案**：
1. 确认已执行点击步骤（步骤3或步骤5）使输入框获得焦点
2. 检查 selector 是否正确（可用 chrome_get_interactive_elements 验证）
3. 如果内容包含特殊字符，确保正确转义
4. 标题超过20字符会被自动截断，正文超过1000字符同理

---

#### 问题3：发布按钮点击无反应

**症状**：
- 点击发布按钮后页面无变化
- 或出现错误提示

**解决方案**：
1. 检查是否所有必填项都已填写（图片、标题、正文）
2. 查看页面是否有错误提示（如内容违规）
3. 确认账号状态正常（未被限制发布权限）
4. 尝试手动刷新页面后重新执行流程

---

#### 问题4：selector 失效

**症状**：
- 找不到页面元素
- chrome_click_element 或 chrome_fill_or_select 报错

**解决方案**：
1. 小红书平台更新导致页面结构变化
2. 使用 chrome_get_web_content 或 chrome_screenshot 查看当前页面结构
3. 使用 chrome_get_interactive_elements 查找新的 selector
4. 更新 Skill 中的 selector 为新值
5. 考虑使用 Task Tool 动态获取 selector

## 输出示例

执行成功后的返回信息：
```
✅ 小红书笔记发布成功！

📝 笔记信息：
- 标题：求滑雪搭子
- 正文：求望京滑雪搭子
- 图片：已上传 1 张

🔗 发布结果：
- 状态：发布成功
- 页面已跳转到创作中心
```

## 版本信息

- **当前版本**：1.0.0
- **创建日期**：2025-11-18
- **平台版本**：小红书创作者平台 2024
- **测试状态**：已测试通过
