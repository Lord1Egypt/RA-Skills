#!/usr/bin/env node

/**
 * Google Trends CLI - Self-contained script for fetching Google Trends data.
 * No external dependencies required (uses Node.js built-in modules only).
 *
 * Based on https://github.com/Shaivpidadi/trends-js
 */

import https from 'https';
import querystring from 'querystring';

// --- HTTP request layer ---

const MAX_RETRIES = 3;
const BASE_DELAY_MS = 750;
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let cookieVal;

async function runRequest(options, body, attempt) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let chunk = '';
      res.on('data', (data) => { chunk += data; });
      res.on('end', async () => {
        const hasSetCookie = !!res.headers['set-cookie']?.length;
        if (hasSetCookie) {
          cookieVal = res.headers['set-cookie'][0].split(';')[0];
          if (options.headers) options.headers['cookie'] = cookieVal;
        }

        const isRateLimited = res.statusCode === 429 || chunk.includes('Error 429') || chunk.includes('Too Many Requests');
        const isUnauthorized = res.statusCode === 401;
        const isRedirect = res.statusCode === 302;

        if (isRedirect) {
          cookieVal = undefined;
          if (options.headers) delete options.headers['cookie'];
          if (attempt < MAX_RETRIES) {
            resolve(await runRequest(options, body, attempt + 1));
            return;
          }
        }

        if ((isRateLimited || isUnauthorized) && attempt < MAX_RETRIES) {
          const delay = BASE_DELAY_MS * Math.pow(2, attempt) + Math.floor(Math.random() * 250);
          await sleep(delay);
          try {
            resolve(await runRequest(options, body, attempt + 1));
          } catch (err) {
            reject(err);
          }
          return;
        }

        resolve(chunk);
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function request(url, options, enableBackoff = false) {
  const parsedUrl = new URL(url);
  const method = options.method || 'POST';

  let bodyString = '';
  const contentType = options.contentType || 'json';

  if (typeof options.body === 'string') {
    bodyString = options.body;
  } else if (contentType === 'form') {
    bodyString = querystring.stringify(options.body || {});
  } else if (options.body) {
    bodyString = JSON.stringify(options.body);
  }

  const requestOptions = {
    hostname: parsedUrl.hostname,
    port: parsedUrl.port || 443,
    path: `${parsedUrl.pathname}${options.qs ? '?' + querystring.stringify(options.qs) : ''}`,
    method,
    headers: {
      ...(options.headers || {}),
      ...(contentType === 'form'
        ? { 'Content-Type': 'application/x-www-form-urlencoded' }
        : { 'Content-Type': 'application/json' }),
      ...(bodyString ? { 'Content-Length': Buffer.byteLength(bodyString).toString() } : {}),
      ...(cookieVal ? { cookie: cookieVal } : {}),
    },
  };

  const response = enableBackoff
    ? await runRequest(requestOptions, bodyString, 0)
    : await runRequest(requestOptions, bodyString, MAX_RETRIES);

  return { text: () => Promise.resolve(response) };
}

// --- Constants ---

const BASE_URL = 'trends.google.com';

const ENDPOINTS = {
  dailyTrends: {
    path: '/_/TrendsUi/data/batchexecute',
    method: 'POST',
    url: `https://${BASE_URL}/_/TrendsUi/data/batchexecute`,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
  },
  autocomplete: {
    path: '/trends/api/autocomplete',
    method: 'GET',
    url: `https://${BASE_URL}/trends/api/autocomplete`,
    headers: { accept: 'application/json, text/plain, */*' },
  },
  explore: {
    path: '/trends/api/explore',
    method: 'POST',
    url: `https://${BASE_URL}/trends/api/explore`,
    headers: {},
  },
  interestByRegion: {
    path: '/trends/api/widgetdata/comparedgeo',
    method: 'GET',
    url: `https://${BASE_URL}/trends/api/widgetdata/comparedgeo`,
    headers: {},
  },
  relatedSearches: {
    path: '/trends/api/widgetdata/relatedsearches',
    method: 'GET',
    url: `https://${BASE_URL}/trends/api/widgetdata/relatedsearches`,
    headers: {},
  },
};

// --- Format helpers ---

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function extractJsonFromResponse(text) {
  const cleanedText = text.replace(/^\)\]\}'/, '').trim();
  const parsedResponse = JSON.parse(cleanedText);

  if (!Array.isArray(parsedResponse) || parsedResponse.length === 0) {
    throw new Error('Invalid response format: empty array');
  }

  const nestedJsonString = parsedResponse[0][2];
  if (!nestedJsonString) throw new Error('Invalid response format: missing nested JSON');

  const data = JSON.parse(nestedJsonString);
  if (!data || !Array.isArray(data) || data.length < 2) {
    throw new Error('Invalid response format: missing data array');
  }

  return formatTrendingData(data[1]);
}

