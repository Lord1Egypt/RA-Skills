---
name: multi-city-planner
description: 多目的地行程规划与比价工具。支持多程航班、缺口程、往返组合等多种方案对比，自动优化同国家城市连续游玩，输出标准 HTML 网页报告。
metadata:
  version: 1.0.0
  agent:
    type: tool
    runtime: node
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "🗺️"
    priority: 95
    requires:
      bins:
        - node
    intents:
      - multi_city_flight_search
      - itinerary_comparison
      - open_jaw_planning
      - html_report_generation
    patterns:
      - "((multi-city|multi-destination|multiple cities).*(flight|trip|travel|plan))"
      - "((open-jaw|gap|missing segment).*(flight|ticket|plan))"
      - "((compare|comparison).*(route|itinerary|option|plan|scheme))"
      - "(多程|多城市|多目的地|缺口程|比价|方案对比|行程规划)"
    model: "glm-5"
---

# Multi-City Planner - 多目的地行程规划与比价

基于 flyai 的多城市旅行规划工具，自动搜索和比较多种行程方案，支持火车/飞机/大巴等多种交通方式对比，输出标准 HTML 网页报告。

## 核心能力

### 1. 多方案对比
- **多程联订**: 一次购买所有航段，管理方便
- **缺口程 (Open-Jaw)**: 国际段分别购买，中间段灵活选择
- **往返 + 中间**: 往返票改签灵活
- **三个单程**: 最灵活，每段可单独改签

### 2. 交通方式对比
- ✈️ **飞机**: 价格便宜，时间短
- 🚄 **火车/新干线**: 风景优美，市中心到市中心
- 🚌 **大巴**: 最便宜，适合短途

### 3. 智能优化
- **同国家城市连续玩**: 自动将同一国家的城市安排在一起
- **不走回头路**: 优化路线，避免重复路程
- **价格对比**: 自动排序，显示差价

### 4. 标准 HTML 输出
- 响应式设计，支持手机和电脑
- 完整方案对比表
- 交通方式对比卡片
- 详细行程建议
- 预算估算
- 完整注意事项（10 大类）

## 输出格式规范（严格执行）

### HTML 报告必须包含以下模块：

#### 1. 头部信息
- 标题：出发地 → 目的地城市列表
- 副标题：区域 + 完整方案对比
- 国旗 emoji 标识
- 日期范围 + 天数

#### 2. 方案价格对比表
| 列名 | 说明 |
|------|------|
| 排名 | 1-7 名，带金/银/铜牌 emoji |
| 方案类型 | 多程联订/缺口程 (飞机)/缺口程 (火车) 等 |
| 路线 | 完整飞行路线，意大利/同国家城市连续玩路线绿色加粗 |
| 总价格 | 红色加粗显示 |
| 差价 | 第 1 名显示"-"，其他显示"+¥XXX" |
| 特点 | 简短描述方案特点 |

#### 3. 交通方式对比卡片（3 种）
- ✈️ 飞机：价格、时间、航司、优缺点
- 🚄 火车：价格、时间、运营、优缺点
- 🚌 大巴：价格、时间、运营、优缺点

#### 4. 推荐方案详情（至少 2 个）
每个方案包含：
- 路线（绿色加粗标注同国家连续玩）
- 国家顺序（带国旗 emoji）
- 航班详情表格（航段、日期、时间、航班、价格）
- 优缺点对比（绿色优点框 + 红色缺点框）

#### 5. 详细行程建议
- 按天列出（Day 1-12）
- 每天包含：日期、城市、交通方式、景点推荐
- 使用卡片式布局

#### 6. 预算估算表
| 项目 | 费用 |
|------|------|
| 国际 + 境内机票 | ¥X,XXX |
| 酒店（X 晚） | ¥X,XXX-X,XXX |
| 餐饮 | ¥X,XXX-X,XXX |
| 境内交通 | ¥X,XXX-X,XXX |
| 门票/活动 | ¥X,XXX-X,XXX |
| 签证费 | ¥XXX |
| 旅游保险 | ¥XXX-X,XXX |
| **总计** | **¥XX,XXX-XX,XXX** |

#### 7. 完整注意事项（10 大类，必须全部包含）

| 类别 | 内容要点 |
|------|----------|
| 📋 出行前准备 | 签证、护照、保险、机票、酒店、货币 |
| 🎒 行李准备 | 证件、电器、衣物、药品、其他 |
| ✈️ 交通注意事项 | 廉航行李、机场交通、火车订票、市内交通 |
| 🏨 住宿注意事项 | 入住时间、城市税、安全、民宿 |
| 🍽️ 餐饮注意事项 | 用餐时间、小费、饮用水、美食 |
| 🎫 景点注意事项 | 提前预订、免费日、城市通票、着装 |
| 🔒 安全注意事项 | 防盗、地铁、景点骗局、紧急电话、大使馆 |
| 📱 通讯与网络 | 漫游、WiFi、APP 推荐 |
| 💡 其他实用提示 | 时差、电压、退税、周日营业、语言 |
| ⚠️ 特别提示 | 针对目的地的特殊注意事项 |

