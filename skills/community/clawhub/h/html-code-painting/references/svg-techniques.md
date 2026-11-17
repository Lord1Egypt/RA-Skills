# SVG 质感技术手册（svg-techniques）

SVG 的还原能力来自三层武器：**路径功力、滤镜配方、混合模式**。本文按质感分类给出可直接
套用的滤镜起手参数。所有示例默认画布 `<svg viewBox="0 0 1600 900">`。

## 0. 性能红线（先读）

- 同一页面同时存活的 `feTurbulence` 滤镜 ≤ **2 个**；每个滤镜的作用区域用
  `x="-10%" y="-10%" width="120%" height="120%"` 收紧，避免整屏重算。
- 能对**图层组**施加的滤镜不要逐元素施加。
- `filter: url(#x)` 与 CSS `filter: blur()` 混用时，模糊半径 >8px 的元素总数控制在个位数。

## 1. 纸张 / 画布纹理（打底，先铺最下层）

```xml
<filter id="paperGrain">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" result="noise"/>
  <feColorMatrix in="noise" type="matrix"
    values="0 0 0 0 0.94  0 0 0 0 0.91  0 0 0 0 0.84  0 0 0 0.06 0"/>
  <feComposite operator="over" in2="SourceGraphic"/>
</filter>
```
用法：罩在最上层一个全屏 `<rect filter="url(#paperGrain)"/>`，透明度极低(6%)模拟纸纤维。
`baseFrequency` 越大颗粒越细：宣纸 0.7–1.0，亚麻油画布 0.35–0.5。

## 2. 宣纸晕染 / 墨迹边缘（水墨核心）

```xml
<filter id="inkBleed">
  <feTurbulence type="fractalNoise" baseFrequency="0.05 0.09" numOctaves="3" seed="7" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="14"/>
</filter>
```
- 供墨线笔画使用（path stroke 用此滤镜）：scale=8 是"笔锋微颤"，14–22 是"渗墨"，>30 变抽象。
- 让墨色有浓淡：路径填充不用纯黑，改用线性渐变 #222→#555→#111，
  再叠 `mix-blend-mode: multiply` 于纸上。

## 3. 干擦皴 / 山石肌理

```xml
<filter id="dryBrush">
  <feTurbulence type="turbulence" baseFrequency="0.12 0.02" numOctaves="4" seed="11" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="20"/>
  <feComponentTransfer><feFuncA type="gamma" amplitude="1" exponent="0.6"/></feComponentTransfer>
</filter>
```
要点：**两个方向频率差要大**（0.12 vs 0.02）——水平拉丝=斧劈皴方向感。
山体做法：剪影 path → 罩同形 path 用此滤镜 + 半透明深色 → 再叠 2–3 条沿山势的手绘皴线。

## 4. 云雾 / 烟霭（screen 型亮雾）

```xml
<filter id="mist">
  <feTurbulence type="fractalNoise" baseFrequency="0.008 0.02" numOctaves="4" seed="42" result="n"/>
  <feColorMatrix in="n" type="matrix"
    values="0 0 0 0 0.96  0 0 0 0 0.97  0 0 0 0 1.0  0 0 0 0.5 0"/>
  <feComposite operator="in" in2="SourceGraphic"/>
</filter>
```
套在一团不规则椭圆上产生流动雾气；跨层衔接处再叠一层
`linear-gradient(to top, 天色, transparent)` 的 rect 做"山脚呼吸"。雾永远比它遮住的物体亮且低饱和。

## 5. 油画厚涂 / 颜料堆叠感

组合拳（无单条滤镜可达）：
1. 底层：色块间留 1–2px 缝隙露底色（模拟干湿接缝）；
2. 中层：同一形状复制 2–3 层，各偏移 2–4px、色明度 ±8%，制造堆叠厚度;
3. 表层：`feDisplacementMap scale=6 + baseFrequency 0.08` 扰动轮廓做"笔毛分叉"；
4. 高光：短促弧线 stroke（宽 2–5px，不透光白），**顺光方向排列成组**。

## 6. 水彩湿边（湿画法水彩）

```xml
<filter id="watercolor">
  <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="5" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="24" result="disp"/>
  <feGaussianBlur stdDeviation="1.2" result="blur"/>
  <feComponentTransfer in="blur" result="soft">
    <feFuncA type="table" tableValues="0 0 .3 .8 1"/>   <!-- 边缘沉积:两端高 -->
  </feComponentTransfer>
</filter>
```
配套纪律：颜色必须多层薄涂（同形状 fill 不透明度 15%×3 层叠出浓度），禁止一层实色。

## 7. 夜景辉光 / 霓虹

```xml
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="6" result="b1"/>
  <feGaussianBlur in="SourceGraphic" stdDeviation="18" result="b2"/>
  <feMerge>
    <feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```
纪律：光源本体颜色near-white（如 #FFF4D6），辉光层才是纯色相；一画面强光源 ≤3 处。

## 8. 边缘腐蚀/做旧（废土、古画残破）

```xml
<filter id="distress">
  <feTurbulence type="fractalNoise" baseFrequency="0.06 0.04" numOctaves="5" seed="99" result="n"/>
  <feColorMatrix in="n" type="luminanceToAlpha" result="a"/>
  <feComposite operator="out" in="SourceGraphic" in2="a"/>  <!-- 随机啃掉边缘 -->
</filter>
```

## 9. 混合模式速查（置于 `<g style="mix-blend-mode:...">`）

| 模式 | 典型用途 |
|------|----------|
| multiply | 阴影、墨线压色、玻璃投影 |
| screen | 光斑、雾气、星辉 |
| soft-light | 水面倒影、肤色过渡的柔化 |
| overlay | 提对比的氛围光 |
| color-dodge | 强烈体积光(Tyndall光柱) |

## 10. 路径书写规范（复杂画的代码可维护性）

- 每个大块 `<g>` 注释中文说明（<!-- 远山第二叠 -->）。
- 贝塞尔连续拐点用 S/T 命令保持曲率镜像，杜绝"尖端抖动"。
- 重复元素（窗格、瓦垄、栏杆）一律 `<defs>` 定义 + `<use x y transform>`，
  或干脆交给 Canvas 循环生成后叠加。
