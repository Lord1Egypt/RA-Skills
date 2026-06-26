#!/usr/bin/env node
/**
 * PRD 质量自动评分系统
 *
 * 用法：
 *   node score.js              # 评分当前目录的PRD
 *   node score.js <项目目录>   # 评分指定项目
 *   node score.js --html       # 生成HTML评分报告
 */

const fs = require('fs');
const path = require('path');

// 评分维度配置
const DIMENSIONS = {
  completeness: {
    name: '内容完整性',
    weight: 30,
    description: '必需章节是否齐全，内容是否充实'
  },
  structure: {
    name: '结构规范性',
    weight: 25,
    description: '章节组织是否合理，逻辑是否清晰'
  },
  clarity: {
    name: '表达清晰度',
    weight: 20,
    description: '文字表述是否准确，图表是否清晰'
  },
  feasibility: {
    name: '技术可行性',
    weight: 15,
    description: '技术方案是否可行，风险是否评估'
  },
  detail: {
    name: '细节精确度',
    weight: 10,
    description: '边界情况、异常处理是否考虑全面'
  }
};

// 必需章节列表
const REQUIRED_CHAPTERS = [
  { file: '00-cover.html', name: '封面', minLength: 100 },
  { file: '02-overview.html', name: '项目概述', minLength: 500 },
  { file: '03-requirements.html', name: '需求列表', minLength: 800 },
  { file: '05-functional.html', name: '功能规格', minLength: 1500 },
  { file: '07-data.html', name: '数据模型', minLength: 600 }
];

// 可选章节
const OPTIONAL_CHAPTERS = [
  { file: '09-market.html', name: '市场分析', weight: 0.8 },
  { file: '10-architecture.html', name: '架构设计', weight: 0.9 },
  { file: '12-tech.html', name: '技术方案', weight: 0.9 },
  { file: '13-testing.html', name: '测试方案', weight: 0.8 },
  { file: '14-operation.html', name: '运营方案', weight: 0.7 }
];

