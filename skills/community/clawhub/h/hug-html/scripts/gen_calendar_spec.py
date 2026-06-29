#!/usr/bin/env python3
"""Generate the full interactive calendar-dashboard grid spec with embedded JS."""
from _paths import SKILL_DIR
import json, sys
from pathlib import Path


# 内置模板目录（位于安装目录下，跟随技能发布）
TEMPLATES_DIR = SKILL_DIR / "scripts" / "templates"

HEADER_HTML = """\
<div class="gdh-wrapper">
  <h1 style="font-size:1.9rem;font-weight:700;color:#1a4e6e;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin:0 0 0.2rem 0;">
    <span data-field="cal-title">📅 动态周历·法定假日区间管理</span>
    <small style="font-size:0.8rem;background:#eef2fa;padding:5px 14px;border-radius:40px;font-weight:normal;" data-field="cal-subtitle-badge">仿Excel数据库+展示双核逻辑</small>
  </h1>
  <div class="gdh-sub" style="color:#4a627a;border-left:4px solid #2c7da0;padding-left:16px;margin:8px 0 16px 0;font-size:0.9rem;" data-field="cal-subtitle">
    ✔ 假日 = 名称 + 起止日期区间 ✔ 补班单日列表 ✔ 周末规则可配 ✔ 自动更新年份 ✔ 周历+总工日
  </div>
</div>"""

YEAR_HTML = """\
<div class="gpy-panel" style="background:#f8fafd;padding:16px 20px;border-radius:20px;border:1px solid #dce5ef;height:100%;">
  <div class="gpy-title" style="font-weight:700;font-size:1rem;color:#1f5068;border-bottom:2px solid #cbdde9;padding-bottom:6px;margin-bottom:12px;">📆 年份控制 & 周末规则</div>
  <div class="gpy-row" style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
    <label style="font-weight:600;font-size:0.85rem;">📅 年份：</label>
    <input type="number" id="calYearInput" value="2024" min="2020" max="2040" step="1"
      style="padding:6px 10px;border-radius:10px;border:1px solid #cbd5e1;font-size:0.85rem;width:90px;">
    <button id="calSyncBtn" style="background:#d9e6f5;border:none;border-radius:20px;padding:4px 12px;font-size:0.75rem;cursor:pointer;" data-field="cal-sync-btn">🔄 所有假期/补班→本年</button>
  </div>
  <div class="gpy-weekend" style="display:flex;flex-wrap:wrap;gap:6px;background:#ffffffcc;padding:8px 10px;border-radius:16px;">
    <label style="font-weight:600;font-size:0.8rem;width:100%;">📌 休息日：</label>
    <div id="calWeekendGroup" style="display:flex;flex-wrap:wrap;gap:6px;width:100%;"></div>
  </div>
  <div class="gpy-note" style="margin-top:10px;background:#eef3fc;padding:8px 12px;border-radius:14px;font-size:0.75rem;border-left:4px solid #f1c40f;">
    ⚡ 优先级：<strong>补班 > 假日 > 周末</strong>
  </div>
</div>"""

HOLIDAY_HTML = """\
<div class="gph-panel" style="background:#f8fafd;padding:16px 20px;border-radius:20px;border:1px solid #dce5ef;height:100%;">
  <div class="gph-title" style="font-weight:700;font-size:1rem;color:#1f5068;border-bottom:2px solid #cbdde9;padding-bottom:6px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
    <span>🎉 节假日区间</span>
    <button id="calAddInterval" style="background:#eef2ff;border:1px dashed #5f8ab6;padding:3px 10px;border-radius:40px;font-size:0.75rem;cursor:pointer;">+ 添加</button>
  </div>
  <div style="overflow-x:auto;">
  <table class="gph-table" style="width:100%;border-collapse:collapse;font-size:0.78rem;background:white;border-radius:10px;overflow:hidden;">
    <thead><tr style="background:#eef3fc;"><th style="padding:5px 4px;">名称</th><th style="padding:5px 4px;">起始</th><th style="padding:5px 4px;">结束</th><th style="width:32px;"></th></tr></thead>
    <tbody id="calHolidayTbody"></tbody>
  </table>
  </div>
</div>"""

