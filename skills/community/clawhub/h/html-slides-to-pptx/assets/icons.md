# 图标库(icons · 40 枚内联 SVG,线性几何风)

> **用法**:整行复制进页面 → 改两处:`width/height`(尺寸)与 `style="stroke:var(--…)"` 的**变量名**(颜色)。
> 图标是**结构件**(承载语义),不计装饰预算;但**无语义不摆图标**。

## 铁律(2026-08-05 B0 实测)

1. **禁 `currentColor`**(stroke/fill 都是)——转换截图前页面文字会被 `*{color:transparent}` 隐藏,currentColor 随之变透明 → 图标在 PPTX 里空白(浏览器预览正常,极隐蔽)。validate 已配静态 WARN。
2. **颜色写成 CSS 属性形态的变量**:`style="stroke:var(--brand-primary)"`(本库 44 处已全部改成此形态,
   2026-08-17 第九轮)。CSS 属性写法不受 color 隐藏影响 —— 实测同一图标在 `capture.hideTextCss` 下
   与裸 hex 截图**逐字节相同**,而 currentColor 变空白。写属性形态 `stroke="#hex"` 虽然也能渲染,
   但换色板时不跟随,且会被 validate R1 判为色板外用色。
3. **全页图标同一色系**(主色 `var(--brand-primary)` 或炭灰 `var(--ink-soft)`);深底卡上换亮色(`var(--on-navy-text)`)。
4. 实心小点/小三角用 `style="fill:var(--同色)"`(每枚代码里已写好,改色时 stroke/fill 两处都改)。
5. 尺寸惯例:网格卡 44-48px / 色带 44px / 特征行 20-22px / 节点 36px;每页 ≤8 枚。

技术说明:内联 `<svg>` 由转换器整体截图为 2x PNG 原位贴回(同页文字仍原生可编辑);
`<use href="外部.svg">` 外链在 file:// 下不渲染(B0.3 已否),**必须整段内联**。

## 语义速查

| 想表达 | 用 | 想表达 | 用 |
|---|---|---|---|
| 目标/聚焦/定位 | i-target / i-compass | 增长/趋势 | i-growth |
| 里程碑/上市 | i-flag / i-rocket | 方向/下一步 | i-arrow |
| 数据/指标 | i-chart-bar / i-database | 分层/集成 | i-layers |
| 循环/迭代 | i-refresh | 用户/客户 | i-person |
| 团队/生态 | i-people | 沟通/反馈 | i-chat |
| 设置/机制 | i-gear / i-sliders | 搜索/发现 | i-search |
| 关键/密钥 | i-key | 连接/集成 | i-link |
| 想法/创新 | i-bulb | 亮点/优势 | i-star |
| 速度/能量 | i-bolt | 洞察/可见 | i-eye |
| 安全/合规 | i-shield / i-lock | 完成/达成 | i-check |
| 风险/排除 | i-warning / i-x | 时间/周期 | i-clock |
| 计划/日程 | i-calendar | 收藏/保留 | i-bookmark |
| 成本/支付 | i-wallet | 文档/报告 | i-doc |
| 邮件/触达 | i-mail | 电话/联络 | i-phone |
| 首页/门户 | i-home | 全球化 | i-globe |
| 福利/权益 | i-gift / i-heart | 播放/演示 | i-play |
| 云/基建 | i-cloud | 发布/加速 | i-rocket |

---

## 方向与目标

**i-target** · 目标/聚焦/定位
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" style="fill:var(--brand-primary)" stroke="none"/></svg>
```

**i-growth** · 增长/趋势向上
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 17 9 11 13 15 21 7"/><polyline points="15 7 21 7 21 13"/></svg>
```

**i-flag** · 里程碑/目标达成
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="21"/><path d="M6 4 H18 L15 8 L18 12 H6"/></svg>
```

**i-compass** · 方向/战略
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polygon points="15.5 8.5 13.5 13.5 8.5 15.5 10.5 10.5"/></svg>
```

**i-arrow** · 方向/推进
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="12" x2="20" y2="12"/><polyline points="14 6 20 12 14 18"/></svg>
```

## 数据与系统

**i-chart-bar** · 数据/指标
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 4 4 20 20 20"/><line x1="8" y1="20" x2="8" y2="13" stroke-width="3"/><line x1="12" y1="20" x2="12" y2="9" stroke-width="3"/><line x1="16" y1="20" x2="16" y2="15" stroke-width="3"/></svg>
```

**i-database** · 数据库/数据资产
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6 V18 C5 19.66 8.13 21 12 21 C15.87 21 19 19.66 19 18 V6"/><path d="M5 12 C5 13.66 8.13 15 12 15 C15.87 15 19 13.66 19 12"/></svg>
```

**i-layers** · 分层/集成
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 3 21 8 12 13 3 8"/><polyline points="3 12.5 12 17.5 21 12.5"/><polyline points="3 17 12 22 21 17"/></svg>
```