class PRDScorer {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.fragmentsDir = path.join(projectDir, 'fragments');
    this.scores = {};
    this.details = {};
  }

  // 主评分函数
  score() {
    if (!fs.existsSync(this.fragmentsDir)) {
      throw new Error('找不到 fragments 目录');
    }

    // 各维度评分
    this.scoreCompleteness();
    this.scoreStructure();
    this.scoreClarity();
    this.scoreFeasibility();
    this.scoreDetail();

    // 计算总分
    const totalScore = Object.keys(DIMENSIONS).reduce((sum, key) => {
      return sum + this.scores[key] * (DIMENSIONS[key].weight / 100);
    }, 0);

    return {
      total: Math.round(totalScore),
      scores: this.scores,
      details: this.details,
      grade: this.getGrade(totalScore)
    };
  }

  // 1. 内容完整性评分
  scoreCompleteness() {
    let score = 0;
    const details = [];

    // 检查必需章节
    REQUIRED_CHAPTERS.forEach(chapter => {
      const filePath = path.join(this.fragmentsDir, chapter.file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const textContent = this.stripHtml(content);
        const length = textContent.length;

        if (length >= chapter.minLength) {
          score += 12; // 完整
          details.push(`✅ ${chapter.name}: ${length}字`);
        } else if (length >= chapter.minLength * 0.5) {
          score += 8; // 部分
          details.push(`⚠️ ${chapter.name}: ${length}字（偏少）`);
        } else {
          score += 4; // 很少
          details.push(`❌ ${chapter.name}: ${length}字（严重不足）`);
        }
      } else {
        details.push(`❌ ${chapter.name}: 缺失`);
      }
    });

    // 检查可选章节（额外加分）
    let optionalScore = 0;
    OPTIONAL_CHAPTERS.forEach(chapter => {
      const filePath = path.join(this.fragmentsDir, chapter.file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const textContent = this.stripHtml(content);
        if (textContent.length > 300) {
          optionalScore += 4 * chapter.weight;
        }
      }
    });

    score = Math.min(100, score + optionalScore);
    this.scores.completeness = Math.round(score);
    this.details.completeness = details;
  }

  // 2. 结构规范性评分
  scoreStructure() {
    let score = 60; // 基础分
    const details = [];

    // 检查功能编号规范性（F01、F02...）
    const functionalFile = path.join(this.fragmentsDir, '05-functional.html');
    if (fs.existsSync(functionalFile)) {
      const content = fs.readFileSync(functionalFile, 'utf-8');
      const fnMatches = content.match(/F\d{2,3}/g);
      if (fnMatches && fnMatches.length >= 3) {
        // 检查连续性
        const numbers = fnMatches.map(m => parseInt(m.slice(1))).sort((a, b) => a - b);
        const unique = [...new Set(numbers)];
        let continuous = true;
        for (let i = 1; i < unique.length; i++) {
          if (unique[i] - unique[i-1] > 1) {
            continuous = false;
            break;
          }
        }
        if (continuous) {
          score += 15;
          details.push(`✅ 功能编号规范且连续（共${unique.length}个）`);
        } else {
          score += 10;
          details.push(`⚠️ 功能编号不连续`);
        }
      } else {
        details.push(`❌ 缺少规范的功能编号`);
      }
    }

    // 检查流程图数量
    let flowchartCount = 0;
    REQUIRED_CHAPTERS.concat(OPTIONAL_CHAPTERS).forEach(chapter => {
      const filePath = path.join(this.fragmentsDir, chapter.file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const matches = content.match(/flowchart|sequenceDiagram|classDiagram/g);
        if (matches) flowchartCount += matches.length;
      }
    });

    if (flowchartCount >= 5) {
      score += 15;
      details.push(`✅ 流程图丰富（${flowchartCount}个）`);
    } else if (flowchartCount >= 3) {
      score += 10;
      details.push(`⚠️ 流程图数量一般（${flowchartCount}个）`);
    } else {
      details.push(`❌ 流程图不足（${flowchartCount}个）`);
    }

    // 检查表格数量
    let tableCount = 0;
    REQUIRED_CHAPTERS.concat(OPTIONAL_CHAPTERS).forEach(chapter => {
      const filePath = path.join(this.fragmentsDir, chapter.file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const matches = content.match(/<table/g);
        if (matches) tableCount += matches.length;
      }
    });

    if (tableCount >= 10) {
      score += 10;
      details.push(`✅ 表格丰富（${tableCount}个）`);
    } else if (tableCount >= 5) {
      score += 5;
      details.push(`⚠️ 表格数量一般（${tableCount}个）`);
    } else {
      details.push(`❌ 表格不足（${tableCount}个）`);
    }

    this.scores.structure = Math.min(100, score);
    this.details.structure = details;
  }

  // 3. 表达清晰度评分
  scoreClarity() {
    let score = 70;
    const details = [];

    // 检查是否有大量空白或占位符
    let placeholderCount = 0;
    let totalLength = 0;

    REQUIRED_CHAPTERS.forEach(chapter => {
      const filePath = path.join(this.fragmentsDir, chapter.file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const textContent = this.stripHtml(content);
        totalLength += textContent.length;

        // 检查占位符
        const placeholders = textContent.match(/\(待填写\)|\(待补充\)|\(TODO\)|xxx|XXXX/gi);
        if (placeholders) placeholderCount += placeholders.length;
      }
    });

    if (placeholderCount === 0) {
      score += 20;
      details.push(`✅ 无占位符，内容充实`);
    } else if (placeholderCount <= 5) {
      score += 10;
      details.push(`⚠️ 少量占位符（${placeholderCount}处）`);
    } else {
      score -= 10;
      details.push(`❌ 大量占位符（${placeholderCount}处）`);
    }

    // 检查字数
    if (totalLength > 8000) {
      score += 10;
      details.push(`✅ 总字数充足（${totalLength}字）`);
    } else if (totalLength > 5000) {
      details.push(`⚠️ 总字数一般（${totalLength}字）`);
    } else {
      score -= 5;
      details.push(`❌ 总字数偏少（${totalLength}字）`);
    }

    this.scores.clarity = Math.min(100, Math.max(0, score));
    this.details.clarity = details;
  }

  // 4. 技术可行性评分
  scoreFeasibility() {
    let score = 50;
    const details = [];

    // 检查技术方案章节
    const techFile = path.join(this.fragmentsDir, '12-tech.html');
    if (fs.existsSync(techFile)) {
      const content = fs.readFileSync(techFile, 'utf-8');
      const textContent = this.stripHtml(content);

      // 检查技术栈描述
      if (/前端|后端|数据库|架构|接口|部署/i.test(textContent)) {
        score += 20;
        details.push(`✅ 技术方案完整`);
      } else {
        details.push(`⚠️ 技术方案较简略`);
      }

      // 检查是否有架构图
      if (/flowchart|graph|diagram/i.test(content)) {
        score += 15;
        details.push(`✅ 包含架构图`);
      } else {
        details.push(`⚠️ 缺少架构图`);
      }

      // 检查接口定义
      if (/GET|POST|PUT|DELETE|\/api\//i.test(content)) {
        score += 15;
        details.push(`✅ 包含接口定义`);
      } else {
        details.push(`⚠️ 缺少接口定义`);
      }
    } else {
      details.push(`❌ 缺少技术方案章节`);
    }

    this.scores.feasibility = Math.min(100, score);
    this.details.feasibility = details;
  }

  // 5. 细节精确度评分
  scoreDetail() {
    let score = 50;
    const details = [];

    // 检查测试用例
    const testFile = path.join(this.fragmentsDir, '13-testing.html');
    if (fs.existsSync(testFile)) {
      const content = fs.readFileSync(testFile, 'utf-8');
      const textContent = this.stripHtml(content);

      // 检查测试用例数量
      const tcMatches = textContent.match(/TC-\d+|测试用例|前置条件|预期结果/g);
      if (tcMatches && tcMatches.length >= 6) {
        score += 25;
        details.push(`✅ 测试用例完整`);
      } else {
        details.push(`⚠️ 测试用例较少`);
      }

      // 检查是否包含异常场景
      if (/异常|错误|失败|边界/i.test(textContent)) {
        score += 15;
        details.push(`✅ 考虑异常场景`);
      } else {
        details.push(`⚠️ 缺少异常场景`);
      }
    } else {
      details.push(`❌ 缺少测试方案`);
    }

    // 检查数据埋点
    const dataFile = path.join(this.fragmentsDir, '07-data.html');
    if (fs.existsSync(dataFile)) {
      const content = fs.readFileSync(dataFile, 'utf-8');
      if (/埋点|事件|track|event/i.test(content)) {
        score += 10;
        details.push(`✅ 包含数据埋点`);
      } else {
        details.push(`⚠️ 缺少数据埋点`);
      }
    }

    this.scores.detail = Math.min(100, score);
    this.details.detail = details;
  }

  // 获取等级
  getGrade(score) {
    if (score >= 90) return { level: 'A', label: '优秀', emoji: '🏆' };
    if (score >= 80) return { level: 'B', label: '良好', emoji: '✨' };
    if (score >= 70) return { level: 'C', label: '合格', emoji: '👍' };
    if (score >= 60) return { level: 'D', label: '待改进', emoji: '⚠️' };
    return { level: 'E', label: '需重构', emoji: '❌' };
  }

  // 去除HTML标签
  stripHtml(html) {
    return html.replace(/<[^\u003e]*>/g, ' ').replace(/\s+/g, ' ').trim();
  }
}

