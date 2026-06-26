/**
 * TurnManager - 回合管理器
 * 管理游戏回合流程、阶段转换触发器、事件调度系统
 */

const { ThreeActStructure, ActPhase } = require('./three-act-structure');

/**
 * 回合状态
 */
const TurnState = {
    WAITING: 'waiting',      // 等待玩家输入
    PROCESSING: 'processing', // 处理中
    COMPLETED: 'completed',   // 回合完成
    PAUSED: 'paused'         // 暂停中
};

/**
 * 事件类型
 */
const EventType = {
    TURN_START: 'turn_start',
    TURN_END: 'turn_end',
    PHASE_START: 'phase_start',
    PHASE_END: 'phase_end',
    PHASE_TRANSITION: 'phase_transition',
    PLAYER_ACTION: 'player_action',
    SYSTEM_EVENT: 'system_event',
    SCHEDULED_EVENT: 'scheduled_event',
    TRIGGER_EVENT: 'trigger_event'
};

/**
 * 触发器类型
 */
const TriggerType = {
    ON_TURN: 'on_turn',              // 特定回合触发
    ON_PHASE: 'on_phase',            // 特定阶段触发
    ON_CONDITION: 'on_condition',    // 条件触发
    ON_RANDOM: 'on_random',          // 随机触发
    ON_PLAYER_COUNT: 'on_player_count' // 玩家数量触发
};

/**
 * 回合管理器
 */
class TurnManager {
    constructor(config = {}) {
        this.config = {
            // 回合配置
            maxTurns: config.maxTurns || 15,           // 最大回合数
            turnTimeout: config.turnTimeout || 300000, // 回合超时（毫秒）
            autoSkip: config.autoSkip || false,        // 自动跳过超时回合
            
            // 玩家配置
            minPlayers: config.minPlayers || 1,
            maxPlayers: config.maxPlayers || 8,
            
            // AI配置
            aiAssistEnabled: config.aiAssistEnabled || true,
            aiAssistDelay: config.aiAssistDelay || 60000 // AI辅助延迟
        };

        // 三幕式结构
        this.threeActStructure = new ThreeActStructure(config.threeAct || {});

        // 回合状态
        this.turnState = TurnState.WAITING;
        this.currentTurn = 0;
        this.turnStartTime = null;
        this.turnHistory = [];

        // 玩家管理
        this.players = new Map();  // playerId -> playerInfo
        this.playerOrder = [];     // 玩家行动顺序
        this.currentPlayerIndex = 0;

        // 事件系统
        this.eventQueue = [];      // 事件队列
        this.eventHistory = [];    // 事件历史
        this.scheduledEvents = new Map(); // 计划事件 ID -> event

        // 触发器系统
        this.triggers = new Map(); // 触发器 ID -> trigger
        this.triggerHistory = [];  // 触发历史

        // 回调函数
        this.callbacks = {
            onTurnStart: null,
            onTurnEnd: null,
            onPlayerAction: null,
            onEvent: null,
            onError: null
        };

        // 初始化三幕式结构回调
        this._initThreeActCallbacks();
    }

    /**
     * 初始化三幕式结构回调
     */
    _initThreeActCallbacks() {
        this.threeActStructure.setCallbacks({
            onPhaseStart: (data) => {
                this._emitEvent({
                    type: EventType.PHASE_START,
                    data
                });
            },
            onPhaseEnd: (data) => {
                this._emitEvent({
                    type: EventType.PHASE_END,
                    data
                });
            },
            onTransition: (data) => {
                this._emitEvent({
                    type: EventType.PHASE_TRANSITION,
                    data
                });
            },
            onTurnEnd: (data) => {
                this._emitEvent({
                    type: EventType.TURN_END,
                    data
                });
            }
        });
    }

    /**
     * 设置回调函数
     */
    setCallbacks(callbacks) {
        Object.assign(this.callbacks, callbacks);
    }

    // ============ 玩家管理 ============

    /**
     * 添加玩家
     */
    addPlayer(playerId, playerInfo = {}) {
        if (this.players.size >= this.config.maxPlayers) {
            return { success: false, error: '玩家数量已满' };
        }

        const player = {
            id: playerId,
            name: playerInfo.name || `玩家${this.players.size + 1}`,
            joinTime: new Date().toISOString(),
            turnsPlayed: 0,
            lastActionTime: null,
            isAI: playerInfo.isAI || false,
            ...playerInfo
        };

        this.players.set(playerId, player);
        this.playerOrder.push(playerId);

        return { success: true, player };
    }

