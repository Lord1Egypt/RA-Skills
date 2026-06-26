/**
 * PRD 生成模块 v3.0.0（模板约束版）
 * 
 * 架构升级：
 * 1. 使用 PRDTemplate 模板引擎生成结构
 * 2. 按章节调用 AI 填充内容（带 checker 约束）
 * 3. checker 检查项作为生成指导，而非事后验证
 * 4. decomposition 数据转换为 templateData 格式
 */

const fs = require('fs');
const path = require('path');
const { PRDTemplate } = require('../prd_template');
const checkItemsLoader = require('../check_items_loader.js');

class PRDModule {
  constructor() {
    this.template = new PRDTemplate();
  }

  /**
   * 执行 PRD 生成 v3.0.0
   */
  async execute(options) {
    console.log('\n📝 执行技能：PRD 生成 v3.0.0（模板约束版）');
    
    const { dataBus, qualityGate, outputDir } = options;
    
    // Step 1: 读取需求拆解结果
    const decompositionRecord = dataBus.read('decomposition');
    if (!decompositionRecord) {
      throw new Error('需求拆解结果不存在，请先执行需求拆解');
    }
    
    const decomposition = decompositionRecord.data;
    const featuresOrModules = decomposition.features || decomposition.modules || [];
    console.log(`   ✓ 已读取需求拆解：${featuresOrModules.length} 个功能`);
    
    // Step 1.5: 读取 Wiki 搜索结果（v5.1.0 新增）
    const wikiRecord = dataBus.read('wiki_search');
    const wikiEnabled = wikiRecord && wikiRecord.data && wikiRecord.data.enabled;
    let wikiContext = null;
    let wikiBusinessRules = [];
    let wikiGwtTemplates = [];
    
    if (wikiEnabled) {
      wikiContext = wikiRecord.data;
      wikiBusinessRules = wikiContext.businessRules || [];
      wikiGwtTemplates = wikiContext.gwtTemplates || [];
      const moduleNames = wikiContext.matchedModules?.map(m => m.module).join('、') || '未知';
      console.log(`   📚 Wiki 增强已启用：${moduleNames}（${wikiBusinessRules.length} 条业务规则，${wikiGwtTemplates.length} 个 GWT 模板）`);
    } else {
      console.log('   ℹ️  Wiki 未启用，按标准方式生成 PRD');
    }
    
    // Step 2: 加载检查项指导
    console.log('   📋 加载 PRD 阶段质量检查项...');
    const checkItems = await checkItemsLoader.loadForStage('prd');
    console.log(`   ✓ 已加载 ${checkItems.length} 项核心检查项`);
    
    // Step 3: 将 decomposition 转换为 templateData 格式
    console.log('   🔄 转换数据结构：decomposition → templateData...');
    const templateData = this.decompositionToTemplateData(decomposition);
    console.log(`   ✓ 已转换 ${templateData.functions.length} 个功能模块`);
    
    // Step 4: 按章节调用 AI 填充内容（带 checker 约束，启用 Wiki 时注入知识）
    console.log('   🤖 AI 填充：按章节生成内容（带 checker 约束' + (wikiEnabled ? '，Wiki 增强' : '') + '）...');
    await this.fillChaptersWithAI(templateData, decomposition, checkItems, wikiEnabled ? { wikiContext, wikiBusinessRules, wikiGwtTemplates } : null);
    console.log('   ✓ 章节内容填充完成');
    
    // Step 5: 使用模板生成 PRD
    console.log('   📄 模板引擎：生成 PRD 文档...');
    const prdContent = this.template.generatePRD(templateData);
    
    // Step 6: 保存 PRD
    const prdPath = path.join(outputDir, 'PRD.md');
    fs.writeFileSync(prdPath, prdContent, 'utf8');
    console.log(`   ✅ 保存：${prdPath}`);
    
    // Step 7: 质量验证（基于 checker）
    const quality = this.validatePRDWithChecker(prdContent, decomposition, checkItems);
    
    // Step 8: 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate3_prd', {
        chapters: this.extractChapters(prdContent),
        quality: quality,
        templateUsed: true
      });
    }
    
    return {
      content: prdContent,
      chapters: this.extractChapters(prdContent),
      markdownPath: prdPath,
      quality: quality,
      templateVersion: this.template.version
    };
  }
  
  /**
   * 将 decomposition 数据转换为 templateData 格式
   */
  decompositionToTemplateData(decomposition) {
    // 支持 features 或 modules 字段
    const featuresOrModules = decomposition.features || decomposition.modules || [];
    
    const templateData = {
      version: 'v3.0.0',
      overview: {
        productName: decomposition.productName || '产品需求文档',
        productBackground: decomposition.background || '',
        productGoals: decomposition.value ? [{
          type: '核心价值',
          description: decomposition.value,
          metric: '用户满意度',
          target: '提升 80%'
        }] : [],
        targetUsers: [],
        functionList: featuresOrModules.map(f => ({
          name: f.name,
          priority: f.priority || 'P0',
          estimatedDays: this.estimateDays(f.priority),
          status: '待开发'
        }))
      },
      globalFlow: {
        mainFlowchart: null,
        globalRules: featuresOrModules.flatMap(f => f.businessRules || []).map((rule, idx) => ({
          id: rule.id || `BR-${String(idx + 1).padStart(3, '0')}`,
          name: rule.name || rule.description?.substring(0, 20) || '业务规则',
          description: rule.description || '',
          scope: '全部功能'
        })),
        globalData: []
      },
      functions: featuresOrModules.map((f, i) => ({
        featureId: f.id || `MOD-${String(i + 1).padStart(3, '0')}`,
        name: f.name,
        priority: f.priority || 'P0',
        description: f.description || '',
        userStories: f.userStories || [],
        businessRules: f.businessRules || [],
        acceptanceCriteria: f.acceptanceCriteria || [],
        inputDefinition: [],
        outputDefinition: [],
        exceptionHandling: [],
        flowcharts: {
          mainFlow: null,
          sequence: null
        },
        prototype: null
      })),
      nonFunctional: {
        performance: [],
        security: [],
        compatibility: []
      },
      appendix: {
        revisionHistory: [{
          version: 'v3.0.0',
          date: new Date().toISOString().split('T')[0],
          description: '初始版本（模板约束版）',
          author: 'AI',
          status: '草稿'
        }],
        references: [],
        pendingItems: []
      }
    };
    
    return templateData;
  }
  
  /**
   * 估算开发天数
   */
  estimateDays(priority) {
    switch (priority) {
      case 'P0': return '3-5 天';
      case 'P1': return '2-3 天';
      case 'P2': return '1-2 天';
      default: return '待评估';
    }
  }
  
  /**
   * 按章节调用 AI 填充内容（带 checker 约束，可选 Wiki 增强）
   */
  async fillChaptersWithAI(templateData, decomposition, checkItems, wikiData = null) {
    // 支持 features 或 modules 字段
    const featuresOrModules = decomposition.features || decomposition.modules || [];
    
    // 按章节分组检查项
    const chapterCheckers = this.groupCheckersByChapter(checkItems);
    
    // 填充概述章节
    templateData.overview = await this.fillOverviewChapter(templateData.overview, decomposition, chapterCheckers.overview, wikiData);
    
    // 填充全局业务流程章节
    templateData.globalFlow = await this.fillGlobalFlowChapter(templateData.globalFlow, decomposition, chapterCheckers.globalFlow, wikiData);
    
    // 填充每个功能章节
    for (let i = 0; i < templateData.functions.length; i++) {
      const func = templateData.functions[i];
      const decompositionFeature = featuresOrModules[i];
      const funcCheckers = chapterCheckers.function || [];
      
      templateData.functions[i] = await this.fillFunctionChapter(func, decompositionFeature, funcCheckers, wikiData);
    }
    
    // 填充非功能需求章节
    templateData.nonFunctional = await this.fillNonFunctionalChapter(templateData.nonFunctional, decomposition, chapterCheckers.nonFunctional, wikiData);
  }
  
  /**
   * 按章节分组检查项
   */
  groupCheckersByChapter(checkItems) {
    const groups = {
      overview: [],
      globalFlow: [],
      function: [],
      nonFunctional: [],
      appendix: []
    };
    
    checkItems.forEach(item => {
      if (item.id?.includes('用户角色') || item.id?.includes('业务目标')) {
        groups.overview.push(item);
      } else if (item.id?.includes('业务流程') || item.id?.includes('数据字典')) {
        groups.globalFlow.push(item);
      } else if (item.id?.includes('业务规则') || item.id?.includes('输入输出') || item.id?.includes('异常处理')) {
        groups.function.push(item);
      } else if (item.id?.includes('性能') || item.id?.includes('安全')) {
        groups.nonFunctional.push(item);
      }
    });
    
    return groups;
  }
  
  /**
   * 填充概述章节
   */
  async fillOverviewChapter(overview, decomposition, checkers, wikiData = null) {
    const checkerPrompt = this.buildCheckerPrompt(checkers);
    const wikiPrompt = this.buildWikiPrompt(wikiData, 'overview');
    
    const prompt = `
你是产品经理，请完善产品概述章节。

${checkerPrompt}${wikiPrompt}
## 输入数据
- 产品背景：${overview.productBackground}
- 核心价值：${JSON.stringify(overview.productGoals)}
- 功能列表：${JSON.stringify(overview.functionList)}

## 输出要求
1. 补充目标用户画像（年龄、收入、痛点）
2. 细化业务目标（量化指标）
3. 完善功能列表描述

请返回 JSON 格式数据。
`;
    
    try {
      const result = await sessions_spawn({
        runtime: 'subagent',
        mode: 'run',
        task: prompt,
        timeoutSeconds: 120
      });
      
      // 合并 AI 生成内容
      const aiData = typeof result === 'string' ? JSON.parse(result) : result;
      return { ...overview, ...aiData };
    } catch (e) {
      console.log('   ⚠️ 概述章节 AI 填充失败，使用默认数据');
      return overview;
    }
  }
  
  /**
   * 填充全局业务流程章节
   */
  async fillGlobalFlowChapter(globalFlow, decomposition, checkers, wikiData = null) {
    const checkerPrompt = this.buildCheckerPrompt(checkers);
    const wikiPrompt = this.buildWikiPrompt(wikiData, 'globalFlow');
    const featuresOrModules = decomposition.features || decomposition.modules || [];
    
    const prompt = `
你是系统架构师，请设计全局业务流程。

${checkerPrompt}${wikiPrompt}
## 输入数据
- 功能列表：${JSON.stringify(featuresOrModules.map(f => f.name))}
- 业务规则：${JSON.stringify(globalFlow.globalRules)}

## 输出要求
1. 生成主业务流程图（Mermaid 语法）
2. 补充全局数据定义
3. 完善业务规则描述

请返回 JSON 格式，包含 mainFlowchart（Mermaid 字符串）和 globalData 数组。
`;
    
    try {
      const result = await sessions_spawn({
        runtime: 'subagent',
        mode: 'run',
        task: prompt,
        timeoutSeconds: 120
      });
      
      const aiData = typeof result === 'string' ? JSON.parse(result) : result;
      return { ...globalFlow, ...aiData };
    } catch (e) {
      console.log('   ⚠️ 全局流程章节 AI 填充失败，使用默认数据');
      return globalFlow;
    }
  }
  
  /**
   * 填充功能章节（核心）
   */
  async fillFunctionChapter(func, decompositionFeature, checkers, wikiData = null) {
    const checkerPrompt = this.buildCheckerPrompt(checkers);
    const wikiPrompt = this.buildWikiPrompt(wikiData, 'function', func.name);
    
    const prompt = `
你是系统设计专家，请细化功能规格。

${checkerPrompt}${wikiPrompt}
## 输入数据
- 功能名称：${func.name}
- 功能描述：${func.description}
- 业务规则：${JSON.stringify(func.businessRules)}
- 用户故事：${JSON.stringify(func.userStories)}

## 输出要求
1. 每个功能细化到字段级规格（输入/输出定义）
2. 业务流程用泳道图/时序图表示（Mermaid 语法）
3. 异常处理包含异常码 + 触发条件 + 处理方式
4. 输入输出定义完整（类型/必填/约束/示例）
5. **验收标准（GWT 格式）**：基于业务规则和用户故事生成验收标准
   - 每条验收标准必须包含：Given（前置条件）、When（操作/事件）、Then（预期结果）
   - 验收标准要覆盖所有业务规则
   - 验收标准要验证用户故事的实现
   - 使用中文 GWT 格式（Given...When...Then...）
6. **原型设计**：包含 ASCII 布局描述 + 交互说明

请返回 JSON 格式，包含：
- inputDefinition: 数组（字段名、类型、必填、约束、示例）
- outputDefinition: 数组（字段名、类型、说明、示例）
- exceptionHandling: 数组（异常类型、触发条件、错误码、处理方式）
- acceptanceCriteria: 数组（GWT 格式字符串，每条包含 Given/When/Then）
- flowcharts: 对象（mainFlow: Mermaid 字符串，sequence: Mermaid 字符串）
- prototype: 对象（pages 数组、layout ASCII 字符串、interactions 数组、files 对象）

## 原型设计要求

**pages 数组**（示例格式）：
{
  "pages": [
    {
      "name": "${func.name}页",
      "description": "主功能页面",
      "priority": "P0"
    }
  ]
}

**layout ASCII 布局**（用文本字符画界面，示例）：
┌─────────────────────────────────────────┐
│  [筛选条件区域]                          │
│  [产品筛选 ▼]  [日期选择]  [查询 按钮]   │
├─────────────────────────────────────────┤
│                                         │
│        [主要内容区域]                    │
│        - 雷达图/图表/列表                │
│                                         │
├─────────────────────────────────────────┤
│  [底部操作栏]                            │
│  [导出 按钮]  [分享 按钮]                │
└─────────────────────────────────────────┘

**interactions 数组**（示例格式）：
{
  "interactions": [
    {
      "element": "查询按钮",
      "type": "点击",
      "description": "校验筛选条件后加载数据"
    }
  ]
}

**files 对象**：
{
  "files": {
    "html": "prototypes/${func.name.toLowerCase()}.html",
    "png": "prototypes/${func.name.toLowerCase()}.png"
  }
}
`;
    
    try {
      const result = await sessions_spawn({
        runtime: 'subagent',
        mode: 'run',
        task: prompt,
        timeoutSeconds: 180
      });
      
      const aiData = typeof result === 'string' ? JSON.parse(result) : result;
      return { ...func, ...aiData };
    } catch (e) {
      console.log(`   ⚠️ 功能 ${func.name} AI 填充失败，使用默认数据`);
      return func;
    }
  }
  
  /**
   * 填充非功能需求章节
   */
  async fillNonFunctionalChapter(nonFunctional, decomposition, checkers, wikiData = null) {
    const checkerPrompt = this.buildCheckerPrompt(checkers);
    const wikiPrompt = this.buildWikiPrompt(wikiData, 'nonFunctional');
    
    const prompt = `
你是技术架构师，请定义非功能需求。

${checkerPrompt}${wikiPrompt}
## 输出要求
1. 性能指标（响应时间、吞吐量、并发量）
2. 安全要求（权限、加密、审计）
3. 兼容性要求（浏览器、设备、系统）

请返回 JSON 格式，包含 performance、security、compatibility 数组。
`;
    
    try {
      const result = await sessions_spawn({
        runtime: 'subagent',
        mode: 'run',
        task: prompt,
        timeoutSeconds: 120
      });
      
      const aiData = typeof result === 'string' ? JSON.parse(result) : result;
      return { ...nonFunctional, ...aiData };
    } catch (e) {
      console.log('   ⚠️ 非功能需求章节 AI 填充失败，使用默认数据');
      return nonFunctional;
    }
  }
  
  /**
   * 构建 checker 提示词
   */
  buildCheckerPrompt(checkers) {
    if (!checkers || checkers.length === 0) {
      return '';
    }
    
    let prompt = '## 质量检查项（必须满足）\n\n';
    checkers.forEach((item, idx) => {
      prompt += `${idx + 1}. ${item.name || item.id || '检查项'}\n`;
      if (item.checkPoints && item.checkPoints.length > 0) {
        item.checkPoints.forEach(cp => {
          prompt += `   - [ ] ${cp}\n`;
        });
      }
    });
    prompt += '\n';
    
    return prompt;
  }

  /**
   * 构建 Wiki 知识提示词（v5.1.0 新增）
   */
  buildWikiPrompt(wikiData, chapter, featureName = null) {
    if (!wikiData) return '';
    
    let prompt = '';
    
    // 注入 Wiki 知识摘要
    if (wikiData.wikiContext) {
      prompt += '## 📚 Wiki 知识库上下文（已匹配到相关业务模块）\n\n';
      for (const ctx of wikiData.wikiContext) {
        prompt += `### ${ctx.module}（${ctx.code}）\n`;
        prompt += `匹配关键词：${ctx.matchedKeywords.join('、')}\n`;
        for (const doc of ctx.documents) {
          prompt += `\n#### ${doc.file}\n`;
          prompt += doc.content.substring(0, 3000) + '\n';
        }
      }
      prompt += '\n';
    }
    
    // 注入业务规则
    if (wikiData.wikiBusinessRules && wikiData.wikiBusinessRules.length > 0) {
      prompt += '## 📋 Wiki 业务规则（请在 PRD 中遵循）\n\n';
      wikiData.wikiBusinessRules.slice(0, 15).forEach((rule, idx) => {
        prompt += `${idx + 1}. 【${rule.module}】${rule.rule}\n`;
      });
      prompt += '\n';
    }
    
    // 注入 GWT 模板
    if (wikiData.wikiGwtTemplates && wikiData.wikiGwtTemplates.length > 0) {
      prompt += '## ✅ Wiki GWT 模板（参考已有验收标准格式）\n\n';
      wikiData.wikiGwtTemplates.slice(0, 8).forEach((tpl, idx) => {
        prompt += `${idx + 1}. 【${tpl.module}】${tpl.feature} - ${tpl.scenario}\n`;
        prompt += `${tpl.template}\n\n`;
      });
    }
    
    return prompt;
  }
  
  /**
   * 验证 PRD 质量（基于 checker）
   */
  validatePRDWithChecker(prdContent, decomposition, checkItems) {
    const errors = [];
    const warnings = [];
    
    // 检查章节完整性
    const requiredChapters = ['产品概述', '业务流程', '功能', '异常处理'];
    requiredChapters.forEach(chapter => {
      if (!prdContent.includes(chapter)) {
        errors.push(`缺少章节：${chapter}`);
      }
    });
    
    // 检查 checker 覆盖
    checkItems.forEach(item => {
      // 简化验证：检查关键词是否存在
      if (item.name && !prdContent.includes(item.name)) {
        warnings.push(`检查项 "${item.name}" 可能未满足`);
      }
    });
    
    return {
      passed: errors.length === 0,
      errors: errors,
      warnings: warnings,
      chaptersComplete: requiredChapters.length - errors.length,
      checkerCoverage: checkItems.length - warnings.length
    };
  }
  
  /**
   * 验证 PRD 质量（旧版兼容）
   */
  validatePRD(prdContent, decomposition) {
    return this.validatePRDWithChecker(prdContent, decomposition, []);
  }
  
  /**
   * 提取章节
   */
  extractChapters(prdContent) {
    const chapterRegex = /^##\s+(.+)$/gm;
    const chapters = [];
    let match;
    
    while ((match = chapterRegex.exec(prdContent)) !== null) {
      chapters.push(match[1]);
    }
    
    return chapters;
  }
  
  /**
   * 验证一致性
   */
  validateConsistency(decomposition) {
    const errors = [];
    const featuresOrModules = decomposition.features || decomposition.modules || [];
    
    if (!featuresOrModules || featuresOrModules.length === 0) {
      errors.push('功能清单为空');
    }
    
    return {
      passed: errors.length === 0,
      errors: errors
    };
  }
}

module.exports = PRDModule;
