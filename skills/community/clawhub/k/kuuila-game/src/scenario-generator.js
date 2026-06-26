/**
 * 剧本生成器 (Scenario Generator) - v2.9.0
 * 随机组合生成新剧本
 */

const { ScenarioSystem, CATEGORY, DIFFICULTY, SCENARIOS } = require('./scenario-system');

/**
 * 随机工具类
 */
class RandomUtils {
  /**
   * 从数组中随机选取一个元素
   */
  static pick(array) {
    if (!array || array.length === 0) return null;
    return array[Math.floor(Math.random() * array.length)];
  }

  /**
   * 从数组中随机选取多个不重复元素
   */
  static pickMultiple(array, count) {
    if (!array || array.length === 0) return [];
    const shuffled = [...array].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, Math.min(count, array.length));
  }

  /**
   * 生成随机ID
   */
  static generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
  }

  /**
   * 权重随机选择
   */
  static weightedPick(items, weights) {
    const totalWeight = weights.reduce((a, b) => a + b, 0);
    let random = Math.random() * totalWeight;
    
    for (let i = 0; i < items.length; i++) {
      random -= weights[i];
      if (random <= 0) return items[i];
    }
    
    return items[items.length - 1];
  }
}

/**
 * 主题元素库
 */
const THEME_ELEMENTS = {
  // 神话生物元素
  mythical: {
    entities: [
      "克苏鲁", "奈亚拉托提普", "哈斯塔", "犹格·索托斯", 
      "伊德海拉", "夸切乌陶斯", "修德·梅尔", "达奥洛斯",
      "莎布·尼古拉丝", "阿撒托斯", "格赫罗斯", "图鲁格族"
    ],
    traits: [
      "不可名状", "超越时间", "古老存在", "梦境相连",
      "精神污染", "形态变幻", "永恒存在", "疯狂之源"
    ],
    locations: [
      "拉莱耶", "幻梦境", "深空", "异维度", 
      "古老遗迹", "被遗忘的神殿", "时空裂隙", "深渊"
    ]
  },
  
  // 心理恐怖元素
  psychological: {
    fears: [
      "孤立无援", "无法逃脱", "记忆缺失", "身份迷失",
      "时间错乱", "理智崩溃", "信任崩塌", "现实扭曲"
    ],
    symptoms: [
      "幻听", "幻视", "记忆混乱", "人格分裂",
      "强迫行为", "恐惧症", "焦虑", "幻觉"
    ],
    triggers: [
      "创伤回忆", "遗物", "预言", "诅咒",
      "禁忌仪式", "神秘录音", "异常梦境", "不祥征兆"
    ]
  },
  
  // 机构阴谋元素
  conspiracy: {
    organizations: [
      "秘密研究所", "邪教组织", "政府机构", "企业集团",
      "神秘学会", "暗杀组织", "异端教会", "跨国集团"
    ],
    methods: [
      "人体实验", "精神控制", "生物武器", "时空武器",
      "信息操纵", "经济控制", "暗杀", "洗脑"
    ],
    motives: [
      "永恒生命", "统治世界", "召唤邪神", "种族清洗",
      "科学突破", "军事优势", "财富积累", "权力扩张"
    ]
  },
  
  // 怪物悬疑元素
  monster: {
    creatures: [
      "变异生物", "未知怪物", "被诅咒者", "半人怪物",
      "海洋怪物", "森林怪物", "寄生生物", "变形者"
    ],
    origins: [
      "辐射变异", "古老诅咒", "仪式召唤", "遗传变异",
      "外星寄生", "魔法实验", "环境适应", "人工培育"
    ],
    abilities: [
      "变形", "精神控制", "快速愈合", "隐身",
      "超凡力量", "毒素", "催眠", "拟态"
    ]
  }
};

/**
 * 角色特征库
 */
