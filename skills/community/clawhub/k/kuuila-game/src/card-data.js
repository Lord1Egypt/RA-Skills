/**
 * Card Data - 卡牌数据模块
 * 基于脑洞起爆表数据
 * 数据源: data/game-design-source.json
 */

// 基础卡库 - 角色 (14种)
const ROLES = [
    { id: 'role_1', type: 'Role', name: '胖老头', description: '一位年迈的胖老人' },
    { id: 'role_2', type: 'Role', name: '小孩', description: '天真无邪的孩子' },
    { id: 'role_3', type: 'Role', name: '巨人', description: '身材高大的巨人' },
    { id: 'role_4', type: 'Role', name: '贼', description: '身手敏捷的小偷' },
    { id: 'role_5', type: 'Role', name: '敌人', description: '危险的敌对者' },
    { id: 'role_6', type: 'Role', name: '兄弟/姐妹', description: '血脉相连的亲人' },
    { id: 'role_7', type: 'Role', name: '孤儿', description: '无依无靠的孩子' },
    { id: 'role_8', type: 'Role', name: '怪物', description: '神秘可怕的怪物' },
    { id: 'role_9', type: 'Role', name: '丈夫/妻子', description: '人生伴侣' },
    { id: 'role_10', type: 'Role', name: '乞丐', description: '流浪街头的乞丐' },
    { id: 'role_11', type: 'Role', name: '继母', description: '复杂的家庭关系' },
    { id: 'role_12', type: 'Role', name: '鸟', description: '会飞的神秘生物' },
    { id: 'role_13', type: 'Role', name: '父母', description: '慈爱的双亲' },
    { id: 'role_14', type: 'Role', name: '厨师', description: '精通美食的大厨' }
];

// 基础卡库 - 地点 (12种)
const LOCATIONS = [
    { id: 'loc_1', type: 'Location', name: '岛', description: '与世隔绝的岛屿' },
    { id: 'loc_2', type: 'Location', name: '塔', description: '高耸入云的塔楼' },
    { id: 'loc_3', type: 'Location', name: '河流', description: '奔流不息的河流' },
    { id: 'loc_4', type: 'Location', name: '厨房', description: '烹饪美食的地方' },
    { id: 'loc_5', type: 'Location', name: '森林', description: '神秘幽暗的森林' },
    { id: 'loc_6', type: 'Location', name: '家', description: '温馨的住所' },
    { id: 'loc_7', type: 'Location', name: '夜里', description: '黑暗笼罩的时刻' },
    { id: 'loc_8', type: 'Location', name: '教堂', description: '神圣庄严的教堂' },
    { id: 'loc_9', type: 'Location', name: '楼梯', description: '通向上方的阶梯' },
    { id: 'loc_10', type: 'Location', name: '农舍', description: '田园风格的农舍' },
    { id: 'loc_11', type: 'Location', name: '监狱', description: '囚禁之地' },
    { id: 'loc_12', type: 'Location', name: '路', description: '延伸远方的道路' }
];

// 基础卡库 - 物品 (13种)
const ITEMS = [
    { id: 'item_1', type: 'Item', name: '药', description: '能治病的药物' },
    { id: 'item_2', type: 'Item', name: '斧头', description: '锋利的武器' },
    { id: 'item_3', type: 'Item', name: '红酒', description: '美味的饮品' },
    { id: 'item_4', type: 'Item', name: '礼物', description: '赠予的物品' },
    { id: 'item_5', type: 'Item', name: '门', description: '通往未知的入口' },
    { id: 'item_6', type: 'Item', name: '食物', description: '充饥的粮食' },
    { id: 'item_7', type: 'Item', name: '钥匙', description: '开启秘密的钥匙' },
    { id: 'item_8', type: 'Item', name: '火', description: '温暖与危险的火焰' },
    { id: 'item_9', type: 'Item', name: '书', description: '记载知识的书本' },
    { id: 'item_10', type: 'Item', name: '树', description: '参天大树' },
    { id: 'item_11', type: 'Item', name: '戒指', description: '象征承诺的戒指' },
    { id: 'item_12', type: 'Item', name: '窗', description: '眺望外界的窗户' },
    { id: 'item_13', type: 'Item', name: '船', description: '航行的工具' }
];

