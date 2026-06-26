---
name: pogo-pvp
description: Pokémon GO PvP 培养查询技能 v1.1。基于 PvPokeTW 真实排行数据 + gamemaster 基础种族值，提供排名查询、最佳 IV、用户 IV 对比等功能。
---

# PoGo-PvP — Pokémon GO PvP 培养查询 v1.1

数据源：**PvPokeTW**（[pvpoketw.com](https://pvpoketw.com/)）→ 翻译自 PvPoke，排行 JSON 拉取自 `pvpoke/pvpoke` GitHub raw，gamemaster 含宝可梦基础种族值与类型。

## 命令

`/pvp 培养 <宝可梦> <联盟> [攻击/防御/生命]`

### 参数

| 参数 | 示例 | 说明 |
|:----|:----|:----|
| 宝可梦 | `玛力露丽` / `水兔子` / `azumarill` | 支持中文/英文/别名 |
| 联盟 | `1500` / `超级联盟` / `master` / `大师` | 自动识别简写 |
| IV（可选） | `1/15/10` / `0/15/15` | 攻击/防御/HP 各 0~15 |

### 输出字段（无用户 IV）

| 字段 | 来源 | 说明 |
|:----|:----|:-----|
| 宝可梦 | speciesId → 中文映射 | 本地字典 |
| 联盟 | 参数解析 | 自动识别 |
| PvPokeTW排名 | 数组 index + 1 | PvPoke 排行 |
| 评分 | score | PvPoke 综合评分 0~100 |
| 属性 | gamemaster | 类型中文（如 `[水][妖精]`） |
| 推荐招式 | moveset | 官方推荐配置（中文） |
| 最佳 IV | IV 计算 | 4096 种组合中排名第 1 |
| 最佳 CP | IV 计算 | 对应最佳 IV 的 CP |
| 最佳等级 | IV 计算 | 对应最佳 IV 的等级（支持半级） |
| 精英TM | — | 暂无准确数据 |
| 招式池 | fastMoves / chargedMoves | 全部可用招式 |
| 对战分析 | matchups / counters | 前 5 条 |
| 数据来源 | — | PvPokeTW |
| 更新时间 | — | UTC |

### 输出字段（有用户 IV）

新增对比块：

| 字段 | 说明 |
|:----|:-----|
| 我的 IV | 用户输入的 IV 组合 |
| 我的 CP | 该 IV 在联盟限制下的 CP |
| 我的等级 | 该 IV 升级到的等级 |
| 我的 IV 排名 | 在前 50 内显示排名，否则「未进入前 50」 |
| 差别 | 最佳 IV - 用户 IV 的各维差值 |
| 最佳 IV | 排名第 1 的 IV 组合 |

### 示例

```
宝可梦：弃世猴
联盟：超级联盟
PvPokeTW排名：#28
评分：90.1
属性：[格斗][幽灵]
推荐招式：踢倒 + 愤怒之拳 + 近身战
最佳 IV：0/13/14
最佳 CP：1500
最佳等级：17
精英TM：暂无准确数据

我的 IV：1/15/10
我的 CP：1455
我的等级：16.5
我的 IV 排名：未进入前50
差别：攻击 -1，防御 -2，生命 4
最佳 IV：0/13/14
```

**规则：**
1. 不显示乘积
2. 不计算乘积
3. 不显示百分比接近度
4. 不用乘积判断好坏
5. IV / CP / 等级只能来自 PvPokeTW 真实数据
6. 查不到就显示「暂无准确数据」
7. 不允许模拟、不允许随机、不允许补编

## 数据管理

```bash
# 拉取/刷新所有联盟缓存
python scripts/fetch_pvpoke.py --league 1500
python scripts/fetch_pvpoke.py --league 2500
python scripts/fetch_pvpoke.py --league master

# gamemaster 自动在查询时拉取，过期自动刷新

# 手动测试
node dist/index.js 弃世猴 1500
node dist/index.js 弃世猴 1500 1/15/10
node dist/index.js --test
```

## 缓存策略

- 缓存目录：`cache/`
- rankings TTL：7 天
- gamemaster TTL：7 天
- 过期自动回退网络拉取
- 无缓存也拉不到 → 提示

## IV 计算原理

IV 排序来源于 PvPokeTW 数据，不保证所有联盟字段完整。

对所有 4096 种 IV 组合：
- 找到每个组合在 CP ≤ 联盟限制下的**最高等级**
- 内部排序参考原始数据字段
- 取前 50 名

## 数据字典

详见 `data/` 目录：
- `pokemon_alias.json` — 中文俗称/别名 → speciesId
- `src/mapper.ts` — speciesId / moveId → 中文名

## 限制

- ✅ 所有数据来自 PvPoke/PvPokeTW 真实数据源
- ✅ IV/CP/等级均为真实可信计算结果
- ✅ 不输出乘积、不对比乘积、不显示接近度
- ❌ 不猜 XL 糖需求（gamemaster 不含 XL 关联字段）
- ❌ 不生成截图/OCR/组队

## 扩展计划（v1.2+）

1. elite_moves.json 白名单 → 精英TM 判断
2. 中文名全覆盖（800+ speciesId）
3. 属性相性 / 招式属性补充
4. 支持 XL 糖提示（需 PoGo API 或用户输入等级）
