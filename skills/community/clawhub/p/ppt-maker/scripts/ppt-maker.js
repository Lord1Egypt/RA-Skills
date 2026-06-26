/**
 * PPT Maker - Markdown to PPTX Generator
 * Supports auto charts (pie/bar/line), multiple themes, ending page detection.
 */

var PptxGenJS = require("pptxgenjs");

// ══════════════════════════════════════════════════════
//  1. Themes & Colors (no # prefix)
// ══════════════════════════════════════════════════════

var THEMES = {
  sunset:   { bg: 'FFF8F3', title: 'E85D04', text: '3D405B', accent: 'F48C06', secondary: 'FAA307', light: 'FFECD2', lighter: 'FFF5EB' },
  ocean:    { bg: 'F0F8FF', title: '0077B6', text: '2D3748', accent: '00B4D8', secondary: '90E0EF', light: 'CAF0F8', lighter: 'E8F8FF' },
  purple:   { bg: 'FAF5FF', title: '7C3AED', text: '4C1D95', accent: 'A78BFA', secondary: 'C4B5FD', light: 'EDE9FE', lighter: 'F5F3FF' },
  luxury:   { bg: '1C1917', title: 'F5F5F4', text: 'A8A29E', accent: 'D4AF37', secondary: 'F59E0B', light: '292524', lighter: '1C1917' },
  midnight: { bg: '0F172A', title: 'F8FAFC', text: 'CBD5E1', accent: '38BDF8', secondary: '60A5FA', light: '1E293B', lighter: '0F172A' },
  classic:  { bg: 'FFFFFF', title: '1F2937', text: '4B5563', accent: '059669', secondary: '10B981', light: 'ECFDF5', lighter: 'F0FDF4' }
};

var CHART_COLORS = {
  ocean:    ['0077B6', '00B4D8', '90E0EF', '48CAE4', '023E8A', '0096C7', 'ADE8F4'],
  sunset:   ['E85D04', 'F48C06', 'FAA307', 'FFBA08', 'DC2F02', 'E36414', 'F77F00'],
  purple:   ['7C3AED', 'A78BFA', 'C4B5FD', '8B5CF6', '6D28D9', '5B21B6', 'DDD6FE'],
  luxury:   ['D4AF37', 'F59E0B', 'FBBF24', 'FFD700', 'B8860B', 'D97706', 'FCD34D'],
  midnight: ['38BDF8', '60A5FA', '93C5FD', '2563EB', '1D4ED8', '3B82F6', 'BFDBFE'],
  classic:  ['059669', '10B981', '34D399', '6EE7B7', '047857', '065F46', 'A7F3D0']
};

var CHART_RULES = [
  { type: 'pie',  keys: ['饼图', '饼状图', '占比', '比例', '份额', '构成', '组成', '百分比', '比重', 'pie', 'proportion', 'share'] },
  { type: 'line', keys: ['折线', '折线图', '趋势', '增长', '变化', '走势', '曲线', '时间', '月度', '季度', '年度', 'line', 'trend'] },
  { type: 'bar',  keys: ['柱状', '柱状图', '柱形', '柱形图', '排名', 'top', '对比', '比较', '分布', '销售额', '金额', '数量', '业绩', '产量', '营收', '收入', 'bar', 'column', 'chart'] }
];

var ENDING_KEYWORDS = ['感谢', '谢谢', 'thank', 'thanks', 'q&a', 'q & a', '问答', '结束', 'the end', '再见', '联系方式', '联系我们'];

// ══════════════════════════════════════════════════════
//  2. Utility Functions
// ══════════════════════════════════════════════════════

function stripInlineMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/__(.+?)__/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/_(.+?)_/g, '$1')
    .replace(/~~(.+?)~~/g, '$1')
    .replace(/`(.+?)`/g, '$1')
    .replace(/\[(.+?)\]\(.+?\)/g, '$1')
    .trim();
}

function isTableSeparator(line) {
  var inner = line.replace(/^\|/, '').replace(/\|$/, '');
  var cells = inner.split('|');
  return cells.length > 0 && cells.every(function(c) {
    return /^\s*:?-{2,}:?\s*$/.test(c);
  });
}

