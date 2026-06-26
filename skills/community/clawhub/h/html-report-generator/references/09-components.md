# 09 · 组件库

> 可复用的原子级 UI 组件。每个组件独立使用，按需组合。
> 覆盖：页眉变体 / 摘要栏 / 卡片变体 / 标签徽章 / 图标系统 / 数字排版规范

---

## 一、页眉（Header）组件库

> 页眉高度固定 72px，`.hd` 区。同一报告内所有页眉保持同一风格。

### HD1 · 标准双行型（最通用）

```html
<div class="hd" style="background:var(--bg);border-bottom:1px solid rgba(255,255,255,0.06);">
  <!-- 左侧：报告名 + 页面主题 -->
  <div style="display:flex;flex-direction:column;gap:4px;">
    <div style="font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:var(--dt);">
      REPORT NAME · 2025
    </div>
    <div style="font-size:17px;font-weight:700;color:var(--t);letter-spacing:-0.5px;">
      页面主题标题
    </div>
  </div>
  <!-- 右侧：标签 + 状态灯 + 页码 -->
  <div style="display:flex;align-items:center;gap:10px;">
    <span style="background:var(--pm);border:1px solid var(--bd);border-radius:3px;
                 padding:2px 8px;font-size:9px;font-weight:600;color:var(--p);letter-spacing:0.5px;">
      CATEGORY
    </span>
    <div style="width:5px;height:5px;border-radius:50%;background:var(--p);
                box-shadow:0 0 8px var(--p);"></div>
    <span style="font-size:11px;font-family:monospace;color:var(--dt);">01/10</span>
  </div>
</div>
```

### HD2 · 渐变色条型（T1 精品风）

```html
<div class="hd" style="background:var(--bg);position:relative;overflow:hidden;">
  <!-- 底部渐变细线 -->
  <div style="position:absolute;bottom:0;left:0;right:0;height:1px;
              background:linear-gradient(90deg,transparent,var(--p),transparent);"></div>
  <!-- 左侧装饰竖线 -->
  <div style="position:absolute;left:25px;top:16px;bottom:16px;width:2px;
              background:linear-gradient(180deg,transparent,var(--p),transparent);border-radius:1px;"></div>
  <div style="padding-left:14px;">
    <div style="font-size:9.5px;letter-spacing:3px;text-transform:uppercase;color:var(--p);opacity:0.7;">
      SECTION ·
    </div>
    <div style="font-size:18px;font-weight:800;letter-spacing:-1px;color:var(--t);margin-top:2px;">
      页面主题
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:8px;font-family:monospace;">
    <span style="font-size:9px;color:var(--dt);">PAGE</span>
    <span style="font-size:22px;font-weight:800;color:var(--p);letter-spacing:-1px;line-height:1;">01</span>
    <span style="font-size:9px;color:var(--dt);">/10</span>
  </div>
</div>
```

### HD3 · 极简单行型（T5 极简风）

```html
<div class="hd" style="background:#fafaf8;border-bottom:1px solid #e5e7eb;">
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="height:16px;width:3px;background:var(--p);border-radius:2px;"></div>
    <span style="font-size:13px;font-weight:700;color:#111827;letter-spacing:-0.3px;">页面主题标题</span>
    <span style="font-size:10px;color:#9ca3af;">/ 章节名称</span>
  </div>
  <div style="font-size:10px;color:#9ca3af;font-family:monospace;">01 · 10</div>
</div>
```

### HD4 · 终端路径型（T3 专用）

```html
<div class="hd" style="background:#161b22;border-bottom:1px solid #30363d;font-family:monospace;">
  <div style="display:flex;align-items:center;gap:8px;">
    <span style="color:#3fb950;">●</span>
    <span style="color:#8b949e;font-size:10px;">/report/</span>
    <span style="color:#58a6ff;font-size:10px;font-weight:700;">section-name</span>
    <span style="color:#8b949e;font-size:10px;">.md</span>
    <span style="background:rgba(88,166,255,0.1);border:1px solid rgba(88,166,255,0.2);
                 border-radius:3px;padding:1px 6px;font-size:8.5px;color:#58a6ff;">ACTIVE</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px;">
    <span style="font-size:9px;color:#484f58;">last updated</span>
    <span style="font-size:9px;color:#8b949e;font-family:monospace;">2025-03-12</span>
    <span style="font-size:10px;color:#484f58;">·</span>
    <span style="font-size:10px;color:#c9d1d9;font-family:monospace;">01/10</span>
  </div>
</div>
```

