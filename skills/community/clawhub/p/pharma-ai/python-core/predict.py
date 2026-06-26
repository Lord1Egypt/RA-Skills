#!/usr/bin/env python3
"""
PharmaAI Python核心 - 预测模块
通过JSON与Node.js通信
"""

import sys
import json
import os
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
import joblib

# 模型目录
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

# 全局模型缓存
_models = {}

def load_model(model_name):
    """加载模型（带缓存）"""
    if model_name not in _models:
        model_path = os.path.join(MODELS_DIR, f'{model_name}_model.pkl')
        _models[model_name] = joblib.load(model_path)
    return _models[model_name]

def calculate_features(smiles):
    """计算分子特征"""
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return None
    
    # 基础描述符
    features = {
        'MW': Descriptors.MolWt(mol),
        'LogP': Crippen.MolLogP(mol),
        'TPSA': Descriptors.TPSA(mol),
        'HBD': Lipinski.NumHDonors(mol),
        'HBA': Lipinski.NumHAcceptors(mol),
        'RotatableBonds': Lipinski.NumRotatableBonds(mol),
        'AromaticRings': Lipinski.NumAromaticRings(mol),
        'HeavyAtoms': mol.GetNumHeavyAtoms(),
        'NumNitrogens': sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() == 7),
        'NumHalogens': sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() in [9, 17, 35, 53])
    }
    
    # Morgan指纹
    fp = GetMorganFingerprintAsBitVect(mol, 2, 2048)
    features['fingerprint'] = np.array(fp)
    
    return features

def predict_with_model(features, model_data):
    """使用模型预测"""
    desc_cols = model_data['desc_cols']
    model = model_data['model']
    
    X_desc = np.array([[features[c] for c in desc_cols]])
    X_fp = features['fingerprint'].reshape(1, -1)
    X = np.hstack([X_desc, X_fp])
    
    prob = model.predict_proba(X)[0, 1]
    pred = model.predict(X)[0]
    
    return float(prob), int(pred)

def get_risk_level(probability):
    """根据概率确定风险等级"""
    if probability >= 0.7:
        return 'High'
    elif probability >= 0.3:
        return 'Medium'
    return 'Low'

def predict_molecule(smiles):
    """预测单个分子"""
    features = calculate_features(smiles)
    if not features:
        return {'error': 'Invalid SMILES'}
    
    # 加载模型
    herg_model = load_model('herg')
    hep_model = load_model('hepatotoxicity')
    ames_model = load_model('ames')
    
    # 预测
    herg_prob, herg_pred = predict_with_model(features, herg_model)
    hep_prob, hep_pred = predict_with_model(features, hep_model)
    ames_prob, ames_pred = predict_with_model(features, ames_model)
    
    # 构建结果
    result = {
        'smiles': smiles,
        'toxicity': {
            'hERG': {
                'risk': get_risk_level(herg_prob),
                'probability': round(herg_prob, 3)
            },
            'hepatotoxicity': {
                'risk': get_risk_level(hep_prob),
                'probability': round(hep_prob, 3)
            },
            'ames': {
                'risk': get_risk_level(ames_prob),
                'probability': round(ames_prob, 3)
            }
        },
        'overall': 'Safe' if all([
            herg_prob < 0.3,
            hep_prob < 0.3,
            ames_prob < 0.3
        ]) else 'Caution' if all([
            herg_prob < 0.7,
            hep_prob < 0.7,
            ames_prob < 0.7
        ]) else 'Risky'
    }
    
    return result

def main():
    """主函数 - 从命令行读取JSON输入"""
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No input provided'}))
        return
    
    try:
        input_data = json.loads(sys.argv[1])
        action = input_data.get('action', 'predict')
        data = input_data.get('data', {})
        
        if action == 'predict':
            smiles = data.get('smiles', '')
            result = predict_molecule(smiles)
            print(json.dumps(result))
            
        elif action == 'batch_predict':
            smiles_list = data.get('smiles_list', [])
            results = [predict_molecule(s) for s in smiles_list]
            print(json.dumps(results))
            
        elif action == 'screen':
            molecules = data.get('molecules', [])
            top_n = data.get('top_n', 10)
            results = [predict_molecule(s) for s in molecules]
            # 排序并选择Top N
            results.sort(key=lambda x: max([
                x['toxicity']['hERG']['probability'],
                x['toxicity']['hepatotoxicity']['probability'],
                x['toxicity']['ames']['probability']
            ]))
            print(json.dumps(results[:top_n]))
            
        else:
            print(json.dumps({'error': f'Unknown action: {action}'}))
            
    except Exception as e:
        print(json.dumps({'error': str(e)}))

if __name__ == '__main__':
    main()
