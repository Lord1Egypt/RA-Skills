/**
 * 需求拆解模块 v2.6.0
 * 
 * 将共享理解转化为结构化需求
 * 
 * v2.6.0 新增:
 * - 集成检查项指导（CORE-1, CORE-2, CORE-3）
 * - 集成质量检查项加载器
 * - 生成业务分析报告
 * - 增强质量验证逻辑
 * 
 * @version 2.6.0
 * @since 2026-04-05
 */

const fs = require('fs');
const path = require('path');
const checkItemsLoader = require('../check_items_loader.js');
const { DecompositionReportGenerator } = require('../decomposition_report.js');
const schema = require('../decomposition_schema.js');

class DecompositionModule {
  /**
   * 执行需求拆解
   * 
   * @param {Object} options - 执行选项
   * @param {Object} options.dataBus - 数据总线实例
   * @param {Object} options.qualityGate - 质量门禁实例
   * @param {string} options.outputDir - 输出目录
   * @param {string} options.userInput - 用户输入
   * @param {boolean} options.autoRetry - 是否自动重试
   * @param {boolean} options.generateReport - 是否生成业务报告（默认 true）
   * @returns {Promise<Object>} 需求拆解结果
   */
  async execute(options) {
    console.log('\n📝 执行技能：需求拆解 v2.6.0');
    
    const {
      dataBus,
      qualityGate,
      outputDir,
      userInput,
      autoRetry = false,
      generateReport = true
    } = options;
    
    // ========== Step 1: 读取访谈结果 ==========
    const interviewRecord = dataBus.read('interview');
    if (!interviewRecord) {
      throw new Error('访谈结果不存在，请先执行深度访谈');
    }
    
    const sharedUnderstanding = interviewRecord.data;
    console.log('   ✓ 已读取访谈结果');
    
    // ========== Step 2: 加载检查项指导 ==========
    console.log('   📋 加载质量检查项指导...');
    const checkItemsPrompt = await checkItemsLoader.generatePrompt('decomposition');
    const coreItems = await checkItemsLoader.loadForStage('decomposition');
    console.log(`   ✓ 已加载 ${coreItems.length} 项核心检查项`);
    
    // ========== Step 3: 确定核心功能 ==========
    const coreFeaturesFromInput = this.extractCoreFeaturesFromInput(userInput);
    const coreFeatures = (sharedUnderstanding.coreFeatures && sharedUnderstanding.coreFeatures.length > 0)
      ? sharedUnderstanding.coreFeatures
      : coreFeaturesFromInput;
    
    // ========== Step 4: 检查迭代模式 ==========
    const existingRecord = dataBus.read('decomposition');
    let decomposition;
    
    if (existingRecord && existingRecord.data && userInput && userInput.length > 0) {
      const isIteration = ['追加', '新增', '添加', '修改', '调整'].some(k => userInput.includes(k));
      
      if (isIteration) {
        console.log('   🔄 迭代模式：在现有基础上追加功能...');
        decomposition = await this.appendFeatures(existingRecord.data, userInput);
      } else {
        console.log('   🤖 AI 生成：功能清单、用户故事、验收标准...');
        decomposition = await this.generateDecomposition(sharedUnderstanding, coreFeatures, checkItemsPrompt);
      }
    } else {
      console.log('   🤖 AI 生成：功能清单、用户故事、验收标准...');
      decomposition = await this.generateDecomposition(sharedUnderstanding, coreFeatures, checkItemsPrompt);
    }
    
    // ========== Step 5: 质量验证（增强版） ==========
    console.log('   🔍 执行质量验证...');
    const quality = await this.validateDecomposition(decomposition, coreItems);
    
    // ========== Step 6: 生成业务报告（可选） ==========
    let businessReport = null;
    if (generateReport) {
      try {
        console.log('   📊 生成业务分析报告...');
        const reportGenerator = new DecompositionReportGenerator();
        businessReport = await reportGenerator.generate({
          projectName: sharedUnderstanding.productName || '未命名项目',
          modules: decomposition.features || []
        });
        console.log('   ✓ 业务报告生成完成');
      } catch (error) {
        console.warn('   ⚠️  业务报告生成失败:', error.message);
      }
    }
    
    // ========== Step 7: 写入数据总线 ==========
    const decompositionData = {
      ...decomposition,
      businessReport: businessReport,
      checkItemsVersion: '1.0',
      generatedAt: new Date().toISOString()
    };
    
    const filepath = dataBus.write('decomposition', decompositionData, quality, {
      fromInterview: true,
      hasBusinessReport: !!businessReport
    });
    console.log(`   ✓ 已写入数据总线：${filepath}`);
    
    // ========== Step 8: 门禁检查 ==========
    if (qualityGate) {
      console.log('   🚪 执行质量门禁检查...');
      const gateResult = await qualityGate.pass('gate2_decomposition', decompositionData);
      
      if (!gateResult.passed) {
        console.warn('   ⚠️  质量门禁未通过');
        
        if (autoRetry && gateResult.retries > 0) {
          console.log(`   🔄 自动重试（剩余 ${gateResult.retries} 次）...`);
          // 重试逻辑：根据门禁反馈调整生成策略
          return await this.execute({
            ...options,
            userInput: userInput + ' 请改进质量'
          });
        }
      } else {
        console.log('   ✓ 质量门禁通过');
      }
    }
    
    // ========== Step 9: 返回结果 ==========
    return {
      ...decompositionData,
      quality: quality,
      outputPath: filepath,
      businessReport: businessReport
    };
  }
  
