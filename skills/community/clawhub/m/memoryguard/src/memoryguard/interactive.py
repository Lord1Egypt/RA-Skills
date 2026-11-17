"""MemoryGuard 交互式本地治理面板。

界面通过 pywebview JS API 调用本地 Python 后端，完成只读审计、
记忆神经图浏览、人工治理、修复计划、应用与撤销。
"""

from __future__ import annotations


def render_interactive_html() -> str:
    """返回自包含 CSS/JS 的交互式治理面板 HTML。"""
    return _HTML_TEMPLATE


_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MemoryGuard · 本地记忆治理</title>
<script src="cytoscape.min.js"></script>
<style>
:root {
  color-scheme: dark;
  --bg: #040b09;
  --bg-raised: #08120f;
  --panel: rgba(10, 25, 21, 0.86);
  --panel-solid: #0b1a16;
  --panel-bright: #10251f;
  --fg: #e4f5ef;
  --muted: #78988d;
  --faint: #48685e;
  --line: rgba(110, 231, 196, 0.16);
  --line-strong: rgba(110, 231, 196, 0.34);
  --accent: #6ee7c4;
  --accent-bright: #bcffeb;
  --accent-soft: rgba(110, 231, 196, 0.10);
  --red: #ff7d88;
  --orange: #e9bb64;
  --green: #6ee7c4;
  --blue: #6ee7c4;
  --purple: #9be8d4;
  --shadow: 0 24px 70px rgba(0, 0, 0, 0.32);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  position: relative; overflow: hidden; display: flex; flex-direction: column;
  background:
    radial-gradient(circle at 14% 12%, rgba(48, 170, 133, 0.10), transparent 30rem),
    radial-gradient(circle at 84% 82%, rgba(78, 150, 125, 0.07), transparent 34rem),
    var(--bg);
  color: var(--fg);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.55;
}
body::before {
  content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .42;
  background-image:
    linear-gradient(var(--line) 1px, transparent 1px),
    linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(circle at center, black 0, transparent 78%);
}
button, input, select { font: inherit; }
button:focus-visible, [role="tab"]:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
code {
  padding: .15em .4em; border: 1px solid var(--line); border-radius: 5px;
  background: rgba(110, 231, 196, .06); color: #b9d8ce; font-size: .88em;
  overflow-wrap: anywhere;
}
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: rgba(110, 231, 196, .22); border-radius: 8px; }
::-webkit-scrollbar-track { background: transparent; }

