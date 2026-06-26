/**
 * PharmaAI Skill - 主入口
 * 
 * 智能药物发现AI助手
 * 提供分子毒性预测、ADMET评估和虚拟筛选功能
 */

import { predictMolecule, batchPredict, formatPredictionResult } from './commands/predict';

// 导出主要功能
export {
  predictMolecule,
  batchPredict,
  formatPredictionResult
};

// 版本信息
export const VERSION = '1.0.0';

// 默认导出
export default {
  predictMolecule,
  batchPredict,
  formatPredictionResult,
  VERSION
};

// 如果是直接运行，提供CLI接口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🧪 PharmaAI Skill v1.0.0');
    console.log('');
    console.log('Usage:');
    console.log('  predict <SMILES>     - 预测单个分子');
    console.log('  batch <file.csv>     - 批量预测');
    console.log('');
    console.log('Example:');
    console.log('  ts-node src/index.ts predict "CCO"');
    process.exit(0);
  }
  
  const command = args[0];
  const input = args[1];
  
  if (command === 'predict' && input) {
    predictMolecule(input).then(result => {
      console.log(formatPredictionResult(result));
    }).catch(err => {
      console.error('Error:', err.message);
      process.exit(1);
    });
  } else {
    console.error('Unknown command:', command);
    process.exit(1);
  }
}
