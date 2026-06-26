/**
 * openclaw-jetlag
 *
 * Scans Google Calendar for flight events, parses origin/destination/times,
 * calculates timezone delta, and writes a circadian adjustment plan back to
 * your calendar as individual timed events with reminders.
 */

import 'dotenv/config';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { google } from 'googleapis';
import { DateTime } from 'luxon';
import open from 'open';

// ─── OAuth Setup ────────────────────────────────────────────────────────────

const TOKEN_PATH = path.resolve('.oauth-token.json');

const SCOPES = ['https://www.googleapis.com/auth/calendar'];

function getOAuthClient() {
  const { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI } = process.env;
  if (!GOOGLE_CLIENT_ID || !GOOGLE_CLIENT_SECRET) {
    console.error('Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env');
    process.exit(1);
  }
  return new google.auth.OAuth2(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI || 'urn:ietf:wg:oauth:2.0:oob'
  );
}

async function authorize() {
  const auth = getOAuthClient();

  if (fs.existsSync(TOKEN_PATH)) {
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
    auth.setCredentials(token);
    // Refresh if expired
    if (token.expiry_date && Date.now() > token.expiry_date - 60_000) {
      const { credentials } = await auth.refreshAccessToken();
      fs.writeFileSync(TOKEN_PATH, JSON.stringify(credentials));
      auth.setCredentials(credentials);
    }
    return auth;
  }

  const authUrl = auth.generateAuthUrl({ access_type: 'offline', scope: SCOPES });
  console.log('\n► Open this URL in your browser:\n');
  console.log('  ' + authUrl + '\n');
  const opened = await open(authUrl).then(() => true).catch(() => false);
  if (opened) {
    console.log('(Browser window opened)');
  } else {
    console.log('(Could not open browser automatically — paste the URL above into your browser manually)');
  }
  console.log('\nAfter you click "Allow", Google will show you a short code.');
  const code = await promptLine('Paste the code here and press Enter: ');
  const { tokens } = await auth.getToken(code.trim());
  fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens));
  auth.setCredentials(tokens);
  console.log('Authorization saved to', TOKEN_PATH);
  return auth;
}

function promptLine(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => rl.question(question, (ans) => { rl.close(); resolve(ans); }));
}

function validateEnv() {
  const nodeVersion = parseInt(process.version.slice(1).split('.')[0], 10);
  if (nodeVersion < 18) {
    console.error(`Node.js 18+ is required. You are running ${process.version}.`);
    console.error('Download the latest version at https://nodejs.org');
    process.exit(1);
  }

  if (!fs.existsSync('.env')) {
    console.error('No .env file found.');
    console.error('  Run:  cp .env.example .env');
    console.error('  Then open .env and replace the placeholder values with your Google credentials.');
    console.error('  See README.md steps 4–6 for how to get them.');
    process.exit(1);
  }

  const PLACEHOLDERS = [
    'your_client_id_here.apps.googleusercontent.com',
    'your_client_secret_here',
  ];
  const { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET } = process.env;

  if (!GOOGLE_CLIENT_ID || PLACEHOLDERS.includes(GOOGLE_CLIENT_ID)) {
    console.error('GOOGLE_CLIENT_ID is missing or still set to the placeholder value.');
    console.error('  Open .env and replace it with your Client ID from Google Cloud Console.');
    console.error('  See README.md step 6 for where to find it.');
    process.exit(1);
  }
  if (!GOOGLE_CLIENT_SECRET || PLACEHOLDERS.includes(GOOGLE_CLIENT_SECRET)) {
    console.error('GOOGLE_CLIENT_SECRET is missing or still set to the placeholder value.');
    console.error('  Open .env and replace it with your Client Secret from Google Cloud Console.');
    console.error('  See README.md step 6 for where to find it.');
    process.exit(1);
  }
}

// ─── Airport → Timezone Map ──────────────────────────────────────────────────
// Covers major airports commonly seen in airline-added calendar events.

