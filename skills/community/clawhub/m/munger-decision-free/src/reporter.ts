import { DecisionReport, ModelAnalysis, Model, DialogueContext } from './types';

/**
 * 报告生成器
 * 
 * 负责生成决策分析报告，包括各模型的分析结果、综合建议和风险提示。
 * 
 * 核心功能：
 * 1. 分析各模型的答案并评分
 * 2. 生成综合建议（基于所有模型的评分）
 * 3. 识别风险点
 * 4. 格式化为 Markdown 报告
 * 
 * 报告结构：
 * - 标题和元信息（决策主题、时间、场景）
 * - 各模型分析（评分、分析、答案）
 * - 综合建议（基于评分比例）
 * - 风险提示（低分模型的警告）
 * 
 * @example
 * ```typescript
 * const reporter = new ReportGenerator();
 * const report = reporter.generate(context, models, '投资决策');
 * const markdown = reporter.formatMarkdown(report);
 * console.log(markdown);
 * ```
 */
export class ReportGenerator {
  /**
   * 生成决策报告
   * 
   * 根据对话上下文和模型配置，生成完整的决策分析报告。
   * 
   * 生成流程：
   * 1. 遍历所有选中的模型
   * 2. 分析每个模型的答案并评分
   * 3. 生成综合建议（基于评分比例）
   * 4. 识别风险点（低分模型）
   * 
   * @param context - 对话上下文（包含用户答案）
   * @param models - 模型配置列表
   * @param scenarioName - 场景名称（用于展示）
   * @returns 决策报告对象
   * 
   * @example
   * ```typescript
   * const report = reporter.generate(context, models, '投资决策');
   * console.log(report.recommendation); // '建议执行'
   * console.log(report.risks.length); // 2
   * ```
   */
  generate(
    context: DialogueContext,
    models: Model[],
    scenarioName: string
  ): DecisionReport {
    const analyses: ModelAnalysis[] = [];
    
    // 分析每个模型
    for (const modelId of context.selectedModels) {
      const model = models.find(m => m.id === modelId);
      if (!model) continue; // 跳过未找到的模型

      const answers = context.answers[modelId] || [];
      const analysis = this.analyzeModel(model, answers);
      
      analyses.push({
        modelId: model.id,
        modelName: model.name,
        answers,
        score: analysis.score,
        analysis: analysis.text
      });
    }

    // 生成综合建议（基于所有模型的评分）
    const recommendation = this.generateRecommendation(analyses);
    // 识别风险点（低分模型）
    const risks = this.identifyRisks(analyses);

    return {
      title: context.userInput,
      timestamp: Date.now(),
      scenario: scenarioName,
      analyses,
      recommendation,
      risks
    };
  }

  /**
   * 分析单个模型
   * 
   * 根据用户的答案，评估该模型的得分和分析文本。
   * 
   * 评分逻辑（简化版）：
   * - 答案平均长度 > 20 字符：使用模型的第一个评分等级
   * - 答案平均长度 ≤ 20 字符：评分为 'unclear'（需要更详细的分析）
   * 
   * 注意：这是简化版实现，实际应该根据答案内容进行语义分析。
   * 
   * @param model - 模型配置
   * @param answers - 用户的答案列表
   * @returns 评分和分析文本
   * 
   * @example
   * ```typescript
   * const result = reporter.analyzeModel(model, ['我不太了解', '没有经验']);
   * console.log(result.score); // 'low'
   * console.log(result.text); // '了解不足，需要学习'
   * ```
   */
  private analyzeModel(model: Model, answers: string[]): { score: string; text: string } {
    // 计算答案平均长度（作为答案质量的简单指标）
    const avgLength = answers.reduce((sum, a) => sum + a.length, 0) / answers.length;
    
    let score = 'unclear';
    let text = '需要更详细的分析';

    // 如果答案足够详细（平均长度 > 20 字符）
    if (avgLength > 20) {
      // 使用模型的第一个评分等级（通常是最常见的评分）
      const scoringKeys = Object.keys(model.scoring);
      score = scoringKeys[0] || 'unclear';
      text = model.scoring[score] || '分析完成';
    }

    return { score, text };
  }