// 基础卡库 - 状态 (20种)
const STATES = [
    { id: 'state_1', type: 'State', name: '失窃', description: '某物被盗走' },
    { id: 'state_2', type: 'State', name: '丑', description: '令人厌恶的外表' },
    { id: 'state_3', type: 'State', name: '疯', description: '失去理智的状态' },
    { id: 'state_4', type: 'State', name: '中毒', description: '身中剧毒' },
    { id: 'state_5', type: 'State', name: '秘密', description: '隐藏的真相' },
    { id: 'state_6', type: 'State', name: '隐藏', description: '无法被发现' },
    { id: 'state_7', type: 'State', name: '美丽', description: '令人着迷的美貌' },
    { id: 'state_8', type: 'State', name: '害怕', description: '恐惧笼罩' },
    { id: 'state_9', type: 'State', name: '遥远', description: '触不可及' },
    { id: 'state_10', type: 'State', name: '彪悍', description: '强壮威猛' },
    { id: 'state_11', type: 'State', name: '微小', description: '渺小不起眼' },
    { id: 'state_12', type: 'State', name: '高兴', description: '愉悦的心情' },
    { id: 'state_13', type: 'State', name: '愚蠢', description: '不够聪明' },
    { id: 'state_14', type: 'State', name: '伪装', description: '掩饰真实面貌' },
    { id: 'state_15', type: 'State', name: '这个会飞', description: '拥有飞行的能力' },
    { id: 'state_16', type: 'State', name: '这个物品会说话', description: '物品具有灵性' },
    { id: 'state_17', type: 'State', name: '邪恶', description: '内心邪恶' },
    { id: 'state_18', type: 'State', name: '盲', description: '失去视觉' },
    { id: 'state_19', type: 'State', name: '幸运', description: '命运眷顾' },
    { id: 'state_20', type: 'State', name: '睡眠', description: '沉睡不醒' }
];

// 基础卡库 - 事件 (20种)
const EVENTS = [
    { id: 'event_1', type: 'Event', name: '某物坏了', description: '物品损坏' },
    { id: 'event_2', type: 'Event', name: '很冰冷的', description: '寒冷刺骨' },
    { id: 'event_3', type: 'Event', name: '很久不见', description: '久别重逢' },
    { id: 'event_4', type: 'Event', name: '被击倒', description: '被打败' },
    { id: 'event_5', type: 'Event', name: '相遇', description: '命中注定的邂逅' },
    { id: 'event_6', type: 'Event', name: '决斗', description: '生死对决' },
    { id: 'event_7', type: 'Event', name: '变形', description: '形态改变' },
    { id: 'event_8', type: 'Event', name: '梦', description: '梦境中的经历' },
    { id: 'event_9', type: 'Event', name: '比赛', description: '竞技较量' },
    { id: 'event_10', type: 'Event', name: '两人相爱', description: '爱情萌芽' },
    { id: 'event_11', type: 'Event', name: '某人受伤', description: '受伤流血' },
    { id: 'event_12', type: 'Event', name: '风暴', description: '狂风暴雨' },
    { id: 'event_13', type: 'Event', name: '计划', description: '筹划中的行动' },
    { id: 'event_14', type: 'Event', name: '陷阱', description: '危险的陷阱' },
    { id: 'event_15', type: 'Event', name: '分开组队', description: '团队分散' },
    { id: 'event_16', type: 'Event', name: '逃跑', description: '逃离危险' },
    { id: 'event_17', type: 'Event', name: '追逐', description: '追逐战' },
    { id: 'event_18', type: 'Event', name: '死亡', description: '生命的终结' },
    { id: 'event_19', type: 'Event', name: '某事昭显', description: '真相大白' },
    { id: 'event_20', type: 'Event', name: '毁灭', description: '彻底的破坏' }
];

