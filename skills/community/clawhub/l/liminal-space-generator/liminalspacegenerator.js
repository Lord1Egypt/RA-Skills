#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'liminal space, eerie empty hallway with fluorescent lighting, worn carpet, dreamcore aesthetic, uncanny atmosphere, analog horror feel, nostalgic unsettling mood, backrooms style, muted yellow and beige tones, deep perspective, photographic realism with slight VHS grain';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { positional: [], size: 'landscape', token: null, ref: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else args.positional.push(a);
  }
  return args;
}

async function main() {
  const argv = process.argv.slice(2);
  const { positional, size, token: tokenFlag, ref } = parseArgs(argv);
  const prompt = positional[0] || DEFAULT_PROMPT;

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const dims = SIZES[size] || SIZES.landscape;

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

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

  console.error(`→ Generating: "${prompt}"`);
  console.error(`  Size: ${size} (${dims.width}×${dims.height})`);

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
    console.error('✗ No task_uuid in response');
    process.exit(1);
  }

  console.error(`  Task: ${taskUuid}`);

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers,
    });
    if (!pollRes.ok) continue;
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
    console.error(`✗ Task finished with status ${status} but no image URL found`);
    process.exit(1);
  }

  console.error('\n✗ Timed out waiting for image');
  process.exit(1);
}

main().catch((err) => {
  console.error(`✗ ${err.message}`);
  process.exit(1);
});