const CHARACTER_TRAITS = {
  // 职业类
  professions: [
    "医生", "警察", "教授", "记者", "侦探", "军人", "科学家",
    "艺术家", "作家", "律师", "商人", "学生", "工人", "渔民",
    "导游", "图书馆员", "考古学家", "心理学家", "神秘学家"
  ],
  
  // 性格类
  personalities: [
    "好奇心强", "理智脆弱", "意志坚定", "怀疑论者",
    "神秘学爱好者", "保守谨慎", "冲动冒险", "冷静理性"
  ],
  
  // 弱点类
  weaknesses: [
    "酗酒", "抑郁症", "家族遗传诅咒", "过去的秘密",
    "对家人牵挂", "对真相执着", "对财富贪婪", "对名誉追求"
  ]
};

/**
 * 核心转换库
 */
const CORE_TRANSFORMATIONS = {
  // 转换类型
  types: [
    { name: "肉体转换", desc: "身体的异变与扭曲" },
    { name: "精神转换", desc: "意识的崩溃与重塑" },
    { name: "空间转换", desc: "环境的移位与置换" },
    { name: "时间转换", desc: "时间的错乱与回环" },
    { name: "身份转换", desc: "自我的迷失与替代" },
    { name: "信仰转换", desc: "世界观的崩塌与重建" }
  ],
  
  // 转换描述模板
  templates: [
    "在{触发条件}下，{受害者}的{特征}被{效果}",
    "随着{过程}的进行，{现象}逐渐显现",
    "当{条件}满足时，{变化}开始发生",
    "通过{手段}，{目标}完成了{转变}"
  ]
};

/**
 * 核心诡计库
 */
const CORE_TRICKS = {
  // 诡计类型
  types: [
    { name: "身份反转", desc: "谁才是真正的主角/敌人" },
    { name: "时间诡计", desc: "时间线上的欺骗" },
    { name: "空间诡计", desc: "地点与环境的欺骗" },
    { name: "认知诡计", desc: "感官与记忆的欺骗" },
    { name: "叙事诡计", desc: "故事结构的欺骗" },
    { name: "预言诡计", desc: "预言与命运的欺骗" }
  ],
  
  // 诡计模板
  templates: [
    "真相被{手段}所掩盖，{假象}欺骗了所有人",
    "看似{表象}的事件，实际上是{真相}",
    "{误导}让调查员走向错误的方向，{真相}隐藏在{地点}",
    "当{条件}被发现时，{诡计}已经完成"
  ]
};

/**
 * 剧本生成器类
 */
class ScenarioGenerator {
  constructor() {
    this.scenarioSystem = new ScenarioSystem();
    this.themeElements = THEME_ELEMENTS;
    this.characterTraits = CHARACTER_TRAITS;
    this.transformations = CORE_TRANSFORMATIONS;
    this.tricks = CORE_TRICKS;
    
    // 难度权重 (影响生成复杂度)
    this.difficultyWeights = {
      [DIFFICULTY.EASY]: 1,
      [DIFFICULTY.NORMAL]: 2,
      [DIFFICULTY.HARD]: 3,
      [DIFFICULTY.NIGHTMARE]: 4
    };
  }

  /**
   * 生成随机剧本
   */
  generate(options = {}) {
    const {
      category = null,       // 指定分类
      difficulty = null,     // 指定难度
      theme = null,          // 指定主题
      useExistingBase = true // 是否基于现有剧本
    } = options;

    // 选择分类
    const selectedCategory = category || this._selectRandomCategory();
    
    // 选择难度
    const selectedDifficulty = difficulty || this._selectRandomDifficulty();
    
    // 生成剧本
    const scenario = {
      id: RandomUtils.generateId(),
      title: this._generateTitle(selectedCategory),
      category: selectedCategory,
      theme: theme || this._generateTheme(selectedCategory),
      characterTraits: this._generateCharacterTraits(selectedDifficulty),
      coreTransformation: this._generateTransformation(selectedCategory, selectedDifficulty),
      coreTrick: this._generateTrick(selectedCategory, selectedDifficulty),
      difficulty: selectedDifficulty,
      tags: this._generateTags(selectedCategory),
      
      // 生成额外数据
      generated: true,
      createdAt: new Date().toISOString()
    };

    // 可选：融合现有剧本元素
    if (useExistingBase) {
      const baseScenario = this.scenarioSystem.getRandom(selectedCategory);
      scenario.inspiredBy = baseScenario.id;
      scenario.baseTitle = baseScenario.title;
    }

    return scenario;
  }

