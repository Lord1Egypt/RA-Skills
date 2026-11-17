# icon-rail — 水平属性列表

> 3–6 个**不同颜色**的图标圆圈，**水平对齐**，上下各 1–2 行文字。用来**罗列事物的不同属性或不同方面**。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 罗列同一事物的几个维度（产品五大特性、服务三个亮点） | 节点之间有顺序或阶段关系（用 [linear-sequence](linear-sequence.md) 箭头串） |
| 罗列并列的不同侧面 | 只有 1–2 项，列出来太单薄 |
| 摘要性列举（年度成绩、关键能力） | 节点超过 6 个——一行太长，缩到 80% 字号都看不清 |

**关键区分**：节点之间**没有顺序、没有层级、没有因果**——只是几个并列项摆在一起。要是有顺序，改箭头串。

## 变体：水平属性列表

### 坐标公式

```
N 个图标，水平对齐
每个图标：圆 + 上下两行文字（最多 2 行）
中心 cx_i  = (1020 / (N+1)) * (i+1)
列间距   = 1020 / (N+1)  ≈ 730 / N（N=3 时 ~245，N=6 时 ~146）
文字     .sm 居中，14–15px
图标圆   r = 44
图标上方  1–2 行标签，字号 .sm
图标下方  1–2 行说明，字号 .sm，颜色更浅
图标颜色  每项一个色（一项一色，便于区分）
```

```html
<svg viewBox="0 0 1020 360" width="100%">
<text x="510" y="36" class="t" fill="#1a1a2e" text-anchor="middle">产品五大特性</text>
<circle cx="150" cy="170" r="44" fill="#c0392b"/>
<circle cx="320" cy="170" r="44" fill="#2c3e50"/>
<circle cx="510" cy="170" r="44" fill="#5d7d95"/>
<circle cx="700" cy="170" r="44" fill="#E87461"/>
<circle cx="870" cy="170" r="44" fill="#D4A843"/>
<text x="150" y="178" class="tb" fill="#ffffff" text-anchor="middle">快</text>
<text x="320" y="178" class="tb" fill="#ffffff" text-anchor="middle">稳</text>
<text x="510" y="178" class="tb" fill="#ffffff" text-anchor="middle">省</text>
<text x="700" y="178" class="tb" fill="#ffffff" text-anchor="middle">活</text>
<text x="870" y="178" class="tb" fill="#ffffff" text-anchor="middle">省</text>
<text x="150" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">性能</text>
<text x="320" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">稳定</text>
<text x="510" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">成本</text>
<text x="700" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">灵活</text>
<text x="870" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">效率</text>
<text x="150" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">3 秒内完成</text>
<text x="320" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">99.9% 在线</text>
<text x="510" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">-30% 投入</text>
<text x="700" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">按需扩缩</text>
<text x="870" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">一份占用</text>
<text x="510" y="332" class="lbl" text-anchor="middle">颜色区分维度，文字强化含义</text>
</svg>
```

## 硬规则

1. **节点数 3–6。** 少于 3 显得单薄，多于 6 一行放不下。
2. **每个图标一个颜色。** 不要所有圆都用同一色——并列项的视觉区分靠颜色。
3. **图标中心一字（≤ 2 个中文字）**，作为该维度的核心词。
4. **图标上方是标签（具体名词），下方是说明（一句话）。** 三层结构读起来层次分明。
5. **图标水平对齐**——所有圆心 cy 相同。垂直漂移会破坏「罗列」的视觉感。
6. **颜色不要用渐变**——每个圆是单一实色（见通用底线）。

## 连线

**没有连线。** 这是骨架的核心纪律——并列项之间没有关系线，只靠水平对齐和颜色区分。要画连线说明骨架选错了。

## 文字排布

- 标签：`.sm`，深色 `#1a1a2e`
- 说明：`.sm`，浅色 `#7f8c8d`
- 标签 ≤ 4 字，说明 ≤ 12 字
- 中心图标文字：`.tb` 粗体，反白
- 标题：`.t`，图顶 y=36

## 配套隐喻

直接用默认样式，不需要换壳。如要强调「环环相扣」可叠 `Cycle` 隐喻的环形虚线（很少用）。
