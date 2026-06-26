/**
 * PRD 评审模块 v3.1.0
 *
 * 评审 PRD 文档，追踪问题修复
 *
 * v3.0.0 新增：
 * - 形式检查 + 内容检查分层架构
 * - 13项内容质量检查（AI驱动）
 * - 内容检查结果返回，供问答引导使用
 *
 * v3.1.0 新增：
 * - 问答引导修补功能
 * - fixIssue() 单问题修补
 * - applyFix() 应用修补到 PRD
 * - getFixOptions() 获取修补选项
 */

const fs = require('fs');
const path = require('path');

class ReviewModule {
  /**
   * 执行 PRD 评审
   */
  async execute(options) {
    console.log('\n🔍 执行技能：PRD 评审');

    const { dataBus, qualityGate, outputDir, aiExecutor } = options;

    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }

    const prd = prdRecord.data;

    // ========== 阶段1：形式检查（规则匹配）==========
    console.log('\n📋 阶段1：形式检查（规则匹配）');
    const formalResult = await this.executeFormalReview(prd);

    // 检查是否有上一轮评审
    const previousReview = dataBus.read('review');
    if (previousReview) {
      console.log('   对比上一轮评审，追踪问题修复...');
      formalResult.fixTracking = this.trackFixes(previousReview.data, formalResult);
    }

    // 质量验证
    const quality = this.validateReview(formalResult);

    // ========== 阶段2：内容检查（AI驱动）==========
    console.log('\n🤖 阶段2：内容检查（AI驱动）');

