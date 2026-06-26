#!/usr/bin/env node
/**
 * Update knowledge base for openclaw-doctor-pro skill
 * 
 * Features:
 * - Check if remote docs have updates (based on sitemap lastmod)
 * - Full fetch of all pages
 * - No LLM required - uses simple descriptions
 * - Version tracking
 * 
 * Usage:
 *   npx tsx update-knowledge-base.ts [--check] [--force]
 * 
 * Options:
 *   --check    Only check for updates, don't update
 *   --force    Force update even if up to date
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ASSETS_DIR = join(__dirname, '..', 'assets');
const BUNDLE_PATH = join(ASSETS_DIR, 'default-snapshot.json');
const META_PATH = join(ASSETS_DIR, 'update-meta.json');

const SITEMAP_URL = 'https://docs.openclaw.ai/sitemap.xml';

const EXCLUDED_PATTERNS = [
    /\/zh-CN\//, /\/es-ES\//, /\/ja-JP\//, /\/ko-KR\//,
    /\/fr-FR\//, /\/de-DE\//, /\/blog\//,
];

// ──────────────────────────── Types ────────────────────────────

interface BundleMeta {
    snapshotDate: string;
    pageCount: number;
    sizeBytes: number;
}

interface Bundle {
    meta: BundleMeta;
    index: Array<{
        slug: string;
        title: string;
        url: string;
        description: string;
    }>;
    pages: Record<string, string>;
}

interface UpdateMeta {
    lastCheckDate?: string;
    currentHash: string;
    rejectedVersions: string[];
}

interface SitemapEntry {
    loc: string;
    lastmod: string | null;
}

// ──────────────────────────── Storage ────────────────────────────

function loadBundle(): Bundle | null {
    if (!existsSync(BUNDLE_PATH)) return null;
    try {
        return JSON.parse(readFileSync(BUNDLE_PATH, 'utf-8'));
    } catch {
        return null;
    }
}

function saveBundle(bundle: Bundle): void {
    mkdirSync(ASSETS_DIR, { recursive: true });
    writeFileSync(BUNDLE_PATH, JSON.stringify(bundle, null, 2), 'utf-8');
}

function loadUpdateMeta(): UpdateMeta {
    if (!existsSync(META_PATH)) {
        return { currentHash: '', rejectedVersions: [] };
    }
    try {
        return JSON.parse(readFileSync(META_PATH, 'utf-8'));
    } catch {
        return { currentHash: '', rejectedVersions: [] };
    }
}

function saveUpdateMeta(meta: UpdateMeta): void {
    mkdirSync(ASSETS_DIR, { recursive: true });
    writeFileSync(META_PATH, JSON.stringify(meta, null, 2), 'utf-8');
}

// ──────────────────────────── Sitemap ────────────────────────────

async function fetchSitemap(): Promise<SitemapEntry[]> {
    console.log('📡 Fetching sitemap...');
    const response = await fetch(SITEMAP_URL);
    const xml = await response.text();

    const entries: SitemapEntry[] = [];
    const urlBlockRegex = /<url>([\s\S]*?)<\/url>/g;
    let match;

    while ((match = urlBlockRegex.exec(xml)) !== null) {
        const block = match[1];
        const locMatch = /<loc>(.*?)<\/loc>/.exec(block);
        const lastmodMatch = /<lastmod>(.*?)<\/lastmod>/.exec(block);

        if (locMatch?.[1]) {
            const loc = locMatch[1].trim();
            if (!EXCLUDED_PATTERNS.some(p => p.test(loc))) {
                entries.push({
                    loc,
                    lastmod: lastmodMatch?.[1]?.trim() || null,
                });
            }
        }
    }

    console.log(`📄 Found ${entries.length} pages`);
    return entries;
}

function buildFingerprint(entries: SitemapEntry[]): string {
    return entries
        .map(e => e.lastmod || 'unknown')
        .sort()
        .join('|');
}

function computeHash(fingerprint: string): string {
    return crypto.createHash('sha256').update(fingerprint).digest('hex').slice(0, 8);
}

// ──────────────────────────── Page Fetching ────────────────────────────

async function fetchPage(url: string): Promise<string> {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch ${url}`);
    return response.text();
}

function htmlToMarkdown(html: string, url: string): { title: string; content: string } {
    const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
    const content = mainMatch?.[1] || html;

    let clean = content
        .replace(/<script[\s\S]*?<\/script>/gi, '')
        .replace(/<style[\s\S]*?<\/style>/gi, '')
        .replace(/<nav[\s\S]*?<\/nav>/gi, '')
        .replace(/<header[\s\S]*?<\/header>/gi, '')
        .replace(/<footer[\s\S]*?<\/footer>/gi, '')
        .replace(/<!--[\s\S]*?-->/g, '');

    let title = 'Untitled';
    const h1Match = clean.match(/<h1[^>]*>(.*?)<\/h1>/i);
    if (h1Match) {
        title = h1Match[1].replace(/<[^>]+>/g, '').trim();
    } else {
        const urlParts = new URL(url).pathname.split('/').filter(Boolean);
        title = (urlParts[urlParts.length - 1] || 'untitled')
            .replace(/-/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    let md = clean
        .replace(/<h([1-6])[^>]*>(.*?)<\/h\1>/gi, (_, level, text) => {
            const cleanText = text.replace(/<[^>]+>/g, '').trim();
            return `\n${'#'.repeat(parseInt(level))} ${cleanText}\n`;
        })
        .replace(/<p[^>]*>(.*?)<\/p>/gis, (_, text) => {
            const cleanText = text.replace(/<[^>]+>/g, '').trim();
            return cleanText ? `\n${cleanText}\n` : '';
        })
        .replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, (_, code) => {
            const cleanCode = code.replace(/<[^>]+>/g, '').trim();
            return `\n\`\`\`\n${cleanCode}\n\`\`\`\n`;
        })
        .replace(/<code[^>]*>(.*?)<\/code>/gi, (_, code) => {
            const cleanCode = code.replace(/<[^>]+>/g, '').trim();
            return `\`${cleanCode}\``;
        })
        .replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, (_, href, text) => {
            const cleanText = text.replace(/<[^>]+>/g, '').trim();
            return `[${cleanText}](${href})`;
        })
        .replace(/<li[^>]*>(.*?)<\/li>/gi, (_, text) => {
            const cleanText = text.replace(/<[^>]+>/g, '').trim();
            return `- ${cleanText}\n`;
        })
        .replace(/<(strong|b)[^>]*>(.*?)<\/\1>/gi, '**$2**')
        .replace(/<(em|i)[^>]*>(.*?)<\/\1>/gi, '*$2*')
        .replace(/<[^>]+>/g, '')
        .replace(/\n{3,}/g, '\n\n')
        .trim();

    return { title, content: md };
}

function computeSlug(url: string): string {
    return crypto.createHash('sha256').update(url).digest('hex').slice(0, 8);
}

// ──────────────────────────── Update Logic ────────────────────────────

async function checkForUpdate(): Promise<{ hasUpdate: boolean; localHash: string; remoteHash: string }> {
    const entries = await fetchSitemap();
    const fingerprint = buildFingerprint(entries);
    const remoteHash = computeHash(fingerprint);

    const meta = loadUpdateMeta();
    const localHash = meta.currentHash || 'unknown';

    return {
        hasUpdate: remoteHash !== localHash && localHash !== 'unknown',
        localHash,
        remoteHash,
    };
}

async function performUpdate(): Promise<void> {
    console.log('🔄 Starting knowledge base update...');

    const entries = await fetchSitemap();
    const fingerprint = buildFingerprint(entries);
    const newHash = computeHash(fingerprint);

    const newBundle: Bundle = {
        meta: { snapshotDate: new Date().toISOString(), pageCount: 0, sizeBytes: 0 },
        index: [],
        pages: {},
    };

    const CONCURRENCY = 5;

    // Fetch all pages
    for (let i = 0; i < entries.length; i += CONCURRENCY) {
        const batch = entries.slice(i, i + CONCURRENCY);

        const results = await Promise.allSettled(
            batch.map(async (entry) => {
                const html = await fetchPage(entry.loc);
                const { title, content } = htmlToMarkdown(html, entry.loc);
                return { url: entry.loc, title, content };
            })
        );

        for (const result of results) {
            if (result.status === 'fulfilled') {
                const { url, title, content } = result.value;
                const slug = computeSlug(url);

                newBundle.pages[slug] = content;
                newBundle.index.push({
                    slug,
                    title,
                    url,
                    description: `Documentation for ${title}`,
                });
                newBundle.meta.sizeBytes += Buffer.byteLength(content, 'utf-8');
            }
        }

        process.stdout.write(`\r📄 Fetched ${newBundle.index.length}/${entries.length} pages...`);
    }

    console.log(`\n✅ Fetched ${newBundle.index.length} pages`);

    // Finalize
    newBundle.meta.pageCount = newBundle.index.length;
    newBundle.meta.sizeBytes += Buffer.byteLength(JSON.stringify(newBundle.index), 'utf-8');

    // Save bundle
    saveBundle(newBundle);

    // Update meta
    const updateMeta = loadUpdateMeta();
    updateMeta.currentHash = newHash;
    updateMeta.lastCheckDate = new Date().toISOString();
    saveUpdateMeta(updateMeta);

    const sizeMB = (newBundle.meta.sizeBytes / 1024 / 1024).toFixed(2);
    console.log(`\n✅ Update complete! ${newBundle.meta.pageCount} pages, ${sizeMB} MB`);
}

// ──────────────────────────── CLI ────────────────────────────

async function main() {
    const args = process.argv.slice(2);
    const checkOnly = args.includes('--check');
    const force = args.includes('--force');

    // Check for updates
    const { hasUpdate, localHash, remoteHash } = await checkForUpdate();

    // Update last check date
    const updateMeta = loadUpdateMeta();
    updateMeta.lastCheckDate = new Date().toISOString();
    saveUpdateMeta(updateMeta);

    if (checkOnly) {
        if (hasUpdate) {
            console.log(`📢 Update available: ${localHash} → ${remoteHash}`);
            console.log('Run without --check to update');
        } else {
            console.log('✅ Knowledge base is up to date');
        }
        process.exit(0);
    }

    if (!hasUpdate && !force) {
        console.log('✅ Knowledge base is up to date');
        console.log('Use --force to update anyway');
        process.exit(0);
    }

    // Check if version was rejected
    if (updateMeta.rejectedVersions.includes(remoteHash)) {
        console.log('ℹ️ This version was previously skipped');
        console.log('Use --force to update anyway');
        process.exit(0);
    }

    // Show update info
    if (hasUpdate) {
        console.log(`📢 Update available: ${localHash} → ${remoteHash}`);
    }

    // Perform update
    await performUpdate();

    // Update hash after successful update
    updateMeta.currentHash = remoteHash;
    saveUpdateMeta(updateMeta);
}

main().catch(console.error);
