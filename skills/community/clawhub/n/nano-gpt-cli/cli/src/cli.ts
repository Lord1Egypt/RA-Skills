import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";

import { Command } from "commander";

import { NanoGptClient } from "./client.js";
import { readConfig, redactConfig, resolveSettings, setConfigValue, type ConfigKey } from "./config.js";
import {
  normalizeImageGenerationInputs,
  normalizeVideoGenerationImageInput,
  normalizeVideoGenerationVideoInput,
} from "./image-input.js";
import { buildUserMessage } from "./messages.js";
import type {
  AppConfig,
  ChatMessage,
  ImageGenerationResponse,
  VideoGenerationRequest,
  VideoGenerationResponse,
  VideoStatusResponse,
} from "./types.js";

type PromptOptions = {
  model?: string;
  system?: string;
  json?: boolean;
  stream?: boolean;
  image: string[];
};

type ChatOptions = {
  model?: string;
  system?: string;
  json?: boolean;
};

type ModelsOptions = {
  json?: boolean;
};

type ImageOptions = {
  model?: string;
  size?: string;
  quality?: string;
  output?: string;
  json?: boolean;
  image: string[];
};

type VideoOptions = {
  model?: string;
  duration?: string;
  aspectRatio?: string;
  resolution?: string;
  image?: string;
  video?: string;
  output?: string;
  json?: boolean;
  wait?: boolean;
  pollInterval?: string;
  timeout?: string;
};

type VideoStatusOptions = {
  output?: string;
  json?: boolean;
};

type ConfigListOptions = {
  json?: boolean;
};

const CONFIG_KEYS: ConfigKey[] = [
  "api-key",
  "default-model",
  "default-image-model",
  "default-video-model",
  "output-format",
  "base-url",
];

