const RACING_ORIGIN = 'https://racing.hkjc.com';
const RACE_CARD_PATH = '/en-us/local/information/racecard';
const RACE_RESULTS_PATH = '/en-us/local/information/localresults';

function decodeHtml(value) {
  return value
    .replace(/&nbsp;|&#160;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&#(x[0-9a-f]+|\d+);/gi, (_, code) => {
      const radix = code[0].toLowerCase() === 'x' ? 16 : 10;
      const number = Number.parseInt(radix === 16 ? code.slice(1) : code, radix);
      return Number.isFinite(number) ? String.fromCodePoint(number) : _;
    });
}

function textFromHtml(html) {
  return decodeHtml(html
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<br\b[^>]*>/gi, '\n')
    .replace(/<\/(?:div|p|tr|table|h[1-6]|li|td|th)>/gi, '\n')
    .replace(/<[^>]+>/g, ' '))
    .split(/\r?\n/)
    .map(line => line.replace(/\s+/g, ' ').trim())
    .filter(Boolean);
}

function cellText(html) {
  return textFromHtml(html).join(' ').trim();
}

function parseDate(date) {
  if (!date) return null;
  const match = /^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/.exec(date);
  if (!match) {
    throw new Error(`Invalid date "${date}". Expected YYYY-MM-DD.`);
  }
  const [, year, month, day] = match;
  return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}

function formatHkjcDate(date) {
  return parseDate(date).replace(/-/g, '/');
}

function englishDateToIso(value) {
  const match = /(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})/i.exec(value);
  if (!match) return null;
  const months = {
    january: '01', february: '02', march: '03', april: '04',
    may: '05', june: '06', july: '07', august: '08',
    september: '09', october: '10', november: '11', december: '12'
  };
  const month = months[match[1].toLowerCase()];
  if (!month) return null;
  return `${match[3]}-${month}-${match[2].padStart(2, '0')}`;
}

function numericValue(value) {
  const normalized = value.replace(/,/g, '').trim();
  if (!normalized || normalized === '-') return null;
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

function rowsFromTable(tableHtml) {
  return [...tableHtml.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/gi)].map(row => {
    return [...row[1].matchAll(/<(?:td|th)\b[^>]*>([\s\S]*?)<\/(?:td|th)>/gi)]
      .map(cell => cell[1]);
  });
}

function findTable(html, className) {
  const tags = /<table\b[^>]*>|<\/table\s*>/gi;
  let match;
  while ((match = tags.exec(html)) !== null) {
    if (/^<\/table/i.test(match[0])) continue;
    const classValue = /\bclass\s*=\s*["']([^"']*)["']/i.exec(match[0])?.[1] || '';
    if (!classValue.split(/\s+/).includes(className)) continue;

    let depth = 1;
    let endTag;
    while ((endTag = tags.exec(html)) !== null) {
      if (/^<\/table/i.test(endTag[0])) depth--;
      else depth++;
      if (depth === 0) return html.slice(match.index, tags.lastIndex);
    }
    return null;
  }
  return null;
}

function findColumn(headers, expression) {
  return headers.findIndex(header => expression.test(cellText(header)));
}

