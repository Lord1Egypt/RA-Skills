#!/usr/bin/env python3
"""Generate a self-contained interactive workflow documentation HTML page."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class FlowDocError(ValueError):
    """Raised when a flow document cannot be rendered safely."""


def load_flow_doc(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FlowDocError(f"Invalid JSON at {source}:{exc.lineno}:{exc.colno}: {exc.msg}") from exc
    except OSError as exc:
        raise FlowDocError(f"Could not read {source}: {exc}") from exc
    if not isinstance(data, dict):
        raise FlowDocError("Flow document must be a JSON object.")
    return data


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_text(errors: list[str], obj: dict[str, Any], key: str, where: str) -> None:
    if not _is_text(obj.get(key)):
        errors.append(f"{where}.{key} must be a non-empty string.")


def _validate_id(errors: list[str], value: Any, where: str) -> None:
    if not _is_text(value):
        errors.append(f"{where} must be a non-empty string.")
        return
    if not ID_RE.match(value):
        errors.append(f"{where} must start with a letter or digit and contain only letters, digits, dots, underscores, colons, or hyphens.")


def _as_list(data: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = data.get(key, [])
    if not isinstance(value, list):
        errors.append(f"{key} must be a list.")
        return []
    return value


def validate_flow_doc(data: dict[str, Any]) -> dict[str, Any]:
    """Return a validation report with errors and warnings."""

    errors: list[str] = []
    warnings: list[str] = []

    if not _is_text(data.get("title")):
        warnings.append("title is missing; the rendered page will use a generic title.")
    if not _is_text(data.get("description")):
        warnings.append("description is missing; reviewers may not understand the scope.")

    groups = _as_list(data, "groups", errors)
    group_ids: set[str] = set()
    for index, group in enumerate(groups):
        where = f"groups[{index}]"
        if not isinstance(group, dict):
            errors.append(f"{where} must be an object.")
            continue
        group_id = group.get("id")
        _validate_id(errors, group_id, f"{where}.id")
        _require_text(errors, group, "label", where)
        if _is_text(group_id):
            if group_id in group_ids:
                errors.append(f"{where}.id duplicates group '{group_id}'.")
            group_ids.add(group_id)
        color = group.get("color")
        if color is not None and not (isinstance(color, str) and HEX_RE.match(color)):
            errors.append(f"{where}.color must be a 6-digit hex color such as #2563eb.")

    nodes = _as_list(data, "nodes", errors)
    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        where = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{where} must be an object.")
            continue
        node_id = node.get("id")
        _validate_id(errors, node_id, f"{where}.id")
        _require_text(errors, node, "label", where)
        if _is_text(node_id):
            if node_id in node_ids:
                errors.append(f"{where}.id duplicates node '{node_id}'.")
            node_ids.add(node_id)
        group = node.get("group")
        if group is not None and not _is_text(group):
            errors.append(f"{where}.group must be a string when provided.")
        if _is_text(group) and group_ids and group not in group_ids:
            warnings.append(f"{where}.group references undeclared group '{group}'.")
        if not _is_text(node.get("description")):
            warnings.append(f"{where}.description is missing.")

    if not nodes:
        errors.append("nodes must include at least one package or component.")

    actions = _as_list(data, "actions", errors)
    action_ids: set[str] = set()
    for action_index, action in enumerate(actions):
        where = f"actions[{action_index}]"
        if not isinstance(action, dict):
            errors.append(f"{where} must be an object.")
            continue
        action_id = action.get("id")
        _validate_id(errors, action_id, f"{where}.id")
        _require_text(errors, action, "label", where)
        if _is_text(action_id):
            if action_id in action_ids:
                errors.append(f"{where}.id duplicates action '{action_id}'.")
            action_ids.add(action_id)
        if not _is_text(action.get("summary")):
            warnings.append(f"{where}.summary is missing.")

        steps = action.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{where}.steps must be a non-empty list.")
            continue
        for step_index, step in enumerate(steps):
            step_where = f"{where}.steps[{step_index}]"
            if not isinstance(step, dict):
                errors.append(f"{step_where} must be an object.")
                continue
            _require_text(errors, step, "from", step_where)
            _require_text(errors, step, "to", step_where)
            _require_text(errors, step, "label", step_where)
            for endpoint in ("from", "to"):
                endpoint_id = step.get(endpoint)
                if _is_text(endpoint_id) and endpoint_id not in node_ids:
                    errors.append(f"{step_where}.{endpoint} references unknown node '{endpoint_id}'.")
            if not _is_text(step.get("payload")):
                warnings.append(f"{step_where}.payload is missing; reviewers will not see what crosses the boundary.")
            if not _is_text(step.get("notes")):
                warnings.append(f"{step_where}.notes is missing.")

    if not actions:
        errors.append("actions must include at least one clickable workflow.")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "counts": {"groups": len(groups), "nodes": len(nodes), "actions": len(actions)}}


def _title(data: dict[str, Any]) -> str:
    return str(data.get("title") or "Interactive Workflow Map")


def _safe_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=True, indent=2).replace("</", "<\\/")


def render_html(data: dict[str, Any]) -> str:
    page_title = html.escape(_title(data), quote=True)
    payload = _safe_json(data)
    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__PAGE_TITLE__</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #17202a;
      --muted: #667085;
      --line: #cbd5e1;
      --active: #2563eb;
      --active-soft: #dbeafe;
      --accent: #0f766e;
      --warn: #b45309;
      --border: #d8dee8;
      --shadow: 0 10px 28px rgba(23, 32, 42, 0.08);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
    }
    button, input, textarea, select { font: inherit; letter-spacing: 0; }
    .app-shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: minmax(230px, 280px) minmax(360px, 1fr) minmax(280px, 360px);
      gap: 0;
    }
    .sidebar, .details {
      background: var(--panel);
      border-color: var(--border);
      border-style: solid;
      overflow: auto;
      max-height: 100vh;
    }
    .sidebar { border-width: 0 1px 0 0; }
    .details { border-width: 0 0 0 1px; }
    .sidebar-inner, .details-inner { padding: 20px; }
    .title-block h1 {
      margin: 0 0 8px;
      font-size: 20px;
      line-height: 1.2;
    }
    .title-block p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .section-label {
      margin: 24px 0 10px;
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      font-weight: 700;
    }
    .action-list {
      display: grid;
      gap: 8px;
    }
    .action-button {
      width: 100%;
      border: 1px solid var(--border);
      background: #fff;
      border-radius: 8px;
      padding: 10px 11px;
      text-align: left;
      cursor: pointer;
      min-height: 48px;
    }
    .action-button strong {
      display: block;
      font-size: 13px;
      line-height: 1.25;
    }
    .action-button span {
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.3;
    }
    .action-button.is-active {
      border-color: var(--active);
      background: var(--active-soft);
      box-shadow: inset 3px 0 0 var(--active);
    }
    .canvas-shell {
      position: relative;
      padding: 22px;
      min-width: 0;
      overflow: auto;
    }
    .canvas-board {
      position: relative;
      min-width: 720px;
      min-height: calc(100vh - 44px);
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 22px;
    }
    .flow-svg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: visible;
      z-index: 1;
    }
    .group-grid {
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: repeat(var(--group-count), minmax(180px, 1fr));
      align-items: start;
      gap: 18px;
    }
    .group {
      min-width: 0;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      background: rgba(255, 255, 255, 0.92);
    }
    .group-header {
      display: flex;
      align-items: center;
      gap: 8px;
      min-height: 24px;
      margin-bottom: 10px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }
    .swatch {
      width: 11px;
      height: 11px;
      border-radius: 3px;
      background: var(--group-color, var(--active));
      flex: 0 0 auto;
    }
    .node-list {
      display: grid;
      gap: 10px;
    }
    .node-card {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
      padding: 11px;
      min-height: 84px;
      transition: border-color 140ms ease, box-shadow 140ms ease, background-color 140ms ease;
    }
    .node-card.is-active {
      border-color: var(--active);
      background: #eff6ff;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
    }
    .node-card.is-source {
      box-shadow: inset 3px 0 0 var(--accent), 0 0 0 3px rgba(15, 118, 110, 0.10);
    }
    .node-card.is-target {
      box-shadow: inset 3px 0 0 var(--active), 0 0 0 3px rgba(37, 99, 235, 0.12);
    }
    .node-type {
      color: var(--muted);
      font-size: 11px;
      line-height: 1.2;
      text-transform: uppercase;
      font-weight: 700;
    }
    .node-label {
      margin-top: 5px;
      font-size: 14px;
      line-height: 1.25;
      font-weight: 750;
      overflow-wrap: anywhere;
    }
    .node-description {
      margin-top: 7px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }
    .flow-line {
      fill: none;
      stroke: var(--active);
      stroke-width: 3;
      stroke-linecap: round;
      opacity: 0.95;
    }
    .edge-label {
      font-size: 11px;
      font-weight: 700;
      fill: #17202a;
      paint-order: stroke;
      stroke: #fff;
      stroke-width: 4px;
      stroke-linejoin: round;
    }
    .details h2 {
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
    }
    .details-summary {
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .meta-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 12px;
    }
    .pill {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 5px 8px;
      font-size: 12px;
      color: var(--muted);
      background: #fff;
    }
    .step-list {
      list-style: none;
      padding: 0;
      margin: 18px 0 0;
      display: grid;
      gap: 11px;
    }
    .step-card {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
      padding: 12px;
    }
    .step-card strong {
      display: block;
      font-size: 13px;
      line-height: 1.3;
    }
    .step-card p {
      margin: 7px 0 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }
    .payload {
      margin-top: 9px;
      padding: 8px;
      border-radius: 7px;
      background: #f3f6fa;
      color: #334155;
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }
    .risk {
      margin-top: 9px;
      color: var(--warn);
      font-size: 12px;
      line-height: 1.35;
      font-weight: 650;
    }
    .empty-state {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }
    @media (max-width: 980px) {
      .app-shell { grid-template-columns: 1fr; }
      .sidebar, .details {
        max-height: none;
        border-width: 0 0 1px 0;
      }
      .details { border-width: 1px 0 0 0; }
      .canvas-shell { padding: 14px; }
      .canvas-board { min-width: 680px; min-height: 560px; }
    }
  </style>
</head>
<body>
  <main class="app-shell">
    <aside class="sidebar">
      <div class="sidebar-inner">
        <div class="title-block">
          <h1 data-doc-title></h1>
          <p data-doc-description></p>
        </div>
        <div class="section-label">Actions</div>
        <div class="action-list" data-action-list></div>
      </div>
    </aside>
    <section class="canvas-shell" aria-label="Workflow map">
      <div class="canvas-board" data-canvas-board>
        <svg class="flow-svg" data-flow-svg aria-hidden="true"></svg>
        <div class="group-grid" data-group-grid></div>
      </div>
    </section>
    <aside class="details" aria-live="polite">
      <div class="details-inner" data-details></div>
    </aside>
  </main>
  <script>
    const FLOW_DATA = __FLOW_DATA__;
    const palette = ["#2563eb", "#0f766e", "#7c3aed", "#b45309", "#be123c", "#0369a1"];
    const byId = new Map((FLOW_DATA.nodes || []).map((node) => [node.id, node]));
    let activeActionId = (FLOW_DATA.actions && FLOW_DATA.actions[0] && FLOW_DATA.actions[0].id) || null;

    function text(value, fallback = "") {
      if (value === null || value === undefined) return fallback;
      const output = String(value).trim();
      return output || fallback;
    }

    function shorten(value, limit = 46) {
      const output = text(value);
      if (output.length <= limit) return output;
      return output.slice(0, limit - 1) + "...";
    }

    function activeAction() {
      return (FLOW_DATA.actions || []).find((action) => action.id === activeActionId) || null;
    }

    function nodeRoles(action) {
      const active = new Set();
      const sources = new Set();
      const targets = new Set();
      ((action && action.steps) || []).forEach((step) => {
        active.add(step.from);
        active.add(step.to);
        sources.add(step.from);
        targets.add(step.to);
      });
      return { active, sources, targets };
    }

    function groups() {
      const declared = Array.isArray(FLOW_DATA.groups) ? FLOW_DATA.groups.slice() : [];
      const seen = new Set(declared.map((group) => group.id));
      (FLOW_DATA.nodes || []).forEach((node) => {
        const groupId = node.group || "ungrouped";
        if (!seen.has(groupId)) {
          seen.add(groupId);
          declared.push({ id: groupId, label: groupId === "ungrouped" ? "Ungrouped" : groupId });
        }
      });
      return declared.length ? declared : [{ id: "ungrouped", label: "Ungrouped" }];
    }

    function renderActions() {
      const list = document.querySelector("[data-action-list]");
      list.textContent = "";
      (FLOW_DATA.actions || []).forEach((action) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "action-button";
        button.dataset.actionButton = action.id;
        button.setAttribute("aria-pressed", action.id === activeActionId ? "true" : "false");
        if (action.id === activeActionId) button.classList.add("is-active");
        const label = document.createElement("strong");
        label.textContent = text(action.label, action.id);
        const summary = document.createElement("span");
        summary.textContent = text(action.summary, `${(action.steps || []).length} handoffs`);
        button.append(label, summary);
        button.addEventListener("click", () => selectAction(action.id));
        list.append(button);
      });
    }

    function renderNodes() {
      document.querySelector("[data-doc-title]").textContent = text(FLOW_DATA.title, "Interactive Workflow Map");
      document.querySelector("[data-doc-description]").textContent = text(FLOW_DATA.description, "Click an action to inspect how data moves between packages.");

      const groupGrid = document.querySelector("[data-group-grid]");
      const active = activeAction();
      const roles = nodeRoles(active);
      const groupDefs = groups();
      groupGrid.style.setProperty("--group-count", Math.max(1, groupDefs.length));
      groupGrid.textContent = "";

      groupDefs.forEach((group, index) => {
        const section = document.createElement("section");
        section.className = "group";
        section.dataset.groupId = group.id;
        section.style.setProperty("--group-color", group.color || palette[index % palette.length]);

        const header = document.createElement("div");
        header.className = "group-header";
        const swatch = document.createElement("span");
        swatch.className = "swatch";
        const label = document.createElement("span");
        label.textContent = text(group.label, group.id);
        header.append(swatch, label);

        const nodeList = document.createElement("div");
        nodeList.className = "node-list";
        const nodes = (FLOW_DATA.nodes || []).filter((node) => (node.group || "ungrouped") === group.id);
        nodes.forEach((node) => {
          const card = document.createElement("article");
          card.className = "node-card";
          card.dataset.nodeId = node.id;
          if (roles.active.has(node.id)) card.classList.add("is-active");
          if (roles.sources.has(node.id)) card.classList.add("is-source");
          if (roles.targets.has(node.id)) card.classList.add("is-target");
          const nodeType = document.createElement("div");
          nodeType.className = "node-type";
          nodeType.textContent = text(node.type, "component");
          const nodeLabel = document.createElement("div");
          nodeLabel.className = "node-label";
          nodeLabel.textContent = text(node.label, node.id);
          const description = document.createElement("div");
          description.className = "node-description";
          description.textContent = text(node.description, "No description provided.");
          card.append(nodeType, nodeLabel, description);
          nodeList.append(card);
        });
        section.append(header, nodeList);
        groupGrid.append(section);
      });
    }

    function renderDetails() {
      const action = activeAction();
      const details = document.querySelector("[data-details]");
      details.textContent = "";
      if (!action) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "No action selected.";
        details.append(empty);
        return;
      }
      const heading = document.createElement("h2");
      heading.textContent = text(action.label, action.id);
      const summary = document.createElement("p");
      summary.className = "details-summary";
      summary.textContent = text(action.summary, "Ordered component handoffs for the selected action.");
      const meta = document.createElement("div");
      meta.className = "meta-row";
      [["Trigger", action.trigger], ["Steps", (action.steps || []).length], ["Owner", action.owner]].forEach(([label, value]) => {
        if (value === undefined || value === null || value === "") return;
        const pill = document.createElement("span");
        pill.className = "pill";
        pill.textContent = `${label}: ${value}`;
        meta.append(pill);
      });
      const stepList = document.createElement("ol");
      stepList.className = "step-list";
      stepList.dataset.stepList = action.id;
      (action.steps || []).forEach((step, index) => {
        const source = byId.get(step.from) || { label: step.from };
        const target = byId.get(step.to) || { label: step.to };
        const item = document.createElement("li");
        item.className = "step-card";
        item.dataset.stepId = `${action.id}-${index + 1}`;
        const title = document.createElement("strong");
        title.textContent = `${index + 1}. ${text(source.label, step.from)} -> ${text(target.label, step.to)}: ${text(step.label, "handoff")}`;
        const notes = document.createElement("p");
        notes.textContent = text(step.notes, "No notes provided.");
        const payload = document.createElement("div");
        payload.className = "payload";
        payload.textContent = `Payload: ${text(step.payload, "not documented")}`;
        item.append(title, notes, payload);
        if (text(step.risk)) {
          const risk = document.createElement("div");
          risk.className = "risk";
          risk.textContent = `Review risk: ${text(step.risk)}`;
          item.append(risk);
        }
        stepList.append(item);
      });
      details.append(heading, summary, meta, stepList);
    }

    function drawEdges() {
      const action = activeAction();
      const svg = document.querySelector("[data-flow-svg]");
      const board = document.querySelector("[data-canvas-board]");
      const boardRect = board.getBoundingClientRect();
      svg.setAttribute("viewBox", `0 0 ${boardRect.width} ${boardRect.height}`);
      svg.textContent = "";
      const ns = "http://www.w3.org/2000/svg";
      const defs = document.createElementNS(ns, "defs");
      const marker = document.createElementNS(ns, "marker");
      marker.setAttribute("id", "arrow-head");
      marker.setAttribute("markerWidth", "10");
      marker.setAttribute("markerHeight", "10");
      marker.setAttribute("refX", "8");
      marker.setAttribute("refY", "3");
      marker.setAttribute("orient", "auto");
      marker.setAttribute("markerUnits", "strokeWidth");
      const markerPath = document.createElementNS(ns, "path");
      markerPath.setAttribute("d", "M0,0 L0,6 L9,3 z");
      markerPath.setAttribute("fill", "var(--active)");
      marker.append(markerPath);
      defs.append(marker);
      svg.append(defs);

      ((action && action.steps) || []).forEach((step, index) => {
        const source = document.querySelector(`[data-node-id="${CSS.escape(step.from)}"]`);
        const target = document.querySelector(`[data-node-id="${CSS.escape(step.to)}"]`);
        if (!source || !target) return;
        const sourceRect = source.getBoundingClientRect();
        const targetRect = target.getBoundingClientRect();
        const forward = targetRect.left >= sourceRect.left;
        const startX = (forward ? sourceRect.right : sourceRect.left) - boardRect.left;
        const startY = sourceRect.top + sourceRect.height / 2 - boardRect.top;
        const endX = (forward ? targetRect.left : targetRect.right) - boardRect.left;
        const endY = targetRect.top + targetRect.height / 2 - boardRect.top;
        const gap = Math.max(56, Math.abs(endX - startX) * 0.45);
        const control1X = startX + (forward ? gap : -gap);
        const control2X = endX - (forward ? gap : -gap);
        const offset = (index % 3) * 8;
        const path = document.createElementNS(ns, "path");
        path.classList.add("flow-line", "is-active");
        path.dataset.stepPath = `${action.id}-${index + 1}`;
        path.setAttribute("d", `M ${startX} ${startY + offset} C ${control1X} ${startY + offset}, ${control2X} ${endY - offset}, ${endX} ${endY - offset}`);
        path.setAttribute("marker-end", "url(#arrow-head)");
        svg.append(path);

      });
    }

    function selectAction(id) {
      activeActionId = id;
      document.body.dataset.activeAction = id;
      renderActions();
      renderNodes();
      renderDetails();
      requestAnimationFrame(drawEdges);
    }

    window.addEventListener("resize", () => requestAnimationFrame(drawEdges));
    document.addEventListener("DOMContentLoaded", () => selectAction(activeActionId));
  </script>
</body>
</html>
"""
    return template.replace("__PAGE_TITLE__", page_title).replace("__FLOW_DATA__", payload)


