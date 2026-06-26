# 游戏RPG（Game RPG UI）

**气质：** 角色扮演游戏、状态面板、任务日志、像素奇幻
**适用：** 游戏行业报告、玩家数据、游戏策划文档、战绩分析
**推荐字体：** 像素/等宽（Space Mono）+ 奇幻衬线（Cinzel）
**背景类型：** 暗色系（地牢黑 #0d0d0d），羊皮纸卷轴变体可选
**主标题字号：** 32–44px 全大写，类游戏标题字体，边框描边感
**页眉形式：** 左侧 HP/MP 血条，中间任务名，右侧经验值 EXP，像素风

---

## 设计特征

- **魔法金**（#fbbf24 / #f59e0b）+ **生命红**（#dc2626）+ **魔力蓝**（#3b82f6）三色体系
- 地牢石板背景，细石砖纹理
- 血条/经验条/魔法条三层进度系统
- 卡片用石板感边框（双线内嵌，四角装饰）
- 对话框、任务日志、物品栏等 RPG 专属组件

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Space+Mono:wght@400;700&display=swap');

body { background: #0d0d0d; font-family: 'Space Mono',monospace; color: #d4c5a0; }

/* 石砖纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, transparent 1px, transparent 32px),
    repeating-linear-gradient(90deg, rgba(255,255,255,0.015) 0px, transparent 1px, transparent 32px);
  background-size: 32px 32px;
}

/* 展示标题（奇幻魔法） */
.display-title {
  font-family: 'Cinzel',serif;
  font-size: 38px; font-weight: 900; text-transform: uppercase;
  letter-spacing: 3px; line-height: 1.1;
  background: linear-gradient(180deg, #fde68a 0%, #f59e0b 50%, #92400e 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none; filter: drop-shadow(0 2px 8px rgba(251,191,36,0.4));
}

/* 四角装饰卡片（石板感） */
.card {
  background: rgba(13,10,5,0.95);
  border: 1px solid rgba(251,191,36,0.25);
  outline: 3px solid rgba(251,191,36,0.08);
  outline-offset: 2px;
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  position: relative;
}
.card::before, .card::after,
.card-inner::before, .card-inner::after {
  content:'◈'; position:absolute; color:rgba(251,191,36,0.5);
  font-size:10px; line-height:1;
}
.card::before  { top:-6px; left:-6px; }
.card::after   { top:-6px; right:-6px; }

/* 血量/经验值大数字 */
.stat-num {
  font-family: 'Cinzel', serif;
  font-size: 40px; font-weight: 900; line-height: 1;
  letter-spacing: 2px; text-transform: uppercase;
  background: linear-gradient(180deg, #fde68a, #f59e0b);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* HP 血条（生命值） */
.hp-bar {
  height: 10px; background: rgba(220,38,38,0.2);
  border: 1px solid rgba(220,38,38,0.4);
  border-radius: 1px; position: relative; overflow: hidden;
}
.hp-fill { height: 100%; background: linear-gradient(90deg, #991b1b, #dc2626, #fca5a5); }

/* MP 魔法条 */
.mp-bar {
  height: 8px; background: rgba(59,130,246,0.2);
  border: 1px solid rgba(59,130,246,0.4);
  border-radius: 1px; overflow: hidden;
}
.mp-fill { height: 100%; background: linear-gradient(90deg, #1d4ed8, #3b82f6, #93c5fd); }

/* EXP 经验条 */
.exp-bar {
  height: 6px; background: rgba(251,191,36,0.15);
  border: 1px solid rgba(251,191,36,0.3);
  border-radius: 1px; overflow: hidden;
}
.exp-fill { height: 100%; background: linear-gradient(90deg, #92400e, #f59e0b, #fde68a); }

/* 任务/物品标签 */
.item-tag {
  display: inline-flex; align-items: center; gap: 3px;
  border: 1px solid currentColor; padding: 1px 6px;
  font-size: 8.5px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  border-radius: 1px;
}
.item-tag.rare   { color: #a855f7; }
.item-tag.epic   { color: #f59e0b; }
.item-tag.common { color: #6b7280; }
.item-tag.boss   { color: #dc2626; }

/* 对话框（NPC 任务说明） */
.dialog-box {
  background: rgba(0,0,0,0.8);
  border: 2px solid rgba(251,191,36,0.3);
  border-radius: 2px; padding: 8px 10px;
  font-family: 'Space Mono',monospace; font-size: 9.5px;
  color: #d4c5a0; position: relative;
}
.dialog-box::before {
  content: '▶ '; color: #f59e0b; font-size: 8px;
}

/* 任务列表行 */
.quest-item {
  display: flex; gap: 8px; padding: 3px 0; font-size: 9.5px;
  border-bottom: 1px solid rgba(251,191,36,0.08);
}
.quest-item .status-done  { color: #4ade80; }
.quest-item .status-prog  { color: #f59e0b; }
.quest-item .status-lock  { color: #4b5563; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0d0d0d;
  --card: rgba(13,10,5,0.95);
  --p:    #f59e0b;
  --pm:   rgba(251,191,36,0.1);
  --bd:   rgba(251,191,36,0.25);
  --t:    #d4c5a0;
  --mt:   #a08c6a;
  --dt:   #5c4a30;
}
/* --hp: #dc2626; --mp: #3b82f6; --exp: #f59e0b; */
```
