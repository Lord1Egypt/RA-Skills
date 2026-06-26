#!/usr/bin/env node
import process from 'node:process';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT = "humanized version of a pet reimagined as a person, photorealistic portrait, preserving the pet's personality, fur color, eye color, and distinctive features translated into human appearance, expressive face, detailed clothing matching the pet's vibe, studio lighting, high detail";

function parseArgs(argv) {
  const args = { prompt: null, size: 'portrait', token: null, ref: null };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') { args.size = argv[++i]; }
    else if (a === '--token') { args.token = argv[++i]; }
    else if (a === '--ref') { args.ref = argv[++i]; }
    else { rest.push(a); }
  }
  if (rest.length > 0) args.prompt = rest.join(' ');
  return args;
}

const { prompt: promptArg, size, token: tokenFlag, ref } = parseArgs(process.argv.slice(2));

const PROMPT = promptArg || DEFAULT_PROMPT;
const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

const dims = SIZES[size];
if (!dims) {
  console.error(`✗ Invalid --size "${size}". Use: square, portrait, landscape, tall.`);
  process.exit(1);
}

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

async function submitTask() {
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

  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`make_image failed: ${res.status} ${res.statusText} ${text}`);
  }
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    const data = await res.json();
    if (typeof data === 'string') return data;
    if (data && data.task_uuid) return data.task_uuid;
    throw new Error(`Unexpected response: ${JSON.stringify(data)}`);
  }
  const text = (await res.text()).trim().replace(/^"|"$/g, '');
  if (!text) throw new Error('Empty task_uuid response');
  return text;
}

async function pollTask(taskUuid) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const res = await fetch(url, { headers: HEADERS });
    if (!res.ok) continue;
    const data = await res.json().catch(() => null);
    if (!data) continue;
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;
    const artUrl = (Array.isArray(data.artifacts) && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (artUrl) return artUrl;
    throw new Error(`Task finished without URL: ${JSON.stringify(data)}`);
  }
  throw new Error('Timed out waiting for task');
}

(async () => {
  try {
    const taskUuid = await submitTask();
    const imageUrl = await pollTask(taskUuid);
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`✗ ${err.message}`);
    process.exit(1);
  }
})();