    /**
     * 移除玩家
     */
    removePlayer(playerId) {
        if (!this.players.has(playerId)) {
            return { success: false, error: '玩家不存在' };
        }

        this.players.delete(playerId);
        this.playerOrder = this.playerOrder.filter(id => id !== playerId);

        // 调整当前玩家索引
        if (this.currentPlayerIndex >= this.playerOrder.length) {
            this.currentPlayerIndex = 0;
        }

        return { success: true };
    }

    /**
     * 获取当前玩家
     */
    getCurrentPlayer() {
        if (this.playerOrder.length === 0) return null;
        return this.players.get(this.playerOrder[this.currentPlayerIndex]);
    }

    /**
     * 获取下一个玩家
     */
    getNextPlayer() {
        if (this.playerOrder.length === 0) return null;
        const nextIndex = (this.currentPlayerIndex + 1) % this.playerOrder.length;
        return this.players.get(this.playerOrder[nextIndex]);
    }

    /**
     * 获取所有玩家
     */
    getAllPlayers() {
        return Array.from(this.players.values());
    }

    // ============ 回合管理 ============

    /**
     * 开始新回合
     */
    startTurn() {
        if (this.turnState === TurnState.PROCESSING) {
            return { success: false, error: '当前回合正在进行中' };
        }

        this.turnState = TurnState.PROCESSING;
        this.turnStartTime = Date.now();
        this.currentTurn++;

        const currentPlayer = this.getCurrentPlayer();
        const phase = this.threeActStructure.getCurrentPhase();

        // 创建回合记录
        const turnRecord = {
            turn: this.currentTurn,
            phase,
            player: currentPlayer?.id,
            startTime: this.turnStartTime,
            actions: [],
            events: []
        };

        this.turnHistory.push(turnRecord);

        // 发出回合开始事件
        this._emitEvent({
            type: EventType.TURN_START,
            data: {
                turn: this.currentTurn,
                phase,
                player: currentPlayer
            }
        });

        // 检查触发器
        this._checkTriggers({
            turn: this.currentTurn,
            phase,
            player: currentPlayer
        });

        // 执行计划事件
        this._executeScheduledEvents();

        if (this.callbacks.onTurnStart) {
            this.callbacks.onTurnStart({
                turn: this.currentTurn,
                phase,
                player: currentPlayer
            });
        }

        return {
            success: true,
            turn: this.currentTurn,
            phase,
            currentPlayer,
            timeout: this.config.turnTimeout
        };
    }

    /**
     * 处理玩家行动
     */
    processPlayerAction(playerId, action) {
        if (this.turnState !== TurnState.PROCESSING) {
            return { success: false, error: '当前没有进行中的回合' };
        }

        const currentPlayer = this.getCurrentPlayer();
        if (currentPlayer?.id !== playerId) {
            return { success: false, error: '不是你的回合' };
        }

        // 更新玩家信息
        const player = this.players.get(playerId);
        if (player) {
            player.turnsPlayed++;
            player.lastActionTime = Date.now();
        }

        // 记录行动
        const actionRecord = {
            playerId,
            action,
            timestamp: Date.now()
        };

        const currentTurnRecord = this.turnHistory[this.turnHistory.length - 1];
        if (currentTurnRecord) {
            currentTurnRecord.actions.push(actionRecord);
        }

        // 发出玩家行动事件
        this._emitEvent({
            type: EventType.PLAYER_ACTION,
            data: actionRecord
        });

        // 根据三幕式结构处理行动
        const threeActResult = this._processActionByPhase(action);

        if (this.callbacks.onPlayerAction) {
            this.callbacks.onPlayerAction({
                playerId,
                action,
                result: threeActResult
            });
        }

        return {
            success: true,
            action: actionRecord,
            threeActResult
        };
    }

    /**
     * 根据阶段处理行动
     */
    _processActionByPhase(action) {
        const phase = this.threeActStructure.getCurrentPhase();
        
        switch (phase) {
            case ActPhase.PROLOGUE:
                return this._processPrologueAction(action);
            case ActPhase.CONFLICT:
                return this._processConflictAction(action);
            case ActPhase.CLIMAX:
                return this._processClimaxAction(action);
            default:
                return { success: true };
        }
    }

    /**
     * 处理序幕行动
     */
    _processPrologueAction(action) {
        const result = { success: true, effects: [] };

        // 世界观建立
        if (action.type === 'establish_world') {
            const turnResult = this.threeActStructure.addWorldElement(action.element);
            result.effects.push({ type: 'world_element_added', element: action.element });
            result.transition = turnResult.transition;
        }

        // 法则定义
        if (action.type === 'define_rule') {
            this.threeActStructure.defineRule(action.rule);
            result.effects.push({ type: 'rule_defined', rule: action.rule });
        }

        // 主线任务设定
        if (action.type === 'set_quest') {
            this.threeActStructure.setMainQuest(action.quest);
            result.effects.push({ type: 'main_quest_set', quest: action.quest });
        }

        return result;
    }

