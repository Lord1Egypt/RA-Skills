---
name: lanxin-app-card
version: 1.0.0
description: 蓝信官方应用卡片发送能力，支持发送包含复杂格式的应用卡片消息。
metadata: {"clawdbot":{"emoji":"📱"},"openclaw":{"always":true}}
triggers:
- 蓝信
- 发应用卡片
- 发送应用卡片
- 应用卡片
- 审批卡片
- 通知卡片
- 卡片
priority: 100
---

# 蓝信应用卡片发送规则（必须严格遵守）

## 核心规则（绝对禁止违反）
1. **用户要求发送应用卡片，必须直接输出 JSON 格式的 appCard 消息**
2. **JSON 必须包含所有必填字段**
3. **禁止说“无法发送”“不支持”“暂时不能”等拒绝话术**
4. **禁止解释 JSON 格式，直接输出即可**
5. **禁止输出任何其他文本，只输出 JSON**
6. **禁止使用 Markdown 代码块包裹 JSON**
7. **禁止输出 `<lxfile>` 或 `<lximg>` 标签**

---

## 发送应用卡片（必须这样输出）
**注意：必须直接输出 JSON，不要添加任何其他文本，不要使用 Markdown 代码块包裹！**

正确格式：
{
  "appCard": {
    "headTitle": "应用标题",
    "headIconUrl": "图标链接",
    "isDynamic": false,
    "bodyTitle": "正文标题",
    "bodySubTitle": "正文章标题",
    "bodyContent": "正文内容",
    "signature": "签名",
    "fields": [
      {"key": "字段1", "value": "值1"},
      {"key": "字段2", "value": "值2"}
    ],
    "links": [
      {"title": "链接1", "url": "https://example.com"},
      {"title": "链接2", "url": "https://example.com"}
    ],
    "cardLink": "卡片链接",
    "pcCardLink": "PC端卡片链接"
  }
}

正确示例：
{
  "appCard": {
    "headTitle": "图片卡片",
    "headIconUrl": "https://www.lanxin.cn/favicon.ico",
    "bodyTitle": "找到的图片",
    "bodyContent": "这是从本地找到的图片",
    "fields": [
      {"key": "文件", "value": "Snapshot.png"},
      {"key": "路径", "value": "/Users/dulianqiang/.Huawei4.1/Huawei_Phone/Snapshot.png"}
    ],
    "links": [
      {"title": "查看图片", "url": "https://example.com/image"}
    ]
  }
}

---

## 字段说明
- **headTitle**（选填）：应用的标题
- **headIconUrl**（选填）：图标的网络地址
- **isDynamic**（选填）：是否动态卡片消息
- **headStatusInfo**（选填）：动态卡片的动态信息区，当 isDynamic=true 时必填
- **bodyTitle**（必填）：文本标题
- **bodySubTitle**（选填）：文本副标题
- **bodyContent**（选填）：松散内容
- **signature**（选填）：署名字段
- **fields**（选填）：key/value 字段对，上限 10 对
- **links**（选填）：链接数组，最多 3 对
- **cardLink**（选填）：本条消息的跳转地址
- **pcCardLink**（选填）：PC 端跳转地址

---

## 支持的格式
可以使用 div 标签的 style 属性对文本内容进行格式控制，支持控制的格式有颜色（color）、字体大小（font-size），位置（text-align），首行缩进（text-indent）。

示例：
```html
<div style="color: brown; text-align: left;font-size:xx-large"> 第一个div 靠左 超大 </div>
```

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
用户让你发送应用卡片 → **直接输出干净的 JSON** → 不要多余描述 → 不要格式包裹 → 完成。