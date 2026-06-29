#!/usr/bin/env node
/**
 * HTM (Den Haag public transport, "Mijn HTM") CLI wrapper — reads credentials
 * from environment variables: HTM_LOGIN, HTM_PASSWORD
 *
 * Usage: node htm.mjs <command> [args]
 *
 * Commands:
 *   passes                                       list passes (bank cards and OV-passen)
 *   products <tokenId>                           list products for a pass
 *   reizen <tokenId> <from> <to>                 trips for a pass, dates YYYY-MM-DD
 *   reorder <tokenId> <productId> [validFrom]     configure+cart a product, dates YYYY-MM-DD
 */

import { fileURLToPath } from 'url';
import { readFileSync } from 'fs';

const LOGIN = process.env.HTM_LOGIN;
const PASSWORD = process.env.HTM_PASSWORD;

const TENANT = 'htmnlb2c.onmicrosoft.com';
const POLICY = 'B2C_1_ABT-SFA-SignUpSignIn-001';
const UA = 'Mozilla/5.0';

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  if (!LOGIN || !PASSWORD) {
    console.error('Set HTM_LOGIN, HTM_PASSWORD before running.');
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Login (Azure AD B2C custom policy, self-asserted sign-in)
//
// www.htm.nl delegates auth to Azure AD B2C (htmnlb2c.b2clogin.com). The flow
// is OIDC authorization code + PKCE with response_mode=form_post, but the B2C
// sign-in page itself is a plain HTML form (no JS execution needed):
//   1. GET  www.htm.nl/Account/Login            -> 302 to B2C authorize URL
//   2. GET  <authorize URL>                     -> HTML with csrf + transId
//   3. POST <tenant>/<policy>/SelfAsserted       -> {"status":"200"} on success
//   4. GET  <tenant>/<policy>/.../confirmed      -> HTML auto-post form
//      (state, client_info, code) targeting www.htm.nl/signin-oidc
//   5. POST www.htm.nl/signin-oidc with that form -> 302 to /mijn-htm/,
//      sets the .AspNetCore.Cookies session cookie used by every API below.
// ---------------------------------------------------------------------------

function extract(html, re, what) {
  const m = html.match(re);
  if (!m) throw new Error(`Login flow changed: could not find ${what}`);
  return m[1];
}

export async function login(user = LOGIN, password = PASSWORD) {
  const jar = new Map();
  const saveCookies = r => {
    for (const sc of r.headers.getSetCookie()) {
      const kv = sc.split(';', 1)[0];
      const eq = kv.indexOf('=');
      jar.set(kv.slice(0, eq).trim(), kv.slice(eq + 1).trim());
    }
  };
  const cookieHeader = () => [...jar].map(([k, v]) => `${k}=${v}`).join('; ');
  const request = async (url, init = {}) => {
    const r = await fetch(url, {
      ...init,
      redirect: 'manual',
      headers: { 'User-Agent': UA, ...init.headers, Cookie: cookieHeader() },
    });
    saveCookies(r);
    return r;
  };

  // Step 1+2: kick off the OIDC redirect and load the B2C sign-in page.
  let r = await request('https://www.htm.nl/Account/Login?ReturnUrl=%2Fmijn-htm%2F');
  const authorizeUrl = r.headers.get('location');
  if (!authorizeUrl) throw new Error('Login flow changed: expected redirect to B2C authorize endpoint');
  const signinPage = await (await request(authorizeUrl)).text();

  const transId = extract(signinPage, /"transId":"([^"]+)"/, 'transId');
  const csrf = extract(signinPage, /"csrf":"([^"]+)"/, 'csrf token');

  // Step 3: submit credentials to the self-asserted endpoint.
  const selfAssertedUrl = `https://htmnlb2c.b2clogin.com/${TENANT}/${POLICY}/SelfAsserted` +
    `?tx=${encodeURIComponent(transId)}&p=${POLICY}`;
  const body = new URLSearchParams({ request_type: 'RESPONSE', email: user, password });
  const selfAsserted = await (await request(selfAssertedUrl, {
    method: 'POST',
    headers: {
      'x-csrf-token': csrf,
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    },
    body: body.toString(),
  })).json();
  if (selfAsserted.status !== '200') {
    throw new Error(`Login failed: ${selfAsserted.message || JSON.stringify(selfAsserted)}`);
  }

  // Step 4: confirm the sign-in to get the auto-post form with the auth code.
  const confirmedUrl = `https://htmnlb2c.b2clogin.com/${TENANT}/${POLICY}/api/CombinedSigninAndSignup/confirmed` +
    `?csrf_token=${encodeURIComponent(csrf)}&tx=${encodeURIComponent(transId)}&p=${POLICY}`;
  const confirmedHtml = await (await request(confirmedUrl)).text();

  const state = extract(confirmedHtml, /name='state' id='state' value='([^']*)'/, 'OIDC state');
  const clientInfo = extract(confirmedHtml, /name='client_info' id='client_info' value='([^']*)'/, 'client_info');
  const code = extract(confirmedHtml, /name='code' id='code' value='([^']*)'/, 'auth code');

  // Step 5: complete the OIDC flow on www.htm.nl to obtain the session cookie.
  const finish = await request('https://www.htm.nl/signin-oidc', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ state, client_info: clientInfo, code }).toString(),
  });
  if (finish.status !== 302 || !cookieHeader().includes('.AspNetCore.Cookies')) {
    throw new Error('Login flow changed: signin-oidc did not establish a session cookie');
  }

  return cookieHeader();
}

