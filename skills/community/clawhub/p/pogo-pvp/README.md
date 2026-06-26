# PoGo-PvP Skill — Pokémon GO PvP 养号助手

基于 PvPokeTW 真实排名数据，从查排名工具升级为完整 PvP 养号助手。

## 安装

```bash
# 复制到 OpenClaw 技能目录
cp -r pogo-pvp <openclaw-workspace>/skills/

# 安装依赖
cd <openclaw-workspace>/skills/pogo-pvp
npm install

# 首次拉取数据（约 2~3 分钟）
npx tsx src/scripts/fetch.ts
# 或
npm run fetch

# 编译
npx tsc
```

## 已实现功能

### ✅ PvPokeTW 排名导入
- 自动拉取 PvPokeTW rankings（三个联盟：1500/2500/master）
- 7 天本地缓存，避免频繁请求
- 支持增量更新和完整刷新

### ✅ 排名/评分/配招查询 `/pvp 培养 <宝可梦> <联盟>`
- 显示 PvPokeTW 排名和评分
- 推荐配招（小招 + 2 充能招）
- 精英招式用 `*` 标记
- 最佳 IV / CP / 等级
- 支持中文名、英文 speciesId、别名（需收录）

### ✅ 精英招式标记
- 从 `data/elite_moves.json` 判定招式是否需要精英学习器
- 配招中自动追加 `*` 标记

### ✅ IV 本地计算
- 基于 gamemaster 种族值 + CP 公式
- 计算指定 CP 下的最佳 IV 组合
- 输出 Top50 排名
- 大师联盟默认 15/15/15，不做 IV 排名（无 CP 上限）

### ✅ 我的宝可梦库存 `/pvp 添加 / 列表 / 删除 / 修改`
- CRUD 管理本地库存（`data/my_pokemon.json`）
- 记录 IV / CP / 等级 / 招式 / 培养状态
- 支持按联盟筛选

### ✅ 值得练 `/pvp 值得练 [联盟]`
- 从库存中排序最值得培养的宝可梦
- 评分维度：物种排名 + IV 排名 + 培养状态 + 配招缺口 + 配队价值
- 优先推荐排名高、IV 好、未培养的宝可梦
- 已培养的排后面，缺配招的单独提示

### ✅ 培养顺序 `/pvp 培养顺序 [联盟]`
- 资源投入优先级排序（星尘/糖果/精英学习器）
- 输出排序理由和所需资源类型
- 已培养宝可梦排后面
- 需更新配招的单独标记

### ✅ 缺什么 `/pvp 缺什么 [联盟]`
- 对比库存和排名 Top50，找出缺少的关键宝可梦
- 推荐补入优先级和推荐配招
- 关联精英招式需求提示

### ✅ 配队推荐 `/pvp 配队 <联盟> [核心宝可梦]`
- 自动组建 3 人队伍（核心 + 安全换 + 收割）
- 无核心时自动选取库存中排名最高的宝可梦
- 三项评分：环境覆盖(60%) + 战术弹性(20%) + 队伍容错(20%)
- 标记关键威胁 Top5
- 推荐配招和精英招式需求

## 命令一览

| 命令 | 说明 | 示例 |
|------|------|------|
| `/pvp 培养 <宝> <联盟>` | 查询排名/配招/IV | `/pvp 培养 大舌舔 1500` |
| `/pvp 添加 <宝> <联盟> <IV> <CP> <等级>` | 录入库存 | `/pvp 添加 胖嘟嘟 1500 1/14/14 1498 24.5` |
| `/pvp 列表 [联盟]` | 查看库存 | `/pvp 列表 1500` |
| `/pvp 删除 <宝> <联盟>` | 删除库存 | `/pvp 删除 胖嘟嘟 1500` |
| `/pvp 修改 <宝> <联盟> [字段] [值]` | 修改库存 | `/pvp 修改 胖嘟嘟 1500 built true` |
| `/pvp 值得练 [联盟]` | 培养优先级 | `/pvp 值得练` |
| `/pvp 培养顺序 [联盟]` | 资源投入顺序 | `/pvp 培养顺序 1500` |
| `/pvp 缺什么 [联盟]` | 缺少的关键宝可梦 | `/pvp 缺什么` |
| `/pvp 配队 <联盟> [核心]` | 自动配队推荐 | `/pvp 配队 1500 胖嘟嘟` |

## 联盟参数

| 输入 | 联盟 |
|:----:|:----:|
| `1500` / `超级` / `超级联盟` | 超级联盟 |
| `2500` / `高级` / `高级联盟` | 高级联盟 |
| `master` / `大师` / `大师联盟` / `无限制` | 大师联盟 |

## 数据源

- **排名数据**：PvPokeTW（繁体中文版）— `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/`
- **gamemaster**：同 PvPoke 官方 `gamemaster.json`
- **精英招式**：社区整理，存于 `data/elite_moves.json`

## 限制

1. **非官方工具** — 本项目基于 PvPoke 开源数据，与 Pokémon GO 官方无关
2. **数据依赖** — 所有排名/评分/配招数据依赖 PvPokeTW 导出的 JSON 缓存
3. **IV 排名偏差** — 本地 IV 计算与 PvPokeTW 网站可能存在 1~2 位排名差，属正常偏差
4. **大师联盟 IV** — 大师联盟无 CP 上限，默认使用 15/15/15，不做 IV 排名
5. **无胜率模拟** — 不做对战模拟或胜率预测，配队推荐基于排名和队伍角色
6. **精灵招式名前缀空格问题** — 部分招式名前多了一个空格，这是 PvPoke raw data 的格式，尚未修复

## 目录结构

```
pogo-pvp/
├── skill.yaml              # OpenClaw 技能元信息
├── SKILL.md                # 技能使用说明
├── README.md               # 本文件
├── package.json            # Node 包配置
├── tsconfig.json           # TypeScript 配置
├── .gitignore              # Git 忽略规则
├── src/
│   ├── index.ts            # OpenClaw 命令入口
│   ├── fetcher.ts          # PvPoke 数据拉取与缓存
│   ├── query.ts            # 宝可梦查询逻辑
│   ├── mapper.ts           # 中文名映射（species、moves、types）
│   ├── types.ts            # 类型定义
│   ├── iv.ts               # IV 计算
│   ├── list.ts             # 库存管理
│   ├── add.ts              # 库存添加
│   ├── train.ts            # 值得练
│   ├── buildOrder.ts       # 培养顺序
│   ├── missing.ts          # 缺什么
│   └── team.ts             # 配队推荐
├── scripts/
│   └── fetch.ts            # 数据拉取脚本
├── data/
│   ├── my_pokemon.example.json  # 库存模板（请重命名使用）
│   ├── pokemon_alias.json       # 别名映射
│   └── elite_moves.json         # 精英招式清单
├── cache/
│   ├── rankings-1500.json
│   ├── rankings-2500.json
│   ├── rankings-master.json
│   └── gamemaster.json
└── docs/
    ├── roadmap.md
    ├── build-order-plan.md
    ├── league-fit-plan.md
    ├── missing-core-plan.md
    ├── move-cn-plan.md
    └── train-priority-plan.md
```
