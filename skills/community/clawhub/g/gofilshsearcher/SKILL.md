---
name: xianyu-search
description: 闲鱼商品自动搜索技能，支持严格筛选（个人闲置/单一价格/排除商家），输出 TOP10 价格升序列表
version: 2.0.0
updated: 2026-03-10
compatibility: Requires browser tool (playwright-browser or openclaw browser)
---

# 闲鱼搜索技能 - Xianyu Search Skill

## 📋 技能概述

自动在闲鱼网站搜索商品，应用严格筛选条件，输出真实有效的个人闲置商品列表。用户只需提供搜索关键词，技能自动处理搜索、筛选、排序和结果输出。

**核心优势：**
- ✅ 自动排除商家/鱼小铺
- ✅ 自动排除价格区间商品
- ✅ 自动排除回收广告/笔记本/包装盒
- ✅ 价格升序排序，快速找到最低价
- ✅ 支持自定义筛选条件（价格/地区/成色）

---

## 🎯 激活条件

用户消息包含以下任一关键词时激活：

| 关键词 | 示例 |
|--------|------|
| `闲鱼搜索` | 闲鱼搜索 RTX 5090 |
| `闲鱼找` | 闲鱼找 二手 iPhone |
| `闲鱼买` | 闲鱼买 机械键盘 |
| `帮我找闲鱼` | 帮我找闲鱼 DDR5 内存 |
| `二手搜索` | 二手搜索 显卡 |

---

## 🚀 使用格式

### 基础搜索
```
闲鱼搜索 [产品名称]
```

**示例：**
```
闲鱼搜索 RTX 5090
闲鱼搜索 金士顿 DDR5 16G 6000 台式机内存
闲鱼搜索 二手 iPhone 13 128G
```

### 带筛选条件
```
闲鱼搜索 [产品名称] --max-price [价格] --region [地区] --condition [成色]
```

**支持的筛选参数：**
| 参数 | 说明 | 示例 |
|------|------|------|
| `--max-price XXX` | 最高价格 | `--max-price 1200` |
| `--min-price XXX` | 最低价格 | `--min-price 500` |
| `--region XXX` | 指定地区 | `--region 广东` |
| `--condition XXX` | 成色要求 | `--condition 全新` |
| `--shipping` | 仅包邮 | `--shipping` |
| `--verified` | 仅验货宝 | `--verified` |

**示例：**
```
闲鱼搜索 金士顿 DDR5 16G --max-price 1200 --region 广东
闲鱼搜索 iPhone 13 --min-price 2000 --condition 几乎全新 --shipping
```

---

## ⚙️ 执行流程

### 步骤 1: 启动浏览器
```json
{
  "tool": "browser_launch",
  "arguments": {
    "headless": true
  }
}
```

### 步骤 2: 访问闲鱼首页
```json
{
  "tool": "browser_goto",
  "arguments": {
    "url": "https://www.goofish.com"
  }
}
```

### 步骤 3: 执行搜索
```json
{
  "tool": "browser_fill",
  "arguments": {
    "selector": "input[type='text']",
    "value": "[搜索关键词]"
  }
}
```
```json
{
  "tool": "browser_click",
  "arguments": {
    "selector": "button[type='submit']"
  }
}
```

### 步骤 4: 点击个人闲置筛选
```json
{
  "tool": "browser_wait_for_timeout",
  "arguments": {
    "timeout": 3000
  }
}
```
```json
{
  "tool": "browser_click",
  "arguments": {
    "selector": "[个人闲置筛选按钮]"
  }
}
```

### 步骤 5: 提取商品数据
```json
{
  "tool": "browser_evaluate",
  "arguments": {
    "script": "提取商品标题、价格、地区、想要人数、链接"
  }
}
```

### 步骤 6: 应用筛选条件
```javascript
// 排除商家
if (seller.includes('鱼小铺') || seller.includes('超赞')) return false;

// 排除价格区间
if (price.includes('-') || price.includes('~')) return false;

// 排除回收广告
if (title.includes('回收') || title.includes('高价收')) return false;
```

### 步骤 7: 排序并输出
```javascript
// 价格升序
results.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));

// 返回 TOP10
return results.slice(0, 10);
```

