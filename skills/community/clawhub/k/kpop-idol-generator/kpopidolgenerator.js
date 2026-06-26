#!/usr/bin/env node
// K-Pop Idol Generator — generates k-pop idol style portraits via the Neta AI API.

const DEFAULT_PROMPT_SUFFIX = "k-pop idol style portrait, glossy studio lighting, korean beauty aesthetic, flawless dewy skin, trendy designer outfit, colored contacts, styled hair, glamorous magazine-quality photography, soft gradient background, high fashion pose, cinematic bokeh";

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size')       args.size  = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref')   args.ref   = argv[++i];
    else if (a === '--help' || a === '-h') args.help = true;
    else args._.push(a);
  }
  return args;
}

function printHelp() {
  console.log(`K-Pop Idol Generator

Usage:
  node kpopidolgenerator.js "your prompt" --token YOUR_TOKEN [options]

Options:
  --token <token>   Neta API token (required). Get yours at https://www.neta.art/open/
  --size  <size>    portrait | landscape | square | tall  (default: portrait)
  --ref   <uuid>    Reference image UUID for style inheritance
  -h, --help        Show this help

Example:
  node kpopidolgenerator.js "young woman with pastel pink hair smiling" --token "$NETA_TOKEN"
`);
}

async function createTask({ token, prompt, width, height, ref }) {
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };
  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  const res = await fetch("https://api.talesofai.com/v3/make_image", {
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
  let taskUuid;
  try {
    const parsed = JSON.parse(raw);
    taskUuid = typeof parsed === "string" ? parsed : (parsed.task_uuid || parsed.taskUuid);
  } catch {
    taskUuid = raw.replace(/^"|"$/g, "").trim();
  }
  if (!taskUuid) throw new Error(`No task_uuid in response: ${raw}`);
  return taskUuid;
}

async function pollTask({ token, taskUuid }) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  const headers = {
    "x-token": token,
    "x-platform": "nieta-app/web",
    "content-type": "application/json",
  };

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const res = await fetch(url, { headers });
    if (!res.ok) continue;
    const data = await res.json().catch(() => null);
    if (!data) continue;

    const status = data.task_status;
    if (status === "PENDING" || status === "MODERATION") continue;

    const artifactUrl =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;
    if (artifactUrl) return artifactUrl;

    throw new Error(`Task finished with status ${status} but no image URL. Response: ${JSON.stringify(data)}`);
  }
  throw new Error("Timed out waiting for image generation (180s).");
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

  const userPrompt = args._[0];
  if (!userPrompt) {
    console.error('\n✗ Prompt required. Usage: node kpopidolgenerator.js "your prompt" --token YOUR_TOKEN');
    process.exit(1);
  }

  const sizeKey = (args.size || "portrait").toLowerCase();
  const size = SIZES[sizeKey];
  if (!size) {
    console.error(`✗ Unknown size "${sizeKey}". Use one of: ${Object.keys(SIZES).join(", ")}`);
    process.exit(1);
  }

  const PROMPT = `${userPrompt}, ${DEFAULT_PROMPT_SUFFIX}`;

  try {
    console.error(`→ Submitting generation task (${sizeKey} ${size.width}x${size.height})...`);
    const taskUuid = await createTask({
      token: TOKEN,
      prompt: PROMPT,
      width: size.width,
      height: size.height,
      ref: args.ref,
    });
    console.error(`→ Task ${taskUuid} queued. Polling...`);
    const imageUrl = await pollTask({ token: TOKEN, taskUuid });
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message || err}`);
    process.exit(1);
  }
}

main();
