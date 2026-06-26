/**
 * Kuuila Game v2.8 - 核心诡计生成器
 * 基于《针本》的核心诡计模式
 * 
 * 核心诡计 = 类型 + 触发条件 + 揭示方式
 * 类型: 反转/误导/隐藏
 */

// ==================== 数据结构 ====================

/**
 * 核心诡计
 */
class CoreTrick {
  constructor(config = {}) {
    this.id = config.id || `trick_${Date.now()}`;
    this.name = config.name || '未命名诡计';
    this.type = config.type || 'reversal'; // reversal/misdirection/concealment
    this.description = config.description || '';
    this.trigger = config.trigger || null; // 触发条件
    this.reveal = config.reveal || null; // 揭示方式
    this.hints = config.hints || []; // 提示列表
    this.redHerrings = config.redHerrings || []; // 红鲱鱼（误导线索）
    this.difficulty = config.difficulty || 'medium'; // easy/medium/hard/expert
    this.metadata = config.metadata || {};
  }

  addHint(hint) {
    this.hints.push(hint);
    return this;
  }

  addRedHerring(herring) {
    this.redHerrings.push(herring);
    return this;
  }
}

/**
 * 触发条件
 */
class TriggerCondition {
  constructor(config = {}) {
    this.id = config.id || `trigger_${Date.now()}`;
    this.type = config.type || 'choice'; // choice/item/stat/time/location
    this.description = config.description || '';
    this.requirements = config.requirements || {};
    this.probability = config.probability || 1.0;
    this.metadata = config.metadata || {};
  }

  evaluate(context) {
    switch (this.type) {
      case 'choice':
        return this.evaluateChoice(context);
      case 'item':
        return this.evaluateItem(context);
      case 'stat':
        return this.evaluateStat(context);
      case 'time':
        return this.evaluateTime(context);
      case 'location':
        return this.evaluateLocation(context);
      case 'combination':
        return this.evaluateCombination(context);
      default:
        return true;
    }
  }

  evaluateChoice(context) {
    if (!context.choices) return false;
    return this.requirements.choices?.every(c => context.choices.includes(c));
  }

  evaluateItem(context) {
    if (!context.items) return false;
    return this.requirements.items?.every(i => context.items.includes(i));
  }

  evaluateStat(context) {
    if (!context.stats) return false;
    return Object.entries(this.requirements.stats || {}).every(
      ([stat, value]) => context.stats[stat] >= value
    );
  }

  evaluateTime(context) {
    if (!context.time) return false;
    const { min, max } = this.requirements.time || {};
    return (!min || context.time >= min) && (!max || context.time <= max);
  }

  evaluateLocation(context) {
    if (!context.location) return false;
    return this.requirements.locations?.includes(context.location);
  }

  evaluateCombination(context) {
    return this.requirements.conditions?.every(cond => {
      const trigger = new TriggerCondition(cond);
      return trigger.evaluate(context);
    });
  }
}

/**
 * 揭示方式
 */
class RevealMethod {
  constructor(config = {}) {
    this.id = config.id || `reveal_${Date.now()}`;
    this.type = config.type || 'direct'; // direct/gradual/puzzle/narrative
    this.description = config.description || '';
    this.steps = config.steps || []; // 揭示步骤
    this.consequences = config.consequences || []; // 揭示后的后果
    this.metadata = config.metadata || {};
  }

  /**
   * 执行揭示
   */
  execute(context) {
    const results = [];

    switch (this.type) {
      case 'direct':
        results.push(this.revealDirect(context));
        break;
      case 'gradual':
        results.push(...this.revealGradual(context));
        break;
      case 'puzzle':
        results.push(this.revealPuzzle(context));
        break;
      case 'narrative':
        results.push(this.revealNarrative(context));
        break;
    }

    // 应用后果
    this.consequences.forEach(cons => {
      results.push(this.applyConsequence(cons, context));
    });

    return results;
  }

