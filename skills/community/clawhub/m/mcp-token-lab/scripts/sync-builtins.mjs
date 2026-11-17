#!/usr/bin/env node
// Package web scenarios as standalone Skill examples using the app's importer.
import { mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const usage = 'Usage: node sync-builtins.mjs --repo <repo-root> [--check]';
try {
  let repo, check = false;
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--repo' && !repo && args[i + 1] && !args[i + 1].startsWith('--')) repo = resolve(args[++i]);
    else if (args[i] === '--check') check = true;
    else throw new Error(usage);
  }
  if (!repo) throw new Error(usage);
  const source = resolve(repo, 'src/config/default-template');
  const target = fileURLToPath(new URL('../assets/examples/', import.meta.url));
  const { readTemplate } = await import(pathToFileURL(resolve(repo, 'src/templates.js')).href);
  const files = (await readdir(source, { recursive: true })).filter(file => file.endsWith('.json')).sort();
  if (!files.length) throw new Error('No built-in templates found');
  // Read and normalize every source before changing the packaged examples.
  const expected = new Map(await Promise.all(files.map(async file => {
    const data = JSON.parse(await readFile(resolve(source, file), 'utf8'));
    const name = file.replace(/\.json$/, '').split(/[\\/]/).at(-1).slice(0, 100);
    return [file, JSON.stringify(readTemplate(data, name), null, 2) + '\n'];
  })));
  const existing = await readdir(target, { recursive: true }).catch(error => {
    if (error.code === 'ENOENT') return [];
    throw error;
  });
  const stale = existing.filter(file => file.endsWith('.json') && !expected.has(file));
  const changed = [];
  for (const [file, content] of expected) {
    const path = resolve(target, file);
    const current = await readFile(path, 'utf8').catch(error => {
      if (error.code === 'ENOENT') return null;
      throw error;
    });
    if (current === content) continue;
    changed.push(file);
    if (!check) {
      await mkdir(dirname(path), { recursive: true });
      await writeFile(path, content);
    }
  }
  if (check && (changed.length || stale.length)) {
    throw new Error('Packaged examples are out of sync. Run the sync command. Differences: ' + [...changed, ...stale].join(', '));
  }
  if (!check) for (const file of stale) await rm(resolve(target, file));
  console.log(JSON.stringify({ checked: check, examples: expected.size, updated: changed.length, removed: stale.length }));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
