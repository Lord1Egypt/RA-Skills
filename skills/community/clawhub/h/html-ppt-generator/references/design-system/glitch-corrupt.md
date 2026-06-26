# 故障艺术（Glitch Corrupt）

**气质：** 数据损坏、RGB错位、系统崩溃、数字噪声
**适用：** 网络安全报告、黑客事件、错误分析、攻击溯源、艺术实验
**推荐字体：** FP-3（Space Mono），故意错位
**背景类型：** 暗色系（错误黑 #050505），水平扫描线 + RGB偏移
**主标题字号：** 40–60px，带 CSS 故障动画（text-shadow RGB偏移）
**页眉形式：** 文字故意截断/重叠，ERROR 代码混入，系统崩溃感

---

## 设计特征

- **故障红**（#ff0033）+ **故障青**（#00ffee）+ **故障蓝**（#0022ff）RGB三原色错位
- 纯黑背景，水平撕裂扫描线
- 文字带 CSS clip 切割效果（上下偏移 1-3px）
- 卡片边框"破损"（虚线、斜切角、缺口）
- 随机噪点方块模拟数据损坏

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

body { background: #050505; font-family: 'Space Mono',monospace; color: #e0e0e0; }

/* 扫描线噪点 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: repeating-linear-gradient(
    0deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px,
    transparent 1px, transparent 4px
  );
}

/* 展示标题（RGB 三色错位故障） */
.display-title {
  font-family: 'Space Mono',monospace;
  font-size: 50px; font-weight: 700; text-transform: uppercase;
  letter-spacing: -1px; line-height: 1.0;
  color: #e0e0e0;
  text-shadow:
    -2px  0 rgba(255,0,51,0.8),
     2px  0 rgba(0,255,238,0.8),
     0    1px rgba(0,34,255,0.4);
  position: relative;
}

/* 故障标题切割（上半） */
.display-title::before {
  content: attr(data-text);
  position: absolute; left: 0; top: 0; width: 100%;
  clip: rect(0, 9999px, 24px, 0);
  transform: translateX(-3px);
  color: #ff0033; opacity: 0.8;
}

/* 卡片（破损边框） */
.card {
  background: rgba(5,5,5,0.95);
  border: 1px solid rgba(255,0,51,0.3);
  border-right: 1px solid rgba(0,255,238,0.3);
  border-radius: 0;
  padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  position: relative;
  clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));
}

/* 缺角装饰 */
.card::after {
  content: ''; position: absolute; top: 0; right: 0;
  border-top: 8px solid rgba(255,0,51,0.4);
  border-left: 8px solid transparent;
}

/* KPI 数字（故障发光） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 44px; font-weight: 700; line-height: 1;
  color: #00ffee;
  text-shadow:
    -1px 0 #ff0033,
     1px 0 #0022ff;
}

/* ERROR 标签 */
.glitch-tag {
  display: inline-flex; align-items: center;
  background: rgba(255,0,51,0.1); border: 1px solid rgba(255,0,51,0.4);
  padding: 2px 7px; border-radius: 0;
  font-size: 8.5px; font-weight: 700; color: #ff0033;
  letter-spacing: 2px; text-transform: uppercase;
}
.glitch-tag.ok  { background:rgba(0,255,238,0.1); border-color:rgba(0,255,238,0.4); color:#00ffee; }
.glitch-tag.sys { background:rgba(0,34,255,0.1); border-color:rgba(0,34,255,0.4); color:#4488ff; }

/* 故障进度条（信号不稳定感） */
.corrupt-bar {
  height: 4px; background: rgba(255,255,255,0.05);
  border-radius: 0; position: relative; overflow: hidden;
}
.corrupt-fill {
  height: 100%;
  background: repeating-linear-gradient(
    90deg, #ff0033 0, #ff0033 70%, #00ffee 70%, #00ffee 72%, #ff0033 72%
  );
}

/* 噪点方块（数据损坏） */
.noise-block {
  display: inline-block; width: 8px; height: 8px;
  background: #ff0033; opacity: 0.6;
  box-shadow: 12px 0 #00ffee, 24px 0 #0022ff;
}

/* 系统日志行 */
.sys-log {
  font-size: 9px; font-family: 'Space Mono',monospace;
  color: rgba(224,224,224,0.5); padding: 2px 0;
  border-bottom: 1px solid rgba(255,0,51,0.06);
}
.sys-log .err { color: #ff0033; }
.sys-log .warn { color: #ffaa00; }
.sys-log .ok   { color: #00ffee; }
```

---

## CSS 变量

```css
:root {
  --bg:   #050505;
  --card: rgba(5,5,5,0.95);
  --p:    #ff0033;
  --pm:   rgba(255,0,51,0.1);
  --bd:   rgba(255,0,51,0.3);
  --t:    #e0e0e0;
  --mt:   #888888;
  --dt:   #333333;
}
/* --cyan: #00ffee; --blue: #0022ff; */
```
