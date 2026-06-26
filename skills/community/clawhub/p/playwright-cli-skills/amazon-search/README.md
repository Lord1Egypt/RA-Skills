# Amazon Product Search Skill

一键搜索亚马逊商品并生成 CSV 报告！

## 🚀 快速开始

### 方式一：使用 Node.js 脚本（推荐）

```bash
# 搜索毕业派对礼品袋
node ~/playwright-cli-skills/amazon-search/amazon-search.js "graduation party favor bags"

# 搜索其他商品
node ~/playwright-cli-skills/amazon-search/amazon-search.js "wireless earbuds"
```

### 方式二：使用 Bash 脚本

```bash
~/playwright-cli-skills/amazon-search/amazon-search.sh "graduation party favor bags"
```

## 📋 前置要求

1. **Playwright CLI 已安装**
   ```bash
   npm install -g playwright-cli
   ```

2. **亚马逊已登录并保存状态**
   ```bash
   # 第一次使用时需要登录
   playwright-cli open https://www.amazon.com
   # 手动登录后，保存状态
   playwright-cli state-save ~/amazon-auth.json
   ```

## 📊 输出格式

CSV 文件包含以下字段：
- **排名**: 1-10
- **商品名称**: 商品标题
- **评分**: 星级评分（如 4.8）
- **评价数**: 评价数量
- **价格**: 当前价格
- **销量信息**: 如 "50+ bought in past month"
- **图片URL**: 商品主图链接
- **商品链接**: 可直接访问的亚马逊链接（格式: https://www.amazon.com/dp/ASIN）
- **ASIN**: 亚马逊标准识别号码

## 💡 使用技巧

### 1. 搜索带空格的词组
使用引号包裹关键词：
```bash
node amazon-search.js "wireless bluetooth earbuds"
```

### 2. 查看调试信息
设置 DEBUG 环境变量：
```bash
DEBUG=1 node amazon-search.js "laptop stand"
```

### 3. 输出文件位置
生成的 CSV 文件保存在用户主目录：
```
~/amazon-{keyword}-top10-{date}.csv
```

## ⚠️ 踩坑记录（重要！）

### ❌ 坑 1：编造 ASIN
**问题**：CSV 中的链接打不开（Page Not Found）  
**原因**：ASIN 是随机生成的，不是真实值  
**解决**：必须从页面 `[data-asin]` 属性提取真实 ASIN

### ❌ 坑 2：错误的链接格式  
**错误**：`https://www.amazon.com/product/B0xxx`  
**正确**：`https://www.amazon.com/dp/B0xxx`  

### ❌ 坑 3：未加载登录状态  
**问题**：搜索结果不完整或需要反复登录  
**解决**：搜索前必须执行 `state-load ~/amazon-auth.json`

### ❌ 坑 4：页面未完全加载  
**问题**：提取不到数据  
**解决**：等待 3 秒确保页面加载完成

### ❌ 坑 5：CSV 格式问题  
**问题**：商品名称包含逗号导致 CSV 列错乱  
**解决**：商品名称中的逗号替换为分号，并用双引号包裹

## 🔧 故障排除

### 问题：无法提取数据
**检查清单**：
1. 登录状态文件是否存在：`ls ~/amazon-auth.json`
2. Playwright CLI 是否安装：`playwright-cli --version`
3. 网络连接是否正常

### 问题：提取的数据不完整
**可能原因**：
- 页面加载慢 → 增加等待时间（修改脚本中的 `sleep 3`）
- 亚马逊页面结构变化 → 更新 selector

### 问题：链接打不开
**检查**：
- ASIN 是否真实（10位字母数字组合）
- 链接格式是否正确（必须是 `/dp/` 不是 `/product/`）

## 📝 示例输出

```
🔍 开始搜索亚马逊商品: graduation party favor bags
📁 输出文件: /Users/qianxin/amazon-graduation-party-favor-bags-top10-2025-01-15.csv
📋 Step 1: 加载登录状态...
🔎 Step 2: 搜索商品...
⏳ Step 3: 等待页面加载...
📊 Step 4: 提取商品数据...

✅ 完成！CSV 文件已生成: /Users/qianxin/amazon-graduation-party-favor-bags-top10-2025-01-15.csv

📊 数据预览（前5行）：
排名,商品名称,评分,评价数,价格,销量信息,图片URL,商品链接,ASIN
1. Leislam Graduation Treat Bags; 100 PCS Graduat... | ⭐4.8 | 💰$5.98
2. Boao 100 Pieces Graduation Cellophane Bags Mort... | ⭐4.6 | 💰$7.99
3. JarThenaAMCS 50Pcs Graduation Party Favor Bag 2... | ⭐4.8 | 💰$9.99
4. Graduation Treat Cellophane Bags 100 PCS Gradua... | ⭐4.2 | 💰$4.99
5. Blulu 100 Pieces Graduation Cellophane Treat Ba... | ⭐4.7 | 💰$7.99

📈 共提取 10 个商品
```

## 🛠️ 技术细节

### 使用的 Selector
- **商品容器**: `[data-component-type="s-search-result"]`
- **ASIN**: `data-asin` 属性
- **标题**: `h2`
- **价格**: `.a-price .a-offscreen`
- **评分**: `[aria-label*="out of 5 stars"]`
- **评价数**: `a[href*="customerReviews"] span`
- **图片**: `img[src]`
- **销量**: `[aria-label*="bought in past month"]`

### 数据清洗
- 商品名称：逗号替换为分号，截断至 100 字符
- 价格：保留原始格式
- 链接：使用 `/dp/[ASIN]` 格式确保可访问

## 📄 文件说明

```
~/playwright-cli-skills/amazon-search/
├── SKILL.md              # Skill 说明文档
├── README.md             # 本文件
├── amazon-search.js      # Node.js 自动化脚本
└── amazon-search.sh      # Bash 自动化脚本
```

## 🔄 更新记录

- **2025-04-12**: 初始版本，修复 ASIN 和链接格式问题
