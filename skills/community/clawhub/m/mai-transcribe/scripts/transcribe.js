#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const {
  apiBase,
  apiKey,
  apiVersion,
  ensureParentDir,
  extractTranscript,
  formatApiError,
  parseArgs,
  resolveAudioFile,
} = require('./common');

const HELP = `MAI-Transcribe-1 via Azure Speech

Usage:
  node transcribe.js <audio-file> [options]

Options:
  --out <path>           Output file path (default: <input>.txt)
  --json                 Write raw JSON response instead of plain text
  --language <locale>    Locale hint, e.g. en-GB or en-US
  --model <name>         Model name (default: mai-transcribe-1)
  --api-version <ver>    API version (default: env or 2025-10-15)
  --help                 Show this help

Required env:
  AZURE_SPEECH_ENDPOINT  e.g. https://your-resource.cognitiveservices.azure.com
  AZURE_SPEECH_KEY       Azure Speech key
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(HELP);
    return;
  }

  validateArgs(args);

  const { filePath, stat } = resolveAudioFile(args._[0]);
  const outPath = path.resolve(args.out || `${filePath}${args.json ? '.json' : '.txt'}`);
  ensureParentDir(outPath);

  if (stat.size > 25 * 1024 * 1024) {
    console.error(`Warning: buffering a large audio file in memory (${Math.round(stat.size / (1024 * 1024))} MB).`);
  }

  const form = new FormData();
  form.append('audio', new Blob([fs.readFileSync(filePath)]), path.basename(filePath));
  form.append('definition', JSON.stringify(buildDefinition(args)));

  const url = `${apiBase()}/speechtotext/transcriptions:transcribe?api-version=${encodeURIComponent(args['api-version'] || apiVersion())}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Ocp-Apim-Subscription-Key': apiKey(),
    },
    body: form,
  });

  const raw = await res.text();
  let data;
  try {
    data = JSON.parse(raw);
  } catch {
    data = { raw };
  }

  if (!res.ok) throw formatApiError(res, data, url);

  fs.writeFileSync(
    outPath,
    args.json ? JSON.stringify(data, null, 2) : extractTranscript(data),
    'utf8'
  );

  console.log(outPath);
}

function buildDefinition(args) {
  const definition = {
    enhancedMode: {
      enabled: true,
      model: args.model || 'mai-transcribe-1',
    },
  };

  if (args.language) definition.locales = [args.language];
  return definition;
}

function validateArgs(args) {
  const allowed = new Set(['out', 'json', 'language', 'model', 'api-version', 'help', '_', '__unknown']);
  for (const key of Object.keys(args)) {
    if (!allowed.has(key)) {
      throw new Error(`Unknown option: --${key}\n\n${HELP}`);
    }
  }
}

main().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
