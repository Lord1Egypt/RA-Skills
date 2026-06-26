/**
 * 格式化文章模块
 * 根据平台特点格式化文章内容
 */

/**
 * 根据平台格式化文章
 * @param {Object} data 提取的数据
 * @param {string} platform 平台：douyin, xiaohongshu, weibo
 * @returns {string} 格式化后的文章
 */
function formatArticle(data, platform) {
  switch (platform) {
    case 'douyin':
      return formatDouyinArticle(data);
    case 'xiaohongshu':
      return formatXiaohongshuArticle(data);
    case 'weibo':
      return formatWeiboArticle(data);
    default:
      return formatGenericArticle(data);
  }
}

/**
 * 格式化抖音文章
 */
function formatDouyinArticle(data) {
  const { topic, basicInfo, categories, recommendations } = data;
  
  // 生成吸引眼球的标题
  const title = generateDouyinTitle(topic, basicInfo);
  
  // 生成话题标签
  const hashtags = generateDouyinHashtags(topic, categories);
  
  // 生成正文内容（15秒内可读完）
  const content = generateDouyinContent(data);
  
  // 生成互动引导语
  const callToAction = generateDouyinCallToAction();
  
  return `${title}\n\n${content}\n\n${hashtags}\n\n${callToAction}`;
}

/**
 * 格式化小红书文章
 */
function formatXiaohongshuArticle(data) {
  const { topic, basicInfo, categories, recommendations, quotes } = data;
  
  // 生成标题和话题标签
  const title = `#${topic.replace(/\s+/g, '')} #美食攻略 #时令美食`;
  const hashtags = generateXiaohongshuHashtags(topic, categories);
  
  // 生成正文
  const content = generateXiaohongshuContent(data);
  
  // 生成拍照建议
  const photoTips = generatePhotoTips();
  
  // 生成收藏引导
  const savePrompt = generateSavePrompt();
  
  return `${title}\n\n${content}\n\n${photoTips}\n\n${hashtags}\n\n${savePrompt}`;
}

/**
 * 格式化微博文章
 */
function formatWeiboArticle(data) {
  const { topic, basicInfo, categories, recommendations, statistics } = data;
  
  // 生成话题标签
  const hashtags = generateWeiboHashtags(topic);
  
  // 生成标题
  const title = `【${topic}，你了解多少？】`;
  
  // 生成正文（热点讨论风格）
  const content = generateWeiboContent(data);
  
  // 生成互动元素
  const interaction = generateWeiboInteraction(topic);
  
  // 生成数据支撑
  const dataSupport = generateDataSupport(statistics);
  
  return `${hashtags}\n\n${title}\n\n${content}\n\n${dataSupport}\n\n${interaction}`;
}

/**
 * 生成通用文章
 */
