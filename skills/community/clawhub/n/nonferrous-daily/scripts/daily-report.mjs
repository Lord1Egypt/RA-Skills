import { readFileSync, existsSync, mkdirSync, writeFileSync, appendFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { execFile } from 'child_process';
import { promisify } from 'util';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..');
const REPORT_CACHE_PATH = join(PROJECT_ROOT, 'memory', 'daily-report-state.json');
const SIGNAL_HISTORY_PATH = join(PROJECT_ROOT, 'memory', 'signal-history.jsonl');
const execFileAsync = promisify(execFile);

function loadEnv() {
  const envPath = join(PROJECT_ROOT, '.env');
  const env = {};
  try {
    const content = readFileSync(envPath, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIdx = trimmed.indexOf('=');
      if (eqIdx === -1) continue;
      const key = trimmed.slice(0, eqIdx).trim();
      const value = trimmed.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
      env[key] = value;
    }
  } catch {}
  return env;
}

async function runScript(scriptName) {
  const scriptPath = join(__dirname, scriptName);
  const { stdout, stderr } = await execFileAsync(process.execPath, [scriptPath], {
    timeout: 70000,
    maxBuffer: 8 * 1024 * 1024,
  });
  if (stderr) process.stderr.write(stderr);
  return JSON.parse(stdout);
}

function fmtNum(n, decimals = 0) {
  if (n == null || Number.isNaN(Number(n))) return '—';
  const parts = Number(n).toFixed(decimals).split('.');
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return decimals > 0 ? parts.join('.') : parts[0];
}

function fmtPct(n, decimals = 2) {
  if (n == null || Number.isNaN(Number(n))) return '—';
  return `${n >= 0 ? '+' : ''}${Number(n).toFixed(decimals)}%`;
}

function usdToCnyPerTon(usd, unit, fxRate) {
  if (usd == null || fxRate == null) return null;
  const usdPerTon = unit === 'USD/lb' ? usd * 2204.62 : usd;
  return usdPerTon * fxRate;
}

function loadSignalHistory() {
  if (!existsSync(SIGNAL_HISTORY_PATH)) return [];
  const raw = readFileSync(SIGNAL_HISTORY_PATH, 'utf-8').split('\n').filter(Boolean);
  const rows = [];
  for (const l of raw) {
    try { rows.push(JSON.parse(l)); } catch {}
  }
  return rows;
}

function appendSignalHistory(records) {
  const dir = join(PROJECT_ROOT, 'memory');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const existing = loadSignalHistory();
  const existingKey = new Set(existing.map(r => `${r.date}|${r.metal}`));
  const toAppend = records.filter(r => !existingKey.has(`${r.date}|${r.metal}`));
  if (!toAppend.length) return 0;
  appendFileSync(SIGNAL_HISTORY_PATH, toAppend.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf-8');
  return toAppend.length;
}

function recentSeries(history, metal, n = 20) {
  return history.filter(r => r.metal === metal && r.cny != null).slice(-n);
}

function toArrayMaybe(v) {
  return Array.isArray(v) ? v : [];
}

function normalizeSymbol(symbol) {
  return String(symbol || '').toUpperCase().replace(/\s+/g, '');
}

function pickIndustryRaw(data = {}) {
  return [
    ...toArrayMaybe(data.industryIndices),
    ...toArrayMaybe(data.indices),
    ...toArrayMaybe(data.metalIndices),
    ...toArrayMaybe(data.industryIndex),
  ];
}

function ensureIndustryIndices(data = {}) {
  const industryRaw = pickIndustryRaw(data);
  const targets = [
    { symbol: 'XME', name: 'SPDR S&P Metals & Mining ETF', cnName: '标普金属与采矿ETF', aliases: ['XME'] },
    { symbol: 'COPX', name: 'Global X Copper Miners ETF', cnName: '全球X铜矿ETF', aliases: ['COPX'] },
    { symbol: '000812.SS', name: '上证有色金属指数', cnName: '上证有色金属指数', aliases: ['000812.SS', '000812.SH', '000812', 'SH000812'] },
  ];

  return targets.map(t => {
    const hit = industryRaw.find(x => {
      const s = normalizeSymbol(x?.symbol ?? x?.code ?? x?.ticker ?? x?.name);
      return t.aliases.some(a => normalizeSymbol(a) === s);
    });

    const price = hit?.price ?? hit?.last ?? hit?.value ?? hit?.close ?? null;
    const changePct = hit?.changePct ?? hit?.pct ?? hit?.change_percent ?? hit?.percent ?? null;
    const wowPct = hit?.wowPct ?? hit?.weekOverWeekPct ?? hit?.weeklyChangePct ?? null;

    if (!hit || price == null) {
      return {
        symbol: t.symbol,
        name: t.name,
        cnName: t.cnName,
        missing: true,
        reason: `缺失：${t.symbol} 暂无可用行情；替代：以六品种趋势一致性与预警共振做判断。`,
      };
    }

    return {
      symbol: t.symbol,
      name: t.name,
      cnName: t.cnName,
      missing: false,
      price,
      changePct,
      wowPct,
    };
  });
}

function keywordEvidence(text, keywords) {
  const t = (text || '').toLowerCase();
  const hits = keywords.filter(k => t.includes(k.toLowerCase()));
  return { count: hits.length, hits: hits.slice(0, 4) };
}

function hardAlertLevel({ cny, cnyChange, invChange, sentimentCount, hasInventory }) {
  const prev = (cny != null && cnyChange != null) ? (cny - cnyChange) : null;
  const volPct = (prev && prev !== 0) ? Math.abs((cnyChange / prev) * 100) : 0;

  const volScore = volPct >= 2.0 ? 2 : volPct >= 1.0 ? 1 : 0;
  const invScore = hasInventory
    ? (Math.abs(invChange ?? 0) >= 8000 ? 2 : Math.abs(invChange ?? 0) >= 3000 ? 1 : 0)
    : 0;
  const sentScore = sentimentCount >= 2 ? 1 : 0;

  return Math.max(0, Math.min(3, volScore + (invScore > 0 ? 1 : 0) + sentScore));
}

function alertLevelLabel(level) {
  if (level >= 3) return '高';
  if (level >= 2) return '中';
  return '低';
}

function calcSlopePct(series, window = 3) {
  if (!series?.length || series.length < window) return null;
  const s = series.slice(-window);
  const first = s[0]?.cny;
  const last = s[s.length - 1]?.cny;
  if (first == null || last == null || first === 0) return null;
  return ((last - first) / first) * 100;
}

function spreadStatus(cny, extCny) {
  if (cny == null || extCny == null) return { label: '缺失', basis: '内外盘价差缺失' };
  const diff = cny - extCny;
  const pct = extCny !== 0 ? (diff / extCny) * 100 : 0;
  if (pct >= 0.8) return { label: '内强', basis: `内外价差${fmtNum(diff, 0)}/吨（${fmtPct(pct, 2)}）` };
  if (pct <= -0.8) return { label: '外强', basis: `内外价差${fmtNum(diff, 0)}/吨（${fmtPct(pct, 2)}）` };
  return { label: '均衡', basis: `内外价差${fmtNum(diff, 0)}/吨（${fmtPct(pct, 2)}）` };
}

function inventoryDirection(invChange, hasInventory) {
  if (!hasInventory) return '未知';
  if (invChange == null) return '缺失';
  if (invChange > 0) return '累库';
  if (invChange < 0) return '去库';
  return '平稳';
}

function trendDirection(slope5) {
  if (slope5 == null) return '震荡';
  if (slope5 >= 0.8) return '上行';
  if (slope5 <= -0.8) return '下行';
  return '震荡';
}

function trendMomentum({ slope3, slope5, invDir, direction }) {
  if (slope3 == null || slope5 == null) {
    return { status: '不明', basis: '样本不足，无法比较近3日与近5日斜率' };
  }

  const sameSign = Math.sign(slope3) === Math.sign(slope5) || slope3 === 0 || slope5 === 0;
  const faster = Math.abs(slope3) >= Math.abs(slope5) * 1.15;
  const slower = Math.abs(slope3) <= Math.abs(slope5) * 0.75;
  const invAligned = direction === '上行'
    ? invDir === '去库'
    : direction === '下行'
      ? invDir === '累库'
      : false;

  if (!sameSign) {
    return { status: '衰减', basis: `近3日斜率${fmtPct(slope3)}与近5日斜率${fmtPct(slope5)}方向分歧` };
  }
  if (faster && (invAligned || invDir === '未知' || invDir === '缺失')) {
    return { status: '增强', basis: `近3日斜率${fmtPct(slope3)}高于近5日${fmtPct(slope5)}${invAligned ? '且库存配合' : ''}` };
  }
  if (slower) {
    return { status: '衰减', basis: `近3日斜率${fmtPct(slope3)}低于近5日${fmtPct(slope5)}，趋势斜率放缓` };
  }
  return { status: '维持', basis: `近3日斜率${fmtPct(slope3)}与近5日${fmtPct(slope5)}同向，节奏稳定` };
}

function trendStage({ direction, momentum, slope3, slope5 }) {
  if (slope3 != null && slope5 != null && Math.sign(slope3) !== Math.sign(slope5) && slope3 !== 0 && slope5 !== 0) {
    return '转折观察';
  }
  if (direction === '震荡') return '转折观察';
  if (momentum === '增强') return '启动期';
  if (momentum === '维持') return '延续期';
  if (momentum === '衰减') return '钝化期';
  return '转折观察';
}

function trendConfidence({ direction, slope3, slope5, invDir, spread, sentimentCount }) {
  const checks = [];
  if (slope3 != null && slope5 != null) checks.push(Math.sign(slope3) === Math.sign(slope5));

  if (direction === '上行') {
    if (invDir !== '未知' && invDir !== '缺失') checks.push(invDir === '去库' || invDir === '平稳');
    if (spread !== '缺失') checks.push(spread !== '外强');
  } else if (direction === '下行') {
    if (invDir !== '未知' && invDir !== '缺失') checks.push(invDir === '累库' || invDir === '平稳');
    if (spread !== '缺失') checks.push(spread !== '内强');
  } else {
    checks.push(true);
  }

  checks.push(sentimentCount >= 2);

  const agree = checks.filter(Boolean).length;
  if (agree >= 4) return '高';
  if (agree >= 2) return '中';
  return '低';
}

function oneLineOverview(items) {
  const up = items.filter(x => x.trendDirection === '上行').length;
  const down = items.filter(x => x.trendDirection === '下行').length;
  const highAlert = items.filter(x => x.alertLevel >= 2).map(x => x.code);
  if (up > down) return `主线：有色处于偏多趋势，优先跟踪 ${highAlert.length ? highAlert.join('/') : '核心品种'} 的回踩建仓机会。`;
  if (down > up) return `主线：有色偏弱，维持防守仓位，优先处理 ${highAlert.length ? highAlert.join('/') : '高波动品种'} 的回撤风险。`;
  return `主线：板块震荡分化，仓位以均衡配置为主，盯住 ${highAlert.length ? highAlert.join('/') : '关键品种'} 趋势确认信号。`;
}

function buildTradePoints(items) {
  const up = items.filter(x => x.trendDirection === '上行').map(x => x.code);
  const down = items.filter(x => x.trendDirection === '下行').map(x => x.code);
  const highConf = items.filter(x => x.trendConfidence === '高').map(x => x.code);
  const momentumDecay = items.filter(x => x.momentum.status === '衰减').map(x => x.code);

  const trendLine = up.length > down.length
    ? `主趋势线（未来1-3周）：偏上行，重点跟踪 ${up.slice(0, 4).join('/')} 的延续与回踩确认。`
    : down.length > up.length
      ? `主趋势线（未来1-3周）：偏下行，重点防守 ${down.slice(0, 4).join('/')} 的反弹失败风险。`
      : '主趋势线（未来1-3周）：震荡分化，等待趋势置信度升至“高”的品种成为主线。';

  const config = up.length > down.length
    ? `配置建议：进攻/防守≈6:4，进攻端优先 ${highConf.length ? highConf.join('/') : '趋势置信度较高品种'}，防守端保留现金与低波动品种。`
    : down.length > up.length
      ? '配置建议：进攻/防守≈3:7，防守端以现金和低波动品种为主，仅对高置信度反弹做小比例试仓。'
      : '配置建议：进攻/防守≈5:5，采用均衡配置，等待趋势共振后再偏向单侧。';

  const trigger = momentumDecay.length
    ? `触发器：若 ${momentumDecay.join('/')} 持续两日“动量衰减”且斜率转负，减仓10%-20%；若转为“增强”并伴随库存配合，再恢复仓位。`
    : '触发器：当任一主线品种由“维持”切换为“增强”并保持两日，分批加仓；若转为“衰减”，先降仓再观察。';

  return { trendLine, config, trigger };
}

function buildRisks(items) {
  const reversal = items.filter(x => x.trendStage === '转折观察' || x.momentum.status === '衰减').map(x => x.code);
  return [
    `趋势反转风险：${reversal.length ? reversal.join('/') : '当前主线品种'} 出现斜率背离或动量衰减时，按失效条件先减仓后验证。`,
    '宏观/汇率风险：美元与风险偏好共振时，内外盘价差可能快速重估；USD/CNY波动放大阶段降低进攻仓位。',
    '数据失真或时滞风险：库存与资讯存在发布时滞，若价格与数据连续两日背离，降低数据权重并以价格趋势优先。',
  ];
}

function buildStrategy(x) {
  if (x.trendDirection === '上行') {
    return '策略：建仓区=近5日均线下方0%-1.5%回踩区；加仓条件=动量“增强”且库存去库/平稳，减仓条件=动量转“衰减”，失效条件=收盘跌破近5日低点。';
  }
  if (x.trendDirection === '下行') {
    return '策略：建仓区=仅保留防守底仓并等待企稳；加仓条件=由“衰减”转“维持”并连续两日，减仓条件=反弹至近5日高位受阻，失效条件=趋势方向转“上行”且置信度升至中高。';
  }
  return '策略：建仓区=区间下沿分批试仓；加仓条件=趋势方向明确并置信度升至“中”以上，减仓条件=区间中上沿动量衰减，失效条件=区间破位并延续两日。';
}

function buildReport(d, histRows) {
  const fx = d.fxRates?.usdCny?.price ?? null;
  const p = d.prices || {};
  const inv = d.inventory || {};
  const forum = d.forumSentiment || {};
  const newsText = [
    ...(d.news || []).map(x => x.title || ''),
    ...(d.ibNews || []).map(x => x.title || ''),
    forum.smmHighlights || '',
    forum.redditSurging || '',
    forum.redditSummary || '',
  ].join(' | ');

  const defs = [
    { key: 'copper', code: 'Cu', name: '铜', unit: 'USD/lb', invKey: 'copper', kws: ['copper', '铜', 'comex', 'tc'] },
    { key: 'zinc', code: 'Zn', name: '锌', unit: 'USD/t', invKey: 'zinc', kws: ['zinc', '锌', 'galvanized', '镀锌'] },
    { key: 'nickel', code: 'Ni', name: '镍', unit: 'USD/t', invKey: 'nickel', kws: ['nickel', '镍', 'npi', '不锈钢'] },
    { key: 'cobalt', code: 'Co', name: '钴', unit: 'USD/t', invKey: null, kws: ['cobalt', '钴', 'battery', '新能源'] },
    { key: 'bismuth', code: 'Bi', name: '铋', unit: 'USD/t', invKey: null, kws: ['bismuth', '铋', '半导体', '医药'] },
    { key: 'magnesium', code: 'Mg', name: '镁', unit: 'USD/t', invKey: null, kws: ['magnesium', '镁', '轻量化', '煤'] },
  ];

  const items = [];
  const records = [];

  for (const def of defs) {
    const item = p[def.key] || {};
    const invRow = def.invKey ? inv?.[def.invKey] : null;
    const kw = keywordEvidence(newsText, def.kws);

    const extCny = item.usd != null && fx != null ? usdToCnyPerTon(item.usd, def.unit, fx) : null;
    const spread = spreadStatus(item.cny ?? null, extCny);
    const invDir = inventoryDirection(invRow?.change ?? null, Boolean(def.invKey));

    const hist = recentSeries(histRows, def.code, 20);
    const series = [...hist];
    if (item.cny != null) {
      const lastDate = series[series.length - 1]?.date;
      if (lastDate !== d.date) series.push({ date: d.date, cny: item.cny });
    }

    const slope3 = calcSlopePct(series, 3);
    const slope5 = calcSlopePct(series, 5);
    const direction = trendDirection(slope5);
    const momentum = trendMomentum({ slope3, slope5, invDir, direction });
    const stage = trendStage({ direction, momentum: momentum.status, slope3, slope5 });
    const confidence = trendConfidence({
      direction,
      slope3,
      slope5,
      invDir,
      spread: spread.label,
      sentimentCount: kw.count,
    });

    const alertLevel = hardAlertLevel({
      cny: item.cny ?? null,
      cnyChange: item.cnyChange ?? 0,
      invChange: invRow?.change ?? null,
      sentimentCount: kw.count,
      hasInventory: Boolean(def.invKey),
    });

    const inventoryText = def.invKey
      ? (invRow?.tonnes != null
          ? `${fmtNum(invRow.tonnes)}t（${(invRow.change ?? 0) >= 0 ? '+' : ''}${fmtNum(invRow.change ?? 0)}t，${invDir}）`
          : '缺失与替代依据：库存缺失，改用近3日/5日斜率与价差判断')
      : '缺失与替代依据：该品种无稳定库存口径，改用斜率+价差+情绪辅助';

    items.push({
      code: def.code,
      name: def.name,
      trendStage: stage,
      trendDirection: direction,
      trendConfidence: confidence,
      observeCycle: '短中期（5-20交易日）',
      slope3,
      slope5,
      momentum,
      spread,
      invDir,
      inventoryText,
      sentimentHits: kw.hits,
      sentimentCount: kw.count,
      cny: item.cny ?? null,
      usd: item.usd ?? null,
      cnyChange: item.cnyChange ?? null,
      alertLevel,
    });

    records.push({
      date: d.date,
      metal: def.code,
      cny: item.cny ?? null,
      usd: item.usd ?? null,
      lmeInv: invRow?.tonnes ?? null,
      cnyChange: item.cnyChange ?? null,
      alertLevel,
      trendTag: direction,
      trendStage: stage,
      trendConfidence: confidence,
      keyEvidence: `slope3=${slope3 ?? 'NA'} slope5=${slope5 ?? 'NA'} inv=${invDir} spread=${spread.label} sentiment=${kw.count}`,
    });
  }

  const industry = ensureIndustryIndices(d);
  const overview = oneLineOverview(items);
  const points = buildTradePoints(items);
  const risks = buildRisks(items);

  const lines = [];
  lines.push(`有色金属趋势研报 | ${d.date}`);
  lines.push('');
  lines.push(`一句话总览：${overview}`);
  lines.push('');

  lines.push('1) 行业指数');
  for (const idx of industry) {
    const label = `${idx.symbol}（${idx.cnName || idx.name || idx.symbol}）`;
    if (idx.missing) {
      lines.push(`- ${label}：${idx.reason}`);
    } else {
      const wowText = idx.wowPct == null
        ? '周环比缺失'
        : `周环比 ${(idx.wowPct >= 0 ? '+' : '') + fmtNum(idx.wowPct, 2)}%`;
      lines.push(`- ${label}：${fmtNum(idx.price, 3)}（日变 ${(idx.changePct ?? 0) >= 0 ? '+' : ''}${fmtNum(idx.changePct ?? 0, 2)}%｜${wowText}）`);
    }
  }
  lines.push('');

  lines.push('2) 品种数据');
  for (const x of items) {
    const extText = (x.sentimentHits?.length ?? 0) > 0
      ? `${x.sentimentCount}（${x.sentimentHits.join('、')}）`
      : `${x.sentimentCount}`;

    lines.push(`*${x.name}（${x.code}）*`);
    lines.push(`趋势阶段：${x.trendStage}｜趋势方向：${x.trendDirection}｜趋势置信度：${x.trendConfidence}｜观察周期：${x.observeCycle}｜预警：${alertLevelLabel(x.alertLevel)}`);
    lines.push(`依据：近3日斜率${fmtPct(x.slope3)}｜近5日斜率${fmtPct(x.slope5)}｜库存${x.inventoryText}｜内外盘价差${x.spread.basis}｜情绪命中${extText}（辅助）`);
    lines.push(`趋势动量状态：${x.momentum.status}（${x.momentum.basis}）`);
    lines.push(buildStrategy(x));
    lines.push('');
  }

  lines.push('3) 交易要点（技术面/信号摘要）');
  lines.push(`- ${points.trendLine}`);
  lines.push(`- ${points.config}`);
  lines.push(`- ${points.trigger}`);
  lines.push('');

  lines.push('4) 关键风险');
  for (const r of risks) lines.push(`- ${r}`);
  lines.push('');

  lines.push(`数据源与时间戳：Yahoo/CCMN/SMM/Westmetall/GoogleNews/Reddit；生成时间 ${new Date().toISOString()}`);

  return { message: lines.join('\n'), records };
}

async function sendTelegram(token, chatId, text) {
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ chat_id: chatId, text }),
    signal: AbortSignal.timeout(15000),
  });
  const data = await res.json();
  if (!data.ok) throw new Error(`Telegram API error: ${JSON.stringify(data)}`);
  return data;
}

