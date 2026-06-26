/**
 * 智能路由 v2.7.0
 *
 * 解析用户需求，识别需要的技能
 * 检查前置条件，自动补充缺失技能
 * 动态编排执行流程
 *
 * 流程顺序：
 * precheck → interview → decomposition → prd → review → flowchart → design → prototype → export → quality
 *
 * v2.7.0 新增：
 * - precheck 环境检查前置化
 */

const fs = require('fs');
const path = require('path');

class SmartRouter {
  constructor() {
    // 技能定义（v2.7.0 新增 precheck，v5.1.0 新增 wiki_search）
    this.skills = {
      'precheck': { name: '环境检查', keywords: ['检查', '环境', 'precheck'], priority: 0 },
      'wiki_search': { name: 'Wiki 知识搜索', keywords: ['wiki', '知识库', 'knowledge'], priority: 0.5, autoDetect: true },
      'interview': { name: '深度访谈', keywords: ['访谈', 'grill', 'interview'], priority: 1 },
      'decomposition': { name: '需求拆解', keywords: ['拆解', '分解', 'decomposition'], priority: 2 },
      'prd': { name: 'PRD 生成', keywords: ['PRD', '文档', 'prd'], priority: 3 },
      'review': { name: 'PRD 评审', keywords: ['评审', 'review'], priority: 4 },
      'flowchart': { name: '流程图', keywords: ['流程图', 'flowchart', '图表'], priority: 5 },
      'design': { name: 'UI/UX 设计', keywords: ['设计', 'UI', 'UX', 'design'], priority: 6 },
      'prototype': { name: 'HTML 原型', keywords: ['原型', 'prototype', 'HTML'], priority: 7 },
      'export': { name: 'Word 导出', keywords: ['导出', 'Word', 'export', 'DOCX'], priority: 8 },
      'quality': { name: 'Word 质量审核', keywords: ['质量', 'quality', '审核'], priority: 9 }
    };

    // 技能依赖关系（v2.7.0 新增 precheck，v5.1.0 wiki_search 依赖 precheck）
    this.dependencies = {
      'precheck': [],
      'wiki_search': ['precheck'],
      'interview': ['precheck', 'wiki_search'],
      'decomposition': ['interview'],
      'prd': ['decomposition'],
      'prd-segmented': ['decomposition'],  // v5.0.0：分段版同样依赖需求拆解
      'review': ['prd'],  // review 也兼容 prd-segmented（main.js 自动处理）
      'flowchart': ['prd'],
      'design': ['prd'],
      'prototype': ['design'],
      'export': ['prd'],  // export 也兼容 prd-segmented
      'quality': ['export']  // 质量审核依赖导出结果
    };

    // 预定义流程模板（v2.7.0 新增 precheck，v5.0.0 新增 segmented，v5.1.0 新增 wiki_search）
    this.templates = {
      'full': ['precheck', 'wiki_search', 'interview', 'decomposition', 'prd', 'review', 'flowchart', 'design', 'prototype', 'export', 'quality'],
      'lite': ['precheck', 'wiki_search', 'interview', 'decomposition', 'prd'],
      'segmented': ['precheck', 'wiki_search', 'interview', 'decomposition', 'prd-segmented', 'review', 'export'],  // v5.0.0 新增：分段确认版
      'review-only': ['review'],
      'export-only': ['export'],
      'design-only': ['design', 'prototype'],
      'check': ['precheck']  // 新增：只检查环境
    };
  }
  
