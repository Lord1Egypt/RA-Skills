/**
 * BossSystem - Boss战斗系统 v2.5
 * 支持Boss专属卡组、产小怪能力、群攻效果
 */

const { CombatSystem, CombatCard, CombatUnit, CombatCardType, AttackMode } = require('./combat-system');

/**
 * Boss能力类型
 */
const BossAbilityType = {
    SPAWN_MINION: 'spawn_minion',    // 产小怪
    AOE_ATTACK: 'aoe_attack',        // 群体攻击
    HEAL: 'heal',                    // 治疗
    BUFF: 'buff',                     // 增益
    DEBUFF: 'debuff',                // 减益
    STEAL: 'steal',                  // 偷取资源
    SUMMON: 'summon'                 // 召唤特殊单位
};

/**
 * Boss类型
 */
const BossType = {
    DRAGON: 'dragon',                // 龙类
    DEMON: 'demon',                  // 恶魔
    UNDEAD: 'undead',                // 不死族
    ELEMENTAL: 'elemental',          // 元素
    ANCIENT: 'ancient'               // 远古生物
};

/**
 * Boss卡牌类
 */
class BossCard extends CombatCard {
    constructor(data) {
        super({
            ...data,
            type: CombatCardType.BOSS,
            isBossCard: true
        });
        
        // Boss特殊属性
        this.bossType = data.bossType || BossType.ANCIENT;
        this.bossAbilities = data.bossAbilities || [];
        this.spawnMinionCost = data.spawnMinionCost || 2;
        this.spawnMinionLevel = data.spawnMinionLevel || 3;
        this.canSpawnMinions = data.canSpawnMinions !== false;
        
        // Boss独特机制
        this.phase = 1;              // Boss阶段（1-3）
        this.maxPhase = data.maxPhase || 3;
        this.phaseThreshold = data.phaseThreshold || 0.3; // 血量低于30%进入下一阶段
    }

    /**
     * 检查是否需要进入下一阶段
     */
    checkPhaseTransition() {
        const hpPercent = this.hp / this.getTotalDefense();
        
        if (hpPercent <= this.phaseThreshold && this.phase < this.maxPhase) {
            this.phase++;
            return {
                triggered: true,
                newPhase: this.phase,
                message: `${this.name}进入第${this.phase}阶段！`
            };
        }
        
        return { triggered: false };
    }

    /**
     * 获取Boss信息
     */
    toBossJSON() {
        return {
            ...this.toJSON(),
            bossType: this.bossType,
            bossAbilities: this.bossAbilities,
            phase: this.phase,
            maxPhase: this.maxPhase,
            canSpawnMinions: this.canSpawnMinions
        };
    }
}

/**
 * Boss生成器
 */