function saveReportState(state) {
  try {
    const dir = join(PROJECT_ROOT, 'memory');
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    writeFileSync(REPORT_CACHE_PATH, JSON.stringify(state, null, 2), 'utf-8');
  } catch {}
}

async function main() {
  const data = await runScript('fetch-all-data.mjs');
  const history = loadSignalHistory();
  const { message, records } = buildReport(data, history);

  console.log('\n─── 报告预览 ───');
  console.log(message);
  console.log('────────────────\n');

  const env = loadEnv();
  const token = env.TELEGRAM_BOT_TOKEN;
  const chatId = env.TELEGRAM_CHAT_ID;
  const dryRun = process.env.DRY_RUN === '1' || process.env.DRY_RUN === 'true';

  if (!dryRun) {
    appendSignalHistory(records);
    saveReportState({ generatedAt: new Date().toISOString(), date: data.date, recordsCount: records.length });
  }

  if (!token) {
    process.stderr.write('[daily-report] 未配置 TELEGRAM_BOT_TOKEN，跳过发送\n');
    return;
  }
  if (dryRun) {
    process.stderr.write('[daily-report] DRY_RUN=1，仅预览，不发送\n');
    return;
  }

  try {
    await sendTelegram(token, chatId, message);
    process.stderr.write('[daily-report] ✅ 发送成功\n');
  } catch (err) {
    process.stderr.write(`[daily-report] ❌ 发送失败：${err.message}\n`);
    process.stderr.write('[daily-report] 以下为可复制全文：\n');
    process.stderr.write(message + '\n');
    throw err;
  }
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