// 通用结局 (32种)
const ENDINGS = [
    { id: 'end_1', type: 'Ending', name: '她们踏破铁蹄也无法再次找到它', description: '永远失落' },
    { id: 'end_2', type: 'Ending', name: '从那以后，它开始听从母亲的建议', description: '成长的代价' },
    { id: 'end_3', type: 'Ending', name: '据我所知 她们仍然在跳舞', description: '永恒的舞步' },
    { id: 'end_4', type: 'Ending', name: '他们换了地方 一切回复正常', description: '回归平静' },
    { id: 'end_5', type: 'Ending', name: '她和她的家人重新团聚', description: '家庭团聚' },
    { id: 'end_6', type: 'Ending', name: '他们把它还给了它的主人', description: '物归原主' },
    { id: 'end_7', type: 'Ending', name: '他原谅了他，两人结婚了', description: '和解与婚姻' },
    { id: 'end_8', type: 'Ending', name: '他们承诺再不打斗了', description: '和平誓言' },
    { id: 'end_9', type: 'Ending', name: '但她仍然不时地去拜访他们', description: '持续的牵挂' },
    { id: 'end_10', type: 'Ending', name: '他们从追捕者手中逃脱 回到了家', description: '安全归家' },
    { id: 'end_11', type: 'Ending', name: '她停止了受伤 重拾笑颜', description: '治愈' },
    { id: 'end_12', type: 'Ending', name: '一切都重放光彩', description: '恢复美好' },
    { id: 'end_13', type: 'Ending', name: '她总是戴着它 以提醒自己', description: '永恒的纪念' },
    { id: 'end_14', type: 'Ending', name: '他们坐在那里 直到这一天的到来', description: '漫长的等待' },
    { id: 'end_15', type: 'Ending', name: '当它去时 犹如来时之神秘', description: '神秘的离去' },
    { id: 'end_16', type: 'Ending', name: '它不再合适了', description: '时光流逝' },
    { id: 'end_17', type: 'Ending', name: '这对父母与他们失散多年的孩子重逢', description: '血脉重逢' },
    { id: 'end_18', type: 'Ending', name: '她表明了她的真实身份 两人结为夫妻', description: '身份揭露' },
    { id: 'end_19', type: 'Ending', name: '直到今日也没有人知道她跑到哪里去了', description: '永远的谜' },
    { id: 'end_20', type: 'Ending', name: '他们一直照顾他 直到她长大', description: '抚养成人' },
    { id: 'end_21', type: 'Ending', name: '他拾起他的武器，继续前进', description: '继续征程' },
    { id: 'end_22', type: 'Ending', name: '破晓来临 他门看到一切完好', description: '黎明新生' },
    { id: 'end_23', type: 'Ending', name: '对手死后 最终他们结婚了', description: '胜利与爱情' },
    { id: 'end_24', type: 'Ending', name: '她再也不让它离开它的视线半步', description: '永不分离' },
    { id: 'end_25', type: 'Ending', name: '他意识到他的兄弟是多么忠诚', description: '忠诚的证明' },
    { id: 'end_26', type: 'Ending', name: '这个故事证明了 一颗纯洁的心可以战胜一切', description: '纯洁的力量' },
    { id: 'end_27', type: 'Ending', name: '这个故事证明了 每个人都愿意当注意他的同伴', description: '同伴的情谊' },
    { id: 'end_28', type: 'Ending', name: '预言实现了', description: '命运的兑现' },
    { id: 'end_29', type: 'Ending', name: '他和他的家人 重新团聚', description: '家庭重聚' },
    { id: 'end_30', type: 'Ending', name: '他们活在自己 邪恶与欺骗的阴影中 度过余生', description: '黑暗的余生' },
    { id: 'end_31', type: 'Ending', name: '在她的有生之年 它都永远不会消失', description: '永恒的印记' },
    { id: 'end_32', type: 'Ending', name: '他们感谢曾经拯救了他们的所有人的英雄', description: '感恩英雄' }
];