  /**
   * 批量生成剧本
   */
  generateBatch(count, options = {}) {
    const scenarios = [];
    for (let i = 0; i < count; i++) {
      scenarios.push(this.generate(options));
    }
    return scenarios;
  }

  /**
   * 智能生成 - 基于相关性过滤
   */
  generateSmart(requirements) {
    const {
      mustHaveTags = [],    // 必须包含的标签
      excludeTags = [],     // 排除的标签
      minDifficulty = DIFFICULTY.EASY,
      maxDifficulty = DIFFICULTY.NIGHTMARE,
      category = null
    } = requirements;

    let attempts = 0;
    const maxAttempts = 10;

    while (attempts < maxAttempts) {
      const scenario = this.generate({ category });
      
      // 检查标签要求
      const hasRequiredTags = mustHaveTags.every(tag => 
        scenario.tags.includes(tag)
      );
      
      const hasExcludedTags = excludeTags.some(tag => 
        scenario.tags.includes(tag)
      );
      
      // 检查难度范围
      const inDifficultyRange = this._compareDifficulty(
        scenario.difficulty, 
        minDifficulty
      ) >= 0 && this._compareDifficulty(
        scenario.difficulty, 
        maxDifficulty
      ) <= 0;

      if (hasRequiredTags && !hasExcludedTags && inDifficultyRange) {
        return scenario;
      }
      
      attempts++;
    }

    // 超过最大尝试次数，返回最后一个
    return this.generate({ category });
  }

  /**
   * 基于现有剧本变异生成
   */
  generateVariant(baseId, mutationLevel = 'light') {
    const base = this.scenarioSystem.getById(baseId);
    if (!base) {
      throw new Error(`找不到ID为 ${baseId} 的剧本`);
    }

    const variant = { ...base };
    variant.id = RandomUtils.generateId();
    variant.variantOf = baseId;
    variant.variantLevel = mutationLevel;

    switch (mutationLevel) {
      case 'light':
        // 轻微变异：只改变角色特征
        variant.characterTraits = this._generateCharacterTraits(
          this._difficultyToNumber(base.difficulty)
        );
        break;
        
      case 'medium':
        // 中等变异：改变核心转换和角色特征
        variant.characterTraits = this._generateCharacterTraits(
          this._difficultyToNumber(base.difficulty)
        );
        variant.coreTransformation = this._generateTransformation(
          base.category, base.difficulty
        );
        break;
        
      case 'heavy':
        // 重度变异：改变所有核心元素
        variant.theme = this._generateTheme(base.category);
        variant.characterTraits = this._generateCharacterTraits(
          this._difficultyToNumber(base.difficulty)
        );
        variant.coreTransformation = this._generateTransformation(
          base.category, base.difficulty
        );
        variant.coreTrick = this._generateTrick(
          base.category, base.difficulty
        );
        break;
    }

    return variant;
  }

  /**
   * 生成完整剧本 (包含详细信息)
   */
  generateFull(options = {}) {
    const scenario = this.generate(options);
    
    return {
      ...scenario,
      // 添加详细生成内容
      introduction: this._generateIntroduction(scenario),
      chapters: this._generateChapters(scenario),
      NPCs: this._generateDetailedNPCs(scenario),
      clues: this._generateClues(scenario),
      dangers: this._generateDangers(scenario),
      endings: this._generateEndings(scenario)
    };
  }

  // ==================== 私有方法 ====================

  _selectRandomCategory() {
    return RandomUtils.pick(Object.values(CATEGORY));
  }