function formatTrendingData(data) {
  if (!Array.isArray(data)) throw new Error('Invalid data format: expected array');

  const allTrendingStories = [];
  const summary = [];

  for (const item of data) {
    if (!Array.isArray(item)) continue;

    const articles = extractArticles(item);
    const startTime = extractTimestamp(item, 3) ?? 0;
    const endTime = extractTimestamp(item, 4);
    const image = extractImage(item);

    const story = {
      title: String(item[0] || ''),
      traffic: String(item[6] || '0'),
      articles,
      shareUrl: String(item[12] || ''),
      startTime,
      ...(endTime && { endTime }),
      ...(image && { image }),
    };

    allTrendingStories.push(story);
    summary.push({
      title: story.title,
      traffic: story.traffic,
      articles: story.articles,
      startTime,
      ...(endTime && { endTime }),
    });
  }

  return { allTrendingStories, summary };
}

function extractArticles(item) {
  const imageData = item[1];
  if (!imageData || !Array.isArray(imageData) || imageData.length <= 3) return [];
  const articlesArray = imageData[3];
  if (!Array.isArray(articlesArray)) return [];
  return articlesArray
    .filter((a) => Array.isArray(a) && a.length >= 5)
    .map((a) => ({
      title: String(a[0] || ''),
      url: String(a[1] || ''),
      source: String(a[2] || ''),
      time: String(a[3] || ''),
      snippet: String(a[4] || ''),
    }));
}

function extractTimestamp(item, index) {
  const timeArray = item[index];
  if (!Array.isArray(timeArray) || timeArray.length === 0) return undefined;
  const ts = timeArray[0];
  return typeof ts === 'number' ? ts : undefined;
}

function extractImage(item) {
  const imageData = item[1];
  if (!imageData || !Array.isArray(imageData) || imageData.length < 3) return undefined;
  return {
    newsUrl: String(imageData[0] || ''),
    source: String(imageData[1] || ''),
    imageUrl: String(imageData[2] || ''),
  };
}

// --- API functions ---

async function autocomplete(keyword, hl = 'en-US') {
  if (!keyword) return { data: [] };
  const options = {
    ...ENDPOINTS.autocomplete,
    qs: { hl, tz: '240' },
  };
  const response = await request(`${options.url}/${encodeURIComponent(keyword)}`, options);
  const text = await response.text();
  const data = JSON.parse(text.slice(5));
  return { data: data.default.topics.map((t) => t.title) };
}

async function dailyTrends({ geo = 'US', lang = 'en' } = {}) {
  const options = {
    ...ENDPOINTS.dailyTrends,
    body: new URLSearchParams({
      'f.req': `[[["i0OFE","[null,null,\\"${geo}\\",0,\\"${lang}\\",24,1]",null,"generic"]]]`,
    }).toString(),
    contentType: 'form',
  };
  const response = await request(options.url, options);
  const text = await response.text();
  const trendingTopics = extractJsonFromResponse(text);
  if (!trendingTopics) throw new Error('Failed to parse trending topics');
  return { data: trendingTopics };
}