---

## 二、摘要栏（Summary Bar）组件库

> 摘要栏高度固定 48px，`.sm` 区。承载本页核心结论 1 句话 + 辅助信息。

### SM1 · 结论文字型（最通用）

```html
<div class="sm" style="background:rgba(0,0,0,0.3);border-top:1px solid rgba(255,255,255,0.05);">
  <!-- 左侧：核心结论 -->
  <div style="display:flex;align-items:center;gap:8px;flex:1;overflow:hidden;">
    <div style="width:3px;height:20px;background:var(--p);border-radius:2px;flex-shrink:0;"></div>
    <span style="font-size:11px;color:var(--mt);line-height:1.4;overflow:hidden;
                 display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">
      核心结论：用一句话概括本页最重要的发现，包含具体数字如 <b style="color:var(--t);">97%</b> 的攻击可通过X防御。
    </span>
  </div>
  <!-- 右侧：标签 -->
  <div style="display:flex;gap:5px;flex-shrink:0;">
    <span style="background:var(--pm);border:1px solid var(--bd);border-radius:2px;
                 padding:1px 6px;font-size:8.5px;color:var(--p);">标签A</span>
    <span style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);
                 border-radius:2px;padding:1px 6px;font-size:8.5px;color:#10b981;">标签B</span>
  </div>
</div>
```

### SM2 · 多指标横排型

```html
<div class="sm" style="background:rgba(0,0,0,0.25);border-top:1px solid rgba(255,255,255,0.05);">
  <!-- 3个关键指标横排 -->
  <div style="display:flex;align-items:center;gap:0;flex:1;">
    <div style="display:flex;flex-direction:column;padding-right:16px;border-right:1px solid rgba(255,255,255,0.06);">
      <span style="font-size:16px;font-weight:800;color:var(--p);letter-spacing:-0.5px;line-height:1;">97%</span>
      <span style="font-size:8px;color:var(--dt);margin-top:1px;">攻击成功率</span>
    </div>
    <div style="display:flex;flex-direction:column;padding:0 16px;border-right:1px solid rgba(255,255,255,0.06);">
      <span style="font-size:16px;font-weight:800;color:#10b981;letter-spacing:-0.5px;line-height:1;">+34%</span>
      <span style="font-size:8px;color:var(--dt);margin-top:1px;">防御提升</span>
    </div>
    <div style="display:flex;flex-direction:column;padding-left:16px;">
      <span style="font-size:16px;font-weight:800;color:#f59e0b;letter-spacing:-0.5px;line-height:1;">3种</span>
      <span style="font-size:8px;color:var(--dt);margin-top:1px;">主要攻击路径</span>
    </div>
  </div>
  <!-- 右侧进度条 -->
  <div style="display:flex;align-items:center;gap:6px;">
    <div style="width:90px;height:3px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;">
      <div style="width:10%;height:100%;background:var(--p);border-radius:2px;"></div>
    </div>
    <span style="font-size:9px;color:var(--dt);font-family:monospace;">01/10</span>
  </div>
</div>
```

---

## 三、卡片变体库

### 标准内容卡（基础，已在 03-layout 中定义）

### CARD-A · 全色强调卡

```html
<!-- 整个卡片背景是主色，用于强调最重要的一个维度 -->
<div style="background:var(--p);border-radius:8px;padding:10px 12px;
            display:flex;flex-direction:column;gap:4px;height:100%;overflow:hidden;">
  <div style="font-size:12px;font-weight:700;color:rgba(255,255,255,0.9);">卡片标题</div>
  <div style="font-size:11px;line-height:1.45;color:rgba(255,255,255,0.75);flex:1;overflow:hidden;">
    正文内容，这是强调版卡片，适合放核心结论或最重要的数字。
  </div>
  <div style="font-size:22px;font-weight:900;color:#fff;letter-spacing:-1px;line-height:1;">97%</div>
</div>
```

