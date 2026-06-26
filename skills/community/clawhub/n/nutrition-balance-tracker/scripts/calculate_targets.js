#!/usr/bin/env node
const fs = require('fs');

function round(n, d = 1) {
  const p = Math.pow(10, d);
  return Math.round(n * p) / p;
}

function calculateBMR({ sex = 'unknown', weight_kg, height_cm, age }) {
  if (!weight_kg || !height_cm || !age) throw new Error('weight_kg, height_cm, and age are required');
  const base = 10 * weight_kg + 6.25 * height_cm - 5 * age;
  if (sex === 'male') return round(base + 5, 0);
  if (sex === 'female') return round(base - 161, 0);
  return round(base - 78, 0);
}

function getActivityMultiplier(level = 'moderate') {
  const map = { sedentary: 1.2, light: 1.375, moderate: 1.55, active: 1.725, very_active: 1.9 };
  return map[level] || map.moderate;
}

function getGoalDelta(goal = 'maintain', intensity = 'standard') {
  const deltas = {
    fat_loss: { mild: -325, standard: -500, aggressive: -700 },
    maintain: { mild: 0, standard: 0, aggressive: 0 },
    muscle_gain: { mild: 200, standard: 325, aggressive: 500 },
  };
  return (deltas[goal] || deltas.maintain)[intensity] ?? 0;
}

function getProteinPerKg(goal = 'maintain') {
  if (goal === 'fat_loss' || goal === 'muscle_gain') return 1.8;
  return 1.4;
}

function calculateTargets(profile) {
  const bmr = calculateBMR(profile);
  const tdee = round(bmr * getActivityMultiplier(profile.activity_level), 0);
  const targetCalories = tdee + getGoalDelta(profile.goal_type, profile.goal_intensity || 'standard');
  const protein = round(profile.weight_kg * getProteinPerKg(profile.goal_type), 0);
  const fat = round(Math.max(profile.weight_kg * 0.8, (targetCalories * 0.25) / 9), 0);
  const proteinCalories = protein * 4;
  const fatCalories = fat * 9;
  const remaining = Math.max(targetCalories - proteinCalories - fatCalories, 0);
  const carbs = round(remaining / 4, 0);
  const water = round(profile.weight_kg * 33, 0);
  return {
    bmr_kcal: bmr,
    target_calories_kcal: round(targetCalories, 0),
    calorie_target_range: getCalorieRange(profile.goal_type, profile.goal_intensity || 'standard', targetCalories),
    protein_target_g: protein,
    protein_target_range: { min: round(profile.weight_kg * 1.6, 0), max: round(profile.weight_kg * 2.2, 0) },
    fat_target_g: fat,
    fat_target_range: { min: round(profile.weight_kg * 0.6, 0), max: round(profile.weight_kg * 1.0, 0) },
    carb_target_g: carbs,
    carb_target_range: { min: round(carbs * 0.85, 0), max: round(carbs * 1.15, 0) },
    fiber_target_g: 30,
    water_target_ml: water,
    sodium_limit_mg: 2000,
    sugar_limit_g: 50,
  };
}

function getCalorieRange(goal, intensity, targetCalories) {
  if (goal === 'maintain') return { min: targetCalories - 150, max: targetCalories + 150 };
  if (goal === 'fat_loss') {
    const map = { mild: [250, 400], standard: [400, 600], aggressive: [600, 800] };
    const [low, high] = map[intensity] || map.standard;
    return { min: targetCalories, max: targetCalories + (high - low) };
  }
  const map = { mild: [150, 250], standard: [250, 400], aggressive: [400, 600] };
  const [low, high] = map[intensity] || map.standard;
  return { min: targetCalories - (high - low), max: targetCalories };
}

function main() {
  const raw = fs.readFileSync(0, 'utf8');
  const input = JSON.parse(raw || '{}');
  const result = calculateTargets(input);
  process.stdout.write(JSON.stringify(result, null, 2));
}

if (require.main === module) main();
module.exports = { calculateBMR, calculateTargets, getActivityMultiplier };
