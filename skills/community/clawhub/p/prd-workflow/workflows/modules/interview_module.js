/**
 * 深度访谈模块 v2.8.0
 *
 * ⚠️ 此模块不执行访谈，只检查访谈结果是否存在
 *
 * 访谈由 OpenClaw AI 自己执行（参考 grill-me 理念）
 * 此模块作为"契约检查"，确保访谈已完成
 *
 * ✅ v2.7.3 新增：根据流程上下文判断是否需要访谈
 * ✅ v2.8.0 新增：访谈终止判定算法（用于 AI 判断何时停止）
 */

const fs = require('fs');
const path = require('path');

class InterviewModule {
  /**
   * 检查访谈结果是否存在
   *
   * @param {object} options.flowContext - 流程上下文
   * @param {boolean} options.flowContext.needsInterview - 是否需要访谈
   * @param {string} options.flowContext.flowType - 流程类型
   * @throws {Error} 如果访谈未执行（且流程需要访谈）
   */
  async execute(options) {
    console.log('\n🎤 检查访谈结果...');

    const { dataBus, qualityGate, outputDir, flowContext } = options;

    // ✅ 新增：判断当前流程是否需要访谈
    const needsInterview = flowContext?.needsInterview !== false;
    const flowType = flowContext?.flowType || 'unknown';

    console.log(`   流程类型：${flowType}`);
    console.log(`   是否需要访谈：${needsInterview ? '是' : '否'}`);

    // ✅ 如果流程不包含 interview，直接返回
    if (!needsInterview) {
      console.log('   ℹ️  当前流程不包含访谈步骤，跳过检查');
      return {
        skipped: true,
        reason: '当前流程不包含 interview 步骤',
        flowType: flowType
      };
    }

    // 访谈结果文件路径
    const interviewPath = path.join(outputDir, 'interview.json');

    // ✅ 检查访谈是否已执行（流程需要时）
    if (!fs.existsSync(interviewPath)) {
      const errorMessage = `
❌ 访谈未执行！

════════════════════════════════════════════════════════════
⚠️  当前流程包含 interview 步骤，需要先执行访谈
════════════════════════════════════════════════════════════

流程信息：
- 流程类型：${flowType}
- 是否需要访谈：是

期望行为：
1. OpenClaw AI 读取 SKILL.md 中的访谈方法论
2. AI 自己逐个提问（不是调用此模块）
3. 收集用户回答，构建 sharedUnderstanding
4. 写入 ${interviewPath}

访谈要求：
- ✅ 至少 16 个问题
- ✅ 覆盖 6 个维度（产品定位、核心功能、合规要求、技术约束、业务目标、用户场景）
- ✅ 设计树探索（走每个分支）
- ✅ 依赖关系解析
- ✅ 共享理解确认

访谈技巧：
- 一次问一个问题（vertical slicing）
- 根据用户回答追问细节
- "如果选择 A，那么需要决定 X、Y、Z"
- 能查代码就不问

⭐ v2.8.0 新增：访谈终止判定
使用 shouldStopInterview() 判断何时停止提问：
- 数量达标（≥16 问）
- 维度覆盖（≥6 维）
- 回答饱和度检测
- 用户明确确认

请 OpenClaw AI：
1. 不要调用 executeForAI
2. 自己开始向用户提问
3. 完成访谈后再调用工作流

════════════════════════════════════════════════════════════
      `;

      throw new Error(errorMessage);
    }

    // ✅ 读取 OpenClaw AI 执行的访谈结果
    console.log('   ✅ 访谈结果已存在，读取中...');
    const interviewData = JSON.parse(fs.readFileSync(interviewPath, 'utf8'));

    // 质量验证
    const quality = await this.validateInterview(interviewData);

    if (!quality.passed) {
      console.warn('\n⚠️  访谈质量检查未通过:');
      quality.errors.forEach(err => {
        console.warn(`   - ${err}`);
      });
      console.warn('\n   建议：OpenClaw AI 应继续提问，补充缺失信息\n');
    } else {
      console.log(`   ✅ 访谈质量检查通过：${quality.decisionCount} 个决策，${quality.questionCount} 个问题`);
    }

    // 写入数据总线（便于后续模块读取）
    const filepath = dataBus.write('interview', interviewData, quality);

    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate1_interview', interviewData);
    }

