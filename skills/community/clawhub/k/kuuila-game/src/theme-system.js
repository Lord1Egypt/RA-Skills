/**
 * Kuuila Game v2.7 - 主题模组系统
 * 支持多主题切换：武侠、修仙、克苏鲁、赛博朋克、中世纪战团、民国上海滩
 */

const path = require('path');
const fs = require('fs');

// ============================================================================
// 主题定义
// ============================================================================

const THEMES = {
  wuxia: {
    id: 'wuxia',
    name: '武侠',
    nameEn: 'Wuxia',
    style: '国风',
    description: '江湖门派、武功秘籍、侠义恩仇',
    features: ['江湖门派', '武功秘籍', '内功修炼', '兵器锻造'],
    artStyle: '国风',
    keywords: ['侠客', '门派', '江湖', '武功', '秘籍', '兵器', '内功', '轻功'],
    colorScheme: {
      primary: '#8B4513',
      secondary: '#D4AF37',
      accent: '#FF6347',
      background: '#F5F5DC'
    },
    atmosphere: '豪迈热血、侠骨柔情',
    typicalCharacters: ['侠客', '刺客', '道士', '僧侣', '农场主', '皇帝', '复仇之人'],
    typicalLocations: ['竹林', '古宅', '道观', '寺庙', '宫殿', '码头', '房顶']
  },

  xianxia: {
    id: 'xianxia',
    name: '修仙',
    nameEn: 'Xianxia',
    style: '仙侠',
    description: '突破境界、法宝修炼、渡劫飞升',
    features: ['境界突破', '法宝修炼', '渡劫飞升', '丹药炼制'],
    artStyle: '仙侠',
    keywords: ['修仙', '境界', '法宝', '丹药', '渡劫', '飞升', '灵气', '洞府'],
    colorScheme: {
      primary: '#4169E1',
      secondary: '#87CEEB',
      accent: '#FFD700',
      background: '#F0F8FF'
    },
    atmosphere: '仙气缥缈、玄妙空灵',
    typicalCharacters: ['老叟', '魂魄', '精怪', '魔族', '哑巴', '铁匠', '囚犯', '窃贼'],
    typicalLocations: ['洞府', '禁地', '祭台', '战场', '寺庙', '地下', '比武场']
  },

  cthulhu: {
    id: 'cthulhu',
    name: '克苏鲁',
    nameEn: 'Cthulhu Mythos',
    style: '悬疑',
    description: '理智值、邪神、不可名状的恐惧',
    features: ['理智系统', '邪神崇拜', '神秘调查', '禁忌知识'],
    artStyle: '悬疑',
    keywords: ['邪神', '理智', '调查', '禁忌', '仪式', '疯狂', '异象', '献祭'],
    colorScheme: {
      primary: '#2F4F4F',
      secondary: '#696969',
      accent: '#00CED1',
      background: '#1C1C1C'
    },
    atmosphere: '诡秘恐怖、压抑疯狂',
    typicalCharacters: ['医生', '侦探', '记者', '牧师', '深潜者', '食尸鬼', '治安官', '伐木工'],
    typicalLocations: ['教堂', '诊所', '医院', '海边', '仓库', '调查所', '温泉旅馆', '度假村']
  },

  cyberpunk: {
    id: 'cyberpunk',
    name: '赛博朋克',
    nameEn: 'Cyberpunk',
    style: '科幻',
    description: '义体改造、黑客技术、企业阴谋',
    features: ['义体改造', '黑客技术', '企业阴谋', '神经接口'],
    artStyle: '科幻',
    keywords: ['义体', '黑客', '企业', '神经', '赛博', '改造', '虚拟', '数据'],
    colorScheme: {
      primary: '#FF1493',
      secondary: '#00FF7F',
      accent: '#FFFF00',
      background: '#0D0D0D'
    },
    atmosphere: '霓虹闪烁、科技堕落',
    typicalCharacters: ['黑客', '机械工程师', '生化人', '企业间谍', '赏金猎人'],
    typicalLocations: ['酒吧', '贫民窟', '地下赌场', '实验室', '数据中心', '虚拟空间']
  },

  medieval: {
    id: 'medieval',
    name: '中世纪战团',
    nameEn: 'Medieval Warband',
    style: '欧美',
    description: '骑士荣耀、城堡攻防、领主权谋',
    features: ['骑士精神', '城堡攻防', '领主权谋', '魔法诅咒'],
    artStyle: '欧美',
    keywords: ['骑士', '城堡', '领主', '魔法', '战团', '盔甲', '诅咒', '王权'],
    colorScheme: {
      primary: '#8B0000',
      secondary: '#DAA520',
      accent: '#483D8B',
      background: '#2F4F4F'
    },
    atmosphere: '战火纷飞、荣耀背叛',
    typicalCharacters: ['骑士', '船长', '巫婆', '巨人', '国王', '王后', '公主', '王子'],
    typicalLocations: ['城堡', '塔楼', '教堂', '宫殿', '农田', '森林', '码头', '监狱']
  },

  republican: {
    id: 'republican',
    name: '民国上海滩',
    nameEn: 'Republican Shanghai',
    style: '近代',
    description: '谍战风云、怪谈传说、旧上海风情',
    features: ['谍战情报', '帮派纷争', '怪谈传说', '租界势力'],
    artStyle: '近代',
    keywords: ['谍战', '帮派', '租界', '谍报', '上海滩', '青帮', '情报', '暗杀'],
    colorScheme: {
      primary: '#191970',
      secondary: '#B8860B',
      accent: '#DC143C',
      background: '#FFF8DC'
    },
    atmosphere: '纸醉金迷、暗流涌动',
    typicalCharacters: ['民工', '车夫', '斧头帮', '大人物', '军人', '记者', '侦探', '特工'],
    typicalLocations: ['酒吧', '工地', '码头', '舞厅', '租界', '茶馆', '弄堂', '工厂']
  }
};