function isEndingSlide(title) {
  if (!title) return false;
  var lower = title.toLowerCase().trim();
  return ENDING_KEYWORDS.some(function(k) { return lower.indexOf(k) !== -1; });
}

function parseNumericCell(raw) {
  if (!raw) return NaN;
  var cleaned = raw
    .replace(/[,，]/g, '')
    .replace(/[%％]/g, '')
    .replace(/[￥¥$€£₩]/g, '')
    .replace(/[元万亿千百十个份人次件台套组年月日号]/g, '')
    .replace(/[（()）\s]/g, '')
    .trim();
  return parseFloat(cleaned);
}

function ensureColors(colors, needed) {
  var result = [];
  for (var i = 0; i < needed; i++) {
    result.push(colors[i % colors.length]);
  }
  return result;
}

// ══════════════════════════════════════════════════════
//  3. Markdown Parser
// ══════════════════════════════════════════════════════

function parse(text) {
  var slides = [];
  var lines = text.split('\n');
  var current = null;
  var inCode = false;
  var codeContent = [];

  for (var li = 0; li < lines.length; li++) {
    var line = lines[li];
    var trimmed = line.trim();

    if (trimmed.indexOf('```') === 0) {
      if (inCode) {
        if (current) {
          current.content.push({ type: 'code', code: codeContent.join('\n') });
        }
        codeContent = [];
      }
      inCode = !inCode;
      continue;
    }
    if (inCode) {
      codeContent.push(line);
      continue;
    }

    if (!trimmed) continue;

    if (/^# (?!#)/.test(trimmed)) {
      if (current) slides.push(current);
      current = {
        type: 'cover',
        title: stripInlineMarkdown(trimmed.slice(2)),
        subtitle: '',
        content: []
      };
    }
    else if (/^## (?!#)/.test(trimmed)) {
      if (current) slides.push(current);
      var title = stripInlineMarkdown(trimmed.slice(3));
      current = {
        type: isEndingSlide(title) ? 'ending' : 'content',
        title: title,
        content: []
      };
    }
    else if (trimmed.indexOf('### ') === 0) {
      if (!current) current = { type: 'content', title: '', content: [] };
      current.content.push({ type: 'h3', text: stripInlineMarkdown(trimmed.slice(4)) });
    }
    else if (/^[-*]\s/.test(trimmed)) {
      if (!current) current = { type: 'content', title: '', content: [] };
      var itemText = stripInlineMarkdown(trimmed.replace(/^[-*]\s+/, ''));
      var last = current.content[current.content.length - 1];
      if (last && last.type === 'list') {
        last.items.push(itemText);
      } else {
        current.content.push({ type: 'list', items: [itemText] });
      }
    }
    else if (/^\d+\.\s/.test(trimmed)) {
      if (!current) current = { type: 'content', title: '', content: [] };
      var oItemText = stripInlineMarkdown(trimmed.replace(/^\d+\.\s+/, ''));
      var oLast = current.content[current.content.length - 1];
      if (oLast && oLast.type === 'olist') {
        oLast.items.push(oItemText);
      } else {
        current.content.push({ type: 'olist', items: [oItemText] });
      }
    }
    else if (trimmed.charAt(0) === '|') {
      if (isTableSeparator(trimmed)) continue;
      if (!current) current = { type: 'content', title: '', content: [] };
      var inner = trimmed.replace(/^\|/, '').replace(/\|$/, '');
      var cells = inner.split('|').map(function(c) { return c.trim(); });
      if (cells.length === 0) continue;
      var tLast = current.content[current.content.length - 1];
      if (tLast && tLast.type === 'table') {
        tLast.rows.push(cells);
      } else {
        current.content.push({ type: 'table', rows: [cells] });
      }
    }
    else if (trimmed.charAt(0) === '>') {
      if (!current) current = { type: 'content', title: '', content: [] };
      var quoteText = stripInlineMarkdown(trimmed.replace(/^>\s*/, ''));
      var qLast = current.content[current.content.length - 1];
      if (qLast && qLast.type === 'quote') {
        qLast.lines.push(quoteText);
      } else {
        current.content.push({ type: 'quote', lines: [quoteText] });
      }
    }
    else {
      if (!current) current = { type: 'content', title: '', content: [] };
      var cleaned = stripInlineMarkdown(trimmed);
      if (current.type === 'cover' && !current.subtitle) {
        current.subtitle = cleaned;
      } else {
        current.content.push({ type: 'text', text: cleaned });
      }
    }
  }

  if (inCode && codeContent.length > 0 && current) {
    current.content.push({ type: 'code', code: codeContent.join('\n') });
  }
  if (current) slides.push(current);
  return slides;
}

