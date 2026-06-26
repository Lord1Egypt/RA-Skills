/**
 * Kuuila Game - 角色系统 v2.6.0
 * 基于灵安城奇遇记角色设计
 * 
 * 功能：
 * - 角色属性系统 (生命/攻击/防守/速度)
 * - 技能系统 (社交/说服/理财/骗术/潜行/盗窃/侦察/话术/官威等)
 * - 背景故事生成
 * - 随身物品管理
 * - 成长阶段触发
 * - 任务目标系统
 */

// ==================== 常量定义 ====================

/**
 * 技能定义
 */
const SKILLS = {
  // 社交类技能
  social: { name: '社交', desc: '与他人建立关系、影响他人情感的能力', category: 'social' },
  persuasion: { name: '说服', desc: '说服他人接受观点或行动的能力', category: 'social' },
  rhetoric: { name: '话术', desc: '言语技巧，辩论和谈判能力', category: 'social' },
  authority: { name: '官威', desc: '利用官方身份施压的能力', category: 'social' },
  
  // 经济类技能
  finance: { name: '理财', desc: '财务管理、投资和经商能力', category: 'economic' },
  
  // 潜行类技能
  stealth: { name: '潜行', desc: '隐蔽行动、悄无声息移动的能力', category: 'stealth' },
  eavesdrop: { name: '窃听', desc: '偷听他人对话的能力', category: 'stealth' },
  theft: { name: '盗窃', desc: '偷窃物品的能力', category: 'stealth' },
  deception: { name: '骗术', desc: '欺骗他人的能力', category: 'stealth' },
  
  // 侦查类技能
  investigation: { name: '侦察', desc: '调查、搜集线索的能力', category: 'investigation' },
  
  // 战斗类技能
  combat: { name: '格斗', desc: '近身战斗能力', category: 'combat' },
  weapon: { name: '兵器', desc: '使用武器的能力', category: 'combat' },
  
  // 其他技能
  medical: { name: '医术', desc: '治疗疾病和伤势的能力', category: 'other' },
  crafting: { name: '工艺', desc: '制作物品的能力', category: 'other' },
  knowledge: { name: '学识', desc: '知识和学问', category: 'other' }
};

/**
 * 成长阶段定义
 */
const GROWTH_STAGES = [
  { name: '初出茅庐', level: 1, expRequired: 0, statBonus: 0 },
  { name: '小有名气', level: 2, expRequired: 100, statBonus: 1 },
  { name: '崭露头角', level: 3, expRequired: 300, statBonus: 2 },
  { name: '名声渐起', level: 4, expRequired: 600, statBonus: 3 },
  { name: '名震一方', level: 5, expRequired: 1000, statBonus: 4 },
  { name: '威名远扬', level: 6, expRequired: 1500, statBonus: 5 },
  { name: '名满天下', level: 7, expRequired: 2500, statBonus: 6 },
  { name: '传说人物', level: 8, expRequired: 4000, statBonus: 8 },
  { name: '神话传说', level: 9, expRequired: 6000, statBonus: 10 }
];

/**
 * 物品类型定义
 */
const ITEM_TYPES = {
  weapon: { name: '武器', slot: 'weapon', statBonus: { attack: 1 } },
  armor: { name: '护甲', slot: 'armor', statBonus: { defense: 1 } },
  accessory: { name: '饰品', slot: 'accessory', statBonus: {} },
  consumable: { name: '消耗品', slot: 'inventory', consumable: true },
  key: { name: '关键物品', slot: 'key', important: true },
  document: { name: '文书', slot: 'inventory', important: false },
  currency: { name: '货币', slot: 'currency', stackable: true }
};

/**
 * 角色职业模板
 */
