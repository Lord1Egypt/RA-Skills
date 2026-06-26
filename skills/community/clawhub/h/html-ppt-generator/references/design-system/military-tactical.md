# 军事战术（Military Tactical）

**气质：** 作战指挥、任务简报、战术分析、国防安全
**适用：** 军事报告、安防分析、危机应对、应急指挥汇报
**推荐字体：** FP-3（Space Mono + IBM Plex Sans）
**背景类型：** 暗色系（作战黑 #0b0d08 / 深橄榄绿 #1a2010），战术地图感
**主标题字号：** 28–36px 等宽大写，任务编号前缀，MISSION CRITICAL感
**页眉形式：** 左侧任务编号（OPS-2024-001），中间分类密级（SECRET/UNCLASS），右侧UTC时间

---

## 设计特征

- **军绿**（#4d7c0f / #65a30d）+ **橄榄黄**（#a16207）双主色，迷彩战术感
- 深黑背景 + 细横纹扫描线（作战屏幕感）
- 等宽字体显示坐标、编号、参数
- 危险等级用红/橙/黄/绿四色编码（类交通灯）
- 地图网格参照、目标标记 ⊕ 等军事符号

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #0b0d08; font-family: 'IBM Plex Sans','PingFang SC',sans-serif; color: #a8b89a; }

/* 战术扫描线 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: repeating-linear-gradient(
    0deg,
    rgba(77,124,15,0.025) 0px, rgba(77,124,15,0.025) 1px,
    transparent 1px, transparent 3px
  );
}

/* 展示标题（任务代号感） */
.display-title {
  font-family: 'Space Mono',monospace;
  font-size: 30px; font-weight: 700;
  letter-spacing: 2px; line-height: 1.1; text-transform: uppercase;
  color: #65a30d;
  text-shadow: 0 0 20px rgba(101,163,13,0.25);
}

/* 密级标注 */
.classification {
  font-family: 'Space Mono',monospace;
  font-size: 9px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
  border: 1px solid currentColor; padding: 1px 6px; display: inline-block;
}
.classification.secret { color: #dc2626; }
.classification.conf   { color: #ea580c; }
.classification.unclass { color: #65a30d; }

/* 卡片（作战指挥台感） */
.card {
  background: rgba(15,20,10,0.95);
  border: 1px solid rgba(77,124,15,0.2);
  border-left: 3px solid #4d7c0f;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* KPI / 战术数据 */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 36px; font-weight: 700; line-height: 1;
  color: #65a30d;
  text-shadow: 0 0 15px rgba(101,163,13,0.3);
}

/* 威胁等级（四色编码） */
.threat-tag {
  display: inline-flex; align-items: center;
  border-radius: 0; padding: 2px 6px;
  font-family: 'Space Mono',monospace; font-size: 8px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
}
.threat-tag.crit { background:rgba(220,38,38,0.2); color:#dc2626; border:1px solid rgba(220,38,38,0.4); }
.threat-tag.high { background:rgba(234,88,12,0.2); color:#ea580c; border:1px solid rgba(234,88,12,0.4); }
.threat-tag.med  { background:rgba(161,98,7,0.2);  color:#a16207; border:1px solid rgba(161,98,7,0.4); }
.threat-tag.low  { background:rgba(77,124,15,0.2); color:#65a30d; border:1px solid rgba(77,124,15,0.4); }

/* 战术进度（目标达成率） */
.ops-bar { height: 4px; background: rgba(77,124,15,0.1); border-radius:0; }
.ops-fill { height: 100%; background: linear-gradient(90deg, #3f6212, #65a30d); }

/* 任务列表 */
.ops-item {
  display: flex; gap: 8px; font-family: 'Space Mono',monospace;
  font-size: 9.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(77,124,15,0.1); color: #8a9e7a;
}
.ops-item .id { color: #65a30d; font-weight: 700; width: 60px; flex-shrink: 0; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0b0d08;
  --card: #0f140a;
  --p:    #65a30d;
  --pm:   rgba(77,124,15,0.12);
  --bd:   rgba(77,124,15,0.2);
  --t:    #a8b89a;
  --mt:   #6b7c60;
  --dt:   #3d4a34;
}
```
