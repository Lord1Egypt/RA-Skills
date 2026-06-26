/**
 * FlowEngine - 心流优化引擎
 * 基于"心流六大支柱"设计：
 * 1. 清晰目标 - 目标设定与追踪
 * 2. 即时反馈 - 行动反馈系统
 * 3. 挑战匹配 - 动态难度调整
 * 4. 深度沉浸 - 节奏控制
 * 5. 掌控感 - 玩家权限
 * 6. 自我消融 - 角色融合体验
 * 
 * v2.10.0 - 心流优化系统
 */

const { EventEmitter } = require('events');

// 心流状态
const FlowState = {
    FLOW: 'flow',           // 心流状态
    BORED: 'bored',        // 过于简单，无聊
    ANXIETY: 'anxiety',    // 过于困难，焦虑
    CONTROL: 'control',    // 掌控状态
    OVERWHELM: 'overwhelm' // 失控状态
};

// 挑战等级
const ChallengeLevel = {
    EASY: 1,
    NORMAL: 2,
    HARD: 3,
    EXPERT: 4,
    MASTER: 5
};

// 反馈类型
const FeedbackType = {
    ACHIEVEMENT: 'achievement',
    REWARD: 'reward',
    HINT: 'hint',
    PROGRESS: 'progress',
    ENCOURAGEMENT: 'encouragement',
    CHALLENGE: 'challenge',
    MASTERY: 'mastery'
};

class Achievement {
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.description = config.description;
        this.category = config.category || 'general';
        this.condition = config.condition;
        this.rewards = config.rewards || [];
        this.icon = config.icon || '🏆';
        this.rarity = config.rarity || 'common'; // common, rare, epic, legendary
        this.maxProgress = config.maxProgress || 1;
        this.cooldown = config.cooldown || 0;
    }

    checkProgress(state) {
        if (!this.condition) return { completed: false, progress: 0 };
        return this.condition(state);
    }
}

class Reward {
    constructor(config) {
        this.id = config.id;
        this.type = config.type; // exp, item, title, ability, points
        this.value = config.value;
        this.name = config.name;
        this.description = config.description;
    }

    apply(target) {
        switch (this.type) {
            case 'exp':
                target.exp = (target.exp || 0) + this.value;
                break;
            case 'points':
                target.points = (target.points || 0) + this.value;
                break;
            case 'item':
                target.inventory = target.inventory || [];
                target.inventory.push(this.value);
                break;
            case 'title':
                target.titles = target.titles || [];
                if (!target.titles.includes(this.value)) {
                    target.titles.push(this.value);
                }
                break;
            case 'ability':
                target.abilities = target.abilities || [];
                if (!target.abilities.includes(this.value)) {
                    target.abilities.push(this.value);
                }
                break;
        }
        return { applied: true, reward: this };
    }
}

class Hint {
    constructor(config) {
        this.id = config.id;
        this.content = config.content;
        this.type = config.type; // direction, tip, warning, lore
        this.priority = config.priority || 1;
        this.context = config.context || [];
    }

    getDisplay() {
        const icons = {
            direction: '➡️',
            tip: '💡',
            warning: '⚠️',
            lore: '📜'
        };
        return `${icons[this.type] || '💡'} ${this.content}`;
    }
}

class FlowEngine extends EventEmitter {
    constructor() {
        super();
        
        // 心流状态
        this.currentState = FlowState.CONTROL;
        this.flowScore = 0; // -100 到 100
        
        // 挑战平衡
        this.playerSkillLevel = 5; // 玩家技能等级 (1-10)
        this.currentChallengeLevel = 3; // 当前挑战等级
        this.challengeHistory = []; // 挑战历史
        
        // 目标系统
        this.currentGoal = null;
        this.goalStack = [];
        this.goalProgress = 0;
        
        // 反馈系统
        this.achievements = new Map();
        this.rewards = new Map();
        this.hints = new Map();
        this.recentFeedbacks = [];
        
        // 沉浸系统
        this.immersionLevel = 0;
        this.immersionModifiers = {
            narrative: 0,
            challenge: 0,
            choice: 0,
            roleplay: 0
        };
        
        // 节奏控制
        this.pacingState = 'normal'; // slow, normal, fast, intense
        this.pacingModifiers = [];
        this.intensityCurve = [];
        
        // 角色融合
        this.characterFusion = {
            level: 0,
            roleImmersion: 0,
            emotionalInvestment: 0,
            identityBlurring: 0
        };
        
        // 玩家状态追踪
        this.playerState = {
            actions: [],
            successes: 0,
            failures: 0,
            totalActions: 0,
            lastActionTime: Date.now(),
            sessionStartTime: Date.now()
        };
        
        // 初始化内置成就和奖励
        this._initBuiltInAchievements();
        this._initBuiltInRewards();
        this._initBuiltInHints();
    }