async function realTimeTrends({ geo = 'US', trendingHours = 4 } = {}) {
  const options = {
    ...ENDPOINTS.dailyTrends,
    body: new URLSearchParams({
      'f.req': `[[["i0OFE","[null,null,\\"${geo}\\",0,\\"en\\",${trendingHours},1]",null,"generic"]]]`,
    }).toString(),
    contentType: 'form',
  };
  const response = await request(options.url, options);
  const text = await response.text();
  const trendingTopics = extractJsonFromResponse(text);
  if (!trendingTopics) throw new Error('Failed to parse trending topics');
  return { data: trendingTopics };
}

async function explore({ keyword, geo = 'US', time = 'now 1-d', category = 0, property = '', hl = 'en-US', enableBackoff = false } = {}) {
  const options = {
    ...ENDPOINTS.explore,
    qs: {
      hl,
      tz: '240',
      req: JSON.stringify({
        comparisonItem: [{ keyword, geo, time }],
        category,
        property,
      }),
    },
  };
  const response = await request(options.url, options, enableBackoff);
  const text = await response.text();
  if (text.includes('<html') || text.includes('<!DOCTYPE')) {
    throw new Error('Explore request returned HTML instead of JSON');
  }
  const data = JSON.parse(text.slice(5));
  if (data && Array.isArray(data) && data.length > 0) {
    return { widgets: data[0] || [] };
  }
  if (data && typeof data === 'object' && Array.isArray(data.widgets)) {
    return { widgets: data.widgets };
  }
  return { widgets: [] };
}

async function interestByRegion({
  keyword, geo = 'US', resolution = 'REGION', hl = 'en-US',
  startTime = new Date('2004-01-01'), endTime = new Date(),
  timezone = new Date().getTimezoneOffset(), category = 0, enableBackoff = false,
} = {}) {
  if (!keyword) throw new Error('Keyword is required');

  const exploreResponse = await explore({
    keyword, geo,
    time: `${formatDate(startTime)} ${formatDate(endTime)}`,
    category, hl, enableBackoff,
  });

  const widget = exploreResponse.widgets.find((w) => w.id === 'GEO_MAP');
  if (!widget) throw new Error('No GEO_MAP widget found in explore response');

  const options = {
    ...ENDPOINTS.interestByRegion,
    qs: {
      hl,
      tz: timezone.toString(),
      req: JSON.stringify({ ...widget.request, resolution }),
      token: widget.token,
    },
  };

  const response = await request(options.url, options, enableBackoff);
  const text = await response.text();
  if (text.includes('<!DOCTYPE') || text.includes('<html')) {
    throw new Error('Interest by region request returned HTML');
  }
  const data = JSON.parse(text.slice(5));
  return { data: data.default.geoMapData };
}

async function relatedTopics({
  keyword, geo = 'US', startTime = new Date('2004-01-01'), endTime = new Date(),
  category = 0, hl = 'en-US', enableBackoff = false,
} = {}) {
  if (!keyword) throw new Error('Keyword is required');

  const timeValue = `${formatDate(startTime)} ${formatDate(endTime)}`;
  const exploreResponse = await explore({ keyword, geo, time: timeValue, category, hl, enableBackoff });

  if (!exploreResponse.widgets || exploreResponse.widgets.length === 0) {
    throw new Error('No widgets found in explore response');
  }

  const widget = exploreResponse.widgets.find((w) => w.id === 'RELATED_TOPICS') || exploreResponse.widgets[0];
  if (!widget) throw new Error('No related topics widget found');

  const options = {
    ...ENDPOINTS.relatedSearches,
    qs: {
      hl, tz: '240',
      req: JSON.stringify(widget.request),
      ...(widget.token && { token: widget.token }),
    },
  };

  const response = await request(options.url, options, enableBackoff);
  const text = await response.text();
  const data = JSON.parse(text.slice(5));
  return { data: data.default?.rankedList || [] };
}