// ══════════════════════════════════════════════════════
//  4. Chart Detection
// ══════════════════════════════════════════════════════

function extractSeries(table) {
  if (!table.rows || table.rows.length < 2) return null;

  var headers = table.rows[0];
  var dataRows = table.rows.slice(1);
  if (headers.length < 2 || dataRows.length === 0) return null;

  var labels = dataRows.map(function(r) { return (r[0] || '').trim(); });
  var series = [];

  for (var col = 1; col < headers.length; col++) {
    var values = dataRows.map(function(r) { return parseNumericCell(r[col]); });
    if (values.every(function(v) { return !isNaN(v) && isFinite(v); })) {
      series.push({
        name: (headers[col] || '').trim() || ('Series' + col),
        labels: labels,
        values: values
      });
    }
  }
  return series.length > 0 ? series : null;
}

function detectChart(table, slide, tableIndex) {
  var series = extractSeries(table);
  if (!series) return null;

  var labels = series[0].labels;
  var hints = [];

  if (slide.title) hints.push(slide.title.toLowerCase());

  var hintIndex = -1;
  for (var j = tableIndex - 1; j >= 0; j--) {
    var item = slide.content[j];
    if (item.type === 'h3') {
      hints.push(item.text.toLowerCase());
      hintIndex = j;
      break;
    }
    if (item.type === 'text') {
      hints.push(item.text.toLowerCase());
    }
  }

  hints.push(table.rows[0].map(function(h) { return (h || '').toLowerCase(); }).join(' '));

  var combined = hints.join(' ');

  for (var ri = 0; ri < CHART_RULES.length; ri++) {
    var rule = CHART_RULES[ri];
    if (rule.keys.some(function(k) { return combined.indexOf(k) !== -1; })) {
      return { type: rule.type, series: series, labels: labels, hintIndex: hintIndex };
    }
  }

  var vals = series[0].values;
  var sum = vals.reduce(function(a, b) { return a + b; }, 0);
  var count = vals.length;

  if (count >= 2 && count <= 12 && sum >= 80 && sum <= 120) {
    return { type: 'pie', series: series, labels: labels, hintIndex: hintIndex };
  }
  if (count >= 2) {
    return { type: 'bar', series: series, labels: labels, hintIndex: hintIndex };
  }

  return null;
}

// ══════════════════════════════════════════════════════
//  5. Chart Type Resolution (multi-version compat)
// ══════════════════════════════════════════════════════

function getChartType(pres, name) {
  var MAP = { pie: 'PIE', line: 'LINE', bar: 'BAR' };
  var key = MAP[name];
  if (!key) return name;
  if (pres.charts && pres.charts[key] !== undefined) return pres.charts[key];
  if (pres.ChartType && pres.ChartType[key] !== undefined) return pres.ChartType[key];
  if (pres.ChartType && pres.ChartType[name] !== undefined) return pres.ChartType[name];
  return name;
}

// ══════════════════════════════════════════════════════
//  6. Chart Rendering
// ══════════════════════════════════════════════════════

