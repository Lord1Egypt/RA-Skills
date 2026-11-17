/**
 * classifier.js — Classify event type, geography, and affected systems
 */

const EVENT_TYPES = {
  'natural disaster': ['earthquake','flood','wildfire','fire','hurricane','typhoon','tsunami','volcano','landslide','avalanche','storm','cyclone','tornado','drought','heatwave','snowstorm','blizzard'],
  'corporate':       ['ipo','merger','acquisition','bankruptcy','layoffs','revenue','earnings','stock','shares','investor','valuation','startup','funding round','ceo','executive','quarterly results','dividend','buyback','restructuring'],
  'political':       ['election','vote','parliament','congress','senate','policy','regulation','sanctions','treaty','summit','president','prime minister','referendum','legislation','bill'],
  'conflict':        ['war','military','attack','invasion','terrorism','combat','ceasefire','troops','airstrike','missile','defense','security','insurgency','guerilla','occupation'],
  'economic':        ['recession','inflation','interest rate','gdp','trade war','tariff','currency','oil price','market crash','unemployment','central bank','bond','wage','poverty'],
  'health':          ['pandemic','outbreak','virus','disease','vaccine','healthcare','hospital','fda','who','epidemic','quarantine'],
  'climate':         ['climate change','emissions','carbon','green energy','renewable','coal','oil spill','deforestation','biodiversity'],
  'infrastructure':  ['power outage','blackout','bridge collapse','road closure','airport','train derailment','metro','pipeline','dam'],
  'technology':      ['ai','artificial intelligence','semiconductor','chip','data breach','cyberattack','big tech','antitrust','privacy'],
};

const SYSTEM_TAGS = {
  'Roads & Highways':       ['road','highway','bridge','transport','traffic','motorway','freeway'],
  'Power Grid':             ['power','electricity','outage','blackout','grid','energy'],
  'Supply Chains':          ['supply chain','shipping','port','logistics','semiconductor','chip','cargo'],
  'Markets & Finance':      ['stock','market','shares','investor','trading','nasdaq','bond','fund'],
  'Local Economy':          ['jobs','employment','businesses','economy','inflation','wages'],
  'Public Health':          ['hospital','healthcare','medical','doctors','clinics'],
  'Government Services':    ['government','public services','schools','courts'],
  'Environment':            ['air quality','water','soil','wildlife','forest','agriculture'],
  'Digital Infrastructure': ['internet','cloud','data center','telecom','5g','broadband'],
  'Travel & Tourism':        ['airport','flights','tourism','travel','hotel','airline'],
};

function classifyEvent(text) {
  const t = text.toLowerCase();
  const scores = {};
  for (const [type, tags] of Object.entries(EVENT_TYPES)) {
    scores[type] = tags.filter(tag => t.includes(tag)).length;
  }
  const top = Object.entries(scores).sort((a,b) => b[1]-a[1])[0];
  return top[1] > 0 ? top[0] : 'general news';
}

function extractLocation(text) {
  const patterns = [
    /(?:in|at|near|off the coast of)\s+([A-Z][a-zA-Z\s&'-]+?)(?:\s+(?:on|,|\.|$))/,
    /(?:country of|city of|province of|state of)\s+([A-Z][a-zA-Z\s&'-]+)/,
  ];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) return m[1].trim().slice(0, 60);
  }
  return 'Global';
}

function extractTitle(text) {
  const lines = text.split('\n').map(l=>l.trim()).filter(l=>l.length>20);
  if (!lines.length) return 'Unknown';
  return lines[0].replace(/^[""']|[""']$/g,'').slice(0,100);
}

function findAffectedSystems(text) {
  const t = text.toLowerCase();
  const found = [];
  for (const [sys, tags] of Object.entries(SYSTEM_TAGS)) {
    if (tags.some(tag => t.includes(tag))) found.push(sys);
  }
  return found.length ? found : ['General public'];
}

module.exports = { classifyEvent, extractLocation, extractTitle, findAffectedSystems };
