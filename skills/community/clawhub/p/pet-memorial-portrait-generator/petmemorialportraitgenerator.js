#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = "A serene memorial portrait of a beloved pet, soft golden light streaming from above, peaceful meadow background with gentle clouds, tender cinematic atmosphere, warm nostalgic tones, detailed fur texture, gentle eyes full of love, tasteful remembrance composition, professional pet photography, soft bokeh, dreamy celestial mood";

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

function parseArgs(argv) {
  const args = { size: 'portrait', token: null, ref: null, prompt: null };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--size')        args.size  = rest[++i];
    else if (a === '--token')  args.token = rest[++i];
    else if (a === '--ref')    args.ref   = rest[++i];
    else if (!args.prompt)     args.prompt = a;
  }
  return args;
}

async function makeImage({ token, prompt, size, ref }) {
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
    const txt = await res.text();
    throw new Error(`make_image failed: ${res.status} ${txt}`);
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) {
    const data = await res.json();
    if (typeof data === "string") return data;
    if (data && data.task_uuid) return data.task_uuid;
    throw new Error(`Unexpected response: ${JSON.stringify(data)}`);
  }
  const txt = (await res.text()).trim().replace(/^"|"$/g, "");
  return txt;
}

async function pollTask({ token, taskUuid }) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  for (let i = 0; i < 90; i++) {
    const res = await fetch(url, {
      headers: {
        "x-token": token,
        "x-platform": "nieta-app/web",
        "content-type": "application/json",
      },
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`poll failed: ${res.status} ${txt}`);
    }
    const data = await res.json();
    const status = data.task_status;
    if (status !== "PENDING" && status !== "MODERATION") {
      const url0 = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
      if (!url0) throw new Error(`Task finished but no image URL: ${JSON.stringify(data)}`);
      return url0;
    }
    await new Promise(r => setTimeout(r, 2000));
  }
  throw new Error("Timed out waiting for task to finish");
}

async function main() {
  const { prompt: promptArg, size, token: tokenFlag, ref } = parseArgs(process.argv);
  const PROMPT = promptArg || DEFAULT_PROMPT;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  try {
    const taskUuid = await makeImage({ token: TOKEN, prompt: PROMPT, size, ref });
    const imageUrl = await pollTask({ token: TOKEN, taskUuid });
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message}`);
    process.exit(1);
  }
}

main();