function addChartToSlide(s, pres, chartData, colors, t, layout) {
  var lx = (layout && layout.x) || 0.5;
  var ly = (layout && layout.y) || 1.4;
  var lw = (layout && layout.w) || 9;
  var lh = (layout && layout.h) || 3.8;

  var chartType = getChartType(pres, chartData.type);
  var isPie = chartData.type === 'pie';
  var isLine = chartData.type === 'line';

  var data = isPie ? [chartData.series[0]] : chartData.series;
  var needed = isPie ? data[0].values.length : Math.max(data[0].values.length, data.length);
  var clrs = ensureColors(colors, needed);

  var opts = {
    x: lx, y: ly, w: lw, h: lh,
    chartColors: clrs,
    showLegend: true,
    legendPos: isPie ? 'r' : 'b',
    legendFontSize: 9,
    legendColor: t.text,
    showTitle: false
  };

  if (isPie) {
    opts.showPercent = true;
    opts.showValue = false;
    opts.dataLabelColor = t.text;
    opts.dataLabelFontSize = 10;
  } else if (isLine) {
    opts.lineSize = 2;
    opts.showMarker = true;
    opts.markerSize = 6;
    opts.catAxisLabelColor = t.text;
    opts.catAxisLabelFontSize = 9;
    opts.valAxisLabelColor = t.text;
    opts.valAxisLabelFontSize = 9;
    opts.showValue = true;
    opts.dataLabelColor = t.text;
    opts.dataLabelFontSize = 8;
    opts.dataLabelPosition = 'outEnd';
  } else {
    opts.barDir = 'col';
    opts.barGapWidthPct = 80;
    opts.catAxisLabelColor = t.text;
    opts.catAxisLabelFontSize = 10;
    opts.valAxisLabelColor = t.text;
    opts.valAxisLabelFontSize = 9;
    opts.showValue = true;
    opts.dataLabelColor = t.text;
    opts.dataLabelFontSize = 9;
    opts.dataLabelPosition = 'outEnd';
  }

  s.addChart(chartType, data, opts);
}

// ══════════════════════════════════════════════════════
//  7. Content Rendering
// ══════════════════════════════════════════════════════

function renderTable(s, tableItem, t, startY, maxY, startX, totalW) {
  if (!tableItem.rows || tableItem.rows.length === 0) return startY;

  var colCount = Math.max.apply(null, tableItem.rows.map(function(r) { return r.length; }));
  var cw = totalW / colCount;
  var rowH = 0.35;

  for (var r = 0; r < tableItem.rows.length; r++) {
    var ry = startY + r * rowH;
    if (ry + rowH > maxY) break;

    if (r === 0) {
      s.addShape('rect', {
        x: startX - 0.05, y: ry, w: colCount * cw + 0.1, h: rowH,
        fill: { color: t.light }
      });
    } else if (r % 2 === 0) {
      s.addShape('rect', {
        x: startX - 0.05, y: ry, w: colCount * cw + 0.1, h: rowH,
        fill: { color: t.lighter || t.bg }
      });
    }

    for (var c = 0; c < tableItem.rows[r].length; c++) {
      s.addText(tableItem.rows[r][c], {
        x: startX + c * cw, y: ry, w: cw - 0.05, h: rowH,
        fontSize: 10, color: r === 0 ? t.title : t.text,
        fontFace: 'Arial', bold: r === 0, valign: 'middle'
      });
    }
  }

  var renderedRows = Math.min(tableItem.rows.length, Math.floor((maxY - startY) / rowH));
  return startY + renderedRows * rowH + 0.2;
}