class BossGenerator {
    constructor() {
        // Boss模板库
        this.bossTemplates = {
            [BossType.DRAGON]: [
                { name: '炎龙帝', attack: 8, defense: 8, cost: 8, level: 6,
                  abilities: ['flight', 'fire_breath'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.BUFF],
                  maxPhase: 3 },
                { name: '冰霜巨龙', attack: 7, defense: 9, cost: 8, level: 6,
                  abilities: ['freeze', 'flight'], attackMode: AttackMode.SINGLE,
                  bossAbilities: [BossAbilityType.HEAL, BossAbilityType.DEBUFF],
                  maxPhase: 3 },
                { name: '雷霆古龙', attack: 9, defense: 7, cost: 8, level: 6,
                  abilities: ['lightning', 'flight'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.SPAWN_MINION],
                  maxPhase: 2 }
            ],
            [BossType.DEMON]: [
                { name: '深渊魔王', attack: 10, defense: 6, cost: 8, level: 6,
                  abilities: ['corruption', 'shadow'], attackMode: AttackMode.SINGLE,
                  bossAbilities: [BossAbilityType.SPAWN_MINION, BossAbilityType.HEAL],
                  maxPhase: 3 },
                { name: '恐惧之王', attack: 8, defense: 7, cost: 8, level: 6,
                  abilities: ['fear', 'nightmare'], attackMode: AttackMode.RANDOM,
                  bossAbilities: [BossAbilityType.DEBUFF, BossAbilityType.STEAL],
                  maxPhase: 3 },
                { name: '血宴主君', attack: 9, defense: 8, cost: 8, level: 6,
                  abilities: ['lifesteal', 'blood_magic'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.HEAL],
                  maxPhase: 2 }
            ],
            [BossType.UNDEAD]: [
                { name: '亡灵之主', attack: 7, defense: 9, cost: 8, level: 6,
                  abilities: ['soul_harvest', 'reanimate'], attackMode: AttackMode.SINGLE,
                  bossAbilities: [BossAbilityType.SPAWN_MINION, BossAbilityType.HEAL],
                  maxPhase: 3 },
                { name: '骸骨皇帝', attack: 8, defense: 8, cost: 8, level: 6,
                  abilities: ['bone_armor', 'command'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.BUFF, BossAbilityType.AOE_ATTACK],
                  maxPhase: 3 },
                { name: '暗影摄政王', attack: 10, defense: 6, cost: 8, level: 6,
                  abilities: ['possession', 'shadow_step'], attackMode: AttackMode.RANDOM,
                  bossAbilities: [BossAbilityType.STEAL, BossAbilityType.DEBUFF],
                  maxPhase: 2 }
            ],
            [BossType.ELEMENTAL]: [
                { name: '元素君主', attack: 9, defense: 7, cost: 8, level: 6,
                  abilities: ['elemental_fusion'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.BUFF],
                  maxPhase: 3 },
                { name: '风暴之主', attack: 10, defense: 5, cost: 8, level: 6,
                  abilities: ['storm', 'lightning'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.DEBUFF],
                  maxPhase: 3 },
                { name: '烈焰元素', attack: 8, defense: 8, cost: 8, level: 6,
                  abilities: ['inferno', 'fire_shield'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.HEAL],
                  maxPhase: 2 }
            ],
            [BossType.ANCIENT]: [
                { name: '远古泰坦', attack: 11, defense: 9, cost: 8, level: 6,
                  abilities: ['earthquake', 'titan_strike'], attackMode: AttackMode.AOE,
                  bossAbilities: [BossAbilityType.AOE_ATTACK, BossAbilityType.BUFF, BossAbilityType.HEAL],
                  maxPhase: 3 },
                { name: '克苏鲁眷属', attack: 9, defense: 8, cost: 8, level: 6,
                  abilities: ['madness', 'cosmic'], attackMode: AttackMode.RANDOM,
                  bossAbilities: [BossAbilityType.DEBUFF, BossAbilityType.SPAWN_MINION],
                  maxPhase: 3 },
                { name: '世界树意志', attack: 7, defense: 10, cost: 8, level: 6,
                  abilities: ['nature_power', 'regrowth'], attackMode: AttackMode.SINGLE,
                  bossAbilities: [BossAbilityType.HEAL, BossAbilityType.BUFF, BossAbilityType.SPAWN_MINION],
                  maxPhase: 3 }
            ]
        };

        // Boss专属卡牌库
        this.bossExclusiveCards = [
            // 强力单体攻击
            { name: '毁灭打击', cost: 4, attack: 10, defense: 0, attackMode: AttackMode.SINGLE },
            { name: '暗影斩', cost: 4, attack: 9, defense: 1, attackMode: AttackMode.SINGLE },
            { name: '雷霆一击', cost: 4, attack: 8, defense: 2, attackMode: AttackMode.SINGLE },
            
            // 群体攻击
            { name: '烈焰风暴', cost: 5, attack: 6, defense: 0, attackMode: AttackMode.AOE },
            { name: '冰封千里', cost: 5, attack: 5, defense: 2, attackMode: AttackMode.AOE },
            { name: '死亡波纹', cost: 6, attack: 7, defense: 0, attackMode: AttackMode.AOE },
            { name: '连环闪电', cost: 5, attack: 5, defense: 1, attackMode: AttackMode.AOE },
            
            // 召唤类
            { name: '恶魔召唤', cost: 5, attack: 5, defense: 4, abilities: ['summon'] },
            { name: '亡灵复苏', cost: 4, attack: 4, defense: 4, abilities: ['reanimate'] },
            { name: '元素集结', cost: 6, attack: 6, defense: 5, abilities: ['elemental_fusion'] },
            
            // 特殊能力
            { name: '恐惧凝视', cost: 3, attack: 3, defense: 2, abilities: ['fear'] },
            { name: '生命虹吸', cost: 4, attack: 4, defense: 2, abilities: ['lifesteal'] },
            { name: '狂暴之力', cost: 3, attack: 2, defense: 2, abilities: ['berserk'] },
            { name: '护盾结界', cost: 2, attack: 0, defense: 5, abilities: ['shield'] },
            { name: '剧毒侵蚀', cost: 3, attack: 3, defense: 1, abilities: ['poison'] }
        ];
    }

