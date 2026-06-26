/**
 * ThreeActStructure - 三幕式游戏结构
 * 基于规则修改记录v1.3设计
 * 
 * 结构设计：
 * - 序幕 (Act 1): 1-3回合 - 玩家构筑世界观，设定法则，定出主线任务
 * - 破章 (Act 2): 3-5回合 - 围绕主线碰撞，敌人涌出
 * - 急章 (Act 3): 1-3回合 - Boss战阶段
 */

// 幕的阶段定义
const ActPhase = {
    PROLOGUE: 'prologue',   // 序幕
    CONFLICT: 'conflict',   // 破章
    CLIMAX: 'climax'        // 急章
};

// 阶段名称映射
const ActPhaseNames = {
    'prologue': '序幕',
    'conflict': '破章',
    'climax': '急章'
};

// 阶段描述
const ActPhaseDescriptions = {
    'prologue': '构筑世界观，设定法则，定出主线任务',
    'conflict': '围绕主线碰撞，敌人涌出',
    'climax': 'Boss战阶段，终极对决'
};

/**
 * 三幕式结构管理器
 */
class ThreeActStructure {
    constructor(config = {}) {
        this.config = {
            // 序幕回合范围
            prologueMinTurns: config.prologueMinTurns || 1,
            prologueMaxTurns: config.prologueMaxTurns || 3,
            
            // 破章回合范围
            conflictMinTurns: config.conflictMinTurns || 3,
            conflictMaxTurns: config.conflictMaxTurns || 5,
            
            // 急章回合范围
            climaxMinTurns: config.climaxMinTurns || 1,
            climaxMaxTurns: config.climaxMaxTurns || 3,
            
            // 阶段转换条件
            transitionConditions: config.transitionConditions || {
                prologueToConflict: 'world_established',      // 世界观确立
                conflictToClimax: 'main_conflict_defined',     // 主线冲突明确
                climaxToEnd: 'boss_defeated'                   // Boss被击败
            }
        };

        // 当前状态
        this.currentPhase = ActPhase.PROLOGUE;
        this.turnCount = 0;
        this.phaseTurnCount = 0;  // 当前阶段的回合数
        
        // 阶段状态追踪
        this.phaseState = {
            [ActPhase.PROLOGUE]: {
                worldEstablished: false,      // 世界观是否确立
                rulesDefined: [],             // 已定义的法则
                mainQuestSet: false,          // 主线任务是否设定
                mainQuest: null,              // 主线任务内容
                elements: []                  // 世界观元素
            },
            [ActPhase.CONFLICT]: {
                enemies: [],                  // 出现的敌人
                conflicts: [],                // 冲突事件
                mainConflictDefined: false,   // 主线冲突是否明确
                plotPoints: []                // 剧情点
            },
            [ActPhase.CLIMAX]: {
                boss: null,                   // Boss信息
                bossDefeated: false,          // Boss是否被击败
                finalBattleStarted: false,    // 最终战是否开始
                endings: []                   // 可能的结局
            }
        };

        // 事件回调
        this.callbacks = {
            onPhaseStart: null,
            onPhaseEnd: null,
            onTransition: null,
            onTurnEnd: null
        };
    }

    /**
     * 设置回调函数
     */
    setCallbacks(callbacks) {
        Object.assign(this.callbacks, callbacks);
    }

    /**
     * 获取当前阶段
     */
    getCurrentPhase() {
        return this.currentPhase;
    }

    /**
     * 获取阶段名称
     */
    getPhaseName(phase = this.currentPhase) {
        return ActPhaseNames[phase] || phase;
    }

    /**
     * 获取阶段描述
     */
    getPhaseDescription(phase = this.currentPhase) {
        return ActPhaseDescriptions[phase] || '';
    }

    /**
     * 获取当前阶段状态
     */
    getPhaseState(phase = this.currentPhase) {
        return this.phaseState[phase];
    }

    /**
     * 获取完整状态
     */
    getFullState() {
        return {
            currentPhase: this.currentPhase,
            phaseName: this.getPhaseName(),
            phaseDescription: this.getPhaseDescription(),
            totalTurns: this.turnCount,
            phaseTurns: this.phaseTurnCount,
            phaseState: this.phaseState,
            isComplete: this.currentPhase === ActPhase.CLIMAX && 
                        this.phaseState[ActPhase.CLIMAX].bossDefeated
        };
    }

