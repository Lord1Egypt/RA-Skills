#!/usr/bin/env python3
"""Render a Life Fork markdown report to mobile-friendly HTML."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


LEGACY_RESULT_HEADER = "".join(("人", "生", "线"))


CSS = """
:root {
  --ink: #1f2933;
  --muted: #64748b;
  --line: #d9e2ec;
  --soft: #f7f5ef;
  --paper: #fffdf8;
  --card: #ffffff;
  --accent: #245b77;
  --accent-2: #8a6f3d;
  --good: #2f6f63;
  --shadow: 0 18px 45px rgba(31, 41, 51, 0.10);
}

@page {
  size: A4;
  margin: 18mm 16mm 18mm 16mm;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: var(--ink);
  background-color: #f4f1e8;
  background-image:
    linear-gradient(180deg, rgba(255, 255, 255, 0.74), rgba(255, 255, 255, 0.92)),
    repeating-linear-gradient(90deg, rgba(36, 91, 119, 0.06) 0 1px, transparent 1px 46px),
    repeating-linear-gradient(180deg, rgba(138, 111, 61, 0.05) 0 1px, transparent 1px 46px);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
  font-size: 15px;
  line-height: 1.68;
  overflow-x: hidden;
}

.page {
  counter-reset: report-section;
  max-width: 1080px;
  margin: 0 auto;
  overflow-x: hidden;
  padding: 28px 18px 54px;
  width: 100%;
}

.cover {
  background: var(--paper);
  border: 1px solid rgba(36, 91, 119, 0.18);
  border-radius: 18px;
  box-shadow: var(--shadow);
  display: grid;
  gap: 24px;
  grid-template-columns: minmax(0, 1.12fr) minmax(320px, 0.88fr);
  margin-bottom: 18px;
  overflow: hidden;
  padding: 28px 26px;
}

.hit-cover {
  align-content: center;
  grid-template-columns: minmax(0, 1fr);
  min-height: calc(100vh - 28px);
  page-break-after: always;
  padding: 30px;
}

.hit-hero {
  display: grid;
  gap: 18px;
}

.hit-line {
  color: #17384a;
  font-size: 32px;
  font-weight: 900;
  letter-spacing: 0;
  line-height: 1.24;
  margin: 0;
  max-width: 900px;
}

