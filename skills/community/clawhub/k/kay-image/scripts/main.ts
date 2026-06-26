#!/usr/bin/env bun
/**
 * Kay Image - AI Image Generation & Understanding Tool
 * Supports nano-banana-2 model for text-to-image and image-to-image
 * Supports GPT-5, Gemini 2.5 Pro/Flash for image/video understanding
 * 
 * API Endpoints:
 * - KIE AI (Generation):
 *   - Create Task: POST /api/v1/jobs/createTask
 *   - Query Task: GET /api/v1/jobs/recordInfo?taskId={taskId}
 * - LaoZhang AI (Understanding):
 *   - Chat Completions: POST /v1/chat/completions
 */

import { parseArgs } from "util";
import { readFileSync, existsSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";

// API Configuration
const KIE_API_BASE = process.env.KIE_BASE_URL || "https://api.kie.ai";
const KIE_API_KEY = process.env.KIE_API_KEY;

const LAOZHANG_API_BASE = process.env.LAOZHANG_BASE_URL || "https://api.laozhang.ai/v1";
const LAOZHANG_API_KEY = process.env.LAOZHANG_API_KEY;

// API Source for understanding mode
const UNDERSTANDING_API_BASE = process.env.KIE_UNDERSTANDING_BASE_URL || "https://api.kie.ai";
const UNDERSTANDING_API_KEY = process.env.KIE_UNDERSTANDING_API_KEY;

// Parse command line arguments
const { values, positionals } = parseArgs({
  args: Bun.argv,
  options: {
    prompt: { type: "string", short: "p" },
    output: { type: "string", short: "o" },
    input: { type: "string", short: "i" },
    ar: { type: "string", default: "1:1" },
    resolution: { type: "string", short: "r", default: "1K" },
    format: { type: "string", short: "f", default: "jpg" },
    model: { type: "string", short: "m", default: "nano-banana-2" },
    "google-search": { type: "boolean", default: false },
    taskId: { type: "string", short: "t" },
    query: { type: "boolean", short: "q", default: false },
    wait: { type: "boolean", short: "w", default: true },
    noWait: { type: "boolean", default: false },
    "max-attempts": { type: "string", default: "60" },
    "poll-interval": { type: "string", default: "5" },
    // Understanding mode
    understand: { type: "boolean", short: "u", default: false },
    image: { type: "string", multiple: true },
    video: { type: "string" },
    "vision-model": { type: "string" },
    "max-tokens": { type: "string", default: "1000" },
    "use-laozhang": { type: "boolean", default: false },  // Use LaoZhang API instead of KIE for understanding
    help: { type: "boolean", short: "h" },
  },
  strict: true,
  allowPositionals: true,
});

// Show help
if (values.help) {
  console.log(`
Kay Image - AI Image Generation & Understanding Tool

USAGE:
  kay-image [options]                    # Generate image from prompt
  kay-image -q -t <taskId>               # Query existing task status
  kay-image -u --image <url>             # Understand image content
  kay-image -u --video <url>             # Understand video content

OPTIONS:
  Generation:
    -p, --prompt <text>       Image generation prompt (required for generation)
    -o, --output <path>       Output image path (required)
    -i, --input <path>        Input reference image URL (optional, for img2img)
    --ar <ratio>              Aspect ratio: 1:1, 3:4, 16:9, etc. (default: 1:1)
    -r, --resolution <size>   Resolution: 1K/2K/4K (default: 1K)
    -f, --format <format>     Output format: jpg/png (default: jpg)
    -m, --model <name>        Model name (default: nano-banana-2)
    --google-search           Enable Google search grounding

  Understanding:
    -u, --understand          Enable understanding mode
    --image <url/path>        Image URL or path (can be used multiple times)
    --video <url/path>        Video URL or path
    --vision-model <model>    Vision model: gpt-5, gemini-2.5-pro, gemini-2.5-flash, gemini-3.1-pro
                              Default: gpt-5 (image), gemini-2.5-pro (video)
    --max-tokens <n>          Max output tokens (default: 1000)
    --use-laozhang            Use LaoZhang API instead of KIE for understanding

  Query:
    -q, --query               Query mode: check task status
    -t, --taskId <id>         Task ID to query
    -w, --wait                Wait for completion (default: true)
    --no-wait                 Don't wait, check once and exit
    --max-attempts <n>        Max poll attempts (default: 60)
    --poll-interval <sec>     Poll interval in seconds (default: 5)

  Other:
    -h, --help                Show this help

EXAMPLES:
  # Generate image
  kay-image -p "a cute cat" -o cat.png
  kay-image -p "sunset" -o sunset.png --ar 16:9 -r 2K
  kay-image -p "anime style" -i https://example.com/photo.jpg -o anime.png

  # Understand image (default: KIE API with gemini-3.1-pro)
  kay-image -u --image https://example.com/photo.jpg -p "describe this image"
  kay-image -u --image photo.jpg -p "extract all text" --vision-model gemini-3.1-pro

  # Understand video (default: KIE API with gemini-3.1-pro)
  kay-image -u --video https://example.com/video.mp4 -p "summarize this video"

  # Use LaoZhang API for understanding (instead of KIE)
  kay-image -u --image https://example.com/photo.jpg -p "describe this" --use-laozhang
  kay-image -u --video https://example.com/video.mp4 -p "analyze this" --use-laozhang --vision-model gemini-2.5-pro

  # Query task status
  kay-image -q -t <taskId>
  kay-image -q -t <taskId> --noWait

ENVIRONMENT:
  KIE_API_KEY                   Required for image generation
  KIE_UNDERSTANDING_API_KEY     Required for image/video understanding (default)
  LAOZHANG_API_KEY              Required for image/video understanding with --use-laozhang
`);
  process.exit(0);
}

// Supported aspect ratios
const VALID_AR = ["1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9", "auto"];

// Supported resolutions
const VALID_RES = ["1K", "2K", "4K"];

// Supported formats
const VALID_FORMAT = ["jpg", "png"];

// Default vision models
const DEFAULT_IMAGE_MODEL = "gpt-5";
const DEFAULT_VIDEO_MODEL = "gemini-2.5-pro";

/**
 * Validate generation parameters
 */
function validateGenerationParams(): void {
  if (!values.prompt) {
    console.error("❌ Error: --prompt is required for image generation");
    console.error("Use -h for help");
    process.exit(1);
  }

  if (!values.output) {
    console.error("❌ Error: --output is required");
    console.error("Use -h for help");
    process.exit(1);
  }

  if (!VALID_AR.includes(values.ar)) {
    console.error(`❌ Error: Invalid aspect ratio "${values.ar}"`);
    console.error(`Valid options: ${VALID_AR.join(", ")}`);
    process.exit(1);
  }

  if (!VALID_RES.includes(values.resolution)) {
    console.error(`❌ Error: Invalid resolution "${values.resolution}"`);
    console.error(`Valid options: ${VALID_RES.join(", ")}`);
    process.exit(1);
  }

  if (!VALID_FORMAT.includes(values.format.toLowerCase())) {
    console.error(`❌ Error: Invalid format "${values.format}"`);
    console.error(`Valid options: ${VALID_FORMAT.join(", ")}`);
    process.exit(1);
  }

  if (!KIE_API_KEY) {
    console.error("❌ Error: KIE_API_KEY environment variable is required for image generation");
    console.error("Set it with: export KIE_API_KEY='your-api-key'");
    process.exit(1);
  }
}

/**
 * Validate understanding parameters
 */
function validateUnderstandingParams(): void {
  const useLaozhang = values["use-laozhang"];

  if (useLaozhang) {
    // LaoZhang API for understanding
    if (!LAOZHANG_API_KEY) {
      console.error("❌ Error: LAOZHANG_API_KEY environment variable is required for LaoZhang understanding");
      console.error("Set it with: export LAOZHANG_API_KEY='your-api-key'");
      process.exit(1);
    }
  } else {
    // KIE API for understanding (default)
    if (!UNDERSTANDING_API_KEY) {
      console.error("❌ Error: KIE_UNDERSTANDING_API_KEY environment variable is required for understanding");
      console.error("Set it with: export KIE_UNDERSTANDING_API_KEY='your-api-key'");
      console.error("Or use --use-laozhang to use LaoZhang API instead");
      process.exit(1);
    }
  }

  const images = values.image || [];
  const video = values.video;

  if (images.length === 0 && !video) {
    console.error("❌ Error: --image or --video is required for understanding mode");
    console.error("Use -h for help");
    process.exit(1);
  }

  if (!values.prompt) {
    console.error("❌ Error: --prompt is required for understanding mode");
    console.error("Use -h for help");
    process.exit(1);
  }

  // Validate video model
  if (video) {
    const model = values["vision-model"] || "gemini-3.1-pro";
    if (!model.startsWith("gemini")) {
      console.error(`❌ Error: Video understanding requires Gemini models`);
      console.error(`Supported models: gemini-3.1-pro, gemini-2.5-pro, gemini-2.5-flash`);
      process.exit(1);
    }
  }
}

/**
 * Validate query parameters
 */
function validateQueryParams(): void {
  if (!values.taskId) {
    console.error("❌ Error: --taskId is required for query mode");
    console.error("Use -h for help");
    process.exit(1);
  }
}

/**
 * Convert file to base64
 */
async function fileToBase64(filePath: string): Promise<{ data: string; mimeType: string }> {
  const resolvedPath = resolve(filePath);
  if (!existsSync(resolvedPath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  const buffer = readFileSync(resolvedPath);
  const data = buffer.toString("base64");
  
  // Detect mime type from extension
  const ext = filePath.split(".").pop()?.toLowerCase();
  const mimeTypes: Record<string, string> = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    webp: "image/webp",
    gif: "image/gif",
    mp4: "video/mp4",
    mov: "video/quicktime",
    avi: "video/x-msvideo",
    mkv: "video/x-matroska",
  };
  
  const mimeType = mimeTypes[ext || ""] || "application/octet-stream";
  return { data, mimeType };
}

/**
 * Create image generation task
 * POST /api/v1/jobs/createTask
 */
async function createTask(): Promise<string> {
  const url = `${KIE_API_BASE}/api/v1/jobs/createTask`;
  
  const body: any = {
    model: values.model,
    input: {
      prompt: values.prompt,
      aspect_ratio: values.ar,
      resolution: values.resolution,
      output_format: values.format.toLowerCase(),
      google_search: values["google-search"] || false,
    },
  };

  // Handle input image
  if (values.input) {
    if (values.input.startsWith("http")) {
      body.input.image_input = [values.input];
    } else {
      console.error("⚠️  Local file detected. Please upload to a public URL first.");
      console.error("   Or use a URL: -i https://example.com/image.jpg");
      throw new Error("Local files not supported");
    }
  }

  console.log(`🎨 Creating task...`);
  console.log(`   Model: ${values.model}`);
  console.log(`   Resolution: ${values.resolution}`);
  console.log(`   Aspect Ratio: ${values.ar}`);
  console.log(`   Format: ${values.format}`);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${KIE_API_KEY}`,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error: ${response.status} - ${error}`);
  }

  const data = await response.json();
  
  if (data.code !== 200) {
    throw new Error(`API Error: ${data.message}`);
  }

  return data.data.taskId;
}

