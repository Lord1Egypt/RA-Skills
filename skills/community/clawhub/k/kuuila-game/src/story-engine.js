/**
 * StoryEngine - 剧情引擎
 * 基于针本剧本集设计，支持转换链、分支剧情、事件触发
 * 
 * v2.8.0 实现
 * 
 * 设计理念：
 * - 核心转换：剧情推进的关键转折点
 * - 核心诡计：故事的解谜线索
 * - 多分支选择：玩家决策影响剧情走向
 * - 与三幕式结构兼容：适配序幕/破章/急章
 */

// 剧情节点类型
const StoryNodeType = {
    NARRATION: 'narration',     // 叙述节点
    CHOICE: 'choice',           // 选择节点
    TRANSITION: 'transition',   // 转换节点（核心转换）
    TRICK: 'trick',             // 诡计节点（核心诡计）
    BATTLE: 'battle',           // 战斗节点
    INVESTIGATION: 'investigation', // 调查节点
    EVENT: 'event',             // 事件节点
    ENDING: 'ending'            // 结局节点
};

// 结局类型
const EndingType = {
    GOOD: 'good',               // 好结局
    BAD: 'bad',                 // 坏结局
    TRUE: 'true',               // 真结局
    NORMAL: 'normal',           // 普通结局
    SECRET: 'secret'            // 隐藏结局
};

// 剧情分支状态
const BranchState = {
    ACTIVE: 'active',           // 活跃分支
    COMPLETED: 'completed',     // 已完成分支
    LOCKED: 'locked',           // 锁定分支
    ABANDONED: 'abandoned'      // 放弃分支
};

/**
 * 转换链引擎
 * 管理剧情的核心转换序列
 */
class TransformationChain {
    constructor(config = {}) {
        this.chains = new Map();        // 转换链集合
        this.currentChain = null;       // 当前激活的链
        this.currentIndex = 0;          // 当前链中的位置
        this.history = [];              // 转换历史
        this.config = {
            maxChainLength: config.maxChainLength || 10,
            allowBranching: config.allowBranching !== false
        };
    }

    /**
     * 添加转换链
     * @param {string} chainId - 链ID
     * @param {Array} transformations - 转换序列
     */
    addChain(chainId, transformations) {
        this.chains.set(chainId, {
            id: chainId,
            transformations: transformations.map((t, index) => ({
                id: `${chainId}-t${index}`,
                ...t,
                index
            })),
            branches: new Map(),
            state: 'ready'
        });
        return { success: true, chainId, length: transformations.length };
    }

    /**
     * 激活转换链
     */
    activateChain(chainId) {
        if (!this.chains.has(chainId)) {
            return { error: '转换链不存在', chainId };
        }

        this.currentChain = this.chains.get(chainId);
        this.currentIndex = 0;
        this.currentChain.state = 'active';

        return {
            success: true,
            chain: this.currentChain,
            currentTransformation: this.getCurrentTransformation()
        };
    }

    /**
     * 获取当前转换
     */
    getCurrentTransformation() {
        if (!this.currentChain) return null;
        return this.currentChain.transformations[this.currentIndex];
    }

    /**
     * 推进转换链
     */
    advance(choice = null) {
        if (!this.currentChain) {
            return { error: '没有激活的转换链' };
        }

        const current = this.getCurrentTransformation();
        if (!current) {
            return { error: '已到达转换链末端' };
        }

        // 记录历史
        this.history.push({
            chainId: this.currentChain.id,
            transformationId: current.id,
            choice,
            timestamp: Date.now()
        });

        // 检查是否有分支
        if (current.branches && choice) {
            const branch = current.branches.find(b => b.choiceId === choice);
            if (branch) {
                return this._followBranch(branch);
            }
        }

        // 正常推进
        this.currentIndex++;

        const next = this.getCurrentTransformation();
        
        return {
            success: true,
            previous: current,
            current: next,
            isComplete: !next,
            chainProgress: {
                current: this.currentIndex,
                total: this.currentChain.transformations.length
            }
        };
    }

