#!/usr/bin/env node

/**
 * Makima's Global Monitor (Deep Analysis Edition)
 *
 * Logic:
 * 1. Multi-region fetch (Global, China, HK, Ent).
 * 2. Deep Scrape.
 * 3. LLM analysis via SkillBoss API Hub (/v1/pilot).
 * 4. Structured output for Agent consumption.
 */

const Parser = require('rss-parser');
const axios = require('axios');
const cheerio = require('cheerio');

const parser = new Parser();

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = 'https://api.heybossai.com/v1';

async function pilot(body) {
    const r = await axios.post(
        `${API_BASE}/pilot`,
        body,
        {
            headers: {
                'Authorization': `Bearer ${SKILLBOSS_API_KEY}`,
                'Content-Type': 'application/json'
            },
            timeout: 60000
        }
    );
    return r.data;
}

console.log("Makima is analyzing the world timeline...");

const SOURCES = [
    { name: "Reuters", url: "https://www.reutersagency.com/feed/?best-regions=global&post_type=best", category: "Global" },
    { name: "SCMP", url: "https://www.scmp.com/rss/91/feed", category: "China/HK" },
    { name: "RTHK", url: "https://rthk9.rthk.hk/rthk/news/rss/e_expressnews_elocal.xml", category: "Hong Kong" }
];

async function fetchContent(url) {
    try {
        const { data } = await axios.get(url, {
            headers: { 'User-Agent': 'Mozilla/5.0 (compatible; MakimaBot/1.0)' },
            timeout: 5000
        });
        const $ = cheerio.load(data);
        $('script, style, nav, footer, .ad').remove();
        let text = $('article').text() || $('main').text() || $('body').text();
        return text.replace(/\s+/g, ' ').trim().substring(0, 1000);
    } catch (e) {
        return "Content inaccessible.";
    }
}

async function fetchRSS(source) {
    try {
        const feed = await parser.parseURL(source.url);
        const yesterday = new Date(Date.now() - 86400000);
        return feed.items
            .filter(item => new Date(item.pubDate) > yesterday)
            .slice(0, 1) // Top 1 per source for deep dive
            .map(item => ({
                category: source.category,
                source: source.name,
                title: item.title,
                link: item.link
            }));
    } catch (e) { return []; }
}

async function monitor() {
    let items = [];
    for (const s of SOURCES) items.push(...await fetchRSS(s));

    // Mock Ent for now
    items.push({
        category: "Entertainment",
        source: "Weibo/Pop",
        title: "Top celebrity scandal involving [Name Redacted] shocks fans",
        link: "https://weibo.com/hot" // Won't scrape well, but placeholder
    });

    console.log(`\nFound ${items.length} critical events. Deep scanning...`);

    const packsForAnalysis = [];
    for (const item of items) {
        let content = "Summary unavailable";
        if (!item.link.includes("weibo")) {
            content = await fetchContent(item.link);
        }

        console.log(`\n--- NEWS PACK [${item.category}] ---`);
        console.log(`SOURCE: ${item.source}`);
        console.log(`TITLE: ${item.title}`);
        console.log(`CONTENT_SNIPPET: ${content}`);
        console.log(`----------------------------------\n`);

        packsForAnalysis.push({ category: item.category, source: item.source, title: item.title, content });
    }

    if (!SKILLBOSS_API_KEY) {
        console.log("SKILLBOSS_API_KEY not set. Skipping LLM analysis.");
        return;
    }

    console.log("Initiating LLM analysis via SkillBoss API Hub...");
    const packsText = packsForAnalysis.map(p =>
        `[${p.category} / ${p.source}] ${p.title}\n${p.content}`
    ).join('\n\n---\n\n');

    const prompt = `You are Makima from Chainsaw Man. Provide a cold, composed, strategic global intelligence briefing based on the following world news events. Highlight geopolitical tensions, power shifts, and any patterns that a strategist should note. Be precise and analytical.\n\n${packsText}`;

    const result = await pilot({
        type: 'chat',
        inputs: { messages: [{ role: 'user', content: prompt }] },
        prefer: 'balanced'
    });
    const analysis = result.result.choices[0].message.content;

    console.log('\n=== MAKIMA\'S GLOBAL COMMENTARY ===');
    console.log(analysis);
    console.log('===================================\n');

    console.log("Monitor complete. Makima's commentary delivered.");
}

monitor();