// ============================================================================
// 主题卡牌库 - 从游戏设计源数据提取
// ============================================================================

const THEME_CARD_LIBRARIES = {
  wuxia: {
    characters: [
      '复仇之人', '退伍士兵', '执刑人', '刺客', '车夫', '小狗', '道士',
      '生化人', '猎人', '农场主', '老鼠', '鱼群', '小孩子', '侠客',
      '黄衣女子', '皇帝', '水管工', '僧侣'
    ],
    locations: [
      '岛', '塔', '码头', '房顶', '森林', '壁炉', '道观', '实验室',
      '古堡', '葡萄园', '地下酒窖', '温泉', '青楼', '竹林', '古宅',
      '宫殿', '密道', '寺庙', '颉嵬城', '灵安城'
    ],
    items: [
      '财宝', '斧头', '围巾', '礼物', '铁锅', '食物', '十字架', '针管',
      '猎枪', '账本', '金子', '石头', '花灯', '断剑', '被破坏的伞',
      '白绫', '蘑菇', '佛珠'
    ],
    states: [
      '失窃', '丑', '感动', '中毒', '马虎', '害怕', '怜悯', '狂暴',
      '惊喜', '贪婪', '逃窜', '惊恐', '心满意足', '愤怒', '憎恨',
      '哀怨', '困惑', '神圣'
    ],
    events: [
      '某物坏了', '很冰冷的', '很久不见', '被击倒', '复仇失败', '守护',
      '倾听祷告', '发现与家人合影', '发现可爱猎物', '铺面扩张', '失忆',
      '在梦中', '竞赛', '风暴雨来了', '地震', '被胁迫', '重病', '录像'
    ],
    endings: [
      '揪出了藏匿在水手里的叛徒', '属于他的守护神消失了',
      '这对父母与他们失散多年的孩子重逢', '她表明了她的真实身份 两人结为夫妻',
      '真心忏悔，帮助村里的居民', '他们一直照顾它 直到它长大',
      '通过拯救收获一批教徒', '回忆起曾经的自己', '它长久陪伴着他',
      '葡萄泛滥成灾', '饿到发狂了', '两个人不欢而散'
    ],
    rules: [
      '世道充满邪恶（之后没有善良角色出场）',
      '传奇总是少数（每人的故事最多出现5人）',
      '世界发生巨大的变故',
      '故事背后有可怕的内幕'
    ],
    mapRules: {
      land: { cost: 1, description: '路面消耗1点' },
      building: { cost: 2, description: '建筑物消耗2点' },
      river: { 
        cost: 'variable',
        description: '先判定天气，1-3为阴天，阴天只能随机方向一格。4-6为晴天，任意走一格'
      },
      respawn: { description: '角色转生 重新捏角色' }
    }
  },

  xianxia: {
    characters: [
      '老叟', '魂魄', '王', '哑巴', '精怪', '铁匠', '窃贼', '厨师',
      '囚犯', '复仇之人', '孤儿', '魔族'
    ],
    locations: [
      '洞府', '高处', '地下', '黑暗的地方', '无人之处', '迷雾笼罩之处',
      '刑场', '宫殿', '交易市场', '寺庙', '岛', '禁地',
      '比武场', '吃饭的地方', '祭台', '战场', '墓地'
    ],
    items: [
      '尸体', '武器', '鼎', '门', '丹药', '碎片', '镜', '珠宝',
      '瓶子', '锁链', '云', '铜钱', '气', '草', '咒语', '宴席',
      '书', '影子', '鱼竿', '水', '火', '神像', '平底锅', '魔兽',
      '毒', '祭品', '可乐', '乐器'
    ],
    states: [
      '冰冻的', '无法书写', '想象之中', '被人传颂', '古老', '美丽',
      '丑', '散发异味', '崭新', '断开', '无人知晓', '会说话的',
      '失去形体', '变形', '失去理智', '发出异香', '伪装', '裸体'
    ],
    events: [], // 修仙流更注重规则而非事件
    endings: [
      '他成为了一段传奇，但除此之外什么也没有剩下',
      '从此以后，再也没有人能够找到它',
      '他们抛弃了过去的一切', '一家人再度团聚', '财富就埋藏在此处',
      '光阴荏苒\n那段往事也逐渐被淡忘', '长生\n终究是一个虚幻的梦',
      '最终\n只有他一人达到了那个境界', '他们的恩怨一笔勾销',
      '为了世界的安宁\n它再次被封印', '除了他之外\n再也没有人可以做到',
      '这是他们的选择\n他们必须承受后果', '危机就此解除\n他们再次踏上了旅途',
      '他的路还很长'
    ],
    rules: [
      '世道充满邪恶（之后没有善良角色出场）',
      '传奇总是少数（每人的故事最多出现5人）',
      '世界发生巨大的变故',
      '故事背后有可怕的内幕',
      '你拥有了一件有灵智的物品',
      '行善积德（故事中发生一件善事）',
      '命运让你们交汇（让你的角色与其他人的角色遭遇）',
      '现有的一个人物拥有惊人的背景',
      '一场大战一触即发',
      '运气离你远去',
      '先祖指引我们前行',
      '可恨之人必有可怜之处',
      '戛然而止（故事必须在3回合内结束）',
      '漫漫长路（故事不得在5回合内结束）',
      '事情发展更加错综复杂（抽词数+1）',
      '天降的好运改变了某人的命运'
    ]
  },

  cthulhu: {
    characters: [
      '医生', '保姆', '镇长', '治安官', '伐木工', '管理员', '侦探',
      '盗贼', '法官', '记者', '牧师', '变种组合生物', '食尸鬼',
      '深潜者', '巨型海怪', '猎犬', '苍蝇', '蜘蛛', '老鼠', '蜜蜂', '毒蛇'
    ],
    locations: [
      '教堂', '诊所', '温泉旅馆', '农庄', '度假村', '仓库', '中心广场',
      '会议室', '学校', '街道', '医院', '调查所', '海边'
    ],
    items: [
      '枪', '棍棒', '绳索', '细针', '画像', '血迹', '信件', '档案记录',
      '头发', '纸片', '阵法', '催眠', '幻术', '诅咒', '长生不老术',
      '民间法典', '旧神遗物', '都市异闻'
    ],
    states: [
      '响动', '悄悄的', '丧失一点理智', '陷入疯狂', '恐怖的景象',
      '被蛊惑的', '行动受阻', '完全防御', '发出蓝光的', '彼此不信任的',
      '闪动的黑影', '时空碎裂', '患上抑郁症', '分裂的人格'
    ],
    events: [
      '生育', '某地区受到攻击', '侦察信息', '心理学鉴定', '献祭某物',
      '拯救某人', '血脉繁衍', '快速进攻', '战斗打响', '能量波动吸引它们',
      '获得了那个法术'
    ],
    endings: [
      '被不可名状的存在吞噬', '陷入永恒的疯狂',
      '揭开了禁忌的真相，付出代价', '成功封印了邪恶',
      '逃离了诅咒之地', '成为邪神的眷属'
    ],
    rules: [
      '理智值低于一定数值会陷入疯狂',
      '遭遇邪神相关事件需要理智判定',
      '禁忌知识会降低理智但提供线索'
    ],
    sanityMechanics: {
      initialSanity: 100,
      lossThreshold: 30,
      recoveryActions: ['休息', '治疗', '精神慰藉']
    }
  },

  cyberpunk: {
    characters: [
      '黑客', '机械工程师', '生化人', '企业间谍', '赏金猎人', '街童',
      '公司高管', '义体医生', '夜之城守护者'
    ],
    locations: [
      '酒吧', '贫民窟', '地下赌场', '实验室', '数据中心', '虚拟空间',
      '企业大楼', '黑市', '改造诊所', '霓虹街'
    ],
    items: [
      '义肢', '浮空摩托', '人工心脏', '神经接口', '数据芯片', '黑客工具',
      '武器模组', '能量护盾', '隐身装置', '记忆芯片'
    ],
    states: [
      '被通缉', '义体过载', '神经损伤', '企业追杀', '身份暴露',
      '数据被黑', '系统崩溃', '改造完成'
    ],
    events: [
      '收保护费', '手术', '火拼', '被通缉', '数据入侵', '企业突袭',
      '黑客攻击', '义体故障', '记忆篡改'
    ],
    endings: [
      '推翻了企业的统治', '成为传说级黑客',
      '融入了赛博空间', '找到了真实的人性',
      '被系统同化消失', '逃离了夜之城'
    ],
    rules: [
      '义体改造会消耗人性值',
      '企业追杀会增加危险等级',
      '黑客技能可以远程操控'
    ],
    augmentSystem: {
      bodyParts: ['手臂', '腿', '眼', '神经', '心脏'],
      rarity: ['普通', '军用', '传说'],
      humanityCost: 10
    }
  },

  medieval: {
    characters: [
      '船长', '小孩', '巨人', '贼', '巫婆', '小狗', '小姑娘', '怪物',
      '丈夫/妻子', '乞丐', '继母', '父母', '复仇之人', '退伍老兵',
      '执刑人', '刺客', '骑士'
    ],
    locations: [
      '岛', '塔', '码头', '房顶', '森林', '壁炉', '阁楼', '教堂',
      '马车', '农舍', '监狱', '路', '废墟', '农田', '沙发', '托斯卡纳大陆'
    ],
    items: [
      '财宝', '斧头', '围巾', '礼物', '铁锅', '食物', '钥匙', '火鸡',
      '奶酪', '树', '戒指', '窗', '船', '钢琴', '绞架', '大炮', '盔甲'
    ],
    states: [
      '失窃', '丑', '感动', '中毒', '马虎', '害怕', '美丽', '心满意足',
      '贪婪', '彪悍', '微笑', '高兴', '愚蠢', '贫穷', '古老', '散发异味',
      '失去理智'
    ],
    events: [
      '某物坏了', '很冰冷的', '很久不见', '被击倒', '复仇失败', '守护',
      '失忆', '梦', '比赛', '两人相爱', '某人受伤', '风暴', '计划', '发病了'
    ],
    endings: [
      '揪出了藏匿在水手里的叛徒', '属于他的守护神消失了',
      '这对父母与他们失散多年的孩子重逢', '她表明了她的真实身份 两人结为夫妻',
      '真心忏悔，帮助村里的居民', '他们一直照顾他 直到她长大',
      '寻找自己的亲生父亲', '饿到发狂了', '两个人不欢而散',
      '她再也不让它离开它的视线半步', '他意识到他的兄弟是多么忠诚',
      '这个故事证明了 一颗纯洁的心可以战胜一切'
    ],
    rules: [
      '骑士精神影响NPC态度',
      '魔法诅咒需要特殊方法解除',
      '城堡攻防有战术加成'
    ],
    mapRules: {
      land: { cost: 1, description: '陆地消耗1点' },
      forest: { cost: 2, description: '森林消耗2点' },
      ocean: { 
        cost: 'variable',
        description: '先判定天气，1-3为阴天，阴天只能随机方向一格。4-6为晴天，任意走一格'
      }
    },
    historicalProgress: {
      description: '中世纪历史进程',
      phases: ['和平', '动荡', '战争', '重建']
    }
  },

  republican: {
    characters: [
      '民工', '车夫', '斧头帮', '大人物', '丈夫/妻子', '厨师', '记者', '军人'
    ],
    locations: [
      '酒吧', '工地', '森林', '塔', '张宅', '地图', '街道', '茶馆',
      '舞厅', '码头', '租界', '弄堂', '工厂'
    ],
    items: [
      '情报', '密信', '武器', '金钱', '鸦片', '证件', '照片', '账本'
    ],
    states: [
      '被监视', '身份暴露', '受伤', '中毒', '被捕', '潜伏', '逃亡'
    ],
    events: [
      '帮派火拼', '情报交易', '暗杀行动', '租界巡捕', '青帮收租',
      '谍报交换', '突发事件', '政治风云'
    ],
    endings: [
      '成功完成谍报任务', '揭露了惊天阴谋',
      '逃离了上海滩', '成为帮派大佬',
      '在上海滩建立势力', '被卷入漩涡消失'
    ],
    rules: [
      '租界有特殊法律保护',
      '帮派关系影响行动',
      '情报网络提供线索'
    ],
    factionSystem: {
      factions: ['青帮', '红帮', '租界势力', '国民政府', '日本特务'],
      reputation: ['敌对', '中立', '友好', '盟友']
    },
    mapRules: {
      unknown: { cost: 2, description: '未翻开消耗2点' },
      revealed: { cost: 1, description: '已翻开消耗1点' }
    }
  }
};

