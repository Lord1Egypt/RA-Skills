/**
 * Interactive Games - 互动游戏框架主入口
 * 统一接口，管理所有游戏类型（单人 + 多人 + 三幕式结构）
 * 
 * v2.7 新增主题模组系统
 * v2.3 新增三幕式游戏结构
 */

const { GameEngine } = require('./game-engine');
const { AdventureGame } = require('./adventure-game');
const { PuzzleGame } = require('./puzzle-game');
const { StoryGenerator } = require('./story-generator');
const { MultiplayerGameEngine } = require('./multiplayer-engine');
const { MultiplayerWuxiaGame } = require('./multiplayer-wuxia');
const { CardSystem, CardType, Theme } = require('./card-system');

// 三幕式系统 v2.3
const { ThreeActStructure, ActPhase, ActPhaseNames, ActPhaseDescriptions } = require('./three-act-structure');
const { TurnManager, TurnState, EventType, TriggerType } = require('./turn-manager');

// 主题模组系统 v2.7
const { 
    ThemeSystem, 
    ThemeLoader, 
    ThemeCardManager, 
    ThemeStoryGenerator, 
    ArtStyleManager,
    THEMES,
    THEME_CARD_LIBRARIES,
    THEME_STORY_TEMPLATES,
    ART_STYLE_TAGS
} = require('./theme-system');

// 主题模组加载器 v2.7 (向后兼容)
const { ThemeModuleLoader, ThemeType } = require('./theme-loader');

// 剧情引擎系统 v2.8
const {
    StoryEngine,
    TransformationChain,
    StoryNodeManager,
    EventTriggerSystem,
    EndingSystem,
    CoreTrickGenerator,
    StoryNodeType,
    EndingType,
    BranchState
} = require('./story-engine');

// 剧本系统 v2.9
const {
    ScenarioSystem,
    Scenario,
    ScenarioProgressManager,
    ClueSystem,
    ScenarioState,
    DifficultyLevel,
    ClueState,
    CharacterRoleState
} = require('./scenario-system');

// 心流引擎系统 v2.10
const {
    FlowEngine,
    FlowState,
    ChallengeLevel,
    FeedbackType,
    Achievement,
    Reward,
    Hint
} = require('./flow-engine');

class InteractiveGames {
    constructor() {
        this.engine = new GameEngine();
        this.storyGenerator = new StoryGenerator();
        this.cardSystem = new CardSystem();
        this.activeGame = null;
        this.multiplayerGame = null;
        this.isMultiplayer = false;
        
        // 三幕式系统 v2.3
        this.turnManager = null;
        this.threeActStructure = null;
        
        // 主题模组系统 v2.7 - 默认加载武侠主题
        this.themeSystem = new ThemeSystem();
        this.themeSystem.initialize('wuxia');
        this.themeLoader = new ThemeModuleLoader(); // 向后兼容
        
        // 剧情引擎系统 v2.8
        this.storyEngine = new StoryEngine();
        
        // 剧本系统 v2.9
        this.scenarioSystem = new ScenarioSystem();
        
        // 心流引擎系统 v2.10
        this.flowEngine = new FlowEngine();
        
        // 关联系统
        this._linkFlowEngine();
    }

    /**
     * 关联心流引擎与其他系统
     */
    _linkFlowEngine() {
        // 关联三幕式结构
        if (this.threeActStructure) {
            this.flowEngine.linkThreeActStructure(this.threeActStructure);
        }
        
        // 关联卡牌系统
        if (this.cardSystem) {
            this.flowEngine.linkCardSystem(this.cardSystem);
        }
        
        // 关联角色系统（如果存在）
        if (this.characterSystem) {
            this.flowEngine.linkCharacterSystem(this.characterSystem);
        }
    }

    // 检查是否处于多人游戏沙箱模式
    isInSandbox() {
        return this.isMultiplayer && 
               this.multiplayerGame && 
               this.multiplayerGame.engine && 
               this.multiplayerGame.engine.sandboxMode &&
               this.multiplayerGame.engine.isActive;
    }

    // 验证命令是否允许（沙箱安全检查）
    validateCommand(input, playerId = null) {
        // 如果不在沙箱模式，允许所有命令
        if (!this.isInSandbox()) {
            return { allowed: true };
        }

        const mpEngine = this.multiplayerGame.engine;

        // 游戏创建者有完全权限
        if (playerId && playerId === mpEngine.gameHostId) {
            return { allowed: true };
        }

        // 检查命令白名单
        if (mpEngine.isCommandAllowed(input)) {
            return { allowed: true };
        }

        // 检查玩家是否在游戏中
        if (playerId && !mpEngine.isPlayerInGame(playerId)) {
            return {
                allowed: false,
                reason: 'not_in_game',
                message: '⚠️ 您未加入当前游戏，无法执行此命令。'
            };
        }

        // 沙箱拒绝
        return {
            allowed: false,
            reason: 'sandbox_restricted',
            ...mpEngine.getSandboxRejectMessage()
        };
    }

    // 安全处理输入（带沙箱检查）
    safeHandleInput(input, playerId = null) {
        const validation = this.validateCommand(input, playerId);
        
        if (!validation.allowed) {
            return validation;
        }

        return this.handleInput(input, playerId);
    }

