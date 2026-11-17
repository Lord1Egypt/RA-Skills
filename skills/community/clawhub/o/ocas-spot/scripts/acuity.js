#!/usr/bin/env node
/**
 * Acuity Scheduling availability checker — public REST API, no auth required.
 * Usage: node acuity.js <owner> <appointmentTypeId> <calendarId> <month YYYY-MM> [timezone]
 *
 * Find params: owner from booking URL or window.Acuity.business.owner,
 * appointmentTypeId from service selection URL, calendarId from provider dropdown.
 */
const https = require('https');

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse failed: ${data.slice(0, 200)}`)); }
      });
    }).on('error', reject);
  });
}

async function checkMonthlyAvailability(owner, appointmentTypeId, calendarId, month, timezone = 'America/Los_Angeles') {
  const tz = encodeURIComponent(timezone);
  const url = `https://app.acuityscheduling.com/api/scheduling/v1/availability/month` +
    `?owner=${owner}&appointmentTypeId=${appointmentTypeId}&calendarId=${calendarId}` +
    `&timezone=${tz}&month=${month}`;
  return fetchJson(url);
}

async function main() {
  const [,, owner, aptTypeId, calendarId, month, tz] = process.argv;
  if (!owner || !aptTypeId || !calendarId || !month) {
    console.error('Usage: acuity.js <owner> <appointmentTypeId> <calendarId> <month YYYY-MM> [timezone]');
    process.exit(1);
  }
  const monthly = await checkMonthlyAvailability(owner, aptTypeId, calendarId, month, tz);
  const availableDates = Object.entries(monthly)
    .filter(([, v]) => v)
    .map(([d]) => d);
  console.log(JSON.stringify({ month, availableDates, totalAvailable: availableDates.length }, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