// ============================================================================
// 主题剧情模板
// ============================================================================

const THEME_STORY_TEMPLATES = {
  wuxia: {
    opening: [
      '在颉嵬城的街头，江湖人士暗流涌动...',
      '灵安年间，一场瘟疫打破了平静...',
      '古老门派的秘籍重现江湖，各路人马虎视眈眈...'
    ],
    conflict: [
      '门派之间的恩怨纠葛',
      '朝廷与江湖的对立',
      '武功秘籍引发的争夺',
      '复仇与救赎的故事'
    ],
    climax: [
      '门派大战一触即发',
      '真相大白于天下',
      '生死决战在即'
    ],
    resolution: [
      '侠义精神得以传承',
      '江湖重归平静',
      '新的传说开始流传'
    ]
  },

  xianxia: {
    opening: [
      '天地灵气复苏，修仙之路开启...',
      '洞府深处，一道金光冲天而起...',
      '渡劫失败，重修再起...'
    ],
    conflict: [
      '境界突破的瓶颈',
      '法宝争夺的纷争',
      '正邪两道的较量',
      '仙魔大战的序幕'
    ],
    climax: [
      '渡劫飞升的关键时刻',
      '仙魔大战全面爆发',
      '天地大劫降临'
    ],
    resolution: [
      '成功飞升成仙',
      '守护了人间安宁',
      '修仙之道永无止境'
    ]
  },

  cthulhu: {
    opening: [
      '夜晚的街道传来诡异的声响...',
      '收到一封神秘的信件，开启了调查之旅...',
      '海边的小镇，最近失踪事件频发...'
    ],
    conflict: [
      '理智的逐渐丧失',
      '禁忌知识的诱惑',
      '邪神信徒的阴谋',
      '不可名状的恐怖'
    ],
    climax: [
      '直面邪神的恐惧',
      '揭开终极真相',
      '理智濒临崩溃'
    ],
    resolution: [
      '成功封印了邪恶',
      '逃离了诅咒之地',
      '永远被困在疯狂中'
    ]
  },

  cyberpunk: {
    opening: [
      '霓虹灯下，夜之城的阴影中...',
      '接到了一个高价的委托任务...',
      '企业大楼的顶层，一场密谋正在进行...'
    ],
    conflict: [
      '企业之间的权力斗争',
      '义体改造的代价',
      '黑客攻击的威胁',
      '身份认同的危机'
    ],
    climax: [
      '突入企业核心',
      '终极黑客对决',
      '真相即将揭露'
    ],
    resolution: [
      '推翻了企业的统治',
      '找到了真实的人性',
      '消失在赛博空间中'
    ]
  },

  medieval: {
    opening: [
      '战鼓擂响，中世纪的战场...',
      '城堡的钟声响起，领主召集骑士...',
      '一片祥和的村庄，突然遭到袭击...'
    ],
    conflict: [
      '骑士精神的考验',
      '领主之间的战争',
      '魔法诅咒的阴影',
      '荣誉与背叛的选择'
    ],
    climax: [
      '城堡攻防战',
      '骑士的终极决斗',
      '魔法力量觉醒'
    ],
    resolution: [
      '捍卫了骑士荣耀',
      '解除了古老诅咒',
      '和平重归大地'
    ]
  },

  republican: {
    opening: [
      '上海滩的夜晚，霓虹初上...',
      '收到一份机密文件，命运的齿轮开始转动...',
      '帮派的争斗一触即发...'
    ],
    conflict: [
      '帮派地盘的争夺',
      '谍报战的暗流',
      '租界势力的角力',
      '身份的隐藏与暴露'
    ],
    climax: [
      '惊天阴谋即将揭晓',
      '多方势力的最终对决',
      '生死存亡的关键时刻'
    ],
    resolution: [
      '成功完成谍报任务',
      '在上海滩站稳脚跟',
      '离开是非之地'
    ]
  }
};

