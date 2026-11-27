#!/usr/bin/env node
import { readAnalytics, setAnalytics } from './analytics.mjs';
import { firstRun } from './first-run.mjs';
import { writeFile, readFile } from 'node:fs/promises';
import { parseArgs } from 'node:util';
import { ImagenClient, readKey } from './client.mjs';
import { previewDemand, submitDemand } from './demand.mjs';
import { startPanel } from './panel.mjs';
import { searchMarkdown, placeImage, renderManifest, WATERMARK_NOTICE } from './markdown.mjs';

const [command, ...args] = process.argv.slice(2);
const string = { type: 'string' };
const flag = { type: 'boolean' };
const outputOptions = { out: string, format: string };
const originalOptions = { id: string, 'max-credits': string, 'operation-id': string };
const commandOptions = new Map(Object.entries({
  analytics: { keywords: string, confirm: flag },
  version: { check: flag },
  start: { query: string, ...outputOptions },
  search: {
    query: string, orientation: string, style: string, topic: string, 'use-case': string,
    composition: string, limit: string, page: string, ...outputOptions,
  },
  'demand-preview': { file: string },
  'demand-submit': { file: string, confirm: string },
  place: { id: string, manifest: string, slot: string, caption: string, placement: string, format: string },
  render: { manifest: string },
  detail: { id: string },
  status: {},
  'original-link': originalOptions,
  download: { ...originalOptions, out: string, original: flag },
  panel: { manifest: string, selection: string, open: flag },
  configure: { manifest: string, selection: string, open: flag },
}));

function boundedInteger(value, option, maximum, fallback) {
  if (value === undefined) return fallback;
  const number = Number(value);
  if (!/^\d+$/.test(value) || number < 1 || number > maximum) {
    throw new Error(`${option} 必须是 1 到 ${maximum} 之间的整数。`);
  }
  return number;
}

const orientations = new Map(Object.entries({
  landscape: 'landscape', 横图: 'landscape', 横版: 'landscape',
  portrait: 'portrait', 竖图: 'portrait', 竖版: 'portrait',
  square: 'square', 方图: 'square', 方形: 'square',
}));

