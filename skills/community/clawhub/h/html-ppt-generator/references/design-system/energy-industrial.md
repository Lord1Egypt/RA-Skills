# 能源工业（Energy Industrial）

**气质：** 重工业感、石油天然气、工程精密严谨
**适用：** 能源报告、工程技术、产能分析、安全规范
**推荐字体：** FP-3（Space Mono + IBM Plex Sans）
**背景类型：** 暗色系（深煤灰黑）
**主标题字号：** 32–40px，粗黑体无衬线，工业感强
**页眉形式：** 左侧项目编号 + 文档标题，右侧版本/日期，等宽字体

---

## 设计特征

- **橙黄安全色**（#f59e0b / #ea580c）作为主强调色（工业警示感）
- 深煤灰黑背景，模拟炼厂/矿区夜间感
- 卡片带橙色左侧色条（危险等级标注）
- 数据密集，使用 Space Mono 等宽字体展示参数
- 横向进度条模拟仪表盘读数风格

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #0c0d0b; font-family: 'IBM Plex Sans','PingFang SC',sans-serif; color: #d4d0c8; }

/* 工业纹理（斜条纹） */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image: repeating-linear-gradient(
    -45deg,
    rgba(245,158,11,0.015) 0px, rgba(245,158,11,0.015) 1px,
    transparent 1px, transparent 24px
  );
}

/* 展示标题（粗大无衬线） */
.display-title {
  font-family: 'Space Mono','PingFang SC',monospace;
  font-size: 34px; font-weight: 700;
  letter-spacing: -0.5px; line-height: 1.05;
  color: #f59e0b;
  text-shadow: 0 0 30px rgba(245,158,11,0.25);
}

/* 卡片（带橙色左侧色条） */
.card {
  background: rgba(18,20,15,0.9);
  border: 1px solid rgba(245,158,11,0.12);
  border-left: 3px solid #f59e0b;
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* 仪表盘风格进度条 */
.gauge-row {
  display:flex; align-items:center; gap:8px; font-size:9.5px; font-family:monospace;
}
.gauge-bar {
  flex:1; height:6px; background:rgba(245,158,11,0.1);
  border-radius:0; border:1px solid rgba(245,158,11,0.2);
}
.gauge-fill { height:100%; background: linear-gradient(90deg, #ea580c, #f59e0b); }

/* KPI 数字（等宽） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 38px; font-weight: 700; line-height: 1; letter-spacing: -1px;
  color: #f59e0b;
}

/* 警告标签 */
.alert-tag {
  display:inline-flex; align-items:center; gap:4px;
  background:rgba(234,88,12,0.15); border:1px solid rgba(234,88,12,0.35);
  border-radius:2px; padding:2px 6px; font-size:8.5px; font-weight:700;
  color:#ea580c; font-family:monospace; letter-spacing:0.5px;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #0c0d0b;
  --card: #12140f;
  --p:    #f59e0b;
  --pm:   rgba(245,158,11,0.12);
  --bd:   rgba(245,158,11,0.18);
  --t:    #d4d0c8;
  --mt:   #a09a8e;
  --dt:   #6b6558;
}
```