**i-refresh** · 循环/迭代
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12 a9 9 0 1 1 -9 -9 c2.52 0 4.93 1 6.74 2.74 L21 8"/><polyline points="21 3 21 8 16 8"/></svg>
```

**i-cloud** · 云/基础设施
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19 H9 a7 7 0 1 1 6.71 -9 h1.79 a4.5 4.5 0 1 1 0 9 Z"/></svg>
```

## 人与组织

**i-person** · 用户/客户
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.5"/><path d="M5 20 C5 15.5 8 13.5 12 13.5 C16 13.5 19 15.5 19 20"/></svg>
```

**i-people** · 团队/生态
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8.5" r="3"/><path d="M3.5 19.5 C3.5 15.8 6 14 9 14 C12 14 14.5 15.8 14.5 19.5"/><circle cx="16.8" cy="9.5" r="2.4"/><path d="M15.8 14.2 C18.4 13.8 20.8 15.5 20.8 19"/></svg>
```

**i-chat** · 沟通/反馈
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5 a8.38 8.38 0 0 1 -0.9 3.8 8.5 8.5 0 0 1 -7.6 4.7 8.38 8.38 0 0 1 -3.8 -0.9 L3 21 l1.9 -5.7 a8.38 8.38 0 0 1 -0.9 -3.8 8.5 8.5 0 0 1 4.7 -7.6 8.38 8.38 0 0 1 3.8 -0.9 h0.5 a8.48 8.48 0 0 1 8 8 v0.5 Z"/></svg>
```

## 工具与机制

**i-gear** · 设置/机制/引擎
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3.2"/><line x1="18.2" y1="12" x2="21" y2="12"/><line x1="16.38" y1="16.38" x2="18.36" y2="18.36"/><line x1="12" y1="18.2" x2="12" y2="21"/><line x1="7.62" y1="16.38" x2="5.64" y2="18.36"/><line x1="5.8" y1="12" x2="3" y2="12"/><line x1="7.62" y1="7.62" x2="5.64" y2="5.64"/><line x1="12" y1="5.8" x2="12" y2="3"/><line x1="16.38" y1="7.62" x2="18.36" y2="5.64"/></svg>
```

**i-sliders** · 调控/配置
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="7" x2="19" y2="7"/><line x1="5" y1="12" x2="19" y2="12"/><line x1="5" y1="17" x2="19" y2="17"/><circle cx="9" cy="7" r="2"/><circle cx="15" cy="12" r="2"/><circle cx="8" cy="17" r="2"/></svg>
```

**i-search** · 搜索/发现
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6.5"/><line x1="16" y1="16" x2="21" y2="21"/></svg>
```

**i-key** · 关键/密钥/破局点
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="4.5"/><line x1="10.7" y1="12.3" x2="20" y2="3"/><line x1="15" y1="8" x2="18" y2="11"/><line x1="17.5" y1="5.5" x2="20" y2="8"/></svg>
```

**i-link** · 连接/打通
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13 a5 5 0 0 0 7.54 0.54 l3 -3 a5 5 0 0 0 -7.07 -7.07 l-1.72 1.71"/><path d="M14 11 a5 5 0 0 0 -7.54 -0.54 l-3 3 a5 5 0 0 0 7.07 7.07 l1.71 -1.71"/></svg>
```

## 想法与亮点

**i-bulb** · 想法/创新
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14 c0.2 -1 0.7 -1.7 1.4 -2.4 C17.4 10.1 18 8.6 18 7 A6 6 0 1 0 6 7 c0 1.6 0.6 3.1 1.6 4.6 C8.3 12.3 8.8 13 9 14"/><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="21" x2="14" y2="21"/></svg>
```

**i-star** · 亮点/优势/评分
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 L14.7 8.6 L20.9 9.4 L16.4 13.7 L17.5 19.8 L12 16.9 L6.5 19.8 L7.6 13.7 L3.1 9.4 L9.3 8.6 Z"/></svg>
```

**i-bolt** · 速度/能量
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 L4 14 H11 L10 22 L20 9 H13 Z"/></svg>
```

**i-eye** · 洞察/可见性
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 12 C5 7.5 8.5 5 12 5 C15.5 5 19 7.5 21.5 12 C19 16.5 15.5 19 12 19 C8.5 19 5 16.5 2.5 12 Z"/><circle cx="12" cy="12" r="2.8"/></svg>
```

**i-rocket** · 发布/加速/增长
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5 c-1.5 1.26 -2 5 -2 5 s3.74 -0.5 5 -2 c0.71 -0.84 0.7 -2.13 -0.09 -2.91 a2.18 2.18 0 0 0 -2.91 -0.09 Z"/><path d="M12 15 l-3 -3 a22 22 0 0 1 2 -3.95 A12.88 12.88 0 0 1 22 2 c0 2.72 -0.78 7.5 -6 11 a22.35 22.35 0 0 1 -4 2 Z"/><path d="M9 12 H4 s0.55 -3.03 2 -4 c1.62 -1.08 5 0 5 0"/><path d="M12 15 v5 s3.03 0.55 4 2 c1.08 1.62 0 5 0 5"/></svg>
```

## 安全与状态

**i-shield** · 安全/合规/保障
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 L19 6 V11 C19 15.5 15.7 18.8 12 20 C8.3 18.8 5 15.5 5 11 V6 Z"/><polyline points="9 11.5 11.2 13.7 15.5 9.4"/></svg>
```

