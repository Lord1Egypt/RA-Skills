#!/usr/bin/env node

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = 'portrait';
let ref = null;
let tokenFlag = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === '--token' && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === '--ref' && args[i + 1]) {
    ref = args[++i];
  } else if (!args[i].startsWith('--') && !prompt) {
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
  prompt = 'gothic portrait, dramatic dark lighting, ornate Victorian setting, deep shadows, rich dark tones, moody atmosphere, detailed face, elegant gothic fashion, cathedral background, candlelight, oil painting texture';
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const dimensions = SIZES[size];
if (!dimensions) {
  console.error(`\u2717 Invalid size "${size}". Use: square, portrait, landscape, tall`);
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
  // Submit the image generation task
  const createRes = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!createRes.ok) {
    const text = await createRes.text();
    console.error(`\u2717 API error (${createRes.status}): ${text}`);
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
    console.error('\u2717 No task UUID returned from API.');
    process.exit(1);
  }

  console.error(`Task submitted: ${taskUuid}`);
  console.error('Polling for result...');

  // Poll for completion
  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise(resolve => setTimeout(resolve, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers,
    });

    if (!pollRes.ok) {
      console.error(`\u2717 Poll error (${pollRes.status})`);
      continue;
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      console.error(`  Status: ${status} (attempt ${attempt + 1}/90)`);
      continue;
    }

    // Task is done
    const url = pollData.artifacts?.[0]?.url || pollData.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    } else {
      console.error('\u2717 Task completed but no image URL found.');
      console.error(JSON.stringify(pollData, null, 2));
      process.exit(1);
    }
  }

  console.error('\u2717 Timed out after 90 polling attempts.');
  process.exit(1);
}

main().catch(err => {
  console.error(`\u2717 ${err.message}`);
  process.exit(1);
});
