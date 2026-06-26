#!/usr/bin/env node
import { createSign } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import process from 'node:process';
import { buildSeoSummary, writeJsonOutput } from './openclaw-exporters-lib.mjs';
import { loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
Export SEO Summary

Builds an OpenClaw-compatible SEO summary JSON from Google Search Console, keyword CSVs, and optional DataForSEO.

Usage:
  node scripts/export-seo-summary.mjs [options]

Options:
  --site <url>              Optional GSC site URL/property (default: GSC_SITE_URL; omitted = all verified sites)
  --from <date>             Start date YYYY-MM-DD (default: 90 days before --to)
  --to <date>               End date YYYY-MM-DD (default: yesterday UTC)
  --last <duration>         Relative GSC window like 90d (used when --from is omitted)
  --dimensions <a,b>        GSC dimensions (default: query,page)
  --row-limit <n>           GSC row limit (default: 250)
  --max-sites <n>           Max GSC sites to query when --site is omitted (default: 20)
  --country <code>          Optional GSC country dimension filter
  --device <device>         Optional GSC device dimension filter
  --include-sitemaps        Fetch Search Console sitemap status (default)
  --no-sitemaps             Skip Search Console sitemap status
  --inspect-url <url>       Run URL Inspection for a URL under an accessible property (repeatable)
  --gsc-csv <file>          Import Google Search Console CSV (repeatable)
  --csv <file>              Import keyword metrics CSV from Ahrefs/Semrush/DataForSEO/etc. (repeatable)
  --seed <keyword>          Seed keyword for optional DataForSEO (repeatable)
  --dataforseo              Fetch live DataForSEO keyword data
  --confirm-paid            Required for live DataForSEO calls
  --max-paid-requests <n>   DataForSEO request cap (default: 1)
  --location-code <n>       DataForSEO location code (default: 2840)
  --language-code <code>    DataForSEO language code (default: en)
  --out <file>              Write JSON to file instead of stdout
  --max-signals <n>         Maximum signals to emit (default: 8)
  --help, -h                Show help

Environment:
  GSC_SITE_URL
  GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN or GSC_ACCESS_TOKEN
  GOOGLE_APPLICATION_CREDENTIALS or GSC_SERVICE_ACCOUNT_JSON
  DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD
`);
    process.exit(exitCode);
}
function formatDate(date) {
    return date.toISOString().slice(0, 10);
}
function addDays(date, days) {
    const copy = new Date(date);
    copy.setUTCDate(copy.getUTCDate() + days);
    return copy;
}
function parseDurationDays(value, fallback) {
    const match = String(value || '').trim().match(/^(\d+)\s*d$/i);
    if (!match)
        return fallback;
    const parsed = Number.parseInt(match[1], 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}
function parseArgs(argv) {
    const defaultTo = formatDate(addDays(new Date(), -1));
    const args = {
        site: String(process.env.GSC_SITE_URL || '').trim(),
        from: '',
        to: defaultTo,
        last: '90d',
        dimensions: ['query', 'page'],
        rowLimit: 250,
        maxSites: 20,
        country: '',
        device: '',
        includeSitemaps: true,
        inspectUrls: [],
        gscCsvFiles: [],
        csvFiles: [],
        seeds: [],
        dataforseo: false,
        confirmPaid: false,
        maxPaidRequests: 1,
        locationCode: 2840,
        languageCode: 'en',
        out: '',
        maxSignals: 8,
    };
    for (let index = 0; index < argv.length; index += 1) {
        const token = argv[index];
        const next = argv[index + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--site') {
            args.site = String(next || '').trim();
            index += 1;
        }
        else if (token === '--from') {
            args.from = String(next || '').trim();
            index += 1;
        }
        else if (token === '--to') {
            args.to = String(next || '').trim();
            index += 1;
        }
        else if (token === '--last') {
            args.last = String(next || '').trim() || args.last;
            index += 1;
        }
        else if (token === '--dimensions') {
            args.dimensions = String(next || '')
                .split(',')
                .map((value) => value.trim())
                .filter(Boolean);
            index += 1;
        }
        else if (token === '--row-limit') {
            args.rowLimit = positiveInt(next, '--row-limit');
            index += 1;
        }
        else if (token === '--max-sites') {
            args.maxSites = positiveInt(next, '--max-sites');
            index += 1;
        }
        else if (token === '--country') {
            args.country = String(next || '').trim();
            index += 1;
        }
        else if (token === '--device') {
            args.device = String(next || '').trim();
            index += 1;
        }
        else if (token === '--include-sitemaps') {
            args.includeSitemaps = true;
        }
        else if (token === '--no-sitemaps') {
            args.includeSitemaps = false;
        }
        else if (token === '--inspect-url') {
            args.inspectUrls.push(String(next || '').trim());
            index += 1;
        }
        else if (token === '--gsc-csv') {
            args.gscCsvFiles.push(String(next || '').trim());
            index += 1;
        }
        else if (token === '--csv') {
            args.csvFiles.push(String(next || '').trim());
            index += 1;
        }
        else if (token === '--seed') {
            args.seeds.push(String(next || '').trim());
            index += 1;
        }
        else if (token === '--dataforseo') {
            args.dataforseo = true;
        }
        else if (token === '--confirm-paid') {
            args.confirmPaid = true;
        }
        else if (token === '--max-paid-requests') {
            args.maxPaidRequests = positiveInt(next, '--max-paid-requests');
            index += 1;
        }
        else if (token === '--location-code') {
            args.locationCode = positiveInt(next, '--location-code');
            index += 1;
        }
        else if (token === '--language-code') {
            args.languageCode = String(next || 'en').trim() || 'en';
            index += 1;
        }
        else if (token === '--out') {
            args.out = String(next || '').trim();
            index += 1;
        }
        else if (token === '--max-signals') {
            args.maxSignals = positiveInt(next, '--max-signals');
            index += 1;
        }
        else if (token === '--help' || token === '-h') {
            printHelpAndExit(0);
        }
        else {
            printHelpAndExit(1, `Unknown argument: ${token}`);
        }
    }
    if (!args.from) {
        args.from = formatDate(addDays(new Date(`${args.to}T00:00:00Z`), -parseDurationDays(args.last, 90)));
    }
    return args;
}
function positiveInt(value, label) {
    const parsed = Number.parseInt(String(value || ''), 10);
    if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for ${label}: ${String(value || '')}`);
    }
    return parsed;
}
function parseCsv(raw) {
    const rows = [];
    let current = [];
    let field = '';
    let quoted = false;
    for (let index = 0; index < raw.length; index += 1) {
        const char = raw[index];
        if (char === '"') {
            if (quoted && raw[index + 1] === '"') {
                field += '"';
                index += 1;
            }
            else {
                quoted = !quoted;
            }
        }
        else if (char === ',' && !quoted) {
            current.push(field);
            field = '';
        }
        else if (char === '\n' && !quoted) {
            current.push(field);
            rows.push(current);
            current = [];
            field = '';
        }
        else if (char !== '\r') {
            field += char;
        }
    }
    if (field || current.length) {
        current.push(field);
        rows.push(current);
    }
    return rows;
}
function normalizeHeader(value) {
    return String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
}
function parseNumber(value) {
    if (value === undefined || value === null || value === '')
        return undefined;
    const parsed = Number(String(value).trim().replace(/[$,%]/g, '').replace(/,/g, ''));
    return Number.isFinite(parsed) ? parsed : undefined;
}
async function readKeywordCsv(filePath, source) {
    const raw = await readFile(filePath, 'utf8');
    const rows = parseCsv(raw).filter((row) => row.some((cell) => String(cell).trim()));
    if (rows.length < 2)
        return [];
    const headers = rows[0].map(normalizeHeader);
    const indexOf = (...names) => names.map((name) => headers.indexOf(name)).find((index) => index >= 0) ?? -1;
    const keywordIndex = indexOf('keyword', 'query', 'search_query', 'term');
    if (keywordIndex < 0) {
        throw new Error(`No keyword/query column found in ${filePath}`);
    }
    const pageIndex = indexOf('page', 'url', 'landing_page');
    const clicksIndex = indexOf('clicks');
    const impressionsIndex = indexOf('impressions');
    const ctrIndex = indexOf('ctr');
    const positionIndex = indexOf('position', 'average_position', 'avg_position');
    const volumeIndex = indexOf('volume', 'search_volume', 'avg_monthly_searches', 'monthly_volume');
    const difficultyIndex = indexOf('kd', 'difficulty', 'keyword_difficulty', 'competition_index');
    const cpcIndex = indexOf('cpc', 'cost_per_click');
    return rows.slice(1).map((row) => ({
        query: String(row[keywordIndex] || '').trim().toLowerCase(),
        page: pageIndex >= 0 ? String(row[pageIndex] || '').trim() : '',
        clicks: clicksIndex >= 0 ? parseNumber(row[clicksIndex]) : undefined,
        impressions: impressionsIndex >= 0 ? parseNumber(row[impressionsIndex]) : undefined,
        ctr: ctrIndex >= 0 ? parseNumber(row[ctrIndex]) : undefined,
        position: positionIndex >= 0 ? parseNumber(row[positionIndex]) : undefined,
        volume: volumeIndex >= 0 ? parseNumber(row[volumeIndex]) : undefined,
        difficulty: difficultyIndex >= 0 ? parseNumber(row[difficultyIndex]) : undefined,
        cpc: cpcIndex >= 0 ? parseNumber(row[cpcIndex]) : undefined,
        source,
    })).filter((row) => row.query);
}
function base64url(value) {
    return Buffer.from(value).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}
