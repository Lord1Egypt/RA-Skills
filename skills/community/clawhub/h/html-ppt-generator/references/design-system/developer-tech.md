# 程序员技术（Developer Tech）

**气质：** 代码终端、黑客美学、开源社区、技术极客
**适用：** 技术报告、系统架构、开发总结、API文档、代码审计
**推荐字体：** FP-3（Space Mono + IBM Plex Sans）
**背景类型：** 暗色系（终端黑 #0d0d0d / 深炭灰 #111827），代码编辑器感
**主标题字号：** 30–40px 等宽字体，前缀 `>_` 或 `//`
**页眉形式：** 左侧 `$ project --report`，右侧 `v1.x.x · YYYY-MM-DD`，等宽风格

---

## 设计特征

- **终端绿**（#22c55e / #4ade80）作为主强调色，命令行美学
- 深炭黑背景，模拟 VS Code / Terminal 配色
- 等宽字体（Space Mono）显示代码、参数、版本号
- 卡片用绿色左侧边条，代码块风格边框
- 注释风格文字（灰色 `// comment`）装饰说明

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #0d1117; font-family: 'IBM Plex Sans','PingFang SC',sans-serif; color: #c9d1d9; }

/* 终端纹理（扫描线） */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: repeating-linear-gradient(
    0deg,
    rgba(34,197,94,0.012) 0px, rgba(34,197,94,0.012) 1px,
    transparent 1px, transparent 4px
  );
}

/* 展示标题（等宽终端风） */
.display-title {
  font-family: 'Space Mono',monospace;
  font-size: 34px; font-weight: 700;
  letter-spacing: -0.5px; line-height: 1.1;
  color: #4ade80;
  text-shadow: 0 0 20px rgba(74,222,128,0.2);
}
.display-title::before { content: '> '; color: rgba(74,222,128,0.4); }

/* 卡片（绿色左侧边条，代码块感） */
.card {
  background: rgba(13,17,23,0.95);
  border: 1px solid rgba(34,197,94,0.12);
  border-left: 3px solid #22c55e;
  border-radius: 4px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  font-family: 'IBM Plex Sans',sans-serif;
}

/* KPI 数字（等宽绿色） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 38px; font-weight: 700; line-height: 1; letter-spacing: -1px;
  color: #4ade80;
}

/* 代码注释标签 */
.comment-label {
  font-family: 'Space Mono',monospace;
  font-size: 9px; color: #6e7681;
  letter-spacing: 0;
}
.comment-label::before { content: '// '; }

/* 版本/状态徽章 */
.version-badge {
  display: inline-flex; align-items: center;
  background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25);
  border-radius: 4px; padding: 2px 7px;
  font-family: 'Space Mono',monospace; font-size: 8px;
  color: #4ade80; letter-spacing: 0;
}
.version-badge.warn { background:rgba(234,179,8,0.1); border-color:rgba(234,179,8,0.25); color:#fbbf24; }
.version-badge.err  { background:rgba(239,68,68,0.1); border-color:rgba(239,68,68,0.25); color:#f87171; }

/* 进度条（类似 npm install 进度） */
.cli-bar {
  height: 3px; background: rgba(34,197,94,0.1);
  border-radius: 0; font-family: monospace;
}
.cli-fill { height: 100%; background: linear-gradient(90deg, #16a34a, #4ade80); }

/* 数据行（终端输出风格） */
.cli-row {
  display: flex; gap: 8px; align-items: center;
  font-family: 'Space Mono',monospace; font-size: 9px;
  color: #8b949e; padding: 2px 0;
}
.cli-row .key  { color: #79c0ff; }
.cli-row .val  { color: #4ade80; margin-left: auto; }
.cli-row .sep  { color: #30363d; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0d1117;
  --card: #161b22;
  --p:    #22c55e;
  --pm:   rgba(34,197,94,0.1);
  --bd:   rgba(34,197,94,0.15);
  --t:    #c9d1d9;
  --mt:   #8b949e;
  --dt:   #484f58;
}
```