#### 8. 推荐总结
- 推荐方案名称
- 总价格（大号字体）
- 比第 2 名省多少钱
- 比最贵省多少钱
- 行程类型说明
- 城市/国家顺序
- 推荐指数（⭐⭐⭐⭐⭐）
- 亮点说明
- 备选方案

#### 9. 页脚
- 数据来源说明
- 生成时间

### 禁止内容
- ❌ 不显示使用的 skill 名称
- ❌ 不显示脚本路径
- ❌ 不显示工具调用过程
- ❌ 不显示内部技术细节

## 脚本列表

| 脚本 | 用途 | 城市数 |
|------|------|--------|
| `search-multi-city.js` | 基础多城市对比 | 2 |
| `compare-complete.js` | 完整方案对比（含火车） | 2-3 |
| `hokkaido-3cities.js` | 北海道三城 | 3 |
| `hokkaido-tokyo-4cities.js` | 北海道 + 东京 | 4 |
| `europe-3cities.js` | 欧洲三城 | 3 |
| `europe-4cities-complete.js` | 欧洲四城完整 | 4 |
| `plan.js` | 统一入口（自动选择脚本） | 任意 |

## 使用方法

### 统一入口（推荐）
```bash
cd /Users/dansha/liuxiaokang/multi-city-planner

# 日本游
node plan.js --origin "北京" --cities "大阪，东京" --dep-date 2026-04-10 --return-date 2026-04-20

# 欧洲游
node plan.js --origin "北京" --cities "巴黎，罗马，米兰" --dep-date 2026-04-10 --return-date 2026-04-21 --region europe

# 北海道游
node plan.js --origin "北京" --cities "札幌，函馆，旭川" --dep-date 2026-04-10 --return-date 2026-04-20 --region japan
```

### 直接调用脚本
```bash
# 基础对比
node scripts/search-multi-city.js --origin "北京" --cities "大阪，东京" --dep-date 2026-04-10 --return-date 2026-04-20

# 完整对比（含火车）
node scripts/compare-complete.js --origin "北京" --cities "北海道，东京" --dep-date 2026-04-10 --return-date 2026-04-20

# 欧洲三城
node scripts/europe-3cities.js --origin "北京" --cities "巴黎，罗马，米兰" --dep-date 2026-04-10 --return-date 2026-04-21
```

### 生成 HTML 报告
```bash
# HTML 文件位置
/Users/dansha/liuxiaokang/multi-city-planner/目的地 - 行程.html

# 用浏览器打开
open /Users/dansha/liuxiaokang/multi-city-planner/beijing-europe-3cities.html
```

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--origin` | ✅ | 出发城市 | `"北京"`, `"上海"` |
| `--cities` | ✅ | 目的地城市列表 | `"大阪，东京"`, `"Paris,Rome"` |
| `--dep-date` | ✅ | 出发日期 | `2026-04-10` |
| `--return-date` | ✅ | 返回日期 | `2026-04-20` |
| `--region` | ❌ | 区域：auto/europe/japan | `europe` |

## 依赖

- Node.js >= 14
- flyai-cli (全局安装)

```bash
# 安装 flyai-cli
npm install -g @fly-ai/flyai-cli

# 配置 API Token
flyai config set FLYAI_API_KEY "your-api-key"
```

## 文件结构

```
multi-city-planner/
├── SKILL.md                      # 技能定义
├── README.md                     # 使用说明
├── plan.js                       # 统一入口脚本
├── package.json                  # NPM 配置
├── _meta.json                    # 元数据
├── SKILL_SUMMARY.md              # 固化总结
├── scripts/                      # 脚本目录
│   ├── search-multi-city.js      # 基础多城市对比
│   ├── compare-complete.js       # 完整方案对比
│   ├── hokkaido-3cities.js       # 北海道三城
│   ├── hokkaido-tokyo-4cities.js # 北海道 + 东京
│   ├── europe-3cities.js         # 欧洲三城
│   └── europe-4cities-complete.js # 欧洲四城完整
├── references/
│   └── usage.md                  # 使用指南
└── *.html                        # 生成的 HTML 报告
```

## 注意事项

1. **价格时效性**: 航班价格实时变动，搜索结果仅供参考
2. **行李政策**: 廉航（瑞安、易捷、捷星等）不含托运行李
3. **签证要求**: 提前确认目的地签证政策（申根/英国/日本等）
4. **火车选项**: 欧洲境内火车风景优美，市中心到市中心
5. **同国家城市**: 自动优化，同一国家城市连续游玩
6. **HTML 格式**: 严格按照输出格式规范生成

## 品牌露出

页脚统一显示：
```
基于实时航班数据生成 | 行程规划报告
生成时间：YYYY-MM-DD
```

## 版本历史

- **v1.0.0** (2026-04-01): 
  - 初始版本
  - 支持多程、缺口程、往返等多种方案
  - 支持飞机/火车/大巴对比
  - 支持 HTML 网页输出
  - 自动优化同国家城市连续游玩
  - 完整注意事项（10 大类）