  /**
   * 迭代模式：追加新功能
   */
  async appendFeatures(existingDecomp, userInput) {
    // 从用户输入中提取新功能名称
    const featureName = this.extractFeatureName(userInput);
    
    // 追加新功能
    const newFeature = {
      id: `f${existingDecomp.features.length + 1}`,
      name: featureName,
      priority: 'P0',
      description: `${featureName}功能`
    };
    
    // 追加到功能列表
    existingDecomp.features.push(newFeature);
    
    // 追加用户故事
    const newUserStory = `As a 用户，I want ${featureName}, So that 获得${featureName}的价值`;
    existingDecomp.userStories.push(newUserStory);
    
    // v3.1.0: 验收标准在 PRD 阶段生成，需求拆解不再生成
    
    return existingDecomp;
  }
  
  /**
   * 从用户输入提取功能名称
   */
  extractFeatureName(userInput) {
    // "追加产品推荐功能" → "产品推荐"
    // "新增用户管理" → "用户管理"
    const keywords = ['追加', '新增', '添加', '修改', '调整'];
    let name = userInput;
    
    keywords.forEach(keyword => {
      name = name.replace(keyword, '');
    });
    
    name = name.replace(/功能/g, '').trim();
    
    return name || '新功能';
  }
  
  /**
   * 从用户输入提取核心功能关键词
   */
  extractCoreFeaturesFromInput(userInput) {
    if (!userInput) return ['核心功能'];
    
    const features = [];
    if (userInput.includes('养老')) features.push('养老金测算');
    if (userInput.includes('推荐')) features.push('产品推荐');
    if (userInput.includes('配置')) features.push('配置建议');
    
    return features.length > 0 ? features : ['核心功能'];
  }
  
