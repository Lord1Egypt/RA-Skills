---
name: web-data-extractor
description: 通过Chrome MCP服务器执行内置脚本提取页面结构化数据。当用户需要从当前打开的网页中提取、抓取或获取结构化数据时使用此skill，包括产品信息、社交媒体内容、表格、列表或页面上任何可见的结构化内容。
---

# 网页数据提取器

## 概述

此skill通过执行内联的 DOM 提取脚本，从网页中提取结构化数据。通过以下流程：
1. 直接调用 `mcp__browser__chrome_execute_script` 执行内联脚本（脚本内部会自动滚动页面触发所有懒加载内容）
2. 使用 `async () => await (脚本)` 等待Promise完成并获取JSON结果
3. 返回包含文本节点（带上下文）、链接、标题的结构化数据

**🚨 最关键要求**：
调用 `mcp__browser__chrome_execute_script` 工具时，**必须完整传递步骤2中定义的 jsScript 参数**，不能省略、简化或修改任何字符，否则会导致数据提取失败！
 



**核心原则**：自动触发数据加载，一次性提取所有结构化内容及上下文，智能过滤和优化数据。


**前置要求**：
- Chrome MCP服务器已启动并连接
- 无需外部插件或扩展

## 何时使用此Skill

当用户提出以下请求时调用此skill：
- 从当前网页提取数据
- 抓取网站中的结构化信息
- 获取产品详情、价格、评论或其他电商数据
- 提取社交媒体帖子、评论或互动统计数据
- 导出网页中的表格或列表数据
- 获取任何可见的结构化内容的JSON格式

触发此skill的用户请求示例：
- "提取这个页面的所有产品信息"
- "把这个表格的数据转成JSON"
- "抓取这个社交媒体帖子的内容"
- "获取这个页面的结构化数据"
- "这个页面上有什么数据？"
- "提取当前网页的内容"

## 数据提取流程

### 步骤1：验证Chrome MCP工具可用性

在提取数据之前，确认以下工具可用：
- `mcp__browser__chrome_execute_script` - 用于执行JavaScript脚本
如果工具不可访问，告知用户需要启动并连接Chrome MCP服务器。

### 步骤2：执行提取脚本获取DOM数据

**🚨 关键要求：必须完整传递下面的 jsScript 参数，不能省略、简化或修改任何部分！**

直接调用 `mcp__browser__chrome_execute_script` 工具执行内联的提取脚本：

