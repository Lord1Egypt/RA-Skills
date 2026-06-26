#!/usr/bin/env ts-node
import * as fs from 'fs';
import * as path from 'path';

const MODELS_DIR = '/root/.openclaw/workspace/munger-models/models';
const OUTPUT_FILE = path.join(__dirname, '../data/models-full.json');

interface Model {
  id: string;
  name: string;
  category: string;
  description: string;
  questions: string[];
  keywords: string[];
  scoring: {
    high?: string;
    medium?: string;
    low?: string;
  };
}

function extractModelFromMarkdown(filePath: string, category: string): Model | null {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  
  const idMatch = path.basename(filePath).match(/^(\d+)-/);
  if (!idMatch) return null;
  
  const id = idMatch[1];
  const nameMatch = content.match(/^#\s+(.+?)(?:\s+\(|$)/m);
  const name = nameMatch ? nameMatch[1].trim() : '';
  
  const descMatch = content.match(/##\s+核心概念\s*\n\n(.+?)(?:\n\n|$)/s);
  const description = descMatch ? descMatch[1].trim() : '';
  
  const questions: string[] = [];
  const questionsMatch = content.match(/##\s+使用时的检查清单[\s\S]*?(?=##|$)/);
  if (questionsMatch) {
    const qLines = questionsMatch[0].split('\n').filter(l => l.trim().startsWith('-'));
    questions.push(...qLines.slice(0, 3).map(l => l.replace(/^-\s*/, '').trim()));
  }
  
  return {
    id,
    name,
    category,
    description,
    questions: questions.length > 0 ? questions : [
      `在这个决策中，是否存在${name}的影响？`,
      `如何避免${name}导致的判断偏差？`,
      `${name}可能让你忽视哪些重要信息？`
    ],
    keywords: [],
    scoring: { high: '高度相关', medium: '中等相关', low: '低度相关' }
  };
}

function convertModels() {
  const models: Model[] = [];
  const categories = ['core', 'psychology', 'business', 'investing', 'systems'];
  
  for (const category of categories) {
    const categoryDir = path.join(MODELS_DIR, category);
    if (!fs.existsSync(categoryDir)) continue;
    
    const files = fs.readdirSync(categoryDir).filter(f => f.endsWith('.md'));
    for (const file of files) {
      const model = extractModelFromMarkdown(path.join(categoryDir, file), category);
      if (model) models.push(model);
    }
  }
  
  models.sort((a, b) => parseInt(a.id) - parseInt(b.id));
  
  const output = {
    version: '1.0',
    total: models.length,
    models
  };
  
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2));
  console.log(`✅ 转换完成：${models.length} 个模型`);
  console.log(`📁 输出文件：${OUTPUT_FILE}`);
}

convertModels();