/**
 * Query task status
 * GET /api/v1/jobs/recordInfo?taskId={taskId}
 */
async function queryTaskStatus(taskId: string): Promise<{
  state: string;
  resultUrl?: string;
  failMsg?: string;
  costTime?: number;
}> {
  const url = `${KIE_API_BASE}/api/v1/jobs/recordInfo?taskId=${encodeURIComponent(taskId)}`;
  
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${KIE_API_KEY}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Query failed: ${response.status}`);
  }

  const data = await response.json();
  
  if (data.code !== 200) {
    throw new Error(`Query error: ${data.message}`);
  }

  const task = data.data;
  
  // Parse result if available
  let resultUrl: string | undefined;
  if (task.resultJson) {
    try {
      const result = JSON.parse(task.resultJson);
      resultUrl = result.resultUrls?.[0];
    } catch (e) {
      // Ignore parse error
    }
  }

  return {
    state: task.state,
    resultUrl,
    failMsg: task.failMsg,
    costTime: task.costTime,
  };
}

/**
 * Poll task until completion
 */
async function pollTask(taskId: string): Promise<string> {
  const maxAttempts = parseInt(values["max-attempts"] || "60");
  const interval = parseInt(values["poll-interval"] || "5") * 1000;

  console.log(`⏳ Polling task: ${taskId}`);
  console.log(`   Max attempts: ${maxAttempts}`);
  console.log(`   Interval: ${interval / 1000}s`);

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const status = await queryTaskStatus(taskId);

    if (status.state === "success") {
      if (status.resultUrl) {
        console.log(`\n✅ Task completed!`);
        console.log(`   Cost time: ${status.costTime}s`);
        return status.resultUrl;
      } else {
        throw new Error("Task succeeded but no result URL found");
      }
    }

    if (status.state === "fail") {
      throw new Error(`Task failed: ${status.failMsg || "Unknown error"}`);
    }

    // Still processing
    process.stdout.write(`\r⏳ Waiting... (${attempt}/${maxAttempts}) - State: ${status.state}`);
    await new Promise((resolve) => setTimeout(resolve, interval));
  }

  throw new Error("Timeout: Task took too long to complete");
}

/**
 * Query mode: check task status
 */
async function queryMode(): Promise<void> {
  validateQueryParams();
  
  const taskId = values.taskId!;
  const shouldWait = values.wait && !values.noWait;

  if (shouldWait) {
    // Poll until completion
    const imageUrl = await pollTask(taskId);
    console.log(`\n📎 Result URL: ${imageUrl}`);
    
    // Download if output is specified
    if (values.output) {
      const outputPath = resolve(values.output);
      console.log(`💾 Downloading to ${outputPath}...`);
      await downloadFile(imageUrl, outputPath);
      console.log(`✅ Saved to: ${outputPath}`);
    }
  } else {
    // Check once
    const status = await queryTaskStatus(taskId);
    console.log(`📊 Task Status: ${taskId}`);
    console.log(`   State: ${status.state}`);
    if (status.resultUrl) {
      console.log(`   Result: ${status.resultUrl}`);
    }
    if (status.failMsg) {
      console.log(`   Error: ${status.failMsg}`);
    }
    if (status.costTime) {
      console.log(`   Cost time: ${status.costTime}s`);
    }
  }
}

/**
 * Download file from URL
 */
async function downloadFile(url: string, outputPath: string): Promise<void> {
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Download failed: ${response.status}`);
  }

  const buffer = await response.arrayBuffer();
  writeFileSync(outputPath, new Uint8Array(buffer));
}

