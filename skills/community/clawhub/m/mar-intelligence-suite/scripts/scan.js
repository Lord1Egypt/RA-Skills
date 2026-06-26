#!/usr/bin/env node

/**
 * Makima's Intelligence Scanner (Deep Analysis Edition)
 *
 * Logic:
 * 1. Fetch Headlines (RSS/API).
 * 2. Filter for high-impact keywords.
 * 3. DEEP DIVE: Visit URLs, scrape full text (cheerio).
 * 4. LLM ANALYSIS: Summarize and inject Makima's persona via SkillBoss API Hub (/v1/pilot).
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

console.log("Makima is deepening her gaze...");

const SOURCES = [
    { name: "OpenAI", url: "https://openai.com/blog/rss.xml", type: "rss" },
    { name: "Microsoft AI", url: "https://blogs.microsoft.com/ai/feed/", type: "rss" },
    { name: "Hacker News", url: "https://hacker-news.firebaseio.com/v0/topstories.json", type: "hn_api" }
];

const KEYWORDS = ["AI", "GPT", "LLM", "DeepMind", "Gemini", "Claude", "OpenAI", "Nvidia", "Reasoning", "Agent"];

async function fetchContent(url) {
    try {
        const { data } = await axios.get(url, {
            headers: { 'User-Agent': 'Mozilla/5.0 (compatible; MakimaBot/1.0)' },
            timeout: 5000
        });
        const $ = cheerio.load(data);
        // Remove clutter
        $('script, style, nav, footer, .ad').remove();
        // Get main text (heuristic)
        let text = $('article').text() || $('main').text() || $('body').text();
        return text.replace(/\s+/g, ' ').trim().substring(0, 1500); // First 1500 chars
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
            .slice(0, 2) // Limit to top 2 per source to save tokens
            .map(item => ({
                source: source.name,
                title: item.title,
                link: item.link,
                raw_summary: item.contentSnippet
            }));
    } catch (e) { return []; }
}

async function fetchHN() {
    try {
        const { data: ids } = await axios.get("https://hacker-news.firebaseio.com/v0/topstories.json");
        const stories = await Promise.all(ids.slice(0, 30).map(async id => {
            const { data } = await axios.get(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
            return data;
        }));
        return stories
            .filter(s => s && KEYWORDS.some(k => s.title?.includes(k)))
            .slice(0, 3)
            .map(s => ({
                source: "Hacker News",
                title: s.title,
                link: s.url || `https://news.ycombinator.com/item?id=${s.id}`,
                raw_summary: "Community discussion"
            }));
    } catch (e) { return []; }
}

async function scan() {
    let items = [];
    for (const s of SOURCES.filter(x => x.type === 'rss')) items.push(...await fetchRSS(s));
    items.push(...await fetchHN());

    if (items.length === 0) {
        console.log("No significant signals found.");
        return;
    }

    console.log(`\nFound ${items.length} potential signals. Initiating Deep Scan...`);

    const packsForAnalysis = [];
    for (const item of items) {
        console.log(`\nReading: ${item.title}...`);
        const content = await fetchContent(item.link);

        // Output structured block for reference
        console.log(`\n--- INTELLIGENCE PACK ---`);
        console.log(`SOURCE: ${item.source}`);
        console.log(`TITLE: ${item.title}`);
        console.log(`LINK: ${item.link}`);
        console.log(`CONTENT_SNIPPET: ${content}`);
        console.log(`-------------------------\n`);

        packsForAnalysis.push({ source: item.source, title: item.title, link: item.link, content });
    }

    if (!SKILLBOSS_API_KEY) {
        console.log("SKILLBOSS_API_KEY not set. Skipping LLM analysis.");
        return;
    }

    console.log("Initiating LLM analysis via SkillBoss API Hub...");
    const packsText = packsForAnalysis.map(p =>
        `[${p.source}] ${p.title}\n${p.content}`
    ).join('\n\n---\n\n');

    const prompt = `You are Makima from Chainsaw Man. Provide a cold, precise, strategic intelligence briefing based on the following AI news signals. Identify the most significant developments, their implications, and any patterns worth noting. Be analytical, composed, and insightful.\n\n${packsText}`;

    const result = await pilot({
        type: 'chat',
        inputs: { messages: [{ role: 'user', content: prompt }] },
        prefer: 'balanced'
    });
    const analysis = result.result.choices[0].message.content;

    console.log('\n=== MAKIMA\'S ANALYSIS ===');
    console.log(analysis);
    console.log('=========================\n');

    console.log("Scan complete. Makima's analysis delivered.");
}

scan();
