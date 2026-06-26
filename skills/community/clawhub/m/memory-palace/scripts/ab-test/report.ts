/**
 * A/B 测试报告生成脚本
 * 生成对比报告和可视化数据
 */

import { TestResult, StorageMetrics, RetrievalMetrics, PerformanceMetrics } from './run-test';
import { testMemories, testQueries, categoryStats, difficultyStats } from './test-data';

// ========== 报告类型 ==========

export interface ComparisonReport {
  metadata: ReportMetadata;
  summary: SummarySection;
  storageComparison: StorageComparison;
  retrievalComparison: RetrievalComparison;
  performanceComparison: PerformanceComparison;
  errorAnalysis: ErrorAnalysis;
  recommendations: string[];
  rawResults: {
    baseline: TestResult;
    treatment: TestResult;
  };
}

export interface ReportMetadata {
  testId: string;
  generatedAt: string;
  baselineName: string;
  treatmentName: string;
  testDuration: string;
}

export interface SummarySection {
  winner: 'baseline' | 'treatment' | 'tie';
  overallScore: {
    baseline: number;
    treatment: number;
  };
  keyFindings: string[];
  statisticalSignificance: boolean;
}

export interface StorageComparison {
  baseline: StorageMetrics;
  treatment: StorageMetrics;
  improvement: {
    successRate: number; // percentage improvement
    avgStoreTime: number; // ms improvement
  };
  chart: string; // ASCII bar chart
}

export interface RetrievalComparison {
  baseline: RetrievalMetrics;
  treatment: RetrievalMetrics;
  improvement: {
    hitRate: number;
    precisionAt5: number;
    recallAt5: number;
    keywordMatchRate: number;
  };
  byDifficulty: {
    easy: { baseline: number; treatment: number; improvement: number };
    medium: { baseline: number; treatment: number; improvement: number };
    hard: { baseline: number; treatment: number; improvement: number };
  };
  chart: string;
}

export interface PerformanceComparison {
  baseline: PerformanceMetrics;
  treatment: PerformanceMetrics;
  improvement: {
    avgQueryTime: number;
    p95QueryTime: number;
    p99QueryTime: number;
  };
  chart: string;
}

export interface ErrorAnalysis {
  baselineErrors: number;
  treatmentErrors: number;
  errorTypes: {
    storage: number;
    retrieval: number;
  };
  errorRateReduction: number;
}

// ========== 报告生成器 ==========

export class ReportGenerator {
  private baseline: TestResult;
  private treatment: TestResult;
  private baselineName: string;
  private treatmentName: string;

  constructor(
    baseline: TestResult,
    treatment: TestResult,
    options: { baselineName?: string; treatmentName?: string } = {}
  ) {
    this.baseline = baseline;
    this.treatment = treatment;
    this.baselineName = options.baselineName || 'Without Memory Palace';
    this.treatmentName = options.treatmentName || 'With Memory Palace';
  }

  /**
   * 生成完整对比报告
   */
  generateReport(): ComparisonReport {
    return {
      metadata: this.generateMetadata(),
      summary: this.generateSummary(),
      storageComparison: this.compareStorage(),
      retrievalComparison: this.compareRetrieval(),
      performanceComparison: this.comparePerformance(),
      errorAnalysis: this.analyzeErrors(),
      recommendations: this.generateRecommendations(),
      rawResults: {
        baseline: this.baseline,
        treatment: this.treatment
      }
    };
  }

  private generateMetadata(): ReportMetadata {
    const baselineTime = new Date(this.baseline.timestamp);
    const treatmentTime = new Date(this.treatment.timestamp);
    const duration = Math.abs(treatmentTime.getTime() - baselineTime.getTime());
    
    return {
      testId: this.baseline.testId,
      generatedAt: new Date().toISOString(),
      baselineName: this.baselineName,
      treatmentName: this.treatmentName,
      testDuration: this.formatDuration(duration)
    };
  }

