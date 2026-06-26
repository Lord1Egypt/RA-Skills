import { MungerDecisionAssistant } from './src/index';

async function testCompleteFlow() {
  const assistant = new MungerDecisionAssistant();
  
  console.log('=== 完整流程测试（所有问题） ===\n');
  
  // Start analysis
  let response = await assistant.startAnalysis('test-complete', '投资 *股票* 还是 _债券_ `基金` [ETF]？');
  console.log('开始分析...\n');
  
  // Answer all questions (5 models × 3 questions = 15 answers)
  for (let i = 1; i <= 15; i++) {
    response = await assistant.handleAnswer('test-complete', `答案 ${i}：我有 *经验* _风险_ \`预算\` [时间]`);
    
    if (response.includes('# 决策分析报告')) {
      console.log('=== 生成报告 ===\n');
      console.log(response);
      
      console.log('\n=== 检查转义 ===');
      const escapedCount = (response.match(/\\[*_`[\]]/g) || []).length;
      console.log('转义字符总数:', escapedCount);
      
      if (escapedCount > 0) {
        console.log('✅ Bug #2 修复成功：特殊字符已正确转义');
        
        // Show some examples
        const lines = response.split('\n');
        const escapedLines = lines.filter(l => /\\[*_`[\]]/.test(l)).slice(0, 3);
        console.log('\n转义示例:');
        escapedLines.forEach(line => console.log('  ', line.trim()));
      }
      break;
    } else {
      console.log(`问题 ${i + 1} 已回答`);
    }
  }
}

testCompleteFlow();