    // 启动单人游戏
    startGame(gameType, options = {}) {
        console.log('🎮 互动游戏框架启动');
        this.isMultiplayer = false;
        
        switch (gameType) {
            case 'adventure':
            case '文字冒险':
                this.activeGame = new AdventureGame(options.theme || '历史穿越');
                this.engine.currentGame = this.activeGame;
                return this.activeGame.start();
            
            case 'puzzle':
            case '猜谜':
                this.activeGame = new PuzzleGame();
                this.engine.currentGame = this.activeGame;
                return this.activeGame.start(options.type || 'mixed');
            
            default:
                return {
                    error: '未知游戏类型',
                    supported: ['文字冒险', '猜谜', 'adventure', 'puzzle']
                };
        }
    }

    // 启动多人游戏
    startMultiplayerGame(gameType = 'wuxia', options = {}) {
        console.log('🎮🎮 多人游戏框架启动');
        this.isMultiplayer = true;
        
        switch (gameType) {
            case 'wuxia':
            case '武侠':
                this.multiplayerGame = new MultiplayerWuxiaGame();
                // 记录游戏创建者
                if (options.hostId) {
                    this.multiplayerGame.engine.setGameHost(options.hostId);
                }
                return this.multiplayerGame.init(options);
            
            default:
                return {
                    error: '未知的多人游戏类型',
                    supported: ['武侠', 'wuxia']
                };
        }
    }

    // 添加玩家到多人游戏
    addPlayer(playerId, playerName) {
        if (!this.isMultiplayer || !this.multiplayerGame) {
            return { error: '请先启动多人游戏' };
        }
        return this.multiplayerGame.addPlayer(playerId, playerName);
    }

    // 移除玩家
    removePlayer(playerId) {
        if (!this.isMultiplayer || !this.multiplayerGame) {
            return { error: '没有活跃的多人游戏' };
        }
        return this.multiplayerGame.removePlayer(playerId);
    }

    // 设置多人游戏模式
    setMultiplayerMode(mode) {
        if (!this.multiplayerGame) {
            return { error: '请先初始化多人游戏' };
        }
        return this.multiplayerGame.setMode(mode);
    }

    // 开始多人游戏
    beginMultiplayerGame() {
        if (!this.multiplayerGame) {
            return { error: '请先初始化多人游戏' };
        }
        return this.multiplayerGame.startGame();
    }

    // 处理用户输入
    handleInput(input, playerId = null) {
        const inputStr = typeof input === 'string' ? input : (input.choice || '');
        const normalizedInput = inputStr.toLowerCase().trim();
        
        // 处理退出命令（特殊处理，不经过沙箱检查）
        if (normalizedInput === '退出游戏' || normalizedInput === '退出' || normalizedInput === 'quit') {
            return this.quitGame(playerId);
        }
        
        // 多人游戏模式
        if (this.isMultiplayer && this.multiplayerGame) {
            // 沙箱安全检查
            const validation = this.validateCommand(input, playerId);
            if (!validation.allowed) {
                return validation;
            }
            
            // 处理游戏命令
            if (typeof input === 'object' && input.choice) {
                return this.multiplayerGame.processChoice(input.playerId || playerId, input.choice);
            }
            
            // 简单文本输入
            return this.multiplayerGame.processChoice(playerId, input);
        }
        
        // 单人游戏模式
        if (!this.activeGame) {
            return { error: '请先启动游戏' };
        }
        return this.activeGame.processInput(input);
    }

    // 处理多人游戏选择
    processMultiplayerChoice(playerId, choice) {
        if (!this.isMultiplayer || !this.multiplayerGame) {
            return { error: '没有活跃的多人游戏' };
        }
        return this.multiplayerGame.processChoice(playerId, choice);
    }

    // 获取游戏状态
    getStatus() {
        if (this.isMultiplayer && this.multiplayerGame) {
            return {
                active: true,
                isMultiplayer: true,
                ...this.multiplayerGame.getStatus()
            };
        }

        if (!this.activeGame) {
            return { active: false };
        }
        return {
            active: true,
            isMultiplayer: false,
            type: this.activeGame.type,
            state: this.activeGame.getState()
        };
    }

    // 保存游戏
    saveGame(slot = 'autosave') {
        if (this.isMultiplayer && this.multiplayerGame) {
            return this.multiplayerGame.saveGame(slot);
        }
        return this.engine.saveGame(slot);
    }

    // 读取游戏
    loadGame(slot = 'autosave') {
        return this.engine.loadGame(slot);
    }

    // 退出游戏
    quitGame(playerId = null) {
        if (this.isMultiplayer && this.multiplayerGame) {
            // 检查权限：只有主机或已加入的玩家可以退出
            const engine = this.multiplayerGame.engine;
            if (playerId && playerId !== engine.gameHostId && !engine.isPlayerInGame(playerId)) {
                return { error: '您没有权限退出此游戏' };
            }
            
            const result = this.multiplayerGame.endGame('玩家退出');
            this.multiplayerGame = null;
            this.isMultiplayer = false;
            return result;
        }

        if (this.activeGame) {
            this.engine.saveGame('autosave');
            this.activeGame = null;
            return { message: '游戏已退出，进度已自动保存' };
        }
        return { message: '没有活跃的游戏' };
    }

    // ============ 卡牌系统方法 ============
    
    // 查看卡牌系统状态
    getCardStats() {
        return this.cardSystem.getStats();
    }

    // 抽卡
    drawCards(deckName = 'all', count = 1) {
        if (count === 1) {
            return this.cardSystem.draw(deckName);
        }
        return this.cardSystem.drawMultiple(deckName, count);
    }

    // 随机抽卡
    drawRandomCards(types = [], count = 1) {
        return this.cardSystem.drawRandom(types, count);
    }

