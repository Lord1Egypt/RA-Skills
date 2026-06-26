#!/usr/bin/env node
/**
 * Universe Scanner — Fetches ALL active Polymarket markets, categorizes, and finds opportunities
 * Converted from Python to Node.js for self-contained operation
 * 
 * Usage:
 *   node universe_scanner.cjs                 # Display categorized analysis
 *   node universe_scanner.cjs --save          # Also save JSON to data/
 *   node universe_scanner.cjs --category=Crypto   # Show only crypto markets
 *   node universe_scanner.cjs --min-volume=10000  # Filter by minimum volume
 */

const fs = require('fs');
const path = require('path');

const GAMMA_BASE = "https://gamma-api.polymarket.com";
const RATE_LIMIT_DELAY = 150; // milliseconds between requests
const DATA_DIR = path.join(__dirname, 'data');
const UNIVERSE_FILE = path.join(DATA_DIR, 'polymarket_universe.json');

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// Category keywords
const CATEGORY_KEYWORDS = {
    "Crypto": ["bitcoin", "btc", "ethereum", "eth", "crypto", "solana", "sol", "token", "defi", "blockchain", "coin", "nft", "web3", "doge", "xrp", "ada", "matic", "avax", "dot", "link", "uni"],
    "Politics": ["president", "election", "trump", "biden", "congress", "senate", "governor", "political", "democrat", "republican", "vote", "poll", "impeach", "legislation", "party", "primary", "gop", "harris", "desantis"],
    "Sports": ["nba", "nfl", "mlb", "nhl", "soccer", "football", "basketball", "baseball", "tennis", "ufc", "mma", "boxing", "f1", "formula", "olympics", "match", "game", "score", "championship", "super bowl", "world cup", "winner:", "playoffs"],
    "Finance": ["stock", "s&p", "nasdaq", "fed", "interest rate", "inflation", "gdp", "unemployment", "treasury", "dow", "market cap", "ipo", "earnings", "recession", "cpi", "fomc"],
    "Entertainment": ["oscar", "grammy", "movie", "film", "music", "album", "tv show", "netflix", "streaming", "celebrity", "awards", "box office", "concert", "tour"],
    "Science": ["nasa", "spacex", "climate", "vaccine", "fda", "drug", "ai ", "artificial intelligence", "research", "study", "breakthrough", "discovery", "covid", "weather"]
};