const CHARACTER_TEMPLATES = {
  guard: {
    name: '御前侍卫',
    baseStats: { hp: 12, attack: 6, defense: 5, speed: 6 },
    baseSkills: { investigation: 2, rhetoric: 2, authority: 2 },
    startingItems: ['双刀', '腰牌'],
    traits: ['武艺超群', '机敏'],
    background: '学得文武艺，报于帝皇家。层层选拔为御前侍卫，被前任统领赏识传授双刀技法。'
  },
  
  merchant: {
    name: '农场主',
    baseStats: { hp: 9, attack: 3, defense: 3, speed: 3 },
    baseSkills: { social: 2, persuasion: 2, finance: 2 },
    startingItems: ['账本', '算盘', '债卷'],
    traits: ['商业头脑', '胆小易怒'],
    background: '家族产业继承者，曾创作奶茶商业奇迹，独身未嫁是个谜。'
  },
  
  rogue: {
    name: '侠盗',
    baseStats: { hp: 11, attack: 4, defense: 4, speed: 5 },
    baseSkills: { deception: 2, stealth: 2, theft: 2 },
    startingItems: ['绳索', '夜行衣'],
    traits: ['武痴', '怕麻烦', '憎恨权贵'],
    background: '自幼孤儿，被乞丐抚养长大。痴迷武学，只偷富贵者，在乞丐中有人缘。'
  },
  
  assassin: {
    name: '刺客',
    baseStats: { hp: 10, attack: 4, defense: 3, speed: 3 },
    baseSkills: { stealth: 3 },
    startingItems: ['竹篙刀', '黑球'],
    traits: ['冷酷', '隐蔽'],
    background: '身份神秘的刺客，擅长伪装和暗杀。'
  }
};

// ==================== 角色类 ====================

/**
 * 角色类
 */
class Character {
  constructor(options = {}) {
    // 基本信息
    this.id = options.id || this.generateId();
    this.name = options.name || '无名氏';
    this.age = options.age || null;
    this.occupation = options.occupation || '平民';
    
    // 基础属性
    this.stats = {
      hp: options.hp || 10,
      maxHp: options.maxHp || options.hp || 10,
      attack: options.attack || 3,
      defense: options.defense || 3,
      speed: options.speed || 3
    };
    
    // 技能
    this.skills = options.skills || {};
    
    // 背景
    this.background = options.background || '';
    this.traits = options.traits || [];
    
    // 物品
    this.inventory = {
      weapon: null,
      armor: null,
      accessory: null,
      items: options.items || [],
      keyItems: [],
      currency: options.currency || 0
    };
    
    // 成长
    this.level = 1;
    this.exp = 0;
    this.growthStage = GROWTH_STAGES[0];
    
    // 任务
    this.objectives = options.objectives || [];
    this.completedObjectives = [];
    
    // 状态
    this.status = {
      mood: 'normal', // normal, happy, sad, angry, scared, etc.
      conditions: [], // 中毒, 受伤, etc.
      location: null,
      relationships: new Map() // 与其他角色的关系
    };
    
    // 灵安城特定属性
    this.lingan = {
      affectedByPlague: false,
      knownSecrets: [],
      faction: null // 所属派系
    };
  }
  
