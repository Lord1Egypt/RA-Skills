---
name: lanxin-media
version: 1.0.0
description: 蓝信官方媒体发送能力，支持发送图片、文件。使用 <lximg> <lxfile> 标签发送，系统自动解析上传。
metadata: {"clawdbot":{"emoji":"📸"},"openclaw":{"always":true}}
triggers:
- 蓝信
- 发图片
- 发文件
- 发送图片
- 发送文件
- 图片
- 文件
- 本地文件
- 本地图片
- 文档
- 表格
priority: 99
---

# 蓝信媒体发送规则（必须严格遵守）

## 核心规则（绝对禁止违反）
1. **用户要求发图片/文件，必须直接输出 <lximg> 或 <lxfile> 标签**
2. **标签必须单独成行，不使用任何 markdown、代码块、加粗、斜体**
3. **禁止把标签放在 ``` 代码块中**
4. **禁止说“无法发送”“不支持”“暂时不能”等拒绝话术**
5. **禁止解释标签作用，直接输出即可**
6. **一次只发送一个文件或一张图片**
7. **路径必须真实有效，格式干净无多余符号**

---

## 发送图片（必须这样输出）
**注意：发送图片时必须使用 `<lximg>` 标签，而不是 `<lxfile>` 标签！**
**注意：SVG 文件请使用 `<lxfile>` 标签发送，而不是 `<lximg>` 标签！**

格式：
<lximg>文件路径或URL</lximg>

示例（正确）：
这是你要的图片：
<lximg>/Users/user/photo.jpg</lximg>

示例（正确）：
<lximg>https://example.com/image.png</lximg>

## 发送 SVG 文件（必须这样输出）
**注意：SVG 文件必须使用 `<lxfile>` 标签，而不是 `<lximg>` 标签！**

格式：
<lxfile>文件路径或URL</lxfile>

示例（正确）：
<lxfile>/Users/user/image.svg</lxfile>

示例（正确）：
<lxfile>https://example.com/image.svg</lxfile>

## 发送文件（必须这样输出）
**注意：发送文件时必须使用 `<lxfile>` 标签，而不是 `<lximg>` 标签！**

格式：
<lxfile>文件路径或URL</lxfile>

示例（正确）：
文件已发送：
<lxfile>/Users/user/report.pdf</lxfile>

示例（正确）：
<lxfile>https://example.com/document.pdf</lxfile>

---

## 支持的闭合格式（任选一种）
<lximg>...</lximg>   或   <lximg>...</img>
<lxfile>...</lxfile> 或   <lxfile>...</file>

---

## 蓝信限制
- 图片/文件大小 ≤ 2MB
- 支持：png、jpg、jpeg、pdf、doc、docx、xls、xlsx、txt
- 视频、音频暂不支持

---

## 严禁出现的错误行为
❌ 禁止：```markdown <lxfile>...</lxfile> ```
❌ 禁止：**<lxfile>...</lxfile>**
❌ 禁止：` <lxfile>...`
❌ 禁止：解释“这是标签”“系统会解析”
❌ 禁止：拒绝发送
❌ 禁止：只输出文字内容，不输出标签

## 你的行为准则
用户让你发文件/图片 → **直接输出干净标签** → 不要多余描述 → 不要格式包裹 → 完成。