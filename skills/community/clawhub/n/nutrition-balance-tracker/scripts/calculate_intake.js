#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const db = JSON.parse(fs.readFileSync(path.join(__dirname, 'food_db.json'), 'utf8'));

const UNIT_GRAMS = {
  g: 1, gram: 1, grams: 1,
  kg: 1000,
  ml: 1,
  piece: null, slice: null, bowl: null, scoop: null,
};

function round(n, d = 1) {
  const p = Math.pow(10, d);
  return Math.round(n * p) / p;
}

function lookupFood(name) {
  if (db[name]) return { key: name, item: db[name] };
  const lowered = String(name).toLowerCase();
  for (const [key, item] of Object.entries(db)) {
    if ((item.aliases || []).some(a => a.toLowerCase() === lowered) || key.toLowerCase() === lowered) return { key, item };
  }
  return null;
}

function getWeightGrams(entry, item) {
  const unit = entry.unit || item.base_unit || 'g';
  const amount = Number(entry.amount || entry.quantity || 0);
  if (unit === 'ml') return amount;
  if (UNIT_GRAMS[unit]) return amount * UNIT_GRAMS[unit];
  if (item.grams_per_unit) return amount * item.grams_per_unit;
  return amount;
}

function nutritionFor(entry) {
  const found = lookupFood(entry.food_name || entry.name);
  if (!found) {
    return { found: false, name: entry.food_name || entry.name, estimated: true, uncertainty: 'food_not_found' };
  }
  const { key, item } = found;
  const grams = getWeightGrams(entry, item);
  const ref = item.per_100g || item.per_100ml;
  const factor = grams / 100;
  const nutrition = {};
  for (const [k, v] of Object.entries(ref)) nutrition[k] = round(v * factor, 1);
  return { found: true, name: key, grams, nutrition };
}

function sumNutrition(entries = []) {
  const totals = { calories: 0, protein: 0, fat: 0, carbs: 0, fiber: 0, water_ml: 0, sodium_mg: 0, sugar: 0 };
  const details = [];
  const missing = [];
  for (const entry of entries) {
    const res = nutritionFor(entry);
    details.push(res);
    if (!res.found) { missing.push(res.name); continue; }
    for (const key of Object.keys(totals)) totals[key] = round(totals[key] + (res.nutrition[key] || 0), 1);
  }
  return { totals, details, missing_foods: missing, confidence: entries.length ? round((entries.length - missing.length) / entries.length, 2) : 1 };
}

function main() {
  const raw = fs.readFileSync(0, 'utf8');
  const input = JSON.parse(raw || '{}');
  const foods = input.foods || input.meals || [];
  const waterEntries = input.water_logs || [];
  const res = sumNutrition(foods);
  const addedWater = waterEntries.reduce((sum, e) => sum + Number(e.water_ml || 0), 0);
  res.totals.water_ml = round(res.totals.water_ml + addedWater, 1);
  process.stdout.write(JSON.stringify(res, null, 2));
}

if (require.main === module) main();
module.exports = { lookupFood, nutritionFor, sumNutrition };
