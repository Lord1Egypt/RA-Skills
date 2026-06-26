#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function usage() {
  console.error(`Usage:
  marktplaats-live-verify --ad-json ./ad.json [--url URL | --html page.html | --text live.txt] [options]

Options:
  --description PATH        Override local description file
  --url URL                 Fetch live page and verify fetched HTML/text
  --html PATH               Verify saved HTML
  --text PATH               Verify saved visible/live text
  --start-chars N           Characters from local description used as start marker, default 90
  --max-start-count N       Maximum accepted start marker occurrences, default 1
  --update-ad-json          Write live verification evidence to ad.json
  --json                    Emit JSON only
  --self-test               Run deterministic smoke test
  -h, --help                Show this help
`);
}

function parseArgs(argv) {
  const out = {
    adJson: null,
    description: null,
    url: null,
    html: null,
    text: null,
    startChars: 90,
    maxStartCount: 1,
    updateAdJson: false,
    json: false,
    selfTest: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`Missing value for ${arg}`);
      i += 1;
      return argv[i];
    };

    if (arg === '-h' || arg === '--help') {
      usage();
      process.exit(0);
    } else if (arg === '--ad-json') out.adJson = next();
    else if (arg === '--description') out.description = next();
    else if (arg === '--url') out.url = next();
    else if (arg === '--html') out.html = next();
    else if (arg === '--text') out.text = next();
    else if (arg === '--start-chars') out.startChars = Number(next());
    else if (arg === '--max-start-count') out.maxStartCount = Number(next());
    else if (arg === '--update-ad-json') out.updateAdJson = true;
    else if (arg === '--json') out.json = true;
    else if (arg === '--self-test') out.selfTest = true;
    else throw new Error(`Unknown option: ${arg}`);
  }

  if (!out.selfTest && !out.adJson) {
    usage();
    process.exit(2);
  }
  return out;
}

function decodeHtmlEntities(value) {
  return value
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/gi, "'")
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCodePoint(parseInt(code, 16)));
}

function htmlToText(html) {
  return decodeHtmlEntities(html)
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ');
}

function normalizeText(value) {
  return decodeHtmlEntities(String(value || ''))
    .replace(/\r\n/g, '\n')
    .replace(/\s+/g, ' ')
    .trim()
    .toLocaleLowerCase('nl-NL');
}

function countOccurrences(haystack, needle) {
  if (!needle) return 0;
  let count = 0;
  let offset = 0;
  while (true) {
    const index = haystack.indexOf(needle, offset);
    if (index === -1) return count;
    count += 1;
    offset = index + needle.length;
  }
}

function getLastSentence(text) {
  return text.trim().replace(/\r\n/g, '\n').match(/[^.!?\n][^.!?]*(?:[.!?])?\s*$/)?.[0]?.trim() || '';
}

function hasKeywordDump(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (/^\s*(zoektermen|keywords?|seo)\s*:/gim.test(normalized)) return true;
  return normalized.split('\n').some((line) => {
    const trimmed = line.trim();
    return trimmed.length >= 120 && (trimmed.match(/,/g) || []).length >= 8;
  });
}

function resolveMaybeRelative(baseDir, value) {
  if (!value) return null;
  return path.isAbsolute(value) ? value : path.resolve(baseDir, value);
}

function readAdAndDescription(adJsonPath, descriptionOverride) {
  const ad = JSON.parse(fs.readFileSync(adJsonPath, 'utf8'));
  const baseDir = path.dirname(adJsonPath);
  const descriptionPath = resolveMaybeRelative(baseDir, descriptionOverride || ad.descriptionFile || 'description.md');
  if (!descriptionPath || !fs.existsSync(descriptionPath)) {
    throw new Error(`Description file not found: ${descriptionPath || '(missing)'}`);
  }
  const description = fs.readFileSync(descriptionPath, 'utf8').replace(/\r\n/g, '\n');
  return { ad, descriptionPath, description };
}

async function loadLiveText(options, ad) {
  if (options.text) {
    return {
      source: 'text-file',
      url: null,
      text: fs.readFileSync(path.resolve(options.text), 'utf8'),
    };
  }
  if (options.html) {
    const html = fs.readFileSync(path.resolve(options.html), 'utf8');
    return {
      source: 'html-file',
      url: null,
      text: htmlToText(html),
    };
  }
  const url = options.url || ad.url;
  if (!url) throw new Error('No live source. Provide --url, --html, --text, or ad.url.');
  const response = await fetch(url, {
    redirect: 'follow',
    headers: {
      Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    },
  });
  const html = await response.text();
  return {
    source: 'url-fetch',
    url: response.url,
    status: response.status,
    ok: response.ok,
    text: htmlToText(html),
  };
}

