#!/usr/bin/env node
/**
 * Fetch both calendars and extract training + content dev data.
 * 
 * USAGE: node calendar-fetch.js [--date 2026-03-18]
 * Defaults to today (SGT) if no date provided.
 * 
 * CALENDARS:
 *   1. Training Calendar (TMS) → Training Hours (source of truth)
 *   2. Outlook Calendar       → Content Dev Hours (blockout periods)
 * 
 * Handles: UTC times, TZID (SGT/IST/SE Asia), VALUE=DATE all-day events, line folding
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load calendar URLs from config (falls back to example)
function loadCalendarUrls() {
  const configDir = path.join(__dirname, '..', 'config');
  const configFile = path.join(configDir, 'calendars.json');
  const exampleFile = path.join(configDir, 'calendars.json.example');
  
  const source = fs.existsSync(configFile) ? configFile : exampleFile;
  const config = JSON.parse(fs.readFileSync(source, 'utf-8'));
  
  if (!config.training || config.training.includes('YOUR_')) {
    throw new Error('Missing config/calendars.json — run: cp config/calendars.json.example config/calendars.json and add your URLs');
  }
  
  return config;
}

const { training: TRAINING_CAL_URL, outlook: OUTLOOK_CAL_URL } = loadCalendarUrls();

const CONTENT_DEV_KEYWORDS = [
  'content dev', 'content development', 'course dev', 'course development',
  'material dev', 'material development', 'module dev', 'module development',
  'blockout', 'content creation', 'curriculum', 'courseware',
];

const EXCLUDE_KEYWORDS = [
  'kt session',        // Knowledge Transfer sessions — not form-relevant
];

// Master's learning topic pool (randomized daily)
const LEARNING_TOPIC_POOL = [
  'Web3 & Cryptocurrency',
  'NFT Development',
  'Automated Trading Strategies',
  'Agentic AI Workflows',
  'OpenClaw Automation',
  'Power BI Dashboards',
  'Data Storytelling',
  'Japanese Language',
  'Prompt Engineering',
  'DeFi Protocols',
  'Machine Learning Fundamentals',
  'Corporate Training Methodologies',
  'Python for Data Analysis',
  'Cloud Infrastructure',
  'M365 Power Platform',
];

// Timezone offsets from UTC in hours
const TZ_OFFSETS = {
  'singapore standard time': 8,
  'sgt': 8,
  'asia/singapore': 8,
  'india standard time': 5.5,
  'ist': 5.5,
  'asia/kolkata': 5.5,
  'se asia standard time': 7,
  'asia/bangkok': 7,
};

function fetchCalendar(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 15000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function parseIcalDate(raw) {
  // raw format: "DTSTART:20260318T110000Z" or "DTSTART;TZID=Singapore Standard Time:20260318T170000"
  // or "DTSTART;VALUE=DATE:20251129"
  
  // Extract the timezone ID if present
  const tzidMatch = raw.match(/TZID=([^:]+):/i);
  const tzId = tzidMatch ? tzidMatch[1].trim().toLowerCase() : null;
  
  // Extract the date/time value
  const valueMatch = raw.match(/:(\d{8}T?\d{0,6}Z?)\s*$/);
  if (!valueMatch) return null;
  
  const dtStr = valueMatch[1];
  
  // VALUE=DATE format: 20251129 (all-day event, midnight local)
  if (dtStr.length === 8) {
    const y = +dtStr.substring(0, 4);
    const m = +dtStr.substring(4, 6);
    const d = +dtStr.substring(6, 8);
    const offset = tzId ? (TZ_OFFSETS[tzId] || 8) : 8; // default SGT
    return new Date(Date.UTC(y, m - 1, d, -offset, 0, 0));
  }
  
  // UTC format: 20260318T110000Z
  if (dtStr.endsWith('Z')) {
    const y = +dtStr.substring(0, 4);
    const m = +dtStr.substring(4, 6);
    const d = +dtStr.substring(6, 8);
    const H = +dtStr.substring(9, 11);
    const M = +dtStr.substring(11, 13);
    const S = +dtStr.substring(13, 15);
    return new Date(Date.UTC(y, m - 1, d, H, M, S));
  }
  
  // Local time: 20260318T170000 — convert from the specified timezone
  const y = +dtStr.substring(0, 4);
  const m = +dtStr.substring(4, 6);
  const d = +dtStr.substring(6, 8);
  const H = +dtStr.substring(9, 11);
  const M = +dtStr.substring(11, 13);
  const S = +dtStr.substring(13, 15);
  const offset = tzId ? (TZ_OFFSETS[tzId] || 8) : 8; // default SGT
  return new Date(Date.UTC(y, m - 1, d, H - offset, M, S));
}

function getField(text, name) {
  const regex = new RegExp(`^${name}(?:;[^:]*)?:(.+)$`, 'm');
  const match = text.match(regex);
  return match ? match[1].trim() : null;
}

function getFieldRaw(text, name) {
  // Return the full line including TZID for date parsing
  const regex = new RegExp(`^${name}(?:;[^:]*)?:.+$`, 'm');
  return text.match(regex)?.[0] || null;
}

function getEventsForDate(icalText, targetDate) {
  // Unfold iCal line folding (RFC 5545)
  const unfolded = icalText.replace(/\r?\n[ \t]/g, '');
  
  const [year, month, day] = targetDate.split('-').map(Number);
  const dayStartSGT = new Date(Date.UTC(year, month - 1, day, -8, 0, 0));
  const dayEndSGT = new Date(Date.UTC(year, month - 1, day + 1, -8, 0, 0));
  
  const events = [];
  const eventBlocks = unfolded.split('BEGIN:VEVENT');
  
  for (const block of eventBlocks.slice(1)) {
    const endIdx = block.indexOf('END:VEVENT');
    const eventText = block.substring(0, endIdx < 0 ? block.length : endIdx);
    
    const summary = getField(eventText, 'SUMMARY');
    if (summary?.toLowerCase().startsWith('canceled')) continue;
    
    const dtstartRaw = getFieldRaw(eventText, 'DTSTART');
    const dtendRaw = getFieldRaw(eventText, 'DTEND');
    
    if (!dtstartRaw) continue;
    
    const startDate = parseIcalDate(dtstartRaw);
    const endDate = dtendRaw ? parseIcalDate(dtendRaw) : new Date(startDate.getTime() + 3600000);
    
    if (!startDate) continue;
    
    // Check if event overlaps with target day (in SGT)
    if (startDate < dayEndSGT && endDate > dayStartSGT) {
      const actualStart = startDate < dayStartSGT ? dayStartSGT : startDate;
      const actualEnd = endDate > dayEndSGT ? dayEndSGT : endDate;
      const durationHours = Math.round((actualEnd - actualStart) / 3600000 * 100) / 100;
      
      const toSGT = (d) => {
        const sgt = new Date(d.getTime() + 8 * 3600000);
        return `${String(sgt.getUTCHours()).padStart(2, '0')}:${String(sgt.getUTCMinutes()).padStart(2, '0')}`;
      };
      
      events.push({
        title: summary || 'Untitled',
        location: getField(eventText, 'LOCATION') || '',
        description: getField(eventText, 'DESCRIPTION') || '',
        startSGT: toSGT(startDate),
        endSGT: toSGT(endDate),
        durationHours,
      });
    }
  }
  
  return events;
}

function isContentDevEvent(event) {
  const text = `${event.title} ${event.description}`.toLowerCase();
  return CONTENT_DEV_KEYWORDS.some(kw => text.includes(kw));
}

function isExcludedEvent(event) {
  const text = `${event.title} ${event.description}`.toLowerCase();
  return EXCLUDE_KEYWORDS.some(kw => text.includes(kw));
}

function isOtherWorkEvent(event, trainingEvents) {
  // Exclude content dev events
  if (isContentDevEvent(event)) return false;
  // Exclude KT sessions and other filtered events
  if (isExcludedEvent(event)) return false;
  // Exclude events that overlap with training calendar (Outlook duplicates)
  for (const te of trainingEvents) {
    if (event.startSGT === te.startSGT && event.endSGT === te.endSGT) return false;
    // Also check if times overlap significantly (>50% overlap)
    if (event.startSGT < te.endSGT && event.endSGT > te.startSGT) {
      const overlapStart = event.startSGT > te.startSGT ? event.startSGT : te.startSGT;
      const overlapEnd = event.endSGT < te.endSGT ? event.endSGT : te.endSGT;
      const overlapMins = (parseTime(overlapEnd) - parseTime(overlapStart));
      const eventMins = (parseTime(event.endSGT) - parseTime(event.startSGT));
      if (overlapMins / eventMins > 0.5) return false;
    }
  }
  return true;
}

function parseTime(hhmm) {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
}

function isKtSessionEvent(event) {
  const text = `${event.title} ${event.description}`.toLowerCase();
  return text.includes('kt session');
}

function getRandomLearningTopics(count) {
  const shuffled = [...LEARNING_TOPIC_POOL].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

function buildLearningTopic(outlookEvents) {
  const ktEvents = outlookEvents.filter(isKtSessionEvent);
  const topicCount = ktEvents.length > 0 ? 2 : 3;
  const randomTopics = getRandomLearningTopics(topicCount);
  
  if (ktEvents.length > 0) {
    const ktTitles = ktEvents.map(e => e.title);
    return [...randomTopics, ...ktTitles].join('; ');
  }
  
  return randomTopics.join(', ');
}

function extractContentDevTopic(event) {
  const desc = event.description;
  if (!desc || desc.length < 3) return event.title;
  
  let topic = desc
    .replace(/Microsoft Teams Need help\?.*/s, '')
    .replace(/Join the meeting now.*/s, '')
    .replace(/Meeting ID.*/s, '')
    .replace(/Passcode.*/s, '')
    .replace(/For organizers.*/s, '')
    .replace(/Meeting options.*/s, '')
    .replace(/________________________________.*/g, '')
    .replace(/\\n/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  
  return topic.length > 3 ? topic.substring(0, 200) : event.title;
}

