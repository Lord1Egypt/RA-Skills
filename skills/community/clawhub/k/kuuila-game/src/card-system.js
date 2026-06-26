/**
 * Card System - 卡牌系统
 * 基于脑洞起爆表数据
 * 支持抽卡、洗牌、组合等功能
 */

const {
    ROLES,
    LOCATIONS,
    ITEMS,
    STATES,
    EVENTS,
    ENDINGS,
    WUXIA_TERMS,
    CTHULHU_TERMS,
    CardType,
    Theme,
    getAllBaseCards,
    getAllEndings,
    getAllCards,
    getCardsByType,
    getCardsByTheme
} = require('./card-data');

/**
 * 卡牌类 - 单张卡牌
 */
class Card {
    constructor(data) {
        this.id = data.id;
        this.type = data.type;
        this.name = data.name;
        this.description = data.description || '';
        this.theme = data.theme || Theme.BASE;
    }

    toString() {
        return `【${this.type}】${this.name}`;
    }

    toJSON() {
        return {
            id: this.id,
            type: this.type,
            name: this.name,
            description: this.description,
            theme: this.theme
        };
    }
}

/**
 * 卡组类 - 管理一组卡牌
 */
class Deck {
    constructor(name = '未命名卡组') {
        this.name = name;
        this.cards = [];
        this.discardPile = [];
    }

    // 添加卡牌
    addCard(card) {
        this.cards.push(card instanceof Card ? card : new Card(card));
        return this;
    }

    // 批量添加卡牌
    addCards(cards) {
        cards.forEach(card => this.addCard(card));
        return this;
    }

    // 洗牌 (Fisher-Yates算法)
    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
        return this;
    }

    // 抽一张牌
    draw() {
        if (this.cards.length === 0) {
            return null;
        }
        const card = this.cards.pop();
        this.discardPile.push(card);
        return card;
    }

    // 抽多张牌
    drawMultiple(count) {
        const drawn = [];
        for (let i = 0; i < count && this.cards.length > 0; i++) {
            drawn.push(this.draw());
        }
        return drawn;
    }

    // 查看顶部N张牌（不抽走）
    peek(count = 1) {
        return this.cards.slice(-count).reverse();
    }

    // 重新洗入弃牌堆
    reshuffleDiscards() {
        this.cards = [...this.cards, ...this.discardPile];
        this.discardPile = [];
        this.shuffle();
        return this;
    }

    // 获取剩余卡牌数
    get remainingCount() {
        return this.cards.length;
    }

    // 获取弃牌堆数量
    get discardCount() {
        return this.discardPile.length;
    }
}

/**
 * 卡牌系统 - 核心类
 */
class CardSystem {
    constructor() {
        this.decks = new Map();  // 存储多个卡组
        this.hand = [];          // 当前手牌
        this.combinations = [];  // 已组合的卡牌
        
        // 初始化默认卡组
        this._initDefaultDecks();
    }

    // 初始化默认卡组
    _initDefaultDecks() {
        // 基础角色卡组
        const roleDeck = new Deck('角色卡组');
        roleDeck.addCards(ROLES.map(r => ({ ...r, theme: Theme.BASE })));
        this.decks.set('role', roleDeck);

        // 地点卡组
        const locationDeck = new Deck('地点卡组');
        locationDeck.addCards(LOCATIONS.map(l => ({ ...l, theme: Theme.BASE })));
        this.decks.set('location', locationDeck);

        // 物品卡组
        const itemDeck = new Deck('物品卡组');
        itemDeck.addCards(ITEMS.map(i => ({ ...i, theme: Theme.BASE })));
        this.decks.set('item', itemDeck);

        // 状态卡组
        const stateDeck = new Deck('状态卡组');
        stateDeck.addCards(STATES.map(s => ({ ...s, theme: Theme.BASE })));
        this.decks.set('state', stateDeck);

        // 事件卡组
        const eventDeck = new Deck('事件卡组');
        eventDeck.addCards(EVENTS.map(e => ({ ...e, theme: Theme.BASE })));
        this.decks.set('event', eventDeck);

        // 结局卡组
        const endingDeck = new Deck('结局卡组');
        endingDeck.addCards(ENDINGS.map(e => ({ ...e, theme: Theme.BASE })));
        this.decks.set('ending', endingDeck);

        // 武侠主题卡组
        const wuxiaDeck = new Deck('武侠卡组');
        wuxiaDeck.addCards(WUXIA_TERMS);
        this.decks.set('wuxia', wuxiaDeck);

        // 克苏鲁主题卡组
        const cthulhuDeck = new Deck('克苏鲁卡组');
        cthulhuDeck.addCards(CTHULHU_TERMS);
        this.decks.set('cthulhu', cthulhuDeck);

        // 全卡组
        const allDeck = new Deck('全部卡牌');
        allDeck.addCards(getAllCards());
        this.decks.set('all', allDeck);
    }