    // 初始化内置成就
    _initBuiltInAchievements() {
        const builtInAchievements = [
            // 目标类成就
            {
                id: 'first_goal',
                name: '初立目标',
                description: '完成第一个目标',
                category: 'goal',
                icon: '🎯',
                rarity: 'common',
                condition: (state) => ({ completed: state.goalsCompleted >= 1, progress: state.goalsCompleted })
            },
            {
                id: 'goal_getter',
                name: '目标达人',
                description: '完成5个目标',
                category: 'goal',
                icon: '🎯',
                rarity: 'rare',
                condition: (state) => ({ completed: state.goalsCompleted >= 5, progress: state.goalsCompleted })
            },
            // 反馈类成就
            {
                id: 'first_feedback',
                name: '初获反馈',
                description: '获得第一次即时反馈',
                category: 'feedback',
                icon: '📣',
                rarity: 'common',
                condition: (state) => ({ completed: state.feedbacksReceived >= 1, progress: state.feedbacksReceived })
            },
            // 挑战类成就
            {
                id: 'challenge_seeker',
                name: '挑战者',
                description: '完成一次困难挑战',
                category: 'challenge',
                icon: '⚔️',
                rarity: 'common',
                condition: (state) => ({ completed: state.hardChallengesCompleted >= 1, progress: state.hardChallengesCompleted })
            },
            {
                id: 'master_challenger',
                name: '大师挑战者',
                description: '完成一次大师级挑战',
                category: 'challenge',
                icon: '👑',
                rarity: 'legendary',
                condition: (state) => ({ completed: state.masterChallengesCompleted >= 1, progress: state.masterChallengesCompleted })
            },
            // 沉浸类成就
            {
                id: 'immersed',
                name: '沉浸其中',
                description: '达到深度沉浸状态',
                category: 'immersion',
                icon: '🌊',
                rarity: 'rare',
                condition: (state) => ({ completed: state.immersionLevel >= 8, progress: state.immersionLevel })
            },
            // 角色融合类成就
            {
                id: '角色融合',
                name: '角色融合',
                description: '与角色产生深度共鸣',
                category: 'fusion',
                icon: '🎭',
                rarity: 'epic',
                condition: (state) => ({ completed: state.characterFusion >= 7, progress: state.characterFusion })
            },
            // 连续成功类成就
            {
                id: 'streak_3',
                name: '三连胜',
                description: '连续3次成功行动',
                category: 'mastery',
                icon: '🔥',
                rarity: 'common',
                condition: (state) => ({ completed: state.maxSuccessStreak >= 3, progress: state.maxSuccessStreak })
            },
            {
                id: 'streak_5',
                name: '五连胜',
                description: '连续5次成功行动',
                category: 'mastery',
                icon: '💥',
                rarity: 'rare',
                condition: (state) => ({ completed: state.maxSuccessStreak >= 5, progress: state.maxSuccessStreak })
            },
            {
                id: 'streak_10',
                name: '十连胜',
                description: '连续10次成功行动',
                category: 'mastery',
                icon: '🌟',
                rarity: 'legendary',
                condition: (state) => ({ completed: state.maxSuccessStreak >= 10, progress: state.maxSuccessStreak })
            }
        ];

        builtInAchievements.forEach(ach => {
            this.achievements.set(ach.id, new Achievement(ach));
        });
    }

    // 初始化内置奖励
    _initBuiltInRewards() {
        const builtInRewards = [
            { id: 'exp_10', type: 'exp', value: 10, name: '经验+10', description: '获得10点经验' },
            { id: 'exp_50', type: 'exp', value: 50, name: '经验+50', description: '获得50点经验' },
            { id: 'exp_100', type: 'exp', value: 100, name: '经验+100', description: '获得100点经验' },
            { id: 'points_100', type: 'points', value: 100, name: '积分+100', description: '获得100点积分' },
            { id: 'title_novice', type: 'title', value: '初学者', name: '称号：初学者', description: '获得初学者称号' },
            { id: 'title_challenger', type: 'title', value: '挑战者', name: '称号：挑战者', description: '获得挑战者称号' },
            { id: 'title_master', type: 'title', value: '大师', name: '称号：大师', description: '获得大师称号' },
            { id: 'ability_focus', type: 'ability', value: '专注', name: '能力：专注', description: '获得专注能力' },
            { id: 'ability_adapt', type: 'ability', value: '适应', name: '能力：适应', description: '获得适应能力' }
        ];

        builtInRewards.forEach(rew => {
            this.rewards.set(rew.id, new Reward(rew));
        });
    }

