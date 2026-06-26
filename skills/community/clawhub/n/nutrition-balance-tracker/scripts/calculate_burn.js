#!/usr/bin/env node
const fs = require('fs');
const { calculateBMR, getActivityMultiplier } = require('./calculate_targets');

const MET = {
  walking: { low: 2.8, moderate: 3.5, high: 4.3 },
  running: { low: 7.0, moderate: 9.8, high: 11.0 },
  cycling: { low: 4.0, moderate: 6.8, high: 8.5 },
  strength_training: { low: 3.5, moderate: 5.0, high: 6.0 },
  swimming: { low: 6.0, moderate: 8.0, high: 10.0 },
  yoga: { low: 2.5, moderate: 3.0, high: 4.0 },
};

function round(n, d = 1) {
  const p = Math.pow(10, d);
  return Math.round(n * p) / p;
}

function getExerciseBurn(exercise, weightKg) {
  const type = exercise.exercise_type || exercise.type;
  const intensity = exercise.intensity || 'moderate';
  const minutes = Number(exercise.duration_min || exercise.duration || 0);
  const met = (MET[type] && MET[type][intensity]) || 5.0;
  return round((met * 3.5 * weightKg / 200) * minutes, 0);
}

function calculateBurn(input) {
  const profile = input.profile || input.user || input;
  const exercises = input.exercises || input.exercise || [];
  const bmr = calculateBMR(profile);
  const activityBurn = round(bmr * (getActivityMultiplier(profile.activity_level) - 1), 0);
  const exerciseBurn = exercises.reduce((sum, ex) => sum + getExerciseBurn(ex, profile.weight_kg), 0);
  return {
    bmr_kcal: bmr,
    activity_burn_kcal: activityBurn,
    exercise_burn_kcal: round(exerciseBurn, 0),
    total_burn_kcal: round(bmr + activityBurn + exerciseBurn, 0),
    exercises: exercises.map(ex => ({ ...ex, estimated_burn_kcal: getExerciseBurn(ex, profile.weight_kg) }))
  };
}

function main() {
  const raw = fs.readFileSync(0, 'utf8');
  const input = JSON.parse(raw || '{}');
  process.stdout.write(JSON.stringify(calculateBurn(input), null, 2));
}

if (require.main === module) main();
module.exports = { calculateBurn, getExerciseBurn };
