import { readFile, writeFile, rename, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { validateID } from './client.mjs';

function text(value) { return String(value || '').replace(/[\r\n]+/g, ' ').replace(/[\\`*_{}\[\]<>|]/g, '\\$&'); }
function preview(asset) {
  validateID(asset.public_id);
  const url = new URL(asset.preview?.url);
  if (url.protocol !== 'https:' || url.hostname !== 'cdn.imagen.chat' || url.username || url.password) throw new Error('Expected a public Imagen watermarked preview.');
  return url.href;
}
function source(asset) { return `https://imagen.chat/en/images/${encodeURIComponent(asset.slug)}--${asset.public_id}`; }
export function imageMarkdown(item) {
  const label = `图 ${item.slot}`;
  return `**${label}｜${text(item.caption || item.title)}**\n\n![${label}：${text(item.caption || item.title)}](<${item.url}>)\n\n*${label} · AI 配图 · 带水印 · [Imagen 来源](<${item.detail_url}>)*`;
}
export const WATERMARK_NOTICE = '以上为免费水印图链接，可直接引用或按需下载。部分终端或聊天客户端可能无法显示网络图片；可使用已下载的本地素材查看，或在支持远程图片的网页及 Markdown 渲染器中使用。显示效果取决于客户端与网络环境。';
export const NO_SEARCH_RESULTS = '没有找到合适的图片。可以试试缩短关键词、换个中英文同义词，或减少筛选条件。';
export function searchMarkdown(result) {
  const page = result.page_info;
  if (!result.items.length) {
    if (page?.total > 0 && page.page > page.total_pages) {
      return `第 ${page.page} 页超出范围。共 ${page.total} 张，${page.total_pages} 页。请用 \`--page ${page.total_pages}\` 或更小的页码重试。`;
    }
    return NO_SEARCH_RESULTS;
  }
  const summary = page ? `第 ${page.page}/${page.total_pages} 页，共 ${page.total} 张。` : '';
  const next = page?.has_next ? `用 \`--page ${page.page + 1}\` 查看下一页。` : '';
  const candidates = result.items.map(asset => {
    const label = `候选 ${asset.public_id.slice(0, 8)}`;
    return `**${label}｜${text(asset.title)}**\n\n![${label}：${text(asset.title)}](<${preview(asset)}>)\n\n[查看来源](<${source(asset)}>) · public_id: \`${asset.public_id}\``;
  });
  return [summary + next, ...candidates, '> ' + WATERMARK_NOTICE].filter(Boolean).join('\n\n');
}
export async function readManifest(file) {
  try {
    const value = JSON.parse(await readFile(file, 'utf8'));
    if (value.version !== 1 || !Array.isArray(value.images) || value.images.some(item => !Number.isSafeInteger(item.slot) || item.slot < 1) || new Set(value.images.map(item => item.slot)).size !== value.images.length) throw new Error('Invalid manifest');
    return value;
  } catch (error) {
    if (error.code === 'ENOENT') return { version: 1, images: [] };
    throw new Error('Cannot read the illustration manifest. Preserve it and use a valid manifest.');
  }
}
// Serialize writes for the same document. Slot numbers identify placements, not assets.
export async function placeImage(file, asset, { slot, caption, placement } = {}) {
  const absolute = path.resolve(file);
  const manifest = await readManifest(absolute);
  if (slot === undefined) slot = Math.max(0, ...manifest.images.map(item => item.slot)) + 1;
  if (!Number.isSafeInteger(slot) || slot < 1) throw new Error('Image slot must be a positive integer.');
  const existing = manifest.images.find(item => item.slot === slot);
  const item = { slot, public_id: asset.public_id, title: asset.title, caption: caption ?? existing?.caption ?? asset.title, placement: placement ?? existing?.placement ?? '', url: preview(asset), detail_url: source(asset), watermarked: true, revision: (existing?.revision || 0) + 1, history: existing ? [...(existing.history || []), { public_id: existing.public_id, url: existing.url, revision: existing.revision }] : [] };
  manifest.images = [...manifest.images.filter(item => item.slot !== slot), item].sort((a,b) => a.slot-b.slot);
  await mkdir(path.dirname(absolute), { recursive: true });
  const temporary = `${absolute}.${randomUUID()}.tmp`;
  await writeFile(temporary, JSON.stringify(manifest, null, 2), { mode: 0o600, flag: 'wx' });
  await rename(temporary, absolute);
  return { ...item, markdown: imageMarkdown(item), manifest: absolute };
}
export async function renderManifest(file) {
  const manifest = await readManifest(file);
  return manifest.images.map(imageMarkdown).join('\n\n') + (manifest.images.length ? '\n\n> ' + WATERMARK_NOTICE : '');
}