    // 初始化内置提示
    _initBuiltInHints() {
        const builtInHints = [
            { id: 'hint_goal', content: '明确的目标是进入心流的关键', type: 'tip', context: ['goal'] },
            { id: 'hint_challenge', content: '当前挑战可能太简单了，尝试更高难度', type: 'direction', context: ['bored'] },
            { id: 'hint_easier', content: '如果感到困难，可以先尝试简单一些的挑战', type: 'direction', context: ['anxiety'] },
            { id: 'hint_immersion', content: '尝试更深入地融入角色，感受他们的情感', type: 'tip', context: ['immersion'] },
            { id: 'hint_pacing', content: '注意节奏变化，适时调整挑战难度', type: 'warning', context: ['pacing'] },
            { id: 'hint_story', content: '关注剧情发展，每个选择都有意义', type: 'lore', context: ['narrative'] }
        ];

        builtInHints.forEach(hint => {
            this.hints.set(hint.id, new Hint(hint));
        });
    }

    // ============ 清晰目标系统 ============

    /**
     * 设置当前目标
     * @param {Object} goal - 目标配置
     * @param {string} goal.id - 目标ID
     * @param {string} goal.name - 目标名称
     * @param {string} goal.description - 目标描述
     * @param {number} goal.total - 目标总量
     * @param {string} goal.type - 目标类型 (main/side/challenge)
     */
    setGoal(goal) {
        const newGoal = {
            id: goal.id || `goal_${Date.now()}`,
            name: goal.name,
            description: goal.description,
            type: goal.type || 'main',
            total: goal.total || 1,
            progress: 0,
            createdAt: Date.now(),
            completedAt: null,
            rewards: goal.rewards || []
        };
        
        this.currentGoal = newGoal;
        this.goalStack.push(newGoal);
        
        this._updateFlowState();
        this.emit('goal:set', newGoal);
        
        return {
            success: true,
            goal: newGoal,
            message: `🎯 目标已设定: ${newGoal.name}`
        };
    }

    /**
     * 更新目标进度
     * @param {number} amount - 进度增量
     */
    updateGoalProgress(amount = 1) {
        if (!this.currentGoal) {
            return { error: '没有当前目标' };
        }

        this.currentGoal.progress += amount;
        this.goalProgress = this.currentGoal.progress / this.currentGoal.total;
        
        const completed = this.currentGoal.progress >= this.currentGoal.total;
        
        if (completed) {
            this.currentGoal.completedAt = Date.now();
            this._completeGoal();
        }
        
        this._updateFlowState();
        this.emit('goal:progress', { 
            goal: this.currentGoal, 
            progress: this.goalProgress,
            completed 
        });
        
        return {
            success: true,
            goal: this.currentGoal,
            progress: this.goalProgress,
            completed
        };
    }

    /**
     * 完成任务
     */
    _completeGoal() {
        const goal = this.currentGoal;
        
        // 发放奖励
        if (goal.rewards && goal.rewards.length > 0) {
            goal.rewards.forEach(rewardId => {
                const reward = this.rewards.get(rewardId);
                if (reward) {
                    this._giveReward(reward);
                }
            });
        }
        
        // 检查成就
        this._checkAchievements();
        
        this.emit('goal:completed', goal);
    }

    /**
     * 清除当前目标
     */
    clearGoal() {
        const goal = this.currentGoal;
        this.currentGoal = null;
        this.goalProgress = 0;
        
        this.emit('goal:cleared', goal);
        
        return { success: true, message: '目标已清除' };
    }

    /**
     * 获取目标状态
     */
    getGoalStatus() {
        if (!this.currentGoal) {
            return { active: false };
        }
        
        return {
            active: true,
            goal: this.currentGoal,
            progress: this.goalProgress,
            progressPercent: Math.round(this.goalProgress * 100)
        };
    }

    // ============ 即时反馈系统 ============

    /**
     * 记录玩家行动并生成反馈
     * @param {Object} action - 行动数据
     * @param {string} action.type - 行动类型
     * @param {boolean} action.success - 是否成功
     * @param {number} action.value - 行动价值
     */
    recordAction(action) {
        this.playerState.actions.push({
            ...action,
            timestamp: Date.now()
        });
        
        this.playerState.totalActions++;
        
        if (action.success) {
            this.playerState.successes++;
            this.playerState.lastSuccessTime = Date.now();
        } else {
            this.playerState.failures++;
        }
        
        // 计算连击
        this._updateStreak(action.success);
        
        // 生成反馈
        const feedback = this._generateFeedback(action);
        
        // 添加到最近反馈
        this.recentFeedbacks.push(feedback);
        if (this.recentFeedbacks.length > 20) {
            this.recentFeedbacks.shift();
        }
        
        // 检查成就
        this._checkAchievements();
        
        // 更新心流状态
        this._updateFlowState();
        
        this.emit('action:recorded', { action, feedback });
        
        return {
            action,
            feedback,
            flowState: this.currentState,
            flowScore: this.flowScore
        };
    }

    /**
     * 更新连击
     */
    _updateStreak(success) {
        if (!this.playerState.currentStreak) {
            this.playerState.currentStreak = 0;
        }
        
        if (success) {
            this.playerState.currentStreak++;
            if (!this.playerState.maxSuccessStreak || 
                this.playerState.currentStreak > this.playerState.maxSuccessStreak) {
                this.playerState.maxSuccessStreak = this.playerState.currentStreak;
            }
        } else {
            this.playerState.currentStreak = 0;
        }
    }

