---
name: noon-product-search
description: Noon 商品搜索工具。输入阿拉伯语关键词，使用 Chrome 浏览器在 noon.com/saudi-ar 搜索，返回第一页所有商品的标题、评分、评价数和价格。
---

# Noon 商品搜索工具

## 功能

使用 Chrome 浏览器自动化，在 noon.com/saudi-ar 搜索阿拉伯语关键词，返回第一页所有商品的：
- 商品标题
- 评分
- 评价数
- 价格

## 使用方法

### 命令行

```bash
node ~/.openclaw/workspace/skills/noon-product-search/index.js "阿语关键词"
```

### 示例

```bash
node ~/.openclaw/workspace/skills/noon-product-search/index.js "عربة تسوق"
```

## 输出示例

```
============================================================
🔍 搜索: "عربة تسوق"
============================================================

📦 商品 1
   标题: عربة تسوق صغيرة محمولة...
   评分: 4.5
   评价数: (2,340)
   价格: 159 ر.س

📦 商品 2
   标题: ...
```

## 依赖

- Chrome 浏览器（带调试端口 9222）
- chrome-remote-interface

## 启动 Chrome 调试模式

```bash
open -a "Google Chrome" --args --remote-debugging-port=9222 --new-window "about:blank"
```

## 注意事项

- 确保 Chrome 调试端口 9222 已开启
- 首次运行会自动安装依赖
- 如果搜索结果为空，尝试增加等待时间