### 步骤 8: 关闭浏览器
```json
{
  "tool": "browser_close",
  "arguments": {}
}
```

---

## 📊 输出格式

### 标准输出（单条消息）

```markdown
🦞 闲鱼 [关键词] 搜索结果

已应用严格筛选：**仅限个人闲置** + **单一价格** + **排除商家/回收广告**

### 📦 商品列表（价格升序）

| # | 价格 | 商品标题 | 地区 | 想要 | 链接 |
|---|------|----------|------|------|------|
| 1 | **¥1.74 万** | 技嘉 RTX 5090 D V2 魔鹰 OC 24G | 广东 | - | [🔗查看](链接) |
| 2 | **¥1.79 万** | 影驰 RTX5090 D V2 星曜白色 | 湖南 | - | [🔗查看](链接) |
| ... | ... | ... | ... | ... | ... |

---

### 📊 价格统计
| 指标 | 价格 |
|------|------|
| **最低价** | ¥1.74 万（技嘉魔鹰 OC，广东） |
| **最高价** | ¥1.90 万（七彩虹白火神，广东） |
| **平均价** | 约 ¥1.86 万 |

### 🔥 热门商品
1. **微星超龙 5090** - 35 人想要（¥1.83 万）
2. **七彩虹火神 24G** - 30 人想要（¥1.89 万）

### ✅ 筛选说明
- 已排除商家（鱼小铺/超赞鱼小铺）
- 已排除价格区间商品
- 已排除回收广告/笔记本/包装盒
- 共扫描约 25 个商品，有效个人闲置 9 个
```

### 企业微信输出（多条消息）

**每条消息 1 个商品，间隔 1.5 秒：**

```
🥇 TOP1 - **¥1.74 万**

技嘉 RTX 5090 D V2 魔鹰 OC 24G，全新未拆封

📍 地区：广东 | 👥 8 人想要

🔗 查看：https://www.goofish.com/item?id=xxxxx
```

---

## 🔧 配置参数

### 默认配置
```json
{
  "xianyu_search": {
    "browser": {
      "headless": true,
      "timeout_ms": 30000,
      "retry_count": 2
    },
    "filters": {
      "personal_only": true,
      "single_price_only": true,
      "exclude_merchants": true,
      "exclude_price_range": true,
      "exclude_ads": true
    },
    "output": {
      "result_limit": 10,
      "sort_by": "price_asc",
      "items_per_message": 1,
      "send_interval_ms": 1500
    }
  }
}
```

### 自定义配置
在技能调用时传入配置覆盖默认值：
```json
{
  "result_limit": 20,
  "sort_by": "wanted_desc",
  "headless": false
}
```

---

## 🎯 数据提取规则

### 商品卡片选择器
```css
/* 商品卡片容器 */
.item-card, .search-result-item, [class*="item-card"]

/* 商品标题 */
.title, h3, [class*="title"]

/* 价格 */
.price, [class*="price"]

/* 地区 */
.location, [class*="location"]

/* 想要人数 */
[class*="wanted"], [class*="want"]
```

### 价格验证逻辑
```javascript
function isValidPrice(priceText) {
  // 排除价格区间
  if (priceText.includes('-') || priceText.includes('~')) {
    return false;
  }
  // 排除"XXX 起"
  if (priceText.includes('起')) {
    return false;
  }
  // 排除"面议"
  if (priceText.includes('面议')) {
    return false;
  }
  // 只保留纯数字价格
  return /^\d+$/.test(priceText.replace('¥', '').replace('万', '').trim());
}
```

### 规格验证逻辑
```javascript
function matchesSpec(title, requiredSpecs, excludeSpecs) {
  // 必须包含所有必需规格
  for (const spec of requiredSpecs) {
    if (!title.includes(spec)) {
      return false;
    }
  }
  // 排除不符规格
  for (const exclude of excludeSpecs) {
    if (title.includes(exclude)) {
      return false;
    }
  }
  return true;
}

// 示例：DDR5 内存搜索
const requiredSpecs = ['DDR5', '16G', '6000'];
const excludeSpecs = ['笔记本', '包装盒', '回收', 'DDR4', 'DDR3', 'SO-DIMM'];
```

