/**
 * Game Master System - 城主规则系统
 * v2.4 核心组件
 * 
 * 功能：
 * - 轮换城主机制 (v1.4)
 * - 城主权限系统 (设定主题/抽卡/事件判定)
 * - NPC扮演机制 (v1.4)
 * - 地块行动规则 (v1.2)
 *   * 路面: 消耗1点，roll 角色+物品+状态/事件
 *   * 建筑: 消耗2点，roll 地点+人物/物品+状态/事件
 *   * 河流: 先判定天气(1-3阴天/4-6晴天)，roll 物品/状态/事件
 *   * 转生点: 角色转生
 */

const { CardSystem } = require('./card-system');
const { WeatherSystem, WeatherType } = require('./weather-system');

/**
 * 地块类型枚举
 */
const TileType = {
    ROAD: 'road',           // 路面
    BUILDING: 'building',   // 建筑
    RIVER: 'river',         // 河流
    RESPAWN: 'respawn',     // 转生点
    FOREST: 'forest',       // 森林
    MOUNTAIN: 'mountain'    // 山地
};

/**
 * 地块配置
 */
const TILE_CONFIG = {
    [TileType.ROAD]: {
        name: '路面',
        icon: '🛤️',
        baseCost: 1,
        description: '平坦的道路，便于通行',
        drawRules: {
            types: ['role', 'item', 'state', 'event'],
            count: { min: 1, max: 2 }
        }
    },
    [TileType.BUILDING]: {
        name: '建筑',
        icon: '🏛️',
        baseCost: 2,
        description: '建筑物内，资源丰富',
        drawRules: {
            types: ['location', 'role', 'item', 'state', 'event'],
            count: { min: 2, max: 3 }
        }
    },
    [TileType.RIVER]: {
        name: '河流',
        icon: '🌊',
        baseCost: 1,
        description: '水流湍急，需先判定天气',
        drawRules: {
            types: ['item', 'state', 'event'],
            count: { min: 1, max: 2 },
            requiresWeather: true  // 需要先判定天气
        }
    },
    [TileType.RESPAWN]: {
        name: '转生点',
        icon: '✨',
        baseCost: 0,
        description: '角色转生，重新捏角色',
        drawRules: {
            types: ['role'],
            count: { min: 1, max: 1 },
            specialAction: 'rebirth'
        }
    },
    [TileType.FOREST]: {
        name: '森林',
        icon: '🌲',
        baseCost: 2,
        description: '茂密的森林，探索困难',
        drawRules: {
            types: ['item', 'state', 'event'],
            count: { min: 1, max: 2 }
        }
    },
    [TileType.MOUNTAIN]: {
        name: '山地',
        icon: '⛰️',
        baseCost: 3,
        description: '崎岖的山路，消耗体力',
        drawRules: {
            types: ['location', 'item', 'state', 'event'],
            count: { min: 1, max: 2 }
        }
    }
};

/**
 * 城主权限枚举
 */
const GMPermission = {
    SET_THEME: 'set_theme',           // 设定主题
    DRAW_CARDS: 'draw_cards',         // 抽卡
    JUDGE_EVENT: 'judge_event',       // 事件判定
    PLAY_NPC: 'play_npc',             // 扮演NPC
    SET_RULES: 'set_rules',           // 设定规则
    CONTROL_PLOT: 'control_plot',     // 剧情控制
    AWARD_PENALTY: 'award_penalty'    // 奖惩判定
};

/**
 * NPC角色类
 */