function formatGenericArticle(data) {
  const { topic, basicInfo, categories, recommendations } = data;
  
  return `# ${topic}

## 基本信息
${basicInfo.description || '暂无描述'}

${basicInfo.history ? `## 历史渊源\n${basicInfo.history}\n` : ''}

## 主要特点
${basicInfo.characteristics.length > 0 ? basicInfo.characteristics.map(c => `- ${c}`).join('\n') : '暂无特点描述'}

## 分类信息
${Object.entries(categories)
  .filter(([_, items]) => items.length > 0)
  .map(([category, items]) => `### ${getCategoryName(category)}\n${items.map(item => `- ${item}`).join('\n')}`)
  .join('\n\n')}

## 推荐信息
${recommendations.bestTime ? `### 最佳时间\n${recommendations.bestTime}\n` : ''}
${recommendations.bestPlaces.length > 0 ? `### 推荐地点\n${recommendations.bestPlaces.map(p => `- ${p}`).join('\n')}\n` : ''}
${recommendations.mustTry.length > 0 ? `### 必尝推荐\n${recommendations.mustTry.map(m => `- ${m}`).join('\n')}\n` : ''}
${recommendations.tips.length > 0 ? `### 小贴士\n${recommendations.tips.map(t => `- ${t}`).join('\n')}\n` : ''}

---
*文章基于${statistics?.sourceCount || 0}个来源生成，相关性评分：${statistics?.relevanceScore || 0}/100*`;
}

/**
 * 生成抖音标题
 */
function generateDouyinTitle(topic, basicInfo) {
  const emojis = ['🍜', '✨', '🌟', '💫', '🔥', '👍', '👑'];
  const emoji = emojis[Math.floor(Math.random() * emojis.length)];
  
  const titleTemplates = [
    `${emoji} ${topic}这样吃才地道！`,
    `${emoji} 揭秘${topic}的正确打开方式`,
    `${emoji} ${topic}｜本地人才知道的吃法`,
    `${emoji} 春天必吃！${topic}攻略`,
    `${emoji} ${topic}｜吃货必备指南`
  ];
  
  return titleTemplates[Math.floor(Math.random() * titleTemplates.length)];
}

/**
 * 生成抖音内容
 */
function generateDouyinContent(data) {
  const { categories, recommendations } = data;
  
  const contentParts = [];
  
  // 浇头推荐
  if (categories.toppings.length > 0) {
    const toppings = categories.toppings.slice(0, 3).join('、');
    contentParts.push(`👉 浇头推荐：${toppings}`);
  }
  
  // 最佳时间
  if (recommendations.bestTime) {
    contentParts.push(`👉 最佳时间：${recommendations.bestTime}`);
  }
  
  // 推荐地点
  if (recommendations.bestPlaces.length > 0) {
    const places = recommendations.bestPlaces.slice(0, 2).join('、');
    contentParts.push(`👉 老字号推荐：${places}`);
  }
  
  // 必尝推荐
  if (recommendations.mustTry.length > 0) {
    const mustTry = recommendations.mustTry[0];
    contentParts.push(`👉 必尝：${mustTry}`);
  }
  
  // 小贴士
  if (recommendations.tips.length > 0) {
    const tip = recommendations.tips[0];
    contentParts.push(`👉 小贴士：${tip}`);
  }
  
  return contentParts.join('\n');
}

/**
 * 生成抖音话题标签
 */
function generateDouyinHashtags(topic, categories) {
  const baseHashtags = [
    `#${topic}`,
    '#美食',
    '#吃货',
    '#美食教程',
    '#地方美食'
  ];
  
  const specificHashtags = [];
  
  // 根据分类添加标签
  if (categories.toppings.length > 0) {
    specificHashtags.push('#浇头', '#配料');
  }
  
  if (categories.seasonal.length > 0) {
    specificHashtags.push('#时令美食', '#春季美食');
  }
  
  if (categories.cultural.length > 0) {
    specificHashtags.push('#美食文化', '#传统美食');
  }
  
  // 合并并限制数量
  const allHashtags = [...baseHashtags, ...specificHashtags];
  return allHashtags.slice(0, 8).join(' ');
}

/**
 * 生成抖音互动引导语
 */
function generateDouyinCallToAction() {
  const ctas = [
    '关注我，解锁更多美食攻略！👇',
    '点赞收藏，下次不迷路！❤️',
    '评论区告诉我你想看哪个城市的美食攻略！💬',
    '转发给爱吃面的朋友！👯‍♀️',
    '下期想看什么美食？留言告诉我！📝'
  ];
  
  return ctas[Math.floor(Math.random() * ctas.length)];
}

/**
 * 生成小红书内容
 */
function generateXiaohongshuContent(data) {
  const { topic, basicInfo, categories, recommendations } = data;
  
  const sections = [];
  
  // 引言
  sections.push(`${topic}，作为传统美食的代表，今天给大家分享全攻略！`);
  
  // 浇头推荐
  if (categories.toppings.length > 0) {
    sections.push(`🍜 浇头推荐（精选）：\n${categories.toppings.slice(0, 5).map(t => `• ${t}`).join('\n')}`);
  }
  
  // 最佳时间
  if (recommendations.bestTime) {
    sections.push(`⏰ 最佳时间：${recommendations.bestTime}`);
  }
  
  // 老字号推荐
  if (recommendations.bestPlaces.length > 0) {
    sections.push(`📍 老字号推荐：\n${recommendations.bestPlaces.slice(0, 5).map(p => `• ${p}`).join('\n')}`);
  }
  
  // 吃法讲究
  if (categories.eatingMethods.length > 0) {
    sections.push(`🎯 吃法讲究：\n${categories.eatingMethods.slice(0, 3).map(m => `• ${m}`).join('\n')}`);
  }
  
  // 健康好处
  if (categories.healthBenefits.length > 0) {
    sections.push(`💪 健康好处：\n${categories.healthBenefits.slice(0, 3).map(h => `• ${h}`).join('\n')}`);
  }
  
  // 文化内涵
  if (categories.cultural.length > 0) {
    sections.push(`📚 文化内涵：\n${categories.cultural.slice(0, 2).map(c => `• ${c}`).join('\n')}`);
  }
  
  return sections.join('\n\n');
}

/**
 * 生成小红书话题标签
 */
