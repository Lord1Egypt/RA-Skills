---
name: kongfz-ankang-search
description: 孔夫子旧书网拍卖栏目检索技能，自动搜索安康、来鹿堂、兴安府三个关键词相关文献拍品。触发词：搜孔夫子拍卖安康
---

# 孔夫子安康文献检索技能

## 概述

本技能提供孔夫子二手网（kongfz.com）拍卖栏目的自动化检索功能，专注于发现与陕西安康地区相关的文献、书籍等拍卖物品。当检测到相关物品时，会立即向用户发送提示。

## 核心功能

### 0. 固定搜索关键词

**每次调用本技能，必须依次搜索以下三个关键词：**

1. **安康** - 搜索安康地区相关文献和物品
2. **来鹿堂** - 搜索安康著名老字号（清代书商、印书局）相关拍品
3. **兴安府** - 搜索清代陕南行政区划（辖安康、汉阴、石泉等地）相关文献

**执行顺序**：安康 → 来鹿堂 → 兴安府

**输出格式**：汇总三个关键词的搜索结果，按关键词分开展示。

---

### 1. 网站检索

使用 **xbrowser** 技能执行检索（必须，不可直接用 Python requests）。

执行步骤：

1. **初始化 xbrowser**：`node "C:\Program Files\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" init`
2. **打开拍卖搜索页**：`open https://search.kongfz.com/adv.html?type=pm`
3. **等待加载**：`wait --load networkidle`
4. **获取元素引用**：`snapshot -i`（记录 textbox 引用，通常是 e21 为关键词输入框）
5. **填入关键词**：`fill @e21 关键词`
6. **提交搜索**：`press Enter`
7. **等待结果**：`wait --load networkidle`
8. **提取结果**：`get text body` 或 `snapshot -i` 获取拍品列表

### 2. 地区识别规则

识别陕西安康相关物品的优先级：

**高优先级（立即提示）**：
- 物品地区明确标注为"陕西 安康"
- 标题包含"安康文献"、"安康史料"、"安康地方志"等
- 描述中提到"安康县"、"安康地区"、"陕南安康"等

**中优先级（关注但不立即提示）**：
- 标题包含"安康"但地区不明确
- 相关但非核心的安康文化物品

**低优先级（记录但不提示）**：
- 仅提及"安康"但实际无关的物品

### 3. 提示机制

当发现高优先级物品时，使用以下格式提示用户：

```
📚 发现安康相关拍品！
标题：[物品标题]
地区：[明确地区]
当前价格：[价格] | 剩余时间：[时间]
链接：[物品链接]
```

## 执行流程

### 使用 xbrowser 执行检索

根据 qclaw-rules 系统规则，所有浏览器自动化任务必须委托给 **xbrowser** 技能执行。

**完整 batch 命令模板**（一次性执行）：

```bash
node "C:\Program Files\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" run --browser cft batch --bail \
  "open 'https://search.kongfz.com/adv.html?type=pm'" \
  "wait --load networkidle" \
  "snapshot -i" \
  "fill @e21 安康文字" \
  "press Enter" \
  "wait --load networkidle" \
  "snapshot -i" \
  "get text body"
```

**注意**：
- `e21` 是拍品名称输入框的引用（来自 snapshot），如果页面结构变化需重新获取
- 搜索结果页 URL 格式：`https://search.kongfz.com/pm-search-web/pc/auction/search?key=关键词`
- 必须用 `press Enter` 提交，点击搜索按钮可能无效

### 结果解析

从 `get text body` 的输出中解析：
- 拍品标题（heading 元素）
- 作者、出版社、年代等信息
- 当前价格（`￥` 开头）
- 剩余时间（`X时X分X秒` 格式）
- 拍主昵称和拍品数量

**筛选安康相关**：
1. 搜索结果文本中包含"安康"的拍品
2. 检查标题、描述、地区字段
3. 按优先级分类后提示用户

## 脚本说明

### scripts/kongfz_search_xbrowser.py

Python 脚本，调用 xbrowser CLI 执行完整搜索流程。

**使用方法**：
```bash
python scripts/kongfz_search_xbrowser.py --keyword "安康文字" --region "安康"
```

## 参考文档

### references/kongfz_structure.md

孔夫子网站结构说明，包含：
- 主站：`https://www.kongfz.com/`
- 拍卖栏目：`https://www.kongfz.cn/`（新版独立域名）
- 搜索页面：`https://search.kongfz.com/adv.html?type=pm`（拍卖区高级搜索）
- 搜索结果：`https://search.kongfz.com/pm-search-web/pc/auction/search?key=关键词`
- 商品详情：`https://item.kongfz.com/book/{ID}.html`
- 分类ID参考：34=红色文献, 3=历史, 12=国学古籍, 3003=地方史志

**⚠️ 已废弃URL**：
- `https://www.kongfz.com/auction/`（404错误）
- `https://search.kongfz.com/product/search?q=...`（404错误）

## 使用示例

**用户请求示例**：
1. "帮我看看孔夫子网上有没有安康的文献拍卖"
2. "监控孔夫子拍卖栏目，有安康的书就告诉我"
3. "搜索陕西安康的地方志拍卖"

**技能响应示例**：
```
🔍 正在检索孔夫子拍卖栏目...
✅ 检索完成，发现 3 件安康相关拍品：

📚 高优先级（立即提示）
1. 《安康地区志》1995年版，地区：陕西 安康，当前价：¥280
2. 安康文史资料选辑（全套），地区：陕西 安康，当前价：¥450

📋 中优先级（已记录）
3. 陕南民俗文化（含安康章节），地区未明确，当前价：¥120
```
