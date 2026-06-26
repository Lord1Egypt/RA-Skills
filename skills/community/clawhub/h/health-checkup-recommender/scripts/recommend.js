#!/usr/bin/env node
'use strict';

// Unified recommendation engine for health-checkup-recommender
// Moves risk assessment + symptom matching from LLM to deterministic code.
// Called by serve.js (OceanBus) or standalone via CLI for testing.

const fs = require('fs');
const path = require('path');
const { verifyAll } = require('./verify_items');
const { calculateTotal } = require('./calculate_prices');
let buildQRContent;
try { ({ buildQRContent } = require('./generate_qr')); } catch (_) { buildQRContent = null; }

const REF_DIR = path.join(__dirname, '..', 'reference');

let DATA = null;
function loadData() {
  if (DATA) return DATA;
  DATA = {
    items: JSON.parse(fs.readFileSync(path.join(REF_DIR, 'checkup_items.json'), 'utf-8')).items,
    riskTable: JSON.parse(fs.readFileSync(path.join(REF_DIR, 'risk_logic_table.json'), 'utf-8')),
    symptomMap: JSON.parse(fs.readFileSync(path.join(REF_DIR, 'symptom_mapping.json'), 'utf-8')),
  };
  return DATA;
}

// ── Risk assessment ──

function findAgeGroup(age) {
  if (age < 18) return '18岁以下';
  if (age <= 35) return '18-35';
  if (age <= 49) return '36-49';
  if (age <= 64) return '50-64';
  return '65+';
}

function assessRisks(age, gender) {
  const { riskTable } = loadData();
  const bucket = gender === 'female' ? (riskTable.female || riskTable['女性']) : (riskTable.male || riskTable['男性']);
  if (!bucket) return [];
  const ageGroup = findAgeGroup(age);
  const groupData = bucket[ageGroup];
  if (!groupData) return [];

  const diseases = groupData.diseases || [];
  const notes = groupData.notes || '';
  return diseases.slice(0, 3).map(disease => ({
    disease,
    explanation: notes,
    items: [], // risk items are mapped via symptom_mapping or added manually
  }));
}

// ── Symptom matching ──

function matchSymptoms(userSymptoms) {
  const { symptomMap } = loadData();
  const synonyms = symptomMap['症状同义词映射'] || {};
  const itemMap = symptomMap['症状加项映射'] || {};

  const results = [];
  const seen = new Set();
  for (const raw of userSymptoms) {
    const s = raw.trim().toLowerCase();
    if (!s) continue;
    for (const [canonical, aliases] of Object.entries(synonyms)) {
      if (seen.has(canonical)) continue;
      const match = aliases.some(a => s.includes(a.toLowerCase()) || a.toLowerCase().includes(s));
      if (match) {
        const addon = itemMap[canonical];
        if (addon && addon.addon) {
          seen.add(canonical);
          results.push({
            category: canonical,
            items: addon.addon,
            itemNames: addon.item_names || '',
            note: addon.note || '',
          });
        }
        break;
      }
    }
  }
  return results;
}

// ── Known conditions ──

function matchConditions(conditions) {
  const { symptomMap } = loadData();
  const itemMap = symptomMap['症状加项映射'] || {};
  const synonyms = symptomMap['症状同义词映射'] || {};

  const results = [];
  const seen = new Set();
  for (const raw of conditions) {
    const c = raw.trim();
    if (!c || seen.has(c)) continue;
    // Try direct lookup in item map
    if (itemMap[c] && itemMap[c].addon) {
      seen.add(c);
      results.push({ category: c, items: itemMap[c].addon });
      continue;
    }
    // Try synonym matching
    for (const [canonical, aliases] of Object.entries(synonyms)) {
      if (seen.has(canonical)) continue;
      if (aliases.some(a => c.includes(a) || a.includes(c))) {
        const addon = itemMap[canonical];
        if (addon && addon.addon) {
          seen.add(canonical);
          results.push({ category: canonical, items: addon.addon });
        }
        break;
      }
    }
  }
  return results;
}

// ── Main entry point ──

async function recommend(profile) {
  const { age, gender, symptoms = [], familyHistory = {}, knownConditions = [], consent = false } = profile;

  loadData();

  // 1. Risk assessment
  const risks = assessRisks(age, gender);

  // 2. Symptom matching
  const symptomMatches = matchSymptoms(symptoms);

  // 3. Condition matching
  const conditionMatches = matchConditions(knownConditions);

  // 4. Build item set: baseline + risk items + symptom items + condition items
  const itemSet = new Set(['HaoLa01']); // mandatory baseline
  for (const r of risks) {
    for (const id of r.items) itemSet.add(id);
  }
  for (const s of symptomMatches) {
    for (const id of s.items) itemSet.add(id);
  }
  for (const c of conditionMatches) {
    for (const id of c.items) itemSet.add(id);
  }

  const itemIds = [...itemSet];

  // 5. Verify items
  const verified = verifyAll(itemIds);

  // 6. Calculate prices (includes conflict resolution)
  const validIds = verified.results.map(r => r.id);
  const pricing = calculateTotal(validIds);

  // 7. Check minimum 600 yuan
  const meetsMinimum = pricing.total >= 600;

  // 8. QR code (only with consent and when qrcode module available)
  let qrDataUri = null;
  let bookingUrl = null;
  if (consent && buildQRContent) {
    try {
      const { ItemSyncService, ApiClient } = require('./sync_items');
      const config = require('../config/api');
      const apiClient = new ApiClient(config.baseUrl);
      const syncService = new ItemSyncService(apiClient);
      const resp = await syncService.syncItems(pricing.items.map(i => i.id));
      const welfareid = resp?.data?.welfareid || resp?.welfareid;
      const ruleid = resp?.data?.ruleid || resp?.ruleid;
      if (welfareid && ruleid) {
        bookingUrl = buildQRContent({ welfareid, ruleid });
        try {
          const QRCode = require('qrcode');
          qrDataUri = await QRCode.toDataURL(bookingUrl, {
            errorCorrectionLevel: 'M', margin: 3, width: 400,
            color: { dark: '#1a3a5c', light: '#ffffff' }
          });
        } catch (_) {}
      }
    } catch (_) {}
  }

  return {
    patient: { age, gender },
    riskAssessment: risks.map(r => ({ disease: r.disease, incidence: r.incidence, explanation: r.explanation })),
    symptomMatches: symptomMatches.map(s => ({ category: s.category, itemNames: s.itemNames, note: s.note })),
    recommendations: pricing.items.map(i => ({ id: i.id, name: i.name, price: i.price })),
    totalPrice: pricing.total,
    meetsMinimum,
    minimumNote: meetsMinimum ? null : '总价不足600元，合作体检机构有最低消费要求，建议补充项目。',
    removedItems: (pricing.removed || []).map(r => ({ id: r.id, name: r.name, reason: r.reason })),
    invalidItems: verified.errors.map(e => ({ id: e.id, hint: e.hint })),
    qrDataUri,
    bookingUrl,
    consentUsed: consent,
  };
}

// ── CLI test mode ──
if (require.main === module) {
  const testProfile = {
    age: 45,
    gender: 'male',
    symptoms: ['胸闷', '胃痛'],
    familyHistory: { cardiovascular: true },
    knownConditions: [],
    consent: false,
  };
  recommend(testProfile).then(r => {
    console.log(JSON.stringify(r, null, 2));
  }).catch(e => {
    console.error(e);
    process.exit(1);
  });
}

module.exports = { recommend, assessRisks, matchSymptoms };
