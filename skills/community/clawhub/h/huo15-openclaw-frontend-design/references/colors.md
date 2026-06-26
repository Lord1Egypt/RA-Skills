# 5 流派配色基线（oklch）

> 全部使用 oklch 色空间。**禁紫渐变、禁 AI 模糊渐变背景**（参见 SKILL.md §四 红线 #2 / #11）。
>
> **⭐v4.0 起**：每个流派的配色已落到结构化 [`tokens/<slug>.json`](../tokens/) — 本文档保留可读的人类视角说明，jq 一行可转 CSS variables / Tailwind / Figma。配色硬规则源头仍在本文档。

## 1. BOLD-MINIMAL · 勇敢极简

| 角色 | oklch | 用途 |
|---|---|---|
| ink | `oklch(0.18 0 0)` | 主文字、主结构线 |
| paper | `oklch(0.99 0.005 95)` | 背景，几乎纯白带极淡暖调 |
| accent | `oklch(0.66 0.20 28)` | 锐利橙红，仅用于强调（hover / em） |
| mute | `oklch(0.45 0 0)` | 次要文字 |

**比例**：墨黑 20% / 留白 70% / 强调 10%。

## 2. EDITORIAL · 编辑杂志

| 角色 | oklch | 用途 |
|---|---|---|
| paper | `oklch(0.97 0.012 75)` | 暖纸色 |
| ink | `oklch(0.20 0.015 280)` | 偏冷的墨黑 |
| accent | `oklch(0.50 0.18 25)` | 砖红，首字下沉 / kicker / 引号 |
| mute | `oklch(0.42 0.02 280)` | 副文字 |
| rule | `oklch(0.20 0.015 280 / .25)` | 细分隔线 |

**比例**：纸 75% / 墨 18% / 砖红 5% / 灰线 2%。

## 3. BRUTALIST · 野兽派

| 角色 | oklch | 用途 |
|---|---|---|
| paper | `oklch(0.985 0 0)` | 近纯白（不做暖偏） |
| ink | `oklch(0.10 0 0)` | 真黑，6px 粗边 |
| warn | `oklch(0.78 0.22 105)` | 警示黄，stamp 块 |

**比例**：白 60% / 黑 30% / 警示黄 10%。**只许 3 色**。

## 4. RETRO-FUTURE · 复古未来

| 角色 | oklch | 用途 |
|---|---|---|
| bg | `oklch(0.13 0.04 280)` | 深夜紫蓝（注意：纯色，**不是渐变**） |
| ink | `oklch(0.96 0.04 110)` | 暖白主字 |
| neon-cyan | `oklch(0.85 0.18 195)` | 霓虹青 |
| neon-magenta | `oklch(0.72 0.25 5)` | 霓虹洋红（**不是紫**） |

**红线声明**：本流派使用霓虹双色对撞，**不得退化成紫渐变模糊背景**。所有发光必须由 `text-shadow` 多层叠加产生，禁用 `filter: blur()` 大色块当氛围。

## 5. ORGANIC · 有机自然

| 角色 | oklch | 用途 |
|---|---|---|
| paper | `oklch(0.96 0.025 85)` | 米白偏暖 |
| ink | `oklch(0.28 0.04 50)` | 棕墨 |
| clay | `oklch(0.62 0.13 45)` | 土橙 |
| moss | `oklch(0.45 0.10 145)` | 森林绿 |
| sky | `oklch(0.78 0.07 220)` | 雾蓝 |

**比例**：纸 60% / 棕墨 15% / 三原色（土橙 / 苔绿 / 雾蓝）各 8% 左右。

## 6. MOBILE-NATIVE · 移动原生 ⭐v2.1

> 三套对照不是要你"复制官方默认色"——而是体现各平台的**色彩语义体系**。

### 6.1 iOS HIG 风（推荐自有 brand color，避开系统蓝）

| 角色 | oklch | 用途 |
|---|---|---|
| paper | `oklch(0.985 0.005 75)` | non-grouped 背景（暖中性） |
| grouped-bg | `oklch(0.94 0.005 75)` | grouped table view 背景 |
| ink | `oklch(0.18 0.005 280)` | label 主字 |
| mute | `oklch(0.55 0.01 280)` | secondary label |
| sep | `oklch(0.88 0.005 280)` | separator 0.5pt |
| accent | `oklch(0.66 0.16 50)` | brand 强调（暖橙）— **替代 system blue** |

**红线**：禁直接用 `#007AFF`（红线 #8）。Apple 自家 App（Music / Books / News）也都用品牌色而非系统蓝。

### 6.2 Material Design 3（dynamic color，seed 自选）

| 角色 | oklch | 派生方式 |
|---|---|---|
| seed | `oklch(0.55 0.13 175)` | **自选**色相（示例青绿，**避开 Material 默认紫**） |
| primary | `oklch(0.55 0.13 175)` | = seed |
| primary-container | `oklch(0.88 0.06 175)` | seed L+33 / C-50% |
| secondary-container | `oklch(0.92 0.04 60)` | seed hue+245 / 低饱和 |
| tertiary-container | `oklch(0.90 0.05 320)` | seed hue+145 / 低饱和 |
| surface | `oklch(0.985 0.003 175)` | 近白带极淡 seed 色相 |
| surface-variant | `oklch(0.93 0.01 175)` | 比 surface 暗 5% |
| outline | `oklch(0.72 0.01 175)` | mid-tone |

**规则**：seed 选 oklch C ∈ [0.10, 0.18]，避免高饱和（饱和过 → 派生 container 太脏）。

### 6.3 HarmonyOS 鸿蒙（灵动色块）

| 角色 | oklch | 用途 |
|---|---|---|
| paper | `oklch(0.97 0.005 240)` | 主背景 |
| paper-2 | `oklch(0.94 0.008 240)` | hero / scene 卡片 |
| ink | `oklch(0.18 0.01 260)` | 主字 |
| mute | `oklch(0.50 0.01 260)` | 副字 |
| c-cyan | `oklch(0.78 0.12 220)` | 灵动青 |
| c-orange | `oklch(0.78 0.13 55)` | 灵动橙 |
| c-green | `oklch(0.78 0.14 145)` | 灵动绿 |
| c-pink | `oklch(0.82 0.10 5)` | 灵动粉 |

**规则**：4 个灵动色 **同明度（L≈0.78）+ 同低饱和（C≈0.10–0.14）+ 不同色相**。同明度让多色拼一起不打架，这是鸿蒙"灵动色块"的核心。

---

## 通用约束

- **禁** evenly-distributed palette（5 色等比例）
- **禁** 默认暗黑 `#121212` + 紫主题
- **禁** 全局 iOS 系统蓝 `#007AFF`、警示红 `#FF3B30` 当主色
- **强制** oklch；如需 fallback 可附 hex 注释，但 hex 不能是唯一来源
- 主色单一（**60–70%**）+ 强调色锐利（**5–10%**）+ 中性（20–30%）