  private generateSummary(): SummarySection {
    const storageDiff = this.treatment.storage.successRate - this.baseline.storage.successRate;
    const retrievalDiff = this.treatment.retrieval.hitRate - this.baseline.retrieval.hitRate;
    
    const baselineScore = this.calculateOverallScore(this.baseline);
    const treatmentScore = this.calculateOverallScore(this.treatment);
    
    let winner: 'baseline' | 'treatment' | 'tie' = 'tie';
    if (treatmentScore > baselineScore + 5) winner = 'treatment';
    else if (baselineScore > treatmentScore + 5) winner = 'baseline';

    const keyFindings: string[] = [];
    
    if (storageDiff > 5) {
      keyFindings.push(`存储成功率提升 ${storageDiff.toFixed(1)}%`);
    }
    if (retrievalDiff > 10) {
      keyFindings.push(`检索命中率提升 ${retrievalDiff.toFixed(1)}%`);
    }
    if (this.treatment.retrieval.keywordMatchRate - this.baseline.retrieval.keywordMatchRate > 10) {
      keyFindings.push('关键词匹配率显著提升');
    }
    if (this.baseline.performance.avgQueryTime - this.treatment.performance.avgQueryTime > 50) {
      keyFindings.push('查询响应时间优化');
    }

    return {
      winner,
      overallScore: { baseline: baselineScore, treatment: treatmentScore },
      keyFindings,
      statisticalSignificance: this.isStatisticallySignificant()
    };
  }

  private calculateOverallScore(result: TestResult): number {
    const storageScore = result.storage.successRate * 0.2;
    const retrievalScore = result.retrieval.hitRate * 0.4;
    const precisionScore = result.retrieval.precisionAt5 * 0.2;
    const performanceScore = Math.max(0, 100 - (result.performance.avgQueryTime / 10)) * 0.2;
    
    return storageScore + retrievalScore + precisionScore + performanceScore;
  }

  private compareStorage(): StorageComparison {
    return {
      baseline: this.baseline.storage,
      treatment: this.treatment.storage,
      improvement: {
        successRate: this.treatment.storage.successRate - this.baseline.storage.successRate,
        avgStoreTime: this.baseline.storage.avgStoreTime - this.treatment.storage.avgStoreTime
      },
      chart: this.generateBarChart(
        [this.baseline.storage.successRate, this.treatment.storage.successRate],
        ['Baseline', 'Treatment'],
        'Storage Success Rate (%)'
      )
    };
  }

  private compareRetrieval(): RetrievalComparison {
    const baseline = this.baseline.retrieval;
    const treatment = this.treatment.retrieval;

    return {
      baseline,
      treatment,
      improvement: {
        hitRate: treatment.hitRate - baseline.hitRate,
        precisionAt5: treatment.precisionAt5 - baseline.precisionAt5,
        recallAt5: treatment.recallAt5 - baseline.recallAt5,
        keywordMatchRate: treatment.keywordMatchRate - baseline.keywordMatchRate
      },
      byDifficulty: {
        easy: {
          baseline: baseline.easyHitRate,
          treatment: treatment.easyHitRate,
          improvement: treatment.easyHitRate - baseline.easyHitRate
        },
        medium: {
          baseline: baseline.mediumHitRate,
          treatment: treatment.mediumHitRate,
          improvement: treatment.mediumHitRate - baseline.mediumHitRate
        },
        hard: {
          baseline: baseline.hardHitRate,
          treatment: treatment.hardHitRate,
          improvement: treatment.hardHitRate - baseline.hardHitRate
        }
      },
      chart: this.generateBarChart(
        [baseline.hitRate, treatment.hitRate],
        ['Baseline', 'Treatment'],
        'Hit Rate (%)'
      )
    };
  }