// 生成雷达图（ASCII）
function generateRadarChart(scores) {
  const keys = Object.keys(DIMENSIONS);
  const values = keys.map(k => scores[k]);
  const maxVal = 100;

  // 简化的ASCII雷达图
  const size = 20;
  const center = size / 2;
  const radius = center - 2;

  let chart = [];
  chart.push('    表达清晰度');
  chart.push('        ↑');

  for (let y = 0; y < size; y++) {
    let row = '';
    for (let x = 0; x < size * 2; x++) {
      // 这里简化处理，实际应该计算极坐标
      if (x === 0 && y === center) row += '技术可行性';
      else if (x === size * 2 - 8 && y === center) row += '内容完整性';
      else if (x === center && y === size - 1) row += '结构规范性';
      else row += ' ';
    }
    if (row.trim()) chart.push(row);
  }

  chart.push('        ↓');
  chart.push('    细节精确度');

  return chart.join('\n');
}

// 生成进度条
function progressBar(value, max = 100, width = 30) {
  const filled = Math.round((value / max) * width);
  const empty = width - filled;
  return '█'.repeat(filled) + '░'.repeat(empty) + ` ${value}/${max}`;
}

// 生成改进建议
function generateSuggestions(scores, details) {
  const suggestions = [];

  if (scores.completeness < 80) {
    suggestions.push('【内容完整性】补充缺失章节，确保必需内容（项目概述、需求列表、功能规格）齐全');
  }
  if (scores.structure < 80) {
    suggestions.push('【结构规范性】规范功能编号（F01、F02...），增加流程图和表格数量');
  }
  if (scores.clarity < 80) {
    suggestions.push('【表达清晰度】填充占位符，扩充内容描述，增加实际案例');
  }
  if (scores.feasibility < 80) {
    suggestions.push('【技术可行性】补充技术方案，添加架构图和接口定义');
  }
  if (scores.detail < 80) {
    suggestions.push('【细节精确度】增加测试用例，补充异常场景和数据埋点');
  }

  return suggestions;
}

