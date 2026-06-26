#!/usr/bin/env node
/**
 * Alpha Scanner — Detects mispriced markets using volume, time decay, and momentum signals
 * 
 * Usage:
 *   node alpha_scan.cjs                    # Full scan with all strategies
 *   node alpha_scan.cjs --cheap            # Only cheap YES plays (5-35¢)
 *   node alpha_scan.cjs --expiry           # Only near-expiry opportunities
 *   node alpha_scan.cjs --volume           # Only high-volume movers
 *   node alpha_scan.cjs --coin-flips       # Only 40-60¢ opportunities
 */

const GAMMA_BASE = "https://gamma-api.polymarket.com";

async function fetchMarkets(maxMarkets = 2000) {
    console.log(`🔍 Fetching up to ${maxMarkets} markets...`);
    let allMarkets = [];
    for (let offset = 0; offset < maxMarkets; offset += 100) {
        const resp = await fetch(`${GAMMA_BASE}/markets?closed=false&active=true&limit=100&offset=${offset}&order=volumeNum&ascending=false`);
        if (!resp.ok) {
            console.error(`Failed to fetch markets at offset ${offset}: ${resp.status}`);
            break;
        }
        const batch = await resp.json();
        if (!batch.length) break;
        allMarkets = allMarkets.concat(batch);
        process.stdout.write(`\r  Fetched ${allMarkets.length} markets...`);
    }
    console.log(`\n  Found ${allMarkets.length} active markets\n`);
    return allMarkets;
}