// 武侠词条 (18种)
const WUXIA_TERMS = [
    { id: 'wuxia_1', type: 'Role', theme: '武侠', name: '复仇之人', description: '背负血海深仇的侠客' },
    { id: 'wuxia_2', type: 'Role', theme: '武侠', name: '退伍士兵', description: '卸甲归田的老兵' },
    { id: 'wuxia_3', type: 'Role', theme: '武侠', name: '执刑人', description: '执行死刑的刽子手' },
    { id: 'wuxia_4', type: 'Role', theme: '武侠', name: '刺客', description: '暗杀为业的杀手' },
    { id: 'wuxia_5', type: 'Role', theme: '武侠', name: '车夫', description: '驾车的平凡人' },
    { id: 'wuxia_6', type: 'Role', theme: '武侠', name: '道士', description: '修行道法的方士' },
    { id: 'wuxia_7', type: 'Role', theme: '武侠', name: '猎人', description: '狩猎为生的猎人' },
    { id: 'wuxia_8', type: 'Role', theme: '武侠', name: '农场主', description: '拥有土地的富户' },
    { id: 'wuxia_9', type: 'Role', theme: '武侠', name: '侠客', description: '行走江湖的侠士' },
    { id: 'wuxia_10', type: 'Role', theme: '武侠', name: '皇帝', description: '一国之君' },
    { id: 'wuxia_11', type: 'Role', theme: '武侠', name: '僧侣', description: '出家修行的僧人' },
    { id: 'wuxia_12', type: 'Location', theme: '武侠', name: '码头', description: '船只停靠之地' },
    { id: 'wuxia_13', type: 'Location', theme: '武侠', name: '竹林', description: '翠竹成林的幽静之地' },
    { id: 'wuxia_14', type: 'Location', theme: '武侠', name: '宫殿', description: '帝王居住的地方' },
    { id: 'wuxia_15', type: 'Location', theme: '武侠', name: '寺庙', description: '供奉神佛的场所' },
    { id: 'wuxia_16', type: 'Item', theme: '武侠', name: '断剑', description: '断了一半的剑' },
    { id: 'wuxia_17', type: 'Item', theme: '武侠', name: '佛珠', description: '佛教念珠' },
    { id: 'wuxia_18', type: 'Item', theme: '武侠', name: '账本', description: '记录账目的本子' }
];

// 克苏鲁词条 (26种)
const CTHULHU_TERMS = [
    { id: 'cthulhu_1', type: 'Role', theme: '克苏鲁', name: '医生', description: '救死扶伤的医者' },
    { id: 'cthulhu_2', type: 'Role', theme: '克苏鲁', name: '保姆', description: '照顾孩子的人' },
    { id: 'cthulhu_3', type: 'Role', theme: '克苏鲁', name: '镇长', description: '小镇的管理者' },
    { id: 'cthulhu_4', type: 'Role', theme: '克苏鲁', name: '治安官', description: '维护治安的官员' },
    { id: 'cthulhu_5', type: 'Role', theme: '克苏鲁', name: '伐木工', description: '砍伐树木的工人' },
    { id: 'cthulhu_6', type: 'Role', theme: '克苏鲁', name: '管理员', description: '管理事务的人' },
    { id: 'cthulhu_7', type: 'Role', theme: '克苏鲁', name: '侦探', description: '调查真相的人' },
    { id: 'cthulhu_8', type: 'Role', theme: '克苏鲁', name: '盗贼', description: '偷盗为生的人' },
    { id: 'cthulhu_9', type: 'Role', theme: '克苏鲁', name: '法官', description: '审判案件的人' },
    { id: 'cthulhu_10', type: 'Role', theme: '克苏鲁', name: '记者', description: '新闻报道者' },
    { id: 'cthulhu_11', type: 'Role', theme: '克苏鲁', name: '牧师', description: '宗教人士' },
    { id: 'cthulhu_12', type: 'Role', theme: '克苏鲁', name: '食尸鬼', description: '食腐的怪物' },
    { id: 'cthulhu_13', type: 'Role', theme: '克苏鲁', name: '深潜者', description: '水中的怪物' },
    { id: 'cthulhu_14', type: 'Role', theme: '克苏鲁', name: '巨型海怪', description: '巨大的海洋生物' },
    { id: 'cthulhu_15', type: 'Role', theme: '克苏鲁', name: '猎犬', description: '追猎的狗' },
    { id: 'cthulhu_16', type: 'Location', theme: '克苏鲁', name: '诊所', description: '看病的地方' },
    { id: 'cthulhu_17', type: 'Location', theme: '克苏鲁', name: '温泉旅馆', description: '休息的场所' },
    { id: 'cthulhu_18', type: 'Location', theme: '克苏鲁', name: '农庄', description: '乡间农场' },
    { id: 'cthulhu_19', type: 'Location', theme: '克苏鲁', name: '度假村', description: '度假胜地' },
    { id: 'cthulhu_20', type: 'Location', theme: '克苏鲁', name: '仓库', description: '存放物品的地方' },
    { id: 'cthulhu_21', type: 'Location', theme: '克苏鲁', name: '学校', description: '学习的地方' },
    { id: 'cthulhu_22', type: 'Item', theme: '克苏鲁', name: '枪', description: '致命的武器' },
    { id: 'cthulhu_23', type: 'Item', theme: '克苏鲁', name: '细针', description: '细长的针' },
    { id: 'cthulhu_24', type: 'Item', theme: '克苏鲁', name: '阵法', description: '神秘法阵' },
    { id: 'cthulhu_25', type: 'Item', theme: '克苏鲁', name: '旧神遗物', description: '古老神器的碎片' },
    { id: 'cthulhu_26', type: 'State', theme: '克苏鲁', name: '陷入疯狂', description: '理智崩溃' }
];

