#!/usr/bin/env node
/**
 * Edge Finder — Detects arbitrage, time decay, order book imbalance, and momentum
 * Converted from Python to Node.js for self-contained operation
 * 
 * Usage:
 *   node edge_finder.cjs                    # Full multi-strategy scan
 *   node edge_finder.cjs --no-books         # Skip order book checks (faster)
 *   node edge_finder.cjs --max-books=50     # Limit order book checks
 *   node edge_finder.cjs --top-20           # Show only top 20 opportunities
 *   node edge_finder.cjs --min-ev=5         # Minimum 5% expected value
 */

const fs = require('fs');
const path = require('path');

const GAMMA_BASE = "https://gamma-api.polymarket.com";
const CLOB_BASE = "https://clob.polymarket.com";
const RATE_LIMIT = 200; // milliseconds between requests
const DATA_DIR = path.join(__dirname, 'data');
const EDGES_FILE = path.join(DATA_DIR, 'edge_opportunities.json');

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// Opportunity class equivalent
class Opportunity {
    constructor(type, market, details = {}) {
        this.type = type;
        this.market = market;
        this.details = details;
        this.timestamp = new Date().toISOString();
    }
    
    display() {
        const m = this.market;
        const d = this.details;
        const q = m.question || "?";
        const yes = m.yes_price || 0;
        
        console.log(`\n${'─'.repeat(78)}`);
        console.log(`  [${this.type.toUpperCase()}] ${q.slice(0, 60)}`);
        console.log(`${'─'.repeat(78)}`);
        console.log(`  Current Price:  Yes=${(yes*100).toFixed(1)}¢  No=${((m.no_price||0)*100).toFixed(1)}¢`);
        
        if (d.fair_value !== undefined) {
            console.log(`  Est. Fair Value: ${(d.fair_value*100).toFixed(1)}¢`);
        }
        if (d.reason) {
            console.log(`  Reasoning:      ${d.reason}`);
        }
        if (d.position) {
            console.log(`  Suggested:      ${d.position}`);
        }
        if (d.ev !== undefined) {
            console.log(`  Expected Value:  ${d.ev.toFixed(1)}%`);
        }
        if (d.risk) {
            console.log(`  Risk:           ${d.risk}`);
        }
        
        // Display other details
        Object.entries(d).forEach(([key, value]) => {
            if (!['fair_value', 'reason', 'position', 'ev', 'risk'].includes(key)) {
                console.log(`  ${key}: ${value}`);
            }
        });
    }
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchMarkets() {
    console.log("🔍 Fetching active markets...");
    const markets = [];
    let offset = 0;
    
    while (true) {
        const url = `${GAMMA_BASE}/markets?active=true&closed=false&limit=100&offset=${offset}`;
        try {
            const response = await fetch(url);
            if (response.status === 429) {
                console.log("  Rate limited, waiting...");
                await sleep(2000);
                continue;
            }
            if (!response.ok) {
                break;
            }
            const data = await response.json();
            if (!data || data.length === 0) {
                break;
            }
            markets.push(...data);
            process.stdout.write(`\r  Fetched ${markets.length} markets...`);
            offset += 100;
            await sleep(RATE_LIMIT);
        } catch (error) {
            console.log(`\n  Error fetching markets: ${error.message}`);
            break;
        }
    }
    
    console.log(`\n  Total: ${markets.length} active markets`);
    return markets;
}

async function fetchOrderBook(tokenId) {
    try {
        const response = await fetch(`${CLOB_BASE}/book?token_id=${tokenId}`);
        if (!response.ok) return null;
        const book = await response.json();
        return book;
    } catch (error) {
        return null;
    }
}

// Time decay detection
function detectTimeDecay(market) {
    const opportunities = [];
    
    try {
        const endDate = new Date(market.endDate || market.end_date_iso);
        const now = new Date();
        const daysLeft = (endDate - now) / (1000 * 60 * 60 * 24);
        
        if (daysLeft < 0 || daysLeft > 30) return opportunities;
        
        const prices = JSON.parse(market.outcomePrices || '["0.5", "0.5"]');
        const yesPrice = parseFloat(prices[0]);
        const volume = parseFloat(market.volumeNum || 0);
        
        // Near-expiry opportunities
        if (daysLeft < 7 && volume > 10000) {
            let reason, position, ev;
            
            if (yesPrice > 0.85 && daysLeft < 3) {
                reason = `${daysLeft.toFixed(1)} days left, market at ${(yesPrice*100).toFixed(0)}¢ - likely resolves YES`;
                position = `BUY YES at ${(yesPrice*100).toFixed(0)}¢`;
                ev = ((1 - yesPrice) / yesPrice) * 100 * 0.8; // 80% confidence
            } else if (yesPrice < 0.15 && daysLeft < 3) {
                reason = `${daysLeft.toFixed(1)} days left, market at ${(yesPrice*100).toFixed(0)}¢ - likely resolves NO`;
                position = `BUY NO at ${((1-yesPrice)*100).toFixed(0)}¢`;
                ev = (yesPrice / (1 - yesPrice)) * 100 * 0.8;
            } else if (daysLeft < 1 && Math.abs(yesPrice - 0.5) > 0.2) {
                reason = `<24h left, directional bias at ${(yesPrice*100).toFixed(0)}¢`;
                position = yesPrice > 0.5 ? "BUY YES" : "BUY NO";
                ev = Math.abs(yesPrice - 0.5) * 100;
            }
            
            if (reason) {
                opportunities.push(new Opportunity('TIME_DECAY', {
                    ...market,
                    yes_price: yesPrice,
                    no_price: 1 - yesPrice
                }, {
                    reason,
                    position,
                    ev,
                    days_left: daysLeft,
                    risk: 'Medium - time-based resolution'
                }));
            }
        }
    } catch (error) {
        // Skip malformed markets
    }
    
    return opportunities;
}

// Volume spike detection
function detectMomentum(market, allMarkets) {
    const opportunities = [];
    
    try {
        const volume = parseFloat(market.volumeNum || 0);
        const prices = JSON.parse(market.outcomePrices || '["0.5", "0.5"]');
        const yesPrice = parseFloat(prices[0]);
        
        if (volume < 50000) return opportunities;
        
        // Find similar markets by category/keyword matching for comparison
        const question = (market.question || '').toLowerCase();
        const keywords = question.split(' ').filter(w => w.length > 3);
        
        const similarMarkets = allMarkets.filter(m => {
            if (m.id === market.id) return false;
            const otherQuestion = (m.question || '').toLowerCase();
            return keywords.some(kw => otherQuestion.includes(kw));
        });
        
        if (similarMarkets.length > 2) {
            const avgVolume = similarMarkets.reduce((sum, m) => sum + parseFloat(m.volumeNum || 0), 0) / similarMarkets.length;
            const volumeMultiple = volume / (avgVolume || 1);
            
            if (volumeMultiple > 3 && volume > 100000) {
                const reason = `Volume spike: ${Math.round(volumeMultiple)}x normal (${volume.toLocaleString()} vs ${avgVolume.toFixed(0)} avg)`;
                const position = volume > 500000 ? 
                    (yesPrice > 0.6 ? "TREND: YES momentum" : yesPrice < 0.4 ? "TREND: NO momentum" : "WATCH: unclear direction") :
                    "INVESTIGATE: high volume, determine cause";
                
                opportunities.push(new Opportunity('MOMENTUM', {
                    ...market,
                    yes_price: yesPrice,
                    no_price: 1 - yesPrice
                }, {
                    reason,
                    position,
                    volume_multiple: volumeMultiple,
                    risk: 'High - momentum can reverse',
                    ev: Math.min(volumeMultiple * 2, 15) // Cap at 15%
                }));
            }
        }
    } catch (error) {
        // Skip malformed markets
    }
    
    return opportunities;
}

// Book imbalance detection
async function detectBookImbalance(market, checkBooks = true) {
    const opportunities = [];
    
    if (!checkBooks) return opportunities;
    
    try {
        const tokenIds = JSON.parse(market.clobTokenIds || '[]');
        if (tokenIds.length < 2) return opportunities;
        
        const yesTokenId = tokenIds[0];
        const noTokenId = tokenIds[1];
        
        const [yesBook, noBook] = await Promise.all([
            fetchOrderBook(yesTokenId),
            fetchOrderBook(noTokenId)
        ]);
        
        if (!yesBook || !noBook || !yesBook.bids || !noBook.bids) {
            return opportunities;
        }
        
        // Calculate liquidity imbalances
        const yesBidLiq = yesBook.bids.reduce((sum, bid) => sum + parseFloat(bid.size), 0);
        const yesAskLiq = yesBook.asks.reduce((sum, ask) => sum + parseFloat(ask.size), 0);
        const noBidLiq = noBook.bids.reduce((sum, bid) => sum + parseFloat(bid.size), 0);
        const noAskLiq = noBook.asks.reduce((sum, ask) => sum + parseFloat(ask.size), 0);
        
        const totalBuyInterest = yesBidLiq + noAskLiq; // People wanting to buy YES or sell NO
        const totalSellInterest = yesAskLiq + noBidLiq; // People wanting to sell YES or buy NO
        
        const imbalanceRatio = totalBuyInterest / (totalSellInterest || 1);
        
        if (imbalanceRatio > 2 || imbalanceRatio < 0.5) {
            const prices = JSON.parse(market.outcomePrices || '["0.5", "0.5"]');
            const yesPrice = parseFloat(prices[0]);
            
            const direction = imbalanceRatio > 2 ? 'bullish' : 'bearish';
            const suggestedSide = imbalanceRatio > 2 ? 'YES' : 'NO';
            const reason = `Book imbalance: ${imbalanceRatio.toFixed(1)}:1 ${direction} (buy interest >> sell interest)`;
            
            opportunities.push(new Opportunity('BOOK_IMBALANCE', {
                ...market,
                yes_price: yesPrice,
                no_price: 1 - yesPrice
            }, {
                reason,
                position: `BUY ${suggestedSide} - book supports move`,
                imbalance_ratio: imbalanceRatio,
                yes_bid_liq: yesBidLiq,
                yes_ask_liq: yesAskLiq,
                no_bid_liq: noBidLiq,
                no_ask_liq: noAskLiq,
                risk: 'Medium - liquidity can shift',
                ev: Math.min(Math.abs(Math.log(imbalanceRatio)) * 10, 12)
            }));
        }
    } catch (error) {
        // Skip on error
    }
    
    return opportunities;
}

// Price inefficiency detection
function detectPriceInefficiency(market) {
    const opportunities = [];
    
    try {
        const prices = JSON.parse(market.outcomePrices || '["0.5", "0.5"]');
        const yesPrice = parseFloat(prices[0]);
        const noPrice = parseFloat(prices[1]);
        const volume = parseFloat(market.volumeNum || 0);
        
        // Check if prices don't sum to 1 (arbitrage opportunity)
        const priceSum = yesPrice + noPrice;
        if (Math.abs(priceSum - 1) > 0.05 && volume > 25000) {
            const reason = priceSum > 1 ? 
                `Overpriced: YES+NO = ${(priceSum*100).toFixed(1)}¢ > 100¢` :
                `Underpriced: YES+NO = ${(priceSum*100).toFixed(1)}¢ < 100¢`;
            
            const position = priceSum > 1 ? 
                "ARBITRAGE: Sell both sides" : 
                "ARBITRAGE: Buy both sides";
                
            opportunities.push(new Opportunity('PRICE_INEFFICIENCY', {
                ...market,
                yes_price: yesPrice,
                no_price: noPrice
            }, {
                reason,
                position,
                price_sum: priceSum,
                arbitrage_profit: Math.abs(1 - priceSum),
                risk: 'Low - mathematical arbitrage',
                ev: Math.abs(1 - priceSum) * 100
            }));
        }
        
        // Extreme price + high volume = potential overreaction
        if ((yesPrice < 0.05 || yesPrice > 0.95) && volume > 100000) {
            const isExtremeLow = yesPrice < 0.05;
            const reason = isExtremeLow ?
                `Extreme pessimism: ${(yesPrice*100).toFixed(1)}¢ with $${Math.round(volume/1000)}K volume` :
                `Extreme optimism: ${(yesPrice*100).toFixed(1)}¢ with $${Math.round(volume/1000)}K volume`;
                
            opportunities.push(new Opportunity('EXTREME_PRICING', {
                ...market,
                yes_price: yesPrice,
                no_price: noPrice
            }, {
                reason,
                position: isExtremeLow ? "CONTRARIAN: Consider YES" : "CONTRARIAN: Consider NO",
                risk: 'High - extreme prices often justified',
                ev: Math.min((isExtremeLow ? (1-yesPrice)/yesPrice : yesPrice/(1-yesPrice)) * 10, 20)
            }));
        }
    } catch (error) {
        // Skip malformed markets
    }
    
    return opportunities;
}

async function findAllOpportunities(options = {}) {
    const { checkBooks = true, maxBooks = 100, minEV = 0, topN = null } = options;
    
    const markets = await fetchMarkets();
    const allOpportunities = [];
    
    console.log("\n🔍 Analyzing opportunities...");
    
    let booksChecked = 0;
    for (let i = 0; i < markets.length; i++) {
        const market = markets[i];
        
        // Time decay opportunities
        const timeDecayOpps = detectTimeDecay(market);
        allOpportunities.push(...timeDecayOpps);
        
        // Momentum opportunities
        const momentumOpps = detectMomentum(market, markets);
        allOpportunities.push(...momentumOpps);
        
        // Price inefficiency opportunities
        const priceOpps = detectPriceInefficiency(market);
        allOpportunities.push(...priceOpps);
        
        // Book imbalance (limited by maxBooks)
        if (checkBooks && booksChecked < maxBooks) {
            const bookOpps = await detectBookImbalance(market, true);
            allOpportunities.push(...bookOpps);
            if (bookOpps.length > 0) booksChecked++;
            await sleep(100); // Rate limit for order book calls
        }
        
        if (i % 100 === 0) {
            process.stdout.write(`\r  Analyzed ${i}/${markets.length} markets... (${booksChecked} books checked)`);
        }
    }
    
    console.log(`\n  Found ${allOpportunities.length} total opportunities`);
    
    // Filter by minimum EV
    const filtered = allOpportunities.filter(opp => (opp.details.ev || 0) >= minEV);
    console.log(`  ${filtered.length} opportunities with EV >= ${minEV}%`);
    
    // Sort by EV
    filtered.sort((a, b) => (b.details.ev || 0) - (a.details.ev || 0));
    
    // Take top N if specified
    const finalOpps = topN ? filtered.slice(0, topN) : filtered;
    
    return finalOpps;
}

function displayOpportunities(opportunities) {
    if (opportunities.length === 0) {
        console.log("\n📭 No opportunities found with current filters");
        return;
    }
    
    console.log(`\n🎯 FOUND ${opportunities.length} OPPORTUNITIES`);
    console.log("═".repeat(80));
    
    // Group by type
    const byType = {};
    opportunities.forEach(opp => {
        if (!byType[opp.type]) byType[opp.type] = [];
        byType[opp.type].push(opp);
    });
    
    Object.entries(byType).forEach(([type, opps]) => {
        console.log(`\n📊 ${type.replace('_', ' ')} (${opps.length} opportunities)`);
        console.log("─".repeat(80));
        
        opps.slice(0, 5).forEach(opp => {
            const m = opp.market;
            const d = opp.details;
            const ev = d.ev ? `+${d.ev.toFixed(1)}%` : 'N/A';
            const vol = m.volumeNum ? `$${Math.round(m.volumeNum/1000)}K` : '$0';
            
            console.log(`  ${ev.padStart(6)} EV | ${vol.padStart(6)} vol | ${m.question?.slice(0, 60) || 'Unknown market'}`);
            console.log(`           | ${d.reason || 'No reason provided'}`);
            console.log(`           | ${d.position || 'No position suggested'}`);
            console.log();
        });
    });
    
    // Summary statistics
    const totalEV = opportunities.reduce((sum, opp) => sum + (opp.details.ev || 0), 0);
    const avgEV = totalEV / opportunities.length;
    const maxEV = Math.max(...opportunities.map(opp => opp.details.ev || 0));
    
    console.log("📊 SUMMARY STATISTICS");
    console.log("─".repeat(40));
    console.log(`  Total opportunities: ${opportunities.length}`);
    console.log(`  Average EV: ${avgEV.toFixed(1)}%`);
    console.log(`  Maximum EV: ${maxEV.toFixed(1)}%`);
    console.log(`  Total EV: ${totalEV.toFixed(1)}%`);
    
    const typeCount = Object.keys(byType).length;
    console.log(`  Strategy types: ${typeCount}`);
    Object.entries(byType).forEach(([type, opps]) => {
        console.log(`    ${type.replace('_', ' ')}: ${opps.length}`);
    });
}

async function main() {
    const args = process.argv.slice(2);
    const checkBooks = !args.includes('--no-books');
    const maxBooksArg = args.find(arg => arg.startsWith('--max-books='));
    const maxBooks = maxBooksArg ? parseInt(maxBooksArg.split('=')[1]) : 100;
    const topNArg = args.find(arg => arg.startsWith('--top-'));
    const topN = topNArg ? parseInt(topNArg.replace('--top-', '')) : null;
    const minEVArg = args.find(arg => arg.startsWith('--min-ev='));
    const minEV = minEVArg ? parseFloat(minEVArg.split('=')[1]) : 0;
    const shouldSave = args.includes('--save');
    
    try {
        console.log("🚀 POLYMARKET EDGE FINDER");
        console.log(`   Books: ${checkBooks ? `Yes (max ${maxBooks})` : 'No'}`);
        console.log(`   Min EV: ${minEV}%`);
        console.log(`   Results: ${topN ? `Top ${topN}` : 'All'}`);
        console.log();
        
        const opportunities = await findAllOpportunities({
            checkBooks,
            maxBooks,
            minEV,
            topN
        });
        
        if (shouldSave) {
            const data = {
                timestamp: new Date().toISOString(),
                opportunities: opportunities.map(opp => ({
                    type: opp.type,
                    market_id: opp.market.id,
                    market_question: opp.market.question,
                    details: opp.details
                }))
            };
            fs.writeFileSync(EDGES_FILE, JSON.stringify(data, null, 2));
            console.log(`💾 Saved ${opportunities.length} opportunities to ${EDGES_FILE}`);
        }
        
        displayOpportunities(opportunities);
        
        console.log("\n💡 NEXT STEPS:");
        console.log("  1. Research the fundamentals behind high-EV opportunities");
        console.log("  2. Check recent news/events for momentum plays");
        console.log("  3. Verify order book data before trading");
        console.log("  4. Size positions based on risk level");
        console.log("  5. Monitor for changes in market conditions");
        
    } catch (error) {
        console.error("❌ Error:", error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}