const AIRPORT_TZ = {
  // North America – US
  ATL: 'America/New_York', BOS: 'America/New_York', JFK: 'America/New_York',
  LGA: 'America/New_York', EWR: 'America/New_York', MIA: 'America/New_York',
  MCO: 'America/New_York', CLT: 'America/New_York', PHL: 'America/New_York',
  DCA: 'America/New_York', IAD: 'America/New_York', BWI: 'America/New_York',
  DTW: 'America/New_York', PIT: 'America/New_York', BUF: 'America/New_York',
  RDU: 'America/New_York', BNA: 'America/Chicago', MSP: 'America/Chicago',
  ORD: 'America/Chicago', MDW: 'America/Chicago', DFW: 'America/Chicago',
  DAL: 'America/Chicago', IAH: 'America/Chicago', HOU: 'America/Chicago',
  STL: 'America/Chicago', MKE: 'America/Chicago', MCI: 'America/Chicago',
  MSY: 'America/Chicago', OMA: 'America/Chicago', DSM: 'America/Chicago',
  MEM: 'America/Chicago', LIT: 'America/Chicago', TUL: 'America/Chicago',
  OKC: 'America/Chicago', FSD: 'America/Chicago', CID: 'America/Chicago',
  DEN: 'America/Denver', SLC: 'America/Denver', PHX: 'America/Phoenix',
  ABQ: 'America/Denver', BOI: 'America/Boise', BZN: 'America/Denver',
  LAX: 'America/Los_Angeles', SFO: 'America/Los_Angeles', SJC: 'America/Los_Angeles',
  OAK: 'America/Los_Angeles', SAN: 'America/Los_Angeles', SEA: 'America/Los_Angeles',
  PDX: 'America/Los_Angeles', LAS: 'America/Los_Angeles', BUR: 'America/Los_Angeles',
  SMF: 'America/Los_Angeles', RNO: 'America/Los_Angeles', FAT: 'America/Los_Angeles',
  SBA: 'America/Los_Angeles', SPS: 'America/Los_Angeles', GEG: 'America/Los_Angeles',
  ANC: 'America/Anchorage', FAI: 'America/Anchorage',
  HNL: 'Pacific/Honolulu', OGG: 'Pacific/Honolulu', KOA: 'Pacific/Honolulu',
  // Canada
  YYZ: 'America/Toronto', YUL: 'America/Toronto', YOW: 'America/Toronto',
  YVR: 'America/Vancouver', YYC: 'America/Edmonton', YEG: 'America/Edmonton',
  YWG: 'America/Winnipeg', YHZ: 'America/Halifax', YQB: 'America/Toronto',
  // Mexico & Caribbean
  MEX: 'America/Mexico_City', CUN: 'America/Cancun', GDL: 'America/Mexico_City',
  MTY: 'America/Monterrey', SJD: 'America/Mazatlan', PVR: 'America/Mexico_City',
  // Europe
  LHR: 'Europe/London', LGW: 'Europe/London', STN: 'Europe/London',
  CDG: 'Europe/Paris', ORY: 'Europe/Paris', AMS: 'Europe/Amsterdam',
  FRA: 'Europe/Berlin', MUC: 'Europe/Berlin', BER: 'Europe/Berlin',
  ZRH: 'Europe/Zurich', GVA: 'Europe/Zurich', VIE: 'Europe/Vienna',
  FCO: 'Europe/Rome', MXP: 'Europe/Rome', MAD: 'Europe/Madrid',
  BCN: 'Europe/Madrid', LIS: 'Europe/Lisbon', BRU: 'Europe/Brussels',
  CPH: 'Europe/Copenhagen', OSL: 'Europe/Oslo', ARN: 'Europe/Stockholm',
  HEL: 'Europe/Helsinki', WAW: 'Europe/Warsaw', PRG: 'Europe/Prague',
  BUD: 'Europe/Budapest', ATH: 'Europe/Athens', IST: 'Europe/Istanbul',
  SVO: 'Europe/Moscow', LED: 'Europe/Moscow', DME: 'Europe/Moscow',
  DUB: 'Europe/Dublin', EDI: 'Europe/London', MAN: 'Europe/London',
  // Middle East
  DXB: 'Asia/Dubai', AUH: 'Asia/Dubai', DOH: 'Asia/Qatar',
  RUH: 'Asia/Riyadh', KWI: 'Asia/Kuwait', TLV: 'Asia/Jerusalem',
  AMM: 'Asia/Amman', BEY: 'Asia/Beirut', BAH: 'Asia/Bahrain',
  // Africa
  JNB: 'Africa/Johannesburg', CPT: 'Africa/Johannesburg', CAI: 'Africa/Cairo',
  CMN: 'Africa/Casablanca', NBO: 'Africa/Nairobi', LOS: 'Africa/Lagos',
  ADD: 'Africa/Addis_Ababa', ACC: 'Africa/Accra',
  // South Asia
  DEL: 'Asia/Kolkata', BOM: 'Asia/Kolkata', MAA: 'Asia/Kolkata',
  BLR: 'Asia/Kolkata', HYD: 'Asia/Kolkata', CCU: 'Asia/Kolkata',
  COK: 'Asia/Kolkata', AMD: 'Asia/Kolkata',
  KTM: 'Asia/Kathmandu', DAC: 'Asia/Dhaka', CMB: 'Asia/Colombo',
  KHI: 'Asia/Karachi', LHE: 'Asia/Karachi',
  // Southeast Asia
  BKK: 'Asia/Bangkok', DMK: 'Asia/Bangkok', CNX: 'Asia/Bangkok',
  SIN: 'Asia/Singapore', KUL: 'Asia/Kuala_Lumpur', CGK: 'Asia/Jakarta',
  MNL: 'Asia/Manila', HAN: 'Asia/Ho_Chi_Minh', SGN: 'Asia/Ho_Chi_Minh',
  RGN: 'Asia/Rangoon', REP: 'Asia/Phnom_Penh', PNH: 'Asia/Phnom_Penh',
  VTE: 'Asia/Vientiane', DPS: 'Asia/Jakarta',
  // East Asia
  PEK: 'Asia/Shanghai', PKX: 'Asia/Shanghai', PVG: 'Asia/Shanghai',
  SHA: 'Asia/Shanghai', CAN: 'Asia/Shanghai', SZX: 'Asia/Shanghai',
  CTU: 'Asia/Shanghai', XIY: 'Asia/Shanghai', HKG: 'Asia/Hong_Kong',
  MFM: 'Asia/Macau', TPE: 'Asia/Taipei', KHH: 'Asia/Taipei',
  ICN: 'Asia/Seoul', GMP: 'Asia/Seoul', NRT: 'Asia/Tokyo',
  HND: 'Asia/Tokyo', KIX: 'Asia/Tokyo', CTS: 'Asia/Tokyo',
  FUK: 'Asia/Tokyo', NGO: 'Asia/Tokyo',
  // Oceania
  SYD: 'Australia/Sydney', MEL: 'Australia/Melbourne', BNE: 'Australia/Brisbane',
  PER: 'Australia/Perth', ADL: 'Australia/Adelaide', CBR: 'Australia/Sydney',
  AKL: 'Pacific/Auckland', CHC: 'Pacific/Auckland', WLG: 'Pacific/Auckland',
  // South America
  GRU: 'America/Sao_Paulo', GIG: 'America/Sao_Paulo', BSB: 'America/Sao_Paulo',
  EZE: 'America/Argentina/Buenos_Aires', SCL: 'America/Santiago',
  BOG: 'America/Bogota', LIM: 'America/Lima', UIO: 'America/Guayaquil',
  CCS: 'America/Caracas', PTY: 'America/Panama',
};

