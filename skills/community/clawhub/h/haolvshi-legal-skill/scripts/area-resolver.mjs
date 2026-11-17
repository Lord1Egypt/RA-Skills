// 地区题（component 17，前端 QArea）的取值是地区 id，不是"云南省昆明市"这样的名称。
//
// 前端行为：从 area/getQuestionAllArea 拉全量地区（扁平结构 { id, name, parentId }），
// 用户在 config.areaLevel 指定的层级上逐级点选，最终把叶子节点的 id 写进 value。
// areaLevel = 1 只选到省，2 选到省市，3 选到省市区县。
//
// 技能这边没有点选界面，必须把宿主给出的名称文本解析成同一层级的 id；
// 解析不出来就把该层级的真实候选交还用户，绝不能把原文直接提交。

import { SkillError } from './errors.mjs';

const AREA_PATH = '/area/getQuestionAllArea';
const CACHE_TTL_MS = 60 * 60 * 1000;

let cache = null;

/** 去掉行政区划后缀和标点，让"云南"和"云南省"可以互相匹配。 */
function normalizeName(value) {
  return String(value || '')
    .replace(/\s+/g, '')
    .replace(/(省|市|自治区|特别行政区|自治州|地区|盟|区|县|旗|镇|街道)$/g, '')
    .toLowerCase();
}

/** 把用户写的"云南省昆明市五华区"拆成层级片段。 */
export function splitRegionText(text) {
  const source = String(text || '').trim();
  if (!source) return [];
  if (Array.isArray(text)) return text.map(item => String(item).trim()).filter(Boolean);

  const matched = source.match(
    /[一-龥]{2,15}?(?:省|自治区|特别行政区|自治州|地区|盟|市|区|县|旗)/g
  );
  if (matched && matched.length) return matched;
  return source.split(/[\s,，/>-]+/).filter(Boolean);
}

export function buildAreaIndex(list = []) {
  const byId = new Map();
  const childrenOf = new Map();
  for (const item of list) {
    const id = String(item.id);
    byId.set(id, { id, name: String(item.name || item.title || ''), parentId: item.parentId ? String(item.parentId) : null });
  }
  for (const area of byId.values()) {
    const key = area.parentId || '__root__';
    if (!childrenOf.has(key)) childrenOf.set(key, []);
    childrenOf.get(key).push(area);
  }
  return { byId, childrenOf };
}

export async function loadAreaIndex(api, config, { force = false } = {}) {
  if (!force && cache && Date.now() - cache.at < CACHE_TTL_MS) return cache.index;
  const data = await api.get(AREA_PATH, {
    query: { deviceType: config.deviceType, appId: config.appId }
  });
  const list = Array.isArray(data) ? data : (data?.list || data?.records || []);
  if (!list.length) throw new SkillError('AREA_CATALOG_EMPTY', '地区目录为空，无法匹配地区题答案');
  const index = buildAreaIndex(list);
  cache = { at: Date.now(), index };
  return index;
}

export function resetAreaCache() {
  cache = null;
}

/** config.areaLevel 缺省按省市两级处理，与前端 CAreaSelectAll 的默认表现一致。 */
export function areaLevelOf(node) {
  const level = Number(node?.config?.areaLevel);
  return Number.isInteger(level) && level >= 1 && level <= 3 ? level : 2;
}

function childrenOfLevel(index, parentId) {
  return index.childrenOf.get(parentId || '__root__') || [];
}

function matchOne(candidates, text) {
  const target = normalizeName(text);
  if (!target) return null;
  const exact = candidates.filter(area => normalizeName(area.name) === target);
  if (exact.length === 1) return exact[0];
  if (exact.length > 1) return null;
  const partial = candidates.filter(area => {
    const name = normalizeName(area.name);
    return name.includes(target) || target.includes(name);
  });
  return partial.length === 1 ? partial[0] : null;
}

function stripSuffix(name) {
  return String(name).replace(/(省|市|自治区|特别行政区|自治州|地区|盟|区|县|旗)$/g, '');
}

/**
 * 从文本开头吃掉一个地区名。用户常写"云南昆明"这种不带后缀的连写，
 * 按前缀逐级消费比先分词更稳，取最长匹配避免"市辖区"之类的短名抢先。
 */
function consumePrefix(text, candidates) {
  let best = null;
  for (const area of candidates) {
    for (const variant of [area.name, stripSuffix(area.name)]) {
      if (!variant) continue;
      if (text.startsWith(variant) && (!best || variant.length > best.matched.length)) {
        best = { area, matched: variant };
      }
    }
  }
  return best;
}

/**
 * 把地区文本解析成指定层级的地区 id。
 * 返回 { ok: true, id, path } 或 { ok: false, reason, level, candidates }，
 * 其中 candidates 是该层级真实存在的地区，供宿主交给用户选择。
 */
