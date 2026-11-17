#!/usr/bin/env node
// Render a voice-tagged chapter to one MP3 with edge-tts.
// Usage: node narrate.js <slug> <number> [--out chapter3.mp3] [--rate -5%] [--pitch -2Hz] [--gap 0.4] [--dry-run] [--keep]
//
// Voice resolution, per tag, first hit wins:
//   1. the registered character's voice
//   2. NARRATOR's voice
//   3. the first edge-tts voice for the book's language
// Every fallback is printed before rendering so it never happens silently.

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { readKey } = require('./key');

const API = 'https://www.latentpress.com/api';
const VOICE_TAG = /^\[([A-Z_]+)\]$/;
const INLINE_TAG = /\[[A-Z_]+\]\s*/g;
const NARRATOR = 'NARRATOR';

const USAGE = `Usage: node narrate.js <slug> <number> [options]

Options:
  --out <file>     Output MP3 (default: chapter<number>.mp3 in the current directory)
  --rate <value>   edge-tts rate for every segment, e.g. -10% (default +0%)
  --pitch <value>  edge-tts pitch for every segment, e.g. -2Hz (default +0Hz)
  --gap <seconds>  Silence between speaker changes (default 0.4, needs ffmpeg)
  --dry-run        Print the cast and segment plan, render nothing
  --keep           Keep the per-segment work directory after a successful render`;

async function get(pathname) {
  const res = await fetch(`${API}${pathname}`, { headers: { Authorization: `Bearer ${readKey({ quiet: true })}` } });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    console.error(`Error ${res.status} on ${pathname}:`, data.error || data);
    process.exit(1);
  }
  return data;
}

function parseArgs(args) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--dry-run' || args[i] === '--keep') flags[args[i].slice(2)] = true;
    else if (args[i].startsWith('--') && i + 1 < args.length) flags[args[i].slice(2)] = args[++i];
    else positional.push(args[i]);
  }
  return { flags, positional };
}

function has(bin) {
  return spawnSync('which', [bin]).status === 0;
}

function listVoices() {
  const out = spawnSync('edge-tts', ['--list-voices'], { encoding: 'utf8' });
  if (out.status !== 0) {
    console.error('edge-tts --list-voices failed. Install it with: pip install "edge-tts==7.2.8"');
    process.exit(1);
  }
  return out.stdout.split('\n').slice(2).map((l) => l.trim().split(/\s+/)[0]).filter((id) => /^[a-z]{2,3}-/.test(id));
}

function defaultVoiceFor(language, voices) {
  const lang = language.toLowerCase();
  const base = lang.split('-')[0];
  return (
    voices.find((id) => id.toLowerCase().startsWith(`${lang}-`)) ||
    voices.find((id) => id.toLowerCase().startsWith(`${base}-`)) ||
    null
  );
}

function segment(content) {
  const segments = [];
  let tag = NARRATOR;
  let buffer = [];
  const flush = () => {
    const text = buffer.join('\n').replace(INLINE_TAG, '').trim();
    if (text) segments.push({ tag, text });
    buffer = [];
  };
  for (const raw of content.split('\n')) {
    const line = raw.trim();
    const match = VOICE_TAG.exec(line);
    if (match) {
      flush();
      tag = match[1];
    } else {
      buffer.push(raw);
    }
  }
  flush();
  return segments;
}

function castFor(tags, characters, language, voices) {
  const byName = new Map(characters.map((c) => [c.name, c]));
  const narratorVoice = byName.get(NARRATOR)?.voice || null;
  const languageVoice = defaultVoiceFor(language, voices);
  const cast = new Map();
  for (const tag of tags) {
    const own = byName.get(tag)?.voice || null;
    if (own) cast.set(tag, { voice: own, source: 'registered' });
    else if (narratorVoice) cast.set(tag, { voice: narratorVoice, source: byName.has(tag) ? `no voice set, using ${NARRATOR}` : `unregistered, using ${NARRATOR}` });
    else if (languageVoice) cast.set(tag, { voice: languageVoice, source: `no ${NARRATOR} voice, using first ${language} voice` });
    else {
      console.error(`No voice for [${tag}], no ${NARRATOR} voice, and no edge-tts voice for language "${language}". Register a NARRATOR with a voice first.`);
      process.exit(1);
    }
  }
  for (const [tag, { voice }] of cast) {
    if (!voices.includes(voice)) {
      console.error(`[${tag}] is mapped to "${voice}", which is not an edge-tts voice. Fix it with add-character.`);
      process.exit(1);
    }
  }
  return cast;
}

