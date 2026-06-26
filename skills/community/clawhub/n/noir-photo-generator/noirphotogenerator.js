#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = "film noir portrait, dramatic high-contrast black and white, venetian blind shadows, cigarette smoke, rain-soaked street, vintage 1940s detective aesthetic, cinematic lighting, grainy film texture, moody atmosphere";

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { size: 'portrait', prompt: null, token: null, ref: null };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--size') {
      args.size = rest[++i];
    } else if (a === '--token') {
      args.token = rest[++i];
    } else if (a === '--ref') {
      args.ref = rest[++i];
    } else if (!a.startsWith('--') && args.prompt === null) {
      args.prompt = a;
    }
  }
  return args;
}

async function main() {
  const { prompt: promptArg, size, token: tokenFlag, ref } = parseArgs(process.argv);

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = promptArg || DEFAULT_PROMPT;
  const dims = SIZES[size] || SIZES.portrait;

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: dims.width,
    height: dims.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  console.error(`→ Generating film noir image (${dims.width}×${dims.height})...`);

  const submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`✗ Submit failed (${submitRes.status}): ${text}`);
    process.exit(1);
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
    console.error('✗ No task_uuid returned');
    process.exit(1);
  }

  console.error(`→ Task: ${taskUuid}`);

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers,
    });

    if (!pollRes.ok) {
      continue;
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      process.stderr.write('.');
      continue;
    }

    process.stderr.write('\n');

    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`✗ Task ended with status "${status}" but no image URL`);
    process.exit(1);
  }

  console.error('✗ Timed out waiting for image');
  process.exit(1);
}

main().catch((err) => {
  console.error(`✗ ${err.message}`);
  process.exit(1);
});
