/**
 * 内容生成器
 * 使用 AI 生成祝福语和礼物建议
 */

class ContentGenerator {
  constructor(config = {}) {
    this.config = {
      toneAdaptation: true,
      budgetRules: {
        friend: { max: 300, currency: 'CNY' },
        close_friend: { max: 300, currency: 'CNY' },
        family: { flexible: true },
        colleague: { max: 200, currency: 'CNY' }
      },
      ...config
    };
  }

  /**
   * 生成生日祝福语
   * @param {Object} contact - 联系人信息
   * @param {Object} event - 事件信息
   * @param {Object} options - 生成选项
   * @returns {string} 生成的祝福语
   */
  async generateBirthdayWish(contact, event, options = {}) {
    const { 
      style = 'casual',  // casual | formal | humorous | warm
      length = 'medium',  // short | medium | long
      includeEmoji = true
    } = options;

    const context = this.buildContext(contact, event);
    
    // 根据关系类型选择基础模板
    const templates = this.getTemplates(contact.relationship, style);
    
    // 个性化处理
    let wish = this.personalizeTemplate(templates, context);
    
    // 根据长度调整
    wish = this.adjustLength(wish, length);
    
    // 添加表情符号
    if (includeEmoji) {
      wish = this.addEmojis(wish, contact.relationship);
    }

    return wish;
  }

  /**
   * 生成礼物建议
   * @param {Object} contact - 联系人信息
   * @param {Object} event - 事件信息
   * @returns {Object} 礼物建议对象
   */
  async generateGiftSuggestion(contact, event) {
    const budget = this.getBudget(contact.relationship);
    const preferences = this.parsePreferences(contact);
    
    const suggestions = {
      budget: budget,
      categories: [],
      specificIdeas: [],
      reasoning: ''
    };

    // 根据关系类型和偏好生成建议
    switch (contact.relationship) {
      case 'family':
        suggestions.categories = ['实用家居', '健康关怀', '纪念相册'];
        suggestions.reasoning = '家人礼物重在心意和实用性';
        break;
      case 'close_friend':
        suggestions.categories = ['兴趣爱好相关', '体验类礼物', '定制礼品'];
        suggestions.reasoning = '密友之间可以选择更有个人特色的礼物';
        break;
      case 'friend':
        suggestions.categories = ['书籍', '小家电', '文创产品'];
        suggestions.reasoning = '朋友礼物宜选实用且有心意的物品';
        break;
      case 'colleague':
        suggestions.categories = ['办公用品', '零食礼盒', '绿植'];
        suggestions.reasoning = '同事礼物宜保持适度，避免过于私人化';
        break;
      default:
        suggestions.categories = ['通用礼品'];
    }

    // 根据具体偏好细化建议
    if (preferences.hobbies) {
      suggestions.specificIdeas = this.generateSpecificIdeas(preferences.hobbies, budget);
    }

    return suggestions;
  }

  /**
   * 构建上下文信息
   */
  buildContext(contact, event) {
    return {
      name: contact.name,
      relationship: contact.relationship,
      relationshipDetail: contact.relationship_detail || '',
      tags: contact.tags || [],
      eventType: event.type,
      eventName: event.name,
      notes: contact.notes || ''
    };
  }

  /**
   * 获取祝福语模板
   */
  getTemplates(relationship, style) {
    const templates = {
      family: {
        warm: [
          "亲爱的{name}，祝你生日快乐！愿健康、快乐永远陪伴着你。",
          "{name}，又长了一岁，愿你在新的一年里身体健康，万事如意！"
        ],
        casual: [
          "{name}生日快乐！希望你每天都开开心心的。",
          "祝{name}生日快乐，越来越年轻！"
        ],
        humorous: [
          "{name}，生日快乐！虽然你又老了一岁，但在我眼里永远是最棒的！",
          "恭喜{name}成功升级到最新版本，bug全修复，性能更强劲！"
        ]
      },
      close_friend: {
        warm: [
          "{name}，生日快乐！很庆幸能有你这样的朋友，愿你所有的愿望都能实现。",
          "老朋友{name}，生日快乐！无论时光如何流转，我们的友谊永远不变。"
        ],
        casual: [
          "{name}生日快乐！晚上一起吃饭庆祝吧！",
          "祝我最铁的哥们{name}生日快乐，永远18岁！"
        ],
        humorous: [
          "{name}，生日快乐！记得许愿的时候别把我忘了，毕竟我这么帅的朋友不好找。",
          "祝{name}生日快乐，愿你年年有今日，岁岁有今朝，虽然这意味着你又老了..."
        ]
      },
      friend: {
        warm: [
          "{name}，生日快乐！很高兴认识你，祝你前程似锦。",
          "祝{name}生日快乐，愿你的生活充满阳光和欢笑。"
        ],
        casual: [
          "{name}生日快乐！祝你一切顺利。",
          "祝{name}生日快乐，天天好心情！"
        ],
        humorous: [
          "{name}，生日快乐！又成功活过了一年，真不容易啊！",
          "祝{name}生日快乐，愿你早日实现暴富的梦想，然后别忘了请我吃饭！"
        ]
      },
      colleague: {
        warm: [
          "{name}，生日快乐！很高兴能和你一起工作，祝你工作顺利。",
          "祝{name}生日快乐，愿你的事业更上一层楼。"
        ],
        casual: [
          "{name}生日快乐！工作再忙也要注意身体哦。",
          "祝{name}生日快乐，工作顺利，生活愉快！"
        ],
        humorous: [
          "{name}，生日快乐！希望老板今天能让你早点下班。",
          "祝{name}生日快乐，愿你代码无bug，需求不更改！"
        ]
      }
    };

    const relationshipTemplates = templates[relationship] || templates.friend;
    return relationshipTemplates[style] || relationshipTemplates.casual;
  }

