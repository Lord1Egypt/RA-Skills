/**
 * PRD 优化模块 v2.6.3（新增）
 * 
 * 根据评审问题自动优化 PRD
 */

const fs = require('fs');
const path = require('path');

class OptimizeModule {
  /**
   * 执行 PRD 优化
   */
  async execute(options) {
    console.log('\n🔧 执行技能：PRD 优化');
    
    const { dataBus, outputDir } = options;
    
    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }
    
    // 读取评审结果
    const reviewRecord = dataBus.read('review');
    if (!reviewRecord) {
      throw new Error('评审结果不存在，请先执行 PRD 评审');
    }
    
    const prd = prdRecord.data;
    const reviewResult = reviewRecord.data;
    
    // 检查是否需要优化
    if (reviewResult.overall >= 80) {
      console.log('   ✅ PRD 评分达标（≥80 分），无需优化');
      return { optimized: false, prd, reviewResult };
    }
    
    console.log(`   ⚠️  PRD 评分${reviewResult.overall}<80，启动优化...`);
    
    // 执行优化
    const optimizedPRD = await this.optimizePRD(prd.content, reviewResult.issues);
    
    // 更新 PRD
    const updatedPRD = {
      ...prd,
      content: optimizedPRD,
      chapters: this.extractChapters(optimizedPRD)
    };
    
    // 写入数据总线
    const filepath = dataBus.write('prd', updatedPRD, { passed: true });
    
    console.log('   ✅ 优化完成，PRD 已更新');
    
    return {
      optimized: true,
      prd: updatedPRD,
      reviewResult,
      outputPath: filepath
    };
  }
  
  /**
   * 优化 PRD
   */
  async optimizePRD(prdContent, issues) {
    let optimizedPRD = prdContent;
    
    // 分类问题
    const missingChapters = issues.filter(i => i.type === 'missing_section');
    const incompleteContent = issues.filter(i => i.type === 'incomplete_section');
    const aiIssues = issues.filter(i => i.id?.startsWith('AI-'));
    
    console.log(`   发现问题：${issues.length}个`);
    console.log(`   - 缺失章节：${missingChapters.length}个`);
    console.log(`   - 内容不完整：${incompleteContent.length}个`);
    console.log(`   - AI 语义问题：${aiIssues.length}个`);
    
    // 修复 1：补充缺失章节
    for (const issue of missingChapters) {
      const chapterName = issue.location || '章节';
      const suggestion = issue.suggestion || '';
      console.log(`   - 补充：${chapterName}`);
      optimizedPRD = this.addMissingChapter(optimizedPRD, chapterName, suggestion);
    }
    
    // 修复 2：优化 AI 语义问题
    for (const issue of aiIssues) {
      const issueType = issue.type || '';
      const suggestion = issue.suggestion || '';
      
      if (issueType.includes('boundary')) {
        console.log(`   - 添加边界条件`);
        optimizedPRD = this.addBoundaryConditions(optimizedPRD, suggestion);
      }
      
      if (issueType.includes('exception')) {
        console.log(`   - 添加异常处理`);
        optimizedPRD = this.addExceptionHandling(optimizedPRD, suggestion);
      }
      
      if (issueType.includes('vague')) {
        console.log(`   - 修复模糊描述`);
        optimizedPRD = this.fixVagueDescription(optimizedPRD, suggestion);
      }
      
      if (issueType.includes('risk')) {
        console.log(`   - 添加风险识别`);
        optimizedPRD = this.addRiskIdentification(optimizedPRD, suggestion);
      }
    }
    
    return optimizedPRD;
  }
  
  /**
   * 补充缺失章节
   */
  addMissingChapter(prdContent, chapterName, suggestion) {
    const appendixMatch = prdContent.match(/\n## 附录/);
    
    if (appendixMatch) {
      const insertPos = appendixMatch.index;
      const newChapter = `\n## ${chapterName}\n\n${suggestion}\n`;
      return prdContent.slice(0, insertPos) + newChapter + prdContent.slice(insertPos);
    }
    
    return prdContent + `\n\n## ${chapterName}\n\n${suggestion}\n`;
  }
  
  /**
   * 添加边界条件
   */
  addBoundaryConditions(prdContent, suggestion) {
    const funcMatch = prdContent.match(/### \d+\.\d+ 功能/);
    
    if (funcMatch) {
      const insertPos = funcMatch.index;
      const boundaryText = `\n**边界条件**:\n- 最大值：待补充\n- 最小值：待补充\n- 异常值处理：待补充\n\n`;
      return prdContent.slice(0, insertPos) + boundaryText + prdContent.slice(insertPos);
    }
    
    return prdContent;
  }
  
  /**
   * 添加异常处理
   */
  addExceptionHandling(prdContent, suggestion) {
    const acceptanceMatch = prdContent.match(/### \d+\.\d+ 验收标准/);
    
    if (acceptanceMatch) {
      const insertPos = acceptanceMatch.index;
      const exceptionText = `\n**异常处理**:\n- 参数校验失败：提示用户\n- 系统异常：记录日志并返回错误\n- 超时处理：30 秒超时\n\n`;
      return prdContent.slice(0, insertPos) + exceptionText + prdContent.slice(insertPos);
    }
    
    return prdContent;
  }
  
  /**
   * 修复模糊描述
   */
  fixVagueDescription(prdContent, suggestion) {
    // TODO: 使用 AI 大模型替换模糊词汇
    // 简化实现：添加注释
    return prdContent + `\n\n<!-- 优化建议：${suggestion} -->\n`;
  }
  
  /**
   * 添加风险识别
   */
  addRiskIdentification(prdContent, suggestion) {
    const appendixMatch = prdContent.match(/\n## 附录/);
    
    if (appendixMatch) {
      const insertPos = appendixMatch.index;
      const riskText = `\n## 风险识别\n\n**技术风险**:\n- 性能风险：高并发下响应超时\n- 数据风险：数据丢失或泄露\n\n**业务风险**:\n- 合规风险：监管政策变化\n- 市场风险：市场竞争加剧\n\n**应对措施**:\n- 性能优化：缓存、CDN、负载均衡\n- 数据备份：定期备份、异地容灾\n- 合规审查：定期合规检查\n\n`;
      return prdContent.slice(0, insertPos) + riskText + prdContent.slice(insertPos);
    }
    
    return prdContent + `\n\n## 风险识别\n\n${suggestion}\n`;
  }
  
  /**
   * 提取章节
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
}

module.exports = OptimizeModule;