// 卡牌类型枚举
const CardType = {
    ROLE: 'Role',
    LOCATION: 'Location',
    ITEM: 'Item',
    STATE: 'State',
    EVENT: 'Event',
    ENDING: 'Ending'
};

// 主题枚举
const Theme = {
    BASE: 'base',       // 基础卡库
    WUXIA: 'wuxia',     // 武侠
    CTHULHU: 'cthulhu'  // 克苏鲁
};

// 获取所有基础卡牌
function getAllBaseCards() {
    return [
        ...ROLES,
        ...LOCATIONS,
        ...ITEMS,
        ...STATES,
        ...EVENTS
    ];
}

// 获取所有结局卡牌
function getAllEndings() {
    return [...ENDINGS];
}

// 获取所有卡牌（包括主题卡）
function getAllCards() {
    return [
        ...getAllBaseCards(),
        ...getAllEndings(),
        ...WUXIA_TERMS,
        ...CTHULHU_TERMS
    ];
}

// 按类型获取卡牌
function getCardsByType(type) {
    // 为基础卡牌添加默认主题
    const addTheme = (cards, theme) => cards.map(c => ({ ...c, theme: c.theme || theme }));
    
    switch (type) {
        case CardType.ROLE:
            return [
                ...addTheme(ROLES, Theme.BASE),
                ...WUXIA_TERMS.filter(c => c.type === 'Role'),
                ...CTHULHU_TERMS.filter(c => c.type === 'Role')
            ];
        case CardType.LOCATION:
            return [
                ...addTheme(LOCATIONS, Theme.BASE),
                ...WUXIA_TERMS.filter(c => c.type === 'Location'),
                ...CTHULHU_TERMS.filter(c => c.type === 'Location')
            ];
        case CardType.ITEM:
            return [
                ...addTheme(ITEMS, Theme.BASE),
                ...WUXIA_TERMS.filter(c => c.type === 'Item'),
                ...CTHULHU_TERMS.filter(c => c.type === 'Item')
            ];
        case CardType.STATE:
            return [
                ...addTheme(STATES, Theme.BASE),
                ...CTHULHU_TERMS.filter(c => c.type === 'State')
            ];
        case CardType.EVENT:
            return [...addTheme(EVENTS, Theme.BASE)];
        case CardType.ENDING:
            return [...addTheme(ENDINGS, Theme.BASE)];
        default:
            return getAllCards();
    }
}

// 按主题获取卡牌
function getCardsByTheme(theme) {
    switch (theme) {
        case Theme.BASE:
            return getAllBaseCards();
        case Theme.WUXIA:
            return WUXIA_TERMS;
        case Theme.CTHULHU:
            return CTHULHU_TERMS;
        default:
            return getAllCards();
    }
}

// 导出
module.exports = {
    // 卡牌数据
    ROLES,
    LOCATIONS,
    ITEMS,
    STATES,
    EVENTS,
    ENDINGS,
    WUXIA_TERMS,
    CTHULHU_TERMS,
    
    // 枚举
    CardType,
    Theme,
    
    // 工具函数
    getAllBaseCards,
    getAllEndings,
    getAllCards,
    getCardsByType,
    getCardsByTheme
};