    // 查看手牌
    showHand() {
        return this.cardSystem.showHand();
    }

    // 打出手牌
    playCard(cardIndex) {
        return this.cardSystem.playCard(cardIndex);
    }

    // 洗牌
    shuffleDeck(deckName = 'all') {
        return this.cardSystem.shuffle(deckName);
    }

    // 组合卡牌
    combineCards(cardIndices = []) {
        return this.cardSystem.combine(cardIndices);
    }

    // 生成故事场景
    generateStoryScene() {
        return this.cardSystem._generateStoryElement(['Role', 'Location', 'Event']);
    }

    // 生成完整故事
    generateStory() {
        return this.cardSystem._generateStoryElement(['Role', 'Location', 'Item', 'State', 'Event', 'Ending']);
    }

    // 列出所有卡组
    listCardDecks() {
        return this.cardSystem.listDecks();
    }

    // 重置卡牌系统
    resetCardSystem() {
        return this.cardSystem.reset();
    }

    // 获取游戏启动配置
    getGameSetup(playerCount = 1, theme = Theme.BASE) {
        return this.cardSystem.getGameSetup(playerCount, theme);
    }

    // ============ 三幕式系统方法 v2.3 ============
    
    /**
     * 启动三幕式游戏
     * @param {Object} options - 游戏配置
     * @param {number} options.prologueMinTurns - 序幕最小回合数（默认1）
     * @param {number} options.prologueMaxTurns - 序幕最大回合数（默认3）
     * @param {number} options.conflictMinTurns - 破章最小回合数（默认3）
     * @param {number} options.conflictMaxTurns - 破章最大回合数（默认5）
     * @param {number} options.climaxMinTurns - 急章最小回合数（默认1）
     * @param {number} options.climaxMaxTurns - 急章最大回合数（默认3）
     */
    startThreeActGame(options = {}) {
        console.log('🎭 三幕式游戏启动');
        
        this.turnManager = new TurnManager({
            threeAct: options,
            maxTurns: options.maxTurns || 15,
            turnTimeout: options.turnTimeout || 300000,
            ...options
        });
        
        this.threeActStructure = this.turnManager.threeActStructure;
        
        return {
            success: true,
            message: '🎭 三幕式游戏已启动',
            phase: this.threeActStructure.getCurrentPhase(),
            phaseName: this.threeActStructure.getPhaseName(),
            phaseDescription: this.threeActStructure.getPhaseDescription(),
            state: this.threeActStructure.getFullState()
        };
    }

    /**
     * 获取当前游戏阶段
     */
    getCurrentPhase() {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return {
            phase: this.threeActStructure.getCurrentPhase(),
            phaseName: this.threeActStructure.getPhaseName(),
            description: this.threeActStructure.getPhaseDescription(),
            state: this.threeActStructure.getFullState()
        };
    }

    /**
     * 获取阶段报告
     */
    getPhaseReport() {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.generatePhaseReport();
    }

    /**
     * 添加玩家到三幕式游戏
     */
    addThreeActPlayer(playerId, playerInfo = {}) {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.addPlayer(playerId, playerInfo);
    }

    /**
     * 移除三幕式游戏玩家
     */
    removeThreeActPlayer(playerId) {
        if (!this.turnManager) {
            return { error: '没有活跃的三幕式游戏' };
        }
        return this.turnManager.removePlayer(playerId);
    }

    /**
     * 开始新回合
     */
    startTurn() {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.startTurn();
    }

    /**
     * 处理玩家行动
     */
    processAction(playerId, action) {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.processPlayerAction(playerId, action);
    }

    /**
     * 结束当前回合
     */
    endTurn(actions = {}) {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.endTurn(actions);
    }

    /**
     * 获取当前回合玩家
     */
    getCurrentTurnPlayer() {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.getCurrentPlayer();
    }

    /**
     * 添加事件触发器
     */
    addTrigger(triggerConfig) {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.addTrigger(triggerConfig);
    }

    /**
     * 调度事件
     */
    scheduleEvent(eventConfig) {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.scheduleEvent(eventConfig);
    }

    /**
     * 获取AI辅助建议
     */
    getAIAssist(playerId) {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.getAIAssist(playerId);
    }

    /**
     * 手动触发阶段转换（GM干预）
     */
    forcePhaseTransition(toPhase, reason = 'GM干预') {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.forceTransition(toPhase, reason);
    }