function renderContent(s, content, t, opts) {
  var startY = (opts && opts.startY) || 1.4;
  var maxY = (opts && opts.maxY) || 5.0;
  var x = (opts && opts.x) || 0.4;
  var w = (opts && opts.w) || 8.5;
  var y = startY;

  for (var idx = 0; idx < content.length; idx++) {
    var item = content[idx];
    if (y > maxY) break;

    if (item.type === 'h3') {
      s.addText(item.text, {
        x: x, y: y, w: w, h: 0.4,
        fontSize: 16, color: t.title, fontFace: 'Arial', bold: true
      });
      y += 0.5;
    }
    else if (item.type === 'list') {
      for (var li = 0; li < item.items.length; li++) {
        if (y > maxY) break;
        s.addShape('ellipse', {
          x: x + 0.02, y: y + 0.13, w: 0.09, h: 0.09,
          fill: { color: t.accent }
        });
        s.addText(item.items[li], {
          x: x + 0.22, y: y, w: w - 0.3, h: 0.35,
          fontSize: 13, color: t.text, fontFace: 'Arial'
        });
        y += 0.42;
      }
    }
    else if (item.type === 'olist') {
      for (var oi = 0; oi < item.items.length; oi++) {
        if (y > maxY) break;
        s.addShape('ellipse', {
          x: x, y: y + 0.05, w: 0.22, h: 0.22,
          fill: { color: t.accent }
        });
        s.addText(String(oi + 1), {
          x: x, y: y + 0.05, w: 0.22, h: 0.22,
          fontSize: 9, color: 'FFFFFF', fontFace: 'Arial', bold: true,
          align: 'center', valign: 'middle'
        });
        s.addText(item.items[oi], {
          x: x + 0.3, y: y, w: w - 0.4, h: 0.35,
          fontSize: 13, color: t.text, fontFace: 'Arial'
        });
        y += 0.42;
      }
    }
    else if (item.type === 'code') {
      var lineCount = item.code.split('\n').length;
      var ch = Math.min(2.5, lineCount * 0.22 + 0.3);
      s.addShape('roundRect', {
        x: x - 0.1, y: y, w: w + 0.2, h: ch,
        fill: { color: '1E1E1E' }, rectRadius: 0.05
      });
      s.addText(item.code, {
        x: x + 0.05, y: y + 0.1, w: w - 0.1, h: ch - 0.2,
        fontSize: 10, color: 'D4D4D4', fontFace: 'Consolas', valign: 'top'
      });
      y += ch + 0.2;
    }
    else if (item.type === 'quote') {
      var quoteText = item.lines.join('\n');
      var qLines = item.lines.length;
      var qh = Math.min(2.0, qLines * 0.25 + 0.2);
      s.addShape('rect', {
        x: x, y: y, w: 0.05, h: qh,
        fill: { color: t.accent }
      });
      s.addShape('rect', {
        x: x + 0.05, y: y, w: w - 0.05, h: qh,
        fill: { color: t.light }
      });
      s.addText(quoteText, {
        x: x + 0.2, y: y + 0.05, w: w - 0.3, h: qh - 0.1,
        fontSize: 12, color: t.text, fontFace: 'Arial', italic: true, valign: 'top'
      });
      y += qh + 0.15;
    }
    else if (item.type === 'table') {
      y = renderTable(s, item, t, y, maxY, x, w);
    }
    else if (item.type === 'text') {
      s.addText(item.text, {
        x: x, y: y, w: w, h: 0.35,
        fontSize: 12, color: t.text, fontFace: 'Arial'
      });
      y += 0.4;
    }
  }
  return y;
}

// ══════════════════════════════════════════════════════
//  8. Slide Renderers
// ══════════════════════════════════════════════════════

function addDecorations(s, t) {
  s.addShape('rect', { x: 0, y: 0, w: 10, h: 0.12, fill: { color: t.accent } });
  s.addShape('rect', { x: 0, y: 0, w: 0.10, h: 5.625, fill: { color: t.accent } });
}

function renderCoverSlide(s, slide, t) {
  s.addShape('rect', { x: 0.4, y: 1.3, w: 0.06, h: 1.6, fill: { color: t.accent } });
  s.addText(slide.title, {
    x: 0.7, y: 1.3, w: 8.5, h: 1.4,
    fontSize: 40, color: t.title, fontFace: 'Arial', bold: true, valign: 'middle'
  });
  if (slide.subtitle) {
    s.addText(slide.subtitle, {
      x: 0.7, y: 3.0, w: 8, h: 0.8,
      fontSize: 18, color: t.text, fontFace: 'Arial'
    });
  }
  s.addShape('rect', { x: 0.7, y: 4.2, w: 2.5, h: 0.03, fill: { color: t.secondary } });
  if (slide.content && slide.content.length > 0) {
    renderContent(s, slide.content, t, { startY: 4.5, maxY: 5.3 });
  }
}

function renderEndingSlide(s, slide, t) {
  s.addShape('rect', { x: 1.5, y: 1.0, w: 7, h: 3.5, fill: { color: t.light } });
  s.addShape('rect', { x: 2.5, y: 1.3, w: 5, h: 0.04, fill: { color: t.accent } });
  s.addShape('rect', { x: 2.5, y: 4.2, w: 5, h: 0.04, fill: { color: t.accent } });
  s.addText(slide.title, {
    x: 1, y: 1.5, w: 8, h: 1.5,
    fontSize: 44, color: t.title, fontFace: 'Arial', bold: true,
    align: 'center', valign: 'middle'
  });
  if (slide.content && slide.content.length > 0) {
    var texts = [];
    for (var i = 0; i < slide.content.length; i++) {
      var ci = slide.content[i];
      if (ci.type === 'text') texts.push(ci.text);
      if (ci.type === 'list') texts = texts.concat(ci.items);
      if (ci.type === 'olist') texts = texts.concat(ci.items);
    }
    if (texts.length > 0) {
      s.addText(texts.join('\n'), {
        x: 2, y: 3.0, w: 6, h: 1.2,
        fontSize: 14, color: t.text, fontFace: 'Arial',
        align: 'center', valign: 'top'
      });
    }
  }
}

