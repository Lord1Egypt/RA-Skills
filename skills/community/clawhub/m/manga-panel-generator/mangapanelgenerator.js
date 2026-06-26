#!/usr/bin/env node
// Manga Panel Generator — generate manga panels via Neta AI image generation API.

const DEFAULT_PROMPT = "black and white manga panel, dynamic composition, screentone shading, expressive character with action lines, speech bubble placeholders, dramatic angle, crisp ink linework, Japanese manga art style";

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { prompt: null, size: "portrait", token: null, ref: null };
  const rest = argv.slice(2);
  const positional = [];
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === "--size") args.size = rest[++i];
    else if (a === "--token") args.token = rest[++i];
    else if (a === "--ref") args.ref = rest[++i];
    else positional.push(a);
  }
  if (positional.length > 0) args.prompt = positional.join(" ");
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
    const text = await res.text();
    throw new Error(`make_image failed: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  let taskUuid;
  if (contentType.includes("application/json")) {
    const json = await res.json();
    if (typeof json === "string") taskUuid = json;
    else if (json && typeof json === "object") taskUuid = json.task_uuid || json.taskUuid;
  } else {
    const text = (await res.text()).trim();
    try {
      const parsed = JSON.parse(text);
      if (typeof parsed === "string") taskUuid = parsed;
      else if (parsed && typeof parsed === "object") taskUuid = parsed.task_uuid || parsed.taskUuid;
    } catch {
      taskUuid = text.replace(/^"|"$/g, "");
    }
  }

  if (!taskUuid) throw new Error("No task_uuid returned from make_image");
  return taskUuid;
}

async function pollTask(token, taskUuid) {
  const maxAttempts = 90;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: "GET",
      headers: {
        "x-token": token,
        "x-platform": "nieta-app/web",
        "content-type": "application/json",
      },
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`poll failed: ${res.status} ${text}`);
    }

    const data = await res.json();
    const status = data.task_status;

    if (status === "PENDING" || status === "MODERATION") continue;

    const url =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;
    if (url) return url;
    throw new Error(`Task finished with status ${status} but no image URL: ${JSON.stringify(data)}`);
  }
  throw new Error("Timed out waiting for image generation");
}

async function main() {
  const args = parseArgs(process.argv);
  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const prompt = args.prompt || DEFAULT_PROMPT;
  const size = args.size || "portrait";

  try {
    const taskUuid = await makeImage({ token: TOKEN, prompt, size, ref: args.ref });
    const url = await pollTask(TOKEN, taskUuid);
    console.log(url);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message}`);
    process.exit(1);
  }
}

main();