    // ✅ 使用 aiExecutor（OpenClaw 架构）
    if (aiExecutor) {
      const contentResult = await this.executeContentReviewWithAI(prd, aiExecutor);

      // 合并结果
      const reviewResult = {
        // 形式检查结果
        formal: {
          issues: formalResult.issues || [],
          suggestions: formalResult.suggestions || [],
          scores: formalResult.check_results || {},
          overall: formalResult.overall_score || 0,
          scenario: formalResult.scenario || 'default'
        },
        // 内容检查结果
        content: {
          totalIssues: contentResult.total_issues || 0,
          coreIssues: contentResult.core_issues || 0,
          improveIssues: contentResult.improve_issues || 0,
          optimizeIssues: contentResult.optimize_issues || 0,
          issues: contentResult.issues || [],
          groupedIssues: contentResult.grouped_issues || {}
        },
        // 综合评分
        overall: this.calculateOverallScore(formalResult, contentResult)
      };

      // 写入数据总线
      const filepath = dataBus.write('review', reviewResult, quality, {
        reviewedPRD: 'prd.json'
      });

      // 门禁检查
      if (qualityGate) {
        await qualityGate.pass('gate4_review', reviewResult);
      }

      return {
        ...reviewResult,
        quality: quality,
        outputPath: filepath
      };
    } else {
      // 无 aiExecutor 时跳过内容检查
      console.warn('⚠️  aiExecutor 未提供，跳过内容检查');

      const reviewResult = {
        formal: {
          issues: formalResult.issues || [],
          suggestions: formalResult.suggestions || [],
          scores: formalResult.check_results || {},
          overall: formalResult.overall_score || 0,
          scenario: formalResult.scenario || 'default'
        },
        content: {
          totalIssues: 0,
          issues: [],
          skipped: true,
          reason: 'aiExecutor not provided'
        },
        overall: formalResult.overall_score || 0
      };

      const filepath = dataBus.write('review', reviewResult, quality);

      return {
        ...reviewResult,
        quality: quality,
        outputPath: filepath
      };
    }
  }

  /**
   * 执行形式检查（原有逻辑）
   */
  async executeFormalReview(prd) {
    const { execSync } = require('child_process');
    const fs = require('fs');
    const path = require('path');

    // requirement-reviewer CLI 路径
    const reviewCliPath = path.join(__dirname, '../../skills/requirement-reviewer/engines/review_cli.py');

    // 检查脚本是否存在
    if (!fs.existsSync(reviewCliPath)) {
      console.warn('⚠️  requirement-reviewer 脚本不存在，使用备用方案');
      return this.executeFallbackReview(prd);
    }

    // 临时保存 PRD 内容
    const tempPrdPath = path.join(__dirname, '../temp_prd_for_review.md');
    fs.writeFileSync(tempPrdPath, prd.content || '', 'utf8');

    try {
      console.log('   调用形式检查引擎...');

      // 调用 review_cli.py（只评审，不迭代）
      const result = execSync(
        `python3 "${reviewCliPath}" --prd "${tempPrdPath}" --format json --auto-detect`,
        { encoding: 'utf8' }
      );

      // 解析 JSON 结果
      const reviewResult = JSON.parse(result);

      // 清理临时文件
      try { fs.unlinkSync(tempPrdPath); } catch (e) {}

      console.log(`   ✅ 形式检查完成：总分${reviewResult.overall_score}/100`);
      console.log(`   ✅ 问题数：${reviewResult.total_issues}（严重：${reviewResult.critical_issues}）`);

      // 转换为 prd-workflow 期望的格式
      return {
        issues: reviewResult.issues || [],
        suggestions: reviewResult.suggestions || [],
        check_results: reviewResult.check_results || {},
        overall_score: reviewResult.overall_score || 0,
        total_issues: reviewResult.total_issues || 0,
        critical_issues: reviewResult.critical_issues || 0,
        scenario: reviewResult.scenario || 'default'
      };

    } catch (error) {
      console.warn('⚠️  形式检查调用失败，使用备用方案');
      console.warn('   错误:', error.message);
      try { fs.unlinkSync(tempPrdPath); } catch (e) {}
      return this.executeFallbackReview(prd);
    }
  }

  /**
   * 执行内容检查（使用 aiExecutor）
   *
   * 流程：
   * 1. 调用 Python CLI 获取检查任务列表
   * 2. 对每个任务使用 aiExecutor 调用 AI
   * 3. 整合检查结果
   */
  async executeContentReviewWithAI(prd, aiExecutor) {
    const { execSync } = require('child_process');
    const fs = require('fs');
    const path = require('path');

    // 任务提取 CLI 路径
    const tasksCliPath = path.join(__dirname, '../../skills/requirement-reviewer/engines/get_tasks_cli.py');

    // 检查脚本是否存在
    if (!fs.existsSync(tasksCliPath)) {
      console.warn('⚠️  任务提取脚本不存在，跳过内容检查');
      return { total_issues: 0, issues: [] };
    }

    // 临时保存 PRD 内容
    const tempPrdPath = path.join(__dirname, '../temp_prd_for_tasks.md');
    fs.writeFileSync(tempPrdPath, prd.content || '', 'utf8');

    try {
      // 1. 获取检查任务列表
      console.log('   步骤1：提取检查任务...');
      const tasksResult = execSync(
        `python3 "${tasksCliPath}" --prd "${tempPrdPath}" --format json`,
        { encoding: 'utf8' }
      );

      const tasksData = JSON.parse(tasksResult);
      const tasks = tasksData.tasks || [];

      console.log(`   ✅ 提取到 ${tasks.length} 个检查任务`);

      // 2. 执行 AI 检查
      console.log('   步骤2：执行 AI 检查...');
      const allIssues = [];

      for (let i = 0; i < tasks.length; i++) {
        const task = tasks[i];
        console.log(`      检查 [${i + 1}/${tasks.length}]: ${task.check_item.name}...`);

        // 构建检查 Prompt
        const prompt = this.buildCheckPrompt(task);

        // 使用 aiExecutor 调用 AI
        try {
          const aiResponse = await aiExecutor(prompt);

          // 解析 AI 返回结果
          const issues = this.parseAIResponse(aiResponse, task);
          allIssues.push(...issues);

        } catch (aiError) {
          console.warn(`      ⚠️ AI 检查失败: ${aiError.message}`);
          // AI 检查失败时跳过该任务
        }
      }

      // 3. 按优先级分组
      const coreIssues = allIssues.filter(i => i.priority === 'core');
      const improveIssues = allIssues.filter(i => i.priority === 'improve');
      const optimizeIssues = allIssues.filter(i => i.priority === 'optimize');

      // 清理临时文件
      try { fs.unlinkSync(tempPrdPath); } catch (e) {}

      console.log(`   ✅ 内容检查完成：共 ${allIssues.length} 个问题`);
      console.log(`      核心问题：${coreIssues.length}`);
      console.log(`      完善问题：${improveIssues.length}`);
      console.log(`      优化问题：${optimizeIssues.length}`);

      return {
        total_issues: allIssues.length,
        core_issues: coreIssues.length,
        improve_issues: improveIssues.length,
        optimize_issues: optimizeIssues.length,
        issues: allIssues,
        grouped_issues: {
          core: coreIssues,
          improve: improveIssues,
          optimize: optimizeIssues
        }
      };

    } catch (error) {
      console.warn('⚠️  内容检查调用失败，跳过');
      console.warn('   错误:', error.message);
      try { fs.unlinkSync(tempPrdPath); } catch (e) {}
      return { total_issues: 0, issues: [] };
    }
  }

  /**
   * 构建检查 Prompt
   */
  buildCheckPrompt(task) {
    const checkItem = task.check_item;
    const checkPoints = checkItem.check_points.map(p => `  - ${p}`).join('\n');

    return `你是一个专业的软件需求文档评审专家。请检查以下内容是否符合"${checkItem.name}"的要求。

## 检查项说明
- 名称：${checkItem.name}
- 描述：${checkItem.description}
- 检查要点：
${checkPoints}

## 良好示例
${checkItem.example_good}

## 不良示例
${checkItem.example_bad}

## 待检查内容
章节：${task.section.title}
内容：
\`\`\`
${task.content}
\`\`\`

## 检查要求
1. 仔细阅读内容，判断是否符合检查项要求
2. 如果存在问题，请明确指出问题所在
3. 给出具体的修补建议
4. 引用原文中有问题的部分

## 话术要求（重要）

请使用**温柔话术（建议式）**，帮助用户完善文档，而不是挑毛病：

- ✅ 用"如果能...会更完整"代替"未说明..."
- ✅ 用"建议补充"代替"缺失"
- ✅ 用"可以考虑"代替"必须"
- ✅ 用"可能需要"代替"缺少"
- ✅ 用"建议优化"代替"错误"
- ✅ 拿不准时温柔建议，让用户自己判断

**示例对比**：
- ❌ "缺少异常处理说明"
- ✅ "如果能补充异常场景的处理方式，会更完整"

- ❌ "未说明输入格式"
- ✅ "建议补充输入数据的格式说明，方便开发理解"

- ❌ "流程描述不清晰"
- ✅ "如果能添加具体步骤和分支流程，会更清晰"

## 输出格式（JSON）
\`\`\`json
{
  "passed": true/false,
  "issues": [
    {
      "description": "问题描述（使用温柔话术）",
      "suggestion": "修补建议（建议式）",
      "original_text": "原文引用（如果适用）"
    }
  ]
}
\`\`\`

请直接输出 JSON，不要有其他内容。`;
  }

  /**
   * 解析 AI 返回结果
   */
  parseAIResponse(aiResponse, task) {
    const issues = [];

    try {
      // 提取 JSON
      let jsonMatch = aiResponse;
      if (typeof aiResponse === 'object') {
        // aiExecutor 可能返回对象
        jsonMatch = aiResponse.content || aiResponse.result || JSON.stringify(aiResponse);
      }

      if (typeof jsonMatch === 'string') {
        if (jsonMatch.includes('```json')) {
          jsonMatch = jsonMatch.split('```json')[1].split('```')[0];
        } else if (jsonMatch.includes('```')) {
          jsonMatch = jsonMatch.split('```')[1].split('```')[0];
        }
      }

      const result = JSON.parse(jsonMatch.trim());

      if (!result.passed && result.issues) {
        for (const issueData of result.issues) {
          issues.push({
            id: `${task.check_item.id}-${issues.length}`,
            check_item_id: task.check_item.id,
            check_item_name: task.check_item.name,
            priority: task.check_item.priority,
            section_title: task.section.title,
            description: issueData.description || '',
            suggestion: issueData.suggestion || '',
            original_text: issueData.original_text || ''
          });
        }
      }

    } catch (parseError) {
      console.warn(`      ⚠️ JSON 解析失败: ${parseError.message}`);
    }

    return issues;
  }

  /**
   * 执行内容检查（旧方法 - Python直接调用API，已废弃）
   * @deprecated 使用 executeContentReviewWithAI 替代
   */
  async executeContentReview(prd) {
    console.warn('⚠️  executeContentReview 已废弃，请使用 executeContentReviewWithAI');
    return { total_issues: 0, issues: [] };
  }

  /**
   * 计算综合评分
   */
  calculateOverallScore(formalResult, contentResult) {
    // 形式检查评分（权重60%）
    const formalScore = formalResult.overall_score || 0;

    // 内容检查评分（权重40%）
    // 基于问题数量扣分
    const totalIssues = contentResult.total_issues || 0;
    const coreIssues = contentResult.core_issues || 0;
    const improveIssues = contentResult.improve_issues || 0;

    // 核心问题扣15分，完善问题扣10分，优化问题扣5分
    const deduction = coreIssues * 15 + improveIssues * 10 + (totalIssues - coreIssues - improveIssues) * 5;
    const contentScore = Math.max(0, 100 - deduction);

    // 综合评分
    const overall = Math.round(formalScore * 0.6 + contentScore * 0.4);

    return overall;
  }

  /**
   * 备用评审方案（当 requirement-reviewer 不可用时）
   */
  async executeFallbackReview(prd) {
    // 从 prd 内容中提取章节信息
    const chapters = this.extractChapters(prd.content || '');
    const issues = [];

    // 检查章节完整性
    const requiredChapters = ['需求概述', '用户场景', '功能', '验收标准', '非功能需求'];
    requiredChapters.forEach(chapter => {
      if (!chapters.some(c => c.includes(chapter))) {
        issues.push({
          id: `issue-${issues.length + 1}`,
          type: 'completeness',
          severity: 'high',
          description: `缺失${chapter}章节`,
          location: chapter,
          suggestion: `补充${chapter}内容`
        });
      }
    });

    // 如果没有问题，返回通过
    if (issues.length === 0) {
      return {
        issues: [],
        suggestions: ['PRD 结构完整，内容清晰'],
        check_results: {
          completeness: 100,
          consistency: 100,
          terminology: 100,
          acceptanceCriteria: 100
        },
        overall_score: 100,
        total_issues: 0,
        critical_issues: 0
      };
    }

    // 有问题的情况
    return {
      issues,
      suggestions: ['建议补充缺失的章节'],
      check_results: {
        completeness: 100 - (issues.length * 10),
        consistency: 90,
        terminology: 95,
        acceptanceCriteria: 85
      },
      overall_score: 100 - (issues.length * 10),
      total_issues: issues.length,
      critical_issues: issues.filter(i => i.severity === 'high').length
    };
  }

  /**
   * 提取章节列表
   */
  extractChapters(content) {
    const chapterRegex = /^##\s+(.+)/gm;
    const chapters = [];
    let match;
    while ((match = chapterRegex.exec(content)) !== null) {
      chapters.push(match[1]);
    }
    return chapters;
  }

  /**
   * 代码验证：检查评审质量
   */
  async validateReview(reviewResult) {
    const errors = [];

    // 检查评分
    if (reviewResult.overall === undefined) {
      errors.push('缺少整体评分');
    }

    return {
      passed: errors.length === 0,
      errors: errors,
      issuesIdentified: (reviewResult.formal?.issues?.length > 0) || (reviewResult.content?.totalIssues > 0)
    };
  }

  /**
   * 追踪问题修复
   */
  trackFixes(previousReview, currentReview) {
    const tracking = {
      previousIssues: previousReview.formal?.issues || [],
      currentIssues: currentReview.formal?.issues || [],
      fixed: [],
      unresolved: [],
      new: []
    };

    // 检查已修复的问题
    tracking.previousIssues.forEach(prevIssue => {
      const stillExists = tracking.currentIssues.find(currIssue =>
        currIssue.description === prevIssue.description
      );

      if (stillExists) {
        tracking.unresolved.push(prevIssue);
      } else {
        tracking.fixed.push(prevIssue);
      }
    });

    // 检查新问题
    tracking.currentIssues.forEach(currIssue => {
      const existedBefore = tracking.previousIssues.find(prevIssue =>
        prevIssue.description === currIssue.description
      );

      if (!existedBefore) {
        tracking.new.push(currIssue);
      }
    });

    // 计算修复率
    const totalPrevious = tracking.previousIssues.length;
    const fixedCount = tracking.fixed.length;
    const fixRate = totalPrevious > 0 ? (fixedCount / totalPrevious) * 100 : 100;

    tracking.fixRate = Math.round(fixRate * 100) / 100;
    tracking.summary = `已修复 ${fixedCount}/${totalPrevious} 个问题 (${tracking.fixRate}%)`;

    return tracking;
  }

  // ========== v3.1.0 新增：问答引导修补功能 ==========

  /**
   * 获取问题的修补选项
   *
   * 返回供用户选择的3个选项
   */
  getFixOptions(issue) {
    return {
      issue: issue,
      options: [
        {
          id: 'auto_fix',
          label: 'AI 自动修补',
          description: '让 AI 根据检查建议自动生成修补内容',
          action: 'auto'
        },
        {
          id: 'user_guide',
          label: '告诉 AI 如何修补',
          description: '你提供修补思路，AI 按你的要求生成内容',
          action: 'user_guide'
        },
        {
          id: 'skip',
          label: '误报跳过',
          description: '标记为误报，不处理此问题',
          action: 'skip'
        }
      ]
    };
  }

  /**
   * 执行单问题修补
   *
   * @param {object} issue - 问题对象
   * @param {string} action - 处理方式：'auto' | 'user_guide' | 'skip'
   * @param {string} userInstruction - 用户指令（action='user_guide'时使用）
   * @param {object} prd - PRD 对象
   * @param {function} aiExecutor - AI 执行器
   * @returns {object} 修补结果
   */
  async fixIssue(issue, action, userInstruction, prd, aiExecutor) {
    console.log(`\n🔧 处理问题：${issue.check_item_name}`);
    console.log(`   章节：${issue.section_title}`);
    console.log(`   问题：${issue.description}`);
    console.log(`   处理方式：${action}`);

    if (action === 'skip') {
      // 误报跳过
      console.log('   ✅ 标记为误报，跳过处理');
      return {
        success: true,
        action: 'skip',
        issue: issue,
        message: '已标记为误报'
      };
    }

    // 构建修补 Prompt
    const fixPrompt = this.buildFixPrompt(issue, prd, action === 'user_guide' ? userInstruction : null);

    try {
      // 调用 AI 生成修补内容
      const fixContent = await aiExecutor(fixPrompt);

      // 解析修补内容
      const parsedFix = this.parseFixContent(fixContent);

      console.log('   ✅ AI 生成修补内容成功');

      return {
        success: true,
        action: action,
        issue: issue,
        fixContent: parsedFix,
        message: '修补内容已生成'
      };

    } catch (error) {
      console.warn(`   ⚠️ 修补生成失败: ${error.message}`);
      return {
        success: false,
        action: action,
        issue: issue,
        error: error.message
      };
    }
  }

  /**
   * 构建修补 Prompt
   */
  buildFixPrompt(issue, prd, userInstruction) {
    const basePrompt = `你是一个专业的软件需求文档编写专家。请根据以下问题生成修补内容。

## 问题信息
- 检查项：${issue.check_item_name}
- 章节：${issue.section_title}
- 问题描述：${issue.description}
- 修补建议：${issue.suggestion}

## 原文（有问题的部分）
${issue.original_text || '（未引用原文）'}

## 当前 PRD 章节
${prd.content || '（无内容）'}

## 输出要求
1. 只输出修补后的内容（不要包含原章节其他内容）
2. 使用 Markdown 格式
3. 保持专业、准确、完整
4. 确保修补内容能解决上述问题`;

    if (userInstruction) {
      return `${basePrompt}

## 用户修补要求
${userInstruction}

请根据用户要求生成修补内容：`;
    } else {
      return `${basePrompt}

请自动生成合适的修补内容：`;
    }
  }

  /**
   * 解析修补内容
   */
  parseFixContent(aiResponse) {
    let content = aiResponse;

    if (typeof aiResponse === 'object') {
      content = aiResponse.content || aiResponse.result || JSON.stringify(aiResponse);
    }

    // 去除可能的 Markdown 代码块标记
    if (typeof content === 'string') {
      if (content.startsWith('```markdown')) {
        content = content.replace(/^```markdown\n/, '').replace(/\n```$/, '');
      } else if (content.startsWith('```')) {
        content = content.replace(/^```\n/, '').replace(/\n```$/, '');
      }
    }

    return content.trim();
  }

  /**
   * 应用修补到 PRD
   *
   * @param {object} prd - PRD 对象
   * @param {object} fixResult - 修补结果（来自 fixIssue）
   * @param {object} dataBus - 数据总线
   * @returns {object} 更新后的 PRD
   */
  async applyFix(prd, fixResult, dataBus) {
    if (!fixResult.success || fixResult.action === 'skip') {
      // 无需应用修补
      return prd;
    }

    console.log('\n📝 应用修补到 PRD...');

    // 定位章节并替换/插入内容
    const updatedContent = this.updatePRDContent(prd.content, fixResult);

    // 更新 PRD 对象
    const updatedPRD = {
      ...prd,
      content: updatedContent,
      lastFix: {
        issue: fixResult.issue,
        action: fixResult.action,
        timestamp: new Date().toISOString()
      }
    };

    // 写入数据总线
    if (dataBus) {
      dataBus.write('prd', updatedPRD, { passed: true, fixed: true });
    }

    console.log('   ✅ PRD 已更新');

    return updatedPRD;
  }

  /**
   * 更新 PRD 内容
   *
   * 在对应章节插入/替换修补内容
   */
  updatePRDContent(content, fixResult) {
    const issue = fixResult.issue;
    const fixContent = fixResult.fixContent;

    if (!fixContent) {
      return content;
    }

    // 策略：在问题章节末尾追加修补内容（带标注）
    const sectionTitle = issue.section_title;

    // 找到章节位置
    const lines = content.split('\n');
    let insertPosition = -1;
    let sectionLevel = 2;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // 匹配章节标题
      if (line.includes(sectionTitle)) {
        // 找到章节开始位置，找到下一个同级或更高层级章节
        const headingMatch = line.match(/^#+\s+/);
        if (headingMatch) {
          sectionLevel = headingMatch[0].length - 1; // # 的数量
        }

        // 继续找章节结束位置
        for (let j = i + 1; j < lines.length; j++) {
          const nextLine = lines[j];
          // 检查是否是同级或更高级标题
          const nextHeadingMatch = nextLine.match(/^#+\s+/);
          if (nextHeadingMatch) {
            const nextLevel = nextHeadingMatch[0].length - 1;
            if (nextLevel <= sectionLevel) {
              insertPosition = j;
              break;
            }
          }
        }

        if (insertPosition === -1) {
          // 没找到下一个章节，插入到文档末尾
          insertPosition = lines.length;
        }

        break;
      }
    }

    if (insertPosition === -1) {
      // 未找到章节，追加到末尾
      console.warn('   ⚠️ 未找到对应章节，追加到末尾');
      return content + '\n\n' + this.formatFixContent(fixContent, issue);
    }

    // 在章节末尾插入修补内容
    const fixBlock = '\n\n' + this.formatFixContent(fixContent, issue);
    lines.splice(insertPosition, 0, fixBlock);

    return lines.join('\n');
  }

  /**
   * 格式化修补内容
   */
  formatFixContent(content, issue) {
    return `<!-- 修补：${issue.check_item_name} - ${new Date().toISOString().slice(0, 10)} -->

${content}
`;
  }
}

module.exports = ReviewModule;
