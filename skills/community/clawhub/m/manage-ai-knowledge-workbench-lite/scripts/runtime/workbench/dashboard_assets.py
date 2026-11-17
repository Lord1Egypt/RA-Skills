"""Dependency-free dashboard templates bundled with the deterministic core."""

from __future__ import annotations


STYLES_CSS = r"""
:root {
  color-scheme: dark;
  --bg-0: #030914;
  --bg-1: #061226;
  --bg-2: #081a35;
  --panel: rgba(8, 23, 49, 0.82);
  --panel-strong: rgba(8, 27, 59, 0.94);
  --panel-soft: rgba(11, 34, 70, 0.68);
  --ink: #f4f8ff;
  --muted: #8fa2c5;
  --line: rgba(89, 131, 211, 0.28);
  --line-hot: rgba(69, 177, 255, 0.62);
  --brand: #4275ff;
  --brand-2: #744cff;
  --neon-cyan: #28dcff;
  --neon-blue: #3f7cff;
  --neon-gold: #ffb85a;
  --good: #39e6b0;
  --warn: #ffb45c;
  --danger: #ff6e91;
  --shadow: 0 22px 60px rgba(0, 5, 18, 0.42);
  --glow: 0 0 28px rgba(48, 148, 255, 0.18);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background:
    radial-gradient(circle at 18% 0%, rgba(46, 93, 222, 0.2), transparent 32%),
    radial-gradient(circle at 90% 10%, rgba(25, 197, 233, 0.12), transparent 28%),
    radial-gradient(circle at 68% 90%, rgba(84, 49, 202, 0.12), transparent 30%),
    linear-gradient(145deg, var(--bg-0), var(--bg-1) 48%, #03101f);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  opacity: .32;
  background-image:
    linear-gradient(rgba(88, 132, 210, .08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(88, 132, 210, .08) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: linear-gradient(to bottom, #000, transparent 92%);
}
a { color: inherit; text-decoration: none; }
button, input { font: inherit; }
.app-shell { min-height: 100vh; display: grid; grid-template-columns: 164px minmax(0, 1fr); }
.side-rail {
  position: sticky;
  top: 0;
  z-index: 8;
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 28px 14px 20px;
  border-right: 1px solid rgba(84, 126, 202, .25);
  background: linear-gradient(180deg, rgba(3, 13, 31, .97), rgba(3, 12, 28, .88));
  backdrop-filter: blur(22px);
  box-shadow: 18px 0 55px rgba(0, 5, 18, .18);
}
.brand-lockup { display: grid; place-items: center; gap: 10px; margin-bottom: 30px; }
.brand-orb {
  position: relative;
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #fff;
  background:
    radial-gradient(circle at 50% 45%, #efffff 0 6%, #63edff 7% 13%, transparent 14%),
    radial-gradient(circle, rgba(46, 118, 255, .68), rgba(5, 17, 42, .96) 64%);
  border: 1px solid rgba(88, 215, 255, .8);
  box-shadow: 0 0 18px rgba(52, 139, 255, .52), inset 0 0 18px rgba(64, 194, 255, .22);
}
.brand-orb::before,
.brand-orb::after {
  content: "";
  position: absolute;
  inset: -7px;
  border: 1px solid rgba(71, 120, 255, .42);
  border-radius: 50%;
  animation: orbit-pulse 3.4s ease-in-out infinite;
}
.brand-orb::after { inset: 8px; border-color: rgba(80, 236, 255, .42); animation-delay: -1.4s; }
.brand-orb span { font-size: 24px; filter: drop-shadow(0 0 8px #5ff1ff); }
.brand-lockup small { color: #7e93bb; font-size: 10px; font-weight: 800; letter-spacing: .16em; }
@keyframes orbit-pulse {
  0%, 100% { transform: scale(.94); opacity: .45; }
  50% { transform: scale(1.08); opacity: 1; }
}
.rail-nav { display: grid; gap: 8px; }
.rail-link {
  display: grid;
  grid-template-columns: 28px 1fr;
  align-items: center;
  gap: 8px;
  min-height: 46px;
  padding: 0 11px;
  border: 1px solid transparent;
  border-radius: 13px;
  color: #91a5ca;
  font-size: 13px;
  transition: .2s ease;
}
.rail-link:hover,
.rail-link.active {
  color: #eef6ff;
  border-color: rgba(60, 131, 255, .5);
  background: linear-gradient(90deg, rgba(48, 104, 255, .28), rgba(27, 185, 240, .08));
  box-shadow: inset 0 0 22px rgba(52, 117, 255, .08), 0 0 20px rgba(40, 113, 255, .08);
}
.rail-icon { color: var(--neon-cyan); font-size: 17px; text-align: center; text-shadow: 0 0 10px rgba(40, 220, 255, .5); }
.privacy-mini {
  margin-top: auto;
  padding: 15px 13px;
  border: 1px solid rgba(75, 126, 218, .34);
  border-radius: 16px;
  background: rgba(8, 28, 62, .72);
  box-shadow: var(--glow);
}
.privacy-mini h3 { margin: 0 0 10px; font-size: 13px; }
.privacy-line { display: flex; gap: 7px; align-items: center; margin-top: 7px; color: #8fa4ca; font-size: 10px; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--good); box-shadow: 0 0 10px var(--good); }
.workspace { min-width: 0; padding: 24px 28px 38px; }
.topbar { display: flex; justify-content: space-between; gap: 24px; align-items: flex-start; margin-bottom: 17px; }
.eyebrow { margin: 0 0 6px; color: var(--neon-cyan); font-size: 11px; font-weight: 850; letter-spacing: .16em; text-transform: uppercase; }
h1 { margin: 0; font-size: clamp(30px, 3vw, 42px); line-height: 1.05; letter-spacing: -.04em; text-shadow: 0 0 32px rgba(73, 129, 255, .22); }
.topbar-copy { margin: 9px 0 0; max-width: 720px; color: var(--muted); font-size: 13px; line-height: 1.6; }
.top-actions { display: grid; justify-items: end; gap: 10px; }
.synthetic-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 999px;
  border: 1px solid rgba(54, 202, 255, .45);
  background: rgba(8, 37, 73, .78);
  color: #dffaff;
  font-size: 12px;
  font-weight: 760;
  box-shadow: 0 0 22px rgba(40, 186, 255, .12);
}
.synthetic-badge::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--neon-cyan); box-shadow: 0 0 10px var(--neon-cyan); }
.meta-strip { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }
.meta-pill { padding: 7px 10px; border: 1px solid rgba(83, 120, 188, .28); border-radius: 10px; background: rgba(7, 24, 52, .68); color: #90a4c8; font-size: 10px; }
.meta-pill strong { margin-left: 5px; color: #e7f2ff; font-weight: 700; }
.toolbar { position: relative; margin-bottom: 15px; }
.toolbar::before { content: "⌕"; position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: var(--neon-cyan); font-size: 18px; }
.toolbar input {
  width: 100%;
  height: 44px;
  padding: 0 16px 0 45px;
  border: 1px solid rgba(77, 124, 204, .3);
  border-radius: 13px;
  outline: none;
  color: var(--ink);
  background: rgba(7, 24, 51, .72);
  box-shadow: inset 0 0 20px rgba(35, 95, 194, .05);
}
.toolbar input::placeholder { color: #64789d; }
.toolbar input:focus { border-color: var(--neon-cyan); box-shadow: 0 0 0 3px rgba(40, 220, 255, .08), 0 0 24px rgba(40, 144, 255, .12); }
.kpis { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 13px; }
.kpi,
.glass-panel {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--line);
  background: linear-gradient(145deg, rgba(10, 31, 66, .94), rgba(5, 19, 43, .84));
  box-shadow: var(--shadow), inset 0 1px 0 rgba(123, 185, 255, .06);
}
.kpi::before,
.glass-panel::before {
  content: "";
  position: absolute;
  left: 12%;
  right: 12%;
  top: -1px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(61, 186, 255, .72), transparent);
}
.kpi {
  min-height: 103px;
  display: grid;
  grid-template-columns: 48px 1fr;
  align-items: center;
  gap: 13px;
  padding: 15px;
  border-radius: 17px;
}
.kpi .kpi-icon { width: 46px; height: 46px; display: grid; place-items: center; border: 1px solid rgba(74, 139, 255, .55); border-radius: 50%; color: var(--neon-cyan); background: radial-gradient(circle, rgba(54, 115, 255, .25), transparent 70%); box-shadow: 0 0 18px rgba(49, 127, 255, .18); font-size: 20px; text-shadow: 0 0 10px rgba(40, 220, 255, .55); }
.kpi span { display: block; color: #8fa4ca; font-size: 11px; }
.kpi strong { display: block; margin-top: 3px; font-size: 25px; letter-spacing: -.03em; }
.kpi small { display: block; margin-top: 4px; color: #587399; font-size: 9px; }
.dashboard-grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; margin-top: 14px; }
.glass-panel { border-radius: 19px; padding: 18px; min-width: 0; }
.span-3 { grid-column: span 3; }
.span-4 { grid-column: span 4; }
.span-5 { grid-column: span 5; }
.span-7 { grid-column: span 7; }
.span-8 { grid-column: span 8; }
.span-12 { grid-column: span 12; }
.panel-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 13px; }
.panel-heading h2 { margin: 0; font-size: 16px; letter-spacing: -.01em; }
.panel-sub { margin: 5px 0 0; color: #7085aa; font-size: 10px; }
.panel-kicker { padding: 5px 8px; border: 1px solid rgba(65, 122, 221, .3); border-radius: 8px; color: #7595cc; font-size: 9px; background: rgba(17, 48, 94, .38); }
.graph-panel,
.project-panel { min-height: 342px; }
.graph {
  position: relative;
  min-height: 280px;
  overflow: hidden;
  border: 1px solid rgba(77, 126, 211, .22);
  border-radius: 15px;
  background:
    radial-gradient(circle at center, rgba(43, 112, 255, .16), transparent 33%),
    linear-gradient(rgba(70, 115, 195, .06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(70, 115, 195, .06) 1px, transparent 1px),
    rgba(2, 13, 34, .62);
  background-size: auto, 28px 28px, 28px 28px, auto;
}
.graph::before,
.graph::after { content: ""; position: absolute; left: 50%; top: 50%; border: 1px solid rgba(57, 115, 234, .18); border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none; }
.graph::before { width: 58%; height: 58%; }
.graph::after { width: 82%; height: 82%; border-style: dashed; opacity: .55; }
.graph svg { position: relative; z-index: 1; display: block; width: 100%; height: 280px; }
.graph-hint { position: absolute; right: 11px; bottom: 10px; z-index: 2; padding: 5px 8px; border-radius: 8px; color: #6f87b0; background: rgba(4, 17, 39, .76); font-size: 9px; }
.edge { stroke: url(#edge-gradient); stroke-width: 1.4; opacity: .72; }
.orbit { fill: none; stroke: rgba(65, 126, 241, .2); stroke-width: 1; stroke-dasharray: 4 7; }
.node-halo { fill: rgba(47, 120, 255, .12); stroke: rgba(62, 177, 255, .22); }
.node { fill: #56cfff; stroke: #d7fbff; stroke-width: 1.2; filter: url(#soft-glow); }
.node.gold { fill: var(--neon-gold); stroke: #ffe1a5; }
.node-label { fill: #dfeaff; stroke: rgba(2, 12, 30, .95); stroke-width: 3px; paint-order: stroke; font-size: 10px; }
.graph-core { fill: rgba(21, 67, 163, .62); stroke: #49dfff; stroke-width: 1.7; filter: url(#strong-glow); }
.graph-star { fill: #ecffff; stroke: #6eeeff; stroke-width: 1; filter: url(#strong-glow); }
.graph-core-label { fill: #9fbfff; stroke: rgba(2, 12, 30, .95); stroke-width: 3px; paint-order: stroke; font-size: 9px; font-weight: 800; letter-spacing: 1.2px; }
.project-list { display: grid; gap: 10px; }
.empty-project { min-height: 248px; display: grid; place-items: center; align-content: center; gap: 10px; text-align: center; color: #758caf; }
.empty-project-orb { position: relative; width: 82px; height: 82px; display: grid; place-items: center; border: 1px solid rgba(61, 151, 255, .5); border-radius: 50%; color: #e9ffff; background: radial-gradient(circle, rgba(45, 122, 255, .38), rgba(5, 20, 46, .3) 65%); box-shadow: 0 0 32px rgba(50, 145, 255, .18), inset 0 0 22px rgba(45, 201, 255, .12); font-size: 28px; text-shadow: 0 0 13px var(--neon-cyan); }
.empty-project-orb::before { content: ""; position: absolute; inset: -10px; border: 1px dashed rgba(79, 130, 229, .34); border-radius: 50%; }
.empty-project strong { color: #c9dcff; font-size: 13px; }
.empty-project small { max-width: 250px; color: #667b9f; font-size: 9px; line-height: 1.55; }
.project {
  display: grid;
  grid-template-columns: 68px 1fr;
  gap: 13px;
  align-items: center;
  padding: 12px;
  border: 1px solid rgba(76, 126, 207, .26);
  border-radius: 14px;
  background: rgba(4, 18, 43, .6);
}
.project-ring { --progress: 0deg; position: relative; width: 62px; height: 62px; display: grid; place-items: center; border-radius: 50%; background: conic-gradient(var(--neon-cyan) var(--progress), rgba(72, 104, 164, .2) 0); box-shadow: 0 0 18px rgba(44, 193, 255, .16); }
.project-ring::before { content: ""; position: absolute; inset: 6px; border-radius: 50%; background: #071a37; border: 1px solid rgba(83, 142, 235, .25); }
.project-ring span { position: relative; z-index: 1; font-size: 14px; font-weight: 800; }
.project-ring.unknown { background: conic-gradient(#536b96 34deg, rgba(72, 104, 164, .2) 0); }
.project-copy { min-width: 0; }
.project-head { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }
.project-head strong { overflow-wrap: anywhere; font-size: 12px; }
.project-copy small { display: block; margin-top: 5px; color: #7186aa; font-size: 9px; line-height: 1.4; }
.progress { height: 4px; margin-top: 9px; border-radius: 999px; background: rgba(68, 94, 146, .3); overflow: hidden; }
.progress i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--neon-blue), var(--neon-cyan)); box-shadow: 0 0 8px var(--neon-cyan); }
.chips { display: flex; flex-wrap: wrap; align-content: flex-start; gap: 8px; }
.chip { display: inline-flex; align-items: center; gap: 7px; padding: 8px 10px; border: 1px solid rgba(68, 127, 225, .38); border-radius: 10px; color: #a9c8ff; background: rgba(15, 52, 105, .42); font-size: 10px; box-shadow: inset 0 0 15px rgba(46, 111, 228, .06); }
.chip b { color: var(--neon-cyan); font-size: 9px; }
.list { display: grid; gap: 8px; }
.row { display: grid; grid-template-columns: 30px minmax(0, 1fr); gap: 10px; align-items: center; padding: 9px 10px; border: 1px solid rgba(72, 117, 194, .2); border-radius: 11px; background: rgba(4, 18, 42, .54); }
.row-icon { width: 28px; height: 28px; display: grid; place-items: center; border: 1px solid rgba(63, 130, 244, .42); border-radius: 8px; color: var(--neon-cyan); background: rgba(28, 77, 163, .26); font-size: 12px; }
.row-copy { min-width: 0; display: grid; gap: 3px; }
.row strong { overflow-wrap: anywhere; font-size: 11px; }
.row small { color: #6f83a8; overflow-wrap: anywhere; font-size: 8px; }
.timeline-row { position: relative; display: grid; grid-template-columns: 12px 1fr; gap: 10px; padding: 6px 0; }
.timeline-row:not(:last-child)::after { content: ""; position: absolute; left: 5px; top: 18px; bottom: -7px; width: 1px; background: linear-gradient(var(--neon-blue), rgba(63, 124, 255, .08)); }
.timeline-dot { position: relative; z-index: 1; width: 11px; height: 11px; margin-top: 3px; border: 2px solid #9ff6ff; border-radius: 50%; background: var(--neon-cyan); box-shadow: 0 0 12px rgba(40, 220, 255, .64); }
.timeline-row:first-child .timeline-dot { border-color: #ffe4b6; background: var(--neon-gold); box-shadow: 0 0 12px rgba(255, 184, 90, .62); }
.timeline-copy { min-width: 0; display: grid; gap: 3px; }
.timeline-copy strong { overflow-wrap: anywhere; font-size: 10px; }
.timeline-copy small { color: #6f83a8; overflow-wrap: anywhere; font-size: 8px; }
.boundary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.boundary-card { position: relative; min-height: 90px; padding: 14px 14px 14px 42px; border: 1px solid rgba(74, 128, 218, .25); border-radius: 13px; background: rgba(5, 20, 46, .58); }
.boundary-card::before { position: absolute; left: 14px; top: 14px; color: var(--good); text-shadow: 0 0 10px rgba(57, 230, 176, .5); }
.boundary-card:nth-child(1)::before { content: "◈"; }
.boundary-card:nth-child(2)::before { content: "◎"; color: var(--neon-cyan); }
.boundary-card:nth-child(3)::before { content: "◇"; color: var(--neon-gold); }
.boundary-card strong { font-size: 11px; }
.boundary-card span { display: block; margin-top: 6px; color: #7085aa; font-size: 9px; line-height: 1.5; }
.muted { color: var(--muted); }
.good { color: var(--good); }
.warn { color: var(--warn); }
.danger { color: var(--danger); }
.empty { min-height: 80px; display: grid; place-items: center; color: #63789e; padding: 16px; text-align: center; font-size: 10px; }
footer { margin-top: 16px; display: flex; justify-content: space-between; gap: 16px; color: #526889; font-size: 9px; }
@media (max-width: 1180px) {
  .app-shell { grid-template-columns: 92px minmax(0, 1fr); }
  .rail-link { grid-template-columns: 1fr; justify-items: center; padding: 7px; }
  .rail-link span:last-child, .brand-lockup small, .privacy-mini { display: none; }
  .span-8, .span-7, .span-5, .span-4, .span-3 { grid-column: span 6; }
}
@media (max-width: 820px) {
  .app-shell { display: block; }
  .side-rail { position: static; width: auto; height: auto; display: flex; flex-direction: row; align-items: center; padding: 12px 16px; border-right: 0; border-bottom: 1px solid var(--line); }
  .brand-lockup { margin: 0 14px 0 0; }
  .brand-orb { width: 42px; height: 42px; }
  .rail-nav { display: flex; overflow-x: auto; }
  .rail-link { min-width: 46px; }
  .workspace { padding: 18px 16px 32px; }
  .topbar { display: grid; }
  .top-actions { justify-items: start; }
  .meta-strip { justify-content: flex-start; }
  .kpis { grid-template-columns: repeat(2, 1fr); }
  .span-8, .span-7, .span-5, .span-4, .span-3, .span-12 { grid-column: span 12; }
  .boundary { grid-template-columns: 1fr; }
}
@media (max-width: 520px) {
  .kpis { grid-template-columns: 1fr; }
  h1 { font-size: 30px; }
  .graph-panel { min-height: 300px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .brand-orb::before, .brand-orb::after { animation: none; }
}
""".strip() + "\n"


