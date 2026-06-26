# 轻小说异世界（Light Novel Isekai）

**气质：** 异世界转生、轻小说封面感、奇幻标题、主角光环
**适用：** 游戏奇幻数据、轻小说销量、二次元内容报告
**推荐字体：** FP-2（Playfair Display + Source Sans 3），封面衬线感
**背景类型：** 暗色系（异世界暮色 #0e0a1e），魔法阵紫蓝光晕
**主标题字号：** 36–54px，带副标题（长副标题是异世界精髓）
**页眉形式：** 魔法阵装饰圆形，"第N章"格式，金色卷轴感页眉

---

## 设计特征

- **异世界紫**（#7c3aed / #a855f7）+ **神圣金**（#f59e0b / #fbbf24）双主色
- 深暮色背景，魔法阵六芒星光晕
- 卡片模拟轻小说页边注释（金色细边）
- 技能名/称号/等级 等 LN 专属组件
- 副标题允许超长（异世界副标题就是要长）

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Source+Sans+3:wght@300;400;600&display=swap');

body { background: #0e0a1e; font-family: 'Source Sans 3','PingFang SC',sans-serif; color: #e8e0f0; }

/* 魔法阵光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 40%, rgba(124,58,237,0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 20% 70%, rgba(245,158,11,0.07) 0%, transparent 35%),
    radial-gradient(ellipse at 80% 20%, rgba(124,58,237,0.1)  0%, transparent 35%);
}

/* 展示标题（LN 封面感） */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 44px; font-weight: 900; font-style: italic;
  letter-spacing: -0.5px; line-height: 1.05;
  background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 20px rgba(245,158,11,0.4));
}

/* 异世界副标题（长副标题） */
.isekai-subtitle {
  font-family: 'Source Sans 3',sans-serif;
  font-size: 9.5px; color: rgba(168,85,247,0.8);
  line-height: 1.5; letter-spacing: 0.5px;
  font-style: italic;
}

/* 卡片（魔法卷轴感，金色细边） */
.card {
  background: rgba(14,10,30,0.92);
  border: 1px solid rgba(245,158,11,0.2);
  border-top: 1px solid rgba(245,158,11,0.5);
  border-radius: 4px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow:
    0 0 20px rgba(124,58,237,0.1),
    inset 0 0 30px rgba(0,0,0,0.4);
}

/* KPI（神圣金数字） */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 46px; font-weight: 900; font-style: italic; line-height: 1;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 12px rgba(245,158,11,0.5));
}

/* 技能名/称号框 */
.skill-box {
  display: inline-flex; align-items: center; gap: 4px;
  border: 1px solid rgba(245,158,11,0.4);
  background: rgba(245,158,11,0.06);
  padding: 2px 8px; border-radius: 2px;
  font-size: 9px; font-weight: 600; color: #fbbf24;
  letter-spacing: 0.5px;
}
.skill-box::before { content:'【'; color:rgba(245,158,11,0.5); }
.skill-box::after  { content:'】'; color:rgba(245,158,11,0.5); }

/* 等级/状态标签 */
.status-tag {
  display: inline-flex; align-items: center;
  border-radius: 2px; padding: 2px 7px;
  font-size: 9px; font-weight: 700; letter-spacing: 1px;
}
.status-tag.legendary { background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.35); }
.status-tag.rare      { background:rgba(124,58,237,0.15); color:#a855f7; border:1px solid rgba(124,58,237,0.35); }
.status-tag.common    { background:rgba(100,100,120,0.15); color:#9ca3af; border:1px solid rgba(100,100,120,0.25); }

/* 魔力值进度条 */
.mana-bar {
  height: 5px; border-radius: 0;
  background: rgba(124,58,237,0.1);
  border: 1px solid rgba(124,58,237,0.2);
}
.mana-fill {
  height: 100%;
  background: linear-gradient(90deg, #4c1d95, #7c3aed, #a855f7);
  box-shadow: 0 0 8px rgba(124,58,237,0.4);
}

/* 魔法阵分割线 */
.magic-rule {
  border: none; height: 1px; margin: 6px 0;
  background: linear-gradient(90deg, transparent, rgba(245,158,11,0.4), rgba(124,58,237,0.4), transparent);
}

/* 数据行（RPG 状态面板感） */
.isekai-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(124,58,237,0.08);
}
.isekai-row .label { color: rgba(232,224,240,0.45); }
.isekai-row .value { color: #fbbf24; font-weight: 600; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0e0a1e;
  --card: rgba(14,10,30,0.92);
  --p:    #f59e0b;
  --pm:   rgba(245,158,11,0.08);
  --bd:   rgba(245,158,11,0.2);
  --t:    #e8e0f0;
  --mt:   #a898c0;
  --dt:   #4a4060;
}
/* --magic: #7c3aed; (魔法紫) */
```