const client = new ImagenClient();
try {
  if (command && command !== 'help' && command !== '--help' && !commandOptions.has(command)) {
    throw new Error(`未知命令 ${command}。运行 imagen.mjs help 查看用法。`);
  }
  const { values: options } = parseArgs({ args, options: commandOptions.get(command) || {} });
  if (options.format !== undefined && !['json', 'markdown'].includes(options.format)) {
    throw new Error('--format 支持 json 或 markdown。');
  }
  if (['search', 'start'].includes(command) && [...(options.query ?? '').trim()].length > 120) {
    throw new Error('--query 最多支持 120 个字符。');
  }
  let result;
  if (command === 'analytics') {
    if (options.keywords === 'on') {
      if (options.confirm !== true) throw new Error('Obtain explicit user consent, then use analytics --keywords on --confirm. Terms are stored for 30 days; no articles, conversations or keys.');
      result = await setAnalytics(true);
    } else if (options.keywords === 'off') result = await setAnalytics(false);
    else if (options.keywords) throw new Error('Use --keywords on or off.');
    else result = { record_keywords: await readAnalytics(), operational_metrics: true, retention_days: 30 };
  } else if (command === 'version') {
    const installed = JSON.parse(await readFile(new URL('../release.json', import.meta.url), 'utf8'));
    result = { ...installed, checked_online: false };
    if (options.check) {
      const response = await fetch('https://imagen.chat/downloads/imagen-search-release.json', { headers: { 'User-Agent': 'ImagenSearchSkill/1.1' }, redirect: 'error', signal: AbortSignal.timeout(20000) });
      if (!response.ok) throw new Error('Cannot check the latest version. Installed files were not changed.');
      const latest = await response.json();
      if (!/^\d+\.\d+\.\d+$/.test(latest.version)) throw new Error('Invalid release version. Installed files were not changed.');
      const a = installed.version.split('.').map(Number), b = latest.version.split('.').map(Number);
      const difference = b.map((n, i) => n - a[i]).find(n => n !== 0) || 0;
      result = { installed: installed.version, latest: latest.version, update_available: difference > 0, checked_online: true, changes: latest.changes, installation_guide: 'https://imagen.chat/install/imagen-search.md' };
    }
  } else if (command === 'start') {
    result = await firstRun(client, { query: options.query?.trim() || 'ancient Rome', out: options.out });
    if (options.format !== 'json') { console.log(result.markdown + '\n预览文件：' + result.preview + '\n图片清单：' + result.manifest); result = undefined; }
  } else if (command === 'demand-preview' || command === 'demand-submit') {
    if (!options.file) throw new Error('Provide --file with the minimal demand JSON.');
    result = command === 'demand-preview' ? await previewDemand(options.file) : await submitDemand(client, options.file, options.confirm);
  } else if (command === 'search') {
    const orientation = orientations.get(options.orientation);
    if (options.orientation !== undefined && !orientation) {
      throw new Error('--orientation 支持 landscape（横图）、portrait（竖图）或 square（方图）。');
    }
    const topic = options.topic?.trim();
    if (topic && (topic.length > 80 || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(topic))) {
      throw new Error('--topic 需要专题链接里的短名，例如 history-civilizations-events。');
    }
    for (const [name, limit] of [['style', 64], ['use-case', 64], ['composition', 32]]) {
      if ([...(options[name] ?? '').trim()].length > limit) {
        throw new Error(`--${name} 最多支持 ${limit} 个字符。`);
      }
    }
    result = await client.search({
      query: options.query?.trim() ?? '',
      orientation,
      style: options.style?.trim(),
      topic,
      use_case: options['use-case']?.trim(),
      composition: options.composition?.trim(),
      page_size: boundedInteger(options.limit, '--limit', 60, 12),
      page: boundedInteger(options.page, '--page', 10000, 1),
    });
    if (options.out) await writeFile(options.out, JSON.stringify(result, null, 2), { flag: 'wx' });
    if (options.format !== 'json') { console.log(searchMarkdown(result)); result = undefined; }
  } else if (command === 'place') {
    if (!options.manifest) throw new Error('Provide --manifest for stable document image numbers.');
    const detail = await client.detail(options.id);
    result = await placeImage(options.manifest, detail.asset, { ...(options.slot ? { slot: Number(options.slot) } : {}), caption: options.caption, placement: options.placement });
    if (options.format !== 'json') { console.log(result.markdown + '\n\n> ' + WATERMARK_NOTICE); result = undefined; }
  } else if (command === 'render') {
    if (!options.manifest) throw new Error('Provide --manifest.');
    console.log(await renderManifest(options.manifest));
  } else if (command === 'detail') result = await client.detail(options.id);
  else if (command === 'status') result = await readKey() ? { connected: true, ...await client.credits() } : { connected: false, mode: 'free-watermarked' };
  else if (command === 'original-link') {
    result = await client.originalLink(options.id, { maxCredits: Number(options['max-credits'] || 0), ...(options['operation-id'] ? { operationID: options['operation-id'] } : {}) });
  }
  else if (command === 'download') {
    if (!options.out) throw new Error('Provide --out with a new destination filename.');
    result = await client.download(options.id, options.out, { original: options.original === true, maxCredits: Number(options['max-credits'] || 0), ...(options['operation-id'] ? { operationID: options['operation-id'] } : {}) });
  } else if (command === 'panel' || command === 'configure') {
    const manifest = options.manifest ? JSON.parse(await readFile(options.manifest, 'utf8')) : { items: [] };
    const panel = await startPanel({ client, manifest, selectionFile: options.selection });
    console.log(JSON.stringify({ local_url: panel.url, selection_file: panel.selectionFile, instruction: 'Open local_url in the user browser. The local session expires after 30 minutes.' }));
    if (options.open) {
      const { spawn } = await import('node:child_process');
      const opener = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'explorer.exe' : 'xdg-open';
      const child = spawn(opener, [panel.url], { stdio: 'ignore' }); child.on('error', () => {}); child.unref();
    }
    process.on('SIGINT', () => panel.close());
  } else {
    result = { usage: ['analytics [--keywords on --confirm | --keywords off]', 'version [--check]', 'start --query \"ancient Rome\" --out NEW_WORKSPACE_FOLDER', 'demand-preview --file request.json', 'demand-submit --file request.json --confirm APPROVED_PAYLOAD_HASH', 'search --query "salt trade" --orientation landscape --limit 8 --out candidates.json', 'place --id PUBLIC_ID --manifest article-images.json --caption "Image caption" --placement "After paragraph 2"', 'place --id REPLACEMENT_ID --manifest article-images.json --slot 2', 'render --manifest article-images.json', 'search --query "salt trade" --format json', 'panel --manifest candidates.json --selection selected.json --open', 'configure --open', 'status', 'detail --id PUBLIC_ID', 'original-link --id PUBLIC_ID --max-credits 1 --operation-id STABLE_UUID', 'download --id PUBLIC_ID --out image.webp', 'download --id PUBLIC_ID --original --max-credits 1 --operation-id STABLE_UUID --out original.png'], requires: 'Node.js 22+' };
  }
  if (result) console.log(JSON.stringify(result, null, 2));
} catch (error) { console.error(error.message); process.exitCode = 1; }
