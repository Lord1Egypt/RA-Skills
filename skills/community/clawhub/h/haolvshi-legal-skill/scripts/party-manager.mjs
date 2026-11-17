import crypto from 'node:crypto';
import { SkillError } from './errors.mjs';

function pathParts(path) {
  return String(path)
    .replace(/\[(\d+)\]/g, '.$1')
    .split('.')
    .filter(Boolean);
}

export function getAtPath(target, path) {
  return pathParts(path).reduce((value, key) => value?.[key], target);
}

export function setAtPath(target, path, value) {
  const keys = pathParts(path);
  if (!keys.length) throw new SkillError('PATCH_PATH_REQUIRED', '更新字段时缺少字段路径');
  let cursor = target;
  keys.forEach((key, index) => {
    if (index === keys.length - 1) {
      cursor[key] = value;
      return;
    }
    const nextKey = keys[index + 1];
    if (cursor[key] === undefined || cursor[key] === null) {
      cursor[key] = /^\d+$/.test(nextKey) ? [] : {};
    }
    cursor = cursor[key];
  });
  return target;
}

export function applyPatches(params, patches = {}) {
  const next = structuredClone(params || {});
  for (const [path, value] of Object.entries(patches)) setAtPath(next, path, value);
  return next;
}

function resolveArray(params, collection) {
  const value = getAtPath(params, collection);
  if (value === undefined) {
    setAtPath(params, collection, []);
    return getAtPath(params, collection);
  }
  if (!Array.isArray(value)) {
    throw new SkillError('PARTY_COLLECTION_INVALID', `字段 ${collection} 不是可重复列表`);
  }
  return value;
}

export function applyPartyAction(params, action) {
  const next = structuredClone(params || {});
  const collection = action?.collection;
  if (!collection) throw new SkillError('PARTY_COLLECTION_REQUIRED', '当事人操作缺少列表名称');
  const parties = resolveArray(next, collection);

  if (action.type === 'add') {
    parties.push({ _clientId: crypto.randomUUID(), ...(action.value || {}) });
  } else if (action.type === 'update') {
    const index = Number(action.index);
    if (!Number.isInteger(index) || index < 0 || index >= parties.length) {
      throw new SkillError('PARTY_INDEX_INVALID', '需要修改的当事人序号不存在');
    }
    parties[index] = { ...parties[index], ...(action.value || {}) };
  } else if (action.type === 'remove') {
    const index = Number(action.index);
    if (!Number.isInteger(index) || index < 0 || index >= parties.length) {
      throw new SkillError('PARTY_INDEX_INVALID', '需要删除的当事人序号不存在');
    }
    parties.splice(index, 1);
  } else {
    throw new SkillError('PARTY_ACTION_INVALID', '当事人操作类型应为 add、update 或 remove');
  }
  return next;
}

const PARTY_COLLECTION = /(plaintiff|defendant|third|applicant|respondent|party|prosecutor|executed|claimant|obligated|guardian|agent|defender)/i;

export function summarizePleadingParams(params = {}) {
  const parties = [];
  const sections = [];
  for (const [key, value] of Object.entries(params)) {
    if (Array.isArray(value) && PARTY_COLLECTION.test(key)) {
      parties.push({ collection: key, count: value.length, items: value });
    } else if (value !== '' && value !== null && value !== undefined) {
      sections.push({ key, value });
    }
  }
  return { parties, filledFieldCount: sections.length, fields: sections };
}
