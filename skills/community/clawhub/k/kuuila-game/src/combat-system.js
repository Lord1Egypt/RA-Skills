/**
 * CombatSystem - 万智牌风格战斗系统 v2.5
 * 支持费用/攻击/防御卡牌、行动点系统、回血机制
 */

const { ActPhase } = require('./turn-manager');

/**
 * 卡牌类型
 */
const CombatCardType = {
    CREATURE: 'creature',    // 生物卡（可攻击/防御）
    SPELL: 'spell',          // 法术卡（一次性效果）
    EQUIPMENT: 'equipment',  // 装备卡（增益效果）
    BOSS: 'boss'             // Boss专属卡
};

/**
 * 攻击模式
 */
const AttackMode = {
    SINGLE: 'single',        // 单体攻击
    AOE: 'aoe',              // 群体攻击
    RANDOM: 'random'         // 随机攻击
};

/**
 * 战斗卡牌类
 */
class CombatCard {
    constructor(data) {
        this.id = data.id || `card_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        this.name = data.name;
        this.type = data.type || CombatCardType.CREATURE;
        this.description = data.description || '';
        
        // 万智牌风格数值
        this.cost = data.cost || 0;          // 费用（血量）
        this.attack = data.attack || 0;      // 攻击力
        this.defense = data.defense || 0;    // 防御力
        
        // 特殊能力
        this.abilities = data.abilities || [];
        this.attackMode = data.attackMode || AttackMode.SINGLE;
        
        // 等级（用于小怪）
        this.level = data.level || 1;
        
        // 状态
        this.isExhausted = false;      // 是否已行动
        this.isTapped = false;         // 是否横置
        this.bonusAttack = 0;          // 攻击加成
        this.bonusDefense = 0;         // 防御加成
        this.hp = this.defense;        // 当前血量
        
        // 来源标记
        this.isMinion = data.isMinion || false;  // 是否为小怪
        this.isBossCard = data.isBossCard || false; // 是否为Boss卡
    }

    /**
     * 获取总攻击力
     */
    getTotalAttack() {
        return this.attack + this.bonusAttack;
    }

    /**
     * 获取总防御力
     */
    getTotalDefense() {
        return this.defense + this.bonusDefense;
    }

    /**
     * 受到伤害
     */
    takeDamage(damage) {
        this.hp -= damage;
        return this.hp <= 0;
    }

    /**
     * 重置回合状态
     */
    resetTurn() {
        this.isExhausted = false;
        this.isTapped = false;
        this.hp = this.getTotalDefense();
    }

    /**
     * 序列化
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            type: this.type,
            description: this.description,
            cost: this.cost,
            attack: this.attack,
            defense: this.defense,
            level: this.level,
            abilities: this.abilities,
            attackMode: this.attackMode,
            isExhausted: this.isExhausted,
            isTapped: this.isTapped,
            hp: this.hp,
            totalAttack: this.getTotalAttack(),
            totalDefense: this.getTotalDefense(),
            isMinion: this.isMinion,
            isBossCard: this.isBossCard
        };
    }
}

/**
 * 战斗单位（玩家或敌人）
 */
class CombatUnit {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.isPlayer = data.isPlayer || false;
        
        // 血量系统（血和货币共用）
        this.maxHp = data.maxHp || 10;
        this.hp = data.hp || this.maxHp;
        
        // 手牌
        this.hand = [];
        this.maxHandSize = data.maxHandSize || 7;
        
        // 战场
        this.battlefield = [];
        this.maxBattlefieldSize = data.maxBattlefieldSize || 5;
        
        // 行动点
        this.actionPoints = 0;
        this.maxActionPoints = data.maxActionPoints || 3;
        
        // 统计
        this.kills = 0;
        this.damageDealt = 0;
        this.damageTaken = 0;
        
        // AI控制
        this.isAI = data.isAI || false;
        this.aiStrategy = data.aiStrategy || 'balanced';
    }

    /**
     * 抽卡
     */
    drawCard(card) {
        if (this.hand.length < this.maxHandSize) {
            this.hand.push(card);
            return true;
        }
        return false;
    }

    /**
     * 打出卡牌
     */
    playCard(cardIndex) {
        if (cardIndex < 0 || cardIndex >= this.hand.length) {
            return null;
        }
        return this.hand.splice(cardIndex, 1)[0];
    }

    /**
     * 召唤到战场
     */
    summon(card) {
        if (this.battlefield.length < this.maxBattlefieldSize) {
            card.resetTurn();
            this.battlefield.push(card);
            return true;
        }
        return false;
    }

    /**
     * 从战场移除
     */
    removeFromBattlefield(cardId) {
        const index = this.battlefield.findIndex(c => c.id === cardId);
        if (index >= 0) {
            return this.battlefield.splice(index, 1)[0];
        }
        return null;
    }

    /**
     * 受到伤害
     */
    takeDamage(damage) {
        this.hp -= damage;
        this.damageTaken += damage;
        return this.hp <= 0;
    }

    /**
     * 治疗
     */
    heal(amount) {
        const oldHp = this.hp;
        this.hp = Math.min(this.hp + amount, this.maxHp);
        return this.hp - oldHp;
    }

    /**
     * 支付血量（作为货币）
     */
    payBlood(amount) {
        if (this.hp > amount) {
            this.hp -= amount;
            return true;
        }
        return false;
    }

    /**
     * 重置回合
     */
    resetTurn() {
        this.battlefield.forEach(card => card.resetTurn());
        this.actionPoints = this.maxActionPoints;
    }

    /**
     * 获取可行动的卡牌
     */
    getAvailableCards() {
        return this.battlefield.filter(card => !card.isExhausted && !card.isTapped);
    }

    /**
     * 序列化
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            isPlayer: this.isPlayer,
            hp: this.hp,
            maxHp: this.maxHp,
            handSize: this.hand.length,
            hand: this.hand.map(c => c.toJSON()),
            battlefield: this.battlefield.map(c => c.toJSON()),
            actionPoints: this.actionPoints,
            maxActionPoints: this.maxActionPoints,
            kills: this.kills,
            damageDealt: this.damageDealt,
            damageTaken: this.damageTaken
        };
    }
}

/**
 * 小怪生成器
 */
class MinionGenerator {
    constructor() {
        // 小怪模板库
        this.minionTemplates = [
            // 1-3级小怪（第一幕）
            { level: 1, name: '小喽啰', attack: 1, defense: 1, cost: 1 },
            { level: 1, name: '迷雾精灵', attack: 0, defense: 2, cost: 1, abilities: ['taunt'] },
            { level: 2, name: '山贼', attack: 2, defense: 1, cost: 2 },
            { level: 2, name: '流浪剑客', attack: 1, defense: 2, cost: 2 },
            { level: 2, name: '毒蛇', attack: 3, defense: 1, cost: 2, abilities: ['poison'] },
            { level: 3, name: '黑衣刺客', attack: 3, defense: 2, cost: 3 },
            { level: 3, name: '铁甲卫士', attack: 2, defense: 3, cost: 3, abilities: ['taunt'] },
            { level: 3, name: '火焰精灵', attack: 2, defense: 2, cost: 3, attackMode: AttackMode.AOE },
            
            // 4-6级小怪（第二幕）
            { level: 4, name: '影武者', attack: 4, defense: 3, cost: 4 },
            { level: 4, name: '狂战士', attack: 5, defense: 2, cost: 4, abilities: ['berserk'] },
            { level: 4, name: '冰霜巨人', attack: 3, defense: 4, cost: 4, abilities: ['freeze'] },
            { level: 5, name: '暗夜猎手', attack: 5, defense: 3, cost: 5, abilities: ['stealth'] },
            { level: 5, name: '雷霆战神', attack: 4, defense: 4, cost: 5, attackMode: AttackMode.AOE },
            { level: 5, name: '血族亲王', attack: 4, defense: 3, cost: 5, abilities: ['lifesteal'] },
            { level: 6, name: '深渊领主', attack: 6, defense: 5, cost: 6 },
            { level: 6, name: '天火法师', attack: 5, defense: 4, cost: 6, attackMode: AttackMode.AOE },
            { level: 6, name: '不朽守护者', attack: 4, defense: 6, cost: 6, abilities: ['taunt', 'divine_shield'] }
        ];
    }

    /**
     * 根据等级范围生成小怪
     */
    generateMinion(levelRange = { min: 1, max: 3 }) {
        const candidates = this.minionTemplates.filter(
            t => t.level >= levelRange.min && t.level <= levelRange.max
        );

        if (candidates.length === 0) {
            return null;
        }

        const template = candidates[Math.floor(Math.random() * candidates.length)];
        
        return new CombatCard({
            ...template,
            type: CombatCardType.CREATURE,
            isMinion: true
        });
    }

    /**
     * 批量生成小怪
     */
    generateMinions(count, levelRange = { min: 1, max: 3 }) {
        const minions = [];
        for (let i = 0; i < count; i++) {
            const minion = this.generateMinion(levelRange);
            if (minion) {
                minions.push(minion);
            }
        }
        return minions;
    }
}

/**
 * 卡组构建器
 */
class DeckBuilder {
    constructor() {
        // 基础卡牌库
        this.cardPool = [
            // 低费卡牌（1-2费）
            { name: '轻骑兵', cost: 1, attack: 2, defense: 1 },
            { name: '盾卫', cost: 1, attack: 1, defense: 2, abilities: ['taunt'] },
            { name: '斥候', cost: 1, attack: 1, defense: 1, abilities: ['charge'] },
            { name: '剑士', cost: 2, attack: 2, defense: 2 },
            { name: '弓箭手', cost: 2, attack: 3, defense: 1 },
            { name: '医师', cost: 2, attack: 1, defense: 1, abilities: ['heal'] },
            
            // 中费卡牌（3-4费）
            { name: '骑士', cost: 3, attack: 3, defense: 3, abilities: ['charge'] },
            { name: '法师', cost: 3, attack: 4, defense: 2, attackMode: AttackMode.AOE },
            { name: '圣骑', cost: 3, attack: 2, defense: 3, abilities: ['divine_shield'] },
            { name: '刺客', cost: 4, attack: 5, defense: 2, abilities: ['stealth'] },
            { name: '龙骑士', cost: 4, attack: 4, defense: 4 },
            { name: '暗影法师', cost: 4, attack: 3, defense: 3, attackMode: AttackMode.AOE },
            
            // 高费卡牌（5-6费）
            { name: '狂龙', cost: 5, attack: 6, defense: 4, abilities: ['berserk'] },
            { name: '天使', cost: 5, attack: 4, defense: 5, abilities: ['divine_shield', 'lifesteal'] },
            { name: '泰坦', cost: 6, attack: 5, defense: 6, abilities: ['taunt'] },
            { name: '末日审判', cost: 6, attack: 8, defense: 3, attackMode: AttackMode.AOE }
        ];
    }

    /**
     * 构建玩家卡组
     */
    buildPlayerDeck(cardCount = 30) {
        const deck = [];
        
        for (let i = 0; i < cardCount; i++) {
            const template = this.cardPool[Math.floor(Math.random() * this.cardPool.length)];
            const card = new CombatCard({
                ...template,
                type: CombatCardType.CREATURE
            });
            deck.push(card);
        }

        return deck;
    }
}

/**
 * 战斗系统核心
 */
class CombatSystem {
    constructor(config = {}) {
        this.config = {
            // 初始血量（血和货币共用）
            startingHp: config.startingHp || 10,
            
            // 行动点
            maxActionPoints: config.maxActionPoints || 3,
            
            // 战场限制
            maxBattlefieldSize: config.maxBattlefieldSize || 5,
            maxHandSize: config.maxHandSize || 7,
            
            // 回血机制
            actionPointHealing: config.actionPointHealing || true,
            
            // 初始手牌数
            startingHandSize: config.startingHandSize || 3
        };

        // 战斗单位
        this.players = [];
        this.enemies = [];
        
        // 卡组
        this.playerDeck = [];
        this.enemyDeck = [];
        
        // 小怪生成器
        this.minionGenerator = new MinionGenerator();
        this.deckBuilder = new DeckBuilder();
        
        // 战斗状态
        this.turn = 0;
        this.currentPhase = ActPhase.PROLOGUE;
        this.isPlayerTurn = true;
        this.combatLog = [];
        
        // 回调
        this.callbacks = {
            onCombatStart: null,
            onCombatEnd: null,
            onTurnStart: null,
            onTurnEnd: null,
            onCardPlay: null,
            onAttack: null,
            onDeath: null
        };
    }

    /**
     * 设置回调
     */
    setCallbacks(callbacks) {
        Object.assign(this.callbacks, callbacks);
    }

    /**
     * 初始化战斗
     */
    initCombat(playerCount = 1, actPhase = ActPhase.PROLOGUE) {
        this.currentPhase = actPhase;
        this.turn = 0;
        this.combatLog = [];

        // 创建玩家
        this.players = [];
        for (let i = 0; i < playerCount; i++) {
            const player = new CombatUnit({
                id: `player_${i}`,
                name: `玩家${i + 1}`,
                isPlayer: true,
                maxHp: this.config.startingHp,
                maxActionPoints: this.config.maxActionPoints,
                maxBattlefieldSize: this.config.maxBattlefieldSize,
                maxHandSize: this.config.maxHandSize
            });
            this.players.push(player);
        }

        // 构建玩家卡组
        this.playerDeck = this.deckBuilder.buildPlayerDeck();

        // 玩家抽初始手牌
        this.players.forEach(player => {
            for (let i = 0; i < this.config.startingHandSize; i++) {
                const card = this.playerDeck.pop();
                if (card) {
                    player.drawCard(card);
                }
            }
        });

        // 根据幕生成敌人
        this._generateEnemiesForPhase(playerCount);

        this._log('战斗初始化完成', { playerCount, phase: actPhase });

        if (this.callbacks.onCombatStart) {
            this.callbacks.onCombatStart({
                players: this.players.map(p => p.toJSON()),
                enemies: this.enemies.map(e => e.toJSON()),
                phase: actPhase
            });
        }

        return {
            success: true,
            players: this.players.map(p => p.toJSON()),
            enemies: this.enemies.map(e => e.toJSON())
        };
    }

    /**
     * 根据幕生成敌人
     */
    _generateEnemiesForPhase(playerCount) {
        this.enemies = [];
        
        let levelRange;
        let enemyCount;
        
        switch (this.currentPhase) {
            case ActPhase.PROLOGUE:
                levelRange = { min: 1, max: 3 };
                enemyCount = Math.floor(Math.random() * 2) + 1; // 1-2个小怪
                break;
            case ActPhase.CONFLICT:
                levelRange = { min: 4, max: 6 };
                enemyCount = Math.floor(Math.random() * 3) + 2; // 2-4个小怪
                break;
            case ActPhase.CLIMAX:
                levelRange = { min: 4, max: 6 };
                enemyCount = playerCount; // Boss战：按玩家人数生成
                break;
            default:
                levelRange = { min: 1, max: 3 };
                enemyCount = 1;
        }

        // 生成敌人单位
        for (let i = 0; i < enemyCount; i++) {
            const enemy = new CombatUnit({
                id: `enemy_${i}`,
                name: `敌人${i + 1}`,
                isPlayer: false,
                maxHp: this.config.startingHp,
                maxActionPoints: this.config.maxActionPoints,
                isAI: true
            });
            
            // 生成小怪卡牌
            const minion = this.minionGenerator.generateMinion(levelRange);
            if (minion) {
                enemy.summon(minion);
                enemy.name = minion.name;
            }
            
            this.enemies.push(enemy);
        }

        this._log(`为${this.currentPhase}幕生成${enemyCount}个敌人`, { levelRange });
    }

    /**
     * 开始玩家回合
     */
    startPlayerTurn(playerIndex = 0) {
        if (playerIndex >= this.players.length) {
            return { success: false, error: '玩家不存在' };
        }

        const player = this.players[playerIndex];
        player.resetTurn();
        this.turn++;
        this.isPlayerTurn = true;

        // 抽一张牌
        if (this.playerDeck.length > 0 && player.hand.length < player.maxHandSize) {
            const card = this.playerDeck.pop();
            player.drawCard(card);
            this._log(`${player.name}抽了一张牌`, { card: card.name });
        }

        this._log(`${player.name}回合开始`, {
            turn: this.turn,
            actionPoints: player.actionPoints,
            handSize: player.hand.length,
            battlefieldSize: player.battlefield.length
        });

        if (this.callbacks.onTurnStart) {
            this.callbacks.onTurnStart({
                turn: this.turn,
                player: player.toJSON(),
                isPlayerTurn: true
            });
        }

        return {
            success: true,
            turn: this.turn,
            player: player.toJSON()
        };
    }

    /**
     * 打出卡牌
     */
    playCard(playerIndex, cardIndex, targetId = null) {
        const player = this.players[playerIndex];
        if (!player) {
            return { success: false, error: '玩家不存在' };
        }

        const card = player.hand[cardIndex];
        if (!card) {
            return { success: false, error: '卡牌不存在' };
        }

        // 检查行动点
        if (player.actionPoints <= 0) {
            return { success: false, error: '行动点不足' };
        }

        // 检查战场空间
        if (player.battlefield.length >= player.maxBattlefieldSize) {
            return { success: false, error: '战场已满' };
        }

        // 支付费用（血量）
        if (!player.payBlood(card.cost)) {
            return { success: false, error: `血量不足，需要${card.cost}点` };
        }

        // 移除手牌并召唤到战场
        const playedCard = player.playCard(cardIndex);
        player.summon(playedCard);
        player.actionPoints--;

        this._log(`${player.name}打出${playedCard.name}`, {
            cost: playedCard.cost,
            attack: playedCard.getTotalAttack(),
            defense: playedCard.getTotalDefense(),
            playerHp: player.hp
        });

        if (this.callbacks.onCardPlay) {
            this.callbacks.onCardPlay({
                player: player.toJSON(),
                card: playedCard.toJSON(),
                cost: playedCard.cost
            });
        }

        return {
            success: true,
            card: playedCard.toJSON(),
            player: player.toJSON()
        };
    }

    /**
     * 攻击
     */
    attack(playerIndex, attackerCardId, targetId) {
        const player = this.players[playerIndex];
        if (!player) {
            return { success: false, error: '玩家不存在' };
        }

        const attacker = player.battlefield.find(c => c.id === attackerCardId);
        if (!attacker) {
            return { success: false, error: '攻击卡不存在' };
        }

        if (attacker.isExhausted) {
            return { success: false, error: '该单位已行动' };
        }

        if (player.actionPoints <= 0) {
            return { success: false, error: '行动点不足' };
        }

        // 查找目标
        let targets = [];
        const attackMode = attacker.attackMode;

        if (attackMode === AttackMode.AOE) {
            // 群体攻击
            targets = this.enemies.filter(e => e.battlefield.length > 0 || e.hp > 0);
        } else if (attackMode === AttackMode.RANDOM) {
            // 随机攻击
            const validEnemies = this.enemies.filter(e => e.battlefield.length > 0 || e.hp > 0);
            if (validEnemies.length > 0) {
                targets = [validEnemies[Math.floor(Math.random() * validEnemies.length)]];
            }
        } else {
            // 单体攻击
            const enemy = this.enemies.find(e => e.id === targetId);
            if (enemy) {
                targets = [enemy];
            }
        }

        if (targets.length === 0) {
            return { success: false, error: '没有有效目标' };
        }

        // 执行攻击
        const results = [];
        targets.forEach(target => {
            const result = this._executeAttack(player, attacker, target);
            results.push(result);
        });

        attacker.isExhausted = true;
        player.actionPoints--;

        this._log(`${player.name}的${attacker.name}发起攻击`, {
            attackMode,
            targets: targets.map(t => t.name),
            results
        });

        if (this.callbacks.onAttack) {
            this.callbacks.onAttack({
                player: player.toJSON(),
                attacker: attacker.toJSON(),
                targets: targets.map(t => t.toJSON()),
                results
            });
        }

        return {
            success: true,
            attackMode,
            results
        };
    }

    /**
     * 执行攻击逻辑
     */
    _executeAttack(attacker, attackCard, target) {
        const result = {
            targetId: target.id,
            targetName: target.name,
            damageDealt: 0,
            killed: false
        };

        // 优先攻击战场上的随从
        if (target.battlefield.length > 0) {
            const defender = target.battlefield[0];
            const damage = attackCard.getTotalAttack();
            
            const isDead = defender.takeDamage(damage);
            result.damageDealt = damage;
            result.defender = defender.name;

            if (isDead) {
                target.removeFromBattlefield(defender.id);
                result.killed = true;
                attacker.kills++;
                
                this._log(`${defender.name}被击败`, { killer: attacker.name });
                
                if (this.callbacks.onDeath) {
                    this.callbacks.onDeath({
                        unit: defender.toJSON(),
                        killer: attacker.toJSON()
                    });
                }
            }
        } else {
            // 直接攻击玩家
            const damage = attackCard.getTotalAttack();
            const isDead = target.takeDamage(damage);
            
            result.damageDealt = damage;
            result.killed = isDead;
            attacker.damageDealt += damage;

            this._log(`${target.name}受到${damage}点伤害`, {
                remainingHp: target.hp,
                isDead
            });
        }

        return result;
    }

    /**
     * 结束玩家回合（应用回血机制）
     */
    endPlayerTurn(playerIndex = 0) {
        const player = this.players[playerIndex];
        if (!player) {
            return { success: false, error: '玩家不存在' };
        }

        // 回血机制：未使用行动点÷2
        let healing = 0;
        if (this.config.actionPointHealing && player.actionPoints > 0) {
            healing = Math.floor(player.actionPoints / 2);
            if (healing > 0) {
                const healed = player.heal(healing);
                this._log(`${player.name}通过休息回复${healed}点血量`, {
                    unusedActionPoints: player.actionPoints,
                    healing: healed
                });
            }
        }

        this._log(`${player.name}回合结束`, {
            healing,
            finalHp: player.hp,
            battlefieldSize: player.battlefield.length
        });

        if (this.callbacks.onTurnEnd) {
            this.callbacks.onTurnEnd({
                turn: this.turn,
                player: player.toJSON(),
                healing
            });
        }

        return {
            success: true,
            healing,
            player: player.toJSON()
        };
    }

    /**
     * 收复小怪
     */
    captureMinion(playerIndex, enemyIndex) {
        const player = this.players[playerIndex];
        const enemy = this.enemies[enemyIndex];

        if (!player || !enemy) {
            return { success: false, error: '目标不存在' };
        }

        if (enemy.battlefield.length === 0) {
            return { success: false, error: '该敌人没有小怪' };
        }

        const minion = enemy.battlefield[0];
        const captureCost = minion.cost;

        // 支付血量收复
        if (!player.payBlood(captureCost)) {
            return { success: false, error: `血量不足，需要${captureCost}点` };
        }

        // 移除敌人战场，加入玩家手牌
        enemy.removeFromBattlefield(minion.id);
        minion.isMinion = false; // 不再是小怪
        player.drawCard(minion);

        this._log(`${player.name}收复了${minion.name}`, {
            cost: captureCost,
            playerHp: player.hp
        });

        return {
            success: true,
            minion: minion.toJSON(),
            cost: captureCost,
            player: player.toJSON()
        };
    }

    /**
     * 敌人回合
     */
    enemyTurn() {
        this.isPlayerTurn = false;
        const actions = [];

        this.enemies.forEach(enemy => {
            if (enemy.hp <= 0) return;

            enemy.resetTurn();
            
            // AI决策
            const action = this._enemyAI(enemy);
            actions.push(action);

            this._log(`敌人${enemy.name}回合`, action);
        });

        // 检查战斗结束
        const combatStatus = this.checkCombatEnd();

        return {
            success: true,
            actions,
            combatStatus
        };
    }

    /**
     * 敌人AI决策
     */
    _enemyAI(enemy) {
        const action = {
            enemyId: enemy.id,
            enemyName: enemy.name,
            type: 'attack',
            targets: []
        };

        // 找到可行动的单位
        const availableCards = enemy.getAvailableCards();
        
        if (availableCards.length > 0) {
            const attacker = availableCards[0];
            const attackMode = attacker.attackMode;

            // 选择目标
            const validPlayers = this.players.filter(p => p.hp > 0 && (p.battlefield.length > 0 || p.hp > 0));
            
            if (validPlayers.length > 0) {
                let targets = [];
                
                if (attackMode === AttackMode.AOE) {
                    targets = validPlayers;
                } else if (attackMode === AttackMode.RANDOM) {
                    targets = [validPlayers[Math.floor(Math.random() * validPlayers.length)]];
                } else {
                    // 优先攻击血量最少的玩家
                    targets = [validPlayers.sort((a, b) => a.hp - b.hp)[0]];
                }

                targets.forEach(target => {
                    const result = this._executeAttack(enemy, attacker, target);
                    action.targets.push(result);
                });

                attacker.isExhausted = true;
                enemy.actionPoints--;
            }
        }

        return action;
    }

    /**
     * 检查战斗结束
     */
    checkCombatEnd() {
        const alivePlayers = this.players.filter(p => p.hp > 0);
        const aliveEnemies = this.enemies.filter(e => e.hp > 0 || e.battlefield.length > 0);

        if (alivePlayers.length === 0) {
            return {
                ended: true,
                winner: 'enemy',
                message: '玩家全军覆没'
            };
        }

        if (aliveEnemies.length === 0) {
            return {
                ended: true,
                winner: 'player',
                message: '敌人被消灭'
            };
        }

        return {
            ended: false,
            alivePlayers: alivePlayers.length,
            aliveEnemies: aliveEnemies.length
        };
    }

    /**
     * 获取战斗状态
     */
    getCombatState() {
        return {
            turn: this.turn,
            phase: this.currentPhase,
            isPlayerTurn: this.isPlayerTurn,
            players: this.players.map(p => p.toJSON()),
            enemies: this.enemies.map(e => e.toJSON()),
            deckSize: this.playerDeck.length,
            combatLog: this.combatLog.slice(-20)
        };
    }

    /**
     * 记录日志
     */
    _log(message, data = {}) {
        const logEntry = {
            turn: this.turn,
            timestamp: Date.now(),
            message,
            ...data
        };
        this.combatLog.push(logEntry);
    }

    /**
     * 重置战斗系统
     */
    reset() {
        this.players = [];
        this.enemies = [];
        this.playerDeck = [];
        this.enemyDeck = [];
        this.turn = 0;
        this.isPlayerTurn = true;
        this.combatLog = [];
        this.currentPhase = ActPhase.PROLOGUE;

        return { success: true, message: '战斗系统已重置' };
    }
}

module.exports = {
    CombatSystem,
    CombatCard,
    CombatUnit,
    CombatCardType,
    AttackMode,
    MinionGenerator,
    DeckBuilder
};