function airportTz(code) {
  return AIRPORT_TZ[code?.toUpperCase()] || null;
}

// ─── Flight Event Detection ──────────────────────────────────────────────────

const AIRLINE_KEYWORDS = [
  'united airlines', 'delta air', 'american airlines', 'southwest', 'alaska airlines',
  'jetblue', 'spirit airlines', 'frontier', 'hawaiian', 'sun country',
  'air canada', 'lufthansa', 'british airways', 'air france', 'klm',
  'emirates', 'qatar', 'etihad', 'singapore airlines', 'cathay',
  'japan airlines', 'ana ', 'air india', 'turkish airlines',
  'ryanair', 'easyjet', 'wizz', 'iberia', 'tap ', 'swiss',
  'flight ', ' flight', 'departing', 'arrives ', 'boarding',
];

// Matches: UA 1234, DL123, AA 456, F9 789, etc.
const FLIGHT_NUMBER_RE = /\b([A-Z]{2})\s?(\d{1,4})\b/;

// Matches IATA codes in various formats:
//   SFO → JFK  |  SFO-JFK  |  SFO to JFK  |  (SFO) ... (JFK)
const ROUTE_RE = /\b([A-Z]{3})\s*(?:→|->|–|-|to)\s*([A-Z]{3})\b/i;
const PARENS_ROUTE_RE = /\(([A-Z]{3})\).*?\(([A-Z]{3})\)/i;
// Matches United's format: "Flight: SFO (UA2279) to SEA Confirmation PECRX5"
const INLINE_FLIGHT_ROUTE_RE = /\b([A-Z]{3})\s+\([A-Z]{2}\d{1,4}\)\s+to\s+([A-Z]{3})\b/i;