.core-judgement {
  color: #355466;
  font-size: 16px;
  line-height: 1.72;
  margin: 0;
  max-width: 880px;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero-pill {
  background: #eef6f5;
  border: 1px solid rgba(36, 91, 119, 0.16);
  border-radius: 999px;
  color: #295a63;
  font-size: 13px;
  font-weight: 760;
  padding: 7px 12px;
}

.verdict-cover {
  display: grid;
  gap: 24px;
}

.verdict-line {
  color: #163447;
  font-size: 35px;
  font-weight: 930;
  letter-spacing: 0;
  line-height: 1.22;
  margin: 0;
  max-width: 920px;
}

.verdict-helps {
  background: #f7f5ef;
  border: 1px solid rgba(36, 91, 119, 0.14);
  border-radius: 14px;
  color: #334e68;
  font-size: 16px;
  line-height: 1.7;
  margin: 0;
  padding: 15px 17px;
}

.named-lines {
  border: 1px solid rgba(36, 91, 119, 0.16);
  border-radius: 16px;
  overflow: hidden;
}

.named-line {
  display: grid;
  gap: 14px;
  grid-template-columns: minmax(130px, 0.55fr) repeat(3, minmax(0, 1fr));
  padding: 15px 17px;
}

.named-line + .named-line {
  border-top: 1px solid rgba(36, 91, 119, 0.12);
}

.named-line:nth-child(odd) {
  background: rgba(247, 245, 239, 0.64);
}

.named-line-title {
  color: #17384a;
  font-size: 16px;
  font-weight: 920;
  line-height: 1.35;
}

.named-line-cell {
  color: #48606f;
  font-size: 13px;
  line-height: 1.55;
}

.named-line-cell strong {
  color: #245b77;
  display: block;
  font-size: 12px;
  font-weight: 860;
  margin-bottom: 3px;
}

.life-line-chart,
.variable-chart,
.attribution-chart,
.action-timeline {
  display: grid;
  gap: 12px;
  margin: 1em 0 1.2em;
}

.life-line-chart {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.life-line-card,
.variable-chip-card,
.attribution-card,
.action-step {
  background: linear-gradient(180deg, rgba(255, 253, 248, 0.96), rgba(247, 245, 239, 0.72));
  border: 1px solid rgba(36, 91, 119, 0.15);
  border-radius: 14px;
  min-width: 0;
  padding: 14px 15px;
}

.life-line-card h3,
.variable-chip-card h3,
.attribution-card h3 {
  color: #17384a;
  font-size: 16px;
  font-weight: 920;
  line-height: 1.35;
  margin: 0 0 12px;
}

.mini-label {
  color: var(--accent);
  display: block;
  font-size: 12px;
  font-weight: 860;
  margin: 9px 0 3px;
}

.shock-anchor-label {
  background: rgba(36, 91, 119, 0.08);
  border: 1px solid rgba(36, 91, 119, 0.14);
  border-radius: 999px;
  color: var(--accent);
  display: inline-flex;
  font-size: 11px;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 8px;
  padding: 5px 8px;
}

.mini-text {
  color: #405869;
  font-size: 13px;
  line-height: 1.56;
  margin: 0;
}

.variable-chart {
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.variable-chip-card {
  border-top: 4px solid rgba(36, 91, 119, 0.55);
}

.variable-chip-card .mini-text {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  overflow: hidden;
}

.attribution-chart {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.attribution-card {
  position: relative;
}

.attribution-card::before {
  background: linear-gradient(180deg, var(--accent), var(--accent-2));
  border-radius: 999px;
  content: "";
  height: 30px;
  position: absolute;
  right: 14px;
  top: 14px;
  width: 4px;
}

.action-timeline {
  counter-reset: action-step;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.action-step {
  display: grid;
  gap: 10px;
  position: relative;
}

.action-step::before {
  align-items: center;
  background: #17384a;
  border-radius: 999px;
  color: #fffdf8;
  content: counter(action-step);
  counter-increment: action-step;
  display: inline-flex;
  font-size: 12px;
  font-weight: 900;
  height: 28px;
  justify-content: center;
  width: 28px;
}

.action-week {
  color: #17384a;
  font-size: 15px;
  font-weight: 920;
  line-height: 1.35;
}

.action-main {
  color: #334e68;
  font-size: 13px;
  line-height: 1.58;
}

.action-output,
.action-threshold {
  background: rgba(255, 255, 255, 0.64);
  border: 1px solid rgba(36, 91, 119, 0.12);
  border-radius: 10px;
  color: #48606f;
  font-size: 12px;
  line-height: 1.5;
  padding: 8px 9px;
}

.variable-board {
  background: rgba(255, 253, 248, 0.96);
  border: 1px solid rgba(36, 91, 119, 0.14);
  border-radius: 16px;
  box-shadow: 0 10px 28px rgba(31, 41, 51, 0.06);
  margin: 0 0 18px;
  padding: 18px;
}

.variable-board-head {
  align-items: center;
  display: flex;
  gap: 12px;
  justify-content: space-between;
  margin-bottom: 14px;
}

.variable-board-title {
  color: #17384a;
  font-size: 20px;
  font-weight: 900;
  line-height: 1.25;
}

.variable-board-note {
  color: var(--muted);
  font-size: 13px;
}

.variable-grid {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.variable-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 12px;
  min-width: 0;
  padding: 12px;
}

.variable-name {
  color: var(--accent);
  display: block;
  font-size: 14px;
  font-weight: 900;
  line-height: 1.25;
  margin-bottom: 8px;
}

.variable-meter {
  background: #edf2f4;
  border-radius: 999px;
  display: block;
  height: 8px;
  margin-bottom: 9px;
  overflow: hidden;
}

.variable-meter::before {
  background: linear-gradient(90deg, #245b77, #9fd6d0);
  border-radius: inherit;
  content: "";
  display: block;
  height: 100%;
  width: var(--bar-width, 60%);
}

.variable-text {
  color: #48606f;
  display: -webkit-box;
  font-size: 12px;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-height: 1.48;
  overflow: hidden;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.cover-copy,
.cover-card,
.fork-panel,
.route-lane,
.report-section {
  max-width: 100%;
  min-width: 0;
}

.eyebrow {
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  margin: 0 0 8px;
}

h1, h2, h3, h4 {
  color: var(--ink);
  line-height: 1.28;
  margin: 1.15em 0 0.55em;
  overflow-wrap: anywhere;
  page-break-after: avoid;
  word-break: break-word;
}

h1 {
  font-size: 34px;
  margin-top: 0;
}

h2 {
  border: 0;
  color: #1b3343;
  font-size: 22px;
  margin-top: 0;
  padding-top: 0;
}

h3 {
  color: var(--accent);
  font-size: 16px;
}

h4 {
  font-size: 14px;
}

p {
  margin: 0.45em 0 0.9em;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.cover-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 22px;
}

.cover-card {
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px 14px;
}

.cover-label {
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 6px;
}

.cover-value {
  color: #263947;
  display: -webkit-box;
  font-size: 13px;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  line-height: 1.58;
  max-width: 100%;
  overflow: hidden;
  overflow-wrap: anywhere;
  white-space: normal;
  word-break: break-word;
}

.confidence-meter {
  background: #e9edf0;
  border-radius: 999px;
  height: 8px;
  margin-top: 10px;
  overflow: hidden;
}

.confidence-meter span {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border-radius: inherit;
  display: block;
  height: 100%;
}

.fork-panel {
  align-self: stretch;
  background:
    linear-gradient(135deg, #172a36 0%, #213b49 50%, #544626 100%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
  color: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 18px;
  justify-content: space-between;
  min-height: 320px;
  padding: 20px;
}

.fork-kicker {
  color: rgba(248, 250, 252, 0.72);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  margin: 0 0 6px;
}

.fork-title {
  font-size: 22px;
  font-weight: 800;
  line-height: 1.25;
  margin: 0;
}

.fork-subtitle {
  color: rgba(248, 250, 252, 0.78);
  font-size: 13px;
  margin: 10px 0 0;
}

.route-map {
  display: grid;
  gap: 12px;
}

.route-lane {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  padding: 12px;
}

.route-label {
  color: rgba(248, 250, 252, 0.82);
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 10px;
}

.route-name {
  color: #ffffff;
  display: block;
  font-size: 16px;
  font-weight: 800;
  line-height: 1.35;
  margin-bottom: 8px;
  max-width: 100%;
  overflow-wrap: anywhere;
  white-space: normal;
  word-break: break-word;
}

.route-bars {
  display: grid;
  gap: 6px;
}

.route-bar {
  align-items: center;
  display: grid;
  gap: 8px;
  grid-template-columns: 38px 1fr;
}

.route-bar span {
  color: rgba(248, 250, 252, 0.78);
  font-size: 12px;
  font-weight: 700;
}

.route-bar strong {
  background: rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  display: block;
  height: 8px;
  overflow: hidden;
}

.route-bar strong::before {
  background: linear-gradient(90deg, #f6d88f, #9fd6d0);
  border-radius: inherit;
  content: "";
  display: block;
  height: 100%;
  width: var(--bar-width, 64%);
}

.route-note {
  background: rgba(255, 255, 255, 0.10);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 10px;
  color: rgba(248, 250, 252, 0.9);
  font-size: 12px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-height: 1.5;
  margin-top: 10px;
  max-width: 100%;
  overflow: hidden;
  overflow-wrap: anywhere;
  padding: 8px 10px;
  white-space: normal;
  word-break: break-word;
}

.chart-panel {
  background: rgba(255, 253, 248, 0.96);
  border: 1px solid rgba(36, 91, 119, 0.14);
  border-radius: 16px;
  box-shadow: 0 10px 28px rgba(31, 41, 51, 0.06);
  margin: 0 0 18px;
  padding: 18px;
}

.chart-title {
  color: #1b3343;
  font-size: 18px;
  font-weight: 850;
  line-height: 1.25;
  margin: 0 0 12px;
}

.view-chart {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.view-name {
  color: var(--accent);
  display: block;
  font-size: 13px;
  font-weight: 850;
  margin-bottom: 8px;
}

.view-path {
  background: #eef6f5;
  border-radius: 999px;
  color: #315b57;
  display: inline-block;
  font-size: 12px;
  font-weight: 750;
  margin-bottom: 10px;
  padding: 4px 8px;
}

.view-meter {
  display: grid;
  gap: 6px;
}

.view-meter-row {
  align-items: center;
  display: grid;
  gap: 6px;
  grid-template-columns: 34px 1fr;
}

.view-meter-row span {
  color: var(--muted);
  font-size: 11px;
  font-weight: 750;
}

.view-meter-row strong {
  background: #edf2f4;
  border-radius: 999px;
  display: block;
  height: 7px;
  overflow: hidden;
}

.view-meter-row strong::before {
  background: linear-gradient(90deg, #245b77, #9fd6d0);
  border-radius: inherit;
  content: "";
  display: block;
  height: 100%;
  width: var(--bar-width, 60%);
}

.event-timeline {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.event-time {
  color: var(--accent);
  display: block;
  font-size: 12px;
  font-weight: 850;
  margin: 4px 0 8px;
}

.event-name {
  color: #1f2933;
  display: block;
  font-size: 13px;
  font-weight: 850;
  line-height: 1.35;
}

.event-impact {
  color: #48606f;
  display: -webkit-box;
  font-size: 12px;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-height: 1.5;
  margin-top: 8px;
  overflow: hidden;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.fork-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.fork-chip {
  background: rgba(255, 255, 255, 0.10);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  color: rgba(248, 250, 252, 0.88);
  font-size: 12px;
  padding: 5px 9px;
}

.report-section {
  background: var(--card);
  border: 1px solid rgba(217, 226, 236, 0.95);
  border-radius: 16px;
  box-shadow: 0 10px 28px rgba(31, 41, 51, 0.06);
  margin: 16px 0;
  padding: 22px 24px;
  overflow: hidden;
  position: relative;
}

.report-section::before {
  background: linear-gradient(180deg, var(--accent), var(--accent-2));
  content: "";
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 5px;
}

.report-section h2 {
  align-items: center;
  display: flex;
  gap: 10px;
}

.report-section h2::before {
  align-items: center;
  background: #eaf2f4;
  border: 1px solid rgba(36, 91, 119, 0.18);
  border-radius: 999px;
  color: var(--accent);
  content: counter(report-section, decimal-leading-zero);
  counter-increment: report-section;
  display: inline-flex;
  flex: 0 0 auto;
  font-size: 11px;
  height: 26px;
  justify-content: center;
  width: 36px;
}

ul, ol {
  margin: 0.4em 0 1em 1.35em;
  padding: 0;
}

li {
  margin: 0.22em 0;
}

blockquote {
  background: var(--soft);
  border-left: 4px solid var(--accent);
  color: #334e68;
  margin: 1em 0;
  padding: 10px 14px;
}

code {
  background: #eef2f7;
  border-radius: 4px;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 12px;
  padding: 1px 4px;
}

pre {
  background: #17202a;
  border-radius: 8px;
  color: white;
  font-size: 12px;
  line-height: 1.55;
  overflow-wrap: break-word;
  padding: 12px 14px;
  white-space: pre-wrap;
}

pre code {
  background: transparent;
  color: inherit;
  padding: 0;
}

table {
  border-collapse: collapse;
  font-size: 12.5px;
  margin: 0;
  page-break-inside: avoid;
  width: 100%;
}

.table-wrap {
  background: linear-gradient(180deg, rgba(247, 245, 239, 0.72), rgba(255, 255, 255, 0.92));
  border: 1px solid var(--line);
  border-radius: 12px;
  margin: 1em 0 1.2em;
  overflow-x: auto;
}

th, td {
  border: 1px solid var(--line);
  overflow-wrap: anywhere;
  padding: 7px 8px;
  text-align: left;
  vertical-align: top;
  word-break: break-word;
}

th {
  background: var(--soft);
  color: #334e68;
  font-weight: 700;
}

tbody tr:nth-child(even) td {
  background: rgba(247, 245, 239, 0.42);
}

td:first-child,
th:first-child {
  color: #1f4f68;
  font-weight: 750;
}

hr {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 24px 0;
}

.footer {
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 11px;
  margin-top: 36px;
  padding-top: 12px;
}

@media (max-width: 720px) {
  body {
    font-size: 14px;
  }

  .page {
    margin: 0;
    max-width: 390px;
    padding: 14px 10px 38px;
  }

  .cover,
  .report-section {
    border-radius: 12px;
    padding: 18px 16px;
  }

  .cover {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 24px;
  }

  .hit-line {
    font-size: 24px;
  }

  .verdict-line {
    font-size: 26px;
  }

  h2 {
    font-size: 20px;
  }

  .named-line {
    gap: 8px;
    grid-template-columns: 1fr;
  }

  .life-line-chart,
  .variable-chart,
  .attribution-chart,
  .action-timeline {
    grid-template-columns: 1fr;
  }

  .variable-board-head {
    align-items: start;
    flex-direction: column;
  }

  .variable-grid {
    grid-template-columns: 1fr;
  }

  .cover-grid {
    grid-template-columns: 1fr;
  }

  .view-chart,
  .event-timeline {
    grid-template-columns: 1fr;
  }

  .fork-panel {
    min-height: 280px;
  }
}

@media print {
  body {
    background: white;
    font-size: 13.5px;
  }

  .page {
    max-width: none;
    padding: 0;
  }

  .cover,
  .report-section {
    border: 0;
    border-radius: 0;
    box-shadow: none;
    margin: 0 0 18px;
    padding: 0;
  }

  .cover {
    border-bottom: 2px solid var(--accent);
    display: block;
    padding-bottom: 18px;
  }

  .fork-panel {
    box-shadow: none;
  }

  .view-chart,
  .event-timeline {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }

  .table-wrap {
    border: 0;
    border-radius: 0;
    overflow: visible;
  }

  a {
    color: inherit;
    text-decoration: none;
  }
}
"""

INTERNAL_CALIBRATION_RE = re.compile(
    r"<!--\s*life-fork-calibration[\s\S]*?-->\s*",
    flags=re.MULTILINE,
)


def strip_internal_calibration(markdown_text: str) -> str:
    """Remove developer-only calibration records before user-facing render."""
    return INTERNAL_CALIBRATION_RE.sub("", markdown_text)


def inline_markup(text: str) -> str:
    text = user_facing_text(text)
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def user_facing_text(text: str) -> str:
    replacements = {
        "附录 A：Agent 详细输出": "附录 A：各视角详细判断",
        "Agent 详细输出": "各视角详细判断",
        "人生叙事 Agent": "人生叙事视角",
        "职业路径 Agent": "职业路径视角",
        "资产现金流 Agent": "资产现金流视角",
        "关系与家庭 Agent": "关系与家庭视角",
        "健康与能量 Agent": "健康与能量视角",
        "时代事件 Agent": "时代事件视角",
        "反方审计 Agent": "反过来提醒视角",
        "反方审计": "反过来提醒",
        "审计": "复看",
        "多 Agent 观点": "多视角观点",
        "AI 和 Agent 工作流": "AI 和自动化工作流",
        "Agent": "视角",
        "事件库": "外部资料",
        "报告质量": "报告状态",
        "质量评分": "状态检查",
        "质量检查": "状态检查",
        "变量": "因素",
        "矩阵": "对照",
        "模型": "方法",
        "路径依赖": "后续牵连",
        "置信度": "材料充分度",
        "产物": "留下的东西",
        "判断门槛": "怎么看结果",
        "项目卡": "案例页",
        "反馈记录": "反馈摘要",
        "交付": "工作节奏",
        "回写": "修订",
        "Demo": "示例",
        "材料充分度与待补信息": "还缺哪些细节",
        "还需要补的 5 个问题": "还可以补的 5 个信息",
        "还需要补的 3 个问题": "还可以补的 3 个信息",
        "用户补完后如何升级": "补完后会怎么校准",
        "安全边界": "这份报告不能替你决定什么",
        "使用边界": "怎么理解",
        "事件 / 周期": "外部变化",
        "时间范围": "时间",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def row_value(row: list[str], header: list[str], key: str) -> str:
    if key not in header:
        return ""
    index = header.index(key)
    if index >= len(row):
        return ""
    return row[index]


def render_life_line_chart(header: list[str], body: list[list[str]]) -> str:
    cards = []
    name_key = "结果" if "结果" in header else LEGACY_RESULT_HEADER
    for row in body[:3]:
        cards.append(
            '<article class="life-line-card">'
            f'<h3>{inline_markup(row_value(row, header, name_key))}</h3>'
            f'<span class="mini-label">会给你什么</span><p class="mini-text">{inline_markup(row_value(row, header, "会给你什么"))}</p>'
            f'<span class="mini-label">会拿走什么</span><p class="mini-text">{inline_markup(row_value(row, header, "会拿走什么"))}</p>'
            f'<span class="mini-label">最大陷阱</span><p class="mini-text">{inline_markup(row_value(row, header, "最大陷阱"))}</p>'
            "</article>"
        )
    return '<div class="life-line-chart">' + "\n".join(cards) + "</div>"


def render_variable_chart(header: list[str], body: list[list[str]]) -> str:
    cards = []
    for row in body[:6]:
        if "事件锚点" in header:
            cards.append(
                '<article class="variable-chip-card causal-card event-shock-card deep-shock-card">'
                '<span class="shock-anchor-label">事件锚点</span>'
                f'<h3>{inline_markup(row_value(row, header, "事件锚点"))}</h3>'
                f'<span class="mini-label">生活场景</span><p class="mini-text">{inline_markup(row_value(row, header, "生活场景"))}</p>'
                f'<span class="mini-label">现实代价</span><p class="mini-text">{inline_markup(row_value(row, header, "现实代价"))}</p>'
                f'<span class="mini-label">情绪代价</span><p class="mini-text">{inline_markup(row_value(row, header, "情绪代价"))}</p>'
                f'<span class="mini-label">误判点</span><p class="mini-text">{inline_markup(row_value(row, header, "误判点"))}</p>'
                f'<span class="mini-label">今天验证</span><p class="mini-text">{inline_markup(row_value(row, header, "今天验证"))}</p>'
                "</article>"
            )
        elif "当年具体是什么" in header:
            cards.append(
                '<article class="variable-chip-card causal-card event-shock-card">'
                f'<h3>{inline_markup(row_value(row, header, "事件冲击"))}</h3>'
                f'<span class="mini-label">当年具体是什么</span><p class="mini-text">{inline_markup(row_value(row, header, "当年具体是什么"))}</p>'
                f'<span class="mini-label">后来它怎样影响你</span><p class="mini-text">{inline_markup(row_value(row, header, "后来它怎样影响你"))}</p>'
                f'<span class="mini-label">你可能误判了什么</span><p class="mini-text">{inline_markup(row_value(row, header, "你可能误判了什么"))}</p>'
                f'<span class="mini-label">今天怎么验证</span><p class="mini-text">{inline_markup(row_value(row, header, "今天怎么验证"))}</p>'
                "</article>"
            )
        elif "当年它意味着什么" in header:
            cards.append(
                '<article class="variable-chip-card causal-card">'
                f'<h3>{inline_markup(row_value(row, header, "当年没看见的东西"))}</h3>'
                f'<span class="mini-label">当年它意味着什么</span><p class="mini-text">{inline_markup(row_value(row, header, "当年它意味着什么"))}</p>'
                f'<span class="mini-label">后来它怎样影响你</span><p class="mini-text">{inline_markup(row_value(row, header, "后来它怎样影响你"))}</p>'
                f'<span class="mini-label">你可能误判了什么</span><p class="mini-text">{inline_markup(row_value(row, header, "你可能误判了什么"))}</p>'
                f'<span class="mini-label">今天怎么验证</span><p class="mini-text">{inline_markup(row_value(row, header, "今天怎么验证"))}</p>'
                "</article>"
            )
        else:
            cards.append(
                '<article class="variable-chip-card">'
                f'<h3>{inline_markup(row_value(row, header, "当年没看见的东西"))}</h3>'
                f'<span class="mini-label">后来怎么影响你</span><p class="mini-text">{inline_markup(row_value(row, header, "后来怎么影响你"))}</p>'
                f'<span class="mini-label">今天怎么验证</span><p class="mini-text">{inline_markup(row_value(row, header, "今天怎么验证"))}</p>'
                "</article>"
            )
    return '<div class="variable-chart">' + "\n".join(cards) + "</div>"


def render_attribution_chart(header: list[str], body: list[list[str]]) -> str:
    cards = []
    for row in body[:4]:
        cards.append(
            '<article class="attribution-card">'
            f'<h3>{inline_markup(row_value(row, header, "来源"))}</h3>'
            f'<span class="mini-label">它改变了什么</span><p class="mini-text">{inline_markup(row_value(row, header, "它改变了什么"))}</p>'
            f'<span class="mini-label">你该怎么理解</span><p class="mini-text">{inline_markup(row_value(row, header, "你该怎么理解"))}</p>'
            "</article>"
        )
    labels = [row_value(row, header, "来源") for row in body[:4]]
    while len(labels) < 4:
        labels.append(["你的选择", "当时环境", "后来变化", "遇到的人"][len(labels)])
    xs = [42, 132, 222, 312]
    dots = []
    dot_classes = ["dot-choice", "dot-context", "dot-event", "dot-luck"]
    for index, label in enumerate(labels[:4]):
        lines = svg_caption_lines(label, 6)
        label_svg = [f'<text class="chart-text" x="{xs[index]}" y="90" text-anchor="middle">']
        for line_index, line in enumerate(lines[:2]):
            dy = 0 if line_index == 0 else 14
            label_svg.append(f'<tspan x="{xs[index]}" dy="{dy}">{html.escape(line)}</tspan>')
        label_svg.append("</text>")
        dots.append(
            f'<circle class="attribution-dot {dot_classes[index]}" cx="{xs[index]}" cy="48" r="12" />'
            + "".join(label_svg)
        )
    visual = (
        '<div class="attribution-visual">'
        '<svg class="attribution-mini-svg" viewBox="0 0 360 122" role="img" aria-label="选择和外部环境共同影响示意图">'
        '<path class="attribution-line" d="M42 48 C92 28, 108 68, 132 48 S202 48, 222 48 S292 70, 312 48" />'
        + "".join(dots)
        + '<text class="chart-subtext" x="180" y="116" text-anchor="middle">这件事由几股力量一起推着走</text>'
        "</svg></div>"
    )
    return visual + '<div class="attribution-chart">' + "\n".join(cards) + "</div>"


def render_action_timeline(header: list[str], body: list[list[str]]) -> str:
    cards = []
    for row in body[:4]:
        time_value = row_value(row, header, "时间") or row_value(row, header, "周次")
        action_value = row_value(row, header, "动作") or row_value(row, header, "这一周做什么")
        how_value = row_value(row, header, "怎么做") or row_value(row, header, "留下什么")
        observe_value = row_value(row, header, "看什么") or row_value(row, header, "怎么看结果")
        cards.append(
            '<article class="action-step">'
            f'<div class="action-week">{inline_markup(time_value)}</div>'
            f'<div class="action-main">{inline_markup(action_value)}</div>'
            f'<div class="action-output"><span class="mini-label">怎么做</span>{inline_markup(how_value)}</div>'
            f'<div class="action-threshold"><span class="mini-label">看什么</span>{inline_markup(observe_value)}</div>'
            "</article>"
        )
    return '<div class="action-timeline">' + "\n".join(cards) + "</div>"


def render_detail_action_grid(header: list[str], body: list[list[str]]) -> str:
    cards = []
    for row in body[:3]:
        cards.append(
            '<article class="detail-action-card">'
            f'<h4>{inline_markup(row_value(row, header, "动作"))}</h4>'
            f'<span class="mini-label">怎么做</span><p>{inline_markup(row_value(row, header, "怎么做"))}</p>'
            f'<span class="mini-label">看什么</span><p>{inline_markup(row_value(row, header, "看什么"))}</p>'
            "</article>"
        )
    return '<div class="detail-action-grid">' + "\n".join(cards) + "</div>"


def render_audit_grid(header: list[str], body: list[list[str]]) -> str:
    cards = []
    for row in body[:6]:
        cards.append(
            '<article class="audit-card">'
            f'<h4>{inline_markup(row_value(row, header, "来源"))}</h4>'
            f'<span class="mini-label">关键提醒</span><p>{inline_markup(row_value(row, header, "关键提醒"))}</p>'
            f'<span class="mini-label">制衡点</span><p>{inline_markup(row_value(row, header, "制衡点"))}</p>'
            "</article>"
        )
    return '<div class="audit-grid">' + "\n".join(cards) + "</div>"


def render_event_card_grid(header: list[str], body: list[list[str]]) -> str:
    cards = []
    event_key = "事件 / 周期" if "事件 / 周期" in header else "外部变化"
    time_key = "时间范围" if "时间范围" in header else "时间"
    boundary_key = "使用边界" if "使用边界" in header else "怎么理解"
    for row in body[:5]:
        cards.append(
            '<article class="event-card">'
            f'<span class="event-meta">{inline_markup(row_value(row, header, time_key))}</span>'
            f'<h4>{inline_markup(row_value(row, header, event_key))}</h4>'
            f'<span class="mini-label">改变了什么</span><p>{inline_markup(row_value(row, header, "改变了什么"))}</p>'
            f'<span class="mini-label">怎么理解</span><p>{inline_markup(row_value(row, header, boundary_key))}</p>'
            "</article>"
        )
    points = []
    rows = body[:5]
    if rows:
        gap = 304 / max(1, len(rows) - 1)
        for index, row in enumerate(rows):
            x = 28 + gap * index
            y = 70 if index % 2 == 0 else 92
            title = row_value(row, header, event_key)
            time_range = row_value(row, header, time_key)
            points.append(
                f'<circle class="event-dot dot-{["choice", "context", "event", "luck", "context"][index]}" cx="{x:.1f}" cy="{y}" r="8" />'
                f'<text class="chart-text" x="{x:.1f}" y="{34 if index % 2 == 0 else 122}" text-anchor="middle">{html.escape(shorten(time_range, 10))}</text>'
                f'<text class="chart-subtext" x="{x:.1f}" y="{48 if index % 2 == 0 else 136}" text-anchor="middle">{html.escape(shorten(title, 9))}</text>'
            )
    visual = (
        '<div class="event-timeline-visual">'
        '<svg class="event-timeline-svg" viewBox="0 0 360 150" role="img" aria-label="外部环境时间线示意图">'
        '<path class="event-line" d="M28 70 C86 46, 105 108, 180 76 S274 40, 332 84" />'
        + "".join(points)
        + "</svg></div>"
    )
    return visual + '<div class="event-card-grid">' + "\n".join(cards) + "</div>"


def render_quality_grid(header: list[str], body: list[list[str]]) -> str:
    cards = []
    for row in body[:6]:
        cards.append(
            '<article class="quality-card">'
            f'<div class="quality-head"><h4>{inline_markup(row_value(row, header, "维度"))}</h4>'
            f'<span>{inline_markup(row_value(row, header, "分数"))}</span></div>'
            f'<span class="mini-label">依据</span><p>{inline_markup(row_value(row, header, "证据"))}</p>'
            f'<span class="mini-label">修订方向</span><p>{inline_markup(row_value(row, header, "改进"))}</p>'
            "</article>"
        )
    return '<div class="quality-grid">' + "\n".join(cards) + "</div>"


def render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:] if len(rows) > 2 and is_table_separator(lines[1]) else rows[1:]

    if header in ([LEGACY_RESULT_HEADER, "会给你什么", "会拿走什么", "最大陷阱"], ["结果", "会给你什么", "会拿走什么", "最大陷阱"]):
        return render_life_line_chart(header, body)
    if header == ["事件锚点", "生活场景", "现实代价", "情绪代价", "误判点", "今天验证"]:
        return render_variable_chart(header, body)
    if header == ["事件冲击", "当年具体是什么", "后来它怎样影响你", "你可能误判了什么", "今天怎么验证"]:
        return render_variable_chart(header, body)
    if header == ["当年没看见的东西", "当年它意味着什么", "后来它怎样影响你", "你可能误判了什么", "今天怎么验证"]:
        return render_variable_chart(header, body)
    if header == ["当年没看见的东西", "后来怎么影响你", "今天怎么验证"]:
        return render_variable_chart(header, body)
    if header == ["来源", "它改变了什么", "你该怎么理解"]:
        return render_attribution_chart(header, body)
    if header in (["周次", "这一周做什么", "留下什么", "怎么看结果"], ["时间", "动作", "怎么做", "看什么"]):
        return render_action_timeline(header, body)
    if header == ["动作", "怎么做", "看什么"]:
        return render_detail_action_grid(header, body)
    if header == ["来源", "关键提醒", "制衡点"]:
        return render_audit_grid(header, body)
    if header in (
        ["事件 / 周期", "时间范围", "改变了什么", "使用边界"],
        ["外部变化", "时间", "改变了什么", "怎么理解"],
    ):
        return render_event_card_grid(header, body)
    if header == ["维度", "分数", "证据", "改进"]:
        return render_quality_grid(header, body)

    out = ["<table>", "<thead><tr>"]
    out.extend(f"<th>{inline_markup(cell)}</th>" for cell in header)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline_markup(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table></div>")
    out.insert(0, '<div class="table-wrap">')
    return "\n".join(out)


def markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_stack: list[str] = []
    section_open = False
    in_code = False
    code_lines: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")
            paragraph = []

    def close_lists() -> None:
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    def close_section() -> None:
        nonlocal section_open
        if section_open:
            out.append("</section>")
            section_open = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            close_lists()
            i += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i])
                i += 1
            flush_paragraph()
            close_lists()
            out.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_lists()
            level = len(heading.group(1))
            if level == 2:
                close_section()
                out.append('<section class="report-section">')
                section_open = True
            out.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped == "---":
            flush_paragraph()
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_lists()
            quote = stripped.lstrip(">").strip()
            out.append(f"<blockquote>{inline_markup(quote)}</blockquote>")
            i += 1
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if ordered or unordered:
            flush_paragraph()
            tag = "ol" if ordered else "ul"
            if not list_stack or list_stack[-1] != tag:
                close_lists()
                out.append(f"<{tag}>")
                list_stack.append(tag)
            item = ordered.group(1) if ordered else unordered.group(1)
            out.append(f"<li>{inline_markup(item)}</li>")
            i += 1
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    close_lists()
    close_section()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(out)


def extract_cover_fields(markdown_text: str) -> tuple[dict[str, str], str]:
    fields: dict[str, str] = {}
    body_lines: list[str] = []
    for line in markdown_text.splitlines():
        matched = False
        for key in ("判词", "命中句", "看清", "问题", "核心判断", "置信度"):
            prefix = f"{key}："
            if line.startswith(prefix):
                fields[key] = line[len(prefix) :].strip()
                matched = True
                break
        if not matched:
            body_lines.append(line)
    return fields, "\n".join(body_lines)


def render_cover_cards(fields: dict[str, str]) -> str:
    if not fields:
        return ""
    cards = []
    for key in ("问题", "核心判断", "置信度"):
        value = fields.get(key)
        if value:
            extra = ""
            if key == "置信度":
                width = confidence_width(value)
                extra = f'<div class="confidence-meter"><span style="width: {width}%"></span></div>'
            cards.append(
                '<div class="cover-card">'
                f'<div class="cover-label">{html.escape(key)}</div>'
                f'<div class="cover-value">{inline_markup(value)}</div>'
                f"{extra}"
                "</div>"
            )
    return '<div class="cover-grid">' + "\n".join(cards) + "</div>"


def confidence_width(value: str) -> int:
    if "高" in value:
        return 82
    if "低" in value:
        return 38
    return 58


def shorten(text: str, limit: int = 54) -> str:
    cleaned = re.sub(r"\s+", "", text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1] + "…"


def svg_caption_lines(text: str, limit: int = 8) -> list[str]:
    cleaned = re.sub(r"\s+", "", text)
    if not cleaned:
        return []
    if len(cleaned) <= limit:
        return [cleaned]
    tokens = re.findall(r"[A-Za-z0-9+#.-]+|.", cleaned)
    lines: list[str] = []
    current = ""
    for token in tokens:
        allowance = limit + 2 if re.fullmatch(r"[A-Za-z0-9+#.-]+", token) and len(token) <= 5 else limit
        if current and len(current) + len(token) > allowance:
            lines.append(current)
            current = token
            if len(lines) == 1:
                continue
            break
        else:
            current += token
    if current and len(lines) < 2:
        lines.append(current)
    consumed = sum(len(line) for line in lines)
    if consumed < len(cleaned):
        remaining = cleaned[consumed:]
        if len(lines) < 2:
            lines.append(shorten(remaining, limit))
        else:
            lines[-1] = shorten(lines[-1] + remaining, limit)
    return lines[:2]


def section_between(markdown_text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown_text.find(marker)
    if start == -1:
        return ""
    next_heading = markdown_text.find("\n## ", start + len(marker))
    if next_heading == -1:
        return markdown_text[start:]
    return markdown_text[start:next_heading]


def parse_first_table(section_text: str) -> tuple[list[str], list[list[str]]]:
    table_lines = [
        line.strip()
        for line in section_text.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]
    if len(table_lines) < 3:
        return [], []
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in table_lines]
    header = rows[0]
    data_rows = [row for row in rows[2:] if len(row) == len(header)]
    return header, data_rows


def path_rows(markdown_text: str) -> list[dict[str, str]]:
    header, rows = parse_first_table(section_between(markdown_text, "2. 当年的岔路"))
    items: list[dict[str, str]] = []
    for row in rows[:3]:
        data = dict(zip(header, row))
        items.append(
            {
                "name": data.get("路径", "一条人生路径"),
                "gain": data.get("当时看起来的收益", ""),
                "cost": data.get("当时看不清的代价", ""),
                "check": data.get("今天需要验证", ""),
            }
        )
    return items


def table_rows(markdown_text: str, heading: str) -> list[dict[str, str]]:
    header, rows = parse_first_table(section_between(markdown_text, heading))
    return [dict(zip(header, row)) for row in rows]


def named_line_rows(markdown_text: str) -> list[dict[str, str]]:
    rows = table_rows(markdown_text, "2. 三种结果")
    if rows:
        return [
            {
                "name": row.get("结果") or row.get(LEGACY_RESULT_HEADER, "结果"),
                "give": row.get("会给你什么", ""),
                "take": row.get("会拿走什么", ""),
                "trap": row.get("最大陷阱", ""),
            }
            for row in rows[:3]
        ]
    return [
        {"name": "现实结果", "give": "已经得到的稳定和经验", "take": "也留下新遗憾", "trap": "把过去审判过重"},
        {"name": "假设结果", "give": "可能打开新样本", "take": "也会带来新成本", "trap": "把另一个结果想得太亮"},
        {"name": "回补结果", "give": "今天还能补回一部分", "take": "需要持续输出和验证", "trap": "只怀旧，不验证"},
    ]


def render_named_lines(rows: list[dict[str, str]]) -> str:
    if not rows:
        rows = [
            {"name": "现实结果", "give": "稳定和缓冲", "take": "外部碰撞", "trap": "把安全感当成全部答案"},
            {"name": "假设结果", "give": "更早被看见", "take": "更高成本", "trap": "把外部光环当成能力"},
            {"name": "回补结果", "give": "补回作品和连接", "take": "持续输出压力", "trap": "只复盘，不验证"},
        ]
    line_html = []
    for row in rows[:3]:
        line_html.append(
            '<div class="named-line">'
            f'<div class="named-line-title">{inline_markup(shorten(row.get("name", "结果"), 24))}</div>'
            f'<div class="named-line-cell"><strong>会给你什么</strong>{inline_markup(shorten(row.get("give", ""), 42))}</div>'
            f'<div class="named-line-cell"><strong>会拿走什么</strong>{inline_markup(shorten(row.get("take", ""), 42))}</div>'
            f'<div class="named-line-cell"><strong>最大陷阱</strong>{inline_markup(shorten(row.get("trap", ""), 42))}</div>'
            "</div>"
        )
    return '<div class="named-lines">' + "\n".join(line_html) + "</div>"


def render_verdict_cover(title: str, fields: dict[str, str], markdown_text: str) -> str:
    verdict = fields.get("判词") or fields.get("命中句") or fields.get("核心判断") or title
    helps = fields.get("看清") or fields.get("核心判断") or "看清那个假设结果到底给你什么、拿走什么，以及今天还能补回哪一块。"
    return (
        '<div class="verdict-cover">'
        f"<h1>{html.escape(title)}</h1>"
        f'<p class="verdict-line">{inline_markup(verdict)}</p>'
        f"{render_named_lines(named_line_rows(markdown_text))}"
        f'<p class="verdict-helps"><strong>这份报告帮你看清：</strong>{inline_markup(helps)}</p>'
        "</div>"
    )


USER_HTML_CSS = """
:root {
  --ink: #192632;
  --muted: #66788a;
  --paper: #fffdf7;
  --soft: #f6f1e7;
  --line: #e0d8c8;
  --accent: #214e62;
  --warm: #8b6c3e;
  --shadow: 0 20px 48px rgba(25, 38, 50, 0.10);
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: auto;
}

body {
  background:
    linear-gradient(180deg, rgba(255, 253, 247, 0.92), rgba(246, 241, 231, 0.96)),
    repeating-linear-gradient(90deg, rgba(33, 78, 98, 0.055) 0 1px, transparent 1px 40px);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
  line-height: 1.7;
  margin: 0;
}

.reader {
  margin: 0 auto;
  max-width: 760px;
  padding: 0 14px 48px;
}

.screen,
.block,
.folded {
  background: rgba(255, 253, 247, 0.94);
  border: 1px solid rgba(33, 78, 98, 0.14);
  border-radius: 22px;
  box-shadow: var(--shadow);
  margin: 14px 0;
}

.hero-screen {
  align-content: center;
  display: grid;
  min-height: 100vh;
  padding: 42px 24px;
}

.report-name {
  color: var(--accent);
  font-size: 13px;
  font-weight: 850;
  letter-spacing: 0.12em;
  margin: 0 0 24px;
}

.hero-screen h1 {
  color: #1d2c38;
  font-size: clamp(28px, 8vw, 42px);
  line-height: 1.18;
  margin: 0 0 28px;
}

.verdict {
  color: #163447;
  font-size: clamp(25px, 7vw, 40px);
  font-weight: 930;
  line-height: 1.24;
  margin: 0;
}

.hero-explain {
  color: #405869;
  font-size: 16px;
  line-height: 1.66;
  margin: 18px 0 0;
}

.scroll-cue {
  border-top: 1px solid rgba(33, 78, 98, 0.16);
  color: var(--muted);
  font-size: 14px;
  margin: 36px 0 0;
  padding-top: 18px;
}

.fork-screen {
  display: grid;
  gap: 20px;
  min-height: 76vh;
  padding: 28px 22px;
}

.section-kicker {
  color: var(--accent);
  font-size: 13px;
  font-weight: 850;
  letter-spacing: 0.08em;
  margin: 0 0 8px;
}

.fork-screen h2,
.block h2 {
  color: #1d2c38;
  font-size: 25px;
  line-height: 1.25;
  margin: 0;
}

.fork-visual {
  overflow: hidden;
}

.fork-map {
  background:
    linear-gradient(180deg, rgba(255, 250, 240, 0.96), rgba(247, 241, 230, 0.9)),
    repeating-linear-gradient(90deg, rgba(33, 78, 98, 0.045) 0 1px, transparent 1px 32px),
    repeating-linear-gradient(180deg, rgba(139, 108, 62, 0.04) 0 1px, transparent 1px 32px);
  border: 1px solid rgba(33, 78, 98, 0.16);
  border-radius: 20px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
  display: grid;
  gap: 14px;
  padding: 14px 12px 12px;
}

.fork-chart-shell {
  background:
    radial-gradient(circle at 24% 52%, rgba(33, 78, 98, 0.10), transparent 23%),
    radial-gradient(circle at 82% 20%, rgba(209, 177, 108, 0.20), transparent 22%),
    radial-gradient(circle at 82% 78%, rgba(112, 145, 167, 0.16), transparent 22%),
    rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(33, 78, 98, 0.12);
  border-radius: 18px;
  overflow: hidden;
  padding: 8px 4px;
}

.fork-map-svg {
  display: block;
  height: auto;
  max-height: 330px;
  min-height: 260px;
  overflow: visible;
  width: 100%;
}

.fork-map-svg path {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 7;
}

.fork-map-svg .past-route {
  stroke: rgba(33, 78, 98, 0.42);
}

.fork-map-svg .route-chosen {
  stroke: #d1a85d;
}

.fork-map-svg .route-unchosen {
  stroke: #69aaa1;
}

.fork-map-svg .route-repair {
  stroke: #7091a7;
}

.fork-map-svg .route-shadow {
  filter: drop-shadow(0 7px 10px rgba(33, 78, 98, 0.10));
}

.fork-map-svg .fork-node,
.fork-map-svg .end-node,
.fork-map-svg .start-node {
  fill: #fffdf7;
  stroke-width: 5;
}

.fork-map-svg .start-node {
  stroke: rgba(33, 78, 98, 0.62);
}

.fork-map-svg .fork-node {
  fill: #fff7db;
  stroke: #214e62;
}

.fork-map-svg .end-node.chosen {
  stroke: #d1a85d;
}

.fork-map-svg .end-node.unchosen {
  stroke: #69aaa1;
}

.fork-map-svg .end-node.repair {
  stroke: #7091a7;
}

.fork-map-svg .node-label,
.fork-map-svg .route-title,
.fork-map-svg .route-caption {
  fill: #214e62;
  letter-spacing: 0;
}

.fork-map-svg .node-label {
  font-size: 12px;
  font-weight: 860;
}

.fork-map-svg .route-title {
  font-size: 14px;
  font-weight: 920;
}

.fork-map-svg .route-caption {
  fill: #496171;
  font-size: 11px;
  font-weight: 760;
}

.fork-map-note {
  color: #405869;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(33, 78, 98, 0.12);
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.62;
  margin: 0 4px;
  padding: 11px 12px;
}

.fork-start,
.fork-result {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(33, 78, 98, 0.14);
  border-radius: 16px;
  padding: 14px;
}

.fork-label {
  color: var(--accent);
  display: block;
  font-size: 13px;
  font-weight: 900;
  margin-bottom: 5px;
}

.fork-text {
  color: #384c5b;
  font-size: 14px;
  margin: 0;
}

.fork-line {
  align-items: center;
  display: grid;
  grid-template-columns: 1fr 36px 1fr;
  min-height: 78px;
}

.fork-line::before,
.fork-line::after {
  background: linear-gradient(90deg, rgba(33, 78, 98, 0.18), rgba(139, 108, 62, 0.5));
  content: "";
  display: block;
  height: 2px;
}

.fork-dot {
  background: var(--accent);
  border: 5px solid #ecf4f4;
  border-radius: 999px;
  height: 28px;
  justify-self: center;
  width: 28px;
}

.block {
  padding: 24px 22px;
}

.story p,
.variable-intro,
.recover-intro,
.closing-line {
  color: #2f4352;
  font-size: 16px;
  margin: 14px 0 0;
}

.result-cards {
  display: grid;
  gap: 14px;
  margin-top: 18px;
}

.variable-front .variable-chart {
  gap: 16px;
  margin-top: 18px;
}

.result-card,
.action-card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(250, 246, 237, 0.78));
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px;
}

.result-card {
  border-color: rgba(33, 78, 98, 0.13);
  border-left: 7px solid var(--card-accent, #214e62);
  box-shadow: 0 12px 24px rgba(25, 38, 50, 0.07);
  overflow: hidden;
  position: relative;
}

.result-card::before {
  background: linear-gradient(90deg, var(--card-accent, #214e62), transparent);
  content: "";
  height: 4px;
  left: 0;
  opacity: 0.72;
  position: absolute;
  right: 0;
  top: 0;
}

.result-card--1 {
  --card-accent: #d1a85d;
}

.result-card--2 {
  --card-accent: #69aaa1;
}

.result-card--3 {
  --card-accent: #7091a7;
}

.result-card h3,
.action-card h3 {
  color: #17384a;
  font-size: 20px;
  line-height: 1.28;
  margin: 0 0 12px;
}

.result-verdict {
  color: #2f4352;
  font-size: 15px;
  font-weight: 760;
  line-height: 1.55;
  margin: -2px 0 14px;
}

.result-row {
  margin: 12px 0 0;
}

.result-row span,
.action-card span {
  color: var(--accent);
  display: block;
  font-size: 13px;
  font-weight: 900;
  margin-bottom: 4px;
}

.result-row p,
.action-card p {
  color: #3d5262;
  font-size: 15px;
  margin: 0;
}

.actions {
  display: grid;
  gap: 14px;
  margin-top: 18px;
}

.action-number {
  align-items: center;
  background: #17384a;
  border-radius: 999px;
  color: #fffdf7;
  display: inline-flex;
  font-size: 13px;
  font-weight: 900;
  height: 30px;
  justify-content: center;
  margin-bottom: 12px;
  width: 30px;
}

.closing-line {
  background: #f6f1e7;
  border: 1px solid rgba(33, 78, 98, 0.14);
  border-radius: 16px;
  font-weight: 760;
  padding: 14px;
}

.folded {
  overflow: hidden;
}

details {
  border-top: 1px solid rgba(33, 78, 98, 0.12);
  padding: 0;
}

details:first-child {
  border-top: 0;
}

summary {
  color: #17384a;
  cursor: pointer;
  font-size: 17px;
  font-weight: 880;
  list-style: none;
  padding: 18px 20px;
}

summary::-webkit-details-marker {
  display: none;
}

summary::after {
  color: var(--muted);
  content: "展开";
  float: right;
  font-size: 13px;
  font-weight: 760;
}

details[open] summary::after {
  content: "收起";
}

.detail-body {
  color: #344b5c;
  font-size: 14px;
  padding: 0 20px 20px;
}

.detail-intro {
  background: rgba(246, 241, 231, 0.72);
  border: 1px solid rgba(33, 78, 98, 0.10);
  border-radius: 14px;
  color: #294a5d;
  font-size: 14px;
  font-weight: 680;
  line-height: 1.7;
  margin: 0 0 14px;
  padding: 12px 13px;
}

.detail-body h3,
.detail-body h4 {
  color: var(--accent);
  margin: 16px 0 8px;
}

.detail-body table {
  border-collapse: collapse;
  font-size: 12px;
  width: 100%;
}

.detail-body th,
.detail-body td {
  border: 1px solid var(--line);
  padding: 7px;
  text-align: left;
  vertical-align: top;
}

.detail-body th {
  background: var(--soft);
}

.variable-chart,
.attribution-chart,
.audit-grid,
.event-card-grid,
.detail-action-grid,
.quality-grid {
  display: grid;
  gap: 12px;
  margin: 12px 0 16px;
}

.variable-chart,
.attribution-chart {
  grid-template-columns: 1fr;
}

.attribution-visual,
.event-timeline-visual {
  background: linear-gradient(135deg, rgba(36, 91, 119, 0.08), rgba(209, 168, 93, 0.10));
  border: 1px solid rgba(33, 78, 98, 0.12);
  border-radius: 18px;
  margin: 12px 0 14px;
  padding: 8px;
}

.attribution-mini-svg,
.event-timeline-svg {
  display: block;
  height: auto;
  width: 100%;
}

.attribution-line,
.event-line {
  fill: none;
  stroke: rgba(33, 78, 98, 0.34);
  stroke-linecap: round;
  stroke-width: 4;
}

.attribution-dot,
.event-dot {
  fill: #fffdf7;
  stroke-width: 5;
}

.dot-choice {
  stroke: #d1a85d;
}

.dot-context {
  stroke: #69aaa1;
}

.dot-event {
  stroke: #7091a7;
}

.dot-luck {
  stroke: #9a8b6b;
}

.chart-text {
  fill: #17384a;
  font-size: 12px;
  font-weight: 850;
}

.chart-subtext {
  fill: #607381;
  font-size: 10px;
  font-weight: 700;
}

.audit-card,
.event-card,
.detail-action-card,
.quality-card,
.variable-chip-card,
.attribution-card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(250, 246, 237, 0.74));
  border: 1px solid rgba(33, 78, 98, 0.13);
  border-radius: 16px;
  box-shadow: 0 10px 22px rgba(25, 38, 50, 0.06);
  padding: 14px;
}

.audit-card {
  border-left: 6px solid #69aaa1;
}

.variable-chip-card {
  border-top: 5px solid rgba(36, 91, 119, 0.46);
}

.variable-front .variable-chip-card {
  padding: 18px;
}

.causal-card .mini-label {
  border-top: 1px solid rgba(33, 78, 98, 0.10);
  padding-top: 10px;
}

.causal-card .mini-label:first-of-type {
  border-top: 0;
  padding-top: 0;
}

.causal-card .mini-text {
  font-size: 14px;
  line-height: 1.66;
}

.variable-chip-card:nth-child(2n) {
  border-top-color: #d1a85d;
}

.variable-chip-card:nth-child(3n) {
  border-top-color: #69aaa1;
}

.attribution-card {
  border-left: 6px solid #d1a85d;
}

.attribution-card:nth-child(2n) {
  border-left-color: #69aaa1;
}

.attribution-card:nth-child(3n) {
  border-left-color: #7091a7;
}

.audit-card:nth-child(2n) {
  border-left-color: #d1a85d;
}

.audit-card:nth-child(3n) {
  border-left-color: #7091a7;
}

.event-card {
  border-top: 5px solid #d1a85d;
}

.event-card:nth-child(2n) {
  border-top-color: #69aaa1;
}

.event-card:nth-child(3n) {
  border-top-color: #7091a7;
}

.detail-action-card {
  border-left: 6px solid #214e62;
}

.quality-card {
  border-left: 6px solid #d1a85d;
}

.quality-card:nth-child(2n) {
  border-left-color: #69aaa1;
}

.quality-card:nth-child(3n) {
  border-left-color: #7091a7;
}

.audit-card h4,
.event-card h4,
.detail-action-card h4,
.quality-card h4,
.variable-chip-card h3,
.attribution-card h3 {
  color: #17384a;
  font-size: 17px;
  line-height: 1.3;
  margin: 0 0 10px;
}

.audit-card p,
.event-card p,
.detail-action-card p,
.quality-card p,
.variable-chip-card p,
.attribution-card p {
  color: #405869;
  font-size: 13px;
  line-height: 1.58;
  margin: 0;
}

.audit-card .mini-label,
.event-card .mini-label,
.detail-action-card .mini-label,
.quality-card .mini-label,
.variable-chip-card .mini-label,
.attribution-card .mini-label {
  margin-top: 9px;
}

.quality-head {
  align-items: center;
  display: flex;
  gap: 10px;
  justify-content: space-between;
  margin-bottom: 4px;
}

.quality-head h4 {
  margin: 0;
}

.quality-head span {
  background: rgba(33, 78, 98, 0.10);
  border: 1px solid rgba(33, 78, 98, 0.12);
  border-radius: 999px;
  color: #214e62;
  flex: 0 0 auto;
  font-size: 13px;
  font-weight: 900;
  padding: 5px 10px;
}

.event-meta {
  color: #8b6c3e;
  display: inline-flex;
  font-size: 12px;
  font-weight: 850;
  margin: 0 0 8px;
}

.footer {
  color: var(--muted);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.74), rgba(246, 241, 231, 0.88));
  border: 1px solid rgba(33, 78, 98, 0.13);
  border-radius: 20px;
  font-size: 13px;
  line-height: 1.72;
  margin: 18px 0 0;
  padding: 18px;
}

.footer h2 {
  color: #17384a;
  font-size: 18px;
  margin: 0 0 8px;
}

.footer p {
  margin: 0;
}

@media (min-width: 780px) {
  .reader {
    max-width: 900px;
  }

  .result-cards,
  .actions,
  .audit-grid,
  .event-card-grid,
  .detail-action-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .fork-line {
    grid-template-columns: 1fr 44px 1fr;
  }
}
"""


def strip_number_prefix(text: str) -> str:
    return re.sub(r"^\d+\.\s*", "", text.strip())


def strip_result_prefix(text: str) -> str:
    return text.split("：", 1)[-1].strip() if "：" in text else text.strip()


def fragment(text: str, limit: int = 36) -> str:
    return shorten(text, limit).rstrip("。！？；，,.")


def first_plain_paragraphs(section_text: str, limit: int = 3) -> list[str]:
    paragraphs: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("### "):
            break
        if stripped.startswith("## "):
            continue
        if stripped.startswith("|") or stripped.startswith("- "):
            continue
        paragraphs.append(stripped)
        if len(paragraphs) >= limit:
            break
    return paragraphs


def strip_developer_internal_sections(markdown_text: str) -> str:
    markers = [
        "### 开发者内部检查",
        "#### Magic Score",
        "#### 结构与交付评分",
        "修订记录：",
    ]
    cut_points = [markdown_text.find(marker) for marker in markers if marker in markdown_text]
    if not cut_points:
        return markdown_text
    return markdown_text[: min(cut_points)].rstrip()


def compact_detail(markdown_text: str) -> str:
    cleaned = strip_developer_internal_sections(markdown_text)
    cleaned = re.sub(r"^##\s+.+\n?", "", cleaned.strip())
    return markdown_to_html(cleaned)


def subsection_between(markdown_text: str, heading: str) -> str:
    marker = f"### {heading}"
    start = markdown_text.find(marker)
    if start == -1:
        return ""
    next_heading = markdown_text.find("\n### ", start + len(marker))
    if next_heading == -1:
        return markdown_text[start:]
    return markdown_text[start:next_heading]


def first_section_between(markdown_text: str, headings: list[str]) -> str:
    for heading in headings:
        section = section_between(markdown_text, heading)
        if section:
            return section
    return ""


def first_subsection_between(markdown_text: str, headings: list[str]) -> str:
    for heading in headings:
        section = subsection_between(markdown_text, heading)
        if section:
            return section
    return ""


def render_detail(title: str, markdown_text: str, intro: str = "") -> str:
    content = compact_detail(markdown_text)
    if not content.strip():
        return ""
    if intro:
        content = f'<p class="detail-intro">{inline_markup(intro)}</p>' + content
    return (
        "<details>"
        f"<summary>{html.escape(title)}</summary>"
        f'<div class="detail-body">{content}</div>'
        "</details>"
    )


def result_rows_for_user(markdown_text: str, title: str) -> list[dict[str, str]]:
    rows = named_line_rows(markdown_text)
    labels = ["现实结果", "假设结果", "回补结果"]
    result: list[dict[str, str]] = []
    for index, row in enumerate(rows[:3]):
        result.append(
            {
                "name": f"{labels[index]}：{strip_result_prefix(row.get('name', labels[index]))}",
                "give": row.get("give", ""),
                "take": row.get("take", ""),
                "trap": row.get("trap", ""),
            }
        )
    fallback = [
        {
            "name": "现实结果：已经走过的选择",
            "give": "它给过你一部分确定感和已经积累下来的生活经验。",
            "take": "它也可能拿走了另一种更早被看见、被推动的机会。",
            "trap": "把已经熟悉的生活当成全部答案。",
        },
        {
            "name": "假设结果：当年没走的选择",
            "give": "它可能带来新的圈层、节奏和外部反馈。",
            "take": "它也会拿走原有的安全感、支持网络和恢复空间。",
            "trap": "把没走过的路想得过于完整。",
        },
        {
            "name": "回补结果：今天还能补的部分",
            "give": "它能把旧经验重新整理成别人看得见的作品和连接。",
            "take": "它会拿走只在心里回看的舒服感。",
            "trap": "只反复回想当年，却没有把现在往前推一步。",
        },
    ]
    while len(result) < 3:
        result.append(fallback[len(result)])
    return result


def diagnostic_line(row: dict[str, str]) -> str:
    source = row.get("trap") or row.get("give") or row.get("take") or "这条结果有它给你的，也有它拿走的。"
    return shorten(source, 52)


def render_result_cards(rows: list[dict[str, str]]) -> str:
    cards = []
    for index, row in enumerate(rows[:3], start=1):
        cards.append(
            f'<article class="result-card result-card--{index}">'
            f'<h3>{inline_markup(row["name"])}</h3>'
            f'<p class="result-verdict">{inline_markup(diagnostic_line(row))}</p>'
            f'<div class="result-row"><span>它给你的</span><p>{inline_markup(row["give"])}</p></div>'
            f'<div class="result-row"><span>它拿走的</span><p>{inline_markup(row["take"])}</p></div>'
            f'<div class="result-row"><span>它最大的误判</span><p>{inline_markup(row["trap"])}</p></div>'
            "</article>"
        )
    return '<div class="result-cards">' + "\n".join(cards) + "</div>"


def render_result_section(rows: list[dict[str, str]]) -> str:
    return (
        '<section class="block result-screen" id="results">'
        '<p class="section-kicker">三种结果</p>'
        "<h2>三种结果都会给你东西，也会拿走东西</h2>"
        + render_result_cards(rows)
        + "</section>"
    )


def render_fork_screen(rows: list[dict[str, str]]) -> str:
    labels = []
    kinds = ["现实结果", "假设结果", "回补结果"]
    for index, row in enumerate(rows[:3]):
        name = row.get("name", kinds[index])
        if "：" in name:
            kind, caption = name.split("：", 1)
        else:
            kind, caption = kinds[index], name
        labels.append(
            {
                "kind": html.escape(shorten(kind.strip() or kinds[index], 10)),
                "caption_lines": [
                    html.escape(item)
                    for item in svg_caption_lines(caption.strip() or kinds[index], 8)
                ],
            }
        )
    def route_label(index: int, y: int) -> str:
        parts = [
            f'<text x="224" y="{y}">',
            f'<tspan class="route-title">{labels[index]["kind"]}</tspan>',
        ]
        for line_index, line in enumerate(labels[index]["caption_lines"]):
            dy = 17 if line_index == 0 else 14
            parts.append(f'<tspan class="route-caption" x="224" dy="{dy}">{line}</tspan>')
        parts.append("</text>")
        return "".join(parts)

    return (
        '<section class="screen fork-screen fork-visual" id="fork">'
        "<div>"
        '<p class="section-kicker">那次选择</p>'
        "<h2>一次选择，后来分出了三种结果</h2>"
        "</div>"
        '<div class="fork-map">'
        '<div class="fork-chart-shell" aria-label="一次选择分成三种结果">'
        '<svg class="fork-map-svg" viewBox="0 0 360 260" role="img" aria-label="人生岔路分叉示意图">'
        '<path class="past-route route-shadow" d="M24 132 C70 110, 110 150, 150 132" />'
        '<path class="route-chosen route-shadow" d="M154 132 C205 80, 260 64, 330 62" />'
        '<path class="route-unchosen route-shadow" d="M154 132 C210 124, 270 126, 330 130" />'
        '<path class="route-repair route-shadow" d="M154 132 C205 180, 260 205, 330 210" />'
        '<circle class="start-node" cx="24" cy="132" r="8" />'
        '<circle class="fork-node" cx="154" cy="132" r="10" />'
        '<circle class="end-node chosen" cx="330" cy="62" r="9" />'
        '<circle class="end-node unchosen" cx="330" cy="130" r="9" />'
        '<circle class="end-node repair" cx="330" cy="210" r="9" />'
        '<text class="node-label" x="20" y="108">已经发生的人生</text>'
        '<text class="node-label" x="116" y="118">现实分岔点</text>'
        f"{route_label(0, 46)}"
        f"{route_label(1, 116)}"
        f"{route_label(2, 196)}"
        "</svg>"
        "</div>"
        '<p class="fork-map-note"><strong>怎么读这张图：</strong>这张图只帮你拆开选择后的三种结果。现实结果解释已经发生的收益和代价。假设结果提醒你没走的结果也有成本。回补结果把后悔压成 30 天内能验证的小动作。</p>'
        "</div>"
        "</section>"
    )


def first_table_lines(markdown_text: str) -> list[str]:
    lines = markdown_text.splitlines()
    result: list[str] = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            result.append(line)
            continue
        if in_table:
            break
    return result


def variable_detail_markdown(markdown_text: str) -> str:
    section = section_between(markdown_text, "3. 事件冲击卡")
    return "\n\n".join(
        part
        for part in [
            subsection_between(section, "被低估"),
            subsection_between(section, "被高估"),
            subsection_between(section, "真正的盲点"),
        ]
        if part
    )


def render_variable_section(markdown_text: str) -> str:
    table = first_table_lines(section_between(markdown_text, "3. 事件冲击卡"))
    if not table:
        return ""
    return (
        '<section class="block variable-front" id="variables">'
        '<p class="section-kicker">事件冲击</p>'
        "<h2>那些真正撞到你的事</h2>"
        '<p class="variable-intro">这里不讲抽象词，只看真实撞到身上的事：当年发生了什么，它带来哪些现实代价和情绪代价，以及今天还能用什么小动作校准。</p>'
        + render_table(table)
        + "</section>"
    )


def recovery_actions_for_user(markdown_text: str, title: str) -> list[dict[str, str]]:
    if "北京" in title:
        return [
            {
                "name": "找一个北京同行聊一次",
                "text": "不用问人生建议，只问三个问题：他们当年怎么入局，现在最累的是什么，哪些机会外人看不见。",
            },
            {
                "name": "把一个旧项目写成别人看得懂的案例",
                "text": "不要写流水账，只写问题、你的判断、你做了什么、结果怎样、这件事证明了你什么能力。",
            },
            {
                "name": "做一次可见度测试",
                "text": "把案例发给 3 个可信的人，看他们能不能在 1 分钟内说出你的优势。如果说不出来，你缺的更像是表达方式。",
            },
        ]
    if "留学" in title or "回国" in title:
        return [
            {
                "name": "找一个还留在海外的同学聊一次",
                "text": "不用问谁选得更好，只问三个问题：留下后最真实的代价是什么，最值得的部分是什么，哪些机会外人容易想象过度。",
            },
            {
                "name": "把当年想留下的理由写清楚",
                "text": "只写三列：你当年想要什么，你后来得到了什么，今天还有哪一小块可以重新靠近。写完看哪一列最空。",
            },
            {
                "name": "做一次现实反馈检查",
                "text": "把这三列发给 3 个了解你的人，看他们能不能说出你真正舍不得的部分。如果说不出来，先补表达。",
            },
        ]
    if "体制" in title:
        return [
            {
                "name": "找一个还在体制内的同龄人聊一次",
                "text": "少问稳定，多问日常：他最安心的是什么，最被困住的是什么，十年后哪些能力变强了。听完记录哪一点最触动你。",
            },
            {
                "name": "把你现在的生活节奏写出来",
                "text": "把收入、自由度、家庭距离、身体状态和成长空间放在同一页上，看你真正羡慕的是稳定，还是被照顾的感觉。",
            },
            {
                "name": "问 3 个可信的人怎么看你",
                "text": "让他们只说一句：你更适合高弹性工作，还是稳定规则里的长期积累。听完先记录，别急着反驳。",
            },
        ]
    if "AI" in title or "ai" in title:
        return [
            {
                "name": "找一个 2023 年前入局 AI 的人聊一次",
                "text": "只问三个问题：他最早做对了什么，最痛苦的误判是什么，现在回头看哪件事价值最大。",
            },
            {
                "name": "把一个旧能力改写成 AI 时代案例",
                "text": "不要写工具清单，只写你原来的判断如何被 AI 放大，别人看完能不能记住你的能力。",
            },
            {
                "name": "发给 3 个同行看一眼",
                "text": "让他们说出这件事证明了你什么。如果他们只记住工具名，你缺的更像是叙事。",
            },
        ]
    return [
        {
            "name": "找一个经历过类似选择的人聊一次",
            "text": "不用问人生建议，只问真实日常：它给过什么，也拿走过什么，哪些地方外人容易想象过度。",
        },
        {
            "name": "把一个旧经历写成别人看得懂的案例",
            "text": "只写问题、你的判断、你做了什么、结果怎样，以及这件事说明你有什么能力。",
        },
        {
            "name": "做一次现实反馈检查",
            "text": "发给 3 个可信的人，看他们能不能在 1 分钟内说出你的优势。如果说不出来，先补表达方式。",
        },
    ]


def action_rows_for_user(markdown_text: str) -> list[dict[str, str]]:
    table = first_table_lines(section_between(markdown_text, "5. 30 天验证实验") or section_between(markdown_text, "5. 今天还能补回什么"))
    if not table:
        return []
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in table]
    if len(rows) < 3:
        return []
    header = rows[0]
    body = rows[2:] if is_table_separator(table[1]) else rows[1:]
    if header not in (["动作", "怎么做", "看什么"], ["时间", "动作", "怎么做", "看什么"]):
        return []
    return [
        {
            "time": row_value(row, header, "时间"),
            "name": row_value(row, header, "动作"),
            "how": row_value(row, header, "怎么做"),
            "observe": row_value(row, header, "看什么"),
        }
        for row in body[:4]
        if row_value(row, header, "动作")
    ]


def render_recovery(markdown_text: str, title: str) -> str:
    actions = action_rows_for_user(markdown_text) or recovery_actions_for_user(markdown_text, title)
    action_html = []
    for index, action in enumerate(actions[:4], start=1):
        action_title = action["name"]
        if action.get("time"):
            action_title = f'{action["time"]}：{action_title}'
        if "how" in action:
            body = (
                f'<span>怎么做</span><p>{inline_markup(action["how"])}</p>'
                f'<span>看什么</span><p>{inline_markup(action["observe"])}</p>'
            )
        else:
            body = f'<p>{inline_markup(action["text"])}</p>'
        action_html.append(
            '<article class="action-card">'
            f'<div class="action-number">{index}</div>'
            f'<h3>{inline_markup(action_title)}</h3>'
            f"{body}"
            "</article>"
        )
    section_intro = first_plain_paragraphs(section_between(markdown_text, "5. 30 天验证实验") or section_between(markdown_text, "5. 今天还能补回什么"), 1)
    intro, closing = recovery_copy_for_user(title)
    if section_intro:
        intro = section_intro[0]
    return (
        '<section class="block recover" id="recover">'
        "<h2>30 天验证实验</h2>"
        f'<p class="recover-intro">{inline_markup(intro)}</p>'
        '<div class="actions">'
        + "\n".join(action_html)
        + "</div>"
        f'<p class="closing-line">{inline_markup(closing)}</p>'
        "</section>"
    )


def recovery_copy_for_user(title: str) -> tuple[str, str]:
    if "北京" in title:
        return (
            "你补不回当年的北京，但可以补回一部分当年真正想要的东西：更高密度的信息、更真实的同行反馈，以及别人看得见的作品。",
            "真正能补回的，未必是那座城市，更像是你把自己放进更高密度网络的能力。",
        )
    if "没有回国" in title or "海外" in title or "国际" in title:
        return (
            "你回不到当年刚毕业的路口，但可以补回一部分当时真正向往的东西：英文表达、跨文化连接和国际反馈。",
            "真正能补回的，未必是某个国家，更像是你把海外经历重新变成可见能力。",
        )
    if "留学" in title or "回国" in title:
        return (
            "你回不到当年刚毕业的路口，但可以补回一部分当时真正向往的东西：新的身份感、跨文化连接，以及重新开始的勇气。",
            "真正能补回的，未必是某个国家，更像是你重新打开世界半径的能力。",
        )
    if "体制" in title:
        return (
            "你拿不回当年的体制名额，但可以补回一部分当时想要的东西：更稳的节奏、更低的消耗，以及对长期生活的掌控感。",
            "真正能补回的，未必是那个岗位，更像是你给自己重建稳定感的能力。",
        )
    if "AI" in title or "ai" in title:
        return (
            "你回不到 2023 年的第一波热潮，但可以补回一部分当时该留下的东西：真实作品、外部反馈，以及能被别人使用的判断。",
            "真正能补回的，未必是起跑时间，更像是你把旧经验封装成作品的能力。",
        )
    return (
        "你回不到当年的路口，但可以补回一部分当时真正想要的东西：更清楚的自我理解、更真实的外部反馈，以及别人看得见的作品。",
        "真正能补回的，未必是那条旧路，更像是你重新组织当下生活的能力。",
    )


def render_story(markdown_text: str) -> str:
    paragraphs = first_plain_paragraphs(section_between(markdown_text, "1. 你真正放不下的是什么"), 2)
    body = "\n".join(f"<p>{inline_markup(paragraph)}</p>" for paragraph in paragraphs)
    return (
        '<section class="block story" id="story">'
        "<h2>你真正放不下的是什么</h2>"
        f"{body}"
        "</section>"
    )


def render_folded_details(markdown_text: str) -> str:
    appendix = first_section_between(
        markdown_text,
        [
            "6. 继续解释：这份报告怎么判断",
        ],
    )
    uncertainty = "\n\n".join(
        part
        for part in [
            first_subsection_between(appendix, ["还有哪些信息会改写结论"]),
            first_subsection_between(appendix, ["还可以补的 5 个信息", "还需要补的 5 个问题"]),
            first_subsection_between(appendix, ["还可以补的 3 个信息", "还需要补的 3 个问题"]),
            first_subsection_between(appendix, ["补完后会怎么校准", "用户补完后如何升级"]),
        ]
        if part
    )
    items = [
        (
            "你当年没算进去的事",
            variable_detail_markdown(markdown_text),
            "前面的卡片讲了主要影响。这里继续拆开：当年哪些东西被低估，哪些东西被放大，最后真正的盲点落在哪里。",
        ),
        (
            "哪些是你选的，哪些是时代推的",
            section_between(markdown_text, "4. 哪些来自选择，哪些来自时代"),
            "这件事里，有些部分来自你当年的选择，有些部分来自行业、城市和遇到的人。分清它们，后悔感会更有边界。",
        ),
        (
            "我为什么会这样判断",
            section_between(markdown_text, "1. 你真正放不下的是什么"),
            "这部分解释报告的判断从哪里来。重点不在证明某条路更好，而在看清你反复想起它的原因。",
        ),
        (
            "换几个角度看这件事",
            first_subsection_between(appendix, ["换几个角度看这件事"]),
            "换几个角度看，这件事不会只有一个答案。职业角度可能羡慕机会，生活角度会理解安全感，反过来看，未走的路也有自己的代价。",
        ),
        (
            "那几年，外部环境也在变",
            first_subsection_between(appendix, ["那几年，外部环境也在变"]),
            "你当年做选择时，不只你一个人在变。城市机会、平台风向和行业周期也在变，它们会改变假设结果的成本和回报。",
        ),
        (
            "还有哪些信息会改写结论",
            uncertainty,
            "现在的判断还会被真实细节校准。年份、岗位、收入、家庭距离和身体状态这些信息，都会让结论变得更具体。",
        ),
        (
            "这份报告不能替你决定什么",
            first_subsection_between(appendix, ["这份报告不能替你决定什么", "安全边界"]),
            "这份报告只帮你复盘和校准判断。它不会替你做搬迁、离职、婚恋、投资、医疗或法律决定。",
        ),
    ]
    details = [render_detail(title, content, intro) for title, content, intro in items]
    return '<section class="folded" id="details">' + "\n".join(item for item in details if item) + "<!-- developer quality record kept in source markdown -->" + "</section>"


def build_html(markdown_text: str, title: str) -> str:
    markdown_text = strip_internal_calibration(markdown_text)
    markdown_text = strip_developer_internal_sections(markdown_text)
    body_source = re.sub(r"^#\s+.+\n+", "", markdown_text, count=1)
    cover_fields, report_body_source = extract_cover_fields(body_source)
    verdict = cover_fields.get("判词") or cover_fields.get("命中句") or cover_fields.get("核心判断") or title
    hero_explain = cover_fields.get("看清") or cover_fields.get("核心判断") or "看清当年放下了什么、保住了什么，以及今天还能补回哪一块。"
    results = result_rows_for_user(markdown_text, title)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{USER_HTML_CSS}</style>
</head>
<body>
  <main class="reader">
    <section class="screen hero-screen" id="top">
      <p class="report-name">人生岔路复盘报告</p>
      <h1>{html.escape(title)}</h1>
      <p class="verdict">{inline_markup(verdict)}</p>
      <p class="hero-explain">{inline_markup(hero_explain)}</p>
      <p class="scroll-cue">向下看：那次选择后来分出了什么</p>
    </section>
    {render_fork_screen(results)}
    {render_result_section(results)}
    {render_variable_section(report_body_source)}
    {render_story(report_body_source)}
    {render_recovery(report_body_source, title)}
    {render_folded_details(report_body_source)}
    <section class="footer"><h2>最后提醒</h2><p>这份报告不会告诉你当年选错了。它只帮你看清：那条没走的路，哪些只是想象，哪些今天还能补回来。你补充更多真实信息后，结论还可以继续校准。</p></section>
  </main>
</body>
</html>
"""


def infer_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an HTML-first Life Fork report.")
    parser.add_argument("input", type=Path, help="Markdown report path")
    parser.add_argument("--html", type=Path, required=True, help="Output HTML path")
    parser.add_argument("--title", help="Override report title")
    args = parser.parse_args()

    markdown_text = args.input.read_text(encoding="utf-8")
    title = args.title or infer_title(markdown_text, args.input.stem)
    args.html.parent.mkdir(parents=True, exist_ok=True)
    args.html.write_text(build_html(markdown_text, title), encoding="utf-8")

    print(f"HTML: {args.html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
