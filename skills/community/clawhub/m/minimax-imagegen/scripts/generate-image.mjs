#!/usr/bin/env node
/**
 * MiniMax Image Generation via image-01 model
 * API: POST https://api.minimax.io/v1/image_generation
 * 
 * Response contains image URLs — script downloads the first one as PNG.
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

const API_KEY = process.env.MINIMAX_API_KEY;
const API_BASE = 'https://api.minimax.io';

function getApiKey() {
  if (API_KEY) return API_KEY;
  console.error('Error: MINIMAX_API_KEY environment variable is not set.');
  process.exit(1);
}

function getArg(arg, defaultVal) {
  const idx = process.argv.indexOf(arg);
  if (idx !== -1 && process.argv[idx + 1] !== undefined) return process.argv[idx + 1];
  return defaultVal;
}

const prompt = process.argv[2];
if (!prompt) {
  console.error('Usage: node generate-image.mjs "<prompt>" [--output <path>] [--model <model>]');
  process.exit(1);
}

const defaultOutputDir = `${process.env.HOME}/.openclaw/workspace/images`;
mkdirSync(defaultOutputDir, { recursive: true });
const outputPath = getArg('--output', `${defaultOutputDir}/minimax-image-${Date.now()}.png`);
const model = getArg('--model', 'image-01');
const apiKey = getApiKey();

async function generate() {
  // Step 1: Generate — get image URLs
  const genRes = await fetch(`${API_BASE}/v1/image_generation`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model, prompt }),
  });

  if (!genRes.ok) {
    const text = await genRes.text();
    throw new Error(`Generation API error ${genRes.status}: ${text}`);
  }

  const genData = await genRes.json();
  const imageUrl = genData?.data?.image_urls?.[0];
  if (!imageUrl) {
    throw new Error(`No image URL in response: ${JSON.stringify(genData)}`);
  }

  // Step 2: Download the image
  const imgRes = await fetch(imageUrl);
  if (!imgRes.ok) {
    throw new Error(`Failed to download image: ${imgRes.status} ${imgRes.statusText}`);
  }

  const buffer = Buffer.from(await imgRes.arrayBuffer());
  mkdirSync(dirname(outputPath), { recursive: true });
  writeFileSync(outputPath, buffer);

  const result = {
    success: true,
    path: outputPath,
    revisedPrompt: genData?.data?.revised_prompt || prompt,
    model,
    imageUrl,
    sizeBytes: buffer.length,
  };

  console.log(JSON.stringify(result));
}

generate().catch(err => {
  console.error('ERROR:', err.message);
  process.exit(1);
});