  /**
   * AI 驱动：生成需求内容（增强版）
   * 
   * 基于检查项指导生成详细的功能数据，包括业务规则、输入输出、原型等
   * 
   * @param {Object} sharedUnderstanding - 共享理解数据
   * @param {Array} coreFeatures - 核心功能列表
   * @param {string} checkItemsPrompt - 检查项指导提示词
   * @returns {Promise<Object>} 需求分解结果
   */
  /**
   * AI 驱动：生成需求内容 v2.6.0（真实调用 AI）
   */
  async generateDecomposition(sharedUnderstanding, coreFeatures, checkItemsPrompt = '') {
    const featuresList = coreFeatures || sharedUnderstanding.coreFeatures || [];
    const productPositioning = sharedUnderstanding.productPositioning || {};
    
    console.log(`   📋 检查项指导：${checkItemsPrompt ? '已加载' : '未加载'}`);
    
    // 真实调用 AI
    if (checkItemsPrompt && featuresList.length > 0) {
      try {
        console.log('   🤖 AI 生成：功能清单、业务规则、输入输出...');
        const prompt = `你是专业需求分析师，请基于检查项指导生成需求。${checkItemsPrompt}。核心功能：${featuresList.join(', ')}。输出 JSON 格式。`;
        const result = await sessions_spawn({ runtime: 'subagent', mode: 'run', task: prompt, timeoutSeconds: 300 });
        const aiDecomposition = this.parseAIDecomposition(result.content || result);
        if (aiDecomposition && aiDecomposition.features) {
          console.log(`   ✅ AI 生成完成：${aiDecomposition.features.length} 个功能`);
          return aiDecomposition;
        }
      } catch (error) {
        console.warn('⚠️  AI 生成失败，使用本地模板:', error.message);
      }
    }
    
    // Fallback: 本地模板
    console.log('   📝 使用本地模板生成需求拆解...');
    return this.generateDecompositionFromTemplate(featuresList, productPositioning);
  }
  
  parseAIDecomposition(aiResult) {
    try {
      const jsonMatch = aiResult.match(/\{[\s\S]*\}/);
      if (jsonMatch) return JSON.parse(jsonMatch[0]);
      return JSON.parse(aiResult);
    } catch (error) {
      console.warn('⚠️  解析 AI 结果失败:', error.message);
      return null;
    }
  }
  
  generateDecompositionFromTemplate(featuresList, productPositioning) {
    const features = featuresList.map((name, i) => ({
      id: `f${i + 1}`,
      name: name || `功能${i + 1}`,
      priority: i === 0 ? 'P0' : (i === 1 ? 'P1' : 'P2'),
      description: this.generateFeatureDescription(name),
      businessRules: this.generateBusinessRules(name),
      inputs: this.generateInputs(name),
      outputs: this.generateOutputs(name),
      exceptions: this.generateExceptions(name)
    }));
    return { features: features.length > 0 ? features : [{ id: 'f1', name: '核心功能' }], userStories: [] };  // v3.1.0: 验收标准在 PRD 阶段生成
  }
  generateFeatureDescription(featureName) {
    if (featureName.includes('测算') || featureName.includes('计算')) {
      return `基于用户输入的年龄、收入、缴存比例等信息，通过精算模型${featureName}，提供养老金领取金额、预计领取总额等详细数据，帮助用户规划养老生活。`;
    }
    if (featureName.includes('推荐') || featureName.includes('产品')) {
      return `根据用户的风险偏好、收益预期和流动性需求，智能${featureName}，提供个性化的产品配置建议。`;
    }
    if (featureName.includes('配置') || featureName.includes('建议')) {
      return `综合分析用户的财务状况和目标，提供资产${featureName}，包括各类资产的配置比例和调整建议。`;
    }
    return `${featureName}功能，满足用户核心需求。`;
  }
  
  /**
   * 生成业务规则
   */
  generateBusinessRules(featureName) {
    if (featureName.includes('测算') || featureName.includes('计算')) {
      return [
        { id: 'BR-001', name: '年龄限制', description: '年龄必须在 18-60 岁之间', validation: '18 ≤ age ≤ 60', error: '年龄必须在 18-60 岁之间' },
        { id: 'BR-002', name: '收入限制', description: '月收入必须在 3000-100000 元之间', validation: '3000 ≤ income ≤ 100000', error: '月收入必须在 3000-100000 元之间' },
        { id: 'BR-003', name: '缴存比例', description: '缴存比例必须在 5%-12% 之间', validation: '0.05 ≤ ratio ≤ 0.12', error: '缴存比例必须在 5%-12% 之间' }
      ];
    }
    
    return [
      { id: 'BR-001', name: '待填写', description: '待填写', validation: '待填写', error: '待填写' }
    ];
  }
  