class NPC {
    constructor(data) {
        this.id = `npc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        this.name = data.name || '神秘人物';
        this.description = data.description || '';
        this.role = data.role || '路人';
        this.traits = data.traits || [];
        this.dialogues = data.dialogues || [];
        this.secrets = data.secrets || [];
        this.hostility = data.hostility || 0;  // 敌对度 0-100
        this.playerController = null;  // 控制玩家
        this.position = data.position || null;  // 位置
        this.status = 'active';  // active/inactive/dead
    }

    /**
     * 分配玩家控制
     * @param {string} playerId 玩家ID
     */
    assignController(playerId) {
        this.playerController = playerId;
        return {
            success: true,
            message: `🎭 ${this.name} 已分配给玩家 ${playerId} 扮演`
        };
    }

    /**
     * 获取对话
     * @param {string} context 上下文
     */
    getDialogue(context = 'default') {
        if (this.dialogues.length === 0) {
            return `${this.name} 沉默地看着你。`;
        }
        
        // 根据上下文选择合适的对话
        const contextDialogues = this.dialogues.filter(d => 
            d.context === context || d.context === 'default'
        );
        
        if (contextDialogues.length > 0) {
            const dialogue = contextDialogues[Math.floor(Math.random() * contextDialogues.length)];
            return dialogue.text;
        }
        
        return this.dialogues[0].text;
    }

    /**
     * 调整敌对度
     * @param {number} delta 变化值
     */
    adjustHostility(delta) {
        this.hostility = Math.max(0, Math.min(100, this.hostility + delta));
        
        let attitude = '';
        if (this.hostility < 20) attitude = '友好';
        else if (this.hostility < 50) attitude = '中立';
        else if (this.hostility < 80) attitude = '警惕';
        else attitude = '敌对';
        
        return {
            hostility: this.hostility,
            attitude,
            message: `${this.name} 对你的态度变为 ${attitude} (${this.hostility}/100)`
        };
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            role: this.role,
            description: this.description,
            traits: this.traits,
            hostility: this.hostility,
            controller: this.playerController,
            position: this.position,
            status: this.status
        };
    }
}

/**
 * 地块类
 */
class Tile {
    constructor(x, y, type = TileType.ROAD, data = {}) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.config = TILE_CONFIG[type];
        this.discovered = false;  // 是否被发现
        this.revealed = false;    // 是否被揭开
        this.eventCard = null;    // 暗盖的事件卡
        this.items = [];          // 掉落的物品
        this.traps = [];          // 陷阱
        this.npcs = [];           // NPC
        this.data = data;         // 额外数据
    }

    /**
     * 揭开地块
     */
    reveal() {
        this.revealed = true;
        this.discovered = true;
        
        return {
            type: this.type,
            name: this.config.name,
            icon: this.config.icon,
            description: this.config.description,
            revealed: true,
            eventCard: this.eventCard,
            npcs: this.npcs.map(n => n.toJSON()),
            items: this.items
        };
    }

    /**
     * 发现地块（但不完全揭开）
     */
    discover() {
        this.discovered = true;
        return {
            type: this.type,
            icon: this.config.icon,
            discovered: true
        };
    }

    /**
     * 放置物品
     * @param {Object} item 物品
     */
    placeItem(item) {
        this.items.push(item);
        return {
            success: true,
            message: `${this.config.icon} 在${this.config.name}处放置了 ${item.name}`
        };
    }

    /**
     * 放置陷阱
     * @param {Object} trap 陷阱
     * @param {string} playerId 设置者ID
     */
    placeTrap(trap, playerId) {
        this.traps.push({
            ...trap,
            placedBy: playerId,
            placedAt: Date.now()
        });
        return {
            success: true,
            message: `在${this.config.name}处设置了陷阱: ${trap.name}`
        };
    }

    /**
     * 添加NPC
     * @param {NPC} npc NPC对象
     */
    addNPC(npc) {
        this.npcs.push(npc);
        npc.position = { x: this.x, y: this.y };
        return {
            success: true,
            message: `${npc.name} 出现在 ${this.config.icon} ${this.config.name}`
        };
    }

    /**
     * 触发陷阱
     * @param {string} playerId 触发者ID
     */
    triggerTraps(playerId) {
        if (this.traps.length === 0) return null;
        
        const triggered = this.traps.filter(t => t.placedBy !== playerId);
        this.traps = []; // 触发后清除
        
        return triggered.map(t => ({
            name: t.name,
            effect: t.effect,
            damage: t.damage || 0,
            placedBy: t.placedBy
        }));
    }

    toJSON() {
        return {
            x: this.x,
            y: this.y,
            type: this.type,
            name: this.config.name,
            icon: this.config.icon,
            discovered: this.discovered,
            revealed: this.revealed,
            hasEvent: !!this.eventCard,
            itemCount: this.items.length,
            npcCount: this.npcs.length
        };
    }
}

/**
 * 城主系统核心类
 */
class GameMasterSystem {
    constructor() {
        this.cardSystem = new CardSystem();
        this.weatherSystem = new WeatherSystem();
        
        // 城主相关
        this.currentGM = null;           // 当前城主玩家ID
        this.gmRotation = [];            // 轮换队列
        this.gmHistory = [];             // 历史记录
        
        // 游戏状态
        this.gameTheme = null;           // 游戏主题
        this.gameRules = {};             // 游戏规则
        this.activeNPCs = new Map();     // 活跃NPC
        this.map = new Map();            // 地图地块
        this.players = new Map();        // 玩家信息
        
        // 回合状态
        this.currentPlayer = null;       // 当前行动玩家
        this.turnCount = 0;              // 回合数
        this.activePlayerActions = new Map();  // 玩家行动点数
    }

    // ═══════════════════════════════════════════════════════════════
    // 轮换城主机制 (v1.4)
    // ═══════════════════════════════════════════════════════════════

    /**
     * 初始化城主轮换
     * @param {Array<string>} playerIds 玩家ID列表
     * @param {string} firstGM 首任城主
     */
    initGMRotation(playerIds, firstGM = null) {
        this.gmRotation = [...playerIds];
        
        // 随机或指定首任城主
        if (firstGM) {
            this.currentGM = firstGM;
        } else {
            const randomIndex = Math.floor(Math.random() * playerIds.length);
            this.currentGM = playerIds[randomIndex];
        }
        
        // 初始化玩家
        playerIds.forEach(id => {
            this.players.set(id, {
                id,
                role: null,
                position: null,
                actionPoints: 0,
                inventory: [],
                states: [],
                traits: { positive: null, negative: null }
            });
        });
        
        return {
            success: true,
            currentGM: this.currentGM,
            rotation: this.gmRotation,
            message: `🎭 城主轮换已初始化，首任城主: ${this.currentGM}`
        };
    }

    /**
     * 轮换城主 (v1.4核心机制)
     * 当轮到一个玩家回合时，其他玩家充当城主
     */
    rotateGM() {
        // 记录历史
        this.gmHistory.push({
            gm: this.currentGM,
            turn: this.turnCount,
            timestamp: Date.now()
        });
        
        // 轮换到下一个
        const currentIndex = this.gmRotation.indexOf(this.currentGM);
        const nextIndex = (currentIndex + 1) % this.gmRotation.length;
        this.currentGM = this.gmRotation[nextIndex];
        
        this.turnCount++;
        
        return {
            success: true,
            newGM: this.currentGM,
            turnCount: this.turnCount,
            message: `🎭 城主轮换 → ${this.currentGM} 成为新任城主 (第${this.turnCount}回合)`
        };
    }

    /**
     * 获取当前城主
     */
    getCurrentGM() {
        return {
            gm: this.currentGM,
            permissions: Object.values(GMPermission),
            isActive: this.currentGM !== null
        };
    }

    /**
     * 获取非城主玩家列表 (v1.4: 其他玩家充当城主)
     */
    getOtherPlayers(asGM = false) {
        if (!this.currentGM) return [];
        
        const others = this.gmRotation.filter(id => id !== this.currentGM);
        
        if (asGM) {
            return others.map(id => ({
                id,
                role: 'assistant_gm',
                permissions: [GMPermission.DRAW_CARDS, GMPermission.PLAY_NPC]
            }));
        }
        
        return others;
    }

    // ═══════════════════════════════════════════════════════════════
    // 城主权限系统
    // ═══════════════════════════════════════════════════════════════

    /**
     * 设定游戏主题 (城主权限)
     * @param {string} playerId 玩家ID
     * @param {Object} theme 主题配置
     */
    setGameTheme(playerId, theme) {
        // 检查权限
        if (playerId !== this.currentGM) {
            return { error: '只有当前城主可以设定主题' };
        }
        
        this.gameTheme = {
            name: theme.name || '未知主题',
            description: theme.description || '',
            goal: theme.goal || '',
            setting: theme.setting || '',
            specialRules: theme.specialRules || [],
            setBy: playerId,
            setAt: Date.now()
        };
        
        return {
            success: true,
            theme: this.gameTheme,
            message: `🎭 城主 ${playerId} 设定了游戏主题: ${theme.name}`
        };
    }

    /**
     * 城主抽卡 (城主权限)
     * @param {string} playerId 玩家ID
     * @param {string} deckName 卡组名
     * @param {number} count 数量
     */
    gmDrawCards(playerId, deckName = 'all', count = 1) {
        // 检查权限 - 城主或助手GM都可以
        if (!this._hasGMPermission(playerId, GMPermission.DRAW_CARDS)) {
            return { error: '没有抽卡权限' };
        }
        
        const result = this.cardSystem.drawMultiple(deckName, count);
        
        return {
            ...result,
            drawnBy: playerId,
            isGM: playerId === this.currentGM,
            message: `🎴 城主 ${playerId} 抽取了 ${count} 张卡牌`
        };
    }

    /**
     * 事件判定 (城主权限)
     * @param {string} playerId 玩家ID
     * @param {string} eventType 事件类型
     * @param {Object} context 上下文
     */
    judgeEvent(playerId, eventType, context = {}) {
        if (!this._hasGMPermission(playerId, GMPermission.JUDGE_EVENT)) {
            return { error: '没有事件判定权限' };
        }
        
        const roll = Math.floor(Math.random() * 20) + 1;  // D20判定
        let result = '';
        let success = false;
        
        // 判定逻辑
        if (roll >= 15) {
            result = '大成功';
            success = true;
        } else if (roll >= 10) {
            result = '成功';
            success = true;
        } else if (roll >= 5) {
            result = '失败';
            success = false;
        } else {
            result = '大失败';
            success = false;
        }
        
        return {
            success: true,
            judgeResult: {
                roll,
                result,
                outcome: success,
                eventType,
                context,
                judgedBy: playerId
            },
            message: `🎲 城主判定 [${eventType}]: ${roll} → ${result}`
        };
    }

    /**
     * 检查是否有城主权限
     */
    _hasGMPermission(playerId, permission) {
        // 当前城主拥有所有权限
        if (playerId === this.currentGM) return true;
        
        // 助手GM拥有部分权限
        const isAssistant = this.gmRotation.includes(playerId) && playerId !== this.currentGM;
        if (isAssistant) {
            const assistantPermissions = [
                GMPermission.DRAW_CARDS,
                GMPermission.PLAY_NPC
            ];
            return assistantPermissions.includes(permission);
        }
        
        return false;
    }

    // ═══════════════════════════════════════════════════════════════
    // NPC扮演机制 (v1.4)
    // ═══════════════════════════════════════════════════════════════

    /**
     * 创建NPC (城主权限)
     * @param {string} playerId 创建者ID
     * @param {Object} npcData NPC数据
     */
    createNPC(playerId, npcData) {
        if (!this._hasGMPermission(playerId, GMPermission.PLAY_NPC)) {
            return { error: '没有创建NPC的权限' };
        }
        
        const npc = new NPC(npcData);
        this.activeNPCs.set(npc.id, npc);
        
        return {
            success: true,
            npc: npc.toJSON(),
            message: `🎭 ${playerId} 创建了NPC: ${npc.name}`
        };
    }

    /**
     * 请求扮演NPC (v1.4: 玩家可以主动申请其他玩家扮演NPC)
     * @param {string} playerId 请求者
     * @param {string} npcId NPC ID
     * @param {string} targetPlayerId 目标玩家
     */
    requestNPCRole(playerId, npcId, targetPlayerId) {
        const npc = this.activeNPCs.get(npcId);
        if (!npc) {
            return { error: 'NPC不存在' };
        }
        
        // 分配控制器
        const result = npc.assignController(targetPlayerId);
        
        return {
            ...result,
            requester: playerId,
            npcId,
            controller: targetPlayerId,
            message: `🎭 ${playerId} 请求 ${targetPlayerId} 扮演 ${npc.name}`
        };
    }

    /**
     * 轮换NPC扮演 (v1.4: 多方飙戏)
     * @param {string} npcId NPC ID
     * @param {string} newController 新控制者
     */
    rotateNPCController(npcId, newController) {
        const npc = this.activeNPCs.get(npcId);
        if (!npc) {
            return { error: 'NPC不存在' };
        }
        
        const oldController = npc.playerController;
        const result = npc.assignController(newController);
        
        return {
            ...result,
            npcId,
            oldController,
            newController,
            message: `🎭 ${npc.name} 的扮演者从 ${oldController} 轮换为 ${newController}`
        };
    }

    /**
     * NPC对话
     * @param {string} npcId NPC ID
     * @param {string} context 对话上下文
     */
    npcDialogue(npcId, context = 'default') {
        const npc = this.activeNPCs.get(npcId);
        if (!npc) {
            return { error: 'NPC不存在' };
        }
        
        return {
            npcId,
            name: npc.name,
            dialogue: npc.getDialogue(context),
            controller: npc.playerController,
            hostility: npc.hostility
        };
    }

    /**
     * 获取可扮演的NPC列表
     * @param {string} playerId 玩家ID
     */
    getPlayableNPCs(playerId) {
        const npcs = [];
        for (const npc of this.activeNPCs.values()) {
            if (!npc.playerController || npc.playerController === playerId) {
                npcs.push(npc.toJSON());
            }
        }
        return npcs;
    }

    // ═══════════════════════════════════════════════════════════════
    // 地块行动规则 (v1.2)
    // ═══════════════════════════════════════════════════════════════

    /**
     * 初始化地图
     * @param {number} width 宽度
     * @param {number} height 高度
     * @param {Array} specialTiles 特殊地块配置
     */
    initMap(width = 3, height = 3, specialTiles = []) {
        this.map.clear();
        
        for (let x = 0; x < width; x++) {
            for (let y = 0; y < height; y++) {
                const key = `${x},${y}`;
                
                // 根据配置确定地块类型
                const special = specialTiles.find(t => t.x === x && t.y === y);
                const type = special ? special.type : this._randomTileType();
                
                const tile = new Tile(x, y, type, special?.data || {});
                
                // 放置随机事件卡
                if (type !== TileType.RESPAWN) {
                    tile.eventCard = this._generateRandomEvent();
                }
                
                this.map.set(key, tile);
            }
        }
        
        return {
            success: true,
            mapSize: { width, height },
            tileCount: this.map.size,
            message: `🗺️ 地图已初始化: ${width}x${height}`
        };
    }

    /**
     * 执行地块行动 (v1.2核心规则)
     * @param {string} playerId 玩家ID
     * @param {number} x X坐标
     * @param {number} y Y坐标
     * @param {number} actionPoints 可用行动点数
     */
    performTileAction(playerId, x, y, actionPoints = 0) {
        const key = `${x},${y}`;
        const tile = this.map.get(key);
        
        if (!tile) {
            return { error: '无效的地块坐标' };
        }
        
        const player = this.players.get(playerId);
        if (!player) {
            return { error: '玩家不存在' };
        }
        
        const config = tile.config;
        let result = {
            success: true,
            tile: {
                x, y,
                type: tile.type,
                name: config.name,
                icon: config.icon
            },
            consumedPoints: 0,
            weatherCheck: null,
            draws: [],
            messages: []
        };
        
        // ═══════════════════════════════════════════════════════════
        // 不同地块的特殊规则
        // ═══════════════════════════════════════════════════════════
        
        switch (tile.type) {
            case TileType.ROAD: {
                // 路面: 消耗1点，roll 角色+物品+状态/事件
                result.consumedPoints = 1;
                if (actionPoints < result.consumedPoints) {
                    return { error: `行动点数不足，需要 ${result.consumedPoints} 点` };
                }
                
                result.draws = this._performDraws(['role', 'item', 'state', 'event']);
                result.messages.push(`🛤️ 在${config.name}上行动，消耗 ${result.consumedPoints} 点`);
                break;
            }
                
            case TileType.BUILDING: {
                // 建筑: 消耗2点，roll 地点+人物/物品+状态/事件
                result.consumedPoints = 2;
                if (actionPoints < result.consumedPoints) {
                    return { error: `行动点数不足，需要 ${result.consumedPoints} 点` };
                }
                
                result.draws = this._performDraws(['location', 'role', 'item', 'state', 'event']);
                result.messages.push(`🏛️ 探索${config.name}，消耗 ${result.consumedPoints} 点`);
                break;
            }
                
            case TileType.RIVER: {
                // 河流: 先判定天气(1-3阴天/4-6晴天)，roll 物品/状态/事件
                result.consumedPoints = 1;
                if (actionPoints < result.consumedPoints) {
                    return { error: `行动点数不足，需要 ${result.consumedPoints} 点` };
                }
                
                // 天气判定
                result.weatherCheck = this.weatherSystem.rollRiverWeather();
                
                if (result.weatherCheck.isSunny) {
                    // 晴天，正常行动
                    result.draws = this._performDraws(['item', 'state', 'event']);
                    result.messages.push(`🌊 河流上天气晴朗，顺利通行`);
                } else {
                    // 阴天/雨天，可能有额外事件
                    result.draws = this._performDraws(['item', 'state', 'event']);
                    result.draws.push(this._performDraws(['event'])[0]);  // 额外事件
                    result.messages.push(`🌊 河流上天气阴沉，可能会遭遇意外`);
                }
                break;
            }
                
            case TileType.RESPAWN: {
                // 转生点: 角色转生
                result.consumedPoints = 0;
                
                // 执行转生
                const rebirthResult = this._performRebirth(playerId);
                result.rebirth = rebirthResult;
                result.messages.push(`✨ 在转生点触发转生！`);
                break;
            }
                
            case TileType.FOREST:
            case TileType.MOUNTAIN: {
                // 其他地形: 按配置消耗点数
                result.consumedPoints = config.baseCost;
                if (actionPoints < result.consumedPoints) {
                    return { error: `行动点数不足，需要 ${result.consumedPoints} 点` };
                }
                
                result.draws = this._performDraws(config.drawRules.types);
                result.messages.push(`${config.icon} 穿越${config.name}，消耗 ${result.consumedPoints} 点`);
                break;
            }
        }
        
        // 揭开地块
        const revealed = tile.reveal();
        result.revealedContent = revealed;
        
        // 检查陷阱
        const traps = tile.triggerTraps(playerId);
        if (traps && traps.length > 0) {
            result.trapsTriggered = traps;
            result.messages.push(`💥 触发了 ${traps.length} 个陷阱!`);
        }
        
        // 更新玩家位置
        player.position = { x, y };
        
        // 构建故事
        result.story = this._generateTileStory(result);
        
        return result;
    }

    /**
     * 执行抽卡
     */
    _performDraws(types) {
        const draws = [];
        types.forEach(type => {
            const deckMap = {
                'role': 'role',
                'location': 'location', 
                'item': 'item',
                'state': 'state',
                'event': 'event'
            };
            
            const deckName = deckMap[type];
            if (deckName) {
                const result = this.cardSystem.draw(deckName);
                if (result.success) {
                    draws.push({
                        type,
                        card: result.card.toJSON()
                    });
                }
            }
        });
        return draws;
    }

    /**
     * 执行转生
     */
    _performRebirth(playerId) {
        const player = this.players.get(playerId);
        
        // 抽取新角色
        const roleResult = this.cardSystem.draw('role');
        const stateResults = this.cardSystem.drawMultiple('state', 2);
        
        // 重新生成角色
        player.role = roleResult.success ? roleResult.card.toJSON() : null;
        player.states = stateResults.cards.map(c => c.toJSON());
        player.inventory = []; // 清空背包
        
        // 确定先天天赋 (一个增益一个减益)
        const positiveTrait = this._generateRandomTrait('positive');
        const negativeTrait = this._generateRandomTrait('negative');
        player.traits = { positive: positiveTrait, negative: negativeTrait };
        
        return {
            newRole: player.role,
            newStates: player.states,
            traits: player.traits,
            message: `✨ ${playerId} 完成转生！获得新身份: ${player.role?.name || '未知'}`
        };
    }

    /**
     * 生成地块故事
     */
    _generateTileStory(actionResult) {
        const parts = [];
        
        // 基础行动描述
        parts.push(actionResult.messages[0]);
        
        // 抽卡结果
        if (actionResult.draws && actionResult.draws.length > 0) {
            const drawDesc = actionResult.draws.map(d => 
                `[${d.type}]${d.card.name}`
            ).join(' + ');
            parts.push(`你遇到了: ${drawDesc}`);
        }
        
        // 天气影响
        if (actionResult.weatherCheck) {
            parts.push(actionResult.weatherCheck.message);
        }
        
        // 陷阱
        if (actionResult.trapsTriggered) {
            parts.push(`小心！${actionResult.trapsTriggered.map(t => t.name).join('、')}`);
        }
        
        return parts.join('\n');
    }

    /**
     * 生成随机事件
     */
    _generateRandomEvent() {
        const events = [
            '发现神秘符号', '听到奇怪的声音', '发现隐藏的暗格',
            '遭遇不速之客', '触发机关', '发现被遗忘的物品'
        ];
        return events[Math.floor(Math.random() * events.length)];
    }

    /**
     * 生成随机特质
     */
    _generateRandomTrait(type) {
        const positive = ['天赋异禀', '好运连连', '身轻如燕', '过目不忘'];
        const negative = ['厄运缠身', '体弱多病', '笨手笨脚', '口无遮拦'];
        
        const list = type === 'positive' ? positive : negative;
        return list[Math.floor(Math.random() * list.length)];
    }

    /**
     * 随机地块类型
     */
    _randomTileType() {
        const types = [
            TileType.ROAD, TileType.ROAD, TileType.ROAD,
            TileType.BUILDING, TileType.BUILDING,
            TileType.RIVER,
            TileType.FOREST
        ];
        return types[Math.floor(Math.random() * types.length)];
    }

    // ═══════════════════════════════════════════════════════════════
    // 游戏流程控制
    // ═══════════════════════════════════════════════════════════════

    /**
     * 开始玩家回合
     * @param {string} playerId 玩家ID
     */
    startPlayerTurn(playerId) {
        this.currentPlayer = playerId;
        
        // 分配行动点数 (默认每回合6点)
        this.activePlayerActions.set(playerId, 6);
        
        // 城主轮换 (v1.4)
        if (this.turnCount > 0) {
            this.rotateGM();
        }
        
        return {
            playerId,
            actionPoints: 6,
            currentGM: this.currentGM,
            message: `🎮 ${playerId} 的回合开始，获得 6 点行动力。当前城主: ${this.currentGM}`
        };
    }

    /**
     * 使用行动点数
     * @param {string} playerId 玩家ID
     * @param {number} points 消耗点数
     */
    consumeActionPoints(playerId, points) {
        const current = this.activePlayerActions.get(playerId) || 0;
        
        if (current < points) {
            return { error: `行动点数不足，当前: ${current}，需要: ${points}` };
        }
        
        this.activePlayerActions.set(playerId, current - points);
        
        return {
            success: true,
            consumed: points,
            remaining: current - points,
            message: `消耗 ${points} 点行动力，剩余 ${current - points} 点`
        };
    }

    /**
     * 回合结束处理
     * @param {string} playerId 玩家ID
     */
    endPlayerTurn(playerId) {
        const remaining = this.activePlayerActions.get(playerId) || 0;
        
        // 未使用的行动点可以回血 (v1.5规则: 行动点÷2做回血)
        const healAmount = Math.floor(remaining / 2);
        
        this.activePlayerActions.delete(playerId);
        this.currentPlayer = null;
        
        return {
            success: true,
            remainingActionPoints: remaining,
            healAmount,
            message: `回合结束。剩余 ${remaining} 点行动力可回复 ${healAmount} 点生命`
        };
    }

    /**
     * 获取地图状态
     */
    getMapStatus() {
        const tiles = [];
        for (const [key, tile] of this.map) {
            tiles.push(tile.toJSON());
        }
        
        return {
            tiles,
            discoveredCount: tiles.filter(t => t.discovered).length,
            revealedCount: tiles.filter(t => t.revealed).length,
            totalTiles: tiles.length
        };
    }

    /**
     * 获取游戏状态
     */
    getGameState() {
        return {
            theme: this.gameTheme,
            turnCount: this.turnCount,
            currentGM: this.currentGM,
            currentPlayer: this.currentPlayer,
            playerCount: this.players.size,
            npcCount: this.activeNPCs.size,
            weather: this.weatherSystem.getCurrentWeatherEffect(),
            map: this.getMapStatus()
        };
    }

    /**
     * 设置陷阱 (v1.2规则)
     * @param {string} playerId 玩家ID
     * @param {number} x X坐标
     * @param {number} y Y坐标
     * @param {Object} trap 陷阱配置
     */
    setTrap(playerId, x, y, trap) {
        const key = `${x},${y}`;
        const tile = this.map.get(key);
        
        if (!tile) {
            return { error: '无效的地块坐标' };
        }
        
        // 消耗物品卡
        // player.inventory 中需要有对应物品
        
        return tile.placeTrap(trap, playerId);
    }

    /**
     * 添加事件 (城主权限)
     * @param {string} playerId 玩家ID
     * @param {Object} event 事件配置
     */
    addEvent(playerId, event) {
        if (!this._hasGMPermission(playerId, GMPermission.CONTROL_PLOT)) {
            return { error: '没有添加事件的权限' };
        }
        
        // 事件可以是周期性的 (v1.4规则)
        const newEvent = {
            id: `event_${Date.now()}`,
            name: event.name,
            description: event.description,
            type: event.type || 'random',  // random/scheduled/conditional
            progress: event.progress || 0,
            maxProgress: event.maxProgress || 100,
            effects: event.effects || [],
            isPeriodic: event.isPeriodic || false,
            period: event.period || 1,  // 每N回合触发
            addedBy: playerId,
            addedAt: Date.now()
        };
        
        return {
            success: true,
            event: newEvent,
            message: `📅 ${playerId} 添加了事件: ${event.name}`
        };
    }

    /**
     * 玩家初始化 (v1.2规则)
     * @param {string} playerId 玩家ID
     * @param {Object} options 初始化选项
     */
    initializePlayer(playerId, options = {}) {
        const player = this.players.get(playerId);
        if (!player) {
            this.players.set(playerId, {
                id: playerId,
                role: null,
                position: null,
                actionPoints: 0,
                inventory: [],
                states: [],
                traits: { positive: null, negative: null }
            });
        }
        
        // 抽取角色卡
        const roleResult = this.cardSystem.draw('role');
        
        // 抽取两个状态卡 (v1.2规则)
        const stateResults = this.cardSystem.drawMultiple('state', 2);
        
        // 在城主协助下获得增益和减益天赋
        const positiveTrait = this._generateRandomTrait('positive');
        const negativeTrait = this._generateRandomTrait('negative');
        
        const playerData = this.players.get(playerId);
        playerData.role = roleResult.success ? roleResult.card.toJSON() : null;
        playerData.states = stateResults.cards.map(c => c.toJSON());
        playerData.traits = { positive: positiveTrait, negative: negativeTrait };
        
        return {
            success: true,
            player: playerData,
            message: `🎭 ${playerId} 初始化完成！\n` +
                    `角色: ${playerData.role?.name || '未知'}\n` +
                    `状态: ${playerData.states.map(s => s.name).join(', ')}\n` +
                    `天赋: [+${positiveTrait}] [-${negativeTrait}]`
        };
    }

    /**
     * 重置系统
     */
    reset() {
        this.currentGM = null;
        this.gmRotation = [];
        this.gmHistory = [];
        this.gameTheme = null;
        this.gameRules = {};
        this.activeNPCs.clear();
        this.map.clear();
        this.players.clear();
        this.currentPlayer = null;
        this.turnCount = 0;
        this.activePlayerActions.clear();
        
        this.cardSystem.reset();
        this.weatherSystem.reset();
        
        return {
            success: true,
            message: '城主系统已完全重置'
        };
    }
}

// 导出
module.exports = {
    GameMasterSystem,
    Tile,
    NPC,
    TileType,
    GMPermission,
    TILE_CONFIG
};