// ============================================================================
// 画风标签系统
// ============================================================================

const ART_STYLE_TAGS = {
  // 基础画风
  styles: ['国风', '仙侠', '悬疑', '科幻', '欧美', '近代', '日漫', '都市', '热血', '战团', '日常', '鬼畜', '狗血'],
  
  // 氛围标签
  atmospheres: {
    wuxia: ['豪迈', '热血', '侠义', '恩仇', '江湖', '柔情'],
    xianxia: ['缥缈', '玄妙', '空灵', '仙气', '神秘', '超脱'],
    cthulhu: ['诡秘', '恐怖', '压抑', '疯狂', '诡异', '阴森'],
    cyberpunk: ['霓虹', '科技', '堕落', '前卫', '炫酷', '赛博'],
    medieval: ['史诗', '荣耀', '战火', '背叛', '魔法', '骑士'],
    republican: ['纸醉金迷', '暗流', '谍影', '风情', '旧时光', '魅惑']
  },
  
  // 场景标签
  sceneTypes: {
    battle: ['战斗', '决斗', '群战', '突袭', '防守'],
    exploration: ['探险', '寻宝', '调查', '发现', '解密'],
    social: ['交易', '谈判', '社交', '聚会', '宴会'],
    mystery: ['悬疑', '推理', '调查', '线索', '真相'],
    romance: ['情感', '爱情', '纠葛', '守护', '牺牲']
  },
  
  // 角色标签
  characterArchetypes: {
    hero: ['主角', '英雄', '救世主', '天选之人'],
    villain: ['反派', '邪神', '魔头', '幕后黑手'],
    mentor: ['导师', '长者', '智者', '引路人'],
    companion: ['伙伴', '战友', '恋人', '助手'],
    neutral: ['中立', '旁观者', '商人', '路人']
  }
};

