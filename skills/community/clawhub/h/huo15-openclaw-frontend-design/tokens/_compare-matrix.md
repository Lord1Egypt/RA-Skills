# 8 流派横向对比矩阵 ⭐v4.1

> 给 `huo15-openclaw-design-director` 选流派用，或用户要做 multi-genre 平行对比时的速查表。

## 关键 token 对比

| 流派 | 主色 (oklch) | 重音色 | display 字体 | radius 哲学 | 适合场景 |
|---|---|---|---|---|---|
| **bold-minimal** | 0.18 0 0（墨黑） | 0.66 0.20 28（锐橙） | Playfair Display 900 italic | sm 2 / md 8 / lg 14 / pill | 科技、B 端、作品集 |
| **editorial** | 0.20 0.015 280（冷墨） | 0.50 0.18 25（砖红） | DM Serif Display 400 | sm 2 / md 4 / lg 8 | 内容、品牌故事、报告 |
| **brutalist** | 0.10 0 0（真黑） | 0.78 0.22 105（警示黄） | Space Grotesk 700 + JetBrains Mono | 全 0（直角） | 独立工作室、Web3、先锋 |
| **retro-future** | 0.13 0.04 280（深紫蓝 bg） | 0.85 0.18 195 / 0.72 0.25 5（霓虹双色） | Major Mono Display + VT323 | 主 0 / lg 4 | 游戏、音乐、娱乐 |
| **organic** | 0.28 0.04 50（棕墨） | 0.62 0.13 45（土橙） | Caveat 600 + Source Serif | irregular 4 段 / soft 24 / pill | 食品、母婴、健康 |
| **mobile-native-ios** | 0.18 0.005 280（HIG 墨） | 0.66 0.16 50（暖橙替代系统蓝） | Manrope 800 | icon 8 / button 7 / list 14 / fab 18 | iOS APP / iPhone H5 |
| **mobile-native-md3** | 0.55 0.13 175（青绿 seed） | dynamic primary container | DM Sans 700 | chip 8 / card 16 / fab 18 / topBar 24 | Android APP / MD3 |
| **mobile-native-harmony** | 0.18 0.01 260（鸿蒙墨） | 4 灵动色块同明度 L≈0.78 | Noto Sans SC 700/900 + DM Sans | control 14 / tile 24 / card 28 / hero 32 | HarmonyOS / 鸿蒙生态 |

## 反差对位（multi-genre 三选时常用）

| 命题 | 流派组合 |
|---|---|
| 理性 vs 感性 vs 实验 | bold-minimal × organic × brutalist |
| 冷峻 vs 温暖 vs 复古 | editorial × organic × retro-future |
| 桌面 vs 移动 vs 跨端 | bold-minimal × mobile-native-ios × mobile-native-harmony |
| 极简 vs 信息密度 vs 装饰 | bold-minimal × editorial × retro-future |
| Web 端 vs 双移动端 | bold-minimal × mobile-native-md3 × mobile-native-harmony |

## redLineWaiver 速查

| 流派 | 豁免说明 |
|---|---|
| brutalist | radius 全 0 是 hallmark，**不是**红线 #9 违规 |
| retro-future | bg 深紫蓝纯色（非渐变），霓虹靠 text-shadow 不靠 backdrop-blur |
| organic | irregular radius 4 段不同百分比，不犯统一 16px |
| mobile-native-ios | accent 暖橙替代 #007AFF（红线 #8 合规：Apple 自家 App 也这么做） |
| mobile-native-md3 | seed 青绿避开 Material 默认紫 |
| mobile-native-harmony | 4 灵动色块同明度多色相，避免单色一统天下 |

## motion 哲学速查 ⭐v4.5

| 流派 | 主 duration | 主 easing | stagger | 一句话动效原则 |
|---|---|---|---|---|
| **bold-minimal** | normal 300ms | standard | 80ms | 克制 — 单一 easing、绝不弹跳 |
| **editorial** | normal 400ms / slow 700ms | decelerate | 120ms | 稳重 — 偏长 duration 模仿翻页 |
| **brutalist** | instant 80ms / fast 120ms | linear / step2 | 30ms | 硬切 — 禁缓动函数 |
| **retro-future** | blink 1000ms 周期 | step2 / linear | 50ms | CRT 闪烁 — 用 step 模拟显像管 |
| **organic** | normal 500ms / slow 800ms | spring（1.56 超调） | 140ms | 弹性 — 卡片落下有回弹 |
| **mobile-native-ios** | normal 350ms | iosSpring | 70ms | Apple HIG spring |
| **mobile-native-md3** | medium2 300ms | emphasized | 75ms | MD3 完整 12 档 duration + 4 档 emphasized easing |
| **mobile-native-harmony** | normal 300ms | fluid | 80ms | 鸿蒙流畅感（比 iOS 偏快） |

**反差选 motion 的命题**：
- 静态 vs 闪烁 vs 弹性：bold-minimal × retro-future × organic
- 克制 vs 严谨 vs 灵动：brutalist × md3 × harmony

详细 motion token JSON 见 [`<slug>.json`](.) 的 `motion` 字段；导出到 CSS / Tailwind / Figma 见 [`exporters/`](exporters/)。

## design-director 集成点

director 需要挑 3 流派对比时，对每个候选：
1. 读 [`<slug>.json`](.) 拿 color / typography / spacing / radius
2. 看 redLineWaiver（避免误判违规）
3. 用 `examples/<dir>/index.html` 作 Junior pass 起手（不用空白起步）
4. 截 3 张图喂给五维矩阵打分

详细接力流程见 [`../references/multi-genre-compare.md`](../references/multi-genre-compare.md)。
