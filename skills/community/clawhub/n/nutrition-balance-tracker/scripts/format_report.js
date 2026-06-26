#!/usr/bin/env node
const fs = require('fs');

function fmt(n, unit = '') {
  if (n === undefined || n === null || Number.isNaN(n)) return `--${unit}`;
  return `${n}${unit}`;
}

function humanStatus(s) {
  const map = {
    good: '合理', slightly_low: '略低', low: '偏低', slightly_high: '略高', high: '偏高',
    within_target: '符合目标', slightly_off: '略偏离', too_high: '偏高', too_low: '偏低',
    within_target_deficit: '赤字合理', deficit_too_small: '赤字不足', deficit_too_large: '赤字过大',
    within_target_surplus: '盈余合理', surplus_too_small: '盈余不足', surplus_too_large: '盈余过大'
  };
  return map[s] || s;
}

function formatReport(input) {
  const { date, goal_type, targets, burn, intake, evaluation, confidence = 1, missing_foods = [] } = input;
  const summary = evaluation.balance_status.overall === 'good' ? '今天整体较平衡。' : evaluation.balance_status.overall === 'warning' ? '今天有几项需要调整。' : '今天失衡项较多，建议优先修正。';
  const completeness = confidence >= 0.9 ? '较高' : confidence >= 0.7 ? '中等' : '较低';
  const goalMap = { fat_loss: '减脂', maintain: '维持', muscle_gain: '增肌' };
  return `# 营养平衡追踪结果\n\n## 今日总览\n- **日期**：${date}\n- **记录完整度**：${completeness}\n- **今日结论**：${summary}${confidence < 1 ? '（含估算）' : ''}\n- **优先目标**：${goalMap[goal_type] || goal_type}\n\n## 热量收支\n- **目标热量**：${fmt(targets.target_calories_kcal, ' kcal')}\n- **已摄入热量**：${fmt(intake.calories, ' kcal')}\n- **已消耗热量**：${fmt(burn.total_burn_kcal, ' kcal')}\n- **当前净热量**：${fmt(evaluation.net_energy_kcal, ' kcal')}\n- **热量状态**：${humanStatus(evaluation.balance_status.energy)}\n\n> 判断：当前结果按“${goalMap[goal_type] || goal_type}”目标估算。\n\n## 营养项状态\n- **蛋白质**：${humanStatus(evaluation.balance_status.protein)}（${fmt(intake.protein, 'g')} / ${fmt(targets.protein_target_g, 'g')}）\n- **碳水**：${humanStatus(evaluation.balance_status.carbs)}（${fmt(intake.carbs, 'g')} / ${fmt(targets.carb_target_g, 'g')}）\n- **脂肪**：${humanStatus(evaluation.balance_status.fat)}（${fmt(intake.fat, 'g')} / ${fmt(targets.fat_target_g, 'g')}）\n- **膳食纤维**：${humanStatus(evaluation.balance_status.fiber)}（${fmt(intake.fiber, 'g')} / ${fmt(targets.fiber_target_g, 'g')}）\n- **饮水**：${humanStatus(evaluation.balance_status.water)}（${fmt(intake.water_ml, 'ml')} / ${fmt(targets.water_target_ml, 'ml')}）\n- **钠**：${humanStatus(evaluation.balance_status.sodium)}（${fmt(intake.sodium_mg, 'mg')} / ≤${fmt(targets.sodium_limit_mg, 'mg')}）\n- **糖**：${humanStatus(evaluation.balance_status.sugar)}（${fmt(intake.sugar, 'g')} / ≤${fmt(targets.sugar_limit_g, 'g')}）\n\n> 总体评价：${summary}\n\n## 关键问题\n1. ${evaluation.alerts[0] || '暂无明显问题'}\n2. ${evaluation.alerts[1] || '继续保持当前结构'}\n3. ${evaluation.alerts[2] || '若有漏记，结论可能变化'}\n\n## 下一步建议\n- **现在先做**：${evaluation.suggestions[0] || '继续保持。'}\n- **下一餐建议**：${evaluation.suggestions[1] || evaluation.suggestions[0] || '按目标补齐缺口。'}\n- **今天收尾建议**：${evaluation.suggestions[2] || '睡前不必为追求完美而极端加餐或节食。'}\n\n## 免责声明\n- 本结果基于你提供的饮食、运动和目标信息估算，仅用于日常营养管理参考。\n- 若存在疾病、特殊饮食需求、孕期或医学减重计划，请以医生或营养师建议为准。${missing_foods.length ? `\n- 以下食物未命中内置食物库，可能影响准确度：${missing_foods.join('、')}。` : ''}`;
}

function main() {
  const raw = fs.readFileSync(0, 'utf8');
  const input = JSON.parse(raw || '{}');
  process.stdout.write(formatReport(input));
}

if (require.main === module) main();
module.exports = { formatReport, humanStatus };