  /**
   * 解析用户需求，识别需要的技能
   * 
   * @param {string} userInput - 用户输入
   * @returns {Array<string>} 技能列表
   */
  parseUserRequest(userInput) {
    const requestedSkills = [];
    const input = userInput.toLowerCase();
    
    // 检查是否使用模板
    for (const [templateName, skills] of Object.entries(this.templates)) {
      if (input.includes(templateName) || input.includes(this.getTemplateNameCN(templateName))) {
        console.log(`✅ 使用流程模板：${templateName}`);
        return [...skills];
      }
    }
    
    // 检查是否请求完整流程
    if (input.includes('完整') || input.includes('all') || input.includes('所有')) {
      console.log('✅ 使用完整流程模板');
      return [...this.templates.full];
    }
    
    // 关键词匹配
    for (const [skillId, skillDef] of Object.entries(this.skills)) {
      for (const keyword of skillDef.keywords) {
        if (input.includes(keyword.toLowerCase())) {
          if (!requestedSkills.includes(skillId)) {
            requestedSkills.push(skillId);
            console.log(`   识别技能：${skillId}（${skillDef.name}）`);
          }
          break;
        }
      }
    }
    
    // 如果没有识别到任何技能，默认执行分段流程（v5.0.0 默认）
    if (requestedSkills.length === 0) {
      console.log('⚠️  未识别到具体技能，默认执行分段确认流程（v5.0.0）');
      return [...this.templates.segmented];
    }
    
    return requestedSkills;
  }
  
  /**
   * 获取模板中文名
   */
  getTemplateNameCN(templateName) {
    const names = {
      'full': '完整',
      'lite': '轻量',
      'segmented': '分段',  // v5.0.0 新增
      'review-only': '评审',
      'export-only': '导出',
      'design-only': '设计',
      'check': '环境检查'
    };
    return names[templateName] || templateName;
  }
  
  /**
   * 检查前置条件
   * 
   * @param {Array<string>} requestedSkills - 请求的技能列表
   * @param {string} outputDir - 输出目录
   * @returns {Array<object>} 缺失的前置条件
   */
  checkPrerequisites(requestedSkills, outputDir = './output') {
    const missingPrereqs = [];
    
    for (const skill of requestedSkills) {
      const deps = this.dependencies[skill] || [];
      
      for (const dep of deps) {
        const depFile = path.join(outputDir, `${dep}.json`);
        if (!fs.existsSync(depFile)) {
          missingPrereqs.push({
            skill: skill,
            missing: dep,
            file: depFile
          });
        }
      }
    }
    
    return missingPrereqs;
  }
  
  /**
   * 自动补充缺失的前置技能
   * 
   * @param {Array<string>} requestedSkills - 请求的技能列表
   * @param {Array<object>} missingPrereqs - 缺失的前置条件
   * @returns {Array<string>} 完整的技能列表
   */
  autoFillPrerequisites(requestedSkills, missingPrereqs) {
    const additionalSkills = missingPrereqs.map(({missing}) => {
      // v5.1.0：如果请求了 prd-segmented，export/review 依赖的 prd 视为已满足
      if (missing === 'prd' && requestedSkills.includes('prd-segmented')) {
        return null;
      }
      return missing;
    }).filter(Boolean);
    const allSkills = [...new Set([...additionalSkills, ...requestedSkills])];
    
    // 保持正确的执行顺序
    const orderedSkills = [];
    const visited = new Set();
    
    const visit = (skill) => {
      if (visited.has(skill)) return;
      visited.add(skill);
      
      // v5.1.0：跳过 prd 依赖（当 prd-segmented 已在列表中时）
      const deps = (this.dependencies[skill] || []).filter(dep => {
        if (dep === 'prd' && allSkills.includes('prd-segmented')) return false;
        return true;
      });
      deps.forEach(visit);
      orderedSkills.push(skill);
    };
    
    allSkills.forEach(visit);
    
    return orderedSkills;
  }
  