  revealDirect(context) {
    return {
      type: 'reveal',
      method: 'direct',
      message: this.description,
      immediate: true
    };
  }

  revealGradual(context) {
    return this.steps.map((step, index) => ({
      type: 'reveal',
      method: 'gradual',
      step: index + 1,
      totalSteps: this.steps.length,
      message: step,
      immediate: index === 0
    }));
  }

  revealPuzzle(context) {
    const solved = this.checkPuzzleSolution(context);
    return {
      type: 'reveal',
      method: 'puzzle',
      solved: solved,
      message: solved ? this.description : this.getHint(context),
      immediate: solved
    };
  }

  revealNarrative(context) {
    return {
      type: 'reveal',
      method: 'narrative',
      message: this.generateNarrative(context),
      immediate: true
    };
  }

  checkPuzzleSolution(context) {
    if (!context.puzzleAnswers) return false;
    return this.requirements?.answers?.every(a => context.puzzleAnswers.includes(a));
  }

  getHint(context) {
    const hintsAvailable = this.steps.filter((_, i) => 
      context.hintsUsed?.includes(i) === false
    );
    if (hintsAvailable.length === 0) return null;
    return hintsAvailable[0];
  }

  generateNarrative(context) {
    let narrative = this.description;
    
    // 根据上下文定制叙述
    if (context.characterName) {
      narrative = narrative.replace('{character}', context.characterName);
    }
    if (context.locationName) {
      narrative = narrative.replace('{location}', context.locationName);
    }
    
    return narrative;
  }

  applyConsequence(consequence, context) {
    return {
      type: 'consequence',
      effect: consequence.type,
      value: consequence.value,
      target: consequence.target
    };
  }
}

// ==================== 核心诡计生成器 ====================

class CoreTrickGenerator {
  constructor(config = {}) {
    this.config = {
      difficulty: config.difficulty || 'medium',
      theme: config.theme || 'horror', // horror/mystery/sci-fi/fantasy
      style: config.style || 'classic', // classic/modern/experimental
      ...config
    };

    // 诡计类型概率分布
    this.typeDistribution = {
      reversal: 0.35,      // 反转
      misdirection: 0.40,  // 误导
      concealment: 0.25    // 隐藏
    };

    // 难度参数
    this.difficultyParams = {
      easy: {
        hints: 5,
        redHerrings: 1,
        triggerComplexity: 1,
        revealSteps: 1
      },
      medium: {
        hints: 3,
        redHerrings: 3,
        triggerComplexity: 2,
        revealSteps: 3
      },
      hard: {
        hints: 1,
        redHerrings: 5,
        triggerComplexity: 3,
        revealSteps: 5
      },
      expert: {
        hints: 0,
        redHerrings: 7,
        triggerComplexity: 4,
        revealSteps: 7
      }
    };

    // 主题词库
    this.themeVocabulary = {
      horror: {
        objects: ['古镜', '黑书', '遗物', '诅咒', '符文', '祭坛'],
        entities: ['幽魂', '邪神', '异种', '梦魇', '分身', '替身'],
        locations: ['废弃宅邸', '地下实验室', '精神病院', '古墓', '深海'],
        events: ['仪式', '献祭', '附身', '变异', '觉醒', '降临']
      },
      mystery: {
        objects: ['密信', '遗书', '证据', '密码', '钥匙', '照片'],
        entities: ['凶手', '目击者', '嫌疑人', '侦探', '叛徒'],
        locations: ['密室', '庄园', '火车', '孤岛', '档案室'],
        events: ['谋杀', '失踪', '盗窃', '背叛', '复仇']
      },
      'sci-fi': {
        objects: ['芯片', '程序', '信号', '装置', '档案', '样本'],
        entities: ['AI', '外星人', '仿生人', '时间旅行者', '观察者'],
        locations: ['空间站', '实验室', '虚拟世界', '未来城市', '黑洞边缘'],
        events: ['实验事故', '时空扭曲', '意识上传', '文明崩溃', '觉醒']
      },
      fantasy: {
        objects: ['法器', '卷轴', '宝石', '圣剑', '秘药', '符咒'],
        entities: ['恶魔', '天使', '龙', '精灵', '亡灵', '元素'],
        locations: ['魔法塔', '地下城', '精灵森林', '龙巢', '异次元'],
        events: ['召唤', '转生', '诅咒解除', '神器觉醒', '世界重塑']
      }
    };
  }