async function readServiceAccount() {
    const raw = process.env.GSC_SERVICE_ACCOUNT_JSON || process.env.GOOGLE_SERVICE_ACCOUNT_JSON;
    if (raw?.trim())
        return JSON.parse(raw);
    const filePath = process.env.GOOGLE_APPLICATION_CREDENTIALS || process.env.GSC_SERVICE_ACCOUNT_FILE;
    if (!filePath)
        return null;
    return JSON.parse(await readFile(filePath, 'utf8'));
}
async function getGscAccessToken() {
    const direct = String(process.env.GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN || process.env.GSC_ACCESS_TOKEN || '').trim();
    if (direct)
        return direct;
    const account = await readServiceAccount();
    if (!account)
        return '';
    const now = Math.floor(Date.now() / 1000);
    const header = { alg: 'RS256', typ: 'JWT' };
    const claim = {
        iss: account.client_email,
        scope: 'https://www.googleapis.com/auth/webmasters.readonly',
        aud: account.token_uri || 'https://oauth2.googleapis.com/token',
        exp: now + 3600,
        iat: now,
    };
    const unsigned = `${base64url(JSON.stringify(header))}.${base64url(JSON.stringify(claim))}`;
    const signer = createSign('RSA-SHA256');
    signer.update(unsigned);
    signer.end();
    const assertion = `${unsigned}.${signer.sign(account.private_key, 'base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_')}`;
    const response = await fetch(account.token_uri || 'https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            assertion,
        }),
    });
    const body = await response.json().catch(() => null);
    if (!response.ok) {
        throw new Error(`GSC service account token exchange failed (${response.status}): ${JSON.stringify(body)}`);
    }
    return String(body?.access_token || '').trim();
}
function buildDimensionFilterGroups(args) {
    const filters = [];
    if (args.country) {
        filters.push({ dimension: 'country', operator: 'equals', expression: args.country.toLowerCase() });
    }
    if (args.device) {
        filters.push({ dimension: 'device', operator: 'equals', expression: args.device.toUpperCase() });
    }
    return filters.length > 0 ? [{ filters }] : undefined;
}
async function gscFetchJson(url, token, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${token}`,
            ...(options.headers || {}),
        },
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${JSON.stringify(payload)}`);
    }
    return payload || {};
}
async function listGscSites(token, args, warnings) {
    if (args.site)
        return [args.site];
    const payload = await gscFetchJson('https://www.googleapis.com/webmasters/v3/sites', token);
    const sites = (Array.isArray(payload?.siteEntry) ? payload.siteEntry : [])
        .filter((entry) => {
        const siteUrl = String(entry?.siteUrl || '').trim();
        const permissionLevel = String(entry?.permissionLevel || '').trim();
        return siteUrl && permissionLevel !== 'siteUnverifiedUser';
    })
        .map((entry) => String(entry.siteUrl).trim())
        .slice(0, Math.max(1, Number(args.maxSites) || 20));
    if (sites.length === 0) {
        warnings.push('GSC account returned no verified sites; skipped Search Analytics API fetch.');
    }
    if (Array.isArray(payload?.siteEntry) && payload.siteEntry.length > sites.length) {
        warnings.push(`GSC site list was capped at ${sites.length} verified sites. Use --site for a specific property or raise --max-sites intentionally.`);
    }
    return sites;
}
async function fetchGscRows(args, warnings) {
    const token = await getGscAccessToken();
    if (!token) {
        warnings.push('GSC access token/service account missing; skipped Google Search Console API fetch.');
        return [];
    }
    const sites = await listGscSites(token, args, warnings);
    const rows = [];
    const body = {
        startDate: args.from,
        endDate: args.to,
        dimensions: args.dimensions,
        rowLimit: args.rowLimit,
        dimensionFilterGroups: buildDimensionFilterGroups(args),
    };
    for (const siteUrl of sites) {
        try {
            const payload = await gscFetchJson(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/searchAnalytics/query`, token, {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                },
                body: JSON.stringify(body),
            });
            rows.push(...(Array.isArray(payload?.rows) ? payload.rows : []).map((row) => ({
                ...row,
                siteUrl,
                source: args.site ? 'gsc-api' : `gsc-api:${siteUrl}`,
            })));
        }
        catch (error) {
            warnings.push(`GSC Search Analytics query failed for ${siteUrl}: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    return rows;
}
async function fetchGscContext(args, warnings) {
    const token = await getGscAccessToken();
    if (!token) {
        warnings.push('GSC access token/service account missing; skipped Search Console sitemap and URL Inspection API fetch.');
        return { sites: [], sitemaps: [], inspections: [] };
    }
    const sites = await listGscSites(token, args, warnings);
    const sitemaps = [];
    if (args.includeSitemaps) {
        for (const siteUrl of sites) {
            try {
                const payload = await gscFetchJson(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/sitemaps`, token);
                sitemaps.push({
                    siteUrl,
                    sitemaps: Array.isArray(payload?.sitemap) ? payload.sitemap : [],
                });
            }
            catch (error) {
                warnings.push(`GSC sitemap query failed for ${siteUrl}: ${error instanceof Error ? error.message : String(error)}`);
            }
        }
    }
    const inspections = [];
    for (const inspectionUrl of args.inspectUrls.filter(Boolean).slice(0, 25)) {
        const siteUrl = sites.find((candidate) => propertyOwnsUrl(candidate, inspectionUrl)) || args.site || sites[0] || '';
        if (!siteUrl) {
            warnings.push(`Skipped URL Inspection for ${inspectionUrl}: no accessible GSC property found.`);
            continue;
        }
        try {
            const payload = await gscFetchJson('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', token, {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify({
                    inspectionUrl,
                    siteUrl,
                }),
            });
            inspections.push({ siteUrl, inspectionUrl, result: payload?.inspectionResult || payload });
        }
        catch (error) {
            warnings.push(`GSC URL Inspection failed for ${inspectionUrl}: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    return { sites, sitemaps, inspections };
}
function propertyOwnsUrl(property, inspectedUrl) {
    const site = String(property || '').trim();
    const url = String(inspectedUrl || '').trim();
    if (!site || !url)
        return false;
    if (site.startsWith('sc-domain:')) {
        const domain = site.slice('sc-domain:'.length).toLowerCase();
        try {
            return new URL(url).hostname.toLowerCase().endsWith(domain);
        }
        catch {
            return false;
        }
    }
    return url.startsWith(site);
}
async function dataForSeoRequest(endpoint, tasks) {
    const login = process.env.DATAFORSEO_LOGIN;
    const password = process.env.DATAFORSEO_PASSWORD;
    if (!login || !password) {
        throw new Error('DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are required for --dataforseo.');
    }
    const response = await fetch(`https://api.dataforseo.com/v3/${endpoint}`, {
        method: 'POST',
        headers: {
            authorization: `Basic ${Buffer.from(`${login}:${password}`).toString('base64')}`,
            'content-type': 'application/json',
        },
        body: JSON.stringify(tasks),
    });
    const body = await response.json().catch(() => null);
    if (!response.ok) {
        throw new Error(`DataForSEO request failed (${response.status}): ${JSON.stringify(body)}`);
    }
    return body;
}
function normalizeDataForSeoItems(payload, source) {
    const rows = [];
    for (const task of payload?.tasks || []) {
        for (const item of task?.result || []) {
            const query = String(item?.keyword || '').trim().toLowerCase();
            if (!query)
                continue;
            rows.push({
                query,
                volume: parseNumber(item.search_volume),
                cpc: parseNumber(item.cpc),
                difficulty: parseNumber(item.competition_index ?? item.keyword_difficulty),
                source,
            });
        }
    }
    return rows;
}
async function fetchDataForSeoRows(args, warnings) {
    if (!args.dataforseo)
        return [];
    if (!args.confirmPaid) {
        warnings.push(`Skipped DataForSEO because --confirm-paid is missing (max-paid-requests would be ${args.maxPaidRequests}).`);
        return [];
    }
    const seeds = args.seeds.filter(Boolean).slice(0, Math.max(1, args.maxPaidRequests));
    if (seeds.length === 0) {
        warnings.push('Skipped DataForSEO because no --seed values were provided.');
        return [];
    }
    const tasks = seeds.map((seed) => ({
        keywords: [seed],
        location_code: args.locationCode,
        language_code: args.languageCode,
        sort_by: 'search_volume',
        include_adult_keywords: false,
    }));
    const payload = await dataForSeoRequest('keywords_data/google_ads/keywords_for_keywords/live', tasks);
    return normalizeDataForSeoItems(payload, 'dataforseo-ideas');
}
async function main() {
    await loadOpenClawGrowthSecrets();
    const args = parseArgs(process.argv.slice(2));
    const warnings = [];
    const rows = [];
    const keywordRows = [];
    try {
        rows.push(...(await fetchGscRows(args, warnings)));
    }
    catch (error) {
        warnings.push(error instanceof Error ? error.message : String(error));
    }
    const gscContext = await fetchGscContext(args, warnings).catch((error) => {
        warnings.push(error instanceof Error ? error.message : String(error));
        return { sites: [], sitemaps: [], inspections: [] };
    });
    for (const filePath of args.gscCsvFiles.filter(Boolean)) {
        try {
            rows.push(...(await readKeywordCsv(filePath, 'gsc-csv')));
        }
        catch (error) {
            warnings.push(`${filePath}: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    for (const filePath of args.csvFiles.filter(Boolean)) {
        try {
            keywordRows.push(...(await readKeywordCsv(filePath, 'keyword-csv')));
        }
        catch (error) {
            warnings.push(`${filePath}: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    try {
        keywordRows.push(...(await fetchDataForSeoRows(args, warnings)));
    }
    catch (error) {
        warnings.push(error instanceof Error ? error.message : String(error));
    }
    const summary = buildSeoSummary({
        siteUrl: args.site || 'all_verified_gsc_sites',
        window: `${args.from}_${args.to}`,
        rows,
        keywordRows,
        gscContext,
        paidProvider: args.dataforseo && args.confirmPaid ? 'dataforseo' : null,
        warnings,
        maxSignals: args.maxSignals,
    });
    await writeJsonOutput(args.out, summary);
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
});
