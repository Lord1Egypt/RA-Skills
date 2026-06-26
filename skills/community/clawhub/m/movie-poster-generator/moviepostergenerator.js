#!/usr/bin/env node

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = 'tall';
let tokenFlag = null;
let ref = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--token' && i + 1 < args.length) {
    tokenFlag = args[++i];
  } else if (args[i] === '--size' && i + 1 < args.length) {
    size = args[++i];
  } else if (args[i] === '--ref' && i + 1 < args.length) {
    ref = args[++i];
  } else if (!prompt && !args[i].startsWith('--')) {
    prompt = args[i];
  }
}

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n\u2717 Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

if (!prompt) {
  console.error('\n\u2717 Prompt required. Usage: node moviepostergenerator.js "your prompt" --token YOUR_TOKEN');
  process.exit(1);
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const dimensions = SIZES[size];
if (!dimensions) {
  console.error(`\n\u2717 Invalid size "${size}". Choose from: portrait, landscape, square, tall`);
  process.exit(1);
}

const headers = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
  width: dimensions.width,
  height: dimensions.height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (ref) {
  body.inherit_params = {
    collection_uuid: ref,
    picture_uuid: ref,
  };
}

async function main() {
  console.error(`\u2139 Generating movie poster (${size}: ${dimensions.width}x${dimensions.height})...`);
  console.error(`\u2139 Prompt: "${prompt}"`);

  // Submit the image generation task
  const createRes = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!createRes.ok) {
    const errText = await createRes.text();
    console.error(`\n\u2717 API error (${createRes.status}): ${errText}`);
    process.exit(1);
  }

  const createData = await createRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(createData);
    taskUuid = parsed.task_uuid || parsed;
  } catch {
    taskUuid = createData.replace(/"/g, '').trim();
  }

  if (!taskUuid) {
    console.error('\n\u2717 No task UUID returned from API.');
    process.exit(1);
  }

  console.error(`\u2139 Task UUID: ${taskUuid}`);
  console.error('\u2139 Polling for result...');

  // Poll for completion
  const maxAttempts = 90;
  const pollInterval = 2000;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, pollInterval));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: "GET",
      headers,
    });

    if (!pollRes.ok) {
      console.error(`\u2139 Poll attempt ${attempt}/${maxAttempts} — HTTP ${pollRes.status}, retrying...`);
      continue;
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      console.error(`\u2139 Poll attempt ${attempt}/${maxAttempts} — status: ${status}`);
      continue;
    }

    // Task is done
    const imageUrl =
      (pollData.artifacts && pollData.artifacts[0] && pollData.artifacts[0].url) ||
      pollData.result_image_url;

    if (imageUrl) {
      console.log(imageUrl);
      process.exit(0);
    } else {
      console.error('\n\u2717 Task completed but no image URL found in response.');
      console.error(JSON.stringify(pollData, null, 2));
      process.exit(1);
    }
  }

  console.error(`\n\u2717 Timed out after ${maxAttempts} polling attempts.`);
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n\u2717 Unexpected error: ${err.message}`);
  process.exit(1);
});