  /**
   * 个性化模板
   */
  personalizeTemplate(templates, context) {
    let template = templates[Math.floor(Math.random() * templates.length)];
    
    // 替换基本占位符
    template = template.replace(/{name}/g, context.name);
    
    // 根据关系详情添加个性化内容
    if (context.relationshipDetail && context.relationshipDetail.includes('大学')) {
      template = template.replace(/生日快乐/, '生日快乐！大学时光历历在目');
    }
    
    if (context.tags && context.tags.includes('篮球')) {
      template += ' 希望你球场上依旧生龙活虎！';
    }
    
    if (context.tags && context.tags.includes('科技')) {
      template += ' 祝你早日拿到最新的科技产品！';
    }

    return template;
  }

  /**
   * 调整祝福语长度
   */
  adjustLength(wish, length) {
    const lengthMap = {
      short: 50,
      medium: 100,
      long: 200
    };
    
    const maxLength = lengthMap[length] || 100;
    
    if (wish.length > maxLength) {
      // 截取到最近的句号
      const truncated = wish.substring(0, maxLength);
      const lastPeriod = truncated.lastIndexOf('。');
      if (lastPeriod > 0) {
        return truncated.substring(0, lastPeriod + 1);
      }
    }
    
    return wish;
  }

  /**
   * 添加表情符号
   */
  addEmojis(wish, relationship) {
    const emojiMap = {
      family: ['🎂', '❤️', '🎉'],
      close_friend: ['🎂', '🎉', '🍻', '🎁'],
      friend: ['🎂', '🎉', '🎈'],
      colleague: ['🎂', '💼', '🎊']
    };

    const emojis = emojiMap[relationship] || emojiMap.friend;
    const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
    
    return `${randomEmoji} ${wish}`;
  }

  /**
   * 获取预算
   */
  getBudget(relationship) {
    const rule = this.config.budgetRules[relationship] || this.config.budgetRules.friend;
    
    if (rule.flexible) {
      return { type: 'flexible', description: '根据具体情况弹性调整' };
    }
    
    return { 
      type: 'fixed', 
      max: rule.max, 
      currency: rule.currency 
    };
  }

  /**
   * 解析偏好
   */
  parsePreferences(contact) {
    const preferences = {
      hobbies: contact.tags || [],
      dislikes: [],
      notes: contact.notes || ''
    };

    // 从 notes 中提取不喜欢的东西
    if (contact.notes) {
      const dislikeMatch = contact.notes.match(/不喜欢(.+?)(?=\n|$)/);
      if (dislikeMatch) {
        preferences.dislikes = dislikeMatch[1].split(/[,，]/).map(s => s.trim());
      }
    }

    return preferences;
  }

  /**
   * 生成具体建议
   */
  generateSpecificIdeas(hobbies, budget) {
    const ideas = [];
    
    const hobbyIdeas = {
      '篮球': ['篮球周边', '球衣', '运动鞋', '球星卡'],
      '足球': ['足球', '球衣', '球鞋'],
      '音乐': ['耳机', '音响', '专辑'],
      '阅读': ['书籍', '电子书阅读器', '书签'],
      '游戏': ['游戏周边', '手柄', '游戏卡'],
      '摄影': ['相机配件', '相册', '三脚架'],
      '美食': ['零食礼盒', '餐厅券', '厨具'],
      '旅行': ['旅行用品', '行李箱', '相机']
    };

    hobbies.forEach(hobby => {
      if (hobbyIdeas[hobby]) {
        ideas.push(...hobbyIdeas[hobby]);
      }
    });

    // 根据预算过滤
    if (budget.type === 'fixed') {
      // 这里可以添加价格过滤逻辑
      return ideas.slice(0, 3);
    }

    return ideas.slice(0, 5);
  }

  /**
   * 生成提醒消息
   */
  async generateReminderMessage(contact, event, reminderType) {
    const wish = await this.generateBirthdayWish(contact, event);
    const giftSuggestion = await this.generateGiftSuggestion(contact, event);

    let message = '';

    if (reminderType === 'today') {
      message = `🎉 **今天提醒**\n\n`;
      message += `今天是 **${contact.name}** 的 **${event.name}**！\n\n`;
      message += `**祝福语：**\n${wish}\n\n`;
    } else {
      message = `📅 **提前提醒**\n\n`;
      message += `${contact.name} 的 ${event.name} 还有7天就到了（${event.target_date}）。\n\n`;
    }

    message += `**礼物建议：**\n`;
    if (giftSuggestion.budget.type === 'fixed') {
      message += `预算：≤${giftSuggestion.budget.max}元\n`;
    } else {
      message += `预算：${giftSuggestion.budget.description}\n`;
    }
    message += `类别：${giftSuggestion.categories.join('、')}\n`;
    
    if (giftSuggestion.specificIdeas.length > 0) {
      message += `具体建议：${giftSuggestion.specificIdeas.join('、')}\n`;
    }

    return message;
  }
}

module.exports = ContentGenerator;