    /**
     * 生成随机Boss
     */
    generateBoss(bossType = null, playerCount = 1) {
        // 随机选择Boss类型
        const types = Object.keys(this.bossTemplates);
        const selectedType = bossType || types[Math.floor(Math.random() * types.length)];
        
        const templates = this.bossTemplates[selectedType];
        const template = templates[Math.floor(Math.random() * templates.length)];
        
        // 根据玩家人数调整等级
        const level = Math.max(4, Math.min(6, template.level + Math.floor(playerCount / 2)));
        
        // 创建Boss卡牌
        const bossCard = new BossCard({
            ...template,
            level,
            bossType: selectedType,
            canSpawnMinions: template.bossAbilities.includes(BossAbilityType.SPAWN_MINION)
        });

        return bossCard;
    }

    /**
     * 获取Boss专属卡组
     */
    getBossExclusiveDeck(size = 15) {
        const deck = [];
        
        // 添加Boss专属卡
        for (let i = 0; i < size; i++) {
            const template = this.bossExclusiveCards[Math.floor(Math.random() * this.bossExclusiveCards.length)];
            const card = new CombatCard({
                ...template,
                type: CombatCardType.BOSS,
                isBossCard: true
            });
            deck.push(card);
        }

        return deck;
    }

    /**
     * 获取所有Boss类型
     */
    getAllBossTypes() {
        return Object.entries(this.bossTemplates).map(([type, bosses]) => ({
            type,
            bossCount: bosses.length,
            bosses: bosses.map(b => ({
                name: b.name,
                attack: b.attack,
                defense: b.defense,
                abilities: b.bossAbilities
            }))
        }));
    }
}

/**
 * Boss战斗单位
 */
class BossUnit extends CombatUnit {
    constructor(data) {
        super({
            ...data,
            isPlayer: false,
            isBoss: true
        });

        // Boss特殊属性
        this.bossCard = data.bossCard;
        this.bossType = data.bossType || BossType.ANCIENT;
        this.bossAbilities = data.bossAbilities || [];
        
        // 小怪管理
        this.minionSpawnQueue = [];  // 待生成的小怪队列
        this.activeMinions = [];     // 当前活跃的小怪
        
        // Boss阶段
        this.phase = 1;
        this.maxPhase = data.maxPhase || 3;
        
        // 战斗策略
        this.aiStrategy = data.aiStrategy || 'aggressive';
        
        // 设置Boss卡牌的血量
        if (this.bossCard) {
            this.name = this.bossCard.name;
        }
    }

    /**
     * 添加待生成的小怪
     */
    queueMinionSpawn(level, count = 1) {
        for (let i = 0; i < count; i++) {
            this.minionSpawnQueue.push({ level, ready: true });
        }
    }

