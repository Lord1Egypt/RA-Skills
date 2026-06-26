#!/usr/bin/env node
import { argv, exit, stdout } from 'node:process';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT = 'anime style isekai protagonist character, transported to a fantasy other-world, magical sword and ornate armor, vibrant Niji-style colors, dramatic cinematic lighting, light novel cover art composition, detailed face and outfit, full body character design sheet';

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

async function makeImage({ prompt, size, token, ref }) {
  const dims = SIZES[size] || SIZES.portrait;

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width: dims.width,
    height: dims.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: {
      'x-token': token,
      'x-platform': 'nieta-app/web',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`make_image failed: ${res.status} ${text}`);
  }

  const raw = await res.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(raw);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = raw.trim().replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    throw new Error(`No task_uuid returned: ${raw}`);
  }

  return taskUuid;
}

async function pollTask(taskUuid, token) {
  for (let i = 0; i < 90; i++) {
    await new Promise((r) => setTimeout(r, 2000));

    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: {
        'x-token': token,
        'x-platform': 'nieta-app/web',
        'content-type': 'application/json',
      },
    });

    if (!res.ok) continue;

    const data = await res.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (url) return url;
    throw new Error(`Task finished but no URL: ${JSON.stringify(data)}`);
  }

  throw new Error('Timed out after 90 polling attempts.');
}

async function main() {
  const { prompt, size, tokenFlag, ref } = parseArgs(argv.slice(2));

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const finalPrompt = prompt || DEFAULT_PROMPT;

  const taskUuid = await makeImage({ prompt: finalPrompt, size, token: TOKEN, ref });
  const url = await pollTask(taskUuid, TOKEN);
  stdout.write(url + '\n');
  exit(0);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message}`);
  exit(1);
});
