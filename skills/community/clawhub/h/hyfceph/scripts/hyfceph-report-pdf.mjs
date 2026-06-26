#!/usr/bin/env node

import { execFile } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { promisify } from 'node:util';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';

const execFileAsync = promisify(execFile);
const PAGE_WIDTH = 1240;
const PAGE_HEIGHT = 1754;
const MARGIN_X = 72;
const MARGIN_Y = 72;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_X * 2;
const MAX_PAGE_IMAGE_WIDTH = CONTENT_WIDTH;
const SECTION_GAP = 26;
const CHROME_CANDIDATES = [
  process.env.HYFCEPH_CHROME_PATH,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta',
  '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Arc.app/Contents/MacOS/Arc',
  'google-chrome',
  'google-chrome-stable',
  'chrome',
  'chromium',
  'chromium-browser',
  'microsoft-edge',
  'brave-browser',
  'brave',
  'arc',
].filter(Boolean);

function escapeXml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

function ensureArray(value) {
  return Array.isArray(value) ? value : [];
}

function round1(value) {
  return Math.round(Number(value) * 10) / 10;
}

function toTitleCase(value) {
  return String(value || '')
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function formatDateTime(value) {
  if (!value) {
    return '-';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function formatDateOnly(value) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function formatFrameworkStatus(value) {
  if (value === 'supported') return '支持';
  if (value === 'partial') return '部分支持';
  if (value === 'unsupported') return '暂不支持';
  return String(value || '-');
}

function estimateCharUnits(char) {
  if (/[\u4e00-\u9fff]/u.test(char)) return 1;
  if (/\s/u.test(char)) return 0.35;
  if (/[A-Z0-9]/.test(char)) return 0.68;
  if (/[a-z]/.test(char)) return 0.58;
  return 0.62;
}

function wrapText(text, maxUnits) {
  const source = String(text || '').replace(/\r/g, '').split('\n');
  const lines = [];
  for (const paragraph of source) {
    const trimmed = paragraph.trim();
    if (!trimmed) {
      lines.push('');
      continue;
    }
    let current = '';
    let currentUnits = 0;
    for (const char of trimmed) {
      const units = estimateCharUnits(char);
      if (current && currentUnits + units > maxUnits) {
        lines.push(current);
        current = char;
        currentUnits = units;
      } else {
        current += char;
        currentUnits += units;
      }
    }
    if (current) {
      lines.push(current);
    }
  }
  return lines.length ? lines : [''];
}

function defaultPdfPath(inputPath) {
  const parsed = path.parse(inputPath);
  return path.join(parsed.dir, `${parsed.name}.report.pdf`);
}

function toneColor(tone) {
  if (tone === 'success') return '#13805f';
  if (tone === 'danger') return '#bd3f2f';
  if (tone === 'warn') return '#8f5c16';
  return '#5c4bc4';
}

function safeMetricValue(metric) {
  if (!metric) return '-';
  return metric.valueText || (Number.isFinite(metric.value) ? String(metric.value) : '-');
}

function normalizeFrameworkEntries(frameworkReports, preferredOrder = []) {
  const reports = frameworkReports && typeof frameworkReports === 'object' ? frameworkReports : {};
  const byCode = Object.values(reports);
  const ordered = [];
  const used = new Set();
  for (const name of preferredOrder) {
    const found = byCode.find((report) => report?.label === name || report?.code === name);
    if (found && !used.has(found.code)) {
      ordered.push(found);
      used.add(found.code);
    }
  }
  for (const report of byCode) {
    if (report?.code && !used.has(report.code)) {
      ordered.push(report);
      used.add(report.code);
    }
  }
  return ordered;
}

async function canExecute(command) {
  try {
    await execFileAsync(command, ['--version']);
    return true;
  } catch {
    return false;
  }
}

async function findChromeBinary() {
  for (const candidate of CHROME_CANDIDATES) {
    if (await canExecute(candidate)) {
      return candidate;
    }
  }
  return null;
}

function htmlText(value) {
  return escapeXml(value).replace(/\n/g, '<br />');
}

function toneLabel(tone, status) {
  if (status && status !== 'supported') return '未算出';
  if (tone === 'success') return '在范围内';
  if (tone === 'danger') return '偏离较大';
  if (tone === 'warn') return '轻度偏离';
  return '已计算';
}

function toneClass(tone, status) {
  if (status && status !== 'supported') return 'tone-muted';
  if (tone === 'success') return 'tone-success';
  if (tone === 'danger') return 'tone-danger';
  if (tone === 'warn') return 'tone-warn';
  return 'tone-default';
}

function rowToneClass(tone, status) {
  if (status && status !== 'supported') return 'row-muted';
  if (tone === 'success') return 'row-success';
  if (tone === 'danger') return 'row-danger';
  if (tone === 'warn') return 'row-warn';
  return '';
}

function parseReferenceTarget(reference) {
  const text = String(reference || '').trim();
  if (!text || /需结合|不直接|暂不|无法|未提供/.test(text)) {
    return null;
  }
  const match = text.match(/(-?\d+(?:\.\d+)?)\s*(?:°|mm|%)?\s*±\s*(-?\d+(?:\.\d+)?)/);
  if (!match) {
    return null;
  }
  let unit = 'deg';
  if (/%/.test(text)) unit = '%';
  else if (/mm/.test(text)) unit = 'mm';
  return {
    mean: Number(match[1]),
    tolerance: Math.abs(Number(match[2])),
    unit,
  };
}

function severityRank(tone, status) {
  if (status && status !== 'supported') return 99;
  if (tone === 'success') return 0;
  if (tone === 'warn') return 1;
  if (tone === 'danger') return 2;
  return 1;
}

function singleMeaningfulRowClass(item) {
  if (!item) return 'row-muted';
  if (item.status && item.status !== 'supported') return 'row-muted';

  const target = parseReferenceTarget(item.reference);
  const numeric = toNumber(item.value ?? item.valueText);
  if (target && numeric != null) {
    const distance = Math.abs(numeric - target.mean);
    if (distance <= target.tolerance) return 'row-normal';
    if (distance <= target.tolerance * 2) return 'row-caution';
    return 'row-risk';
  }

  if (/需结合|不直接/.test(String(item.reference || ''))) {
    return 'row-info';
  }
  if (item.tone === 'success') return 'row-normal';
  if (item.tone === 'warn') return 'row-caution';
  if (item.tone === 'danger') return 'row-risk';
  return 'row-info';
}

function overlapMeaningfulRowClass(baseItem, compareItem) {
  const item = compareItem || baseItem;
  if (!item) return 'row-muted';
  if (item.status && item.status !== 'supported') return 'row-muted';

  const baseValue = toNumber(baseItem?.value ?? baseItem?.valueText);
  const compareValue = toNumber(compareItem?.value ?? compareItem?.valueText);
  const target = parseReferenceTarget(compareItem?.reference || baseItem?.reference);
  if (target && baseValue != null && compareValue != null) {
    const baseDist = Math.abs(baseValue - target.mean);
    const compareDist = Math.abs(compareValue - target.mean);
    const epsilon = Math.max(0.3, target.tolerance * 0.15);
    if (compareDist < baseDist - epsilon) return 'row-improved';
    if (compareDist > baseDist + epsilon) return 'row-worse';
    if (compareDist <= target.tolerance) return 'row-normal';
    return 'row-caution';
  }

  const baseRank = severityRank(baseItem?.tone, baseItem?.status);
  const compareRank = severityRank(compareItem?.tone, compareItem?.status);
  if (compareRank < baseRank) return 'row-improved';
  if (compareRank > baseRank) return 'row-worse';
  if (compareRank === 0) return 'row-normal';
  return 'row-caution';
}

function chineseSectionNumber(index) {
  const map = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'];
  return map[index - 1] || String(index);
}

function toNumber(value) {
  const numeric = Number(value);
  if (Number.isFinite(numeric)) {
    return numeric;
  }
  const match = String(value || '').match(/-?\d+(?:\.\d+)?/);
  return match ? Number(match[0]) : null;
}

function findFrameworkItem(frameworkReports, candidates) {
  const lowerCandidates = ensureArray(candidates).map((item) => String(item).toLowerCase());
  for (const report of Object.values(frameworkReports || {})) {
    for (const item of ensureArray(report?.items)) {
      const itemCode = String(item?.code || '').toLowerCase();
      const itemLabel = String(item?.label || '').toLowerCase();
      if (lowerCandidates.includes(itemCode) || lowerCandidates.includes(itemLabel)) {
        return item;
      }
    }
  }
  return null;
}

function buildMeasurementBundle({ metrics, frameworkReports, riskLabel = '', insight = '' }) {
  const metricMap = new Map(ensureArray(metrics).map((metric) => [String(metric.code || '').toLowerCase(), metric]));
  const pick = (...codes) => {
    for (const code of codes) {
      const hit = metricMap.get(String(code).toLowerCase());
      if (hit) return hit;
    }
    return findFrameworkItem(frameworkReports, codes);
  };

  return {
    riskLabel,
    insight,
    frameworks: frameworkReports || {},
    ANB: pick('ANB'),
    Wits: pick('wits', 'AO-BO(mm)', 'AO-BO'),
    FMA: pick('FMA', 'mandibularPlaneAngle', 'mandibularPlane'),
    GoGnSN: pick('GoGn-SN', 'goGnToSN'),
    JarabakRatio: pick('posteriorAnteriorRatio', 'Posterior / Anterior Facial Height'),
    YAxis: pick('yAxis', 'Y-Axis'),
    FacialAxis: pick('facialAxis', 'Facial Axis'),
    U1SN: pick('U1-SN', 'u1ToSN'),
    IMPA: pick('IMPA', 'impa'),
    Interincisal: pick('interincisalAngle', 'Interincisal Angle'),
    ANSMe: pick('ANSMe'),
  };
}

function classifySagittal(bundle) {
  const anb = toNumber(bundle.ANB?.value ?? bundle.ANB?.valueText);
  const wits = toNumber(bundle.Wits?.value ?? bundle.Wits?.valueText);
  let label = '骨性 I 类倾向';
  const reasons = [];
  if (anb != null) {
    reasons.push(`ANB ${bundle.ANB?.valueText || anb + '°'}`);
    if (anb < 0) label = '骨性 III 类倾向';
    else if (anb > 4) label = '骨性 II 类倾向';
  }
  if (wits != null) {
    reasons.push(`Wits ${bundle.Wits?.valueText || `${wits} mm`}`);
    if (wits < -2 && label === '骨性 I 类倾向') label = '骨性 III 类倾向';
    if (wits > 2 && label === '骨性 I 类倾向') label = '骨性 II 类倾向';
  }
  let detail;
  if (label === '骨性 III 类倾向') {
    detail = '上下颌前后关系偏向 III 类，需重点关注下颌相对前突或上颌相对后缩。';
  } else if (label === '骨性 II 类倾向') {
    detail = '上下颌前后关系偏向 II 类，需关注上颌前突或下颌后缩。';
  } else {
    detail = '上下颌骨前后关系总体接近 I 类范围。';
  }
  return { label, reasons, detail };
}

function classifyVertical(bundle) {
  const fma = toNumber(bundle.FMA?.value ?? bundle.FMA?.valueText);
  const goGnSN = toNumber(bundle.GoGnSN?.value ?? bundle.GoGnSN?.valueText);
  const ratio = toNumber(bundle.JarabakRatio?.value ?? bundle.JarabakRatio?.valueText);
  let highSignals = 0;
  let lowSignals = 0;
  const reasons = [];

  if (fma != null) {
    reasons.push(`FMA ${bundle.FMA?.valueText || fma + '°'}`);
    if (fma >= 29) highSignals += 1;
    if (fma <= 21) lowSignals += 1;
  }
  if (goGnSN != null) {
    reasons.push(`GoGn-SN ${bundle.GoGnSN?.valueText || goGnSN + '°'}`);
    if (goGnSN >= 36) highSignals += 1;
    if (goGnSN <= 27) lowSignals += 1;
  }
  if (ratio != null) {
    reasons.push(`PFH/AFH ${bundle.JarabakRatio?.valueText || ratio + '%'}`);
    if (ratio <= 59) highSignals += 1;
    if (ratio >= 67) lowSignals += 1;
  }

  let label = '均衡生长型';
  let rotation = '旋转趋势不明显';
  let detail = '垂直向比例总体接近均衡，面下 1/3 没有明显过长或过短的倾向。';
  if (highSignals > lowSignals) {
    label = '垂直生长型 / 高角倾向';
    rotation = '下颌顺时针旋转倾向';
    detail = '下颌平面偏陡，提示下前面高增加及高角风险，治疗中需重点关注垂直控制。';
  } else if (lowSignals > highSignals) {
    label = '水平生长型 / 低角倾向';
    rotation = '下颌逆时针旋转倾向';
    detail = '下颌平面相对平缓，后面高支持较好，更偏向短面或低角生长表现。';
  }

  return { label, rotation, reasons, detail };
}

function describeDentalCompensation(bundle) {
  const points = [];
  const u1 = toNumber(bundle.U1SN?.value ?? bundle.U1SN?.valueText);
  const impa = toNumber(bundle.IMPA?.value ?? bundle.IMPA?.valueText);
  const interincisal = toNumber(bundle.Interincisal?.value ?? bundle.Interincisal?.valueText);

  if (u1 != null) {
    if (u1 >= 110) {
      points.push(`上前牙相对前颅底明显前倾（U1-SN ${bundle.U1SN?.valueText || `${u1}°`}），提示上切牙存在前倾代偿。`);
    } else if (u1 <= 98) {
      points.push(`上前牙相对前颅底偏舌倾（U1-SN ${bundle.U1SN?.valueText || `${u1}°`}），提示上切牙代偿不足或偏内收。`);
    }
  }
  if (impa != null) {
    if (impa >= 95) {
      points.push(`下前牙相对下颌平面偏前倾（IMPA ${bundle.IMPA?.valueText || `${impa}°`}），常见于下牙性前突或代偿。`);
    } else if (impa <= 85) {
      points.push(`下前牙相对下颌平面偏舌倾（IMPA ${bundle.IMPA?.valueText || `${impa}°`}），提示下前牙后倾代偿。`);
    }
  }
  if (interincisal != null && interincisal <= 123) {
    points.push(`上下前牙夹角偏小（${bundle.Interincisal?.valueText || `${interincisal}°`}），提示双前牙整体更前倾。`);
  }
  return points;
}

function buildSingleInterpretation(bundle) {
  const sagittal = classifySagittal(bundle);
  const vertical = classifyVertical(bundle);
  const dental = describeDentalCompensation(bundle);
  const faceHeightBody = [
    `垂直向主要参考 ${vertical.reasons.filter(Boolean).join('、')}。${vertical.detail}`,
    vertical.rotation !== '旋转趋势不明显'
      ? `结合当前结果，更符合${vertical.rotation}的表现。`
      : '当前资料未见明确的顺时针或逆时针旋转证据。',
  ].join('');
  const comprehensiveBody = [
    `${sagittal.reasons.filter(Boolean).join('、')}。${sagittal.detail}`,
    bundle.riskLabel ? `结合本轮自动结论，整体可归纳为“${bundle.riskLabel}”。` : '',
    dental.length ? dental.join('') : '牙性代偿信息以当前可计算指标看，未见特别突出的异常模式。',
    bundle.insight || '',
  ].join('');
  const growthBody = [
    `综合 FMA、GoGn-SN 与 Jarabak 比值，当前更倾向“${vertical.label}”。`,
    vertical.label.includes('高角')
      ? '这类病例治疗时通常需要把垂直控制放在前列，避免面下 1/3 继续拉长。'
      : vertical.label.includes('低角')
        ? '这类病例整体垂直向较稳定，更多体现为水平或前向生长表现。'
        : '这类病例垂直向相对均衡，治疗重点可更多放在前后向关系和牙性排布协调。',
  ].join('');
  return {
    faceHeight: faceHeightBody,
    comprehensive: comprehensiveBody,
    growthType: growthBody,
    sagittal,
    vertical,
  };
}

function describeMetricShift(name, baseItem, compareItem, target, betterText, worseHighText, worseLowText) {
  const base = toNumber(baseItem?.value ?? baseItem?.valueText);
  const compare = toNumber(compareItem?.value ?? compareItem?.valueText);
  if (base == null || compare == null) return null;
  const delta = round1(compare - base);
  if (Math.abs(delta) < 0.5) return null;
  const baseDist = Math.abs(base - target);
  const compareDist = Math.abs(compare - target);
  let trend = betterText;
  if (compareDist > baseDist + 0.2) {
    trend = compare > target ? worseHighText : worseLowText;
  }
  return `${name} 由 ${baseItem?.valueText || base} 变化到 ${compareItem?.valueText || compare}，变化 ${delta > 0 ? '+' : ''}${delta}${baseItem?.unit === 'mm' ? ' mm' : baseItem?.unit === '%' ? '%' : '°'}，${trend}。`;
}

function buildOverlapInterpretation(baseBundle, compareBundle) {
  const baseSagittal = classifySagittal(baseBundle);
  const compareSagittal = classifySagittal(compareBundle);
  const baseVertical = classifyVertical(baseBundle);
  const compareVertical = classifyVertical(compareBundle);

  const keyChanges = [
    describeMetricShift('ANB', baseBundle.ANB, compareBundle.ANB, 2, '提示上下颌骨关系向 I 类均衡方向移动', '提示上下颌关系向 II 类方向偏移', '提示上下颌关系向 III 类方向偏移'),
    describeMetricShift('Wits', baseBundle.Wits, compareBundle.Wits, 0, '提示前后向骨性关系更接近协调', '提示骨性 II 类倾向加重', '提示骨性 III 类倾向加重'),
    describeMetricShift('FMA', baseBundle.FMA, compareBundle.FMA, 25, '提示垂直向更接近常模', '提示高角或面下 1/3 增加趋势加重', '提示低角或短面趋势增强'),
    describeMetricShift('GoGn-SN', baseBundle.GoGnSN, compareBundle.GoGnSN, 32, '提示下颌平面角更接近常模', '提示下颌平面继续变陡，垂直控制压力增大', '提示下颌平面变平，垂直向更受控'),
    describeMetricShift('U1-SN', baseBundle.U1SN, compareBundle.U1SN, 102, '提示上前牙位置更接近常模', '提示上前牙前倾进一步增加', '提示上前牙较前期有所内收'),
    describeMetricShift('IMPA', baseBundle.IMPA, compareBundle.IMPA, 90, '提示下前牙位置更接近常模', '提示下前牙前倾增加', '提示下前牙较前期更后倾'),
    describeMetricShift('PFH/AFH', baseBundle.JarabakRatio, compareBundle.JarabakRatio, 62, '提示后面高/前面高比例更趋协调', '提示后面高优势增加，更偏低角', '提示后面高支持不足，面高问题更明显'),
  ].filter(Boolean);

  const overallChange = [
    `治疗前总体表现为“${baseSagittal.label}、${baseVertical.label}”；治疗后则更偏向“${compareSagittal.label}、${compareVertical.label}”。`,
    baseSagittal.label === compareSagittal.label
      ? '前后向骨性分类没有发生根本改变，但程度上已出现可量化变化。'
      : '前后向骨性分类已经出现方向性变化，提示治疗对骨性关系产生了实际影响。',
    baseBundle.riskLabel || compareBundle.riskLabel
      ? `自动综合标签由“${baseBundle.riskLabel || '未提供'}”变化为“${compareBundle.riskLabel || '未提供'}”。`
      : '',
  ].filter(Boolean).join('');

  const growthChange = [
    `治疗前生长型判断为“${baseVertical.label}”，治疗后为“${compareVertical.label}”。`,
    baseVertical.label === compareVertical.label
      ? '说明生长型主体框架基本稳定，更多体现为程度变化而非类型改变。'
      : '提示垂直向或旋转模式已有明显变化，应结合临床面型继续复核。',
    `旋转趋势方面，治疗前更符合“${baseVertical.rotation}”，治疗后更符合“${compareVertical.rotation}”。`,
  ].join('');

  const faceHeightChange = [
    `治疗前主要参考 ${baseVertical.reasons.filter(Boolean).join('、')}；治疗后主要参考 ${compareVertical.reasons.filter(Boolean).join('、')}。`,
    baseVertical.label === compareVertical.label
      ? `面部高度模式整体仍属“${compareVertical.label}”，但垂直向程度已有变化。`
      : `面部高度模式由“${baseVertical.label}”向“${compareVertical.label}”转变。`,
    compareVertical.detail,
  ].join('');

  return {
    keyChanges: keyChanges.length ? keyChanges : ['本次关键指标整体变化不大，更多体现为数值微调。'],
    overallChange,
    growthChange,
    faceHeightChange,
  };
}

function buildDerivedWitsMetric(bundle) {
  const item = bundle?.Wits;
  if (!item) return null;
  return {
    ...item,
    code: 'Wits',
    label: 'Wits 指数',
    unit: item.unit || 'mm',
    valueText: item.valueText || (Number.isFinite(item.value) ? `${item.value} mm` : '-'),
  };
}

function augmentMetricsWithDerived(metrics, bundle) {
  const list = ensureArray(metrics).map((item) => ({ ...item }));
  const hasWits = list.some((item) => String(item?.code || '').toLowerCase() === 'wits');
  const derivedWits = hasWits ? null : buildDerivedWitsMetric(bundle);
  if (!derivedWits) {
    return list;
  }
  const insertAfterAnb = list.findIndex((item) => String(item?.code || '').toUpperCase() === 'ANB');
  if (insertAfterAnb >= 0) {
    list.splice(insertAfterAnb + 1, 0, derivedWits);
  } else {
    list.push(derivedWits);
  }
  return list;
}

function buildSingleFrameworkSynthesisItems(frameworks) {
  return ensureArray(frameworks).map((framework) => `${framework.label}：${buildFrameworkComprehensiveJudgment(framework)}`);
}

function buildOverlapFrameworkSynthesisItems(baseFrameworks, compareFrameworkMap) {
  return ensureArray(baseFrameworks).map((framework) => (
    `${framework.label}：${buildOverlapFrameworkComprehensiveJudgment(framework, compareFrameworkMap.get(framework.code))}`
  ));
}

function buildSingleClinicalMeaningItems(bundle, interpretation, frameworks) {
  const items = [
    `骨性关系方面，${interpretation.sagittal.detail}`,
    `垂直向方面，${interpretation.vertical.detail}`,
    `生长型方面，当前更倾向“${interpretation.vertical.label}”，并表现为“${interpretation.vertical.rotation}”。`,
  ];
  const dental = describeDentalCompensation(bundle);
  if (dental.length) {
    items.push(`牙性代偿方面，${dental.join('')}`);
  }
  if (frameworks.length) {
    items.push(`综合 ${frameworks.length} 套分析法结果，当前结论来自多套分析法在前后向、垂直向和牙性倾斜三方面的共同支持。`);
  }
  return items;
}

function buildOverlapClinicalMeaningItems(baseBundle, compareBundle, interpretation, baseFrameworks) {
  return [
    `治疗前后整体骨性关系由“${classifySagittal(baseBundle).label}”变化为“${classifySagittal(compareBundle).label}”。${interpretation.overallChange}`,
    `垂直向与生长型由“${classifyVertical(baseBundle).label}”变化为“${classifyVertical(compareBundle).label}”。${interpretation.growthChange}`,
    `面部高度与旋转模式方面，${interpretation.faceHeightChange}`,
    `综合 ${baseFrameworks.length} 套分析法前后对比，本次变化既要看数值是否改变，也要看是否更接近稳定、可维持的骨性与牙性平衡。`,
  ];
}

function buildSingleTreatmentSuggestionItems(bundle, interpretation) {
  const sagittal = interpretation.sagittal.label;
  const vertical = interpretation.vertical.label;
  const items = [];

  if (sagittal.includes('III')) {
    items.push('前后向关系偏 III 类时，建议优先评估骨性来源与牙性代偿范围，再决定掩饰性治疗还是进一步外科评估。');
  } else if (sagittal.includes('II')) {
    items.push('前后向关系偏 II 类时，建议重点判断上颌前突、下颌后缩或两者并存，再选择相应的支抗与矫治设计。');
  } else {
    items.push('当前前后向关系总体接近 I 类，可把治疗重点更多放在牙列协调、咬合精细化与面型优化。');
  }

  if (vertical.includes('高角')) {
    items.push('高角 / 垂直生长型病例应把垂直控制放在前列，尽量避免后牙过度伸长和面下 1/3 进一步增加。');
  } else if (vertical.includes('低角')) {
    items.push('低角 / 水平生长型病例治疗时通常垂直稳定性较好，但仍需注意避免前牙过度内收或覆盖加深。');
  } else {
    items.push('均衡生长型病例整体垂直向相对稳定，可将重点放在前后向协调与牙弓形态重建。');
  }

  if (describeDentalCompensation(bundle).length) {
    items.push('当前存在一定牙性代偿，建议在前牙转矩与内收/外展设计时同时关注牙槽骨边界与软组织侧貌。');
  }

  items.push('所有方案建议仍需结合临床检查、模型或口扫、软组织目标及医生治疗策略综合确定。');
  return items;
}

function buildOverlapTreatmentSuggestionItems(baseBundle, compareBundle, interpretation) {
  const baseSagittal = classifySagittal(baseBundle).label;
  const compareSagittal = classifySagittal(compareBundle).label;
  const baseVertical = classifyVertical(baseBundle).label;
  const compareVertical = classifyVertical(compareBundle).label;
  const items = [];

  if (baseSagittal !== compareSagittal) {
    items.push(`前后向骨性分类已由“${baseSagittal}”变化为“${compareSagittal}”，后续方案应围绕新的骨性关系重新评估支抗与治疗目标。`);
  } else {
    items.push(`前后向骨性分类仍为“${compareSagittal}”，说明治疗更多改变的是程度而非类型，后续应继续围绕该类问题精细调整。`);
  }

  if (baseVertical !== compareVertical) {
    items.push(`垂直向模式由“${baseVertical}”变化为“${compareVertical}”，提示后续需要重新评估垂直控制和下颌旋转管理。`);
  } else {
    items.push(`垂直向模式仍为“${compareVertical}”，后续重点应放在保持现有垂直控制效果并降低复发风险。`);
  }

  items.push(`结合关键变化：${ensureArray(interpretation.keyChanges).slice(0, 2).join('')}`);
  items.push('若治疗后前牙代偿仍明显，应在后续阶段重点关注转矩、覆盖覆盖关系及保持期稳定性。');
  items.push('前后对比结论应与临床照片、咬合关系和治疗阶段目标联合判断，避免单凭单个指标决定最终方案。');
  return items;
}

function renderAnalysisParagraph(title, body) {
  return `
    <div class="subsection">
      <h3>${htmlText(title)}</h3>
      <div class="note-box">${htmlText(body)}</div>
    </div>
  `;
}

function renderAnalysisList(title, items) {
  return `
    <div class="subsection">
      <h3>${htmlText(title)}</h3>
      <div class="note-box">
        <ul class="analysis-list">
          ${ensureArray(items).map((item) => `<li>${htmlText(item)}</li>`).join('')}
        </ul>
      </div>
    </div>
  `;
}

function formatDeltaValue(baseItem, compareItem) {
  if (!baseItem || !compareItem || !Number.isFinite(baseItem.value) || !Number.isFinite(compareItem.value)) {
    return '-';
  }
  const delta = round1(compareItem.value - baseItem.value);
  const unit = compareItem.unit || baseItem.unit || '';
  if (unit === 'mm') return `${delta} mm`;
  if (unit === '%') return `${delta}%`;
  return `${delta}°`;
}

function buildMetricComparisonRows(baseMetrics, compareMetrics) {
  const baseMetricMap = new Map(ensureArray(baseMetrics).map((metric) => [metric.code, metric]));
  const compareMetricMap = new Map(ensureArray(compareMetrics).map((metric) => [metric.code, metric]));
  return Array.from(new Set([...baseMetricMap.keys(), ...compareMetricMap.keys()])).map((code) => ({
    code,
    base: baseMetricMap.get(code) || null,
    compare: compareMetricMap.get(code) || null,
  }));
}

function renderMetricCards(metrics) {
  return `
    <div class="metric-grid">
      ${ensureArray(metrics).map((metric) => `
        <article class="metric-card">
          <div class="metric-code">${htmlText(metric.code || '-')}</div>
          <div class="metric-value ${toneClass(metric.tone, metric.status)}">${htmlText(safeMetricValue(metric))}</div>
          <div class="metric-label">${htmlText(metric.label || metric.code || '')}</div>
          <div class="metric-reference">${htmlText(metric.reference || '')}</div>
        </article>
      `).join('')}
    </div>
  `;
}

function renderReportInfoBox({ generatedAt, patientName }) {
  return `
    <section class="info-box">
      <div class="info-grid">
        <div class="info-item"><strong>患者姓名：</strong>${htmlText(patientName || '未提供')}</div>
        <div class="info-item"><strong>检查日期：</strong>${htmlText(formatDateOnly(generatedAt))}</div>
        <div class="info-item info-item-wide"><strong>测量系统：</strong>HYFCeph 头影测量分析系统</div>
      </div>
    </section>
  `;
}

function renderLegend(items) {
  return `
    <div class="legend">
      ${ensureArray(items).map((item) => `
        <span class="legend-item">
          <span class="legend-swatch ${item.className}"></span>
          <span>${htmlText(item.label)}</span>
        </span>
      `).join('')}
    </div>
  `;
}

const CLINICAL_MEANING_MAP = {
  sna: '用于评估上颌相对前颅底的前后位置。',
  snb: '用于评估下颌相对前颅底的前后位置。',
  anb: '用于判断上下颌骨前后关系与骨性分类。',
  wits: '用于补充判断上下颌骨前后差异，减少颅底角干扰。',
  aobomm: '即 Wits 指数，用于补充判断上下颌骨前后差异，减少颅底角干扰。',
  aobo: '即 Wits 指数，用于补充判断上下颌骨前后差异，减少颅底角干扰。',
  fma: '用于判断垂直生长型与下颌平面陡峭程度。',
  'gogn-sn': '用于判断下颌平面与前颅底的垂直关系。',
  gogntosn: '用于判断下颌平面与前颅底的垂直关系。',
  'u1-sn': '用于评估上前牙唇倾或舌倾程度。',
  u1tosn: '用于评估上前牙唇倾或舌倾程度。',
  impa: '用于评估下前牙相对下颌平面的倾斜程度。',
  interincisalangle: '用于评估上下前牙整体前倾或内收程度。',
  occltosn: '用于评估咬合平面倾斜，反映垂直向与咬合重建趋势。',
  facialangle: '用于评估颏部与面部骨架的前后向表现。',
  mandibularplaneangle: '用于评估下颌平面陡峭程度与垂直向风险。',
  yaxis: '用于评估下颌生长方向，反映垂直或前向生长趋势。',
  u1toapogangle: '用于评估上前牙相对骨基底的倾斜代偿。',
  u1toapogmm: '用于评估上前牙相对骨基底的前后位置。',
  u1tonaangle: '用于评估上前牙相对上颌骨的唇倾程度。',
  u1tonamm: '用于评估上前牙相对上颌骨的前突程度。',
  l1tonbangle: '用于评估下前牙相对下颌骨的倾斜程度。',
  l1tonbmm: '用于评估下前牙相对下颌骨的前突程度。',
  facialaxis: '用于综合评估面部生长方向。',
  facialdepth: '用于评估下颌骨相对面部的前后位置。',
  mandibularplane: '用于评估垂直向与下颌平面角表现。',
  convexityata: '用于评估面部骨性凸度与前后向协调。',
  l1toapogangle: '用于评估下前牙对骨基底的倾斜代偿。',
  l1toapogmm: '用于评估下前牙对骨基底的前后位置。',
  fmia: '用于联合 FMA、IMPA 判断 Tweed 三角平衡。',
  atonperp: '用于评估上颌基骨相对 N 垂线的前后位置。',
  pogtonperp: '用于评估颏部相对 N 垂线的前后位置。',
  coa: '用于评估上颌骨有效长度，需结合年龄和性别。',
  cogn: '用于评估下颌骨有效长度，需结合年龄和性别。',
  ansme: '用于评估下前面高，反映面部高度比例。',
  u1toapogmm: '用于评估上前牙对骨基底的前突与牙性代偿。',
  saddleangle: '用于评估颅底形态，对骨性关系有间接影响。',
  articularangle: '用于评估髁突与下颌支关系，反映下颌生长方向。',
  gonialangle: '用于评估下颌角形态与垂直生长趋势。',
  sumofangles: '用于综合判断 Jarabak 角度总和与生长型。',
  posterioranteriorratio: '用于评估后面高与前面高比例，是面高分析核心指标。',
};

const SAGITTAL_CODES = new Set([
  'sna', 'snb', 'anb', 'wits', 'facialangle', 'facialdepth', 'convexityata', 'atonperp', 'pogtonperp',
]);
const VERTICAL_CODES = new Set([
  'fma', 'gognsn', 'gogntosn', 'mandibularplaneangle', 'mandibularplane', 'yaxis', 'facialaxis',
  'posterioranteriorratio', 'ansme', 'sumofangles', 'gonialangle', 'articularangle', 'saddleangle', 'occltosn',
]);
const DENTAL_CODES = new Set([
  'u1sn', 'u1tosn', 'impa', 'interincisalangle', 'u1toapogangle', 'u1toapogmm', 'u1tonaangle', 'u1tonamm',
  'l1tonbangle', 'l1tonbmm', 'l1toapogangle', 'l1toapogmm', 'fmia',
]);

function normalizeMeaningKey(item) {
  return String(item?.code || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '');
}

function clinicalMeaningBaseText(item) {
  const key = normalizeMeaningKey(item);
  return CLINICAL_MEANING_MAP[key] || `${item?.label || item?.code || '该项目'}用于补充判断当前骨性、牙性或垂直向表现。`;
}

function clinicalDirectionText(item) {
  if (!item || (item.status && item.status !== 'supported')) {
    return '当前未能完成可靠计算，需结合原图和人工复核。';
  }
  const target = parseReferenceTarget(item.reference);
  const numeric = toNumber(item.value ?? item.valueText);
  if (target && numeric != null) {
    const diff = round1(numeric - target.mean);
    const absDiff = Math.abs(diff);
    if (absDiff <= target.tolerance) {
      return '当前结果接近常模。';
    }
    if (diff > 0) {
      if (absDiff <= target.tolerance * 2) return '当前偏高，属于轻度偏离。';
      return '当前明显偏高，提示偏离常模较大。';
    }
    if (absDiff <= target.tolerance * 2) return '当前偏低，属于轻度偏离。';
    return '当前明显偏低，提示偏离常模较大。';
  }
  if (item.tone === 'success') return '当前结果基本处于可接受范围。';
  if (item.tone === 'warn') return '当前结果存在一定偏离，需结合其他指标综合判断。';
  if (item.tone === 'danger') return '当前结果偏离较明显，建议重点关注。';
  return '当前结果需结合临床背景与其他指标共同解读。';
}

function buildClinicalMeaning(item) {
  return `${clinicalMeaningBaseText(item)}${clinicalDirectionText(item)}`;
}

function buildOverlapClinicalMeaning(baseItem, compareItem) {
  const primary = compareItem || baseItem;
  const base = clinicalMeaningBaseText(primary);
  if (!primary) {
    return '该项目本次未能形成可读对比，建议结合其他指标判断。';
  }
  const rowClass = overlapMeaningfulRowClass(baseItem, compareItem);
  if (rowClass === 'row-improved') {
    return `${base} 与治疗前相比，本项更接近常模，提示变化方向较理想。`;
  }
  if (rowClass === 'row-worse') {
    return `${base} 与治疗前相比，本项偏离常模增加，提示变化方向欠理想。`;
  }
  if (rowClass === 'row-normal') {
    return `${base} 本项前后差异不大，且整体处于相对可接受范围。`;
  }
  if (rowClass === 'row-caution') {
    return `${base} 本项前后有变化，但仍需结合临床与其他指标综合判断。`;
  }
  return `${base} 该项目当前未形成稳定可比结果，建议结合原始测量复核。`;
}

function classifyFrameworkDomain(item) {
  const key = normalizeMeaningKey(item);
  if (SAGITTAL_CODES.has(key)) return 'sagittal';
  if (VERTICAL_CODES.has(key)) return 'vertical';
  if (DENTAL_CODES.has(key)) return 'dental';
  return 'other';
}

function frameworkItemsSorted(framework) {
  return ensureArray(framework?.items)
    .filter((item) => item)
    .slice()
    .sort((a, b) => {
      const aRank = severityRank(a.tone, a.status);
      const bRank = severityRank(b.tone, b.status);
      if (aRank !== bRank) return bRank - aRank;
      return String(a.label || a.code || '').localeCompare(String(b.label || b.code || ''), 'zh-CN');
    });
}

function buildFrameworkMeasurementInterpretation(framework) {
  const sorted = frameworkItemsSorted(framework);
  const chosen = sorted.filter((item) => item.status === 'supported').slice(0, 4);
  if (!chosen.length) {
    return '当前分析法暂未输出足够的可解释项目，建议以基础测量指标和原始点位复核为主。';
  }
  return chosen.map((item) => {
    const base = `${item.label || item.code} 为 ${item.valueText || item.value || '-'}`;
    const direction = clinicalDirectionText(item);
    return `${base}，${direction}`;
  }).join('');
}

function buildFrameworkComprehensiveJudgment(framework) {
  const items = ensureArray(framework?.items).filter((item) => item.status === 'supported');
  const counts = { sagittal: 0, vertical: 0, dental: 0, other: 0 };
  const severities = { sagittal: 0, vertical: 0, dental: 0, other: 0 };
  for (const item of items) {
    const domain = classifyFrameworkDomain(item);
    counts[domain] += 1;
    severities[domain] += severityRank(item.tone, item.status);
  }
  const ranked = Object.entries(severities).sort((a, b) => b[1] - a[1]);
  const dominant = ranked[0]?.[0] || 'other';
  const riskCount = items.filter((item) => severityRank(item.tone, item.status) >= 2).length;
  const warnCount = items.filter((item) => severityRank(item.tone, item.status) === 1).length;

  const domainText = dominant === 'sagittal'
    ? '这一分析法下更突出的信息集中在前后向骨性关系'
    : dominant === 'vertical'
      ? '这一分析法下更突出的信息集中在垂直向和面高模式'
      : dominant === 'dental'
        ? '这一分析法下更突出的信息集中在前牙代偿与牙性倾斜'
        : '这一分析法下各维度信息相对分散，需要综合解读';

  const severityText = riskCount > 0
    ? `其中 ${riskCount} 项偏离较明显，${warnCount} 项存在轻度偏离。`
    : warnCount > 0
      ? `主要表现为 ${warnCount} 项轻度偏离，尚未见特别突出的重度偏离。`
      : '多数项目接近参考范围，整体表现较稳定。';

  return `${domainText}。${severityText} 综合来看，${framework?.label || '该分析法'}更适合作为当前病例该维度诊断的补充证据，而不是孤立单项判断。`;
}

function buildOverlapFrameworkMeasurementInterpretation(baseFramework, compareFramework) {
  const rows = buildOverlapComparisonRows(baseFramework, compareFramework)
    .map((row) => ({
      ...row,
      state: overlapMeaningfulRowClass(row.base, row.compare),
    }))
    .filter((row) => row.base || row.compare);

  const ranked = rows.slice().sort((a, b) => {
    const score = (state) => state === 'row-worse' ? 4 : state === 'row-improved' ? 3 : state === 'row-caution' ? 2 : state === 'row-normal' ? 1 : 0;
    return score(b.state) - score(a.state);
  }).slice(0, 4);

  if (!ranked.length) {
    return '该分析法在治疗前后未形成可读的对比项目，建议结合基础重叠指标判断。';
  }

  return ranked.map((row) => {
    const label = row.base?.label || row.compare?.label || row.code || '该项目';
    const beforeText = row.base?.valueText || '未算出';
    const afterText = row.compare?.valueText || '未算出';
    const direction = row.state === 'row-improved'
      ? '较前改善'
      : row.state === 'row-worse'
        ? '较前变差'
        : row.state === 'row-normal'
          ? '较前基本稳定'
          : '前后存在变化';
    return `${label} 由 ${beforeText} 变为 ${afterText}，${direction}。`;
  }).join('');
}

function buildOverlapFrameworkComprehensiveJudgment(baseFramework, compareFramework) {
  const rows = buildOverlapComparisonRows(baseFramework, compareFramework);
  let improved = 0;
  let worse = 0;
  let stable = 0;
  let caution = 0;
  for (const row of rows) {
    const state = overlapMeaningfulRowClass(row.base, row.compare);
    if (state === 'row-improved') improved += 1;
    else if (state === 'row-worse') worse += 1;
    else if (state === 'row-normal') stable += 1;
    else if (state === 'row-caution') caution += 1;
  }

  let summary;
  if (improved > worse) {
    summary = `该分析法下改善项目 (${improved} 项) 多于变差项目 (${worse} 项)，整体趋势偏向改善。`;
  } else if (worse > improved) {
    summary = `该分析法下变差项目 (${worse} 项) 多于改善项目 (${improved} 项)，整体趋势需谨慎评估。`;
  } else {
    summary = `该分析法下改善与变差项目数量接近，整体变化偏中性或混合。`;
  }
  const stability = stable > 0 ? `另有 ${stable} 项基本稳定。` : '';
  const cautionText = caution > 0 ? `其中 ${caution} 项虽有变化，但仍需结合临床进一步解释。` : '';
  return `${summary}${stability}${cautionText} 综合来看，${baseFramework?.label || compareFramework?.label || '该分析法'}可用于观察治疗前后趋势，但仍应与基础重叠指标联合判断。`;
}

function renderSingleMetricsTable(metrics) {
  return `
    <table class="framework-table metrics-table">
      <thead>
        <tr>
          <th>指标</th>
          <th>测量值</th>
          <th>参考值</th>
          <th>临床意义</th>
        </tr>
      </thead>
      <tbody>
        ${ensureArray(metrics).map((metric) => `
          <tr class="${singleMeaningfulRowClass(metric)}">
            <td><span class="mono">${htmlText(metric.code || '-')}</span></td>
            <td class="${toneClass(metric.tone, metric.status)}">${htmlText(safeMetricValue(metric))}</td>
            <td>${htmlText(metric.reference || '-')}</td>
            <td class="clinical-cell">${htmlText(buildClinicalMeaning(metric))}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function renderOverlapMetricsTable(rows) {
  return `
    <table class="framework-table metrics-table">
      <thead>
        <tr>
          <th>指标</th>
          <th>治疗前</th>
          <th>治疗后</th>
          <th>变化</th>
          <th>参考值</th>
          <th>临床意义</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((row) => `
          <tr class="${overlapMeaningfulRowClass(row.base, row.compare)}">
            <td><span class="mono">${htmlText(row.code || '-')}</span></td>
            <td class="${toneClass(row.base?.tone, row.base?.status)}">${htmlText(safeMetricValue(row.base))}</td>
            <td class="${toneClass(row.compare?.tone, row.compare?.status)}">${htmlText(safeMetricValue(row.compare))}</td>
            <td>${htmlText(formatDeltaValue(row.base, row.compare))}</td>
            <td>${htmlText(row.compare?.reference || row.base?.reference || '-')}</td>
            <td class="clinical-cell">${htmlText(buildOverlapClinicalMeaning(row.base, row.compare))}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function renderKeyMetricComparisonTable(rows) {
  return `
    <table class="framework-table">
      <thead>
        <tr>
          <th>指标</th>
          <th>治疗前</th>
          <th>治疗后</th>
          <th>变化</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((row) => `
          <tr>
            <td><span class="mono">${htmlText(row.code || '-')}</span></td>
            <td class="${toneClass(row.base?.tone, row.base?.status)}">${htmlText(safeMetricValue(row.base))}</td>
            <td class="${toneClass(row.compare?.tone, row.compare?.status)}">${htmlText(safeMetricValue(row.compare))}</td>
            <td>${htmlText(formatDeltaValue(row.base, row.compare))}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function renderSingleFrameworkTable(framework) {
  return `
    <table class="framework-table">
      <thead>
        <tr>
          <th>项目</th>
          <th>数值</th>
          <th>参考</th>
          <th>状态</th>
          <th>临床意义</th>
        </tr>
      </thead>
      <tbody>
        ${ensureArray(framework.items).map((item) => {
          const valueText = item.status === 'supported'
            ? (item.valueText || (Number.isFinite(item.value) ? String(item.value) : '-'))
            : `暂不支持：${item.reason || '-'}`;
          return `
            <tr class="${singleMeaningfulRowClass(item)}">
              <td>${htmlText(item.label || item.code || '-')}</td>
              <td class="${toneClass(item.tone, item.status)}">${htmlText(valueText)}</td>
              <td>${htmlText(item.reference || '-')}</td>
              <td>${htmlText(toneLabel(item.tone, item.status))}</td>
              <td class="clinical-cell">${htmlText(buildClinicalMeaning(item))}</td>
            </tr>
          `;
        }).join('')}
      </tbody>
    </table>
  `;
}

function renderOverlapFrameworkTable(label, baseFramework, compareFramework) {
  const rows = buildOverlapComparisonRows(baseFramework, compareFramework);
  return `
    <table class="framework-table">
      <thead>
        <tr>
          <th>项目</th>
          <th>治疗前</th>
          <th>治疗后</th>
          <th>参考</th>
          <th>差值</th>
          <th>临床意义</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((row) => `
          <tr class="${overlapMeaningfulRowClass(row.base, row.compare)}">
            <td>${htmlText(row.base?.label || row.compare?.label || row.code || '-')}</td>
            <td class="${toneClass(row.base?.tone, row.base?.status)}">${htmlText(row.base?.status === 'supported' ? (row.base?.valueText || '-') : '未算出')}</td>
            <td class="${toneClass(row.compare?.tone, row.compare?.status)}">${htmlText(row.compare?.status === 'supported' ? (row.compare?.valueText || '-') : '未算出')}</td>
            <td>${htmlText(row.base?.reference || row.compare?.reference || '-')}</td>
            <td>${htmlText(formatDeltaValue(row.base, row.compare))}</td>
            <td class="clinical-cell">${htmlText(buildOverlapClinicalMeaning(row.base, row.compare))}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function renderFrameworkNarrative(sectionIndex, framework, mode, compareFramework) {
  const sectionNo = chineseSectionNumber(sectionIndex);
  const intro = framework?.note
    || (mode === 'overlap'
      ? `本页展示 ${framework?.label || compareFramework?.label || '该分析法'} 在治疗前后两次测量中的原始项目对比。`
      : `本页展示 ${framework?.label || '该分析法'} 的完整原始项目与参考范围。`);

  const diagnosis = mode === 'overlap'
    ? `治疗前：${baseFrameworkSummary(framework)}；治疗后：${baseFrameworkSummary(compareFramework)}。`
    : `当前状态：${formatFrameworkStatus(framework?.status)}；已输出 ${ensureArray(framework?.items).length} 个项目。`;
  const measurementInterpretation = mode === 'overlap'
    ? buildOverlapFrameworkMeasurementInterpretation(framework, compareFramework)
    : buildFrameworkMeasurementInterpretation(framework);
  const comprehensiveJudgment = mode === 'overlap'
    ? buildOverlapFrameworkComprehensiveJudgment(framework, compareFramework)
    : buildFrameworkComprehensiveJudgment(framework);

  return `
    <div class="section-heading"><span class="bar"></span><h2>${sectionNo}、${htmlText((framework?.label || compareFramework?.label || '分析法') + (mode === 'overlap' ? '对比' : ''))}</h2></div>
    <div class="subsection">
      <h3>${sectionIndex}.1 分析说明</h3>
      <div class="note-box">${htmlText(intro)}</div>
    </div>
    <div class="subsection">
      <h3>${sectionIndex}.2 结果摘要</h3>
      <p class="body-copy">${htmlText(diagnosis)}</p>
    </div>
    <div class="subsection">
      <h3>${sectionIndex}.3 测量值分析解读</h3>
      <div class="note-box">${htmlText(measurementInterpretation)}</div>
    </div>
    <div class="subsection">
      <h3>${sectionIndex}.4 综合判断</h3>
      <div class="note-box">${htmlText(comprehensiveJudgment)}</div>
    </div>
    <div class="subsection">
      <h3>${sectionIndex}.5 原始数据明细</h3>
    </div>
  `;
}

function baseFrameworkSummary(framework) {
  if (!framework) return '未提供';
  return `${formatFrameworkStatus(framework.status)}，共 ${ensureArray(framework.items).length} 项`;
}

function renderImageAppendixPage(title, imageDataUri, caption) {
  if (!imageDataUri) return '';
  return `
    <section class="page appendix-page">
      <div class="main-title">${htmlText(title)}</div>
      <div class="main-divider"></div>
      <figure class="image-frame large-frame">
        <img src="${imageDataUri}" alt="${htmlText(caption)}" />
        <figcaption>${htmlText(caption)}</figcaption>
      </figure>
    </section>
  `;
}

async function buildHtmlReport(payload) {
  const mode = String(payload.mode || payload.analysis?.type || 'image').trim();
  const reportTitle = mode === 'overlap' ? 'HYFCeph 重叠对比报告' : 'HYFCeph 侧位片测量报告';
  const generatedAt = formatDateTime(new Date().toISOString());
  const imageDataUri = await imageToDataUri(payload.annotatedPngPath || payload.annotatedSvgPath);
  const frameworkChoices = payload.frameworkChoices || payload.analysis?.frameworkChoices || payload.summary?.frameworkChoices || [];
  const patientName = String(payload.patientName || '').trim();

  let bodySections = '';

  if (mode === 'overlap') {
    const baseBundle = buildMeasurementBundle({
      metrics: payload.analysis?.base?.metrics,
      frameworkReports: payload.analysis?.base?.frameworkReports,
      riskLabel: payload.analysis?.base?.riskLabel,
      insight: payload.analysis?.base?.insight,
    });
    const compareBundle = buildMeasurementBundle({
      metrics: payload.analysis?.compare?.metrics,
      frameworkReports: payload.analysis?.compare?.frameworkReports,
      riskLabel: payload.analysis?.compare?.riskLabel,
      insight: payload.analysis?.compare?.insight,
    });
    const baseMetrics = augmentMetricsWithDerived(payload.analysis?.base?.metrics, baseBundle);
    const compareMetrics = augmentMetricsWithDerived(payload.analysis?.compare?.metrics, compareBundle);
    const metricRows = buildMetricComparisonRows(baseMetrics, compareMetrics);
    const overlapInterpretation = buildOverlapInterpretation(baseBundle, compareBundle);
    const baseFrameworks = normalizeFrameworkEntries(payload.analysis?.base?.frameworkReports, frameworkChoices);
    const compareFrameworkMap = new Map(
      normalizeFrameworkEntries(payload.analysis?.compare?.frameworkReports, frameworkChoices).map((item) => [item.code, item]),
    );

    bodySections += `
      <section class="page report-page">
        <div class="main-title">${htmlText(reportTitle)}</div>
        ${patientName ? `<div class="main-subtitle">患者：${htmlText(patientName)}</div>` : ''}
        <div class="main-divider"></div>
        ${renderReportInfoBox({ generatedAt, patientName })}
        <div class="section-heading"><span class="bar"></span><h2>一、基础测量数据对比</h2></div>
        ${renderLegend([
          { className: 'row-improved', label: '较前改善' },
          { className: 'row-worse', label: '较前变差' },
          { className: 'row-normal', label: '基本稳定 / 接近常模' },
          { className: 'row-caution', label: '变化存在，需结合临床' },
        ])}
        ${renderOverlapMetricsTable(metricRows)}
        ${renderAnalysisList('2.1 关键变化解读', overlapInterpretation.keyChanges)}
        ${renderAnalysisParagraph('2.2 整体诊断变化', overlapInterpretation.overallChange)}
        ${renderAnalysisParagraph('2.3 生长型判断', overlapInterpretation.growthChange)}
        ${renderAnalysisParagraph('2.4 面部高度分析', overlapInterpretation.faceHeightChange)}
        ${renderAnalysisParagraph('2.5 对齐方式', `本次重叠图采用 ${payload.alignMode || payload.summary?.alignLabel || '-'} 对齐，用于比较治疗前后轮廓与关键指标变化。`)}
      </section>
    `;

    baseFrameworks.forEach((framework, index) => {
      const sectionIndex = index + 2;
      bodySections += `
        <section class="page report-page">
          ${renderFrameworkNarrative(sectionIndex, framework, 'overlap', compareFrameworkMap.get(framework.code))}
          ${renderOverlapFrameworkTable(framework.label, framework, compareFrameworkMap.get(framework.code))}
        </section>
      `;
    });

    bodySections += `
      <section class="page report-page">
        <div class="section-heading"><span class="bar"></span><h2>${chineseSectionNumber(baseFrameworks.length + 2)}、全部分析法综合结论</h2></div>
        ${renderAnalysisList('末页.1 所有分析法综合分析', buildOverlapFrameworkSynthesisItems(baseFrameworks, compareFrameworkMap))}
        ${renderAnalysisList('末页.2 临床意义', buildOverlapClinicalMeaningItems(baseBundle, compareBundle, overlapInterpretation, baseFrameworks))}
        ${renderAnalysisList('末页.3 方案建议', buildOverlapTreatmentSuggestionItems(baseBundle, compareBundle, overlapInterpretation))}
      </section>
    `;

    bodySections += renderImageAppendixPage('治疗前后重叠图', imageDataUri, '治疗前后重叠图');
  } else {
    const singleBundle = buildMeasurementBundle({
      metrics: payload.metrics || payload.analysis?.metrics || [],
      frameworkReports: payload.analysis?.frameworkReports,
      riskLabel: payload.analysis?.riskLabel,
      insight: payload.analysis?.insight,
    });
    const singleMetrics = augmentMetricsWithDerived(payload.metrics || payload.analysis?.metrics || [], singleBundle);
    const singleInterpretation = buildSingleInterpretation(singleBundle);
    const frameworks = normalizeFrameworkEntries(payload.analysis?.frameworkReports, frameworkChoices);

    bodySections += `
      <section class="page report-page">
        <div class="main-title">${htmlText(reportTitle)}</div>
        ${patientName ? `<div class="main-subtitle">患者：${htmlText(patientName)}</div>` : ''}
        <div class="main-divider"></div>
        ${renderReportInfoBox({ generatedAt, patientName })}
        <div class="section-heading"><span class="bar"></span><h2>一、基础测量数据总览</h2></div>
        ${renderLegend([
          { className: 'row-normal', label: '接近常模' },
          { className: 'row-caution', label: '轻度偏离' },
          { className: 'row-risk', label: '偏离较大' },
          { className: 'row-info', label: '需结合临床' },
        ])}
        ${renderSingleMetricsTable(singleMetrics)}
        ${renderAnalysisParagraph('2.1 面部高度分析', singleInterpretation.faceHeight)}
        ${renderAnalysisParagraph('2.2 综合判断', singleInterpretation.comprehensive)}
        ${renderAnalysisParagraph('2.3 生长型判断', singleInterpretation.growthType)}
      </section>
    `;

    frameworks.forEach((framework, index) => {
      const sectionIndex = index + 2;
      bodySections += `
        <section class="page report-page">
          ${renderFrameworkNarrative(sectionIndex, framework, 'single')}
          ${renderSingleFrameworkTable(framework)}
        </section>
      `;
    });

    bodySections += `
      <section class="page report-page">
        <div class="section-heading"><span class="bar"></span><h2>${chineseSectionNumber(frameworks.length + 2)}、全部分析法综合结论</h2></div>
        ${renderAnalysisList('末页.1 所有分析法综合分析', buildSingleFrameworkSynthesisItems(frameworks))}
        ${renderAnalysisList('末页.2 临床意义', buildSingleClinicalMeaningItems(singleBundle, singleInterpretation, frameworks))}
        ${renderAnalysisList('末页.3 方案建议', buildSingleTreatmentSuggestionItems(singleBundle, singleInterpretation))}
      </section>
    `;

    bodySections += renderImageAppendixPage('标注图附页', imageDataUri, '自动定点标注图');
  }

  return `<!doctype html>
  <html lang="zh-CN">
    <head>
      <meta charset="utf-8" />
      <title>${htmlText(reportTitle)}</title>
      <style>
        @page {
          size: A4;
          margin: 14mm;
        }
        * {
          box-sizing: border-box;
          -webkit-print-color-adjust: exact;
          print-color-adjust: exact;
        }
        html, body {
          margin: 0;
          padding: 0;
          font-family: "PingFang SC","Noto Sans SC","Helvetica Neue",Arial,sans-serif;
          color: #2c2c2c;
          background: #ffffff;
        }
        body {
          font-size: 12px;
          line-height: 1.6;
        }
        .page {
          break-after: page;
          min-height: 268mm;
        }
        .page:last-child {
          break-after: auto;
        }
        .report-page,
        .appendix-page {
          padding: 4mm 2mm 2mm;
        }
        .main-title {
          text-align: center;
          font-size: 24px;
          font-weight: 700;
          color: #333;
          margin: 12px 0 10px;
        }
        .main-subtitle {
          text-align: center;
          font-size: 13px;
          color: #5a6470;
          margin: -2px 0 10px;
        }
        .main-divider {
          height: 1.5px;
          background: #444;
          margin: 0 0 16px;
        }
        .info-box {
          border: 1px solid #d9e1eb;
          background: #fbfdff;
          border-radius: 4px;
          padding: 14px 18px;
          margin-bottom: 18px;
        }
        .info-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 8px 18px;
        }
        .info-item {
          color: #3e4957;
        }
        .info-item strong {
          color: #333;
          font-weight: 700;
        }
        .info-item-wide {
          grid-column: 1 / -1;
        }
        .section-heading {
          display: flex;
          align-items: center;
          gap: 10px;
          margin: 18px 0 12px;
        }
        .section-heading .bar {
          width: 4px;
          height: 24px;
          border-radius: 2px;
          background: #3a9df5;
        }
        .section-heading h2 {
          margin: 0;
          font-size: 16px;
          color: #314559;
          font-weight: 800;
        }
        .subsection {
          margin-top: 14px;
        }
        .subsection h3 {
          margin: 0 0 8px;
          font-size: 13px;
          color: #41566d;
          font-weight: 700;
        }
        .body-copy {
          margin: 0;
          color: #4b5867;
        }
        .note-box {
          border: 1px solid #dce6ef;
          background: #f9fbfd;
          border-radius: 4px;
          padding: 12px 14px;
          color: #465668;
        }
        .framework-table {
          width: 100%;
          border-collapse: collapse;
          border-spacing: 0;
          margin-top: 10px;
          border: 1px solid #dfe5eb;
        }
        .framework-table thead {
          display: table-header-group;
        }
        .framework-table tr {
          page-break-inside: avoid;
        }
        .framework-table th {
          background: #f7f7f7;
          color: #4c5b6d;
          font-size: 11px;
          font-weight: 700;
          text-align: center;
          padding: 8px 10px;
          border: 1px solid #dfe5eb;
        }
        .framework-table td {
          padding: 8px 10px;
          border: 1px solid #e3e8ee;
          vertical-align: top;
          color: #2f3c4b;
        }
        .metrics-table td,
        .metrics-table th {
          text-align: center;
        }
        .metrics-table td:last-child,
        .metrics-table th:last-child {
          text-align: left;
        }
        .clinical-cell {
          text-align: left;
          min-width: 180px;
          color: #4c5b6d;
          line-height: 1.55;
        }
        .mono {
          font-family: Menlo, Consolas, monospace;
          font-weight: 700;
        }
        .row-success {
          background: #f3fbf6;
        }
        .row-danger {
          background: #fff7f2;
        }
        .row-warn {
          background: #fff8dc;
        }
        .row-muted {
          background: #faf8fb;
        }
        .row-normal {
          background: #eef9f0;
        }
        .row-caution {
          background: #fff4e8;
        }
        .row-risk {
          background: #fdeff3;
        }
        .row-info {
          background: #eef5ff;
        }
        .row-improved {
          background: #eef5ff;
        }
        .row-worse {
          background: #fdeff3;
        }
        .tone-success { color: #1f9d55; font-weight: 700; }
        .tone-danger { color: #e67e22; font-weight: 700; }
        .tone-warn { color: #2ecc71; font-weight: 700; }
        .tone-default { color: #5c4bc4; font-weight: 700; }
        .tone-muted { color: #8b6380; }
        .legend {
          display: flex;
          flex-wrap: wrap;
          gap: 8px 14px;
          margin: 8px 0 12px;
          font-size: 11px;
          color: #566577;
        }
        .legend-item {
          display: inline-flex;
          align-items: center;
          gap: 6px;
        }
        .legend-swatch {
          width: 14px;
          height: 14px;
          border-radius: 3px;
          border: 1px solid #d9e1eb;
          display: inline-block;
        }
        .image-frame {
          margin: 18px 0 0;
          text-align: center;
        }
        .large-frame img {
          display: block;
          max-width: 100%;
          max-height: 225mm;
          object-fit: contain;
          margin: 0 auto;
        }
        .large-frame figcaption {
          margin-top: 10px;
          font-size: 11px;
          color: #687789;
        }
      </style>
    </head>
    <body>
      ${bodySections}
    </body>
  </html>`;
}

async function renderHtmlToPdfWithChrome(html, outputPath) {
  const chromeBinary = await findChromeBinary();
  if (!chromeBinary) {
    throw new Error('Chrome not found');
  }

  const tempDir = await fs.mkdtemp(path.join(process.cwd(), 'hyfceph-html-pdf-'));
  const htmlPath = path.join(tempDir, 'report.html');
  await fs.writeFile(htmlPath, html, 'utf8');

  const args = [
    '--headless=new',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--no-pdf-header-footer',
    '--print-to-pdf-no-header',
    `--print-to-pdf=${outputPath}`,
    `file://${htmlPath}`,
  ];

  try {
    await execFileAsync(chromeBinary, args);
  } catch {
    const fallbackArgs = [
      '--headless',
      '--disable-gpu',
      '--allow-file-access-from-files',
      '--no-pdf-header-footer',
      '--print-to-pdf-no-header',
      `--print-to-pdf=${outputPath}`,
      `file://${htmlPath}`,
    ];
    await execFileAsync(chromeBinary, fallbackArgs);
  }

  return path.resolve(outputPath);
}

function buildJpegPdf(pages) {
  const objects = [];
  const addObject = (value) => {
    objects.push(value);
    return objects.length;
  };

  const imageObjectIds = [];
  const contentObjectIds = [];
  const pageObjectIds = [];

  for (const page of pages) {
    const imageId = addObject(
      `<< /Type /XObject /Subtype /Image /Width ${page.imageWidth} /Height ${page.imageHeight} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${page.jpegBuffer.length} >>\nstream\n${page.jpegBuffer.toString('binary')}\nendstream`,
    );
    imageObjectIds.push(imageId);

    const content = `q\n595 0 0 842 0 0 cm\n/Im0 Do\nQ`;
    const contentId = addObject(`<< /Length ${Buffer.byteLength(content, 'utf8')} >>\nstream\n${content}\nendstream`);
    contentObjectIds.push(contentId);
  }

  const pagesId = addObject('');
  const catalogId = addObject(`<< /Type /Catalog /Pages ${pagesId} 0 R >>`);

  for (let index = 0; index < pages.length; index += 1) {
    const pageId = addObject(
      `<< /Type /Page /Parent ${pagesId} 0 R /MediaBox [0 0 595 842] /Resources << /XObject << /Im0 ${imageObjectIds[index]} 0 R >> >> /Contents ${contentObjectIds[index]} 0 R >>`,
    );
    pageObjectIds.push(pageId);
  }

  objects[pagesId - 1] = `<< /Type /Pages /Count ${pageObjectIds.length} /Kids [${pageObjectIds.map((id) => `${id} 0 R`).join(' ')}] >>`;

  let pdf = '%PDF-1.4\n';
  const offsets = [0];
  for (let index = 0; index < objects.length; index += 1) {
    offsets.push(Buffer.byteLength(pdf, 'binary'));
    pdf += `${index + 1} 0 obj\n${objects[index]}\nendobj\n`;
  }
  const xrefOffset = Buffer.byteLength(pdf, 'binary');
  pdf += `xref\n0 ${objects.length + 1}\n`;
  pdf += '0000000000 65535 f \n';
  for (let index = 1; index < offsets.length; index += 1) {
    pdf += `${String(offsets[index]).padStart(10, '0')} 00000 n \n`;
  }
  pdf += `trailer\n<< /Size ${objects.length + 1} /Root ${catalogId} 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`;
  return Buffer.from(pdf, 'binary');
}

async function imageToDataUri(filePath) {
  if (!filePath) return null;
  const buffer = await fs.readFile(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const mime = ext === '.svg'
    ? 'image/svg+xml'
    : ext === '.jpg' || ext === '.jpeg'
      ? 'image/jpeg'
      : 'image/png';
  return `data:${mime};base64,${buffer.toString('base64')}`;
}

async function getImageSize(filePath) {
  const buffer = await fs.readFile(filePath);
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.png') {
    return {
      width: buffer.readUInt32BE(16),
      height: buffer.readUInt32BE(20),
    };
  }
  if (ext === '.jpg' || ext === '.jpeg') {
    let offset = 2;
    while (offset < buffer.length) {
      if (buffer[offset] !== 0xff) {
        offset += 1;
        continue;
      }
      const marker = buffer[offset + 1];
      const length = buffer.readUInt16BE(offset + 2);
      if (marker >= 0xc0 && marker <= 0xc3) {
        return {
          height: buffer.readUInt16BE(offset + 5),
          width: buffer.readUInt16BE(offset + 7),
        };
      }
      offset += 2 + length;
    }
  }
  return { width: 1200, height: 1200 };
}

async function convertSvgToJpeg(svgPath, jpgPath) {
  const attempts = [
    ['/usr/bin/sips', ['-s', 'format', 'jpeg', svgPath, '--out', jpgPath]],
    ['sips', ['-s', 'format', 'jpeg', svgPath, '--out', jpgPath]],
    ['/opt/homebrew/bin/magick', [svgPath, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', jpgPath]],
    ['/usr/local/bin/magick', [svgPath, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', jpgPath]],
    ['magick', [svgPath, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', jpgPath]],
    ['/opt/homebrew/bin/convert', [svgPath, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', jpgPath]],
    ['/usr/local/bin/convert', [svgPath, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', jpgPath]],
    ['convert', [svgPath, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', jpgPath]],
  ];
  const failures = [];
  for (const [command, args] of attempts) {
    try {
      await execFileAsync(command, args);
      return path.resolve(jpgPath);
    } catch (error) {
      failures.push(`${command}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  throw new Error(`无法把 SVG 转成 JPEG 页面：${failures.join(' | ')}`);
}

function createPage(pages) {
  const page = {
    fragments: [],
    cursorY: MARGIN_Y,
    index: pages.length + 1,
  };

  page.fragments.push(
    `<rect width="${PAGE_WIDTH}" height="${PAGE_HEIGHT}" fill="#ffffff" />`,
    `<rect x="${MARGIN_X}" y="38" width="${CONTENT_WIDTH}" height="2" fill="#ebe8ff" />`,
    `<text x="${MARGIN_X}" y="54" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="14" font-weight="700" fill="#6a6398">HYFCeph Report</text>`,
    `<text x="${PAGE_WIDTH - MARGIN_X}" y="54" text-anchor="end" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="12" fill="#8a86ab">第 ${pages.length + 1} 页</text>`,
  );

  pages.push(page);
  return page;
}

function ensurePage(pages, minHeight = 120) {
  const page = pages[pages.length - 1] || createPage(pages);
  if (page.cursorY + minHeight <= PAGE_HEIGHT - MARGIN_Y) {
    return page;
  }
  return createPage(pages);
}

function addSectionTitle(page, title, subtitle = '') {
  page.fragments.push(
    `<text x="${MARGIN_X}" y="${page.cursorY}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="26" font-weight="800" fill="#1b1847">${escapeXml(title)}</text>`,
  );
  page.cursorY += 18;
  if (subtitle) {
    const lines = wrapText(subtitle, 78);
    for (const line of lines) {
      page.cursorY += 24;
      page.fragments.push(
        `<text x="${MARGIN_X}" y="${page.cursorY}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="14" fill="#67648f">${escapeXml(line)}</text>`,
      );
    }
  }
  page.cursorY += 20;
}

function addParagraph(page, text, maxUnits = 82, fontSize = 15, lineHeight = 24, color = '#4f4a7e') {
  const lines = wrapText(text, maxUnits);
  for (const line of lines) {
    page.fragments.push(
      `<text x="${MARGIN_X}" y="${page.cursorY}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="${fontSize}" fill="${color}">${escapeXml(line)}</text>`,
    );
    page.cursorY += lineHeight;
  }
  page.cursorY += 8;
}

function addSummaryChips(page, items) {
  let x = MARGIN_X;
  let y = page.cursorY;
  const chipHeight = 82;
  const gap = 14;
  const chipWidth = (CONTENT_WIDTH - gap * 2) / 3;
  items.forEach((item, index) => {
    const col = index % 3;
    const row = Math.floor(index / 3);
    x = MARGIN_X + col * (chipWidth + gap);
    y = page.cursorY + row * (chipHeight + gap);
    page.fragments.push(
      `<rect x="${x}" y="${y}" width="${chipWidth}" height="${chipHeight}" rx="18" fill="#f7f5ff" stroke="#e4defa" stroke-width="1" />`,
      `<text x="${x + 18}" y="${y + 28}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="12" font-weight="700" fill="#726aa6">${escapeXml(item.label)}</text>`,
      `<text x="${x + 18}" y="${y + 58}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="24" font-weight="800" fill="#1b1847">${escapeXml(item.value)}</text>`,
    );
  });
  page.cursorY += Math.ceil(items.length / 3) * (chipHeight + gap) + 6;
}

function addMetricGrid(page, metrics) {
  const cardsPerRow = 3;
  const gap = 14;
  const cardWidth = (CONTENT_WIDTH - gap * (cardsPerRow - 1)) / cardsPerRow;
  const cardHeight = 102;
  metrics.forEach((metric, index) => {
    const row = Math.floor(index / cardsPerRow);
    const col = index % cardsPerRow;
    const x = MARGIN_X + col * (cardWidth + gap);
    const y = page.cursorY + row * (cardHeight + gap);
    page.fragments.push(
      `<rect x="${x}" y="${y}" width="${cardWidth}" height="${cardHeight}" rx="18" fill="#ffffff" stroke="#e4defa" stroke-width="1" />`,
      `<text x="${x + 18}" y="${y + 28}" font-family="Menlo, Consolas, monospace" font-size="13" font-weight="700" fill="#6c66a1">${escapeXml(metric.code || '-')}</text>`,
      `<text x="${x + 18}" y="${y + 61}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="28" font-weight="800" fill="${toneColor(metric.tone)}">${escapeXml(safeMetricValue(metric))}</text>`,
      `<text x="${x + 18}" y="${y + 84}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="#726d9a">${escapeXml(metric.label || metric.code || '')}</text>`,
    );
  });
  page.cursorY += Math.ceil(metrics.length / cardsPerRow) * (cardHeight + gap) + 4;
}

async function addImageBlock(page, imagePath, title) {
  if (!imagePath) {
    return;
  }
  const dataUri = await imageToDataUri(imagePath);
  if (!dataUri) {
    return;
  }
  const imageSize = await getImageSize(imagePath);
  const maxHeight = 620;
  const scale = Math.min(MAX_PAGE_IMAGE_WIDTH / imageSize.width, maxHeight / imageSize.height, 1);
  const width = round1(imageSize.width * scale);
  const height = round1(imageSize.height * scale);
  const x = MARGIN_X + (CONTENT_WIDTH - width) / 2;
  page.fragments.push(
    `<text x="${MARGIN_X}" y="${page.cursorY}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="18" font-weight="700" fill="#1b1847">${escapeXml(title)}</text>`,
  );
  page.cursorY += 18;
  page.fragments.push(
    `<rect x="${x - 10}" y="${page.cursorY}" width="${width + 20}" height="${height + 20}" rx="18" fill="#fbfaff" stroke="#e4defa" stroke-width="1" />`,
    `<image href="${dataUri}" x="${x}" y="${page.cursorY + 10}" width="${width}" height="${height}" preserveAspectRatio="xMidYMid meet" />`,
  );
  page.cursorY += height + 38;
}

function frameworkRowHeight() {
  return 30;
}

function drawTableHeader(page, columns) {
  const headerY = page.cursorY;
  page.fragments.push(
    `<rect x="${MARGIN_X}" y="${headerY}" width="${CONTENT_WIDTH}" height="34" rx="10" fill="#f4f2fe" />`,
  );
  columns.forEach((column) => {
    page.fragments.push(
      `<text x="${column.x}" y="${headerY + 22}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="12" font-weight="700" fill="#6b649d">${escapeXml(column.label)}</text>`,
    );
  });
  page.cursorY += 42;
}

function addSingleFrameworkRows(pages, framework) {
  const columns = [
    { label: '项目', x: MARGIN_X + 12, width: 260 },
    { label: '数值', x: MARGIN_X + 270, width: 160 },
    { label: '参考', x: MARGIN_X + 430, width: 250 },
    { label: '状态', x: MARGIN_X + 700, width: 120 },
  ];
  let page = ensurePage(pages, 120);
  addSectionTitle(page, framework.label, `完整项目 ${framework.items.length} 项，当前状态：${formatFrameworkStatus(framework.status)}`);
  drawTableHeader(page, columns);

  for (const item of ensureArray(framework.items)) {
    page = ensurePage(pages, 56);
    if (page.cursorY <= MARGIN_Y + 140) {
      drawTableHeader(page, columns);
    }
    const y = page.cursorY;
    const valueText = item.status === 'supported'
      ? (item.valueText || (Number.isFinite(item.value) ? String(item.value) : '-'))
      : `暂不支持：${item.reason || '-'}`;
    const statusText = item.status === 'supported'
      ? (item.tone === 'success' ? '在范围内' : item.tone === 'danger' ? '偏离较大' : item.tone === 'warn' ? '轻度偏离' : '已计算')
      : '未算出';
    page.fragments.push(
      `<line x1="${MARGIN_X}" y1="${y + 22}" x2="${MARGIN_X + CONTENT_WIDTH}" y2="${y + 22}" stroke="#ece8fd" stroke-width="1" />`,
      `<text x="${columns[0].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" font-weight="700" fill="#1b1847">${escapeXml(item.label || item.code || '-')}</text>`,
      `<text x="${columns[1].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="${item.status === 'supported' ? toneColor(item.tone) : '#8b6380'}">${escapeXml(valueText)}</text>`,
      `<text x="${columns[2].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="#635d93">${escapeXml(item.reference || '-')}</text>`,
      `<text x="${columns[3].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="#635d93">${escapeXml(statusText)}</text>`,
    );
    page.cursorY += frameworkRowHeight();
  }

  page.cursorY += SECTION_GAP;
}

function buildOverlapComparisonRows(baseFramework, compareFramework) {
  const baseItems = new Map(ensureArray(baseFramework?.items).map((item) => [item.code, item]));
  const compareItems = new Map(ensureArray(compareFramework?.items).map((item) => [item.code, item]));
  const codes = Array.from(new Set([...baseItems.keys(), ...compareItems.keys()]));
  return codes.map((code) => ({
    code,
    base: baseItems.get(code) || null,
    compare: compareItems.get(code) || null,
  }));
}

function addOverlapFrameworkRows(pages, label, baseFramework, compareFramework) {
  const rows = buildOverlapComparisonRows(baseFramework, compareFramework);
  const columns = [
    { label: '项目', x: MARGIN_X + 12 },
    { label: '治疗前', x: MARGIN_X + 222 },
    { label: '治疗后', x: MARGIN_X + 412 },
    { label: '参考', x: MARGIN_X + 602 },
    { label: '差值', x: MARGIN_X + 832 },
  ];

  let page = ensurePage(pages, 120);
  addSectionTitle(page, label, `治疗前 ${formatFrameworkStatus(baseFramework?.status)}，治疗后 ${formatFrameworkStatus(compareFramework?.status)}。`);
  drawTableHeader(page, columns);

  for (const row of rows) {
    page = ensurePage(pages, 56);
    if (page.cursorY <= MARGIN_Y + 140) {
      drawTableHeader(page, columns);
    }
    const y = page.cursorY;
    const baseValue = row.base?.status === 'supported' ? (row.base.valueText || '-') : `未算出`;
    const compareValue = row.compare?.status === 'supported' ? (row.compare.valueText || '-') : `未算出`;
    const reference = row.base?.reference || row.compare?.reference || '-';
    const delta = row.base?.status === 'supported' && row.compare?.status === 'supported' && Number.isFinite(row.base.value) && Number.isFinite(row.compare.value)
      ? `${round1(row.compare.value - row.base.value)}${row.base.unit === 'mm' ? ' mm' : row.base.unit === '%' ? '%' : '°'}`
      : '-';

    page.fragments.push(
      `<line x1="${MARGIN_X}" y1="${y + 22}" x2="${MARGIN_X + CONTENT_WIDTH}" y2="${y + 22}" stroke="#ece8fd" stroke-width="1" />`,
      `<text x="${columns[0].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" font-weight="700" fill="#1b1847">${escapeXml(row.base?.label || row.compare?.label || row.code || '-')}</text>`,
      `<text x="${columns[1].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="${row.base?.status === 'supported' ? toneColor(row.base?.tone) : '#8b6380'}">${escapeXml(baseValue)}</text>`,
      `<text x="${columns[2].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="${row.compare?.status === 'supported' ? toneColor(row.compare?.tone) : '#8b6380'}">${escapeXml(compareValue)}</text>`,
      `<text x="${columns[3].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="#635d93">${escapeXml(reference)}</text>`,
      `<text x="${columns[4].x}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="#635d93">${escapeXml(delta)}</text>`,
    );
    page.cursorY += frameworkRowHeight();
  }
  page.cursorY += SECTION_GAP;
}

function buildSingleSummaryItems(result) {
  const analysis = result.analysis || {};
  return [
    { label: '模式', value: '单图测量' },
    { label: '结论', value: analysis.riskLabel || '-' },
    { label: '支持指标', value: String(ensureArray(result.metrics).length) },
  ];
}

function buildOverlapSummaryItems(result) {
  return [
    { label: '模式', value: '重叠对比' },
    { label: '对齐', value: result.alignMode || result.summary?.alignLabel || '-' },
    { label: '框架', value: String(ensureArray(result.frameworkChoices).length) },
  ];
}

function makeSvgPage(page) {
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${PAGE_WIDTH}" height="${PAGE_HEIGHT}" viewBox="0 0 ${PAGE_WIDTH} ${PAGE_HEIGHT}">`,
    ...page.fragments,
    `</svg>`,
  ].join('');
}

async function renderPagesToJpegs(svgPages, tempDir) {
  const pages = [];
  for (let index = 0; index < svgPages.length; index += 1) {
    const svgPath = path.join(tempDir, `page-${String(index + 1).padStart(2, '0')}.svg`);
    const jpgPath = path.join(tempDir, `page-${String(index + 1).padStart(2, '0')}.jpg`);
    await fs.writeFile(svgPath, svgPages[index], 'utf8');
    await convertSvgToJpeg(svgPath, jpgPath);
    const jpegBuffer = await fs.readFile(jpgPath);
    const { width, height } = await getImageSize(jpgPath);
    pages.push({
      jpegBuffer,
      imageWidth: width,
      imageHeight: height,
    });
  }
  return pages;
}

async function generateLegacyPdfReport({ inputPath, outputPath }) {
  const resolvedInputPath = path.resolve(inputPath);
  const resolvedOutputPath = path.resolve(outputPath || defaultPdfPath(resolvedInputPath));
  const payload = JSON.parse(await fs.readFile(resolvedInputPath, 'utf8'));
  const pages = [];
  let page = createPage(pages);

  const mode = String(payload.mode || payload.analysis?.type || 'image').trim();
  const reportTitle = mode === 'overlap' ? 'HYFCeph 重叠对比报告' : 'HYFCeph 侧位片测量报告';
  const generatedAt = formatDateTime(new Date().toISOString());
  addSectionTitle(page, reportTitle, `本地生成时间：${generatedAt}`);

  if (mode === 'overlap') {
    addSummaryChips(page, buildOverlapSummaryItems(payload));
    addParagraph(page, `治疗前结论：${payload.analysis?.base?.riskLabel || payload.summary?.baseRiskLabel || '-'}。治疗后结论：${payload.analysis?.compare?.riskLabel || payload.summary?.compareRiskLabel || '-'}。`, 78);
    await addImageBlock(page, payload.annotatedPngPath, '重叠图');

    const baseMetrics = ensureArray(payload.analysis?.base?.metrics);
    const compareMetrics = ensureArray(payload.analysis?.compare?.metrics);
    const baseMetricMap = new Map(baseMetrics.map((metric) => [metric.code, metric]));
    const compareMetricMap = new Map(compareMetrics.map((metric) => [metric.code, metric]));
    const metricRows = Array.from(new Set([...baseMetricMap.keys(), ...compareMetricMap.keys()])).map((code) => ({
      code,
      base: baseMetricMap.get(code) || null,
      compare: compareMetricMap.get(code) || null,
    }));

    page = ensurePage(pages, 160);
    addSectionTitle(page, '关键指标对比', '以下为服务端本次返回的治疗前后主要指标对比。');
    drawTableHeader(page, [
      { label: '指标', x: MARGIN_X + 12 },
      { label: '治疗前', x: MARGIN_X + 250 },
      { label: '治疗后', x: MARGIN_X + 470 },
      { label: '变化', x: MARGIN_X + 690 },
    ]);
    for (const row of metricRows) {
      page = ensurePage(pages, 56);
      if (page.cursorY <= MARGIN_Y + 140) {
        drawTableHeader(page, [
          { label: '指标', x: MARGIN_X + 12 },
          { label: '治疗前', x: MARGIN_X + 250 },
          { label: '治疗后', x: MARGIN_X + 470 },
          { label: '变化', x: MARGIN_X + 690 },
        ]);
      }
      const y = page.cursorY;
      const baseText = safeMetricValue(row.base);
      const compareText = safeMetricValue(row.compare);
      const delta = row.base && row.compare && Number.isFinite(row.base.value) && Number.isFinite(row.compare.value)
        ? `${round1(row.compare.value - row.base.value)}`
        : '-';
      page.fragments.push(
        `<line x1="${MARGIN_X}" y1="${y + 22}" x2="${MARGIN_X + CONTENT_WIDTH}" y2="${y + 22}" stroke="#ece8fd" stroke-width="1" />`,
        `<text x="${MARGIN_X + 12}" y="${y + 18}" font-family="Menlo, Consolas, monospace" font-size="13" font-weight="700" fill="#1b1847">${escapeXml(row.code)}</text>`,
        `<text x="${MARGIN_X + 250}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="${row.base ? toneColor(row.base.tone) : '#8b6380'}">${escapeXml(baseText)}</text>`,
        `<text x="${MARGIN_X + 470}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="${row.compare ? toneColor(row.compare.tone) : '#8b6380'}">${escapeXml(compareText)}</text>`,
        `<text x="${MARGIN_X + 690}" y="${y + 18}" font-family="PingFang SC, Noto Sans SC, sans-serif" font-size="13" fill="#635d93">${escapeXml(delta)}</text>`,
      );
      page.cursorY += frameworkRowHeight();
    }
    page.cursorY += SECTION_GAP;

    const baseFrameworks = normalizeFrameworkEntries(payload.analysis?.base?.frameworkReports, payload.frameworkChoices);
    const compareFrameworkMap = new Map(normalizeFrameworkEntries(payload.analysis?.compare?.frameworkReports, payload.frameworkChoices).map((item) => [item.code, item]));
    for (const framework of baseFrameworks) {
      addOverlapFrameworkRows(pages, framework.label, framework, compareFrameworkMap.get(framework.code));
    }
  } else {
    addSummaryChips(page, buildSingleSummaryItems(payload));
    addParagraph(page, payload.analysis?.insight || payload.summary?.riskLabel || '本次服务端测量已完成。', 80);
    await addImageBlock(page, payload.annotatedPngPath, '标注图');

    page = ensurePage(pages, 180);
    addSectionTitle(page, '关键指标', '以下为本次返回的主要测量值。');
    addMetricGrid(page, ensureArray(payload.metrics));

    const frameworks = normalizeFrameworkEntries(payload.analysis?.frameworkReports, payload.frameworkChoices);
    for (const framework of frameworks) {
      addSingleFrameworkRows(pages, framework);
    }
  }

  const svgPages = pages.map((item) => makeSvgPage(item));
  const tempDir = await fs.mkdtemp(path.join(process.cwd(), 'hyfceph-pdf-'));
  const rasterPages = await renderPagesToJpegs(svgPages, tempDir);
  const pdfBuffer = buildJpegPdf(rasterPages);
  await fs.mkdir(path.dirname(resolvedOutputPath), { recursive: true });
  await fs.writeFile(resolvedOutputPath, pdfBuffer);
  return path.resolve(resolvedOutputPath);
}

export async function generateHyfcephPdfReport({ inputPath, outputPath, patientName }) {
  const resolvedInputPath = path.resolve(inputPath);
  const resolvedOutputPath = path.resolve(outputPath || defaultPdfPath(resolvedInputPath));
  const payload = JSON.parse(await fs.readFile(resolvedInputPath, 'utf8'));
  if (patientName) {
    payload.patientName = patientName;
  }

  try {
    const html = await buildHtmlReport(payload);
    await fs.mkdir(path.dirname(resolvedOutputPath), { recursive: true });
    return await renderHtmlToPdfWithChrome(html, resolvedOutputPath);
  } catch (chromeError) {
    try {
      return await generateLegacyPdfReport({
        inputPath: resolvedInputPath,
        outputPath: resolvedOutputPath,
      });
    } catch (legacyError) {
      const chromeReason = chromeError instanceof Error ? chromeError.message : String(chromeError);
      const legacyReason = legacyError instanceof Error ? legacyError.message : String(legacyError);
      throw new Error(`本地 PDF 生成失败（Chrome/Chromium 不可用：${chromeReason}；SVG 转 JPEG 工具不可用：${legacyReason}）。`);
    }
  }
}

async function main() {
  const { values } = parseArgs({
    options: {
      input: { type: 'string' },
      output: { type: 'string' },
      help: { type: 'boolean', short: 'h', default: false },
    },
  });

  if (values.help || !values.input) {
    console.log(`Usage:
  node scripts/hyfceph-report-pdf.mjs --input /path/to/result.json [--output /path/to/report.pdf]
`);
    return;
  }

  const pdfPath = await generateHyfcephPdfReport({
    inputPath: values.input,
    outputPath: values.output,
  });

  console.log(JSON.stringify({ pdfPath }, null, 2));
}

const isDirectRun = (() => {
  if (!process.argv[1]) {
    return false;
  }
  return path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
})();

if (isDirectRun) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