export function createProgram(): Command {
  const program = new Command();

  program
    .name("nano-gpt")
    .description("CLI for NanoGPT text and image APIs")
    .showHelpAfterError();

  program
    .command("prompt")
    .description("Send a one-shot prompt to NanoGPT")
    .argument("[text...]", "Prompt text. Reads stdin when omitted.")
    .option("-m, --model <model>", "Model override")
    .option("-s, --system <prompt>", "System prompt")
    .option("--json", "Print the raw JSON response")
    .option("--no-stream", "Disable streaming text output")
    .option("--image <pathOrUrl>", "Attach an image path or URL", collectValues, [])
    .action(async (textParts: string[], options: PromptOptions) => {
      const prompt = await resolvePromptText(textParts);
      const settings = await resolveSettings({
        defaultModel: options.model,
        outputFormat: options.json ? "json" : undefined,
      });
      ensureApiKey(settings.apiKey);
      const jsonOutput = shouldUseJsonOutput(settings.outputFormat);

      const model = options.model ?? settings.defaultModel;
      const messages = await buildConversation(options.system, prompt, options.image);
      const client = new NanoGptClient(settings);

      if (jsonOutput) {
        const response = await client.createChatCompletion({ model, messages });
        writeJson(response);
        return;
      }

      if (options.stream !== false) {
        let sawOutput = false;
        for await (const chunk of client.streamChatCompletion({ model, messages })) {
          sawOutput = true;
          output.write(chunk);
        }

        if (sawOutput) {
          output.write("\n");
        }
        return;
      }

      const response = await client.createChatCompletion({ model, messages });
      const text = NanoGptClient.extractResponseText(response);
      output.write(`${text}\n`);
    });

  program
    .command("chat")
    .description("Start an interactive NanoGPT session")
    .argument("[text...]", "Optional initial user prompt")
    .option("-m, --model <model>", "Model override")
    .option("-s, --system <prompt>", "System prompt")
    .option("--json", "Print each turn as JSON instead of plain text")
    .action(async (textParts: string[], options: ChatOptions) => {
      const settings = await resolveSettings({
        defaultModel: options.model,
        outputFormat: options.json ? "json" : undefined,
      });
      ensureApiKey(settings.apiKey);
      const jsonOutput = shouldUseJsonOutput(settings.outputFormat);

      const client = new NanoGptClient(settings);
      const history: ChatMessage[] = [];
      if (options.system) {
        history.push({
          role: "system",
          content: options.system,
        });
      }

      let currentModel = options.model ?? settings.defaultModel;
      const initialPrompt = textParts.join(" ").trim();
      if (initialPrompt) {
        await runChatTurn(client, history, currentModel, initialPrompt, jsonOutput);
      }

      const rl = createInterface({ input, output });
      try {
        while (true) {
          const line = (await rl.question("> ")).trim();
          if (!line) {
            continue;
          }

          if (line === "/exit") {
            break;
          }

          if (line === "/clear") {
            history.splice(options.system ? 1 : 0);
            output.write("Conversation cleared.\n");
            continue;
          }

          if (line.startsWith("/model ")) {
            currentModel = line.slice(7).trim();
            output.write(`Model set to ${currentModel}\n`);
            continue;
          }

          await runChatTurn(client, history, currentModel, line, jsonOutput);
        }
      } finally {
        rl.close();
      }
    });

  program
    .command("models")
    .description("List available NanoGPT models")
    .option("--json", "Print the raw JSON response")
    .action(async (options: ModelsOptions) => {
      const settings = await resolveSettings({
        outputFormat: options.json ? "json" : undefined,
      });
      ensureApiKey(settings.apiKey);
      const jsonOutput = shouldUseJsonOutput(settings.outputFormat);

      const client = new NanoGptClient(settings);
      const response = await client.listModels();
      if (jsonOutput) {
        writeJson(response);
        return;
      }

      for (const model of response.data ?? []) {
        output.write(`${model.id ?? "<unknown>"}\n`);
      }
    });

  program
    .command("image")
    .description("Generate or transform an image with NanoGPT")
    .argument("[prompt...]", "Image prompt. Reads stdin when omitted.")
    .option("-m, --model <model>", "Model override")
    .option("--size <size>", "Image size override")
    .option("--quality <quality>", "Image quality override")
    .option("--image <pathOrUrl>", "Source image path, URL, or data URL", collectValues, [])
    .option("-o, --output <path>", "Write the image artifact to a file")
    .option("--json", "Print the raw JSON response")
    .action(async (promptParts: string[], options: ImageOptions) => {
      const prompt = await resolvePromptText(promptParts);
      const settings = await resolveSettings({
        defaultImageModel: options.model,
        outputFormat: options.json ? "json" : undefined,
      });
      ensureApiKey(settings.apiKey);
      const jsonOutput = shouldUseJsonOutput(settings.outputFormat);

      const client = new NanoGptClient(settings);
      const imageInputs = await normalizeImageGenerationInputs(options.image);
      const response = await client.generateImage({
        model: options.model ?? settings.defaultImageModel,
        prompt,
        size: options.size,
        quality: options.quality,
        ...imageInputs,
      });

      const savedPath = options.output
        ? await persistImageOutput(client, response, options.output)
        : undefined;

      if (jsonOutput) {
        writeJson({
          ...response,
          outputPath: savedPath,
        });
        return;
      }

      const first = response.data?.[0];
      if (savedPath) {
        output.write(`${savedPath}\n`);
        return;
      }

      if (first?.url) {
        output.write(`${first.url}\n`);
        return;
      }

      if (first?.b64_json) {
        output.write(`${first.b64_json}\n`);
        return;
      }

      output.write("NanoGPT did not return image data.\n");
    });

  program
    .command("video")
    .description("Generate a video with NanoGPT")
    .argument("[prompt...]", "Video prompt. Reads stdin when omitted.")
    .option("-m, --model <model>", "Model override")
    .option("--duration <duration>", "Video duration, for example 5 or 5s")
    .option("--aspect-ratio <ratio>", "Aspect ratio override")
    .option("--resolution <resolution>", "Resolution override")
    .option("--image <pathOrUrl>", "Condition on an image path, URL, or data URL")
    .option("--video <pathOrUrl>", "Condition on a video path, URL, or data URL")
    .option("-o, --output <path>", "Write the final video artifact to a file")
    .option("--json", "Print the raw JSON response")
    .option("--no-wait", "Return the run id immediately without polling")
    .option("--poll-interval <seconds>", "Polling interval in seconds when waiting", "5")
    .option("--timeout <seconds>", "Maximum seconds to wait for completion")
    .action(async (promptParts: string[], options: VideoOptions) => {
      const prompt = await resolvePromptText(promptParts);
      const settings = await resolveSettings({
        defaultVideoModel: options.model,
        outputFormat: options.json ? "json" : undefined,
      });
      ensureApiKey(settings.apiKey);
      const jsonOutput = shouldUseJsonOutput(settings.outputFormat);

      if (options.image && options.video) {
        throw new Error("Pass either --image or --video for video generation, not both.");
      }

      const client = new NanoGptClient(settings);
      const request = await buildVideoGenerationRequest(
        {
          model: options.model ?? settings.defaultVideoModel,
          prompt,
          duration: options.duration,
          aspect_ratio: options.aspectRatio,
          resolution: options.resolution,
        },
        {
          image: options.image,
          video: options.video,
        },
      );

      const submission = await client.generateVideo(request);
      const requestId = getVideoRequestId(submission);
      if (!requestId) {
        throw new Error("NanoGPT did not return a video request id.");
      }

      if (options.wait === false) {
        if (jsonOutput) {
          writeJson(submission);
        } else {
          output.write(`${requestId}\n`);
        }
        return;
      }

      const status = await pollVideoStatus(client, requestId, {
        pollIntervalMs: parseOptionalSeconds(options.pollInterval, "--poll-interval") ?? 5000,
        timeoutMs: parseOptionalSeconds(options.timeout, "--timeout"),
      });

      const savedPath = options.output
        ? await persistVideoOutput(client, status, options.output)
        : undefined;

      if (jsonOutput) {
        writeJson({
          submission,
          status,
          outputPath: savedPath,
        });
        return;
      }

      if (savedPath) {
        output.write(`${savedPath}\n`);
        return;
      }

      const videoUrl = getVideoOutputUrl(status);
      if (videoUrl) {
        output.write(`${videoUrl}\n`);
        return;
      }

      output.write("NanoGPT completed the video run without a downloadable output URL.\n");
    });

  program
    .command("video-status")
    .description("Inspect the status of an async NanoGPT video run")
    .argument("<requestId>", "Video request id returned by `nano-gpt video --no-wait`")
    .option("-o, --output <path>", "Write the completed video artifact to a file")
    .option("--json", "Print the raw JSON response")
    .action(async (requestId: string, options: VideoStatusOptions) => {
      const settings = await resolveSettings({
        outputFormat: options.json ? "json" : undefined,
      });
      ensureApiKey(settings.apiKey);
      const jsonOutput = shouldUseJsonOutput(settings.outputFormat);

      const client = new NanoGptClient(settings);
      const status = await client.getVideoStatus(requestId);
      assertVideoStatusNotFailed(status, requestId);
      const savedPath = options.output
        ? await persistVideoOutput(client, status, options.output)
        : undefined;

      if (jsonOutput) {
        writeJson({
          ...status,
          outputPath: savedPath,
        });
        return;
      }

      if (savedPath) {
        output.write(`${savedPath}\n`);
        return;
      }

      const videoUrl = getVideoOutputUrl(status);
      if (videoUrl) {
        output.write(`${videoUrl}\n`);
        return;
      }

      output.write(`${getVideoStatusValue(status) ?? "UNKNOWN"}\n`);
    });

  const configCommand = program
    .command("config")
    .description("Manage user configuration");

  configCommand
    .command("set")
    .argument("<key>", `One of: ${CONFIG_KEYS.join(", ")}`)
    .argument("<value>", "Value to store")
    .action(async (key: string, value: string) => {
      assertConfigKey(key);
      await setConfigValue(key, value);
      output.write(`Saved ${key}\n`);
    });

  configCommand
    .command("get")
    .argument("<key>", `One of: ${CONFIG_KEYS.join(", ")}`)
    .action(async (key: string) => {
      assertConfigKey(key);
      const config = await readConfig();
      const mapped = getConfigValue(config, key);
      if (mapped) {
        output.write(`${mapped}\n`);
      }
    });

  configCommand
    .command("list")
    .option("--json", "Print config as JSON")
    .action(async (options: ConfigListOptions) => {
      const config = await readConfig();
      if (options.json) {
        writeJson(redactConfig(config));
        return;
      }

      for (const key of CONFIG_KEYS) {
        const value = getConfigValue(redactConfig(config), key);
        if (value) {
          output.write(`${key}=${value}\n`);
        }
      }
    });

  return program;
}