function categorizeMarket(question, apiCategory = "") {
    const text = (question + " " + apiCategory).toLowerCase();
    for (const [cat, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
        if (keywords.some(kw => text.includes(kw))) {
            return cat;
        }
    }
    return "Other";
}

function parseOutcomePrices(raw) {
    try {
        if (typeof raw === 'string') {
            const prices = JSON.parse(raw);
            return prices.map(p => parseFloat(p));
        } else if (Array.isArray(raw)) {
            return raw.map(p => parseFloat(p));
        }
        return [];
    } catch (e) {
        return [];
    }
}

function parseClobTokenIds(raw) {
    try {
        if (typeof raw === 'string') {
            return JSON.parse(raw);
        }
        return Array.isArray(raw) ? raw : [];
    } catch (e) {
        return [];
    }
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchAllMarkets(closed = false) {
    console.log(`🔍 Fetching ${closed ? 'closed' : 'active'} markets from Polymarket...`);
    const markets = [];
    let offset = 0;
    const limit = 100;
    
    while (true) {
        const url = `${GAMMA_BASE}/markets?active=true&closed=${closed}&limit=${limit}&offset=${offset}`;
        try {
            const response = await fetch(url);
            if (response.status === 429) {
                console.log(`  Rate limited at offset ${offset}, waiting...`);
                await sleep(2000);
                continue;
            }
            if (!response.ok) {
                console.log(`  HTTP ${response.status} at offset ${offset}, stopping`);
                break;
            }
            const data = await response.json();
            if (!data || data.length === 0) {
                break;
            }
            markets.push(...data);
            process.stdout.write(`\r  Fetched ${markets.length} markets...`);
            offset += limit;
            await sleep(RATE_LIMIT_DELAY);
        } catch (error) {
            console.log(`\n  Error fetching markets: ${error.message}`);
            break;
        }
    }
    
    console.log(`\n  Total: ${markets.length} markets`);
    return markets;
}

async function analyzeUniverse() {
    const startTime = Date.now();
    const markets = await fetchAllMarkets();
    
    console.log("\n📊 Analyzing market universe...\n");
    
    // Enhanced market processing
    const processedMarkets = markets.map(market => {
        const prices = parseOutcomePrices(market.outcomePrices || "[]");
        const tokenIds = parseClobTokenIds(market.clobTokenIds || "[]");
        const category = categorizeMarket(market.question || "", market.category || "");
        
        const volume = parseFloat(market.volume || 0);
        const liquidity = parseFloat(market.liquidity || 0);
        const volumeNum = parseFloat(market.volumeNum || 0);
        
        // Time analysis
        const endDate = new Date(market.endDate || market.end_date_iso);
        const daysLeft = Math.max(0, (endDate - Date.now()) / (1000 * 60 * 60 * 24));
        
        // Outcome analysis
        const yesPrice = prices[0] || 0.5;
        const noPrice = prices[1] || (1 - yesPrice);
        
        // Opportunity flags
        const isExtreme = yesPrice < 0.1 || yesPrice > 0.9;
        const isHighVolume = volumeNum > 100000;
        const isNearExpiry = daysLeft < 7 && daysLeft > 0;
        const isCheapYes = yesPrice >= 0.05 && yesPrice <= 0.3;
        const isCoinFlip = yesPrice >= 0.4 && yesPrice <= 0.6;
        
        return {
            ...market,
            category,
            prices,
            tokenIds,
            volume: Math.max(volume, volumeNum),
            volumeNum: volumeNum,
            liquidity,
            daysLeft: Math.round(daysLeft * 10) / 10,
            yesPrice,
            noPrice,
            isExtreme,
            isHighVolume,
            isNearExpiry,
            isCheapYes,
            isCoinFlip,
            slug: market.slug || `market-${market.id || Math.random().toString(36).substr(2, 9)}`
        };
    });
    
    // Category analysis
    const categoryStats = {};
    const opportunities = {
        extreme: [],
        cheapYes: [],
        coinFlips: [],
        nearExpiry: [],
        highVolume: []
    };
    
    for (const market of processedMarkets) {
        // Category stats
        if (!categoryStats[market.category]) {
            categoryStats[market.category] = {
                count: 0,
                totalVolume: 0,
                avgPrice: 0,
                markets: []
            };
        }
        categoryStats[market.category].count++;
        categoryStats[market.category].totalVolume += market.volume;
        categoryStats[market.category].markets.push(market);
        
        // Opportunity detection
        if (market.isExtreme && market.isHighVolume) {
            opportunities.extreme.push(market);
        }
        if (market.isCheapYes && market.volume > 50000) {
            opportunities.cheapYes.push(market);
        }
        if (market.isCoinFlip && market.volume > 100000) {
            opportunities.coinFlips.push(market);
        }
        if (market.isNearExpiry && market.volume > 25000) {
            opportunities.nearExpiry.push(market);
        }
        if (market.isHighVolume) {
            opportunities.highVolume.push(market);
        }
    }
    
    // Calculate averages
    Object.values(categoryStats).forEach(stats => {
        stats.avgVolume = stats.totalVolume / stats.count;
        stats.avgPrice = stats.markets.reduce((sum, m) => sum + m.yesPrice, 0) / stats.count;
    });
    
    // Sort opportunities
    Object.keys(opportunities).forEach(key => {
        opportunities[key].sort((a, b) => b.volume - a.volume);
    });
    
    const elapsedTime = (Date.now() - startTime) / 1000;
    
    return {
        timestamp: new Date().toISOString(),
        totalMarkets: processedMarkets.length,
        elapsedTime,
        categoryStats,
        opportunities,
        markets: processedMarkets
    };
}

function displayResults(analysis, options = {}) {
    const { categoryFilter, minVolume = 0 } = options;
    
    console.log("═".repeat(80));
    console.log("  POLYMARKET UNIVERSE ANALYSIS");
    console.log("═".repeat(80));
    console.log(`  Total Markets: ${analysis.totalMarkets.toLocaleString()}`);
    console.log(`  Scan Time: ${analysis.elapsedTime.toFixed(1)}s`);
    console.log(`  Timestamp: ${new Date(analysis.timestamp).toLocaleString()}`);
    console.log();
    
    // Category breakdown
    if (!categoryFilter) {
        console.log("📊 CATEGORY BREAKDOWN");
        console.log("─".repeat(80));
        const sortedCategories = Object.entries(analysis.categoryStats)
            .sort(([,a], [,b]) => b.totalVolume - a.totalVolume);
        
        for (const [category, stats] of sortedCategories) {
            const avgVolStr = stats.avgVolume > 1000 ? `$${Math.round(stats.avgVolume/1000)}K` : `$${Math.round(stats.avgVolume)}`;
            console.log(`  ${category.padEnd(12)} | ${stats.count.toString().padStart(5)} markets | Avg vol: ${avgVolStr.padStart(6)} | Avg price: ${(stats.avgPrice*100).toFixed(0)}¢`);
        }
        console.log();
    }
    
    // Show opportunities for specific category or all
    const categoriesToShow = categoryFilter ? [categoryFilter] : Object.keys(analysis.categoryStats);
    
    for (const category of categoriesToShow) {
        if (!analysis.categoryStats[category]) {
            console.log(`❌ Category '${category}' not found`);
            continue;
        }
        
        console.log(`🎯 ${category.toUpperCase()} OPPORTUNITIES`);
        console.log("─".repeat(80));
        
        const categoryMarkets = analysis.categoryStats[category].markets
            .filter(m => m.volume >= minVolume)
            .sort((a, b) => b.volume - a.volume);
        
        if (categoryMarkets.length === 0) {
            console.log(`  No markets found with volume >= $${minVolume.toLocaleString()}`);
            console.log();
            continue;
        }
        
        // Top volume markets
        console.log("  Top Volume:");
        for (const market of categoryMarkets.slice(0, 5)) {
            const volStr = market.volume > 1000 ? `$${Math.round(market.volume/1000)}K` : `$${Math.round(market.volume)}`;
            console.log(`    YES:${(market.yesPrice*100).toFixed(0)}¢ | ${market.daysLeft}d | Vol:${volStr.padStart(6)} | ${market.question?.slice(0, 60)}`);
        }
        
        // Extreme prices
        const extremeInCategory = categoryMarkets.filter(m => m.isExtreme);
        if (extremeInCategory.length > 0) {
            console.log("\n  Extreme Prices (< 10¢ or > 90¢):");
            for (const market of extremeInCategory.slice(0, 3)) {
                const volStr = market.volume > 1000 ? `$${Math.round(market.volume/1000)}K` : `$${Math.round(market.volume)}`;
                const flag = market.yesPrice > 0.9 ? '🟢' : '🔴';
                console.log(`    ${flag} YES:${(market.yesPrice*100).toFixed(0)}¢ | ${market.daysLeft}d | Vol:${volStr.padStart(6)} | ${market.question?.slice(0, 55)}`);
            }
        }
        
        // Cheap YES opportunities
        const cheapYesInCategory = categoryMarkets.filter(m => m.isCheapYes);
        if (cheapYesInCategory.length > 0) {
            console.log("\n  Cheap YES (5-30¢):");
            for (const market of cheapYesInCategory.slice(0, 3)) {
                const volStr = market.volume > 1000 ? `$${Math.round(market.volume/1000)}K` : `$${Math.round(market.volume)}`;
                const returnMultiple = ((1 - market.yesPrice) / market.yesPrice).toFixed(1);
                console.log(`    💰 YES:${(market.yesPrice*100).toFixed(0)}¢ (${returnMultiple}x) | ${market.daysLeft}d | Vol:${volStr.padStart(6)} | ${market.question?.slice(0, 50)}`);
            }
        }
        
        console.log();
    }
    
    // Overall opportunity summary
    if (!categoryFilter) {
        console.log("🚨 TOP OPPORTUNITIES ACROSS ALL CATEGORIES");
        console.log("─".repeat(80));
        
        const allOpps = [
            ...analysis.opportunities.extreme.slice(0, 3).map(m => ({ ...m, type: 'EXTREME' })),
            ...analysis.opportunities.cheapYes.slice(0, 3).map(m => ({ ...m, type: 'CHEAP YES' })),
            ...analysis.opportunities.nearExpiry.slice(0, 3).map(m => ({ ...m, type: 'NEAR EXPIRY' }))
        ].sort((a, b) => b.volume - a.volume).slice(0, 10);
        
        for (const opp of allOpps) {
            const volStr = opp.volume > 1000 ? `$${Math.round(opp.volume/1000)}K` : `$${Math.round(opp.volume)}`;
            const typeStr = opp.type.padEnd(11);
            console.log(`  ${typeStr} | YES:${(opp.yesPrice*100).toFixed(0)}¢ | ${opp.daysLeft}d | ${volStr.padStart(6)} | ${opp.category} | ${opp.question?.slice(0, 40)}`);
        }
        console.log();
    }
}

async function main() {
    const args = process.argv.slice(2);
    const shouldSave = args.includes('--save');
    const categoryFilter = args.find(arg => arg.startsWith('--category='))?.split('=')[1];
    const minVolumeArg = args.find(arg => arg.startsWith('--min-volume='));
    const minVolume = minVolumeArg ? parseInt(minVolumeArg.split('=')[1]) : 0;
    
    try {
        const analysis = await analyzeUniverse();
        
        if (shouldSave) {
            console.log(`💾 Saving analysis to ${UNIVERSE_FILE}...`);
            fs.writeFileSync(UNIVERSE_FILE, JSON.stringify(analysis, null, 2));
            console.log("   Saved successfully!\n");
        }
        
        displayResults(analysis, { categoryFilter, minVolume });
        
        console.log("💡 USAGE TIPS:");
        console.log("  • High volume + extreme prices = market consensus worth investigating");
        console.log("  • Cheap YES + research = potential high-return asymmetric bets");
        console.log("  • Near expiry + clear outcome = time-decay alpha");
        console.log("  • Use --save to export data for further analysis");
        console.log();
        
    } catch (error) {
        console.error("❌ Error:", error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}