function isFlightEvent(event) {
  const text = `${event.summary || ''} ${event.description || ''}`.toLowerCase();
  return AIRLINE_KEYWORDS.some((kw) => text.includes(kw)) || FLIGHT_NUMBER_RE.test(event.summary || '');
}

function parseRoute(event) {
  const text = `${event.summary || ''} ${event.description || ''}`;
  const m = ROUTE_RE.exec(text) || PARENS_ROUTE_RE.exec(text) || INLINE_FLIGHT_ROUTE_RE.exec(text);
  if (m) return { origin: m[1].toUpperCase(), destination: m[2].toUpperCase() };
  return null;
}

function parseEventTime(event) {
  const raw = event.start?.dateTime || event.start?.date;
  const endRaw = event.end?.dateTime || event.end?.date;
  const tz = event.start?.timeZone || 'UTC';
  return {
    start: DateTime.fromISO(raw, { zone: tz }),
    end: DateTime.fromISO(endRaw, { zone: tz }),
  };
}

// ─── Timezone Delta ──────────────────────────────────────────────────────────

function tzOffsetHours(ianaZone) {
  return DateTime.now().setZone(ianaZone).offset / 60;
}

function tzDeltaHours(originTz, destTz) {
  return tzOffsetHours(destTz) - tzOffsetHours(originTz);
}

// ─── Plan Generation ─────────────────────────────────────────────────────────

/**
 * Returns the runway (days before departure) and adjustment interval.
 * Bigger shifts get longer runways.
 */
function planConfig(absDelta) {
  if (absDelta < 4) return { runwayDays: 1, shiftHrsPerDay: 1 };
  if (absDelta < 7) return { runwayDays: 2, shiftHrsPerDay: 1 };
  if (absDelta < 10) return { runwayDays: 3, shiftHrsPerDay: 1.5 };
  return { runwayDays: 5, shiftHrsPerDay: 1.5 };
}

/**
 * Generates a list of calendar event specs for a given flight.
 * Each spec has: summary, description, start (DateTime), durationMins, reminderMins
 */
