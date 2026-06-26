/**
 * PRD Workflow - 完整 PRD 工作流
 *
 * 功能：
 * - 深度访谈 → 需求拆解 → PRD 生成 → 评审 → 流程图 → 设计 → 原型 → 导出
 * - 迭代模式（追加/修改需求）
 * - 版本管理（回溯/对比）
 * - 环境检查前置化
 * - 流程降级策略
 * - 进度反馈机制
 * - 内容检查问答引导修补
 */

const VERSION = require('./version');
const { SmartRouter } = require('./smart_router');
const { DataBus } = require('./data_bus');
const { QualityGate } = require('./quality_gates');
const { VersionManager } = require('./version_manager');
const { RequirementDiff } = require('./requirement_diff');

// ⭐ v2.8.0 新增：流程步骤定义（用于进度显示）
// v5.0.0 新增：prd-segmented（分段确认版）
const STEPS = [
  { name: 'precheck', label: '环境检查', icon: '🔍' },
  { name: 'wiki_search', label: 'Wiki 知识搜索', icon: '📚' },  // v5.1.0 新增
  { name: 'interview', label: '深度访谈', icon: '💬' },
  { name: 'decomposition', label: '需求拆解', icon: '📦' },
  { name: 'prd', label: 'PRD 生成', icon: '📝' },
  { name: 'prd-segmented', label: 'PRD 分段确认', icon: '📝✨' },  // v5.0.0 新增
  { name: 'review', label: 'PRD 评审', icon: '🔍' },
  { name: 'flowchart', label: '流程图生成', icon: '📊' },
  { name: 'design', label: 'UI/UX 设计', icon: '🎨' },
  { name: 'prototype', label: '原型生成', icon: '🖥️' },
  { name: 'export', label: 'Word 导出', icon: '📄' },
  { name: 'quality', label: '质量审核', icon: '✅' }
];

// ⭐ v2.8.0 新增：降级策略配置
const FALLBACK_STRATEGIES = {
  'flowchart': {
    condition: 'mermaid-cli 不可用',
    action: 'skip',
    message: '跳过流程图生成，PRD 中用文字描述替代',
    fallback: { skipped: true, textDescription: '流程图未生成（环境不支持）' }
  },
  'prototype': {
    condition: 'Chrome 不可用',
    action: 'skip',
    message: '跳过原型截图，仅保留设计描述',
    fallback: { skipped: true, message: '原型截图未生成（环境不支持）' }
  },
  'quality': {
    condition: '.NET SDK 不可用',
    action: 'degrade',
    message: '跳过 OpenXML 验证，使用简化检查',
    fallback: { degraded: true, skippedOpenXml: true }
  }
};

/**

/**
 * ⭐ v2.8.0 新增：显示进度
 */
function showProgress(currentStep, totalSteps, stepInfo, allSteps) {
  const percent = Math.round((currentStep / totalSteps) * 100);
  console.log(`\n${'─'.repeat(50)}`);
  console.log(`📊 进度：${percent}% (${currentStep}/${totalSteps})`);
  console.log(`   ${stepInfo.icon} 正在执行：${stepInfo.label}`);

  // 显示已完成的步骤
  allSteps.slice(0, currentStep - 1).forEach(s => {
    console.log(`   ✅ ${s.icon} ${s.label}`);
  });

  // 显示待执行的步骤
  allSteps.slice(currentStep).forEach(s => {
    console.log(`   ⏳ ${s.icon} ${s.label}`);
  });
}

/**
 * ⭐ v2.8.0 新增：获取步骤信息
 */
function getStepInfo(stepName) {
  return STEPS.find(s => s.name === stepName) || { name: stepName, label: stepName, icon: '⚙️' };
}

/**
 * ⭐ v2.8.0 新增：检查是否可以降级
 */