function collectValues(value: string, previous: string[]): string[] {
  previous.push(value);
  return previous;
}

async function resolvePromptText(textParts: string[]): Promise<string> {
  const inline = textParts.join(" ").trim();
  if (inline) {
    return inline;
  }

  if (!input.isTTY) {
    const chunks: Buffer[] = [];
    for await (const chunk of input) {
      chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
    }
    const stdinText = Buffer.concat(chunks).toString("utf8").trim();
    if (stdinText) {
      return stdinText;
    }
  }

  throw new Error("Prompt text is required. Pass text as an argument or pipe stdin.");
}

async function buildConversation(
  systemPrompt: string | undefined,
  prompt: string,
  imageInputs: string[],
): Promise<ChatMessage[]> {
  const messages: ChatMessage[] = [];
  if (systemPrompt) {
    messages.push({
      role: "system",
      content: systemPrompt,
    });
  }
  messages.push(await buildUserMessage(prompt, imageInputs));
  return messages;
}

async function runChatTurn(
  client: NanoGptClient,
  history: ChatMessage[],
  model: string,
  prompt: string,
  json: boolean,
): Promise<void> {
  history.push({
    role: "user",
    content: prompt,
  });

  if (json) {
    const response = await client.createChatCompletion({ model, messages: history });
    writeJson(response);
    history.push({
      role: "assistant",
      content: NanoGptClient.extractResponseText(response),
    });
    return;
  }

  let assistantText = "";
  for await (const chunk of client.streamChatCompletion({ model, messages: history })) {
    assistantText += chunk;
    output.write(chunk);
  }
  output.write("\n");

  history.push({
    role: "assistant",
    content: assistantText,
  });
}

