#!/usr/bin/env node
import { promises as fs, realpathSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';

import { sanitizeMarkdown } from './utils/sanitizer.mjs';
import { calculateMetrics, mean, punctuationRates } from './utils/metrics.mjs';
import { tokenizeText } from './utils/tokenizer.mjs';

const { mkdir, readFile, readdir, rename, stat, writeFile } = fs;

function round(value, places = 4) {
  const factor = 10 ** places;
  return Math.round(value * factor) / factor;
}

function averageObjects(objects) {
  const keys = [...new Set(objects.flatMap((object) => Object.keys(object)))];
  return Object.fromEntries(keys.map((key) => [key, round(mean(objects.map((object) => object[key] ?? 0)))]));
}

export async function fingerprintSamples(files, options = {}) {
  if (!Array.isArray(files) || files.length < 1 || files.length > 5) throw new Error('Fingerprint requires 1 to 5 sample files');
  const samples = [];
  for (const file of files) {
    const raw = await readFile(file, 'utf8');
    const sanitized = sanitizeMarkdown(raw);
    const tokenized = tokenizeText(sanitized, 'auto');
    const metrics = calculateMetrics(tokenized, sanitized);
    if (metrics.wordCount < 20 || metrics.sentenceCount < 3) throw new Error(`Sample is too short: ${file}`);
    samples.push({
      ...metrics,
      averageParagraphSentenceCount: mean(tokenized.paragraphs.map((paragraph) => paragraph.sentences.length)),
      punctuationRates: punctuationRates(sanitized, metrics.wordCount),
    });
  }

  const punctuation = averageObjects(samples.map((sample) => sample.punctuationRates));
  const profile = {
    name: options.name ?? 'custom-voice',
    version: 1,
    sampleCount: samples.length,
    language: options.language ?? 'auto',
    metrics: {
      meanSentenceLength: round(mean(samples.map((sample) => sample.meanSentenceLength))),
      stdDev: round(mean(samples.map((sample) => sample.stdDev))),
      burstinessCV: round(mean(samples.map((sample) => sample.burstinessCV))),
      adjacentDelta: round(mean(samples.map((sample) => sample.adjacentDelta))),
      mattr: round(mean(samples.map((sample) => sample.mattr))),
      averageParagraphSentenceCount: round(mean(samples.map((sample) => sample.averageParagraphSentenceCount))),
      punctuationRates: punctuation,
    },
  };

  if (options.output) {
    const output = path.resolve(options.output);
    await mkdir(path.dirname(output), { recursive: true });
    const temporary = `${output}.tmp-${process.pid}`;
    await writeFile(temporary, `${JSON.stringify(profile, null, 2)}\n`, 'utf8');
    await rename(temporary, output);
  }
  return profile;
}

async function collectInput(input) {
  const info = await stat(input);
  if (info.isFile()) return [path.resolve(input)];
  if (!info.isDirectory()) throw new Error('--input must be a file or directory');
  const entries = await readdir(input, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isFile() && /\.(?:md|txt)$/i.test(entry.name))
    .map((entry) => path.resolve(input, entry.name))
    .sort()
    .slice(0, 5);
}

export async function runFingerprintCli(argv, io = {}) {
  const stdout = io.stdout ?? ((value) => process.stdout.write(value));
  const stderr = io.stderr ?? ((value) => process.stderr.write(value));
  try {
    const { values } = parseArgs({
      args: argv,
      options: {
        input: { type: 'string' },
        output: { type: 'string' },
        name: { type: 'string' },
        lang: { type: 'string', default: 'auto' },
        help: { type: 'boolean' },
      },
      strict: true,
      allowPositionals: false,
    });
    if (values.help) {
      stdout('Usage: humanizer-fingerprint --input <file-or-dir> --output <profile.json> [--name <name>] [--lang id|en|auto]\n');
      return 0;
    }
    if (!values.input || !values.output) throw new Error('--input and --output are required');
    if (!['id', 'en', 'auto'].includes(values.lang)) throw new Error('--lang must be id, en, or auto');
    const files = await collectInput(values.input);
    if (!files.length) throw new Error('No .txt or .md samples found');
    const profile = await fingerprintSamples(files, { output: values.output, name: values.name, language: values.lang });
    stdout(`${JSON.stringify(profile, null, 2)}\n`);
    return 0;
  } catch (error) {
    stderr(`ERROR: ${error.message}\n`);
    return 2;
  }
}

function currentModulePath() {
  let value = decodeURIComponent(new URL(import.meta.url).pathname);
  if (/^\/[A-Za-z]:/.test(value)) value = value.slice(1);
  return path.resolve(value);
}

function isMainModule() {
  if (!process.argv[1]) return false;
  try {
    return realpathSync(process.argv[1]) === realpathSync(currentModulePath());
  } catch {
    return false;
  }
}

if (isMainModule()) {
  process.exitCode = await runFingerprintCli(process.argv.slice(2));
}