def write_html(data: dict[str, Any], out_path: str | Path) -> Path:
    report = validate_flow_doc(data)
    if not report["ok"]:
        raise FlowDocError("Flow document is invalid:\n- " + "\n- ".join(report["errors"]))
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(data), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an interactive workflow documentation HTML page from JSON.")
    parser.add_argument("--input", required=True, help="Path to the workflow JSON document.")
    parser.add_argument("--out", required=True, help="Path for the generated self-contained HTML file.")
    parser.add_argument("--validation-out", help="Optional path for the JSON validation report.")
    parser.add_argument("--print-summary", action="store_true", help="Print a concise summary after rendering.")
    args = parser.parse_args(argv)

    try:
        data = load_flow_doc(args.input)
        report = validate_flow_doc(data)
        if args.validation_out:
            validation_path = Path(args.validation_out)
            validation_path.parent.mkdir(parents=True, exist_ok=True)
            validation_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        if not report["ok"]:
            raise FlowDocError("Flow document is invalid:\n- " + "\n- ".join(report["errors"]))
        out = write_html(data, args.out)
    except FlowDocError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.print_summary:
        counts = report["counts"]
        print(f"Wrote {out} with {counts['nodes']} nodes and {counts['actions']} actions.")
        if report["warnings"]:
            print(f"Warnings: {len(report['warnings'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