  /**
   * 生成输入定义
   */
  generateInputs(featureName) {
    if (featureName.includes('测算') || featureName.includes('计算')) {
      return [
        { field: '年龄', type: '整数', required: true, default: '无', description: '用户当前年龄', validation: '18 ≤ age ≤ 60', error: '年龄必须在 18-60 岁之间' },
        { field: '月收入', type: '数字 (2 位小数)', required: true, default: '无', description: '用户月收入（元）', validation: '3000 ≤ income ≤ 100000', error: '月收入必须在 3000-100000 元之间' },
        { field: '缴存比例', type: '百分比 (1 位小数)', required: true, default: '8.0%', description: '公积金缴存比例', validation: '5% ≤ ratio ≤ 12%', error: '缴存比例必须在 5%-12% 之间' }
      ];
    }
    
    return [
      { field: '待填写', type: '待填写', required: true, default: '无', description: '待填写', validation: '待填写', error: '待填写' }
    ];
  }
  
  /**
   * 生成输出定义
   */
  generateOutputs(featureName) {
    if (featureName.includes('测算') || featureName.includes('计算')) {
      return [
        { field: 'monthlyPension', type: '数字 (2 位小数)', description: '每月可领取养老金（元）', example: '8500.00' },
        { field: 'totalPension', type: '数字 (2 位小数)', description: '预计领取总额（元）', example: '2040000.00' },
        { field: 'calculationDate', type: '日期时间', description: '测算日期', example: '2026-04-01 10:30:00' }
      ];
    }
    
    return [
      { field: '待填写', type: '待填写', description: '待填写', example: '待填写' }
    ];
  }
  
  /**
   * 生成用户场景
   */
  generateScenarios(featureName) {
    return [
      {
        name: '首次使用',
        user: '张先生，35 岁，首次使用',
        goal: `了解${featureName}结果`,
        steps: [
          `打开${featureName}页面`,
          '输入必要参数',
          '点击提交',
          '查看结果'
        ],
        expectation: '操作简单，3 分钟内完成，结果清晰易懂'
      }
    ];
  }
  
  /**
   * 生成用户故事
   */
  generateUserStories(featureName, productPositioning) {
    const targetUser = productPositioning.targetUsers || '用户';
    return [
      {
        content: `As a ${targetUser}, I want to use ${featureName}, So that I can get the value of ${featureName}`,
        priority: 'P0',
        acceptance: '功能正常工作，结果准确'
      }
    ];
  }
  
  /**
   * 生成原型信息
   */
  generatePrototype(featureName) {
    return {
      pages: [
        { name: `${featureName}页`, description: `主${featureName}页面`, priority: 'P0', file: `prototypes/${featureName}.html` }
      ],
      layout: `┌─────────────────────────────────────────┐
│  ← 返回     ${featureName}                  │
├─────────────────────────────────────────┤
│                                         │
│  输入区域                                │
│  [____]                                 │
│                                         │
├─────────────────────────────────────────┤
│         [ 提交 ]                         │
└─────────────────────────────────────────┘`,
      interactions: [
        { element: '输入框', type: '输入', description: '输入必要参数' },
        { element: '提交按钮', type: '点击', description: '校验通过后提交' }
      ],
      files: {
        html: `prototypes/${featureName.toLowerCase()}.html`,
        png: `prototypes/${featureName.toLowerCase()}.png`
      }
    };
  }
  
