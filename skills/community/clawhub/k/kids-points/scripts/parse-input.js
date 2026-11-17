/**
 * 积分输入解析器
 * 解析自然语言输入，提取任务和分数
 */

// 任务关键词映射
const TASK_PATTERNS = {
  '汉字抄写': {
    keywords: ['汉字抄写', '抄写汉字', '抄写'],
    parse: (text) => {
      const match = text.match(/(\d+)\s*(课|节|个)/);
      return match ? { count: parseInt(match[1]), unit: match[2] } : { count: 1 };
    }
  },
  '汉字默写': {
    keywords: ['汉字默写', '默写汉字', '默写'],
    parse: (text) => {
      const match = text.match(/(\d+)\s*(个|字)/);
      return match ? { count: parseInt(match[1]) } : { count: 1 };
    }
  },
  '口算题卡': {
    keywords: ['口算题卡', '口算', '题卡'],
    parse: (text) => {
      const match = text.match(/(\d+)\s*篇/);
      const allCorrect = text.includes('全对');
      return { 
        count: match ? parseInt(match[1]) : 1,
        allCorrect: allCorrect
      };
    }
  },
  '英语描红': {
    keywords: ['英语描红', '描红', '英语'],
    parse: () => ({ count: 1 })
  },
  'ABC Reading': {
    keywords: ['ABC Reading', 'ABC', '英语阅读', '阅读'],
    parse: (text) => {
      const match = text.match(/(\d+)\s*篇/);
      const autoComplete = text.includes('自主') || text.includes('主动');
      return { 
        count: match ? parseInt(match[1]) : 2,
        autoComplete: autoComplete
      };
    }
  },
  '复述学习内容': {
    keywords: ['复述', '学习内容', '今天学了'],
    parse: (text) => {
      const over10min = text.includes('超过 10 分钟') || text.includes('大于 10 分钟');
      return { over10min };
    }
  },
  '跳绳': {
    keywords: ['跳绳'],
    parse: (text) => {
      const count350 = text.includes('350') || text.includes('完成');
      const speed110 = text.includes('110');
      const speed117 = text.includes('117');
      return { count350, speed110, speed117 };
    }
  },
  '自主洗澡': {
    keywords: ['自主洗澡', '自己洗澡', '洗澡'],
    parse: () => ({ done: true })
  },
  '自己换居家服': {
    keywords: ['换居家服', '换衣服', '居家服'],
    parse: () => ({ done: true })
  },
  '整理书包': {
    keywords: ['整理书包', '书包'],
    parse: () => ({ done: true })
  },
  '睡前主动洗漱': {
    keywords: ['洗漱', '刷牙', '洗脸'],
    parse: (text) => {
      const before10pm = text.includes('10 点') || text.includes('睡前');
      return { before10pm: true };
    }
  },
  '学校表扬': {
    keywords: ['表扬', '奖状', '奖励'],
    parse: (text) => {
      const match = text.match(/(\d+)\s*分/);
      return { points: match ? parseInt(match[1]) : 20 };
    }
  }
};

/**
 * 解析积分输入
 * @param {string} input - 用户输入
 * @returns {Array} - 解析后的任务列表
 */
function parsePointsInput(input) {
  const results = [];
  const text = input.toLowerCase();
  
  for (const [taskName, config] of Object.entries(TASK_PATTERNS)) {
    const found = config.keywords.some(keyword => 
      text.includes(keyword.toLowerCase())
    );
    
    if (found) {
      const data = config.parse(text);
      results.push({ task: taskName, ...data });
    }
  }
  
  return results;
}

/**
 * 计算积分
 * @param {Array} tasks - 任务列表
 * @param {Object} rules - 积分规则
 * @returns {Object} - 积分详情
 */
function calculatePoints(tasks, rules) {
  const details = [];
  let total = 0;
  
  for (const task of tasks) {
    const rule = rules.tasks[task.task];
    if (!rule) continue;
    
    let points = 0;
    let note = '';
    
    switch (task.task) {
      case '汉字抄写':
        points = Math.min(task.count, rule.dailyLimit) * rule.points;
        note = `${task.count}课 × ${rule.points}分`;
        break;
        
      case '汉字默写':
        points = task.count * rule.points;
        note = `${task.count}个 × ${rule.points}分`;
        break;
        
      case '口算题卡':
        points = task.count * rule.points;
        if (task.allCorrect) {
          points += task.count * rule.bonus['全对'];
          note = `${task.count}篇 × ${rule.points}分 + 全对 ${task.count}分`;
        } else {
          note = `${task.count}篇 × ${rule.points}分`;
        }
        break;
        
      case '英语描红':
        points = rule.points;
        note = '1 次';
        break;
        
      case 'ABC Reading':
        if (task.count >= 2) {
          points = rule.points;
          if (task.autoComplete) {
            points *= rule.autoCompleteMultiplier;
            note = '2 篇 自主完成 ×2';
          } else {
            note = '2 篇';
          }
        }
        break;
        
      case '复述学习内容':
        points = task.over10min ? rule.bonus['超过 10 分钟'] : rule.points;
        note = task.over10min ? '超过 10 分钟' : '10 分钟内';
        break;
        
      case '跳绳':
        if (task.count350) points += 1;
        if (task.speed110) points += 1;
        if (task.speed117) points += 1;
        points = Math.min(points, rule.maxPoints);
        note = `350 个:${task.count350 ? '✓' : '✗'}, 110 个:${task.speed110 ? '✓' : '✗'}, 117 个:${task.speed117 ? '✓' : '✗'}`;
        break;
        
      case '自主洗澡':
      case '自己换居家服':
      case '整理书包':
      case '睡前主动洗漱':
        points = rule.points;
        note = '完成';
        break;
        
      case '学校表扬':
        points = Math.min(task.points, rule.maxPoints);
        note = `${task.points}分`;
        break;
    }
    
    if (points > 0) {
      total += points;
      details.push({ task: task.task, points, note });
    }
  }
  
  return { total, details };
}

module.exports = { parsePointsInput, calculatePoints, TASK_PATTERNS };