    /**
     * 处理回合结束
     */
    endTurn(actions = {}) {
        this.turnCount++;
        this.phaseTurnCount++;

        // 根据当前阶段处理行为
        switch (this.currentPhase) {
            case ActPhase.PROLOGUE:
                this._processPrologueActions(actions);
                break;
            case ActPhase.CONFLICT:
                this._processConflictActions(actions);
                break;
            case ActPhase.CLIMAX:
                this._processClimaxActions(actions);
                break;
        }

        // 检查阶段转换
        const transition = this._checkTransition();

        // 触发回合结束回调
        if (this.callbacks.onTurnEnd) {
            this.callbacks.onTurnEnd({
                turn: this.turnCount,
                phase: this.currentPhase,
                phaseTurn: this.phaseTurnCount,
                transition
            });
        }

        return {
            turnCount: this.turnCount,
            phaseTurnCount: this.phaseTurnCount,
            phase: this.currentPhase,
            transition
        };
    }

    /**
     * 处理序幕阶段行为
     */
    _processPrologueActions(actions) {
        const state = this.phaseState[ActPhase.PROLOGUE];

        // 处理世界观建立
        if (actions.worldElement) {
            state.elements.push(actions.worldElement);
            if (state.elements.length >= 3) {
                state.worldEstablished = true;
            }
        }

        // 处理法则定义
        if (actions.rule) {
            state.rulesDefined.push(actions.rule);
        }

        // 处理主线任务设定
        if (actions.mainQuest) {
            state.mainQuest = actions.mainQuest;
            state.mainQuestSet = true;
        }
    }

    /**
     * 处理破章阶段行为
     */
    _processConflictActions(actions) {
        const state = this.phaseState[ActPhase.CONFLICT];

        // 处理敌人出现
        if (actions.enemy) {
            state.enemies.push(actions.enemy);
        }

        // 处理冲突事件
        if (actions.conflict) {
            state.conflicts.push(actions.conflict);
        }

        // 处理剧情点
        if (actions.plotPoint) {
            state.plotPoints.push(actions.plotPoint);
        }

        // 检查主线冲突是否明确
        if (state.enemies.length >= 2 && state.conflicts.length >= 2) {
            state.mainConflictDefined = true;
        }
    }

    /**
     * 处理急章阶段行为
     */
    _processClimaxActions(actions) {
        const state = this.phaseState[ActPhase.CLIMAX];

        // 处理Boss设定
        if (actions.boss && !state.boss) {
            state.boss = actions.boss;
            state.finalBattleStarted = true;
        }

        // 处理Boss被击败
        if (actions.bossDefeated) {
            state.bossDefeated = true;
        }

        // 处理结局
        if (actions.ending) {
            state.endings.push(actions.ending);
        }
    }