// ============================================================================
// 主题加载器类
// ============================================================================

class ThemeLoader {
  constructor() {
    this.currentTheme = null;
    this.cardLibrary = null;
    this.storyTemplate = null;
    this.artStyleConfig = null;
    this.customThemes = new Map();
  }

  /**
   * 加载指定主题
   */
  loadTheme(themeId) {
    // 检查是否是内置主题
    if (THEMES[themeId]) {
      this.currentTheme = THEMES[themeId];
      this.cardLibrary = THEME_CARD_LIBRARIES[themeId];
      this.storyTemplate = THEME_STORY_TEMPLATES[themeId];
      this.artStyleConfig = this._buildArtStyleConfig(themeId);
      return true;
    }
    
    // 检查是否是自定义主题
    if (this.customThemes.has(themeId)) {
      const customTheme = this.customThemes.get(themeId);
      this.currentTheme = customTheme.theme;
      this.cardLibrary = customTheme.cardLibrary;
      this.storyTemplate = customTheme.storyTemplate;
      this.artStyleConfig = this._buildArtStyleConfig(themeId);
      return true;
    }
    
    return false;
  }

  /**
   * 注册自定义主题
   */
  registerCustomTheme(themeId, themeConfig) {
    if (THEMES[themeId]) {
      throw new Error(`主题 ${themeId} 已存在，不能覆盖内置主题`);
    }
    
    this.customThemes.set(themeId, {
      theme: {
        id: themeId,
        ...themeConfig
      },
      cardLibrary: themeConfig.cardLibrary || {},
      storyTemplate: themeConfig.storyTemplate || {}
    });
    
    return true;
  }

  /**
   * 获取当前主题
   */
  getCurrentTheme() {
    return this.currentTheme;
  }

  /**
   * 获取当前卡牌库
   */
  getCardLibrary() {
    return this.cardLibrary;
  }

  /**
   * 获取剧情模板
   */
  getStoryTemplate() {
    return this.storyTemplate;
  }

  /**
   * 获取画风配置
   */
  getArtStyleConfig() {
    return this.artStyleConfig;
  }

  /**
   * 列出所有可用主题
   */
  listThemes() {
    const builtIn = Object.keys(THEMES);
    const custom = Array.from(this.customThemes.keys());
    return {
      builtIn,
      custom,
      all: [...builtIn, ...custom]
    };
  }

