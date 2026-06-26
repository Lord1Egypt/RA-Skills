# 教育科技（Education Tech）

**气质：** 学习成长、知识传递、校园活力、EdTech产品感
**适用：** 教育报告、学情分析、课程数据、校园运营
**推荐字体：** FP-6（Fraunces + Nunito）
**背景类型：** 亮色系（知识白 #fafbff / 微蓝白），温和友好
**主标题字号：** 40–54px Fraunces 可变体，圆润亲和，不失力量
**页眉形式：** 左侧课程/学期，右侧班级/学号范围，彩色渐变分割线

---

## 设计特征

- **知识蓝紫**（#4f46e5 / #7c3aed）+ **活力黄**（#f59e0b）双主色
- 白底蓝紫系，友好圆润，不压迫
- 圆角卡片 12px，活泼配色，学习进度可视化
- 彩色多段进度条（模拟学科分布）
- 成就徽章、知识点标签，游戏化学习感

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,900&family=Nunito:wght@400;600;700;800&display=swap');

body { background: #fafbff; font-family: 'Nunito','PingFang SC',sans-serif; color: #1e1b4b; }

/* 渐变背景晕染 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 90% 10%, rgba(79,70,229,0.07) 0%, transparent 45%),
    radial-gradient(ellipse at 10% 90%, rgba(245,158,11,0.06) 0%, transparent 40%);
}

/* 展示标题（圆润活力） */
.display-title {
  font-family: 'Fraunces','Noto Serif SC',serif;
  font-size: 48px; font-weight: 900;
  letter-spacing: -1.5px; line-height: 1.0;
  color: #4f46e5;
}

/* 卡片（圆角友好） */
.card {
  background: #ffffff;
  border: none;
  border-radius: 12px; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 6px;
  box-shadow: 0 4px 16px rgba(79,70,229,0.09), 0 1px 4px rgba(0,0,0,0.05);
}

/* KPI / 学习指标 */
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 46px; font-weight: 900; line-height: 1; letter-spacing: -1.5px;
  color: #4f46e5;
}

/* 知识点/技能标签（彩色） */
.skill-tag {
  display: inline-flex; align-items: center;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 800; letter-spacing: 0.3px;
}
.skill-tag.blue   { background: rgba(79,70,229,0.1); color: #4f46e5; }
.skill-tag.purple { background: rgba(124,58,237,0.1); color: #7c3aed; }
.skill-tag.amber  { background: rgba(245,158,11,0.12); color: #d97706; }
.skill-tag.green  { background: rgba(22,163,74,0.1); color: #16a34a; }

/* 学习进度条（多色分段） */
.learn-bar { height: 6px; border-radius: 6px; overflow: hidden; display: flex; }
.learn-seg { height: 100%; }

/* 单科进度条 */
.subject-bar {
  height: 5px; border-radius: 5px;
  background: rgba(79,70,229,0.1);
}
.subject-fill { height: 100%; border-radius: 5px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed); }

/* 成就徽章 */
.achievement {
  display: inline-flex; align-items: center; gap: 4px;
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  color: #78350f; border-radius: 6px; padding: 3px 8px;
  font-size: 9px; font-weight: 800;
}

/* 学情数据行 */
.edu-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(79,70,229,0.07);
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fafbff;
  --card: #ffffff;
  --p:    #4f46e5;
  --pm:   rgba(79,70,229,0.08);
  --bd:   rgba(79,70,229,0.12);
  --t:    #1e1b4b;
  --mt:   #4b5563;
  --dt:   #9ca3af;
}
/* --p2: #7c3aed; --accent: #f59e0b; */
```