  /**
   * 生成唯一ID
   */
  generateId() {
    return `char_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  // ==================== 属性相关 ====================
  
  /**
   * 获取当前属性（包含成长加成和装备加成）
   */
  getStats() {
    const baseStats = { ...this.stats };
    const growthBonus = this.growthStage.statBonus;
    
    // 应用成长加成
    baseStats.attack += growthBonus;
    baseStats.defense += growthBonus;
    
    // 应用装备加成
    if (this.inventory.weapon) {
      const weaponBonus = ITEM_TYPES.weapon.statBonus;
      baseStats.attack += weaponBonus.attack;
    }
    if (this.inventory.armor) {
      const armorBonus = ITEM_TYPES.armor.statBonus;
      baseStats.defense += armorBonus.defense;
    }
    
    return baseStats;
  }
  
  /**
   * 修改属性
   */
  modifyStat(stat, amount) {
    if (this.stats[stat] !== undefined) {
      this.stats[stat] += amount;
      if (stat === 'hp' && this.stats.hp > this.stats.maxHp) {
        this.stats.hp = this.stats.maxHp;
      }
      if (this.stats.hp < 0) this.stats.hp = 0;
      return true;
    }
    return false;
  }
  
  /**
   * 受伤
   */
  takeDamage(amount) {
    const defense = this.getStats().defense;
    const actualDamage = Math.max(1, amount - defense);
    this.stats.hp -= actualDamage;
    
    if (this.stats.hp <= 0) {
      this.stats.hp = 0;
      return { defeated: true, damage: actualDamage };
    }
    return { defeated: false, damage: actualDamage };
  }
  
  /**
   * 治疗
   */
  heal(amount) {
    const oldHp = this.stats.hp;
    this.stats.hp = Math.min(this.stats.maxHp, this.stats.hp + amount);
    return this.stats.hp - oldHp;
  }
  
  // ==================== 技能相关 ====================
  
  /**
   * 获取技能等级
   */
  getSkillLevel(skillName) {
    return this.skills[skillName] || 0;
  }
  
  /**
   * 设置技能等级
   */
  setSkillLevel(skillName, level) {
    if (SKILLS[skillName]) {
      this.skills[skillName] = Math.min(10, Math.max(0, level));
      return true;
    }
    return false;
  }
  
  /**
   * 提升技能
   */
  improveSkill(skillName, amount = 1) {
    const currentLevel = this.getSkillLevel(skillName);
    return this.setSkillLevel(skillName, currentLevel + amount);
  }
  
  /**
   * 技能检定
   */
  skillCheck(skillName, difficulty = 5) {
    const skillLevel = this.getSkillLevel(skillName);
    const roll = Math.floor(Math.random() * 20) + 1;
    const total = roll + skillLevel * 2;
    
    return {
      roll,
      skillLevel,
      total,
      difficulty,
      success: total >= difficulty,
      margin: total - difficulty
    };
  }
  
  /**
   * 获取所有技能
   */
  getAllSkills() {
    const result = [];
    for (const [key, level] of Object.entries(this.skills)) {
      if (level > 0 && SKILLS[key]) {
        result.push({
          id: key,
          ...SKILLS[key],
          level
        });
      }
    }
    return result;
  }
  
  // ==================== 物品相关 ====================
  
  /**
   * 添加物品
   */
  addItem(item) {
    if (typeof item === 'string') {
      item = { name: item, type: 'consumable' };
    }
    
    if (item.type === 'key' || item.important) {
      this.inventory.keyItems.push(item);
    } else if (item.type === 'currency') {
      this.inventory.currency += item.amount || 1;
    } else {
      this.inventory.items.push(item);
    }
    return true;
  }
  
  /**
   * 移除物品
   */
  removeItem(itemName) {
    const index = this.inventory.items.findIndex(i => i.name === itemName);
    if (index !== -1) {
      this.inventory.items.splice(index, 1);
      return true;
    }
    return false;
  }
  
  /**
   * 装备物品
   */
  equipItem(item) {
    const itemDef = ITEM_TYPES[item.type];
    if (!itemDef || !itemDef.slot) return false;
    
    // 如果已有装备，放入背包
    if (this.inventory[itemDef.slot]) {
      this.inventory.items.push(this.inventory[itemDef.slot]);
    }
    
    this.inventory[itemDef.slot] = item;
    return true;
  }
  
  /**
   * 卸下装备
   */
  unequipItem(slot) {
    if (this.inventory[slot]) {
      this.inventory.items.push(this.inventory[slot]);
      this.inventory[slot] = null;
      return true;
    }
    return false;
  }
  
  /**
   * 使用消耗品
   */
  useConsumable(itemName) {
    const index = this.inventory.items.findIndex(i => i.name === itemName);
    if (index === -1) return null;
    
    const item = this.inventory.items[index];
    if (item.type !== 'consumable') return null;
    
    // 应用效果
    if (item.effects) {
      for (const [stat, amount] of Object.entries(item.effects)) {
        this.modifyStat(stat, amount);
      }
    }
    
    this.inventory.items.splice(index, 1);
    return item;
  }
  
  /**
   * 获取所有物品
   */
  getAllItems() {
    return {
      weapon: this.inventory.weapon,
      armor: this.inventory.armor,
      accessory: this.inventory.accessory,
      items: this.inventory.items,
      keyItems: this.inventory.keyItems,
      currency: this.inventory.currency
    };
  }
  
  // ==================== 成长相关 ====================
  
  /**
   * 获得经验
   */
  gainExp(amount) {
    this.exp += amount;
    
    // 检查是否升级
    const newStage = GROWTH_STAGES.find((stage, index) => {
      const nextStage = GROWTH_STAGES[index + 1];
      return this.exp >= stage.expRequired && 
             (!nextStage || this.exp < nextStage.expRequired);
    });
    
    if (newStage && newStage.level > this.growthStage.level) {
      this.growthStage = newStage;
      this.level = newStage.level;
      return { leveledUp: true, newStage };
    }
    
    return { leveledUp: false };
  }
  
  /**
   * 获取成长进度
   */
  getGrowthProgress() {
    const currentExp = this.exp;
    const currentReq = this.growthStage.expRequired;
    const nextStage = GROWTH_STAGES.find(s => s.level === this.growthStage.level + 1);
    const nextReq = nextStage ? nextStage.expRequired : currentReq;
    
    return {
      stage: this.growthStage,
      currentExp,
      expInStage: currentExp - currentReq,
      expToNextLevel: nextReq - currentExp,
      progress: nextStage ? (currentExp - currentReq) / (nextReq - currentReq) : 1
    };
  }
  
  // ==================== 任务目标相关 ====================
  
  /**
   * 添加目标
   */
  addObjective(objective) {
    if (typeof objective === 'string') {
      objective = { id: this.generateId(), description: objective, completed: false };
    }
    this.objectives.push(objective);
    return objective;
  }
  
  /**
   * 完成目标
   */
  completeObjective(objectiveId) {
    const index = this.objectives.findIndex(o => o.id === objectiveId);
    if (index !== -1) {
      const objective = this.objectives.splice(index, 1)[0];
      objective.completed = true;
      objective.completedAt = new Date();
      this.completedObjectives.push(objective);
      
      // 完成目标获得经验
      const expGain = objective.expReward || 50;
      this.gainExp(expGain);
      
      return { objective, expGained: expGain };
    }
    return null;
  }
  
  /**
   * 获取所有目标
   */
  getObjectives() {
    return {
      active: this.objectives,
      completed: this.completedObjectives
    };
  }
  
  // ==================== 关系相关 ====================
  
  /**
   * 设置关系
   */
  setRelationship(targetId, relationship) {
    this.status.relationships.set(targetId, {
      ...relationship,
      since: new Date()
    });
  }
  
  /**
   * 获取关系
   */
  getRelationship(targetId) {
    return this.status.relationships.get(targetId) || null;
  }
  
  /**
   * 修改关系值
   */
  modifyRelationship(targetId, amount) {
    const current = this.getRelationship(targetId) || { value: 0 };
    current.value = Math.max(-100, Math.min(100, current.value + amount));
    this.setRelationship(targetId, current);
    return current.value;
  }
  
  // ==================== 状态相关 ====================
  
  /**
   * 添加状态效果
   */
  addCondition(condition) {
    if (!this.status.conditions.includes(condition)) {
      this.status.conditions.push(condition);
      return true;
    }
    return false;
  }
  
  /**
   * 移除状态效果
   */
  removeCondition(condition) {
    const index = this.status.conditions.indexOf(condition);
    if (index !== -1) {
      this.status.conditions.splice(index, 1);
      return true;
    }
    return false;
  }
  
  /**
   * 设置心情
   */
  setMood(mood) {
    this.status.mood = mood;
  }
  
  // ==================== 导出/导入 ====================
  
  /**
   * 导出角色数据
   */
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      age: this.age,
      occupation: this.occupation,
      stats: this.stats,
      skills: this.skills,
      background: this.background,
      traits: this.traits,
      inventory: {
        ...this.inventory,
        relationships: Object.fromEntries(this.status.relationships)
      },
      level: this.level,
      exp: this.exp,
      growthStage: this.growthStage,
      objectives: this.objectives,
      completedObjectives: this.completedObjectives,
      status: this.status,
      lingan: this.lingan
    };
  }
  
  /**
   * 从JSON导入
   */
  static fromJSON(data) {
    const char = new Character(data);
    if (data.inventory && data.inventory.relationships) {
      char.status.relationships = new Map(Object.entries(data.inventory.relationships));
    }
    return char;
  }
  
  /**
   * 获取角色摘要
   */
  getSummary() {
    const stats = this.getStats();
    return `【${this.name}】${this.occupation}
生命: ${stats.hp}/${stats.maxHp} | 攻击: ${stats.attack} | 防守: ${stats.defense} | 速度: ${stats.speed}
成长: ${this.growthStage.name} (Lv.${this.level})
技能: ${this.getAllSkills().map(s => `${s.name}(${s.level})`).join(' / ') || '无'}
随身: ${this.inventory.items.map(i => i.name || i).join('、') || '无'}
目标: ${this.objectives.map(o => o.description).join('、') || '无'}`;
  }
}

// ==================== 角色系统管理器 ====================

/**
 * 角色系统管理器
 */
class CharacterSystem {
  constructor() {
    this.characters = new Map();
    this.templates = CHARACTER_TEMPLATES;
    this.skills = SKILLS;
    this.growthStages = GROWTH_STAGES;
  }
  
  /**
   * 创建角色
   */
  createCharacter(options = {}) {
    // 如果指定了模板，使用模板作为基础
    if (options.template && this.templates[options.template]) {
      const template = this.templates[options.template];
      options = {
        ...template,
        ...options,
        hp: options.hp || template.baseStats.hp,
        maxHp: options.maxHp || options.hp || template.baseStats.hp,
        attack: options.attack || template.baseStats.attack,
        defense: options.defense || template.baseStats.defense,
        speed: options.speed || template.baseStats.speed,
        skills: { ...template.baseSkills, ...options.skills },
        items: options.items || [...template.startingItems],
        occupation: options.occupation || template.name,
        background: options.background || template.background,
        traits: options.traits || [...template.traits]
      };
    }
    
    const character = new Character(options);
    this.characters.set(character.id, character);
    return character;
  }
  
  /**
   * 获取角色
   */
  getCharacter(id) {
    return this.characters.get(id);
  }
  
  /**
   * 删除角色
   */
  removeCharacter(id) {
    return this.characters.delete(id);
  }
  
  /**
   * 获取所有角色
   */
  getAllCharacters() {
    return Array.from(this.characters.values());
  }
  
  /**
   * 从灵安城数据创建角色
   */
  createFromLinganData(data) {
    const characters = [];
    
    // 解析灵安城角色数据
    // 根据数据结构提取角色信息
    const roleRecords = data['角色记录'] || [];
    
    // 锦娘
    const jinNiang = this.createCharacter({
      template: 'merchant',
      name: '锦娘',
      age: '30岁',
      occupation: '农场主',
      hp: 9,
      attack: 3,
      defense: 3,
      speed: 3,
      skills: { social: 2, persuasion: 2, finance: 2 },
      background: '家族产业继承者，曾创作奶茶商业奇迹。独身未嫁是个谜。',
      traits: ['商业头脑', '胆小易怒'],
      items: ['账本', '算盘', '债卷'],
      currency: 20000,
      objectives: [
        { id: 'obj_jn_1', description: '维持生意正常运转' },
        { id: 'obj_jn_2', description: '复兴家业，家财万贯' }
      ]
    });
    jinNiang.setMood('惊恐'); // 因瘟疫影响
    characters.push(jinNiang);
    
    // 欢喜仔
    const huanXi = this.createCharacter({
      template: 'rogue',
      name: '欢喜仔',
      age: '20岁出头',
      occupation: '侠盗',
      hp: 11,
      attack: 4,
      defense: 4,
      speed: 5,
      skills: { deception: 2, stealth: 2, theft: 2 },
      background: '自幼孤儿，被乞丐抚养长大。痴迷武学，只偷富贵者，在乞丐中有人缘。',
      traits: ['武痴', '怕麻烦', '憎恨权贵'],
      items: ['绳索', '夜行衣'],
      currency: 500,
      objectives: [
        { id: 'obj_hx_1', description: '练成盖世武功，成为一代大侠' },
        { id: 'obj_hx_2', description: '隐身江湖，肆意恩仇' }
      ]
    });
    characters.push(huanXi);
    
    // 王双
    const wangShuang = this.createCharacter({
      template: 'guard',
      name: '王双',
      age: '35岁',
      occupation: '御前侍卫',
      hp: 12,
      attack: 6,
      defense: 5,
      speed: 6,
      skills: { investigation: 2, rhetoric: 2, authority: 2 },
      background: '学得文武艺，层层选拔为御前侍卫，被前任统领赏识传授双刀技法。有一妻一女。',
      traits: ['武艺超群', '机敏'],
      items: ['双刀', '腰牌', '佛珠(线索物品)'],
      currency: 2000,
      objectives: [
        { id: 'obj_ws_1', description: '奉皇帝旨意调查瘟疫起源', urgent: true }
      ]
    });
    wangShuang.setMood('惊喜'); // 发现了线索
    characters.push(wangShuang);
    
    // 刺客
    const assassin = this.createCharacter({
      template: 'assassin',
      name: '神秘刺客',
      occupation: '刺客',
      hp: 10,
      attack: 4,
      defense: 3,
      speed: 3,
      skills: { stealth: 3 },
      background: '身份神秘的刺客，擅长伪装和暗杀。',
      traits: ['冷酷', '隐蔽'],
      items: ['竹篙刀', '黑球(烟雾弹)'],
      objectives: [
        { id: 'obj_as_1', description: '阻止瘟疫调查', hidden: true }
      ]
    });
    characters.push(assassin);
    
    // NPC角色
    const yuanYi = this.createCharacter({
      name: '元姨',
      age: '不详',
      occupation: '古宅主人',
      hp: 6,
      attack: 1,
      defense: 2,
      speed: 2,
      skills: { social: 3, rhetoric: 2 },
      background: '太爷的小妾，太爷娶她时已年近花甲。每日吃斋念佛，供奉地藏菩萨。',
      traits: ['威严', '神秘', '守口如瓶'],
      items: ['地藏菩萨像(缺失宝珠)'],
      objectives: [
        { id: 'obj_yy_1', description: '守护古宅秘密', hidden: true }
      ]
    });
    characters.push(yuanYi);
    
    return characters;
  }
  
  /**
   * 生成角色背景故事
   */
  generateBackground(character, theme = 'lingan') {
    const templates = {
      lingan: [
        '灵安年间，社会升平，{name}却卷入了暗流涌动的漩涡...',
        '瘟疫肆虐之际，{name}的命运发生了转折...',
        '在灵安城的某个角落，{name}开始了{occupation}的生涯...',
        '{name}，一个{traits.join("、")}的人，在乱世中寻找自己的道路...'
      ]
    };
    
    const templateList = templates[theme] || templates.lingan;
    const template = templateList[Math.floor(Math.random() * templateList.length)];
    
    return template
      .replace('{name}', character.name)
      .replace('{occupation}', character.occupation)
      .replace('{traits}', character.traits.join('、'));
  }
  
  /**
   * 角色互动
   */
  interaction(char1Id, char2Id, type = 'talk') {
    const char1 = this.getCharacter(char1Id);
    const char2 = this.getCharacter(char2Id);
    
    if (!char1 || !char2) return null;
    
    const result = {
      type,
      participants: [char1.name, char2.name],
      effects: []
    };
    
    switch (type) {
      case 'talk':
        // 社交检定
        const check1 = char1.skillCheck('social', 5);
        const check2 = char2.skillCheck('social', 5);
        
        if (check1.success && check2.success) {
          char1.modifyRelationship(char2Id, 5);
          char2.modifyRelationship(char1Id, 5);
          result.effects.push({ type: 'relationship', change: 5 });
        }
        break;
        
      case 'combat':
        // 战斗（简化版）
        while (char1.stats.hp > 0 && char2.stats.hp > 0) {
          // char1攻击
          const dmg1 = char1.getStats().attack - char2.getStats().defense;
          char2.takeDamage(Math.max(1, dmg1));
          
          if (char2.stats.hp <= 0) {
            result.winner = char1.name;
            break;
          }
          
          // char2攻击
          const dmg2 = char2.getStats().attack - char1.getStats().defense;
          char1.takeDamage(Math.max(1, dmg2));
          
          if (char1.stats.hp <= 0) {
            result.winner = char2.name;
            break;
          }
        }
        break;
        
      case 'trade':
        // 交易
        result.effects.push({ type: 'trade', possible: true });
        break;
    }
    
    return result;
  }
  
  /**
   * 保存所有角色数据
   */
  save() {
    const data = {};
    for (const [id, char] of this.characters) {
      data[id] = char.toJSON();
    }
    return data;
  }
  
  /**
   * 加载角色数据
   */
  load(data) {
    this.characters.clear();
    for (const [id, charData] of Object.entries(data)) {
      this.characters.set(id, Character.fromJSON(charData));
    }
  }
  
  /**
   * 获取系统状态摘要
   */
  getStatus() {
    return {
      totalCharacters: this.characters.size,
      characters: Array.from(this.characters.values()).map(c => ({
        id: c.id,
        name: c.name,
        occupation: c.occupation,
        level: c.level,
        stage: c.growthStage.name
      }))
    };
  }
}

// ==================== 导出 ====================

module.exports = {
  Character,
  CharacterSystem,
  SKILLS,
  GROWTH_STAGES,
  ITEM_TYPES,
  CHARACTER_TEMPLATES
};
