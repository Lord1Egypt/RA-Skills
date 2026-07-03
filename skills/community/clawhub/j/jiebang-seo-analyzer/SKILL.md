---
name: jiebang-seo-analyzer
description: 网站SEO分析与元数据提取工具 - 提取网页元信息（标题、描述、OG标签等）并执行SEO健康检查，获取优化建议。当用户提到SEO分析、网站元数据、网页标题描述提取、SEO检查、网页优化建议等需求时使用此技能。
---

# 捷帮SEO分析

提取网页元数据并执行SEO健康检查的专业工具。

## 核心能力

### 1. 元数据提取 (meta-extract)
提取网页的元信息，包括：
- 网页标题 (title)
- 网页描述 (description)
- 关键词 (keywords)
- Open Graph 标签 (og:title, og:description, og:image 等)
- Twitter Card 标签
- canonical URL
- 移动端适配标签

### 2. SEO健康检查 (seo-check)
对网页进行全面的SEO健康检查，包括：
- 标题标签检查（长度、是否缺失、是否重复）
- 描述标签检查
- 关键词使用分析
- 图片ALT属性检查
- 链接有效性检查
- 页面加载速度建议
- 移动端友好度
- 结构化数据检测

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 要分析的网页URL（需包含http://或https://） |

## 输出格式

### 元数据提取结果
```json
{
  "success": true,
  "data": {
    "title": "网页标题",
    "description": "网页描述",
    "keywords": "关键词1, 关键词2",
    "og": {
      "title": "OG标题",
      "description": "OG描述",
      "image": "OG图片URL"
    },
    "twitter_card": "summary_large_image",
    "canonical": "规范URL"
  }
}
```

### SEO检查结果
```json
{
  "success": true,
  "data": {
    "score": 85,
    "checks": [
      {"item": "标题标签", "status": "pass", "message": "标题长度合适"},
      {"item": "描述标签", "status": "warning", "message": "描述偏短，建议120字符以上"},
      {"item": "图片ALT", "status": "fail", "message": "发现3张图片缺少ALT属性"}
    ],
    "suggestions": [
      "建议为所有图片添加alt属性",
      "页面加载时间较长，建议优化"
    ]
  }
}
```

## 使用示例

**示例1：提取网页元数据**
```
输入：帮我提取 https://example.com 的元数据
输出：{
  "title": "Example Domain",
  "description": "这是一个示例网站",
  "og:image": "https://example.com/og-image.jpg"
}
```

**示例2：SEO健康检查**
```
输入：检查 https://example.com 的SEO健康状况
输出：{
  "score": 85,
  "issues": ["缺少meta keywords", "2张图片缺少ALT"],
  "suggestions": ["建议添加页面描述"]
}
```

## 注意事项

- URL必须以 http:// 或 https:// 开头
- 对于需要登录的网页可能无法获取完整信息
- 检查结果仅供参考，具体优化需结合业务需求