  _selectRandomDifficulty() {
    const diffs = Object.values(DIFFICULTY);
    const weights = [3, 5, 3, 1]; // EASY, NORMAL, HARD, NIGHTMARE
    return RandomUtils.weightedPick(diffs, weights);
  }

  _generateTitle(category) {
    const prefixes = {
      [CATEGORY.MYTHICAL]: ["古老", "深渊", "神话", "永恒"],
      [CATEGORY.PSYCHOLOGICAL]: ["暗影", "心魔", "迷失", "破碎"],
      [CATEGORY.CONSPIRACY]: ["秘密", "真相", "阴谋", "阴谋"],
      [CATEGORY.MONSTER]: ["怪物", "变异", "诅咒", "恐怖"]
    };

    const nouns = {
      [CATEGORY.MYTHICAL]: ["召唤", "降临", "契约", "低语"],
      [CATEGORY.PSYCHOLOGICAL]: ["记忆", "梦境", "疯狂", "恐惧"],
      [CATEGORY.CONSPIRACY]: ["计划", "档案", "协议", "实验"],
      [CATEGORY.MONSTER]: ["猎物", "巢穴", "血肉", "转化"]
    };

    const prefix = RandomUtils.pick(prefixes[category] || []);
    const noun = RandomUtils.pick(nouns[category] || []);
    
    const titleFormats = [
      `${prefix}${noun}`,
      `${prefix}的${noun}`,
      `${noun}之${prefix}`,
      `${prefix}${noun}事件`
    ];

    return RandomUtils.pick(titleFormats);
  }

  _generateTheme(category) {
    const elements = this.themeElements[this._getCategoryKey(category)];
    if (!elements) return "未知主题";

    const entity = RandomUtils.pick(elements.entities || elements.fears || elements.organizations || elements.creatures);
    const trait = RandomUtils.pick(elements.traits || elements.symptoms || elements.methods || elements.origins);

    return `${entity}的${trait}`;
  }

  _generateCharacterTraits(difficulty) {
    const difficultyNum = this._difficultyToNumber(difficulty);
    const traitCount = 2 + difficultyNum; // 难度越高，特征越多

    const traits = [
      ...RandomUtils.pickMultiple(CHARACTER_TRAITS.professions, Math.ceil(traitCount / 2)),
      ...RandomUtils.pickMultiple(CHARACTER_TRAITS.personalities, Math.floor(traitCount / 2))
    ];

    return traits;
  }

  _generateTransformation(category, difficulty) {
    const categoryKey = this._getCategoryKey(category);
    const elements = this.themeElements[categoryKey];
    const type = RandomUtils.pick(CORE_TRANSFORMATIONS.types);
    const template = RandomUtils.pick(CORE_TRANSFORMATIONS.templates);

    // 根据分类填充模板
    let result = template;
    result = result.replace('{触发条件}', RandomUtils.pick(elements.triggers || elements.origins || elements.entities || ['未知']));
    result = result.replace('{受害者}', '调查员');
    result = result.replace('{特征}', type.name);
    result = result.replace('{效果}', type.desc);
    result = result.replace('{过程}', '仪式');
    result = result.replace('{现象}', '异常');
    result = result.replace('{条件}', '条件');
    result = result.replace('{变化}', type.name);
    result = result.replace('{手段}', RandomUtils.pick(elements.triggers || elements.methods || ['神秘力量']));
    result = result.replace('{目标}', '对象');
    result = result.replace('{转变}', '转换');

    return result;
  }

  _generateTrick(category, difficulty) {
    const type = RandomUtils.pick(CORE_TRICKS.types);
    const template = RandomUtils.pick(CORE_TRICKS.templates);

    let result = template;
    result = result.replace('{手段}', '精心设计的');
    result = result.replace('{假象}', '表面现象');
    result = result.replace('{表象}', '正常');
    result = result.replace('{真相}', type.desc);
    result = result.replace('{误导}', '线索');
    result = result.replace('{地点}', '隐蔽处');
    result = result.replace('{条件}', '真相');
    result = result.replace('{诡计}', type.name);

    return result;
  }

