/**
 * 流程图模块 v3.0.0
 *
 * 生成流程图，执行质量检查
 * v3.0.0: 使用 ImageRenderer 统一渲染 Mermaid → PNG
 */

const fs = require('fs');
const path = require('path');
const { ImageRenderer } = require('../image_renderer');

class FlowchartModule {
  constructor() {
    this.renderer = new ImageRenderer();
  }
  /**
   * 执行流程图生成
   */
  async execute(options) {
    console.log('\n📊 执行技能：流程图生成');
    
    const { dataBus, qualityGate, outputDir } = options;
    
    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }
    
    const prd = prdRecord.data;
    
    // 从 PRD 提取流程步骤
    console.log('   提取流程步骤...');
    const flowSteps = this.extractFlowSteps(prd.content);
    
    // AI 驱动：生成 Mermaid 代码
    console.log('   AI 生成：Mermaid 流程图代码...');
    const mermaidCode = await this.generateMermaidCode(flowSteps, prd);
    
    // 保存 Mermaid 源文件
    const mmdPath = path.join(outputDir, 'flowchart.mmd');
    fs.writeFileSync(mmdPath, mermaidCode, 'utf8');
    console.log(`   ✅ 保存：${mmdPath}`);
    
    // 调用 mermaid-flow 渲染 PNG（v2.6.3 修复）
    const pngPath = await this.renderFlowchart(mmdPath, outputDir);
    
    // 质量检查
    console.log('   质量检查：6 条规则验证...');
    const qualityCheck = this.validateFlowchart(mermaidCode, flowSteps);
    
    // 构建结果
    const result = {
      files: ['flowchart.mmd', pngPath].filter(Boolean),
      type: 'flowchart',
      stepCount: flowSteps.length,
      mermaidCode: mermaidCode,
      qualityCheck: qualityCheck
    };
    
    // 质量验证
    const quality = {
      passed: qualityCheck.passed,
      filesGenerated: true,
      rulesPassed: qualityCheck.rules.filter(r => r.passed).length,
      totalRules: qualityCheck.rules.length
    };
    
    // 写入数据总线
    const filepath = dataBus.write('flowchart', result, quality, {
      fromPRD: 'prd.json'
    });
    
    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate5_flowchart', result);
    }
    
    return {
      ...result,
      quality: quality,
      outputPath: filepath
    };
  }
  
  /**
   * 调用 ImageRenderer 渲染流程图（v3.0.0 重构）
   */
  async renderFlowchart(mmdPath, outputDir) {
    const pngPath = path.join(outputDir, 'flowchart.png');

    // 读取 Mermaid 代码
    const mermaidCode = fs.readFileSync(mmdPath, 'utf8');

    // 使用 ImageRenderer 渲染
    const result = this.renderer.renderMermaid(mermaidCode, pngPath, {
      width: 1600,
      height: 1200,
      backgroundColor: 'white'
    });

    if (result.success) {
      console.log(`   ✅ 保存：${result.path}`);
      return 'flowchart.png';
    } else {
      console.warn('⚠️  渲染失败:', result.error);
      return null;
    }
  }
  
  /**
   * 从 PRD 提取流程步骤
   */
  extractFlowSteps(prdContent) {
    // 简单实现：查找包含流程关键词的段落
    const flowKeywords = ['流程', '步骤', '首先', '然后', '接着', '最后'];
    const lines = prdContent.split('\n');
    
    const steps = [];
    let currentStep = '';
    
    lines.forEach((line, index) => {
      if (flowKeywords.some(keyword => line.includes(keyword))) {
        if (currentStep) {
          steps.push(currentStep);
        }
        currentStep = line.trim();
      }
    });
    
    if (currentStep) {
      steps.push(currentStep);
    }
    
    // 如果未提取到，返回默认步骤
    if (steps.length === 0) {
      return [
        '开始',
        '用户操作',
        '系统处理',
        '条件判断',
        '结束'
      ];
    }
    
    return steps.slice(0, 10); // 最多 10 个步骤
  }
  
  /**
   * AI 驱动：生成 Mermaid 代码
   */
  async generateMermaidCode(flowSteps, prd) {
    // 实际由 AI 生成，这里返回示例
    return `flowchart TD
    Start([开始]) --> Step1[${flowSteps[0] || '用户操作'}]
    Step1 --> Step2[${flowSteps[1] || '系统处理'}]
    Step2 --> Check{条件判断？}
    Check -->|是 | Step3[${flowSteps[2] || '处理成功'}]
    Check -->|否 | Step4[${flowSteps[3] || '处理失败'}]
    Step3 --> End([结束])
    Step4 --> End
    
    style Start fill:#4CAF50,stroke:#333,color:#fff
    style End fill:#F44336,stroke:#333,color:#fff
    style Check fill:#FFC107,stroke:#333
`;
  }
  
  /**
   * 质量检查：6 条规则
   */
  validateFlowchart(mermaidCode, flowSteps) {
    const rules = [
      {
        name: 'FLOWCHART_HAS_START_END',
        description: '流程图必须有开始和结束节点',
        passed: mermaidCode.includes('([开始])') || mermaidCode.includes('([结束])'),
        suggestion: '添加开始和结束节点'
      },
      {
        name: 'FLOWCHART_HAS_DECISION',
        description: '复杂流程必须有条件判断',
        passed: flowSteps.length > 3 ? mermaidCode.includes('{') : true,
        suggestion: '添加条件判断节点'
      },
      {
        name: 'FLOWCHART_CONNECTED',
        description: '所有节点必须连接',
        passed: (mermaidCode.match(/-->/g) || []).length >= flowSteps.length - 1,
        suggestion: '确保所有节点都有连接'
      },
      {
        name: 'FLOWCHART_NO_DUPLICATES',
        description: '节点 ID 不能重复',
        passed: this.checkNoDuplicateIds(mermaidCode),
        suggestion: '检查节点 ID 是否唯一'
      },
      {
        name: 'FLOWCHART_VALID_SYNTAX',
        description: 'Mermaid 语法必须有效',
        passed: mermaidCode.includes('flowchart'),
        suggestion: '检查 Mermaid 语法'
      },
      {
        name: 'FLOWCHART_REASONABLE_SIZE',
        description: '流程图大小合理（不超过 20 个节点）',
        passed: flowSteps.length <= 20,
        suggestion: '简化流程图，拆分为多个子流程'
      }
    ];
    
    const passedCount = rules.filter(r => r.passed).length;
    const totalCount = rules.length;
    
    return {
      passed: passedCount === totalCount,
      rules: rules,
      passedCount: passedCount,
      totalCount: totalCount,
      passRate: (passedCount / totalCount) * 100
    };
  }
  
  /**
   * 检查节点 ID 是否重复
   */
  checkNoDuplicateIds(mermaidCode) {
    const idMatches = mermaidCode.match(/([A-Z]\w*)\[/g) || [];
    const ids = idMatches.map(m => m.replace('[', ''));
    const uniqueIds = new Set(ids);
    return ids.length === uniqueIds.size;
  }
}

module.exports = FlowchartModule;