function generatePlan({ origin, destination, departure, arrival, delta }) {
  const absDelta = Math.abs(delta);
  const eastward = delta > 0;
  const { runwayDays, shiftHrsPerDay } = planConfig(absDelta);
  const events = [];

  // ── Pre-departure: sleep-shift events ────────────────────────────────────
  for (let day = runwayDays; day >= 1; day--) {
    const date = departure.minus({ days: day });
    const shiftApplied = (runwayDays - day + 1) * shiftHrsPerDay;
    const direction = eastward ? 'earlier' : 'later';

    // Bedtime shift
    const normalBed = date.set({ hour: 23, minute: 0, second: 0 });
    const shiftedBed = eastward
      ? normalBed.minus({ hours: shiftApplied })
      : normalBed.plus({ hours: shiftApplied });

    events.push({
      summary: `🌙 Jetlag Prep: Bedtime shift (Day ${runwayDays - day + 1})`,
      description:
        `Shift bedtime ${shiftApplied}h ${direction} to ease into ${destination} time.\n` +
        `Target bedtime: ${shiftedBed.toFormat('h:mm a')}\n\n` +
        `Part of your jetlag plan: ${origin} → ${destination} (${delta > 0 ? '+' : ''}${delta}h shift)`,
      start: shiftedBed,
      durationMins: 15,
      reminderMins: 30,
    });

    // Morning light exposure
    const normalWake = date.set({ hour: 7, minute: 0, second: 0 });
    const shiftedWake = eastward
      ? normalWake.minus({ hours: shiftApplied })
      : normalWake.plus({ hours: shiftApplied });

    const lightNote = eastward
      ? 'Get bright light immediately on waking — helps advance your clock.'
      : 'Avoid bright light in the morning — delay your clock with evening light instead.';

    events.push({
      summary: `☀️ Jetlag Prep: Light exposure window (Day ${runwayDays - day + 1})`,
      description: `${lightNote}\n\nTarget wake: ${shiftedWake.toFormat('h:mm a')}\n\n` +
        `Part of your jetlag plan: ${origin} → ${destination}`,
      start: shiftedWake,
      durationMins: 30,
      reminderMins: 5,
    });

    // Melatonin (only for shifts >= 4h)
    if (absDelta >= 4) {
      const melTime = eastward
        ? shiftedBed.minus({ hours: 1 })
        : shiftedBed.plus({ hours: 1 });
      events.push({
        summary: `💊 Jetlag Prep: Melatonin (Day ${runwayDays - day + 1})`,
        description:
          `Take 0.5–1 mg of melatonin to support your sleep shift.\n` +
          `Timing: ${melTime.toFormat('h:mm a')} (1 hour before adjusted bedtime)\n\n` +
          `Part of your jetlag plan: ${origin} → ${destination}`,
        start: melTime,
        durationMins: 10,
        reminderMins: 10,
      });
    }
  }

  // ── Arrival day ──────────────────────────────────────────────────────────
  const arrivalLocal = arrival.setZone(airportTz(destination) || arrival.zoneName);

  // Stay awake until local bedtime
  const localBedtime = arrivalLocal.set({ hour: 22, minute: 30, second: 0 });
  if (localBedtime > arrivalLocal) {
    events.push({
      summary: `☕ Arrival: Stay awake until local bedtime`,
      description:
        `You've landed in ${destination}. Push through until ~10:30 PM local time.\n` +
        `Avoid napping longer than 20 minutes — short naps only if needed.\n` +
        `Get outside for natural light exposure as soon as possible.\n\n` +
        `Target bedtime: ${localBedtime.toFormat('h:mm a ZZZZ')}`,
      start: arrivalLocal.plus({ minutes: 30 }),
      durationMins: 15,
      reminderMins: 0,
    });
  }

  // First local bedtime
  events.push({
    summary: `🌙 Arrival Night: First local bedtime`,
    description:
      `Aim for your first full night of sleep on ${destination} schedule.\n` +
      `Take 0.5–1 mg melatonin 30 minutes before sleep if needed.\n` +
      `Keep the room dark and cool.`,
    start: localBedtime,
    durationMins: 15,
    reminderMins: 30,
  });

  // Morning light on arrival+1
  const morningAfter = localBedtime.plus({ days: 1 }).set({ hour: 7, minute: 0, second: 0 });
  const lightInstr = eastward
    ? 'Get bright natural light as early as possible — this anchors your new clock.'
    : 'Morning light is fine. Focus on avoiding light in the evening to delay your rhythm.';

  events.push({
    summary: `☀️ Day After Arrival: Morning light`,
    description: `${lightInstr}\n\n` +
      `Aim to be outside within 30 minutes of waking.\n` +
      `Part of your jetlag plan: ${origin} → ${destination}`,
    start: morningAfter,
    durationMins: 30,
    reminderMins: 15,
  });

  // Recovery check-in (day 2 post-arrival)
  const day2 = morningAfter.plus({ days: 1 });
  events.push({
    summary: `✅ Jetlag Check-In: Day 2 in ${destination}`,
    description:
      `How are you feeling? By now most travelers with a ${absDelta}h shift feel ~60–70% adjusted.\n\n` +
      `Tips if still struggling:\n` +
      `• Continue melatonin at local bedtime for 2–3 more nights\n` +
      `• Eat meals on local time — meal timing reinforces circadian rhythm\n` +
      `• Avoid caffeine after 2 PM local time\n` +
      `• Prioritize morning light exposure`,
    start: day2.set({ hour: 9, minute: 0, second: 0 }),
    durationMins: 15,
    reminderMins: 0,
  });

  return events;
}

