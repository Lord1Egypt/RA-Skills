---
name: noon-product-count
description: Noon 商品数量统计工具。输入阿拉伯语关键词，在 noon.com 沙特站搜索，返回搜索结果的商品数量。
---

# Noon 商品数量统计工具

## 功能

使用 Chrome 浏览器自动化，在 noon.com/saudi-ar 搜索阿拉伯语关键词，返回搜索结果的总数量。

## 使用方法

### 命令行

```bash
node ~/.openclaw/workspace/skills/noon-product-count/index.js "阿语关键词"
```

### 示例

```bash
node ~/.openclaw/workspace/skills/noon-product-count/index.js "سماعات بلوتوث"
```

### 批量搜索

```bash
node ~/.openclaw/workspace/skills/noon-product-count/index.js "سماعات" "بلوتوث" "لاسلكي"
```

## 输出示例

```
============================================================
🔍 搜索关键词: "سماعات بلوتوث"
============================================================

📊 商品数量: 28,412
```

## 技术说明

- 使用 puppeteer-extra + stealth 反检测
- 自动绕过 reCAPTCHA 验证
- 从页面提取 "X نتائج البحث" 格式的总数量

## 依赖

- puppeteer-extra
- puppeteer-extra-plugin-stealth
- puppeteer

## 安装依赖

```bash
cd ~/.openclaw/workspace/skills/noon-product-count
npm install puppeteer-extra puppeteer-extra-plugin-stealth puppeteer
```