// 生成HTML报告
function generateHtmlReport(result, projectName) {
  const { total, scores, details, grade } = result;

  const radarData = Object.keys(DIMENSIONS).map(key => ({
    name: DIMENSIONS[key].name,
    value: scores[key]
  }));

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>PRD质量评估报告 - ${projectName}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f5f7fa;
      padding: 40px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      padding: 40px;
    }
    h1 { color: #1a1a2e; margin-bottom: 8px; }
    .subtitle { color: #666; margin-bottom: 30px; }
    .score-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 12px;
      padding: 30px;
      text-align: center;
      margin-bottom: 30px;
    }
    .score-number {
      font-size: 72px;
      font-weight: bold;
      line-height: 1;
    }
    .score-grade {
      font-size: 24px;
      margin-top: 10px;
    }
    .radar-container {
      max-width: 400px;
      margin: 30px auto;
    }
    .dimension-list {
      margin-top: 30px;
    }
    .dimension-item {
      display: flex;
      align-items: center;
      padding: 15px;
      margin-bottom: 10px;
      background: #f8f9fa;
      border-radius: 8px;
    }
    .dimension-name {
      width: 120px;
      font-weight: 500;
    }
    .dimension-bar {
      flex: 1;
      height: 8px;
      background: #e9ecef;
      border-radius: 4px;
      margin: 0 15px;
      overflow: hidden;
    }
    .dimension-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.5s ease;
    }
    .dimension-score {
      width: 50px;
      text-align: right;
      font-weight: bold;
    }
    .suggestions {
      margin-top: 30px;
      padding: 20px;
      background: #fff3cd;
      border-radius: 8px;
      border-left: 4px solid #ffc107;
    }
    .suggestions h3 { margin-bottom: 15px; color: #856404; }
    .suggestions li {
      margin-bottom: 8px;
      color: #856404;
    }
    .footer {
      text-align: center;
      margin-top: 30px;
      color: #999;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>📊 PRD 质量评估报告</h1>
    <p class="subtitle">项目名称: ${projectName} | 评估时间: ${new Date().toLocaleString('zh-CN')}</p>

    <div class="score-card">
      <div class="score-number">${total}</div>
      <div class="score-grade">${grade.emoji} ${grade.label} (${grade.level}级)</div>
    </div>

    <div class="radar-container">
      <canvas id="radarChart"></canvas>
    </div>

    <div class="dimension-list">
      ${radarData.map(d => `
        <div class="dimension-item">
          <div class="dimension-name">${d.name}</div>
          <div class="dimension-bar">
            <div class="dimension-fill" style="width: ${d.value}%; background: ${d.value >= 80 ? '#28a745' : d.value >= 60 ? '#ffc107' : '#dc3545'}"></div>
          </div>
          <div class="dimension-score">${d.value}</div>
        </div>
      `).join('')}
    </div>

    <div class="suggestions">
      <h3>💡 改进建议</h3>
      <ul>
        ${generateSuggestions(scores, details).map(s => `<li>${s}</li>`).join('') || '<li>文档质量良好，继续保持！</li>'}
      </ul>
    </div>

    <div class="footer">
      PRD FullStack 自动评分系统 v1.0.0
    </div>
  </div>

  <script>
    const ctx = document.getElementById('radarChart').getContext('2d');
    new Chart(ctx, {
      type: 'radar',
      data: {
        labels: ${JSON.stringify(radarData.map(d => d.name))},
        datasets: [{
          label: '得分',
          data: ${JSON.stringify(radarData.map(d => d.value))},
          backgroundColor: 'rgba(102, 126, 234, 0.2)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(102, 126, 234, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(102, 126, 234, 1)'
        }]
      },
      options: {
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            ticks: {
              stepSize: 20
            }
          }
        },
        plugins: {
          legend: {
            display: false
          }
        }
      }
    });
  </script>