function renderContentSlide(s, pres, slide, slideIndex, totalSlides, colors, t) {
  s.addShape('rect', { x: 0, y: 0.15, w: 10, h: 1.0, fill: { color: t.light } });
  s.addText(slide.title, {
    x: 0.5, y: 0.25, w: 9, h: 0.8,
    fontSize: 26, color: t.title, fontFace: 'Arial', bold: true, valign: 'middle'
  });

  var chartData = null;
  var chartTableIdx = -1;

  for (var ci = 0; ci < slide.content.length; ci++) {
    if (slide.content[ci].type === 'table') {
      var detected = detectChart(slide.content[ci], slide, ci);
      if (detected) {
        chartData = detected;
        chartTableIdx = ci;
        break;
      }
    }
  }

  if (chartData) {
    var remaining = slide.content.filter(function(_, idx) {
      return idx !== chartTableIdx && idx !== chartData.hintIndex;
    });
    var hasExtra = remaining.length > 0;

    try {
      var isPie = chartData.type === 'pie';
      var chartW = hasExtra ? (isPie ? 5.5 : 6.0) : (isPie ? 6.5 : 9.0);

      addChartToSlide(s, pres, chartData, colors, t, {
        x: 0.5, y: 1.4, w: chartW, h: 3.8
      });

      if (hasExtra) {
        var sideX = chartW + 0.8;
        var sideW = 10 - sideX - 0.3;
        if (sideW > 1.5) {
          renderContent(s, remaining, t, { startY: 1.5, maxY: 5.0, x: sideX, w: sideW });
        }
      }
    } catch (err) {
      renderContent(s, slide.content, t);
    }
  } else {
    renderContent(s, slide.content, t);
  }

  s.addText((slideIndex + 1) + ' / ' + totalSlides, {
    x: 8.5, y: 5.3, w: 1.3, h: 0.25,
    fontSize: 9, color: t.secondary, fontFace: 'Arial', align: 'right'
  });
}

// ══════════════════════════════════════════════════════
//  9. Main Generator
// ══════════════════════════════════════════════════════

function createPPTX(markdownText, options) {
  options = options || {};
  var themeName = options.theme || 'ocean';
  var t = THEMES[themeName] || THEMES.ocean;
  var colors = (CHART_COLORS[themeName] || CHART_COLORS.ocean).slice();

  var pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9';

  var slides = parse(markdownText);

  if (slides.length === 0) {
    var emptySlide = pres.addSlide();
    emptySlide.background = { color: t.bg };
    emptySlide.addText('(empty content)', {
      x: 1, y: 2, w: 8, h: 1.5,
      fontSize: 24, color: t.text, fontFace: 'Arial', align: 'center', valign: 'middle'
    });
    return pres;
  }

  for (var si = 0; si < slides.length; si++) {
    var slide = slides[si];
    var s = pres.addSlide();
    s.background = { color: t.bg };
    addDecorations(s, t);

    if (slide.type === 'cover') {
      renderCoverSlide(s, slide, t);
    } else if (slide.type === 'ending') {
      renderEndingSlide(s, slide, t);
      s.addText((si + 1) + ' / ' + slides.length, {
        x: 8.5, y: 5.3, w: 1.3, h: 0.25,
        fontSize: 9, color: t.secondary, fontFace: 'Arial', align: 'right'
      });
    } else {
      renderContentSlide(s, pres, slide, si, slides.length, colors, t);
    }
  }

  return pres;
}

// ══════════════════════════════════════════════════════
//  10. Module Export
// ══════════════════════════════════════════════════════

module.exports = {
  createPPTX: createPPTX,
  parse: parse,
  THEMES: THEMES,
  CHART_COLORS: CHART_COLORS
};