  private comparePerformance(): PerformanceComparison {
    const baseline = this.baseline.performance;
    const treatment = this.treatment.performance;

    return {
      baseline,
      treatment,
      improvement: {
        avgQueryTime: baseline.avgQueryTime - treatment.avgQueryTime,
        p95QueryTime: baseline.p95QueryTime - treatment.p95QueryTime,
        p99QueryTime: baseline.p99QueryTime - treatment.p99QueryTime
      },
      chart: this.generateBarChart(
        [baseline.avgQueryTime, treatment.avgQueryTime],
        ['Baseline', 'Treatment'],
        'Avg Query Time (ms)'
      )
    };
  }

  private analyzeErrors(): ErrorAnalysis {
    const baselineErrors = this.baseline.errors.length;
    const treatmentErrors = this.treatment.errors.length;

    const baselineByType = this.groupErrors(this.baseline.errors);
    const treatmentByType = this.groupErrors(this.treatment.errors);

    const errorRateReduction = this.baseline.retrieval.totalQueries > 0
      ? ((baselineErrors - treatmentErrors) / (this.baseline.retrieval.totalQueries * 2)) * 100
      : 0;

    return {
      baselineErrors,
      treatmentErrors,
      errorTypes: {
        storage: baselineByType.storage + treatmentByType.storage,
        retrieval: baselineByType.retrieval + treatmentByType.retrieval
      },
      errorRateReduction
    };
  }

  private groupErrors(errors: { operation: string }[]): { storage: number; retrieval: number } {
    return {
      storage: errors.filter(e => e.operation === 'store').length,
      retrieval: errors.filter(e => e.operation === 'retrieve').length
    };
  }

  private generateRecommendations(): string[] {
    const recommendations: string[] = [];
    const retrieval = this.compareRetrieval();

    if (retrieval.improvement.hitRate < 10) {
      recommendations.push('建议优化向量嵌入模型，提高语义相似度匹配能力');
    }
    
    if (retrieval.byDifficulty.hard.improvement < 0) {
      recommendations.push('复杂查询表现下降，建议增加推理链或上下文增强机制');
    }

    if (this.treatment.storage.avgStoreTime > 200) {
      recommendations.push('存储延迟较高，建议考虑批量写入或异步索引');
    }

    if (this.treatment.performance.p95QueryTime > 500) {
      recommendations.push('P95 延迟较高，建议检查索引效率或增加缓存层');
    }

    const keywordDiff = this.treatment.retrieval.keywordMatchRate - this.baseline.retrieval.keywordMatchRate;
    if (keywordDiff < 5) {
      recommendations.push('关键词匹配改进有限，建议增强关键词提取和加权策略');
    }

    if (recommendations.length === 0) {
      recommendations.push('Memory Palace 整体表现良好，建议继续监控生产环境指标');
    }

    return recommendations;
  }

  private isStatisticallySignificant(): boolean {
    // 简化版统计显著性判断
    // 实际应使用 t-test 或其他统计方法
    const retrievalDiff = Math.abs(
      this.treatment.retrieval.hitRate - this.baseline.retrieval.hitRate
    );
    return retrievalDiff > 10;
  }

  // ========== 可视化工具 ==========

  private generateBarChart(values: number[], labels: string[], title: string): string {
    const maxValue = Math.max(...values);
    const barWidth = 30;
    
    let chart = `\n${title}\n${'─'.repeat(50)}\n`;
    
    values.forEach((value, i) => {
      const barLength = Math.round((value / maxValue) * barWidth);
      const bar = '█'.repeat(barLength) + '░'.repeat(barWidth - barLength);
      chart += `${labels[i].padEnd(12)} |${bar}| ${value.toFixed(1)}\n`;
    });
    
    return chart;
  }

  private formatDuration(ms: number): string {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    return `${(ms / 60000).toFixed(1)}min`;
  }

  // ========== 导出格式 ==========