async function persistImageOutput(
  client: NanoGptClient,
  response: ImageGenerationResponse,
  outputPath: string,
): Promise<string> {
  const absolutePath = resolve(outputPath);
  const image = response.data?.[0];
  if (!image) {
    throw new Error("NanoGPT did not return an image.");
  }

  if (image.b64_json) {
    await mkdir(dirname(absolutePath), { recursive: true });
    await writeFile(absolutePath, Buffer.from(image.b64_json, "base64"));
    return absolutePath;
  }

  if (image.url) {
    await client.downloadToFile(image.url, absolutePath);
    return absolutePath;
  }

  throw new Error("NanoGPT returned an image response without data.");
}

function ensureApiKey(apiKey?: string): asserts apiKey is string {
  if (!apiKey) {
    throw new Error(
      "Missing NanoGPT API key. Set NANO_GPT_API_KEY or run `nano-gpt config set api-key ...`.",
    );
  }
}

function assertConfigKey(key: string): asserts key is ConfigKey {
  if (!CONFIG_KEYS.includes(key as ConfigKey)) {
    throw new Error(`Invalid config key: ${key}`);
  }
}

function getConfigValue(config: AppConfig, key: ConfigKey): string | undefined {
  switch (key) {
    case "api-key":
      return config.apiKey;
    case "default-model":
      return config.defaultModel;
    case "default-image-model":
      return config.defaultImageModel;
    case "default-video-model":
      return config.defaultVideoModel;
    case "output-format":
      return config.outputFormat;
    case "base-url":
      return config.baseUrl;
  }
}

function writeJson(value: unknown): void {
  output.write(`${JSON.stringify(value, null, 2)}\n`);
}

export function shouldUseJsonOutput(outputFormat: AppConfig["outputFormat"]): boolean {
  return outputFormat === "json";
}