async function relatedQueries({
  keyword, geo = 'US', startTime = new Date('2004-01-01'), endTime = new Date(),
  category = 0, hl = 'en-US', enableBackoff = false,
} = {}) {
  if (!keyword) throw new Error('Keyword is required');

  const timeValue = `${formatDate(startTime)} ${formatDate(endTime)}`;
  const exploreResponse = await explore({ keyword, geo, time: timeValue, category, hl, enableBackoff });

  if (!exploreResponse.widgets || exploreResponse.widgets.length === 0) {
    throw new Error('No widgets found in explore response');
  }

  const widget = exploreResponse.widgets.find((w) => w.id === 'RELATED_QUERIES');
  if (!widget) throw new Error('No related queries widget found');

  const options = {
    ...ENDPOINTS.relatedSearches,
    qs: {
      hl, tz: '240',
      req: JSON.stringify(widget.request),
      token: widget.token,
    },
  };

  const response = await request(options.url, options, enableBackoff);
  const text = await response.text();
  const data = JSON.parse(text.slice(5));
  return { data: data.default?.rankedList || [] };
}

// --- CLI ---

function parseArgs(args) {
  const parsed = { _positional: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        parsed[key] = next;
        i++;
      } else {
        parsed[key] = true;
      }
    } else {
      parsed._positional.push(args[i]);
    }
  }
  return parsed;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: trends.mjs <command> [options]\n\nCommands: daily-trends, realtime-trends, autocomplete, explore, interest-by-region, related-topics, related-queries');
    process.exit(1);
  }

  const command = args[0];
  const parsed = parseArgs(args.slice(1));
  const keyword = parsed._positional[0];

  try {
    let result;
    switch (command) {
      case 'daily-trends':
        result = await dailyTrends({ geo: parsed.geo || 'US', lang: parsed.lang || 'en' });
        break;

      case 'realtime-trends':
        result = await realTimeTrends({ geo: parsed.geo || 'US', trendingHours: parseInt(parsed.hours || '4', 10) });
        break;

      case 'autocomplete':
        if (!keyword) { console.error('Error: keyword required'); process.exit(1); }
        result = await autocomplete(keyword, parsed.hl || 'en-US');
        break;

      case 'explore':
        if (!keyword) { console.error('Error: keyword required'); process.exit(1); }
        result = await explore({
          keyword, geo: parsed.geo || 'US', time: parsed.time || 'now 1-d',
          category: parseInt(parsed.category || '0', 10), property: parsed.property || '', hl: parsed.hl || 'en-US',
          enableBackoff: !!parsed['enable-backoff'],
        });
        break;

      case 'interest-by-region':
        if (!keyword) { console.error('Error: keyword required'); process.exit(1); }
        result = await interestByRegion({
          keyword, geo: parsed.geo || 'US', resolution: parsed.resolution || 'REGION', hl: parsed.hl || 'en-US',
          startTime: parsed['start-time'] ? new Date(parsed['start-time']) : new Date('2004-01-01'),
          endTime: parsed['end-time'] ? new Date(parsed['end-time']) : new Date(),
          category: parseInt(parsed.category || '0', 10), enableBackoff: !!parsed['enable-backoff'],
        });
        break;

      case 'related-topics':
        if (!keyword) { console.error('Error: keyword required'); process.exit(1); }
        result = await relatedTopics({
          keyword, geo: parsed.geo || 'US', hl: parsed.hl || 'en-US',
          startTime: parsed['start-time'] ? new Date(parsed['start-time']) : new Date('2004-01-01'),
          endTime: parsed['end-time'] ? new Date(parsed['end-time']) : new Date(),
          category: parseInt(parsed.category || '0', 10), enableBackoff: !!parsed['enable-backoff'],
        });
        break;

      case 'related-queries':
        if (!keyword) { console.error('Error: keyword required'); process.exit(1); }
        result = await relatedQueries({
          keyword, geo: parsed.geo || 'US', hl: parsed.hl || 'en-US',
          startTime: parsed['start-time'] ? new Date(parsed['start-time']) : new Date('2004-01-01'),
          endTime: parsed['end-time'] ? new Date(parsed['end-time']) : new Date(),
          category: parseInt(parsed.category || '0', 10), enableBackoff: !!parsed['enable-backoff'],
        });
        break;

      default:
        console.error(`Unknown command: ${command}\n\nCommands: daily-trends, realtime-trends, autocomplete, explore, interest-by-region, related-topics, related-queries`);
        process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(JSON.stringify({ error: err.message }));
    process.exit(1);
  }
}

main();