  /**
   * 生成 Markdown 报告
   */
  generateMarkdown(): string {
    const report = this.generateReport();
    
    return `# A/B Test Report: Memory Palace Effectiveness

## 📋 Test Metadata

| Item | Value |
|------|-------|
| Test ID | ${report.metadata.testId} |
| Generated | ${report.metadata.generatedAt} |
| Baseline | ${report.metadata.baselineName} |
| Treatment | ${report.metadata.treatmentName} |
| Duration | ${report.metadata.testDuration} |

## 🎯 Summary

**Winner: ${report.summary.winner === 'treatment' ? '✅ ' + this.treatmentName : report.summary.winner === 'baseline' ? '❌ ' + this.baselineName : '🤝 Tie'}**

| Metric | Baseline | Treatment | Diff |
|--------|----------|-----------|------|
| Overall Score | ${report.summary.overallScore.baseline.toFixed(1)} | ${report.summary.overallScore.treatment.toFixed(1)} | ${(report.summary.overallScore.treatment - report.summary.overallScore.baseline).toFixed(1)} |
| Statistical Significance | ${report.summary.statisticalSignificance ? '✅ Yes' : '❌ No'} |

### Key Findings
${report.summary.keyFindings.map(f => `- ${f}`).join('\n')}

## 📦 Storage Metrics

| Metric | Baseline | Treatment | Improvement |
|--------|----------|-----------|-------------|
| Success Rate | ${report.storageComparison.baseline.successRate.toFixed(1)}% | ${report.storageComparison.treatment.successRate.toFixed(1)}% | ${report.storageComparison.improvement.successRate > 0 ? '+' : ''}${report.storageComparison.improvement.successRate.toFixed(1)}% |
| Avg Store Time | ${report.storageComparison.baseline.avgStoreTime.toFixed(0)}ms | ${report.storageComparison.treatment.avgStoreTime.toFixed(0)}ms | ${report.storageComparison.improvement.avgStoreTime > 0 ? '+' : ''}${report.storageComparison.improvement.avgStoreTime.toFixed(0)}ms |

${report.storageComparison.chart}

## 🔍 Retrieval Metrics

| Metric | Baseline | Treatment | Improvement |
|--------|----------|-----------|-------------|
| Hit Rate | ${report.retrievalComparison.baseline.hitRate.toFixed(1)}% | ${report.retrievalComparison.treatment.hitRate.toFixed(1)}% | ${report.retrievalComparison.improvement.hitRate > 0 ? '+' : ''}${report.retrievalComparison.improvement.hitRate.toFixed(1)}% |
| Precision@5 | ${report.retrievalComparison.baseline.precisionAt5.toFixed(1)}% | ${report.retrievalComparison.treatment.precisionAt5.toFixed(1)}% | ${report.retrievalComparison.improvement.precisionAt5 > 0 ? '+' : ''}${report.retrievalComparison.improvement.precisionAt5.toFixed(1)}% |
| Recall@5 | ${report.retrievalComparison.baseline.recallAt5.toFixed(1)}% | ${report.retrievalComparison.treatment.recallAt5.toFixed(1)}% | ${report.retrievalComparison.improvement.recallAt5 > 0 ? '+' : ''}${report.retrievalComparison.improvement.recallAt5.toFixed(1)}% |
| Keyword Match | ${report.retrievalComparison.baseline.keywordMatchRate.toFixed(1)}% | ${report.retrievalComparison.treatment.keywordMatchRate.toFixed(1)}% | ${report.retrievalComparison.improvement.keywordMatchRate > 0 ? '+' : ''}${report.retrievalComparison.improvement.keywordMatchRate.toFixed(1)}% |

### By Difficulty

| Difficulty | Baseline | Treatment | Improvement |
|------------|----------|-----------|-------------|
| Easy | ${report.retrievalComparison.byDifficulty.easy.baseline.toFixed(1)}% | ${report.retrievalComparison.byDifficulty.easy.treatment.toFixed(1)}% | ${report.retrievalComparison.byDifficulty.easy.improvement > 0 ? '+' : ''}${report.retrievalComparison.byDifficulty.easy.improvement.toFixed(1)}% |
| Medium | ${report.retrievalComparison.byDifficulty.medium.baseline.toFixed(1)}% | ${report.retrievalComparison.byDifficulty.medium.treatment.toFixed(1)}% | ${report.retrievalComparison.byDifficulty.medium.improvement > 0 ? '+' : ''}${report.retrievalComparison.byDifficulty.medium.improvement.toFixed(1)}% |
| Hard | ${report.retrievalComparison.byDifficulty.hard.baseline.toFixed(1)}% | ${report.retrievalComparison.byDifficulty.hard.treatment.toFixed(1)}% | ${report.retrievalComparison.byDifficulty.hard.improvement > 0 ? '+' : ''}${report.retrievalComparison.byDifficulty.hard.improvement.toFixed(1)}% |

${report.retrievalComparison.chart}

## ⚡ Performance Metrics

| Metric | Baseline | Treatment | Improvement |
|--------|----------|-----------|-------------|
| Avg Query Time | ${report.performanceComparison.baseline.avgQueryTime.toFixed(0)}ms | ${report.performanceComparison.treatment.avgQueryTime.toFixed(0)}ms | ${report.performanceComparison.improvement.avgQueryTime > 0 ? '+' : ''}${report.performanceComparison.improvement.avgQueryTime.toFixed(0)}ms |
| P95 Query Time | ${report.performanceComparison.baseline.p95QueryTime.toFixed(0)}ms | ${report.performanceComparison.treatment.p95QueryTime.toFixed(0)}ms | ${report.performanceComparison.improvement.p95QueryTime > 0 ? '+' : ''}${report.performanceComparison.improvement.p95QueryTime.toFixed(0)}ms |
| P99 Query Time | ${report.performanceComparison.baseline.p99QueryTime.toFixed(0)}ms | ${report.performanceComparison.treatment.p99QueryTime.toFixed(0)}ms | ${report.performanceComparison.improvement.p99QueryTime > 0 ? '+' : ''}${report.performanceComparison.improvement.p99QueryTime.toFixed(0)}ms |

${report.performanceComparison.chart}

## ❌ Error Analysis

| Type | Count |
|-----|-------|
| Baseline Errors | ${report.errorAnalysis.baselineErrors} |
| Treatment Errors | ${report.errorAnalysis.treatmentErrors} |
| Storage Errors | ${report.errorAnalysis.errorTypes.storage} |
| Retrieval Errors | ${report.errorAnalysis.errorTypes.retrieval} |

## 💡 Recommendations

${report.recommendations.map(r => `- ${r}`).join('\n')}

---

*Generated by A/B Test Report Generator*
`;
  }

