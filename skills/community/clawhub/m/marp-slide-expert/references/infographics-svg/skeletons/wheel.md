# wheel — 平衡轮（玫瑰图式自评）

> 一个对象、6–10 个方面、统一 1–10 刻度。每个维度一根**花瓣**——扇形填充，半径 = 分值；短的那几瓣就是短板。教练 / 复盘语境的标准工具（生命平衡轮、团队健康度轮、业务成熟度轮）。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 单对象全域自评：个人生活平衡、团队健康度、业务板块成熟度 | 多对象对比（那是 [radar](radar.md) 雷达图） |
| 现状 vs 目标——花瓣与目标弧的缺口就是改进优先级 | 各维度量纲不同（先归一化到同一把尺） |
| 要对话「选 2–3 个短板去改进」的场景 | 只想要一个平均分（那用大字报数字） |

**和 [radar 雷达图](radar.md) 的分工——连形状都要能一眼分开**：雷达图是**折线多边形**，叠比 2–3 个对象；平衡轮是**扇形花瓣**（玫瑰图 / 南丁格尔玫瑰），只画一个对象。看到实心花瓣 = 平衡轮；看到多边形轮廓 = 雷达图。**不要**把平衡轮画成雷达那样的折线轮廓——那是两张不同的图。

## 变体：平衡轮 Balance Wheel

### 坐标公式（N 扇区玫瑰图）

```
圆心 cx, cy = 510, 255        满分半径 R = 195（对应 10 分）
扇区数 N = 6–10（8 最常用）    每扇区张角 360/N；每侧留 1° 缝，花瓣之间不相粘
扇区中心角 c_i = -90° + i×(360/N)                从正上方开始，顺时针
半径映射   r(v) = R × v / 10                     所有扇区同一把尺
花瓣路径   M cx,cy
           L (cx + r·cos(c−21.5°), cy + r·sin(c−21.5°))
           A r,r 0 0 1 (cx + r·cos(c+21.5°), cy + r·sin(c+21.5°)) Z
目标弧     同一扇区起止角上、半径 r(目标) 的虚线段（A 命令，sweep 1）
刻度环     2/4/6/8 分 → r = 39 / 78 / 117 / 156（浅灰虚线）
名字锚点   (cx + (R+30)·cos c, cy + (R+30)·sin c)
分值标签   (cx + (r−16)·cos c, cy + (r−16)·sin c)，白色嵌在花瓣尖内侧
```

8 扇区的中心角与名字锚点（R=195，圆心 510,255）：

| 扇区 | 中心角 | 名字锚点 | 锚点对齐 |
|---|---|---|---|
| 0 事业 | -90° | 510,30 | middle |
| 1 财富 | -45° | 669.1,95.9 | start |
| 2 健康 | 0° | 735,255 | start |
| 3 家庭 | 45° | 669.1,414.1 | start |
| 4 成长 | 90° | 510,480 | middle |
| 5 社交 | 135° | 350.9,414.1 | end |
| 6 休闲 | 180° | 285,255 | end |
| 7 贡献 | 225° | 350.9,95.9 | end |