APP_JS = r"""
(() => {
  "use strict";
  const embedded = document.getElementById("workbench-data");
  const data = JSON.parse(embedded.textContent);
  const byId = (id) => document.getElementById(id);
  const escapeText = (value) => String(value ?? "");
  const shortPath = (record) => `${record.source_id}/${record.path}`;
  const svgNS = "http://www.w3.org/2000/svg";

  const setText = (id, value) => { byId(id).textContent = escapeText(value); };
  setText("generated", data.generated_at);
  setText("privacy", data.privacy.mode);
  setText("update-mode", data.update.mode);
  setText("source-count", data.summary.files_total);
  setText("visible-count", data.summary.visible_records);
  setText("relation-count", data.summary.relations_total);
  setText("issue-count", data.summary.issues_total);
  setText("excluded-count", data.summary.excluded_sensitive);

  const renderRecords = (records) => {
    const root = byId("records");
    root.replaceChildren();
    if (!records.length) {
      const empty = document.createElement("div");
      empty.className = "empty";
      empty.textContent = "没有匹配的可见记录";
      root.appendChild(empty);
      return;
    }
    records.slice(0, 80).forEach((record) => {
      const row = document.createElement("div");
      row.className = "row";
      const icon = document.createElement("span");
      icon.className = "row-icon";
      icon.textContent = record.type === "project" ? "◇" : "▤";
      const copy = document.createElement("span");
      copy.className = "row-copy";
      const title = document.createElement("strong");
      title.textContent = record.title;
      const meta = document.createElement("small");
      meta.textContent = `${shortPath(record)} · ${record.type || record.kind} · ${record.sensitivity}`;
      copy.append(title, meta);
      row.append(icon, copy);
      root.appendChild(row);
    });
  };

  const renderTopics = () => {
    const root = byId("topics");
    root.replaceChildren();
    data.topics.forEach((topic) => {
      const chip = document.createElement("span");
      chip.className = "chip";
      const label = document.createElement("span");
      label.textContent = topic.label;
      const count = document.createElement("b");
      count.textContent = topic.count;
      chip.append(label, count);
      root.appendChild(chip);
    });
    if (!data.topics.length) root.textContent = "暂无标签";
  };

  const renderProjects = () => {
    const root = byId("projects");
    root.replaceChildren();
    data.projects.forEach((project) => {
      const card = document.createElement("div");
      card.className = "project";
      const known = project.progress.status === "known";
      const value = known ? Math.max(0, Math.min(100, Number(project.progress.value))) : 0;
      const ring = document.createElement("div");
      ring.className = known ? "project-ring" : "project-ring unknown";
      ring.style.setProperty("--progress", `${value * 3.6}deg`);
      const ringValue = document.createElement("span");
      ringValue.textContent = known ? `${value}%` : "?";
      ring.appendChild(ringValue);
      const copy = document.createElement("div");
      copy.className = "project-copy";
      const head = document.createElement("div");
      head.className = "project-head";
      const title = document.createElement("strong");
      title.textContent = project.title;
      const state = document.createElement("span");
      state.className = known ? "good" : "muted";
      state.textContent = known ? "已验证" : "unknown";
      head.append(title, state);
      const basis = document.createElement("small");
      basis.textContent = project.progress.basis || "没有可审计分母";
      copy.append(head, basis);
      if (known) {
        const bar = document.createElement("div");
        bar.className = "progress";
        const fill = document.createElement("i");
        fill.style.width = `${value}%`;
        bar.appendChild(fill);
        copy.appendChild(bar);
      }
      card.append(ring, copy);
      root.appendChild(card);
    });
    if (!data.projects.length) {
      const empty = document.createElement("div");
      empty.className = "empty-project";
      const orb = document.createElement("span");
      orb.className = "empty-project-orb";
      orb.textContent = "✦";
      const title = document.createElement("strong");
      title.textContent = "等待项目证据";
      const note = document.createElement("small");
      note.textContent = "识别到具有可审计分母的项目记录后，将在这里显示真实进度。";
      empty.append(orb, title, note);
      root.appendChild(empty);
    }
  };

  const renderRecent = () => {
    const root = byId("recent");
    root.replaceChildren();
    data.recent_changes.slice(0, 7).forEach((record) => {
      const row = document.createElement("div");
      row.className = "timeline-row";
      const dot = document.createElement("span");
      dot.className = "timeline-dot";
      const copy = document.createElement("span");
      copy.className = "timeline-copy";
      const title = document.createElement("strong");
      title.textContent = record.title;
      const meta = document.createElement("small");
      meta.textContent = `${shortPath(record)} · ${record.updated_at}`;
      copy.append(title, meta);
      row.append(dot, copy);
      root.appendChild(row);
    });
    if (!data.recent_changes.length) root.textContent = "暂无变化";
  };

  const addSvg = (tag, attributes = {}) => {
    const element = document.createElementNS(svgNS, tag);
    Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, value));
    return element;
  };

  const renderGraph = () => {
    const root = byId("graph");
    root.replaceChildren();
    const relations = data.relations.slice(0, 60);
    const related = [...new Set(relations.flatMap((edge) => [edge.from, edge.to]))];
    const fallback = data.records.map((record) => `${record.source_id}/${record.path}`);
    const nodeNames = (related.length ? related : fallback).slice(0, 20);
    if (!nodeNames.length) {
      const empty = document.createElement("div");
      empty.className = "empty";
      empty.textContent = "暂无可见记录或关系";
      root.appendChild(empty);
      return;
    }

    const svg = addSvg("svg", {viewBox: "0 0 900 280", role: "img", "aria-label": "知识关系星图"});
    const defs = addSvg("defs");
    const edgeGradient = addSvg("linearGradient", {id: "edge-gradient", x1: "0%", y1: "0%", x2: "100%", y2: "0%"});
    edgeGradient.append(
      Object.assign(addSvg("stop", {offset: "0%", "stop-color": "#335fff"})),
      Object.assign(addSvg("stop", {offset: "50%", "stop-color": "#28dcff"})),
      Object.assign(addSvg("stop", {offset: "100%", "stop-color": "#7a58ff"}))
    );
    const softGlow = addSvg("filter", {id: "soft-glow", x: "-100%", y: "-100%", width: "300%", height: "300%"});
    softGlow.appendChild(addSvg("feGaussianBlur", {stdDeviation: "3", result: "blur"}));
    const softMerge = addSvg("feMerge");
    softMerge.append(addSvg("feMergeNode", {in: "blur"}), addSvg("feMergeNode", {in: "SourceGraphic"}));
    softGlow.appendChild(softMerge);
    const strongGlow = addSvg("filter", {id: "strong-glow", x: "-120%", y: "-120%", width: "340%", height: "340%"});
    strongGlow.appendChild(addSvg("feGaussianBlur", {stdDeviation: "5", result: "blur"}));
    const strongMerge = addSvg("feMerge");
    strongMerge.append(addSvg("feMergeNode", {in: "blur"}), addSvg("feMergeNode", {in: "SourceGraphic"}));
    strongGlow.appendChild(strongMerge);
    defs.append(edgeGradient, softGlow, strongGlow);
    svg.appendChild(defs);

    svg.append(
      addSvg("ellipse", {class: "orbit", cx: "450", cy: "140", rx: "205", ry: "88"}),
      addSvg("ellipse", {class: "orbit", cx: "450", cy: "140", rx: "340", ry: "122"})
    );
    const positions = new Map();
    nodeNames.forEach((name, index) => {
      const angle = (Math.PI * 2 * index) / nodeNames.length - Math.PI / 2;
      const rx = index % 2 === 0 ? 300 : 220;
      const ry = index % 2 === 0 ? 112 : 82;
      positions.set(name, {x: 450 + Math.cos(angle) * rx, y: 140 + Math.sin(angle) * ry});
    });
    relations.forEach((edge) => {
      if (!positions.has(edge.from) || !positions.has(edge.to)) return;
      const start = positions.get(edge.from);
      const end = positions.get(edge.to);
      svg.appendChild(addSvg("line", {class: "edge", x1: start.x, y1: start.y, x2: end.x, y2: end.y}));
    });
    nodeNames.forEach((name, index) => {
      const position = positions.get(name);
      svg.appendChild(addSvg("circle", {class: "node-halo", cx: position.x, cy: position.y, r: "13"}));
      const circle = addSvg("circle", {class: index % 5 === 4 ? "node gold" : "node", cx: position.x, cy: position.y, r: "5.5"});
      const label = addSvg("text", {class: "node-label", x: position.x + 10, y: position.y + 3});
      label.textContent = name.split("/").pop().slice(0, 24);
      svg.append(circle, label);
    });
    svg.append(
      addSvg("circle", {class: "graph-core", cx: "450", cy: "140", r: "33"}),
      addSvg("circle", {class: "orbit", cx: "450", cy: "140", r: "45"})
    );
    const star = addSvg("polygon", {class: "graph-star", points: "450,115 457,133 475,140 457,147 450,165 443,147 425,140 443,133"});
    const coreLabel = addSvg("text", {class: "graph-core-label", x: "450", y: "184", "text-anchor": "middle"});
    coreLabel.textContent = "AI INDEX";
    svg.append(star, coreLabel);
    root.appendChild(svg);
    const hint = document.createElement("div");
    hint.className = "graph-hint";
    hint.textContent = relations.length ? `${relations.length} 条显式关系` : "记录星图 · 暂无显式关系";
    root.appendChild(hint);
  };

  renderRecords(data.records);
  renderTopics();
  renderProjects();
  renderRecent();
  renderGraph();

  byId("search").addEventListener("input", (event) => {
    const query = event.target.value.trim().toLocaleLowerCase();
    const filtered = !query ? data.records : data.records.filter((record) => {
      const haystack = [record.title, record.path, record.type, ...(record.tags || [])].join(" ").toLocaleLowerCase();
      return haystack.includes(query);
    });
    renderRecords(filtered);
  });
})();
""".strip() + "\n"