function canFallback(stepName, precheckResult) {
  const strategy = FALLBACK_STRATEGIES[stepName];
  if (!strategy) return null;

  // 如果没有 precheck 结果，无法判断，返回 null（后续模块自己处理）
  if (!precheckResult || !precheckResult.checks) {
    return null;
  }

  const checks = precheckResult.checks;

  // 根据步骤检查对应依赖
  if (stepName === 'flowchart' && !checks.mermaid?.available) {
    return strategy;
  }
  if (stepName === 'prototype' && !checks.chrome?.available) {
    return strategy;
  }
  if (stepName === 'quality' && !checks.dotnet?.available) {
    return strategy;
  }

  return null;
}

/**
 * ⭐ v2.8.0 新增：强制执行 precheck（无论模板是否包含）
 */
async function ensurePrecheck(router, dataBus, options) {
  const precheckModule = router.getModule('precheck');
  if (!precheckModule) {
    console.warn('⚠️  precheck 模块不可用，跳过环境检查');
    return null;
  }

  try {
    console.log('\n🔍 强制执行环境检查...');
    const result = await precheckModule.execute({
      dataBus,
      outputDir: dataBus.outputDir
    });
    return result;
  } catch (error) {
    console.warn(`⚠️  环境检查失败：${error.message}`);
    // 返回部分结果，而不是 throw
    return {
      checks: {},
      summary: { passed: 0, total: 0, missing: [] },
      canProceed: false,
      error: error.message
    };
  }
}

/**
 * 主入口函数
 * 
 * @param {string} userInput - 用户需求
 * @param {object} options - 配置选项
 * @param {string} options.mode - 执行模式：'auto' | 'iteration' | 'fresh' | 'rollback'
 * @param {string} options.version - 版本号（用于 rollback）
 */
