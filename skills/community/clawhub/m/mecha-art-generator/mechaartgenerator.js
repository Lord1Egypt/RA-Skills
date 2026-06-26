#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'highly detailed mecha robot, intricate sci-fi armor plating, dynamic action pose, glowing energy core, futuristic battlefield background, panel lines and weathering, anime style, cinematic lighting, hyper-detailed mechanical design';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const API_BASE = 'https://api.talesofai.com';

function parseArgs(argv) {
  const args = { positional: [], size: 'landscape', token: null, ref: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') {
      args.size = argv[++i];
    } else if (a === '--token') {
      args.token = argv[++i];
    } else if (a === '--ref') {
      args.ref = argv[++i];
    } else if (a === '--help' || a === '-h') {
      args.help = true;
    } else {
      args.positional.push(a);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Mecha Art Generator

Usage:
  node mechaartgenerator.js "your prompt" --token YOUR_TOKEN [options]

Options:
  --size <size>   portrait | landscape | square | tall (default: landscape)
  --token <tok>   Neta API token (required)
  --ref <uuid>    Reference image UUID for style inheritance
  --help, -h      Show this help

Get a free trial token at https://www.neta.art/open/
`);
}

async function createTask({ token, prompt, width, height, ref }) {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
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
    throw new Error(`make_image failed: ${res.status} ${res.statusText} ${text}`);
  }

  const text = await res.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(text);
    if (typeof parsed === 'string') {
      taskUuid = parsed;
    } else if (parsed && typeof parsed === 'object') {
      taskUuid = parsed.task_uuid || parsed.taskUuid || parsed.uuid;
    }
  } catch {
    taskUuid = text.trim().replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    throw new Error(`Could not parse task_uuid from response: ${text}`);
  }
  return taskUuid;
}

async function pollTask({ token, taskUuid }) {
  for (let attempt = 0; attempt < 90; attempt++) {
    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers: {
        'x-token': token,
        'x-platform': 'nieta-app/web',
        'content-type': 'application/json',
      },
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`poll failed: ${res.status} ${res.statusText} ${text}`);
    }

    const data = await res.json();
    const status = data.task_status;

    if (status && status !== 'PENDING' && status !== 'MODERATION') {
      let url = null;
      if (Array.isArray(data.artifacts) && data.artifacts.length > 0) {
        url = data.artifacts[0].url;
      }
      if (!url) {
        url = data.result_image_url;
      }
      if (!url) {
        throw new Error(`Task finished with status ${status} but no image url returned: ${JSON.stringify(data)}`);
      }
      return url;
    }

    await new Promise((r) => setTimeout(r, 2000));
  }
  throw new Error('Timed out waiting for image generation');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = args.positional[0] || DEFAULT_PROMPT;

  const sizeKey = (args.size || 'landscape').toLowerCase();
  if (!SIZES[sizeKey]) {
    console.error(`✗ Unknown size: ${args.size}. Valid: ${Object.keys(SIZES).join(', ')}`);
    process.exit(1);
  }
  const { width, height } = SIZES[sizeKey];

  try {
    const taskUuid = await createTask({ token: TOKEN, prompt: PROMPT, width, height, ref: args.ref });
    const url = await pollTask({ token: TOKEN, taskUuid });
    console.log(url);
    process.exit(0);
  } catch (err) {
    console.error(`✗ ${err.message}`);
    process.exit(1);
  }
}

main();