    /**
     * 尝试生成小怪
     */
    trySpawnMinion(minionGenerator) {
        if (this.minionSpawnQueue.length > 0 && this.actionPoints >= 2) {
            const spawnInfo = this.minionSpawnQueue.shift();
            const minion = minionGenerator.generateMinion({ min: spawnInfo.level, max: spawnInfo.level });
            
            if (minion) {
                this.activeMinions.push(minion);
                this.actionPoints -= 2; // 产小怪消耗2点
                return {
                    success: true,
                    minion: minion.toJSON(),
                    remainingQueue: this.minionSpawnQueue.length
                };
            }
        }
        
        return { success: false };
    }

    /**
     * 检查阶段转换
     */
    checkPhaseTransition() {
        if (this.bossCard) {
            const result = this.bossCard.checkPhaseTransition();
            if (result.triggered) {
                this.phase = result.newPhase;
                return result;
            }
        }
        return { triggered: false };
    }

    /**
     * 序列化
     */
    toJSON() {
        return {
            ...super.toJSON(),
            isBoss: true,
            bossType: this.bossType,
            bossAbilities: this.bossAbilities,
            phase: this.phase,
            maxPhase: this.maxPhase,
            minionQueueSize: this.minionSpawnQueue.length,
            activeMinions: this.activeMinions.map(m => m.toJSON())
        };
    }
}

/**
 * Boss战斗系统
 */
class BossSystem extends CombatSystem {
    constructor(config = {}) {
        super({
            ...config,
            // Boss战特殊配置
            startingHp: config.startingHp || 15,  // Boss初始血量更高
            maxActionPoints: config.maxActionPoints || 4  // Boss有更多行动点
        });

        this.config = {
            ...this.config,
            // Boss战配置
            bossSpawnCost: config.bossSpawnCost || 3,    // 产小怪消耗
            minMinionLevel: config.minMinionLevel || 3,  // 最小小怪等级
            maxMinionLevel: config.maxMinionLevel || 6,  // 最大小怪等级
            bossDeckSize: config.bossDeckSize || 20      // Boss卡组大小
        };

        // Boss生成器
        this.bossGenerator = new BossGenerator();
        
        // 当前Boss
        this.currentBoss = null;
        
        // Boss战日志
        this.bossLog = [];
    }

    /**
     * 初始化Boss战
     */
    initBossBattle(playerCount = 1, bossType = null) {
        // 调用父类初始化
        this.initCombat(playerCount, 'climax');
        
        // 创建Boss
        const bossCard = this.bossGenerator.generateBoss(bossType, playerCount);
        const bossDeck = this.bossGenerator.getBossExclusiveDeck(this.config.bossDeckSize);
        
        this.currentBoss = new BossUnit({
            id: 'boss',
            name: bossCard.name,
            isPlayer: false,
            isBoss: true,
            maxHp: this.config.startingHp,
            maxActionPoints: this.config.maxActionPoints,
            bossCard: bossCard,
            bossType: bossCard.bossType,
            bossAbilities: bossCard.bossAbilities,
            maxPhase: bossCard.maxPhase,
            aiStrategy: 'aggressive'
        });

        // 将Boss卡牌放入战场
        this.currentBoss.summon(bossCard);
        
        // Boss抽牌
        for (let i = 0; i < 4; i++) {
            const card = bossDeck.pop();
            if (card) {
                this.currentBoss.drawCard(card);
            }
        }

        // 替换敌人
        this.enemies = [this.currentBoss];

        this._logBoss(`Boss战开始！${bossCard.name}出现！`, {
            bossType: bossCard.bossType,
            bossAttack: bossCard.attack,
            bossDefense: bossCard.defense,
            bossAbilities: bossCard.bossAbilities,
            phase: 1,
            playerCount
        });

        if (this.callbacks.onCombatStart) {
            this.callbacks.onCombatStart({
                type: 'boss_battle',
                boss: this.currentBoss.toJSON(),
                players: this.players.map(p => p.toJSON())
            });
        }

        return {
            success: true,
            boss: this.currentBoss.toJSON(),
            players: this.players.map(p => p.toJSON()),
            message: `Boss战开始！${bossCard.name}出现！`
        };
    }

