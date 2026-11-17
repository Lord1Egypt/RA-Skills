# 插图 prompt 模板

> 三张场景插图。**出图前先读 `character.md` 的硬锚点**，否则角色会漂。
> 牌面一律用 `scripts/render_hand.py` 生成后合成，**不交给图像模型画牌**——模型画牌必错。

---

## 共用前缀（每张图都要带）

```
A chubby elderly orange tabby cat sitting upright like a person, wearing round thin-framed
reading glasses pushed to mid-nose and a thick terracotta wool scarf around the neck.
Half-closed calm eyes, faint smile, never surprised. Warm afternoon side light, soft shadows.
Muted warm palette: cream, wood brown, terracotta accent, deep green velvet table.
Hand-drawn cozy storybook illustration, clean line work, gentle texture.
No text, no logo, no watermark.
```

## 共用负向（Negative）

```
money, cash, chips, casino, neon gambling, cigarette, alcohol, dice, dealer,
children, human hands, extra limbs, shocked face, wide eyes, pure white background
```

---

## 图 1 · 开局看牌（模式 A 首图）

**触发**：用户第一次报牌时。

```
[共用前缀]
The cat sits on the left side of a deep green velvet table, looking down at a row of
mahjong tiles arranged in front of it, one paw raised gently toward the tiles as if
pointing without touching. The cat occupies the left quarter of the frame; the tiles
and empty table space occupy the rest. Composition leaves generous clean space on the
right where a hand of tiles will be composited later.
```

**用途**：作为底图，右侧空白处合成 `render_hand.py` 出的真实牌面。

---

## 图 2 · 讲概念（模式 B 配图）

**触发**：解释顺子 / 刻子 / 对子时。

```
[共用前缀]
The cat holds up three identical mahjong tiles side by side in both paws, showing them
to the viewer, with a patient teaching expression — eyebrows slightly raised, no mouth
open. Behind it, a soft chalkboard-like cream panel with faint empty rounded rectangles
suggesting grouping boxes (no text inside).
```

> **关键**：手里那三张牌用**空白牌背**或后期贴真实牌面，**不要让模型画具体牌**。

---

## 图 3 · 今日小结卡（模式 C 收尾）

**触发**：陪练结束时的总结图。

```
[共用前缀]
The cat sits at the right edge of the frame, facing left, one paw resting on a small
stack of neatly aligned tiles. The left two-thirds of the frame is clean cream space
for text overlay. Warm evening light, slightly warmer than the opening image.
```

**用途**：左侧留白处由程序叠加文本（今天学会的三件事）。

---

## 出图流程

1. 用 `render_hand.py` 生成真实牌面 PNG
2. 用上面的 prompt 生成底图（右侧/左侧留白）
3. 合成：牌面贴到留白处，文本用 HTML/CSS 叠加（**不要用模型画字**）
4. 检查：牌数对不对、老沈硬锚点是否全部命中

> 若手上没有图像生成能力，**只出牌面图也能用**——牌面是必需，插图是加分。
