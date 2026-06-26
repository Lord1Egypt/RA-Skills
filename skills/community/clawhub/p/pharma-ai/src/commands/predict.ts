/**
 * 预测命令
 */

import { 
  predictMolecule as bridgePredict, 
  batchPredict as bridgeBatchPredict 
} from '../python-bridge';
import { MoleculePrediction, MoleculeInput } from '../types';

/**
 * 预测单个分子
 */
export async function predictMolecule(smiles: string): Promise<MoleculePrediction> {
  const result = await bridgePredict(smiles);
  
  return {
    smiles: result.smiles,
    name: undefined,
    toxicity: result.toxicity,
    admet: {
      solubility: 'Medium', // 简化版，实际应从Python获取
      metabolicStability: 'Medium',
      cypInhibition: 'Low'
    },
    overallScore: calculateOverallScore(result.toxicity),
    lipinskiPass: true // 简化版
  };
}

/**
 * 批量预测
 */
export async function batchPredict(smilesList: string[]): Promise<MoleculePrediction[]> {
  const results = await bridgeBatchPredict(smilesList);
  return results.map((r: any) => ({
    smiles: r.smiles,
    toxicity: r.toxicity,
    admet: {
      solubility: 'Medium',
      metabolicStability: 'Medium',
      cypInhibition: 'Low'
    },
    overallScore: calculateOverallScore(r.toxicity),
    lipinskiPass: true
  }));
}

/**
 * 计算综合评分
 */
function calculateOverallScore(toxicity: any): number {
  const scores = [
    1 - toxicity.hERG.probability,
    1 - toxicity.hepatotoxicity.probability,
    1 - toxicity.ames.probability
  ];
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}

/**
 * 格式化预测结果为可读文本
 */
export function formatPredictionResult(result: MoleculePrediction): string {
  const lines = [
    `🧪 分子: ${result.smiles}`,
    ``,
    `⚠️ 毒性预测:`,
    `  • hERG心脏毒性: ${result.toxicity.hERG.risk} (${(result.toxicity.hERG.probability * 100).toFixed(1)}%)`,
    `  • 肝毒性: ${result.toxicity.hepatotoxicity.risk} (${(result.toxicity.hepatotoxicity.probability * 100).toFixed(1)}%)`,
    `  • Ames致突变性: ${result.toxicity.ames.risk} (${(result.toxicity.ames.probability * 100).toFixed(1)}%)`,
    ``,
    `📊 综合评估: ${result.overall === 'Safe' ? '✅ 安全' : result.overall === 'Caution' ? '⚠️ 谨慎' : '❌ 风险'}`,
  ];
  
  return lines.join('\n');
}
