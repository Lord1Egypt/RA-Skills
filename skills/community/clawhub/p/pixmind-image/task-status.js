const API_BASE = 'https://aihub-admin.aimix.pro';

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help')) {
  console.log(`
Usage: node task-status.js --task-id <id> [--poll] [--interval <ms>]

Options:
  --task-id <id>   (required) Task ID from generate response
  --poll           Keep polling until task completes
  --interval <ms>  Poll interval in ms (default: 3000)
`);
  process.exit(0);
}

function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      if (args[i] === '--poll') {
        opts.poll = true;
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
        opts[key] = args[++i];
      }
    }
  }
  return opts;
}

const opts = parseArgs(args);

if (!opts.taskId) {
  console.error('Error: --task-id is required');
  process.exit(1);
}

const apiKey = process.env.PIXMIND_API_KEY;
if (!apiKey) {
  console.error('Error: PIXMIND_API_KEY not set. Get one at https://www.pixmind.io/api-keys');
  process.exit(1);
}

const poll = opts.poll;
const interval = parseInt(opts.interval) || 3000;

async function checkStatus() {
  const res = await fetch(`${API_BASE}/open-api/v1/task/${opts.taskId}`, {
    headers: { 'X-API-Key': apiKey },
  });
  return res.json();
}

async function pollStatus() {
  while (true) {
    const result = await checkStatus();
    const data = result.data || result;

    const status = data.status || 'unknown';
    const progress = data.progress || 0;
    console.log(`[${new Date().toISOString()}] Status: ${status} | Progress: ${progress}%`);

    if (status === 'ready' || status === 'success' || status === 'completed') {
      if (data.images) console.log('Image URLs:', data.images);
      if (data.videoUrl) console.log('Video URL:', data.videoUrl);
      if (data.coverUrl) console.log('Cover URL:', data.coverUrl);
      break;
    }

    if (status === 'failed' || status === 'error') {
      console.error('Task failed:', data.errorMessage || 'Unknown error');
      process.exit(1);
    }

    await new Promise(r => setTimeout(r, interval));
  }
}

if (poll) {
  await pollStatus();
} else {
  const result = await checkStatus();
  console.log(JSON.stringify(result, null, 2));
}