  /**
   * 生成核心诡计
   */
  generate(options = {}) {
    const theme = options.theme || this.config.theme;
    const difficulty = options.difficulty || this.config.difficulty;
    const type = options.type || this.selectType();

    const params = this.difficultyParams[difficulty];
    const vocabulary = this.themeVocabulary[theme] || this.themeVocabulary.horror;

    // 生成基础诡计
    const trick = new CoreTrick({
      id: `trick_${Date.now()}`,
      name: this.generateName(type, vocabulary),
      type: type,
      description: this.generateDescription(type, vocabulary),
      difficulty: difficulty
    });

    // 生成触发条件
    trick.trigger = this.generateTrigger(type, params.triggerComplexity, vocabulary);

    // 生成揭示方式
    trick.reveal = this.generateReveal(type, params.revealSteps, vocabulary);

    // 生成提示
    for (let i = 0; i < params.hints; i++) {
      trick.addHint(this.generateHint(type, i, vocabulary, trick.description));
    }

    // 生成红鲱鱼
    for (let i = 0; i < params.redHerrings; i++) {
      trick.addRedHerring(this.generateRedHerring(vocabulary));
    }

    return trick;
  }

  /**
   * 选择诡计类型
   */
  selectType() {
    const rand = Math.random();
    let cumulative = 0;
    
    for (const [type, prob] of Object.entries(this.typeDistribution)) {
      cumulative += prob;
      if (rand <= cumulative) {
        return type;
      }
    }
    
    return 'reversal';
  }

  /**
   * 生成诡计名称
   */
  generateName(type, vocabulary) {
    const objects = vocabulary.objects;
    const events = vocabulary.events;
    
    const templates = {
      reversal: `${objects[Math.floor(Math.random() * objects.length)]}的${events[Math.floor(Math.random() * events.length)]}`,
      misdirection: `${vocabulary.entities[Math.floor(Math.random() * vocabulary.entities.length)]}之${objects[Math.floor(Math.random() * objects.length)]}`,
      concealment: `隐藏的${objects[Math.floor(Math.random() * objects.length)]}`
    };
    
    return templates[type];
  }

  /**
   * 生成描述
   */
  generateDescription(type, vocabulary) {
    const templates = {
      reversal: [
        `看似${vocabulary.events[0]}，实则是${vocabulary.events[3]}`,
        `${vocabulary.entities[0]}的真正目的是${vocabulary.events[4]}`,
        `所有的${vocabulary.objects[0]}都是${vocabulary.objects[3]}的伪装`
      ],
      misdirection: [
        `${vocabulary.objects[0]}并非关键，真正的线索在${vocabulary.locations[0]}`,
        `看似${vocabulary.entities[0]}所为，实则是${vocabulary.entities[3]}`,
        `${vocabulary.events[0]}只是幌子`
      ],
      concealment: [
        `${vocabulary.objects[0]}被隐藏在${vocabulary.locations[0]}中`,
        `${vocabulary.entities[0]}一直隐藏在主角身边`,
        `真相被封印在${vocabulary.objects[0]}里`
      ]
    };
    
    const options = templates[type];
    return options[Math.floor(Math.random() * options.length)];
  }

