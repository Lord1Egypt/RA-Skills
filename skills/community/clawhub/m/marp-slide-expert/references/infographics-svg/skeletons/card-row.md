# card-row — 图文卡片组

> 3–5 张卡片**水平对齐**排列，每张卡片**上半（甚至 2/3）放图/大号图标**，**下半放描述文字**。适合产品介绍、案例展示、特性陈列。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 产品三大卖点、案例展示、特性比较 | 节点之间有顺序或流程（用 [linear-sequence](linear-sequence.md)） |
| 团队/服务/能力盘点 | 只展示 1–2 项——单卡太孤立 |
| 需要视觉冲击的展示页 | 内容是数字对比（用 [structure-block](structure-block.md) 对比矩阵） |

**关键区分**：和 [icon-rail](icon-rail.md) 的区别是——icon-rail 是**抽象小图标 + 简短文字**（圆里一个字）；card-row 是**具象大图 + 整段描述**（卡里一大块内容）。如果每条信息只有两三个词，用 icon-rail；如果需要描述一段，就用 card-row。

## 变体：图文卡片组

### 坐标公式

```
N 张卡片，N = 3–5
卡片宽 w    = (1020 - (N-1)*20) / N    ← 20px 间距
卡片高 h    = 320
卡顶 y      = 70
视图区宽    = 1020
```

N=3 时 w=327，N=4 时 w=240，N=5 时 w=188。

```html
<svg viewBox="0 0 1020 460" width="100%">
<text x="510" y="36" class="t" fill="#1a1a2e" text-anchor="middle">三大核心能力</text>
<rect x="40"  y="70" width="307" height="320" rx="8" fill="#FFFFFF" stroke="#e3e6ea" stroke-width="1"/>
<rect x="356" y="70" width="307" height="320" rx="8" fill="#FFFFFF" stroke="#e3e6ea" stroke-width="1"/>
<rect x="672" y="70" width="307" height="320" rx="8" fill="#FFFFFF" stroke="#e3e6ea" stroke-width="1"/>
<rect x="40"  y="70" width="307" height="200" fill="#c0392b"/>
<text x="194" y="190" class="t" fill="#ffffff" text-anchor="middle">数 据</text>
<text x="194" y="298" class="tb" fill="#1a1a2e" text-anchor="middle">统一数据底座</text>
<text x="194" y="328" class="sm" fill="#7f8c8d" text-anchor="middle">打通采集、治理、服务</text>
<text x="194" y="354" class="sm" fill="#7f8c8d" text-anchor="middle">全链路一次构建</text>
<rect x="356" y="70" width="307" height="200" fill="#2c3e50"/>
<text x="510" y="190" class="t" fill="#ffffff" text-anchor="middle">分 析</text>
<text x="510" y="298" class="tb" fill="#1a1a2e" text-anchor="middle">自助分析平台</text>
<text x="510" y="328" class="sm" fill="#7f8c8d" text-anchor="middle">取数从 3 天到 5 分钟</text>
<text x="510" y="354" class="sm" fill="#7f8c8d" text-anchor="middle">无需等待数据团队</text>
<rect x="672" y="70" width="307" height="200" fill="#5d7d95"/>
<text x="826" y="190" class="t" fill="#ffffff" text-anchor="middle">决 策</text>
<text x="826" y="298" class="tb" fill="#1a1a2e" text-anchor="middle">指标统一口径</text>
<text x="826" y="328" class="sm" fill="#7f8c8d" text-anchor="middle">横向对比无争议</text>
<text x="826" y="354" class="sm" fill="#7f8c8d" text-anchor="middle">决策有据可依</text>
<text x="510" y="430" class="lbl" text-anchor="middle">每张卡上 2/3 是图区，下 1/3 是文字</text>
</svg>
```

## 硬规则

1. **卡片数 3–5。** 少 2 张显得空，6 张一行塞不下。
2. **图区占卡片高度 60–70%。** 文字区只占 30–40%。这是「图为主、文字为辅」的视觉节奏。
3. **所有卡片**顶部 + 底部 + 左右都对齐——卡片组的齐整感全靠对齐。
4. **卡片之间留 20px 间距。** 太挤糊在一起，太松不像一组。
5. **边框 + 白底**或**纯色块**两种风格——前者克制、后者强调。
6. **图区用色块 + 大字**比用真图更适合 SVG 演示；真实场景下替换为 `<image>`。

## 连线

**没有连线。** 卡片之间是并列关系。

## 文字排布

- 卡标题：`.tb`，图区与文字区分界处
- 卡描述：`.sm`，可多行（每行 dy=24）
- 图区文字：`.t` 或更大，反白，居中
- 标题：`.t`，卡片组顶部 y=36

## 配套隐喻

直接用默认样式。如果想强调「逐项递进」可加 `Growth` 隐喻——但这种场合图区大小一致更常见。