async function main() {
    const args = process.argv.slice(2);
    const cheapOnly = args.includes('--cheap');
    const expiryOnly = args.includes('--expiry');
    const volumeOnly = args.includes('--volume');
    const coinFlipsOnly = args.includes('--coin-flips');
    const showAll = !cheapOnly && !expiryOnly && !volumeOnly && !coinFlipsOnly;

    const allMarkets = await fetchMarkets();
    
    // === NEAR-EXPIRY HIGH CONFIDENCE (resolving soon, clear winner) ===
    if (showAll || expiryOnly) {
        console.log("=== 🔥 NEAR-EXPIRY OPPORTUNITIES (< 14 days, high volume) ===");
        const now = Date.now();
        const nearExpiry = allMarkets.filter(m => {
            const end = new Date(m.endDate || m.end_date_iso).getTime();
            const daysLeft = (end - now) / 86400000;
            return daysLeft > 0 && daysLeft < 14 && m.volumeNum > 50000;
        }).sort((a, b) => b.volumeNum - a.volumeNum);
        
        console.log(`Found ${nearExpiry.length} near-expiry markets with >$50K volume\n`);
        
        for (const m of nearExpiry.slice(0, 15)) {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const end = new Date(m.endDate || m.end_date_iso);
            const daysLeft = ((end - now) / 86400000).toFixed(1);
            const yesP = parseFloat(prices[0] || 0);
            const noP = parseFloat(prices[1] || 0);
            
            // Flag extreme prices as potential opportunities
            const flag = yesP > 0.85 ? '🟢' : yesP < 0.15 ? '🔴' : yesP > 0.7 ? '🟡' : '';
            
            console.log(`  ${flag} ${daysLeft}d | YES:${(yesP*100).toFixed(0)}¢ NO:${(noP*100).toFixed(0)}¢ | Vol:$${Math.round(m.volumeNum/1000)}K | ${m.question?.slice(0,70)}`);
        }
        console.log();
    }
    
    // === CHEAP YES PLAYS (5-35¢, high volume = market disagrees with price) ===
    if (showAll || cheapOnly) {
        console.log("=== 💰 CHEAP YES PLAYS (5-35¢, vol > $100K) ===");
        const cheapYes = allMarkets.filter(m => {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const yesP = parseFloat(prices[0] || 0);
            return yesP >= 0.05 && yesP <= 0.35 && m.volumeNum > 100000;
        }).sort((a, b) => b.volumeNum - a.volumeNum);
        
        console.log(`Found ${cheapYes.length} cheap YES opportunities with >$100K volume\n`);
        
        for (const m of cheapYes.slice(0, 15)) {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const end = new Date(m.endDate || m.end_date_iso);
            const daysLeft = ((end - now) / 86400000).toFixed(0);
            const yesP = parseFloat(prices[0]);
            
            // Calculate potential return (if YES wins)
            const potentialReturn = ((1 - yesP) / yesP * 100).toFixed(0);
            
            console.log(`  YES:${(yesP*100).toFixed(0)}¢ (${potentialReturn}x) | ${daysLeft}d | Vol:$${Math.round(m.volumeNum/1000)}K | ${m.question?.slice(0,65)}`);
        }
        console.log();
    }
    
    // === MID-RANGE CONVICTION (40-60¢ — coin flips where research gives edge) ===
    if (showAll || coinFlipsOnly) {
        console.log("=== 🎯 COIN FLIPS (40-60¢, vol > $200K) ===");
        const coinFlips = allMarkets.filter(m => {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const yesP = parseFloat(prices[0] || 0);
            return yesP >= 0.40 && yesP <= 0.60 && m.volumeNum > 200000;
        }).sort((a, b) => b.volumeNum - a.volumeNum);
        
        console.log(`Found ${coinFlips.length} coin-flip opportunities with >$200K volume\n`);
        
        for (const m of coinFlips.slice(0, 15)) {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const end = new Date(m.endDate || m.end_date_iso);
            const daysLeft = ((end - now) / 86400000).toFixed(0);
            const yesP = parseFloat(prices[0]);
            
            // Show how close to 50/50
            const deviation = Math.abs(yesP - 0.5) * 100;
            
            console.log(`  YES:${(yesP*100).toFixed(0)}¢ (±${deviation.toFixed(0)}¢) | ${daysLeft}d | Vol:$${Math.round(m.volumeNum/1000)}K | ${m.question?.slice(0,62)}`);
        }
        console.log();
    }
    
    // === HIGH VOLUME TODAY (something's happening) ===
    if (showAll || volumeOnly) {
        console.log("=== 📈 HIGHEST RECENT VOLUME (market movers) ===");
        const movers = allMarkets.filter(m => m.volumeNum > 500000)
            .sort((a, b) => b.volumeNum - a.volumeNum);
        
        console.log(`Found ${movers.length} high-volume markets (>$500K)\n`);
        
        for (const m of movers.slice(0, 15)) {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const end = new Date(m.endDate || m.end_date_iso);
            const daysLeft = ((end - now) / 86400000).toFixed(0);
            const yesP = parseFloat(prices[0]);
            
            // Flag based on volume size
            let volumeFlag = '';
            const volMil = m.volumeNum / 1000000;
            if (volMil > 10) volumeFlag = '🔥';
            else if (volMil > 5) volumeFlag = '📈';
            else if (volMil > 2) volumeFlag = '📊';
            
            console.log(`  ${volumeFlag} YES:${(yesP*100).toFixed(0)}¢ | ${daysLeft}d | Vol:$${Math.round(m.volumeNum/1000)}K | ${m.question?.slice(0,62)}`);
        }
        console.log();
    }
    
    // === SUMMARY STATS ===
    if (showAll) {
        console.log("=== 📊 MARKET OVERVIEW ===");
        const totalVolume = allMarkets.reduce((sum, m) => sum + m.volumeNum, 0);
        const avgVolume = totalVolume / allMarkets.length;
        
        // Price distribution
        const priceDistribution = { 
            veryLow: 0,    // 0-10¢
            low: 0,        // 10-30¢
            coinFlip: 0,   // 30-70¢
            high: 0,       // 70-90¢
            veryHigh: 0    // 90-100¢
        };
        
        for (const m of allMarkets) {
            const prices = JSON.parse(m.outcomePrices || "[]");
            const yesP = parseFloat(prices[0] || 0);
            if (yesP < 0.1) priceDistribution.veryLow++;
            else if (yesP < 0.3) priceDistribution.low++;
            else if (yesP < 0.7) priceDistribution.coinFlip++;
            else if (yesP < 0.9) priceDistribution.high++;
            else priceDistribution.veryHigh++;
        }
        
        console.log(`  Total markets: ${allMarkets.length.toLocaleString()}`);
        console.log(`  Total volume: $${(totalVolume / 1000000).toFixed(1)}M`);
        console.log(`  Avg volume: $${Math.round(avgVolume).toLocaleString()}`);
        console.log();
        console.log(`  Price distribution:`);
        console.log(`    0-10¢:  ${priceDistribution.veryLow.toLocaleString()} markets (${(priceDistribution.veryLow/allMarkets.length*100).toFixed(1)}%)`);
        console.log(`    10-30¢: ${priceDistribution.low.toLocaleString()} markets (${(priceDistribution.low/allMarkets.length*100).toFixed(1)}%)`);
        console.log(`    30-70¢: ${priceDistribution.coinFlip.toLocaleString()} markets (${(priceDistribution.coinFlip/allMarkets.length*100).toFixed(1)}%)`);
        console.log(`    70-90¢: ${priceDistribution.high.toLocaleString()} markets (${(priceDistribution.high/allMarkets.length*100).toFixed(1)}%)`);
        console.log(`    90-99¢: ${priceDistribution.veryHigh.toLocaleString()} markets (${(priceDistribution.veryHigh/allMarkets.length*100).toFixed(1)}%)`);
        console.log();
    }
    
    // === ACTIONABLE INSIGHTS ===
    if (showAll) {
        console.log("=== 💡 TRADING INSIGHTS ===");
        console.log("  🔥 Near-expiry + extreme prices = highest confidence");
        console.log("  💰 Cheap YES + high volume = market disagreement (research opportunity)");
        console.log("  📈 Volume spikes = news/events driving repricing");
        console.log("  🎯 Coin flips = where fundamental analysis matters most");
        console.log();
        console.log("  Next steps:");
        console.log("    1. Research the fundamentals of flagged opportunities");
        console.log("    2. Check recent news/events for volume spikes");
        console.log("    3. Compare to prediction models or expert opinions");
        console.log("    4. Size positions based on edge confidence");
    }
}

main().catch(console.error);