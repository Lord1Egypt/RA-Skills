#!/usr/bin/env node
import { argv, exit, stdout } from 'node:process';

const DEFAULT_PROMPT = 'vintage 1950s pin-up art illustration, classic retro glamour pose, stylized lineart with soft shading, warm sepia and pastel palette, mid-century advertising poster aesthetic, playful elegant composition, film grain texture, art by Gil Elvgren';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(args) {
  let prompt = null;
  let size = 'portrait';
  let tokenFlag = null;
  let ref = null;

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--size') {
      size = args[++i];
    } else if (a === '--token') {
      tokenFlag = args[++i];
    } else if (a === '--ref') {
      ref = args[++i];
    } else if (!a.startsWith('--') && prompt === null) {
      prompt = a;
    }
  }

  return { prompt, size, tokenFlag, ref };
}

async function main() {
  const { prompt: userPrompt, size, tokenFlag, ref } = parseArgs(argv.slice(2));

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = userPrompt || DEFAULT_PROMPT;
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

  console.error(`→ Submitting job (${dims.width}×${dims.height})...`);

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

  const rawText = await submitRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(rawText);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = rawText.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error(`\n✗ No task_uuid in response: ${rawText}`);
    process.exit(1);
  }

  console.error(`→ Task: ${taskUuid}`);
  console.error('→ Polling...');

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers,
    });

    if (!pollRes.ok) {
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

    console.error(`\n✗ Task ended with status "${status}" but no image URL.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('\n✗ Timed out after 90 attempts (~3 minutes).');
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n✗ Error: ${err.message}`);
  process.exit(1);
});
