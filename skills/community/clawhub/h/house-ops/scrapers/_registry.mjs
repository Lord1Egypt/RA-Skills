// _registry.mjs — 平台模块的加载与路由（career-ops providers 模式）。
// 目录约定：scrapers/ 下每个非 `_` 前缀的 .mjs 是一个平台模块；`_` 前缀是共享工具，
// 永远不会被当作平台加载。模块按文件名字母序加载，detect() 优先级因此确定。

import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

/**
 * 把目录里所有平台模块加载成 id→module 的 Map。
 * 坏模块（形状不对、id 重复、import 报错）打警告并跳过，绝不 fatal。
 * @param {string} dir - scrapers 目录绝对路径。
 * @returns {Promise<Map<string, object>>}
 */
export async function loadScrapers(dir) {
  const scrapers = new Map();
  if (!existsSync(dir)) return scrapers;
  const entries = readdirSync(dir)
    .filter((f) => f.endsWith('.mjs') && !f.startsWith('_'))
    .sort();
  for (const file of entries) {
    let mod;
    try {
      mod = await import(pathToFileURL(path.join(dir, file)).href);
    } catch (err) {
      console.error(`⚠️  ${file}: 加载失败 — ${err.message}`);
      continue;
    }
    const s = mod.default;
    if (!s || !s.id || typeof s.detect !== 'function') {
      console.error(`⚠️  ${file}: 跳过 — default export 需为 { id, detect }`);
      continue;
    }
    if (scrapers.has(s.id)) {
      console.error(`⚠️  ${file}: 平台 id "${s.id}" 重复 — 保留首个`);
      continue;
    }
    scrapers.set(s.id, s);
  }
  return scrapers;
}

/**
 * 移动端子域（m.）的 URL 把城市码放在路径首段：m.ke.com/sh/ershoufang/x → sh。
 * 返回 [cityCode, path]（非移动端原样返回）。
 */
export function liftMobileCity(cityCode, path) {
  if (!/^m$/i.test(cityCode ?? '') || !path) return [cityCode, path];
  const seg = path.split('/');
  if (seg.length > 1 && /^[a-z]{2,12}$/i.test(seg[0])) return [seg[0], seg.slice(1).join('/')];
  return [cityCode, path];
}

/**
 * 按加载顺序依次跑各平台 detect(url)，首个命中的胜出。
 * @param {string} url
 * @param {Map<string, object>} scrapers - loadScrapers() 的返回值。
 * @returns {{ scraper: object, hit: object } | null} 都不命中时返回 null（调用方走 generic 清单）。
 */
export function detectPlatform(url, scrapers) {
  for (const scraper of scrapers.values()) {
    let hit;
    try {
      hit = scraper.detect(url);
    } catch (err) {
      console.error(`⚠️  ${scraper.id}: detect() 异常 — ${err.message}`);
      continue;
    }
    if (hit) return { scraper, hit };
  }
  return null;
}
