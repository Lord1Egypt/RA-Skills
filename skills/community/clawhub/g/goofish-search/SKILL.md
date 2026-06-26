---
name: goofish-search
description: Use when user wants to search Xianyu/Goofish for products. Auto-search, filter merchants, sort by price, and output TOP results.
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [xianyu, goofish, search, shopping,二手]
    related_skills: [browser-marketplace-search]
---

# 闲鱼自动化搜索技能 - Goofish Search

## Overview

自动在闲鱼网站（goofish.com）搜索商品，应用严格筛选条件（排除商家/鱼小铺/回收广告），按价格升序排序，输出个人闲置商品列表。

**核心优势：**
- ✅ 自动排除商家（鱼小铺/超赞鱼小铺）
- ✅ 自动排除价格区间商品（如 "500-600"）
- ✅ 自动排除回收广告/笔记本/包装盒
- ✅ 价格升序排序，快速找到最低价
- ✅ 支持自定义筛选条件（价格/地区/成色）

**参考文档：**
- `references/goofish-dom-structure.md` — 闲鱼页面 DOM 结构和翻页栏 class 名称

## When to Use

- 用户说 "闲鱼搜索 XXX"
- 用户说 "帮我找闲鱼 XXX"
- 用户说 "闲鱼买 XXX"
- 用户说 "二手搜索 XXX"

**不适用于：**
- 非闲鱼平台搜索（如淘宝、京东）
- 全新商品购买（闲鱼主打二手）

## 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `keyword` | string | 是 | 搜索关键词 |
| `max_price` | number | 否 | 最高价格（元） |
| `min_price` | number | 否 | 最低价格（元） |
| `max_pages` | number | 否 | 最大翻页数，最少 3 页，默认 5 |
| `region` | string | 否 | 指定地区（如 "广东"） |
| `condition` | string | 否 | 成色要求（如 "全新"、"几乎全新"） |
| `sort` | string | 否 | 排序方式："price_asc"（价格从低到高）或 "price_desc"（从高到低） |

## 执行流程

### 步骤 1: 访问闲鱼并搜索

```
1. browser_navigate → https://www.goofish.com/search?q={keyword}
2. 等待 3 秒加载
3. browser_snapshot 获取页面结构
```

### 步骤 2: 应用筛选条件

```
1. 点击 "个人闲置" 筛选按钮（ref 含 "个人闲置" 文本）
2. 等待 2 秒刷新
3. 设置价格区间：
   - 找到最小价格输入框（textbox ref，placeholder 为 "¥"）
   - 使用 browser_type 输入 min_price（如 "1300"）
   - 找到最大价格输入框（textbox ref，placeholder 为 "¥"）
   - 使用 browser_type 输入 max_price（如 "2000"）
   - 点击确定按钮（button ref，文本为 "确定"）
4. 设置排序：
   - 找到 "价格" 排序按钮
   - 使用 browser_console 执行：
     ```javascript
     (() => {
       const allElements = document.querySelectorAll('*');
       for (const el of allElements) {
         if (el.textContent.trim() === '价格从低到高') {
           el.click();
           return { clicked: true };
         }
       }
       return { clicked: false };
     })();
     ```
5. 等待 2 秒刷新
6. browser_snapshot 获取筛选后结果
```

### 步骤 2.5: 设置价格范围（如有 min_price / max_price）

```
1. browser_snapshot 获取当前页结构
2. 找到价格输入区域的两个 textbox（min_price 和 max_price）
3. 使用 browser_type 在第一个 textbox 输入最低价格
4. 使用 browser_type 在第二个 textbox 输入最高价格
5. 找到"确定"按钮（button ref，位于价格输入框右侧）
6. 使用 browser_click 点击确定按钮
7. 等待 2 秒刷新
8. browser_snapshot 获取筛选后结果
```

**价格输入区域选择器：**
- 最低价格输入框：`textbox "¥"` (第一个)
- 最高价格输入框：`textbox "¥"` (第二个)
- 确定按钮：位于价格输入框右侧的 `button`，可能有 `disabled` 状态变化

### 步骤 2.6: 设置价格排序（如有 sort_by = "price_asc"）