// ---------------------------------------------------------------------------
// Authenticated GET against www.htm.nl's own API (same-origin, cookie auth)
// ---------------------------------------------------------------------------

export async function apiGet(session, path, query = {}) {
  const qs = new URLSearchParams(query).toString();
  const url = `https://www.htm.nl${path}${qs ? `?${qs}` : ''}`;
  const r = await fetch(url, { headers: { Cookie: session, Accept: 'application/json', 'User-Agent': UA } });
  if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
  return r.json();
}

// ---------------------------------------------------------------------------
// Order/cart API (www.htm.nl/v3/order/*)
//
// Unlike everything above, these endpoints require an `X-API-Key` header in
// addition to the session cookie. The key is hardcoded in HTM's own frontend
// bundle under the name TEMP_EXPOSED_API_ORDER_V3_KEY — see README.md. There
// is no guarantee HTM keeps honoring it; orderApiCall() below turns a
// 401/403 from this group into an error that says so explicitly, so that a
// revoked key fails loudly and distinguishably instead of as a generic HTTP
// error.
// ---------------------------------------------------------------------------

const ORDER_API_KEY = 'be3fb314-eabf-4a20-b672-da3ff062750e'; // TEMP_EXPOSED_API_ORDER_V3_KEY

export async function orderApiCall(session, method, path, body) {
  const r = await fetch(`https://www.htm.nl${path}`, {
    method,
    headers: {
      Cookie: session,
      'User-Agent': UA,
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-API-Key': ORDER_API_KEY,
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (r.status === 401 || r.status === 403) {
    throw new Error(
      `Order API key rejected (HTTP ${r.status} for ${method} ${path}). HTM likely revoked/rotated ` +
      `the internal order API key (TEMP_EXPOSED_API_ORDER_V3_KEY) this command depends on — see README.md. ` +
      `passes/products/reizen are unaffected, only reorder needs this key.`
    );
  }
  if (!r.ok) throw new Error(`HTTP ${r.status} for ${method} ${path}`);
  return r.json();
}

// ---------------------------------------------------------------------------
// passes / products / reizen
// ---------------------------------------------------------------------------

export async function passes(session) {
  const tokens = await apiGet(session, '/v1/PortalCustomer/OvPayToken');
  return tokens.map(t => ({
    id: t.ovPayTokenId,
    type: t.tokenType?.name ?? null,
    alias: t.alias ?? null,
    lastDigits: t.lastDigits ?? null,
    ovPasNumber: t.ovPasNumber ?? null,
    statusId: t.tokenStatusId,
    expirationDate: t.expirationDate,
    balance: t.amount,
  }));
}

export async function products(session, tokenId) {
  const [active, inactive] = await Promise.all([
    apiGet(session, '/v1/PortalCustomer/ActiveProductsForToken', { tokenId }),
    apiGet(session, '/v1/PortalCustomer/InactiveProductsForToken', { tokenId }),
  ]);
  const map = (instances, isActive) => (instances ?? []).map(p => ({
    id: p.productId,
    name: p.name,
    category: p.productCategory?.name ?? null,
    status: p.displayStatus ?? p.status,
    active: isActive,
    from: p.fromInclusive,
    until: p.untilInclusive,
  }));
  return [...map(active.productInstances, true), ...map(inactive.productInstances, false)];
}

const stopName = loc => loc?.stopName?.items?.find(i => i.key === 'nl-NL')?.value ?? null;
const amsterdamDate = iso => new Date(iso).toLocaleDateString('en-CA', { timeZone: 'Europe/Amsterdam' });

/** Raw trips (untransformed API shape) for a pass, filtered to local calendar dates. */
async function fetchTrips(session, tokenId, from, to) {
  // The API filters by UTC instant, but `from`/`to` are local (Europe/Amsterdam)
  // calendar dates. Request a one-day-padded window, then filter precisely on
  // the trip's local checkin date so we never miss trips near midnight.
  const start = new Date(`${from}T00:00:00.000Z`);
  start.setUTCDate(start.getUTCDate() - 1);
  const end = new Date(`${to}T23:59:59.999Z`);
  end.setUTCDate(end.getUTCDate() + 1);

  const trips = [];
  for (let page = 0; page < 50; page++) {
    const data = await apiGet(session, '/v1/PortalCustomer/Trips', {
      ovPayTokenId: tokenId,
      start: start.toISOString(),
      end: end.toISOString(),
      pageSize: 100,
      pageNumber: page,
    });
    trips.push(...data.pages);
    if (page + 1 >= data.totalPages) break;
  }

  return trips.filter(t => {
    const d = amsterdamDate(t.checkinTransactionTimestamp);
    return d >= from && d <= to;
  });
}

export async function reizen(session, tokenId, from, to) {
  const trips = await fetchTrips(session, tokenId, from, to);
  return trips.map(t => ({
    id: t.tripId,
    status: t.tripStatus,
    transport: t.transportType,
    line: t.lineId,
    fare: t.fare / 100,
    currency: t.currency,
    checkin: t.checkinTransactionTimestamp,
    checkout: t.checkoutTransactionTimestamp,
    from: stopName(t.checkinLocation),
    to: stopName(t.checkoutLocation),
  }));
}

// ---------------------------------------------------------------------------
// regioAdvies — is a "Regio Vrij" (Den Haag/Delft/Zoetermeer area flat-rate)
// subscription worth it for one or more passes, based on actual trip history?
//
// Prices and region/stop membership are read from the bundled regio-catalog.json
// rather than fetched live, since the source data — /v1/wipkip/getdata (the
// data behind the webshop's "Reisgebied bepalen" map tool: region polygons
// plus ~1250 stops' coordinates, keyed by the same stopId trips carry in
// checkinLocation/checkoutLocation) and /v3/order/product/regions/6
// (productId 6 = Regio Vrij) — only changes on HTM's fixed annual
// pricing/network revision date. Bundling means evaluating several family
// members' passes costs one trip-history fetch per pass and no catalog fetch
// at all — and regio-advies no longer needs the order API key. htm.test.mjs
// re-fetches live and fails loudly if the bundle has drifted; run
// `node refresh-regio-catalog.mjs` to update it.
//
// All that coverage computation ever needs is "is this stopId inside this
// region", so the catalog stores precomputed stop *membership* rather than
// coordinates or polygons. Several of HTM's named regions are explicitly
// combinations of smaller ones (e.g. "DH72 | Den Haag Centrum /
// Leidschendam / Voorburg / Leidschenveen" is a strict superset of
// "DH70 | Den Haag Centrum", and "HL64"/"HL65" each contain ~10 of the other
// 11 regions) — repeating their ~1250-stop membership list per region would
// be ~8x larger than necessary, so each region is instead stored as the
// other regions it fully contains (`includes`) plus only the stops not
// already covered by one of those (`extraStopIds`). A trip is "covered" by a
// region only if both its checkin and checkout stop are members — matching
// how the area pass actually works (unlimited travel *within* the area, not
// to/from it).
// ---------------------------------------------------------------------------

export const REGIO_VRIJ_PRODUCT_ID = 6;

const CATALOG_PATH = new URL('./regio-catalog.json', import.meta.url);
const regioCatalog = () => JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));

/** Ray-casting point-in-polygon test. point/ring are [lng, lat] pairs. */
function pointInPolygon([lng, lat], ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i];
    const [xj, yj] = ring[j];
    if ((yi > lat) !== (yj > lat) && lng < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

/**
 * Builds the regio-catalog.json shape from live wipkip + region-prices
 * responses: resolves each region's stop membership by point-in-polygon,
 * then factors out any region that's a strict subset of another into
 * `includes` so combined regions don't repeat near-identical stop lists.
 * Since `includes` is computed against *every* other region (not just
 * direct/minimal ones), it's already the full transitive closure — so a
 * region's effective membership is just its own extraStopIds plus the
 * extraStopIds of everything in `includes`, with no recursion needed.
 */
export function buildRegioCatalog(wipkip, regionPrices) {
  const pricesById = new Map(regionPrices.map(r => [r.productId, r.prices]));
  const stops = wipkip.stopsData.map(s => ({
    stopId: String(s.stopId),
    coordinates: [s.coordinates.longitude, s.coordinates.latitude],
  }));

  const bases = wipkip.wipKipGeoData
    .map(r => {
      const polygon = r.coordinates.map(c => [c.longitude, c.latitude]);
      return {
        id: r.productExternalId,
        name: r.productName,
        prices: pricesById.get(r.productExternalId) ?? null,
        stopIds: new Set(stops.filter(s => pointInPolygon(s.coordinates, polygon)).map(s => s.stopId)),
      };
    })
    .filter(r => r.prices != null);

  return {
    regions: bases.map(b => {
      const includes = bases
        .filter(a => a.id !== b.id && a.stopIds.size < b.stopIds.size && [...a.stopIds].every(s => b.stopIds.has(s)))
        .map(a => a.id);
      const covered = new Set(includes.flatMap(id => [...bases.find(a => a.id === id).stopIds]));
      const extraStopIds = [...b.stopIds].filter(s => !covered.has(s)).sort();
      return { id: b.id, name: b.name, prices: b.prices, includes, extraStopIds };
    }),
  };
}

function monthsBetween(from, to) {
  const months = new Set();
  const d = new Date(`${from}T00:00:00`);
  const end = new Date(`${to}T00:00:00`);
  while (d <= end) {
    months.add(d.toISOString().slice(0, 7));
    d.setMonth(d.getMonth() + 1);
  }
  return months.size;
}

const round2 = n => Math.round(n * 100) / 100;

/** Pure: how well each catalog region's price would have been justified by these raw trips. */
export function coverageForTrips(trips, catalog, ageProfile, months) {
  const byId = new Map(catalog.regions.map(r => [r.id, r]));
  const regions = catalog.regions
    .map(r => {
      const stopIds = new Set(r.extraStopIds);
      for (const includedId of r.includes) for (const s of byId.get(includedId).extraStopIds) stopIds.add(s);
      return { id: r.id, name: r.name, stopIds, price: r.prices.find(p => p.ageProfiles.includes(ageProfile))?.price ?? null };
    })
    .filter(r => r.price != null);

  const totals = new Map(regions.map(r => [r.id, 0]));
  let totalFare = 0;
  let uncoveredTrips = 0;

  for (const t of trips) {
    const fare = t.fare / 100;
    totalFare += fare;
    const inId = String(t.checkinLocation?.stopId);
    const outId = String(t.checkoutLocation?.stopId);
    const coveringRegions = regions.filter(r => r.stopIds.has(inId) && r.stopIds.has(outId));
    if (coveringRegions.length === 0) uncoveredTrips++;
    for (const r of coveringRegions) totals.set(r.id, totals.get(r.id) + fare);
  }

  const results = regions
    .map(r => {
      const coveredFare = totals.get(r.id);
      const avgMonthlyCoveredFare = coveredFare / months;
      return {
        id: r.id,
        name: r.name,
        price: r.price,
        coveredFare: round2(coveredFare),
        avgMonthlyCoveredFare: round2(avgMonthlyCoveredFare),
        monthlyMargin: round2(avgMonthlyCoveredFare - r.price),
        worthIt: avgMonthlyCoveredFare > r.price,
      };
    })
    .sort((a, b) => b.monthlyMargin - a.monthlyMargin);

  return { totalTrips: trips.length, totalFare: round2(totalFare), uncoveredTrips, regions: results };
}

export async function regioAdvies(session, tokenIds, from, to, ageProfile = 'Adult') {
  const catalog = regioCatalog();
  const months = monthsBetween(from, to);
  const ids = Array.isArray(tokenIds) ? tokenIds : [tokenIds];

  return Promise.all(ids.map(async tokenId => {
    const trips = await fetchTrips(session, tokenId, from, to);
    return {
      tokenId: Number(tokenId),
      ageProfile,
      periodMonths: months,
      ...coverageForTrips(trips, catalog, ageProfile, months),
    };
  }));
}

// ---------------------------------------------------------------------------
// reorder — configure a product and add it to the cart for a pass. Stops
// short of payment: HTM's checkout hands off to Buckaroo (iDEAL/etc.), which
// requires interactive bank authorization no script can do. Returns a
// checkoutUrl to open in a browser and pay manually.
//
// HTM caps how far in advance you can set a custom start date: the API
// rejects a validFrom more than ~30 days out with a clear validation error
// ("The start date is too far in the future..."), which surfaces as-is.
// ---------------------------------------------------------------------------

export async function reorder(session, tokenId, productId, validFrom) {
  tokenId = Number(tokenId);
  productId = Number(productId);

  const tokens = await apiGet(session, '/v1/PortalCustomer/OvPayToken');
  const token = tokens.find(t => t.ovPayTokenId === tokenId);
  if (!token) throw new Error(`No pass found with id ${tokenId}`);
  const tokenTypeId = token.tokenType?.tokenTypeId;

  // Reuse any existing line for this product rather than adding a new one each
  // call, so re-running reorder() (e.g. to change the date) is idempotent and
  // never piles up duplicate billable lines on the same draft order.
  const matchLine = order => order.orderLines.find(l => l.productId === productId);

  let order = await orderApiCall(session, 'POST', '/v3/order/initialize', { orderLines: [{ productId }] });
  let line = matchLine(order);
  if (!line) {
    order = await orderApiCall(session, 'POST', `/v3/order/${order.orderId}/orderline`, { productId });
    line = matchLine(order) ?? order.orderLines.at(-1);
  }

  // Re-attaching a token that's already on the line doesn't replace it — it adds
  // a second, duplicate customerTokens entry, which then makes the next PATCH
  // (date change) fail with a 500. Only attach if it isn't there yet.
  const alreadyAttached = line.customerTokens?.some(t => t.ovPayTokenId === tokenId);
  if (!alreadyAttached) {
    order = await orderApiCall(session, 'POST', `/v3/order/orderline/${line.orderLineId}/token`, {
      tokenTypeId,
      ovPayTokenId: tokenId,
    });
  }

  if (validFrom) {
    order = await orderApiCall(session, 'PATCH', `/v3/order/orderline/${line.orderLineId}`, { validFrom });
  }

  // Only this line's own validation matters — the draft order may carry other,
  // unrelated lines (e.g. an abandoned earlier attempt) that shouldn't block us.
  const finalLine = order.orderLines.find(l => l.orderLineId === line.orderLineId);
  const errors = finalLine?.validationErrors ?? [];
  if (errors.length > 0) {
    throw new Error(errors.map(e => e.detail).join('; '));
  }

  return {
    orderId: order.orderId,
    orderNumber: order.orderNumber,
    orderLineId: finalLine.orderLineId,
    product: finalLine.productName,
    validFrom: finalLine.validFrom,
    validUntil: finalLine.validUntil,
    totalAmount: order.totalAmount / 100,
    currency: 'EUR',
    checkoutUrl: 'https://www.htm.nl/winkelwagen/',
  };
}

/** Removes an orderline added by reorder() — used to abandon a draft without paying. */
export async function cancelOrderline(session, orderLineId) {
  return orderApiCall(session, 'DELETE', `/v3/order/orderline/${orderLineId}`);
}

// ---------------------------------------------------------------------------
// CLI (only when run directly)
// ---------------------------------------------------------------------------

const COMMANDS = 'Commands: passes | products <tokenId> | reizen <tokenId> <from> <to> | ' +
  'regio-advies <tokenId>[,<tokenId>...] <from> <to> [ageProfile] | reorder <tokenId> <productId> [validFrom]';

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [cmd, ...rest] = process.argv.slice(2);

  async function run() {
    if (!['passes', 'products', 'reizen', 'regio-advies', 'reorder'].includes(cmd)) {
      console.error(COMMANDS);
      process.exit(1);
    }
    const session = await login();
    switch (cmd) {
      case 'passes':
        console.log(JSON.stringify(await passes(session)));
        break;
      case 'products': {
        const [tokenId] = rest;
        console.log(JSON.stringify(await products(session, tokenId)));
        break;
      }
      case 'reizen': {
        const [tokenId, from, to] = rest;
        console.log(JSON.stringify(await reizen(session, tokenId, from, to)));
        break;
      }
      case 'regio-advies': {
        const [tokenIds, from, to, ageProfile] = rest;
        console.log(JSON.stringify(await regioAdvies(session, tokenIds.split(','), from, to, ageProfile)));
        break;
      }
      case 'reorder': {
        const [tokenId, productId, validFrom] = rest;
        console.log(JSON.stringify(await reorder(session, tokenId, productId, validFrom)));
        break;
      }
    }
  }

  run().catch(e => { console.error(e.message); process.exit(1); });
}
