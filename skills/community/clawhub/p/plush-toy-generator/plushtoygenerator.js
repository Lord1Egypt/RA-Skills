#!/usr/bin/env node
import { argv, exit, stdout } from 'node:process';

const DEFAULT_PROMPT_TEMPLATE = 'adorable handmade plush toy of {subject}, soft fluffy fabric texture, visible stitching and seams, button eyes, embroidered details, sitting upright on plain pastel background, shot like a product photo for a toy store, soft studio lighting, kawaii stuffed animal aesthetic, hyper-tactile fuzzy surface, cute collectible plushie, high detail';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(args) {
  const out = { positional: [], size: 'square', token: null, ref: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--size') { out.size = args[++i]; }
    else if (a === '--token') { out.token = args[++i]; }
    else if (a === '--ref') { out.ref = args[++i]; }
    else { out.positional.push(a); }
  }
  return out;
}

async function main() {
  const args = parseArgs(argv.slice(2));
  const subject = args.positional.join(' ').trim();

  if (!subject) {
    console.error('\n✗ Prompt required. Usage: node plushtoygenerator.js "your description" --token YOUR_TOKEN');
    exit(1);
  }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    exit(1);
  }

  const sizeKey = (args.size || 'square').toLowerCase();
  const size = SIZES[sizeKey] || SIZES.square;

  const PROMPT = subject.includes('{subject}')
    ? subject
    : DEFAULT_PROMPT_TEMPLATE.replace('{subject}', subject);

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

  console.error('→ Submitting plush toy generation request...');

  const submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`✗ Submit failed: ${submitRes.status} ${submitRes.statusText}`);
    console.error(text);
    exit(1);
  }

  const submitText = await submitRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(submitText);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = submitText.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error('✗ No task_uuid returned from API');
    console.error(submitText);
    exit(1);
  }

  console.error(`→ Task submitted: ${taskUuid}`);
  console.error('→ Polling for result...');

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers,
    });

    if (!pollRes.ok) {
      console.error(`✗ Poll failed: ${pollRes.status} ${pollRes.statusText}`);
      continue;
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) {
      stdout.write(url + '\n');
      exit(0);
    }

    console.error(`✗ Task ended with status: ${status}`);
    console.error(JSON.stringify(data, null, 2));
    exit(1);
  }

  console.error('✗ Timed out waiting for result');
  exit(1);
}

main().catch((err) => {
  console.error('✗ Error:', err.message);
  exit(1);
});
