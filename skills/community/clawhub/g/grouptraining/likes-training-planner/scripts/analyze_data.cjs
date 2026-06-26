#!/usr/bin/env node
/**
 * Analyze training data and generate insights
 * Usage: node analyze_data.cjs [data.json]
 *    or: cat data.json | node analyze_data.cjs
 */

const fs = require('fs');

function loadData() {
  const args = process.argv.slice(2);
  let input = '';
  
  if (args.length > 0 && fs.existsSync(args[0])) {
    input = fs.readFileSync(args[0], 'utf8');
  } else {
    // Read from stdin
    input = fs.readFileSync(0, 'utf8');
  }
  
  try {
    const parsed = JSON.parse(input);
    return parsed.activities || parsed;
  } catch (e) {
    console.error('Error: Invalid JSON input');
    process.exit(1);
  }
}

function analyze(activities) {
  // Filter valid runs
  const runs = activities.filter(a => a.run_km > 0.5 && a.run_time > 60);
  
  if (runs.length === 0) {
    return { error: 'No valid running data found' };
  }
  
  // Group by day
  const byDay = {};
  runs.forEach(run => {
    const date = new Date(run.sign_date * 1000);
    const dayKey = date.toISOString().split('T')[0];
    if (!byDay[dayKey]) {
      byDay[dayKey] = { km: 0, time: 0, count: 0, paces: [] };
    }
    byDay[dayKey].km += run.run_km;
    byDay[dayKey].time += run.run_time;
    byDay[dayKey].count++;
    byDay[dayKey].paces.push(run.run_pace);
  });
  
  const days = Object.keys(byDay).sort();
  const totalDays = days.length;
  
  // Calculate totals
  let totalKm = 0;
  let totalTime = 0;
  let totalRuns = 0;
  let allPaces = [];
  
  days.forEach(day => {
    totalKm += byDay[day].km;
    totalTime += byDay[day].time;
    totalRuns += byDay[day].count;
    allPaces.push(...byDay[day].paces);
  });
  
  // Calculate averages
  const avgPace = allPaces.reduce((a, b) => a + b, 0) / allPaces.length;
  const avgDistance = totalKm / totalRuns;
  const avgDailyKm = totalKm / totalDays;
  const frequency = totalRuns / totalDays;
  
  // Calculate pace distribution
  const pacesSorted = [...allPaces].sort((a, b) => a - b);
  const fastest = pacesSorted[0];
  const slowest = pacesSorted[pacesSorted.length - 1];
  const median = pacesSorted[Math.floor(pacesSorted.length / 2)];
  
  // Format pace (seconds to min:sec)
  const formatPace = (sec) => {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}'${s.toString().padStart(2, '0')}"`;
  };
  
  // Format time (seconds to h:mm:ss)
  const formatTime = (sec) => {
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    const s = sec % 60;
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };
  
  // Determine training characteristics
  let characteristics = [];
  if (frequency > 1.3) characteristics.push('高频次');
  else if (frequency < 0.7) characteristics.push('低频次');
  else characteristics.push('中等频次');
  
  if (avgDistance < 2.5) characteristics.push('短距离');
  else if (avgDistance > 5) characteristics.push('长距离');
  else characteristics.push('中等距离');
  
  if (avgPace > 10 * 60) characteristics.push('恢复性有氧');
  else if (avgPace > 7 * 60) characteristics.push('有氧基础');
  else if (avgPace > 5.5 * 60) characteristics.push(' tempo 节奏');
  else characteristics.push('速度训练');
  
  // Generate recommendations
  let recommendations = [];
  if (frequency > 1.5) {
    recommendations.push('保持当前高频次，适合健康维持');
  } else if (frequency < 0.5) {
    recommendations.push('建议增加运动频率，每周至少3-4次');
  }
  
  if (avgDistance < 3) {
    recommendations.push('可以适当增加单次距离，提升耐力');
  }
  
  if (avgPace > 9 * 60) {
    recommendations.push('当前配速偏慢，适合减脂和恢复');
  }
  
  return {
    period: {
      days: totalDays,
      start: days[0],
      end: days[days.length - 1]
    },
    summary: {
      totalRuns,
      totalKm: Math.round(totalKm * 100) / 100,
      totalTime: formatTime(totalTime),
      avgDailyKm: Math.round(avgDailyKm * 100) / 100,
      frequency: Math.round(frequency * 10) / 10
    },
    pace: {
      avg: formatPace(avgPace),
      fastest: formatPace(fastest),
      slowest: formatPace(slowest),
      median: formatPace(median)
    },
    distance: {
      avg: Math.round(avgDistance * 100) / 100,
      max: Math.round(Math.max(...runs.map(r => r.run_km)) * 100) / 100
    },
    characteristics: characteristics.join('、'),
    recommendations
  };
}

function main() {
  const activities = loadData();
  const analysis = analyze(activities);
  
  console.log(JSON.stringify(analysis, null, 2));
}

main();