    /**
     * 处理破章行动
     */
    _processConflictAction(action) {
        const result = { success: true, effects: [] };

        // 遭遇敌人
        if (action.type === 'encounter_enemy') {
            const turnResult = this.threeActStructure.addEnemy(action.enemy);
            result.effects.push({ type: 'enemy_encountered', enemy: action.enemy });
            result.transition = turnResult.transition;
        }

        // 发生冲突
        if (action.type === 'add_conflict') {
            this.threeActStructure.addConflict(action.conflict);
            result.effects.push({ type: 'conflict_added', conflict: action.conflict });
        }

        // 剧情推进
        if (action.type === 'advance_plot') {
            const state = this.threeActStructure.getPhaseState(ActPhase.CONFLICT);
            state.plotPoints.push(action.plotPoint);
            result.effects.push({ type: 'plot_advanced', plotPoint: action.plotPoint });
        }

        return result;
    }

    /**
     * 处理急章行动
     */
    _processClimaxAction(action) {
        const result = { success: true, effects: [] };

        // Boss战开始
        if (action.type === 'boss_battle_start') {
            this.threeActStructure.setBoss(action.boss);
            result.effects.push({ type: 'boss_battle_started', boss: action.boss });
        }

        // Boss战行动
        if (action.type === 'boss_action') {
            result.effects.push({ type: 'boss_action', action: action.bossAction });
        }

        // Boss被击败
        if (action.type === 'defeat_boss') {
            const turnResult = this.threeActStructure.defeatBoss();
            result.effects.push({ type: 'boss_defeated' });
            result.transition = turnResult.transition;
        }

        // 添加结局
        if (action.type === 'add_ending') {
            this.threeActStructure.addEnding(action.ending);
            result.effects.push({ type: 'ending_added', ending: action.ending });
        }

        return result;
    }

    /**
     * 结束当前回合
     */
    endTurn(actions = {}) {
        if (this.turnState !== TurnState.PROCESSING) {
            return { success: false, error: '当前没有进行中的回合' };
        }

        // 处理三幕式结构回合结束
        const threeActResult = this.threeActStructure.endTurn(actions);

        // 更新回合记录
        const currentTurnRecord = this.turnHistory[this.turnHistory.length - 1];
        if (currentTurnRecord) {
            currentTurnRecord.endTime = Date.now();
            currentTurnRecord.duration = currentTurnRecord.endTime - currentTurnRecord.startTime;
            currentTurnRecord.threeActResult = threeActResult;
        }

        // 移动到下一个玩家
        this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.playerOrder.length;

        this.turnState = TurnState.COMPLETED;

        if (this.callbacks.onTurnEnd) {
            this.callbacks.onTurnEnd({
                turn: this.currentTurn,
                threeActResult
            });
        }

        return {
            success: true,
            turn: this.currentTurn,
            threeActResult,
            nextPlayer: this.getCurrentPlayer()
        };
    }

    /**
     * 跳过当前回合
     */
    skipTurn(reason = 'skipped') {
        return this.endTurn({ skipped: true, reason });
    }

    // ============ 事件系统 ============

    /**
     * 发出事件
     */
    _emitEvent(event) {
        event.timestamp = event.timestamp || Date.now();
        event.id = `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        this.eventHistory.push(event);

        if (this.callbacks.onEvent) {
            this.callbacks.onEvent(event);
        }

        return event;
    }

    /**
     * 调度事件
     */
    scheduleEvent(eventConfig) {
        const scheduledEvent = {
            id: `scheduled_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type: eventConfig.type || EventType.SCHEDULED_EVENT,
            data: eventConfig.data,
            triggerTurn: eventConfig.triggerTurn,
            triggerPhase: eventConfig.triggerPhase,
            delay: eventConfig.delay,
            recurring: eventConfig.recurring || false,
            createdAt: Date.now()
        };

        this.scheduledEvents.set(scheduledEvent.id, scheduledEvent);

