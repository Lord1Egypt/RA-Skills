const API_BASE = 'https://aihub-admin.aimix.pro';

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help')) {
  console.log(`
Usage: node video-generate.js <options>

Options:
  --prompt <text>        (required) Video generation prompt
  --model <name>         Model name
  --duration <seconds>   Video duration in seconds
  --aspect-ratio <ratio> Aspect ratio like 16:9, 9:16
  --resolution <res>     Resolution like 1080p, 720p
  --type <type>          text2video or img2video (default: text2video)
  --image <url>          Reference image URL (for img2video)

Examples:
  node video-generate.js --prompt "ocean waves crashing on rocks" --duration 5 --aspect-ratio 16:9
  node video-generate.js --prompt "camera pans left" --type img2video --image https://example.com/img.jpg
`);
  process.exit(0);
}

function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
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
  generateType: opts.type || 'text2video',
};

if (opts.model) body.model = opts.model;
if (opts.duration) body.duration = parseFloat(opts.duration);
if (opts.aspectRatio) body.aspectRatio = opts.aspectRatio;
if (opts.resolution) body.resolution = opts.resolution;
if (opts.image) body.imageUrl = opts.image;

console.log('Generating video...');
console.log('Prompt:', body.prompt);
if (body.model) console.log('Model:', body.model);

const res = await fetch(`${API_BASE}/open-api/v1/video/generate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify(body),
});
const result = await res.json();
console.log('\nResult:', JSON.stringify(result, null, 2));
