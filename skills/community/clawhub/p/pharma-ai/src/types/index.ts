/**
 * Python桥接层类型定义
 */

export interface MoleculeInput {
  smiles: string;
  name?: string;
}

export interface ToxicityPrediction {
  hERG: {
    risk: 'Low' | 'Medium' | 'High';
    probability: number;
  };
  hepatotoxicity: {
    risk: 'Low' | 'Medium' | 'High';
    probability: number;
  };
  ames: {
    risk: 'Low' | 'Medium' | 'High';
    probability: number;
  };
}

export interface ADMETPrediction {
  solubility: 'Low' | 'Medium' | 'High';
  metabolicStability: 'Low' | 'Medium' | 'High';
  cypInhibition: 'Low' | 'Medium' | 'High';
}

export interface MoleculePrediction extends MoleculeInput {
  toxicity: ToxicityPrediction;
  admet: ADMETPrediction;
  overallScore: number;
  lipinskiPass: boolean;
}

export interface PythonInput {
  action: 'predict' | 'batch_predict' | 'screen';
  data: any;
}

export interface PythonOutput {
  success: boolean;
  result?: any;
  error?: string;
}
