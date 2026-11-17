// lib/geo.mjs — 地理编码缓存读写
// 规范：零依赖。缓存命中与否由 map.mjs 决定；geocode 实际由页面前端完成（ADR 化的死适配器已删）。

import { readFile, writeFile } from 'node:fs/promises';

/**
 * 读取本地地理编码缓存
 */
export async function loadGeoCache(cachePath) {
  try {
    const raw = await readFile(cachePath, 'utf8');
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

/**
 * 保存地理编码缓存
 */
export async function saveGeoCache(cachePath, cache) {
  try {
    await writeFile(cachePath, JSON.stringify(cache, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('保存地理编码缓存失败:', err.message);
    return false;
  }
}