INDEX_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <title>AI 自动知识工作台</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <div class="app-shell">
    <aside class="side-rail">
      <div class="brand-lockup">
        <div class="brand-orb" aria-hidden="true"><span>✦</span></div>
        <small>AI WORKBENCH</small>
      </div>
      <nav class="rail-nav" aria-label="工作台导航">
        <a class="rail-link active" href="#overview"><span class="rail-icon">▦</span><span>总览</span></a>
        <a class="rail-link" href="#knowledge-graph"><span class="rail-icon">⌬</span><span>知识图谱</span></a>
        <a class="rail-link" href="#project-center"><span class="rail-icon">◇</span><span>项目状态</span></a>
        <a class="rail-link" href="#topic-library"><span class="rail-icon">◫</span><span>主题聚合</span></a>
        <a class="rail-link" href="#record-center"><span class="rail-icon">▤</span><span>记录中心</span></a>
      </nav>
      <section class="privacy-mini" aria-label="隐私状态">
        <h3>隐私状态</h3>
        <div class="privacy-line"><span class="status-dot"></span><span>源目录只读</span></div>
        <div class="privacy-line"><span class="status-dot"></span><span>正文不嵌入</span></div>
        <div class="privacy-line"><span class="status-dot"></span><span>本地派生输出</span></div>
      </section>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">Local-first · AI-derived knowledge cockpit</p>
          <h1>AI 自动知识工作台</h1>
          <p class="topbar-copy">AI 负责规划和推进，确定性引擎负责扫描、校验与渲染。原始资料保持只读，页面仅展示允许的派生元数据。</p>
        </div>
        <div class="top-actions">
          <div class="synthetic-badge">合成演示数据</div>
          <div class="meta-strip">
            <span class="meta-pill">生成<strong id="generated">-</strong></span>
            <span class="meta-pill">隐私<strong id="privacy">-</strong></span>
            <span class="meta-pill">更新<strong id="update-mode">-</strong></span>
          </div>
        </div>
      </header>

      <div class="toolbar"><input id="search" type="search" placeholder="搜索标题、相对路径、类型或标签" aria-label="搜索可见记录"></div>

      <section id="overview" class="kpis" aria-label="工作台总览">
        <article class="kpi"><span class="kpi-icon">◫</span><div><span>源记录</span><strong id="source-count">0</strong><small>受控扫描</small></div></article>
        <article class="kpi"><span class="kpi-icon">◎</span><div><span>可见记录</span><strong id="visible-count">0</strong><small>派生视图</small></div></article>
        <article class="kpi"><span class="kpi-icon">⌁</span><div><span>可见关系</span><strong id="relation-count">0</strong><small>显式链接</small></div></article>
        <article class="kpi"><span class="kpi-icon">⚡</span><div><span>检查问题</span><strong id="issue-count">0</strong><small>质量校验</small></div></article>
        <article class="kpi"><span class="kpi-icon">⊘</span><div><span>敏感排除</span><strong id="excluded-count">0</strong><small>默认隐藏</small></div></article>
      </section>

      <section class="dashboard-grid">
        <article id="knowledge-graph" class="glass-panel graph-panel span-8">
          <div class="panel-heading"><div><h2>AI 知识星图</h2><p class="panel-sub">可见记录与已解析显式关系</p></div><span class="panel-kicker">LOCAL GRAPH</span></div>
          <div id="graph" class="graph"></div>
        </article>

        <article id="project-center" class="glass-panel project-panel span-4">
          <div class="panel-heading"><div><h2>项目状态</h2><p class="panel-sub">只显示具有证据分母的进度</p></div><span class="panel-kicker">EVIDENCE</span></div>
          <div id="projects" class="project-list"></div>
        </article>

        <article id="recent-changes" class="glass-panel span-5">
          <div class="panel-heading"><div><h2>最近变化</h2><p class="panel-sub">文件活动不等同于业务进度</p></div><span class="panel-kicker">ACTIVITY</span></div>
          <div id="recent" class="list"></div>
        </article>

        <article id="topic-library" class="glass-panel span-3">
          <div class="panel-heading"><div><h2>知识主题</h2><p class="panel-sub">按可见记录标签聚合</p></div><span class="panel-kicker">TOPICS</span></div>
          <div id="topics" class="chips"></div>
        </article>

        <article id="record-center" class="glass-panel span-4">
          <div class="panel-heading"><div><h2>可见记录</h2><p class="panel-sub">最多 80 条，可通过搜索过滤</p></div><span class="panel-kicker">RECORDS</span></div>
          <div id="records" class="list"></div>
        </article>

        <article id="privacy-boundary" class="glass-panel span-12">
          <div class="panel-heading"><div><h2>数据与权限边界</h2><p class="panel-sub">工作台是可重建派生视图，不是事实源或远程数据库</p></div><span class="panel-kicker">PRIVACY</span></div>
          <div class="boundary">
            <div class="boundary-card"><strong>原始资料</strong><span>保留在用户指定目录，默认只读，不由工作台改写。</span></div>
            <div class="boundary-card"><strong>知识与 HTML</strong><span>均为本地生成、可删除并可重新构建的派生产物。</span></div>
            <div class="boundary-card"><strong>正文与敏感数据</strong><span>正文不嵌入页面；敏感记录不进入可见视图。</span></div>
          </div>
        </article>
      </section>
      <footer><span>AI Knowledge Workbench · Offline-first interface</span><span>Metadata-only · Read-only sources</span></footer>
    </main>
  </div>
  <script id="workbench-data" type="application/json">__EMBEDDED_DATA__</script>
  <script src="assets/app.js" defer></script>
</body>
</html>
"""