// ─── Google Calendar Helpers ─────────────────────────────────────────────────

async function fetchFlightEvents(calendar) {
  const now = DateTime.now().toISO();
  const future = DateTime.now().plus({ days: 90 }).toISO();

  let res;
  try {
    res = await calendar.events.list({
      calendarId: 'primary',
      timeMin: now,
      timeMax: future,
      singleEvents: true,
      orderBy: 'startTime',
      maxResults: 250,
    });
  } catch (err) {
    const status = err?.response?.status || err?.code;
    if (status === 401 || status === 403) {
      console.error('Auth error: your token may be expired or revoked.');
      console.error('Delete .oauth-token.json and run again to re-authorize:');
      console.error('  rm .oauth-token.json && node index.js');
    } else {
      console.error('Google Calendar API error:', err?.message || err);
    }
    process.exit(1);
  }

  return (res.data.items || []).filter(isFlightEvent);
}

async function createCalendarEvent(calendar, spec, calendarId = 'primary') {
  const end = spec.start.plus({ minutes: spec.durationMins });
  try {
    await calendar.events.insert({
      calendarId,
      resource: {
        summary: spec.summary,
        description: spec.description,
        start: { dateTime: spec.start.toISO(), timeZone: spec.start.zoneName },
        end: { dateTime: end.toISO(), timeZone: end.zoneName },
        reminders: spec.reminderMins != null
          ? {
              useDefault: false,
              overrides: [{ method: 'popup', minutes: spec.reminderMins }],
            }
          : { useDefault: true },
        colorId: '10', // sage green — distinct from other events
      },
    });
  } catch (err) {
    const status = err?.response?.status || err?.code;
    if (status === 401 || status === 403) {
      console.error('\nAuth error writing to calendar. Delete .oauth-token.json and run again.');
      process.exit(1);
    }
    console.error(`  ⚠️  Failed to create event "${spec.summary}": ${err?.message || err}`);
  }
}

