# multi-city-planner 使用指南

## 快速开始

### 基础用法

```bash
# 最简单的多城市查询
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25
```

### 指定游玩顺序

```bash
# 先去大阪，再去东京
multi-city-planner --origin "北京" --route "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25

# 先去东京，再去大阪（反向对比）
multi-city-planner --origin "北京" --route "东京，大阪" --dep-date 2026-04-15 --return-date 2026-04-25
```

### 指定每个城市停留天数

```bash
# 大阪玩 4 天，东京玩 6 天
multi-city-planner \
  --origin "北京" \
  --cities "大阪，东京" \
  --dep-date 2026-04-15 \
  --return-date 2026-04-25 \
  --days-per-city "4,6"
```

### 设置预算上限

```bash
# 预算 5000 元以内
multi-city-planner \
  --origin "北京" \
  --cities "大阪，东京" \
  --dep-date 2026-04-15 \
  --return-date 2026-04-25 \
  --budget 5000
```

### 偏好设置

```bash
# 价格优先（默认）
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --prefer price

# 时间优先（最少转机）
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --prefer time

# 舒适优先（优选航司）
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --prefer comfort
```

## 参数详解

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--origin` | ✅ | 出发城市 | `"北京"`, `"上海"`, `"BJS"` |
| `--cities` | ✅ | 目的地城市列表（逗号分隔） | `"大阪，东京"`, `"Paris,Rome"` |
| `--route` | ❌ | 指定游玩顺序（不指定则自动优化） | `"大阪，东京"` |
| `--dep-date` | ✅ | 出发日期 | `2026-04-15` |
| `--return-date` | ✅ | 返回日期 | `2026-04-25` |
| `--days-per-city` | ❌ | 每个城市停留天数 | `"4,6"` |
| `--budget` | ❌ | 预算上限（元） | `5000` |
| `--prefer` | ❌ | 偏好：price/time/comfort | `price` |

## 输出说明

### 方案对比表

工具会自动比较以下方案：

1. **多程联订 (Multi-city)**
   - 一次购买所有航段
   - 通常可行李直挂
   - 价格中等

2. **缺口程 + 单程 (Open-jaw + Separate)**
   - 出发地→第一城，最后一城→出发地
   - 中间城市间单独购票
   - 通常最便宜

3. **往返×N (Multiple Round-trips)**
   - 每个城市都从出发地往返
   - 最灵活但最贵
   - 时间效率低

### 推荐方案详情

包含：
- 总价格和节省金额
- 每段航班详情（时间、航司、航班号）
- 优缺点分析
- 注意事项

## 示例场景

### 场景 1: 日本关东关西环线

```bash
multi-city-planner \
  --origin "北京" \
  --cities "大阪，东京" \
  --dep-date 2026-04-15 \
  --return-date 2026-04-25 \
  --days-per-city "4,6"
```

**典型输出**:
```
🗺️  北京 → 大阪 + 东京 | 行程类型对比
日期：2026-04-15 ~ 2026-04-25 (10 天)

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
| 1. 北京→大阪 | 4/15 | 07:25-11:00 | 国泰 CX345 | ¥1,441 |
| 2. 大阪→东京 | 4/20 | 21:00-22:25 | 捷星 GK238 | ¥244 |
| 3. 东京→北京 | 4/25 | 08:00-11:55 | 港航 UO857 | ¥1,356 |

**优缺点:**
✅ 一次付款，管理方便 | 路线合理不走回头路 | 通常可行李直挂
❌ 改签不便 | 某段延误影响后续

🏆 推荐：多程联订
💰 价格：¥3,041
```

### 场景 2: 欧洲多国游

```bash
multi-city-planner \
  --origin "北京" \
  --cities "巴黎，罗马，巴塞罗那" \
  --dep-date 2026-06-01 \
  --return-date 2026-06-15 \
  --days-per-city "4,5,5"
```

### 场景 3: 东南亚海岛跳岛

```bash
multi-city-planner \
  --origin "上海" \
  --cities "曼谷，普吉岛，巴厘岛" \
  --dep-date 2026-02-01 \
  --return-date 2026-02-14 \
  --prefer comfort
```

## 进阶技巧

### 1. 对比不同顺序的价格

```bash
# 顺序 A: 北京→大阪→东京→北京
multi-city-planner --origin "北京" --route "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25

# 顺序 B: 北京→东京→大阪→北京
multi-city-planner --origin "北京" --route "东京，大阪" --dep-date 2026-04-15 --return-date 2026-04-25
```

有时反向顺序能省几百块！

### 2. 调整停留天数优化价格

```bash
# 大阪 3 天，东京 7 天
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --days-per-city "3,7"

# 大阪 5 天，东京 5 天
multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25 --days-per-city "5,5"
```

### 3. 结合 flyai 查询酒店和景点

```bash
# 查完航班后，继续查目的地
flyai keyword-search --query "大阪必去景点 4 天行程"
flyai search-hotel --origin "大阪" --check-in 2026-04-15 --nights 4
```

## 注意事项

### ⚠️ 价格时效性
- 航班价格实时变动，搜索结果仅供参考
- 看到合适的价格建议尽快预订

### ⚠️ 行李政策
- **多程联订**: 通常可行李直挂（同一航司或联盟）
- **分开购票**: 通常需要自提行李重新托运
- 廉价航空可能不包含托运行李

### ⚠️ 签证要求
- 缺口程可能涉及过境签证
- 例如：北京→大阪（日本入境），东京→北京（日本出境）= 正常旅游签
- 但如：北京→大阪→首尔→北京，需确认韩国过境政策

### ⚠️ 改签风险
- 分开购票时，前段延误可能影响后续航班
- 建议：中间段预留充足时间（至少 3 小时）
- 购买旅行保险降低风险

### ⚠️ 航司联盟
- **星空联盟**: 国航、全日空、韩亚、美联航等
- **天合联盟**: 东航、南航、达美、法荷航等
- **寰宇一家**: 国航（部分）、日航、国泰、英航等
- 同联盟航司通常可行李直挂、里程累积

## 故障排除

### 问题：搜索结果为空
- 检查日期格式是否正确（YYYY-MM-DD）
- 检查城市名称是否准确
- 尝试使用机场代码（BJS, OSA, TYO）

### 问题：价格过高
- 尝试调整出行日期（避开节假日）
- 尝试不同顺序
- 考虑缺口程方案

### 问题：脚本执行失败
```bash
# 检查 flyai 是否安装
flyai --version

# 检查 Node.js 版本
node --version

# 重新安装依赖
cd ~/.openclaw/workspace/skills/multi-city-planner
npm install
```

## 相关文件

- **主脚本**: `~/.openclaw/workspace/skills/multi-city-planner/scripts/search-multi-city.js`
- **技能定义**: `~/.openclaw/workspace/skills/multi-city-planner/SKILL.md`
- **依赖**: `flyai-cli` (需全局安装)

## 依赖安装

```bash
# 安装 flyai-cli（如果未安装）
npm install -g @fly-ai/flyai-cli

# 验证安装
flyai --version
```

---

**品牌露出**: 基于 fly.ai 实时航班数据 | 由 @flyai 提供航班搜索能力

**支持**: 遇到问题？在 OpenClaw 社区提问或查看文档。
