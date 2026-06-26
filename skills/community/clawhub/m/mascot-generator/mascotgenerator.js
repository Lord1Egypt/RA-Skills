#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'cute friendly brand mascot character, full body pose, clean bold outlines, vibrant colors, professional mascot design, commercial character art, memorable and expressive, centered composition, plain background';
const STYLE = 'cinematic';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const API_BASE = 'https://api.talesofai.com';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else if (a === '--help' || a === '-h') args.help = true;
    else args._.push(a);
  }
  return args;
}

function printHelp() {
  console.log(`Mascot Generator

Usage:
  node mascotgenerator.js "your prompt" --token YOUR_TOKEN [options]

Options:
  --size <size>   square (default), portrait, landscape, tall
  --token <tok>   Neta API token (required) — get one at https://www.neta.art/open/
  --ref <uuid>    Reference image UUID for style inheritance
  -h, --help      Show this help
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const userPrompt = args._[0];
  const PROMPT = userPrompt && userPrompt.trim().length > 0
    ? `${userPrompt.trim()}, ${DEFAULT_PROMPT}`
    : DEFAULT_PROMPT;

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const sizeKey = (args.size || 'square').toLowerCase();
  const size = SIZES[sizeKey];
  if (!size) {
    console.error(`✗ Invalid size "${sizeKey}". Valid: ${Object.keys(SIZES).join(', ')}`);
    process.exit(1);
  }

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: size.width,
    height: size.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (args.ref) {
    body.inherit_params = {
      collection_uuid: args.ref,
      picture_uuid: args.ref,
    };
  }

  console.error(`→ Submitting mascot generation request (${size.width}×${size.height}, style: ${STYLE})...`);

  let submitRes;
  try {
    submitRes = await fetch(`https://api.talesofai.com/v3/make_image`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  } catch (err) {
    console.error(`✗ Network error: ${err.message}`);
    process.exit(1);
  }

  if (!submitRes.ok) {
    const text = await submitRes.text().catch(() => '');
    console.error(`✗ Submit failed (${submitRes.status}): ${text}`);
    process.exit(1);
  }

  const submitText = await submitRes.text();
  let taskUuid;
  const trimmed = submitText.trim();
  try {
    const parsed = JSON.parse(trimmed);
    if (typeof parsed === 'string') taskUuid = parsed;
    else if (parsed && typeof parsed === 'object') taskUuid = parsed.task_uuid || parsed.taskUuid;
  } catch {
    taskUuid = trimmed.replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    console.error(`✗ Could not parse task_uuid from response: ${submitText}`);
    process.exit(1);
  }

  console.error(`→ Task submitted: ${taskUuid}`);
  console.error('→ Polling for result...');

  const maxAttempts = 90;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    let pollRes;
    try {
      pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, { headers });
    } catch (err) {
      console.error(`  (attempt ${attempt}) network error: ${err.message}`);
      continue;
    }

    if (!pollRes.ok) {
      console.error(`  (attempt ${attempt}) poll failed: ${pollRes.status}`);
      continue;
    }

    let data;
    try {
      data = await pollRes.json();
    } catch {
      continue;
    }

    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') {
      if (attempt % 5 === 0) console.error(`  ...still ${status.toLowerCase()} (${attempt}/${maxAttempts})`);
      continue;
    }

    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`✗ Task finished with status "${status}" but no image URL found.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch((err) => {
  console.error(`✗ Unexpected error: ${err.message}`);
  process.exit(1);
});