  /**
   * 构建画风配置
   */
  _buildArtStyleConfig(themeId) {
    const theme = THEMES[themeId] || this.customThemes.get(themeId)?.theme;
    if (!theme) return null;
    
    return {
      primaryStyle: theme.artStyle,
      colorScheme: theme.colorScheme,
      atmosphere: theme.atmosphere,
      tags: ART_STYLE_TAGS.atmospheres[themeId] || [],
      sceneTypes: ART_STYLE_TAGS.sceneTypes,
      characterArchetypes: ART_STYLE_TAGS.characterArchetypes
    };
  }
}

// ============================================================================
// 主题卡牌库管理器
// ============================================================================

class ThemeCardManager {
  constructor(themeLoader) {
    this.themeLoader = themeLoader;
    this.drawnCards = {
      characters: [],
      locations: [],
      items: [],
      states: [],
      events: [],
      endings: []
    };
  }

  /**
   * 随机抽取卡牌
   */
  drawCard(type, count = 1) {
    const library = this.themeLoader.getCardLibrary();
    if (!library || !library[type] || library[type].length === 0) {
      // 该类型卡牌库为空或不存在，返回空数组
      return [];
    }
    
    const available = library[type].filter(card => 
      !this.drawnCards[type].includes(card)
    );
    
    if (available.length === 0) {
      // 如果所有卡牌都已抽取，重置已抽取列表后重新抽取
      this.drawnCards[type] = [];
      // 直接从原始库中随机抽取，避免递归
      const pool = library[type];
      const drawn = [];
      for (let i = 0; i < Math.min(count, pool.length); i++) {
        const randomIndex = Math.floor(Math.random() * pool.length);
        const card = pool[randomIndex];
        if (!drawn.includes(card)) {
          drawn.push(card);
          this.drawnCards[type].push(card);
        }
      }
      return drawn;
    }
    
    const drawn = [];
    for (let i = 0; i < Math.min(count, available.length); i++) {
      const randomIndex = Math.floor(Math.random() * available.length);
      const card = available[randomIndex];
      drawn.push(card);
      this.drawnCards[type].push(card);
      available.splice(randomIndex, 1);
    }
    
    return drawn;
  }

  /**
   * 抽取完整场景
   */
  drawScene() {
    return {
      character: this.drawCard('characters', 1)[0],
      location: this.drawCard('locations', 1)[0],
      item: this.drawCard('items', 1)[0],
      state: this.drawCard('states', 1)[0],
      event: this.drawCard('events', 1)[0]
    };
  }

  /**
   * 抽取结局
   */
  drawEnding() {
    return this.drawCard('endings', 1)[0];
  }

  /**
   * 获取主题规则
   */
  getRules() {
    const library = this.themeLoader.getCardLibrary();
    return library?.rules || [];
  }

  /**
   * 获取地图规则
   */
  getMapRules() {
    const library = this.themeLoader.getCardLibrary();
    return library?.mapRules || {};
  }

  /**
   * 重置已抽取的卡牌
   */
  reset() {
    this.drawnCards = {
      characters: [],
      locations: [],
      items: [],
      states: [],
      events: [],
      endings: []
    };
  }

  /**
   * 获取剩余卡牌数量
   */
  getRemainingCards() {
    const library = this.themeLoader.getCardLibrary();
    if (!library) return {};
    
    const remaining = {};
    for (const type of Object.keys(this.drawnCards)) {
      if (library[type]) {
        remaining[type] = library[type].length - this.drawnCards[type].length;
      }
    }
    return remaining;
  }
}

// ============================================================================
// 主题剧情生成器
// ============================================================================

class ThemeStoryGenerator {
  constructor(themeLoader, cardManager) {
    this.themeLoader = themeLoader;
    this.cardManager = cardManager;
  }

  /**
   * 生成开场
   */
  generateOpening() {
    const template = this.themeLoader.getStoryTemplate();
    if (!template || !template.opening) {
      return '故事开始了...';
    }
    
    const scene = this.cardManager.drawScene();
    const openingLine = template.opening[Math.floor(Math.random() * template.opening.length)];
    
    return this._interpolateTemplate(openingLine, scene);
  }

  /**
   * 生成分歧点
   */
  generateConflict() {
    const template = this.themeLoader.getStoryTemplate();
    if (!template || !template.conflict) {
      return '冲突发生了...';
    }
    
    const scene = this.cardManager.drawScene();
    const conflictLine = template.conflict[Math.floor(Math.random() * template.conflict.length)];
    
    return {
      description: this._interpolateTemplate(conflictLine, scene),
      scene,
      choices: this._generateChoices(scene)
    };
  }

  /**
   * 生成高潮
   */
  generateClimax() {
    const template = this.themeLoader.getStoryTemplate();
    if (!template || !template.climax) {
      return '高潮来临...';
    }
    
    const scene = this.cardManager.drawScene();
    const climaxLine = template.climax[Math.floor(Math.random() * template.climax.length)];
    
    return this._interpolateTemplate(climaxLine, scene);
  }

  /**
   * 生成结局
   */
  generateResolution() {
    const template = this.themeLoader.getStoryTemplate();
    const ending = this.cardManager.drawEnding();
    
    if (!template || !template.resolution) {
      return ending || '故事结束了...';
    }
    
    const resolutionLine = template.resolution[Math.floor(Math.random() * template.resolution.length)];
    
    return {
      description: resolutionLine,
      ending: ending
    };
  }