  /**
   * 生成触发条件
   */
  generateTrigger(type, complexity, vocabulary) {
    const conditions = [];
    
    for (let i = 0; i < complexity; i++) {
      const conditionType = ['choice', 'item', 'stat', 'location'][Math.floor(Math.random() * 4)];
      
      conditions.push({
        type: conditionType,
        description: this.generateTriggerDescription(conditionType, vocabulary),
        requirements: this.generateTriggerRequirements(conditionType, vocabulary)
      });
    }

    return new TriggerCondition({
      type: 'combination',
      description: conditions.map(c => c.description).join(' 并且 '),
      requirements: { conditions }
    });
  }

  /**
   * 生成触发描述
   */
  generateTriggerDescription(type, vocabulary) {
    const templates = {
      choice: `选择${vocabulary.events[Math.floor(Math.random() * vocabulary.events.length)]}`,
      item: `获得${vocabulary.objects[Math.floor(Math.random() * vocabulary.objects.length)]}`,
      stat: `${['理智', '力量', '智慧', '魅力'][Math.floor(Math.random() * 4)]}达到一定程度`,
      location: `到达${vocabulary.locations[Math.floor(Math.random() * vocabulary.locations.length)]}`
    };
    
    return templates[type];
  }

  /**
   * 生成触发需求
   */
  generateTriggerRequirements(type, vocabulary) {
    switch (type) {
      case 'choice':
        return { choices: [vocabulary.events[Math.floor(Math.random() * vocabulary.events.length)]] };
      case 'item':
        return { items: [vocabulary.objects[Math.floor(Math.random() * vocabulary.objects.length)]] };
      case 'stat':
        return { stats: { [(['sanity', 'strength', 'wisdom', 'charm'][Math.floor(Math.random() * 4)])]: Math.floor(Math.random() * 50) + 50 } };
      case 'location':
        return { locations: [vocabulary.locations[Math.floor(Math.random() * vocabulary.locations.length)]] };
      default:
        return {};
    }
  }

  /**
   * 生成揭示方式
   */
  generateReveal(type, steps, vocabulary) {
    const revealTypes = ['direct', 'gradual', 'puzzle', 'narrative'];
    const selectedType = revealTypes[Math.floor(Math.random() * revealTypes.length)];

    const revealSteps = [];
    for (let i = 0; i < steps; i++) {
      revealSteps.push(this.generateRevealStep(type, i, vocabulary));
    }

    return new RevealMethod({
      type: selectedType,
      description: `真相终于大白：${vocabulary.entities[Math.floor(Math.random() * vocabulary.entities.length)]}才是真正的${vocabulary.events[Math.floor(Math.random() * vocabulary.events.length)]}者`,
      steps: revealSteps,
      consequences: [
        { type: 'stat_change', target: 'sanity', value: -10 },
        { type: 'flag_set', target: 'truth_revealed', value: true }
      ]
    });
  }

  /**
   * 生成揭示步骤
   */
  generateRevealStep(type, index, vocabulary) {
    const templates = [
      `发现${vocabulary.objects[Math.floor(Math.random() * vocabulary.objects.length)]}的异常`,
      `${vocabulary.entities[Math.floor(Math.random() * vocabulary.entities.length)]}露出破绽`,
      `回忆起被遗忘的${vocabulary.events[Math.floor(Math.random() * vocabulary.events.length)]}`,
      `在${vocabulary.locations[Math.floor(Math.random() * vocabulary.locations.length)]}找到关键证据`,
      `理解了${vocabulary.objects[Math.floor(Math.random() * vocabulary.objects.length)]}的真正含义`
    ];
    
    return templates[index % templates.length];
  }

  /**
   * 生成提示
   */
  generateHint(type, index, vocabulary, description) {
    const templates = {
      reversal: [
        `注意${vocabulary.objects[0]}和${vocabulary.objects[1]}的关联`,
        `时间线有矛盾`,
        `角色的动机值得怀疑`
      ],
      misdirection: [
        `不要被表面现象迷惑`,
        `${vocabulary.objects[0]}可能不是你想的那样`,
        `关注细节而非重点`
      ],
      concealment: [
        `某些东西被刻意隐藏了`,
        `检查${vocabulary.locations[Math.floor(Math.random() * vocabulary.locations.length)]}`,
        `回忆之前忽略的对话`
      ]
    };
    
    const hints = templates[type];
    return hints[index % hints.length];
  }