COMP_HTML = """\
<div class="gpc-panel" style="background:#f8fafd;padding:16px 20px;border-radius:20px;border:1px solid #dce5ef;height:100%;">
  <div class="gpc-title" style="font-weight:700;font-size:1rem;color:#1f5068;border-bottom:2px solid #cbdde9;padding-bottom:6px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
    <span>⚙️ 补班日期</span>
    <button id="calAddComp" style="background:#eef2ff;border:1px dashed #5f8ab6;padding:3px 10px;border-radius:40px;font-size:0.75rem;cursor:pointer;">+ 添加</button>
  </div>
  <div style="overflow-x:auto;">
  <table class="gpc-table" style="width:100%;border-collapse:collapse;font-size:0.78rem;background:white;border-radius:10px;overflow:hidden;">
    <thead><tr style="background:#eef3fc;"><th style="padding:5px 4px;">日期</th><th style="width:32px;"></th></tr></thead>
    <tbody id="calCompTbody"></tbody>
  </table>
  </div>
</div>"""

STAT_HTML = """\
<div class="gs-panel" style="background:#eef3fa;border-radius:20px;padding:12px 20px;display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:12px;">
  <div>
    <div style="font-size:0.9rem;color:#4a627a;">🏆 年度实际总工日</div>
    <div style="font-size:2rem;font-weight:800;color:#1f6392;" id="calTotalDays">—</div>
  </div>
  <div class="gs-legend" style="display:flex;gap:12px;font-size:0.7rem;flex-wrap:wrap;">
    <span class="gs-badge" style="background:#e1f7dc;color:#2c6e2c;padding:2px 8px;border-radius:30px;">🟢 工作日</span>
    <span class="gs-badge" style="background:#ffdec2;color:#bc5100;padding:2px 8px;border-radius:30px;">🟠 节假日</span>
    <span class="gs-badge" style="background:#d9effa;color:#00668c;padding:2px 8px;border-radius:30px;">🔵 补班日</span>
    <span class="gs-badge" style="background:#ffe6e5;color:#b13e3e;padding:2px 8px;border-radius:30px;">🔴 休息</span>
  </div>
</div>"""

CALENDAR_HTML = """\
<div class="gc-wrapper" style="overflow-x:auto;border-radius:16px;border:1px solid #dce5f0;background:white;">
  <table class="gc-table" style="width:100%;border-collapse:collapse;font-size:0.78rem;min-width:600px;">
    <thead id="calTableHead">
      <tr><th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周数</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周日</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周一</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周二</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周三</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周四</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周五</th>
      <th style="background:#f0f4fa;padding:8px 4px;border-bottom:2px solid #d0dfec;text-align:center;">周六</th></tr>
    </thead>
    <tbody id="calTableBody"></tbody>
  </table>
</div>"""

FOOTER_HTML = """\
<div class="gf-section" style="margin-top:20px;font-size:0.75rem;text-align:center;color:#6c86a3;border-top:1px solid #e2edf7;padding-top:14px;">
  📐 原Excel逻辑：数据库sheet(节假日区间+补班+周末) → 展示sheet(周历+工日) | 切换年份后点击"同步"一键适配
</div>"""