    /**
     * 生成反馈
     */
    _generateFeedback(action) {
        const feedbacks = [];
        
        // 基于成功/失败生成反馈
        if (action.success) {
            // 成功反馈
            if (action.value >= 10) {
                feedbacks.push(this._createFeedback(FeedbackType.MASTERY, 
                    `精彩！获得了 ${action.value} 点收获！`));
            } else if (action.value >= 5) {
                feedbacks.push(this._createFeedback(FeedbackType.REWARD, 
                    `干得好！+${action.value}`));
            } else {
                feedbacks.push(this._createFeedback(FeedbackType.PROGRESS, 
                    '进展顺利'));
            }
            
            // 检查是否触发成就
            const achievements = this._checkAchievements(true);
            achievements.forEach(ach => {
                feedbacks.push(this._createFeedback(FeedbackType.ACHIEVEMENT, 
                    `🏆 成就解锁: ${ach.name}`));
            });
            
        } else {
            // 失败反馈
            if (this.playerState.currentStreak >= 3) {
                feedbacks.push(this._createFeedback(FeedbackType.ENCOURAGEMENT, 
                    '遇到挫折是正常的，继续加油！'));
            } else {
                // 根据当前状态提供提示
                if (this.currentState === FlowState.ANXIETY) {
                    const hint = this._getContextualHint('anxiety');
                    if (hint) feedbacks.push(hint);
                } else if (this.currentState === FlowState.BORED) {
                    const hint = this._getContextualHint('bored');
                    if (hint) feedbacks.push(hint);
                }
            }
        }
        
        // 检查心流状态变化
        if (this.flowScore > 50) {
            feedbacks.push(this._createFeedback(FeedbackType.CHALLENGE, 
                '🌊 状态火热！进入心流状态！'));
        }
        
        return feedbacks;
    }