  /**
   * 生成红鲱鱼
   */
  generateRedHerring(vocabulary) {
    const templates = [
      {
        type: 'false_clue',
        description: `看似重要的${vocabulary.objects[Math.floor(Math.random() * vocabulary.objects.length)]}`,
        purpose: '误导玩家关注错误方向'
      },
      {
        type: 'suspicious_character',
        description: `行为怪异的${vocabulary.entities[Math.floor(Math.random() * vocabulary.entities.length)]}`,
        purpose: '让玩家怀疑错误的人'
      },
      {
        type: 'false_event',
        description: `发生的${vocabulary.events[Math.floor(Math.random() * vocabulary.events.length)]}`,
        purpose: '转移注意力'
      }
    ];
    
    return templates[Math.floor(Math.random() * templates.length)];
  }

  /**
   * 从《针本》剧本生成核心诡计
   */
  generateFromZhenben(scriptData) {
    const trick = new CoreTrick({
      id: `zhenben_trick_${scriptData.编号}`,
      name: scriptData.目录,
      type: this.inferTrickType(scriptData),
      description: scriptData.核心诡计 || scriptData.主题,
      difficulty: 'medium'
    });

    // 如果有核心转换，生成触发条件
    if (scriptData.核心转换) {
      const transforms = scriptData.核心转换.split(/\s+/);
      trick.trigger = new TriggerCondition({
        type: 'combination',
        description: `完成核心转换流程`,
        requirements: {
          conditions: transforms.map((t, i) => ({
            type: 'choice',
            description: t,
            requirements: { choices: [t] }
          }))
        }
      });
    }

    // 生成揭示方式
    trick.reveal = new RevealMethod({
      type: 'narrative',
      description: scriptData.核心诡计 || '真相被揭示',
      steps: scriptData.核心转换 ? scriptData.核心转换.split(/\s+/) : [],
      consequences: [
        { type: 'story_complete', target: scriptData.目录 }
      ]
    });

    return trick;
  }

  /**
   * 推断诡计类型
   */
  inferTrickType(scriptData) {
    const text = `${scriptData.主题} ${scriptData.核心转换 || ''} ${scriptData.核心诡计 || ''}`;
    
    if (text.includes('隐藏') || text.includes('秘密') || text.includes('未发现')) {
      return 'concealment';
    }
    if (text.includes('误导') || text.includes('幌子') || text.includes('伪装')) {
      return 'misdirection';
    }
    
    return 'reversal';
  }

  /**
   * 批量生成诡计
   */
  generateBatch(count = 5, options = {}) {
    const tricks = [];
    for (let i = 0; i < count; i++) {
      tricks.push(this.generate(options));
    }
    return tricks;
  }

  /**
   * 验证诡计的合理性
   */
  validate(trick) {
    const issues = [];

    // 检查是否有足够的提示
    if (trick.difficulty === 'hard' && trick.hints.length < 1) {
      issues.push('高难度诡计应该至少有一个提示');
    }

    // 检查红鲱鱼数量
    if (trick.redHerrings.length > 5) {
      issues.push('红鲱鱼过多可能导致玩家困惑');
    }

    // 检查触发条件
    if (!trick.trigger || !trick.trigger.requirements) {
      issues.push('缺少有效的触发条件');
    }

    // 检查揭示方式
    if (!trick.reveal || !trick.reveal.description) {
      issues.push('缺少揭示方式');
    }

    return {
      valid: issues.length === 0,
      issues: issues
    };
  }

