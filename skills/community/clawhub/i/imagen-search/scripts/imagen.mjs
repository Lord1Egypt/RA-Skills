#!/usr/bin/env node
import { firstRun } from './first-run.mjs';
import { writeFile, readFile } from 'node:fs/promises';
import { ImagenClient, readKey } from './client.mjs';
import { previewDemand, submitDemand } from './demand.mjs';
import { startPanel } from './panel.mjs';
import { searchMarkdown, placeImage, renderManifest, WATERMARK_NOTICE } from './markdown.mjs';

const [command, ...args] = process.argv.slice(2);
const options = {};
for (let i = 0; i < args.length; i++) {
  if (!args[i].startsWith('--')) throw new Error('Use named --options.');
  const name = args[i].slice(2);
  options[name] = args[i+1] && !args[i+1].startsWith('--') ? args[++i] : true;
}
const client = new ImagenClient();
try {
  let result;
  if (command === 'version') {
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
    result = await firstRun(client, { query: options.query || 'ancient Rome', out: options.out });
    if (options.format !== 'json') { console.log(result.markdown + '\n预览文件：' + result.preview + '\n图片清单：' + result.manifest); result = undefined; }
  } else if (command === 'demand-preview' || command === 'demand-submit') {
    if (!options.file) throw new Error('Provide --file with the minimal demand JSON.');
    result = command === 'demand-preview' ? await previewDemand(options.file) : await submitDemand(client, options.file, options.confirm);
  } else if (command === 'search') {
    result = await client.search({ query: options.query || '', orientation: options.orientation, style: options.style, topic: options.topic, use_case: options['use-case'], composition: options.composition, page_size: options.limit || 12, page: options.page || 1 });
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
    result = { usage: ['version [--check]', 'start --query \"ancient Rome\" --out NEW_WORKSPACE_FOLDER', 'demand-preview --file request.json', 'demand-submit --file request.json --confirm APPROVED_PAYLOAD_HASH', 'search --query "salt trade" --orientation landscape --limit 8 --out candidates.json', 'place --id PUBLIC_ID --manifest article-images.json --caption "Image caption" --placement "After paragraph 2"', 'place --id REPLACEMENT_ID --manifest article-images.json --slot 2', 'render --manifest article-images.json', 'search --query "salt trade" --format json', 'panel --manifest candidates.json --selection selected.json --open', 'configure --open', 'status', 'detail --id PUBLIC_ID', 'original-link --id PUBLIC_ID --max-credits 1 --operation-id STABLE_UUID', 'download --id PUBLIC_ID --out image.webp', 'download --id PUBLIC_ID --original --max-credits 1 --operation-id STABLE_UUID --out original.png'], requires: 'Node.js 22+' };
  }
  if (result) console.log(JSON.stringify(result, null, 2));
} catch (error) { console.error(error.message); process.exitCode = 1; }
