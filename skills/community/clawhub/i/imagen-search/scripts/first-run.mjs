import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { placeImage, renderManifest } from './markdown.mjs';

export async function firstRun(client, { query = 'ancient Rome', out } = {}) {
  if (!out || typeof out !== 'string') throw new Error('Provide --out with a new workspace folder for your first search.');
  const result = await client.search({ query, page_size: 3, page: 1 });
  if (!result.items?.length) throw new Error('没有找到相关素材。请换一个更具体的关键词后重试；尚未创建预览目录。');
  const directory = path.resolve(out);
  await mkdir(directory); // Exclusive: never overwrite an existing preview or project.
  await writeFile(path.join(directory, 'candidates.json'), JSON.stringify(result, null, 2), { flag: 'wx' });
  const manifest = path.join(directory, 'images.json');
  for (const asset of result.items.slice(0, 3)) await placeImage(manifest, asset);
  const markdown = '# 第一次搜图\n\n以下是检索候选，尚未经过视觉适配判断，请根据内容选择。\n\n' + await renderManifest(manifest) + '\n\n接下来可以说：“图 2 换成修建水渠的场景，其他编号保持不变。”\n';
  const preview = path.join(directory, 'preview.md');
  await writeFile(preview, markdown, { flag: 'wx' });
  return { directory, manifest, preview, markdown };
}
