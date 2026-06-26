# 恐怖惊悚（Horror Dark）

**气质：** 惊悚氛围、都市传说、Creepypasta、诡异数据
**适用：** 网络安全事件报告、异常数据分析、黑暗主题创意、游戏恐怖内容
**推荐字体：** 衬线+等宽混用（Playfair Display + Space Mono）
**背景类型：** 极暗色系（深渊黑 #030303），血痕红光晕
**主标题字号：** 36–50px，斜体衬线，字体微颤感（letter-spacing 不规则）
**页眉形式：** 左侧倒计时或警告代码，右侧"██/██/████ 23:47"，红色光晕

---

## 设计特征

- **血腥红**（#8b0000 / #dc2626）+ **腐败绿**（#1a4a1a / #22c55e暗版）双主色
- 深渊黑背景，红色径向光晕从中心渗出
- 文字带微弱阴影模拟纸张霉斑老化
- 卡片边框用虚线（破损羊皮纸感）
- 警告符号、倒置十字、感叹号等惊悚装饰

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,700;1,900&family=Space+Mono:wght@400;700&display=swap');

body { background: #030303; font-family: 'Space Mono',monospace; color: #c8b8a8; }

/* 深渊血光 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 60%, rgba(139,0,0,0.12) 0%, transparent 60%),
    radial-gradient(ellipse at 30% 80%, rgba(80,0,0,0.08) 0%, transparent 40%);
}

/* 霉斑噪点 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:0.4;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='turbulence' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.12'/%3E%3C/svg%3E");
}

/* 展示标题（诡异斜体衬线） */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 44px; font-weight: 900; font-style: italic;
  letter-spacing: 1px; line-height: 1.05;
  color: #c8b8a8;
  text-shadow:
    0 0 30px rgba(139,0,0,0.4),
    2px 2px 8px rgba(0,0,0,0.8);
}
.display-title .blood { color: #8b0000; }

/* 警告标注 */
.warning-header {
  font-family: 'Space Mono',monospace;
  font-size: 9px; letter-spacing: 3px; text-transform: uppercase;
  color: rgba(139,0,0,0.8);
  border: 1px solid rgba(139,0,0,0.3); padding: 2px 8px; display: inline-block;
}
.warning-header::before { content: '⚠ '; }

/* 卡片（破损羊皮纸感） */
.card {
  background: rgba(10,5,5,0.95);
  border: 1px dashed rgba(139,0,0,0.25);
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 0 20px rgba(139,0,0,0.06), inset 0 0 30px rgba(0,0,0,0.5);
}

/* KPI（血红数字） */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 48px; font-weight: 900; font-style: italic; line-height: 1;
  color: #8b0000;
  text-shadow: 0 0 20px rgba(139,0,0,0.5), 0 2px 4px rgba(0,0,0,0.8);
}

/* 异常数据行（红色标注） */
.anomaly-row {
  display: flex; gap: 8px; padding: 3px 0; font-size: 9.5px;
  border-bottom: 1px solid rgba(139,0,0,0.08);
  font-family: 'Space Mono',monospace;
}
.anomaly-row .type { color: rgba(200,184,168,0.5); }
.anomaly-row .val  { color: #c8b8a8; margin-left: auto; }
.anomaly-row.alert .val { color: #dc2626; }

/* 血色进度条 */
.blood-bar { height: 4px; background: rgba(139,0,0,0.1); border-radius:0; }
.blood-fill { height: 100%; background: linear-gradient(90deg, #450000, #8b0000, #dc2626); }

/* 惊悚标签 */
.horror-tag {
  display: inline-flex; align-items: center;
  background: rgba(139,0,0,0.1); border: 1px solid rgba(139,0,0,0.25);
  padding: 2px 7px; border-radius: 0;
  font-family: 'Space Mono',monospace; font-size: 8.5px;
  color: rgba(139,0,0,0.9); letter-spacing: 1.5px; text-transform: uppercase;
}

/* 羊皮纸分割线 */
.decay-rule {
  height: 1px; border: none;
  background: repeating-linear-gradient(
    90deg, transparent, transparent 4px, rgba(139,0,0,0.2) 4px, rgba(139,0,0,0.2) 5px
  );
  margin: 6px 0;
}

/* 引用（目击者证词） */
.testimony {
  background: rgba(139,0,0,0.05);
  border-left: 2px solid rgba(139,0,0,0.4);
  padding: 6px 10px; font-size: 10px;
  font-family: 'Playfair Display',serif; font-style: italic;
  color: rgba(200,184,168,0.7);
}
```

---

## CSS 变量

```css
:root {
  --bg:   #030303;
  --card: rgba(10,5,5,0.95);
  --p:    #8b0000;
  --pm:   rgba(139,0,0,0.08);
  --bd:   rgba(139,0,0,0.2);
  --t:    #c8b8a8;
  --mt:   #7a6a5a;
  --dt:   #3a2a1a;
}
```