### CARD-B · 无边框透明卡（内容为王）

```html
<!-- 无背景色，仅靠内容撑起，左侧色条定位 -->
<div style="border-left:3px solid var(--p);padding:6px 0 6px 14px;
            display:flex;flex-direction:column;gap:4px;height:100%;overflow:hidden;">
  <div style="font-size:12px;font-weight:700;color:var(--t);">卡片标题</div>
  <div style="font-size:11px;line-height:1.45;color:var(--mt);flex:1;overflow:hidden;">
    正文内容，无底色卡片适合 T5 极简模板或 T2 分割模板的右栏。
  </div>
</div>
```

### CARD-C · 图标+数字+说明三件套

```html
<!-- 适合特性/优势的展示 -->
<div style="background:var(--card);border:1px solid var(--bd);border-radius:8px;
            padding:10px 12px;display:flex;flex-direction:column;gap:6px;height:100%;overflow:hidden;">
  <!-- 图标行 -->
  <div style="display:flex;align-items:center;gap:8px;">
    <!-- SVG 图标（16×16）-->
    <div style="width:28px;height:28px;border-radius:6px;background:var(--pm);
                border:1px solid var(--bd);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M7 1L9 5H13L10 8L11 12L7 10L3 12L4 8L1 5H5L7 1Z"
              fill="var(--p)" opacity="0.9"/>
      </svg>
    </div>
    <div style="font-size:12px;font-weight:700;color:var(--t);">特性名称</div>
  </div>
  <div style="font-size:26px;font-weight:900;color:var(--p);letter-spacing:-1px;line-height:1;">97%</div>
  <div style="font-size:10.5px;line-height:1.45;color:var(--mt);flex:1;overflow:hidden;">
    简短说明文字，描述这个数字的含义和背景。
  </div>
</div>
```

### CARD-D · 横向宽卡（跨列 Featured）

```html
<!-- 适合 grid-column:span 2 的横向大卡 -->
<div style="background:var(--card);border:1px solid var(--bd);border-radius:8px;
            padding:10px 16px;display:flex;gap:16px;align-items:center;overflow:hidden;">
  <!-- 左侧大数字 -->
  <div style="flex-shrink:0;text-align:center;width:80px;">
    <div style="font-size:44px;font-weight:900;color:var(--p);letter-spacing:-2px;line-height:1;">73</div>
    <div style="font-size:8.5px;color:var(--dt);margin-top:2px;text-transform:uppercase;letter-spacing:0.5px;">
      核心指标
    </div>
  </div>
  <!-- 分隔线 -->
  <div style="width:1px;height:60px;background:linear-gradient(180deg,transparent,var(--p),transparent);
              flex-shrink:0;opacity:0.4;"></div>
  <!-- 右侧内容 -->
  <div style="flex:1;overflow:hidden;">
    <div style="font-size:12.5px;font-weight:700;color:var(--t);margin-bottom:4px;">横向宽卡标题</div>
    <div style="font-size:11px;line-height:1.45;color:var(--mt);">
      横向宽卡适合需要左侧大数字 + 右侧详细说明的内容，或需要跨越两列突出显示的关键信息。
    </div>
  </div>
</div>
```

### CARD-E · 语义状态卡（危险/成功/警告/信息）

```html
<!-- 危险状态 -->
<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);
            border-left:3px solid #ef4444;border-radius:0 6px 6px 0;padding:8px 12px;overflow:hidden;">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
    <div style="width:6px;height:6px;border-radius:50%;background:#ef4444;flex-shrink:0;"></div>
    <span style="font-size:10px;font-weight:700;color:#ef4444;text-transform:uppercase;letter-spacing:0.5px;">
      HIGH RISK
    </span>
  </div>
  <div style="font-size:11px;line-height:1.45;color:#fca5a5;">内容说明</div>
</div>

<!-- 成功状态 -->
<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);
            border-left:3px solid #10b981;border-radius:0 6px 6px 0;padding:8px 12px;overflow:hidden;">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
    <div style="width:6px;height:6px;border-radius:50%;background:#10b981;flex-shrink:0;"></div>
    <span style="font-size:10px;font-weight:700;color:#10b981;text-transform:uppercase;letter-spacing:0.5px;">
      PROTECTED
    </span>
  </div>
  <div style="font-size:11px;line-height:1.45;color:#6ee7b7;">内容说明</div>
</div>
```

