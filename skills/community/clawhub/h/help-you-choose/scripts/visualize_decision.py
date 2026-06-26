#!/usr/bin/env python3
"""
Decision Visualization Generator
Generates an interactive HTML page with radar chart, weight sliders, and comparison matrix.

Usage:
  python visualize_decision.py --title "Where to live" \
    --dimensions '["收入","生活成本","生活质量","职业发展","社交"]' \
    --weights '[30,20,25,15,10]' \
    --options '{"北京":[9,3,5,9,7],"成都":[6,8,8,6,6],"深圳":[8,4,6,8,5]}' \
    --output decision_report.html
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>决策分析: {{TITLE}}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e1e4e8; padding: 24px; min-height: 100vh; }
  .container { max-width: 1200px; margin: 0 auto; }
  h1 { font-size: 28px; font-weight: 600; margin-bottom: 8px; color: #fff; }
  .subtitle { color: #8b949e; margin-bottom: 32px; font-size: 14px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 24px; }
  .card-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #c9d1d9; display: flex; align-items: center; gap: 8px; }
  .card-title::before { content: ''; display: inline-block; width: 4px; height: 16px; border-radius: 2px; background: #58a6ff; }
  .full-width { grid-column: 1 / -1; }
  .radar-container { display: flex; justify-content: center; padding: 16px 0; }
  svg text { font-size: 12px; fill: #8b949e; }
  svg .label-text { font-size: 13px; fill: #c9d1d9; font-weight: 500; }
  .slider-row { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
  .slider-label { width: 80px; font-size: 13px; color: #c9d1d9; text-align: right; flex-shrink: 0; }
  input[type="range"] { -webkit-appearance: none; width: 100%; height: 6px; border-radius: 3px; background: #30363d; outline: none; }
  input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%; background: #58a6ff; cursor: pointer; border: 2px solid #0d1117; }
  .slider-value { width: 48px; text-align: center; font-size: 14px; font-weight: 600; color: #58a6ff; flex-shrink: 0; }
  table { width: 100%; border-collapse: collapse; }
  th, td { padding: 12px 16px; text-align: center; border-bottom: 1px solid #21262d; font-size: 13px; }
  th { color: #8b949e; font-weight: 500; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
  th:first-child, td:first-child { text-align: left; color: #c9d1d9; font-weight: 500; }
  .score-cell { font-weight: 600; }
  .score-high { color: #3fb950; }
  .score-mid { color: #d29922; }
  .score-low { color: #f85149; }
  .total-row td { border-top: 2px solid #58a6ff; font-weight: 700; font-size: 15px; color: #fff; }
  .winner { background: rgba(56, 166, 255, 0.08); }
  .result-bar-container { margin-bottom: 14px; }
  .result-label { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 14px; }
  .result-name { color: #c9d1d9; font-weight: 500; }
  .result-score { color: #58a6ff; font-weight: 700; }
  .bar-bg { height: 24px; background: #21262d; border-radius: 6px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 6px; transition: width 0.5s ease; }
  .colors-0 { background: linear-gradient(90deg, #58a6ff, #388bfd); }
  .colors-1 { background: linear-gradient(90deg, #3fb950, #2ea043); }
  .colors-2 { background: linear-gradient(90deg, #d29922, #bb8009); }
  .colors-3 { background: linear-gradient(90deg, #f778ba, #db61a2); }
  .colors-4 { background: linear-gradient(90deg, #bc8cff, #a371f7); }
  .legend { display: flex; gap: 20px; justify-content: center; margin-top: 16px; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #8b949e; }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; }
  .table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
  @media (max-width: 768px) {
    body { padding: 12px; }
    h1 { font-size: 20px; }
    .subtitle { font-size: 12px; margin-bottom: 20px; }
    .grid { grid-template-columns: 1fr; gap: 16px; }
    .full-width { grid-column: auto; }
    .card { padding: 16px; }
    .radar-container svg { width: 100%; height: auto; }
    .slider-label { width: 60px; font-size: 12px; }
    .slider-value { width: 40px; font-size: 12px; }
    input[type="range"]::-webkit-slider-thumb { width: 24px; height: 24px; }
    th, td { padding: 8px 6px; font-size: 12px; white-space: nowrap; }
  }
</style>
</head>
<body>
<div class="container">
  <h1>决策分析: {{TITLE}}</h1>
  <p class="subtitle">生成时间: {{TIMESTAMP}} | 拖动权重滑块可实时查看结果变化</p>
  <div class="grid">
    <div class="card">
      <div class="card-title">雷达图对比</div>
      <div class="radar-container"><svg id="radar" width="400" height="400" viewBox="0 0 400 400"></svg></div>
      <div class="legend" id="legend"></div>
    </div>
    <div class="card">
      <div class="card-title">维度权重调整</div>
      <div id="sliders"></div>
      <div style="margin-top: 20px;">
        <div class="card-title">加权总分</div>
        <div id="result-bars"></div>
      </div>
    </div>
    <div class="card full-width">
      <div class="card-title">对比矩阵</div>
      <div class="table-wrap"><table id="matrix"></table></div>
    </div>
  </div>
</div>
<script>
const DATA = {
  title: {{TITLE_JSON}},
  dimensions: {{DIMS_JSON}},
  weights: {{WEIGHTS_JSON}},
  options: {{OPTIONS_JSON}}
};
const COLORS = ['#58a6ff','#3fb950','#d29922','#f778ba','#bc8cff'];
const optionNames = Object.keys(DATA.options);
let weights = [...DATA.weights];

function renderLegend() {
  document.getElementById('legend').innerHTML = optionNames.map((name, i) =>
    '<div class="legend-item"><div class="legend-dot" style="background:'+COLORS[i%5]+'"></div>'+name+'</div>'
  ).join('');
}

function drawRadar() {
  const svg = document.getElementById('radar');
  const cx = 200, cy = 200, R = 150;
  const n = DATA.dimensions.length;
  const angles = DATA.dimensions.map((_, i) => (Math.PI * 2 * i / n) - Math.PI / 2);
  let html = '';
  for (let r = 1; r <= 5; r++) {
    const radius = R * r / 5;
    html += '<circle cx="'+cx+'" cy="'+cy+'" r="'+radius+'" fill="none" stroke="#21262d" stroke-width="1"/>';
  }
  angles.forEach((a, i) => {
    const x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
    html += '<line x1="'+cx+'" y1="'+cy+'" x2="'+x+'" y2="'+y+'" stroke="#21262d" stroke-width="1"/>';
    const lx = cx + (R + 24) * Math.cos(a), ly = cy + (R + 24) * Math.sin(a);
    html += '<text x="'+lx+'" y="'+ly+'" text-anchor="middle" dominant-baseline="middle" class="label-text">'+DATA.dimensions[i]+'</text>';
  });
  optionNames.forEach((name, oi) => {
    const scores = DATA.options[name];
    const points = scores.map((s, i) => {
      const r = R * s / 10;
      return (cx + r * Math.cos(angles[i]))+','+(cy + r * Math.sin(angles[i]));
    }).join(' ');
    html += '<polygon points="'+points+'" fill="'+COLORS[oi%5]+'22" stroke="'+COLORS[oi%5]+'" stroke-width="2"/>';
    scores.forEach((s, i) => {
      const r = R * s / 10;
      html += '<circle cx="'+(cx + r * Math.cos(angles[i]))+'" cy="'+(cy + r * Math.sin(angles[i]))+'" r="4" fill="'+COLORS[oi%5]+'"/>';
    });
  });
  svg.innerHTML = html;
}

function renderSliders() {
  document.getElementById('sliders').innerHTML = DATA.dimensions.map((dim, i) =>
    '<div class="slider-row"><span class="slider-label">'+dim+'</span><div style="flex:1"><input type="range" min="0" max="100" value="'+weights[i]+'" oninput="onW('+i+',this.value)"></div><span class="slider-value" id="wv-'+i+'">'+weights[i]+'%</span></div>'
  ).join('');
}

function onW(idx, val) {
  weights[idx] = parseInt(val);
  document.getElementById('wv-'+idx).textContent = val + '%';
  renderResults();
  renderMatrix();
}

function calcScores() {
  const totalW = weights.reduce((a, b) => a + b, 0) || 1;
  return optionNames.map(name => {
    const scores = DATA.options[name];
    const weighted = scores.reduce((sum, s, i) => sum + s * weights[i], 0) / totalW;
    return { name, score: Math.round(weighted * 100) / 100 };
  });
}

function renderResults() {
  const results = calcScores();
  document.getElementById('result-bars').innerHTML = results.map((r, i) =>
    '<div class="result-bar-container"><div class="result-label"><span class="result-name">'+r.name+'</span><span class="result-score">'+r.score.toFixed(2)+'</span></div><div class="bar-bg"><div class="bar-fill colors-'+i%5+'" style="width:'+(r.score/10*100).toFixed(1)+'%"></div></div></div>'
  ).join('');
}

function renderMatrix() {
  const results = calcScores();
  const maxTotal = Math.max(...results.map(r => r.score));
  let html = '<thead><tr><th>维度 / 权重</th>';
  optionNames.forEach(n => html += '<th>'+n+'</th>');
  html += '</tr></thead><tbody>';
  DATA.dimensions.forEach((dim, di) => {
    html += '<tr><td>'+dim+' ('+weights[di]+'%)</td>';
    const rowScores = optionNames.map(n => DATA.options[n][di]);
    const maxInRow = Math.max(...rowScores);
    optionNames.forEach(name => {
      const s = DATA.options[name][di];
      const cls = s >= 8 ? 'score-high' : s >= 5 ? 'score-mid' : 'score-low';
      const bold = s === maxInRow ? 'font-weight:800;' : '';
      html += '<td class="score-cell '+cls+'" style="'+bold+'">'+s+'</td>';
    });
    html += '</tr>';
  });
  html += '<tr class="total-row"><td>加权总分</td>';
  results.forEach(r => {
    html += '<td class="'+(r.score === maxTotal ? 'winner' : '')+'">'+r.score.toFixed(2)+'</td>';
  });
  html += '</tr></tbody>';
  document.getElementById('matrix').innerHTML = html;
}

renderLegend(); drawRadar(); renderSliders(); renderResults(); renderMatrix();
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate interactive decision visualization")
    parser.add_argument("--title", required=True, help="Decision title")
    parser.add_argument("--dimensions", required=True, help='JSON array of dimension names')
    parser.add_argument("--weights", required=True, help='JSON array of weights (integers)')
    parser.add_argument("--options", required=True, help='JSON object: {"name": [score1, score2, ...]}')
    parser.add_argument("--output", default=None, help="Output HTML file path")
    args = parser.parse_args()

    dims = json.loads(args.dimensions)
    weights = json.loads(args.weights)
    options = json.loads(args.options)

    n = len(dims)
    assert len(weights) == n, f"Weights count ({len(weights)}) must match dimensions count ({n})"
    for name, scores in options.items():
        assert len(scores) == n, f"Option '{name}' has {len(scores)} scores, expected {n}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = HTML_TEMPLATE
    html = html.replace("{{TITLE}}", args.title)
    html = html.replace("{{TITLE_JSON}}", json.dumps(args.title, ensure_ascii=False))
    html = html.replace("{{TIMESTAMP}}", timestamp)
    html = html.replace("{{DIMS_JSON}}", json.dumps(dims, ensure_ascii=False))
    html = html.replace("{{WEIGHTS_JSON}}", json.dumps(weights))
    html = html.replace("{{OPTIONS_JSON}}", json.dumps(options, ensure_ascii=False))

    output_path = args.output or f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Visualization generated: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