async function createSummaryEvent(calendar, { origin, destination, departure, delta }) {
  const sign = delta > 0 ? '+' : '';
  const absDelta = Math.abs(delta);
  const { runwayDays } = planConfig(absDelta);
  const planStart = departure.minus({ days: runwayDays });

  await calendar.events.insert({
    calendarId: 'primary',
    resource: {
      summary: `✈️ JetLag Plan: ${origin} → ${destination}`,
      description:
        `Circadian adjustment plan auto-generated by openclaw-jetlag.\n\n` +
        `Route: ${origin} → ${destination}\n` +
        `Timezone shift: ${sign}${delta}h\n` +
        `Adjustment runway: ${runwayDays} day(s) before departure\n\n` +
        `Events in this plan:\n` +
        `• 🌙 Bedtime shifts (pre-departure)\n` +
        `• ☀️ Light exposure windows\n` +
        `${absDelta >= 4 ? '• 💊 Melatonin timing\n' : ''}` +
        `• ☕ Arrival-day strategy\n` +
        `• ✅ Recovery check-ins\n\n` +
        `Generated by openclaw-jetlag — https://github.com/chadholdorf/openclaw-jetlag`,
      start: { dateTime: planStart.toISO(), timeZone: planStart.zoneName },
      end: { dateTime: planStart.plus({ hours: 1 }).toISO(), timeZone: planStart.zoneName },
      colorId: '11', // tomato — stands out as the summary anchor
      reminders: {
        useDefault: false,
        overrides: [{ method: 'popup', minutes: 60 * 24 }], // 1 day heads-up
      },
    },
  });
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  console.log('\n🛫  openclaw-jetlag — circadian planner\n');

  validateEnv();
  const auth = await authorize();
  const calendar = google.calendar({ version: 'v3', auth });

  console.log('Scanning Google Calendar for flight events (next 90 days)...');
  const flightEvents = await fetchFlightEvents(calendar);

  if (flightEvents.length === 0) {
    console.log('No flight events found in the next 90 days.');
    console.log('Tip: Google Calendar auto-imports flights from Gmail. Make sure the Gmail account');
    console.log('     linked to this calendar has received airline confirmation emails.');
    return;
  }

  console.log(`Found ${flightEvents.length} potential flight event(s).\n`);

  let plansCreated = 0;

  for (const event of flightEvents) {
    const { start: departure, end: arrival } = parseEventTime(event);
    if (!departure.isValid || !arrival.isValid) {
      console.log(`  ⚠️  Could not parse event time for: "${event.summary}" — skipping.`);
      continue;
    }
    const route = parseRoute(event);

    if (!route) {
      console.log(`  ⚠️  Could not parse route from: "${event.summary}" — skipping.`);
      continue;
    }

    const { origin, destination } = route;
    const originTz = airportTz(origin);
    const destTz = airportTz(destination);

    if (!originTz || !destTz) {
      console.log(`  ⚠️  Unknown airport code(s): ${!originTz ? origin : ''} ${!destTz ? destination : ''} — skipping.`);
      continue;
    }

    const delta = Math.round(tzDeltaHours(originTz, destTz) * 2) / 2; // round to nearest 0.5h
    const absDelta = Math.abs(delta);

    console.log(`  ✈️  ${origin} → ${destination}  |  shift: ${delta > 0 ? '+' : ''}${delta}h`);

    if (absDelta < 2) {
      console.log(`      Timezone difference is under 2 hours — no plan needed.\n`);
      continue;
    }

    console.log(`      Generating ${planConfig(absDelta).runwayDays}-day adjustment plan...`);

    const planEvents = generatePlan({ origin, destination, departure, arrival, delta });

    for (const spec of planEvents) {
      await createCalendarEvent(calendar, spec);
    }

    await createSummaryEvent(calendar, { origin, destination, departure, delta });

    console.log(`      ✅ Created ${planEvents.length + 1} events for ${origin} → ${destination}\n`);
    plansCreated++;
  }

  if (plansCreated > 0) {
    console.log(`\n🎉 Done! ${plansCreated} jetlag plan(s) added to your Google Calendar.`);
    console.log('   Open Google Calendar to review your adjustment schedule.\n');
  } else {
    console.log('\nNo plans were created. Possible reasons (see warnings above):');
    console.log('  • Unrecognized airport code — add it to the AIRPORT_TZ map in index.js');
    console.log('  • Timezone shift under 2 hours — short hops are intentionally skipped');
    console.log('  • Route not parsed — event title needs a pattern like "SFO → JFK" or "SFO-JFK"\n');
  }
}

main().catch((err) => {
  console.error('\nFatal error:', err.message || err);
  process.exit(1);
});
