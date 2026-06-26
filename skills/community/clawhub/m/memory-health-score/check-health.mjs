#!/usr/bin/env node
/**
 * Memory Health Score Calculator
 * 计算 Agent 记忆系统健康度评分
 */

import fs from 'fs';
import path from 'path';

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.cwd();

// 评分函数
function calculateScore() {
  const score = {
    timestamp: new Date().toISOString(),
    totalScore: 0,
    grade: '',
    dimensions: {
      completeness: { score: 0, max: 30, issues: [] },
      freshness: { score: 0, max: 25, issues: [] },
      structure: { score: 0, max: 20, issues: [] },
      density: { score: 0, max: 15, issues: [] },
      consistency: { score: 0, max: 10, issues: [] }
    },
    recommendations: []
  };

  // 1. 完整性 (30分)
  const memoryPath = path.join(WORKSPACE, 'MEMORY.md');
  const indexPath = path.join(WORKSPACE, 'memory/INDEX.md');
  
  if (fs.existsSync(memoryPath) && fs.statSync(memoryPath).size > 100) {
    score.dimensions.completeness.score += 10;
  } else {
    score.dimensions.completeness.issues.push('MEMORY.md 缺失或为空');
  }

  if (fs.existsSync(indexPath)) {
    score.dimensions.completeness.score += 5;
  } else {
    score.dimensions.completeness.issues.push('INDEX.md 缺失');
  }

  // 检查近 7 天日志
  const memoryDir = path.join(WORKSPACE, 'memory');
  if (fs.existsSync(memoryDir)) {
    const files = fs.readdirSync(memoryDir);
    const dateFiles = files.filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f));
    const now = Date.now();
    const recent = dateFiles.filter(f => {
      const date = new Date(f.replace('.md', ''));
      return (now - date.getTime()) < 7 * 24 * 60 * 60 * 1000;
    });
    if (recent.length >= 3) {
      score.dimensions.completeness.score += 10;
    } else {
      score.dimensions.completeness.issues.push(`近 7 天日志不足 (${recent.length}/3)`);
    }
  }

  // P0 标记使用率
  if (fs.existsSync(memoryPath)) {
    const content = fs.readFileSync(memoryPath, 'utf-8');
    const p0Count = (content.match(/\[P0\]/g) || []).length;
    if (p0Count >= 3) {
      score.dimensions.completeness.score += 5;
    } else {
      score.dimensions.completeness.issues.push(`P0 标记不足 (${p0Count}/3)`);
    }
  }

  // 2. 新鲜度 (25分)
  const now = Date.now();
  const today = new Date().toISOString().split('T')[0];
  const todayLog = path.join(memoryDir, `${today}.md`);
  if (fs.existsSync(todayLog)) {
    score.dimensions.freshness.score += 10;
  } else {
    score.dimensions.freshness.issues.push('今日日志未创建');
  }

  if (fs.existsSync(memoryPath)) {
    const stat = fs.statSync(memoryPath);
    const daysSince = (now - stat.mtimeMs) / (24 * 60 * 60 * 1000);
    if (daysSince <= 7) {
      score.dimensions.freshness.score += 10;
    } else {
      score.dimensions.freshness.issues.push(`MEMORY.md ${Math.floor(daysSince)} 天未更新`);
    }
  }

  if (fs.existsSync(indexPath)) {
    const stat = fs.statSync(indexPath);
    const daysSince = (now - stat.mtimeMs) / (24 * 60 * 60 * 1000);
    if (daysSince <= 3) {
      score.dimensions.freshness.score += 5;
    } else {
      score.dimensions.freshness.issues.push(`INDEX.md ${Math.floor(daysSince)} 天未更新`);
    }
  }

  // 3. 结构化 (20分)
  const issuesDir = path.join(WORKSPACE, '.issues');
  if (fs.existsSync(issuesDir)) {
    score.dimensions.structure.score += 10;
    const openIssues = fs.readdirSync(issuesDir).filter(f => f.startsWith('open-'));
    if (openIssues.length >= 3) {
      score.dimensions.structure.score += 5;
    } else {
      score.dimensions.structure.issues.push(`open issue 不足 (${openIssues.length}/3)`);
    }
  } else {
    score.dimensions.structure.issues.push('.issues/ 目录缺失');
  }

  const heartbeatPath = path.join(WORKSPACE, 'HEARTBEAT.md');
  if (fs.existsSync(heartbeatPath)) {
    const content = fs.readFileSync(heartbeatPath, 'utf-8');
    if (content.includes('.issues') || content.includes('issue')) {
      score.dimensions.structure.score += 5;
    } else {
      score.dimensions.structure.issues.push('HEARTBEAT.md 未配置 issue 扫描');
    }
  }

  // 4. 密度 (15分)
  if (fs.existsSync(memoryPath)) {
    const lines = fs.readFileSync(memoryPath, 'utf-8').split('\n').length;
    if (lines >= 50 && lines <= 500) {
      score.dimensions.density.score += 10;
    } else if (lines < 50) {
      score.dimensions.density.issues.push(`MEMORY.md 过短 (${lines} 行)`);
    } else {
      score.dimensions.density.issues.push(`MEMORY.md 过长 (${lines} 行，需压缩)`);
    }
  }

  // 5. 一致性 (10分) — 简化检查
  if (fs.existsSync(memoryPath) && fs.existsSync(indexPath)) {
    score.dimensions.consistency.score += 5;
  }
  if (fs.existsSync(issuesDir) && fs.existsSync(indexPath)) {
    score.dimensions.consistency.score += 5;
  }

  // 计算总分
  score.totalScore = Object.values(score.dimensions).reduce((sum, d) => sum + d.score, 0);

  // 评级
  if (score.totalScore >= 90) score.grade = '🟢 优秀';
  else if (score.totalScore >= 70) score.grade = '🟡 良好';
  else if (score.totalScore >= 50) score.grade = '🟠 警告';
  else score.grade = '🔴 危险';

  // 生成建议
  Object.values(score.dimensions).forEach(d => {
    d.issues.forEach(issue => score.recommendations.push(issue));
  });

  return score;
}

// 主函数
const score = calculateScore();
console.log(JSON.stringify(score, null, 2));

// 保存到文件
const outputPath = path.join(WORKSPACE, 'memory/health-score.json');
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, JSON.stringify(score, null, 2));