    /**
     * 跟随分支
     */
    _followBranch(branch) {
        if (!branch.targetChain) {
            return { error: '分支目标链不存在' };
        }

        // 保存当前链状态
        const parentChain = this.currentChain;
        parentChain.branches.set(branch.id, {
            fromIndex: this.currentIndex,
            toChain: branch.targetChain,
            timestamp: Date.now()
        });

        // 切换到目标链
        return this.activateChain(branch.targetChain);
    }

    /**
     * 添加分支到转换点
     */
    addBranch(chainId, transformationIndex, branchConfig) {
        const chain = this.chains.get(chainId);
        if (!chain) {
            return { error: '转换链不存在' };
        }

        const transformation = chain.transformations[transformationIndex];
        if (!transformation) {
            return { error: '转换点不存在' };
        }

        if (!transformation.branches) {
            transformation.branches = [];
        }

        transformation.branches.push(branchConfig);
        return { success: true, branch: branchConfig };
    }

    /**
     * 获取转换链状态
     */
    getState() {
        return {
            currentChain: this.currentChain ? this.currentChain.id : null,
            currentIndex: this.currentIndex,
            totalChains: this.chains.size,
            historyLength: this.history.length,
            currentTransformation: this.getCurrentTransformation()
        };
    }

    /**
     * 重置转换链引擎
     */
    reset() {
        this.currentChain = null;
        this.currentIndex = 0;
        this.history = [];
        this.chains.forEach(chain => {
            chain.state = 'ready';
        });
        return { success: true };
    }
}

/**
 * 剧情节点管理器
 */
class StoryNodeManager {
    constructor() {
        this.nodes = new Map();         // 所有节点
        this.currentNode = null;        // 当前节点
        this.visitedNodes = new Set();  // 已访问节点
        this.nodeHistory = [];          // 节点访问历史
        this.storyContext = {};         // 故事上下文
    }