  /**
   * 生成异常处理
   */
  generateExceptions(featureName) {
    return [
      { type: '参数校验失败', condition: '参数超范围', code: 'PARAM_ERROR', message: '参数校验失败，请检查输入', handling: '前端提示，阻止提交' },
      { type: '系统异常', condition: '服务器错误', code: 'SYSTEM_ERROR', message: '系统繁忙，请稍后重试', handling: '后端捕获，返回错误' }
    ];
  }
  
  /**
   * 代码验证：检查拆解质量（增强版）
   * 
   * 基于检查项进行质量验证，支持 CORE-1, CORE-2, CORE-3
   * 
   * @param {Object} decomposition - 需求拆解结果
   * @param {Array} checkItems - 检查项列表
   * @returns {Promise<Object>} 质量验证结果
   */
  async validateDecomposition(decomposition, checkItems = []) {
    const errors = [];
    const warnings = [];
    const checkResults = [];
    
    const features = decomposition.features || [];
    
    // ========== 基础验证 ==========
    // 检查功能清单
    if (!features || features.length === 0) {
      errors.push('功能清单为空');
    }
    
    // 检查用户故事格式
    if (decomposition.userStories) {
      const invalidStories = decomposition.userStories.filter(story => {
        const storyText = typeof story === 'string' ? story : (story.content || '');
        return !storyText.includes('As a') || !storyText.includes('I want') || !storyText.includes('So that');
      });
      if (invalidStories.length > 0) {
        warnings.push(`用户故事格式错误：${invalidStories.length} 个`);
      }
    }
    
    // v3.1.0: 需求拆解不再生成验收标准，验收标准在 PRD 阶段生成
    // 检查项验证（新增）
    if (checkItems && checkItems.length > 0) {
      console.log(`   🔍 执行 ${checkItems.length} 项检查项验证...`);
      
      for (const item of checkItems) {
        const result = await this.validateCheckItem(item, features);
        checkResults.push(result);
        
        if (result.status === 'fail') {
          errors.push(`[${item.id}] ${item.name}: ${result.comment}`);
        } else if (result.status === 'warning') {
          warnings.push(`[${item.id}] ${item.name}: ${result.comment}`);
        }
      }
    }
    
    // ========== 计算质量分数 ==========
    const qualityMetrics = this.calculateQualityMetrics(decomposition, checkResults);
    
    // ========== 返回验证结果 ==========
    return {
      passed: errors.length === 0,
      errors: errors,
      warnings: warnings,
      checkResults: checkResults,
      ...qualityMetrics,
      userStoryFormat: this.calculateUserStoryFormat(decomposition),
      acFormat: this.calculateACFormat(decomposition)
    };
  }
  
  /**
   * 验证单个检查项
   * 
   * @param {Object} checkItem - 检查项定义
   * @param {Array} features - 功能列表
   * @returns {Promise<Object>} 验证结果
   */
  async validateCheckItem(checkItem, features) {
    const result = {
      itemId: checkItem.id,
      itemName: checkItem.name,
      category: checkItem.category,
      status: 'pending',
      score: 0,
      evidence: [],
      comment: ''
    };
    
    // 根据检查项 ID 执行特定验证
    switch (checkItem.id) {
      case 'CORE-1': // 业务规则完整性
        return this.validateCore1(result, features);
      
      case 'CORE-2': // 输入输出定义
        return this.validateCore2(result, features);
      
      case 'CORE-3': // 异常处理
        return this.validateCore3(result, features);
      
      default:
        result.status = 'pass';
        result.score = 100;
        result.comment = '检查通过';
        return result;
    }
  }
  
