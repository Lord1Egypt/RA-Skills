---
name: pharma-ai
description: |
  智能药物发现AI助手，提供分子毒性预测、ADMET评估和虚拟筛选功能。
  基于Python科学计算核心(RDKit + scikit-learn)和Node.js Skill包装。
  
  Use when:
  - 需要预测分子的hERG心脏毒性、肝毒性或Ames致突变性
  - 需要评估分子的溶解度、代谢稳定性等ADMET性质
  - 需要从化合物库中筛选候选药物
  - 需要验证分子是否符合Lipinski五规则
  - 需要批量分析分子数据
  
  Supports: SMILES输入, CSV批量处理, 实时预测
---

# PharmaAI Skill

智能药物发现工作流，整合数据增强、分子性质预测、毒性预测、ADMET预测和虚拟筛选。

## 核心功能

### 1. 分子毒性预测
- **hERG心脏毒性**: 预测QT间期延长风险 (ROC-AUC 0.852)
- **肝毒性**: 预测肝损伤风险
- **Ames致突变性**: 预测基因突变风险

### 2. ADMET性质预测
- **溶解度**: 水溶性等级预测
- **代谢稳定性**: 半衰期预测
- **CYP450抑制**: 药物相互作用风险

### 3. 虚拟筛选
- 综合评分系统
- Top N候选筛选
- 分子结构可视化

## 使用方式

### 预测单个分子

```typescript
import { predictMolecule } from './src/commands/predict';

const result = await predictMolecule('CC(C)Cc1ccc(cc1)C(C)C(=O)O');
console.log(result);
// {
//   smiles: 'CC(C)Cc1ccc(cc1)C(C)C(=O)O',
//   hERG: { risk: 'Low', probability: 0.05 },
//   hepatotoxicity: { risk: 'Low', probability: 0.10 },
//   ames: { risk: 'Low', probability: 0.05 },
//   overall: 'Safe'
// }
```

### 批量预测

```typescript
import { batchPredict } from './src/commands/predict';

const results = await batchPredict([
  'CCO',
  'CC(C)O',
  'c1ccccc1'
]);
```

### 虚拟筛选

```typescript
import { virtualScreen } from './src/commands/screen';

const topCandidates = await virtualScreen('molecules.csv', 10);
```

## 模型性能

| 模型 | ROC-AUC | 描述 |
|------|---------|------|
| hERG | 0.852 | 心脏毒性预测 |
| 肝毒性 | 1.000 | 肝损伤预测 |
| Ames | 1.000 | 致突变性预测 |

## 技术架构

```
User Request
    ↓
OpenClaw Agent
    ↓
pharma-ai Skill (Node.js)
    ↓ [Python Bridge]
Python Core (RDKit + scikit-learn)
    ↓
Return Result
```

- **Node.js层**: Skill接口、命令处理、结果格式化
- **Python层**: RDKit化学计算、ML模型推理

## 依赖

- Node.js: `onnxruntime-node` (可选ONNX模型)
- Python: `rdkit`, `scikit-learn`, `pandas`, `numpy`

## 参考文档

- 详细使用说明: `references/manual.md`
- 开发路线图: `references/roadmap.md`