    // 获取卡组
    getDeck(deckName) {
        return this.decks.get(deckName);
    }

    // 列出所有卡组
    listDecks() {
        const deckList = [];
        for (const [name, deck] of this.decks) {
            deckList.push({
                name,
                displayName: deck.name,
                remaining: deck.cards.length,
                discarded: deck.discardPile.length
            });
        }
        return deckList;
    }

    // 从指定卡组抽一张牌
    draw(deckName = 'all') {
        const deck = this.decks.get(deckName);
        if (!deck) {
            return { error: `卡组 "${deckName}" 不存在` };
        }
        
        const card = deck.draw();
        if (!card) {
            return { error: '卡组已空', deckName };
        }
        
        this.hand.push(card);
        return {
            success: true,
            card,
            handCount: this.hand.length
        };
    }

    // 抽多张牌
    drawMultiple(deckName = 'all', count = 3) {
        const deck = this.decks.get(deckName);
        if (!deck) {
            return { error: `卡组 "${deckName}" 不存在` };
        }

        const cards = deck.drawMultiple(count);
        this.hand.push(...cards);
        
        return {
            success: true,
            cards,
            drawnCount: cards.length,
            handCount: this.hand.length
        };
    }

    // 随机抽卡（不限卡组）
    drawRandom(types = [], count = 1) {
        const result = [];
        
        for (let i = 0; i < count; i++) {
            if (types.length > 0) {
                // 从指定类型中随机抽取
                const randomType = types[Math.floor(Math.random() * types.length)];
                const deckName = this._typeToDeckName(randomType);
                const deck = this.decks.get(deckName);
                
                if (deck && deck.remainingCount > 0) {
                    const card = deck.draw();
                    this.hand.push(card);
                    result.push(card);
                }
            } else {
                // 从全卡组中抽取
                const deck = this.decks.get('all');
                if (deck && deck.remainingCount > 0) {
                    const card = deck.draw();
                    this.hand.push(card);
                    result.push(card);
                }
            }
        }

        return {
            success: true,
            cards: result,
            handCount: this.hand.length
        };
    }

    // 类型转卡组名
    _typeToDeckName(type) {
        const typeMap = {
            [CardType.ROLE]: 'role',
            [CardType.LOCATION]: 'location',
            [CardType.ITEM]: 'item',
            [CardType.STATE]: 'state',
            [CardType.EVENT]: 'event',
            [CardType.ENDING]: 'ending'
        };
        return typeMap[type] || 'all';
    }

    // 洗牌
    shuffle(deckName = 'all') {
        const deck = this.decks.get(deckName);
        if (!deck) {
            return { error: `卡组 "${deckName}" 不存在` };
        }
        
        deck.shuffle();
        return {
            success: true,
            message: `已洗牌: ${deck.name}`,
            remaining: deck.remainingCount
        };
    }

    // 重新洗入弃牌
    reshuffleDiscards(deckName = 'all') {
        const deck = this.decks.get(deckName);
        if (!deck) {
            return { error: `卡组 "${deckName}" 不存在` };
        }
        
        deck.reshuffleDiscards();
        return {
            success: true,
            message: `已将弃牌堆重新洗入`,
            remaining: deck.remainingCount
        };
    }

    // 查看手牌
    showHand() {
        return {
            count: this.hand.length,
            cards: this.hand.map(c => c.toJSON())
        };
    }

    // 打出手牌
    playCard(cardIndex) {
        if (cardIndex < 0 || cardIndex >= this.hand.length) {
            return { error: '无效的卡牌索引' };
        }
        
        const card = this.hand.splice(cardIndex, 1)[0];
        return {
            success: true,
            card,
            message: `打出了: ${card.toString()}`,
            handCount: this.hand.length
        };
    }

    // 清空手牌
    clearHand() {
        const count = this.hand.length;
        this.hand = [];
        return {
            success: true,
            message: `已清空手牌 (${count}张)`
        };
    }

    // 组合卡牌 - 生成故事元素
    combine(cardIndices = []) {
        if (cardIndices.length === 0) {
            // 默认组合：角色+地点+事件
            return this._generateStoryElement(['Role', 'Location', 'Event']);
        }

        const cards = cardIndices
            .map(idx => this.hand[idx])
            .filter(c => c !== undefined);

        if (cards.length === 0) {
            return { error: '没有有效的卡牌' };
        }

        const combination = {
            cards: cards.map(c => c.toJSON()),
            story: this._generateStoryFromCards(cards)
        };

        this.combinations.push(combination);
        return combination;
    }

    // 生成故事元素
    _generateStoryElement(types) {
        const elements = {};
        
        for (const type of types) {
            const deckName = this._typeToDeckName(type);
            const deck = this.decks.get(deckName);
            
            if (deck && deck.remainingCount > 0) {
                const card = deck.draw();
                elements[type.toLowerCase()] = card.toJSON();
            }
        }

        return {
            success: true,
            elements,
            story: this._generateStoryFromElements(elements)
        };
    }