  /**
   * 验证 CORE-1: 业务规则完整性
   * 
   * @param {Object} result - 结果对象
   * @param {Array} features - 功能列表
   * @returns {Object} 验证结果
   */
  validateCore1(result, features) {
    if (features.length === 0) {
      result.status = 'fail';
      result.score = 0;
      result.comment = '功能列表为空，无法验证业务规则';
      return result;
    }
    
    // 统计有业务规则的功能数
    const featuresWithRules = features.filter(
      f => f.businessRules && f.businessRules.length > 0
    );
    
    const coverage = (featuresWithRules.length / features.length) * 100;
    result.evidence.push(`覆盖率：${coverage.toFixed(1)}% (${featuresWithRules.length}/${features.length})`);
    
    // 统计规则总数
    const totalRules = features.reduce((sum, f) => {
      return sum + (f.businessRules?.length || 0);
    }, 0);
    result.evidence.push(`规则总数：${totalRules} 条`);
    
    // 计算得分
    if (coverage >= 90 && totalRules >= features.length * 2) {
      result.status = 'pass';
      result.score = 100;
      result.comment = '业务规则完整性优秀';
    } else if (coverage >= 70 && totalRules >= features.length) {
      result.status = 'warning';
      result.score = 75;
      result.comment = '业务规则基本完整，建议补充';
    } else {
      result.status = 'fail';
      result.score = Math.round(coverage * 0.8);
      result.comment = '业务规则不完整，需要补充';
    }
    
    return result;
  }
  
  /**
   * 验证 CORE-2: 输入输出定义
   * 
   * @param {Object} result - 结果对象
   * @param {Array} features - 功能列表
   * @returns {Object} 验证结果
   */
  validateCore2(result, features) {
    if (features.length === 0) {
      result.status = 'fail';
      result.score = 0;
      result.comment = '功能列表为空，无法验证输入输出';
      return result;
    }
    
    // 统计有输入和输出定义的功能数
    const featuresWithInputs = features.filter(
      f => f.inputs && f.inputs.length > 0
    );
    const featuresWithOutputs = features.filter(
      f => f.outputs && f.outputs.length > 0
    );
    const featuresWithBoth = features.filter(
      f => (f.inputs && f.inputs.length > 0) && (f.outputs && f.outputs.length > 0)
    );
    
    const inputCoverage = (featuresWithInputs.length / features.length) * 100;
    const outputCoverage = (featuresWithOutputs.length / features.length) * 100;
    const bothCoverage = (featuresWithBoth.length / features.length) * 100;
    
    result.evidence.push(`输入定义覆盖率：${inputCoverage.toFixed(1)}%`);
    result.evidence.push(`输出定义覆盖率：${outputCoverage.toFixed(1)}%`);
    result.evidence.push(`完整定义覆盖率：${bothCoverage.toFixed(1)}%`);
    
    // 计算得分
    if (bothCoverage >= 90) {
      result.status = 'pass';
      result.score = 100;
      result.comment = '输入输出定义完整';
    } else if (bothCoverage >= 70) {
      result.status = 'warning';
      result.score = 75;
      result.comment = '输入输出定义基本完整，建议补充';
    } else {
      result.status = 'fail';
      result.score = Math.round(bothCoverage * 0.9);
      result.comment = '输入输出定义不完整，需要补充';
    }
    
    return result;
  }
  
  /**
   * 验证 CORE-3: 异常处理
   * 
   * @param {Object} result - 结果对象
   * @param {Array} features - 功能列表
   * @returns {Object} 验证结果
   */
  validateCore3(result, features) {
    if (features.length === 0) {
      result.status = 'fail';
      result.score = 0;
      result.comment = '功能列表为空，无法验证异常处理';
      return result;
    }
    
    // 统计有异常处理的功能数
    const featuresWithExceptions = features.filter(
      f => f.exceptions && f.exceptions.length > 0
    );
    
    const coverage = (featuresWithExceptions.length / features.length) * 100;
    result.evidence.push(`异常处理覆盖率：${coverage.toFixed(1)}% (${featuresWithExceptions.length}/${features.length})`);
    
    // 统计异常处理总数
    const totalExceptions = features.reduce((sum, f) => {
      return sum + (f.exceptions?.length || 0);
    }, 0);
    result.evidence.push(`异常处理总数：${totalExceptions} 个`);
    
    // 计算得分
    if (coverage >= 90 && totalExceptions >= features.length * 2) {
      result.status = 'pass';
      result.score = 100;
      result.comment = '异常处理完善';
    } else if (coverage >= 70 && totalExceptions >= features.length) {
      result.status = 'warning';
      result.score = 75;
      result.comment = '异常处理基本完整，建议补充';
    } else {
      result.status = 'fail';
      result.score = Math.round(coverage * 0.8);
      result.comment = '异常处理不完整，需要补充';
    }
    
    return result;
  }
  