    /**
     * Boss产小怪能力
     */
    bossSpawnMinion(playerCount = 1) {
        if (!this.currentBoss) {
            return { success: false, error: '没有Boss' };
        }

        const bossCard = this.currentBoss.battlefield[0];
        if (!bossCard || !bossCard.canSpawnMinions) {
            return { success: false, error: 'Boss没有产小怪能力' };
        }

        // 根据Boss类型和玩家人数决定生成的小怪等级和数量
        const minionLevel = Math.max(
            this.config.minMinionLevel,
            Math.min(this.config.maxMinionLevel, 4 + Math.floor(playerCount / 2))
        );
        
        const spawnCount = Math.min(2, playerCount); // 最多产2个小怪

        // 生成小怪
        const minions = [];
        for (let i = 0; i < spawnCount; i++) {
            const minion = this.minionGenerator.generateMinion({ min: minionLevel, max: minionLevel });
            if (minion) {
                minion.isMinion = true;
                minions.push(minion);
                
                // 创建小怪战斗单位
                const minionUnit = new CombatUnit({
                    id: `minion_${Date.now()}_${i}`,
                    name: minion.name,
                    isPlayer: false,
                    isMinion: true,
                    maxHp: 5
                });
                minionUnit.summon(minion);
                this.enemies.push(minionUnit);
            }
        }

        this._logBoss(`${this.currentBoss.name}产出了${spawnCount}个${minionLevel}级小怪！`, {
            minions: minions.map(m => m.name),
            level: minionLevel,
            count: spawnCount
        });

        return {
            success: true,
            minions: minions.map(m => m.toJSON()),
            message: `${this.currentBoss.name}产出了${spawnCount}个${minionLevel}级小怪！`
        };
    }

    /**
     * Boss群体攻击
     */
    bossAOEAttack() {
        if (!this.currentBoss) {
            return { success: false, error: '没有Boss' };
        }

        const bossCard = this.currentBoss.battlefield[0];
        if (!bossCard) {
            return { success: false, error: 'Boss不在战场' };
        }

        const damage = bossCard.getTotalAttack();
        const results = [];

        // 攻击所有玩家和他们的随从
        this.players.forEach(player => {
            if (player.hp <= 0) return;

            // 先攻击战场随从
            player.battlefield.forEach(card => {
                const isDead = card.takeDamage(damage);
                results.push({
                    target: card.name,
                    type: 'minion',
                    damage,
                    killed: isDead
                });

                if (isDead) {
                    player.removeFromBattlefield(card.id);
                }
            });

            // 再攻击玩家本体
            const isDead = player.takeDamage(damage);
            results.push({
                target: player.name,
                type: 'player',
                damage,
                killed: isDead
            });
        });

        this.currentBoss.actionPoints -= 2; // 群攻消耗2点

        this._logBoss(`${this.currentBoss.name}发动群体攻击！`, {
            damage,
            targets: results
        });

        return {
            success: true,
            damage,
            results,
            message: `${this.currentBoss.name}发动群体攻击，造成${damage}点伤害！`
        };
    }

    /**
     * Boss回合
     */
    enemyTurn() {
        if (!this.currentBoss) {
            return super.enemyTurn();
        }

        const actions = [];
        
        // Boss重置
        this.currentBoss.resetTurn();
        
        // 决定Boss行动
        const action = this._bossAI();
        actions.push(action);

        this._logBoss(`Boss回合`, action);

        // 检查阶段转换
        const phaseResult = this.currentBoss.checkPhaseTransition();
        if (phaseResult.triggered) {
            this._logBoss(`Boss进入新阶段！`, phaseResult);
            actions.push({ type: 'phase_change', ...phaseResult });
        }

        // 检查战斗结束
        const combatStatus = this.checkCombatEnd();

        if (this.callbacks.onTurnEnd) {
            this.callbacks.onTurnEnd({
                turn: this.turn,
                boss: this.currentBoss.toJSON(),
                actions,
                combatStatus
            });
        }

        return {
            success: true,
            actions,
            combatStatus
        };
    }

