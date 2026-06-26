#!/usr/bin/env node
// Podcast Cover Generator — AI-powered podcast cover art via Neta API

const API_BASE = 'https://api.talesofai.com';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_STYLE_SUFFIX = 'professional podcast cover art, bold central visual focus, dramatic lighting, vibrant color palette, modern minimalist design, broadcast quality, square 1:1 composition, eye-catching thumbnail-ready artwork, clean negative space for title typography, cinematic style';

function parseArgs(argv) {
  const args = { prompt: null, size: 'square', token: null, ref: null };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--size') {
      args.size = rest[++i];
    } else if (a === '--token') {
      args.token = rest[++i];
    } else if (a === '--ref') {
      args.ref = rest[++i];
    } else if (a === '--help' || a === '-h') {
      args.help = true;
    } else if (!args.prompt) {
      args.prompt = a;
    }
  }
  return args;
}

function printHelp() {
  console.log(`Podcast Cover Generator — generate podcast cover art from a text prompt

Usage:
  node podcastcovergenerator.js "your description" --token YOUR_TOKEN [options]

Options:
  --size <preset>   square | portrait | landscape | tall  (default: square)
  --token <token>   Neta API token (required)
  --ref <uuid>      Reference image picture_uuid for style inheritance
  -h, --help        Show this help

Get a free trial token at: https://www.neta.art/open/
`);
}

async function createTask({ prompt, size, token, ref }) {
  const dims = SIZES[size] || SIZES.square;
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

  const res = await fetch(`https://api.talesofai.com/v3/make_image`, {
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
    throw new Error(`make_image failed: ${res.status} ${res.statusText} — ${text}`);
  }

  const raw = await res.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(raw);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = raw.replace(/^"|"$/g, '').trim();
  }
  if (!taskUuid) throw new Error(`No task_uuid in response: ${raw}`);
  return taskUuid;
}

async function pollTask(taskUuid, token) {
  const maxAttempts = 90;
  for (let i = 0; i < maxAttempts; i++) {
    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: {
        'x-token': token,
        'x-platform': 'nieta-app/web',
        'content-type': 'application/json',
      },
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`poll failed: ${res.status} ${res.statusText} — ${text}`);
    }

    const data = await res.json();
    const status = data.task_status;

    if (status !== 'PENDING' && status !== 'MODERATION') {
      const url =
        (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
        data.result_image_url;
      if (!url) {
        throw new Error(`Task finished but no image URL. status=${status} data=${JSON.stringify(data)}`);
      }
      return url;
    }

    await new Promise((r) => setTimeout(r, 2000));
  }
  throw new Error('Timed out waiting for image generation');
}

async function main() {
  const args = parseArgs(process.argv);

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  if (!args.prompt) {
    console.error('\n✗ Prompt required. Usage: node podcastcovergenerator.js "your description" --token YOUR_TOKEN');
    process.exit(1);
  }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  if (!SIZES[args.size]) {
    console.error(`\n✗ Unknown size "${args.size}". Use: square | portrait | landscape | tall`);
    process.exit(1);
  }

  const fullPrompt = `${args.prompt}, ${DEFAULT_STYLE_SUFFIX}`;

  console.error(`→ Generating ${args.size} image...`);
  try {
    const taskUuid = await createTask({
      prompt: fullPrompt,
      size: args.size,
      token: TOKEN,
      ref: args.ref,
    });
    console.error(`  task_uuid: ${taskUuid}`);
    console.error('  polling...');
    const url = await pollTask(taskUuid, TOKEN);
    console.log(url);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message}`);
    process.exit(1);
  }
}

main();
