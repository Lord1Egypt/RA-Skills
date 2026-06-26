# 终端代码（Terminal Code Audit）

**气质：** 技术极客、审计报告、真实感、开发者专属
**适用：** 技术实现、工具框架、检测评估、漏洞分析
**推荐字体：** FP-3（Space Mono + IBM Plex Sans）
**背景类型：** 暗色系，固定使用 GitHub Dark 色板，不与主题配色混用
**主标题字号：** 无大展示标题，以路径+命令行格式替代
**页眉形式：** terminal-bar（32px）+ 路径命令行

---

## 四区特殊调整

> ⚠ 此风格四区高度与标准不同，必须按此分配：

```
terminal-bar  32px
hd            40px
ct           608px
ft            40px
─────────────
总计          720px ✓
```

---

## CSS 片段

```css
body { background: #0d1117; font-family: 'Space Mono','Courier New',monospace; color: #c9d1d9; }

/* 扫描线 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:100;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px,
    rgba(0,255,65,0.012) 2px, rgba(0,255,65,0.012) 4px);
}

/* 细网格 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* Terminal 标题栏 */
.terminal-bar {
  height: 32px; background: #161b22; border-bottom: 1px solid #30363d;
  display: flex; align-items: center; padding: 0 16px; gap: 8px; flex-shrink: 0;
}
.term-dot { width:10px; height:10px; border-radius:50%; }
/* #ff5f57 红  #febc2e 黄  #28c840 绿 */

/* 代码卡片 */
.code-card { background: #161b22; border: 1px solid #30363d; border-radius: 6px; overflow:hidden; }
.code-card-header { background: #21262d; padding: 6px 12px; border-bottom: 1px solid #30363d; display:flex; align-items:center; gap:8px; }
.code-body { padding: 10px 12px; font-family: 'Space Mono',monospace; font-size: 10.5px; }
.line { line-height: 1.6; white-space: nowrap; overflow: hidden; }
.ln   { color:#484f58; width:24px; display:inline-block; text-align:right; margin-right:12px; user-select:none; }

/* 语法高亮 */
.kw { color: #ff7b72; } .fn { color: #d2a8ff; } .st { color: #a5d6ff; }
.nm { color: #79c0ff; } .cm { color: #8b949e; } .vr { color: #ffa657; }

/* 状态徽章 */
.badge-ok   { background:rgba(63,185,80,.15);  color:#3fb950; border:1px solid rgba(63,185,80,.3);  }
.badge-warn { background:rgba(210,153,34,.15); color:#d29922; border:1px solid rgba(210,153,34,.3); }
.badge-err  { background:rgba(248,81,73,.15);  color:#f85149; border:1px solid rgba(248,81,73,.3);  }
.badge-info { background:rgba(88,166,255,.15); color:#58a6ff; border:1px solid rgba(88,166,255,.3); }
.badge-term { padding:1px 6px; border-radius:3px; font-size:9px; font-family:monospace; font-weight:600; }

/* 终端输出色 */
.t-ok { color:#3fb950; } .t-warn { color:#d29922; } .t-err { color:#f85149; }
.t-info { color:#58a6ff; } .t-dim { color:#8b949e; }
```

---

## GitHub Dark 固定色板

```css
--term-bg:      #0d1117;   --term-surface: #161b22;
--term-header:  #21262d;   --term-border:  #30363d;
--term-text:    #c9d1d9;   --term-dim:     #8b949e;
--term-muted:   #484f58;
```