    /**
     * 检查阶段转换条件
     */
    _checkTransition() {
        const prologueState = this.phaseState[ActPhase.PROLOGUE];
        const conflictState = this.phaseState[ActPhase.CONFLICT];
        const climaxState = this.phaseState[ActPhase.CLIMAX];

        let shouldTransition = false;
        let fromPhase = this.currentPhase;
        let toPhase = null;
        let reason = '';

        switch (this.currentPhase) {
            case ActPhase.PROLOGUE:
                // 序幕结束条件：回合数达到且世界观确立
                if (this.phaseTurnCount >= this.config.prologueMinTurns &&
                    prologueState.worldEstablished && 
                    prologueState.mainQuestSet) {
                    shouldTransition = true;
                    toPhase = ActPhase.CONFLICT;
                    reason = '世界观已确立，主线任务已设定';
                }
                // 强制转换：达到最大回合数
                else if (this.phaseTurnCount >= this.config.prologueMaxTurns) {
                    shouldTransition = true;
                    toPhase = ActPhase.CONFLICT;
                    reason = '序幕回合上限已达成';
                }
                break;

            case ActPhase.CONFLICT:
                // 破章结束条件：回合数达到且主线冲突明确
                if (this.phaseTurnCount >= this.config.conflictMinTurns &&
                    conflictState.mainConflictDefined) {
                    shouldTransition = true;
                    toPhase = ActPhase.CLIMAX;
                    reason = '主线冲突已明确，准备最终决战';
                }
                // 强制转换：达到最大回合数
                else if (this.phaseTurnCount >= this.config.conflictMaxTurns) {
                    shouldTransition = true;
                    toPhase = ActPhase.CLIMAX;
                    reason = '破章回合上限已达成';
                }
                break;

            case ActPhase.CLIMAX:
                // 急章结束：Boss被击败
                if (climaxState.bossDefeated) {
                    shouldTransition = true;
                    toPhase = 'END';
                    reason = 'Boss已被击败，故事完结';
                }
                // 超时强制结束
                else if (this.phaseTurnCount >= this.config.climaxMaxTurns) {
                    shouldTransition = true;
                    toPhase = 'END';
                    reason = '急章回合上限已达成';
                }
                break;
        }

        if (shouldTransition && toPhase) {
            return this._executeTransition(fromPhase, toPhase, reason);
        }

        return null;
    }

    /**
     * 执行阶段转换
     */
    _executeTransition(fromPhase, toPhase, reason) {
        // 触发阶段结束回调
        if (this.callbacks.onPhaseEnd) {
            this.callbacks.onPhaseEnd({
                phase: fromPhase,
                turns: this.phaseTurnCount,
                state: this.phaseState[fromPhase]
            });
        }

        const transition = {
            from: fromPhase,
            to: toPhase,
            reason,
            turn: this.turnCount
        };

        // 更新当前阶段
        if (toPhase !== 'END') {
            this.currentPhase = toPhase;
            this.phaseTurnCount = 0;
        }

        // 触发转换回调
        if (this.callbacks.onTransition) {
            this.callbacks.onTransition(transition);
        }

        // 触发新阶段开始回调
        if (toPhase !== 'END' && this.callbacks.onPhaseStart) {
            this.callbacks.onPhaseStart({
                phase: toPhase,
                state: this.phaseState[toPhase]
            });
        }

        return transition;
    }

    /**
     * 手动触发阶段转换（GM干预）
     */
    forceTransition(toPhase, reason = 'GM干预') {
        return this._executeTransition(this.currentPhase, toPhase, reason);
    }

    /**
     * 添加世界观元素（不触发回合结束）
     */
    addWorldElement(element) {
        const state = this.phaseState[ActPhase.PROLOGUE];
        state.elements.push(element);
        if (state.elements.length >= 3) {
            state.worldEstablished = true;
        }
        return { success: true, element, worldEstablished: state.worldEstablished };
    }

    /**
     * 定义法则（不触发回合结束）
     */
    defineRule(rule) {
        this.phaseState[ActPhase.PROLOGUE].rulesDefined.push(rule);
        return { success: true, rule };
    }

    /**
     * 设定主线任务（不触发回合结束）
     */
    setMainQuest(quest) {
        const state = this.phaseState[ActPhase.PROLOGUE];
        state.mainQuest = quest;
        state.mainQuestSet = true;
        return { success: true, quest };
    }

    /**
     * 添加敌人（不触发回合结束）
     */
    addEnemy(enemy) {
        const state = this.phaseState[ActPhase.CONFLICT];
        state.enemies.push(enemy);
        return { success: true, enemy };
    }

    /**
     * 添加冲突事件（不触发回合结束）
     */
    addConflict(conflict) {
        this.phaseState[ActPhase.CONFLICT].conflicts.push(conflict);
        return { success: true, conflict };
    }

    /**
     * 设定Boss（不触发回合结束）
     */
    setBoss(boss) {
        const state = this.phaseState[ActPhase.CLIMAX];
        state.boss = boss;
        state.finalBattleStarted = true;
        return { success: true, boss };
    }

    /**
     * 击败Boss（不触发回合结束）
     */
    defeatBoss() {
        const state = this.phaseState[ActPhase.CLIMAX];
        state.bossDefeated = true;
        return { success: true, message: 'Boss已被击败' };
    }

