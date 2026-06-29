import { getGtfsFeed, getTrainsAtStation, getArrivalsMessage } from './lib/gtfs-client.js';

const PANYNJ_ALERTS_URL = 'https://www.panynj.gov/bin/portauthority/everbridge/incidents';

// Cache to avoid duplicate alerts
let lastAlerts = new Set();

// PATH line mappings
export const LINES = {
  'HOB-33': { name: 'Hoboken - 33rd St', color: '#FF9900' },
  'JSQ-33': { name: 'Journal Square - 33rd St', color: '#4D92FB' },
  'NWK-WTC': { name: 'Newark - World Trade Center', color: '#65C100' },
  'HOB-WTC': { name: 'Hoboken - World Trade Center', color: '#65C100' }
};

// Station ID mappings (GTFS stop IDs)
export const STATIONS = {
  'newark': { id: '26732', name: 'Newark' },
  'harrison': { id: '26731', name: 'Harrison' },
  'journal_square': { id: '26730', name: 'Journal Square' },
  'grove_street': { id: '26729', name: 'Grove Street' },
  'exchange_place': { id: '26728', name: 'Exchange Place' },
  'newport': { id: '26727', name: 'Newport' },
  'hoboken': { id: '26726', name: 'Hoboken' },
  'christopher_street': { id: '26725', name: 'Christopher Street' },
  'ninth_street': { id: '26724', name: '9th Street' },
  'fourteenth_street': { id: '26723', name: '14th Street' },
  'twenty_third_street': { id: '26722', name: '23rd Street' },
  'thirty_third_street': { id: '26721', name: '33rd Street' },
  'world_trade_center': { id: '26720', name: 'World Trade Center' }
};

/**
 * Fetch current PATH service alerts from PANYNJ
 */
export async function getPathAlerts() {
  try {
    const url = `${PANYNJ_ALERTS_URL}?status=All&department=Path`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'OpenClaw-PATH-Alerts/1.0',
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) throw new Error(`PANYNJ API error: ${response.status}`);
    const data = await response.json();
    return data.data || [];
  } catch (error) {
    console.error('Failed to fetch PATH alerts:', error.message);
    return [];
  }
}

/**
 * Get arrivals for a station by name
 */
export async function getStationArrivals(stationName) {
  const key = stationName.toLowerCase().replace(/[^a-z0-9]/g, '_');
  const station = STATIONS[key];
  
  if (!station) {
    throw new Error(`Unknown station: ${stationName}. Valid: ${Object.keys(STATIONS).join(', ')}`);
  }
  
  return getArrivalsMessage(station.id, station.name);
}

// Re-export GTFS functions
export { getGtfsFeed, getTrainsAtStation, getArrivalsMessage } from './lib/gtfs-client.js';

// Export everything else from original
export * from './lib/gtfs-client.js';

let lastCheck = 0;

export async function checkForNewAlerts() {
  const alerts = await getPathAlerts();
  const newAlerts = alerts.filter(alert => {
    const id = alert.id || alert.incidentId || JSON.stringify(alert);
    if (lastAlerts.has(id)) return false;
    lastAlerts.add(id);
    return true;
  });
  
  if (lastAlerts.size > 100) {
    const ids = Array.from(lastAlerts);
    lastAlerts = new Set(ids.slice(-50));
  }
  
  lastCheck = Date.now();
  return newAlerts;
}

export function formatAlert(alert) {
  const title = alert.title || alert.incidentType || 'PATH Alert';
  const desc = alert.description || alert.details || '';
  const severity = alert.severity || 'INFO';
  const lines = alert.affectedLines || [];
  
  let emoji = 'ℹ️';
  if (severity === 'CRITICAL' || severity === 'MAJOR') emoji = '🚨';
  else if (severity === 'MINOR') emoji = '⚠️';
  
  let msg = `${emoji} **${title}**\n`;
  if (lines.length > 0) msg += `📍 Lines: ${lines.join(', ')}\n`;
  if (desc) msg += `\n${desc}\n`;
  return msg;
}

export async function getAlertsMessage(lineCode = null) {
  const alerts = await getPathAlerts();
  const filtered = lineCode 
    ? alerts.filter(a => {
        const code = lineCode.toUpperCase();
        return (a.affectedLines || []).some(l => l.includes(code)) ||
               (a.title || '').toUpperCase().includes(code);
      })
    : alerts;
  
  if (filtered.length === 0) {
    const lineText = lineCode ? ` for ${lineCode}` : '';
    return `✅ No current PATH service alerts${lineText}. All lines operating normally.`;
  }
  
  const lineText = lineCode ? ` for ${lineCode}` : '';
  let msg = `🚊 **PATH Service Alerts${lineText}** (${filtered.length} active)\n\n`;
  msg += filtered.map(formatAlert).join('\n---\n\n');
  return msg;
}

export async function getServiceStatus() {
  const alerts = await getPathAlerts();
  const status = {};
  
  Object.keys(LINES).forEach(code => {
    status[code] = { status: '✅ Good Service', alerts: [] };
  });
  
  alerts.forEach(alert => {
    Object.keys(LINES).forEach(code => {
      const title = (alert.title || '').toUpperCase();
      if ((alert.affectedLines || []).some(l => l.includes(code)) || 
          title.includes(code)) {
        status[code].status = '⚠️ Delays';
        status[code].alerts.push(alert);
      }
    });
  });
  
  return status;
}

export async function getStatusMessage() {
  const status = await getServiceStatus();
  let msg = '🚊 **PATH Service Status**\n\n';
  
  Object.entries(status).forEach(([code, info]) => {
    msg += `${info.status} **${code}** - ${LINES[code].name}\n`;
  });
  
  const alerts = await getPathAlerts();
  if (alerts.length > 0) {
    msg += `\n${alerts.length} active alert(s). Use "path alerts" for details.`;
  }
  
  return msg;
}

export default {
  getPathAlerts,
  checkForNewAlerts,
  getAlertsMessage,
  getStatusMessage,
  getServiceStatus,
  getStationArrivals,
  getArrivalsMessage,
  formatAlert,
  LINES,
  STATIONS
};
