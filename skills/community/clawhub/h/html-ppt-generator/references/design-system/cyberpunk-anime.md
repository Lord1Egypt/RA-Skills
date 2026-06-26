# 赛博朋克动漫（Cyberpunk Anime）
<!-- Note: 与通用 neon-cyberpunk.md 区别：本模板侧重动漫美学（攻壳/赛博都市），双色青+洋红碰撞，有 anime 感；neon-cyberpunk 偏西方赛博朋克/暗网美学 -->

**气质：** 攻壳机动队、赛博都市、义体改造、AI觉醒、意识上传
**适用：** 科幻题材报告、AI/科技趋势、网络安全、未来主义分析
**推荐字体：** FP-3（Space Mono + IBM Plex Sans），机械感
**背景类型：** 暗色系（赛博黑 #030810），青色+洋红 neon 双色光
**主标题字号：** 36–50px，带 glitch 错位感描边，半透明感
**页眉形式：** 左侧 SECTOR/NODE 编号，右侧系统时间+信号条，青色光条

---

## 设计特征

- **赛博青**（#00fff0 / #22d3ee）+ **义体洋红**（#ff0080 / #ec4899）双色碰撞
- 深海蓝黑背景，双色发光光晕
- 文字带 RGB split 效果（text-shadow 青+洋红偏移）
- 卡片半透明磨砂玻璃 + 青色顶部扫描线
- 数据流/脑机接口/义体等赛博词汇混入组件

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #030810; font-family: 'IBM Plex Sans','PingFang SC',sans-serif; color: #c8f0f8; }

/* 赛博双色光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(0,255,240,0.08) 0%, transparent 45%),
    radial-gradient(ellipse at 80% 70%, rgba(255,0,128,0.07) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 50%, rgba(0,30,60,0.5)    0%, transparent 70%);
}

/* 雨水竖线扫描 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: repeating-linear-gradient(
    90deg, rgba(0,255,240,0.015) 0, rgba(0,255,240,0.015) 1px,
    transparent 1px, transparent 4px
  );
}

/* 展示标题（赛博 RGB split） */
.display-title {
  font-family: 'Space Mono',monospace;
  font-size: 44px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 2px; line-height: 1.05;
  color: #00fff0;
  text-shadow:
    -2px 0 rgba(255,0,128,0.7),
     2px 0 rgba(0,200,255,0.5);
  filter: drop-shadow(0 0 12px rgba(0,255,240,0.4));
}

/* 卡片（赛博磨砂玻璃） */
.card {
  background: rgba(3,8,16,0.85);
  border: 1px solid rgba(0,255,240,0.15);
  border-top: 1px solid rgba(0,255,240,0.5);
  border-radius: 4px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  backdrop-filter: blur(8px);
  box-shadow:
    0 0 20px rgba(0,255,240,0.05),
    inset 0 0 40px rgba(0,0,0,0.4);
  position: relative; overflow: hidden;
}
/* 顶部扫描线 */
.card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg, transparent, #00fff0, transparent);
  opacity: 0.6;
}

/* KPI（双色发光数字） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 42px; font-weight: 700; line-height: 1; letter-spacing: 1px;
  color: #00fff0;
  text-shadow:
    -1px 0 rgba(255,0,128,0.6),
     1px 0 rgba(0,200,255,0.4),
     0   0 20px rgba(0,255,240,0.5);
}

/* 系统状态标签（赛博feel） */
.cyber-tag {
  display: inline-flex; align-items: center; gap: 3px;
  border-radius: 2px; padding: 2px 7px;
  font-family: 'Space Mono',monospace; font-size: 8.5px; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
}
.cyber-tag.online  { background:rgba(0,255,240,0.1); color:#00fff0; border:1px solid rgba(0,255,240,0.3); }
.cyber-tag.offline { background:rgba(255,0,128,0.1); color:#ff0080; border:1px solid rgba(255,0,128,0.3); }
.cyber-tag.warn    { background:rgba(255,170,0,0.1); color:#ffaa00; border:1px solid rgba(255,170,0,0.3); }
.cyber-tag::before { content:'◉ '; font-size:7px; }

/* 数据流进度条 */
.dataflow-bar {
  height: 4px;
  background: rgba(0,255,240,0.08);
  border-radius: 0; position: relative;
}
.dataflow-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff0080, #00fff0);
  box-shadow: 0 0 8px rgba(0,255,240,0.4);
}

/* 义体/节点分割线 */
.node-rule {
  display: flex; align-items: center; gap: 6px;
  margin: 6px 0; font-family: 'Space Mono',monospace;
  font-size: 8px; color: rgba(0,255,240,0.4); letter-spacing: 2px;
}
.node-rule::before, .node-rule::after {
  content:''; flex:1; height:1px;
  background: rgba(0,255,240,0.2);
}

/* 数据行（脑机接口监控） */
.neural-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 9.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(0,255,240,0.06);
  font-family: 'Space Mono',monospace;
}
.neural-row .node  { color: rgba(200,240,248,0.45); }
.neural-row .val   { color: #00fff0; font-weight: 700; }
.neural-row .val.alert { color: #ff0080; }
```

---

## CSS 变量

```css
:root {
  --bg:   #030810;
  --card: rgba(3,8,16,0.85);
  --p:    #00fff0;
  --pm:   rgba(0,255,240,0.08);
  --bd:   rgba(0,255,240,0.15);
  --t:    #c8f0f8;
  --mt:   #5a9aaa;
  --dt:   #1a3040;
}
/* --magenta: #ff0080; (义体洋红，对比/警示) */
```
