#!/usr/bin/env node
import path from "node:path";

import {
  buildImagePayload,
  createImageTask,
  extractTaskId,
  resolveConfig,
  saveImageOutputs,
  warnOrRequireSkillUpdate,
  waitForImage,
} from "./lib/gpt-image-2.mjs";

function parseArgs(argv) {
  const options = {
    aspectRatio: "auto",
    outputDir: "outputs",
  };
  const promptParts = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      options.help = true;
    } else if (arg === "--model") {
      options.model = argv[++i];
    } else if (arg === "--prompt" || arg === "-p") {
      options.prompt = argv[++i];
    } else if (arg === "--aspect-ratio" || arg === "--aspect") {
      options.aspectRatio = argv[++i];
    } else if (arg === "--resolution") {
      options.resolution = argv[++i];
    } else if (arg === "--input-url" || arg === "--input-urls" || arg === "--input-image-url") {
      if (!options.inputUrls) options.inputUrls = [];
      options.inputUrls.push(argv[++i]);
    } else if (arg === "--output-dir" || arg === "-o") {
      options.outputDir = argv[++i];
    } else if (arg === "--no-save") {
      options.save = false;
    } else if (arg === "--no-wait") {
      options.wait = false;
    } else if (arg?.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      promptParts.push(arg);
    }
  }

  if (!options.prompt && promptParts.length > 0) {
    options.prompt = promptParts.join(" ");
  }

  return options;
}

function printHelp() {
  console.log(`Usage:
  hiapi-gpt-image-2 --prompt "Create a product poster" --aspect-ratio 16:9

Options:
      --model           gpt-image-2, gpt-image-2-pro,
                        gpt-image-2-image-to-image, or gpt-image-2-image-to-image-pro.
                        Default: gpt-image-2
  -p, --prompt          Image prompt. Positional prompt text is also accepted.
      --aspect-ratio    auto, 1:1, 3:2, 2:3, 4:3, 3:4, 5:4, 4:5,
                        16:9, 9:16, 2:1, 1:2, 3:1, 1:3, 21:9, or 9:21.
                        Default: auto
      --resolution      1K, 2K, or 4K. Default: 1K
      --input-url       Repeatable. Required 1-5 times for image-to-image models.
  -o, --output-dir      Directory for generated image files. Default: outputs
      --no-save         Return remote URLs or data URIs without writing files
      --no-wait         Create the task and return the task id
  -h, --help            Show this help

Environment:
  HIAPI_API_KEY         Required HiAPI API key
  HIAPI_BASE_URL        Optional, defaults to https://api.hiapi.ai`);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  await warnOrRequireSkillUpdate();

  const config = resolveConfig();
  const payload = buildImagePayload({
    model: options.model,
    prompt: options.prompt,
    aspectRatio: options.aspectRatio,
    resolution: options.resolution,
    inputUrls: options.inputUrls,
  });

  const created = await createImageTask(payload, { config });
  const taskId = extractTaskId(created);
  if (!taskId) {
    throw new Error(`No image task id returned: ${JSON.stringify(created)}`);
  }

  if (options.wait === false) {
    console.log(
      JSON.stringify(
        {
          model: payload.model,
          taskId,
          status: "created",
          aspectRatio: payload.input.aspect_ratio,
          resolution: payload.input.resolution,
          outputs: [],
        },
        null,
        2,
      ),
    );
    return;
  }

  const { response, outputs } = await waitForImage(taskId, { config });
  const savedOutputs = options.save === false
    ? outputs.map((output) => output.kind === "url"
      ? { kind: "url", url: output.value }
      : { kind: "data-uri", value: output.value, mimeType: output.mimeType })
    : await saveImageOutputs(outputs, {
      outputDir: path.resolve(process.cwd(), options.outputDir),
    });

  console.log(
    JSON.stringify(
      {
        model: payload.model,
        taskId,
        aspectRatio: payload.input.aspect_ratio,
        resolution: payload.input.resolution,
        outputs: savedOutputs,
        rawStatus: response,
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
