#!/usr/bin/env node
/**
 * MIA Feedback - 反馈收集器
 * 职责：收集用户对答案的反馈（仅针对全新问题）
 */

import { appendFileSync, existsSync, readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 从环境变量获取配置
const FEEDBACK_FILE = process.env.MIA_FEEDBACK_FILE || join(__dirname, 'feedback.jsonl');

// 存储反馈
function storeFeedback(feedback) {
  const record = {
    timestamp: new Date().toISOString(),
    ...feedback
  };
  
  appendFileSync(FEEDBACK_FILE, JSON.stringify(record) + '\n');
  return record;
}

// 列出反馈
function listFeedback(limit = 10) {
  if (!existsSync(FEEDBACK_FILE)) {
    return [];
  }
  
  const content = readFileSync(FEEDBACK_FILE, 'utf-8');
  const lines = content.split('\n').filter(line => line.trim());
  
  return lines
    .slice(-limit)
    .map(line => {
      try {
        return JSON.parse(line);
      } catch (e) {
        return null;
      }
    })
    .filter(Boolean);
}

// 主函数
async function main() {
  const command = process.argv[2];
  
  if (!command) {
    console.error('Usage: mia-feedback.mjs <command> [args]');
    console.error('Commands:');
    console.error('  store <question> <result> <label>  - 存储反馈（label: good/bad）');
    console.error('  list [limit]                         - 列出反馈');
    process.exit(1);
  }
  
  try {
    switch (command) {
      case 'store': {
        const question = process.argv[3];
        const result = process.argv[4];
        const label = process.argv[5];
        
        if (!question || !result || !label) {
          console.error('Usage: mia-feedback.mjs store "question" "result" "good|bad"');
          process.exit(1);
        }
        
        const record = storeFeedback({ question, result, label });
        console.log(JSON.stringify({ success: true, record }, null, 2));
        break;
      }
      
      case 'list': {
        const limit = parseInt(process.argv[3] || '10', 10);
        const feedbacks = listFeedback(limit);
        console.log(JSON.stringify({ feedbacks, count: feedbacks.length }, null, 2));
        break;
      }
      
      default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
  } catch (error) {
    console.error(JSON.stringify({ error: error.message }));
    process.exit(1);
  }
}

main();
