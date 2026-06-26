# 零售电商（Retail Commerce）

**气质：** 商业活力、消费增长、用户转化、大促氛围
**适用：** 销售报告、电商数据、消费者洞察、GMV分析
**推荐字体：** FP-1（Syne + DM Sans）
**背景类型：** 亮白（#ffffff）或极浅暖灰（#fafaf8），商务干净
**主标题字号：** 44–60px Syne 粗体，GMV/转化率数字最大化
**页眉形式：** 左侧大促节点名（618/双11），右侧周期与平台，橙色底线

---

## 设计特征

- **商业橙**（#ea580c / #f97316）+ **增长绿**（#16a34a）双强调色
- 纯白背景，高密度数据，GMV/转化/复购三核心
- 超大金额数字 + 亿/万单位标注
- 漏斗图/转化链路为核心视觉
- 徽章用橙色圆角胶囊，活动感十足

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

body { background: #fafaf8; font-family: 'DM Sans','PingFang SC',sans-serif; color: #111827; }

/* 展示标题（GMV 冲击） */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 56px; font-weight: 800;
  letter-spacing: -2.5px; line-height: 0.92;
  color: #ea580c;
}

/* 大促节点标签 */
.promo-badge {
  display: inline-flex; align-items: center;
  background: linear-gradient(135deg, #ea580c, #f97316);
  color: #ffffff; border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 800; letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* 卡片（白色，橙色顶线） */
.card {
  background: #ffffff;
  border: 1px solid rgba(234,88,12,0.1);
  border-top: 2px solid #ea580c;
  border-radius: 6px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 2px 8px rgba(234,88,12,0.07);
}

/* KPI 金额/GMV */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 48px; font-weight: 800; line-height: 1; letter-spacing: -2px;
  color: #ea580c;
}
.stat-unit { font-size: 16px; font-weight: 600; color: #9ca3af; margin-left: 2px; }

/* 增长率（绿色正向） */
.growth-rate {
  font-size: 12px; font-weight: 700; color: #16a34a;
}
.growth-rate::before { content: '↑ '; }
.growth-rate.neg { color: #dc2626; }
.growth-rate.neg::before { content: '↓ '; }

/* 转化漏斗节点 */
.funnel-node {
  display: flex; justify-content: space-between; align-items: center;
  padding: 4px 8px; border-radius: 3px; font-size: 10px;
  background: rgba(234,88,12,0.06); margin-bottom: 2px;
}
.funnel-node .rate { color: #ea580c; font-weight: 700; }

/* 数据行 */
.commerce-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(234,88,12,0.07);
}

/* 进度条（橙色） */
.sales-bar { height: 4px; border-radius: 4px; background: rgba(234,88,12,0.1); }
.sales-fill { height: 100%; border-radius: 4px;
  background: linear-gradient(90deg, #c2410c, #ea580c, #fb923c); }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fafaf8;
  --card: #ffffff;
  --p:    #ea580c;
  --pm:   rgba(234,88,12,0.08);
  --bd:   rgba(234,88,12,0.12);
  --t:    #111827;
  --mt:   #4b5563;
  --dt:   #9ca3af;
}
/* --ok: #16a34a; (增长绿) */
```