---

## ⚠️ 错误处理

### 无搜索结果
```markdown
❌ 未找到符合条件的商品

建议：
1. 放宽筛选条件（如接受商家商品）
2. 调整搜索关键词
3. 尝试不同规格

需要我重新搜索吗？
```

### 筛选失败
```markdown
⚠️ 筛选条件应用失败，显示原始结果

可能原因：
- 闲鱼页面结构变更
- 网络加载超时
- 筛选按钮不可用

请人工筛选，或稍后重试。
```

### 网络超时
```markdown
⏱️ 网络超时，正在重试...（第 X 次）

如多次重试失败，建议：
1. 检查网络连接
2. 稍后重试
3. 手动访问闲鱼网站
```

### 浏览器启动失败
```markdown
❌ 浏览器启动失败

请执行以下操作：
1. 重启 OpenClaw Gateway：`openclaw gateway restart`
2. 检查浏览器配置
3. 如仍失败，手动访问：https://www.goofish.com
```

---

## 📝 记忆记录

搜索完成后自动记录到 `memory/YYYY-MM-DD.md`：

```markdown
### 闲鱼搜索记录

**时间：** 2026-03-10 18:36
**关键词：** RTX 5090
**结果数量：** 10 条
**价格区间：** ¥1.74 万 - ¥1.90 万
**最低价商品：** [技嘉魔鹰 OC](https://www.goofish.com/item?id=1017187960312)
**筛选条件：** 个人闲置/单一价格/排除商家
```

---

## 🔗 相关工作流

### 企业微信 ↔ 闲鱼搜索
**文档：** `memory/workflows/wechat-xianyu-search.md`

**流程：**
```
企业微信消息 → OpenClaw 接收 → xianyu-search 技能 → 闲鱼网站 → 
结果提取 → 筛选排序 → 企业微信返回（多条消息）
```

**触发关键词：**
- "闲鱼搜索 XXX"
- "闲鱼找 XXX"
- "帮我找闲鱼 XXX"

---

## 🧪 测试用例

### 测试 1: 基础搜索
```
输入：闲鱼搜索 RTX 5090
预期：返回 TOP10 商品列表，价格升序
```

### 测试 2: 带价格筛选
```
输入：闲鱼搜索 DDR5 内存 --max-price 1200
预期：所有商品价格 ≤ ¥1200
```

### 测试 3: 带地区筛选
```
输入：闲鱼搜索 iPhone 13 --region 广东
预期：所有商品地区为广东
```

### 测试 4: 无结果处理
```
输入：闲鱼搜索 不存在的商品 XYZ123
预期：返回"未找到符合条件的商品"建议消息
```

### 测试 5: 筛选失败处理
```
模拟：闲鱼页面结构变更
预期：返回"筛选条件应用失败"并显示原始结果
```

---

## 📚 依赖技能

| 技能 | 用途 |
|------|------|
| `playwright-browser` | 浏览器自动化（推荐） |
| `openclaw browser` | OpenClaw 内置浏览器工具 |
| `message` | 发送结果到聊天渠道 |
| `finder` | 保存搜索结果到文件（可选） |

---

## 🔄 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03-06 | 初始版本，基础筛选功能 |
| 2.0 | 2026-03-10 | 整合完整工作流，添加企业微信支持，优化筛选逻辑 |

---

## 💡 最佳实践

### 1. 关键词优化
- ✅ 具体明确：`金士顿 DDR5 16G 6000 台式机内存`
- ❌ 过于宽泛：`内存条`

### 2. 筛选条件使用
- 高价商品：添加 `--max-price` 避免超出预算
- 本地交易：添加 `--region` 方便面交
- 品质要求：添加 `--condition 全新` 或 `--verified`

### 3. 结果验证
- 检查卖家信用（个人卖家通常信用良好但非"极好"）
- 查看商品实拍图
- 确认支持验货宝（贵重物品）

### 4. 购买时机
- 晚上 20:00-23:00：新发布商品较多
- 周末：个人卖家活跃度更高
- 月初/月末：资金周转期，好价商品多

---

_此技能文件于 2026-03-10 更新 v2.0。自动严格筛选，买二手不踩坑。_
