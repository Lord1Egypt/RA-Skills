#!/usr/bin/env node
// dashboard.mjs — Ink TUI 购房决策中枢仪表盘 (支持高交互光标/详情翻页/打开原网页/地图深链)
// 用法: node scripts/dashboard.mjs [PROJECT_ROOT]   （或 npm run dashboard）
// 交互快捷键:
//   ↑ / ↓ (或 k / j): 上下选择房源
//   Enter 或 m: 生成地图静态页面并在浏览器中定位到选定房源
//   i: 查看选定房源的深度评估报告（内嵌滚动视图）
//   o: 在浏览器中打开挂牌原网页 (若无则打开报告文件)
//   p: 切换排序 · r: 刷新数据 · q / Esc: 退出程序或返回主列表
// （交易状态跟踪已移除，见 docs/adr/0001——watchlist 为纯候选清单，备注即事实）

import { join, dirname, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { existsSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { collectReports, parseWatchlist, readReportDetail, num } from './lib/data.mjs';

// ink 的依赖链（string-width）用到了 RegExp 的 v flag，Node 18 上一加载就是 SyntaxError。
// 所以这里必须动态 import：静态 import 会在版本检查之前就把进程炸掉，用户只看到一段看不懂的堆栈。
if (Number(process.versions.node.split('.')[0]) < 20) {
  console.error(`⛔ dashboard 需要 Node ≥ 20，当前是 ${process.versions.node}。`);
  console.error('   ink 的依赖链用了 Node 20 才支持的正则特性（RegExp v flag）。');
  console.error('   核心脚本（scan / doctor / selftest / stats / map）在 Node 18 上照常可用，只有这个 TUI 不行。');
  process.exit(1);
}
const React = (await import('react')).default;
const { useState, useEffect } = React;
const { render, Text, Box, Static, useInput, useApp } = await import('ink');
import { conclusionLabel, riskLabel } from './lib/decision.mjs';

const h = React.createElement;
const ROOT = process.argv[2] ?? join(dirname(fileURLToPath(import.meta.url)), '..');

// ---------- 跨平台打开 URL 或文件 ----------
// 打开的目标里有一部分是**抓取来的房源链接**，所以：
// 1) 不能拼进 shell 字符串——只转义双引号挡不住 `; rm -rf` 这类注入。一律 execFile 传数组，参数不经 shell。
// 2) 按目标类型分别放行：http(s) 交给浏览器；仓库内的文件才允许打开，其余 scheme（javascript:、smb:…）一律拒绝。
const HTTP_URL = /^https?:\/\//i;
const ANY_SCHEME = /^[a-z][a-z0-9+.-]*:/i;
function openExternal(target) {
  if (!target) return;
  const raw = String(target).trim();

  let openArg = null;
  if (HTTP_URL.test(raw)) {
    openArg = raw;
  } else if (/^file:\/\//i.test(raw) || !ANY_SCHEME.test(raw)) {
    // 自己生成的 file:// URL，或仓库内的裸路径 —— 都必须落在 ROOT 内且真实存在
    let abs = raw;
    let tail = '';
    if (/^file:\/\//i.test(raw)) {
      const u = new URL(raw);
      tail = u.search + u.hash;
      abs = fileURLToPath(u.href.slice(0, u.href.length - tail.length));
    } else {
      abs = resolve(ROOT, raw);
    }
    if (!(abs === ROOT || abs.startsWith(ROOT + sep)) || !existsSync(abs)) {
      console.error('⛔ 拒绝打开（不在仓库内或文件不存在）:', raw.slice(0, 80));
      return;
    }
    openArg = pathToFileURL(abs).href + tail;
  } else {
    console.error('⛔ 拒绝打开（只允许 http/https 与仓库内文件）:', raw.slice(0, 80));
    return;
  }

  const cmd = process.platform === 'darwin' ? 'open'
    : process.platform === 'win32' ? 'cmd' : 'xdg-open';
  execFile(cmd, process.platform === 'win32' ? ['/c', 'start', '', openArg] : [openArg],
    err => { if (err) console.error('打开失败:', err.message); });
}

// ---------- 地图：生成静态页面后打开本地文件 ----------
const MAP_OUT_PATH = join(ROOT, 'data', 'map.html');

// 地图是纯静态单文件页面（数据内联在 HTML 里），没有本地服务、没有开放端口。
// 每次调用都重新生成，保证打开的是最新的报告数据；?house= 深链由页面自己解析。
function openMapForHouse(house, notify = () => {}) {
  notify(house ? `🗺️ 正在生成地图并定位 ${house.no} ${house.community}…` : '🗺️ 正在生成房源地图…');
  execFile(process.execPath, [join(ROOT, 'scripts', 'map.mjs')], (err) => {
    if (err) {
      notify('❌ 地图生成失败——可手动运行 npm run map 查看');
      return;
    }
    const q = house?.no ? `?house=${encodeURIComponent(house.no)}` : '';
    openExternal(pathToFileURL(MAP_OUT_PATH).href + q);
  });
}

// ---------- CJK 视觉宽度工具 ----------
const WIDE = /[\u1100-\u115F\u2E80-\uA4CF\uAC00-\uD7A3\uF900-\uFAFF\uFE10-\uFE19\uFE30-\uFE6F\uFF00-\uFF60\uFFE0-\uFFE6\u3000-\u303E]/;
const vwidth = s => [...String(s)].reduce((n, ch) => n + (WIDE.test(ch) ? 2 : 1), 0);
const pad = (s, w) => { s = String(s); const d = w - vwidth(s); return d > 0 ? s + ' '.repeat(d) : s; };
const trunc = (s, w) => {
  s = String(s ?? '');
  if (vwidth(s) <= w) return s;
  let out = '';
  for (const ch of s) { if (vwidth(out + ch) > w - 1) break; out += ch; }
  return out + '…';
};

// ---------- 排序比较器（loadData 默认序与 p 键切换共用，唯一实现） ----------
const WATCHLIST_COMPARATORS = {
  score: (a, b) => {
    const sa = num(a.score), sb = num(b.score);
    if (sa != null && sb != null) return sb !== sa ? sb - sa : String(a.no).localeCompare(String(b.no));
    return sa != null ? -1 : sb != null ? 1 : String(a.no).localeCompare(String(b.no));
  },
  price: (a, b) => {
    const pa = num(a.price), pb = num(b.price);
    if (pa != null && pb != null) return pa !== pb ? pa - pb : String(a.no).localeCompare(String(b.no));
    return pa != null ? -1 : pb != null ? 1 : String(a.no).localeCompare(String(b.no));
  },
  no: (a, b) => String(a.no).localeCompare(String(b.no)),
};

// ---------- 数据加载 ----------
async function loadData() {
  const [reports, watchlist] = await Promise.all([
    collectReports(join(ROOT, 'reports')),
    parseWatchlist(join(ROOT, 'data', 'watchlist.md')),
  ]);
  // 默认按综合评分降序（高分在先）；TUI 内 p 键切换经 displayWatchlist 用同一张比较器表
  const sortedWatchlist = [...(watchlist ?? [])].sort(WATCHLIST_COMPARATORS.score);
  return { reports, watchlist: sortedWatchlist, loadedAt: new Date() };
}

// ---------- 样式与辅助 ----------
// 真实性/结论/风险的语义来自 lib/data.mjs 与 lib/decision.mjs 唯一实现，这里只做 TUI 着色
const scoreColor = s => (s == null ? 'gray' : s >= 4 ? 'green' : s >= 3.5 ? 'yellow' : 'red');
const riskColor = r => ({ 低: 'green', 注意: 'yellow', 高: 'red' }[riskLabel(r)] ?? 'gray');

const dim = (s, key) => h(Text, { key, color: 'gray' }, s);
function sectionTitle(title) {
  return h(Text, { bold: true }, ` ${title} `, h(Text, { color: 'gray' }, '─'.repeat(Math.max(0, 56 - vwidth(title)))));
}

// ---------- 关注清单表格 (带光标指示与高亮) ----------
// 编号列宽需容纳真实性前缀标记（⚠️/⛔ 各占 2 视觉宽）+ 3 位编号，否则会被截断成「⚠ 0…」
const COLS = [
  ['编号', 7], ['小区/项目', 16], ['板块', 18], ['总价万', 8], ['评分', 8], ['风险', 8],
];
const ROW = [r => r.no, r => r.community, r => r.district, r => r.price, r => r.score, r => r.risk];

function WatchTable({ rows, selectedIndex }) {
  const header = h(Box, { key: 'h' }, [
    h(Box, { key: 'ptr', width: 3 }, h(Text, { bold: true }, '  ')),
    ...COLS.map(([name, w]) =>
      h(Box, { key: name, width: w }, h(Text, { bold: true }, pad(trunc(name, w - 2), w))))
  ]);

  const body = rows.map((r, idx) => {
    const isSelected = idx === selectedIndex;
    const ptr = isSelected ? '▶ ' : '  ';
    const ptrColor = isSelected ? 'cyan' : undefined;

    return h(Box, { key: r.no }, [
      h(Box, { key: 'ptr', width: 3 }, h(Text, { bold: isSelected, color: ptrColor }, ptr)),
      ...COLS.map(([name, w], i) => {
        const raw = ROW[i](r);
        let color = i === 4 ? scoreColor(num(r.score))
          : i === 5 ? riskColor(String(r.risk ?? '').trim())
          : undefined;

        if (isSelected && i <= 3) {
          color = 'cyan';
        }
        return h(Box, { key: name, width: w },
          h(Text, { bold: isSelected, color, underline: isSelected && i === 1, dimColor: r.authenticity === 'void' },
            pad(trunc((i === 0 && r.authenticity === 'suspect' ? '⚠ ' : i === 0 && r.authenticity === 'void' ? '⛔ ' : '') + raw, w - 2), w)));
      })
    ]);
  });

  return h(Box, { flexDirection: 'column' }, [header, ...body]);
}

// ---------- 综合评分直方图 ----------
function Histogram({ scores }) {
  const bins = [
    ['<3.0', s => s < 3],
    ['3.0-3.5', s => s >= 3 && s < 3.5],
    ['3.5-4.0', s => s >= 3.5 && s < 4],
    ['4.0-4.5', s => s >= 4 && s < 4.5],
    ['4.5+', s => s >= 4.5],
  ];
  return h(Box, { flexDirection: 'column' }, bins.map(([label, pred]) => {
    const n = scores.filter(pred).length;
    return h(Box, { key: label }, [
      h(Text, { key: 'l' }, pad(label, 8)),
      h(Text, { key: 'b', color: n ? 'green' : 'gray' }, ' ' + (n ? '█'.repeat(n) : '·')),
      n ? h(Text, { key: 'c', dimColor: true }, ` ${n}`) : null,
    ]);
  }));
}

// ---------- 报告详情视图 (Report Viewer) ----------
function ReportViewer({ reportDetail, reportMeta, scrollOffset, totalLines }) {
  if (!reportDetail) {
    return h(Box, { flexDirection: 'column', padding: 1 }, [
      h(Text, { color: 'yellow', bold: true }, '⚠️ 未找到该房源对应的评估报告'),
      dim('按 Esc 或 q 返回关注清单')
    ]);
  }

  const lines = reportDetail.text.split('\n');
  const visibleCount = 20;
  const maxScroll = Math.max(0, lines.length - visibleCount);
  const currentScroll = Math.min(scrollOffset, maxScroll);
  const displayedLines = lines.slice(currentScroll, currentScroll + visibleCount);

  return h(Box, { flexDirection: 'column' }, [
    // 报告标题栏
    h(Box, { key: 'head', marginBottom: 1, borderStyle: 'round', borderColor: 'cyan', paddingX: 1, flexDirection: 'column' }, [
      h(Box, { key: 'info' }, [
        h(Text, { key: 't', bold: true, color: 'cyan' }, `📄 深度评估报告 · ${reportMeta?.no ?? '???'} ${reportMeta?.community ?? ''}  `),
        h(Text, { key: 's', color: scoreColor(num(reportMeta?.score)) }, `综合评分: ${reportMeta?.score ?? '—'}  `),
        h(Text, { key: 'r', color: riskColor(reportMeta?.risk) }, `风险: ${reportMeta?.risk ?? '—'}  `)
      ]),
      reportDetail.url ? h(Text, { key: 'url', color: 'gray' }, `🔗 挂牌链接: ${reportDetail.url}`) : null
    ]),

    // 报告正文视口
    h(Box, { key: 'body', flexDirection: 'column', minHeight: 20, paddingX: 1 },
      displayedLines.map((line, idx) => {
        let color = undefined;
        let bold = false;
        if (line.startsWith('# ')) { color = 'magenta'; bold = true; }
        else if (line.startsWith('## ')) { color = 'cyan'; bold = true; }
        else if (line.startsWith('### ')) { color = 'yellow'; bold = true; }
        else if (line.includes('```')) { color = 'gray'; }
        else if (line.startsWith('- **') || line.startsWith('|')) { color = 'white'; }
        return h(Text, { key: String(currentScroll + idx), color, bold }, line || ' ');
      })
    ),

    // 滚动与操作指示
    h(Box, { key: 'nav', marginTop: 1, borderStyle: 'single', borderColor: 'gray', paddingX: 1 }, [
      h(Text, { key: 'pg', color: 'green' }, `[第 ${currentScroll + 1}-${Math.min(lines.length, currentScroll + visibleCount)} 行 / 共 ${lines.length} 行] `),
      h(Text, { key: 'hlp', bold: true }, '↑/↓: 滚动 · m: 地图定位 · o: 打开原网页 · Esc / q: 返回列表')
    ])
  ]);
}

// ---------- 主控制台视图 (List View) ----------
function MainView({ data, selectedIndex, flashMessage, sortMode = 'score' }) {
  if (!data || !data.loadedAt) return dim(' 载入中…');
  const { reports = [], watchlist = [], loadedAt } = data;
  const date = loadedAt instanceof Date
    ? `${loadedAt.getFullYear()}-${String(loadedAt.getMonth() + 1).padStart(2, '0')}-${String(loadedAt.getDate()).padStart(2, '0')}`
    : new Date().toISOString().slice(0, 10);
  // ⛔作废已在 data 层过滤（ADR-0002：collectReports/parseWatchlist 默认排除 void）
  const validReports = reports;
  const scores = validReports.map(r => num(r.score_global)).filter(v => v != null);
  const avg = scores.length ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(2) : '—';
  const top = [...validReports].sort((a, b) => (num(b.score_global) ?? 0) - (num(a.score_global) ?? 0)).slice(0, 3);
  const sortLabels = { score: '按综合评分高→低', no: '按编号顺序', price: '按总价低→高' };

  return h(Box, { flexDirection: 'column' }, [
    h(Box, { key: 'head', marginBottom: 1 },
      h(Text, { bold: true, color: 'magenta' }, 'house-ops 购房操作台'),
      dim(`  ${date}  ·  评估报告 ${reports.length} 份 · 候选 ${watchlist.length} 套 · 均分 ${avg}`, 'sub')),

    h(Box, { key: 'wl', flexDirection: 'column', marginBottom: 1 },
      sectionTitle(`关注清单 [${sortLabels[sortMode] || '综合评分'}] (上下移动)`),
      watchlist.length
        ? h(WatchTable, { rows: watchlist, selectedIndex })
        : dim('  （还没有候选房源）')),

    h(Box, { key: 'hist', flexDirection: 'column', marginBottom: 1 },
      sectionTitle('综合评分分布'),
      scores.length ? h(Histogram, { scores }) : dim('  （还没有评分）')),

    h(Box, { key: 'top', flexDirection: 'column', marginBottom: 1 },
      sectionTitle('Top 高分房源'),
      top.length
        ? h(Box, { flexDirection: 'column' }, top.map((r, i) =>
            h(Box, { key: String(r.report_no ?? r.file) },
              h(Text, { color: i === 0 ? 'yellow' : 'gray' }, `${i + 1}. `),
              h(Text, null, `${r.report_no ?? '???'} ${trunc(r.community, 18)}  `),
              h(Text, { color: scoreColor(num(r.score_global)) }, `评分 ${r.score_global ?? '—'}`),
              dim(`  ${conclusionLabel(r.conclusion)}`))))
        : dim('  （还没有评估报告 — 粘贴一条房源链接开始）')),

    // 即时反馈 Toast
    flashMessage
      ? h(Box, { key: 'flash', marginTop: 1 }, h(Text, { color: 'cyan', bold: true }, `💡 ${flashMessage}`))
      : null,

    // 快捷键底栏
    h(Box, { key: 'foot', marginTop: 1, borderStyle: 'single', borderColor: 'gray', paddingX: 1 },
      h(Text, { bold: true }, '↑/↓: 移动 · Enter/m: 地图定位 · i: 报告 · o: 挂牌页 · p: 排序 · r: 刷新 · q: 退出')
    ),
  ]);
}

// ---------- 交互壳容器 ----------
function Interactive({ onReady }) {
  const [data, setData] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [sortMode, setSortMode] = useState('score'); // 'score' | 'no' | 'price'
  const [viewMode, setViewMode] = useState('list'); // 'list' | 'report'
  const [reportDetail, setReportDetail] = useState(null);
  const [reportScroll, setReportScroll] = useState(0);
  const [flashMessage, setFlashMessage] = useState('');
  const { exit } = useApp();

  const showToast = (msg, duration = 3000) => {
    setFlashMessage(msg);
    setTimeout(() => setFlashMessage(''), duration);
  };

  const refreshAll = () => {
    loadData().then(d => {
      setData(d);
      setSelectedIndex(idx => Math.min(idx, Math.max(0, (d.watchlist?.length ?? 1) - 1)));
    });
  };

  useEffect(() => {
    let on = true;
    loadData().then(d => {
      if (on) {
        setData(d);
        onReady();
      }
    });
    return () => { on = false; };
  }, []);

  const displayWatchlist = React.useMemo(() => {
    if (!data?.watchlist) return [];
    // ⛔作废行已在 parseWatchlist 下沉过滤（ADR-0002）；⚠存疑行保留但标记
    return [...data.watchlist].sort(WATCHLIST_COMPARATORS[sortMode] ?? WATCHLIST_COMPARATORS.no);
  }, [data?.watchlist, sortMode]);

  useInput((input, key) => {
    if (!data) return;
    const currentHouse = displayWatchlist[selectedIndex];

    // ===== 模式 1: 详情报告视图 =====
    if (viewMode === 'report') {
      if (input === 'q' || key.escape || key.backspace || key.delete) {
        setViewMode('list');
        setReportDetail(null);
        return;
      }
      if (key.upArrow || input === 'k') {
        setReportScroll(s => Math.max(0, s - 2));
        return;
      }
      if (key.downArrow || input === 'j') {
        setReportScroll(s => s + 2);
        return;
      }
      if (key.pageUp) {
        setReportScroll(s => Math.max(0, s - 10));
        return;
      }
      if (key.pageDown) {
        setReportScroll(s => s + 10);
        return;
      }
      if (input === 'o') {
        if (reportDetail?.url) {
          openExternal(reportDetail.url);
          showToast(`已在浏览器打开: ${reportDetail.url}`);
        } else if (reportDetail?.filePath) {
          openExternal(reportDetail.filePath);
          showToast(`已在默认应用打开报告: ${reportDetail.file}`);
        }
        return;
      }
      if (input === 'm') {
        openMapForHouse(currentHouse, showToast);
        return;
      }
      return;
    }

    // ===== 模式 2: 主列表视图 =====
    if (input === 'q') {
      exit();
      return;
    }
    if (input === 'r') {
      refreshAll();
      showToast('🔄 已重新加载最新数据');
      return;
    }
    if (key.upArrow || input === 'k') {
      setSelectedIndex(i => Math.max(0, i - 1));
      return;
    }
    if (key.downArrow || input === 'j') {
      setSelectedIndex(i => Math.min(Math.max(0, displayWatchlist.length - 1), i + 1));
      return;
    }
    // Enter / m：拉起地图服务并在浏览器中定位到选定房源（深链）
    if (key.return || input === 'm') {
      if (!currentHouse) return;
      openMapForHouse(currentHouse, showToast);
      return;
    }
    // i 键查看内嵌详情报告
    if (input === 'i') {
      if (!currentHouse) return;
      readReportDetail(join(ROOT, 'reports'), currentHouse.no).then(detail => {
        if (detail) {
          setReportDetail(detail);
          setReportScroll(0);
          setViewMode('report');
        } else {
          showToast(`⚠️ 未找到编号 ${currentHouse.no} 的详细评估报告`);
        }
      });
      return;
    }
    // o 键打开原始挂牌网页或报告
    if (input === 'o') {
      if (!currentHouse) return;
      readReportDetail(join(ROOT, 'reports'), currentHouse.no).then(detail => {
        if (detail?.url) {
          openExternal(detail.url);
          showToast(`🌐 正在浏览器打开 ${currentHouse.community} 挂牌页面...`);
        } else if (detail?.filePath) {
          openExternal(detail.filePath);
          showToast(`📄 打开本地评估报告: ${detail.file}`);
        } else {
          showToast(`⚠️ 该房源暂无挂牌 URL 记录`);
        }
      });
      return;
    }
    // p 键切换排序方式
    if (input === 'p') {
      const next = sortMode === 'score' ? 'no' : sortMode === 'no' ? 'price' : 'score';
      setSortMode(next);
      setSelectedIndex(0);
      const labels = { score: '综合评分 (从高到低)', no: '编号顺序 (升序)', price: '总价 (从低到高)' };
      showToast(`🔀 已切换排序方式: ${labels[next]}`);
      return;
    }
  });

  if (!data) {
    return h(Box, { padding: 1 }, [
      h(Text, { color: 'cyan', bold: true }, '⏳ 正在加载房源数据…')
    ]);
  }

  const currentHouse = displayWatchlist[selectedIndex];

  if (viewMode === 'report') {
    return h(ReportViewer, {
      reportDetail,
      reportMeta: currentHouse,
      scrollOffset: reportScroll,
      totalLines: reportDetail?.text?.split('\n')?.length ?? 0
    });
  }

  return h(Box, { flexDirection: 'column' }, [
    h(MainView, {
      key: 'main',
      data: { ...data, watchlist: displayWatchlist },
      selectedIndex,
      flashMessage,
      sortMode
    })
  ]);
}

// ---------- 运行启动 ----------
const isTTY = Boolean(process.stdout.isTTY && process.stdin.isTTY);
if (isTTY) {
  let markReady;
  const ready = new Promise(resolve => { markReady = resolve; });
  const instance = render(h(Interactive, { onReady: markReady }), { exitOnCtrlC: true });
  await instance.waitUntilExit();
} else {
  // 管道/CI: 单帧静态纯文本输出（⛔作废行已在 data 层过滤，与 TTY 同规则）
  const data = await loadData();
  const frame = { ...data, watchlist: data.watchlist ?? [] };
  const instance = render(
    h(Static, { items: ['dash'] }, item => h(Box, { key: item, flexDirection: 'column' }, h(MainView, {
      data: frame,
      selectedIndex: 0,
      sortMode: 'score'
    })))
  );
  setTimeout(() => instance.unmount(), 50);
  await instance.waitUntilExit();
}