    /**
     * 添加结局（不触发回合结束）
     */
    addEnding(ending) {
        this.phaseState[ActPhase.CLIMAX].endings.push(ending);
        return { success: true, ending };
    }

    /**
     * 生成阶段报告
     */
    generatePhaseReport() {
        const report = {
            phase: this.getPhaseName(),
            turn: `${this.phaseTurnCount}/${this._getMaxTurnsForPhase()}`,
            status: this.getPhaseState(),
            progress: this._calculatePhaseProgress(),
            nextMilestone: this._getNextMilestone()
        };

        return report;
    }

    /**
     * 获取当前阶段最大回合数
     */
    _getMaxTurnsForPhase() {
        switch (this.currentPhase) {
            case ActPhase.PROLOGUE:
                return this.config.prologueMaxTurns;
            case ActPhase.CONFLICT:
                return this.config.conflictMaxTurns;
            case ActPhase.CLIMAX:
                return this.config.climaxMaxTurns;
            default:
                return 0;
        }
    }

    /**
     * 计算阶段进度
     */
    _calculatePhaseProgress() {
        const maxTurns = this._getMaxTurnsForPhase();
        const turnProgress = (this.phaseTurnCount / maxTurns) * 100;

        let conditionProgress = 0;
        const state = this.phaseState[this.currentPhase];

        switch (this.currentPhase) {
            case ActPhase.PROLOGUE:
                conditionProgress = (
                    (state.worldEstablished ? 40 : state.elements.length * 13) +
                    (state.mainQuestSet ? 40 : 0) +
                    (state.rulesDefined.length > 0 ? 20 : 0)
                );
                break;
            case ActPhase.CONFLICT:
                conditionProgress = (
                    (state.mainConflictDefined ? 50 : Math.min(state.enemies.length * 10 + state.conflicts.length * 15, 50)) +
                    (state.plotPoints.length * 10)
                );
                break;
            case ActPhase.CLIMAX:
                conditionProgress = state.bossDefeated ? 100 : (state.finalBattleStarted ? 50 : 0);
                break;
        }

        return {
            turnProgress: Math.min(turnProgress, 100),
            conditionProgress: Math.min(conditionProgress, 100),
            overall: Math.min((turnProgress + conditionProgress) / 2, 100)
        };
    }

    /**
     * 获取下一个里程碑
     */
    _getNextMilestone() {
        const state = this.phaseState[this.currentPhase];

        switch (this.currentPhase) {
            case ActPhase.PROLOGUE:
                if (!state.worldEstablished) {
                    return '确立世界观 (需要更多世界观元素)';
                }
                if (!state.mainQuestSet) {
                    return '设定主线任务';
                }
                return '准备进入破章阶段';

            case ActPhase.CONFLICT:
                if (!state.mainConflictDefined) {
                    return '明确主线冲突 (需要更多敌人或冲突事件)';
                }
                return '准备进入急章阶段';

            case ActPhase.CLIMAX:
                if (!state.finalBattleStarted) {
                    return '开始最终决战';
                }
                if (!state.bossDefeated) {
                    return '击败Boss';
                }
                return '故事完结';

            default:
                return '未知里程碑';
        }
    }

    /**
     * 重置三幕式结构
     */
    reset(config = {}) {
        this.config = { ...this.config, ...config };
        this.currentPhase = ActPhase.PROLOGUE;
        this.turnCount = 0;
        this.phaseTurnCount = 0;
        this.phaseState = {
            [ActPhase.PROLOGUE]: {
                worldEstablished: false,
                rulesDefined: [],
                mainQuestSet: false,
                mainQuest: null,
                elements: []
            },
            [ActPhase.CONFLICT]: {
                enemies: [],
                conflicts: [],
                mainConflictDefined: false,
                plotPoints: []
            },
            [ActPhase.CLIMAX]: {
                boss: null,
                bossDefeated: false,
                finalBattleStarted: false,
                endings: []
            }
        };
        return { success: true, message: '三幕式结构已重置' };
    }
}

module.exports = {
    ThreeActStructure,
    ActPhase,
    ActPhaseNames,
    ActPhaseDescriptions
};