function evaluate({ ad, description, live, options }) {
  const failures = [];
  const warnings = [];
  const local = normalizeText(description);
  const liveText = normalizeText(live.text);
  const startMarker = normalizeText(description.slice(0, options.startChars));
  const lastSentence = ad.copyQuality?.lastSentence || getLastSentence(description);
  const lastMarker = normalizeText(lastSentence);
  const titleMarker = normalizeText(ad.title || '');
  const startCount = countOccurrences(liveText, startMarker);

  if (live.status && live.status >= 400) failures.push(`live fetch returned HTTP ${live.status}`);
  if (/\/identity\/v2\/login\b/.test(String(live.url || '')) || /inloggen op uw account/i.test(live.text)) {
    failures.push('live source is a login page; use an authenticated browser text snapshot');
  }
  if (!startMarker || startCount === 0) failures.push('live text does not contain description start marker');
  if (startCount > options.maxStartCount) failures.push(`description start marker appears too often: ${startCount} > ${options.maxStartCount}`);
  if (!lastMarker || !liveText.includes(lastMarker)) failures.push('live text does not contain expected last sentence');
  if (titleMarker && !liveText.includes(titleMarker)) warnings.push('live text does not contain ad title');
  if (hasKeywordDump(description)) failures.push('local description contains keyword dump');
  if (/zoektermen\s*:/i.test(live.text)) failures.push('live text contains Zoektermen: keyword footer');
  if (local.length < 1000) warnings.push('local description is unexpectedly short for live verification');

  return {
    checkedAt: new Date().toISOString(),
    passed: failures.length === 0,
    source: live.source,
    url: live.url || ad.url || null,
    status: live.status ?? null,
    startChars: options.startChars,
    startCount,
    maxStartCount: options.maxStartCount,
    hasLastSentence: Boolean(lastMarker && liveText.includes(lastMarker)),
    lastSentence,
    liveTextChars: live.text.length,
    failures,
    warnings,
  };
}

function updateAdJson(adJsonPath, result) {
  const ad = JSON.parse(fs.readFileSync(adJsonPath, 'utf8'));
  ad.lastCheckedAt = result.checkedAt;
  if (result.passed && result.url) ad.url = result.url;
  ad.copyQuality = ad.copyQuality || {};
  ad.copyQuality.lastSentenceVerified = result.passed;
  ad.copyQuality.liveVerifiedAt = result.checkedAt;
  ad.copyQuality.liveVerification = {
    source: result.source,
    url: result.url,
    startCount: result.startCount,
    hasLastSentence: result.hasLastSentence,
    failures: result.failures,
    warnings: result.warnings,
  };
  fs.writeFileSync(adJsonPath, `${JSON.stringify(ad, null, 2)}\n`, 'utf8');
}

function printResult(result, json) {
  if (json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }
  console.log(`Live verify: ${result.passed ? 'PASS' : 'FAIL'}`);
  console.log(`source=${result.source} startCount=${result.startCount} hasLastSentence=${result.hasLastSentence}`);
  if (result.warnings.length) console.log(`warnings:\n- ${result.warnings.join('\n- ')}`);
  if (result.failures.length) console.log(`failures:\n- ${result.failures.join('\n- ')}`);
}

async function runSelfTest() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'marktplaats-live-verify-'));
  const description = [
    'Te koop: Testmerk Model X buitenantenne voor router of modem.',
    'Deze tekst is lang genoeg om een echte advertentie te simuleren en blijft in gewone taal.',
    'Stuur gerust een bericht als je wilt controleren of dit item past voordat je biedt.',
  ].join('\n\n');
  const adJson = path.join(dir, 'ad.json');
  const descriptionFile = path.join(dir, 'description.md');
  fs.writeFileSync(descriptionFile, description);
  fs.writeFileSync(adJson, `${JSON.stringify({
    title: 'Testmerk Model X buitenantenne',
    url: 'https://example.invalid/ad',
    descriptionFile,
    copyQuality: {
      lastSentence: getLastSentence(description),
    },
  }, null, 2)}\n`);
  const liveText = `Marktplaats Testmerk Model X buitenantenne ${description}`;
  const liveFile = path.join(dir, 'live.txt');
  fs.writeFileSync(liveFile, liveText);
  const { ad } = readAdAndDescription(adJson, null);
  const live = await loadLiveText({ text: liveFile }, ad);
  const ok = evaluate({ ad, description, live, options: { startChars: 40, maxStartCount: 1 } });
  if (!ok.passed) throw new Error(`self-test expected PASS: ${ok.failures.join('; ')}`);
  fs.writeFileSync(liveFile, `${liveText}\n${description}`);
  const dupLive = await loadLiveText({ text: liveFile }, ad);
  const bad = evaluate({ ad, description, live: dupLive, options: { startChars: 40, maxStartCount: 1 } });
  if (bad.passed) throw new Error('self-test expected duplicate FAIL');
  console.log('marktplaats-live-verify self-test: PASS');
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.selfTest) {
    await runSelfTest();
    return;
  }
  const adJsonPath = path.resolve(options.adJson);
  const { ad, description } = readAdAndDescription(adJsonPath, options.description);
  const live = await loadLiveText(options, ad);
  const result = evaluate({ ad, description, live, options });
  if (options.updateAdJson) updateAdJson(adJsonPath, result);
  printResult(result, options.json);
  if (!result.passed) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error?.stack || error?.message || String(error));
  process.exitCode = 1;
});