  /**
   * 生成完整三幕结构故事
   */
  generateFullStory() {
    return {
      opening: this.generateOpening(),
      conflicts: [
        this.generateConflict(),
        this.generateConflict()
      ],
      climax: this.generateClimax(),
      resolution: this.generateResolution()
    };
  }

  /**
   * 模板插值
   */
  _interpolateTemplate(template, scene) {
    let result = template;
    
    // 替换常见占位符
    if (scene.character) {
      result = result.replace(/\{角色\}/g, scene.character);
      result = result.replace(/\{character\}/gi, scene.character);
    }
    if (scene.location) {
      result = result.replace(/\{地点\}/g, scene.location);
      result = result.replace(/\{location\}/gi, scene.location);
    }
    if (scene.item) {
      result = result.replace(/\{物品\}/g, scene.item);
      result = result.replace(/\{item\}/gi, scene.item);
    }
    
    return result;
  }

  /**
   * 生成选择项
   */
  _generateChoices(scene) {
    const theme = this.themeLoader.getCurrentTheme();
    const choices = [];
    
    // 基于场景生成选择
    choices.push({
      text: `与${scene.character || '神秘人'}交谈`,
      type: 'social',
      difficulty: 1
    });
    
    choices.push({
      text: `在${scene.location || '附近'}探索`,
      type: 'exploration',
      difficulty: 2
    });
    
    if (scene.item) {
      choices.push({
        text: `使用${scene.item}`,
        type: 'action',
        difficulty: 2
      });
    }
    
    // 根据主题添加特殊选择
    if (theme?.id === 'cthulhu') {
      choices.push({
        text: '进行理智判定',
        type: 'sanity',
        difficulty: 3
      });
    } else if (theme?.id === 'xianxia') {
      choices.push({
        text: '尝试突破境界',
        type: 'cultivation',
        difficulty: 3
      });
    }
    
    return choices;
  }
}

// ============================================================================
// 画风标签管理器
// ============================================================================

class ArtStyleManager {
  constructor(themeLoader) {
    this.themeLoader = themeLoader;
    this.activeTags = new Set();
  }

  /**
   * 获取当前主题的画风
   */
  getCurrentArtStyle() {
    const config = this.themeLoader.getArtStyleConfig();
    return config?.primaryStyle || '默认';
  }

  /**
   * 获取颜色方案
   */
  getColorScheme() {
    const config = this.themeLoader.getArtStyleConfig();
    return config?.colorScheme || {};
  }

  /**
   * 添加活跃标签
   */
  addActiveTag(tag) {
    this.activeTags.add(tag);
  }

  /**
   * 移除活跃标签
   */
  removeActiveTag(tag) {
    this.activeTags.delete(tag);
  }

  /**
   * 获取所有活跃标签
   */
  getActiveTags() {
    return Array.from(this.activeTags);
  }

  /**
   * 清除所有活跃标签
   */
  clearActiveTags() {
    this.activeTags.clear();
  }

  /**
   * 获取场景类型标签
   */
  getSceneTypeTags(sceneType) {
    return ART_STYLE_TAGS.sceneTypes[sceneType] || [];
  }

  /**
   * 获取角色原型标签
   */
  getCharacterArchetypeTags(archetype) {
    return ART_STYLE_TAGS.characterArchetypes[archetype] || [];
  }

  /**
   * 生成画风描述
   */
  generateArtStyleDescription() {
    const theme = this.themeLoader.getCurrentTheme();
    const config = this.themeLoader.getArtStyleConfig();
    
    if (!theme || !config) {
      return '默认风格';
    }
    
    const parts = [
      `主风格: ${config.primaryStyle}`,
      `氛围: ${config.atmosphere}`,
      `标签: ${config.tags.join(', ')}`
    ];
    
    if (this.activeTags.size > 0) {
      parts.push(`活跃元素: ${Array.from(this.activeTags).join(', ')}`);
    }
    
    return parts.join(' | ');
  }

  /**
   * 获取推荐的视觉元素
   */
  getRecommendedVisualElements() {
    const theme = this.themeLoader.getCurrentTheme();
    const config = this.themeLoader.getArtStyleConfig();
    
    if (!theme || !config) {
      return [];
    }
    
    const elements = [];
    
    // 基于主题添加推荐元素
    elements.push({
      type: 'color',
      value: config.colorScheme.primary,
      usage: '主色调'
    });
    
    elements.push({
      type: 'color',
      value: config.colorScheme.accent,
      usage: '强调色'
    });
    
    // 添加主题特色元素
    switch (theme.id) {
      case 'wuxia':
        elements.push(
          { type: 'texture', value: '水墨', usage: '背景纹理' },
          { type: 'font', value: '书法', usage: '标题字体' }
        );
        break;
      case 'xianxia':
        elements.push(
          { type: 'effect', value: '流光', usage: '特效' },
          { type: 'texture', value: '云雾', usage: '氛围' }
        );
        break;
      case 'cthulhu':
        elements.push(
          { type: 'filter', value: '暗角', usage: '氛围' },
          { type: 'effect', value: '扭曲', usage: '理智影响' }
        );
        break;
      case 'cyberpunk':
        elements.push(
          { type: 'effect', value: '霓虹', usage: '灯光' },
          { type: 'texture', value: '电路', usage: '背景元素' }
        );
        break;
      case 'medieval':
        elements.push(
          { type: 'texture', value: '羊皮纸', usage: 'UI背景' },
          { type: 'font', value: '哥特', usage: '标题字体' }
        );
        break;
      case 'republican':
        elements.push(
          { type: 'filter', value: '复古', usage: '整体风格' },
          { type: 'texture', value: '报纸', usage: '背景元素' }
        );
        break;
    }
    
    return elements;
  }
}