  /**
   * 获取技能执行计划
   * 
   * @param {string} userInput - 用户输入
   * @param {string} outputDir - 输出目录
   * @returns {object} 执行计划
   */
  getExecutionPlan(userInput, outputDir = './output') {
    console.log('\n📋 生成执行计划...');
    
    // Step 1: 解析用户需求
    const requestedSkills = this.parseUserRequest(userInput);
    
    // Step 2: 检查前置条件
    const missingPrereqs = this.checkPrerequisites(requestedSkills, outputDir);
    
    // Step 3: 自动补充缺失的前置技能
    let finalSkills;
    let autoFillMessage = null;
    
    if (missingPrereqs.length > 0) {
      finalSkills = this.autoFillPrerequisites(requestedSkills, missingPrereqs);
      autoFillMessage = `自动补充前置技能：${missingPrereqs.map(({missing}) => missing).join(', ')}`;
    } else {
      finalSkills = requestedSkills;
    }
    
    // Step 4: 检查已有技能（可跳过）
    const existingSkills = [];
    const skillsToExecute = [];
    
    for (const skill of finalSkills) {
      const skillFile = path.join(outputDir, `${skill}.json`);
      if (fs.existsSync(skillFile)) {
        existingSkills.push(skill);
      } else {
        skillsToExecute.push(skill);
      }
    }
    
    // 生成执行计划
    const plan = {
      requestedSkills: requestedSkills,
      allRequiredSkills: finalSkills,
      existingSkills: existingSkills,
      skillsToExecute: skillsToExecute,
      autoFillMessage: autoFillMessage,
      estimatedSteps: skillsToExecute.length
    };
    
    // 打印执行计划
    console.log('\n📋 执行计划:');
    console.log(`   请求技能：${requestedSkills.join(', ') || '无'}`);
    console.log(`   需要技能：${finalSkills.join(' → ')}`);
    if (existingSkills.length > 0) {
      console.log(`   已有结果：${existingSkills.join(', ')}（将跳过）`);
    }
    console.log(`   待执行：${skillsToExecute.join(' → ') || '无（所有技能已完成）'}`);
    console.log(`   预计步骤：${skillsToExecute.length}`);
    
    return plan;
  }
  
  /**
   * 获取技能模块（增强版 v2.7.0）
   * 
   * @param {string} skillId - 技能 ID
   * @returns {object|null} 技能模块实例，不存在返回 null
   */
  getModule(skillId) {
    const moduleMap = {
      'precheck': './modules/precheck_module.js',
      'wiki_search': './modules/wiki_search_module.js',  // v5.1.0 新增
      'interview': './modules/interview_module.js',
      'decomposition': './modules/decomposition_module.js',
      'prd': './modules/prd_module.js',
      'prd-segmented': './modules/prd_segmented_module.js',  // v5.0.0 新增：分段确认版
      'review': './modules/review_module.js',
      'optimize': './modules/optimize_module.js',
      'flowchart': './modules/flowchart_module.js',
      'quality': './modules/quality_module.js',
      'design': './modules/design_module.js',
      'prototype': './modules/prototype_module.js',
      'export': './modules/export_module.js'
    };
    
    const modulePath = moduleMap[skillId];
    if (!modulePath) {
      console.error(`❌ 未知技能：${skillId}`);
      return null;
    }
    
    // ✅ v2.7.0 新增：检查模块文件是否存在
    const fullPath = path.join(__dirname, modulePath);
    if (!fs.existsSync(fullPath)) {
      console.warn(`⚠️  技能模块文件不存在：${skillId}`);
      console.warn(`   路径：${fullPath}`);
      console.warn(`   将跳过此技能`);
      return null;
    }
    
    try {
      const ModuleExport = require(modulePath);
      // v5.1.0：wiki_search 导出函数对象，不是类，直接返回
      if (typeof ModuleExport !== 'function' && ModuleExport.searchWiki) {
        return ModuleExport;
      }
      // v5.1.0：prd_segmented 导出 { PRDSegmentedModule } 对象
      if (typeof ModuleExport !== 'function' && ModuleExport.PRDSegmentedModule) {
        return new ModuleExport.PRDSegmentedModule();
      }
      // 其他模块：类构造函数
      return new ModuleExport();
    } catch (error) {
      console.error(`❌ 加载技能模块失败：${skillId}`);
      console.error(`   错误：${error.message}`);
      return null;
    }
  }
}

module.exports = { SmartRouter };
