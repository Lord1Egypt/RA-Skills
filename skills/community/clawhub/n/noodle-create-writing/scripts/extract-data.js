/**
 * 提取关键数据模块
 * 从搜索结果中提取结构化数据
 */

/**
 * 从搜索结果中提取关键数据
 * @param {Object} searchResults 搜索结果
 * @param {Object} options 选项
 * @returns {Object} 提取的结构化数据
 */
function extractData(searchResults, options = {}) {
  const { topic, verbose = false } = options;
  
  const sources = searchResults.sources || [];
  const summary = searchResults.summary || '';
  
  if (verbose) {
    console.log(`📊 处理 ${sources.length} 个来源`);
  }
  
  // 初始化数据结构
  const data = {
    topic,
    basicInfo: {
      description: '',
      characteristics: [],
      history: ''
    },
    categories: {
      toppings: [],      // 浇头
      soupBases: [],     // 汤底
      noodleTypes: [],   // 面条类型
      eatingMethods: [], // 吃法
      seasonal: [],      // 季节限定
      regional: [],      // 地方特色
      healthBenefits: [], // 健康好处
      cultural: []       // 文化内涵
    },
    recommendations: {
      bestTime: '',      // 最佳时间
      bestPlaces: [],    // 推荐地点
      mustTry: [],       // 必尝推荐
      tips: []           // 小贴士
    },
    statistics: {
      sourceCount: sources.length,
      topSources: [],
      relevanceScore: 0
    },
    quotes: [],          // 引用语句
    keywords: searchResults.keywords || []
  };
  
  // 处理每个来源
  for (const source of sources) {
    const content = (source.content || '').toLowerCase();
    const title = (source.title || '').toLowerCase();
    
    // 提取基本信息
    extractBasicInfo(data, content, title, source);
    
    // 提取分类信息
    extractCategoryInfo(data, content, title);
    
    // 提取推荐信息
    extractRecommendationInfo(data, content, title);
    
    // 收集引用
    if (source.content && source.content.length > 20 && source.content.length < 200) {
      data.quotes.push({
        text: source.content.trim(),
        source: source.title,
        url: source.url
      });
    }
  }
  
  // 处理总结
  if (summary) {
    data.basicInfo.description = summary;
  }
  
  // 去重和排序
  processExtractedData(data);
  
  // 计算相关性分数
  data.statistics.relevanceScore = calculateRelevanceScore(data, sources);
  
  // 选择最重要的来源
  data.statistics.topSources = sources
    .slice(0, 5)
    .map(s => ({ title: s.title, url: s.url, relevance: s.relevance }));
  
  if (verbose) {
    console.log('✅ 数据提取完成');
    console.log(`📈 提取到：${data.categories.toppings.length} 种浇头，${data.recommendations.bestPlaces.length} 个推荐地点`);
  }
  
  return data;
}

/**
 * 提取基本信息
 */
function extractBasicInfo(data, content, title, source) {
  // 提取描述
  if (!data.basicInfo.description && content.length > 50) {
    const sentences = content.split(/[.!?。！？]/);
    if (sentences[0] && sentences[0].length > 20) {
      data.basicInfo.description = sentences[0].trim();
    }
  }
  
  // 提取特点
  const characteristicKeywords = ['特点', '特色', '特征', '独特', '与众不同'];
  if (characteristicKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (characteristicKeywords.some(keyword => line.includes(keyword)) && line.length > 10) {
        data.basicInfo.characteristics.push(line.trim());
      }
    }
  }
  
  // 提取历史
  const historyKeywords = ['历史', '由来', '起源', '传统', '古老', '百年'];
  if (historyKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (historyKeywords.some(keyword => line.includes(keyword)) && line.length > 15) {
        if (!data.basicInfo.history) {
          data.basicInfo.history = line.trim();
        }
      }
    }
  }
}

/**
 * 提取分类信息
 */
function extractCategoryInfo(data, content, title) {
  // 浇头提取
  const toppingKeywords = ['浇头', '配料', '臊子', '码子', 'topping'];
  const toppingItems = ['焖肉', '爆鱼', '爆鳝', '虾仁', '卤鸭', '大排', '炒素', '三虾', '蟹粉', '秃黄油'];
  
  if (toppingKeywords.some(keyword => content.includes(keyword))) {
    for (const item of toppingItems) {
      if (content.includes(item.toLowerCase())) {
        data.categories.toppings.push(item);
      }
    }
  }
  
  // 汤底提取
  const soupKeywords = ['汤', '汤底', '汤头', '高汤', 'soup'];
  const soupTypes = ['红汤', '白汤', '清汤', '浓汤'];
  
  if (soupKeywords.some(keyword => content.includes(keyword))) {
    for (const type of soupTypes) {
      if (content.includes(type.toLowerCase())) {
        data.categories.soupBases.push(type);
      }
    }
  }
  
  // 吃法提取
  const eatingKeywords = ['吃法', '怎么吃', '如何吃', '吃的方式', 'eating method'];
  const eatingMethods = ['宽汤', '紧汤', '重青', '免青', '过桥', '头汤面'];
  
  if (eatingKeywords.some(keyword => content.includes(keyword))) {
    for (const method of eatingMethods) {
      if (content.includes(method.toLowerCase())) {
        data.categories.eatingMethods.push(method);
      }
    }
  }
  
  // 季节限定提取
  const seasonalKeywords = ['季节', '时令', '春季', '夏季', '秋季', '冬季', 'seasonal'];
  if (seasonalKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (seasonalKeywords.some(keyword => line.includes(keyword)) && line.length > 10) {
        data.categories.seasonal.push(line.trim());
      }
    }
  }
  
  // 健康好处提取
  const healthKeywords = ['健康', '营养', '养生', '好处', '功效', 'health', 'benefit'];
  if (healthKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (healthKeywords.some(keyword => line.includes(keyword)) && line.length > 10) {
        data.categories.healthBenefits.push(line.trim());
      }
    }
  }
  
  // 文化内涵提取
  const cultureKeywords = ['文化', '内涵', '历史', '传统', '民俗', 'culture'];
  if (cultureKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (cultureKeywords.some(keyword => line.includes(keyword)) && line.length > 15) {
        data.categories.cultural.push(line.trim());
      }
    }
  }
}