---

## 四、标签/徽章（Badge & Tag）系统

```html
<!-- 实色填充标签 -->
<span style="background:var(--p);color:#fff;padding:2px 7px;border-radius:2px;
             font-size:8.5px;font-weight:700;letter-spacing:0.3px;">PRIMARY</span>

<!-- 描边标签 -->
<span style="border:1px solid var(--p);color:var(--p);padding:2px 7px;border-radius:2px;
             font-size:8.5px;font-weight:600;">OUTLINE</span>

<!-- 圆角pill标签 -->
<span style="background:var(--pm);border:1px solid var(--bd);color:var(--p);
             padding:2px 8px;border-radius:10px;font-size:8.5px;font-weight:600;">PILL</span>

<!-- 状态徽章（含圆点） -->
<span style="display:inline-flex;align-items:center;gap:4px;background:rgba(16,185,129,0.1);
             border:1px solid rgba(16,185,129,0.25);border-radius:10px;
             padding:2px 8px;font-size:8.5px;color:#10b981;">
  <span style="width:5px;height:5px;border-radius:50%;background:#10b981;"></span>
  ACTIVE
</span>

<!-- 数字徽章 -->
<span style="background:var(--p);color:#fff;min-width:18px;height:18px;border-radius:9px;
             display:inline-flex;align-items:center;justify-content:center;
             font-size:9px;font-weight:700;padding:0 5px;">42</span>

<!-- Callout/引用框 -->
<div style="background:var(--pm);border-left:3px solid var(--p);border-radius:0 4px 4px 0;
            padding:6px 10px;font-size:10.5px;color:var(--mt);line-height:1.5;">
  💡 <strong style="color:var(--t);">关键洞察：</strong>这是一个重要的补充说明或引用内容。
</div>
```

---

## 六、数字排版规范

### 大数字单位格式

```
国内报告（中文）：
  < 1万      → 直接写数字：8,234
  1万~1亿    → 万为单位：2.3万 / 156万
  > 1亿      → 亿为单位：1.2亿 / 34.5亿

国际报告（英文混排）：
  < 1K       → 直接写：834
  1K~1M      → K单位：23.4K
  1M+        → M/B单位：1.2M / 3.4B

禁止：1,234,567（正文中太长）→ 改为 123.5万 / 1.2M
```

### 正负变化颜色规则

```html
<!-- 正增长 → 绿色 + 上箭头 -->
<span style="color:#10b981;font-weight:600;">↑ +34%</span>

<!-- 负变化 → 红色 + 下箭头 -->
<span style="color:#ef4444;font-weight:600;">↓ -12%</span>

<!-- 中性/持平 → 灰色 -->
<span style="color:#94a3b8;font-weight:600;">→ 0%</span>

<!-- 特例：风险报告中"下降是好事"时手动指定颜色 -->
<span style="color:#10b981;font-weight:600;">↓ -8% 漏洞减少</span>
```

### 中英文混排间距

```html
<!-- 正确：中文与英文/数字之间加细空格（&thinsp;）-->
<span>检测到 <b>97%</b>&thinsp;的&thinsp;AI&thinsp;生成内容</span>

<!-- 代码片段用等宽 + 主色 -->
<em style="font-family:monospace;color:var(--p);font-style:normal;">PGD-AT</em>

<!-- 百分比数字与单位不换行 -->
<span style="white-space:nowrap;"><b>97</b>%</span>
```

---

## 组件使用检查

```
□ 同一报告内页眉使用统一的 HD 变体（不混用HD1/HD2/HD3）？
□ 摘要栏包含本页核心结论（含具体数字），而非空白？
□ 全色强调卡(CARD-A)每页最多1个？
□ 语义状态卡的颜色与语义一致（危险=红，安全=绿，警告=橙）？
□ 大数字使用了正确的单位格式（万/亿 或 K/M/B）？
□ 正负变化使用了正确的颜色（正=绿，负=红）？
```