</body>
</html>`;
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const generateHtml = args.includes('--html');
  const projectDir = args.find(arg => !arg.startsWith('--')) || '.';

  try {
    const scorer = new PRDScorer(projectDir);
    const result = scorer.score();

    // 获取项目名
    const versionPath = path.join(projectDir, 'version.json');
    let projectName = '未知项目';
    if (fs.existsSync(versionPath)) {
      const version = JSON.parse(fs.readFileSync(versionPath, 'utf-8'));
      projectName = version.productName || version.title || '未知项目';
    }

    // 控制台输出
    console.log('');
    console.log('╔════════════════════════════════════════════════╗');
    console.log('║         📊 PRD 质量评估报告                    ║');
    console.log('╠════════════════════════════════════════════════╣');
    console.log(`║  项目: ${projectName.padEnd(39)}║`);
    console.log(`║  时间: ${new Date().toLocaleString('zh-CN').padEnd(39)}║`);
    console.log('╠════════════════════════════════════════════════╣');
    console.log(`║  总评分: ${result.total}/100 ${result.grade.emoji} ${result.grade.label.padEnd(25)}║`);
    console.log('╠════════════════════════════════════════════════╣');

    // 各维度得分
    Object.keys(DIMENSIONS).forEach(key => {
      const dim = DIMENSIONS[key];
      const score = result.scores[key];
      const bar = progressBar(score, 100, 20);
      console.log(`║  ${dim.name.slice(0, 10).padEnd(10)} ${bar} ║`);
    });

    console.log('╚════════════════════════════════════════════════╝');
    console.log('');

    // 详细说明
    console.log('📋 详细评分:');
    Object.keys(DIMENSIONS).forEach(key => {
      console.log(`\n${DIMENSIONS[key].name} (${result.scores[key]}分):`);
      result.details[key].forEach(detail => {
        console.log(`  ${detail}`);
      });
    });

    // 改进建议
    const suggestions = generateSuggestions(result.scores, result.details);
    if (suggestions.length > 0) {
      console.log('\n💡 改进建议:');
      suggestions.forEach(s => console.log(`  • ${s}`));
    } else {
      console.log('\n✨ 文档质量优秀，无需改进！');
    }

    // 生成HTML报告
    if (generateHtml) {
      const html = generateHtmlReport(result, projectName);
      const outputPath = path.join(projectDir, 'output', `score-report-${Date.now()}.html`);

      // 确保output目录存在
      const outputDir = path.dirname(outputPath);
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      fs.writeFileSync(outputPath, html);
      console.log(`\n📄 HTML报告已生成: ${outputPath}`);
    }

    console.log('');

  } catch (error) {
    console.error('❌ 评分失败:', error.message);
    process.exit(1);
  }
}

main();