/**
 * 提取推荐信息
 */
function extractRecommendationInfo(data, content, title) {
  // 最佳时间提取
  const timeKeywords = ['时间', '时候', '时机', '最佳时间', '最好吃', 'time', 'best time'];
  if (timeKeywords.some(keyword => content.includes(keyword)) && !data.recommendations.bestTime) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (timeKeywords.some(keyword => line.includes(keyword)) && line.length > 8) {
        data.recommendations.bestTime = line.trim();
        break;
      }
    }
  }
  
  // 推荐地点提取
  const placeKeywords = ['地方', '地点', '店铺', '面馆', '老字号', '推荐', 'place', 'restaurant'];
  const placeNames = ['松鹤楼', '朱鸿兴', '同得兴', '裕面堂', '陆长兴', '黄天源'];
  
  if (placeKeywords.some(keyword => content.includes(keyword))) {
    for (const place of placeNames) {
      if (content.includes(place.toLowerCase())) {
        data.recommendations.bestPlaces.push(place);
      }
    }
  }
  
  // 必尝推荐提取
  const mustTryKeywords = ['必吃', '必尝', '推荐', '招牌', '特色', 'must try'];
  if (mustTryKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (mustTryKeywords.some(keyword => line.includes(keyword)) && line.length > 8) {
        data.recommendations.mustTry.push(line.trim());
      }
    }
  }
  
  // 小贴士提取
  const tipsKeywords = ['贴士', '技巧', '注意', '建议', 'tip', 'advice'];
  if (tipsKeywords.some(keyword => content.includes(keyword))) {
    const lines = content.split(/[.!?。！？]/);
    for (const line of lines) {
      if (tipsKeywords.some(keyword => line.includes(keyword)) && line.length > 8) {
        data.recommendations.tips.push(line.trim());
      }
    }
  }
}

/**
 * 处理提取的数据（去重、排序等）
 */
function processExtractedData(data) {
  // 去重
  for (const category in data.categories) {
    data.categories[category] = [...new Set(data.categories[category])];
  }
  
  data.recommendations.bestPlaces = [...new Set(data.recommendations.bestPlaces)];
  data.recommendations.mustTry = [...new Set(data.recommendations.mustTry)];
  data.recommendations.tips = [...new Set(data.recommendations.tips)];
  
  // 限制数量
  data.categories.toppings = data.categories.toppings.slice(0, 10);
  data.categories.soupBases = data.categories.soupBases.slice(0, 5);
  data.categories.eatingMethods = data.categories.eatingMethods.slice(0, 8);
  data.categories.seasonal = data.categories.seasonal.slice(0, 5);
  data.categories.healthBenefits = data.categories.healthBenefits.slice(0, 5);
  data.categories.cultural = data.categories.cultural.slice(0, 5);
  
  data.recommendations.bestPlaces = data.recommendations.bestPlaces.slice(0, 8);
  data.recommendations.mustTry = data.recommendations.mustTry.slice(0, 5);
  data.recommendations.tips = data.recommendations.tips.slice(0, 5);
  
  // 排序（按长度或重要性）
  data.categories.toppings.sort();
  data.recommendations.bestPlaces.sort();
}

/**
 * 计算相关性分数
 */
function calculateRelevanceScore(data, sources) {
  if (sources.length === 0) return 0;
  
  let score = 0;
  
  // 基础分数：来源数量和质量
  score += Math.min(sources.length, 10) * 5;
  
  // 数据丰富度分数
  const dataPoints = 
    data.categories.toppings.length +
    data.categories.soupBases.length +
    data.categories.eatingMethods.length +
    data.recommendations.bestPlaces.length +
    data.categories.healthBenefits.length +
    data.categories.cultural.length;
  
  score += Math.min(dataPoints, 20) * 2;
  
  // 关键信息完整性分数
  if (data.basicInfo.description) score += 10;
  if (data.recommendations.bestTime) score += 5;
  if (data.basicInfo.history) score += 5;
  if (data.categories.cultural.length > 0) score += 5;
  
  return Math.min(score, 100);
}

module.exports = { extractData };