  /**
   * 生成 JSON 报告
   */
  generateJSON(): string {
    return JSON.stringify(this.generateReport(), null, 2);
  }

  /**
   * 生成 CSV 摘要
   */
  generateCSV(): string {
    const report = this.generateReport();
    
    const rows = [
      ['Metric', 'Baseline', 'Treatment', 'Improvement'],
      ['Storage Success Rate', report.storageComparison.baseline.successRate, report.storageComparison.treatment.successRate, report.storageComparison.improvement.successRate],
      ['Hit Rate', report.retrievalComparison.baseline.hitRate, report.retrievalComparison.treatment.hitRate, report.retrievalComparison.improvement.hitRate],
      ['Precision@5', report.retrievalComparison.baseline.precisionAt5, report.retrievalComparison.treatment.precisionAt5, report.retrievalComparison.improvement.precisionAt5],
      ['Recall@5', report.retrievalComparison.baseline.recallAt5, report.retrievalComparison.treatment.recallAt5, report.retrievalComparison.improvement.recallAt5],
      ['Keyword Match', report.retrievalComparison.baseline.keywordMatchRate, report.retrievalComparison.treatment.keywordMatchRate, report.retrievalComparison.improvement.keywordMatchRate],
      ['Avg Query Time', report.performanceComparison.baseline.avgQueryTime, report.performanceComparison.treatment.avgQueryTime, report.performanceComparison.improvement.avgQueryTime],
      ['P95 Query Time', report.performanceComparison.baseline.p95QueryTime, report.performanceComparison.treatment.p95QueryTime, report.performanceComparison.improvement.p95QueryTime],
      ['P99 Query Time', report.performanceComparison.baseline.p99QueryTime, report.performanceComparison.treatment.p99QueryTime, report.performanceComparison.improvement.p99QueryTime],
      ['Overall Score', report.summary.overallScore.baseline, report.summary.overallScore.treatment, report.summary.overallScore.treatment - report.summary.overallScore.baseline]
    ];

    return rows.map(row => row.join(',')).join('\n');
  }
}

