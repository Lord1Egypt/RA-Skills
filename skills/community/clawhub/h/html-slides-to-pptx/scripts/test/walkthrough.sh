#!/bin/bash
# walkthrough.sh — 端到端工作流走查(SKILL.md Step 2→5 的可执行版本)
# 在临时目录搭一套幻灯片项目:theme.css + 片段/方式 C 组合页面 + playlist,
# 跑 validate(须 0 ERROR)与 convert(须产出 pptx)。任一步失败即非零退出。
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="$(mktemp -d)/walkthrough"
trap 'rm -rf "$(dirname "$WORK")"' EXIT

# ---- Step 2 · 搭目录结构 ----
mkdir -p "$WORK/assets" "$WORK/slides"
cp "$SKILL_DIR/assets/theme.css" "$WORK/assets/theme.css"
cat > "$WORK/slides/playlist.json" <<'JSON'
{ "playlist": ["01-demo.html"] }
JSON

# ---- Step 3 · 写页面(页头片段 + grid 统计带 + stack 横条目 + 渐变条片段) ----
cat > "$WORK/slides/01-demo.html" <<'HTML'
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>走查演示页</title>
<link rel="stylesheet" href="../assets/theme.css">
</head>
<body>
<div class="slide-container" style="background:var(--off-white);">

  <!-- 页头(page-header 片段,参数已替换) -->
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:60px;width:80px;height:4px;background:var(--lenovo-red);z-index:10;"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:88px;width:1000px;z-index:10;">
    <div style="font-size:20px;font-weight:600;letter-spacing:4px;color:var(--lenovo-red);">端到端走查</div>
  </div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:1720px;top:92px;width:100px;text-align:right;z-index:10;">
    <div class="num" style="font-size:18px;font-weight:600;color:var(--text-tertiary);letter-spacing:2px;">01 / 01</div>
  </div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;z-index:10;">
    <div style="font-size:56px;font-weight:700;line-height:1.15;color:var(--charcoal);letter-spacing:-0.5px;">片段 + <span style="color:var(--lenovo-red);">data-layout</span> 组合页</div>
  </div>

  <!-- 统计带(方式 C:grid × stat-number 片段) -->
  <div data-layout="grid" data-layout-cols="4" data-layout-gap="20" style="position:absolute;left:100px;top:280px;width:1720px;">
    <div data-object="true" data-layout-h="160" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;">
      <div class="num" style="font-size:44px;font-weight:800;color:var(--lenovo-red);line-height:1.1;">87<span style="font-size:22px;font-weight:600;">%</span></div>
      <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:8px;">完成率</div>
    </div>
    <div data-object="true" data-layout-h="160" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;">
      <div class="num" style="font-size:44px;font-weight:800;color:var(--deep-navy);line-height:1.1;">3.2<span style="font-size:22px;font-weight:600;">倍</span></div>
      <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:8px;">效率提升</div>
    </div>
    <div data-object="true" data-layout-h="160" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;">
      <div class="num" style="font-size:44px;font-weight:800;color:var(--signal-green);line-height:1.1;">+42<span style="font-size:22px;font-weight:600;">pp</span></div>
      <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:8px;">满意度变化</div>
    </div>
    <div data-object="true" data-layout-h="160" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;">
      <div class="num" style="font-size:44px;font-weight:800;color:var(--charcoal);line-height:1.1;">12<span style="font-size:22px;font-weight:600;">项</span></div>
      <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:8px;">落地举措</div>
    </div>
  </div>

  <!-- 横条目(方式 C:stack × layer-row 片段结构) -->
  <div data-layout="stack" data-layout-gap="20" style="position:absolute;left:100px;top:500px;width:1720px;">
    <div data-object="true" data-layout-h="110" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:0 28px;display:flex;align-items:center;gap:24px;">
      <div style="width:64px;height:64px;background:var(--lenovo-red);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:#FFFFFF;">1</div>
      <div style="flex:1;">
        <div style="font-size:24px;font-weight:700;line-height:1.3;color:var(--charcoal);">第一步行</div>
        <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:4px;">条目说明文字</div>
      </div>
    </div>
    <div data-object="true" data-layout-h="110" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:0 28px;display:flex;align-items:center;gap:24px;">
      <div style="width:64px;height:64px;background:var(--deep-navy);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:#FFFFFF;">2</div>
      <div style="flex:1;">
        <div style="font-size:24px;font-weight:700;line-height:1.3;color:var(--charcoal);">第二步</div>
        <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:4px;">条目说明文字</div>
      </div>
    </div>
  </div>

  <!-- 渐变横条(gradient-bar 片段,参数已替换) -->
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:800px;width:1720px;height:80px;background:linear-gradient(90deg, var(--deep-navy) 0%, var(--deep-navy-light) 100%);border-radius:8px;z-index:5;"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:800px;width:1720px;height:80px;text-align:center;z-index:11;">
    <div style="font-size:22px;font-weight:600;color:var(--on-navy-text);line-height:80px;letter-spacing:2px;">结论横条,<span style="color:var(--accent-orange);font-weight:800;">关键句橙色高亮</span></div>
  </div>

</div>
<template data-slide-notes>端到端走查页:页头片段 + grid 统计带 + stack 条目 + 渐变条。</template>
</body>
</html>
HTML

# ---- Step 4 · 预检(必须零 ERROR) ----
echo "── validate ──"
node "$SKILL_DIR/scripts/validate.js" "$WORK/slides/"
[ $? -eq 0 ] || { echo "❌ validate 未过"; exit 1; }

# ---- Step 5 · 转换 ----
echo "── convert ──"
node "$SKILL_DIR/scripts/convert.js" "$WORK/slides" "$WORK/slides/playlist.json" "$WORK/output.pptx"
[ -s "$WORK/output.pptx" ] || { echo "❌ 未产出 pptx"; exit 1; }

echo "✅ 走查通过: $WORK/output.pptx ($(stat -f%z "$WORK/output.pptx") bytes)"