    /**
     * 序幕：添加世界观元素
     */
    addWorldElement(element) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.addWorldElement(element);
    }

    /**
     * 序幕：定义法则
     */
    defineRule(rule) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.defineRule(rule);
    }

    /**
     * 序幕：设定主线任务
     */
    setMainQuest(quest) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.setMainQuest(quest);
    }

    /**
     * 破章：添加敌人
     */
    addEnemy(enemy) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.addEnemy(enemy);
    }

    /**
     * 破章：添加冲突事件
     */
    addConflict(conflict) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.addConflict(conflict);
    }

    /**
     * 急章：设定Boss
     */
    setBoss(boss) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.setBoss(boss);
    }

    /**
     * 急章：击败Boss
     */
    defeatBoss() {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.defeatBoss();
    }

    /**
     * 急章：添加结局
     */
    addEnding(ending) {
        if (!this.threeActStructure) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.threeActStructure.addEnding(ending);
    }

    /**
     * 获取三幕式游戏完整状态
     */
    getThreeActState() {
        if (!this.turnManager) {
            return { error: '请先启动三幕式游戏' };
        }
        return this.turnManager.getFullState();
    }

    /**
     * 暂停三幕式游戏
     */
    pauseThreeActGame() {
        if (!this.turnManager) {
            return { error: '没有活跃的三幕式游戏' };
        }
        return this.turnManager.pause();
    }

    /**
     * 恢复三幕式游戏
     */
    resumeThreeActGame() {
        if (!this.turnManager) {
            return { error: '没有暂停的三幕式游戏' };
        }
        return this.turnManager.resume();
    }

    /**
     * 退出三幕式游戏
     */
    quitThreeActGame() {
        if (this.turnManager) {
            this.turnManager.reset();
            this.turnManager = null;
            this.threeActStructure = null;
            return { success: true, message: '🎭 三幕式游戏已退出' };
        }
        return { message: '没有活跃的三幕式游戏' };
    }

    // ============ 主题模组加载器方法 v2.7 ============
    
    /**
     * 获取所有可用主题
     */
    getAvailableThemes() {
        return this.themeLoader.getAvailableThemes();
    }

    /**
     * 加载指定主题
     * @param {string} themeType - 主题类型 (wuxia/xianxia/medieval/cyberpunk/lovecraft/shanghai)
     */
    async loadTheme(themeType) {
        return await this.themeLoader.loadTheme(themeType);
    }

    /**
     * 切换主题
     * @param {string} themeType - 目标主题
     */
    async switchTheme(themeType) {
        return await this.themeLoader.switchTheme(themeType);
    }

    /**
     * 获取当前主题
     */
    getCurrentTheme() {
        return this.themeLoader.getCurrentTheme();
    }

    /**
     * 获取当前主题数据
     * @param {string} category - 数据类别 (roles/locations/items/events/states/endings/terms)
     */
    getCurrentThemeData(category = null) {
        return this.themeLoader.getCurrentThemeData(category);
    }

    /**
     * 获取主题配置
     * @param {string} themeType - 主题类型
     */
    getThemeConfig(themeType) {
        return this.themeLoader.getThemeConfig(themeType);
    }

    /**
     * 验证主题兼容性
     * @param {string} themeType - 主题类型
     */
    validateThemeCompatibility(themeType) {
        return this.themeLoader.validateCompatibility(themeType);
    }

    /**
     * 生成主题报告
     * @param {string} themeType - 主题类型（可选，默认当前主题）
     */
    generateThemeReport(themeType = null) {
        return this.themeLoader.generateThemeReport(themeType);
    }

    /**
     * 获取主题卡牌数据
     * @param {string} themeType - 主题类型（可选）
     */
    getThemeCards(themeType = null) {
        return this.themeLoader.getThemeCards(themeType);
    }

    /**
     * 重置到基础主题
     */
    resetToBaseTheme() {
        return this.themeLoader.resetToBase();
    }

    /**
     * 导出主题配置
     */
    exportThemeConfig() {
        return this.themeLoader.exportConfig();
    }

    /**
     * 基于当前主题启动游戏
     * @param {string} gameType - 游戏类型
     * @param {Object} options - 游戏选项
     */
    async startThemedGame(gameType, options = {}) {
        // 如果指定了主题，先加载
        if (options.theme) {
            const themeResult = await this.loadTheme(options.theme);
            if (!themeResult.success) {
                return themeResult;
            }
        }

        // 获取当前主题数据
        const themeData = this.getCurrentThemeData();
        const currentTheme = this.getCurrentTheme();

        // 根据游戏类型启动
        const gameResult = this.startGame(gameType, {
            ...options,
            themeData,
            themeConfig: currentTheme ? currentTheme.config : null
        });

        return {
            ...gameResult,
            theme: currentTheme ? currentTheme.type : 'base'
        };
    }

    // ============ 剧情引擎方法 v2.8 ============
    
    /**
     * 加载针本剧本集
     * @param {Object} zhenbenData - 针本数据（从 data/zhenben_module.json）
     */
    loadZhenbenScenarios(zhenbenData) {
        return this.storyEngine.loadZhenbenScenarios(zhenbenData);
    }

    /**
     * 选择剧本
     * @param {string} scenarioId - 剧本ID (scenario-1 到 scenario-26)
     */
    selectScenario(scenarioId) {
        const result = this.storyEngine.selectScenario(scenarioId);
        
        // 如果有三幕式结构，关联到剧情引擎
        if (result.success && this.threeActStructure) {
            this.storyEngine.linkThreeActStructure(this.threeActStructure);
        }
        
        // 如果有卡牌系统，关联到剧情引擎
        if (result.success && this.cardSystem) {
            this.storyEngine.linkCardSystem(this.cardSystem);
        }
        
        return result;
    }

    /**
     * 启动剧情游戏
     * @param {string} scenarioId - 剧本ID（可选，不指定则随机选择）
     */
    startStoryGame(scenarioId = null) {
        // 如果有三幕式结构，关联到剧情引擎
        if (this.threeActStructure) {
            this.storyEngine.linkThreeActStructure(this.threeActStructure);
        }
        
        // 如果有卡牌系统，关联到剧情引擎
        if (this.cardSystem) {
            this.storyEngine.linkCardSystem(this.cardSystem);
        }
        
        return this.storyEngine.startStory(scenarioId);
    }

    /**
     * 推进剧情
     * @param {string|number} choice - 选择（可选）
     */
    advanceStory(choice = null) {
        return this.storyEngine.advanceStory(choice);
    }

    /**
     * 创建剧情选择节点
     * @param {Object} config - 节点配置
     */
    createStoryChoiceNode(config) {
        return this.storyEngine.createChoiceNode(config);
    }

    /**
     * 触发卡牌抽取（剧情节点用）
     * @param {Object} drawConfig - 抽卡配置
     */
    triggerStoryCardDraw(drawConfig = {}) {
        return this.storyEngine.triggerCardDraw(drawConfig);
    }

    /**
     * 生成诡计故事节点
     * @param {string} theme - 主题（可选）
     */
    generateTrickNode(theme = null) {
        return this.storyEngine.generateTrickStoryNode(theme);
    }

    /**
     * 定义故事结局
     * @param {string} endingId - 结局ID
     * @param {Object} config - 结局配置
     */
    defineStoryEnding(endingId, config) {
        return this.storyEngine.defineStoryEnding(endingId, config);
    }

    /**
     * 达成故事结局
     * @param {string} endingId - 结局ID
     */
    reachStoryEnding(endingId) {
        return this.storyEngine.reachStoryEnding(endingId);
    }

    /**
     * 获取剧情完整状态
     */
    getStoryState() {
        return this.storyEngine.getFullState();
    }

    /**
     * 获取剧本列表
     */
    listScenarios() {
        return this.storyEngine.listScenarios();
    }

    /**
     * 生成剧情报告
     */
    generateStoryReport() {
        return this.storyEngine.generateReport();
    }

    /**
     * 添加转换链
     * @param {string} chainId - 链ID
     * @param {Array} transformations - 转换序列
     */
    addTransformationChain(chainId, transformations) {
        return this.storyEngine.transformationChain.addChain(chainId, transformations);
    }

    /**
     * 激活转换链
     * @param {string} chainId - 链ID
     */
    activateTransformationChain(chainId) {
        return this.storyEngine.transformationChain.activateChain(chainId);
    }

    /**
     * 添加转换分支
     * @param {string} chainId - 链ID
     * @param {number} transformationIndex - 转换点索引
     * @param {Object} branchConfig - 分支配置
     */
    addTransformationBranch(chainId, transformationIndex, branchConfig) {
        return this.storyEngine.transformationChain.addBranch(chainId, transformationIndex, branchConfig);
    }

    /**
     * 注册事件触发器
     * @param {string} triggerId - 触发器ID
     * @param {Object} config - 触发器配置
     */
    registerStoryTrigger(triggerId, config) {
        return this.storyEngine.eventSystem.registerTrigger(triggerId, config);
    }

    /**
     * 手动触发故事事件
     * @param {Object} eventConfig - 事件配置
     */
    triggerStoryEvent(eventConfig) {
        return this.storyEngine.eventSystem.triggerManual(eventConfig);
    }

    /**
     * 获取结局统计
     */
    getEndingStats() {
        return this.storyEngine.endingSystem.getStats();
    }

    /**
     * 获取未解锁结局提示
     */
    getUnlockHints() {
        return this.storyEngine.endingSystem.getUnlockHints();
    }

    /**
     * 获取诡计类型列表
     */
    getTrickTypes() {
        return this.storyEngine.trickGenerator.getTrickTypes();
    }

    /**
     * 添加自定义诡计
     * @param {Object} trickConfig - 诡计配置
     */
    addCustomTrick(trickConfig) {
        return this.storyEngine.trickGenerator.addCustomTrick(trickConfig);
    }

    /**
     * 获取当前剧情节点
     */
    getCurrentStoryNode() {
        return this.storyEngine.nodeManager.currentNode;
    }

    /**
     * 获取故事上下文
     */
    getStoryContext() {
        return this.storyEngine.nodeManager.getContext();
    }

    /**
     * 更新故事上下文
     * @param {string} key - 键
     * @param {*} value - 值
     */
    updateStoryContext(key, value) {
        return this.storyEngine.nodeManager.updateContext(key, value);
    }

    /**
     * 获取节点访问历史
     */
    getStoryNodeHistory() {
        return this.storyEngine.nodeManager.getHistory();
    }

    /**
     * 重置剧情引擎
     */
    resetStoryEngine() {
        return this.storyEngine.reset();
    }

    // ============ 剧本系统方法 v2.9 ============
    
    /**
     * 加载剧本数据
     * @param {Object} zhenbenData - 针本剧本数据
     */
    loadScenarioData(zhenbenData) {
        const result = this.scenarioSystem.loadZhenbenData(zhenbenData);
        
        // 关联剧情引擎
        if (result.success && this.storyEngine) {
            this.scenarioSystem.linkStoryEngine(this.storyEngine);
        }
        
        // 关联三幕式结构
        if (result.success && this.threeActStructure) {
            this.scenarioSystem.linkThreeActStructure(this.threeActStructure);
        }
        
        // 关联角色系统
        if (result.success && this.characterSystem) {
            this.scenarioSystem.linkCharacterSystem(this.characterSystem);
        }
        
        return result;
    }

    /**
     * 选择剧本
     * @param {string} scenarioId - 剧本ID (scenario-1 到 scenario-26)
     */
    selectGameScenario(scenarioId) {
        return this.scenarioSystem.selectScenario(scenarioId);
    }

    /**
     * 随机选择剧本
     * @param {Object} filters - 筛选条件
     */
    selectRandomGameScenario(filters = {}) {
        return this.scenarioSystem.selectRandomScenario(filters);
    }

    /**
     * 按难度获取剧本
     * @param {string} difficulty - 难度级别
     */
    getScenariosByDifficulty(difficulty) {
        return this.scenarioSystem.getScenariosByDifficulty(difficulty);
    }

    /**
     * 按标签获取剧本
     * @param {string} tag - 标签
     */
    getScenariosByTag(tag) {
        return this.scenarioSystem.getScenariosByTag(tag);
    }

    /**
     * 开始当前剧本
     */
    startCurrentScenario() {
        const result = this.scenarioSystem.startCurrentScenario();
        
        // 同步启动三幕式结构
        if (result.success && !this.turnManager) {
            this.startThreeActGame();
        }
        
        return result;
    }

    /**
     * 推进当前剧本
     * @param {Object} turnData - 回合数据
     */
    advanceCurrentScenario(turnData = {}) {
        return this.scenarioSystem.advanceCurrentScenario(turnData);
    }

    /**
     * 完成当前剧本
     * @param {string} endingType - 结局类型
     */
    completeCurrentScenario(endingType = 'normal') {
        return this.scenarioSystem.completeCurrentScenario(endingType);
    }

    /**
     * 分配角色
     * @param {string} playerId - 玩家ID
     * @param {string} roleId - 角色ID
     */
    assignScenarioRole(playerId, roleId) {
        return this.scenarioSystem.assignRole(playerId, roleId);
    }

    /**
     * 批量分配角色
     * @param {Array} assignments - 分配列表 [{playerId, roleId}]
     */
    assignScenarioRoles(assignments) {
        return this.scenarioSystem.assignRoles(assignments);
    }

    /**
     * 获取可用角色
     */
    getAvailableScenarioRoles() {
        return this.scenarioSystem.getAvailableRoles();
    }

    /**
     * 发现线索
     * @param {string} clueId - 线索ID
     * @param {string} playerId - 玩家ID
     */
    discoverScenarioClue(clueId, playerId) {
        return this.scenarioSystem.discoverClue(clueId, playerId);
    }

    /**
     * 分析线索
     * @param {string} clueId - 线索ID
     * @param {string} playerId - 玩家ID
     */
    analyzeScenarioClue(clueId, playerId) {
        return this.scenarioSystem.analyzeClue(clueId, playerId);
    }

    /**
     * 关联线索
     * @param {string} clueId1 - 线索1 ID
     * @param {string} clueId2 - 线索2 ID
     * @param {string} playerId - 玩家ID
     */
    linkScenarioClues(clueId1, clueId2, playerId) {
        return this.scenarioSystem.linkClues(clueId1, clueId2, playerId);
    }

    /**
     * 获取当前剧本线索
     */
    getCurrentScenarioClues() {
        return this.scenarioSystem.getCurrentClues();
    }

    /**
     * 获取线索图谱
     */
    getScenarioClueMap() {
        return this.scenarioSystem.getClueMap();
    }

    /**
     * 列出所有剧本
     * @param {Object} filters - 筛选条件
     */
    listAllScenarios(filters = {}) {
        return this.scenarioSystem.listScenarios(filters);
    }

    /**
     * 获取剧本详情
     * @param {string} scenarioId - 剧本ID
     */
    getScenarioDetail(scenarioId) {
        return this.scenarioSystem.getScenarioDetail(scenarioId);
    }

    /**
     * 获取当前剧本状态
     */
    getCurrentScenarioStatus() {
        return this.scenarioSystem.getCurrentScenarioStatus();
    }

    /**
     * 获取剧本系统完整状态
     */
    getScenarioSystemStatus() {
        return this.scenarioSystem.getFullStatus();
    }

    /**
     * 获取玩家进度
     * @param {string} playerId - 玩家ID
     */
    getPlayerScenarioProgress(playerId) {
        return this.scenarioSystem.getPlayerProgress(playerId);
    }

    /**
     * 保存剧本进度
     */
    saveScenarioProgress() {
        return this.scenarioSystem.saveProgress();
    }

    /**
     * 加载剧本进度
     * @param {Object} data - 保存的数据
     */
    loadScenarioProgress(data) {
        return this.scenarioSystem.loadProgress(data);
    }

    /**
     * 重置剧本系统
     */
    resetScenarioSystem() {
        return this.scenarioSystem.reset();
    }

    /**
     * 生成剧本报告
     */
    generateScenarioReport() {
        return this.scenarioSystem.generateReport();
    }

    // ============ 心流引擎方法 v2.10 ============
    
    /**
     * 设置心流目标
     * @param {Object} goal - 目标配置
     */
    setFlowGoal(goal) {
        return this.flowEngine.setGoal(goal);
    }

    /**
     * 更新心流目标进度
     * @param {number} amount - 进度增量
     */
    updateFlowGoalProgress(amount = 1) {
        return this.flowEngine.updateGoalProgress(amount);
    }

    /**
     * 清除心流目标
     */
    clearFlowGoal() {
        return this.flowEngine.clearGoal();
    }

    /**
     * 获取心流目标状态
     */
    getFlowGoalStatus() {
        return this.flowEngine.getGoalStatus();
    }

    /**
     * 记录玩家行动
     * @param {Object} action - 行动数据
     */
    recordFlowAction(action) {
        return this.flowEngine.recordAction(action);
    }

    /**
     * 获取最近反馈
     * @param {number} count - 数量
     */
    getRecentFlowFeedbacks(count = 5) {
        return this.flowEngine.getRecentFeedbacks(count);
    }

    /**
     * 设置玩家技能等级
     * @param {number} level - 技能等级 (1-10)
     */
    setSkillLevel(level) {
        return this.flowEngine.setSkillLevel(level);
    }

    /**
     * 设置挑战等级
     * @param {number} level - 挑战等级 (1-5)
     */
    setChallengeLevel(level) {
        return this.flowEngine.setChallengeLevel(level);
    }

    /**
     * 自动调整难度
     */
    autoAdjustDifficulty() {
        return this.flowEngine.autoAdjustDifficulty();
    }

    /**
     * 获取难度建议
     */
    getDifficultySuggestion() {
        return this.flowEngine.getDifficultySuggestion();
    }

    /**
     * 设置沉浸等级
     * @param {number} level - 沉浸等级 (0-10)
     */
    setImmersionLevel(level) {
        return this.flowEngine.setImmersionLevel(level);
    }

    /**
     * 添加沉浸修饰器
     * @param {string} type - 类型
     * @param {number} value - 修饰值
     */
    addImmersionModifier(type, value) {
        return this.flowEngine.addImmersionModifier(type, value);
    }

    /**
     * 设置节奏状态
     * @param {string} state - 节奏状态
     */
    setPacingState(state) {
        return this.flowEngine.setPacing(state);
    }

    /**
     * 获取节奏建议
     */
    getPacingSuggestion() {
        return this.flowEngine.getPacingSuggestion();
    }

    /**
     * 更新掌控感
     */
    updateControlSense() {
        return this.flowEngine.updateControlSense();
    }

    /**
     * 提供选择权
     * @param {Array} choices - 选项列表
     */
    presentFlowChoices(choices) {
        return this.flowEngine.presentChoices(choices);
    }

    /**
     * 增加角色融合度
     * @param {number} amount - 融合增量
     */
    increaseCharacterFusion(amount = 1) {
        return this.flowEngine.increaseCharacterFusion(amount);
    }

    /**
     * 记录角色扮演事件
     * @param {Object} event - 扮演事件
     */
    recordRoleplayEvent(event) {
        return this.flowEngine.recordRoleplayEvent(event);
    }

    /**
     * 获取角色融合状态
     */
    getCharacterFusionStatus() {
        return this.flowEngine.getCharacterFusionStatus();
    }

    /**
     * 注册成就
     * @param {Object} achievementConfig - 成就配置
     */
    registerAchievement(achievementConfig) {
        return this.flowEngine.registerAchievement(achievementConfig);
    }

    /**
     * 解锁成就
     * @param {string} achievementId - 成就ID
     */
    unlockAchievement(achievementId) {
        return this.flowEngine.unlockAchievement(achievementId);
    }

    /**
     * 列出所有成就
     */
    listAchievements() {
        return this.flowEngine.listAchievements();
    }

    /**
     * 获取已解锁成就
     */
    getUnlockedAchievements() {
        return this.flowEngine.getUnlockedAchievements();
    }

    /**
     * 添加提示
     * @param {Object} hintConfig - 提示配置
     */
    addFlowHint(hintConfig) {
        return this.flowEngine.addHint(hintConfig);
    }

    /**
     * 获取提示
     * @param {string} context - 上下文
     */
    getFlowHint(context = null) {
        return this.flowEngine.getHint(context);
    }

    /**
     * 列出所有提示
     */
    listFlowHints() {
        return this.flowEngine.listHints();
    }

    /**
     * 获取心流状态
     */
    getFlowState() {
        return this.flowEngine.getFlowState();
    }

    /**
     * 获取心流引擎完整状态
     */
    getFlowFullState() {
        return this.flowEngine.getFullState();
    }

    /**
     * 生成心流报告
     */
    generateFlowReport() {
        return this.flowEngine.generateReport();
    }

    /**
     * 重置心流引擎
     */
    resetFlowEngine() {
        return this.flowEngine.reset();
    }
}