/* 顶部：品牌本身就是一个活跃神经元 */
.header {
  position: relative; z-index: 10; min-height: 72px; padding: 0 28px;
  display: flex; align-items: center; justify-content: space-between; gap: 24px;
  border-bottom: 1px solid var(--line); background: rgba(4, 11, 9, .80);
  backdrop-filter: blur(20px);
}
.header-left, .header-right, .brand { display: flex; align-items: center; }
.header-left { gap: 20px; min-width: 0; }
.header-right { gap: 12px; flex: none; }
.brand { gap: 12px; }
.brand-orb {
  position: relative; width: 28px; height: 28px; flex: none; border-radius: 50%;
  border: 1px solid rgba(188, 255, 235, .74);
  background: radial-gradient(circle at 38% 34%, #e4fff7 0 6%, var(--accent) 8% 19%, #163d33 44%, #07120f 72%);
  box-shadow: 0 0 20px rgba(110, 231, 196, .35), inset 0 0 12px rgba(110, 231, 196, .38);
}
.brand-orb::before, .brand-orb::after {
  content: ""; position: absolute; top: 50%; left: 50%; height: 1px;
  transform-origin: left; background: linear-gradient(90deg, var(--accent), transparent);
}
.brand-orb::before { width: 18px; transform: rotate(35deg); }
.brand-orb::after { width: 15px; transform: rotate(150deg); }
.brand-copy strong { display: block; font-size: 15px; letter-spacing: .06em; }
.brand-copy span { display: block; color: var(--muted); font-size: 10px; letter-spacing: .18em; text-transform: uppercase; }
.ws-path {
  max-width: min(42vw, 620px); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  color: var(--muted); font-size: 12px;
}
.health-badge {
  display: inline-flex; align-items: center; gap: 7px; padding: 6px 10px;
  color: var(--fg); border: 1px solid var(--line); border-radius: 999px;
  background: rgba(110, 231, 196, .06); font-size: 12px; font-weight: 600;
}
.health-badge::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: currentColor; box-shadow: 0 0 10px currentColor; }
.btn {
  min-height: 34px; padding: 7px 13px; border: 1px solid var(--line-strong); border-radius: 8px;
  background: rgba(110, 231, 196, .04); color: var(--fg); cursor: pointer; font-size: 12px;
  transition: transform .16s ease, border-color .16s ease, background .16s ease, box-shadow .16s ease;
}
.btn:hover { transform: translateY(-1px); border-color: rgba(110, 231, 196, .62); background: rgba(110, 231, 196, .09); }
.btn:active { transform: translateY(0); }
.btn-primary { border-color: var(--accent); background: var(--accent); color: #062019; font-weight: 700; box-shadow: 0 0 18px rgba(110, 231, 196, .12); }
.btn-primary:hover { background: var(--accent-bright); box-shadow: 0 0 24px rgba(110, 231, 196, .22); }
.btn-danger { border-color: rgba(255, 125, 136, .48); color: var(--red); }
.btn-danger:hover { border-color: var(--red); background: rgba(255, 125, 136, .08); }
.btn-icon { min-width: 32px; padding: 5px 8px; }
.btn:disabled { opacity: .38; cursor: not-allowed; transform: none; }

/* Tab 是一条突触链，不使用胶囊导航 */
.tab-bar {
  position: relative; z-index: 9; min-height: 50px; padding: 0 28px;
  display: flex; align-items: stretch; gap: 28px; border-bottom: 1px solid var(--line);
  background: rgba(4, 11, 9, .64); backdrop-filter: blur(14px);
}
.tab {
  position: relative; display: flex; align-items: center; gap: 8px; padding: 0 2px;
  color: var(--muted); cursor: pointer; font-size: 12px; letter-spacing: .03em;
  transition: color .18s ease;
}
.tab::before { content: ""; width: 5px; height: 5px; border: 1px solid var(--faint); border-radius: 50%; transition: all .18s ease; }
.tab::after { content: ""; position: absolute; left: 0; right: 0; bottom: -1px; height: 1px; background: transparent; }
.tab:hover { color: var(--fg); }
.tab.active { color: var(--accent-bright); }
.tab.active::before { border-color: var(--accent); background: var(--accent); box-shadow: 0 0 12px var(--accent); }
.tab.active::after { background: linear-gradient(90deg, transparent, var(--accent), transparent); box-shadow: 0 0 12px var(--accent); }
.tab .count { min-width: 18px; color: var(--faint); font-size: 10px; }

.content {
  position: relative; z-index: 1; flex: 1; width: 100%; max-width: 1540px; margin: 0 auto;
  overflow: auto; padding: 26px 28px 38px;
}
.view-heading { margin-bottom: 18px; }
.eyebrow { color: var(--accent); font-size: 10px; letter-spacing: .18em; text-transform: uppercase; }
.view-heading h2 { margin-top: 4px; font-size: 24px; font-weight: 560; letter-spacing: -.03em; }
.view-heading p { max-width: 720px; margin-top: 5px; color: var(--muted); font-size: 13px; }
.card {
  position: relative; overflow: hidden; padding: 20px; margin-bottom: 14px;
  border: 1px solid var(--line); border-radius: 14px;
  background: linear-gradient(145deg, rgba(15, 35, 29, .82), rgba(7, 18, 15, .78));
  box-shadow: 0 18px 50px rgba(0, 0, 0, .10);
}
.card::before { content: ""; position: absolute; top: -2px; left: 22px; width: 5px; height: 5px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 12px var(--accent); }
.card h2 { margin-bottom: 14px; font-size: 13px; font-weight: 650; letter-spacing: .04em; }
.card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
.card-head h2 { margin: 0; }
.card-head p { color: var(--muted); font-size: 12px; }

/* 总览 */
.overview-hero { display: grid; grid-template-columns: minmax(220px, .75fr) minmax(0, 2fr); gap: 14px; margin-bottom: 14px; }
.health-orbit { min-height: 238px; display: grid; place-items: center; }
.health-ring {
  --health-angle: 0deg; position: relative; width: 164px; height: 164px; display: grid; place-items: center;
  border-radius: 50%; background: conic-gradient(var(--accent) var(--health-angle), rgba(110, 231, 196, .08) 0);
  box-shadow: 0 0 40px rgba(110, 231, 196, .08);
}
.health-ring::before { content: ""; position: absolute; inset: 10px; border-radius: 50%; background: radial-gradient(circle, #10251f, #07120f 72%); border: 1px solid var(--line); }
.health-ring::after { content: ""; position: absolute; inset: -8px; border: 1px dashed rgba(110, 231, 196, .20); border-radius: 50%; }
.health-ring-content { position: relative; z-index: 1; text-align: center; }
.health-ring-content strong { display: block; color: var(--accent-bright); font-size: 44px; font-weight: 530; line-height: 1; letter-spacing: -.05em; }
.health-ring-content span { color: var(--muted); font-size: 11px; letter-spacing: .14em; }
.metrics { display: grid; grid-template-columns: repeat(2, minmax(130px, 1fr)); gap: 10px; }
.metric {
  position: relative; min-height: 112px; padding: 18px; overflow: hidden;
  border: 1px solid var(--line); border-radius: 11px; background: rgba(110, 231, 196, .035);
}
.metric::after { content: ""; position: absolute; right: -12px; bottom: -12px; width: 58px; height: 58px; border: 1px solid var(--line); border-radius: 50%; box-shadow: 0 0 24px rgba(110, 231, 196, .05); }
.metric .num { color: var(--accent-bright); font-size: 30px; font-weight: 530; line-height: 1.2; letter-spacing: -.04em; }
.metric .label, .metric > div:last-child { margin-top: 8px; color: var(--muted); font-size: 11px; }
.overview-grid { display: grid; grid-template-columns: 1.3fr .7fr; gap: 14px; }
.scan-list { display: grid; gap: 10px; }
.scan-row { display: flex; justify-content: space-between; gap: 16px; padding-bottom: 9px; border-bottom: 1px solid var(--line); color: var(--muted); font-size: 12px; }
.scan-row:last-child { border-bottom: 0; padding-bottom: 0; }
.scan-row strong { color: var(--fg); font-weight: 500; text-align: right; }

/* 状态与列表 */
.chips { display: flex; flex-wrap: wrap; gap: 7px; }
.chip {
  display: inline-flex; align-items: center; gap: 6px; padding: 3px 8px;
  border: 1px solid var(--line); border-radius: 999px; color: var(--muted); background: rgba(255,255,255,.018);
  font-size: 10px; line-height: 1.5;
}
.chip::before { content: ""; width: 4px; height: 4px; border-radius: 50%; background: currentColor; box-shadow: 0 0 7px currentColor; }
.chip-critical, .chip-high { color: var(--red); border-color: rgba(255,125,136,.28); }
.chip-medium { color: var(--orange); border-color: rgba(233,187,100,.28); }
.chip-low, .chip-confirmed { color: var(--accent); }
.chip-info, .chip-tentative { color: #9fc4b8; }
.finding-item, .plan-item {
  position: relative; padding: 15px 16px 15px 22px; margin-bottom: 9px; cursor: pointer;
  border: 1px solid var(--line); border-radius: 11px; background: rgba(10, 26, 21, .70);
  transition: border-color .16s ease, background .16s ease, transform .16s ease;
}
.finding-item::before, .plan-item::before { content: ""; position: absolute; top: 21px; left: 10px; width: 4px; height: 4px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 8px var(--accent); }
.finding-item:hover { transform: translateX(2px); border-color: var(--line-strong); background: rgba(16, 39, 32, .72); }
.finding-item.sev-high::before, .finding-item.sev-critical::before, .plan-item.failed::before { background: var(--red); box-shadow: 0 0 8px var(--red); }
.finding-item.sev-medium::before { background: var(--orange); box-shadow: 0 0 8px var(--orange); }
.finding-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.finding-rule { font-size: 12px; font-weight: 650; }
.finding-evidence { margin-top: 6px; color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }
.finding-detail { margin-top: 12px; padding: 12px 0 0; border-top: 1px solid var(--line); font-size: 12px; }
.row { display: flex; align-items: flex-start; gap: 10px; margin: 5px 0; }
.key { min-width: 72px; color: var(--muted); }
.finding-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.empty-state { min-height: 210px; display: grid; place-items: center; text-align: center; color: var(--muted); }
.empty-state .empty-orb { width: 44px; height: 44px; margin: 0 auto 14px; border: 1px solid var(--line-strong); border-radius: 50%; box-shadow: 0 0 24px rgba(110,231,196,.10), inset 0 0 18px rgba(110,231,196,.06); }

/* 对象表 */
.table-shell { overflow: auto; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th, td { padding: 11px 12px; text-align: left; vertical-align: top; border-bottom: 1px solid var(--line); }
th { color: var(--muted); font-size: 10px; font-weight: 600; letter-spacing: .10em; text-transform: uppercase; }
tbody tr { transition: background .15s ease; }
tbody tr:hover { background: rgba(110, 231, 196, .035); }
tbody tr:last-child td { border-bottom: 0; }
.filter-bar { display: flex; gap: 8px; margin-bottom: 14px; }
.scope-tabs {
  display: flex; gap: 4px; padding: 4px; margin-bottom: 16px;
  border: 1px solid var(--line); border-radius: 10px;
  background: rgba(10, 26, 21, .50);
}
.scope-tab {
  flex: 1; padding: 8px 14px; border-radius: 7px; text-align: center;
  color: var(--muted); cursor: pointer; font-size: 12px; letter-spacing: .04em;
  transition: all .16s ease;
}
.scope-tab:hover { color: var(--fg); background: rgba(110, 231, 196, .05); }
.scope-tab.active {
  color: var(--accent-bright); background: rgba(110, 231, 196, .12);
  box-shadow: inset 0 0 0 1px rgba(110, 231, 196, .35);
}
.scope-tab .count { display: inline-block; min-width: 18px; margin-left: 6px;
  padding: 1px 6px; border-radius: 999px; background: rgba(110, 231, 196, .12);
  color: var(--accent); font-size: 10px; }
.surface-row {
  display: grid; grid-template-columns: auto 1fr auto auto auto; gap: 10px; align-items: center;
  padding: 10px 12px; margin-bottom: 6px;
  border: 1px solid var(--line); border-radius: 9px;
  background: rgba(10, 26, 21, .50); transition: border-color .15s ease;
}
.surface-row:hover { border-color: var(--line-strong); }
.surface-row .surface-icon { width: 8px; height: 8px; border-radius: 50%; flex: none; }
.surface-row .surface-icon.found { background: var(--accent); box-shadow: 0 0 8px var(--accent); }
.surface-row .surface-icon.missing { background: var(--faint); }
.surface-row .surface-icon.unsupported { background: var(--orange); }
.surface-row .surface-icon.permission_denied { background: var(--red); }
.surface-row .surface-path { font-size: 12px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.surface-row .surface-path code { font-size: 11px; }
.surface-row .surface-meta { font-size: 10px; color: var(--muted); letter-spacing: .04em; }
 /* v3.2 Agent 卡片 */
 .agent-cards {
   display: flex; gap: 8px; padding: 8px 0; margin-bottom: 16px;
   overflow-x: auto; flex-wrap: wrap;
 }
 .agent-card {
   flex: none; padding: 12px 16px; border: 1px solid var(--line); border-radius: 12px;
   background: rgba(10, 26, 21, .50); cursor: pointer;
   transition: all .16s ease; min-width: 120px;
 }
 .agent-card:hover { border-color: var(--line-strong); background: rgba(16, 39, 32, .60); }
 .agent-card.active {
   border-color: var(--accent); background: rgba(110, 231, 196, .12);
   box-shadow: 0 0 18px rgba(110, 231, 196, .15);
 }
 .agent-card .agent-name { font-size: 13px; font-weight: 600; color: var(--fg); }
 .agent-card .agent-meta { font-size: 10px; color: var(--muted); margin-top: 4px; }
 .agent-card .agent-badge {
   display: inline-block; padding: 1px 6px; border-radius: 999px;
   background: rgba(110, 231, 196, .12); color: var(--accent);
   font-size: 9px; margin-top: 4px;
 }
 .agent-card.add-card { border-style: dashed; color: var(--muted); }
.plan-item { cursor: default; }
.plan-item.verified::before, .plan-item.applied::before { background: var(--accent); }

/* 神经元画布 */
.neuron-shell {
  position: relative; min-height: calc(100vh - 188px); overflow: hidden;
  border: 1px solid var(--line); border-radius: 18px;
  background: radial-gradient(circle at 50% 48%, rgba(37, 104, 83, .14), transparent 38%), rgba(3, 10, 8, .74);
  box-shadow: var(--shadow), inset 0 0 80px rgba(0, 0, 0, .30);
}
.neuron-shell::before {
  content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .28;
  background-image: radial-gradient(circle, rgba(110,231,196,.28) 1px, transparent 1.4px);
  background-size: 24px 24px; mask-image: radial-gradient(circle at center, black, transparent 82%);
}
.neuron-toolbar {
  position: absolute; z-index: 12; top: 16px; left: 18px; right: 18px;
  display: flex; align-items: flex-start; justify-content: space-between; gap: 18px; pointer-events: none;
}
.neuron-title, .canvas-actions, .neuron-legend, .neuron-stats, .merge-dock { pointer-events: auto; }
.neuron-title { max-width: 390px; }
.neuron-title .eyebrow { display: block; margin-bottom: 5px; }
.neuron-title h2 { font-size: 18px; font-weight: 560; }
.neuron-title p { margin-top: 4px; color: var(--muted); font-size: 11px; }
.canvas-actions { display: flex; gap: 8px; }
.neuron-stage { position: relative; width: 100%; height: calc(100vh - 188px); min-height: 610px; }
.neuron-canvas { position: absolute; inset: 0; }
.neuron-stats {
  position: absolute; z-index: 11; left: 18px; bottom: 18px; max-width: calc(100% - 390px);
  display: flex; flex-wrap: wrap; gap: 8px; padding: 8px;
  border: 1px solid var(--line); border-radius: 11px; background: rgba(4, 13, 10, .78); backdrop-filter: blur(14px);
}
.neuron-stat { min-width: 82px; padding: 6px 10px; border-right: 1px solid var(--line); }
.neuron-stat:last-child { border-right: 0; }
.neuron-stat strong { display: block; color: var(--accent-bright); font-size: 16px; font-weight: 550; }
.neuron-stat span { color: var(--muted); font-size: 9px; letter-spacing: .08em; }
.neuron-legend {
  position: absolute; z-index: 11; right: 18px; top: 82px; padding: 10px 12px;
  border: 1px solid var(--line); border-radius: 10px; background: rgba(4, 13, 10, .76); backdrop-filter: blur(12px);
  color: var(--muted); font-size: 10px;
}
.legend-item { display: flex; align-items: center; gap: 7px; margin: 5px 0; }
.legend-node { width: 7px; height: 7px; border: 1px solid var(--accent); border-radius: 50%; box-shadow: 0 0 7px rgba(110,231,196,.48); }
.legend-node.tentative { border-style: dashed; border-color: var(--orange); box-shadow: none; }
.legend-node.anchor { width: 4px; height: 4px; border: 0; background: rgba(110,231,196,.56); }
.merge-dock {
  position: absolute; z-index: 15; right: 18px; bottom: 18px; width: 310px; max-height: 220px; overflow: auto;
  padding: 12px; border: 1px solid var(--line); border-radius: 12px;
  background: rgba(4, 13, 10, .84); backdrop-filter: blur(16px); box-shadow: 0 18px 48px rgba(0,0,0,.28);
}
.merge-dock h3 { margin-bottom: 8px; font-size: 11px; font-weight: 650; }
.merge-item { padding: 9px 0; border-top: 1px solid var(--line); }
.merge-item:first-of-type { border-top: 0; }
.merge-copy { color: var(--muted); font-size: 10px; overflow-wrap: anywhere; }
.merge-actions { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: 7px; }
.merge-score { color: var(--accent); font-size: 10px; }
.neuron-popover {
  position: absolute; z-index: 30; width: min(360px, calc(100% - 28px)); max-height: min(470px, calc(100% - 32px));
  overflow: auto; padding: 16px; border: 1px solid rgba(110,231,196,.42); border-radius: 14px;
  background: rgba(7, 22, 17, .94); backdrop-filter: blur(22px); box-shadow: 0 24px 64px rgba(0,0,0,.46), 0 0 30px rgba(110,231,196,.09);
  opacity: 0; visibility: hidden; transform: translate(-50%, calc(-100% - 42px)) scale(.96);
  transform-origin: bottom center; transition: opacity .16s ease, transform .16s ease, visibility .16s;
}
.neuron-popover.show { opacity: 1; visibility: visible; transform: translate(-50%, calc(-100% - 42px)) scale(1); }
.neuron-popover.below { transform-origin: top center; transform: translate(-50%, 42px) scale(.96); }
.neuron-popover.below.show { transform: translate(-50%, 42px) scale(1); }
.neuron-popover::after {
  content: ""; position: absolute; left: 50%; bottom: -6px; width: 11px; height: 11px;
  transform: translateX(-50%) rotate(45deg); border-right: 1px solid rgba(110,231,196,.42); border-bottom: 1px solid rgba(110,231,196,.42); background: #071611;
}
.neuron-popover.below::after { top: -6px; bottom: auto; border: 0; border-left: 1px solid rgba(110,231,196,.42); border-top: 1px solid rgba(110,231,196,.42); }
.popover-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 12px; }
.popover-head h3 { font-size: 15px; font-weight: 600; }
.popover-kicker { color: var(--accent); font-size: 9px; letter-spacing: .14em; text-transform: uppercase; }
.claim-list { margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--line); }
.claim-list h4 { margin-bottom: 7px; color: var(--muted); font-size: 10px; font-weight: 600; letter-spacing: .08em; }
.claim-item { position: relative; padding: 7px 0 7px 11px; color: #b8d0c8; font-size: 11px; border-bottom: 1px solid rgba(110,231,196,.08); }
.claim-item::before { content: ""; position: absolute; top: 13px; left: 0; width: 4px; height: 4px; border-radius: 50%; background: var(--accent); }
.claim-item:last-child { border-bottom: 0; }

.loading { min-height: 320px; display: grid; place-items: center; color: var(--muted); font-size: 12px; }
.loading::before { content: ""; width: 34px; height: 34px; margin-right: 12px; border: 1px solid var(--line); border-top-color: var(--accent); border-radius: 50%; animation: pulse-spin 1.2s linear infinite; }
@keyframes pulse-spin { to { transform: rotate(360deg); } }
.toast {
  position: fixed; z-index: 100; right: 22px; bottom: 22px; min-width: 220px; padding: 11px 14px;
  border: 1px solid var(--line-strong); border-radius: 10px; background: rgba(7,22,17,.94); box-shadow: var(--shadow);
  color: var(--fg); font-size: 12px; opacity: 0; transform: translateY(8px); pointer-events: none;
  transition: opacity .22s ease, transform .22s ease;
}
.toast.show { opacity: 1; transform: translateY(0); }
.toast.success { border-color: rgba(110,231,196,.52); }
.toast.error { border-color: rgba(255,125,136,.55); }

@media (max-width: 900px) {
  .header { padding: 0 16px; }
  .ws-path { display: none; }
  .tab-bar { padding: 0 16px; gap: 18px; overflow-x: auto; }
  .tab { flex: none; }
  .content { padding: 18px 16px 28px; }
  .overview-hero, .overview-grid { grid-template-columns: 1fr; }
  .neuron-shell, .neuron-stage { min-height: 680px; height: calc(100vh - 170px); }
  .neuron-stats { max-width: calc(100% - 36px); bottom: 18px; right: 18px; }
  .merge-dock { right: 18px; bottom: 112px; }
}
@media (max-width: 620px) {
  .brand-copy span, .health-badge { display: none; }
  .header-right .btn { padding-inline: 10px; }
  .metrics { grid-template-columns: 1fr 1fr; }
  .neuron-title p, .neuron-legend { display: none; }
  .canvas-actions { flex-direction: column; }
  .merge-dock { width: calc(100% - 36px); max-height: 150px; bottom: 130px; }
  .neuron-stat { min-width: 62px; }
}

/* v3 投影门控 + 数据源 + 变更记录 */
.projection-gate {
  display: grid; grid-template-columns: 80px 1fr; gap: 22px; align-items: start;
  padding: 28px;
}
.projection-gate .gate-orb {
  width: 56px; height: 56px; margin-top: 6px; border-radius: 50%;
  border: 1px dashed var(--line-strong);
  background: radial-gradient(circle, rgba(110,231,196,.08), transparent 70%);
  box-shadow: 0 0 24px rgba(110,231,196,.10), inset 0 0 18px rgba(110,231,196,.06);
  animation: gate-pulse 2.4s ease-in-out infinite;
}
@keyframes gate-pulse {
  0%, 100% { box-shadow: 0 0 24px rgba(110,231,196,.10), inset 0 0 18px rgba(110,231,196,.06); }
  50% { box-shadow: 0 0 36px rgba(110,231,196,.22), inset 0 0 22px rgba(110,231,196,.10); }
}
.gate-body h3 { font-size: 16px; font-weight: 580; margin-bottom: 8px; }
.gate-reason { color: var(--muted); font-size: 12px; margin-bottom: 14px; }
.gate-warning {
  margin: 14px 0; padding: 12px 14px; border: 1px solid rgba(233,187,100,.32);
  border-radius: 9px; background: rgba(233,187,100,.06); color: var(--fg);
  font-size: 12px; line-height: 1.7;
}
.gate-warning strong { color: var(--orange); }

.raw-file-list { margin-top: 10px; display: grid; gap: 4px; }
.raw-file-row {
  display: flex; align-items: center; gap: 10px; padding: 8px 11px;
  border: 1px solid var(--line); border-radius: 8px; background: rgba(10,26,21,.50);
  cursor: pointer; transition: border-color .15s ease, background .15s ease, transform .15s ease;
}
.raw-file-row:hover { transform: translateX(2px); border-color: var(--line-strong); background: rgba(16,39,32,.72); }
.raw-file-path { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.raw-file-path code { font-size: 11px; }

.raw-file-content {
  margin: 0; padding: 16px; border: 1px solid var(--line); border-radius: 10px;
  background: rgba(4,13,10,.78); color: #cce5dc; font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
  font-size: 12px; line-height: 1.65; white-space: pre-wrap; overflow-wrap: anywhere; max-height: 70vh; overflow: auto;
}
</style>
</head>
<body>
<header class="header">
  <div class="header-left">
    <div class="brand" aria-label="MemoryGuard">
      <span class="brand-orb" aria-hidden="true"></span>
      <span class="brand-copy"><strong>MemoryGuard</strong><span>Local cognition control</span></span>
    </div>
    <span class="ws-path" id="ws-path">正在连接本地工作区…</span>
  </div>
  <div class="header-right">
    <span class="health-badge" id="health-badge">健康度 --</span>
    <button class="btn btn-primary" type="button" onclick="runAudit()">重新扫描</button>
  </div>
</header>

<nav class="tab-bar" role="tablist" aria-label="治理模块">
  <div class="tab active" role="tab" tabindex="0" data-tab="overview" onclick="switchTab('overview')">总览</div>
  <div class="tab" role="tab" tabindex="0" data-tab="sources" onclick="switchTab('sources')">数据源<span class="count" id="sources-count"></span></div>
  <div class="tab" role="tab" tabindex="0" data-tab="neurons" onclick="switchTab('neurons')">记忆核心<span class="count" id="neuron-count"></span></div>
  <div class="tab" role="tab" tabindex="0" data-tab="findings" onclick="switchTab('findings')">风险信号<span class="count" id="findings-count"></span></div>
  <div class="tab" role="tab" tabindex="0" data-tab="releases" onclick="switchTab('releases')">变更记录<span class="count" id="releases-count"></span></div>
  <div class="tab" role="tab" tabindex="0" data-tab="governance" onclick="switchTab('governance')">治理台</div>
</nav>

<main class="content" id="content"><div class="loading">正在建立本地治理视图</div></main>
<div class="toast" id="toast" role="status" aria-live="polite"></div>

<script>
let state = { report: null, activeTab: 'overview', plans: [], changes: [], releases: [], lastPlan: null };
let neuronGraph = null;
let cyInstance = null;
let selectedNeuronId = null;
let sourcesScope = 'all';      // 数据源 sub-tab: 'all' | 'user' | 'project'
let discoveryResult = null;    // 缓存 discover_agents 结果
let activeAgentInstanceId = '';  // v3.2：当前选中的 Agent 卡片
let agentCardsData = null;     // v3.2：缓存 list_agents 结果
let dataPageMode = 'single_agent';  // v3.2：single_agent | multi_agent_shared_mcp
let governanceSubTab = 'recent_events';  // 治理台子视图

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;').replaceAll("'", '&#039;');
}

async function callApi(method, ...args) {
  if (window.pywebview && window.pywebview.api) return await window.pywebview.api[method](...args);
  const resp = await fetch('/api/' + method, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(args) });
  if (!resp.ok) throw new Error('API ' + method + ' 返回 ' + resp.status);
  return await resp.json();
}

async function init() {
  try { state.report = await callApi('get_audit'); renderAll(); }
  catch (e) { showToast('扫描失败：' + e, 'error'); }
}

async function runAudit() {
  setContent('<div class="loading">正在重新扫描工作区</div>');
  try { state.report = await callApi('run_audit'); showToast('扫描完成', 'success'); renderAll(); }
  catch (e) { showToast('扫描失败：' + e, 'error'); }
}

function switchTab(tab) {
  state.activeTab = tab;
  document.querySelectorAll('.tab').forEach(el => {
    const active = el.dataset.tab === tab;
    el.classList.toggle('active', active);
    el.setAttribute('aria-selected', active ? 'true' : 'false');
  });
  renderContent();
}

document.querySelectorAll('.tab').forEach(el => el.addEventListener('keydown', event => {
  if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); switchTab(el.dataset.tab); }
}));

function setContent(html) { document.getElementById('content').innerHTML = html; }

function renderAll() {
  if (!state.report) return;
  const r = state.report;
  document.getElementById('ws-path').textContent = r.workspace;
  const badge = document.getElementById('health-badge');
  badge.textContent = '健康度 ' + Math.round(r.health_score) + '/100';
  badge.style.color = r.health_score >= 70 ? 'var(--accent)' : r.health_score >= 40 ? 'var(--orange)' : 'var(--red)';
  document.getElementById('findings-count').textContent = r.findings.length || '';
  document.getElementById('sources-count').textContent = '';
  document.getElementById('releases-count').textContent = state.releases ? state.releases.length : '';
  renderContent();
}

function renderContent() {
  switch (state.activeTab) {
    case 'overview': renderOverview(); break;
    case 'sources': renderSources(); break;
    case 'neurons': renderNeurons(); break;
    case 'findings': renderFindings(); break;
    case 'releases': renderReleases(); break;
    case 'governance': renderGovernance(); break;
  }
}

async function renderNeurons() {
  setContent('<div class="loading">正在读取神经图投影</div>');
  try { neuronGraph = await callApi('get_neuron_graph'); renderNeuronGraph(); }
  catch (e) {
    showToast('神经图构建失败：' + e, 'error');
    setContent(`<div class="card empty-state"><div><div class="empty-orb"></div><p>神经图构建失败：${escapeHtml(e)}</p></div></div>`);
  }
}

function graphElements(graph) {
  // v3.1 §6.3：统一 v3 图契约
  // node: id / parent_id / label / node_kind / memory_id / kind / provenance_count
  // edge: id / source / target / edge_type
  const elements = [];
  for (const node of graph.nodes || []) {
    const root = node.node_kind === 'root';
    const anchor = node.node_kind === 'claim_anchor';
    // v3：用 provenance_count 替代旧 claim_count 决定大小
    const provCount = node.provenance_count || 0;
    const size = root ? 66 : anchor ? 7 : Math.max(27, Math.min(54, 25 + provCount * 3.2));
    elements.push({ data: {
      id: node.id,
      label: anchor ? '' : String(node.label || '').slice(0, 18),
      kind: node.node_kind,
      memory_id: node.memory_id || '',
      record_kind: node.kind || '',
      provenance_count: provCount,
      size,
      opacity: 0.85,
    }});
  }
  for (const edge of graph.edges || []) {
    elements.push({ data: {
      id: edge.id, source: edge.source, target: edge.target,
      etype: edge.edge_type, strength: 0.35,
    }});
  }
  return elements;
}

function renderMergeDock(suggestions) {
  // v3.1 §6.3：projection 不再返回 merge_suggestions（自动晋升凋亡已移除）
  // 重复候选在 Memory IR 的 duplicate_groups 中查看
  if (!suggestions || !suggestions.length) return '';
  return `<aside class="merge-dock" aria-label="重复候选">
    <h3>重复候选 · ${suggestions.length} 条</h3>
    ${suggestions.map(item => `<div class="merge-item">
      <div class="merge-copy">${escapeHtml(item.group_id || '')}</div>
      <div class="merge-actions"><span class="merge-score">${item.member_ids ? item.member_ids.length : 0} 条记录</span></div>
    </div>`).join('')}
  </aside>`;
}

function renderNeuronGraph() {
  const graph = neuronGraph;
  // 顶部 7 项状态信息（v3.1 §6.1）：Agent 实例 / Profile / 规范版本 / Release / 接管状态 / 覆盖状态 / 是否漂移
  // 后端 meta 结构：{agent_instances: [...], instance_count, coverage, coverage_status, release_count, drifted}
  const meta = (graph && graph.meta) || {};
  const instances = meta.agent_instances || [];
  // 每个 agent_instance 一组 chip：产品名 + 接管状态 + 规范版本 + 记录数
  const instanceChips = instances.length ? instances.map(inst => {
    const takeoverClass = (inst.takeover_state === 'operational' || inst.takeover_state === 'runtime_verified') ? 'confirmed'
      : (inst.takeover_state === 'drifted' || inst.takeover_state === 'partial') ? 'high' : 'medium';
    return `<span class="chip chip-info" title="${escapeHtml(inst.instance_id)}">${escapeHtml(inst.product || 'agent')} · ${escapeHtml(inst.takeover_state || 'not_detected')}</span>
      <span class="chip chip-info">版本 · ${escapeHtml(inst.managed_version ? inst.managed_version.slice(0,8) : '—')}</span>
      <span class="chip chip-info">记录 · ${inst.record_count || 0}</span>`;
  }).join('') : '<span class="chip chip-info">Agent · 未发现</span>';
  const metaBar = `<section class="card" style="margin-bottom:14px"><div class="card-head"><div><h2>记忆核心状态</h2>
    <p>顶部 7 项状态信息（v3.1 §6.1）</p></div></div>
    <div class="chips">
      ${instanceChips}
      <span class="chip chip-info">实例数 · ${meta.instance_count || 0}</span>
      <span class="chip chip-info">Release · ${meta.release_count || 0}</span>
      <span class="chip chip-${meta.coverage_status === 'complete' ? 'confirmed' : 'medium'}">覆盖 · ${escapeHtml(meta.coverage_status || 'unknown')}</span>
      <span class="chip chip-${meta.drifted ? 'high' : 'confirmed'}">漂移 · ${meta.drifted ? '是' : '否'}</span>
    </div></section>`;
  // 未构建时显示门控
  if (!graph || graph.empty || !graph.nodes || !graph.nodes.length) {
    document.getElementById('neuron-count').textContent = '';
    const reason = graph && graph.reason ? graph.reason : 'not_built';
    const reasonText = {
      'not_built': '尚未构建投影。神经图是 Memory IR 的可视化投影，不是事实源。',
      'no_ir': 'Memory IR 为空，请先在数据源 tab 扫描来源。',
      'error': '投影读取失败。',
    }[reason] || '尚未构建投影。';
    setContent(`<div class="view-heading"><span class="eyebrow">Live cognition map</span><h2>记忆核心</h2>
      <p>神经图是 Memory IR 的可视化投影，不是事实源。删除后可从 IR + DecisionLog 完整重建。图上治理操作会写入 DecisionLog 并生成新规范版本。</p></div>
      ${metaBar}
      <section class="card projection-gate">
        <div class="gate-orb" aria-hidden="true"></div>
        <div class="gate-body">
          <h3>当前状态：未构建</h3>
          <p class="gate-reason">${escapeHtml(reasonText)}</p>
          <div class="gate-warning">
            <strong>构建投影会扫描所有授权来源并规范化为 Memory IR。</strong><br>
            原始记忆文件不会被修改，投影可随时删除重建。<br>
            此操作不写入受管目标，仅生成可视化投影。
          </div>
          <div class="finding-actions">
            <button class="btn btn-primary" type="button" onclick="buildProjection()">构建投影</button>
          </div>
        </div>
      </section>`);
    return;
  }
  const stats = graph.stats || {};
  const suggestions = [];
  selectedNeuronId = null;
  document.getElementById('neuron-count').textContent = stats.node_count || '';
  setContent(`<div class="view-heading"><span class="eyebrow">Live cognition map</span><h2>记忆核心</h2>
    <p>点击任意光点，在原位查看证据并治理。滚轮缩放，拖拽探索。图上操作会写入 DecisionLog 并生成新规范版本。</p></div>
    ${metaBar}
    <section class="neuron-shell">
    <div class="neuron-toolbar">
      <div class="neuron-title"><span class="eyebrow">Cognition control surface</span><h2>可操作神经图</h2>
        <p>图上接受/排除/隔离/合并操作会写入 DecisionLog，重建规范版本并生成发布计划。</p></div>
      <div class="canvas-actions">
        <button class="btn" type="button" onclick="fitNeuronGraph()">重置视野</button>
        <button class="btn" type="button" onclick="deleteProjection()">删除投影</button>
        <button class="btn btn-primary" type="button" onclick="buildProjection()">重建投影</button>
      </div>
    </div>
    <div class="neuron-stage" id="neuron-stage">
      <div class="neuron-canvas" id="cy" aria-label="本地记忆神经图画布"></div>
      <div class="neuron-legend">
        <div class="legend-item"><span class="legend-node"></span>主题节点</div>
        <div class="legend-item"><span class="legend-node tentative"></span>记忆片段</div>
        <div class="legend-item"><span class="legend-node anchor"></span>原始记录</div>
      </div>
      <div class="neuron-stats">
        <div class="neuron-stat"><strong>${stats.claim_anchor_count || 0}</strong><span>记忆片段</span></div>
        <div class="neuron-stat"><strong>${stats.node_count || 0}</strong><span>总节点</span></div>
        <div class="neuron-stat"><strong>${stats.topic_count || 0}</strong><span>主题节点</span></div>
        <div class="neuron-stat"><strong>${stats.edge_count || 0}</strong><span>关系边</span></div>
        <div class="neuron-stat"><strong>${stats.provenance_total || 0}</strong><span>来源证据</span></div>
      </div>
      ${renderMergeDock(suggestions)}
      <aside class="neuron-popover" id="neuron-popover" role="dialog" aria-live="polite" aria-label="光点治理"></aside>
    </div>
  </section>`);

  if (typeof cytoscape === 'undefined') {
    document.getElementById('cy').innerHTML = '<div class="empty-state" style="color:var(--red)">本地 Cytoscape 资源加载失败</div>';
    return;
  }

  cyInstance = cytoscape({
    container: document.getElementById('cy'),
    elements: graphElements(graph),
    style: [
      { selector: 'node', style: {
        'width': 'data(size)', 'height': 'data(size)', 'background-color': '#173b31',
        'background-opacity': 'data(opacity)', 'border-width': 1.4, 'border-color': '#6ee7c4',
        'label': 'data(label)', 'color': '#cce5dc', 'font-size': 9.5,
        'font-family': 'Segoe UI, PingFang SC, sans-serif', 'font-weight': 500,
        'text-valign': 'bottom', 'text-halign': 'center', 'text-margin-y': 8,
        'text-outline-width': 2, 'text-outline-color': '#040b09', 'text-wrap': 'wrap', 'text-max-width': 92,
        'transition-property': 'border-width, border-color, background-color, opacity', 'transition-duration': '160ms',
      }},
      { selector: 'node[kind = "root"]', style: {
        'background-color': '#6ee7c4', 'background-opacity': .24, 'border-width': 2.5,
        'border-color': '#bcffeb', 'font-size': 11,
      }},
      { selector: 'node[kind = "claim_anchor"]', style: {
        'background-color': '#6ee7c4', 'background-opacity': .62, 'border-width': 0,
        'label': '',
      }},
      { selector: 'node[status = "tentative"]', style: {
        'background-color': '#2b2a20', 'border-color': '#e9bb64', 'border-style': 'dashed',
      }},
      { selector: 'edge', style: {
        'width': 'mapData(strength, 0, 1, .45, 2.4)', 'line-color': '#6ee7c4', 'line-opacity': .18,
        'curve-style': 'unbundled-bezier', 'control-point-distances': 20, 'control-point-weights': .5,
        'target-arrow-shape': 'none', 'transition-property': 'line-opacity, width', 'transition-duration': '140ms',
      }},
      { selector: 'edge[etype = "related"]', style: { 'line-style': 'dashed', 'line-opacity': .12 }},
      { selector: '.neighborhood', style: { 'line-opacity': .62, 'width': 2.1 }},
      { selector: 'node.neighborhood', style: { 'border-color': '#bcffeb', 'border-width': 2.5 }},
      { selector: ':selected', style: { 'opacity': 0, 'text-opacity': 0 }},
    ],
    layout: {
      name: 'cose', animate: true, animationDuration: 650, randomize: true,
      nodeRepulsion: 9500, idealEdgeLength: 94, edgeElasticity: 90,
      nestingFactor: .85, gravity: .28, numIter: 1100, initialTemp: 150, coolingFactor: .97,
      minTemp: 1, nodeOverlap: 26, padding: 76,
    },
    minZoom: .22, maxZoom: 3.6,
  });

  cyInstance.on('tap', 'node', event => selectNeuron(event.target.id()));
  cyInstance.on('mouseover', 'node', event => {
    const node = event.target;
    node.addClass('neighborhood');
    node.connectedEdges().addClass('neighborhood');
    node.neighborhood('node').addClass('neighborhood');
  });
  cyInstance.on('mouseout', 'node', () => cyInstance.elements().removeClass('neighborhood'));
  cyInstance.on('tap', event => { if (event.target === cyInstance) hideNeuronPopover(); });
  cyInstance.on('pan zoom resize', () => { if (selectedNeuronId) positionNeuronPopover(selectedNeuronId); });
  cyInstance.on('drag position', 'node', event => {
    if (selectedNeuronId === event.target.id()) positionNeuronPopover(selectedNeuronId);
  });
}

function fitNeuronGraph() {
  hideNeuronPopover();
  if (cyInstance) cyInstance.animate({ fit: { eles: cyInstance.elements(), padding: 72 }, duration: 340 });
}

function selectNeuron(nodeId) {
  // v3.1 §6.2：节点气泡显示真实可验证字段 + 7 种图上治理操作
  // 字段：record_id / kind / scope / priority / status / 来源与定位 / 冲突重复关系 / 当前发布状态 / 目标兼容性 / 风险与隔离原因
  // 操作：接受候选 / 排除并填写原因 / 隔离敏感或不确定内容 / 标记替代关系 / 确认合并候选 / 修改作用域和优先级 / 生成发布计划
  const node = (neuronGraph.nodes || []).find(item => item.id === nodeId);
  const popover = document.getElementById('neuron-popover');
  if (!node || !popover) return;
  selectedNeuronId = nodeId;
  if (cyInstance) {
    cyInstance.elements().unselect();
    cyInstance.getElementById(nodeId).select();
  }
  const childCount = (neuronGraph.nodes || []).filter(n => n.parent_id === nodeId).length;
  const isAnchor = node.node_kind === 'claim_anchor';
  const popoverBody = isAnchor
    ? `<div class="row"><span class="key">record_id</span><code style="overflow-wrap:anywhere">${escapeHtml(node.memory_id || '')}</code></div>
       <div class="row"><span class="key">kind</span><span>${escapeHtml(node.kind || '')}</span></div>
       <div class="row"><span class="key">scope</span><span>${escapeHtml(node.scope || 'project')}</span></div>
       <div class="row"><span class="key">priority</span><span>${escapeHtml(String(node.priority ?? '—'))}</span></div>
       <div class="row"><span class="key">status</span><span>${escapeHtml(node.decision_state || node.status || 'candidate')}</span></div>
       <div class="row"><span class="key">来源</span><span>${node.provenance_count || 0} 个 provenance</span></div>
       <div class="row"><span class="key">发布</span><span>${escapeHtml(node.release_state || 'unpublished')}</span></div>
       <div class="row"><span class="key">兼容</span><span>${escapeHtml((node.target_compatibility || []).join(', ') || '—')}</span></div>
       ${node.risk_count ? `<div class="row"><span class="key">风险</span><span style="color:var(--red)">${node.risk_count} 条</span></div>` : ''}`
    : `<div class="row"><span class="key">子节点</span><span>${childCount}</span></div>
       <div class="row"><span class="key">节点类型</span><span>${escapeHtml(node.node_kind || '')}</span></div>`;
  const governanceActions = isAnchor ? `
    <div class="finding-actions" style="flex-direction:column;align-items:stretch;gap:6px">
      <div style="font-size:10px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-top:6px">图上治理操作 → DecisionEvent</div>
      <div style="display:flex;flex-wrap:wrap;gap:6px">
        <button class="btn btn-primary" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','accept')">接受候选</button>
        <button class="btn btn-danger" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','exclude')">排除</button>
        <button class="btn" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','quarantine')">隔离</button>
        <button class="btn" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','supersede')">标记替代</button>
        <button class="btn" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','merge')">确认合并</button>
        <button class="btn" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','rescope')">改作用域</button>
        <button class="btn" type="button" onclick="neuronAction('${escapeHtml(nodeId)}','plan')">生成发布计划</button>
      </div>
    </div>` : '';
  popover.innerHTML = `<div class="popover-head">
      <div><div class="popover-kicker">${escapeHtml(node.node_kind)}</div><h3>${escapeHtml(node.label || '未命名节点')}</h3></div>
      <button class="btn btn-icon" type="button" aria-label="关闭" onclick="hideNeuronPopover()">×</button>
    </div>
    <div class="row"><span class="key">节点 ID</span><code>${escapeHtml(node.id || '')}</code></div>
    ${popoverBody}
    ${governanceActions}`;
  popover.classList.add('show');
  requestAnimationFrame(() => positionNeuronPopover(nodeId));
}

async function neuronAction(nodeId, action) {
  // v3.1 §6.2：图上操作 → 追加 DecisionEvent → 生成新规范版本 → 投影重建
  let reason = '';
  if (action === 'exclude' || action === 'quarantine' || action === 'supersede') {
    reason = prompt(action + ' 的原因（必填）：') || '';
    if (!reason) return showToast('需填写原因', 'error');
  }
  showToast('正在写入 DecisionEvent…');
  try {
    const result = await callApi('neuron_decide', nodeId, action, reason, true);
    if (result.error) return showToast(result.error, 'error');
    showToast(`已写入决策，新规范版本：${result.memory_version || ''}`, 'success');
    neuronGraph = await callApi('get_neuron_graph'); renderNeuronGraph();
  } catch (e) { showToast('操作失败：' + e, 'error'); }
}

function positionNeuronPopover(nodeId) {
  const popover = document.getElementById('neuron-popover');
  const stage = document.getElementById('neuron-stage');
  if (!popover || !stage || !cyInstance) return;
  const element = cyInstance.getElementById(nodeId);
  if (!element || !element.length) return;
  const pos = element.renderedPosition();
  const half = Math.min(180, (stage.clientWidth - 28) / 2);
  const x = Math.max(half + 14, Math.min(stage.clientWidth - half - 14, pos.x));
  const needsBelow = pos.y < Math.min(popover.offsetHeight + 30, stage.clientHeight * .48);
  popover.classList.toggle('below', needsBelow);
  popover.style.left = x + 'px';
  popover.style.top = Math.max(14, Math.min(stage.clientHeight - 14, pos.y)) + 'px';
}

function hideNeuronPopover() {
  selectedNeuronId = null;
  const popover = document.getElementById('neuron-popover');
  if (popover) popover.classList.remove('show');
  if (cyInstance) cyInstance.elements().unselect();
}

async function doPromote(lightId) {
  showToast('v3 已移除自动晋升操作（神经图是纯投影）', 'error');
}

async function doDissolve(lightId) {
  showToast('v3 已移除自动凋亡操作（神经图是纯投影）', 'error');
}

async function doMerge(fromId, toId) {
  showToast('v3 已移除合并操作（神经图是纯投影）', 'error');
}

async function buildProjection() {
  // v3 spec §7.3：神经图是纯投影，需用户确认（带警告）
  if (!confirm('此操作将扫描所有授权来源并规范化为 Memory IR，然后构建神经图投影。\n\n'
    + '· 原始记忆文件不会被修改\n'
    + '· 投影可随时删除重建\n'
    + '· 此操作不写入受管目标，仅生成可视化投影\n\n'
    + '继续？')) return;
  setContent('<div class="loading">正在扫描来源并构建投影</div>');
  try {
    const result = await callApi('build_projection', true);
    if (result.error) return showToast(result.error, 'error');
    neuronGraph = await callApi('get_neuron_graph'); renderNeuronGraph(); showToast('投影构建完成', 'success');
  } catch (e) { showToast('构建失败：' + e, 'error'); }
}

async function deleteProjection() {
  if (!confirm('删除当前神经图投影？\n\n投影可从 Memory IR + DecisionLog 完整重建，不会丢失任何原始记忆或决策。')) return;
  try {
    const result = await callApi('delete_projection', true);
    if (result.error) return showToast(result.error, 'error');
    neuronGraph = await callApi('get_neuron_graph');
    renderNeuronGraph();
    showToast('投影已删除，可随时重建', 'success');
  } catch (e) { showToast('删除失败：' + e, 'error'); }
}

async function reExtract() {
  // 兼容旧调用：转发到 buildProjection
  await buildProjection();
}

function renderOverview() {
  const report = state.report;
  const summary = report.summary;
  const severity = Object.entries(summary.finding_count_by_severity || {})
    .map(([name, count]) => `<span class="chip chip-${escapeHtml(name)}">${escapeHtml(name)} · ${count}</span>`).join('');
  const health = Math.max(0, Math.min(100, Number(report.health_score || 0)));
  const invisible = summary.invisible_count > 0 ? `<section class="card"><div class="card-head"><div><h2>不可见范围</h2><p>治理边界之外的对象会明确显示，不会静默忽略。</p></div></div>
    ${report.invisible.map(item => `<div class="finding-evidence">${escapeHtml(item.path)} · ${escapeHtml(item.reason)}</div>`).join('')}</section>` : '';
  setContent(`<div class="view-heading"><span class="eyebrow">System pulse</span><h2>本地认知治理总览</h2><p>一次扫描看清 Agent 指令、技能、记忆和本地 RAG 的健康状态。</p></div>
    <div class="overview-hero">
      <section class="card health-orbit"><div class="health-ring" style="--health-angle:${health * 3.6}deg">
        <div class="health-ring-content"><strong>${Math.round(health)}</strong><span>HEALTH SIGNAL</span></div></div></section>
      <section class="card"><div class="card-head"><div><h2>治理信号</h2><p>当前工作区的可见对象与风险密度</p></div></div>
        <div class="metrics">
          <div class="metric"><div class="num">${summary.object_count}</div><div class="label">已识别对象</div></div>
          <div class="metric"><div class="num">${report.findings.length}</div><div class="label">风险信号</div></div>
          <div class="metric"><div class="num">${summary.invisible_count}</div><div class="label">不可见范围</div></div>
          <div class="metric"><div class="num">18</div><div class="label">治理规则</div></div>
        </div>
      </section>
    </div>
    <div class="overview-grid">
      <section class="card"><div class="card-head"><div><h2>风险频谱</h2><p>仅保留有决策价值的严重度信号</p></div></div><div class="chips">${severity || '<span class="chip chip-low">当前未发现风险</span>'}</div></section>
      <section class="card"><div class="card-head"><div><h2>扫描脉冲</h2></div></div><div class="scan-list">
        <div class="scan-row"><span>耗时</span><strong>${report.duration_ms} ms</strong></div>
        <div class="scan-row"><span>生成时间</span><strong>${escapeHtml(report.generated_at)}</strong></div>
        <div class="scan-row"><span>执行位置</span><strong>仅限本机</strong></div>
      </div></section>
    </div>${invisible}`);
}

function renderFindings() {
  const report = state.report;
  if (!report.findings.length) {
    setContent('<div class="view-heading"><span class="eyebrow">Risk signals</span><h2>风险信号</h2></div><div class="card empty-state"><div><div class="empty-orb"></div><p>没有发现需要处理的风险信号。</p></div></div>');
    return;
  }
  const items = report.findings.map(finding => `<article class="finding-item sev-${escapeHtml(finding.severity)}" onclick="toggleFinding('${escapeHtml(finding.id)}')">
    <div class="finding-header"><span class="finding-rule"><span class="chip chip-${escapeHtml(finding.severity)}">${escapeHtml(finding.severity)}</span> ${escapeHtml(finding.rule_id)}</span>
      ${finding.fixable ? '<span style="color:var(--accent);font-size:10px">可生成变更</span>' : ''}</div>
    <div class="finding-evidence">${escapeHtml(finding.evidence)}</div>
    <div class="finding-detail" id="detail-${escapeHtml(finding.id)}" style="display:none">
      <div class="row"><span class="key">维度</span><span>${escapeHtml(finding.dimension)}</span></div>
      <div class="row"><span class="key">表面</span><span>${escapeHtml(finding.surface)}</span></div>
      <div class="row"><span class="key">位置</span><code>${escapeHtml(finding.location.path)}:${finding.location.span[0]}</code></div>
      <div class="row"><span class="key">影响</span><span>${escapeHtml(finding.impact)}</span></div>
      <div class="row"><span class="key">建议</span><span>${escapeHtml(finding.suggestion)}</span></div>
      <div class="row"><span class="key">置信度</span><span>${(finding.confidence * 100).toFixed(0)}%</span></div>
      <div class="finding-actions">${finding.fixable ? `<button class="btn btn-primary" type="button" onclick="event.stopPropagation();generatePlan('${escapeHtml(finding.id)}')">生成修复计划</button>` : ''}</div>
    </div></article>`).join('');
  setContent(`<div class="view-heading"><span class="eyebrow">Risk signals</span><h2>风险信号</h2><p>沿着证据链查看问题，不隐藏扫描盲区。</p></div>${items}`);
}

function toggleFinding(id) {
  const element = document.getElementById('detail-' + id);
  if (element) element.style.display = element.style.display === 'none' ? 'block' : 'none';
}

async function generatePlan(findingId) {
  showToast('正在生成修复计划…');
  try {
    const result = await callApi('generate_plan', findingId);
    if (result.error) return showToast(result.error, 'error');
    state.plans.push(result.plan);
    document.getElementById('releases-count').textContent = (state.releases ? state.releases.length : 0) + state.plans.length;
    showToast('修复计划已生成', 'success'); switchTab('releases');
  } catch (e) { showToast('生成失败：' + e, 'error'); }
}

async function applyPlan(planId) {
  showToast('正在应用并验证…');
  try {
    const result = await callApi('apply_plan', planId);
    if (result.error) return showToast(result.error, 'error');
    const plan = state.plans.find(item => item.plan_id === planId);
    if (plan) plan.change = result.change;
    showToast(result.change.status === 'verified' ? '变更已通过验证' : '变更未通过验证', result.change.status === 'verified' ? 'success' : 'error');
    state.report = await callApi('get_audit'); renderAll();
  } catch (e) { showToast('应用失败：' + e, 'error'); }
}

async function undoChange(changeId, planId) {
  showToast('正在撤销变更…');
  try {
    const result = await callApi('undo_change', changeId);
    if (result.error) return showToast(result.error, 'error');
    const plan = state.plans.find(item => item.plan_id === planId);
    if (plan) plan.change = null;
    state.report = await callApi('get_audit'); showToast('变更已撤销', 'success'); renderAll();
  } catch (e) { showToast('撤销失败：' + e, 'error'); }
}

// ===========================================================================
// v3 数据源 tab：SourceRoot 列表 + 原始记忆按 agent 分组 + 文件内容查看
// spec §7.1 / §7.2 SourceApi + get_raw_memory + get_source_file_content
// ===========================================================================

async function renderSources() {
  setContent('<div class="loading">正在加载数据页</div>');
  try {
    // v3.2：先加载 Agent 卡片
    agentCardsData = await callApi('list_agents');
    const agents = agentCardsData.agents || [];
    // 默认选中第一个 Agent
    if (!activeAgentInstanceId && agents.length > 0) {
      activeAgentInstanceId = agents[0].instance_id;
    }
    // 加载选中 Agent 的数据 + 来源列表 + 覆盖率
    const [agentData, sourcesResult, rawResult] = await Promise.all([
      activeAgentInstanceId ? callApi('get_agent_data', activeAgentInstanceId) : Promise.resolve(null),
      callApi('list_sources'),
      callApi('get_raw_memory'),
    ]);
    renderSourcesView(sourcesResult, rawResult, agentData);
  } catch (e) {
    showToast('数据源加载失败：' + e, 'error');
    setContent(`<div class="card empty-state"><div><div class="empty-orb"></div><p>数据源加载失败：${escapeHtml(e)}</p></div></div>`);
  }
}

function selectAgentCard(instanceId) {
  activeAgentInstanceId = instanceId;
  renderSources();
}

function renderSourcesView(sourcesResult, rawResult, agentData) {
  const sources = sourcesResult.sources || [];
  const cov = rawResult.coverage || {};
  document.getElementById('sources-count').textContent = sources.length || '';

  // v3.2 Agent 卡片
  const agents = (agentCardsData && agentCardsData.agents) || [];
  const agentCardsHtml = agents.length ? agents.map(a => {
    const isActive = a.instance_id === activeAgentInstanceId;
    return `<div class="agent-card ${isActive ? 'active' : ''}" onclick="selectAgentCard('${escapeHtml(a.instance_id)}')">
      <div class="agent-name">${escapeHtml(a.product)}</div>
      <div class="agent-meta">${a.found_surface_count}/${a.surface_count} 表面 · ${a.bound_source_count} 来源</div>
      <div class="agent-badge">${escapeHtml(a.target_capability || 'export_only')}</div>
    </div>`;
  }).join('') : '<div class="agent-card" style="cursor:default"><div class="agent-meta">未发现 Agent，点击"检测本机 Agent"</div></div>';
  const addCards = `<div class="agent-card add-card" onclick="addSourceDialog()"><div class="agent-name">+ 手动来源</div></div>
    <div class="agent-card add-card" onclick="importBundleDialog()"><div class="agent-name">+ 外部 MCP</div></div>`;

  // 选中 Agent 的分类数据视图
  const categories = (agentData && agentData.categories) || {};
  const catLabels = {
    native_memory: '原生记忆', control_surface: '控制面', skill_surface: 'Skill 表面',
    conversation_history: '会话历史', runtime_evidence: '运行证据', knowledge_source: '知识来源',
    unknown: '其他', project_memory: '项目记忆',
  };
  const agentDataHtml = agentData ? Object.entries(categories).map(([cat, files]) => {
    const label = catLabels[cat] || cat;
    return `<div style="margin-bottom:14px">
      <div class="finding-header"><span class="finding-rule">${escapeHtml(label)}</span>
        <span class="chip chip-info">${files.length} 个文件</span></div>
      <div class="raw-file-list">
        ${files.map(f => `<div class="raw-file-row" onclick="viewSourceFile('${escapeHtml(f.root_id)}','${escapeHtml(f.relative_path).replaceAll("'", "\\'")}')">
          <span class="raw-file-path"><code>${escapeHtml(f.relative_path).replaceAll('\\', '/')}</code></span>
          <span class="chip chip-${f.read_status === 'read' ? 'confirmed' : 'medium'}">${escapeHtml(f.read_status)}</span>
          <span style="color:var(--faint);font-size:10px">${escapeHtml(f.media_type || '')}</span>
        </div>`).join('')}
      </div>
    </div>`;
  }).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>选中一个 Agent 卡片查看其数据。</p></div>';

  // 覆盖率
  const covCard = `<section class="card">
    <div class="card-head"><div><h2>覆盖率账本</h2><p>证明扫描完整性，unaccounted_count 必须为 0</p></div></div>
    <div class="chips">
      <span class="chip chip-info">candidates · ${cov.candidate_count || 0}</span>
      <span class="chip chip-confirmed">read · ${cov.read || 0}</span>
      <span class="chip chip-medium">unsupported · ${cov.unsupported || 0}</span>
      <span class="chip chip-high">unreadable · ${cov.unreadable || 0}</span>
      <span class="chip chip-medium">skipped · ${cov.skipped_by_policy || 0}</span>
      <span class="chip chip-${(cov.unaccounted_count || 0) === 0 ? 'confirmed' : 'high'}">unaccounted · ${cov.unaccounted_count || 0}</span>
      <span class="chip chip-${cov.coverage_status === 'complete' ? 'confirmed' : 'medium'}">${escapeHtml(cov.coverage_status || 'unknown')}</span>
    </div>
  </section>`;

  // 快速操作
  const actionsCard = `<section class="card"><div class="card-head"><div><h2>快速操作</h2>
    <p>自动检测本机已安装的 Agent · 手工添加文件/文件夹 · 导入 ChatAI 网页版导出包</p></div>
    <div class="finding-actions">
      <button class="btn btn-primary" type="button" onclick="discoverAgents()">检测本机 Agent</button>
      <button class="btn" type="button" onclick="addSourceDialog()">手工添加文件/文件夹</button>
      <button class="btn" type="button" onclick="importBundleDialog()">导入离线导出包</button>
    </div></div>
    <div class="gate-warning" style="margin-top:0">
      <strong>网页 ChatAI 记忆导出导入：</strong>ChatGPT/Claude/Gemini 的网页版通常在「Settings -> Data export」导出 zip 包，
      解压后是 conversations.json。点上面"导入离线导出包"选择 zip 或解压后的目录/文件即可。
    </div></section>`;

  const agentInfo = agentData && agentData.agent ? agentData.agent : null;
  setContent(`<div class="view-heading"><span class="eyebrow">Sources</span><h2>数据源</h2>
    <p>v3.2 数据页：顶部 Agent 卡片切换，下方显示该 Agent 的原生记忆、控制面、Skill、会话历史、项目文档。文档不是记忆，只在数据页。</p></div>
    ${actionsCard}
    ${covCard}
    <section class="card"><div class="card-head"><div><h2>Agent 卡片</h2>
      <p>点击卡片切换数据视图。${agents.length} 个 Agent 已发现。</p></div></div>
      <div class="agent-cards">${agentCardsHtml}${addCards}</div></section>
    <section class="card"><div class="card-head"><div><h2>${agentInfo ? escapeHtml(agentInfo.product) + ' 数据视图' : 'Agent 数据视图'}</h2>
      <p>${agentData ? agentData.total_files + ' 个文件，' + agentData.category_count + ' 个类别' : '选中 Agent 后显示数据'}</p></div>
      ${agentInfo ? `<div class="finding-actions"><button class="btn" type="button" onclick="selectAgentInstance('${escapeHtml(agentInfo.instance_id)}')">勾选授权</button>
        <button class="btn btn-primary" type="button" onclick="enterMultiAgentMode()">进入多 Agent 共享 MCP 模式</button></div>` : ''}</div>
      ${agentDataHtml}</section>`);
}

async function enterMultiAgentMode() {
  dataPageMode = 'multi_agent_shared_mcp';
  showToast('进入多 Agent 共享 MCP 模式，请选择 Agent');
  await renderMultiAgentBinding();
}

async function renderMultiAgentBinding() {
  setContent('<div class="loading">正在加载 Agent 列表与已有绑定…</div>');
  try {
    const [agentsResult, bindingsResult] = await Promise.all([
      callApi('list_agents'),
      callApi('list_bindings'),
    ]);
    showMultiAgentBinding(agentsResult, bindingsResult);
  } catch (e) {
    showToast('加载失败：' + e, 'error');
    setContent(`<div class="card empty-state"><div><div class="empty-orb"></div><p>加载失败：${escapeHtml(e)}</p></div></div>`);
  }
}

function showMultiAgentBinding(agentsResult, bindingsResult) {
  const agents = (agentsResult && agentsResult.agents) || [];
  const existingBindings = (bindingsResult && bindingsResult.bindings) || [];
  if (!agents.length) {
    setContent(`<div class="view-heading"><span class="eyebrow">Multi-agent</span><h2>多 Agent 共享 MCP 模式</h2></div>
      <div class="card empty-state"><div><div class="empty-orb"></div><p>未发现 Agent。请先在数据源 tab 检测本机 Agent 或手工添加来源。</p></div></div>
      <div class="finding-actions"><button class="btn" type="button" onclick="renderSources()">← 返回数据源</button></div>`);
    return;
  }
  // 已有 active binding 的 agent 默认勾选
  const boundAgentSet = new Set(
    existingBindings.filter(b => b.status === 'active').map(b => b.agent_instance_id)
  );
  const agentRowsHtml = agents.map(a => {
    const bound = boundAgentSet.has(a.instance_id);
    return `<label class="raw-file-row" style="cursor:pointer;grid-template-columns:auto 1fr auto;align-items:center">
      <input type="checkbox" data-agent-id="${escapeHtml(a.instance_id)}" ${bound ? 'checked' : ''}>
      <div>
        <div class="finding-rule">${escapeHtml(a.product)}</div>
        <div class="surface-meta">${a.found_surface_count}/${a.surface_count} 表面 · ${a.bound_source_count} 来源</div>
      </div>
      ${bound ? '<span class="chip chip-confirmed">已绑定</span>' : '<span class="chip chip-info">未绑定</span>'}
    </label>`;
  }).join('');

  // 已有共享组分组展示
  const groupMap = new Map();
  existingBindings.forEach(b => {
    if (b.status !== 'active') return;
    if (!groupMap.has(b.share_group_id)) groupMap.set(b.share_group_id, []);
    groupMap.get(b.share_group_id).push(b);
  });
  const groupsHtml = groupMap.size ? Array.from(groupMap.entries()).map(([gid, binds]) => `<article class="plan-item verified">
    <div class="finding-header">
      <span class="finding-rule">共享组 ${escapeHtml(gid.slice(0, 16))}</span>
      <span class="chip chip-confirmed">${binds.length} 个 Agent</span>
    </div>
    <div class="finding-evidence">${binds.map(b => escapeHtml(b.agent_instance_id)).join(' · ')}</div>
    <div class="finding-actions">
      <button class="btn" type="button" onclick="previewSharedGroup('${escapeHtml(gid)}')">查看共享组预览</button>
    </div>
  </article>`).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>暂无共享组。勾选 Agent 后创建。</p></div>';

  setContent(`<div class="view-heading"><span class="eyebrow">Multi-agent shared MCP</span><h2>多 Agent 共享 MCP 模式</h2>
    <p>勾选多个 Agent，创建共享组绑定，所有 Agent 通过 MemoryGuard MCP 共享同一组记忆。</p></div>
    <section class="card"><div class="card-head"><div><h2>Agent 列表</h2>
      <p>勾选要加入共享组的 Agent。已有绑定的 Agent 默认勾选。</p></div></div>
      <div class="raw-file-list">${agentRowsHtml}</div>
      <div class="finding-actions" style="margin-top:14px">
        <button class="btn btn-primary" type="button" onclick="createSharedBinding()">创建共享组绑定</button>
        <button class="btn" type="button" onclick="exitMultiAgentMode()">退出多 Agent 模式</button>
      </div>
    </section>
    <section class="card"><div class="card-head"><div><h2>已有共享组</h2></div></div>
      ${groupsHtml}
      <div class="finding-actions" style="margin-top:14px">
        <button class="btn" type="button" onclick="renderSources()">← 返回数据源</button>
      </div>
    </section>`);
}

async function createSharedBinding() {
  const checks = document.querySelectorAll('input[type=checkbox][data-agent-id]:checked');
  const agentIds = Array.from(checks).map(c => c.dataset.agentId);
  if (agentIds.length < 2) return showToast('多 Agent 共享组至少需要选择 2 个 Agent', 'error');
  if (!confirm(`确认创建共享组绑定？\n\n· ${agentIds.length} 个 Agent 将通过 MemoryGuard MCP 共享同一组记忆\n· 每个 Agent 的原生记忆模式默认为 observed\n· 可在共享组预览中查看绑定详情`)) return;
  showToast('正在创建绑定…');
  try {
    const result = await callApi('bind_agents_to_shared_group', agentIds);
    if (result.error) return showToast(result.error, 'error');
    showToast(`已创建共享组，绑定 ${agentIds.length} 个 Agent`, 'success');
    showSharedGroupPreview(result.share_group_id, result.preview);
  } catch (e) { showToast('创建失败：' + e, 'error'); }
}

async function previewSharedGroup(groupId) {
  showToast('正在加载共享组预览…');
  try {
    const result = await callApi('get_shared_group_preview', groupId);
    if (result.error) return showToast(result.error, 'error');
    showSharedGroupPreview(groupId, result);
  } catch (e) { showToast('加载失败：' + e, 'error'); }
}

function showSharedGroupPreview(groupId, preview) {
  const bindings = (preview && preview.bindings) || [];
  const memStatus = (preview && preview.memory_status) || {};
  const bindingsHtml = bindings.length ? bindings.map(b => `<article class="plan-item verified">
    <div class="finding-header">
      <span class="finding-rule">${escapeHtml(b.agent_instance_id)}</span>
      <span class="chip chip-${b.status === 'active' ? 'confirmed' : 'medium'}">${escapeHtml(b.status || '')}</span>
    </div>
    <div class="row"><span class="key">binding_id</span><code>${escapeHtml(b.binding_id || '')}</code></div>
    <div class="row"><span class="key">native_mode</span><span>${escapeHtml(b.native_memory_mode || '')}</span></div>
    <div class="row"><span class="key">mcp_server</span><span>${escapeHtml(b.mcp_server_name || '')}</span></div>
    <div class="row"><span class="key">redirect_paths</span><span>${(b.redirect_paths || []).length} 个</span></div>
  </article>`).join('') : '<div class="empty-state"><p>无绑定</p></div>';
  setContent(`<div class="view-heading"><span class="eyebrow">Shared group preview</span><h2>共享组预览</h2>
    <p>共享组 <code>${escapeHtml(groupId)}</code> · ${preview.agent_count || 0} 个 Agent</p></div>
    <section class="card"><div class="card-head"><div><h2>状态摘要</h2></div></div>
      <div class="chips">
        <span class="chip chip-info">agents · ${preview.agent_count || 0}</span>
        <span class="chip chip-confirmed">auto_writes · ${preview.auto_write_count || 0}</span>
        <span class="chip chip-medium">auto_decisions · ${preview.auto_decision_count || 0}</span>
        <span class="chip chip-high">conflicts · ${preview.conflict_count || 0}</span>
        <span class="chip chip-high">quarantine · ${preview.quarantine_count || 0}</span>
      </div>
    </section>
    <section class="card"><div class="card-head"><div><h2>绑定详情</h2></div></div>
      ${bindingsHtml}
      <div class="finding-actions" style="margin-top:14px">
        <button class="btn" type="button" onclick="renderMultiAgentBinding()">← 返回多 Agent 模式</button>
      </div>
    </section>`);
}

async function exitMultiAgentMode() {
  dataPageMode = 'single_agent';
  showToast('已退回单 Agent 模式');
  renderSources();
}


async function discoverAgents() {
  showToast('正在检测本机 Agent…');
  try {
    const result = await callApi('discover_agents');
    if (result.error) return showToast(result.error, 'error');
    discoveryResult = result;
    showDiscoveryResult(result);
  } catch (e) {
    showToast('检测失败：' + e, 'error');
  }
}

function showDiscoveryResult(result) {
  const instances = result.instances || [];
  const ledger = result.discovery_ledger || {};

  // 聚合所有 surface 按 scope 分组：user / project
  const SCOPE_LABEL = { user: '全局/用户', project: '项目' };
  const scopeOrder = ['user', 'project'];
  const surfacesByScope = { user: [], project: [] };
  instances.forEach(inst => {
    (inst.surfaces || []).forEach(s => {
      const scope = s.scope || 'project';
      if (!surfacesByScope[scope]) surfacesByScope[scope] = [];
      surfacesByScope[scope].push({ ...s, product: inst.product, instance_id: inst.instance_id });
    });
  });

  const surfaceRowHtml = (s) => {
    const state = s.status || 'unknown';
    const role = s.surface_role || '';
    const cat = (s.category || '').replace(/_/g, ' ');
    return `<div class="surface-row" title="${escapeHtml(s.surface_id || '')}">
      <span class="surface-icon ${escapeHtml(state)}"></span>
      <div class="surface-path">
        <code>${escapeHtml(s.resolved_path || s.path_template || '')}</code>
        <div class="surface-meta">${escapeHtml(s.product || '')} · ${escapeHtml(s.surface_id || '')} · ${escapeHtml(role)}</div>
      </div>
      <span class="chip chip-${state==='found'?'confirmed':state==='missing'?'medium':state==='unsupported'?'medium':'info'}">${escapeHtml(state)}</span>
      <span class="chip chip-info">${escapeHtml(cat)}</span>
    </div>`;
  };

  const scopeSectionsHtml = scopeOrder.map(scope => {
    const list = surfacesByScope[scope] || [];
    const foundCount = list.filter(s => s.status === 'found').length;
    return `<section class="card">
      <div class="card-head"><div><h2>${SCOPE_LABEL[scope] || scope}</h2>
        <p>${foundCount} / ${list.length} 个表面已发现</p></div></div>
      ${list.length ? list.map(surfaceRowHtml).join('') : '<div class="empty-state" style="min-height:80px"><p>此层级无候选表面</p></div>'}
    </section>`;
  }).join('');

  // Agent 实例摘要
  const instancesHtml = instances.length ? instances.map(inst => {
    const foundCount = (inst.surfaces || []).filter(s => s.status === 'found').length;
    const totalCount = (inst.surfaces || []).length;
    return `<article class="plan-item verified">
      <div class="finding-header">
        <span class="finding-rule">${escapeHtml(inst.product)}</span>
        <span class="chip chip-confirmed">${foundCount}/${totalCount} 表面</span>
        <span class="chip chip-info">${escapeHtml(inst.target_capability || 'export_only')}</span>
      </div>
      <div class="row"><span class="key">profile</span><code>${escapeHtml(inst.profile_id || '')}</code></div>
      <div class="row"><span class="key">platform</span><span>${escapeHtml(inst.platform || '')} · ${escapeHtml(inst.host_id || '')}</span></div>
      <div class="finding-actions">
        <button class="btn btn-primary" type="button" onclick="selectAgentInstance('${escapeHtml(inst.instance_id)}')">勾选授权</button>
      </div>
    </article>`;
  }).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>未检测到任何已安装 Agent。可手工添加文件/文件夹。</p></div>';

  setContent(`<div class="view-heading"><span class="eyebrow">Discovery</span><h2>本机 Agent 检测</h2>
    <p>有限候选发现：只检测 Profile 声明的固定路径，不递归扫描用户主目录，候选阶段不读取正文。结果按 全局/用户 · 项目 两层作用域分组，与 Agent 自身的记忆层级一致。</p></div>
    <section class="card"><div class="card-head"><div><h2>发现账本</h2>
      <p>所有已知表面 100% 进入账本，unaccounted 必须为 0</p></div></div>
      <div class="chips">
        <span class="chip chip-confirmed">found · ${ledger.found || 0}</span>
        <span class="chip chip-medium">missing · ${ledger.missing || 0}</span>
        <span class="chip chip-high">unsupported · ${ledger.unsupported || 0}</span>
        <span class="chip chip-${(ledger.unaccounted_count || 0) === 0 ? 'confirmed' : 'high'}">unaccounted · ${ledger.unaccounted_count || 0}</span>
        <span class="chip chip-info">total · ${ledger.surface_count || 0}</span>
      </div></section>
    ${scopeSectionsHtml}
    <section class="card"><div class="card-head"><div><h2>Agent 实例摘要</h2><p>${instances.length} 个</p></div></div>
      ${instancesHtml}</section>
    <div class="finding-actions" style="margin-top:14px">
      <button class="btn" type="button" onclick="renderSources()">← 返回数据源</button>
    </div>`);
}

async function selectAgentInstance(instanceId) {
  showToast('正在加载分类勾选树…');
  try {
    const result = await callApi('get_selection_tree', instanceId);
    if (result.error) return showToast(result.error, 'error');
    showSelectionTree(instanceId, result);
  } catch (e) { showToast('加载失败：' + e, 'error'); }
}

function showSelectionTree(instanceId, tree) {
  const categories = tree.categories || [];
  const catsHtml = categories.map(cat => {
    const files = (cat.files || []).map(f => {
      const checked = f.default_selected ? 'checked' : '';
      return `<label class="raw-file-row" style="cursor:pointer">
        <input type="checkbox" data-cat="${escapeHtml(cat.category)}" data-path="${escapeHtml(f.path)}" ${checked}>
        <span class="raw-file-path"><code>${escapeHtml(f.path)}</code></span>
        <span class="chip chip-${f.ingestion_policy === 'import_verbatim' ? 'confirmed' : 'info'}">${escapeHtml(f.ingestion_policy || '')}</span>
      </label>`;
    }).join('');
    return `<div style="margin-bottom:14px">
      <div class="finding-header"><span class="finding-rule">${escapeHtml(cat.category)}</span>
        <span class="chip chip-info">${cat.files.length} 个文件</span></div>
      <div class="raw-file-list">${files}</div>
    </div>`;
  }).join('');
  setContent(`<div class="view-heading"><span class="eyebrow">Selection</span><h2>分类勾选授权</h2>
    <p>勾选要纳入治理的表面。原生记忆会被完整接管和备份，普通文档只萃取选中片段。</p></div>
    <section class="card">
      <div class="card-head"><div><h2>授权摘要</h2>
        <p>instance: <code>${escapeHtml(instanceId)}</code></p></div></div>
      <div class="row"><span class="key">ownership</span><span>原生记忆 → agent_managed；普通文档 → external_read_only</span></div>
      <div class="row"><span class="key">backup</span><span>仅原生记忆会做基线备份，普通文档不整库复制</span></div>
    </section>
    <section class="card"><div class="card-head"><div><h2>分类树</h2></div></div>
      ${catsHtml}
      <div class="finding-actions">
        <button class="btn btn-primary" type="button" onclick="confirmSelection('${escapeHtml(instanceId)}')">确认授权</button>
        <button class="btn" type="button" onclick="renderSources()">取消</button>
      </div>
    </section>`);
}

async function confirmSelection(instanceId) {
  const checks = document.querySelectorAll('input[type=checkbox][data-cat]:checked');
  const selected = Array.from(checks).map(c => ({ category: c.dataset.cat, path: c.dataset.path }));
  if (!selected.length) return showToast('请至少勾选一个文件', 'error');
  showToast('正在写入 SelectionManifest…');
  try {
    const result = await callApi('commit_selection', instanceId, selected, true);
    if (result.error) return showToast(result.error, 'error');
    showToast(`已授权 ${selected.length} 个文件，可去神经图构建投影`, 'success');
    renderSources();
  } catch (e) { showToast('授权失败：' + e, 'error'); }
}

async function addSourceDialog() {
  // 使用系统目录选择器（pywebview）或文件选择器
  const result = await callApi('pick_path');
  if (!result || result.error || !result.path) {
    if (result && result.error && result.error !== 'cancelled') showToast(result.error, 'error');
    return;
  }
  const path = result.path;
  const isDir = result.is_directory;
  const name = prompt('显示名称（可留空）：', '') || '';
  showToast('正在添加来源…');
  try {
    const addResult = await callApi('add_source', path, isDir ? 'directory' : 'file', name, true);
    if (addResult.error) return showToast(addResult.error, 'error');
    showToast('来源已添加', 'success');
    renderSources();
  } catch (e) { showToast('添加失败：' + e, 'error'); }
}

async function importBundleDialog() {
  const result = await callApi('pick_path', true);
  if (!result || result.error || !result.path) {
    if (result && result.error && result.error !== 'cancelled') showToast(result.error, 'error');
    return;
  }
  const path = result.path;
  showToast('正在检测导出包…');
  try {
    const preview = await callApi('preview_import', path);
    if (preview.error) {
      showToast(preview.error, 'error');
      return;
    }
    showImportPreview(path, preview);
  } catch (e) {
    showToast('检测失败：' + e, 'error');
  }
}

async function importBundlePrompt() {
  // 兼容旧调用：转发到 importBundleDialog
  await importBundleDialog();
}

function showImportPreview(path, preview) {
  const inv = preview.inventory || {};
  const invText = Object.keys(inv).map(k => `· ${k}: ${JSON.stringify(inv[k]).slice(0, 200)}`).join('\n');
  setContent(`<div class="view-heading"><span class="eyebrow">Import preview</span><h2>离线导出包预览</h2>
    <p>检测到的 provider 和 inventory。确认后导入到 Memory IR。</p></div>
    <section class="card">
      <div class="card-head"><div><h2>检测结果</h2></div>
        <span class="chip chip-confirmed">${escapeHtml(preview.provider || 'unknown')}</span></div>
      <div class="row"><span class="key">path</span><code style="overflow-wrap:anywhere">${escapeHtml(path)}</code></div>
      <div class="row"><span class="key">confidence</span><span>${(preview.confidence || 0) * 100}%</span></div>
      <div class="row"><span class="key">notes</span><span>${escapeHtml(preview.notes || '')}</span></div>
    </section>
    <section class="card">
      <div class="card-head"><div><h2>Inventory</h2><p>检测到的会话/文件清单</p></div></div>
      <pre class="raw-file-content">${escapeHtml(invText || '(empty)')}</pre>
    </section>
    <section class="card">
      <div class="gate-warning">
        <strong>导入会把会话解析为 MemoryRecord，写入 Memory IR。</strong><br>
        原始文件不会被修改。导入后可在"神经图"tab 构建投影查看。
      </div>
      <div class="finding-actions">
        <button class="btn btn-primary" type="button" onclick="confirmImport('${escapeHtml(path).replaceAll("'", "\\'")}')">确认导入</button>
        <button class="btn" type="button" onclick="renderSources()">取消</button>
      </div>
    </section>`);
}

async function confirmImport(path) {
  if (!confirm('确认导入此导出包？\n· 会话解析为 MemoryRecord 写入 IR\n· 原始文件不被修改\n· 可在神经图 tab 构建投影查看')) return;
  showToast('正在导入…');
  try {
    const result = await callApi('create_import', path, true);
    if (result.error) {
      showToast(result.error, 'error');
      return;
    }
    showToast(`导入完成：${result.conversation_count} 个会话 → ${result.memory_record_count} 条记忆`, 'success');
    renderSources();
  } catch (e) {
    showToast('导入失败：' + e, 'error');
  }
}

async function addSourcePrompt() {
  // 兼容旧调用：转发到 addSourceDialog
  await addSourceDialog();
}

async function removeSource(rootId) {
  if (!confirm('移除来源 ' + rootId + '？\n配置会被删除，原始文件不会被改动。')) return;
  try {
    const result = await callApi('remove_source', rootId, true);
    if (result.error) return showToast(result.error, 'error');
    showToast('来源已移除', 'success');
    renderSources();
  } catch (e) { showToast('移除失败：' + e, 'error'); }
}

async function viewSourceFile(rootId, relativePath) {
  try {
    const result = await callApi('get_source_file_content', rootId, relativePath);
    if (result.error) return showToast(result.error, 'error');
    const escaped = escapeHtml(result.content);
    const lines = result.content.split('\n').length;
    const safePath = escapeHtml(relativePath).replaceAll('\\', '/').replaceAll("'", "\\'");
    setContent(`<div class="view-heading"><span class="eyebrow">Raw memory</span><h2>${escapeHtml(result.display_name)} · ${escapeHtml(relativePath).replaceAll('\\', '/')}</h2>
      <p>原始记忆文件，只读查看。size=${result.size} bytes · lines=${lines}</p></div>
      <section class="card"><div class="card-head"><div>
        <button class="btn" type="button" onclick="renderSources()">← 返回数据源</button>
        <button class="btn btn-primary" type="button" onclick="extractSourceFile('${escapeHtml(rootId)}','${safePath}')">萃取为实用记忆</button>
      </div></div>
      <pre class="raw-file-content">${escaped}</pre></section>`);
  } catch (e) { showToast('读取失败：' + e, 'error'); }
}

async function extractSourceFile(rootId, relativePath) {
  showToast('正在萃取预览…');
  try {
    const result = await callApi('extract_preview', rootId, relativePath);
    if (result.error) return showToast(result.error, 'error');
    showExtractPreview(rootId, relativePath, result);
  } catch (e) { showToast('萃取失败：' + e, 'error'); }
}

function showExtractPreview(rootId, relativePath, result) {
  const candidates = result.candidates || [];
  const riskLabel = { high: '高风险', medium: '中风险', low: '低风险' };
  const riskChip = { high: 'high', medium: 'medium', low: 'confirmed' };
  const itemsHtml = candidates.length ? candidates.map((c, i) => `<label class="raw-file-row" style="cursor:pointer;grid-template-columns:auto 1fr auto;align-items:flex-start">
      <input type="checkbox" data-candidate-id="${escapeHtml(c.candidate_id)}" checked>
      <div>
        <div class="finding-rule">#${i + 1} · ${escapeHtml(c.kind || '')}</div>
        <div class="finding-evidence" style="white-space:pre-wrap;margin-top:4px">${escapeHtml(c.preview || c.body || '').slice(0, 300)}</div>
      </div>
      <span class="chip chip-${riskChip[c.risk_level] || 'info'}">${escapeHtml(riskLabel[c.risk_level] || c.risk_level)}</span>
    </label>`).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>未识别到可萃取的记忆片段。</p></div>';
  const safePath = escapeHtml(relativePath).replaceAll('\\', '/').replaceAll("'", "\\'");
  const extractId = escapeHtml(result.extract_id || '');
  setContent(`<div class="view-heading"><span class="eyebrow">Extract preview</span><h2>萃取候选预览</h2>
    <p>从 <code>${escapeHtml(relativePath).replaceAll('\\', '/')}</code> 提取出 ${result.total || 0} 条候选记忆。请审阅后选择接受哪些。</p></div>
    <section class="card"><div class="card-head"><div><h2>候选列表</h2>
      <p>勾选要接受的候选，取消勾选将丢弃。风险等级标注敏感内容或低置信度。</p></div></div>
      <div class="raw-file-list">${itemsHtml}</div>
      <div class="finding-actions" style="margin-top:14px">
        <button class="btn btn-primary" type="button" onclick="acceptExtractCandidates('${extractId}','${escapeHtml(rootId)}','${safePath}')">接受选中</button>
        <button class="btn btn-danger" type="button" onclick="discardExtractCandidates('${escapeHtml(rootId)}','${safePath}')">全部丢弃</button>
      </div>
    </section>`);
}

async function acceptExtractCandidates(extractId, rootId, relativePath) {
  const checks = document.querySelectorAll('input[type=checkbox][data-candidate-id]:checked');
  const candidateIds = Array.from(checks).map(c => c.dataset.candidateId);
  if (!candidateIds.length) return showToast('请至少勾选一个候选', 'error');
  if (!confirm('确认接受 ' + candidateIds.length + ' 条候选记忆并写入共享记忆？')) return;
  showToast('正在写入记忆…');
  try {
    const result = await callApi('accept_candidates', extractId, candidateIds);
    if (result.error) return showToast(result.error, 'error');
    showToast('已接受 ' + result.total + ' 条记忆', 'success');
    showAcceptResult(rootId, relativePath, result);
  } catch (e) { showToast('写入失败：' + e, 'error'); }
}

function discardExtractCandidates(rootId, relativePath) {
  showToast('已丢弃全部候选，staging 文件将在 24 小时后自动清理', 'success');
  viewSourceFile(rootId, relativePath);
}

function showAcceptResult(rootId, relativePath, result) {
  const accepted = result.accepted || [];
  const itemsHtml = accepted.length ? accepted.map((m, i) => `<article class="plan-item verified">
    <div class="finding-header">
      <span class="finding-rule">#${i + 1} · ${escapeHtml(m.kind || '')}</span>
      <span class="chip chip-${m.status === 'active' ? 'confirmed' : 'medium'}">${escapeHtml(m.status || '')}</span>
    </div>
    <div class="row"><span class="key">memory_id</span><code>${escapeHtml(m.memory_id || '')}</code></div>
  </article>`).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>无写入记录。</p></div>';
  const safePath = escapeHtml(relativePath).replaceAll('\\', '/').replaceAll("'", "\\'");
  setContent(`<div class="view-heading"><span class="eyebrow">Accept</span><h2>写入结果</h2>
    <p>已接受 ${result.total || 0} 条记忆，写入共享组 <code>${escapeHtml(result.share_group_id || 'default')}</code>。</p></div>
    <section class="card"><div class="card-head"><div><h2>写入的记忆</h2></div></div>
      ${itemsHtml}
      <div class="finding-actions" style="margin-top:14px">
        <button class="btn" type="button" onclick="viewSourceFile('${escapeHtml(rootId)}','${safePath}')">← 返回源文件</button>
        <button class="btn btn-primary" type="button" onclick="renderSources()">返回数据源</button>
      </div>
    </section>`);
}

// ===========================================================================
// v3 变更记录 tab：BuildPlan + ReleaseChange + apply/verify/rollback
// spec §7.1 / §7.2 MemoryApi
// ===========================================================================

async function renderReleases() {
  setContent('<div class="loading">正在读取变更记录</div>');
  try {
    // v3.1 §8.4：用 list_history 替代 list_releases，包含 rule_change + memory_release + warnings
    const historyResult = await callApi('list_history');
    state.releases = (historyResult.items || []).filter(it => it.record_type === 'memory_release');
    state.ruleChanges = (historyResult.items || []).filter(it => it.record_type === 'rule_change');
    state.historyWarnings = historyResult.warnings || [];
    document.getElementById('releases-count').textContent = historyResult.items ? historyResult.items.length : 0;
    renderReleasesView();
  } catch (e) {
    showToast('变更记录加载失败：' + e, 'error');
    state.releases = [];
    state.ruleChanges = [];
    state.historyWarnings = [];
    renderReleasesView();
  }
}

function renderReleasesView() {
  const releases = state.releases || [];
  // 规则级修复（spec §11.1 保留 v2.1）
  const plans = state.plans || [];
  // v3.1 §8.4：state.ruleChanges 来自旧 changes/ 的兼容读取
  const ruleChanges = state.ruleChanges || [];
  const warnings = state.historyWarnings || [];

  const warningsHtml = warnings.length ? `<section class="card">
    <div class="card-head"><div><h2>历史解析警告</h2>
      <p>${warnings.length} 条历史记录无法解析，单条坏记录不阻断页面</p></div></div>
    ${warnings.map(w => `<div class="raw-file-row" style="cursor:default">
      <span class="raw-file-path"><code>${escapeHtml(w.file_name)}</code></span>
      <span class="chip chip-high">${escapeHtml(w.reason)}</span>
      ${w.missing_keys && w.missing_keys.length ? `<span class="chip chip-medium">missing: ${escapeHtml(w.missing_keys.join(', '))}</span>` : ''}
    </div>`).join('')}
  </section>` : '';

  const plansHtml = plans.length ? plans.map(plan => {
    const status = plan.change ? plan.change.status : 'pending';
    const statusClass = status === 'verified' ? 'confirmed' : status === 'failed' ? 'high' : 'info';
    return `<article class="plan-item ${escapeHtml(status)}"><div class="finding-header">
      <span class="finding-rule">修复计划 ${escapeHtml(plan.plan_id.slice(-8))}</span><span class="chip chip-${statusClass}">${escapeHtml(status)}</span></div>
      <div class="finding-evidence">处理 ${plan.finding_ids.length} 个风险信号 · ${plan.patches.length} 个补丁 · 风险 ${escapeHtml(plan.risk_level)}</div>
      <div class="finding-actions">
        ${status === 'pending' ? `<button class="btn btn-primary" type="button" onclick="applyPlan('${escapeHtml(plan.plan_id)}')">应用并验证</button>` : ''}
        ${status === 'verified' || status === 'applied' ? `<button class="btn btn-danger" type="button" onclick="undoChange('${escapeHtml(plan.change.change_id)}','${escapeHtml(plan.plan_id)}')">撤销变更</button>` : ''}
      </div></article>`;
  }).join('') : (ruleChanges.length ? ruleChanges.map(rc => `<article class="plan-item">
    <div class="finding-header">
      <span class="finding-rule">规则修复 ${escapeHtml((rc.event_id || '').slice(-8))}</span>
      <span class="chip chip-info">rule_change · schema ${escapeHtml(rc.schema_version || '2.1')}</span>
    </div>
    <div class="row"><span class="key">plan_id</span><code>${escapeHtml(rc.plan_id || '')}</code></div>
    <div class="row"><span class="key">applied_at</span><span>${escapeHtml(rc.applied_at || '')}</span></div>
    <div class="row"><span class="key">status</span><span>${escapeHtml(rc.status || '')}</span></div>
  </article>`).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>没有规则级修复记录。</p></div>');

  const releasesHtml = releases.length ? releases.map(r => {
    const status = r.status || 'unknown';
    const statusClass = status === 'verified' ? 'confirmed' : status === 'rolled_back' ? 'medium' : status === 'failed' ? 'high' : 'info';
    return `<article class="plan-item ${escapeHtml(status)}">
      <div class="finding-header">
        <span class="finding-rule">Release ${escapeHtml((r.event_id || '').slice(-8))}</span>
        <span class="chip chip-${statusClass}">${escapeHtml(status)}</span>
      </div>
      <div class="row"><span class="key">build_id</span><code>${escapeHtml((r.build_id || '').slice(-12))}</code></div>
      <div class="row"><span class="key">profile</span><span>${escapeHtml(r.target_profile || '')}</span></div>
      <div class="row"><span class="key">applied_at</span><span>${escapeHtml(r.applied_at || '')}</span></div>
      <div class="row"><span class="key">changed</span><span>${r.changed_count || 0} 个文件</span></div>
      <div class="finding-actions">
        ${status === 'applied' || status === 'verified' ? `<button class="btn" type="button" onclick="verifyRelease('${escapeHtml(r.event_id)}')">重新验证</button>
        <button class="btn btn-danger" type="button" onclick="rollbackRelease('${escapeHtml(r.event_id)}')">回滚</button>` : ''}
      </div>
    </article>`;
  }).join('') : '<div class="empty-state"><div class="empty-orb"></div><p>尚无发布记录。先生成构建计划。</p></div>';

  setContent(`<div class="view-heading"><span class="eyebrow">Releases</span><h2>变更记录</h2>
    <p>两类变更闭环统一时间线。规则级修复（Finding→Plan→Apply→Undo）和发布事务（BuildPlan→Apply→Verify→Rollback）。</p></div>
    ${warningsHtml}
    <section class="card"><div class="card-head"><div><h2>规则级修复</h2><p>对单个 Finding 生成最小补丁，备份后应用，重扫验证，可撤销</p></div></div>
      ${plansHtml}</section>
    <section class="card"><div class="card-head"><div><h2>发布事务</h2><p>从 Memory IR 生成 BuildPlan，展示完整 Diff 后由用户批准</p></div>
      <div class="finding-actions">
        <button class="btn btn-primary" type="button" onclick="createBuildPlan()">生成构建计划</button>
      </div></div>
      <div class="gate-warning" style="margin-top:0">
        <strong>发布会完整替换受管目标文件。</strong>回滚以 ReleaseChange 为单位，每次回滚前会备份当前目标状态。
      </div>
    </section>
    <section class="card"><div class="card-head"><div><h2>发布历史</h2><p>${releases.length} 条 memory_release 记录</p></div></div>
      ${releasesHtml}</section>`);
}

async function createBuildPlan() {
  const targetPath = prompt('目标路径（留空使用默认 .memoryguard/memory-target）：', '') || '';
  showToast('正在生成构建计划…');
  try {
    const plan = await callApi('create_build_plan', targetPath);
    if (plan.error) return showToast(plan.error, 'error');
    state.lastPlan = plan;
    showBuildPlanDetail(plan);
  } catch (e) { showToast('生成失败：' + e, 'error'); }
}

function showBuildPlanDetail(plan) {
  const manifest = plan.manifest || {};
  const diff = plan.diff_preview || {};
  setContent(`<div class="view-heading"><span class="eyebrow">Build plan</span><h2>构建计划 ${escapeHtml((plan.plan_id || '').slice(-8))}</h2>
    <p>请审阅完整 Diff 和覆盖率状态后批准应用。</p></div>
    <section class="card">
      <div class="card-head"><div><h2>完整性</h2><p>BuildManifest 五个完整性条件</p></div>
        <span class="chip chip-${plan.integrity_ok ? 'confirmed' : 'high'}">${plan.integrity_ok ? 'integrity OK' : 'integrity FAIL'}</span></div>
      <div class="row"><span class="key">coverage</span><span>${escapeHtml(plan.coverage_status || '')}</span></div>
      <div class="row"><span class="key">target_profile</span><span>${escapeHtml(plan.target_profile || '')}</span></div>
      <div class="row"><span class="key">published</span><span>${manifest.published_record_count || 0} 条</span></div>
      <div class="row"><span class="key">unaccounted</span><span>${manifest.unaccounted_record_count || 0} 条</span></div>
    </section>
    <section class="card">
      <div class="card-head"><div><h2>Diff 预览</h2><p>受管目标文件变更摘要</p></div></div>
      <pre class="raw-file-content">${escapeHtml(JSON.stringify(diff, null, 2))}</pre>
    </section>
    <section class="card">
      <div class="gate-warning">
        <strong>应用后会完整替换受管目标文件。</strong>系统会先备份当前目标状态，再原子切换，最后复扫验证。
      </div>
      <div class="finding-actions">
        <button class="btn btn-primary" type="button" onclick="applyBuildPlan('${escapeHtml(plan.plan_id)}')">批准并应用</button>
        <button class="btn" type="button" onclick="renderReleases()">取消</button>
      </div>
    </section>`);
}

async function applyBuildPlan(planId) {
  if (!confirm('确认应用构建计划？\n\n· 会先备份当前受管目标文件\n· 原子切换为新内容\n· 复扫验证\n· 可通过回滚恢复')) return;
  showToast('正在应用并验证…');
  try {
    const result = await callApi('apply_build', planId, true);
    if (result.error) return showToast(result.error, 'error');
    showToast('发布已应用并验证', 'success');
    await renderReleases();
  } catch (e) { showToast('应用失败：' + e, 'error'); }
}

async function verifyRelease(releaseId) {
  showToast('正在重新验证…');
  try {
    const result = await callApi('verify_release', releaseId);
    if (result.error) return showToast(result.error, 'error');
    const ok = result.rescan_match && result.hashes_match;
    showToast(ok ? '验证通过' : '验证失败', ok ? 'success' : 'error');
  } catch (e) { showToast('验证失败：' + e, 'error'); }
}

async function rollbackRelease(releaseId) {
  if (!confirm('回滚此发布？\n\n· 会先备份当前目标状态\n· 恢复为应用前的内容\n· 复扫验证')) return;
  showToast('正在回滚…');
  try {
    const result = await callApi('rollback_release', releaseId, true);
    if (result.error) return showToast(result.error, 'error');
    showToast('已回滚', 'success');
    await renderReleases();
  } catch (e) { showToast('回滚失败：' + e, 'error'); }
}

// ===========================================================================
// 治理台 tab：最近写入 / 覆盖记录 / 冲突队列 / 隔离队列 / 版本回滚
// ===========================================================================

function renderGovernance() {
  const tabs = [
    { id: 'recent_events', label: '最近写入' },
    { id: 'supersede', label: '覆盖记录' },
    { id: 'conflicts', label: '冲突队列' },
    { id: 'quarantine', label: '隔离队列' },
    { id: 'rollback', label: '版本回滚' },
  ];
  const tabsHtml = tabs.map(t =>
    `<div class="scope-tab ${t.id === governanceSubTab ? 'active' : ''}" onclick="switchGovernanceSub('${t.id}')">${t.label}</div>`
  ).join('');
  setContent(`<div class="view-heading"><span class="eyebrow">Governance</span><h2>治理台</h2>
    <p>记忆治理操作台：最近写入、覆盖记录、冲突队列、隔离队列、版本回滚。</p></div>
    <div class="scope-tabs">${tabsHtml}</div>
    <div id="governance-content"><div class="loading">正在加载</div></div>`);
  renderGovernanceSub();
}

function switchGovernanceSub(subTab) {
  governanceSubTab = subTab;
  renderGovernance();
}

function renderGovernanceSub() {
  switch (governanceSubTab) {
    case 'recent_events': renderRecentEvents(); break;
    case 'supersede': renderSupersedeChain(); break;
    case 'conflicts': renderConflictQueue(); break;
    case 'quarantine': renderQuarantine(); break;
    case 'rollback': renderRollback(); break;
  }
}

async function renderRecentEvents() {
  const container = document.getElementById('governance-content');
  if (!container) return;
  container.innerHTML = '<div class="loading">正在读取最近写入</div>';
  try {
    const result = await callApi('get_recent_events');
    if (result.error) return showToast(result.error, 'error');
    const events = result.events || [];
    if (!events.length) {
      container.innerHTML = '<div class="card empty-state"><div><div class="empty-orb"></div><p>暂无自动写入事件。</p></div></div>';
      return;
    }
    const items = events.map(e => {
      const preview = escapeHtml((e.raw_content || '').slice(0, 100));
      const actions = (e.auto_actions || []).map(a => `<span class="chip chip-info">${escapeHtml(a.action || a.type || 'auto')}</span>`).join('');
      return `<article class="plan-item" onclick="toggleEventDetail('${escapeHtml(e.event_id)}')">
        <div class="finding-header">
          <span class="finding-rule">${escapeHtml(e.agent_instance_id || 'unknown')}</span>
          <span class="chip chip-info">${escapeHtml(e.created_at || '')}</span>
        </div>
        <div class="finding-evidence">${preview}${(e.raw_content || '').length > 100 ? '…' : ''}</div>
        ${actions ? `<div class="chips" style="margin-top:6px">${actions}</div>` : ''}
        <div class="finding-detail" id="event-detail-${escapeHtml(e.event_id)}" style="display:none">
          <div class="row"><span class="key">event_id</span><code>${escapeHtml(e.event_id || '')}</code></div>
          <div class="row"><span class="key">agent</span><span>${escapeHtml(e.agent_instance_id || '')}</span></div>
          <div class="row"><span class="key">group</span><span>${escapeHtml(e.share_group_id || '')}</span></div>
          <div class="row"><span class="key">时间</span><span>${escapeHtml(e.created_at || '')}</span></div>
          <div class="row"><span class="key">完整内容</span></div>
          <pre class="raw-file-content" style="max-height:300px">${escapeHtml(e.raw_content || '')}</pre>
        </div>
      </article>`;
    }).join('');
    container.innerHTML = `<section class="card"><div class="card-head"><div><h2>最近自动写入</h2>
      <p>最近 ${events.length} 条 MemoryEvent（最多 50 条）</p></div></div>
      ${items}</section>`;
  } catch (e) {
    showToast('加载失败：' + e, 'error');
    container.innerHTML = `<div class="card empty-state"><div><div class="empty-orb"></div><p>加载失败：${escapeHtml(String(e))}</p></div></div>`;
  }
}

function toggleEventDetail(eventId) {
  const el = document.getElementById('event-detail-' + eventId);
  if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

async function renderSupersedeChain() {
  const container = document.getElementById('governance-content');
  if (!container) return;
  container.innerHTML = '<div class="loading">正在读取覆盖记录</div>';
  try {
    const result = await callApi('get_supersede_decisions');
    if (result.error) return showToast(result.error, 'error');
    const decisions = result.decisions || [];
    if (!decisions.length) {
      container.innerHTML = '<div class="card empty-state"><div><div class="empty-orb"></div><p>暂无自动覆盖记录。</p></div></div>';
      return;
    }
    const items = decisions.map(d => `<article class="plan-item">
      <div class="finding-header">
        <span class="finding-rule">覆盖 · ${escapeHtml(d.created_at || '')}</span>
        <span class="chip chip-medium">auto_supersede</span>
      </div>
      <div class="row" style="margin-top:8px"><span class="key">新记忆</span><code>${escapeHtml(d.new_memory_id || '')}</code></div>
      <div class="finding-evidence" style="margin-left:82px">${escapeHtml(d.new_content_preview || '(无内容)')}</div>
      <div class="row" style="margin-top:8px"><span class="key">旧记忆</span><code>${escapeHtml(d.old_memory_id || '')}</code></div>
      <div class="finding-evidence" style="margin-left:82px;color:var(--faint)">${escapeHtml(d.old_content_preview || '(无内容)')}</div>
      <div class="row" style="margin-top:8px"><span class="key">原因</span><span>${escapeHtml(d.reason || '')}</span></div>
    </article>`).join('');
    container.innerHTML = `<section class="card"><div class="card-head"><div><h2>自动覆盖记录</h2>
      <p>共 ${decisions.length} 条 auto_supersede 决策。新记忆 -> 旧记忆覆盖链。</p></div></div>
      ${items}</section>`;
  } catch (e) {
    showToast('加载失败：' + e, 'error');
    container.innerHTML = `<div class="card empty-state"><div><div class="empty-orb"></div><p>加载失败：${escapeHtml(String(e))}</p></div></div>`;
  }
}

async function renderConflictQueue() {
  const container = document.getElementById('governance-content');
  if (!container) return;
  container.innerHTML = '<div class="loading">正在读取冲突队列</div>';
  try {
    const [conflictsResult, memResult] = await Promise.all([
      callApi('get_conflicts'),
      callApi('list_memory'),
    ]);
    if (conflictsResult.error) return showToast(conflictsResult.error, 'error');
    const conflicts = (conflictsResult.conflicts || []).filter(c => c.status === 'unresolved');
    if (!conflicts.length) {
      container.innerHTML = '<div class="card empty-state"><div><div class="empty-orb"></div><p>暂无未解决冲突。</p></div></div>';
      return;
    }
    const records = {};
    (memResult.records || []).forEach(r => { records[r.memory_id] = r; });
    const items = conflicts.map(c => {
      const members = (c.member_ids || []).map(mid => {
        const rec = records[mid];
        const preview = rec ? escapeHtml((rec.body || '').slice(0, 100)) : '(记录不存在)';
        return `<label class="raw-file-row" style="cursor:pointer;grid-template-columns:auto 1fr auto;align-items:center">
          <input type="radio" name="conflict-${escapeHtml(c.group_id)}" value="${escapeHtml(mid)}">
          <div>
            <code>${escapeHtml(mid)}</code>
            <div class="surface-meta">${preview}</div>
          </div>
          <span class="chip chip-${rec ? 'confirmed' : 'high'}">${rec ? escapeHtml(rec.status || 'active') : 'missing'}</span>
        </label>`;
      }).join('');
      return `<article class="plan-item">
        <div class="finding-header">
          <span class="finding-rule">冲突组 ${escapeHtml((c.group_id || '').slice(0, 16))}</span>
          <span class="chip chip-high">${escapeHtml(c.status || 'unresolved')}</span>
        </div>
        <div class="finding-evidence" style="margin-top:6px">原因：${escapeHtml(c.reason || '')}</div>
        <div class="row" style="margin-top:6px"><span class="key">创建时间</span><span>${escapeHtml(c.created_at || '')}</span></div>
        <div class="raw-file-list" style="margin-top:10px">${members}</div>
        <div class="finding-actions" style="margin-top:10px">
          <button class="btn btn-primary" type="button" onclick="resolveConflict('${escapeHtml(c.group_id)}')">保留选中并解决</button>
        </div>
      </article>`;
    }).join('');
    container.innerHTML = `<section class="card"><div class="card-head"><div><h2>冲突队列</h2>
      <p>共 ${conflicts.length} 个未解决冲突组。选择保留哪条，其余将被软删除。</p></div></div>
      ${items}</section>`;
  } catch (e) {
    showToast('加载失败：' + e, 'error');
    container.innerHTML = `<div class="card empty-state"><div><div class="empty-orb"></div><p>加载失败：${escapeHtml(String(e))}</p></div></div>`;
  }
}

async function resolveConflict(groupId) {
  const selected = document.querySelector(`input[name="conflict-${groupId}"]:checked`);
  if (!selected) return showToast('请先选择要保留的记忆', 'error');
  const keepId = selected.value;
  if (!confirm('确认解决冲突？\n\n· 保留记忆：' + keepId + '\n· 其他成员将被软删除')) return;
  showToast('正在解决冲突…');
  try {
    const result = await callApi('resolve_conflict', groupId, keepId);
    if (result.error) return showToast(result.error, 'error');
    showToast('冲突已解决', 'success');
    renderConflictQueue();
  } catch (e) { showToast('解决失败：' + e, 'error'); }
}

async function renderQuarantine() {
  const container = document.getElementById('governance-content');
  if (!container) return;
  container.innerHTML = '<div class="loading">正在读取隔离队列</div>';
  try {
    const result = await callApi('get_quarantine');
    if (result.error) return showToast(result.error, 'error');
    const entries = (result.quarantine || []).filter(e => !e.released);
    if (!entries.length) {
      container.innerHTML = '<div class="card empty-state"><div><div class="empty-orb"></div><p>隔离队列为空。</p></div></div>';
      return;
    }
    const items = entries.map(e => {
      const content = e.original_content || '';
      const masked = content.length > 20
        ? content.slice(0, 6) + '••••••' + content.slice(-4)
        : '••••';
      return `<article class="plan-item">
        <div class="finding-header">
          <span class="finding-rule">隔离 ${escapeHtml((e.quarantine_id || '').slice(0, 16))}</span>
          <span class="chip chip-high">quarantined</span>
        </div>
        <div class="row"><span class="key">memory_id</span><code>${escapeHtml(e.memory_id || '')}</code></div>
        <div class="row"><span class="key">原内容</span><span style="font-family:monospace">${escapeHtml(masked)}</span></div>
        <div class="row"><span class="key">原因</span><span>${escapeHtml(e.reason || '')}</span></div>
        <div class="row"><span class="key">匹配模式</span><code>${escapeHtml(e.detected_pattern || '')}</code></div>
        <div class="row"><span class="key">隔离时间</span><span>${escapeHtml(e.quarantined_at || '')}</span></div>
        <div class="finding-actions" style="margin-top:10px">
          <button class="btn btn-primary" type="button" onclick="releaseQuarantine('${escapeHtml(e.quarantine_id)}')">释放</button>
          <button class="btn btn-danger" type="button" onclick="deleteQuarantine('${escapeHtml(e.quarantine_id)}')">永久删除</button>
        </div>
      </article>`;
    }).join('');
    container.innerHTML = `<section class="card"><div class="card-head"><div><h2>隔离队列</h2>
      <p>共 ${entries.length} 条未释放隔离记忆。敏感内容已脱敏显示。</p></div></div>
      ${items}</section>`;
  } catch (e) {
    showToast('加载失败：' + e, 'error');
    container.innerHTML = `<div class="card empty-state"><div><div class="empty-orb"></div><p>加载失败：${escapeHtml(String(e))}</p></div></div>`;
  }
}

async function releaseQuarantine(quarantineId) {
  if (!confirm('释放此隔离记忆？\n\n· 记忆将恢复为 active 状态\n· 请确认内容安全')) return;
  showToast('正在释放…');
  try {
    const result = await callApi('release_quarantine', quarantineId);
    if (result.error) return showToast(result.error, 'error');
    showToast('已释放', 'success');
    renderQuarantine();
  } catch (e) { showToast('释放失败：' + e, 'error'); }
}

async function deleteQuarantine(quarantineId) {
  if (!confirm('永久删除此隔离记忆？\n\n· 记忆将被标记为 deleted\n· 此操作不可撤销')) return;
  showToast('正在删除…');
  try {
    const result = await callApi('delete_quarantine', quarantineId);
    if (result.error) return showToast(result.error, 'error');
    showToast('已删除', 'success');
    renderQuarantine();
  } catch (e) { showToast('删除失败：' + e, 'error'); }
}

async function renderRollback() {
  const container = document.getElementById('governance-content');
  if (!container) return;
  container.innerHTML = '<div class="loading">正在读取版本历史</div>';
  try {
    const result = await callApi('list_memory_versions');
    if (result.error) return showToast(result.error, 'error');
    const versions = (result.versions || []).slice().sort((a, b) =>
      (b.created_at || '').localeCompare(a.created_at || ''));
    if (!versions.length) {
      container.innerHTML = '<div class="card empty-state"><div><div class="empty-orb"></div><p>暂无版本记录。</p></div></div>';
      return;
    }
    const items = versions.map(v => `<article class="plan-item">
      <div class="finding-header">
        <span class="finding-rule">版本 ${escapeHtml((v.version_id || '').slice(0, 16))}</span>
        <span class="chip chip-info">${escapeHtml(v.created_at || '')}</span>
      </div>
      <div class="row"><span class="key">version_id</span><code>${escapeHtml(v.version_id || '')}</code></div>
      <div class="row"><span class="key">原因</span><span>${escapeHtml(v.reason || '(无)')}</span></div>
      <div class="row"><span class="key">记录数</span><span>${v.record_count || 0} 条（active: ${v.active_count || 0}）</span></div>
      <div class="finding-actions" style="margin-top:10px">
        <button class="btn btn-danger" type="button" onclick="rollbackToVersion('${escapeHtml(v.version_id)}')">回滚到此版本</button>
      </div>
    </article>`).join('');
    container.innerHTML = `<section class="card"><div class="card-head"><div><h2>版本回滚</h2>
      <p>共 ${versions.length} 个版本。回滚前会自动创建当前状态快照。</p></div></div>
      ${items}</section>`;
  } catch (e) {
    showToast('加载失败：' + e, 'error');
    container.innerHTML = `<div class="card empty-state"><div><div class="empty-orb"></div><p>加载失败：${escapeHtml(String(e))}</p></div></div>`;
  }
}

async function rollbackToVersion(versionId) {
  if (!confirm('确认回滚到版本 ' + versionId.slice(0, 16) + '？\n\n· 会先备份当前状态为新版本\n· 恢复为该版本的 records 和 decisions\n· 可通过新版本再次回滚')) return;
  showToast('正在回滚…');
  try {
    const result = await callApi('rollback_memory', versionId);
    if (result.error) return showToast(result.error, 'error');
    showToast('已回滚到目标版本', 'success');
    renderRollback();
  } catch (e) { showToast('回滚失败：' + e, 'error'); }
}

function showToast(message, type) {
  const toast = document.getElementById('toast');
  toast.textContent = message; toast.className = 'toast show ' + (type || '');
  clearTimeout(showToast.timer); showToast.timer = setTimeout(() => toast.className = 'toast', 2600);
}

window.addEventListener('pywebviewready', init);
setTimeout(() => { if (!state.report) init(); }, 1000);
</script>
</body>
</html>"""
