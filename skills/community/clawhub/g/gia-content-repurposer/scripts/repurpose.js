#!/usr/bin/env node
/**
 * Content Repurposer — Transform long-form content into multi-platform posts
 *
 * Usage:
 *   node repurpose.js --url "https://example.com/post" --formats twitter,linkedin
 *   node repurpose.js --file ./article.md --formats all
 *   cat article.md | node repurpose.js --formats twitter,newsletter
 *
 * Requires: An LLM API (OpenAI, Anthropic, or local) for generation.
 *   Set OPENAI_API_KEY or ANTHROPIC_API_KEY in environment.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf8')) : {};

function parseArgs() {
  const args = { formats: ['all'] };
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--url') args.url = process.argv[++i];
    if (process.argv[i] === '--file') args.file = process.argv[++i];
    if (process.argv[i] === '--formats') args.formats = process.argv[++i].split(',');
    if (process.argv[i] === '--output') args.output = process.argv[++i];
  }
  return args;
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : require('http');
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

function httpPost(url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const data = JSON.stringify(body);
    const req = https.request({
      hostname: u.hostname, path: u.pathname, method: 'POST',
      headers: { 'Content-Type': 'application/json', ...headers }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve(JSON.parse(d)));
    });
    req.on('error', reject);
    req.write(data); req.end();
  });
}

// Extract readable text from HTML (basic)
function extractText(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, 8000); // Limit to ~8K chars for LLM context
}

// Generate content using OpenAI or Anthropic
async function generateWithLLM(prompt, systemPrompt) {
  const openaiKey = process.env.OPENAI_API_KEY;
  const anthropicKey = process.env.ANTHROPIC_API_KEY;

  if (openaiKey) {
    const res = await httpPost('https://api.openai.com/v1/chat/completions', {
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: prompt }
      ],
      max_tokens: 2000,
      temperature: 0.7
    }, { 'Authorization': 'Bearer ' + openaiKey });
    return res.choices?.[0]?.message?.content || '';
  }

  if (anthropicKey) {
    const res = await httpPost('https://api.anthropic.com/v1/messages', {
      model: 'claude-3-5-haiku-20241022',
      max_tokens: 2000,
      system: systemPrompt,
      messages: [{ role: 'user', content: prompt }]
    }, { 'x-api-key': anthropicKey, 'anthropic-version': '2023-06-01' });
    return res.content?.[0]?.text || '';
  }

  console.error('No LLM API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY.');
  process.exit(1);
}

const FORMAT_PROMPTS = {
  twitter: `Create a Twitter/X thread (${config.maxTweets || 6} tweets max).
Rules:
- Tweet 1 = hook (question, bold claim, or stat)
- Each tweet stands alone but builds the narrative
- Last tweet = CTA
- Number each tweet [1/N]
- Max 280 chars per tweet
- Use line breaks for readability
Tone: ${config.tone || 'casual'}`,

  linkedin: `Create a LinkedIn post.
Rules:
- Opening line = scroll-stopper
- Single-line paragraphs with spacing
- Include a personal take or lesson
- End with a question for comments
- 3-5 hashtags at the bottom
- 500-1500 characters total
Tone: ${config.tone || 'professional'}`,

  newsletter: `Create an email newsletter section.
Rules:
- 3 subject line options
- Opening hook → key insights → action items → sign-off
- Bold **key takeaways** for skimmers
- Under 800 words
- Include a TL;DR at the top
Tone: ${config.tone || 'educational'}`,

  instagram: `Create an Instagram caption.
Rules:
- Hook in first line (before "more" cut)
- 200-400 characters
- Relevant emoji (don't overdo)
- 5-10 hashtags at the end
- CTA (save this, share with a friend, etc.)
Tone: ${config.tone || 'casual'}`,

  summary: `Create a TL;DR summary.
Rules:
- 3-5 bullet points
- Each bullet = one key insight or takeaway
- Actionable where possible
- Under 200 words total`
};

async function repurpose(content, formats) {
  const allFormats = formats.includes('all') ? Object.keys(FORMAT_PROMPTS) : formats;
  const results = {};

  for (const fmt of allFormats) {
    if (!FORMAT_PROMPTS[fmt]) {
      console.log(`⚠️  Unknown format: ${fmt}`);
      continue;
    }
    console.log(`📝 Generating ${fmt}...`);
    const result = await generateWithLLM(
      `Repurpose the following content:\n\n${content}`,
      FORMAT_PROMPTS[fmt]
    );
    results[fmt] = result;
    console.log(`✅ ${fmt} done (${result.length} chars)\n`);
  }

  return results;
}

async function main() {
  const args = parseArgs();
  let content = '';

  if (args.url) {
    console.log(`🔗 Fetching ${args.url}...`);
    const html = await httpGet(args.url);
    content = extractText(html);
  } else if (args.file) {
    content = fs.readFileSync(args.file, 'utf8');
  } else {
    // Read from stdin
    content = fs.readFileSync('/dev/stdin', 'utf8');
  }

  if (!content.trim()) {
    console.error('No content provided. Use --url, --file, or pipe via stdin.');
    process.exit(1);
  }

  console.log(`📄 Content loaded (${content.length} chars)\n`);

  const results = await repurpose(content, args.formats);

  // Output
  const outputDir = args.output || './repurposed';
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  for (const [fmt, text] of Object.entries(results)) {
    const outFile = path.join(outputDir, `${fmt}.md`);
    fs.writeFileSync(outFile, `# ${fmt.charAt(0).toUpperCase() + fmt.slice(1)}\n\n${text}\n`);
    console.log(`💾 Saved ${outFile}`);
  }

  // Also print to stdout
  console.log('\n' + '='.repeat(60));
  for (const [fmt, text] of Object.entries(results)) {
    console.log(`\n## ${fmt.toUpperCase()}\n`);
    console.log(text);
    console.log('\n' + '-'.repeat(40));
  }
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