**工具参数（必须严格按照下面的完整参数调用）**：
- `tabId`: 目标标签页ID（可选，不提供则使用当前活动标签页）
- `jsScript`: **必须使用下面的完整脚本，一个字符都不能少** → `async () => await ((async () => { 'use strict'; window.scrollTo({ top: 0, behavior: 'instant' }); await new Promise(resolve => setTimeout(resolve, 300)); const documentHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight, document.body.clientHeight, document.documentElement.clientHeight); window.scrollTo({ top: documentHeight, behavior: 'smooth' }); await new Promise(resolve => setTimeout(resolve, 1500)); window.scrollTo({ top: 0, behavior: 'smooth' }); await new Promise(resolve => setTimeout(resolve, 1000)); function shouldSkipElement(element) { if (!element) return true; const skipClassPrefixes = ['vjs-', 'video-js', 'plyr', 'jwplayer', 'ad-', 'advertisement', 'cookie-', 'gdpr-']; if (element.className && typeof element.className === 'string') { const classes = element.className.toLowerCase(); if (skipClassPrefixes.some(prefix => classes.includes(prefix))) { return true; } } let parent = element.parentElement; let depth = 0; while (parent && depth < 3) { if (parent.className && typeof parent.className === 'string') { const parentClasses = parent.className.toLowerCase(); if (skipClassPrefixes.some(prefix => parentClasses.includes(prefix))) { return true; } } parent = parent.parentElement; depth++; } try { const style = window.getComputedStyle(element); if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') { return true; } } catch (e) { } return false; } function extractFilenameFromUrl(url) { if (!url) return url; try { const pathname = url.split('?')[0].split('#')[0]; const parts = pathname.split('/'); const filename = parts[parts.length - 1]; return filename || url; } catch (e) { return url; } } function extractImagesFromElement(element) { if (!element) return []; const images = []; const imgElements = element.querySelectorAll('img[src], img[data-src]'); for (let i = 0; i < imgElements.length; i++) { const img = imgElements[i]; const src = img.src || img.getAttribute('data-src'); if (src && src.trim() !== '') { images.push(extractFilenameFromUrl(src)); } } const allElements = [element, ...element.querySelectorAll('*')]; for (let i = 0; i < allElements.length; i++) { const el = allElements[i]; try { const style = window.getComputedStyle(el); const bgImage = style.backgroundImage; if (bgImage && bgImage !== 'none') { const matches = bgImage.match(/url\\(['"]?([^'"()]+)['"]?\\)/g); if (matches) { matches.forEach(match => { const url = match.replace(/url\\(['"]?([^'"()]+)['"]?\\)/, '$1'); if (url && url.trim() !== '' && !url.startsWith('data:')) { images.push(extractFilenameFromUrl(url)); } }); } } } catch (e) { } } return [...new Set(images)]; } function extractSVGPathsFromElement(element) { if (!element) return null; const paths = []; const pathElements = element.querySelectorAll('svg path[d]'); for (let i = 0; i < pathElements.length; i++) { const d = pathElements[i].getAttribute('d'); if (d && d.trim() !== '') { paths.push(d.trim()); } } return paths.length > 0 ? paths.join(' ') : null; } function extractTextWithContext(element) { if (!element) return []; if (element.tagName && ['SCRIPT', 'STYLE', 'NOSCRIPT', 'HEAD'].includes(element.tagName)) { return []; } let results = []; if (element.shadowRoot) { const shadowResults = extractTextWithContext(element.shadowRoot); results.push(...shadowResults); } if (element.childNodes && element.childNodes.length > 0) { for (let i = 0; i < element.childNodes.length; i++) { const node = element.childNodes[i]; if (node.nodeType === Node.TEXT_NODE) { const text = node.textContent.trim(); if (text) { const parent = node.parentElement; const grandParent = parent ? parent.parentElement : null; const greatGrandParent = grandParent ? grandParent.parentElement : null; if (shouldSkipElement(parent) || shouldSkipElement(grandParent) || shouldSkipElement(greatGrandParent)) { continue; } const nodeData = { text: text }; if (parent && parent.className) { nodeData.className = parent.className; } if (grandParent && grandParent.className) { nodeData.parentClassName = grandParent.className; } if (greatGrandParent && greatGrandParent.className) { nodeData.grandParentClassName = greatGrandParent.className; } if (parent) { const parentImages = extractImagesFromElement(parent); if (parentImages.length > 0) { nodeData.parentImages = parentImages; } } if (grandParent) { const grandParentImages = extractImagesFromElement(grandParent); if (grandParentImages.length > 0) { nodeData.grandParentImages = grandParentImages; } } let svgPaths = null; if (parent) { svgPaths = extractSVGPathsFromElement(parent); } if (!svgPaths && grandParent) { svgPaths = extractSVGPathsFromElement(grandParent); } if (!svgPaths && greatGrandParent) { svgPaths = extractSVGPathsFromElement(greatGrandParent); } if (svgPaths && svgPaths.length < 1000) { nodeData.svg = svgPaths; } results.push(nodeData); } } else if (node.nodeType === Node.ELEMENT_NODE) { const childResults = extractTextWithContext(node); results.push(...childResults); } } } return results; } function deduplicateImagesGlobally(nodes) { const urlCounts = new Map(); nodes.forEach(node => { ['parentImages', 'grandParentImages'].forEach(field => { if (node[field]) { node[field].forEach(url => { urlCounts.set(url, (urlCounts.get(url) || 0) + 1); }); } }); }); const seenUrls = new Map(); nodes.forEach(node => { ['parentImages', 'grandParentImages'].forEach(field => { if (node[field]) { node[field] = node[field].filter(url => { const totalCount = urlCounts.get(url) || 0; if (totalCount <= 2) { return true; } const currentCount = seenUrls.get(url) || 0; if (currentCount < 2) { seenUrls.set(url, currentCount + 1); return true; } return false; }); if (node[field].length === 0) { delete node[field]; } } }); }); return nodes; } function deduplicateNodesByClassNames(nodes) { const seenKeys = new Set(); nodes.forEach(node => { const hasClassNames = node.className || node.parentClassName || node.grandParentClassName; if (hasClassNames) { const key = (node.className || '') + '|' + (node.parentClassName || '') + '|' + (node.grandParentClassName || ''); if (seenKeys.has(key)) { delete node.className; delete node.parentClassName; delete node.grandParentClassName; } else { seenKeys.add(key); } } }); return nodes; } let textNodes = extractTextWithContext(document.body); textNodes = deduplicateImagesGlobally(textNodes); textNodes = deduplicateNodesByClassNames(textNodes); const result = { url: window.location.href, title: document.title, textNodes: textNodes }; window.extractedData = result; console.log('✅ v0.05'); return JSON.stringify(result); })())`
- `world`: `MAIN`（在页面主上下文中执行）
- `timeout`: `15000`（超时时间15秒，因为包含智能滚动和数据提取）