function formatDateForForm(dateStr) {
  // Convert YYYY-MM-DD to M/d/yyyy for MS Forms
  const [year, month, day] = dateStr.split('-').map(Number);
  return `${month}/${day}/${year}`;
}

async function main() {
  const args = process.argv.slice(2);
  
  const nowSGT = new Date(Date.now() + 8 * 3600000);
  let targetDate = `${nowSGT.getUTCFullYear()}-${String(nowSGT.getUTCMonth() + 1).padStart(2, '0')}-${String(nowSGT.getUTCDate()).padStart(2, '0')}`;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date') targetDate = args[++i];
  }
  
  const errors = [];
  
  // Fetch training calendar (with fallback)
  let trainingEvents = [];
  try {
    const trainingIcal = await fetchCalendar(TRAINING_CAL_URL);
    trainingEvents = getEventsForDate(trainingIcal, targetDate);
  } catch (err) {
    errors.push(`Training calendar: ${err.message}`);
  }
  
  // Fetch Outlook calendar (with fallback)
  let outlookEvents = [];
  try {
    const outlookIcal = await fetchCalendar(OUTLOOK_CAL_URL);
    outlookEvents = getEventsForDate(outlookIcal, targetDate);
  } catch (err) {
    errors.push(`Outlook calendar: ${err.message}`);
  }
  
  const trainingHours = trainingEvents.reduce((sum, e) => sum + e.durationHours, 0);
  
  // Content dev = blockout events from Outlook
  const contentDevEvents = outlookEvents.filter(isContentDevEvent);
  const contentDevHours = contentDevEvents.reduce((sum, e) => sum + e.durationHours, 0);
  
  let contentDevTopic = 'NA';
  if (contentDevEvents.length > 0) {
    contentDevTopic = contentDevEvents.map(e => extractContentDevTopic(e)).join('; ');
  }
  
  // Other items = Outlook events that aren't content dev, aren't excluded, and aren't training duplicates
  const otherEvents = outlookEvents.filter(e => isOtherWorkEvent(e, trainingEvents));
  const otherParts = ['Preparation, testing, and rehearsal for my next class'];
  if (otherEvents.length > 0) {
    otherParts.push(...otherEvents.map(e => `${e.title} (${e.startSGT}-${e.endSGT})`));
  }
  const otherItems = otherParts.join('; ');
  
  // Learning hours = remaining time to make 8 hours total
  const learningHours = Math.max(0, Math.round((8 - trainingHours - contentDevHours) * 100) / 100);
  
  // Learning topic = 2-3 random topics + any KT Sessions
  const learningTopic = buildLearningTopic(outlookEvents);
  
  const result = {
    status: 'draft',
    date: formatDateForForm(targetDate),
    trainingHours: Math.round(trainingHours * 100) / 100,
    trainingEvents: trainingEvents.map(e => ({ title: e.title, time: `${e.startSGT}-${e.endSGT}`, hours: e.durationHours })),
    contentDevHours: Math.round(contentDevHours * 100) / 100,
    contentDevTopic,
    contentDevEvents: contentDevEvents.map(e => ({ title: e.title, time: `${e.startSGT}-${e.endSGT}`, hours: e.durationHours, topic: extractContentDevTopic(e) })),
    learningHours,
    learningTopic,
    otherItems,
    otherEvents: otherEvents.map(e => ({ title: e.title, time: `${e.startSGT}-${e.endSGT}`, hours: e.durationHours })),
    teamHours: '',
    teamDesc: '',
    _errors: errors.length > 0 ? errors : null,
  };
  
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { fetchCalendar, getEventsForDate, isContentDevEvent, isExcludedEvent, isOtherWorkEvent, extractContentDevTopic, parseIcalDate, buildLearningTopic };

if (require.main === module) {
  main();
}