// ============================================================================
// 主题系统主类
// ============================================================================

class ThemeSystem {
  constructor() {
    this.themeLoader = new ThemeLoader();
    this.cardManager = new ThemeCardManager(this.themeLoader);
    this.storyGenerator = new ThemeStoryGenerator(this.themeLoader, this.cardManager);
    this.artStyleManager = new ArtStyleManager(this.themeLoader);
    
    this.initialized = false;
  }

  /**
   * 初始化主题系统
   */
  initialize(themeId = 'wuxia') {
    if (this.themeLoader.loadTheme(themeId)) {
      this.initialized = true;
      return {
        success: true,
        theme: this.themeLoader.getCurrentTheme(),
        availableCards: this.cardManager.getRemainingCards()
      };
    }
    return {
      success: false,
      error: `无法加载主题: ${themeId}`
    };
  }

  /**
   * 切换主题
   */
  switchTheme(themeId) {
    const oldTheme = this.themeLoader.getCurrentTheme();
    
    if (this.themeLoader.loadTheme(themeId)) {
      this.cardManager.reset();
      this.artStyleManager.clearActiveTags();
      
      return {
        success: true,
        previousTheme: oldTheme,
        currentTheme: this.themeLoader.getCurrentTheme()
      };
    }
    
    return {
      success: false,
      error: `无法切换到主题: ${themeId}`
    };
  }

  /**
   * 获取所有可用主题
   */
  getAvailableThemes() {
    return this.themeLoader.listThemes();
  }

  /**
   * 获取当前主题信息
   */
  getCurrentThemeInfo() {
    return {
      theme: this.themeLoader.getCurrentTheme(),
      artStyle: this.artStyleManager.getCurrentArtStyle(),
      colorScheme: this.artStyleManager.getColorScheme(),
      artStyleDescription: this.artStyleManager.generateArtStyleDescription()
    };
  }

  /**
   * 抽取卡牌
   */
  drawCards(type, count = 1) {
    return this.cardManager.drawCard(type, count);
  }

  /**
   * 抽取场景
   */
  drawScene() {
    return this.cardManager.drawScene();
  }

  /**
   * 生成故事
   */
  generateStory() {
    return this.storyGenerator.generateFullStory();
  }

  /**
   * 生成开场
   */
  generateOpening() {
    return this.storyGenerator.generateOpening();
  }

  /**
   * 生成冲突
   */
  generateConflict() {
    return this.storyGenerator.generateConflict();
  }

  /**
   * 生成高潮
   */
  generateClimax() {
    return this.storyGenerator.generateClimax();
  }

  /**
   * 生成结局
   */
  generateResolution() {
    return this.storyGenerator.generateResolution();
  }

  /**
   * 获取主题规则
   */
  getThemeRules() {
    return this.cardManager.getRules();
  }

  /**
   * 获取地图规则
   */
  getMapRules() {
    return this.cardManager.getMapRules();
  }

  /**
   * 获取画风推荐
   */
  getArtStyleRecommendations() {
    return this.artStyleManager.getRecommendedVisualElements();
  }

  /**
   * 设置活跃画风标签
   */
  setActiveArtTags(tags) {
    this.artStyleManager.clearActiveTags();
    tags.forEach(tag => this.artStyleManager.addActiveTag(tag));
  }

  /**
   * 注册自定义主题
   */
  registerCustomTheme(themeId, themeConfig) {
    return this.themeLoader.registerCustomTheme(themeId, themeConfig);
  }

  /**
   * 重置卡牌池
   */
  resetCardPool() {
    this.cardManager.reset();
  }

  /**
   * 获取剩余卡牌统计
   */
  getCardPoolStats() {
    return this.cardManager.getRemainingCards();
  }

  /**
   * 导出主题配置
   */
  exportThemeConfig() {
    return {
      currentTheme: this.themeLoader.getCurrentTheme(),
      cardLibrary: this.themeLoader.getCardLibrary(),
      storyTemplate: this.themeLoader.getStoryTemplate(),
      artStyleConfig: this.themeLoader.getArtStyleConfig()
    };
  }

  /**
   * 生成主题报告
   */
  generateThemeReport() {
    const theme = this.themeLoader.getCurrentTheme();
    const cardStats = this.cardManager.getRemainingCards();
    const artStyle = this.artStyleManager.generateArtStyleDescription();
    
    return {
      themeName: theme?.name || '未加载',
      themeStyle: theme?.style || '未知',
      themeDescription: theme?.description || '无描述',
      artStyle: artStyle,
      cardPoolStats: cardStats,
      activeTags: this.artStyleManager.getActiveTags(),
      themeRules: this.getThemeRules(),
      mapRules: this.getMapRules()
    };
  }
}

// ============================================================================
// 导出
// ============================================================================

module.exports = {
  ThemeSystem,
  ThemeLoader,
  ThemeCardManager,
  ThemeStoryGenerator,
  ArtStyleManager,
  THEMES,
  THEME_CARD_LIBRARIES,
  THEME_STORY_TEMPLATES,
  ART_STYLE_TAGS
};
