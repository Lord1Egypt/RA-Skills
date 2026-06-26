#!/usr/bin/env node
/**
 * Scan Kalshi markets for edges vs Sofascore de-vigged odds.
 * 
 * Usage:
 *   node scan-edges.js --category tennis
 *   node scan-edges.js --category ncaab
 *   node scan-edges.js --min-edge 4
 */

const https = require('https');
const { kalshiApi, getBalance, getMarket } = require('./kalshi-auth');

function parseArgs() {
  const args = { category: 'tennis', minEdge: 4 };
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--category') args.category = process.argv[++i];
    if (process.argv[i] === '--min-edge') args.minEdge = parseFloat(process.argv[++i]);
  }
  return args;
}

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch(e) { resolve(null); } });
    }).on('error', reject);
  });
}

function deVig(oddsA, oddsB) {
  const impA = 1 / oddsA;
  const impB = 1 / oddsB;
  const total = impA + impB;
  return { trueA: impA / total, trueB: impB / total };
}

function parseFractional(frac) {
  const [num, den] = frac.split('/').map(Number);
  return (num / den) + 1; // Convert to decimal
}

async function scanTennis(minEdge) {
  console.log('🎾 Scanning tennis (Sofascore vs Kalshi)...\n');
  
  // Get today's scheduled events from Sofascore
  const today = new Date().toISOString().split('T')[0];
  const scheduled = await fetch(`https://api.sofascore.com/api/v1/sport/tennis/scheduled-events/${today}`);
  if (!scheduled?.events) { console.log('No events found'); return; }

  // Get Kalshi tennis series
  const series = ['KXATPMATCH', 'KXATPCHALLENGERMATCH'];
  const kalshiEvents = {};
  
  for (const s of series) {
    const data = await kalshiApi('GET', '/trade-api/v2/events?series_ticker=' + s + '&status=open&limit=50');
    if (data.events) {
      for (const e of data.events) {
        kalshiEvents[e.event_ticker] = e;
      }
    }
  }

  console.log(`Kalshi: ${Object.keys(kalshiEvents).length} tennis events`);
  console.log(`Sofascore: ${scheduled.events.length} scheduled events\n`);

  // For each Sofascore event with odds, find matching Kalshi market
  const edges = [];
  
  for (const event of scheduled.events) {
    const h = event.homeTeam?.name || '';
    const a = event.awayTeam?.name || '';
    
    // Get Sofascore odds
    const oddsData = await fetch(`https://api.sofascore.com/api/v1/event/${event.id}/odds/1/all`);
    if (!oddsData?.markets?.[0]?.choices) continue;
    
    const choices = oddsData.markets[0].choices;
    if (choices.length !== 2) continue;
    
    const decA = parseFractional(choices[0].fractionalValue);
    const decB = parseFractional(choices[1].fractionalValue);
    const { trueA, trueB } = deVig(decA, decB);
    
    // Try to match with Kalshi markets
    const hLast = h.split(' ').pop().toLowerCase().substring(0, 3);
    const aLast = a.split(' ').pop().toLowerCase().substring(0, 3);
    
    // Search Kalshi events by player name
    for (const [ticker, kEvent] of Object.entries(kalshiEvents)) {
      const kTitle = (kEvent.title || '').toLowerCase();
      if (kTitle.includes(h.toLowerCase().split(' ').pop()) || kTitle.includes(a.toLowerCase().split(' ').pop())) {
        // Found a match — get market prices
        if (kEvent.markets) {
          for (const m of kEvent.markets) {
            const mData = await getMarket(m.ticker);
            if (!mData) continue;
            
            const yesBid = parseFloat(mData.yes_bid_dollars) || 0;
            const yesAsk = parseFloat(mData.yes_ask_dollars) || 1;
            
            // Determine which player this market is for
            const mTitle = (mData.title || mData.ticker || '').toLowerCase();
            let trueProb, playerName;
            
            if (mTitle.includes(h.toLowerCase().split(' ').pop())) {
              trueProb = trueA;
              playerName = h;
            } else {
              trueProb = trueB;
              playerName = a;
            }
            
            const edgeBuy = (trueProb * 100) - (yesAsk * 100);
            
            if (edgeBuy >= minEdge) {
              edges.push({
                player: playerName,
                ticker: m.ticker,
                trueProb: (trueProb * 100).toFixed(1) + '%',
                kalshiAsk: yesAsk,
                edge: edgeBuy.toFixed(1) + '%',
                volume: mData.volume_fp
              });
            }
          }
        }
        break;
      }
    }
  }

  if (edges.length === 0) {
    console.log('❌ No edges found above ' + minEdge + '% threshold');
  } else {
    console.log('✅ EDGES FOUND:');
    edges.forEach(e => {
      console.log(`  ${e.player} | ${e.ticker} | True: ${e.trueProb} | Ask: ${e.kalshiAsk} | Edge: ${e.edge} | Vol: ${e.volume}`);
    });
  }
  
  return edges;
}

async function main() {
  const args = parseArgs();
  const bal = await getBalance();
  console.log(`💰 Balance: $${bal.cash} cash | $${bal.portfolio} portfolio\n`);
  
  if (args.category === 'tennis') {
    await scanTennis(args.minEdge);
  } else {
    console.log('Supported categories: tennis (more coming)');
  }
}

main().catch(e => console.error(e));
