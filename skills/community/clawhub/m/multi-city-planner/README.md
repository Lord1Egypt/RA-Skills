# 🗺️ Multi-City Planner - 多目的地行程规划

智能多城市航班搜索和比价工具，自动比较多种行程方案，帮你找到最优价格组合。

## ✨ 核心功能

- **多程搜索**: 自动搜索 A→B→C→A 等多段航班
- **方案比价**: 对比多程联订、缺口程、往返组合等多种方案
- **智能推荐**: 综合考虑价格、时间、便利性，推荐最优方案
- **灵活配置**: 支持自定义城市顺序、停留天数、预算上限

## 🚀 快速开始

### 基础用法

```bash
# 北京出发，游玩大阪和东京
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25
```

### 指定游玩顺序

```bash
# 先去大阪，再去东京
multi-city-planner --origin "北京" --route "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25

# 反向顺序对比（有时更便宜！）
multi-city-planner --origin "北京" --route "东京，大阪" --dep-date 2026-04-15 --return-date 2026-04-25
```

### 指定停留天数

```bash
# 大阪玩 4 天，东京玩 6 天
multi-city-planner \
  --origin "北京" \
  --cities "大阪，东京" \
  --dep-date 2026-04-15 \
  --return-date 2026-04-25 \
  --days-per-city "4,6"
```

## 📊 输出示例

```
🗺️  北京 → 大阪 + 东京 | 行程类型对比
日期：2026-04-10 ~ 2026-04-20 (10 天)

📊 行程类型价格对比（从低到高）

| 排名 | 行程类型 | 飞行路线 | 总价格 | 差价 |
|------|----------|----------|--------|------|
| 1 | 多程联订 | 北京→大阪 → 大阪→东京 → 东京→北京 | ¥3,041 | - |
| 2 | 缺口程 + 单程 | 北京→大阪 + 东京→北京 + 大阪→东京 | ¥3,041 | +¥0 |
| 3 | 三个单程 | 北京→大阪 → 大阪→东京 → 东京→北京 | ¥3,041 | +¥0 |

### 1. 多程联订 - ¥3,041

**航班详情:**

| 航段 | 日期 | 时间 | 航班 | 价格 |
|------|------|------|------|------|
| 1. 北京→大阪 | 4/10 | 07:25-11:00 | 国泰 CX345 | ¥1,441 |
| 2. 大阪→东京 | 4/15 | 21:00-22:25 | 捷星 GK238 | ¥244 |
| 3. 东京→北京 | 4/20 | 08:00-11:55 | 港航 UO857 | ¥1,356 |

**优缺点:**
✅ 一次付款，管理方便 | 路线合理不走回头路 | 通常可行李直挂
❌ 改签不便 | 某段延误影响后续
```

## 📝 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--origin` | ✅ | 出发城市 | `"北京"`, `"上海"` |
| `--cities` | ✅ | 目的地城市列表 | `"大阪，东京"`, `"Paris,Rome"` |
| `--route` | ❌ | 指定游玩顺序 | `"大阪，东京"` |
| `--dep-date` | ✅ | 出发日期 | `2026-04-15` |
| `--return-date` | ✅ | 返回日期 | `2026-04-25` |
| `--days-per-city` | ❌ | 每个城市停留天数 | `"4,6"` |
| `--budget` | ❌ | 预算上限（元） | `5000` |
| `--prefer` | ❌ | 偏好：price/time/comfort | `price` |

## 💡 使用技巧

### 1. 对比不同顺序

```bash
# 顺序 A
multi-city-planner --origin "北京" --route "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25

# 顺序 B（可能更便宜！）
multi-city-planner --origin "北京" --route "东京，大阪" --dep-date 2026-04-15 --return-date 2026-04-25
```

### 2. 调整停留天数优化价格

```bash
# 大阪 3 天，东京 7 天
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --days-per-city "3,7"

# 大阪 5 天，东京 5 天
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --days-per-city "5,5"
```

### 3. 结合 flyai 查询酒店景点

```bash
# 查完航班查酒店
flyai search-hotel --origin "大阪" --check-in 2026-04-15 --nights 4

# 查询目的地景点
flyai keyword-search --query "大阪必去景点 4 天行程"
```

## ⚠️ 注意事项

### 价格时效性
- 航班价格实时变动，搜索结果仅供参考
- 看到合适的价格建议尽快预订

### 行李政策
- **多程联订**: 通常可行李直挂（同一航司或联盟）
- **分开购票**: 通常需要自提行李重新托运
- 廉价航空可能不包含托运行李

### 签证要求
- 缺口程可能涉及过境签证
- 提前确认中转地签证政策

### 改签风险
- 分开购票时，前段延误可能影响后续航班
- 建议：中间段预留充足时间（至少 3 小时）
- 购买旅行保险降低风险

## 🔧 依赖

- Node.js >= 14
- flyai-cli (全局安装)

```bash
# 安装 flyai-cli
npm install -g @fly-ai/flyai-cli

# 验证安装
flyai --version
```

## 📁 文件结构

```
multi-city-planner/
├── SKILL.md                      # 技能定义文件
├── _meta.json                    # 元数据
├── package.json                  # NPM 包配置
├── README.md                     # 使用说明
├── scripts/
│   └── search-multi-city.js      # 主脚本
└── references/
    └── usage.md                  # 详细使用指南
```

## 🌟 示例场景

### 日本关东关西环线

```bash
multi-city-planner \
  --origin "北京" \
  --cities "大阪，东京" \
  --dep-date 2026-04-15 \
  --return-date 2026-04-25 \
  --days-per-city "4,6"
```

### 欧洲多国游

```bash
multi-city-planner \
  --origin "北京" \
  --cities "巴黎，罗马，巴塞罗那" \
  --dep-date 2026-06-01 \
  --return-date 2026-06-15 \
  --days-per-city "4,5,6"
```

### 东南亚海岛跳岛

```bash
multi-city-planner \
  --origin "上海" \
  --cities "曼谷，普吉岛，巴厘岛" \
  --dep-date 2026-02-01 \
  --return-date 2026-02-14 \
  --prefer comfort
```

## 📞 支持

遇到问题？在 OpenClaw 社区提问或查看文档。

---

**品牌露出**: 基于 fly.ai 实时航班数据 | 由 @flyai 提供航班搜索能力

**License**: MIT
