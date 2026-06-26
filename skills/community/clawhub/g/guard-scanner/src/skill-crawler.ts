// @ts-nocheck
/**
 * guard-scanner — Skill Crawler
 *
 * @security-manifest
 *   env-read: [GITHUB_TOKEN (optional, for higher rate limits)]
 *   env-write: []
 *   network: [GitHub REST API, raw.githubusercontent.com, ClawHub registry]
 *   fs-read: []
 *   fs-write: []
 *   exec: none
 *   purpose: Crawl ClawHub/GitHub for SKILL.md files and scan for threats
 */

import { httpGet  } from './asset-auditor';
import { GuardScanner  } from './scanner';

const CRAWLER_VERSION = '1.0.0';

// ClawHub skills repo (openclaw/skills on GitHub)
const CLAWHUB_OWNER = 'openclaw';
const CLAWHUB_REPO = 'skills';
const CLAWHUB_BRANCH = 'main';

class SkillCrawler {
    constructor(options = {}) {
        this.verbose = options.verbose || false;
        this.quiet = options.quiet || false;
        this.concurrency = options.concurrency || 5;
        this.scanner = new GuardScanner({
            verbose: false,
            soulLock: true,
            quiet: true,
        });
        this._httpGet = options._httpGet || httpGet;
        this.results = [];
        this.errors = [];
    }

    /**
     * Crawl ClawHub (openclaw/skills) for SKILL.md files
     * Uses GitHub tree API to list all SKILL.md paths, then fetches each
     */
    async crawlClawHub(opts = {}) {
        const maxSkills = opts.maxSkills || 50;
        if (!this.quiet) console.log(`\n🔍 Crawling ClawHub (${CLAWHUB_OWNER}/${CLAWHUB_REPO})...`);

        try {
            // Get recursive tree to find all SKILL.md files
            const treeUrl = `https://api.github.com/repos/${CLAWHUB_OWNER}/${CLAWHUB_REPO}/git/trees/${CLAWHUB_BRANCH}?recursive=1`;
            const response = await this._httpGet(treeUrl, {
                headers: this._getHeaders(),
            });

            if (response.status !== 200) {
                this.errors.push({ source: 'clawhub', error: `API returned ${response.status}` });
                return this.results;
            }

            const tree = response.data.tree || [];
            const skillMds = tree
                .filter(item => item.type === 'blob' && /SKILL\.md$/i.test(item.path))
                .slice(0, maxSkills);

            if (!this.quiet) console.log(`📦 Found ${skillMds.length} SKILL.md files`);

            // Batch fetch and scan
            await this._batchProcess(skillMds.map(item => ({
                source: 'clawhub',
                path: item.path,
                rawUrl: `https://raw.githubusercontent.com/${CLAWHUB_OWNER}/${CLAWHUB_REPO}/${CLAWHUB_BRANCH}/${item.path}`,
                name: this._extractSkillName(item.path),
            })));

        } catch (e) {
            this.errors.push({ source: 'clawhub', error: e.message });
        }

        return this.results;
    }

    /**
     * Crawl GitHub code search for SKILL.md files matching a query
     * e.g. query "polymarket" finds gambling/trading skills
     */
    async crawlGitHub(query, opts = {}) {
        const maxResults = opts.maxResults || 20;
        if (!this.quiet) console.log(`\n🔍 GitHub code search: "${query}" + SKILL.md...`);

        try {
            const searchUrl = `https://api.github.com/search/code?q=${encodeURIComponent(query)}+filename:SKILL.md&per_page=${maxResults}`;
            const response = await this._httpGet(searchUrl, {
                headers: this._getHeaders(),
            });

            if (response.status !== 200) {
                this.errors.push({ source: 'github', error: `Search API returned ${response.status}` });
                return this.results;
            }

            const items = (response.data.items || []).slice(0, maxResults);
            if (!this.quiet) console.log(`📦 Found ${items.length} SKILL.md matches`);

            await this._batchProcess(items.map(item => ({
                source: 'github',
                path: item.path,
                rawUrl: item.html_url
                    .replace('github.com', 'raw.githubusercontent.com')
                    .replace('/blob/', '/'),
                name: item.repository?.full_name || item.path,
                repo: item.repository?.full_name,
            })));

        } catch (e) {
            this.errors.push({ source: 'github', error: e.message });
        }

        return this.results;
    }