export function getVideoRequestId(
  submission: Pick<VideoGenerationResponse, "requestId" | "runId">,
): string | undefined {
  return submission.requestId ?? submission.runId;
}

export function getVideoStatusValue(status: VideoStatusResponse): string | undefined {
  return status.data?.status;
}

export function getVideoErrorMessage(status: VideoStatusResponse): string | undefined {
  return status.data?.userFriendlyError ?? status.data?.error;
}

export function getVideoPollDelay(
  elapsedMs: number,
  pollIntervalMs: number,
  timeoutMs?: number,
): number {
  if (timeoutMs === undefined) {
    return pollIntervalMs;
  }

  const remainingMs = timeoutMs - elapsedMs;
  if (remainingMs <= 0) {
    return 0;
  }

  return Math.min(pollIntervalMs, remainingMs);
}

async function buildVideoGenerationRequest(
  request: VideoGenerationRequest,
  inputs: {
    image?: string;
    video?: string;
  },
): Promise<VideoGenerationRequest> {
  const [imageInput, videoInput] = await Promise.all([
    normalizeVideoGenerationImageInput(inputs.image),
    normalizeVideoGenerationVideoInput(inputs.video),
  ]);

  return {
    ...request,
    ...imageInput,
    ...videoInput,
  };
}

async function pollVideoStatus(
  client: NanoGptClient,
  requestId: string,
  options: {
    pollIntervalMs: number;
    timeoutMs?: number;
  },
): Promise<VideoStatusResponse> {
  const startedAt = Date.now();

  while (true) {
    const status = await client.getVideoStatus(requestId);
    if (handleCompletedVideoStatus(status, requestId)) {
      return status;
    }

    const delayMs = getVideoPollDelay(Date.now() - startedAt, options.pollIntervalMs, options.timeoutMs);
    if (delayMs <= 0) {
      throw new Error(`Timed out waiting for NanoGPT video run ${requestId}.`);
    }

    await sleep(delayMs);
  }
}

async function persistVideoOutput(
  client: NanoGptClient,
  status: VideoStatusResponse,
  outputPath: string,
): Promise<string> {
  const currentStatus = getVideoStatusValue(status);
  if (currentStatus !== "COMPLETED") {
    throw new Error(
      `Cannot write video output while NanoGPT status is ${currentStatus ?? "UNKNOWN"}.`,
    );
  }

  const videoUrl = getVideoOutputUrl(status);
  if (!videoUrl) {
    throw new Error("NanoGPT completed the video run without an output URL.");
  }

  const absolutePath = resolve(outputPath);
  await client.downloadToFile(videoUrl, absolutePath);
  return absolutePath;
}

function getVideoOutputUrl(status: VideoStatusResponse): string | undefined {
  return status.data?.output?.video?.url;
}

function handleCompletedVideoStatus(
  status: VideoStatusResponse,
  requestId: string,
): boolean {
  const currentStatus = getVideoStatusValue(status);
  switch (currentStatus) {
    case "COMPLETED":
      return true;
    case "FAILED":
      throw new Error(getVideoErrorMessage(status) ?? `NanoGPT video run failed: ${requestId}`);
    case "PENDING":
    case "PROCESSING":
    case "QUEUED":
    case "IN_QUEUE":
    case "IN_PROGRESS":
    case undefined:
      return false;
    default:
      throw new Error(`Unexpected NanoGPT video status: ${currentStatus}`);
  }
}

function assertVideoStatusNotFailed(
  status: VideoStatusResponse,
  requestId: string,
): void {
  if (getVideoStatusValue(status) !== "FAILED") {
    return;
  }

  throw new Error(getVideoErrorMessage(status) ?? `NanoGPT video run failed: ${requestId}`);
}

function parseOptionalSeconds(value: string | undefined, flagName: string): number | undefined {
  if (value === undefined) {
    return undefined;
  }

  const seconds = Number(value);
  if (!Number.isFinite(seconds) || seconds <= 0) {
    throw new Error(`${flagName} must be a positive number of seconds.`);
  }

  return Math.round(seconds * 1000);
}
