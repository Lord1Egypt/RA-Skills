# Timeline 页面 CSS 组件参考

## CSS 变量完整定义

```css
:root {
  /* 背景层级 */
  --bg: #fff;           /* 主背景 */
  --bg-2: #f8f9fb;      /* 卡片/次级 */
  --bg-3: #f1f3f6;      /* 三级/边框内 */

  /* 边框 */
  --border: #e5e7eb;
  --border-2: #d1d5db;

  /* 文本 */
  --text: #1a1a2e;      /* 主文本 */
  --text-2: #4b5563;    /* 次级文本 */
  --text-3: #9ca3af;    /* 弱文本/辅助 */

  /* 语义色彩 */
  --blue: #2563eb;      /* 交互/信息 */
  --indigo: #6366f1;     /* 辅助蓝 */
  --purple: #7c3aed;    /* 视觉/创意 */
  --rose: #e94560;      /* 发布/重要 */
  --green: #059669;     /* 完成/工具 */
  --amber: #d97706;     /* 警告/评审 */
  --cyan: #0891b2;      /* 测试/进行中 */

  /* 排版 */
  --font: 'Noto Sans SC', sans-serif;
  --font-display: 'Noto Serif SC', serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* 动画 */
  --ease: cubic-bezier(.16, 1, .3, 1);

  /* 布局 */
  --max-w: 820px;
}
```

## 组件样式参考

### Hero 区域

```css
.hero {
  padding: 100px 28px 56px;
  text-align: center;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 14px; border-radius: 100px;
  font-size: 12px; font-weight: 500;
  background: rgba(var(--green-rgb), 0.06);
  border: 1px solid rgba(var(--green-rgb), 0.15);
  color: var(--green);
}
.hero h1 {
  font-family: var(--font-display);
  font-size: clamp(28px, 5vw, 40px);  /* 流式字体 */
  font-weight: 900; letter-spacing: -.02em;
}
.hero-meta {
  display: flex; justify-content: center; gap: 20px;
  font-size: 13px; color: var(--text-3);
  font-family: var(--font-mono);
}
```

### Key Nodes 时间轴

```css
.kn-track {
  position: relative;
  padding-left: 52px;         /* 给圆点留空间 */
}
.kn-track::before {
  content: ''; position: absolute;
  left: 19px; top: 0; bottom: 0;
  width: 2px; background: var(--bg-3);  /* 连线 */
}
.kn-dot {
  position: absolute; left: -38px; top: 16px;
  width: 18px; height: 18px; border-radius: 50%;
  border: 3px solid var(--bg);  /* 白色边框制造空心感 */
}
.kn-dot.c-blue { background: var(--blue); box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
/* 其他颜色同理... */
.kn-dot.active { animation: blink 2s infinite; }  /* 进行中节点闪烁 */

.kn-card {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 11px; overflow: hidden;
  transition: box-shadow .2s;
}
.kn-card:hover { box-shadow: 0 2px 14px rgba(0,0,0,.04); }

.kn-detail {
  max-height: 0; overflow: hidden;
  transition: max-height .35s var(--ease);
}
.kn.open .kn-detail { max-height: 500px; }  /* 折叠动画 */
```

### Gantt 图

```css
.gantt { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.gantt-bar {
  position: absolute; top: 50%; transform: translateY(-50%);
  height: 22px; border-radius: 4px;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 500; color: #fff;
}
.gantt-bar.ix { background: var(--blue); }
.gantt-bar.vis { background: var(--purple); }
.gantt-bar.tool { background: var(--green); }

.gantt-tl {
  position: absolute; top: 0; bottom: 0;
  width: 1.5px; background: var(--blue); opacity: .25;
}
```

### Todo List

```css
.todo-li {
  display: flex; align-items: flex-start; gap: 9px;
  padding: 7px 10px; border-radius: 7px;
  cursor: pointer; user-select: none;
  transition: background .15s;
}
.todo-li.done { opacity: .4; }           /* 完成项变淡 */
.todo-li.done .todo-tx { text-decoration: line-through; }
.todo-ck {
  width: 17px; height: 17px; margin-top: 2px;
  border: 2px solid var(--border-2); border-radius: 4px;
  display: flex; align-items: center; justify-content: center;
}
.todo-li.done .todo-ck { background: var(--green); border-color: var(--green); color: #fff; }

.todo-tg {
  font-size: 10.5px; font-weight: 500;
  padding: 2px 7px; border-radius: 4px; margin-top: 2px;
}
.todo-tg.ix { background: rgba(37,99,235,.06); color: var(--blue); }
.todo-tg.vis { background: rgba(124,58,237,.06); color: var(--purple); }
.todo-tg.plan { background: rgba(217,119,6,.06); color: var(--amber); }
.todo-tg.collab { background: rgba(5,150,105,.06); color: var(--green); }
```

### Callout 信息卡片

```css
.co-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; }
.co {
  background: var(--bg-2); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 18px;
  border-left: 3px solid var(--blue);   /* 左色条 */
}
.co.warn { border-left-color: var(--amber); }
.co.danger { border-left-color: var(--rose); }
.co.ok { border-left-color: var(--green); }
.co.info { border-left-color: var(--cyan); }
.co-t { font-size: 13.5px; font-weight: 600; margin-bottom: 4px; }
.co-b { font-size: 12.5px; color: var(--text-2); line-height: 1.7; }
```

### Chip 状态标签

```css
.kn-chip {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 500; font-family: var(--font-mono);
}
.kn-chip.done { background: rgba(5,150,105,.08); color: var(--green); }
.kn-chip.today { background: rgba(37,99,235,.08); color: var(--blue); }
.kn-chip.soon { background: rgba(99,102,241,.08); color: var(--indigo); }
.kn-chip.later { background: rgba(156,163,175,.1); color: var(--text-3); }
```

## 动画

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.anim { opacity: 0; animation: fadeUp .5s var(--ease) forwards; animation-play-state: paused; }
.d1 { animation-delay: .05s; } .d2 { animation-delay: .1s; }
.d3 { animation-delay: .15s; } .d4 { animation-delay: .2s; }

/* IntersectionObserver 在 JS 中控制播放 */
```

## 响应式断点

```css
@media(max-width:768px){
  .ov { grid-template-columns: repeat(2, 1fr); }  /* 四宫格变两列 */
  .gantt { overflow-x: auto; }                     /* Gantt 横滚 */
  .gantt-head, .gantt-row { min-width: 700px; }
  .hero { padding: 80px 20px 40px; }
}
```
