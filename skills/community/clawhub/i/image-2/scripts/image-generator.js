/**
 * Image2 Skill - GPT-4o Image Generation & Editing
 *
 * Supports GPT-4o native image generation (gpt-image-2) and DALL-E 3.
 * Includes prompt enhancement, local save, and batch operations.
 */

const OpenAI = require('openai');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ─── Configuration ───────────────────────────────────────────────
const DEFAULTS = {
  model: 'gpt-image-2',
  size: '1024x1024',
  quality: 'standard',
  style: 'vivid',
  saveDir: './generated-images',
  maxRetries: 2,
  retryDelay: 1000
};

const VALID_SIZES = ['1024x1024', '1024x1792', '1792x1024'];
const VALID_MODELS = ['gpt-image-2', 'dall-e-3'];

// ─── OpenAI Client ───────────────────────────────────────────────
let openai = null;

function getClient() {
  if (!openai) {
    if (!process.env.OPENAI_API_KEY) {
      throw new Error('OPENAI_API_KEY environment variable is not set. Please set it before using image-2.');
    }
    openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }
  return openai;
}

// ─── Utility Functions ───────────────────────────────────────────

/**
 * Ensure the save directory exists
 */
function ensureSaveDir(dir) {
  const saveDir = dir || DEFAULTS.saveDir;
  if (!fs.existsSync(saveDir)) {
    fs.mkdirSync(saveDir, { recursive: true });
  }
  return saveDir;
}

/**
 * Generate a unique filename
 */