  /**
   * 计算质量指标
   * 
   * @param {Object} decomposition - 需求拆解结果
   * @param {Array} checkResults - 检查项结果
   * @returns {Object} 质量指标
   */
  calculateQualityMetrics(decomposition, checkResults) {
    const features = decomposition.features || [];
    
    // 计算检查项平均分
    const avgScore = checkResults.length > 0
      ? Math.round(checkResults.reduce((sum, r) => sum + r.score, 0) / checkResults.length)
      : 0;
    
    // 计算核心检查项通过率
    const coreResults = checkResults.filter(r => r.category === 'CORE');
    const corePassRate = coreResults.length > 0
      ? Math.round((coreResults.filter(r => r.status === 'pass').length / coreResults.length) * 100)
      : 0;
    
    // 计算覆盖率
    const featuresWithRules = features.filter(f => f.businessRules && f.businessRules.length > 0).length;
    const featuresWithInputs = features.filter(f => f.inputs && f.inputs.length > 0).length;
    const featuresWithOutputs = features.filter(f => f.outputs && f.outputs.length > 0).length;
    const featuresWithExceptions = features.filter(f => f.exceptions && f.exceptions.length > 0).length;
    
    const totalFeatures = features.length || 1;
    const coverage = Math.round(
      ((featuresWithRules / totalFeatures) + 
       (featuresWithInputs / totalFeatures) + 
       (featuresWithOutputs / totalFeatures) + 
       (featuresWithExceptions / totalFeatures)) / 4 * 100
    );
    
    return {
      score: avgScore,
      corePassRate: corePassRate,
      coverage: coverage,
      totalFeatures: features.length,
      featuresWithRules: featuresWithRules,
      featuresWithInputs: featuresWithInputs,
      featuresWithOutputs: featuresWithOutputs,
      featuresWithExceptions: featuresWithExceptions
    };
  }
  
  /**
   * 计算用户故事格式分数
   * 
   * @param {Object} decomposition - 需求拆解结果
   * @returns {number} 格式分数 (0-100)
   */
  calculateUserStoryFormat(decomposition) {
    if (!decomposition.userStories || decomposition.userStories.length === 0) {
      return 0;
    }
    
    const invalidCount = decomposition.userStories.filter(story => {
      const storyText = typeof story === 'string' ? story : (story.content || '');
      return !storyText.includes('As a') || !storyText.includes('I want') || !storyText.includes('So that');
    }).length;
    
    return Math.round((1 - invalidCount / decomposition.userStories.length) * 100);
  }
  
  /**
   * 计算验收标准格式分数
   * v3.1.0: 需求拆解不再生成验收标准，此方法保留用于 PRD 阶段验证
   * 
   * @param {Object} decomposition - 需求拆解结果
   * @returns {number} 格式分数 (0-100)
   */
  calculateACFormat(decomposition) {
    if (!decomposition.acceptanceCriteria || decomposition.acceptanceCriteria.length === 0) {
      return 0;
    }
    
    const invalidCount = decomposition.acceptanceCriteria.filter(ac => {
      const acText = typeof ac === 'string' ? ac : (ac.content || ac.description || '');
      return !acText.includes('Given') || !acText.includes('When') || !acText.includes('Then');
    }).length;
    
    return Math.round((1 - invalidCount / decomposition.acceptanceCriteria.length) * 100);
  }
}

module.exports = DecompositionModule;