        return { success: true, event: scheduledEvent };
    }

    /**
     * 取消计划事件
     */
    cancelScheduledEvent(eventId) {
        if (this.scheduledEvents.has(eventId)) {
            this.scheduledEvents.delete(eventId);
            return { success: true };
        }
        return { success: false, error: '事件不存在' };
    }

    /**
     * 执行计划事件
     */
    _executeScheduledEvents() {
        const currentPhase = this.threeActStructure.getCurrentPhase();
        const eventsToExecute = [];

        this.scheduledEvents.forEach((event, id) => {
            // 按回合触发
            if (event.triggerTurn && event.triggerTurn === this.currentTurn) {
                eventsToExecute.push(event);
            }

            // 按阶段触发
            if (event.triggerPhase && event.triggerPhase === currentPhase) {
                eventsToExecute.push(event);
            }

            // 按延迟触发
            if (event.delay && (Date.now() - event.createdAt) >= event.delay) {
                eventsToExecute.push(event);
            }
        });

        // 执行事件
        eventsToExecute.forEach(event => {
            this._emitEvent({
                type: event.type,
                data: event.data,
                scheduledEventId: event.id
            });

            // 非循环事件移除
            if (!event.recurring) {
                this.scheduledEvents.delete(event.id);
            }
        });

        return eventsToExecute;
    }

    /**
     * 获取事件历史
     */
    getEventHistory(limit = 50) {
        return this.eventHistory.slice(-limit);
    }

    // ============ 触发器系统 ============

    /**
     * 添加触发器
     */
    addTrigger(triggerConfig) {
        const trigger = {
            id: `trigger_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type: triggerConfig.type,
            condition: triggerConfig.condition,
            action: triggerConfig.action,
            enabled: true,
            triggerCount: 0,
            maxTriggers: triggerConfig.maxTriggers || -1, // -1 表示无限
            createdAt: Date.now()
        };

        this.triggers.set(trigger.id, trigger);

        return { success: true, trigger };
    }

    /**
     * 移除触发器
     */
    removeTrigger(triggerId) {
        if (this.triggers.has(triggerId)) {
            this.triggers.delete(triggerId);
            return { success: true };
        }
        return { success: false, error: '触发器不存在' };
    }

    /**
     * 检查触发器
     */
    _checkTriggers(context) {
        const triggeredActions = [];

        this.triggers.forEach((trigger, id) => {
            if (!trigger.enabled) return;
            if (trigger.maxTriggers > 0 && trigger.triggerCount >= trigger.maxTriggers) return;

            let shouldTrigger = false;

            switch (trigger.type) {
                case TriggerType.ON_TURN:
                    shouldTrigger = this._checkTurnTrigger(trigger, context);
                    break;
                case TriggerType.ON_PHASE:
                    shouldTrigger = this._checkPhaseTrigger(trigger, context);
                    break;
                case TriggerType.ON_CONDITION:
                    shouldTrigger = this._checkConditionTrigger(trigger, context);
                    break;
                case TriggerType.ON_RANDOM:
                    shouldTrigger = this._checkRandomTrigger(trigger, context);
                    break;
                case TriggerType.ON_PLAYER_COUNT:
                    shouldTrigger = this._checkPlayerCountTrigger(trigger, context);
                    break;
            }

            if (shouldTrigger) {
                trigger.triggerCount++;
                this.triggerHistory.push({
                    triggerId: id,
                    triggeredAt: Date.now(),
                    context
                });

                // 执行触发器动作
                const actionResult = trigger.action(context);
                triggeredActions.push({
                    triggerId: id,
                    result: actionResult
                });

                // 发出触发器事件
                this._emitEvent({
                    type: EventType.TRIGGER_EVENT,
                    data: {
                        triggerId: id,
                        triggerType: trigger.type,
                        context,
                        result: actionResult
                    }
                });
            }
        });

        return triggeredActions;
    }

    /**
     * 检查回合触发器
     */
    _checkTurnTrigger(trigger, context) {
        if (typeof trigger.condition === 'number') {
            return context.turn === trigger.condition;
        }
        if (typeof trigger.condition === 'object') {
            const { min, max } = trigger.condition;
            return context.turn >= min && context.turn <= max;
        }
        return false;
    }

    /**
     * 检查阶段触发器
     */
    _checkPhaseTrigger(trigger, context) {
        return context.phase === trigger.condition;
    }

    /**
     * 检查条件触发器
     */
    _checkConditionTrigger(trigger, context) {
        if (typeof trigger.condition === 'function') {
            return trigger.condition(context, this);
        }
        return false;
    }

    /**
     * 检查随机触发器
     */
    _checkRandomTrigger(trigger, context) {
        const probability = trigger.condition || 0.1;
        return Math.random() < probability;
    }

    /**
     * 检查玩家数量触发器
     */
    _checkPlayerCountTrigger(trigger, context) {
        const { min, max } = trigger.condition || {};
        const playerCount = this.players.size;
        
        if (min !== undefined && playerCount < min) return false;
        if (max !== undefined && playerCount > max) return false;
        
        return true;
    }

    // ============ 状态管理 ============

    /**
     * 获取完整状态
     */
    getFullState() {
        return {
            turn: {
                current: this.currentTurn,
                state: this.turnState,
                startTime: this.turnStartTime,
                history: this.turnHistory.slice(-10)
            },
            players: {
                list: this.getAllPlayers(),
                order: this.playerOrder,
                currentIndex: this.currentPlayerIndex,
                current: this.getCurrentPlayer()
            },
            threeAct: this.threeActStructure.getFullState(),
            events: {
                scheduled: Array.from(this.scheduledEvents.values()),
                history: this.eventHistory.slice(-20)
            },
            triggers: {
                list: Array.from(this.triggers.values()),
                history: this.triggerHistory.slice(-10)
            }
        };
    }

    /**
     * 暂停游戏
     */
    pause() {
        this.turnState = TurnState.PAUSED;
        return { success: true, message: '游戏已暂停' };
    }

    /**
     * 恢复游戏
     */
    resume() {
        if (this.turnState === TurnState.PAUSED) {
            this.turnState = TurnState.WAITING;
            return { success: true, message: '游戏已恢复' };
        }
        return { success: false, error: '游戏未暂停' };
    }

    /**
     * 重置回合管理器
     */
    reset(config = {}) {
        this.config = { ...this.config, ...config };
        this.threeActStructure.reset(config.threeAct);
        
        this.turnState = TurnState.WAITING;
        this.currentTurn = 0;
        this.turnStartTime = null;
        this.turnHistory = [];
        
        this.players.clear();
        this.playerOrder = [];
        this.currentPlayerIndex = 0;
        
        this.eventQueue = [];
        this.eventHistory = [];
        this.scheduledEvents.clear();
        
        this.triggers.clear();
        this.triggerHistory = [];

        return { success: true, message: '回合管理器已重置' };
    }

    // ============ AI辅助 ============

    /**
     * 获取AI建议
     */
    getAIAssist(playerId) {
        if (!this.config.aiAssistEnabled) {
            return { success: false, error: 'AI辅助未启用' };
        }

        const player = this.players.get(playerId);
        const phase = this.threeActStructure.getCurrentPhase();
        const state = this.threeActStructure.getFullState();

        const suggestions = this._generateSuggestions(phase, state, player);

        return {
            success: true,
            suggestions,
            phase,
            currentProgress: this.threeActStructure.generatePhaseReport()
        };
    }

    /**
     * 生成建议
     */
    _generateSuggestions(phase, state, player) {
        const suggestions = [];

        switch (phase) {
            case ActPhase.PROLOGUE:
                if (!state.phaseState.prologue.worldEstablished) {
                    suggestions.push({
                        type: 'world_building',
                        priority: 'high',
                        description: '建立世界观：定义场景、背景或设定'
                    });
                }
                if (!state.phaseState.prologue.mainQuestSet) {
                    suggestions.push({
                        type: 'quest_setting',
                        priority: 'high',
                        description: '设定主线任务：明确游戏目标'
                    });
                }
                if (state.phaseState.prologue.rulesDefined.length < 2) {
                    suggestions.push({
                        type: 'rule_defining',
                        priority: 'medium',
                        description: '定义游戏法则：设立规则或限制'
                    });
                }
                break;

            case ActPhase.CONFLICT:
                if (state.phaseState.conflict.enemies.length < 2) {
                    suggestions.push({
                        type: 'encounter_enemy',
                        priority: 'high',
                        description: '遭遇敌人：面对挑战或对手'
                    });
                }
                if (!state.phaseState.conflict.mainConflictDefined) {
                    suggestions.push({
                        type: 'define_conflict',
                        priority: 'high',
                        description: '明确主线冲突：推进剧情发展'
                    });
                }
                break;

            case ActPhase.CLIMAX:
                if (!state.phaseState.climax.finalBattleStarted) {
                    suggestions.push({
                        type: 'start_boss_battle',
                        priority: 'critical',
                        description: '开始最终决战：面对Boss'
                    });
                } else if (!state.phaseState.climax.bossDefeated) {
                    suggestions.push({
                        type: 'defeat_boss',
                        priority: 'critical',
                        description: '击败Boss：完成最终挑战'
                    });
                }
                break;
        }

        return suggestions;
    }
}

module.exports = {
    TurnManager,
    TurnState,
    EventType,
    TriggerType,
    ActPhase
};
