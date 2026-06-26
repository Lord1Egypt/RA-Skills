---
name: parse-dedao
description: 解析"得到"笔记分享链接（支持提取正文和下载图片）。自动提取得到（dedao.cn）分享链接的正文内容，并支持将文章中的图片保存到本地。当用户发送得到笔记分享链接时使用此技能。
---

# 解析得到笔记分享链接

## 功能

1. **提取正文内容** - 自动识别并提取文章正文
2. **下载文章图片** - 将文章中的主要图片保存到本地目录

## 使用方法

当用户发送得到笔记分享链接时，自动解析并保存内容。

### 输入
- **URL**: 得到笔记分享链接，格式如：`https://www.dedao.cn/share/packet?packetId=xxx`

### 输出
- **标题**: 文章标题
- **正文**: 清洗后的文章内容
- **图片**: 保存到 `./images/` 目录

## API 使用

```javascript
const { parsePage, parseDedao } = require('./parse.js');

// 通用解析（支持任意网页）
const result = await parsePage(url, {
  saveImages: true,           // 是否保存图片
  outputDir: './downloads',   // 图片保存目录
  contentSelectors: [...],     // 自定义内容选择器
  imageSelectors: [...]        // 自定义图片选择器
});

// 得到笔记专用
const result = await parseDedao(url, {
  saveImages: true,
  outputDir: './images'
});
```

## 返回值

```javascript
{
  success: true,
  title: '文章标题',
  content: '文章正文内容',
  images: [
    { originalUrl: 'https://...', localPath: 'D:/.../image_1.jpg' },
    { originalUrl: 'https://...', localPath: 'D:/.../image_2.jpg' }
  ],
  error: null
}
```

## 依赖

- Playwright
- Chromium 浏览器

## 注意事项

- 图片默认保存到 `./images/` 目录
- 图片按序号命名：`image_1.jpg`, `image_2.jpg` 等
- 每个文章会创建独立的时间戳子目录
