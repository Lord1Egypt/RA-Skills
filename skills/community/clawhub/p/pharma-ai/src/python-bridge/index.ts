/**
 * Python桥接层 - 管理Python子进程通信
 */

import { spawn } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import { PythonInput, PythonOutput } from '../types';

const PYTHON_CORE_DIR = path.join(__dirname, '..', '..', 'python-core');

/**
 * 调用Python脚本
 */
export async function callPython(
  scriptName: string,
  input: PythonInput
): Promise<PythonOutput> {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(PYTHON_CORE_DIR, `${scriptName}.py`);
    
    const python = spawn('python3', [scriptPath, JSON.stringify(input)]);
    
    let stdout = '';
    let stderr = '';
    
    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    python.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          resolve({ success: true, result });
        } catch (e) {
          resolve({ 
            success: false, 
            error: `Failed to parse Python output: ${stdout}` 
          });
        }
      } else {
        resolve({ 
          success: false, 
          error: `Python exit code ${code}: ${stderr || stdout}` 
        });
      }
    });
    
    python.on('error', (err) => {
      resolve({ 
        success: false, 
        error: `Failed to spawn Python: ${err.message}` 
      });
    });
  });
}

/**
 * 预测单个分子
 */
export async function predictMolecule(smiles: string): Promise<any> {
  const output = await callPython('predict', {
    action: 'predict',
    data: { smiles }
  });
  
  if (!output.success) {
    throw new Error(output.error);
  }
  
  return output.result;
}

/**
 * 批量预测
 */
export async function batchPredict(smilesList: string[]): Promise<any[]> {
  const output = await callPython('predict', {
    action: 'batch_predict',
    data: { smiles_list: smilesList }
  });
  
  if (!output.success) {
    throw new Error(output.error);
  }
  
  return output.result;
}

/**
 * 虚拟筛选
 */
export async function virtualScreen(
  molecules: string[], 
  topN: number = 10
): Promise<any[]> {
  const output = await callPython('screen', {
    action: 'screen',
    data: { molecules, top_n: topN }
  });
  
  if (!output.success) {
    throw new Error(output.error);
  }
  
  return output.result;
}