# ── 完整 JavaScript (从用户原模板提取适配) ──
CALENDAR_JS = r"""
// ═══════════════════════════════════════
// Calendar Dashboard - Interactive Logic
// ═══════════════════════════════════════

// Data
let calHolidayIntervals = [
    { name: '\u5143\u65e6', start: '2024-01-01', end: '2024-01-01' },
    { name: '\u6625\u8282', start: '2024-02-10', end: '2024-02-17' },
    { name: '\u6e05\u660e\u8282', start: '2024-04-04', end: '2024-04-06' },
    { name: '\u52b3\u52a8\u8282', start: '2024-05-01', end: '2024-05-05' },
    { name: '\u7aef\u5348\u8282', start: '2024-06-08', end: '2024-06-10' },
    { name: '\u4e2d\u79cb\u8282', start: '2024-09-15', end: '2024-09-17' },
    { name: '\u56fd\u5e86\u8282', start: '2024-10-01', end: '2024-10-07' }
];
let calCompensatoryDays = [
    '2024-02-04', '2024-04-07', '2024-04-28', '2024-05-11',
    '2024-09-14', '2024-09-29', '2024-10-12'
];
let calWeekends = [0, 6];

// Helpers
function calFmt(d) {
    return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}
function calParse(s) {
    let p = s.split('-'); return new Date(+p[0], +p[1]-1, +p[2]);
}
function calHolidaySet() {
    let s = new Set();
    calHolidayIntervals.forEach(iv => {
        if (!iv.start || !iv.end) return;
        let cur = calParse(iv.start), end = calParse(iv.end);
        while (cur <= end) { s.add(calFmt(cur)); cur.setDate(cur.getDate()+1); }
    });
    return s;
}
function calIsWork(d, hSet, cSet, wSet) {
    let s = calFmt(d);
    if (cSet.has(s)) return true;
    if (hSet.has(s)) return false;
    return !wSet.has(d.getDay());
}
function calAllDates(year) {
    let dates = [], cur = new Date(year, 0, 1), end = new Date(year, 11, 31);
    while (cur <= end) { dates.push(new Date(cur)); cur.setDate(cur.getDate()+1); }
    return dates;
}
function calWeekNum(d) {
    let c = new Date(d); c.setHours(0,0,0,0); c.setDate(c.getDate()+3-(c.getDay()+6)%7);
    let y = c.getFullYear(), first = new Date(y, 0, 4);
    let mon = new Date(first); mon.setDate(first.getDate()-(first.getDay()+6)%7);
    return Math.floor((c-mon)/86400000/7)+1;
}

// Render
function calRender() {
    let year = +document.getElementById('calYearInput').value;
    if (!year) return;
    let hSet = calHolidaySet(), cSet = new Set(calCompensatoryDays.filter(d=>d));
    let wSet = new Set(calWeekends), dates = calAllDates(year);
    let weeks = [], curWeek = [];
    let fd = new Date(year,0,1);
    for (let i=0; i<fd.getDay(); i++) curWeek.push(null);
    dates.forEach(d => {
        curWeek.push(d);
        if (d.getDay()===6) { while (curWeek.length<7) curWeek.push(null); weeks.push([...curWeek]); curWeek=[]; }
    });
    if (curWeek.length) { while (curWeek.length<7) curWeek.push(null); weeks.push(curWeek); }

    let totalWork = 0;
    let wkData = weeks.map(wk => {
        let real = wk.find(d=>d);
        let wn = real ? calWeekNum(real) : 0;
        let days = wk.map(d => {
            if (!d) return null;
            let s = calFmt(d), ic = cSet.has(s), ih = hSet.has(s);
            let w = calIsWork(d, hSet, cSet, wSet);
            if (w) totalWork++;
            let t = ic ? '\u8865\u73ed' : ih ? '\u5047\u65e5' : w ? '\u5de5\u4f5c' : '\u4f11\u606f';
            return {s, d:d.getDate(), m:d.getMonth()+1, w, ic, ih, t};
        });
        return {wn, days};
    });

    document.getElementById('calTotalDays').textContent = totalWork;

    let tbody = document.getElementById('calTableBody');
    tbody.innerHTML = '';
    wkData.forEach(wk => {
        let tr = document.createElement('tr');
        let tdw = document.createElement('td');
        tdw.style.cssText = 'background:#eef0f3;font-weight:700;text-align:center;padding:6px 4px;border:1px solid #e4edf5;';
        tdw.textContent = wk.wn;
        tr.appendChild(tdw);
        (wk.days||[]).forEach(d => {
            let td = document.createElement('td');
            td.style.cssText = 'border:1px solid #e4edf5;text-align:center;padding:6px 4px;';
            if (!d) { td.textContent = '\u2014'; td.style.background = '#fafcff'; }
            else {
                td.innerHTML = '<div style="font-weight:600;font-size:0.85rem;">'+d.m+'/'+d.d+'</div>';
                let badge = document.createElement('div');
                badge.style.cssText = 'display:inline-block;margin-top:4px;font-size:0.65rem;border-radius:30px;padding:2px 8px;';
                if (d.ic) { badge.style.cssText += 'background:#d9effa;color:#00668c;'; badge.textContent = '\ud83d\udd27\u8865\u73ed'; td.style.background='#ecf7fc'; }
                else if (d.ih) { badge.style.cssText += 'background:#ffdec2;color:#bc5100;'; badge.textContent = '\ud83d\udcc5\u5047\u65e5'; td.style.background='#fff7ef'; }
                else if (!d.w) { badge.style.cssText += 'background:#ffe6e5;color:#b13e3e;'; badge.textContent = '\u4f11'; td.style.background='#fff5f5'; }
                else { badge.style.cssText += 'background:#e1f7dc;color:#2c6e2c;'; badge.textContent = '\u5de5\u4f5c'; }
                td.appendChild(badge);
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// Interval table render
function calRenderHolidayTable() {
    let tb = document.getElementById('calHolidayTbody');
    tb.innerHTML = '';
    if (!calHolidayIntervals.length) {
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.colSpan = 4; td.style.textAlign = 'center'; td.textContent = '\u6682\u65e0\u8282\u5047\u65e5';
        tr.appendChild(td); tb.appendChild(tr);
        return;
    }
    calHolidayIntervals.forEach((iv, i) => {
        let tr = document.createElement('tr');
        // Name
        let td1 = document.createElement('td');
        let inp1 = document.createElement('input');
        inp1.type = 'text'; inp1.value = iv.name;
        inp1.style.cssText = 'width:70px;padding:3px 4px;border:1px solid #cbd5e1;border-radius:6px;font-size:0.75rem;';
        inp1.onchange = e => { calHolidayIntervals[i].name = e.target.value; calRender(); };
        td1.appendChild(inp1);
        // Start
        let td2 = document.createElement('td');
        let inp2 = document.createElement('input');
        inp2.type = 'date'; inp2.value = iv.start;
        inp2.style.cssText = 'width:110px;padding:3px 4px;border:1px solid #cbd5e1;border-radius:6px;font-size:0.75rem;';
        inp2.onchange = e => { calHolidayIntervals[i].start = e.target.value; calRender(); };
        td2.appendChild(inp2);
        // End
        let td3 = document.createElement('td');
        let inp3 = document.createElement('input');
        inp3.type = 'date'; inp3.value = iv.end;
        inp3.style.cssText = 'width:110px;padding:3px 4px;border:1px solid #cbd5e1;border-radius:6px;font-size:0.75rem;';
        inp3.onchange = e => { calHolidayIntervals[i].end = e.target.value; calRender(); };
        td3.appendChild(inp3);
        // Delete
        let td4 = document.createElement('td');
        let btn = document.createElement('button');
        btn.textContent = '\ud83d\uddd1\ufe0f';
        btn.style.cssText = 'background:none;border:none;cursor:pointer;font-size:1rem;color:#b91c1c;';
        btn.onclick = () => { calHolidayIntervals.splice(i,1); calRenderHolidayTable(); calRender(); };
        td4.appendChild(btn);

        tr.appendChild(td1); tr.appendChild(td2); tr.appendChild(td3); tr.appendChild(td4);
        tb.appendChild(tr);
    });
}

function calRenderCompTable() {
    let tb = document.getElementById('calCompTbody');
    tb.innerHTML = '';
    if (!calCompensatoryDays.length) {
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.colSpan = 2; td.style.textAlign = 'center'; td.textContent = '\u6682\u65e0\u8865\u73ed';
        tr.appendChild(td); tb.appendChild(tr);
        return;
    }
    calCompensatoryDays.forEach((d, i) => {
        let tr = document.createElement('tr');
        let td1 = document.createElement('td');
        let inp = document.createElement('input');
        inp.type = 'date'; inp.value = d;
        inp.style.cssText = 'width:140px;padding:3px 4px;border:1px solid #cbd5e1;border-radius:6px;font-size:0.75rem;';
        inp.onchange = e => { calCompensatoryDays[i] = e.target.value; calRender(); };
        td1.appendChild(inp);
        let td2 = document.createElement('td');
        let btn = document.createElement('button');
        btn.textContent = '\ud83d\uddd1\ufe0f';
        btn.style.cssText = 'background:none;border:none;cursor:pointer;font-size:1rem;color:#b91c1c;';
        btn.onclick = () => { calCompensatoryDays.splice(i,1); calRenderCompTable(); calRender(); };
        td2.appendChild(btn);
        tr.appendChild(td1); tr.appendChild(td2);
        tb.appendChild(tr);
    });
}

function calAddHoliday() {
    let y = document.getElementById('calYearInput').value;
    calHolidayIntervals.push({name:'\u65b0\u8282\u65e5', start:y+'-01-01', end:y+'-01-01'});
    calRenderHolidayTable(); calRender();
}
function calAddComp() {
    let y = document.getElementById('calYearInput').value;
    calCompensatoryDays.push(y+'-01-01');
    calRenderCompTable(); calRender();
}
function calSyncYear() {
    let y = document.getElementById('calYearInput').value;
    calHolidayIntervals.forEach(iv => {
        if (iv.start && iv.start.match(/\d{4}-\d{2}-\d{2}/)) {
            let p = iv.start.split('-'); iv.start = y+'-'+p[1]+'-'+p[2];
        }
        if (iv.end && iv.end.match(/\d{4}-\d{2}-\d{2}/)) {
            let p = iv.end.split('-'); iv.end = y+'-'+p[1]+'-'+p[2];
        }
    });
    calCompensatoryDays = calCompensatoryDays.map(d => {
        if (d.match(/\d{4}-\d{2}-\d{2}/)) { let p = d.split('-'); return y+'-'+p[1]+'-'+p[2]; }
        return d;
    });
    calRenderHolidayTable(); calRenderCompTable(); calRender();
}

function calInit() {
    // Weekend checkboxes
    let g = document.getElementById('calWeekendGroup');
    g.innerHTML = '';
    ['\u5468\u65e5','\u5468\u4e00','\u5468\u4e8c','\u5468\u4e09','\u5468\u56db','\u5468\u4e94','\u5468\u516d'].forEach((n,i) => {
        let lbl = document.createElement('label');
        lbl.style.cssText = 'display:inline-flex;align-items:center;gap:4px;background:#f1f5f9;padding:3px 10px;border-radius:30px;font-size:0.75rem;cursor:pointer;';
        let cb = document.createElement('input');
        cb.type = 'checkbox'; cb.checked = calWeekends.includes(i);
        cb.onchange = e => {
            if (e.target.checked) { if (!calWeekends.includes(i)) calWeekends.push(i); }
            else calWeekends = calWeekends.filter(v => v !== i);
            calRender();
        };
        lbl.appendChild(cb); lbl.appendChild(document.createTextNode(n)); g.appendChild(lbl);
    });

    // Bind events
    document.getElementById('calYearInput').onchange = calRender;
    document.getElementById('calSyncBtn').onclick = calSyncYear;
    document.getElementById('calAddInterval').onclick = calAddHoliday;
    document.getElementById('calAddComp').onclick = calAddComp;

    calRenderHolidayTable(); calRenderCompTable(); calRender();
}

// Auto-init when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', calInit);
} else {
    calInit();
}
"""

