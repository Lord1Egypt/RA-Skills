const API_BASE = 'https://aihub-admin.aimix.pro';

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help')) {
  console.log(`
Usage: node image-generate.js <options>

Options:
  --prompt <text>        (required) Image generation prompt
  --model <name>         Model name (default: seedream-4.0)
  --aspect-ratio <ratio> Aspect ratio like 16:9, 1:1 (default: 1:1)
  --count <n>            Number of images 1-4 (default: 1)
  --enhance              Enable prompt enhancement
  --type <type>          text2img or img2img (default: text2img)
  --image <url>          Reference image URL (for img2img)

Examples:
  node image-generate.js --prompt "a cute cat"
  node image-generate.js --prompt "oil painting" --model imagen-4-ultra --aspect-ratio 16:9 --count 2
`);
  process.exit(0);
}

function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      if (args[i] === '--enhance') {
        opts.enhancePrompt = true;
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        opts[key] = args[++i];
      }
    }
  }
  return opts;
}

const opts = parseArgs(args);

if (!opts.prompt) {
  console.error('Error: --prompt is required');
  process.exit(1);
}

const apiKey = process.env.PIXMIND_API_KEY;
if (!apiKey) {
  console.error('Error: PIXMIND_API_KEY not set. Get one at https://www.pixmind.io/api-keys');
  process.exit(1);
}

const body = {
  prompt: opts.prompt,
  model: opts.model || 'seedream-4.0',
  aspectRatio: opts.aspectRatio || '1:1',
  sampleCount: parseInt(opts.count) || 1,
  enhancePrompt: opts.enhancePrompt || false,
  generateType: opts.type || 'text2img',
};

if (opts.image) body.image = opts.image;

console.log('Generating image...');
console.log('Prompt:', body.prompt);
console.log('Model:', body.model);

const res = await fetch(`${API_BASE}/open-api/v1/image/generate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify(body),
});
const result = await res.json();
console.log('\nResult:', JSON.stringify(result, null, 2));
