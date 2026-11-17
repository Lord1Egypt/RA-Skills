// official-sources.mjs — 政务/官方数据源登记表（templates/official-sources.<market>.yml）的共享解析层。
// 零依赖行级解析（扁平两缩进结构，无需 YAML 库）；scan / doctor / selftest 共用同一套解析器与枚举断言。

import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { SOURCE_GRANULARITIES } from '../../scrapers/_fields.mjs';

export const REGISTRY_FILE_RE = /^official-sources\.([a-z0-9_-]+)\.yml$/;

// 行级解析单份登记表（条目起始行支持 `- city: …` 与 `- market: …` 两种惯例）
export function parseRegistryText(text, marketFromFile) {
  const entries = [];
  let cur = null;
  for (const line of String(text ?? '').split('\n')) {
    const start = /^\s*-\s+(city|market):\s*(.+?)\s*$/.exec(line);
    if (start) {
      const [, key, raw] = start;
      const val = raw.replace(/^["']|["']$/g, '');
      cur = { market: marketFromFile, registry: marketFromFile };
      if (key === 'market') cur.market = val;
      else cur.city = val;
      entries.push(cur);
      continue;
    }
    if (!cur) continue;
    const kv = /^\s+([a-z_]+):\s*(.*?)\s*$/.exec(line);
    if (!kv) continue;
    if (kv[1] === 'city' && cur.city !== undefined) continue; // CN 惯例：city 由起始行给出，不重复覆盖
    const inline = /^\[(.*)\]\s*$/.exec(kv[2]);
    const value = inline
      ? inline[1].split(',').map((s) => s.trim()).filter(Boolean)
      : kv[2].replace(/^["']|["']$/g, '');
    cur[kv[1]] = Array.isArray(value) && kv[1] === 'market' ? value.join(',') : value;
  }
  return entries;
}

export async function readOfficialSources(root) {
  const tplDir = join(root, 'templates');
  const files = (await readdir(tplDir).catch(() => []))
    .filter((f) => REGISTRY_FILE_RE.test(f))
    .sort();
  const out = [];
  for (const f of files) {
    const market = REGISTRY_FILE_RE.exec(f)[1];
    const text = await readFile(join(tplDir, f), 'utf8').catch(() => '');
    for (const e of parseRegistryText(text, market)) out.push({ ...e, _file: f });
  }
  return { files, entries: out };
}

export function filterSources(entries, { query, market } = {}) {
  let list = entries ?? [];
  if (market) {
    const m = String(market).toLowerCase();
    list = list.filter((e) =>
      String(e.market ?? '').toLowerCase() === m || String(e.registry ?? '').toLowerCase() === m);
  }
  if (query) {
    const q = String(query).toLowerCase();
    list = list.filter((e) => Object.values(e).some((v) => {
      const parts = Array.isArray(v) ? v : [v];
      return parts.some((p) => String(p ?? '').toLowerCase().includes(q));
    }));
  }
  return list.map(({ _file, ...rest }) => rest);
}

// 枚举自一致：granularity 的每个取值都必须落在 SOURCE_GRANULARITIES 原子档内。
// 返回 { files, checked, bad } —— bad 非空即登记表漂移（doctor 报 ⛔ 阻塞）。
export async function checkGranularity(root) {
  const { files, entries } = await readOfficialSources(root);
  const bad = [];
  let checked = 0;
  for (const e of entries) {
    const raw = e.granularity;
    if (raw == null || raw === '') continue;
    const tokens = Array.isArray(raw) ? raw : String(raw).split('/').map((s) => s.trim()).filter(Boolean);
    checked++;
    const unknown = tokens.filter((t) => !SOURCE_GRANULARITIES.includes(t));
    if (unknown.length) bad.push({ file: e._file, city: e.city ?? e.market ?? '?', value: raw, unknown });
  }
  return { files, checked, bad };
}