  /**
   * 生成综合建议
   * 
   * 根据所有模型的评分，生成综合决策建议。
   * 
   * 建议逻辑：
   * - 积极评分比例 > 70%：建议执行
   * - 积极评分比例 40%-70%：谨慎推进
   * - 积极评分比例 < 40%：建议暂缓
   * 
   * 积极评分定义：评分包含 'high'、'strong'、'sufficient' 等关键词
   * 
   * @param analyses - 所有模型的分析结果
   * @returns 综合建议文本
   * 
   * @example
   * ```typescript
   * const recommendation = reporter.generateRecommendation(analyses);
   * // '✅ **建议执行**\n分析显示多数维度评估积极，可以推进决策。'
   * ```
   */
  private generateRecommendation(analyses: ModelAnalysis[]): string {
    // 如果没有分析数据，返回警告
    if (analyses.length === 0) {
      return '⚠️ 缺少足够的分析数据';
    }

    // 统计积极评分的模型数量
    const positiveCount = analyses.filter(a => 
      a.score.includes('high') || 
      a.score.includes('strong') || 
      a.score.includes('sufficient')
    ).length;

    // 计算积极评分比例
    const ratio = positiveCount / analyses.length;

    // 根据比例生成建议
    if (ratio > 0.7) {
      return '✅ **建议执行**\n分析显示多数维度评估积极，可以推进决策。';
    } else if (ratio > 0.4) {
      return '⚠️ **谨慎推进**\n存在一些风险点，建议进一步研究后决策。';
    } else {
      return '❌ **建议暂缓**\n多个维度评估不理想，建议重新评估或寻找替代方案。';
    }
  }

  /**
   * 识别风险
   * 
   * 从所有模型的分析结果中，识别评分较低的模型作为风险点。
   * 
   * 风险识别逻辑：
   * - 评分包含 'low'、'weak'、'insufficient' 等关键词的模型
   * - 如果没有识别到风险，返回通用提示
   * 
   * @param analyses - 所有模型的分析结果
   * @returns 风险提示列表
   * 
   * @example
   * ```typescript
   * const risks = reporter.identifyRisks(analyses);
   * // ['能力圈：了解不足', '安全边际：估值过高']
   * ```
   */
  private identifyRisks(analyses: ModelAnalysis[]): string[] {
    const risks: string[] = [];

    // 遍历所有分析结果，找出低分模型
    for (const analysis of analyses) {
      if (analysis.score.includes('low') || 
          analysis.score.includes('weak') || 
          analysis.score.includes('insufficient')) {
        risks.push(`${analysis.modelName}：${analysis.analysis}`);
      }
    }

    // 如果没有识别到风险，返回通用提示
    if (risks.length === 0) {
      risks.push('未识别到明显风险（建议持续监控）');
    }

    return risks;
  }

  /**
   * 格式化为 Markdown
   * 
   * 将决策报告对象格式化为 Markdown 文本，便于展示和分享。
   * 
   * Markdown 结构：
   * 1. 标题和元信息
   * 2. 各模型分析（编号、评分、分析、答案）
   * 3. 综合建议
   * 4. 风险提示
   * 
   * @param report - 决策报告对象
   * @returns Markdown 格式的报告文本
   * 
   * @example
   * ```typescript
   * const markdown = reporter.formatMarkdown(report);
   * console.log(markdown);
   * // # 决策分析报告
   * // **决策主题：** 要不要投资这只股票？
   * // ...
   * ```
   */
  formatMarkdown(report: DecisionReport): string {
    // 格式化时间戳为本地时间
    const date = new Date(report.timestamp).toLocaleString('zh-CN');
    
    // 报告头部
    let md = `# 决策分析报告\n\n`;
    md += `**决策主题：** ${report.title}\n`;
    md += `**分析时间：** ${date}\n`;
    md += `**决策场景：** ${report.scenario}\n`;
    md += `**分析模型：** ${report.analyses.map(a => a.modelName).join('、')}\n\n`;
    md += `---\n\n`;

    // 各模型分析
    for (let i = 0; i < report.analyses.length; i++) {
      const analysis = report.analyses[i];
      md += `## ${i + 1}. ${analysis.modelName}分析\n\n`;
      md += `**评分：** ${analysis.score}\n`;
      md += `**分析：** ${analysis.analysis}\n\n`;
      
      // 如果有答案，展示答案列表
      if (analysis.answers.length > 0) {
        md += `**回答：**\n`;
        analysis.answers.forEach((answer, idx) => {
          md += `${idx + 1}. ${answer}\n`;
        });
        md += `\n`;
      }
    }

    md += `---\n\n`;

    // 综合建议
    md += `## 综合建议\n\n`;
    md += `${report.recommendation}\n\n`;

    // 风险提示
    md += `## 风险提示\n\n`;
    report.risks.forEach(risk => {
      md += `- ${risk}\n`;
    });

    return md;
  }
}
