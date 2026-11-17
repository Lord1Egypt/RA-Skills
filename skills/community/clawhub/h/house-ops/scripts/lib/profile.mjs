// lib/profile.mjs — config/profile.yml 的保真解析与安全更新
// 规范：零依赖。严格保护用户的注释、缩进与未修改字段。
// PROFILE_FIELDS 是字段契约唯一声明：parse/update（本文件）与地图页表单（经 map-html 注入
// PROFILE_FIELDS 表驱动收集/回填）都从这一张表派生，新增画像键只改这里。

/**
 * 字段契约表。
 * kind: scalar(字符串) | number(数字，缺失→null/默认) | numberOrNull(数字或显式 null)
 *       | array2(二元区间 [min,max]) | bool
 * form: 地图页表单 input id（无 form = 仅 API/YAML 层字段，页面不收集）
 */
export const PROFILE_FIELDS = [
  // 市场段：多市场支持（cn / uk / ie / fr / nl / de / es）。无 form = 仅 API/YAML 层字段，
  // 地图页表单不收集（市场由 intake 对话确定，不在地图上改）。
  { section: 'market', key: 'code', kind: 'scalar' },
  { section: 'market', key: 'country', kind: 'scalar' },
  { section: 'market', key: 'city_local', kind: 'scalar' },
  { section: 'market', key: 'currency', kind: 'scalar' },
  { section: 'market', key: 'price_scale', kind: 'scalar' },
  { section: 'market', key: 'area_unit', kind: 'scalar' },
  { section: 'market', key: 'buyer_class', kind: 'scalar' },
  { section: 'market', key: 'residency_status', kind: 'scalar' },
  { section: 'market', key: 'tenure_preference', kind: 'scalar' },
  { section: 'market', key: 'min_lease_years', kind: 'numberOrNull' },
  { section: 'buyer', key: 'city', kind: 'scalar' },
  { section: 'buyer', key: 'work_location', kind: 'scalar', form: 'p-work-location' },
  { section: 'buyer', key: 'work_location_coords', kind: 'array2' },
  { section: 'buyer', key: 'commute_max_minutes', kind: 'numberOrNull', form: 'p-commute-minutes' },
  { section: 'budget', key: 'total_range_wan', kind: 'array2', form: ['p-price-min', 'p-price-max'] },
  { section: 'budget', key: 'walk_away_wan', kind: 'number', form: 'p-price-walkaway' },
  { section: 'budget', key: 'payment', kind: 'scalar' },
  { section: 'budget', key: 'loan_type', kind: 'scalar' },
  { section: 'preferences', key: 'layout', kind: 'scalar', form: 'p-layout' },
  { section: 'preferences', key: 'size_range_sqm', kind: 'array2', form: ['p-area-min', 'p-area-max'] },
  { section: 'preferences', key: 'building_age_max', kind: 'number' },
  { section: 'preferences', key: 'elevator_required', kind: 'bool' },
  { section: 'thresholds', key: 'deep_dive_min', kind: 'number', default: 4.0, form: 'p-threshold-deep' },
  { section: 'thresholds', key: 'give_up_below', kind: 'number', default: 3.5, form: 'p-threshold-giveup' },
];

const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

function parseField(text, f) {
  if (f.kind === 'array2') {
    const m = new RegExp(`^ {2}${f.key}:\\s*\\[(.*?)\\]`, 'm').exec(text);
    if (!m) return null;
    const items = m[1].split(',').map(s => Number(s.trim())).filter(n => !Number.isNaN(n));
    return items.length >= 2 ? [items[0], items[1]] : null;
  }
  const m = new RegExp(`^ {2}${f.key}:\\s*([^\\n]+)`, 'm').exec(text);
  if (!m) return f.default ?? null;
  const clean = m[1].replace(/\s+#.*$/, '').trim();
  if (!clean) return f.default ?? null;
  if (f.kind === 'scalar') return clean;
  if (f.kind === 'bool') return clean === 'true' ? true : clean === 'false' ? false : null;
  if (clean === 'null') return f.default ?? null;
  const n = Number(clean);
  return Number.isFinite(n) ? n : (f.default ?? null);
}

/**
 * 提取 profile 全部契约字段，按 section 嵌套返回（缺失键为 null，阈值带默认值）
 */
export function parseProfile(yamlText) {
  if (!yamlText) return null;
  const out = {};
  for (const f of PROFILE_FIELDS) {
    const section = (out[f.section] ??= {});
    section[f.key] = parseField(yamlText, f);
  }
  return out;
}

function fieldLineRe(f) {
  const k = escRe(f.key);
  if (f.kind === 'array2') {
    return new RegExp(`(^ {2}${k}:\\s*\\[)(.*?)(\\])([^#\\n]*?)(\\s*(?:#.*)?)$`, 'm');
  }
  return new RegExp(`(^ {2}${k}:\\s*)([^#\\n]*?)(\\s*(?:#.*)?)$`, 'm');
}

function serialize(f, v) {
  if (f.kind === 'array2') return `${v?.[0] ?? ''}, ${v?.[1] ?? ''}`;
  if (f.kind === 'bool') return v ? 'true' : 'false';
  if (f.kind === 'number' || f.kind === 'numberOrNull') {
    return (v === null || v === undefined || v === '') ? 'null' : String(v);
  }
  return String(v ?? '');
}

/**
 * 安全且保留注释地更新契约字段。
 * @returns {{ text: string, applied: string[], missing: string[], unknown: string[] }}
 *   applied: 成功替换的字段（section.key）；missing: YAML 中无对应行（显式失败，不再静默跳过）；
 *   unknown: patch 里不在 PROFILE_FIELDS 契约中的键。
 */
export function updateProfileFields(originalYaml, patch = {}) {
  let text = originalYaml ?? '';
  const applied = [], missing = [], unknown = [];

  for (const f of PROFILE_FIELDS) {
    const sectionPatch = patch[f.section];
    if (!sectionPatch || sectionPatch[f.key] === undefined) continue;
    const re = fieldLineRe(f);
    if (!re.test(text)) {
      missing.push(`${f.section}.${f.key}`);
      continue;
    }
    const value = serialize(f, sectionPatch[f.key]);
    text = f.kind === 'array2'
      ? text.replace(re, (_m, p1, _p2, p3, _p4, p5) => p1 + value + p3 + p5)
      : text.replace(re, (_m, p1, _p2, p3) => p1 + value + p3);
    applied.push(`${f.section}.${f.key}`);
  }

  for (const [section, fields] of Object.entries(patch)) {
    for (const key of Object.keys(fields ?? {})) {
      if (!PROFILE_FIELDS.some(f => f.section === section && f.key === key)) {
        unknown.push(`${section}.${key}`);
      }
    }
  }

  return { text, applied, missing, unknown };
}