/**
 * Generation mode: create task and wait for completion
 */
async function generationMode(): Promise<void> {
  validateGenerationParams();

  // Create task
  const taskId = await createTask();
  console.log(`✅ Task created: ${taskId}`);

  // Wait for completion
  const imageUrl = await pollTask(taskId);
  console.log(`\n✅ Image generated!`);
  console.log(`   URL: ${imageUrl}`);

  // Download image
  const outputPath = resolve(values.output!);
  console.log(`💾 Downloading to ${outputPath}...`);
  await downloadFile(imageUrl, outputPath);

  console.log(`✅ Done! Saved to: ${outputPath}`);
}

/**
 * Understanding mode: analyze image or video
 */
async function understandingMode(): Promise<void> {
  validateUnderstandingParams();

  const images = values.image || [];
  const video = values.video;
  const isVideo = !!video;
  const useLaozhang = values["use-laozhang"];

  // Determine model
  let model = values["vision-model"];
  if (!model) {
    if (useLaozhang) {
      // LaoZhang API default models
      model = isVideo ? DEFAULT_VIDEO_MODEL : DEFAULT_IMAGE_MODEL;
    } else {
      // KIE API default models (default)
      model = "gemini-3.1-pro";
    }
  }

  console.log(`🔍 Understanding mode`);
  console.log(`   API: ${useLaozhang ? "LaoZhang" : "KIE"}`);
  console.log(`   Model: ${model}`);
  if (images.length > 0) {
    console.log(`   Images: ${images.length}`);
  }
  if (video) {
    console.log(`   Video: ${video}`);
  }

  // Build content array
  const content: any[] = [];

  // Add text prompt
  content.push({
    type: "text",
    text: values.prompt,
  });

  // Add images
  for (const img of images) {
    if (img.startsWith("http")) {
      content.push({
        type: "image_url",
        image_url: { url: img },
      });
    } else {
      // Local file - convert to base64
      const { data, mimeType } = await fileToBase64(img);
      content.push({
        type: "image_url",
        image_url: { url: `data:${mimeType};base64,${data}` },
      });
    }
  }

  // Add video
  if (video) {
    if (video.startsWith("http")) {
      content.push({
        type: "image_url",
        image_url: { url: video },
      });
    } else {
      // Local file - convert to base64
      const { data, mimeType } = await fileToBase64(video);
      content.push({
        type: "image_url",
        image_url: { url: `data:${mimeType};base64,${data}` },
      });
    }
  }

  // Determine API endpoint and credentials
  const apiBase = useLaozhang ? LAOZHANG_API_BASE : UNDERSTANDING_API_BASE;
  const apiKey = useLaozhang ? LAOZHANG_API_KEY : UNDERSTANDING_API_KEY;
  const apiName = useLaozhang ? "LaoZhang" : "KIE";

  // Call API
  const url = `${apiBase}/v1/chat/completions`;
  const body = {
    model: model,
    messages: [
      {
        role: "user",
        content: content,
      },
    ],
    max_tokens: parseInt(values["max-tokens"] || "1000"),
  };

  console.log(`\n📡 Sending request to ${apiName} API...`);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error: ${response.status} - ${error}`);
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(`API Error: ${data.error.message}`);
  }

  const result = data.choices?.[0]?.message?.content;

  if (!result) {
    throw new Error("No response content received");
  }

  console.log(`\n✅ Analysis complete!\n`);
  console.log(result);

  // Save to file if output specified
  if (values.output) {
    const outputPath = resolve(values.output);
    writeFileSync(outputPath, result, "utf-8");
    console.log(`\n💾 Saved to: ${outputPath}`);
  }
}

/**
 * Main function
 */
async function main() {
  try {
    if (values.understand) {
      await understandingMode();
    } else if (values.query) {
      await queryMode();
    } else {
      await generationMode();
    }
  } catch (error: any) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