export function resolveAreaPath(index, text, level) {
  const segments = splitRegionText(text);
  let remaining = String(Array.isArray(text) ? text.join('') : text || '').replace(/\s+/g, '');
  const path = [];
  let parentId = null;

  for (let depth = 0; depth < level; depth += 1) {
    const candidates = childrenOfLevel(index, parentId);
    if (!candidates.length) break;

    // 先按前缀消费，消费不动时退回分词匹配。
    let matched = null;
    const consumed = consumePrefix(remaining, candidates);
    if (consumed) {
      matched = consumed.area;
      remaining = remaining.slice(consumed.matched.length);
    } else if (segments[depth] !== undefined) {
      matched = matchOne(candidates, segments[depth]);
    }

    if (!matched) {
      // 第一级就匹配不上时，可能是用户省略了上级（只写"杭州"）。
      if (depth === 0) {
        const unique = resolveByUniqueName(index, text, level);
        if (unique) return { ok: true, id: unique[unique.length - 1].id, path: unique };
      }
      const exhausted = !remaining && segments[depth] === undefined;
      return {
        ok: false,
        reason: exhausted ? 'INCOMPLETE' : 'NOT_MATCHED',
        level: depth + 1,
        segment: segments[depth],
        resolved: path,
        candidates
      };
    }
    path.push(matched);
    parentId = matched.id;
  }

  if (!path.length) return { ok: false, reason: 'EMPTY', level: 1, resolved: [], candidates: childrenOfLevel(index, null) };
  return { ok: true, id: path[path.length - 1].id, path };
}

/** 沿 parentId 回溯出 [省, 市, 区] 这样的完整路径。 */
function ancestorPath(index, area) {
  const path = [area];
  let current = area;
  while (current.parentId) {
    const parent = index.byId.get(current.parentId);
    if (!parent) break;
    path.unshift(parent);
    current = parent;
  }
  return path;
}

/**
 * 用户经常省掉上级，只写"杭州""浦东新区"。
 * 逐级匹配失败时在全表找唯一同名地区，深度正好等于要求层级才接受。
 */
function resolveByUniqueName(index, text, level) {
  const target = normalizeName(text);
  if (!target) return null;
  const matches = [];
  for (const area of index.byId.values()) {
    if (normalizeName(area.name) !== target) continue;
    const path = ancestorPath(index, area);
    if (path.length === level) matches.push(path);
  }
  return matches.length === 1 ? matches[0] : null;
}

/** 供交互层展示的精简候选，最多 60 条，避免把 4000 多个地区塞进上下文。 */
export function areaCandidateOptions(candidates, limit = 60) {
  return candidates.slice(0, limit).map(area => ({ value: area.id, label: area.name }));
}

/**
 * 解析一批地区题答案。已经是合法地区 id 的直接放行，
 * 其余按名称解析；解析失败的集中抛出，附带该层级的真实候选。
 */
export async function resolveAreaAnswers({ api, config, nodes, answers }) {
  const pending = nodes.filter(entry => answers[entry.key] !== undefined && answers[entry.key] !== '');
  if (!pending.length) return { answers, resolved: [] };

  const index = await loadAreaIndex(api, config);
  const next = { ...answers };
  const resolved = [];
  const failures = [];

  for (const entry of pending) {
    const raw = answers[entry.key];
    if (typeof raw === 'string' && index.byId.has(raw)) {
      resolved.push({ key: entry.key, id: raw, name: index.byId.get(raw).name });
      continue;
    }
    const level = areaLevelOf(entry.node);
    const outcome = resolveAreaPath(index, raw, level);
    if (outcome.ok) {
      next[entry.key] = outcome.id;
      resolved.push({ key: entry.key, id: outcome.id, name: outcome.path.map(area => area.name).join('') });
      continue;
    }
    failures.push({ key: entry.key, label: entry.label, level, raw, outcome });
  }

  if (failures.length) {
    const first = failures[0];
    const levelName = ['省或直辖市', '市或自治州', '区或县'][first.level - 1] || '地区';
    throw new SkillError(
      'AREA_NOT_MATCHED',
      `地区题“${first.label}”需要选到第 ${first.level} 级（${levelName}），`
        + `提交的“${first.raw}”无法匹配。请把候选交给用户确认后，用候选中的 id 重新提交。`,
      {
        details: failures.map(item => ({
          key: item.key,
          label: item.label,
          areaLevel: item.level,
          needLevel: item.outcome.level,
          submitted: item.raw,
          resolvedPath: (item.outcome.resolved || []).map(area => area.name),
          candidates: areaCandidateOptions(item.outcome.candidates || [])
        }))
      }
    );
  }

  return { answers: next, resolved };
}