    /**
     * 创建反馈对象
     */
    _createFeedback(type, content) {
        return {
            id: `fb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type,
            content,
            timestamp: Date.now()
        };
    }

    /**
     * 获取上下文提示
     */
    _getContextualHint(context) {
        for (const [id, hint] of this.hints) {
            if (hint.context.includes(context)) {
                return this._createFeedback(FeedbackType.HINT, hint.getDisplay());
            }
        }
        return null;
    }

    /**
     * 获取最近反馈
     */
    getRecentFeedbacks(count = 5) {
        return this.recentFeedbacks.slice(-count);
    }

    // ============ 挑战匹配系统（动态难度调整） ============

    /**
     * 设置玩家技能等级
     * @param {number} level - 技能等级 (1-10)
     */
    setSkillLevel(level) {
        this.playerSkillLevel = Math.min(10, Math.max(1, level));
        this._updateFlowState();
        
        return {
            success: true,
            skillLevel: this.playerSkillLevel,
            message: `技能等级设定为 ${this.playerSkillLevel}`
        };
    }

    /**
     * 设置挑战等级
     * @param {number} level - 挑战等级 (1-5)
     */
    setChallengeLevel(level) {
        this.currentChallengeLevel = Math.min(5, Math.max(1, level));
        this.challengeHistory.push({
            level: this.currentChallengeLevel,
            timestamp: Date.now()
        });
        
        this._updateFlowState();
        
        return {
            success: true,
            challengeLevel: this.currentChallengeLevel,
            message: `挑战等级设定为 ${this._getChallengeLevelName(this.currentChallengeLevel)}`
        };
    }

    /**
     * 获取挑战等级名称
     */
    _getChallengeLevelName(level) {
        const names = {
            1: '简单',
            2: '普通',
            3: '困难',
            4: '专家',
            5: '大师'
        };
        return names[level] || '未知';
    }

    /**
     * 智能调整难度
     * 基于玩家表现自动调整挑战难度
     */
    autoAdjustDifficulty() {
        if (this.playerState.totalActions < 3) {
            return { message: '数据不足，无法自动调整' };
        }
        
        const successRate = this.playerState.successes / this.playerState.totalActions;
        let newLevel = this.currentChallengeLevel;
        let message = '';
        
        if (successRate > 0.8 && this.currentChallengeLevel < 5) {
            // 连续成功，提高难度
            newLevel++;
            message = '表现优秀！挑战升级！';
        } else if (successRate < 0.4 && this.currentChallengeLevel > 1) {
            // 连续失败，降低难度
            newLevel--;
            message = '难度降低，更好地享受游戏！';
        } else {
            message = '当前难度适中';
        }
        
        if (newLevel !== this.currentChallengeLevel) {
            return this.setChallengeLevel(newLevel);
        }
        
        return {
            success: true,
            challengeLevel: this.currentChallengeLevel,
            message,
            successRate: Math.round(successRate * 100) + '%'
        };
    }

    /**
     * 获取难度建议
     */
    getDifficultySuggestion() {
        const diff = this.currentChallengeLevel - this.playerSkillLevel;
        
        if (diff > 1) {
            return {
                suggestion: 'lower',
                message: '建议降低难度',
                reason: '挑战对你来说太难了'
            };
        } else if (diff < -1) {
            return {
                suggestion: 'higher',
                message: '建议提高难度',
                reason: '你可以尝试更高难度'
            };
        } else {
            return {
                suggestion: 'maintain',
                message: '当前难度合适',
                reason: '挑战与你的技能相匹配'
            };
        }
    }

    // ============ 深度沉浸系统（节奏控制） ============

    /**
     * 设置沉浸等级
     * @param {number} level - 沉浸等级 (0-10)
     */
    setImmersionLevel(level) {
        this.immersionLevel = Math.min(10, Math.max(0, level));
        
        this.emit('immersion:changed', { level: this.immersionLevel });
        
        return {
            success: true,
            immersionLevel: this.immersionLevel,
            message: this._getImmersionMessage()
        };
    }

    /**
     * 获取沉浸状态消息
     */
    _getImmersionMessage() {
        if (this.immersionLevel >= 8) {
            return '🌊 深度沉浸！完全投入到游戏世界中';
        } else if (this.immersionLevel >= 5) {
            return '💫 良好沉浸感';
        } else if (this.immersionLevel >= 3) {
            return '🌤️ 初步进入状态';
        } else {
            return '💤 需要更多沉浸元素';
        }
    }

    /**
     * 添加沉浸修饰器
     * @param {string} type - 类型 (narrative/challenge/choice/roleplay)
     * @param {number} value - 修饰值
     */
    addImmersionModifier(type, value) {
        if (this.immersionModifiers[type] !== undefined) {
            this.immersionModifiers[type] += value;
            this.immersionModifiers[type] = Math.min(10, Math.max(0, this.immersionModifiers[type]));
        }
        
        // 重新计算总沉浸等级
        const modifiers = Object.values(this.immersionModifiers);
        this.immersionLevel = Math.round(modifiers.reduce((a, b) => a + b, 0) / modifiers.length);
        
        return {
            success: true,
            modifiers: this.immersionModifiers,
            immersionLevel: this.immersionLevel
        };
    }

    /**
     * 设置节奏状态
     * @param {string} state - 节奏状态 (slow/normal/fast/intense)
     */
    setPacing(state) {
        const validStates = ['slow', 'normal', 'fast', 'intense'];
        if (!validStates.includes(state)) {
            return { error: '无效的节奏状态' };
        }
        
        this.pacingState = state;
        
        this.emit('pacing:changed', { state });
        
        return {
            success: true,
            pacing: state,
            message: `节奏已调整为: ${this._getPacingName(state)}`
        };
    }

    /**
     * 获取节奏名称
     */
    _getPacingName(state) {
        const names = {
            slow: '缓慢',
            normal: '正常',
            fast: '快速',
            intense: '紧张'
        };
        return names[state] || '未知';
    }

    /**
     * 获取节奏建议
     */
    getPacingSuggestion() {
        // 基于当前心流状态建议节奏
        if (this.currentState === FlowState.ANXIETY) {
            return { suggestion: 'slow', message: '放缓节奏，让玩家有时间思考' };
        } else if (this.currentState === FlowState.BORED) {
            return { suggestion: 'intense', message: '加快节奏，增加紧张感' };
        } else if (this.currentState === FlowState.FLOW) {
            return { suggestion: 'maintain', message: '保持当前节奏' };
        }
        
        return { suggestion: 'normal', message: '正常节奏' };
    }

    // ============ 掌控感系统 ============

    /**
     * 检查并更新掌控感
     */
    updateControlSense() {
        // 基于成功率和选择权评估掌控感
        const successRate = this.playerState.totalActions > 0 
            ? this.playerState.successes / this.playerState.totalActions 
            : 0.5;
        
        const controlScore = successRate * 0.7 + (this.playerSkillLevel / 10) * 0.3;
        
        if (controlScore > 0.7) {
            this.currentState = FlowState.CONTROL;
        } else if (controlScore < 0.3) {
            this.currentState = FlowState.OVERWHELM;
        }
        
        return {
            controlScore: Math.round(controlScore * 100) + '%',
            state: this.currentState
        };
    }

    /**
     * 提供选择权
     * @param {Array} choices - 选项列表
     */
    presentChoices(choices) {
        // 增加沉浸修饰
        this.addImmersionModifier('choice', 0.5);
        
        return {
            success: true,
            choices,
            message: `你有 ${choices.length} 个选择`
        };
    }

    // ============ 自我消融系统（角色融合） ============

    /**
     * 增加角色融合度
     * @param {number} amount - 融合增量
     */
    increaseCharacterFusion(amount = 1) {
        this.characterFusion.level = Math.min(10, this.characterFusion.level + amount);
        this.characterFusion.roleImmersion = Math.min(10, this.characterFusion.roleImmersion + amount);
        
        this.emit('fusion:increased', { fusion: this.characterFusion });
        
        return {
            success: true,
            fusion: this.characterFusion,
            message: this._getFusionMessage()
        };
    }

    /**
     * 获取融合状态消息
     */
    _getFusionMessage() {
        const level = this.characterFusion.level;
        
        if (level >= 8) {
            return '🎭 你已与角色融为一体';
        } else if (level >= 5) {
            return '🎭 你正在深入理解角色';
        } else if (level >= 2) {
            return '🎭 你开始感受角色的情感';
        } else {
            return '🎭 你还在适应角色';
        }
    }

    /**
     * 记录角色扮演事件
     * @param {Object} event - 扮演事件
     */
    recordRoleplayEvent(event) {
        this.characterFusion.emotionalInvestment += 0.5;
        this.characterFusion.identityBlurring += 0.3;
        
        // 触发沉浸提升
        this.addImmersionModifier('roleplay', 0.5);
        
        return {
            success: true,
            fusion: this.characterFusion
        };
    }

    /**
     * 获取角色融合状态
     */
    getCharacterFusionStatus() {
        return {
            level: this.characterFusion.level,
            roleImmersion: this.characterFusion.roleImmersion,
            emotionalInvestment: this.characterFusion.emotionalInvestment,
            identityBlurring: this.characterFusion.identityBlurring,
            description: this._getFusionMessage()
        };
    }

    // ============ 成就系统 ============

    /**
     * 注册成就
     * @param {Object} achievementConfig - 成就配置
     */
    registerAchievement(achievementConfig) {
        const achievement = new Achievement(achievementConfig);
        this.achievements.set(achievement.id, achievement);
        
        return {
            success: true,
            achievement: achievement,
            message: `成就 "${achievement.name}" 已注册`
        };
    }

    /**
     * 检查成就（内部方法）
     * @param {boolean} justCheck - 是否仅检查不解锁
     */
    _checkAchievements(justCheck = false) {
        const unlocked = [];
        
        // 构建玩家状态快照
        const stateSnapshot = {
            goalsCompleted: this.goalStack.filter(g => g.completedAt).length,
            feedbacksReceived: this.recentFeedbacks.length,
            hardChallengesCompleted: this.challengeHistory.filter(c => c.level >= 3).length,
            masterChallengesCompleted: this.challengeHistory.filter(c => c.level >= 5).length,
            immersionLevel: this.immersionLevel,
            characterFusion: this.characterFusion.level,
            maxSuccessStreak: this.playerState.maxSuccessStreak || 0
        };
        
        for (const [id, achievement] of this.achievements) {
            if (achievement.maxProgress > 1) {
                // 有进度的成就
                const result = achievement.checkProgress(stateSnapshot);
                if (!justCheck && result.completed && !achievement.unlocked) {
                    achievement.unlocked = true;
                    achievement.unlockedAt = Date.now();
                    unlocked.push(achievement);
                    this.emit('achievement:unlocked', achievement);
                }
            } else {
                // 一次性成就
                if (!achievement.unlocked) {
                    const result = achievement.checkProgress(stateSnapshot);
                    if (result.completed) {
                        achievement.unlocked = true;
                        achievement.unlockedAt = Date.now();
                        unlocked.push(achievement);
                        this.emit('achievement:unlocked', achievement);
                    }
                }
            }
        }
        
        return unlocked;
    }

    /**
     * 解锁成就
     * @param {string} achievementId - 成就ID
     */
    unlockAchievement(achievementId) {
        const achievement = this.achievements.get(achievementId);
        
        if (!achievement) {
            return { error: '成就不存在' };
        }
        
        if (achievement.unlocked) {
            return { message: '成就已解锁' };
        }
        
        achievement.unlocked = true;
        achievement.unlockedAt = Date.now();
        
        // 发放奖励
        achievement.rewards.forEach(rewardId => {
            const reward = this.rewards.get(rewardId);
            if (reward) {
                this._giveReward(reward);
            }
        });
        
        this.emit('achievement:unlocked', achievement);
        
        return {
            success: true,
            achievement: achievement,
            message: `🏆 成就解锁: ${achievement.name}`
        };
    }

    /**
     * 发放奖励
     */
    _giveReward(reward) {
        // 通知奖励发放
        this.emit('reward:given', reward);
        
        return {
            success: true,
            reward: reward
        };
    }

    /**
     * 列出所有成就
     */
    listAchievements() {
        const list = [];
        for (const [id, achievement] of this.achievements) {
            list.push({
                id: achievement.id,
                name: achievement.name,
                description: achievement.description,
                category: achievement.category,
                icon: achievement.icon,
                rarity: achievement.rarity,
                unlocked: achievement.unlocked || false
            });
        }
        return list;
    }

    /**
     * 获取已解锁成就
     */
    getUnlockedAchievements() {
        return this.listAchievements().filter(a => a.unlocked);
    }

    // ============ 心流状态管理 ============

    /**
     * 更新心流状态
     */
    _updateFlowState() {
        // 计算心流分数
        const skillDiff = this.currentChallengeLevel - this.playerSkillLevel;
        const successRate = this.playerState.totalActions > 0 
            ? this.playerState.successes / this.playerState.totalActions 
            : 0.5;
        
        // 心流条件：技能与挑战相匹配
        let newFlowScore = 0;
        
        if (Math.abs(skillDiff) <= 1) {
            // 技能与挑战匹配
            newFlowScore = 50 + successRate * 50;
        } else if (skillDiff > 1) {
            // 挑战过高
            newFlowScore = 20 + successRate * 30;
        } else {
            // 挑战过低
            newFlowScore = successRate * 60;
        }
        
        // 考虑沉浸度
        newFlowScore += (this.immersionLevel - 5) * 2;
        
        // 考虑角色融合
        newFlowScore += this.characterFusion.level * 1.5;
        
        // 限制范围
        this.flowScore = Math.min(100, Math.max(-100, newFlowScore));
        
        // 确定状态
        const prevState = this.currentState;
        
        if (this.flowScore >= 60) {
            this.currentState = FlowState.FLOW;
        } else if (this.flowScore <= -20) {
            this.currentState = FlowState.ANXIETY;
        } else if (this.currentChallengeLevel < this.playerSkillLevel - 1) {
            this.currentState = FlowState.BORED;
        } else if (this.currentChallengeLevel > this.playerSkillLevel + 1) {
            this.currentState = FlowState.ANXIETY;
        } else {
            this.currentState = FlowState.CONTROL;
        }
        
        if (prevState !== this.currentState) {
            this.emit('flow:stateChanged', { 
                from: prevState, 
                to: this.currentState,
                flowScore: this.flowScore
            });
        }
    }

    /**
     * 获取心流状态
     */
    getFlowState() {
        const successRate = this.playerState.totalActions > 0 
            ? this.playerState.successes / this.playerState.totalActions 
            : 0;
            
        return {
            state: this.currentState,
            flowScore: Math.round(this.flowScore),
            description: this._getStateDescription(),
            skillLevel: this.playerSkillLevel,
            challengeLevel: this.currentChallengeLevel,
            immersionLevel: this.immersionLevel,
            successRate: Math.round(successRate * 100) + '%',
            characterFusion: this.characterFusion.level
        };
    }

    /**
     * 获取状态描述
     */
    _getStateDescription() {
        switch (this.currentState) {
            case FlowState.FLOW:
                return '🌊 处于心流状态，完全沉浸';
            case FlowState.BORED:
                return '😐 挑战不足，稍感无聊';
            case FlowState.ANXIETY:
                return '😰 挑战过高，感到焦虑';
            case FlowState.CONTROL:
                return '🎮 处于掌控状态';
            case FlowState.OVERWHELM:
                return '😵 状态失控，需要调整';
            default:
                return '状态未知';
        }
    }

    // ============ 提示系统 ============

    /**
     * 添加提示
     * @param {Object} hintConfig - 提示配置
     */
    addHint(hintConfig) {
        const hint = new Hint(hintConfig);
        this.hints.set(hint.id, hint);
        
        return {
            success: true,
            hint: hint,
            message: `提示 "${hint.content}" 已添加`
        };
    }

    /**
     * 获取提示
     * @param {string} context - 上下文
     */
    getHint(context = null) {
        for (const [id, hint] of this.hints) {
            if (!context || hint.context.includes(context)) {
                return {
                    success: true,
                    hint: hint,
                    display: hint.getDisplay()
                };
            }
        }
        return { message: '暂无提示' };
    }

    /**
     * 列出所有提示
     */
    listHints() {
        const list = [];
        for (const [id, hint] of this.hints) {
            list.push({
                id: hint.id,
                content: hint.content,
                type: hint.type,
                context: hint.context,
                display: hint.getDisplay()
            });
        }
        return list;
    }

    // ============ 系统集成方法 ============

    /**
     * 关联三幕式结构
     * @param {Object} threeActStructure - 三幕式结构实例
     */
    linkThreeActStructure(threeActStructure) {
        this.threeActStructure = threeActStructure;
        
        // 监听三幕式阶段变化
        if (threeActStructure.on) {
            threeActStructure.on('phaseChanged', (data) => {
                // 根据阶段调整节奏
                switch (data.to) {
                    case 'prologue':
                        this.setPacing('slow');
                        break;
                    case 'conflict':
                        this.setPacing('fast');
                        break;
                    case 'climax':
                        this.setPacing('intense');
                        break;
                }
            });
        }
        
        return { success: true, message: '已关联三幕式结构' };
    }

    /**
     * 关联角色系统
     * @param {Object} characterSystem - 角色系统实例
     */
    linkCharacterSystem(characterSystem) {
        this.characterSystem = characterSystem;
        
        return { success: true, message: '已关联角色系统' };
    }

    /**
     * 关联战斗系统
     * @param {Object} combatSystem - 战斗系统实例
     */
    linkCombatSystem(combatSystem) {
        this.combatSystem = combatSystem;
        
        // 战斗系统会影响挑战等级
        return { success: true, message: '已关联战斗系统' };
    }

    /**
     * 关联卡牌系统
     * @param {Object} cardSystem - 卡牌系统实例
     */
    linkCardSystem(cardSystem) {
        this.cardSystem = cardSystem;
        
        return { success: true, message: '已关联卡牌系统' };
    }

    // ============ 统计和报告 ============

    /**
     * 获取完整状态
     */
    getFullState() {
        return {
            flow: this.getFlowState(),
            goal: this.getGoalStatus(),
            player: {
                skillLevel: this.playerSkillLevel,
                totalActions: this.playerState.totalActions,
                successes: this.playerState.successes,
                failures: this.playerState.failures,
                currentStreak: this.playerState.currentStreak,
                maxSuccessStreak: this.playerState.maxSuccessStreak
            },
            immersion: {
                level: this.immersionLevel,
                modifiers: this.immersionModifiers,
                pacing: this.pacingState
            },
            fusion: this.getCharacterFusionStatus(),
            achievements: {
                total: this.achievements.size,
                unlocked: this.getUnlockedAchievements().length
            }
        };
    }

    /**
     * 生成心流报告
     */
    generateReport() {
        const state = this.getFullState();
        
        return {
            title: '🌊 心流状态报告',
            timestamp: new Date().toISOString(),
            summary: {
                flowState: state.flow.state,
                flowScore: state.flow.flowScore,
                description: state.flow.description
            },
            details: {
                '目标进度': state.goal.active 
                    ? `${state.goal.goal.name} (${state.goal.progressPercent}%)`
                    : '无当前目标',
                '技能等级': state.player.skillLevel,
                '挑战等级': `${this.currentChallengeLevel} (${this._getChallengeLevelName(this.currentChallengeLevel)})`,
                '沉浸度': `${state.immersion.level}/10`,
                '角色融合': `${state.fusion.level}/10`,
                '节奏状态': this._getPacingName(state.immersion.pacing),
                '成功率': state.flow.successRate,
                '成就进度': `${state.achievements.unlocked}/${state.achievements.total}`
            },
            recommendations: this._generateRecommendations(state)
        };
    }

    /**
     * 生成建议
     */
    _generateRecommendations(state) {
        const recommendations = [];
        
        if (state.flow.state === FlowState.BORED) {
            recommendations.push('💡 建议提高挑战难度，增加新鲜感');
        } else if (state.flow.state === FlowState.ANXIETY) {
            recommendations.push('💡 建议降低挑战难度，或获取更多资源支持');
        } else if (state.flow.state === FlowState.FLOW) {
            recommendations.push('✨ 当前状态极佳，继续保持！');
        }
        
        if (state.immersion.level < 5) {
            recommendations.push('💡 尝试更深入地融入角色和剧情');
        }
        
        if (state.fusion.level < 3) {
            recommendations.push('💡 多进行角色扮演，增强情感连接');
        }
        
        return recommendations;
    }

    /**
     * 重置引擎
     */
    reset() {
        this.currentState = FlowState.CONTROL;
        this.flowScore = 0;
        
        this.playerSkillLevel = 5;
        this.currentChallengeLevel = 3;
        this.challengeHistory = [];
        
        this.currentGoal = null;
        this.goalStack = [];
        this.goalProgress = 0;
        
        this.immersionLevel = 0;
        this.immersionModifiers = {
            narrative: 0,
            challenge: 0,
            choice: 0,
            roleplay: 0
        };
        
        this.pacingState = 'normal';
        
        this.characterFusion = {
            level: 0,
            roleImmersion: 0,
            emotionalInvestment: 0,
            identityBlurring: 0
        };
        
        this.playerState = {
            actions: [],
            successes: 0,
            failures: 0,
            totalActions: 0,
            lastActionTime: Date.now(),
            sessionStartTime: Date.now()
        };
        
        this.recentFeedbacks = [];
        
        // 重置成就解锁状态
        for (const [id, achievement] of this.achievements) {
            achievement.unlocked = false;
            achievement.unlockedAt = null;
        }
        
        this.emit('engine:reset');
        
        return { success: true, message: '心流引擎已重置' };
    }
}

// 导出
module.exports = {
    FlowEngine,
    FlowState,
    ChallengeLevel,
    FeedbackType,
    Achievement,
    Reward,
    Hint
};