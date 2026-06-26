# PPTX 技法牌组（T1-T10）

> 每页抽 2-3 张，相邻页组合必须不同。每张牌给出原子级 CSS 原理（5-8 行），不是模板 -- 必须按 ADAPT 轴变异参数，保证同一技法的两次使用也绝不雷同。

---

## T1. 破界水印 -- 巨型透明文字/数字贯穿画面边缘

```html
<div style="position:absolute; bottom:-20px; left:-40px;
    font-size:280px; font-weight:900; color:var(--accent-1);
    opacity:0.04; white-space:nowrap; pointer-events:none;
    overflow:hidden;">GROWTH</div>
```
**ADAPT**：尺寸 180-400px / 位置四角任选 / 内容（英文大写/中文单字/纯数字/年份） / opacity 0.03-0.06 / 被卡片半遮挡还是完全穿透

---

## T2. 极致字号共生 -- 120px+ 数字紧贴 13px 注解，近零间距

```html
<div style="display:flex; align-items:baseline; gap:4px;">
  <span style="font-size:120px; font-weight:900;
      color:var(--accent-1); line-height:0.85;">47.3</span>
  <div>
    <span style="font-size:13px; color:var(--text-secondary);">%</span>
    <div style="font-size:11px; color:var(--text-secondary);
        opacity:0.6;">同比增长</div>
  </div>
</div>
```
**ADAPT**：数字大小 80-160px / gap 0-8px / 注解位置（右侧baseline/正下方/左侧） / 单位拆分方式

---

## T3. Z轴叠压 -- 卡片用负 margin 侵入相邻区域

```html
<div style="...card-A...">...</div>
<div style="margin-top:-24px; position:relative; z-index:2;
    ...card-B...">...</div>
```
**ADAPT**：侵入量 -16px 到 -40px / 方向（上侵/左侵/右侵） / 谁在上层 / 被侵入方加微妙阴影制造景深
> **与画布安全共存**：负 margin 侵入的是卡片之间的 gap 空间，不破坏任何卡片自身的 overflow:hidden。侵入方和被侵入方各自保持 overflow:hidden。

---

## T4. 浮岛面板 -- 多层阴影制造物理凸起

```html
<div style="background:var(--card-bg-from); border-radius:var(--card-radius);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05),
                0 12px 24px rgba(0,0,0,0.1),
                0 24px 48px rgba(0,0,0,0.08);
    transform:translateY(-4px);">...</div>
```
**ADAPT**：阴影层数 2-4 / 偏移方向和距离 / transform 偏移 -2px 到 -8px / 浅色系强化阴影，深色系弱化

---

## T5. 斜切色带 -- 对角线 accent 条贯穿画面

```html
<div style="position:absolute; left:0; right:0; height:3px;
    background:linear-gradient(90deg, transparent 5%,
        var(--accent-1) 20%, var(--accent-2) 80%, transparent 95%);
    transform:rotate(-2deg); transform-origin:left center;"></div>
```
**ADAPT**：角度 -1deg 到 -4deg / 高度 2-6px / 页面上的 Y 位置 / 渐变色组合 / 单条或平行双条

---

## T6. 底纹穿透 -- 装饰形状被内容卡片半遮挡

```html
<div style="position:absolute; right:-60px; top:120px;
    width:200px; height:200px; border-radius:50%;
    background:var(--accent-1); opacity:0.06;"></div>
```
**ADAPT**：形状（圆/矩形/菱形用内联SVG） / 大小 100-400px / 四角或边缘 / opacity 0.03-0.08 / 被哪些卡片遮挡

---

## T7. 留白压迫 -- 60%+ 面积为空，孤立焦点元素

```html
<div style="display:flex; align-items:center; justify-content:flex-start;
    height:100%; padding:60px 80px;">
  <span style="font-size:42px; font-weight:700;
      color:var(--accent-1); max-width:60%;">
    核心论断只有一句话</span>
</div>
```
**ADAPT**：留白比 50-80% / 焦点位置（居中/偏左偏下/右上角） / 内容类型（金句/单一数字/关键词）

---

## T8. 非对称重力 -- 一侧浓墨重彩，另侧极度克制

```html
<!-- 左侧：重力深渊 -->
<div style="grid-column:1; background:var(--accent-1); opacity:0.08;
    display:flex; align-items:center; justify-content:center;">
  <span style="font-size:96px; font-weight:900;
      color:var(--text-primary);">2847</span>
</div>
<!-- 右侧：轻盈留白 -->
<div style="grid-column:2; padding:40px;">
  <p style="font-size:13px; color:var(--text-secondary);">
    解释性文字悬浮在大面积留白中...</p>
</div>
```
**ADAPT**：重/轻哪侧 / 重力元素类型（大数字/配图/深色块） / 轻侧内容密度 / 宽度比例（7:3 / 6:4 / 8:2）

---

## T9. 脉冲锚点 -- accent 色圆点标记关键位置

```html
<div style="position:relative; display:inline-flex; align-items:center; justify-content:center;
    width:16px; height:16px;">
  <!-- 外圈光晕（自动居中） -->
  <div style="position:absolute; inset:0; border-radius:50%;
      background:var(--accent-1); opacity:0.15;"></div>
  <!-- 内圈实心 -->
  <div style="width:8px; height:8px; border-radius:50%;
      background:var(--accent-1); position:relative; z-index:1;"></div>
</div>
```
**ADAPT**：内圈 6-10px 外圈 14-20px / 位置（时间线节点/卡片角标/标题旁） / 颜色用 accent-1 到 accent-4 轮换 / 外圈也可改为 `border: 1px solid` 实现空心环效果

> **居中原则**：外圈用 `position:absolute; inset:0` 自动撑满父容器居中，不要用手动 `top/left` 负偏移（计算错误会导致偏心）。父容器用 `inline-flex + align-items:center + justify-content:center` 确保内圈也居中。

---

## T10. 数据可视化铺底 -- 图表充满卡片作为底纹，数字浮于其上

```html
<div style="position:relative; overflow:hidden;">
  <!-- 图表占满整个卡片作为视觉底纹 -->
  <svg style="position:absolute; inset:0; width:100%; height:100%;
      opacity:0.15;">...sparkline/bar chart...</svg>
  <!-- 核心数字浮在图表上方 -->
  <div style="position:relative; z-index:1; padding:24px;">
    <span style="font-size:48px; font-weight:800;
        color:var(--accent-1);">89.7%</span>
  </div>
</div>
```
**ADAPT**：底纹图表类型（折线/柱状/环形） / 底纹 opacity 0.08-0.20 / 浮层内容（数字/标题/金句） / 底纹是否裁切出血