```
1. browser_snapshot 获取当前页结构
2. 找到排序区域（含"综合"、"新降价"、"新发布"、"价格"等选项）
3. 点击"价格"文字，展开排序下拉菜单
4. 等待 1 秒
5. 点击"价格从低到高"选项
6. 等待 2 秒刷新
7. browser_snapshot 获取排序后结果
```

**排序选择器：**
- "价格"按钮：class 含 `search-select-title-container`，文本为"价格"
- "价格从低到高"：class 含 `search-select-item`，文本为"价格从低到高"
- "价格从高到低"：class 含 `search-select-item`，文本为"价格从高到低"

**注意：** 排序选项可能需要先点击"价格"展开下拉菜单，再点击具体排序方式。如果直接使用 `browser_console` 执行 `document.querySelector` + `.click()` 可能导致新标签页，建议使用 `browser_click` + ref 或 `browser_console` 包装在 IIFE 中。

### 步骤 3: 提取商品数据

从快照中提取每个商品卡片的：
- **标题**：商品名称文本
- **价格**：¥ 后的数字（解析为纯数字）
- **地区**：省份/城市
- **想要人数**：N人想要
- **链接**：从商品卡片的 `link` 元素中提取 `href`，格式为 `/item?id=xxx`，拼接为完整 URL `https://www.goofish.com/item?id=xxx`

**商品链接提取方法：**
```
从 browser_snapshot 中，每个商品卡片是一个 link 元素，其 ref 属性对应的元素包含：
- href 属性（如 /item?id=103468204167）
- 文本内容（包含标题、价格、地区等）

提取链接时，从快照的 link 元素中获取 href，拼接为：
https://www.goofish.com{href}
```

### 步骤 4: 智能筛选

排除以下商品：
```javascript
// 排除商家
if (seller.includes('鱼小铺') || seller.includes('超赞')) continue;

// 排除价格区间
if (price.includes('-') || price.includes('~')) continue;

// 排除回收广告
if (title.includes('回收') || title.includes('高价收')) continue;

// 排除笔记本/包装盒
if (title.includes('笔记本') || title.includes('包装盒')) continue;

// 排除 "XXX 起" 或 "面议"
if (price.includes('起') || price.includes('面议')) continue;
```

### 步骤 5: 翻页获取更多结果

**标准翻页流程（使用"到第X页"输入框）：**
```
1. browser_snapshot 获取当前页结构
2. 在翻页区域找到输入框（textbox ref）
3. 使用 browser_type 输入目标页码（如 "5"）
4. 找到确定按钮（button ref，文本为"确定"）
5. 使用 browser_click 点击确定按钮
6. 等待 3 秒加载
7. 重复步骤 1-6，直到达到 max_pages
```

**翻页选择器：**
```javascript
// 输入框：class 含 "search-pagination-to-page-input"
// 确认按钮：class 含 "search-pagination-to-page-confirm"
const input = document.querySelector('[class*="search-pagination-to-page-input"]');
const confirmBtn = document.querySelector('[class*="search-pagination-to-page-confirm"]');
input.value = '5';
confirmBtn.click();
```

**翻页栏 DOM 结构：**
```
<div class="search-pagination-pageitem-container--xxx">
  <button>←</button>                    ← 左箭头（上一页）
  <div class="...page-box...">1</div>   ← 页码
  <div class="...page-box-active...">2</div>  ← 当前页（高亮）
  <div class="...page-box...">3</div>   ← 页码
  ...
  <button>→</button>                    ← 右箭头（下一页）
</div>
<div class="search-pagination-to-page-container--xxx">
  到第 <input class="search-pagination-to-page-input--xxx"> 页
  <button class="search-pagination-to-page-confirm--xxx">确定</button>
</div>
```

### 步骤 6: 排序并输出

```
1. 按价格升序排序
2. 输出 TOP 10 结果
3. 生成价格统计
4. 保存商品列表到桌面（包含链接）
```

**保存商品列表（包含链接）：**
```
1. 从搜索结果中提取每个商品的 item_id
2. 构造商品链接：https://www.goofish.com/item?id={item_id}
3. 保存为 Markdown 文件到桌面：/home/k/桌面/闲鱼{关键词}搜索结果.md
4. 文件内容包含：商品列表（价格、标题、地区、想要人数、链接）
```

## 输出格式