**⚠️ 特别强调**：
- 上面的 `jsScript` 参数值必须**完整复制**，不能简化、不能用变量替代、不能省略任何部分
- 这是一个完整的内联脚本，包含智能滚动 + 数据提取 + 控制台输出的完整逻辑
- 任何修改都可能导致数据提取不完整或失败

**⚠️ 重要说明**：
- 脚本会自动执行智能滚动策略触发所有懒加载内容，然后提取数据
- 脚本返回Promise，需要使用 `async () => await (脚本内容)` 来获取结果
- 返回的数据是完整的 JSON 字符串（已经用 `JSON.stringify()` 包裹）
- 返回的数据包含：url、title、textNodes（文本节点数组）




**脚本执行流程**：
1. 滚动到页面顶部（重置位置）
2. 滚动到页面底部并等待1.5秒（触发所有懒加载内容）
3. 滚动回顶部并等待1秒（确保内容稳定）
4. 从 document.body 开始提取所有文本节点及其上下文（包括 Shadow DOM、相关图片URL 和 SVG path 数据）
5. **🔥 执行全局图片URL去重**（只对出现次数>2的URL去重，保留前2次；URL已转换为文件名格式）
6. **🔥 执行className字段去重**（相同的 className 组合只保留第一次出现，后续节点删除 className 字段但保留 text、images 和 svg 字段）
7. **🆕 提取SVG path信息**（从父、祖父、曾祖父元素中查找SVG图标，只保留长度<1000的path数据）
8. 打印版本号到控制台（v0.05）
9. 返回结构化的 JSON 字符串（包装在Promise中）

**图片URL处理逻辑说明**：
- 所有图片URL自动转换为文件名格式（只保留最后的文件名部分，如 `like_icon.png`）
- 去重策略：只对出现次数超过2次的URL进行去重，保留前2次出现
- 如果某个图片文件名在全局只出现1-2次，则全部保留
- 如果某个图片文件名在全局出现3次及以上，则只保留前2次，后续删除

**className 去重逻辑说明**：
- 遍历所有文本节点，基于 `className + parentClassName + grandParentClassName` 组合生成唯一键
- 对于相同的组合，**只保留第一次出现的 className 字段**，后续节点删除这些字段
- **所有节点的 text 字段和 images 字段都会保留**，不会删除任何节点
- 这样可以大幅减少重复的 className 数据，同时保留所有文本内容

**返回数据格式**（JSON 字符串，优化后）：
```json
{
  "url": "https://example.com/page",
  "title": "页面标题",
  "textNodes": [
    {
      "text": "123",
      "className": "like-count",
      "parentClassName": "stats-wrapper",
      "grandParentClassName": "video-info",
      "parentImages": ["like_icon.png"]
    },
    {
      "text": "456",
      "parentImages": ["share_icon.png"]
    },
    {
      "text": "274",
      "svg": "M-4.644999980926514,4.482999801635742 C-7.25,7.818999767303467..."
    },
    {
      "text": "评论"
    },
    {
      "text": "1211"
    }
  ]
}
```

**🆕 SVG Path 字段说明**：
- 从 v0.05 版本开始，新增 `svg` 字段用于存储文本节点关联的 SVG 图标路径数据
- 提取逻辑：在文本节点的父、祖父、曾祖父元素中查找 SVG path 元素
- 长度限制：只保留长度小于 1000 字符的 path 数据（过滤复杂动画SVG）
- 用途：通过 SVG path 的形状特征推断数字的含义（如评论图标、点赞图标等）

**💡 如何利用 SVG Path 推断数字含义**：
当文本节点包含 `svg` 字段时，应该根据 path 数据推断该数字代表的含义：
- **评论图标特征**：通常包含聊天气泡形状，path中会有圆角矩形、三角形（气泡尾巴）等几何形状
- **点赞图标特征**：通常为竖起的大拇指或爱心形状
- **分享图标特征**：通常为箭头、链接符号或分享符号
- **收藏图标特征**：通常为星星、书签或旗帜形状
- **播放/观看图标特征**：通常为眼睛、播放按钮（三角形）等形状

通过分析 `svg` 字段的 path 数据，可以更准确地判断纯数字节点代表的含义。

**⚠️ 通用的语义映射规则**：
语义字段	等价表达
阅读量	次观看、次播放、阅读、浏览、views、plays
点赞量	赞、点赞、likes、👍
评论量	评论、条评论、comments、replies
转发量	转发、分享、shares、retweets
收藏量	收藏、favorites、bookmarks