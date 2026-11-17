import { cp, mkdir, readdir, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { SkillError, fail, parseArgs } from './lib/api.mjs';

export async function scaffold(language, destination) {
  if (!['javascript', 'python'].includes(language)) throw new SkillError('--language must be javascript or python.');
  if (!destination || destination.trim() === '') throw new SkillError('Supply --out with a new project directory.');
  const out = resolve(destination);
  const source = fileURLToPath(new URL(`../assets/${language}/`, import.meta.url));
  // Validate the source before creating the target. Never read runtime environment files.
  const files = await readdir(source);
  if (!files.length) throw new SkillError('The starter assets are missing. Reinstall the complete skill folder.');
  try { await mkdir(out); } catch (error) {
    if (error.code === 'EEXIST') throw new SkillError('The output path already exists. Choose a new directory; existing projects are never overwritten.');
    throw new SkillError('Cannot create the output directory. Check that its parent exists and is writable.');
  }
  for (const name of files) await cp(join(source, name), join(out, name), { recursive: true, errorOnExist: true, force: false });
  await writeFile(join(out, '.gitignore'), '.env\n.env.*\n!.env.example\n__pycache__/\n.venv/\n', { flag: 'wx' });
  return { language, directory: out, files: [...files, '.gitignore'], network_requests: 0, credentials_written: false };
}

export async function main(argv = process.argv.slice(2)) {
  const { command, options } = parseArgs(argv, ['language', 'out']);
  if (options.help) { console.log('Odds API Integration Builder\n\nnode scaffold.mjs --language javascript|python --out NEW_DIRECTORY\n\nRequires Node.js 22+. Offline: no API key, package installation, or network access.\nRefuses existing targets. The generated client reads ODDS_API_KEY only at runtime.'); return; }
  if (command) throw new SkillError('Use --language and --out. There is no positional command.');
  console.log(JSON.stringify(await scaffold(options.language, options.out), null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch(fail);
