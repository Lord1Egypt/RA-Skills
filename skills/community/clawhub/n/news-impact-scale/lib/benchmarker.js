/**
 * benchmarker.js
 * Researches historical benchmarks via web search to ground future projections.
 * Uses OpenClaw's batch_web_search when available (via parent agent).
 * Stores and retrieves benchmarks from benchmarks.json.
 */

const fs   = require('fs');
const path = require('path');

const BENCHMARK_F = path.join(__dirname, '..', 'benchmarks.json');

function loadBenchmarks() {
  try { return JSON.parse(fs.readFileSync(BENCHMARK_F, 'utf8')); }
  catch { return { locations: {} }; }
}

function saveBenchmarks(data) {
  fs.writeFileSync(BENCHMARK_F, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Add a new benchmark case discovered during analysis.
 * Call this after finding useful historical data.
 */
function addBenchmark({ location, eventType, description, year, recoveryDays, recoveryDescription, previousState, futureState, recoverySpeed }) {
  const bm = loadBenchmarks();
  if (!bm.locations[location]) bm.locations[location] = {};
  if (!bm.locations[location][eventType]) bm.locations[location][eventType] = [];

  const entry = {
    description: description || '',
    year: year || new Date().getFullYear(),
    recoveryDays: recoveryDays || null,
    recoveryDescription: recoveryDescription || '',
    previousState: previousState || '',
    futureState: futureState || '',
    recoverySpeed: recoverySpeed || 'moderate',
  };

  // Avoid exact duplicates
  const exists = bm.locations[location][eventType].some(
    e => e.description === entry.description && e.year === entry.year
  );
  if (!exists) {
    bm.locations[location][eventType].unshift(entry);
    bm.locations[location][eventType].sort((a, b) => (b.year || 0) - (a.year || 0));
    saveBenchmarks(bm);
  }
  return entry;
}

/**
 * Get cached benchmarks for a location + event type.
 */
function getCachedBenchmarks(location, eventType) {
  const bm = loadBenchmarks();
  const loc = bm.locations[location] || {};
  return (loc[eventType] || []).slice(0, 5);
}

/**
 * Build search queries for historical benchmark research.
 * Returns an array of {query, eventType, location} to feed into web search.
 */
function buildBenchmarkQueries(eventType, location, affectedSystems) {
  const queries = [];
  const year = new Date().getFullYear();

  const typeMap = {
    'natural disaster': 'earthquake flood wildfire hurricane recovery timeline',
    'infrastructure':   'bridge collapse road closure repair timeline recovery',
    'conflict':         'military conflict economic impact recovery timeline',
    'corporate':        'company bankruptcy restructuring recovery timeline',
    'economic':         'recession economic recovery timeline history',
    'health':           'disease outbreak recovery health system timeline',
    'climate':          'climate disaster environmental damage recovery timeline',
    'political':        'election political change impact timeline',
    'technology':       'tech regulation antitrust impact timeline',
  };

  const suffix = typeMap[eventType] || 'event impact recovery timeline history';
  queries.push(`${location} ${suffix} ${year - 5}..${year}`);
  queries.push(`${location} similar event recovery time historical data`);
  queries.push(`how long did ${location} ${eventType} recovery take past events`);

  return queries.slice(0, 4);
}

/**
 * Parse a web search result snippet into a benchmark entry.
 * Used when the agent finds benchmark data from search results.
 */
function parseBenchmarkFromText(text, eventType, location) {
  const lines = text.split('\n');
  const result = { location, eventType, description: '', year: null, recoveryDays: null };

  // Look for numbers (days, months, years) in the text
  const daysMatch  = text.match(/(\d+)\s*(?:day|days|d)/i);
  const monthsMatch = text.match(/(\d+)\s*(?:month|months|m)/i);
  const yearsMatch  = text.match(/(\d+)\s*(?:year|years|y)/i);

  if (monthsMatch) result.recoveryDays = parseInt(monthsMatch[1]) * 30;
  else if (daysMatch) result.recoveryDays = parseInt(daysMatch[1]);
  else if (yearsMatch) result.recoveryDays = parseInt(yearsMatch[1]) * 365;

  // Extract year
  const yearMatch = text.match(/\b(19\d\d|20\d\d)\b/);
  if (yearMatch) result.year = parseInt(yearMatch[1]);

  // Recovery description
  if (result.recoveryDays) {
    result.recoveryDescription = `Estimated ~${result.recoveryDays} day(s) to recover, based on historical data`;
    result.recoverySpeed = result.recoveryDays <= 14 ? 'fast'
      : result.recoveryDays <= 60 ? 'moderate'
      : result.recoveryDays <= 180 ? 'slow' : 'stalled';
    result.futureState = `System expected to recover within ~${result.recoveryDays} day(s)`;
  }

  result.description = text.slice(0, 150);
  return result;
}

module.exports = { addBenchmark, getCachedBenchmarks, buildBenchmarkQueries, parseBenchmarkFromText, loadBenchmarks };
