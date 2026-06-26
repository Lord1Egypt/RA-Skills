# raci · RACI 矩阵

**适用：** 任务分配、职责边界、项目角色矩阵、协作规范
**高度：** 自适应（行数 × 约 28px + 表头 36px）

**结构公式：** HTML table 实现（比 SVG 更清晰），每格用彩色角标显示 R/A/C/I。

```html
<!-- RACI 矩阵（HTML table，比 SVG 更清晰） -->
<div style="overflow:hidden;font-size:10px;">
  <table style="width:100%;border-collapse:collapse;">
    <thead>
      <tr style="background:var(--card);">
        <th style="padding:5px 8px;text-align:left;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);width:200px;">任务/交付物</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">产品</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">研发</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">测试</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">运营</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
        <td style="padding:5px 8px;color:var(--t);">需求文档</td>
        <td style="text-align:center;"><span style="background:rgba(239,68,68,0.15);color:#ef4444;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">A</span></td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
        <td style="text-align:center;"><span style="background:rgba(148,163,184,0.1);color:#94a3b8;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">I</span></td>
        <td style="text-align:center;"><span style="background:rgba(16,185,129,0.15);color:#10b981;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">R</span></td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
        <td style="padding:5px 8px;color:var(--t);">功能开发</td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
        <td style="text-align:center;"><span style="background:rgba(16,185,129,0.15);color:#10b981;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">R</span></td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
        <td style="text-align:center;"><span style="background:rgba(148,163,184,0.1);color:#94a3b8;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">I</span></td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
        <td style="padding:5px 8px;color:var(--t);">测试验收</td>
        <td style="text-align:center;"><span style="background:rgba(239,68,68,0.15);color:#ef4444;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">A</span></td>
        <td style="text-align:center;"><span style="background:rgba(148,163,184,0.1);color:#94a3b8;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">I</span></td>
        <td style="text-align:center;"><span style="background:rgba(16,185,129,0.15);color:#10b981;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">R</span></td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
      </tr>
    </tbody>
  </table>
  <!-- 图例 -->
  <div style="display:flex;gap:12px;margin-top:5px;font-size:8.5px;">
    <span style="color:#10b981;"><b>R</b> Responsible 执行</span>
    <span style="color:#ef4444;"><b>A</b> Accountable 决策</span>
    <span style="color:#3b82f6;"><b>C</b> Consulted 咨询</span>
    <span style="color:#94a3b8;"><b>I</b> Informed 知会</span>
  </div>
</div>
```

**参数说明：**
- 任务列宽 200px；角色列等宽自适应
- 每个角标：彩色背景 badge（border-radius:3px，padding:2px 7px），font-size:9px
- 颜色编码：R=绿(#10b981)，A=红(#ef4444)，C=蓝(#3b82f6)，I=灰(#94a3b8)
- 同一行可出现多个 R（多人共同执行），但 A 每行至多 1 个（单一决策方）
- 行数超过 5 行时建议减小 padding 至 `3px 6px` 控制高度
