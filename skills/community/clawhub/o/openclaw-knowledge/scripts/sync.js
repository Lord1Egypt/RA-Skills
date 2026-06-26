import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const BASE_URL = 'https://docs.openclaw.ai';
const OUTPUT_DIR = path.join(__dirname, '..', 'docs');
const MANIFEST_FILE = path.join(__dirname, '..', '.scrape-manifest.json');

const args = process.argv.slice(2);
const FORCE_MODE = args.includes('--force') || args.includes('-f');
const SHOW_STATS = args.includes('--stats');
const PARALLEL = parseInt(args.find(a => a.startsWith('--parallel='))?.split('=')[1]) || 5;
const DELAY = parseInt(args.find(a => a.startsWith('--delay='))?.split('=')[1]) || 100;

async function fetchPage(url) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);

    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      signal: controller.signal
    });

    clearTimeout(timeout);

    if (!response.ok) {
      console.error(`HTTP error: ${response.status}`);
      return null;
    }

    const content = await response.text();
    const etag = response.headers.get('etag') || response.headers.get('last-modified');

    return { content, etag };
  } catch (error) {
    console.error(`Error fetching ${url}: ${error.message}`);
    return null;
  }
}

function parseLlmsTxt(content) {
  const docs = [];
  const lines = content.split('\n');

  for (const line of lines) {
    const linkMatch = line.match(/^\s*-\s*\[([^\]]+)\]\((https:\/\/docs\.openclaw\.ai\/([^)]+\.md))\)/);
    if (linkMatch) {
      const title = linkMatch[1];
      const url = linkMatch[2];

      const pathMatch = url.match(/https:\/\/docs\.openclaw\.ai\/([^/]+)\/([^/]+)\.md/);
      if (pathMatch) {
        const category = pathMatch[1];
        const docName = pathMatch[2];
        docs.push({ title, url, category, docName });
      } else {
        const rootMatch = url.match(/https:\/\/docs\.openclaw\.ai\/([^/]+)\.md/);
        if (rootMatch) {
          const docName = rootMatch[1];
          docs.push({ title, url, category: 'root', docName });
        }
      }
    }
  }

  return docs;
}

async function loadManifest() {
  try {
    const data = await fs.readFile(MANIFEST_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

async function saveManifest(manifest) {
  await fs.writeFile(MANIFEST_FILE, JSON.stringify(manifest, null, 2), 'utf-8');
}

async function saveDoc(category, docName, content, url, title, etag) {
  const categoryDir = path.join(OUTPUT_DIR, category);
  await fs.mkdir(categoryDir, { recursive: true });

  const filePath = path.join(categoryDir, `${docName}.md`);

  const cleanContent = content
    .replace(/<AgentInstructions>[\s\S]*?<\/AgentInstructions>/gi, '')
    .replace(/^>\s*##\s*Documentation Index[\s\S]*?(?=\n#)/gm, '')
    .replace(/^\s*<!--[\s\S]*?-->\s*$/gm, '')
    .replace(/^>\s*##\s*Submitting Feedback[\s\S]*$/gm, '')
    .trim();

  const frontmatter = `---
title: "${title || docName}"
category: "${category}"
source: "${url}"
---

`;

  await fs.writeFile(filePath, frontmatter + '\n' + cleanContent, 'utf-8');

  return { category, docName, etag, url };
}

async function main() {
  console.log('OpenClaw Documentation Sync');
  console.log('='.repeat(40));
  console.log(`Base URL: ${BASE_URL}`);
  console.log(`Output Directory: ${OUTPUT_DIR}`);
  console.log(`Force Mode: ${FORCE_MODE ? 'ON' : 'OFF'}`);
  console.log(`Parallel: ${PARALLEL}, Delay: ${DELAY}ms`);
  console.log('');

  if (SHOW_STATS) {
    const manifest = await loadManifest();
    const docs = Object.values(manifest);
    const categories = [...new Set(docs.map(d => d.category))];
    console.log('Current manifest statistics:');
    console.log(`  Total documents: ${docs.length}`);
    for (const cat of categories) {
      const count = docs.filter(d => d.category === cat).length;
      console.log(`  - ${cat}: ${count} docs`);
    }
    return;
  }

  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  console.log('Fetching document index from llms.txt...');
  const llmsContent = await fetchPage(`${BASE_URL}/llms.txt`);

  if (!llmsContent) {
    console.error('Failed to fetch llms.txt');
    process.exit(1);
  }

  const docs = parseLlmsTxt(llmsContent.content);
  console.log(`Found ${docs.length} documents\n`);

  const manifest = await loadManifest();
  const existingUrls = new Set(Object.keys(manifest));

  const newDocs = docs.filter(d => !existingUrls.has(d.url));

  console.log('Document categories found:');
  const categories = [...new Set(docs.map(d => d.category))];
  for (const cat of categories) {
    const count = docs.filter(d => d.category === cat).length;
    console.log(`  - ${cat}: ${count} docs`);
  }
  console.log('');

  if (!FORCE_MODE) {
    console.log(`New documents: ${newDocs.length}`);
    console.log(`Existing documents: ${docs.length - newDocs.length}`);
    console.log('');
  }

  let newCount = 0;
  let updatedCount = 0;
  let skippedCount = 0;
  let failCount = 0;

  async function fetchDoc(doc) {
    const existingEntry = manifest[doc.url];
    const isUpdate = !!existingEntry;

    if (!FORCE_MODE && existingEntry) {
      skippedCount++;
      return;
    }

    const result = await fetchPage(doc.url);

    if (result) {
      await saveDoc(doc.category, doc.docName, '\n' + result.content + '\n', doc.url, doc.title, result.etag);

      manifest[doc.url] = {
        category: doc.category,
        docName: doc.docName,
        etag: result.etag,
        url: doc.url,
        title: doc.title,
        scrapedAt: new Date().toISOString()
      };

      if (isUpdate) {
        updatedCount++;
        console.log(`  -> Updated: ${doc.category}/${doc.docName}.md`);
      } else {
        newCount++;
        console.log(`  -> Saved: ${doc.category}/${doc.docName}.md`);
      }
    } else {
      console.log(`  -> Failed: ${doc.category}/${doc.docName}.md`);
      failCount++;
    }
  }

  async function processBatch(batch) {
    await Promise.all(batch.map(doc => fetchDoc(doc)));
    await saveManifest(manifest);
  }

  const batches = [];
  for (let i = 0; i < docs.length; i += PARALLEL) {
    batches.push(docs.slice(i, i + PARALLEL));
  }

  console.log(`Processing in ${batches.length} batches...\n`);

  for (let i = 0; i < batches.length; i++) {
    const batch = batches[i];
    await processBatch(batch);
    console.log(`Batch ${i + 1}/${batches.length} completed`);
    await new Promise(resolve => setTimeout(resolve, DELAY));
  }

  await saveManifest(manifest);

  console.log('\n' + '='.repeat(40));
  console.log('Sync completed!');
  console.log(`Total docs in index: ${docs.length}`);
  console.log(`New: ${newCount}, Updated: ${updatedCount}, Skipped: ${skippedCount}, Failed: ${failCount}`);
}

main().catch(console.error);
