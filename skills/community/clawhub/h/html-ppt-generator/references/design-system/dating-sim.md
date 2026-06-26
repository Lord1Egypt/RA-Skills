# 美少女游戏（Dating Sim UI）

**气质：** Galgame/美少女游戏界面、对话框选择、角色立绘、恋爱模拟
**适用：** 游戏UI设计报告、视觉小说数据、AVG游戏分析
**推荐字体：** FP-6（Fraunces + Nunito），温柔可亲
**背景类型：** 亮色系（游戏背景蓝白 #eef6ff / 日系学校天空感），清透
**主标题字号：** 32–44px，带文字框背景（半透明黑框），VN 游戏标题感
**页眉形式：** 游戏状态栏（左侧角色名，中间好感度进度，右侧场景/日期）

---

## 设计特征

- **恋爱粉**（#f472b6）+ **天空蓝**（#38bdf8）+ **温柔黄**（#fde68a）三色系
- 淡蓝白背景，日系学校清晨感
- 对话框（VN Dialog Box）为核心组件：半透明黑底+白字+发言人名框
- 选择项按钮（Choice Button）带悬停发光
- 好感度进度条（Affection Bar），角色状态图标

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,700&family=Nunito:wght@400;600;700;800&display=swap');

body { background: #eef6ff; font-family: 'Nunito','PingFang SC',sans-serif; color: #1e3a5f; }

/* 清晨天空渐变 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: linear-gradient(180deg, #dbeafe 0%, #eff6ff 40%, #fdf4ff 100%);
}

/* 展示标题（VN 标题感，带黑框底） */
.display-title {
  font-family: 'Fraunces','Noto Serif SC',serif;
  font-size: 40px; font-weight: 700; font-style: italic;
  letter-spacing: -0.5px; line-height: 1.1;
  color: #ffffff;
  background: rgba(0,0,0,0.6);
  padding: 4px 12px; display: inline-block;
  border-left: 3px solid #f472b6;
}

/* 卡片（VN 信息面板感） */
.card {
  background: rgba(255,255,255,0.88);
  border: 1px solid rgba(56,189,248,0.25);
  border-top: 2px solid #38bdf8;
  border-radius: 8px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  backdrop-filter: blur(6px);
  box-shadow: 0 4px 16px rgba(56,189,248,0.1);
}

/* VN 对话框（核心组件） */
.vn-dialog {
  background: rgba(10,15,30,0.82);
  border: 1px solid rgba(248,182,230,0.3);
  border-radius: 6px; padding: 10px 14px;
  position: relative;
}
.vn-speaker {
  position: absolute; top:-14px; left:12px;
  background: #f472b6; color: #ffffff;
  font-size: 9px; font-weight: 800; padding: 2px 10px;
  border-radius: 4px 4px 0 0; letter-spacing: 1px;
}
.vn-dialog p {
  font-size: 11px; color: #f0e8ff; line-height: 1.7;
  margin: 0; font-family: 'Nunito',sans-serif;
}
.vn-dialog::after {
  content: '▼'; position: absolute; bottom:6px; right:10px;
  color: rgba(244,114,182,0.6); font-size: 8px;
}

/* 选择项按钮 */
.choice-btn {
  display: block; width: 100%;
  background: rgba(255,255,255,0.9);
  border: 1.5px solid rgba(56,189,248,0.4);
  border-radius: 6px; padding: 6px 12px;
  font-size: 10px; font-weight: 700; color: #1e3a5f;
  text-align: center; cursor: pointer;
  box-shadow: 0 2px 6px rgba(56,189,248,0.1);
  transition: none;
}
.choice-btn:hover, .choice-btn.selected {
  background: rgba(244,114,182,0.1);
  border-color: #f472b6; color: #9d174d;
}

/* 好感度进度条 */
.affection-bar {
  height: 8px; border-radius: 100px;
  background: rgba(244,114,182,0.12);
  border: 1px solid rgba(244,114,182,0.2);
}
.affection-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, #f9a8d4, #f472b6, #ec4899);
  box-shadow: 0 0 6px rgba(244,114,182,0.3);
}

/* KPI（好感度/分数大数字） */
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 46px; font-weight: 700; font-style: italic; line-height: 1;
  color: #f472b6;
  filter: drop-shadow(0 0 8px rgba(244,114,182,0.3));
}

/* 角色状态标签 */
.route-tag {
  display: inline-flex; align-items: center; gap: 3px;
  border-radius: 100px; padding: 2px 8px;
  font-size: 9px; font-weight: 800;
}
.route-tag.pink  { background: rgba(244,114,182,0.12); color: #be185d; }
.route-tag.blue  { background: rgba(56,189,248,0.12);  color: #0369a1; }
.route-tag.good  { background: rgba(74,222,128,0.12);  color: #15803d; }
.route-tag.bad   { background: rgba(239,68,68,0.1);    color: #dc2626; }

/* 场景分割线 */
.scene-rule {
  height: 1px; border: none;
  background: linear-gradient(90deg, transparent, rgba(244,114,182,0.3), rgba(56,189,248,0.3), transparent);
  margin: 6px 0;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #eef6ff;
  --card: rgba(255,255,255,0.88);
  --p:    #f472b6;
  --pm:   rgba(244,114,182,0.08);
  --bd:   rgba(56,189,248,0.2);
  --t:    #1e3a5f;
  --mt:   #4b7ab0;
  --dt:   #93c5fd;
}
/* --sky: #38bdf8; --warm: #fde68a; */
```
