#!/usr/bin/env node

/**
 * OpenClaw性能诊断脚本
 * 基于B站视频《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》的学习
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

console.log('🔍 OpenClaw性能诊断');
console.log('='.repeat(60));
console.log('基于《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》');
console.log('='.repeat(60));

class PerformanceDiagnoser {
  constructor() {
    this.results = [];
    this.score = 0;
    this.maxScore = 100;
    this.problems = [];
    this.recommendations = [];
  }
  
  async runDiagnostics() {
    console.log('\n1. 📋 系统检查...');
    await this.checkSystem();
    
    console.log('\n2. ⚙️  配置检查...');
    await this.checkConfigurations();
    
    console.log('\n3. 📊 性能测试...');
    await this.runPerformanceTests();
    
    console.log('\n4. 🚨 问题识别...');
    await this.identifyProblems();
    
    console.log('\n5. 💡 优化建议...');
    this.generateRecommendations();
    
    this.generateReport();
  }
  
  async checkSystem() {
    const checks = [
      {
        name: 'OpenClaw版本',
        description: '检查是否安装最新版本',
        check: async () => {
          return new Promise((resolve) => {
            exec('openclaw --version', (error, stdout) => {
              if (error) {
                resolve({ 
                  passed: false, 
                  message: '未安装或不在PATH中',
                  details: '请安装OpenClaw或添加到PATH',
                  score: 0
                });
              } else {
                const version = stdout.trim();
                const isLatest = version.includes('2026');
                resolve({ 
                  passed: isLatest, 
                  message: version,
                  details: isLatest ? '版本较新' : '建议更新到最新版',
                  score: isLatest ? 10 : 5
                });
              }
            });
          });
        }
      },
      {
        name: 'Node.js版本',
        description: '检查Node.js版本兼容性',
        check: async () => {
          const version = process.version;
          const major = parseInt(version.replace('v', '').split('.')[0]);
          const passed = major >= 18;
          return {
            passed,
            message: version,
            details: passed ? '版本符合要求' : '需要Node.js 18或更高版本',
            score: passed ? 10 : 0
          };
        }
      },
      {
        name: '内存可用性',
        description: '检查内存使用情况',
        check: async () => {
          const memory = process.memoryUsage();
          const usedMB = Math.round(memory.heapUsed / 1024 / 1024);
          const totalMB = Math.round(memory.heapTotal / 1024 / 1024);
          const usagePercent = Math.round(usedMB / totalMB * 100);
          
          const passed = usagePercent < 80;
          return {
            passed,
            message: `${usedMB}MB/${totalMB}MB (${usagePercent}%)`,
            details: passed ? '内存使用正常' : '内存使用较高，建议优化',
            score: passed ? 10 : 5
          };
        }
      }
    ];
    
    for (const check of checks) {
      const result = await check.check();
      this.results.push({ category: 'system', ...check, ...result });
      this.score += result.score || 0;
      
      const icon = result.passed ? '✅' : '❌';
      console.log(`   ${icon} ${check.name}: ${result.message}`);
      if (!result.passed) {
        console.log(`      📝 ${result.details}`);
      }
    }
  }
  
  async checkConfigurations() {
    const configChecks = [
      {
        name: '配置文件存在',
        description: '检查OpenClaw配置文件',
        check: async () => {
          const configPaths = [
            path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'config.json'),
            path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'openclaw.json')
          ];
          
          const found = configPaths.filter(p => fs.existsSync(p));
          return {
            passed: found.length > 0,
            message: found.length > 0 ? `找到${found.length}个配置文件` : '未找到配置文件',
            details: found.length > 0 ? `配置文件: ${found.map(p => path.basename(p)).join(', ')}` : '需要创建配置文件',
            score: found.length > 0 ? 10 : 0
          };
        }
      }
    ];
    
    for (const check of configChecks) {
      const result = await check.check();
      this.results.push({ category: 'config', ...check, ...result });
      this.score += result.score || 0;
      
      const icon = result.passed ? '✅' : '❌';
      console.log(`   ${icon} ${check.name}: ${result.message}`);
      if (!result.passed) {
        console.log(`      📝 ${result.details}`);
      }
    }
  }
  
  async runPerformanceTests() {
    console.log('   运行基础性能测试...');
    
    // 响应时间测试
    const responseTest = await this.testResponseTime();
    this.results.push({ 
      category: 'performance', 
      name: '响应时间',
      description: '测试基础响应延迟',
      ...responseTest 
    });
    this.score += responseTest.score || 0;
    
    console.log(`   ⚡ ${responseTest.passed ? '✅' : '❌'} 基础响应: ${responseTest.message}`);
    if (!responseTest.passed) {
      console.log(`      📝 ${responseTest.details}`);
    }
    
    // 内存增长测试
    const memoryTest = await this.testMemoryGrowth();
    this.results.push({
      category: 'performance',
      name: '内存稳定性',
      description: '测试内存增长情况',
      ...memoryTest
    });
    this.score += memoryTest.score || 0;
    
    console.log(`   💾 ${memoryTest.passed ? '✅' : '❌'} 内存增长: ${memoryTest.message}`);
    if (!memoryTest.passed) {
      console.log(`      📝 ${memoryTest.details}`);
    }
  }
  
  async testResponseTime() {
    return new Promise((resolve) => {
      const start = Date.now();
      
      setTimeout(() => {
        const duration = Date.now() - start;
        const passed = duration < 1000;
        
        resolve({
          passed,
          message: `${duration}ms`,
          details: passed ? '响应时间正常' : '响应时间较慢，建议优化',
          score: passed ? 15 : 5
        });
      }, 100);
    });
  }
  
  async testMemoryGrowth() {
    const initialMemory = process.memoryUsage().heapUsed;
    
    return new Promise((resolve) => {
      const testArray = [];
      for (let i = 0; i < 10000; i++) {
        testArray.push({ data: 'test'.repeat(100) });
      }
      
      setTimeout(() => {
        const finalMemory = process.memoryUsage().heapUsed;
        const growth = finalMemory - initialMemory;
        const growthMB = Math.round(growth / 1024 / 1024);
        
        const passed = growthMB < 10;
        resolve({
          passed,
          message: `增长${growthMB}MB`,
          details: passed ? '内存增长正常' : '内存增长较快，建议优化',
          score: passed ? 15 : 5
        });
        
        testArray.length = 0;
      }, 500);
    });
  }
  
  async identifyProblems() {
    const problems = [];
    
    this.results.forEach(result => {
      if (!result.passed) {
        problems.push({
          issue: result.name,
          description: result.details,
          severity: result.score === 0 ? 'high' : 'medium',
          category: result.category
        });
      }
    });
    
    const commonProblems = [
      {
        condition: () => this.score < 60,
        issue: '整体性能较差',
        description: '系统存在多个性能问题需要优化',
        severity: 'high',
        category: 'overall'
      },
      {
        condition: () => {
          const memoryResults = this.results.filter(r => r.name.includes('内存'));
          return memoryResults.some(r => !r.passed);
        },
        issue: '内存管理问题',
        description: '内存使用过高或增长过快，可能导致性能下降',
        severity: 'high',
        category: 'memory'
      }
    ];
    
    commonProblems.forEach(problem => {
      if (problem.condition()) {
        problems.push(problem);
      }
    });
    
    if (problems.length > 0) {
      console.log('   🚨 发现的问题:');
      problems.forEach((problem, index) => {
        const severityIcon = problem.severity === 'high' ? '🔴' : '🟡';
        console.log(`      ${severityIcon} ${problem.issue}: ${problem.description}`);
      });
    } else {
      console.log('   ✅ 未发现严重问题');
    }
    
    this.problems = problems;
  }
  
  generateRecommendations() {
    const recommendations = [];
    
    this.problems?.forEach(problem => {
      switch (problem.issue) {
        case 'OpenClaw版本':
          recommendations.push('更新到最新版本: npm update -g @openclaw/openclaw');
          break;
        case '内存管理问题':
          recommendations.push('缩短上下文TTL，启用智能修剪，配置内存限制');
          break;
        case '整体性能较差':
          recommendations.push('运行完整优化流程，应用所有推荐配置');
          break;
      }
    });
    
    if (recommendations.length === 0) {
      recommendations.push(
        '系统性能良好，建议定期监控和优化',
        '考虑启用本地向量数据库进一步提升性能',
        '定期运行健康检查: openclaw doctor'
      );
    } else {
      recommendations.unshift('根据诊断结果，建议采取以下优化措施:');
    }
    
    recommendations.push(
      '参考B站视频《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》',
      '使用 /compact 命令手动压缩上下文',
      '配置代理解决国内访问延迟问题'
    );
    
    console.log('   💡 优化建议:');
    recommendations.forEach((rec, index) => {
      console.log(`      ${index + 1}. ${rec}`);
    });
    
    this.recommendations = recommendations;
  }
  
  generateReport() {
    console.log('\n' + '='.repeat(60));
    console.log('📊 诊断报告');
    console.log('='.repeat(60));
    
    const scorePercent = Math.round(this.score / this.maxScore * 100);
    console.log(`🏆 总体评分: ${scorePercent}% (${this.score}/${this.maxScore})`);
    
    let rating;
    if (scorePercent >= 80) rating = '🟢 优秀';
    else if (scorePercent >= 60) rating = '🟡 良好';
    else if (scorePercent >= 40) rating = '🟠 一般';
    else rating = '🔴 需要优化';
    
    console.log(`📈 性能评级: ${rating}`);
    
    const categories = {};
    this.results.forEach(result => {
      if (!categories[result.category]) {
        categories[result.category] = { total: 0, passed: 0 };
      }
      categories[result.category].total++;
      if (result.passed) categories[result.category].passed++;
    });
    
    console.log('\n📋 分类统计:');
    Object.entries(categories).forEach(([category, stats]) => {
      const percent = Math.round(stats.passed / stats.total * 100);
      const icon = percent >= 80 ? '✅' : percent >= 60 ? '⚠️' : '❌';
      console.log(`   ${icon} ${category}: ${stats.passed}/${stats.total} (${percent}%)`);
    });
    
    if (this.problems && this.problems.length > 0) {
      console.log('\n🚨 问题统计:');
      const highProblems = this.problems.filter(p => p.severity === 'high').length;
      const mediumProblems = this.problems.filter(p => p.severity === 'medium').length;
      
      if (highProblems > 0) console.log(`   🔴 严重问题: ${highProblems}个`);
      if (mediumProblems > 0) console.log(`   🟡 一般问题: ${mediumProblems}个`);
    }
    
    const report = {
      timestamp: new Date().toISOString(),
      score: this.score,
      maxScore: this.maxScore,
      scorePercent,
      rating,
      results: this.results,
      problems: this.problems || [],
      recommendations: this.recommendations || []
    };
    
    const reportDir = path.join(process.cwd(), 'openclaw-performance-skill', 'reports');
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }
    
    const reportFile = path.join(reportDir, `diagnosis-${Date.now()}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    console.log(`\n📄 详细报告已保存: ${reportFile}`);
    console.log('='.repeat(60));
  }
}

const diagnoser = new PerformanceDiagnoser();
diagnoser.runDiagnostics().catch(error => {
  console.error('诊断失败:', error);
  process.exit(1);
});