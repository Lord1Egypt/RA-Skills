export const RISK = {
  CRITICAL: { label: 'CRITICAL', emoji: '🔴' },
  TIGHT:    { label: 'TIGHT',    emoji: '🟡' },
  OK:       { label: 'OK',       emoji: '🟢' },
  SAFE:     { label: 'SAFE',     emoji: '✅' },
};

export const verdicts = {
  zugbindung: {
    veryLikely:  (pct) => `Zugbindung release highly likely (>${pct}%).`,
    likely:      (pct) => `Zugbindung release probable (>${pct}%).`,
    unlikely:    (pct) => `Zugbindung release unlikely (<${pct}%).`,
    veryUnlikely:(pct) => `Zugbindung release very unlikely (<${pct}%).`,
  },
  transfer: {
    safe:     (min) => `Transfer is safe. ${min}min buffer.`,
    tight:    (min) => `Transfer is tight. ${min}min buffer — monitor delays.`,
    critical: (min) => `Transfer is critical. ${min}min buffer — have alternatives ready.`,
  },
  live: {
    lifted:   () => `Ticket binding lifted — you may take any train.`,
    safe:     (min, at) => `Transfer is safe. ${min}min effective buffer at ${at}.`,
    atRisk:   (at) => `Transfer at risk at ${at}. Consider alternatives.`,
    missed:   (at) => `Transfer at ${at} very likely missed. Switch to alternative route.`,
  },
};

export function fmtTime(iso) {
  if (!iso) return '??:??';
  return iso.slice(11, 16);
}