    /**
     * 创建节点
     */
    createNode(nodeConfig) {
        const node = {
            id: nodeConfig.id || `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            type: nodeConfig.type || StoryNodeType.NARRATION,
            title: nodeConfig.title || '',
            content: nodeConfig.content || '',
            choices: nodeConfig.choices || [],
            effects: nodeConfig.effects || [],
            triggers: nodeConfig.triggers || [],
            conditions: nodeConfig.conditions || [],
            nextNodes: nodeConfig.nextNodes || [],
            metadata: nodeConfig.metadata || {},
            phase: nodeConfig.phase || null, // 关联的三幕式阶段
            createdAt: Date.now()
        };

        this.nodes.set(node.id, node);
        return node;
    }

    /**
     * 获取节点
     */
    getNode(nodeId) {
        return this.nodes.get(nodeId);
    }

    /**
     * 设置当前节点
     */
    setCurrentNode(nodeId) {
        const node = this.nodes.get(nodeId);
        if (!node) {
            return { error: '节点不存在', nodeId };
        }

        this.currentNode = node;
        this.visitedNodes.add(nodeId);
        this.nodeHistory.push({
            nodeId,
            timestamp: Date.now(),
            context: { ...this.storyContext }
        });

        // 执行节点效果
        this._executeEffects(node.effects);

        // 触发节点触发器
        const triggeredEvents = this._checkTriggers(node.triggers);

        return {
            success: true,
            node,
            triggeredEvents,
            isFirstVisit: this.visitedNodes.size === this.nodeHistory.length
        };
    }

    /**
     * 执行节点效果
     */
    _executeEffects(effects) {
        effects.forEach(effect => {
            switch (effect.type) {
                case 'setContext':
                    this.storyContext[effect.key] = effect.value;
                    break;
                case 'modifyContext':
                    if (this.storyContext[effect.key] !== undefined) {
                        this.storyContext[effect.key] += effect.value;
                    }
                    break;
                case 'addItem':
                    if (!this.storyContext.items) {
                        this.storyContext.items = [];
                    }
                    this.storyContext.items.push(effect.item);
                    break;
                case 'removeItem':
                    if (this.storyContext.items) {
                        const index = this.storyContext.items.findIndex(
                            i => i.id === effect.itemId
                        );
                        if (index !== -1) {
                            this.storyContext.items.splice(index, 1);
                        }
                    }
                    break;
                case 'setFlag':
                    this.storyContext[effect.flag] = true;
                    break;
                case 'clearFlag':
                    this.storyContext[effect.flag] = false;
                    break;
            }
        });
    }

    /**
     * 检查触发器
     */
    _checkTriggers(triggers) {
        return triggers.filter(trigger => {
            // 检查条件
            if (trigger.conditions) {
                const allConditionsMet = trigger.conditions.every(cond => {
                    return this._checkCondition(cond);
                });
                if (!allConditionsMet) return false;
            }
            return true;
        });
    }

    /**
     * 检查条件
     */
    _checkCondition(condition) {
        const value = this.storyContext[condition.key];
        switch (condition.operator) {
            case 'eq': return value === condition.value;
            case 'ne': return value !== condition.value;
            case 'gt': return value > condition.value;
            case 'lt': return value < condition.value;
            case 'gte': return value >= condition.value;
            case 'lte': return value <= condition.value;
            case 'has': return Array.isArray(value) && value.includes(condition.value);
            case 'hasFlag': return !!this.storyContext[condition.flag];
            default: return false;
        }
    }

    /**
     * 处理选择
     */
    processChoice(choiceIndex) {
        if (!this.currentNode) {
            return { error: '没有当前节点' };
        }

        const choice = this.currentNode.choices[choiceIndex];
        if (!choice) {
            return { error: '无效的选择', choiceIndex };
        }

        // 检查选择条件
        if (choice.conditions && !choice.conditions.every(c => this._checkCondition(c))) {
            return { error: '条件不满足', conditions: choice.conditions };
        }

        // 执行选择效果
        if (choice.effects) {
            this._executeEffects(choice.effects);
        }

        // 返回下一个节点
        return {
            success: true,
            choice,
            nextNodeId: choice.nextNode || null,
            context: this.storyContext
        };
    }

    /**
     * 获取故事上下文
     */
    getContext() {
        return { ...this.storyContext };
    }

    /**
     * 更新故事上下文
     */
    updateContext(key, value) {
        this.storyContext[key] = value;
        return { success: true, key, value };
    }

    /**
     * 获取访问历史
     */
    getHistory() {
        return [...this.nodeHistory];
    }

    /**
     * 重置节点管理器
     */
    reset() {
        this.currentNode = null;
        this.visitedNodes.clear();
        this.nodeHistory = [];
        this.storyContext = {};
        return { success: true };
    }
}

/**
 * 事件触发系统
 */
class EventTriggerSystem {
    constructor() {
        this.triggers = new Map();      // 触发器注册表
        this.eventQueue = [];           // 事件队列
        this.eventHistory = [];         // 事件历史
        this.globalListeners = [];      // 全局事件监听器
    }

    /**
     * 注册触发器
     */
    registerTrigger(triggerId, config) {
        const trigger = {
            id: triggerId,
            type: config.type,          // 'turn', 'phase', 'condition', 'random'
            conditions: config.conditions || [],
            effects: config.effects || [],
            priority: config.priority || 0,
            repeatable: config.repeatable || false,
            triggered: false,
            cooldown: config.cooldown || 0,
            lastTriggered: 0
        };

        this.triggers.set(triggerId, trigger);
        return { success: true, trigger };
    }

    /**
     * 检查并触发事件
     */
    checkTriggers(context) {
        const triggered = [];

        for (const [id, trigger] of this.triggers) {
            // 检查冷却时间
            if (trigger.cooldown > 0) {
                const elapsed = Date.now() - trigger.lastTriggered;
                if (elapsed < trigger.cooldown) continue;
            }

            // 检查是否已触发且不可重复
            if (trigger.triggered && !trigger.repeatable) continue;

            // 检查条件
            const shouldTrigger = this._evaluateTrigger(trigger, context);

            if (shouldTrigger) {
                const event = this._createEvent(trigger, context);
                this.eventQueue.push(event);
                triggered.push(event);
                trigger.triggered = true;
                trigger.lastTriggered = Date.now();
            }
        }

        // 按优先级排序
        this.eventQueue.sort((a, b) => b.priority - a.priority);

        return triggered;
    }

    /**
     * 评估触发器
     */
    _evaluateTrigger(trigger, context) {
        switch (trigger.type) {
            case 'turn':
                return context.turn !== undefined && 
                       trigger.conditions.turns?.includes(context.turn);

            case 'phase':
                return context.phase !== undefined &&
                       trigger.conditions.phases?.includes(context.phase);

            case 'condition':
                return trigger.conditions.every(cond => {
                    const value = context[cond.key];
                    switch (cond.operator) {
                        case 'eq': return value === cond.value;
                        case 'ne': return value !== cond.value;
                        case 'gt': return value > cond.value;
                        case 'lt': return value < condition.value;
                        case 'gte': return value >= cond.value;
                        case 'lte': return value <= cond.value;
                        case 'has': return Array.isArray(value) && value.includes(cond.value);
                        case 'hasFlag': return !!context[cond.flag];
                        default: return false;
                    }
                });

            case 'random':
                return Math.random() < (trigger.conditions.probability || 0.5);

            default:
                return false;
        }
    }

    /**
     * 创建事件
     */
    _createEvent(trigger, context) {
        return {
            id: `event-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            triggerId: trigger.id,
            type: trigger.type,
            effects: trigger.effects,
            priority: trigger.priority,
            context: { ...context },
            timestamp: Date.now(),
            processed: false
        };
    }