  /**
   * 调整诡计难度
   */
  adjustDifficulty(trick, newDifficulty) {
    const params = this.difficultyParams[newDifficulty];
    const vocabulary = this.themeVocabulary[this.config.theme];

    // 调整提示数量
    while (trick.hints.length > params.hints) {
      trick.hints.pop();
    }
    while (trick.hints.length < params.hints) {
      trick.addHint(this.generateHint(trick.type, trick.hints.length, vocabulary, trick.description));
    }

    // 调整红鲱鱼数量
    while (trick.redHerrings.length > params.redHerrings) {
      trick.redHerrings.pop();
    }
    while (trick.redHerrings.length < params.redHerrings) {
      trick.addRedHerring(this.generateRedHerring(vocabulary));
    }

    trick.difficulty = newDifficulty;
    return trick;
  }

  /**
   * 序列化诡计
   */
  serialize(trick) {
    return {
      id: trick.id,
      name: trick.name,
      type: trick.type,
      description: trick.description,
      trigger: trick.trigger,
      reveal: trick.reveal,
      hints: trick.hints,
      redHerrings: trick.redHerrings,
      difficulty: trick.difficulty,
      metadata: trick.metadata
    };
  }

  /**
   * 反序列化诡计
   */
  deserialize(data) {
    const trick = new CoreTrick(data);
    if (data.trigger) {
      trick.trigger = new TriggerCondition(data.trigger);
    }
    if (data.reveal) {
      trick.reveal = new RevealMethod(data.reveal);
    }
    return trick;
  }
}

// ==================== 预设核心诡计模板 ====================

const CoreTrickTemplates = {
  /**
   * 《针本》预设诡计
   */
  zhenben: {
    dissociation: {
      name: '解离诡计',
      type: 'concealment',
      description: '大脑是他们身体仅存的剩余部分',
      trigger: {
        type: 'combination',
        requirements: {
          conditions: [
            { type: 'stat', requirements: { stats: { sanity: 30 } } },
            { type: 'choice', requirements: { choices: ['接受实验'] } }
          ]
        }
      },
      reveal: {
        type: 'gradual',
        steps: ['发现镜子中的异常', '意识到记忆的断裂', '发现脑罐的真相'],
        description: '共享的幻景，大脑是他们身体仅存的剩余部分'
      }
    },
    lightsOut: {
      name: '熄灯后诡计',
      type: 'reversal',
      description: '《地狱火之书》浸没在水中',
      trigger: {
        type: 'item',
        requirements: { items: ['地狱火之书', '水'] }
      },
      reveal: {
        type: 'puzzle',
        description: '书被水浸没后失去力量',
        steps: ['第一次召唤失败的原因', '幽灵的真正身份', '如何阻止二次附体']
      }
    },
    poetryNight: {
      name: '诗歌之夜诡计',
      type: 'misdirection',
      description: '仪式的正序和反序',
      trigger: {
        type: 'choice',
        requirements: { choices: ['参加诗歌大会'] }
      },
      reveal: {
        type: 'narrative',
        description: '仪式的正序和反序，获得信息，执行过程的阻碍',
        steps: ['发现诗歌的特殊含义', '理解仪式的方向性', '使用反序返回']
      }
    }
  },

  /**
   * 经典诡计模板
   */
  classic: {
    unreliableNarrator: {
      name: '不可靠叙述者',
      type: 'reversal',
      description: '叙述者本身就是诡计的一部分',
      difficulty: 'hard'
    },
    hiddenInPlainSight: {
      name: '显而易见的隐藏',
      type: 'concealment',
      description: '关键线索一直就在眼前',
      difficulty: 'medium'
    },
    doubleIdentity: {
      name: '双重身份',
      type: 'misdirection',
      description: '两个角色其实是同一个人',
      difficulty: 'hard'
    }
  }
};

// ==================== 导出 ====================

module.exports = {
  CoreTrick,
  TriggerCondition,
  RevealMethod,
  CoreTrickGenerator,
  CoreTrickTemplates
};
