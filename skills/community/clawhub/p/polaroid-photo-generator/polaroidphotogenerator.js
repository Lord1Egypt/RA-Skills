#!/usr/bin/env node
import { setTimeout as sleep } from "timers/promises";

const args = process.argv.slice(2);

function getFlag(name) {
  const idx = args.indexOf(name);
  return idx !== -1 ? args[idx + 1] : null;
}

const PROMPT_RAW = args.find((a) => !a.startsWith("--") && args.indexOf(a) === args.indexOf(a));
const positional = args.filter((a, i) => {
  if (a.startsWith("--")) return false;
  if (i > 0 && args[i - 1].startsWith("--")) return false;
  return true;
});
const PROMPT = positional[0];
const tokenFlag = getFlag("--token");
const sizeFlag = getFlag("--size") || "square";
const refFlag = getFlag("--ref");

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error("\n✗ Token required. Pass via: --token YOUR_TOKEN");
  console.error("  Get yours at: https://www.neta.art/open/");
  process.exit(1);
}

if (!PROMPT) {
  console.error("\n✗ Prompt required. Pass as first positional argument.");
  console.error('  Example: node polaroidphotogenerator.js "your prompt" --token YOUR_TOKEN');
  process.exit(1);
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const { width, height } = SIZES[sizeFlag] || SIZES.square;

const HEADERS = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

const DEFAULT_PROMPT =
  "A vintage polaroid instant photograph with faded warm colors, soft film grain, slight vignette, overexposed highlights, authentic 1970s–1980s color palette, retro instant-film aesthetic, white polaroid border frame";

const fullPrompt = PROMPT
  ? `${PROMPT}. ${DEFAULT_PROMPT}`
  : DEFAULT_PROMPT;

const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: fullPrompt, weight: 1 }],
  width,
  height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (refFlag) {
  body.inherit_params = {
    collection_uuid: refFlag,
    picture_uuid: refFlag,
  };
}

async function main() {
  console.error(`Generating polaroid photo: "${PROMPT}" (${sizeFlag} ${width}×${height})...`);

  const makeRes = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!makeRes.ok) {
    const text = await makeRes.text();
    console.error(`\n✗ API error ${makeRes.status}: ${text}`);
    process.exit(1);
  }

  const makeData = await makeRes.json();
  const task_uuid =
    typeof makeData === "string" ? makeData : makeData.task_uuid;

  if (!task_uuid) {
    console.error("\n✗ No task_uuid returned from API.");
    console.error(JSON.stringify(makeData));
    process.exit(1);
  }

  console.error(`Task started: ${task_uuid}`);
  console.error("Polling for result...");

  const MAX_ATTEMPTS = 90;
  for (let i = 0; i < MAX_ATTEMPTS; i++) {
    await sleep(2000);

    const pollRes = await fetch(
      `https://api.talesofai.com/v1/artifact/task/${task_uuid}`,
      { headers: HEADERS }
    );

    if (!pollRes.ok) {
      console.error(`Poll attempt ${i + 1} failed: ${pollRes.status}`);
      continue;
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      process.stderr.write(".");
      continue;
    }

    process.stderr.write("\n");

    const url =
      pollData.artifacts?.[0]?.url || pollData.result_image_url;

    if (!url) {
      console.error("\n✗ No image URL in response.");
      console.error(JSON.stringify(pollData));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error("\n✗ Timed out waiting for image generation.");
  process.exit(1);
}

main().catch((err) => {
  console.error("\n✗ Unexpected error:", err.message);
  process.exit(1);
});
