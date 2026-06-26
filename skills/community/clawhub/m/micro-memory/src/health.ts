// Micro Memory - Health Report System

import { Memory, HealthReport } from './types';
import { printColored, daysBetween } from './utils';

export function generateHealthReport(memories: Memory[]): HealthReport {
  if (memories.length === 0) {
    return {
      total: 0,
      byTag: {},
      byType: {},
      strengthDistribution: {},
      criticalCount: 0,
      avgStrength: 0,
      healthScore: 100,
      suggestions: ['Start adding memories to build your knowledge base!'],
    };
  }

  const byTag: Record<string, number> = {};
  const byType: Record<string, number> = {};
  const strengthDistribution: Record<string, number> = {};
  let totalStrength = 0;
  let criticalCount = 0;

  for (const memory of memories) {
    // Count by tag
    if (memory.tag) {
      byTag[memory.tag] = (byTag[memory.tag] || 0) + 1;
    }

    // Count by type
    const type = memory.type || 'unknown';
    byType[type] = (byType[type] || 0) + 1;

    // Strength distribution
    const level = memory.strength.level;
    strengthDistribution[level] = (strengthDistribution[level] || 0) + 1;
    
    // 防御性检查：确保 strength.score 是有效数字
    const score = memory.strength.score;
    const validScore = (score !== null && score !== undefined && !isNaN(score)) ? score : 0;
    totalStrength += validScore;

    // Critical memories
    if (level === 'critical') {
      criticalCount++;
    }
  }

  const avgStrength = memories.length > 0 ? totalStrength / memories.length : 0;
  
  // Calculate health score
  let healthScore = 100;
  healthScore -= criticalCount * 5; // -5 for each critical memory
  healthScore -= (strengthDistribution['weak'] || 0) * 2; // -2 for each weak memory
  healthScore = Math.max(0, Math.min(100, healthScore));

  // Generate suggestions
  const suggestions: string[] = [];
  
  if (criticalCount > 0) {
    suggestions.push(`🚨 ${criticalCount} memories are in critical state. Review them immediately!`);
  }
  
  if ((strengthDistribution['weak'] || 0) > memories.length * 0.2) {
    suggestions.push('⚠️ More than 20% of memories are weak. Consider a review session.');
  }
  
  if (avgStrength < 40) {
    suggestions.push('📉 Average strength is low. Regular reviews will help strengthen memories.');
  }
  
  if (Object.keys(byTag).length === 0) {
    suggestions.push('🏷️ Consider adding tags to organize your memories better.');
  }
  
  if (memories.length > 100 && !suggestions.some(s => s.includes('20%'))) {
    suggestions.push('✨ Your memory base is growing! Consider archiving old memories.');
  }

  if (suggestions.length === 0) {
    suggestions.push('✅ Your memory system is healthy! Keep up the good work.');
  }

  return {
    total: memories.length,
    byTag,
    byType,
    strengthDistribution,
    criticalCount,
    avgStrength,
    healthScore,
    suggestions,
  };
}

export function printHealthReport(report: HealthReport): void {
  console.log('\n🏥 Memory Health Report\n');
  
  // Overall score
  const scoreColor = report.healthScore >= 80 ? 'green' : 
                     report.healthScore >= 60 ? 'yellow' : 'red';
  printColored(`Health Score: ${report.healthScore}/100`, scoreColor);
  console.log();

  // Basic stats
  console.log(`Total Memories: ${report.total}`);
  console.log(`Average Strength: ${report.avgStrength.toFixed(1)}`);
  console.log(`Critical Memories: ${report.criticalCount}`);
  console.log();

  // Strength distribution
  console.log('Strength Distribution:');
  const levels = ['permanent', 'strong', 'stable', 'weak', 'critical'];
  const emojis = ['💎', '💪', '📊', '⚠️', '🔴'];
  
  for (let i = 0; i < levels.length; i++) {
    const count = report.strengthDistribution[levels[i]] || 0;
    const percentage = report.total > 0 ? (count / report.total * 100).toFixed(1) : '0.0';
    const bar = '█'.repeat(Math.floor(parseFloat(percentage) / 5));
    console.log(`  ${emojis[i]} ${levels[i].padEnd(10)} ${bar.padEnd(20)} ${count} (${percentage}%)`);
  }
  console.log();

  // Tags
  if (Object.keys(report.byTag).length > 0) {
    console.log('By Tag:');
    for (const [tag, count] of Object.entries(report.byTag)) {
      console.log(`  #${tag}: ${count}`);
    }
    console.log();
  }

  // Suggestions
  console.log('Suggestions:');
  for (const suggestion of report.suggestions) {
    console.log(`  ${suggestion}`);
  }
  console.log();
}

export function healthCommand(memories: Memory[]): void {
  const report = generateHealthReport(memories);
  printHealthReport(report);
}