```markdown
🦞 闲鱼 {关键词} 搜索结果

已应用严格筛选：**仅限个人闲置** + **单一价格** + **排除商家/回收广告**

### 📦 商品列表（价格升序）

| # | 价格 | 商品标题 | 地区 | 想要 | 链接 |
|---|------|----------|------|------|------|
| 1 | **¥550** | 佳能RF24-50镜头... | 江苏 | 41人 | [🔗查看](https://www.goofish.com/item?id=xxx) |
| 2 | **¥600** | 自用佳能RF24-50... | 甘肃 | - | [🔗查看](https://www.goofish.com/item?id=xxx) |
| ... | ... | ... | ... | ... | ... |

### 📊 价格统计
| 指标 | 价格 |
|------|------|
| **最低价** | ¥550（江苏，41人想要） |
| **最高价** | ¥750（湖南） |
| **平均价** | 约 ¥625 |

### 🔥 热门商品
1. **佳能RF24-50** - 41人想要（¥550）[🔗查看](https://www.goofish.com/item?id=xxx)
2. **佳能RF 24-50mm** - 7人想要（¥680）[🔗查看](https://www.goofish.com/item?id=xxx)

### ✅ 筛选说明
- 已排除商家（鱼小铺/超赞鱼小铺）
- 已排除价格区间商品
- 已排除回收广告/笔记本/包装盒
- 共扫描约 25 个商品，有效个人闲置 9 个
```
### 💾 保存结果
- 文件位置：/home/k/桌面/闲鱼{关键词}搜索结果.md
- 包含所有商品的链接，可直接点击访问
```

## 风控注意事项

1. **使用真实 Chrome**：通过 CDP 连接已登录闲鱼的浏览器
2. **操作间隔**：输入后等待 2 秒，翻页等待 3 秒
3. **避免过快点击**：每次点击间隔 0.8-1 秒
4. **页面结构变化**：若选择器失效，使用 `browser_vision` 截图识别

## Common Pitfalls

1. **Goofish 是 SPA**：DOM 查询可能不稳定，优先用 `browser_snapshot` 而非 `browser_console`
2. **需要翻页**：单页结果有限，必须翻页获取完整数据
3. **商家伪装个人**：部分商家冒充个人卖家，需检查 "鱼小铺" 标识
4. **价格区间商品**：如 "500-600" 表示商家多规格，应排除
5. **登录状态**：未登录可能看到有限结果，确保 Chrome 已登录
6. **翻页必须用 browser_type + browser_click**：JavaScript DOM 操作（`document.querySelector` + `.click()`）会导致浏览器跳转到新标签页。必须使用 `browser_type` 输入页码 + `browser_click` 点击确定按钮
7. **翻页后 DOM 更新**：翻页后页面 DOM 会重新渲染，之前的 ref ID 可能失效，需要重新获取 snapshot
8. **确认按钮选择器**：确定按钮 class 含 `search-pagination-to-page-confirm`，输入框 class 含 `search-pagination-to-page-input`
9. **URL 参数翻页备用方案**：如输入框方式失败，可尝试 `?page={页码}` URL 参数直接跳转
10. **保存商品链接**：搜索完成后，将商品列表保存到桌面（/home/k/桌面/闲鱼{关键词}搜索结果.md），包含每个商品的链接（格式：https://www.goofish.com/item?id={item_id}），方便用户直接点击访问
11. **提取 item_id**：从搜索结果的链接中提取 item_id，构造完整的商品链接

## Verification Checklist

- [ ] 搜索结果已按价格升序排序
- [ ] 已排除商家（鱼小铺/超赞鱼小铺）
- [ ] 已排除价格区间商品
- [ ] 已排除回收广告
- [ ] 输出格式清晰易读
- [ ] 包含价格统计和热门商品
- [ ] 每个商品都有链接可点击

## Related Skills

- `xianyu-search` (clawhub) — 功能高度重叠的闲鱼搜索技能。两者触发条件、输出格式、筛选逻辑几乎相同。`xianyu-search` 由 clawhub 社区维护，`goofish-search` 由本用户本地创建并经过实际测试迭代。**优先使用 `goofish-search`**，因为其翻页机制（browser_type + browser_click）经过验证更可靠。如需合并，建议将 `goofish-search` 的翻页和排序逻辑合并到 `xianyu-search` 中。

## 依赖

- Hermes Agent 内置 `browser_*` 工具
- 已登录闲鱼的 Chrome 浏览器（CDP 模式）