function run(bin, args) {
  const out = spawnSync(bin, args, { encoding: 'utf8' });
  if (out.status !== 0) {
    console.error(`${bin} ${args.join(' ')}\n${out.stderr || out.stdout}`);
    process.exit(1);
  }
}

function render(segments, cast, flags, workDir) {
  const rate = flags.rate || '+0%';
  const pitch = flags.pitch || '+0Hz';
  const files = [];
  segments.forEach((seg, i) => {
    const textFile = path.join(workDir, `seg${String(i).padStart(3, '0')}.txt`);
    const mp3 = path.join(workDir, `seg${String(i).padStart(3, '0')}.mp3`);
    fs.writeFileSync(textFile, seg.text);
    console.error(`[${i + 1}/${segments.length}] ${seg.tag} → ${cast.get(seg.tag).voice} (${seg.text.split(/\s+/).length} words)`);
    run('edge-tts', ['--voice', cast.get(seg.tag).voice, `--rate=${rate}`, `--pitch=${pitch}`, '--file', textFile, '--write-media', mp3]);
    files.push({ mp3, tag: seg.tag });
  });
  return files;
}

function stitch(files, out, gapSeconds, workDir) {
  if (!has('ffmpeg')) {
    console.error('ffmpeg not found, joining MP3 frames directly (no gap between speakers)');
    fs.writeFileSync(out, Buffer.concat(files.map((f) => fs.readFileSync(f.mp3))));
    return;
  }
  const gap = path.join(workDir, 'gap.mp3');
  if (gapSeconds > 0) run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', String(gapSeconds), '-q:a', '9', gap]);
  const list = [];
  files.forEach((f, i) => {
    if (i > 0 && gapSeconds > 0 && files[i - 1].tag !== f.tag) list.push(`file '${gap}'`);
    list.push(`file '${f.mp3}'`);
  });
  const listFile = path.join(workDir, 'concat.txt');
  fs.writeFileSync(listFile, list.join('\n'));
  run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', listFile, '-c', 'copy', out]);
}

async function main() {
  const { flags, positional } = parseArgs(process.argv.slice(2));
  const [slug, numberRaw] = positional;
  const number = Number(numberRaw);
  if (!slug || !Number.isInteger(number) || number < 1 || flags.help) {
    console.log(USAGE);
    process.exit(slug ? 1 : 0);
  }
  if (!has('edge-tts')) {
    console.error('edge-tts not found. Install it with: pip install "edge-tts==7.2.8"');
    process.exit(1);
  }

  const [{ chapter }, { characters }, { books }] = await Promise.all([
    get(`/books/${slug}/chapters/${number}`),
    get(`/books/${slug}/characters`),
    get('/books'),
  ]);
  const language = books.find((b) => b.slug === slug)?.language || 'en';
  const segments = segment(chapter.content || '');
  if (segments.length === 0) {
    console.error('Chapter has no text to narrate.');
    process.exit(1);
  }
  const tags = [...new Set(segments.map((s) => s.tag))];
  const cast = castFor(tags, characters, language, listVoices());

  console.error(`Cast for "${chapter.title}" (${language}):`);
  for (const [tag, { voice, source }] of cast) console.error(`  ${tag.padEnd(16)} ${voice.padEnd(36)} ${source}`);
  console.error(`${segments.length} segments`);
  if (flags['dry-run']) return;

  const out = path.resolve(flags.out || `chapter${number}.mp3`);
  const workDir = path.resolve('tts_work', `${slug}-${number}`);
  fs.mkdirSync(workDir, { recursive: true });
  const files = render(segments, cast, flags, workDir);
  stitch(files, out, Number(flags.gap ?? 0.4), workDir);
  if (!flags.keep) fs.rmSync(workDir, { recursive: true, force: true });

  const mb = (fs.statSync(out).size / 1024 / 1024).toFixed(1);
  console.error(`Wrote ${out} (${mb} MB${mb > 50 ? ', over the 50 MB upload limit, try --rate +10% or split the chapter' : ''})`);
  console.log(`node ${path.join(__dirname, 'api.js')} set-audio ${slug} ${number} --file ${out}`);
}

if (require.main === module) main().catch((e) => { console.error(e); process.exit(1); });

module.exports = { segment, castFor, defaultVoiceFor, render, stitch };