    /**
     * 处理事件队列
     */
    processQueue() {
        const processed = [];

        while (this.eventQueue.length > 0) {
            const event = this.eventQueue.shift();
            event.processed = true;
            this.eventHistory.push(event);
            processed.push(event);

            // 通知全局监听器
            this.globalListeners.forEach(listener => {
                listener(event);
            });
        }

        return processed;
    }

    /**
     * 添加全局监听器
     */
    addGlobalListener(listener) {
        this.globalListeners.push(listener);
        return { success: true };
    }

    /**
     * 手动触发事件
     */
    triggerManual(eventConfig) {
        const event = {
            id: `manual-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            type: 'manual',
            ...eventConfig,
            timestamp: Date.now(),
            processed: false
        };

        this.eventQueue.push(event);
        return event;
    }

    /**
     * 获取事件历史
     */
    getHistory() {
        return [...this.eventHistory];
    }

    /**
     * 重置事件系统
     */
    reset() {
        this.eventQueue = [];
        this.eventHistory = [];
        this.triggers.forEach(trigger => {
            trigger.triggered = false;
            trigger.lastTriggered = 0;
        });
        return { success: true };
    }
}

/**
 * 结局判定系统
 */
class EndingSystem {
    constructor() {
        this.endings = new Map();       // 结局定义
        this.endingConditions = [];     // 结局条件
        this.reachedEndings = [];       // 已达成的结局
        this.currentEnding = null;      // 当前结局
    }

    /**
     * 定义结局
     */
    defineEnding(endingId, config) {
        const ending = {
            id: endingId,
            type: config.type || EndingType.NORMAL,
            title: config.title,
            description: config.description,
            conditions: config.conditions || [],
            priority: config.priority || 0,
            epilogue: config.epilogue || '',
            rewards: config.rewards || [],
            unlocked: false,
            unlockHint: config.unlockHint || ''
        };

        this.endings.set(endingId, ending);
        return { success: true, ending };
    }

    /**
     * 检查结局
     */
    checkEndings(context) {
        const possibleEndings = [];

        for (const [id, ending] of this.endings) {
            const conditionsMet = ending.conditions.every(cond => {
                return this._evaluateCondition(cond, context);
            });

            if (conditionsMet) {
                possibleEndings.push(ending);
            }
        }

        // 按优先级排序
        possibleEndings.sort((a, b) => b.priority - a.priority);

        return possibleEndings;
    }

    /**
     * 评估条件
     */
    _evaluateCondition(condition, context) {
        const value = context[condition.key];
        switch (condition.operator) {
            case 'eq': return value === condition.value;
            case 'ne': return value !== condition.value;
            case 'gt': return value > condition.value;
            case 'lt': return value < condition.value;
            case 'gte': return value >= condition.value;
            case 'lte': return value <= condition.value;
            case 'has': return Array.isArray(value) && value.includes(condition.value);
            case 'hasFlag': return !!context[condition.flag];
            case 'hasItem': 
                return Array.isArray(context.items) && 
                       context.items.some(i => i.id === condition.itemId);
            default: return false;
        }
    }

    /**
     * 达成结局
     */
    reachEnding(endingId) {
        const ending = this.endings.get(endingId);
        if (!ending) {
            return { error: '结局不存在', endingId };
        }

        ending.unlocked = true;
        this.reachedEndings.push({
            endingId,
            timestamp: Date.now()
        });
        this.currentEnding = ending;

        return {
            success: true,
            ending,
            totalUnlocked: this.reachedEndings.length,
            totalEndings: this.endings.size
        };
    }

    /**
     * 获取结局统计
     */
    getStats() {
        const stats = {
            total: this.endings.size,
            unlocked: this.reachedEndings.length,
            byType: {}
        };

        for (const [id, ending] of this.endings) {
            if (!stats.byType[ending.type]) {
                stats.byType[ending.type] = { total: 0, unlocked: 0 };
            }
            stats.byType[ending.type].total++;
            if (ending.unlocked) {
                stats.byType[ending.type].unlocked++;
            }
        }

        return stats;
    }

    /**
     * 获取未解锁结局提示
     */
    getUnlockHints() {
        const hints = [];
        for (const [id, ending] of this.endings) {
            if (!ending.unlocked && ending.unlockHint) {
                hints.push({
                    id,
                    type: ending.type,
                    hint: ending.unlockHint
                });
            }
        }
        return hints;
    }

    /**
     * 重置结局系统
     */
    reset() {
        this.reachedEndings = [];
        this.currentEnding = null;
        this.endings.forEach(ending => {
            ending.unlocked = false;
        });
        return { success: true };
    }
}

/**
 * 核心诡计生成器
 * 基于针本剧本集的核心诡计模式
 */
class CoreTrickGenerator {
    constructor() {
        this.trickPatterns = [];
        this.customTricks = [];
    }

    /**
     * 从针本数据加载诡计模式
     */
    loadFromZhenben(zhenbenData) {
        if (!zhenbenData || !zhenbenData.大纲) return;

        zhenbenData.大纲.forEach(scenario => {
            if (scenario.核心诡计) {
                this.trickPatterns.push({
                    id: `trick-${scenario.编号}`,
                    scenarioId: scenario.编号,
                    title: scenario.目录,
                    theme: scenario.主题,
                    pattern: scenario.核心诡计,
                    type: this._classifyTrick(scenario.核心诡计)
                });
            }
        });

        return { success: true, count: this.trickPatterns.length };
    }

    /**
     * 分类诡计类型
     */
    _classifyTrick(trickText) {
        if (!trickText) return 'unknown';
        
        const keywords = {
            time: ['时间', '未来', '过去', '旅行', '历史'],
            identity: ['身份', '伪装', '假扮', '其实是'],
            knowledge: ['知识', '书籍', '文献', '秘密'],
            ritual: ['仪式', '召唤', '祭祀', '法术'],
            transformation: ['变化', '转换', '变形', '附体'],
            space: ['空间', '维度', '异度', '传送'],
            entity: ['怪物', '生物', '实体', '神话']
        };

        for (const [type, words] of Object.entries(keywords)) {
            if (words.some(word => trickText.includes(word))) {
                return type;
            }
        }

        return 'mystery';
    }

    /**
     * 生成诡计节点
     */
    generateTrickNode(theme = null, phase = null) {
        // 过滤符合主题的诡计
        let candidates = this.trickPatterns;
        if (theme) {
            candidates = candidates.filter(t => 
                t.theme && t.theme.includes(theme)
            );
        }

        if (candidates.length === 0) {
            candidates = this.trickPatterns;
        }

        // 随机选择
        const selected = candidates[Math.floor(Math.random() * candidates.length)];

        // 生成节点配置
        return {
            id: `trick-node-${Date.now()}`,
            type: StoryNodeType.TRICK,
            title: `核心诡计：${selected.title}`,
            content: selected.pattern,
            metadata: {
                trickId: selected.id,
                trickType: selected.type,
                scenarioId: selected.scenarioId
            },
            phase,
            choices: [
                { text: '发现线索', nextNode: null },
                { text: '继续调查', nextNode: null },
                { text: '寻求帮助', nextNode: null }
            ]
        };
    }

    /**
     * 获取所有诡计类型
     */
    getTrickTypes() {
        const types = new Set();
        this.trickPatterns.forEach(t => types.add(t.type));
        return Array.from(types);
    }

    /**
     * 添加自定义诡计
     */
    addCustomTrick(trickConfig) {
        const trick = {
            id: `custom-trick-${Date.now()}`,
            ...trickConfig,
            isCustom: true
        };
        this.customTricks.push(trick);
        return trick;
    }
}

/**
 * 剧情引擎主类
 * 整合所有子系统
 */
class StoryEngine {
    constructor(config = {}) {
        this.config = {
            autoTrigger: config.autoTrigger !== false,
            saveHistory: config.saveHistory !== false,
            enableTricks: config.enableTricks !== false,
            ...config
        };

        // 核心子系统
        this.transformationChain = new TransformationChain(config.chain);
        this.nodeManager = new StoryNodeManager();
        this.eventSystem = new EventTriggerSystem();
        this.endingSystem = new EndingSystem();
        this.trickGenerator = new CoreTrickGenerator();

        // 剧本数据
        this.scenarios = [];
        this.currentScenario = null;

        // 关联系统
        this.threeActStructure = null;
        this.cardSystem = null;

        // 状态
        this.isRunning = false;
        this.storyState = {
            started: false,
            turnCount: 0,
            phaseHistory: []
        };
    }

    /**
     * 加载针本剧本集
     */
    loadZhenbenScenarios(zhenbenData) {
        if (!zhenbenData || !zhenbenData.大纲) {
            return { error: '无效的针本数据' };
        }

        this.scenarios = zhenbenData.大纲.map(scenario => ({
            id: `scenario-${scenario.编号}`,
            number: scenario.编号,
            title: scenario.目录,
            theme: scenario.主题 || '',
            coreTransformation: scenario.核心转换 || '',
            coreTrick: scenario.核心诡计 || '',
            characterFeatures: scenario.角色特征 || '',
            metadata: scenario
        }));

        // 加载诡计模式
        this.trickGenerator.loadFromZhenben(zhenbenData);

        // 加载世界观数据
        if (zhenbenData.世界观) {
            this.worldViews = zhenbenData.世界观;
        }

        return {
            success: true,
            count: this.scenarios.length,
            tricksLoaded: this.trickGenerator.trickPatterns.length
        };
    }

    /**
     * 选择剧本
     */
    selectScenario(scenarioId) {
        const scenario = this.scenarios.find(s => s.id === scenarioId);
        if (!scenario) {
            return { error: '剧本不存在', scenarioId };
        }

        this.currentScenario = scenario;

        // 基于剧本创建转换链
        this._createScenarioChain(scenario);

        return {
            success: true,
            scenario,
            chainCreated: true
        };
    }

    /**
     * 创建剧本转换链
     */
    _createScenarioChain(scenario) {
        // 解析核心转换为转换点
        const transformations = this._parseTransformations(scenario.coreTransformation);

        this.transformationChain.addChain('main', transformations);

        return { success: true, transformationCount: transformations.length };
    }

    /**
     * 解析转换描述为转换点
     */
    _parseTransformations(transformationText) {
        if (!transformationText) return [];

        // 简单分割（实际可更智能）
        const parts = transformationText.split(/[，。；\n]/).filter(p => p.trim());

        return parts.map((part, index) => ({
            id: `trans-${index}`,
            description: part.trim(),
            type: 'narrative',
            index
        }));
    }

    /**
     * 关联三幕式结构
     */
    linkThreeActStructure(structure) {
        this.threeActStructure = structure;

        // 注册阶段转换触发器
        this.eventSystem.registerTrigger('phase-transition', {
            type: 'phase',
            conditions: { phases: ['prologue', 'conflict', 'climax'] },
            effects: [{ type: 'updatePhaseStory' }],
            repeatable: true
        });

        return { success: true };
    }

    /**
     * 关联卡牌系统
     */
    linkCardSystem(cardSystem) {
        this.cardSystem = cardSystem;
        return { success: true };
    }

    /**
     * 开始剧情
     */
    startStory(scenarioId = null) {
        if (scenarioId) {
            const result = this.selectScenario(scenarioId);
            if (result.error) return result;
        }

        if (!this.currentScenario) {
            // 随机选择剧本
            if (this.scenarios.length > 0) {
                const randomIndex = Math.floor(Math.random() * this.scenarios.length);
                this.currentScenario = this.scenarios[randomIndex];
                this._createScenarioChain(this.currentScenario);
            } else {
                return { error: '没有可用剧本，请先加载剧本数据' };
            }
        }

        // 激活转换链
        this.transformationChain.activateChain('main');

        // 创建起始节点
        const startNode = this.nodeManager.createNode({
            type: StoryNodeType.NARRATION,
            title: `故事开始：${this.currentScenario.title}`,
            content: this._generateStartNarration(),
            phase: 'prologue'
        });

        this.nodeManager.setCurrentNode(startNode.id);

        this.isRunning = true;
        this.storyState.started = true;
        this.storyState.turnCount = 0;

        return {
            success: true,
            message: '🎭 剧情已启动',
            scenario: this.currentScenario,
            startNode,
            phase: this.threeActStructure ? this.threeActStructure.getCurrentPhase() : null
        };
    }

    /**
     * 生成起始叙述
     */
    _generateStartNarration() {
        if (!this.currentScenario) return '';

        const scenario = this.currentScenario;
        let narration = `# ${scenario.title}\n\n`;

        if (scenario.theme) {
            narration += `**主题**：${scenario.theme}\n\n`;
        }

        narration += '故事即将展开...\n\n';

        if (scenario.characterFeatures) {
            narration += `**关键角色**：${scenario.characterFeatures}\n\n`;
        }

        return narration;
    }

    /**
     * 推进剧情
     */
    advanceStory(choice = null) {
        if (!this.isRunning) {
            return { error: '剧情未启动' };
        }

        this.storyState.turnCount++;

        // 推进转换链
        const chainResult = this.transformationChain.advance(choice);

        // 检查事件触发
        const context = this._buildContext();
        const triggeredEvents = this.eventSystem.checkTriggers(context);

        // 处理事件
        const processedEvents = this.eventSystem.processQueue();

        // 检查结局
        const possibleEndings = this.endingSystem.checkEndings(context);

        // 更新节点
        let newNode = null;
        if (chainResult.current) {
            newNode = this.nodeManager.createNode({
                type: StoryNodeType.TRANSITION,
                title: chainResult.current.description,
                content: `转换点 ${chainResult.chainProgress.current}/${chainResult.chainProgress.total}`,
                phase: this.threeActStructure ? this.threeActStructure.getCurrentPhase() : null
            });
            this.nodeManager.setCurrentNode(newNode.id);
        }

        return {
            success: true,
            chainResult,
            triggeredEvents: processedEvents,
            possibleEndings,
            newNode,
            storyComplete: chainResult.isComplete
        };
    }

    /**
     * 创建选择节点
     */
    createChoiceNode(config) {
        const node = this.nodeManager.createNode({
            type: StoryNodeType.CHOICE,
            ...config
        });

        return node;
    }

    /**
     * 触发卡牌抽取
     */
    triggerCardDraw(drawConfig = {}) {
        if (!this.cardSystem) {
            return { error: '未关联卡牌系统' };
        }

        const {
            deckName = 'all',
            count = 1,
            context = {}
        } = drawConfig;

        const drawResult = this.cardSystem.drawMultiple(deckName, count);

        // 记录到故事上下文
        if (drawResult.cards) {
            this.nodeManager.updateContext('lastDrawnCards', drawResult.cards);
        }

        return {
            success: true,
            cards: drawResult.cards,
            context
        };
    }

    /**
     * 生成诡计节点
     */
    generateTrickStoryNode(theme = null) {
        const phase = this.threeActStructure ? 
            this.threeActStructure.getCurrentPhase() : null;

        const nodeConfig = this.trickGenerator.generateTrickNode(theme, phase);
        const node = this.nodeManager.createNode(nodeConfig);

        return {
            success: true,
            node,
            trickType: nodeConfig.metadata.trickType
        };
    }

    /**
     * 定义结局
     */
    defineStoryEnding(endingId, config) {
        return this.endingSystem.defineEnding(endingId, config);
    }

    /**
     * 达成结局
     */
    reachStoryEnding(endingId) {
        const result = this.endingSystem.reachEnding(endingId);

        if (result.success) {
            this.isRunning = false;

            // 创建结局节点
            const endingNode = this.nodeManager.createNode({
                type: StoryNodeType.ENDING,
                title: `结局：${result.ending.title}`,
                content: result.ending.description,
                metadata: {
                    endingType: result.ending.type,
                    endingId
                }
            });

            this.nodeManager.setCurrentNode(endingNode.id);
        }

        return result;
    }

    /**
     * 构建上下文
     */
    _buildContext() {
        return {
            ...this.nodeManager.getContext(),
            turn: this.storyState.turnCount,
            phase: this.threeActStructure ? this.threeActStructure.getCurrentPhase() : null,
            scenario: this.currentScenario ? this.currentScenario.id : null,
            chainState: this.transformationChain.getState()
        };
    }

    /**
     * 获取完整状态
     */
    getFullState() {
        return {
            isRunning: this.isRunning,
            storyState: this.storyState,
            currentScenario: this.currentScenario,
            currentNode: this.nodeManager.currentNode,
            chainState: this.transformationChain.getState(),
            context: this.nodeManager.getContext(),
            eventHistory: this.eventSystem.getHistory(),
            endingStats: this.endingSystem.getStats()
        };
    }

    /**
     * 获取剧本列表
     */
    listScenarios() {
        return this.scenarios.map(s => ({
            id: s.id,
            number: s.number,
            title: s.title,
            theme: s.theme,
            hasTransformation: !!s.coreTransformation,
            hasTrick: !!s.coreTrick
        }));
    }

    /**
     * 生成故事报告
     */
    generateReport() {
        const state = this.getFullState();

        let report = '# 📖 剧情报告\n\n';

        // 剧本信息
        if (this.currentScenario) {
            report += `## 剧本：${this.currentScenario.title}\n`;
            report += `- **主题**：${this.currentScenario.theme || '未设定'}\n`;
            report += `- **编号**：#${this.currentScenario.number}\n\n`;
        }

        // 状态
        report += `## 状态\n`;
        report += `- 运行中：${this.isRunning ? '✅' : '❌'}\n`;
        report += `- 回合数：${this.storyState.turnCount}\n`;
        report += `- 已访问节点：${this.nodeManager.visitedNodes.size}\n\n`;

        // 转换链
        const chainState = state.chainState;
        if (chainState.currentChain) {
            report += `## 转换链进度\n`;
            report += `- 当前链：${chainState.currentChain}\n`;
            report += `- 进度：${chainState.currentIndex}\n\n`;
        }

        // 结局
        const endingStats = state.endingStats;
        report += `## 结局统计\n`;
        report += `- 已解锁：${endingStats.unlocked}/${endingStats.total}\n`;

        return report;
    }

    /**
     * 重置剧情引擎
     */
    reset() {
        this.transformationChain.reset();
        this.nodeManager.reset();
        this.eventSystem.reset();
        this.endingSystem.reset();

        this.currentScenario = null;
        this.isRunning = false;
        this.storyState = {
            started: false,
            turnCount: 0,
            phaseHistory: []
        };

        return { success: true, message: '剧情引擎已重置' };
    }
}

// 导出
module.exports = {
    StoryEngine,
    TransformationChain,
    StoryNodeManager,
    EventTriggerSystem,
    EndingSystem,
    CoreTrickGenerator,
    StoryNodeType,
    EndingType,
    BranchState
};
