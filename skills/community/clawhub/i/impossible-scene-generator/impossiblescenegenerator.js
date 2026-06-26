#!/usr/bin/env node
import process from 'node:process';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT = 'a photorealistic impossible landscape, crystal mountains beneath cosmic auroras, organic-growing architecture, anti-physics floating islands, hyperdetailed cinematic photography, dramatic volumetric lighting, ultra-wide vista, 8k quality, awe-inspiring atmosphere';

function parseArgs(argv) {
  const args = { size: 'landscape' };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else positional.push(a);
  }
  args.prompt = positional.join(' ').trim();
  return args;
}

async function main() {
  const { prompt, size, token: tokenFlag, ref } = parseArgs(process.argv.slice(2));

  const TOKEN = tokenFlag;
  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = prompt || DEFAULT_PROMPT;
  const dims = SIZES[size] || SIZES.landscape;

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

  console.error(`→ Generating ${dims.width}×${dims.height}: "${PROMPT}"`);

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

  const submitData = await submitRes.json().catch(async () => await submitRes.text());
  const taskUuid = typeof submitData === 'string' ? submitData : submitData.task_uuid;

  if (!taskUuid) {
    console.error('✗ No task_uuid in response:', submitData);
    process.exit(1);
  }

  console.error(`→ Task ${taskUuid} submitted, polling…`);

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
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error('✗ Task done but no image URL:', JSON.stringify(data));
    process.exit(1);
  }

  console.error('✗ Timed out after 90 polls (~3 minutes)');
  process.exit(1);
}

main().catch((err) => {
  console.error('✗ Error:', err.message || err);
  process.exit(1);
});