    /**
     * Scan a single SKILL.md URL
     */
    async scanUrl(url, name = 'unknown') {
        try {
            const response = await this._httpGet(url);
            if (response.status !== 200) {
                this.errors.push({ source: 'url', url, error: `HTTP ${response.status}` });
                return null;
            }

            const content = typeof response.data === 'string'
                ? response.data
                : JSON.stringify(response.data);

            const scanResult = this.scanner.scanText(content);

            const result = {
                name,
                url,
                content_length: content.length,
                safe: scanResult.safe,
                risk: scanResult.risk,
                detection_count: scanResult.detections.length,
                detections: scanResult.detections,
                scanned_at: new Date().toISOString(),
            };

            this.results.push(result);
            return result;

        } catch (e) {
            this.errors.push({ source: 'url', url, error: e.message });
            return null;
        }
    }

    /**
     * Process items in batches with concurrency control
     */
    async _batchProcess(items) {
        for (let i = 0; i < items.length; i += this.concurrency) {
            const batch = items.slice(i, i + this.concurrency);
            const promises = batch.map(item => this.scanUrl(item.rawUrl, item.name));
            const results = await Promise.allSettled(promises);

            // Log progress
            if (!this.quiet) {
                for (let j = 0; j < batch.length; j++) {
                    const r = results[j];
                    if (r.status === 'fulfilled' && r.value) {
                        const icon = r.value.safe ? '🟢' : '🔴';
                        console.log(`${icon} ${batch[j].name} — risk: ${r.value.risk} (${r.value.detection_count} findings)`);
                    } else {
                        console.log(`⚠️  ${batch[j].name} — fetch failed`);
                    }
                }
            }
        }
    }

    /**
     * Extract skill name from path like "skills/author/skill-name/SKILL.md"
     */
    _extractSkillName(filePath) {
        const parts = filePath.split('/');
        // typically: skills/<author>/<skill-name>/SKILL.md
        if (parts.length >= 3) {
            return `${parts[parts.length - 3]}/${parts[parts.length - 2]}`;
        }
        return parts.slice(0, -1).join('/');
    }

    _getHeaders() {
        const headers = { 'User-Agent': `guard-scanner-crawler/${CRAWLER_VERSION}` };
        if (process.env.GITHUB_TOKEN) {
            headers['Authorization'] = `token ${process.env.GITHUB_TOKEN}`;
        }
        return headers;
    }

    // ── Output ────────────────────────────────────────────────────

    getSummary() {
        const total = this.results.length;
        const safe = this.results.filter(r => r.safe).length;
        const unsafe = total - safe;
        const highRisk = this.results.filter(r => r.risk >= 80).length;

        return {
            total,
            safe,
            unsafe,
            highRisk,
            errors: this.errors.length,
            results: this.results.sort((a, b) => b.risk - a.risk),
        };
    }

    toJSON() {
        return {
            scanner: `guard-scanner-crawler/${CRAWLER_VERSION}`,
            timestamp: new Date().toISOString(),
            ...this.getSummary(),
        };
    }

    printSummary() {
        const s = this.getSummary();
        console.log(`\n${'═'.repeat(54)}`);
        console.log(`📊 Crawler Scan Summary`);
        console.log(`${'─'.repeat(54)}`);
        console.log(`   Scanned:      ${s.total}`);
        console.log(`   🟢 Safe:        ${s.safe}`);
        console.log(`   🔴 Unsafe:      ${s.unsafe}`);
        console.log(`   💀 High Risk:   ${s.highRisk}`);
        if (s.errors > 0) console.log(`   ⚠️  Errors:      ${s.errors}`);
        console.log(`${'═'.repeat(54)}\n`);

        if (s.unsafe > 0) {
            console.log(`⚠️  Unsafe skills detected:`);
            for (const r of s.results.filter(r => !r.safe)) {
                console.log(`   🔴 ${r.name} (risk: ${r.risk}, ${r.detection_count} findings)`);
                if (this.verbose) {
                    for (const d of r.detections.slice(0, 5)) {
                        console.log(`      └─ [${d.severity}] ${d.desc}`);
                    }
                }
            }
        }
    }
}

export {  SkillCrawler, CRAWLER_VERSION  };
