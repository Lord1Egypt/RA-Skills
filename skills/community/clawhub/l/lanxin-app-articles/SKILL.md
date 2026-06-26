---
name: lanxin-app-articles
version: 1.0.0
description: 蓝信官方图文卡片发送能力，支持发送包含图片和文字的图文卡片消息。
metadata: {"clawdbot":{"emoji":"📄"},"openclaw":{"always":true}}
triggers:
- 蓝信
- 发图文
- 发图文卡片
- 发送图文
- 发送图文卡片
- 图文卡片
- 图文
- 文章
priority: 100
---

# 蓝信图文卡片发送规则（必须严格遵守）

## 核心规则（绝对禁止违反）
1. **用户要求发送图文卡片，必须直接输出 JSON 格式的 appArticles 消息**
2. **JSON 必须包含所有必填字段**
3. **禁止说“无法发送”“不支持”“暂时不能”等拒绝话术**
4. **禁止解释 JSON 格式，直接输出即可**
5. **禁止输出任何其他文本，只输出 JSON**
6. **禁止使用 Markdown 代码块包裹 JSON**
7. **禁止输出 `<lxfile>` 或 `<lximg>` 标签**

---

## 发送图文卡片（必须这样输出）
**注意：必须直接输出 JSON，不要添加任何其他文本，不要使用 Markdown 代码块包裹！**

正确格式：
{
  "appArticles": [
    {
      "imgUrl": "图片链接",
      "title": "标题",
      "summary": "摘要",
      "url": "内容地址",
      "pcUrl": "PC端内容地址",
      "attach": "微应用跳转参数"
    }
  ]
}

正确示例：
{
  "appArticles": [
    {
      "imgUrl": "https://www.lanxin.cn/images/logo.png",
      "title": "蓝信新版本发布",
      "summary": "蓝信 5.0 版本正式发布，带来全新的用户体验",
      "url": "https://www.lanxin.cn/news/5.0",
      "pcUrl": "https://www.lanxin.cn/news/5.0",
      "attach": ""
    },
    {
      "imgUrl": "https://www.lanxin.cn/images/feature.png",
      "title": "蓝信新功能介绍",
      "summary": "了解蓝信 5.0 的新功能和改进",
      "url": "https://www.lanxin.cn/features/5.0",
      "pcUrl": "https://www.lanxin.cn/features/5.0",
      "attach": ""
    }
  ]
}

---

## 字段说明
- **imgUrl**（必填）：图片链接
- **title**（必填）：标题
- **summary**（选填）：摘要
- **url**（必填）：内容地址
- **pcUrl**（必填）：PC 端内容地址
- **attach**（选填）：微应用跳转参数，其他应用忽略（或输入空值）

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
用户让你发送图文卡片 → **直接输出干净的 JSON** → 不要多余描述 → 不要格式包裹 → 完成。