function generateXiaohongshuHashtags(topic, categories) {
  const baseHashtags = [
    `#${topic.replace(/\s+/g, '')}`,
    '#美食攻略',
    '#吃货日常',
    '#地方美食',
    '#传统美食'
  ];
  
  const specificHashtags = [];
  
  // 添加分类相关标签
  if (categories.seasonal.length > 0) {
    specificHashtags.push('#时令美食', '#春季限定');
  }
  
  if (categories.cultural.length > 0) {
    specificHashtags.push('#美食文化', '#非遗美食');
  }
  
  if (categories.healthBenefits.length > 0) {
    specificHashtags.push('#健康饮食', '#养生美食');
  }
  
  // 合并
  return [...baseHashtags, ...specificHashtags].slice(0, 10).join(' ');
}

/**
 * 生成拍照建议
 */
function generatePhotoTips() {
  return `📸 拍照Tips：
• 拍汤面要体现"观音头、鲤鱼背"
• 浇头特写展示食材新鲜度
• 环境照体现传统风格
• 人物互动增加生活感`;
}

/**
 * 生成收藏引导
 */
function generateSavePrompt() {
  const prompts = [
    '收藏这篇，下次去不迷路！🌟',
    '点赞收藏，美食攻略不丢失！❤️',
    '关注我，更多美食攻略持续更新！👉',
    '转发给朋友，一起打卡美食！👯‍♀️'
  ];
  
  return prompts[Math.floor(Math.random() * prompts.length)];
}

/**
 * 生成微博内容
 */
function generateWeiboContent(data) {
  const { topic, basicInfo, categories, recommendations } = data;
  
  const sections = [];
  
  // 数据开场
  if (categories.toppings.length > 0) {
    sections.push(`数据显示，${topic}最受欢迎的浇头有：${categories.toppings.slice(0, 3).join('、')}`);
  }
  
  // 季节特色
  if (categories.seasonal.length > 0) {
    sections.push(`季节特色：${categories.seasonal[0]}`);
  }
  
  // 文化内涵
  if (categories.cultural.length > 0) {
    sections.push(`文化内涵：${categories.cultural[0]}`);
  }
  
  // 健康好处
  if (categories.healthBenefits.length > 0) {
    sections.push(`健康好处：${categories.healthBenefits[0]}`);
  }
  
  // 老字号推荐
  if (recommendations.bestPlaces.length > 0) {
    sections.push(`老字号推荐：${recommendations.bestPlaces.slice(0, 2).join('、')}`);
  }
  
  return sections.join('\n\n');
}

/**
 * 生成微博话题标签
 */
function generateWeiboHashtags(topic) {
  const baseHashtags = [
    `#${topic}#`,
    '#美食#',
    '#地方美食#',
    '#传统美食#'
  ];
  
  const additionalHashtags = [
    '#美食文化#',
    '#时令饮食#',
    '#饮食养生#',
    '#非遗美食#'
  ];
  
  return [...baseHashtags, ...additionalHashtags].slice(0, 8).join(' ');
}

/**
 * 生成微博互动
 */
function generateWeiboInteraction(topic) {
  const questions = [
    `你最喜欢${topic}的哪种浇头？`,
    `你吃过最地道的${topic}在哪里？`,
    `你觉得${topic}最能代表什么文化？`,
    `你会在什么季节特别想吃${topic}？`
  ];
  
  const question = questions[Math.floor(Math.random() * questions.length)];
  
  const options = ['A', 'B', 'C', 'D'];
  const optionTexts = [
    '经典传统口味',
    '创新改良口味', 
    '季节限定口味',
    '地方特色口味'
  ];
  
  const pollOptions = options.map((opt, i) => `${opt}. ${optionTexts[i]}`).join('\n');
  
  return `🍜 投票：${question}\n\n${pollOptions}\n\n👉 转发+评论，抽3位送美食代金券！`;
}

/**
 * 生成数据支撑
 */
function generateDataSupport(statistics) {
  if (!statistics || statistics.sourceCount === 0) {
    return '';
  }
  
  return `📊 数据支撑：基于${statistics.sourceCount}个权威来源，相关性评分${statistics.relevanceScore}/100`;
}

/**
 * 获取分类名称
 */
function getCategoryName(category) {
  const names = {
    toppings: '浇头推荐',
    soupBases: '汤底类型',
    noodleTypes: '面条种类',
    eatingMethods: '吃法讲究',
    seasonal: '季节限定',
    regional: '地方特色',
    healthBenefits: '健康好处',
    cultural: '文化内涵'
  };
  
  return names[category] || category;
}

module.exports = { formatArticle };