    // 从卡牌生成故事
    _generateStoryFromCards(cards) {
        const parts = cards.map(c => c.name);
        return `故事元素: ${parts.join(' → ')}`;
    }

    // 从元素生成故事
    _generateStoryFromElements(elements) {
        const parts = [];
        if (elements.role) parts.push(`主角是${elements.role.name}`);
        if (elements.location) parts.push(`身处${elements.location.name}`);
        if (elements.item) parts.push(`持有${elements.item.name}`);
        if (elements.state) parts.push(`处于${elements.state.name}状态`);
        if (elements.event) parts.push(`遭遇${elements.event.name}`);
        if (elements.ending) parts.push(`最终${elements.ending.name}`);
        
        return parts.join('，') + '。';
    }

    // 创建自定义卡组
    createCustomDeck(name, cardTypes = [], theme = null) {
        let cards = [];
        
        if (cardTypes.length > 0) {
            cardTypes.forEach(type => {
                // 使用类型筛选基础卡牌
                const typeCards = getCardsByType(type);
                cards = [...cards, ...typeCards];
            });
        } else {
            cards = getAllCards();
        }

        if (theme) {
            cards = cards.filter(c => c.theme === theme);
        }

        const deck = new Deck(name);
        deck.addCards(cards);
        deck.shuffle();
        
        this.decks.set(name, deck);
        
        return {
            success: true,
            deckName: name,
            cardCount: deck.cards.length
        };
    }

    // 获取游戏启动配置
    getGameSetup(playerCount = 1, theme = Theme.BASE) {
        const setup = {
            theme,
            playerCount,
            decks: {},
            startingHand: []
        };

        // 根据主题配置卡组
        const themeDecks = {
            [Theme.BASE]: ['role', 'location', 'item', 'state', 'event', 'ending'],
            [Theme.WUXIA]: ['wuxia', 'role', 'location', 'item', 'event', 'ending'],
            [Theme.CTHULHU]: ['cthulhu', 'role', 'location', 'item', 'state', 'event']
        };

        const deckNames = themeDecks[theme] || themeDecks[Theme.BASE];
        
        // 重置并洗牌
        deckNames.forEach(name => {
            const deck = this.decks.get(name);
            if (deck) {
                deck.reshuffleDiscards();
                deck.shuffle();
                setup.decks[name] = {
                    name: deck.name,
                    count: deck.remainingCount
                };
            }
        });

        // 每位玩家抽初始手牌
        for (let i = 0; i < playerCount; i++) {
            // 角色1张 + 地点1张 + 物品1张 + 状态1张
            const hand = [];
            
            const roleDeck = this.decks.get(deckNames.includes('wuxia') ? 'wuxia' : 'role');
            const locDeck = this.decks.get('location');
            const itemDeck = this.decks.get('item');
            const stateDeck = this.decks.get('state');

            if (roleDeck) hand.push(roleDeck.draw());
            if (locDeck) hand.push(locDeck.draw());
            if (itemDeck) hand.push(itemDeck.draw());
            if (stateDeck) hand.push(stateDeck.draw());

            setup.startingHand.push({
                player: i + 1,
                cards: hand.map(c => c.toJSON())
            });
        }

        return setup;
    }

    // 统计信息
    getStats() {
        const stats = {
            decks: this.listDecks(),
            handCount: this.hand.length,
            combinationsCount: this.combinations.length,
            totalCards: getAllCards().length
        };

        // 按类型统计
        stats.byType = {
            roles: ROLES.length + WUXIA_TERMS.filter(c => c.type === 'Role').length + CTHULHU_TERMS.filter(c => c.type === 'Role').length,
            locations: LOCATIONS.length + WUXIA_TERMS.filter(c => c.type === 'Location').length + CTHULHU_TERMS.filter(c => c.type === 'Location').length,
            items: ITEMS.length + WUXIA_TERMS.filter(c => c.type === 'Item').length + CTHULHU_TERMS.filter(c => c.type === 'Item').length,
            states: STATES.length + CTHULHU_TERMS.filter(c => c.type === 'State').length,
            events: EVENTS.length,
            endings: ENDINGS.length
        };

        // 按主题统计
        stats.byTheme = {
            base: getAllBaseCards().length,
            wuxia: WUXIA_TERMS.length,
            cthulhu: CTHULHU_TERMS.length
        };

        return stats;
    }

    // 重置系统
    reset() {
        // 清空手牌
        this.hand = [];
        this.combinations = [];
        
        // 重新初始化卡组
        this.decks.clear();
        this._initDefaultDecks();
        
        return {
            success: true,
            message: '卡牌系统已重置'
        };
    }
}

// 导出
module.exports = {
    Card,
    Deck,
    CardSystem,
    CardType,
    Theme
};