**i-lock** · 安全/权限
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="11" width="12" height="9" rx="2"/><path d="M9 11 V8 a3 3 0 0 1 6 0 v3"/></svg>
```

**i-check** · 完成/达成/通过
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16.5 9"/></svg>
```

**i-x** · 排除/错误/不做
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="9" y1="9" x2="15" y2="15"/><line x1="15" y1="9" x2="9" y2="15"/></svg>
```

**i-warning** · 风险/注意
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 4.1 L2.9 17.5 A2 2 0 0 0 4.6 20.5 H19.4 A2 2 0 0 0 21.1 17.5 L13.7 4.1 A2 2 0 0 0 10.3 4.1 Z"/><line x1="12" y1="9.5" x2="12" y2="14"/><circle cx="12" cy="17" r="1" style="fill:var(--brand-primary)" stroke="none"/></svg>
```

## 时间与计划

**i-clock** · 时间/时效
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/></svg>
```

**i-calendar** · 计划/日程
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="16" rx="2"/><line x1="4" y1="10" x2="20" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/></svg>
```

**i-bookmark** · 收藏/保留/重点
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3 H17 V21 L12 16.5 L7 21 Z"/></svg>
```

## 业务与资产

**i-wallet** · 成本/支付/预算
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="13" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><circle cx="16.5" cy="14.5" r="1.2" style="fill:var(--brand-primary)" stroke="none"/></svg>
```

**i-doc** · 文档/报告
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3 H14 L18 7 V21 H7 Z"/><polyline points="14 3 14 7 18 7"/><line x1="9.5" y1="13" x2="14.5" y2="13"/><line x1="9.5" y1="16.5" x2="14.5" y2="16.5"/></svg>
```

**i-mail** · 邮件/触达
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3.5 7 12 13 20.5 7"/></svg>
```

**i-phone** · 电话/联络
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92 v3 a2 2 0 0 1 -2.18 2 19.79 19.79 0 0 1 -8.63 -3.07 19.5 19.5 0 0 1 -6 -6 19.79 19.79 0 0 1 -3.07 -8.67 A2 2 0 0 1 4.11 2 h3 a2 2 0 0 1 2 1.72 c0.13 0.96 0.36 1.9 0.7 2.81 a2 2 0 0 1 -0.45 2.11 L8.09 9.91 a16 16 0 0 0 6 6 l1.27 -1.27 a2 2 0 0 1 2.11 -0.45 c0.91 0.34 1.85 0.57 2.81 0.7 A2 2 0 0 1 22 16.92 Z"/></svg>
```

**i-home** · 首页/门户/总部
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11 L12 3 L21 11"/><path d="M6 9.5 V21 H18 V9.5"/><polyline points="10 21 10 15 14 15 14 21"/></svg>
```

**i-globe** · 全球化/市场
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><line x1="3" y1="12" x2="21" y2="12"/></svg>
```

**i-gift** · 福利/权益
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8 v13"/><path d="M19 12 v7 a2 2 0 0 1 -2 2 H7 a2 2 0 0 1 -2 -2 v-7"/><path d="M7.5 8 a2.5 2.5 0 0 1 0 -5 C11 3 12 8 12 8"/><path d="M16.5 8 a2.5 2.5 0 0 0 0 -5 C13 3 12 8 12 8"/></svg>
```

**i-heart** · 喜爱/口碑
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20.5 C6 16 3 12.8 3 9.3 C3 6.4 5.2 4.5 7.7 4.5 C9.5 4.5 11.1 5.5 12 7 C12.9 5.5 14.5 4.5 16.3 4.5 C18.8 4.5 21 6.4 21 9.3 C21 12.8 18 16 12 20.5 Z"/></svg>
```

**i-play** · 播放/演示
```html
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polygon points="10 8.5 16.5 12 10 15.5" style="fill:var(--brand-primary)" stroke="none"/></svg>
```

---

## 组合惯例

- **图标+标题同行**:`<div style="display:flex;align-items:center;gap:20px;">svg + 标题div</div>`(原型 23/30 骨架自带)
- **特征行小图标**(20-22px):`display:flex;align-items:center;gap:14px;`(原型 29 骨架自带)
- **改色**:改该 svg 行内的 `style="stroke:var(--brand-primary)"` → 目标**变量名**
  (炭灰用 `var(--ink-soft)`、强调用 `var(--accent-orange)`);深底卡上用 `var(--on-navy-text)`。
  **不要改回 hex** —— 换色板时变量自动跟随,hex 不会(validate R1 会报色板外用色)
- **改尺寸**:等比改 `width/height`(viewBox 不动);常用 20/36/44/48
