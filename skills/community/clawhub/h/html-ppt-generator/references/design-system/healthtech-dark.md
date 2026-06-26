# 医疗健康科技（HealthTech）

**气质：** 数字健康、可穿戴、AI医疗、生命体征实时感
**适用：** 健康科技报告、数字医疗、运动健康数据、可穿戴设备分析
**推荐字体：** FP-1（Syne + DM Sans）
**背景类型：** 暗色系（深夜健康黑 #080f1a），心率监测屏幕感
**主标题字号：** 36–48px，无衬线冲击，生命体征数字感
**页眉形式：** 左侧设备/用户ID，中间实时时间戳，右侧心率图标，霓虹绿

---

## 设计特征

- **生命绿**（#22c55e / #4ade80）+ **心率粉**（#f43f5e）双主色，生命体征感
- 深夜黑背景，模拟可穿戴设备屏幕
- 心跳折线、血氧圆环、步数进度等专属组件
- 数字实时感（等宽字体，数值变化感）
- 卡片带绿色发光微光效

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

body { background: #080f1a; font-family: 'DM Sans','PingFang SC',sans-serif; color: #d1fae5; }

/* 生命迹象光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 100%, rgba(34,197,94,0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(244,63,94,0.04) 0%, transparent 40%);
}

/* 展示标题（生命绿发光） */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 44px; font-weight: 800;
  letter-spacing: -1.5px; line-height: 1.0;
  color: #4ade80;
  text-shadow: 0 0 30px rgba(74,222,128,0.3);
}

/* 卡片（暗底，绿色微光边） */
.card {
  background: rgba(8,20,38,0.9);
  border: 1px solid rgba(34,197,94,0.15);
  border-top: 1px solid rgba(74,222,128,0.4);
  border-radius: 8px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 0 20px rgba(34,197,94,0.05);
}

/* 生命体征大数字 */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 46px; font-weight: 800; line-height: 1; letter-spacing: -1.5px;
  color: #4ade80;
  text-shadow: 0 0 20px rgba(74,222,128,0.4);
}
.stat-num.heart { color: #f43f5e; text-shadow: 0 0 20px rgba(244,63,94,0.4); }

/* 体征状态标签 */
.vitals-tag {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: 100px; padding: 2px 8px;
  font-size: 9px; font-weight: 700;
}
.vitals-tag.ok   { background: rgba(34,197,94,0.15); color: #4ade80; border:1px solid rgba(34,197,94,0.3); }
.vitals-tag.warn { background: rgba(251,191,36,0.15); color: #fbbf24; border:1px solid rgba(251,191,36,0.3); }
.vitals-tag.risk { background: rgba(244,63,94,0.15);  color: #f43f5e; border:1px solid rgba(244,63,94,0.3); }

/* 心跳脉冲条 */
.pulse-bar { height: 3px; border-radius: 3px;
  background: rgba(34,197,94,0.1); }
.pulse-fill { height: 100%; border-radius: 3px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #4ade80);
  box-shadow: 0 0 8px rgba(74,222,128,0.4); }

/* 数据行（深夜监测） */
.vitals-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10px; padding: 3px 0;
  border-bottom: 1px solid rgba(34,197,94,0.08);
}
.vitals-row .metric { color: #6ee7b7; }
.vitals-row .val    { color: #4ade80; font-weight: 700; font-family: 'DM Sans',monospace; }

/* 时间戳 */
.realtime-stamp {
  font-size: 8.5px; color: rgba(74,222,128,0.5);
  letter-spacing: 1px;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #080f1a;
  --card: #08141e;
  --p:    #22c55e;
  --pm:   rgba(34,197,94,0.12);
  --bd:   rgba(34,197,94,0.18);
  --t:    #d1fae5;
  --mt:   #6ee7b7;
  --dt:   #374151;
}
/* --heart: #f43f5e; (心率粉，异常/心跳) */
```
