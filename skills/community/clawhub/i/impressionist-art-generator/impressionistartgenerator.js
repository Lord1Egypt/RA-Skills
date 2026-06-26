#!/usr/bin/env node
import process from 'node:process';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT_PREFIX = "impressionist oil painting in the style of Claude Monet and Pierre-Auguste Renoir, soft visible brushstrokes, dappled natural light, pastel palette with luminous highlights, atmospheric plein air scene, textured canvas feel, late 19th century French impressionism";

function parseArgs(argv) {
  const args = { positional: [], size: 'landscape', token: null, ref: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') { args.size = argv[++i]; }
    else if (a === '--token') { args.token = argv[++i]; }
    else if (a === '--ref') { args.ref = argv[++i]; }
    else if (a.startsWith('--size=')) { args.size = a.slice(7); }
    else if (a.startsWith('--token=')) { args.token = a.slice(8); }
    else if (a.startsWith('--ref=')) { args.ref = a.slice(6); }
    else { args.positional.push(a); }
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const userPrompt = args.positional.join(' ').trim();

  if (!userPrompt) {
    console.error('\n✗ Prompt required. Usage: node impressionistartgenerator.js "your prompt" --token YOUR_TOKEN');
    process.exit(1);
  }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const size = SIZES[args.size] || SIZES.landscape;
  const PROMPT = `${DEFAULT_PROMPT_PREFIX}, ${userPrompt}`;

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

  console.error(`→ Submitting task (${size.width}×${size.height})...`);

  const submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`\n✗ Submit failed (${submitRes.status}): ${text}`);
    process.exit(1);
  }

  const raw = await submitRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(raw);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = raw.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error('\n✗ No task_uuid returned');
    process.exit(1);
  }

  console.error(`→ Task ${taskUuid} submitted. Polling...`);

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers,
    });

    if (!pollRes.ok) {
      console.error(`  poll ${attempt + 1}: HTTP ${pollRes.status}`);
      continue;
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      if (attempt % 5 === 0) console.error(`  poll ${attempt + 1}: ${status}`);
      continue;
    }

    const url =
      (Array.isArray(data.artifacts) && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`\n✗ Task ended with status=${status} but no URL found`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('\n✗ Timed out waiting for task to complete');
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message}`);
  process.exit(1);
});
