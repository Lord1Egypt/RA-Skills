---
name: lanxin-link-card
version: 1.0.0
description: 蓝信官方链接卡片发送能力，支持发送包含链接的卡片消息。
metadata: {"clawdbot":{"emoji":"🔗"},"openclaw":{"always":true}}
triggers:
- 蓝信
- 发链接
- 发链接卡片
- 发送链接
- 发送链接卡片
- 链接卡片
- 链接
- 跳转链接
priority: 100
---

# 蓝信链接卡片发送规则（必须严格遵守）

## 核心规则（绝对禁止违反）
1. **用户要求发送链接，必须直接输出 JSON 格式的 linkCard 消息**
2. **JSON 必须包含所有必填字段**
3. **禁止说“无法发送”“不支持”“暂时不能”等拒绝话术**
4. **禁止解释 JSON 格式，直接输出即可**
5. **禁止输出任何其他文本，只输出 JSON**
6. **禁止使用 Markdown 代码块包裹 JSON**
7. **禁止输出 `<lxfile>` 或 `<lximg>` 标签**

---

## 发送链接卡片（必须这样输出）
**注意：必须直接输出 JSON，不要添加任何其他文本，不要使用 Markdown 代码块包裹！**

正确格式：
{
  "linkCard": {
    "title": "卡片标题",
    "description": "卡片描述",
    "iconLink": "图片链接",
    "link": "点击跳转链接",
    "pcLink": "PC端点击跳转链接",
    "fromName": "来源名称",
    "fromIconLink": "来源图标链接"
  }
}

正确示例：
{
  "linkCard": {
    "title": "蓝信官网",
    "description": "蓝信官方网站，提供企业级移动办公解决方案",
    "iconLink": "https://www.lanxin.cn/favicon.ico",
    "link": "https://www.lanxin.cn",
    "pcLink": "https://www.lanxin.cn",
    "fromName": "蓝信",
    "fromIconLink": "https://www.lanxin.cn/favicon.ico"
  }
}

---

## 字段说明
- **title**（必填）：卡片标题
- **description**（选填）：卡片描述
- **iconLink**（选填）：卡片消息中展示的图片链接
- **link**（必填）：卡片链接
- **pcLink**（选填）：PC 端卡片链接
- **fromName**（选填）：卡片来源名称
- **fromIconLink**（选填）：卡片来源图片链接

---

## 严禁出现的错误行为
❌ 禁止：缺少必填字段
❌ 禁止：格式错误的 JSON
❌ 禁止：解释“这是 JSON”“系统会解析”
❌ 禁止：拒绝发送
❌ 禁止：只输出文字内容，不输出 JSON
❌ 禁止：输出任何其他文本，只输出 JSON
❌ 禁止：使用 Markdown 代码块包裹 JSON
❌ 禁止：输出 `<lxfile>` 或 `<lximg>` 标签
❌ 禁止：输出 Markdown 格式的文本
❌ 禁止：在 JSON 前后添加任何文字

## 你的行为准则
用户让你发送链接卡片 → **直接输出干净的 JSON** → 不要多余描述 → 不要格式包裹 → 完成。