    /**
     * Boss AI决策
     */
    _bossAI() {
        const action = {
            type: 'boss_turn',
            bossName: this.currentBoss.name,
            phase: this.currentBoss.phase,
            decisions: []
        };

        const bossCard = this.currentBoss.battlefield[0];
        if (!bossCard) {
            return action;
        }

        // 获取存活的玩家
        const alivePlayers = this.players.filter(p => p.hp > 0);
        if (alivePlayers.length === 0) {
            return action;
        }

        // AI策略
        const strategy = this.currentBoss.aiStrategy;

        // 决定行动
        // 1. 如果可以产小怪且小怪少，产小怪
        if (bossCard.canSpawnMinions && this.currentBoss.actionPoints >= 2) {
            const minionCount = this.enemies.filter(e => e.isMinion).length;
            if (minionCount < 2) {
                const spawnResult = this.bossSpawnMinion(this.players.length);
                if (spawnResult.success) {
                    action.decisions.push({ type: 'spawn_minion', ...spawnResult });
                }
            }
        }

        // 2. 如果有群体攻击能力且行动点足够，使用群体攻击
        if (bossCard.attackMode === AttackMode.AOE && this.currentBoss.actionPoints >= 2) {
            const aoeResult = this.bossAOEAttack();
            if (aoeResult.success) {
                action.decisions.push({ type: 'aoe_attack', ...aoeResult });
            }
        }

        // 3. 使用随从攻击
        const availableMinions = this.currentBoss.getAvailableCards();
        const validTargets = alivePlayers.filter(p => p.battlefield.length > 0 || p.hp > 0);
        
        if (availableMinions.length > 0 && validTargets.length > 0) {
            const attacker = availableMinions[0];
            
            // 优先攻击血量最少的玩家或随从
            let target = null;
            
            // 找随从
            for (const player of validTargets) {
                if (player.battlefield.length > 0) {
                    target = player;
                    break;
                }
            }
            
            // 没有随从则攻击玩家
            if (!target) {
                target = validTargets.sort((a, b) => a.hp - b.hp)[0];
            }

            if (target) {
                const result = this._executeAttack(this.currentBoss, attacker, target);
                attacker.isExhausted = true;
                this.currentBoss.actionPoints--;
                
                action.decisions.push({
                    type: 'minion_attack',
                    attacker: attacker.name,
                    target: target.name,
                    result
                });
            }
        }

        // 4. Boss本体攻击
        if (!bossCard.isExhausted && this.currentBoss.actionPoints >= 1) {
            const target = validTargets.sort((a, b) => a.hp - b.hp)[0];
            if (target) {
                const result = this._executeAttack(this.currentBoss, bossCard, target);
                bossCard.isExhausted = true;
                this.currentBoss.actionPoints--;
                
                action.decisions.push({
                    type: 'boss_attack',
                    attacker: bossCard.name,
                    target: target.name,
                    result
                });
            }
        }

        return action;
    }

    /**
     * 获取Boss战状态
     */
    getBossState() {
        return {
            ...this.getCombatState(),
            boss: this.currentBoss ? this.currentBoss.toJSON() : null,
            bossLog: this.bossLog.slice(-20)
        };
    }

    /**
     * Boss战日志
     */
    _logBoss(message, data = {}) {
        const logEntry = {
            turn: this.turn,
            timestamp: Date.now(),
            message,
            ...data
        };
        this.bossLog.push(logEntry);
        this.combatLog.push(logEntry);
    }

    /**
     * 重置Boss系统
     */
    reset() {
        super.reset();
        this.currentBoss = null;
        this.bossLog = [];
        
        return { success: true, message: 'Boss系统已重置' };
    }
}

module.exports = {
    BossSystem,
    BossCard,
    BossUnit,
    BossGenerator,
    BossAbilityType,
    BossType
};
