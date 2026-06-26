#!/usr/bin/env node
/**
 * Poster Generation Script
 * 
 * Generates posters using Gemini image generation API.
 * Supports templates, custom prompts, and multiple output formats.
 * 
 * Usage:
 *   node generate-poster.js --template event --title "My Event" --date "2026-01-01"
 *   node generate-poster.js --prompt "Custom poster description" --output ./poster.png
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load .env file if present
const envPath = path.join(__dirname, '..', '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim();
      if (!process.env[key]) process.env[key] = value;
    }
  });
}

// Configuration
const CONFIG = {
  apiEndpoint: 'generativelanguage.googleapis.com',
  apiPath: '/v1beta/models/',
  defaultModel: 'gemini-3.1-flash-image-preview',
  maxRetries: 3,
  baseDelayMs: 1000,
  // Load default output path from system config
  defaultOutputPath: '/workspace/openclaw-data/exports',
};

// Template definitions
const TEMPLATES = {
  event: {
    name: 'Event Poster',
    defaultPrompt: `A professional event poster design, {style}, featuring:
- Central {imageSubject} illustration
- Clean space for event details text
- {colorScheme} color palette
- Balanced composition with clear visual hierarchy
- Modern event poster aesthetic suitable for digital and print
- Professional typography layout`,
    defaults: {
      style: 'modern minimalist',
      imageSubject: 'abstract geometric patterns',
      colorScheme: 'deep blues and golds',
    },
  },
  concert: {
    name: 'Concert/Music Poster',
    defaultPrompt: `A dynamic concert poster in {style}, featuring:
- {genre}-inspired visual elements
- {imageSubject} as central artwork
- Bold composition suitable for music promotion
- {colorScheme} with high contrast
- Energetic design conveying live music atmosphere
- Music poster aesthetic inspired by {referenceStyle}`,
    defaults: {
      style: 'bold and vibrant',
      genre: 'indie rock',
      imageSubject: 'electric guitar and sound waves',
      colorScheme: 'electric purple and neon pink on black',
      referenceStyle: 'modern gig posters',
    },
  },
  product: {
    name: 'Product Showcase',
    defaultPrompt: `A premium product showcase poster for {productType}, {style}:
- Professional product photography style composition
- {backgroundType} background
- Elegant lighting highlighting product features
- {colorScheme} color palette
- Clean minimalist space for text overlay
- High-end e-commerce aesthetic
- Luxury brand advertisement style`,
    defaults: {
      productType: 'premium electronics',
      style: 'minimalist and elegant',
      backgroundType: 'clean gradient',
      colorScheme: 'matte black and silver',
    },
  },
  sale: {
    name: 'Sale/Promotional',
    defaultPrompt: `An attention-grabbing sale poster, {style}:
- Dynamic composition with strong visual impact
- {colorScheme} creating urgency and excitement
- {imageSubject} as focal point
- Space for large bold promotional text
- High-energy retail advertisement aesthetic
- Modern promotional design`,
    defaults: {
      style: 'bold and energetic',
      colorScheme: 'vibrant red and gold',
      imageSubject: 'exploding confetti and shopping elements',
    },
  },
  announcement: {
    name: 'Announcement/Launch',
    defaultPrompt: `A sophisticated announcement poster, {style}:
- Clean and professional composition
- {imageSubject} as central visual element
- {colorScheme} conveying innovation and trust
- Corporate announcement aesthetic
- Space for clear text hierarchy
- Modern tech company launch style`,
    defaults: {
      style: 'corporate and modern',
      imageSubject: 'abstract geometric shapes suggesting innovation',
      colorScheme: 'navy blue and white with gold accents',
    },
  },
  social: {
    name: 'Social Media',
    defaultPrompt: `An engaging social media post design, {style}:
- Optimized for {platform} with {aspectRatio} aspect ratio
- Eye-catching visual composition
- {colorScheme} color palette
- {imageSubject} as central element
- Modern social media aesthetic
- High engagement potential design`,
    defaults: {
      style: 'trendy and engaging',
      platform: 'Instagram',
      aspectRatio: '1:1 square',
      colorScheme: 'vibrant gradient',
      imageSubject: 'stylized lifestyle imagery',
    },
  },
};

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    template: 'event',
    output: './poster.png',
    aspectRatio: '1:1',
    imageSize: '2K',
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    switch (arg) {
      case '--template':
      case '-t':
        options.template = nextArg;
        i++;
        break;
      case '--prompt':
      case '-p':
        options.customPrompt = nextArg;
        i++;
        break;
      case '--output':
      case '-o':
        options.output = nextArg;
        i++;
        break;
      case '--title':
        options.title = nextArg;
        i++;
        break;
      case '--date':
        options.date = nextArg;
        i++;
        break;
      case '--venue':
        options.venue = nextArg;
        i++;
        break;
      case '--aspect-ratio':
      case '-a':
        options.aspectRatio = nextArg;
        i++;
        break;
      case '--size':
      case '-s':
        options.imageSize = nextArg;
        i++;
        break;
      case '--style':
        options.style = nextArg;
        i++;
        break;
      case '--color':
        options.colorScheme = nextArg;
        i++;
        break;
      case '--model':
      case '-m':
        options.model = nextArg;
        i++;
        break;
      case '--json':
        options.jsonOutput = true;
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
    }
  }

  return options;
}

function showHelp() {
  console.log(`
Poster Generator - Gemini Image Generation

Usage:
  node generate-poster.js [options]

Options:
  --template, -t          Template name: event, concert, product, sale, announcement, social
  --prompt, -p            Custom prompt (overrides template)
  --title                 Event/product title
  --date                  Event date
  --venue                 Event venue
  --style                 Visual style description
  --color                 Color scheme description
  --aspect-ratio, -a      Aspect ratio: 1:1, 4:3, 16:9, 9:16, 3:4 (default: 1:1)
  --size, -s              Image size: 1K, 2K, 4K (default: 2K)
  --model, -m             Gemini model to use
  --output, -o            Output file path (default: ./poster.png)
  --json                  Output JSON with metadata
  --help, -h              Show this help

Templates:
  event        General event poster
  concert      Music/concert poster
  product      Product showcase
  sale         Sale/promotional poster
  announcement Launch/announcement poster
  social       Social media optimized

Examples:
  node generate-poster.js --template event --title "Summer Festival" --date "July 15"
  node generate-poster.js --template concert --title "Live at The Fillmore" --style "vintage rock"
  node generate-poster.js --prompt "Minimalist coffee shop poster, warm tones, clean typography"
`);
}

// Build prompt from template and options
function buildPrompt(options) {
  if (options.customPrompt) {
    return options.customPrompt;
  }

  const template = TEMPLATES[options.template];
  if (!template) {
    throw new Error(`Unknown template: ${options.template}. Available: ${Object.keys(TEMPLATES).join(', ')}`);
  }

  let prompt = template.defaultPrompt;
  const vars = { ...template.defaults, ...options };

  // Replace template variables
  for (const [key, value] of Object.entries(vars)) {
    if (value && typeof value === 'string') {
      prompt = prompt.replace(new RegExp(`{${key}}`, 'g'), value);
    }
  }

  // Add aspect ratio context
  prompt += `\nAspect ratio: ${options.aspectRatio}.`;

  // Add size context
  prompt += `\nImage quality: ${options.imageSize} resolution.`;

  // Add poster-specific context
  if (options.title) {
    prompt += `\nInclude visual elements that complement "${options.title}".`;
  }

  return prompt;
}

// Map aspect ratio to Gemini-supported ratio
function mapAspectRatio(ratio) {
  const supported = ['1:1', '4:3', '16:9', '9:16', '3:4'];
  if (supported.includes(ratio)) return ratio;
  
  // Map common ratios
  const ratioMap = {
    'square': '1:1',
    'landscape': '16:9',
    'portrait': '9:16',
    'instagram': '1:1',
    'story': '9:16',
    'facebook': '16:9',
  };
  
  return ratioMap[ratio] || '1:1';
}

// Generate image using Gemini API
async function generateImage(prompt, options) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error('GEMINI_API_KEY not set. Set it as an environment variable.');
  }

  const model = options.model || CONFIG.defaultModel;
  const aspectRatio = mapAspectRatio(options.aspectRatio);

  const requestBody = {
    contents: [{
      role: 'user',
      parts: [{ text: prompt }],
    }],
    generationConfig: {
      responseModalities: ['TEXT', 'IMAGE'],
    },
  };

  const path = `${CONFIG.apiPath}${model}:generateContent?key=${apiKey}`;

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: CONFIG.apiEndpoint,
      path: path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          
          if (response.error) {
            reject(new Error(`API error: ${response.error.message}`));
            return;
          }

          // Extract image from response
          const candidates = response.candidates || [];
          if (candidates.length === 0) {
            reject(new Error('No candidates in response'));
            return;
          }

          const parts = candidates[0].content?.parts || [];
          const imagePart = parts.find(p => p.inlineData);

          if (!imagePart) {
            // Check for text-only response
            const textPart = parts.find(p => p.text);
            if (textPart) {
              reject(new Error(`Text response received (no image): ${textPart.text}`));
            } else {
              reject(new Error('No image data in response'));
            }
            return;
          }

          resolve({
            imageData: imagePart.inlineData.data,
            mimeType: imagePart.inlineData.mimeType,
            prompt: prompt,
            model: model,
            aspectRatio: aspectRatio,
          });
        } catch (err) {
          reject(new Error(`Failed to parse response: ${err.message}`));
        }
      });
    });

    req.on('error', (err) => reject(new Error(`Request failed: ${err.message}`)));
    req.write(JSON.stringify(requestBody));
    req.end();
  });
}

// Retry wrapper with exponential backoff
async function generateImageWithRetry(prompt, options) {
  let lastError;
  
  for (let attempt = 1; attempt <= CONFIG.maxRetries; attempt++) {
    try {
      console.error(`[Attempt ${attempt}/${CONFIG.maxRetries}] Generating image...`);
      const result = await generateImage(prompt, options);
      return result;
    } catch (err) {
      lastError = err;
      console.error(`[Attempt ${attempt}] Failed: ${err.message}`);
      
      if (attempt < CONFIG.maxRetries) {
        const delay = CONFIG.baseDelayMs * Math.pow(2, attempt - 1);
        console.error(`Waiting ${delay}ms before retry...`);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }
  
  throw lastError;
}

// Save image to file
function saveImage(imageData, outputPath) {
  const buffer = Buffer.from(imageData, 'base64');
  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Main function
async function main() {
  try {
    const options = parseArgs();
    
    console.error('Building prompt...');
    const prompt = buildPrompt(options);
    console.error(`Prompt:\n${prompt}\n`);

    console.error('Generating image...');
    const result = await generateImageWithRetry(prompt, options);

    // Save image
    const outputPath = path.resolve(options.output || path.join(CONFIG.defaultOutputPath, 'poster.png'));
    // Ensure output directory exists
    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    saveImage(result.imageData, outputPath);

    // Output result
    if (options.jsonOutput) {
      console.log(JSON.stringify({
        success: true,
        outputPath: outputPath,
        mimeType: result.mimeType,
        model: result.model,
        aspectRatio: result.aspectRatio,
        prompt: result.prompt,
        fileSize: fs.statSync(outputPath).size,
      }, null, 2));
    } else {
      console.error(`\n✓ Image saved to: ${outputPath}`);
      console.error(`  Format: ${result.mimeType}`);
      console.error(`  Size: ${(fs.statSync(outputPath).size / 1024).toFixed(1)} KB`);
      console.error(`  Model: ${result.model}`);
      console.error(`  Aspect ratio: ${result.aspectRatio}`);
      
      // Output path for piping/other tools
      console.log(outputPath);
    }

  } catch (err) {
    console.error(`\n✗ Error: ${err.message}`);
    process.exit(1);
  }
}

main();