function generateFilename(prefix = 'image', ext = 'png') {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}.${ext}`;
}

/**
 * Download image from URL to local file
 * @param {string} url - Image URL
 * @param {string} savePath - Local file path to save to
 * @returns {Promise<string>} - Saved file path
 */
async function downloadImage(url, savePath) {
  const dir = path.dirname(savePath);
  ensureSaveDir(dir);

  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        return downloadImage(response.headers.location, savePath).then(resolve).catch(reject);
      }
      if (response.statusCode !== 200) {
        return reject(new Error(`Download failed with status ${response.statusCode}`));
      }
      const stream = fs.createWriteStream(savePath);
      response.pipe(stream);
      stream.on('finish', () => {
        stream.close();
        resolve(savePath);
      });
      stream.on('error', reject);
    }).on('error', reject);
  });
}

/**
 * Convert a local file or URL to base64
 * @param {string} source - File path or URL
 * @returns {Promise<string>} - Base64 encoded string
 */
async function toBase64(source) {
  if (fs.existsSync(source)) {
    const buffer = fs.readFileSync(source);
    return buffer.toString('base64');
  }
  // If it's a URL, fetch and convert
  const client = source.startsWith('https') ? https : http;
  return new Promise((resolve, reject) => {
    client.get(source, (response) => {
      const chunks = [];
      response.on('data', chunk => chunks.push(chunk));
      response.on('end', () => {
        const buffer = Buffer.concat(chunks);
        resolve(buffer.toString('base64'));
      });
      response.on('error', reject);
    }).on('error', reject);
  });
}

/**
 * Validate and normalize options
 */
function normalizeOptions(options = {}) {
  const model = VALID_MODELS.includes(options.model) ? options.model : DEFAULTS.model;
  const size = VALID_SIZES.includes(options.size) ? options.size : DEFAULTS.size;
  const quality = ['standard', 'hd'].includes(options.quality) ? options.quality : DEFAULTS.quality;
  const style = ['vivid', 'natural'].includes(options.style) ? options.style : DEFAULTS.style;
  return { model, size, quality, style };
}

/**
 * Retry wrapper for API calls
 */
async function withRetry(fn, maxRetries = DEFAULTS.maxRetries) {
  let lastError;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (error.status === 429 && attempt < maxRetries) {
        const delay = DEFAULTS.retryDelay * Math.pow(2, attempt);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
  throw lastError;
}

// ─── Prompt Enhancement ──────────────────────────────────────────

const QUALITY_BOOSTERS = {
  general: 'professional quality, high resolution, sharp details',
  product: 'studio lighting, clean background, commercial photography, professional product shot',
  portrait: 'professional portrait photography, natural lighting, shallow depth of field',
  social: 'eye-catching, vibrant colors, modern design, trending aesthetic',
  illustration: 'detailed illustration, professional artist quality, clean lines',
  logo: 'clean vector style, scalable, minimal details, professional brand identity',
  architecture: 'architectural visualization, realistic rendering, professional quality',
  food: 'appetizing, professional food styling, restaurant quality, steam visible',
  ui: 'clean design, modern interface, pixel-perfect, professional mockup',
  landscape: 'breathtaking scenery, golden hour lighting, ultra detailed, 8K quality',
  fashion: 'high fashion editorial, Vogue quality, dramatic composition, professional model',
  abstract: 'contemporary art gallery quality, visually striking, sophisticated composition'
};

/**
 * Auto-detect the image category from the prompt
 */
function detectCategory(prompt) {
  const lower = prompt.toLowerCase();
  if (/product|商品|产品|item|goods/.test(lower)) return 'product';
  if (/portrait|人像|头像|headshot|person/.test(lower)) return 'portrait';
  if (/social|social.media|instagram|post|海报|宣传图/.test(lower)) return 'social';
  if (/illustration|插画|drawing|sketch|artwork/.test(lower)) return 'illustration';
  if (/logo|商标|brand|品牌/.test(lower)) return 'logo';
  if (/architecture|建筑|building|interior|室内|房间/.test(lower)) return 'architecture';
  if (/food|美食|dish|餐|cake|drink|beverage/.test(lower)) return 'food';
  if (/ui|ux|interface|界面|app|website|mockup/.test(lower)) return 'ui';
  if (/landscape|风景|scenery|mountain|ocean|sunset/.test(lower)) return 'landscape';
  if (/fashion|时尚|outfit|clothing|dress|穿搭/.test(lower)) return 'fashion';
  if (/abstract|抽象|pattern|texture|gradient/.test(lower)) return 'abstract';
  return 'general';
}

/**
 * Enhance a user prompt with quality boosters
 */
function enhancePrompt(prompt, category = null) {
  const detectedCategory = category || detectCategory(prompt);
  const booster = QUALITY_BOOSTERS[detectedCategory] || QUALITY_BOOSTERS.general;

  // Don't duplicate if similar terms already exist
  const lower = prompt.toLowerCase();
  const boosterWords = booster.toLowerCase().split(', ');
  const newWords = boosterWords.filter(word => !lower.includes(word.split(' ')[0]));

  if (newWords.length === 0) return prompt;
  return `${prompt}, ${newWords.join(', ')}`;
}

// ─── Core API Functions ──────────────────────────────────────────

/**
 * Generate an image from a text description
 * @param {string} prompt - The description of the image to generate
 * @param {Object} options - Generation options
 * @param {boolean} options.autoEnhance - Whether to auto-enhance the prompt (default: true)
 * @returns {Promise<Object>} - { success, url, localPath, revisedPrompt, enhancedPrompt }
 */
async function generateImage(prompt, options = {}) {
  const {
    autoEnhance = true,
    saveTo = null,
    category = null
  } = options;

  const { model, size, quality, style } = normalizeOptions(options);
  const enhancedPrompt = autoEnhance ? enhancePrompt(prompt, category) : prompt;

  try {
    const client = getClient();

    const result = await withRetry(async () => {
      if (model === 'gpt-image-2') {
        // GPT-4o native image generation via chat completions
        const response = await client.chat.completions.create({
          model: 'gpt-4o',
          messages: [
            {
              role: 'user',
              content: [
                {
                  type: 'text',
                  text: `Generate an image: ${enhancedPrompt}`
                }
              ]
            }
          ],
          // Note: GPT-4o image generation parameters may vary
          // This uses the chat completions endpoint with image output
        });

        // Extract image from response
        const content = response.choices[0]?.message?.content;
        if (typeof content === 'string') {
          // If it's text, try to find image URL or base64
          const urlMatch = content.match(/https?:\/\/[^\s"')]+/);
          if (urlMatch) {
            return { url: urlMatch[0], revised_prompt: enhancedPrompt };
          }
        }
        // Fallback to DALL-E if GPT-4o doesn't return an image directly
        return await generateWithDallE(enhancedPrompt, { ...options, model: 'dall-e-3' });
      } else {
        return await generateWithDallE(enhancedPrompt, { ...options, model, size, quality, style });
      }
    });

    // Save to local file
    let localPath = null;
    if (result.url) {
      const saveDir = ensureSaveDir(saveTo ? path.dirname(saveTo) : DEFAULTS.saveDir);
      const filename = saveTo ? path.basename(saveTo) : generateFilename('gen', 'png');
      localPath = path.join(saveDir, filename);
      await downloadImage(result.url, localPath);
    }

    return {
      success: true,
      url: result.url,
      localPath,
      revisedPrompt: result.revised_prompt || enhancedPrompt,
      enhancedPrompt
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      enhancedPrompt
    };
  }
}

/**
 * Internal: Generate with DALL-E API
 */
async function generateWithDallE(prompt, options = {}) {
  const { model = 'dall-e-3', size = '1024x1024', quality = 'standard', style = 'vivid' } = options;
  const client = getClient();

  const response = await client.images.generate({
    model,
    prompt,
    n: 1,
    size,
    quality,
    style
  });

  return {
    url: response.data[0].url,
    revised_prompt: response.data[0].revised_prompt
  };
}

/**
 * Edit an existing image
 * @param {string} imagePath - Path or URL to the source image
 * @param {string} prompt - Edit instruction
 * @param {Object} options - Edit options
 * @returns {Promise<Object>} - { success, url, localPath }
 */
async function editImage(imagePath, prompt, options = {}) {
  const {
    maskPath = null,
    saveTo = null
  } = options;

  const { model, size } = normalizeOptions(options);

  try {
    const client = getClient();
    const result = await withRetry(async () => {
      if (model === 'gpt-image-2') {
        // GPT-4o native image editing via chat completions with image input
        const base64 = await toBase64(imagePath);
        const mimeType = imagePath.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';

        const userContent = [
          {
            type: 'image_url',
            image_url: { url: `data:${mimeType};base64,${base64}` }
          },
          {
            type: 'text',
            text: `Edit this image: ${prompt}`
          }
        ];

        if (maskPath) {
          const maskBase64 = await toBase64(maskPath);
          const maskMime = maskPath.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
          userContent.unshift({
            type: 'image_url',
            image_url: { url: `data:${maskMime};base64,${maskBase64}` }
          });
        }

        const response = await client.chat.completions.create({
          model: 'gpt-4o',
          messages: [{ role: 'user', content: userContent }]
        });

        const content = response.choices[0]?.message?.content;
        if (typeof content === 'string') {
          const urlMatch = content.match(/https?:\/\/[^\s"')]+/);
          if (urlMatch) return { url: urlMatch[0] };
        }

        // Fallback to DALL-E edit
        return await editWithDallE(imagePath, prompt, { maskPath, size });
      } else {
        return await editWithDallE(imagePath, prompt, { maskPath, size });
      }
    });

    let localPath = null;
    if (result.url) {
      const saveDir = ensureSaveDir(saveTo ? path.dirname(saveTo) : DEFAULTS.saveDir);
      const filename = saveTo ? path.basename(saveTo) : generateFilename('edit', 'png');
      localPath = path.join(saveDir, filename);
      await downloadImage(result.url, localPath);
    }

    return { success: true, url: result.url, localPath };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Internal: Edit with DALL-E API
 */
async function editWithDallE(imagePath, prompt, options = {}) {
  const { maskPath = null, size = '1024x1024' } = options;
  const client = getClient();

  const params = {
    model: 'dall-e-3',
    image: fs.existsSync(imagePath) ? fs.createReadStream(imagePath) : imagePath,
    prompt,
    n: 1,
    size
  };

  if (maskPath && fs.existsSync(maskPath)) {
    params.mask = fs.createReadStream(maskPath);
  }

  const response = await client.images.edit(params);
  return { url: response.data[0].url };
}

/**
 * Generate variations of an image
 * @param {string} imagePath - Path to the source image
 * @param {Object} options - Variation options
 * @returns {Promise<Object>} - { success, variations: [{ url, localPath }] }
 */
async function generateVariations(imagePath, options = {}) {
  const {
    count = 2,
    saveTo = null
  } = options;

  const { size } = normalizeOptions(options);
  const n = Math.min(Math.max(count, 1), 4);

  try {
    const client = getClient();

    if (!fs.existsSync(imagePath)) {
      throw new Error(`Image file not found: ${imagePath}`);
    }

    const response = await withRetry(async () => {
      return await client.images.createVariation({
        model: 'dall-e-2',
        image: fs.createReadStream(imagePath),
        n,
        size
      });
    });

    const saveDir = ensureSaveDir(saveTo ? path.dirname(saveTo) : DEFAULTS.saveDir);
    const variations = [];

    for (let i = 0; i < response.data.length; i++) {
      const img = response.data[i];
      const filename = saveTo
        ? `${path.basename(saveTo, path.extname(saveTo))}_${i + 1}${path.extname(saveTo)}`
        : generateFilename(`var_${i + 1}`, 'png');
      const localPath = path.join(saveDir, filename);
      await downloadImage(img.url, localPath);
      variations.push({ url: img.url, localPath });
    }

    return { success: true, variations };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Describe/analyze an image using GPT-4o Vision
 * @param {string} imageSource - File path or URL of the image
 * @param {string} question - Specific question about the image (optional)
 * @returns {Promise<Object>} - { success, description }
 */
async function describeImage(imageSource, question = null) {
  try {
    const client = getClient();

    // Prepare image content
    let imageUrl;
    if (fs.existsSync(imageSource)) {
      const base64 = await toBase64(imageSource);
      const ext = path.extname(imageSource).toLowerCase();
      const mime = ext === '.png' ? 'image/png' : ext === '.webp' ? 'image/webp' : 'image/jpeg';
      imageUrl = `data:${mime};base64,${base64}`;
    } else {
      imageUrl = imageSource; // Assume it's a URL
    }

    const textContent = question || 'Please describe this image in detail, including objects, colors, composition, mood, and any text visible.';

    const response = await client.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'image_url', image_url: { url: imageUrl } },
            { type: 'text', text: textContent }
          ]
        }
      ],
      max_tokens: 1000
    });

    return {
      success: true,
      description: response.choices[0].message.content
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ─── Batch Operations ────────────────────────────────────────────

/**
 * Generate multiple images in batch
 * @param {Array<string>} prompts - Array of prompt strings
 * @param {Object} options - Shared generation options
 * @returns {Promise<Object>} - { success, results: [...] }
 */
async function batchGenerate(prompts, options = {}) {
  const results = [];
  const concurrency = options.concurrency || 2;

  // Process in batches to avoid rate limits
  for (let i = 0; i < prompts.length; i += concurrency) {
    const batch = prompts.slice(i, i + concurrency);
    const batchResults = await Promise.all(
      batch.map(prompt => generateImage(prompt, options))
    );
    results.push(...batchResults);

    // Small delay between batches
    if (i + concurrency < prompts.length) {
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }

  return {
    success: results.every(r => r.success),
    results,
    total: results.length,
    succeeded: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length
  };
}

// ─── Exports ─────────────────────────────────────────────────────

module.exports = {
  generateImage,
  editImage,
  generateVariations,
  describeImage,
  downloadImage,
  batchGenerate,
  enhancePrompt,
  detectCategory,
  VALID_SIZES,
  VALID_MODELS,
  QUALITY_BOOSTERS,
  DEFAULTS
};
