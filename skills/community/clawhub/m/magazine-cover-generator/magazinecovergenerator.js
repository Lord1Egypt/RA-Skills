#!/usr/bin/env node
// Magazine Cover Generator — AI magazine cover art generator
// Powered by the Neta AI image generation API (api.talesofai.com)

const DEFAULT_PROMPT_SUFFIX = "high-fashion editorial magazine cover, bold masthead typography, dramatic lighting, professional photography, glossy finish, cover headlines, barcode, issue date, Vogue TIME GQ style layout, mixed-media collage elements, editorial composition";

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const API_BASE = "https://api.talesofai.com";

function parseArgs(argv) {
  const args = { prompt: null, size: "portrait", token: null, ref: null };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--size") { args.size = argv[++i]; }
    else if (a === "--token") { args.token = argv[++i]; }
    else if (a === "--ref") { args.ref = argv[++i]; }
    else if (a === "--help" || a === "-h") { args.help = true; }
    else { positional.push(a); }
  }
  if (positional.length > 0) args.prompt = positional.join(" ");
  return args;
}

function printHelp() {
  console.log(`Magazine Cover Generator

Usage:
  node magazinecovergenerator.js "your prompt" --token YOUR_TOKEN [options]

Options:
  --size <size>    portrait | landscape | square | tall (default: portrait)
  --token <token>  Neta API token (required) — get one at https://www.neta.art/open/
  --ref <uuid>     reference image UUID for style inheritance
  -h, --help       show this help

Example:
  node magazinecovergenerator.js "astronaut on vogue cover" --token YOUR_TOKEN
`);
}

async function createTask(token, prompt, size, ref) {
  const dims = SIZES[size] || SIZES.portrait;
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width: dims.width,
    height: dims.height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };
  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  const res = await fetch(`https://api.talesofai.com/v3/make_image`, {
    method: "POST",
    headers: {
      "x-token": token,
      "x-platform": "nieta-app/web",
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`make_image failed: ${res.status} ${res.statusText} ${text}`);
  }

  const raw = await res.text();
  let task_uuid = null;
  try {
    const parsed = JSON.parse(raw);
    if (typeof parsed === "string") task_uuid = parsed;
    else if (parsed && parsed.task_uuid) task_uuid = parsed.task_uuid;
  } catch {
    task_uuid = raw.trim().replace(/^"|"$/g, "");
  }
  if (!task_uuid) throw new Error(`No task_uuid in response: ${raw}`);
  return task_uuid;
}

async function pollTask(token, task_uuid) {
  const maxAttempts = 90;
  for (let i = 0; i < maxAttempts; i++) {
    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${task_uuid}`, {
      headers: {
        "x-token": token,
        "x-platform": "nieta-app/web",
        "content-type": "application/json",
      },
    });
    if (!res.ok) {
      await new Promise(r => setTimeout(r, 2000));
      continue;
    }
    const data = await res.json();
    const status = data.task_status;
    if (status === "PENDING" || status === "MODERATION") {
      await new Promise(r => setTimeout(r, 2000));
      continue;
    }
    // Done
    if (data.artifacts && data.artifacts.length > 0 && data.artifacts[0].url) {
      return data.artifacts[0].url;
    }
    if (data.result_image_url) return data.result_image_url;
    throw new Error(`Task finished but no image URL: ${JSON.stringify(data)}`);
  }
  throw new Error("Timed out waiting for image generation");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { printHelp(); process.exit(0); }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  if (!args.prompt) {
    console.error('\n✗ Prompt required. Usage: node magazinecovergenerator.js "your prompt" --token YOUR_TOKEN');
    process.exit(1);
  }

  const fullPrompt = `${args.prompt}, ${DEFAULT_PROMPT_SUFFIX}`;

  try {
    const task_uuid = await createTask(TOKEN, fullPrompt, args.size, args.ref);
    const imageUrl = await pollTask(TOKEN, task_uuid);
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message}`);
    process.exit(1);
  }
}

main();
