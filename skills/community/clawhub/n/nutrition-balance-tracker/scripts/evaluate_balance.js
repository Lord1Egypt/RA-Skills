#!/usr/bin/env node
const fs = require('fs');

function round(n, d = 1) {
  const p = Math.pow(10, d);
  return Math.round(n * p) / p;
}

function statusAgainstRange(value, range, kind = 'range') {
  if (kind === 'max') return value <= range.max ? 'good' : (value <= range.max * 1.2 ? 'slightly_high' : 'high');
  if (kind === 'min') return value >= range.min ? 'good' : (value >= range.min * 0.85 ? 'slightly_low' : 'low');
  if (value < range.min) return value >= range.min * 0.85 ? 'slightly_low' : 'low';
  if (value > range.max) return value <= range.max * 1.15 ? 'slightly_high' : 'high';
  return 'good';
}

function energyStatus(goal, net, targetCalories, totalBurn) {
  const delta = round(targetCalories - totalBurn, 0);
  const diff = round(net - delta, 0);
  const abs = Math.abs(diff);
  if (goal === 'maintain') {
    if (abs <= 150) return 'within_target';
    if (abs <= 300) return 'slightly_off';
    return diff > 0 ? 'too_high' : 'too_low';
  }
  if (goal === 'fat_loss') {
    if (abs <= 100) return 'within_target_deficit';
    return diff > 0 ? 'deficit_too_small' : 'deficit_too_large';
  }
  if (abs <= 100) return 'within_target_surplus';
  return diff > 0 ? 'surplus_too_large' : 'surplus_too_small';
}

function evaluate(input) {
  const targets = input.targets;
  const intake = input.intake || input.intake_totals || {};
  const burn = input.burn || { total_burn_kcal: input.total_burn_kcal || 0 };
  const goal = input.goal_type || 'maintain';

  const net = round((intake.calories || 0) - (burn.total_burn_kcal || 0), 0);
  const status = {
    overall: 'good',
    energy: energyStatus(goal, net, targets.target_calories_kcal, burn.total_burn_kcal),
    protein: statusAgainstRange(intake.protein || 0, targets.protein_target_range),
    fat: statusAgainstRange(intake.fat || 0, targets.fat_target_range),
    carbs: statusAgainstRange(intake.carbs || 0, targets.carb_target_range),
    fiber: statusAgainstRange(intake.fiber || 0, { min: targets.fiber_target_g }, 'min'),
    water: statusAgainstRange(intake.water_ml || 0, { min: targets.water_target_ml }, 'min'),
    sodium: statusAgainstRange(intake.sodium_mg || 0, { max: targets.sodium_limit_mg }, 'max'),
    sugar: statusAgainstRange(intake.sugar || 0, { max: targets.sugar_limit_g }, 'max'),
  };

  const nonGood = Object.entries(status).filter(([k, v]) => k !== 'overall' && v !== 'good');
  if (nonGood.length >= 4) status.overall = 'poor';
  else if (nonGood.length >= 2) status.overall = 'warning';

  const gaps = [
    { metric: 'protein_g', gap: round((intake.protein || 0) - targets.protein_target_g, 1) },
    { metric: 'fat_g', gap: round((intake.fat || 0) - targets.fat_target_g, 1) },
    { metric: 'carb_g', gap: round((intake.carbs || 0) - targets.carb_target_g, 1) },
    { metric: 'fiber_g', gap: round((intake.fiber || 0) - targets.fiber_target_g, 1) },
    { metric: 'water_ml', gap: round((intake.water_ml || 0) - targets.water_target_ml, 1) },
    { metric: 'sodium_mg', gap: round((intake.sodium_mg || 0) - targets.sodium_limit_mg, 1) },
    { metric: 'sugar_g', gap: round((intake.sugar || 0) - targets.sugar_limit_g, 1) },
  ];

  const alerts = [];
  if (status.energy === 'deficit_too_large') alerts.push('今日热量赤字过大，可能影响恢复和可持续性');
  if (status.energy === 'surplus_too_large') alerts.push('今日热量盈余偏大，可能增加增脂风险');
  if (status.protein === 'low') alerts.push('蛋白质摄入不足');
  if (status.fiber !== 'good') alerts.push('膳食纤维偏低');
  if (status.water !== 'good') alerts.push('饮水不足');
  if (status.sodium !== 'good') alerts.push('钠摄入偏高');
  if (status.sugar !== 'good') alerts.push('糖摄入偏高');

  const suggestions = [];
  if (status.protein !== 'good') suggestions.push('优先补充高蛋白食物，如鸡胸肉、鱼、蛋、豆制品或蛋白粉。');
  if (status.fiber !== 'good') suggestions.push('增加蔬菜、豆类、全谷物或水果，提高膳食纤维。');
  if (status.water !== 'good') suggestions.push('分次补水，优先把今日饮水量补到目标附近。');
  if (status.sodium !== 'good') suggestions.push('后续减少重口味酱料、汤底和加工食品。');
  if (status.energy === 'deficit_too_large') suggestions.push('若不是刻意激进减脂，可适度补充碳水和蛋白质。');
  if (status.energy === 'surplus_too_large') suggestions.push('后续餐次控制高糖高脂加餐，优先选择低能量密度食物。');
  if (!suggestions.length) suggestions.push('今天整体较平衡，继续保持当前饮食和补水节奏。');

  return {
    net_energy_kcal: net,
    balance_status: status,
    gaps,
    alerts: alerts.slice(0, 3),
    suggestions: suggestions.slice(0, 3),
  };
}

function main() {
  const raw = fs.readFileSync(0, 'utf8');
  const input = JSON.parse(raw || '{}');
  process.stdout.write(JSON.stringify(evaluate(input), null, 2));
}

if (require.main === module) main();
module.exports = { evaluate, statusAgainstRange, energyStatus };
