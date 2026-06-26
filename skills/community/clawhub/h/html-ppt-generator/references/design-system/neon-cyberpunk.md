# 霓虹赛博（Neon Cyberpunk）

**气质：** 高饱和、夜间城市、未来感、极度视觉冲击
**适用：** 威胁情报、攻击溯源、黑产分析、极客演讲
**推荐字体：** FP-5（Bebas Neue + Barlow）或 FP-1（Syne + DM Sans）+ 辉光叠加
**背景类型：** 极暗色 `#080010`，霓虹色高对比
**主标题字号：** 28–40px，霓虹辉光 text-shadow
**页眉形式：** 赛博路径格式（`root@host:~/path$`）+ 闪烁光标

> ⚠ 每份报告建议不超过 **2 页**，避免视觉疲劳。

---

## CSS 片段

```css
body { background: #080010; color: #e0e0ff; font-family: 'Courier New', monospace; }

/* 霓虹辉光文字 */
.neon-glow-pink   { text-shadow: 0 0 8px #ff2d78, 0 0 20px rgba(255,45,120,0.4);  color: #ff2d78; }
.neon-glow-cyan   { text-shadow: 0 0 8px #00ffe7, 0 0 20px rgba(0,255,231,0.4);   color: #00ffe7; }
.neon-glow-purple { text-shadow: 0 0 8px #bf5fff, 0 0 20px rgba(191,95,255,0.4);  color: #bf5fff; }
.neon-glow-green  { text-shadow: 0 0 8px #39ff14, 0 0 20px rgba(57,255,20,0.4);   color: #39ff14; }

/* 赛博卡片 */
.cyber-card {
  background: rgba(10,0,30,0.85);
  border: 1px solid NEON_COLOR;
  box-shadow: 0 0 12px rgba(NEON_R,NEON_G,NEON_B,0.25), inset 0 0 20px rgba(0,0,0,0.5);
  border-radius: 4px; padding: 14px 16px;
}

/* 扫描线 */
.scan-lines {
  position:fixed; inset:0; pointer-events:none; z-index:100;
  background: repeating-linear-gradient(0deg, transparent, transparent 3px,
    rgba(0,0,0,0.15) 3px, rgba(0,0,0,0.15) 4px);
}

/* 闪烁光标 */
.cursor::after { content:'█'; animation: blink 1s step-end infinite; color: inherit; }
@keyframes blink { 50% { opacity: 0; } }

/* 赛博路径页眉 */
.cyber-path { font-family:'Courier New',monospace; font-size:10px; color:#39ff14; }
.cyber-path .prompt { color: #bf5fff; }
.cyber-path .path   { color: #00ffe7; }

/* 数字矩阵背景（可选）*/
.matrix-bg {
  position:absolute; inset:0; pointer-events:none; z-index:0; overflow:hidden;
  font-family:monospace; font-size:11px; color:rgba(57,255,20,0.04);
  white-space:pre; line-height:1.4; word-break:break-all;
}
```
