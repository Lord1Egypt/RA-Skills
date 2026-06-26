#!/usr/bin/env node
/**
 * 记忆分类脚本
 * 根据内容自动判断记忆类型
 * 
 * 用法: node classify.js "<内容>"
 * 输出: user | feedback | project | reference
 */

// 分类关键词规则
const RULES = {
  user: {
    keywords: ['偏好', '喜欢', '习惯', '角色', '目标', '负责', '职位', '身份', '称呼', '语言', '时区'],
    patterns: [/我是.+/, /我叫.+/, /我的.+是/, /我希望.+/, /我偏好.+/],
    weight: 1
  },
  feedback: {
    keywords: ['不对', '错误', '纠正', '不是', '应该', '不要', '禁止', '避免', '改进', '修复', '教训'],
    patterns: [/不要.+/, /禁止.+/, /避免.+/, /应该.+/, /不应该.+/],
    weight: 1.2
  },
  project: {
    keywords: ['项目', '部署', '环境', '配置', '路径', '地址', '端口', '域名', '工作区', '目录', '版本'],
    patterns: [/部署到.+/, /路径是.+/, /地址是.+/, /使用.+版本/],
    weight: 1
  },
  reference: {
    keywords: ['命令', '用法', '示例', '参考', '解决', '方案', '命令', '脚本', 'API', '接口', '模板'],
    patterns: [/用法:?/, /示例:?/, /命令:?/, /步骤:?/, /\$\s*\w+/],
    weight: 0.8
  }
};

function classify(content) {
  const scores = {};
  
  for (const [type, rule] of Object.entries(RULES)) {
    let score = 0;
    
    // 关键词匹配
    for (const keyword of rule.keywords) {
      if (content.includes(keyword)) {
        score += rule.weight;
      }
    }
    
    // 正则匹配
    for (const pattern of rule.patterns) {
      if (pattern.test(content)) {
        score += rule.weight * 1.5;
      }
    }
    
    scores[type] = score;
  }
  
  // 返回得分最高的类型
  let bestType = 'project';
  let bestScore = 0;
  
  for (const [type, score] of Object.entries(scores)) {
    if (score > bestScore) {
      bestScore = score;
      bestType = type;
    }
  }
  
  return { type: bestType, scores, confidence: bestScore > 0 ? Math.min(bestScore / 5, 1) : 0.3 };
}

function main() {
  const content = process.argv.slice(2).join(' ');
  
  if (!content) {
    console.log('用法: node classify.js "<内容>"');
    process.exit(1);
  }
  
  const result = classify(content);
  console.log(JSON.stringify(result, null, 2));
}

main();