// ========== 辅助函数 ==========

export function printTestInfo(): void {
  console.log('\n📊 测试数据概览');
  console.log('================\n');
  
  console.log('记忆数据:');
  console.log(`  总数: ${testMemories.length} 条`);
  console.log('  类别分布:');
  Object.entries(categoryStats).forEach(([cat, count]) => {
    console.log(`    - ${cat}: ${count} 条`);
  });
  
  console.log('\n测试查询:');
  console.log(`  总数: ${testQueries.length} 个`);
  console.log('  难度分布:');
  Object.entries(difficultyStats).forEach(([diff, count]) => {
    console.log(`    - ${diff}: ${count} 个`);
  });
}

// ========== CLI 入口 ==========

if (require.main === module) {
  // 演示用法
  const mockBaseline: TestResult = {
    testId: 'test-baseline',
    timestamp: new Date().toISOString(),
    config: { baseUrl: '', timeout: 30000, retries: 3, parallel: false, batchSize: 10 },
    storage: {
      totalAttempts: 50,
      successful: 48,
      failed: 2,
      successRate: 96,
      avgStoreTime: 45,
      duplicateDetectRate: 0
    },
    retrieval: {
      totalQueries: 20,
      hits: 14,
      misses: 6,
      hitRate: 70,
      precisionAt1: 60,
      precisionAt3: 55,
      precisionAt5: 52,
      precisionAt10: 45,
      recallAt1: 40,
      recallAt3: 55,
      recallAt5: 65,
      recallAt10: 75,
      easyHitRate: 85,
      mediumHitRate: 70,
      hardHitRate: 40,
      keywordMatchRate: 65,
      avgKeywordMatchCount: 1.5
    },
    performance: {
      avgQueryTime: 120,
      p50QueryTime: 100,
      p95QueryTime: 250,
      p99QueryTime: 350,
      maxQueryTime: 400,
      minQueryTime: 50
    },
    errors: []
  };

  const mockTreatment: TestResult = {
    testId: 'test-treatment',
    timestamp: new Date().toISOString(),
    config: { baseUrl: '', timeout: 30000, retries: 3, parallel: false, batchSize: 10 },
    storage: {
      totalAttempts: 50,
      successful: 50,
      failed: 0,
      successRate: 100,
      avgStoreTime: 35,
      duplicateDetectRate: 5
    },
    retrieval: {
      totalQueries: 20,
      hits: 18,
      misses: 2,
      hitRate: 90,
      precisionAt1: 85,
      precisionAt3: 75,
      precisionAt5: 70,
      precisionAt10: 60,
      recallAt1: 60,
      recallAt3: 75,
      recallAt5: 85,
      recallAt10: 92,
      easyHitRate: 100,
      mediumHitRate: 90,
      hardHitRate: 80,
      keywordMatchRate: 85,
      avgKeywordMatchCount: 2.5
    },
    performance: {
      avgQueryTime: 80,
      p50QueryTime: 70,
      p95QueryTime: 150,
      p99QueryTime: 200,
      maxQueryTime: 250,
      minQueryTime: 40
    },
    errors: []
  };

  const generator = new ReportGenerator(mockBaseline, mockTreatment, {
    baselineName: 'Without Memory Palace',
    treatmentName: 'With Memory Palace'
  });

  console.log(generator.generateMarkdown());
  console.log('\n\nCSV 导出:');
  console.log(generator.generateCSV());
}