function getHorseId(horseCell) {
  const href = /\bhref\s*=\s*["']([^"']+)["']/i.exec(horseCell)?.[1];
  if (!href) return null;
  const decodedHref = decodeHtml(href);
  const queryValue = /[?&]horseid=([^&#]+)/i.exec(decodedHref)?.[1];
  if (queryValue) return decodeURIComponent(queryValue);
  return null;
}

function getRaceNavigation(html, path) {
  const pageUrl = new URL(path, RACING_ORIGIN);
  const routes = new Map();
  for (const match of html.matchAll(/\bhref\s*=\s*["']([^"']+)["']/gi)) {
    const href = decodeHtml(match[1]);
    let url;
    try {
      url = new URL(href, pageUrl);
    } catch {
      continue;
    }
    if (url.origin !== RACING_ORIGIN || !url.pathname.endsWith(path.split('?')[0])) continue;
    const raceNo = Number.parseInt(url.searchParams.get('RaceNo'), 10);
    if (!Number.isInteger(raceNo) || raceNo < 1) continue;
    routes.set(raceNo, {
      raceNo,
      venueCode: url.searchParams.get('Racecourse'),
      date: url.searchParams.get('racedate')
    });
  }
  return [...routes.values()].sort((left, right) => left.raceNo - right.raceNo);
}

function buildUrl(path, date, raceNo, venueCode) {
  const url = new URL(path, RACING_ORIGIN);
  if (date) url.searchParams.set('racedate', formatHkjcDate(date));
  if (venueCode) url.searchParams.set('Racecourse', venueCode);
  if (raceNo != null) url.searchParams.set('RaceNo', String(raceNo));
  return url;
}

async function fetchHtml(url, label) {
  const response = await fetch(url, { headers: { accept: 'text/html' } });
  if (!response.ok) {
    throw new Error(`HKJC ${label} request failed with HTTP ${response.status}.`);
  }
  return response.text();
}

function parseRaceCardPage(html, expectedDate, expectedRaceNo) {
  const mainContent = html.slice(Math.max(0, html.indexOf('id="innerContent"')));
  const header = /Race\s+(\d+)\s*-\s*([^<\r\n]+)/i.exec(mainContent);
  if (!header) return null;

  const raceNo = Number.parseInt(header[1], 10);
  if (expectedRaceNo != null && raceNo !== expectedRaceNo) {
    throw new Error(`HKJC race-card page returned race ${raceNo} instead of race ${expectedRaceNo}.`);
  }

  const headerIndex = header.index;
  const summaryHtml = mainContent.slice(headerIndex, headerIndex + 1800);
  const summaryLines = textFromHtml(summaryHtml);
  const dateLine = summaryLines.find(line => englishDateToIso(line));
  const pageDate = dateLine ? englishDateToIso(dateLine) : null;
  if (expectedDate && pageDate !== parseDate(expectedDate)) {
    throw new Error(`HKJC race-card page date mismatch: expected ${parseDate(expectedDate)}, received ${pageDate || 'unknown'}.`);
  }

  const venueMatch = dateLine && /,\s+(Happy Valley|Sha Tin),\s+\d{1,2}:\d{2}/i.exec(dateLine);
  const venue = venueMatch ? venueMatch[1] : null;
  const summaryText = summaryLines.join(' ');
  const distance = Number.parseInt(/\b(\d{3,4})M\b/i.exec(summaryText)?.[1], 10) || null;
  const classMatch = /\bClass\s+(\d+)\b/i.exec(summaryText);
  const goingMatch = /\bGoing\s*:\s*([A-Z][A-Z -]*)/i.exec(summaryText);
  const table = findTable(mainContent, 'starter');
  if (!table) {
    throw new Error(`HKJC race-card page for ${pageDate || 'unknown date'} race ${raceNo} has no runner table.`);
  }

  const tableRows = rowsFromTable(table);
  const headers = tableRows[0] || [];
  const columns = {
    horseNo: findColumn(headers, /^Horse No\.?$/i),
    form: findColumn(headers, /^Last 6 Runs$/i),
    horseName: findColumn(headers, /^Horse$/i),
    weight: findColumn(headers, /^Wt\.?$/i),
    jockey: findColumn(headers, /^Jockey$/i),
    barrier: findColumn(headers, /^Draw$/i),
    trainer: findColumn(headers, /^Trainer$/i),
    gear: findColumn(headers, /^Gear$/i),
    winOdds: findColumn(headers, /^(?:Win )?Odds$/i),
    placeOdds: findColumn(headers, /^Place Odds$/i)
  };
  const optionalColumns = new Set(['winOdds', 'placeOdds']);
  const missingColumns = Object.entries(columns)
    .filter(([name, index]) => index < 0 && !optionalColumns.has(name))
    .map(([name]) => name);
  if (missingColumns.length) {
    throw new Error(`HKJC race-card runner table is missing columns: ${missingColumns.join(', ')}.`);
  }

  const horses = tableRows.slice(1).map(row => {
    const get = name => row[columns[name]] ? cellText(row[columns[name]]) : '';
    const jockeyCell = get('jockey');
    const allowanceMatch = /\((-?\d+)\)\s*$/.exec(jockeyCell);
    const horseCell = row[columns.horseName] || '';
    const horseName = cellText(horseCell);
    const pastRuns = get('form').split('/').map(value => Number.parseInt(value, 10)).filter(Number.isFinite).reverse();
    const gear = get('gear').split('/').map(value => value.trim()).filter(value => value && value !== '-');

    return {
      barrier: numericValue(get('barrier')),
      horseNo: numericValue(get('horseNo')),
      horseName: horseName || '(no English name)',
      horseId: getHorseId(horseCell),
      weight: numericValue(get('weight')),
      jockey: jockeyCell.replace(/\s*\(-?\d+\)\s*$/, '').trim() || null,
      jockeyAllowance: allowanceMatch ? Number.parseInt(allowanceMatch[1], 10) : null,
      trainer: get('trainer') || null,
      pastRuns,
      gear,
      winOdds: columns.winOdds >= 0 ? numericValue(get('winOdds')) : null,
      placeOdds: columns.placeOdds >= 0 ? numericValue(get('placeOdds')) : null
    };
  }).filter(horse => horse.horseNo != null && horse.barrier != null);

  return {
    raceNo,
    raceName: header[2].trim(),
    venue,
    venueCode: venue === 'Happy Valley' ? 'HV' : venue === 'Sha Tin' ? 'ST' : null,
    date: pageDate,
    distance,
    class: classMatch ? `Class ${classMatch[1]}` : null,
    going: goingMatch ? goingMatch[1].trim() : null,
    horses
  };
}

async function fetchRaceCardMeeting({ date, raceNo }) {
  const firstRaceNo = raceNo == null ? 1 : Number(raceNo);
  const firstUrl = buildUrl(RACE_CARD_PATH, date, firstRaceNo);
  const firstHtml = await fetchHtml(firstUrl, 'race-card');
  const firstRace = parseRaceCardPage(firstHtml, date, firstRaceNo);
  if (!firstRace) return { meeting: null, races: [] };

  const meeting = {
    venue: firstRace.venue,
    date: firstRace.date,
    weather: null,
    trackCondition: firstRace.going
  };
  if (raceNo != null) return { meeting, races: [firstRace] };

  const raceRoutes = getRaceNavigation(firstHtml, RACE_CARD_PATH);
  const races = [firstRace];
  for (const route of raceRoutes) {
    if (route.raceNo === firstRaceNo) continue;
    const routeDate = route.date ? parseDate(route.date.replace(/\//g, '-')) : date;
    if (routeDate !== firstRace.date) continue;
    const url = buildUrl(RACE_CARD_PATH, firstRace.date, route.raceNo, route.venueCode || firstRace.venueCode);
    const html = await fetchHtml(url, 'race-card');
    const race = parseRaceCardPage(html, firstRace.date, route.raceNo);
    if (!race) throw new Error(`HKJC did not return race-card data for race ${route.raceNo} on ${firstRace.date}.`);
    races.push(race);
  }
  return { meeting, races };
}

function parseRaceResultsPage(html, expectedDate, expectedRaceNo) {
  const mainContent = html.slice(Math.max(0, html.indexOf('id="innerContent"')));
  const resultTable = findTable(mainContent, 'draggable');
  if (!resultTable) return null;

  const rows = rowsFromTable(resultTable);
  const headers = rows[0] || [];
  const columns = {
    position: findColumn(headers, /^(?:Pla\.?|Position)$/i),
    horseNo: findColumn(headers, /^Horse No\.?$/i),
    horseName: findColumn(headers, /^Horse$/i),
    jockey: findColumn(headers, /^Jockey$/i),
    trainer: findColumn(headers, /^Trainer$/i),
    actualWeight: findColumn(headers, /^Act\. Wt\.?$/i),
    declaredHorseWeight: findColumn(headers, /^Declar\. Horse Wt\.?$/i),
    barrier: findColumn(headers, /^Dr\.?$/i),
    lengthsBehind: findColumn(headers, /^LBW$/i),
    runningPosition: findColumn(headers, /^Running Position$/i),
    finishTime: findColumn(headers, /^Finish Time$/i),
    winOdds: findColumn(headers, /^Win Odds$/i)
  };
  const missingColumns = Object.entries(columns).filter(([, index]) => index < 0).map(([name]) => name);
  if (missingColumns.length) {
    throw new Error(`HKJC results runner table is missing columns: ${missingColumns.join(', ')}.`);
  }

  const summary = textFromHtml(mainContent);
  const resultHeader = summary.find(line => /^RACE\s+\d+\s*\(\d+\)/i.test(line));
  const headerMatch = resultHeader && /^RACE\s+(\d+)\s*(?:\((\d+)\))?/i.exec(resultHeader);
  const raceNo = headerMatch ? Number.parseInt(headerMatch[1], 10) : null;
  if (raceNo == null) throw new Error('Unable to determine the race number from the HKJC results page.');
  if (expectedRaceNo != null && raceNo !== expectedRaceNo) {
    throw new Error(`HKJC results page returned race ${raceNo} instead of race ${expectedRaceNo}.`);
  }

  const raceInfo = summary.find(line => /\bClass\s+\d+\s*-\s*\d{3,4}M\b/i.test(line)) || '';
  const raceName = summary.find((line, index) => {
    return index > 0 && !/\bClass\s+\d+\s*-\s*\d{3,4}M\b/i.test(line) && /HANDICAP|STAKES|CUP/i.test(line);
  }) || null;
  const classMatch = /\bClass\s+(\d+)\b/i.exec(raceInfo);
  const distanceMatch = /\b(\d{3,4})M\b/i.exec(raceInfo);
  const goingMatch = /\bGoing\s*:\s*([A-Z][A-Z -]*)/i.exec(raceInfo);
  const venueMatch = /^(Happy Valley|Sha Tin):?$/i.exec(summary.find(line => /^(Happy Valley|Sha Tin):?$/i.test(line)) || '');
  const routes = getRaceNavigation(html, RACE_RESULTS_PATH);
  const route = routes[0];
  const pageDate = expectedDate
    ? parseDate(expectedDate)
    : route?.date
      ? parseDate(route.date.replace(/\//g, '-'))
      : null;
  if (expectedDate && route?.date && parseDate(route.date.replace(/\//g, '-')) !== parseDate(expectedDate)) {
    throw new Error(`HKJC results page date mismatch: expected ${parseDate(expectedDate)}, received ${route.date}.`);
  }

  const runnerRows = rows.slice(1).filter(row => row.some(cell => cellText(cell)));
  const results = runnerRows.map(row => {
    const get = name => row[columns[name]] ? cellText(row[columns[name]]) : '';
    const horseCell = row[columns.horseName] || '';
    const fullHorseName = cellText(horseCell);
    return {
      position: get('position') || null,
      horseNo: numericValue(get('horseNo')),
      horseName: fullHorseName.replace(/\s+\([A-Z]\d{3}\)$/i, '') || '(no English name)',
      horseId: getHorseId(horseCell),
      jockey: get('jockey') || null,
      trainer: get('trainer') || null,
      actualWeight: numericValue(get('actualWeight')),
      declaredHorseWeight: numericValue(get('declaredHorseWeight')),
      barrier: numericValue(get('barrier')),
      lengthsBehind: get('lengthsBehind') || null,
      runningPosition: get('runningPosition') || null,
      finishTime: get('finishTime') || null,
      winOdds: numericValue(get('winOdds'))
    };
  }).filter(result => result.horseNo != null);

  const dividendTable = findTable(mainContent, 'f_fs13');
  const dividendRows = dividendTable ? rowsFromTable(dividendTable).slice(2) : [];
  const dividends = dividendRows.map(row => {
    const values = row.map(cellText);
    if (values.length < 3 || !values[0]) return null;
    return {
      pool: values[0],
      winningCombination: values[1] || null,
      dividend: numericValue(values[2])
    };
  }).filter(Boolean);

  return {
    raceNo,
    raceId: headerMatch?.[2] ? Number.parseInt(headerMatch[2], 10) : null,
    raceName,
    class: classMatch ? `Class ${classMatch[1]}` : null,
    distance: distanceMatch ? Number.parseInt(distanceMatch[1], 10) : null,
    going: goingMatch ? goingMatch[1].trim() : null,
    results,
    dividends,
    date: pageDate,
    venue: venueMatch ? venueMatch[1] : null,
    venueCode: route?.venueCode || (venueMatch?.[1] === 'Happy Valley' ? 'HV' : venueMatch?.[1] === 'Sha Tin' ? 'ST' : null)
  };
}

async function fetchRaceResults({ date, raceNo }) {
  const firstRaceNo = raceNo == null ? 1 : Number(raceNo);
  const firstUrl = buildUrl(RACE_RESULTS_PATH, date, raceNo == null ? null : firstRaceNo);
  const firstHtml = await fetchHtml(firstUrl, 'results');
  const firstRace = parseRaceResultsPage(firstHtml, date, raceNo == null ? null : firstRaceNo);
  if (!firstRace) return { date: date ? parseDate(date) : null, venue: null, races: [] };

  if (raceNo != null) {
    return { date: firstRace.date, venue: firstRace.venue, races: [firstRace] };
  }

  const routes = getRaceNavigation(firstHtml, RACE_RESULTS_PATH);
  const races = [firstRace];
  for (const route of routes) {
    if (route.raceNo === firstRaceNo) continue;
    const routeDate = route.date ? parseDate(route.date.replace(/\//g, '-')) : firstRace.date;
    if (firstRace.date && routeDate !== firstRace.date) continue;
    const url = buildUrl(RACE_RESULTS_PATH, routeDate, route.raceNo, route.venueCode || firstRace.venueCode);
    const html = await fetchHtml(url, 'results');
    const race = parseRaceResultsPage(html, routeDate, route.raceNo);
    if (!race) throw new Error(`HKJC did not return results for race ${route.raceNo} on ${routeDate || 'the requested date'}.`);
    races.push(race);
  }
  return { date: firstRace.date, venue: firstRace.venue, races };
}

module.exports = {
  fetchRaceCardMeeting,
  fetchRaceResults,
  parseRaceCardPage,
  parseRaceResultsPage
};