async function prdWorkflow(userInput, options = {}) {
  const mode = options.mode || 'auto';
  
  console.log(`🚀 启动 PRD Workflow ${VERSION.full}（模式：${mode}）...\n`);
  
  const router = new SmartRouter();
  const dataBus = new DataBus(userInput, options);
  const qualityGate = new QualityGate();
  const versionManager = new VersionManager(dataBus.outputDir);
  const requirementDiff = new RequirementDiff();
  
  // 使用传入的 AI 执行器，或创建默认
  const aiExecutor = options.aiExecutor || (async (prompt) => {
    throw new Error('aiExecutor not provided');
  });
  
  try {
    // 处理不同模式
    if (mode === 'fresh') {
      // 全新模式：清空重来
      console.log('🗑️  清空输出目录...\n');
      const fs = require('fs');
      const path = require('path');
      // 使用 dataBus.outputDir（当前需求的输出目录），而不是 options.outputDir
      const freshDir = dataBus.outputDir;
      
      // 只清空当前需求目录下的文件，保留目录本身
      if (fs.existsSync(freshDir)) {
        const files = fs.readdirSync(freshDir);
        files.forEach(file => {
          if (file !== '.versions') {
            const filePath = path.join(freshDir, file);
            if (fs.statSync(filePath).isDirectory()) {
              fs.rmSync(filePath, { recursive: true, force: true });
            } else {
              fs.unlinkSync(filePath);
            }
          }
        });
        console.log(`✅ 已清空：${freshDir}`);
      }
    } else if (mode === 'iteration') {
      // 迭代模式：创建版本 + 分析变更
      console.log('📋 分析需求变更...\n');
      const existingDecomp = dataBus.read('decomposition');
      const changes = await requirementDiff.compare(userInput, existingDecomp?.data);
      
      console.log(`📊 变更类型：${changes.type}`);
      console.log(`📝 变更摘要：${requirementDiff.generateSummary(changes)}\n`);
      
      // 创建当前版本备份（保存版本号）
      const versionBefore = versionManager.getLatestVersion();
      await versionManager.createVersion();
      const versionAfter = versionManager.getLatestVersion();
      
      // 存储版本信息供后续返回
      options._versionBefore = versionBefore;
      options._versionAfter = versionAfter;
    } else if (mode === 'rollback') {
      // 回滚模式：恢复指定版本
      const version = options.version || versionManager.getLatestVersion();
      console.log(`🔄 回滚到版本：${version}\n`);
      await versionManager.restoreVersion(version);
      return { success: true, message: `已回滚到版本 ${version}` };
    }
    
    // Step 1: 生成执行计划
    const plan = router.getExecutionPlan(userInput, dataBus.outputDir);
    
    // 迭代模式：强制重新执行 decomposition 和 prd
    if (mode === 'iteration') {
      if (!plan.skillsToExecute.includes('decomposition')) {
        plan.skillsToExecute.unshift('decomposition');
      }
      if (!plan.skillsToExecute.includes('prd')) {
        const prdIndex = plan.skillsToExecute.indexOf('decomposition');
        plan.skillsToExecute.splice(prdIndex + 1, 0, 'prd');
      }
      console.log(`\n🔄 迭代模式：强制执行 ${plan.skillsToExecute.join(' → ')}`);
    }
    
    if (plan.skillsToExecute.length === 0) {
      console.log('\n✅ 所有技能已完成，无需执行');
      return dataBus.getStatus();
    }

    // ⭐ v2.8.0 修复：无论模板是否包含 precheck，都先执行环境检查
    // 这样降级策略才能正确工作
    let precheckResult = null;
    precheckResult = await ensurePrecheck(router, dataBus, options);

    // 如果环境检查发现关键依赖缺失，提前返回
    if (precheckResult && !precheckResult.canProceed) {
      console.error('\n❌ 环境检查未通过，无法继续执行');
      console.error('   请先安装缺失的依赖');
      dataBus.releaseLock();
      throw new Error(`环境检查失败：${precheckResult.error || '关键依赖缺失'}`);
    }

    // ⭐ v5.1.0 新增：执行 Wiki 知识搜索（在访谈之前，为访谈增强提供知识）
    let wikiResult = null;
    const wikiModule = router.getModule('wiki_search');
    if (wikiModule && typeof wikiModule.searchWiki === 'function') {
      console.log('\n📚 执行 Wiki 知识搜索...');
      try {
        wikiResult = await wikiModule.searchWiki(userInput);
        if (wikiResult.enabled) {
          const moduleNames = wikiResult.matchedModules.map(m => m.module).join('、');
          console.log(`✅ Wiki 增强已启用，匹配模块：${moduleNames}`);
          // 存入 dataBus 供后续模块读取
          dataBus.write('wiki_search', wikiResult, { passed: true });
        } else {
          console.log(`ℹ️  Wiki 未启用：${wikiResult.reason}`);
          // 仍然存储结果，标记为未启用
          dataBus.write('wiki_search', wikiResult, { passed: true, enabled: false });
        }
      } catch (err) {
        console.warn(`⚠️  Wiki 搜索失败：${err.message}，将按标准方式执行`);
        wikiResult = { enabled: false, reason: err.message };
        dataBus.write('wiki_search', wikiResult, { passed: true, enabled: false });
      }
    } else {
      console.log('ℹ️  Wiki 搜索模块不可用，将按标准方式执行');
    }

    // Step 2: 执行技能链
    const results = {};

    // ⭐ v2.8.0：统计实际执行的步骤（排除 precheck 和 wiki_search）
    const executionSteps = plan.skillsToExecute.filter(s => s !== 'precheck' && s !== 'wiki_search');
    let currentStepIndex = 0;

    for (const skillId of plan.skillsToExecute) {
      // ⭐ v2.8.0 / v5.1.0：跳过 precheck 和 wiki_search（已在循环前执行）
      if (skillId !== 'precheck' && skillId !== 'wiki_search') {
        currentStepIndex++;
        const stepInfo = getStepInfo(skillId);
        showProgress(currentStepIndex, executionSteps.length, stepInfo, executionSteps.map(getStepInfo));
      }

      console.log(`\n${'='.repeat(60)}`);
      console.log(`执行技能：${skillId}`);
      console.log('='.repeat(60));

      // ⭐ v5.1.0：wiki_search 已在循环前执行，跳过
      if (skillId === 'wiki_search') {
        console.log('   ℹ️  Wiki 搜索已在访谈前完成，跳过');
        continue;
      }

      const module = router.getModule(skillId);

      if (module) {
        // ⭐ v2.8.0：检查是否可以降级
        const fallback = canFallback(skillId, precheckResult);
        if (fallback) {
          console.log(`⚠️  降级策略：${fallback.message}`);
          results[skillId] = fallback.fallback;
          dataBus.write(skillId, fallback.fallback, { passed: true, degraded: true });
          continue;
        }

        // 有模块：执行模块
        const result = await module.execute({
          dataBus,
          qualityGate,
          outputDir: dataBus.outputDir,
          autoRetry: options.autoRetry !== false,
          userInput: userInput,
          aiExecutor: aiExecutor,  // 传递 AI 执行器（仅 interview 需要）
          flowContext: {  // ✅ 新增：流程上下文
            needsInterview: plan.skillsToExecute.includes('interview'),
            flowType: plan.template || 'custom',
            allSkills: plan.skillsToExecute
          }
        });
        results[skillId] = result;

        // ⭐ v2.8.0：保存 precheck 结果供后续降级判断
        if (skillId === 'precheck') {
          precheckResult = result;
        }

        // ✅ 质量门禁检查（强制执行）
        // 注意：模块的 quality.passed 由模块自己返回，qualityGate.pass 只是记录检查
        if (result.quality && !result.quality.passed) {
          console.error(`\n❌ ${skillId} 质量门禁未通过:`);
          if (result.quality.errors) {
            result.quality.errors.forEach(err => {
              console.error(`   - ${err}`);
            });
          }
          
          // 强制失败：停止执行
          if (options.strictMode !== false) {
            console.error('\n⛔ 严格模式：停止执行');
            dataBus.releaseLock();
            throw new Error(`${skillId} 质量门禁未通过：${result.quality.errors?.join(', ') || '未知错误'}`);
          }
          
          console.warn('\n⚠️  非严格模式：继续执行（不推荐）');
        } else {
          console.log('   ✅ quality 检查通过');
        }
        
        // ⭐ v3.1.0 修改：区分形式检查和内容检查的处理方式
        // 形式检查问题 → 自动修补（规则匹配，无成本）
        // 内容检查问题 → 返回问题列表，由 AI Agent 问答引导
        if (skillId === 'review') {
          const formalIssues = result.formal?.issues?.length || 0;
          const contentIssues = result.content?.totalIssues || 0;

          // 形式检查有问题 → 自动修补
          if (formalIssues > 0 && result.overall < 80) {
            console.log(`\n⚠️  形式检查发现问题（${formalIssues}个），启动自动修补...`);

            const prdModule = router.getModule('prd');
            if (prdModule) {
              console.log('\n调用 prd_module 修补模式...');
              await prdModule.execute({
                dataBus,
                qualityGate,
                outputDir: dataBus.outputDir,
                patchMode: true,
                userInput: userInput,
                isolated: true
              });
              console.log('   ✅ 形式修补完成');
            }

            // 重新评审
            console.log('\n重新评审...');
            const reviewModule = router.getModule('review');
            const reReviewResult = await reviewModule.execute({
              dataBus,
              qualityGate,
              outputDir: dataBus.outputDir,
              aiExecutor: aiExecutor
            });

            result = reReviewResult;
            results['review'] = result;

            console.log(`\n📊 修补后评审结果：${result.overall}分`);

            if (result.overall >= 80) {
              console.log('✅ 形式修补成功，评分达标');
            }
          }

          // 内容检查有问题 → 返回问题列表，由 AI Agent 处理问答引导
          // 不在这里自动修补，AI Agent 会使用 AskUserQuestion 引导用户
          if (result.content?.totalIssues > 0) {
            console.log(`\n📋 内容检查发现 ${result.content.totalIssues} 个问题`);
            console.log('   需要通过问答引导处理，问题列表已返回');
          }
        }
      } else {
        // 无模块：AI 驱动模式（简化处理）
        console.log(`⚠️  ${skillId} 模块未实现，使用 AI 驱动模式`);
        const mockData = { mock: true, skill: skillId };
        const quality = { passed: true };
        dataBus.write(skillId, mockData, quality);
        results[skillId] = mockData;
      }
    }
    
    // Step 3: 输出状态报告
    console.log('\n' + '='.repeat(60));
    console.log('✅ PRD Workflow 完成！');
    console.log('='.repeat(60));
    
    const status = dataBus.getStatus();
    console.log(`\n📊 进度：${status.progress}`);
    console.log(`已完成：${status.completed.join(', ')}`);
    console.log(`待执行：${status.pending.join(', ') || '无'}`);
    console.log(`下一步：${status.nextStep}`);
    
    // 迭代模式版本号已经在模式处理时创建
    const finalVersion = options._versionAfter || (mode === 'iteration' ? versionManager.getLatestVersion() : null);
    
    if (mode === 'iteration' && finalVersion) {
      console.log(`\n📦 迭代版本：${options._versionBefore} → ${finalVersion}`);
    }
    
    // 释放锁
    dataBus.releaseLock();
    
    return {
      success: true,
      results: results,
      status: status,
      version: finalVersion
    };
    
  } catch (error) {
    console.error('\n❌ PRD Workflow 失败:', error.message);
    console.error(`   错误类型：${error.constructor.name}`);
    console.error(`   堆栈：${error.stack}\n`);
    
    // ✅ 确保异常时也释放锁
    if (dataBus) {
      try {
        dataBus.releaseLock();
        console.log('🔓 已释放锁');
      } catch (releaseError) {
        console.warn(`⚠️  释放锁失败：${releaseError.message}`);
      }
    }
    
    // ✅ 包装错误信息，便于 AI 理解
    const wrappedError = new Error(error.message);
    wrappedError.originalError = error;
    wrappedError.errorCode = getErrorCode(error);
    throw wrappedError;
  }
}