// 导出
module.exports = {
    InteractiveGames,
    GameEngine,
    AdventureGame,
    PuzzleGame,
    StoryGenerator,
    MultiplayerGameEngine,
    MultiplayerWuxiaGame,
    // 卡牌系统
    CardSystem,
    CardType,
    Theme,
    // 三幕式系统 v2.3
    ThreeActStructure,
    TurnManager,
    ActPhase,
    ActPhaseNames,
    ActPhaseDescriptions,
    TurnState,
    EventType,
    TriggerType,
    // 主题模组系统 v2.7
    ThemeSystem,
    ThemeLoader,
    ThemeCardManager,
    ThemeStoryGenerator,
    ArtStyleManager,
    THEMES,
    THEME_CARD_LIBRARIES,
    THEME_STORY_TEMPLATES,
    ART_STYLE_TAGS,
    // 主题模组加载器 v2.7 (向后兼容)
    ThemeModuleLoader,
    ThemeType,
    // 剧情引擎系统 v2.8
    StoryEngine,
    TransformationChain,
    StoryNodeManager,
    EventTriggerSystem,
    EndingSystem,
    CoreTrickGenerator,
    StoryNodeType,
    EndingType,
    BranchState,
    // 剧本系统 v2.9
    ScenarioSystem,
    Scenario,
    ScenarioProgressManager,
    ClueSystem,
    ScenarioState,
    DifficultyLevel,
    ClueState,
    CharacterRoleState,
    // 心流引擎系统 v2.10
    FlowEngine,
    FlowState,
    ChallengeLevel,
    FeedbackType,
    Achievement,
    Reward,
    Hint
};