```html
<svg viewBox="0 0 1020 510" width="100%">
<circle cx="510" cy="255" r="39" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="78" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="117" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="156" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="195" fill="none" stroke="#b9c3cc" stroke-width="1.5"/>
<path d="M438.5,73.6 A195,195 0 0 1 581.5,73.6" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M572.2,111.9 A156,156 0 0 1 653.1,192.8" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M655.1,197.8 A156,156 0 0 1 655.1,312.2" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M670.9,325 A175.5,175.5 0 0 1 580,415.9" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M567.2,400.1 A156,156 0 0 1 452.8,400.1" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M447.8,398.1 A156,156 0 0 1 366.9,317.2" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M346.7,319.3 A175.5,175.5 0 0 1 346.7,190.7" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M366.9,192.8 A156,156 0 0 1 447.8,111.9" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M510,255 L452.8,109.9 A156,156 0 0 1 567.2,109.9 Z" fill="#5d7d95"/>
<path d="M510,255 L556.7,147.7 A117,117 0 0 1 617.3,208.3 Z" fill="#5d7d95"/>
<path d="M510,255 L600.7,219.3 A97.5,97.5 0 0 1 600.7,290.7 Z" fill="#c0392b"/>
<path d="M510,255 L635.2,309.4 A136.5,136.5 0 0 1 564.4,380.2 Z" fill="#5d7d95"/>
<path d="M510,255 L538.6,327.6 A78,78 0 0 1 481.4,327.6 Z" fill="#c0392b"/>
<path d="M510,255 L463.3,362.3 A117,117 0 0 1 402.7,301.7 Z" fill="#5d7d95"/>
<path d="M510,255 L383,305 A136.5,136.5 0 0 1 383,205 Z" fill="#5d7d95"/>
<path d="M510,255 L420.6,216.1 A97.5,97.5 0 0 1 471.1,165.6 Z" fill="#5d7d95"/>
<text x="510" y="120" class="sm" fill="#ffffff" text-anchor="middle">8</text>
<text x="581.4" y="188.6" class="sm" fill="#ffffff" text-anchor="middle">6</text>
<text x="591.5" y="260" class="sm" fill="#ffffff" text-anchor="middle">5</text>
<text x="595.2" y="345.2" class="sm" fill="#ffffff" text-anchor="middle">7</text>
<text x="510" y="322" class="sm" fill="#ffffff" text-anchor="middle">4</text>
<text x="438.6" y="331.4" class="sm" fill="#ffffff" text-anchor="middle">6</text>
<text x="389.5" y="260" class="sm" fill="#ffffff" text-anchor="middle">7</text>
<text x="452.4" y="202.4" class="sm" fill="#ffffff" text-anchor="middle">5</text>
<text x="510" y="30" class="tb" fill="#1a1a2e" text-anchor="middle">事业</text>
<text x="669.1" y="95.9" class="tb" fill="#1a1a2e">财富</text>
<text x="735" y="255" class="tb" fill="#1a1a2e">健康</text>
<text x="669.1" y="414.1" class="tb" fill="#1a1a2e">家庭</text>
<text x="510" y="480" class="tb" fill="#1a1a2e" text-anchor="middle">成长</text>
<text x="350.9" y="414.1" class="tb" fill="#1a1a2e" text-anchor="end">社交</text>
<text x="285" y="255" class="tb" fill="#1a1a2e" text-anchor="end">休闲</text>
<text x="350.9" y="95.9" class="tb" fill="#1a1a2e" text-anchor="end">贡献</text>
<rect x="60" y="40" width="14" height="14" fill="#5d7d95"/>
<text x="82" y="52" class="sm" fill="#1a1a2e">维度得分（半径 = 分值）</text>
<rect x="60" y="66" width="14" height="14" fill="#c0392b"/>
<text x="82" y="78" class="sm" fill="#1a1a2e">短板（优先改进）</text>
<line x1="60" y1="99" x2="92" y2="99" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<text x="100" y="104" class="sm" fill="#1a1a2e">目标</text>
<text x="510" y="500" class="lbl" text-anchor="middle">1–10 分制 · 半径 = 分值 · 扇区宽度不代表权重 · 数据为示意</text>
</svg>
```

## 硬规则

1. **扇区数 6–10（8 最常用），宽度均分。** 扇区只编码「有几个方面」——宽度不代表权重，权重全在半径上。
2. **半径 = R × 分值 / 满分，不许手调。** 统一刻度写进注脚。
3. **花瓣之间留缝**（每侧约 1°）。不留缝，八瓣糊成一朵红花，读者数不出边界。
4. **短板染强调色**（最低的 1–2 项），其余同色——一色族 + 一个强调色；这张图的行动项就是那几瓣短的。
5. **现状 = 实心花瓣，目标 = 同扇区虚线弧。** 目标弧短于花瓣说明超额完成——照画，别删。
6. **分值标在花瓣内（白色），名字放环外。** 花瓣太短放不下数字时，把数字挪到名字后面（「成长 4」）。
7. **不要画成雷达。** 花瓣是扇形填充、单对象；雷达是折线轮廓、多对象叠比。混画两张图都废。

## 变体

| 变体 | 改法 | 用在 |
|---|---|---|
| 单花瓣 | 只画现状花瓣 + 分值，删目标弧 | 纯现状盘点 |
| 现状 + 目标 | 本模板（花瓣 + 虚线弧） | 改进对话（默认） |
| 双层花瓣 | 里层现状实色 + 外层目标浅色，花瓣套花瓣 | 想强调「要长多少」时——比虚线弧直白，但更占地方 |

## 文字排布

- 名字：`.tb` 深色 `#1a1a2e`，锚点按角度选 `start` / `end` / `middle`，沿辐射方向放环外
- 分值：`.sm` 反白，嵌在花瓣尖内侧（`r − 16` 处）
- 图例：左上角三行（得分色块 / 短板色块 / 目标虚线），`.sm`
- 注脚：`.lbl` 居中——「分制 + 半径含义 + 扇区宽度不代表权重」
