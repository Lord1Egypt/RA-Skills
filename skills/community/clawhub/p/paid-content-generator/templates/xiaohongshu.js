/**
 * 小红书文案模板生成器
 */

// 从content-generator复制逻辑
const PATH = require('path');
const FS = require('fs');

// 尝试加载原有的内容生成器
let legacyGenerator = null;
try {
  const legacyPath = PATH.join(__dirname, '../../../content-generator/scripts/generator.py');
  if (FS.existsSync(legacyPath)) {
    legacyGenerator = legacyPath;
  }
} catch (e) {}

async function generate(topic) {
  // 简化版生成逻辑
  // 实际使用时可以调用GLM-5等模型
  
  const lines = [
    `${topic}，一篇看懂！`,
    '',
    `最近很多人问我关于${topic}的问题，今天就来详细说说。`,
    '',
    '## 核心要点',
    '',
    `1. 什么是${topic}`,
    `2. 怎样选择好的${topic}`,
    `3. 避坑指南`,
    '',
    '## 详细内容',
    '',
    `关于${topic}，最重要的几点：`,
    '',
    '- 首先看整体气质',
    '- 其次看细节特征', 
    '- 最后看性价比',
    '',
    '## 总结',
    '',
    '希望这篇对你有帮助！有问题欢迎评论区讨论~',
    '',
    '#宠物 #养宠攻略 #新手养宠'
  ];
  
  return lines.join('\n');
}

module.exports = { generate };
