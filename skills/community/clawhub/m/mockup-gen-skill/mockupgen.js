#!/usr/bin/env node

// --- CLI args ---
const args = process.argv.slice(2);
let prompt = null;
let size = "landscape";
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--size" && args[i + 1]) { size = args[++i]; }
  else if (args[i] === "--token" && args[i + 1]) { tokenFlag = args[++i]; }
  else if (args[i] === "--ref" && args[i + 1]) { refUuid = args[++i]; }
  else if (!args[i].startsWith("--") && prompt === null) { prompt = args[i]; }
}

if (!prompt) {
  prompt = "product mockup on clean background, professional photography style";
}

// --- Token resolution ---
const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  process.exit(1);
}

// --- Size map ---
const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const { width, height } = SIZES[size] || SIZES.landscape;

// --- Headers ---
const HEADERS = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

// --- Build request body ---
const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
  width,
  height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (refUuid) {
  body.inherit_params = {
    collection_uuid: refUuid,
    picture_uuid: refUuid,
  };
}

// --- Submit job ---
async function submitJob() {
  const res = await fetch("https://api.talesofai.cn/v3/make_image", {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Submit failed (${res.status}): ${text}`);
  }

  const data = await res.json();

  if (typeof data === "string") return data;
  if (data.task_uuid) return data.task_uuid;
  throw new Error(`Unexpected response: ${JSON.stringify(data)}`);
}

// --- Poll for result ---
async function pollTask(taskUuid) {
  const url = `https://api.talesofai.cn/v1/artifact/task/${taskUuid}`;
  const PENDING_STATUSES = new Set(["PENDING", "MODERATION"]);
  const MAX_ATTEMPTS = 90;
  const INTERVAL_MS = 2000;

  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    await new Promise((r) => setTimeout(r, INTERVAL_MS));

    const res = await fetch(url, { headers: HEADERS });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Poll failed (${res.status}): ${text}`);
    }

    const data = await res.json();
    const status = data.task_status;

    if (PENDING_STATUSES.has(status)) continue;

    // Done
    const imageUrl =
      data.artifacts?.[0]?.url ||
      data.result_image_url;

    if (!imageUrl) {
      throw new Error(`Task done but no image URL found: ${JSON.stringify(data)}`);
    }

    return imageUrl;
  }

  throw new Error("Timed out waiting for image generation.");
}

// --- Main ---
(async () => {
  try {
    const taskUuid = await submitJob();
    const imageUrl = await pollTask(taskUuid);
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  }
})();