/**
 * 获取错误码（v2.7.0 新增）
 */
function getErrorCode(error) {
  const message = error.message.toLowerCase();
  
  if (message.includes('模块不存在') || message.includes('module')) {
    return 'MODULE_NOT_FOUND';
  }
  if (message.includes('锁') || message.includes('lock') || message.includes('并发')) {
    return 'LOCK_CONFLICT';
  }
  if (message.includes('质量') || message.includes('quality') || message.includes('门禁')) {
    return 'QUALITY_FAILED';
  }
  if (message.includes('需求拆解') || message.includes('decomposition')) {
    return 'DECOMPOSITION_ERROR';
  }
  if (message.includes('超时') || message.includes('timeout')) {
    return 'TIMEOUT';
  }
  
  return 'UNKNOWN_ERROR';
}

// 命令行入口
if (require.main === module) {
  const userInput = process.argv.slice(2).join(' ') || '生成养老规划 PRD';
  
  prdWorkflow(userInput, {
    userId: process.env.OPENCLAW_USER_ID || 'default',
    autoRetry: true
  }).then(result => {
    console.log('\n✅ 工作流执行完成！');
    console.log(`📁 输出目录：${result.outputDir}`);
    console.log(JSON.stringify(result, null, 2));
  }).catch(error => {
    console.error('\n❌ 工作流执行失败:', error.message);
    console.error(`   错误码：${getErrorCode(error)}`);
    process.exit(1);
  });
}

module.exports = { prdWorkflow, getErrorCode };