export function fmtDuration(ms) {
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

export function transferRisk(minutes) {
  if (minutes <= 4) return RISK.CRITICAL;
  if (minutes <= 7) return RISK.TIGHT;
  if (minutes <= 14) return RISK.OK;
  return RISK.SAFE;
}

// ── helpers ──────────────────────────────────────────
const pct = (p) => `${(p * 100).toFixed(1)}%`;
const pad = (s, n) => String(s).padEnd(n);
const padL = (s, n) => String(s).padStart(n);

function fmtDelay(d) {
  if (d === null || d === undefined) return '—';
  if (d === 0) return 'on time';
  return d > 0 ? `+${d}min` : `${d}min`;
}

function appendFooter(lines, envelope) {
  if (envelope.errors?.length) {
    lines.push('');
    lines.push('Errors:');
    for (const e of envelope.errors) lines.push(`  - ${e}`);
  }
  if (envelope.warnings?.length) {
    lines.push('');
    lines.push('Warnings:');
    for (const w of envelope.warnings) lines.push(`  - ${w}`);
  }
}

// ── mode formatters ─────────────────────────────────

function formatParse(env) {
  const lines = [];
  const { connection: conn, assessment } = env;

  if (!conn) {
    lines.push('Parse failed — no connection data.');
    return lines;
  }

  // Header
  lines.push(`━━━ Connection Analysis ━━━━━━━━━━━━━━━━━━━━━━━━━`);
  lines.push(`${conn.from} → ${conn.to} | ${conn.date}`);
  lines.push(`${conn.legs.length} legs, ${conn.legs.length - 1} transfers`);
  lines.push('');

  // Per-leg table
  lines.push(`── Legs ──`);

  // Check if any leg has historicalStats (--stats) or if assessment exists (--predict)
  const hasStats = conn.legs.some(l => l.historicalStats);

  if (hasStats) {
    lines.push(`  ${pad('Train', 16)} ${pad('From→To', 42)} ${padL('Mean', 7)} ${padL('p95', 6)} ${padL('P(≥20m)', 8)} ${padL('Days', 4)}`);
    for (const leg of conn.legs) {
      const hs = leg.historicalStats;
      const route = `${leg.from || '?'} → ${leg.to || '?'}`;
      if (hs) {
        const meanStr = hs.mean != null ? `${hs.mean.toFixed(1)}m` : '—';
        const p95Str = hs.p95 != null ? `${hs.p95.toFixed(0)}m` : '—';
        const zbStr = hs.zugbindungRate != null ? pct(hs.zugbindungRate) : '—';
        lines.push(
          `  ${pad(leg.train, 16)} ${pad(route, 42)} ${padL(meanStr, 7)} ${padL(p95Str, 6)} ${padL(zbStr, 8)} ${padL(hs.samples, 4)}`
        );
      } else {
        lines.push(`  ${pad(leg.train, 16)} ${pad(route, 42)} ${'—'.padStart(7)} ${'—'.padStart(6)} ${'—'.padStart(8)} ${'—'.padStart(4)}`);
      }
    }
  } else {
    lines.push(`  ${pad('Train', 16)} ${pad('Dep', 6)} ${pad('From', 24)} ${pad('Arr', 6)} ${pad('To', 24)}`);
    for (const leg of conn.legs) {
      lines.push(
        `  ${pad(leg.train, 16)} ${pad(leg.dep || '?', 6)} ${pad(leg.from || '?', 24)} ${pad(leg.arr || '?', 6)} ${pad(leg.to || '?', 24)}`
      );
    }
  }
  lines.push('');

  // Per-transfer table
  lines.push(`── Transfers ──`);
  for (const t of conn.transfers) {
    const risk = RISK[t.risk] || transferRisk(t.scheduledMinutes);
    const buffer = t.scheduledMinutes - 2;
    const plat = t.platformChange ? ` [Gl.${t.platformFrom}→${t.platformTo}]` : '';
    const flags = [];
    if (t.differentStation) flags.push('DIFFERENT STATION');
    if (risk.label === 'CRITICAL') flags.push('CRITICAL');
    const catchStr = t.catchProb != null ? pct(t.catchProb) : '—';
    lines.push(
      `  ${risk.emoji} ${pad(risk.label, 9)} ${padL(t.scheduledMinutes + 'min', 5)} (buf ${padL(buffer + 'm', 4)}) at ${pad(t.at || '?', 36)}${plat}`
      + (catchStr !== '—' ? ` — ${catchStr} catch` : '')
      + (flags.length ? `  ${flags.join(' | ')}` : '')
    );
  }
  lines.push('');

  // Zugbindung
  if (assessment?.zugbindung) {
    lines.push(`━━━ Zugbindung ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    lines.push(`  P(Zugbindung triggered) = ${pct(assessment.zugbindung.prob)}`);
    if (assessment.zugbindung.verdict) {
      lines.push(`  ${assessment.zugbindung.verdict}`);
    }
    lines.push('');
  }

  // Overall
  if (assessment?.reach) {
    const r = assessment.reach;
    lines.push(`━━━ Overall ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    lines.push(`  P(all transfers)     = ${pct(r.pAllTransfers)}`);
    lines.push(`  P(no cancellations)  = ${pct(r.pNoCancellations)}`);
    lines.push(`  P(reaching ${conn.to}) = ${pct(r.pReaching)}`);
    lines.push('');
  }

  // Verdict
  if (assessment?.verdict) {
    lines.push(assessment.verdict);
    lines.push('');
  }

  // Disruptions per leg
  const disruptedLegs = conn.legs.filter(l => l.remarks?.length > 0);
  if (disruptedLegs.length) {
    lines.push(`━━━ Disruptions ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    for (const leg of disruptedLegs) {
      for (const r of leg.remarks) {
        lines.push(`  ⚠ ${leg.train || '?'}: ${r.text || '?'}`);
      }
    }
    lines.push('');
  }

  return lines;
}

function formatLive(env) {
  const lines = [];
  const s = env.liveStatus;

  if (!s) {
    lines.push('Live check failed — no status data.');
    return lines;
  }

  const cur = s.currentLeg || {};

  const delay = cur.delay ?? 0;
  const delayStr = delay > 0 ? `+${delay}min delay` : 'on time';
  lines.push(`Current: ${cur.train || '?'} at ${cur.station || '?'} — ${delayStr}`);

  if (delay >= 20 || s.zugbindungStatus?.startsWith('triggered')) {
    lines.push('');
    lines.push('Zugbindung lifted — you may take any train.');
  }

  if (s.nextTransfer) {
    const nt = s.nextTransfer;
    const risk = RISK[nt.risk] || transferRisk(nt.effectiveMinutes);
    lines.push('');
    lines.push(`Next transfer: ${nt.nextTrain} in ${nt.effectiveMinutes}min (scheduled ${nt.scheduledMinutes}min)`);
    if (nt.catchProb != null) {
      lines.push(`${risk.emoji} P(making it): ${pct(nt.catchProb)}`);
    } else {
      lines.push(`${risk.emoji} ${risk.label}`);
    }
  }

  if (s.recommendation) {
    lines.push('');
    lines.push(`Recommendation: ${s.recommendation}`);
  }

  if (s.remainingTransfers?.length) {
    lines.push('');
    lines.push('Remaining transfers:');
    for (const rt of s.remainingTransfers) {
      const risk = RISK[rt.risk] || transferRisk(rt.minutes);
      const catchStr = rt.catchProb != null ? ` — ${pct(rt.catchProb)} catch rate` : '';
      lines.push(`  ${risk.emoji} ${rt.minutes}min at ${rt.at}${catchStr}`);
    }
  }

  return lines;
}

function formatJourney(env) {
  const lines = [];
  const opts = env.journeyOptions;

  if (!opts) {
    lines.push('Journey lookup failed — no results.');
    return lines;
  }

  if (opts.from && opts.to) {
    lines.push(`Route: ${opts.from} → ${opts.to}`);
    if (opts.date) lines.push(`Date: ${opts.date}`);
    lines.push('');
  }

  for (const opt of opts.options) {
    const durStr = opt.durationMinutes != null ? fmtDuration(opt.durationMinutes * 60000) : '—';
    const nTransfers = opt.numTransfers ?? opt.transfers?.length ?? 0;
    const pSuccess = opt.assessment?.reach?.pReaching;

    lines.push(`━━━ Option ${opt.index} ━━━━━━━━━━━━━━━━━━━━━━━━━`);
    lines.push(`Duration: ${durStr} | Transfers: ${nTransfers} | Success: ${pSuccess != null ? pct(pSuccess) : '—'}`);
    lines.push('');

    for (const leg of opt.legs) {
      if (leg.walking) {
        lines.push(`  Walk ${leg.distance ? leg.distance + 'm' : ''} → ${leg.destination || leg.to || '?'}`);
        continue;
      }
      const dep = leg.dep || '??:??';
      const arr = leg.arr || '??:??';
      const line = (leg.train || '?').padEnd(12);
      const plats = leg.platformDep || leg.platformArr
        ? `  [Pl.${leg.platformDep || '?'}→${leg.platformArr || '?'}]`
        : '';
      let delayStr = '';
      if (leg.depDelay && leg.depDelay > 0) delayStr = ` (+${leg.depDelay}min)`;
      if (leg.cancelled) delayStr = ' CANCELLED';
      lines.push(`  ${dep} → ${arr}  ${line} ${leg.from || '?'} → ${leg.to || '?'}${plats}${delayStr}`);
    }

    // Transfer details — from opt.transfers (array of transfer objects)
    const transferDetails = opt.transfers;
    if (transferDetails?.length) {
      lines.push('');
      lines.push('  Transfers:');
      for (const t of transferDetails) {
        if (t.cancelled || t.scheduledMinutes == null) {
          lines.push(`    🔴 CANCELLED at ${t.at || '?'} — 0.0% catch rate`);
          continue;
        }
        const risk = RISK[t.risk] || transferRisk(t.scheduledMinutes);
        const plat = t.platformFrom && t.platformTo && t.platformFrom !== t.platformTo
          ? ` (Pl.${t.platformFrom}→${t.platformTo})`
          : '';
        lines.push(`    ${risk.emoji} ${t.scheduledMinutes}min at ${t.at}${plat}${t.catchProb != null ? ` — ${pct(t.catchProb)} catch rate` : ''}`);
      }
    }

    // Disruptions / warnings per leg
    const disruptedLegs = opt.legs.filter(l => l.remarks?.length > 0);
    if (disruptedLegs.length) {
      lines.push('');
      lines.push('  Disruptions:');
      for (const leg of disruptedLegs) {
        for (const r of leg.remarks) {
          lines.push(`    ⚠ ${leg.train || '?'}: ${r.text || '?'}`);
        }
      }
    }

    lines.push('');
    const reach = opt.assessment?.reach;
    if (reach) {
      lines.push(`  All transfers: ${pct(reach.pAllTransfers)} | No cancellations: ${pct(reach.pNoCancellations)} | Overall: ${pct(reach.pReaching)}`);
    }
    lines.push('');
  }

  return lines;
}

function formatDepartures(env) {
  const lines = [];
  const d = env.departures;

  if (!d) {
    lines.push('Departures lookup failed — no data.');
    return lines;
  }

  lines.push(`${d.type === 'arrivals' ? 'Arrivals at' : 'Departures at'} ${d.station}:`);
  lines.push('');

  for (const entry of d.entries) {
    const planned = entry.time || '??:??';
    const delayMin = entry.delay || 0;
    const line = (entry.train || '?').padEnd(12);
    const dir = entry.destination || '?';
    const plat = entry.platform ? `Pl.${entry.platform}` : '';

    let timeStr;
    if (entry.cancelled) {
      timeStr = `${planned}  CANCELLED`;
    } else if (delayMin > 0) {
      timeStr = `${planned} (+${delayMin}min)`;
    } else {
      timeStr = planned;
    }

    lines.push(`  ${timeStr.padEnd(30)} ${line} → ${dir}  ${plat}`);
  }

  return lines;
}

function formatSearch(env) {
  const lines = [];
  const s = env.stations;

  if (!s) {
    lines.push('Search failed — no results.');
    return lines;
  }

  lines.push(`Stations matching "${s.query}":`);
  lines.push('');

  for (const st of s.results) {
    const transports = st.products?.length ? `  (${st.products.join(', ')})` : '';
    lines.push(`  ${st.eva}  ${st.name}${transports}`);
  }

  return lines;
}

function formatTrack(env) {
  const lines = [];
  const t = env.trackStatus || env.liveStatus;

  if (!t) {
    lines.push('Track lookup failed — no data.');
    return lines;
  }

  lines.push(`${t.train} | ${t.from} → ${t.to}`);
  lines.push('');

  if (t.stops?.length) {
    for (const stop of t.stops) {
      const marker = stop.isRealTime ? '*' : (stop.isCurrent ? '>' : ' ');
      const arrDelay = fmtDelay(stop.arrDelay).padEnd(8);
      const depDelay = fmtDelay(stop.depDelay);
      lines.push(`  ${marker} ${(stop.name || '?').padEnd(32)} arr: ${arrDelay}  dep: ${depDelay}`);
    }
  }

  if (t.delayReasons?.length) {
    lines.push(`  Delay reasons: ${t.delayReasons.join(', ')}`);
  }

  lines.push('');
  const maxDelayStr = fmtDelay(t.maxDelay);
  const zugbindung = (t.maxDelay ?? 0) >= 20 ? 'YES' : 'NO';
  lines.push(`Max delay: ${maxDelayStr} | Zugbindung: ${zugbindung}`);

  if (t.thresholdReached) {
    lines.push(`THRESHOLD REACHED: ${maxDelayStr}`);
  }

  return lines;
}

// ── public API ──────────────────────────────────────

export function formatText(envelope) {
  let lines;
  switch (envelope.mode) {
    case 'parse':      lines = formatParse(envelope); break;
    case 'live':       lines = formatLive(envelope); break;
    case 'journey':    lines = formatJourney(envelope); break;
    case 'departures': lines = formatDepartures(envelope); break;
    case 'search':     lines = formatSearch(envelope); break;
    case 'track':      lines = formatTrack(envelope); break;
    default:           lines = [`Unknown mode: ${envelope.mode}`];
  }
  appendFooter(lines, envelope);
  return lines.join('\n');
}

export function formatJson(envelope) {
  return JSON.stringify(envelope, null, 2);
}