    return {
      ...interviewData,
      quality: quality,
      outputPath: filepath
    };
  }

  /**
   * 代码验证：检查访谈质量
   */
  async validateInterview(interviewResult) {
    const errors = [];

    // 检查共享理解
    if (!interviewResult.sharedUnderstanding) {
      errors.push('缺少共享理解总结');
    } else {
      // 检查关键维度
      if (!interviewResult.sharedUnderstanding.productPositioning) {
        errors.push('缺少产品定位');
      }
      if (!interviewResult.sharedUnderstanding.coreFeatures ||
          interviewResult.sharedUnderstanding.coreFeatures.length === 0) {
        errors.push('缺少核心功能定义');
      }
    }

    // 检查关键决策数量
    if (!interviewResult.keyDecisions || interviewResult.keyDecisions.length < 12) {
      errors.push(`关键决策数量不足：${interviewResult.keyDecisions?.length || 0} < 12（建议 12-50 个）`);
    }

    // 检查问题数量
    if (!interviewResult.questions || interviewResult.questions.length < 16) {
      errors.push(`问题数量不足：${interviewResult.questions?.length || 0} < 16（建议 16-50 个）`);
    }

    // 检查设计树
    if (!interviewResult.designTree || !interviewResult.designTree.branches) {
      errors.push('缺少设计树探索');
    }

    return {
      passed: errors.length === 0,
      errors: errors,
      decisionCount: interviewResult.keyDecisions?.length || 0,
      questionCount: interviewResult.questions?.length || 0,
      dimensions: {
        hasProductPositioning: !!interviewResult.sharedUnderstanding?.productPositioning,
        hasCoreFeatures: !!(interviewResult.sharedUnderstanding?.coreFeatures?.length > 0),
        hasCompliance: !!(interviewResult.sharedUnderstanding?.complianceRequirements?.length > 0)
      }
    };
  }

  /**
   * ⭐ v2.8.0 新增：访谈终止判定算法
   *
   * OpenClaw AI 在访谈过程中调用此方法判断是否应该停止
   *
   * @param {Array} questions - 已问的问题列表
   * @param {Array} answers - 用户的回答列表
   * @param {object} currentUnderstanding - 当前构建的共享理解
   * @returns {object} { stop: boolean, reason: string, needConfirm: boolean, suggestion: string }
   */
  shouldStopInterview(questions, answers, currentUnderstanding = {}) {
    const questionCount = questions?.length || 0;
    const answerCount = answers?.length || 0;

    // 阶段 1：数量不足，继续提问
    if (questionCount < 16) {
      return {
        stop: false,
        reason: `问题数量不足 (${questionCount}/16)`,
        suggestion: '继续提问，至少需要 16 个问题'
      };
    }

    // 阶段 2：检查维度覆盖
    const dimensionsCovered = this.countDimensions(questions);
    if (dimensionsCovered < 6) {
      return {
        stop: false,
        reason: `维度覆盖不足 (${dimensionsCovered}/6)`,
        missingDimensions: this.getMissingDimensions(questions),
        suggestion: `补充缺失维度的问题：${this.getMissingDimensions(questions).join('、')}`
      };
    }

    // 阶段 3：回答饱和度检测
    const recentAnswers = answers.slice(-3);
    const saturation = this.calculateSaturation(recentAnswers);

    if (saturation.score > 0.7) {
      return {
        stop: true,
        reason: '用户回答饱和度较高',
        saturationDetails: saturation,
        suggestion: '用户可能已经疲惫，建议总结确认后结束访谈'
      };
    }

    // 阶段 4：关键决策完整性
    const decisions = currentUnderstanding.keyDecisions || [];
    if (decisions.length < 12) {
      return {
        stop: false,
        reason: `关键决策不足 (${decisions.length}/12)`,
        suggestion: '继续追问，构建完整的设计决策树'
      };
    }

    // 阶段 5：用户确认
    return {
      stop: false,
      needConfirm: true,
      reason: '访谈条件满足，需要用户确认共享理解',
      suggestion: '总结共享理解，请用户确认是否准确'
    };
  }

  /**
   * 统计已覆盖的维度数量
   */
  countDimensions(questions) {
    const dimensionKeywords = {
      '产品定位': ['目标用户', '年龄段', '收入', '定位', '用户群体'],
      '核心功能': ['功能', '特性', '能力', '支持', '提供'],
      '合规要求': ['合规', '监管', '风险测评', '适当性', '冷静期', '风险等级'],
      '技术约束': ['技术', '系统', '接口', '渠道', '平台', '上线'],
      '业务目标': ['目标', 'KPI', '指标', '效果', '提升', '解决'],
      '用户场景': ['场景', '使用', '频率', '时机', '流程']
    };

    const covered = new Set();

    questions.forEach(q => {
      const questionText = (typeof q === 'string') ? q : (q.question || '');
      Object.entries(dimensionKeywords).forEach(([dimension, keywords]) => {
        if (keywords.some(kw => questionText.includes(kw))) {
          covered.add(dimension);
        }
      });
    });

    return covered.size;
  }

  /**
   * 获取缺失的维度
   */
  getMissingDimensions(questions) {
    const allDimensions = ['产品定位', '核心功能', '合规要求', '技术约束', '业务目标', '用户场景'];
    const coveredCount = this.countDimensions(questions);

    const dimensionKeywords = {
      '产品定位': ['目标用户', '年龄段', '收入', '定位', '用户群体'],
      '核心功能': ['功能', '特性', '能力', '支持', '提供'],
      '合规要求': ['合规', '监管', '风险测评', '适当性', '冷静期', '风险等级'],
      '技术约束': ['技术', '系统', '接口', '渠道', '平台', '上线'],
      '业务目标': ['目标', 'KPI', '指标', '效果', '提升', '解决'],
      '用户场景': ['场景', '使用', '频率', '时机', '流程']
    };

    const missing = [];

    allDimensions.forEach(dimension => {
      const keywords = dimensionKeywords[dimension];
      const isCovered = questions.some(q => {
        const questionText = (typeof q === 'string') ? q : (q.question || '');
        return keywords.some(kw => questionText.includes(kw));
      });
      if (!isCovered) {
        missing.push(dimension);
      }
    });

    return missing;
  }

  /**
   * 计算回答饱和度
   */
  calculateSaturation(recentAnswers) {
    if (!recentAnswers || recentAnswers.length === 0) {
      return { score: 0, factors: [] };
    }

    const factors = [];

    // 因素 1：回答长度趋势
    const lengths = recentAnswers.map(a => {
      const text = (typeof a === 'string') ? a : (a.answer || '');
      return text.length;
    });
    const avgLength = lengths.reduce((s, l) => s + l, 0) / lengths.length;
    if (avgLength < 20) {
      factors.push({ factor: '回答简短', weight: 0.4 });
    }

    // 因素 2：模糊词检测
    const vagueWords = ['大概', '可能', '不确定', '随便', '都行', '无所谓', '不确定', '看情况'];
    const hasVagueWords = recentAnswers.some(a => {
      const text = (typeof a === 'string') ? a : (a.answer || '');
      return vagueWords.some(w => text.includes(w));
    });
    if (hasVagueWords) {
      factors.push({ factor: '使用模糊词', weight: 0.3 });
    }

    // 因素 3：重复回答
    const answerTexts = recentAnswers.map(a => {
      const text = (typeof a === 'string') ? a : (a.answer || '');
      return text.trim().toLowerCase();
    });
    const uniqueAnswers = new Set(answerTexts);
    if (uniqueAnswers.size < answerTexts.length) {
      factors.push({ factor: '回答重复', weight: 0.2 });
    }

    // 因素 4：用户主动结束信号
    const endSignals = ['没问题了', '就这些', '可以了', '够了', '继续吧', '下一步'];
    const hasEndSignal = recentAnswers.some(a => {
      const text = (typeof a === 'string') ? a : (a.answer || '');
      return endSignals.some(s => text.includes(s));
    });
    if (hasEndSignal) {
      factors.push({ factor: '主动结束信号', weight: 0.5 });
    }

    // 计算综合饱和度
    const score = Math.min(1, factors.reduce((s, f) => s + f.weight, 0));

    return { score, factors };
  }
}

module.exports = InterviewModule;