  _generateTags(category) {
    const categoryKey = this._getCategoryKey(category);
    const elements = this.themeElements[categoryKey];
    
    // 从元素中提取标签
    const allElements = [
      ...(elements.entities || []),
      ...(elements.traits || []),
      ...(elements.fears || []),
      ...(elements.organizations || []),
      ...(elements.creatures || [])
    ];

    return RandomUtils.pickMultiple(allElements, 4);
  }

  _generateIntroduction(scenario) {
    return `${scenario.title}是一个关于${scenario.theme}的故事。调查员将面临${scenario.difficulty}级别的挑战，核心转换涉及${scenario.coreTransformation}。`;
  }

  _generateChapters(scenario) {
    return [
      {
        name: "序幕",
        description: `发现${scenario.theme}的初步线索`,
        objective: "收集信息，了解背景"
      },
      {
        name: "发展",
        description: scenario.coreTransformation,
        objective: "深入调查，揭示真相"
      },
      {
        name: "高潮",
        description: scenario.coreTrick,
        objective: "面对核心挑战"
      },
      {
        name: "结局",
        description: "命运的抉择",
        objective: "完成最终目标"
      }
    ];
  }

  _generateDetailedNPCs(scenario) {
    return scenario.characterTraits.map(trait => ({
      name: `${trait}角色`,
      trait,
      role: RandomUtils.pick(['协助者', '阻碍者', '中立', '关键人物']),
      motivation: RandomUtils.pick(['求生', '真相', '复仇', '贪婪', '保护']),
      secret: `隐藏着与${scenario.theme}相关的秘密`
    }));
  }

  _generateClues(scenario) {
    return [
      { type: "物理证据", description: `与${scenario.theme}相关的实物` },
      { type: "证词", description: "目击者的陈述" },
      { type: "文献", description: "古老的记录或现代档案" },
      { type: "梦境", description: "预知或启示性的梦境" }
    ];
  }

  _generateDangers(scenario) {
    const dangerCount = this._difficultyToNumber(scenario.difficulty);
    const dangers = [];
    
    for (let i = 0; i < dangerCount; i++) {
      dangers.push({
        type: RandomUtils.pick(['物理', '精神', '社会', '超自然']),
        description: `${scenario.theme}带来的威胁`,
        severity: scenario.difficulty
      });
    }

    return dangers;
  }

  _generateEndings(scenario) {
    return [
      {
        type: "好结局",
        condition: "成功揭示并阻止",
        description: `成功阻止${scenario.coreTrick}`
      },
      {
        type: "普通结局",
        condition: "部分成功",
        description: "付出代价但达成目标"
      },
      {
        type: "坏结局",
        condition: "调查失败",
        description: scenario.coreTransformation
      },
      {
        type: "真结局",
        condition: "完美调查",
        description: "揭示所有真相并获得力量"
      }
    ];
  }

  _getCategoryKey(category) {
    const mapping = {
      [CATEGORY.MYTHICAL]: 'mythical',
      [CATEGORY.PSYCHOLOGICAL]: 'psychological',
      [CATEGORY.CONSPIRACY]: 'conspiracy',
      [CATEGORY.MONSTER]: 'monster'
    };
    return mapping[category] || 'mythical';
  }

  _difficultyToNumber(difficulty) {
    const mapping = {
      [DIFFICULTY.EASY]: 1,
      [DIFFICULTY.NORMAL]: 2,
      [DIFFICULTY.HARD]: 3,
      [DIFFICULTY.NIGHTMARE]: 4
    };
    return mapping[difficulty] || 2;
  }

  _compareDifficulty(d1, d2) {
    return this._difficultyToNumber(d1) - this._difficultyToNumber(d2);
  }
}

// 导出
module.exports = {
  ScenarioGenerator,
  RandomUtils,
  THEME_ELEMENTS,
  CHARACTER_TRAITS,
  CORE_TRANSFORMATIONS,
  CORE_TRICKS
};