// 导出沙箱检查函数（供外部调用）
module.exports.createGameSession = function(hostId) {
    const games = new InteractiveGames();
    games.startMultiplayerGame('wuxia', { hostId });
    return {
        games,
        processInput: (input, playerId) => games.safeHandleInput(input, playerId),
        isInSandbox: () => games.isInSandbox(),
        getStatus: () => games.getStatus()
    };
};

// 命令行测试
if (require.main === module) {
    console.log('🎮 Interactive Games Framework v2.3');
    console.log('作者：杨云霄（OpenClaw）');
    console.log('为杨督察创建');
    console.log('支持单人游戏 + 多人游戏 + 卡牌系统 + 三幕式结构');
    
    const games = new InteractiveGames();
    
    // 测试卡牌系统
    console.log('\n=== 测试卡牌系统 ===');
    console.log('卡牌统计:', games.getCardStats().byType);
    
    // 抽卡测试
    console.log('\n--- 抽卡测试 ---');
    const drawResult = games.drawCards('role', 1);
    console.log('抽到的角色:', drawResult.card?.name);
    
    const multiDraw = games.drawCards('all', 3);
    console.log('抽到3张牌:', multiDraw.cards?.map(c => c.name));
    
    // 生成故事
    console.log('\n--- 生成故事 ---');
    const story = games.generateStoryScene();
    console.log('故事场景:', story);
    
    // 测试多人武侠游戏
    console.log('\n=== 测试多人武侠游戏 ===');
    const mpResult = games.startMultiplayerGame('wuxia');
    console.log(mpResult.message);
    
    // 添加玩家
    console.log('\n--- 添加玩家 ---');
    console.log(games.addPlayer('player1', '张三'));
    console.log(games.addPlayer('player2', '李四'));
    
    // 设置模式
    console.log('\n--- 设置协作模式 ---');
    console.log(games.setMultiplayerMode('coop'));
    
    // 开始游戏
    console.log('\n--- 开始游戏 ---');
    const startResult = games.beginMultiplayerGame();
    console.log(startResult.scene);
    
    // 测试三幕式系统
    console.log('\n=== 测试三幕式系统 v2.3 ===');
    const threeAct = new InteractiveGames();
    const taResult = threeAct.startThreeActGame({
        prologueMinTurns: 1,
        prologueMaxTurns: 2,
        conflictMinTurns: 1,
        conflictMaxTurns: 2,
        climaxMinTurns: 1,
        climaxMaxTurns: 1
    });
    console.log(taResult.message);
    console.log('当前阶段:', taResult.phaseName);
    console.log('阶段描述:', taResult.phaseDescription);
    
    // 添加玩家
    console.log('\n--- 添加三幕式玩家 ---');
    console.log(threeAct.addThreeActPlayer('p1', { name: '云霄' }));
    console.log(threeAct.addThreeActPlayer('p2', { name: '清心' }));
    
    // 序幕测试
    console.log('\n--- 序幕阶段测试 ---');
    threeAct.startTurn();
    threeAct.addWorldElement({ name: '云雾山', type: 'location' });
    threeAct.defineRule('山中一日，世上千年');
    threeAct.setMainQuest('寻找传说中的仙人洞府');
    const prologueEnd = threeAct.endTurn();
    console.log('帷幕回合1结束');
    console.log('阶段转换:', prologueEnd.threeActResult?.transition?.reason || '继续序幕');
    
    // 序幕回合2 - 触发转换
    threeAct.startTurn();
    threeAct.addWorldElement({ name: '神秘古洞', type: 'location' });
    const prologueEnd2 = threeAct.endTurn();
    console.log('帷幕回合2结束');
    console.log('阶段转换:', prologueEnd2.threeActResult?.transition?.reason || '无转换');
    
    // 破章测试
    console.log('\n--- 破章阶段测试 ---');
    console.log('当前阶段:', threeAct.getCurrentPhase().phaseName);
    threeAct.startTurn();
    threeAct.addEnemy({ name: '山精', level: 5 });
    threeAct.addConflict({ type: 'battle', description: '遭遇山精袭击' });
    const conflictEnd = threeAct.endTurn();
    console.log('破章回合1结束');
    console.log('阶段转换:', conflictEnd.threeActResult?.transition?.reason || '继续破章');
    
    // 破章回合2
    threeAct.startTurn();
    threeAct.addEnemy({ name: '石像守卫', level: 8 });
    const conflictEnd2 = threeAct.endTurn();
    console.log('破章回合2结束');
    console.log('阶段转换:', conflictEnd2.threeActResult?.transition?.reason || '无转换');
    
    // 急章测试
    console.log('\n--- 急章阶段测试 ---');
    console.log('当前阶段:', threeAct.getCurrentPhase().phaseName);
    threeAct.startTurn();
    threeAct.setBoss({ name: '上古剑灵', hp: 1000, skills: ['剑气纵横', '万剑归宗'] });
    threeAct.defeatBoss();
    threeAct.addEnding('成功获得仙人洞府的传承，修为大进');
    const climaxEnd = threeAct.endTurn();
    console.log('急章回合结束');
    console.log('阶段转换:', climaxEnd.threeActResult?.transition?.reason || '无转换');
    
    // 最终状态
    console.log('\n--- 最终状态 ---');
    const finalState = threeAct.getThreeActState();
    console.log('总回合数:', finalState.turn.current);
    console.log('结局:', finalState.threeAct.phaseState.climax.endings);
    console.log('\n✅ 三幕式系统测试完成！');
}
