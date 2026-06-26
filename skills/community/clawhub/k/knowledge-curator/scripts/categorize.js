/**
 * categorize.js - 自动分类模块
 * 
 * 基于内容语义自动将知识条目分类到指定主题
 * 支持：科技、生活、学习、娱乐、工作、健康
 */

// 分类定义和特征词库
const CATEGORIES = {
  科技: {
    keywords: [
      'AI', '人工智能', '机器学习', '深度学习', '神经网络',
      '编程', '代码', '开发', '软件', '算法', '数据科学',
      '互联网', '网络', '云计算', '大数据', '区块链',
      '数码', '手机', '电脑', '硬件', '芯片', '半导体',
      '科学', '技术', '创新', '研发', '科技', 'IT', '互联网'
    ],
    weight: 1.0
  },
  
  生活: {
    keywords: [
      '美食', '餐厅', '做饭', '菜谱', '烹饪',
      '旅行', '旅游', '景点', '酒店', '机票',
      '家居', '装修', '家具', '收纳', '生活',
      '日常', '情感', '恋爱', '婚姻', '家庭',
      '购物', '穿搭', '时尚', '美妆', '护肤'
    ],
    weight: 1.0
  },
  
  学习: {
    keywords: [
      '教育', '学习', '课程', '教程', '培训',
      '考试', '学校', '大学', '考研', '留学',
      '知识', '技能', '提升', '成长', '进步',
      '读书', '阅读', '笔记', '资料', '教材',
      '语言', '英语', '外语', '证书', '资格'
    ],
    weight: 1.0
  },
  
  娱乐: {
    keywords: [
      '影视', '电影', '电视剧', '综艺', '动画',
      '音乐', '歌曲', '歌手', '演唱会', '专辑',
      '游戏', '手游', '电竞', '玩家', '攻略',
      '明星', '偶像', '艺人', '八卦', '娱乐',
      '搞笑', '段子', '幽默', '笑话', '趣味'
    ],
    weight: 1.0
  },
  
  工作: {
    keywords: [
      '职场', '工作', '上班', '公司', '企业',
      '管理', '领导', '团队', '协作', '沟通',
      '效率', '时间管理', '工具', '方法论',
      '商业', '创业', '投资', '金融', '经济',
      '面试', '简历', '求职', '招聘', '薪资'
    ],
    weight: 1.0
  },
  
  健康: {
    keywords: [
      '运动', '健身', '锻炼', '瑜伽', '跑步',
      '饮食', '营养', '减肥', '瘦身', '健康',
      '医疗', '医院', '医生', '疾病', '治疗',
      '心理', '情绪', '压力', '睡眠', '冥想',
      '养生', '保健', '中医', '调理', '长寿'
    ],
    weight: 1.0
  }
};

/**
 * 计算内容与分类的匹配度
 * @param {string} text - 待分类文本
 * @param {string} categoryName - 分类名称
 * @returns {number} 匹配度分数 (0-1)
 */
function calculateMatchScore(text, categoryName) {
  const category = CATEGORIES[categoryName];
  if (!category) return 0;
  
  const textLower = text.toLowerCase();
  let score = 0;
  
  for (const keyword of category.keywords) {
    const keywordLower = keyword.toLowerCase();
    const regex = new RegExp(keywordLower, 'gi');
    const matches = textLower.match(regex);
    if (matches) {
      score += matches.length;
    }
  }
  
  // 归一化分数
  const maxPossibleScore = category.keywords.length * (text.length / 100);
  const normalizedScore = Math.min(score / Math.max(maxPossibleScore, 1), 1);
  
  return normalizedScore * category.weight;
}

/**
 * 对内容进行分类
 * @param {Object} content - 内容对象 {title, description, content, tags}
 * @returns {Object} 分类结果 {category, scores, confidence}
 */
function categorize(content) {
  const textToAnalyze = [
    content.title || '',
    content.description || '',
    content.content || '',
    (content.tags || []).join(' ')
  ].join(' ');
  
  const scores = {};
  let bestCategory = null;
  let bestScore = 0;
  
  // 计算每个分类的得分
  for (const categoryName of Object.keys(CATEGORIES)) {
    const score = calculateMatchScore(textToAnalyze, categoryName);
    scores[categoryName] = score;
    
    if (score > bestScore) {
      bestScore = score;
      bestCategory = categoryName;
    }
  }
  
  // 计算置信度
  const scoreValues = Object.values(scores);
  const sortedScores = [...scoreValues].sort((a, b) => b - a);
  const confidence = sortedScores.length > 1 
    ? (sortedScores[0] - sortedScores[1]) / sortedScores[0] 
    : 1;
  
  // 如果最高分太低，标记为不确定
  if (bestScore < 0.1) {
    return {
      category: '未分类',
      scores,
      confidence: 0,
      uncertain: true
    };
  }
  
  return {
    category: bestCategory,
    scores,
    confidence,
    uncertain: confidence < 0.3
  };
}

/**
 * 批量分类
 * @param {Array<Object>} contents - 内容数组
 * @returns {Array<Object>} 分类结果数组
 */
function batchCategorize(contents) {
  return contents.map(content => ({
    ...content,
    classification: categorize(content)
  }));
}

/**
 * 获取分类统计
 * @param {Array<Object>} classifiedContents - 已分类内容数组
 * @returns {Object} 统计信息
 */
function getCategoryStats(classifiedContents) {
  const stats = {};
  
  for (const content of classifiedContents) {
    const category = content.classification?.category || '未分类';
    stats[category] = (stats[category] || 0) + 1;
  }
  
  return stats;
}

/**
 * 根据用户反馈调整分类权重（可选的自学习功能）
 * @param {string} categoryName - 分类名称
 * @param {Array<string>} newKeywords - 新增关键词
 */
function adjustCategoryWeights(categoryName, newKeywords) {
  if (CATEGORIES[categoryName]) {
    for (const keyword of newKeywords) {
      if (!CATEGORIES[categoryName].keywords.includes(keyword)) {
        CATEGORIES[categoryName].keywords.push(keyword);
      }
    }
  }
}

// 导出模块
module.exports = {
  categorize,
  batchCategorize,
  getCategoryStats,
  calculateMatchScore,
  adjustCategoryWeights,
  CATEGORIES
};

// CLI 模式支持
if (require.main === module) {
  const testContent = {
    title: process.argv[2] || '测试标题',
    description: process.argv[3] || '测试描述',
    content: process.argv[4] || '',
    tags: []
  };
  
  const result = categorize(testContent);
  console.log('\n=== 分类结果 ===');
  console.log(`分类：${result.category}`);
  console.log(`置信度：${(result.confidence * 100).toFixed(2)}%`);
  console.log(`不确定：${result.uncertain ? '是' : '否'}`);
  console.log('\n各分类得分:');
  for (const [category, score] of Object.entries(result.scores)) {
    console.log(`  ${category}: ${(score * 100).toFixed(2)}%`);
  }
}