# ── Build the full spec ──
SPEC = {
    "name": "动态周历·假日区间管理仪表板（完整交互版）",
    "desc": "完全交互式仪表板：年份控制、周末规则、节假日区间CRUD、补班管理、每周日历视图、总工日统计",
    "source": "智能周历系统（用户模板泛化）",
    "card_style": {
        "max_width": "1600px",
        "width": "100%",
        "bg": "#eef2f7",
        "border_radius": "28px",
        "shadow": "0 20px 35px -12px rgba(0,0,0,0.12)",
        "padding": "24px 28px 36px",
    },
    "grid": {
        "rows": 5,
        "cols": 3,
        "gap": "16px",
        "cells": [
            {"id": "header", "row": 0, "col": 0, "colspan": 3,
             "html": HEADER_HTML},
            {"id": "year-control", "row": 1, "col": 0,
             "html": YEAR_HTML},
            {"id": "holiday-table", "row": 1, "col": 1,
             "html": HOLIDAY_HTML},
            {"id": "comp-table", "row": 1, "col": 2,
             "html": COMP_HTML},
            {"id": "stat", "row": 2, "col": 0, "colspan": 3,
             "html": STAT_HTML},
            {"id": "calendar", "row": 3, "col": 0, "colspan": 3,
             "html": CALENDAR_HTML},
            {"id": "footer", "row": 4, "col": 0, "colspan": 3,
             "html": FOOTER_HTML},
        ],
    },
    "scripts": CALENDAR_JS,
}

def main():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    out = TEMPLATES_DIR / "calendar-dashboard-interactive.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
    print(f"[OK] Calendar dashboard spec generated: {out}")
    print(f"  Grid: {SPEC['grid']['rows']}×{SPEC['grid']['cols']}, {len(SPEC['grid']['cells'])} cells")
    print(f"  JS size: {len(CALENDAR_JS)} chars")

if __name__ == "__main__":
    main()
