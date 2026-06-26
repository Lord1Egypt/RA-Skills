/**
 * ScenarioSystem - 剧本系统
 * 管理26个克苏鲁剧本的选择、进度、角色分配、线索系统
 * 
 * v2.9.0 实现
 * 
 * 设计理念：
 * - 剧本选择：从26个克苏鲁剧本中选择（按编号/主题/难度）
 * - 进度追踪：记录玩家在每个剧本中的进度
 * - 角色分配：为剧本分配角色，支持多角色同时参与
 * - 线索管理：管理剧本中的线索发现和解锁
 * - 与剧情引擎无缝集成：ScenarioSystem + StoryEngine = 完整体验
 */

// 剧本状态
const ScenarioState = {
    LOCKED: 'locked',           // 锁定状态
    AVAILABLE: 'available',     // 可用状态
    IN_PROGRESS: 'in_progress', // 进行中
    COMPLETED: 'completed',     // 已完成
    MASTERED: 'mastered'        // 已精通（达成所有结局）
};

// 剧本难度
const DifficultyLevel = {
    NOVICE: 'novice',           // 新手级
    APPRENTICE: 'apprentice',   // 学徒级
    INVESTIGATOR: 'investigator', // 调查员级
    KEEPER: 'keeper',           // 守密人级
    MASTER: 'master'            // 大师级
};

// 线索状态
const ClueState = {
    HIDDEN: 'hidden',           // 隐藏
    DISCOVERED: 'discovered',   // 已发现
    ANALYZED: 'analyzed',       // 已分析
    LINKED: 'linked',           // 已关联
    RESOLVED: 'resolved'        // 已解决
};

// 角色状态
const CharacterRoleState = {
    AVAILABLE: 'available',     // 可选择
    ASSIGNED: 'assigned',       // 已分配
    ACTIVE: 'active',           // 活跃中
    ELIMINATED: 'eliminated',   // 已淘汰
    SURVIVED: 'survived'        // 存活
};

/**
 * 剧本类 - 单个剧本的完整数据结构
 */
class Scenario {
    constructor(data) {
        this.id = `scenario-${data.编号}`;
        this.number = data.编号;
        this.title = data.目录 || `剧本${data.编号}`;
        this.theme = data.主题 || '';
        this.coreTransformation = data.核心转换 || '';
        this.coreTrick = data.核心诡计 || '';
        this.characterFeatures = data.角色特征 || '';
        
        // 系统属性
        this.state = ScenarioState.AVAILABLE;
        this.difficulty = this._calculateDifficulty(data);
        this.tags = this._extractTags(data);
        
        // 进度追踪
        this.progress = {
            started: false,
            startTime: null,
            endTime: null,
            turnsPlayed: 0,
            phasesCompleted: [],
            percentage: 0
        };
        
        // 角色相关
        this.roles = this._parseRoles(data.角色特征);
        this.assignedCharacters = new Map();
        
        // 线索系统
        this.clues = this._generateClues(data);
        
        // 结局记录
        this.endings = {
            reached: [],
            available: ['good', 'bad', 'normal'],
            secret: []
        };
        
        // 统计数据
        this.stats = {
            playCount: 0,
            completionCount: 0,
            averageTurns: 0,
            successRate: 0
        };
        
        // 元数据
        this.metadata = {
            createdAt: Date.now(),
            lastPlayed: null,
            lastModified: null,
            notes: ''
        };
    }

    /**
     * 计算剧本难度
     */
    _calculateDifficulty(data) {
        let score = 0;
        
        // 基于核心诡计复杂度
        if (data.核心诡计) {
            score += data.核心诡计.length > 100 ? 2 : 1;
        }
        
        // 基于核心转换复杂度
        if (data.核心转换) {
            const transformations = data.核心转换.split(/[，。；\n]/).filter(p => p.trim());
            score += Math.min(transformations.length, 3);
        }
        
        // 基于角色数量
        if (data.角色特征) {
            const roles = data.角色特征.split(/[，、\s]/).filter(r => r.trim());
            score += Math.min(roles.length, 2);
        }
        
        // 映射到难度等级
        if (score <= 2) return DifficultyLevel.NOVICE;
        if (score <= 4) return DifficultyLevel.APPRENTICE;
        if (score <= 6) return DifficultyLevel.INVESTIGATOR;
        if (score <= 8) return DifficultyLevel.KEEPER;
        return DifficultyLevel.MASTER;
    }

    /**
     * 提取标签
     */
    _extractTags(data) {
        const tags = [];
        
        // 从主题提取
        if (data.主题) {
            const themeKeywords = ['神话', '时间', '空间', '梦境', '祭祀', '实验', '失踪', '复仇', '病毒', '怪物'];
            themeKeywords.forEach(keyword => {
                if (data.主题.includes(keyword)) {
                    tags.push(keyword);
                }
            });
        }
        
        // 从核心转换提取
        if (data.核心转换) {
            if (data.核心转换.includes('召唤')) tags.push('召唤');
            if (data.核心转换.includes('附身')) tags.push('附身');
            if (data.核心转换.includes('时间')) tags.push('时间操控');
            if (data.核心转换.includes('空间')) tags.push('空间转换');
        }
        
        return [...new Set(tags)]; // 去重
    }

    /**
     * 解析角色特征
     */
    _parseRoles(characterFeatures) {
        if (!characterFeatures) return [];
        
        const roles = [];
        const parts = characterFeatures.split(/[，、\n]/).filter(p => p.trim());
        
        parts.forEach((part, index) => {
            const trimmed = part.trim();
            if (trimmed && trimmed.length > 1) {
                roles.push({
                    id: `role-${this.number}-${index}`,
                    name: trimmed,
                    description: `${this.title}中的${trimmed}`,
                    state: CharacterRoleState.AVAILABLE,
                    skills: [],
                    secrets: []
                });
            }
        });
        
        // 如果没有指定角色，创建默认角色
        if (roles.length === 0) {
            roles.push({
                id: `role-${this.number}-default`,
                name: '调查员',
                description: `${this.title}的调查员`,
                state: CharacterRoleState.AVAILABLE,
                skills: ['调查', '观察'],
                secrets: []
            });
        }
        
        return roles;
    }

    /**
     * 生成线索
     */
    _generateClues(data) {
        const clues = [];
        
        // 从核心诡计生成线索
        if (data.核心诡计) {
            const trickParts = data.核心诡计.split(/[，。；\n]/).filter(p => p.trim());
            trickParts.forEach((part, index) => {
                if (part.trim().length > 5) {
                    clues.push({
                        id: `clue-${this.number}-trick-${index}`,
                        type: 'trick',
                        content: part.trim(),
                        hint: `这与${this.title}的核心谜题有关`,
                        state: ClueState.HIDDEN,
                        discoveredBy: null,
                        discoveredAt: null,
                        connections: []
                    });
                }
            });
        }
        
        // 从核心转换生成线索
        if (data.核心转换) {
            const transParts = data.核心转换.split(/[，。；\n]/).filter(p => p.trim());
            transParts.forEach((part, index) => {
                if (part.trim().length > 5) {
                    clues.push({
                        id: `clue-${this.number}-trans-${index}`,
                        type: 'transformation',
                        content: part.trim(),
                        hint: `关键转换线索`,
                        state: ClueState.HIDDEN,
                        discoveredBy: null,
                        discoveredAt: null,
                        connections: []
                    });
                }
            });
        }
        
        // 从主题生成线索
        if (data.主题) {
            clues.push({
                id: `clue-${this.number}-theme`,
                type: 'theme',
                content: data.主题,
                hint: `剧本主题线索`,
                state: ClueState.HIDDEN,
                discoveredBy: null,
                discoveredAt: null,
                connections: []
            });
        }
        
        return clues;
    }

    /**
     * 开始剧本
     */
    start() {
        this.state = ScenarioState.IN_PROGRESS;
        this.progress.started = true;
        this.progress.startTime = Date.now();
        this.progress.endTime = null;
        this.progress.turnsPlayed = 0;
        this.progress.phasesCompleted = [];
        this.progress.percentage = 0;
        this.stats.playCount++;
        this.metadata.lastPlayed = Date.now();
        
        return {
            success: true,
            scenario: this.getInfo(),
            message: `🎭 剧本《${this.title}》已开始`
        };
    }

    /**
     * 推进剧本
     */
    advance(turnData = {}) {
        if (this.state !== ScenarioState.IN_PROGRESS) {
            return { error: '剧本未在进行中' };
        }
        
        this.progress.turnsPlayed++;
        
        // 更新进度百分比
        if (turnData.phaseCompleted) {
            this.progress.phasesCompleted.push(turnData.phaseCompleted);
        }
        
        this.progress.percentage = this._calculateProgress(turnData);
        
        return {
            success: true,
            progress: this.progress,
            message: `剧本进度：${this.progress.percentage}%`
        };
    }

    /**
     * 计算进度百分比
     */
    _calculateProgress(turnData) {
        const clueProgress = this.clues.filter(c => c.state !== ClueState.HIDDEN).length / 
                            Math.max(this.clues.length, 1) * 40;
        
        const phaseProgress = this.progress.phasesCompleted.length >= 3 ? 40 : 
                             this.progress.phasesCompleted.length * 15;
        
        const turnProgress = Math.min(this.progress.turnsPlayed * 2, 20);
        
        return Math.min(Math.round(clueProgress + phaseProgress + turnProgress), 100);
    }

    /**
     * 完成剧本
     */
    complete(endingType = 'normal') {
        this.state = ScenarioState.COMPLETED;
        this.progress.endTime = Date.now();
        this.progress.percentage = 100;
        this.stats.completionCount++;
        
        // 记录结局
        if (!this.endings.reached.includes(endingType)) {
            this.endings.reached.push(endingType);
        }
        
        // 检查是否精通
        if (this.endings.reached.length >= this.endings.available.length) {
            this.state = ScenarioState.MASTERED;
        }
        
        return {
            success: true,
            scenario: this.getInfo(),
            ending: endingType,
            message: `🎉 剧本《${this.title}》已完成！结局：${endingType}`
        };
    }

    /**
     * 分配角色
     */
    assignRole(playerId, roleId) {
        const role = this.roles.find(r => r.id === roleId);
        if (!role) {
            return { error: '角色不存在', roleId };
        }
        
        if (role.state !== CharacterRoleState.AVAILABLE) {
            return { error: '角色已被分配', roleId };
        }
        
        role.state = CharacterRoleState.ASSIGNED;
        this.assignedCharacters.set(playerId, {
            playerId,
            roleId,
            assignedAt: Date.now()
        });
        
        return {
            success: true,
            role,
            message: `👤 玩家 ${playerId} 已选择角色：${role.name}`
        };
    }

    /**
     * 激活角色
     */
    activateRole(playerId) {
        const assignment = this.assignedCharacters.get(playerId);
        if (!assignment) {
            return { error: '玩家未分配角色' };
        }
        
        const role = this.roles.find(r => r.id === assignment.roleId);
        if (role) {
            role.state = CharacterRoleState.ACTIVE;
        }
        
        return {
            success: true,
            role,
            message: `🎮 角色 ${role?.name} 已激活`
        };
    }

    /**
     * 发现线索
     */
    discoverClue(clueId, playerId) {
        const clue = this.clues.find(c => c.id === clueId);
        if (!clue) {
            return { error: '线索不存在', clueId };
        }
        
        clue.state = ClueState.DISCOVERED;
        clue.discoveredBy = playerId;
        clue.discoveredAt = Date.now();
        
        return {
            success: true,
            clue,
            message: `🔍 发现线索：${clue.content.substring(0, 30)}...`
        };
    }

    /**
     * 分析线索
     */
    analyzeClue(clueId) {
        const clue = this.clues.find(c => c.id === clueId);
        if (!clue) {
            return { error: '线索不存在', clueId };
        }
        
        if (clue.state !== ClueState.DISCOVERED) {
            return { error: '线索未发现，无法分析' };
        }
        
        clue.state = ClueState.ANALYZED;
        
        return {
            success: true,
            clue,
            analysis: `分析结果：${clue.hint}`,
            message: `📊 线索已分析`
        };
    }

    /**
     * 关联线索
     */
    linkClues(clueId1, clueId2) {
        const clue1 = this.clues.find(c => c.id === clueId1);
        const clue2 = this.clues.find(c => c.id === clueId2);
        
        if (!clue1 || !clue2) {
            return { error: '线索不存在' };
        }
        
        if (clue1.state !== ClueState.ANALYZED || clue2.state !== ClueState.ANALYZED) {
            return { error: '线索需要先分析才能关联' };
        }
        
        clue1.connections.push(clueId2);
        clue2.connections.push(clueId1);
        clue1.state = ClueState.LINKED;
        clue2.state = ClueState.LINKED;
        
        return {
            success: true,
            message: `🔗 线索已关联`,
            connection: {
                clue1: clue1.content.substring(0, 20),
                clue2: clue2.content.substring(0, 20)
            }
        };
    }

    /**
     * 获取剧本信息
     */
    getInfo() {
        return {
            id: this.id,
            number: this.number,
            title: this.title,
            theme: this.theme,
            difficulty: this.difficulty,
            tags: this.tags,
            state: this.state,
            progress: this.progress,
            roles: this.roles.map(r => ({
                id: r.id,
                name: r.name,
                state: r.state
            })),
            clues: {
                total: this.clues.length,
                discovered: this.clues.filter(c => c.state !== ClueState.HIDDEN).length,
                analyzed: this.clues.filter(c => c.state === ClueState.ANALYZED || c.state === ClueState.LINKED).length
            },
            endings: {
                reached: this.endings.reached,
                total: this.endings.available.length + this.endings.secret.length
            },
            stats: this.stats
        };
    }

    /**
     * 获取完整数据（用于保存）
     */
    serialize() {
        return {
            id: this.id,
            number: this.number,
            title: this.title,
            theme: this.theme,
            coreTransformation: this.coreTransformation,
            coreTrick: this.coreTrick,
            characterFeatures: this.characterFeatures,
            state: this.state,
            difficulty: this.difficulty,
            tags: this.tags,
            progress: this.progress,
            roles: this.roles,
            assignedCharacters: Array.from(this.assignedCharacters.entries()),
            clues: this.clues,
            endings: this.endings,
            stats: this.stats,
            metadata: this.metadata
        };
    }

    /**
     * 从保存数据恢复
     */
    static deserialize(data) {
        const scenario = new Scenario({
            编号: data.number,
            目录: data.title,
            主题: data.theme,
            核心转换: data.coreTransformation,
            核心诡计: data.coreTrick,
            角色特征: data.characterFeatures
        });
        
        scenario.state = data.state;
        scenario.difficulty = data.difficulty;
        scenario.tags = data.tags;
        scenario.progress = data.progress;
        scenario.roles = data.roles;
        scenario.assignedCharacters = new Map(data.assignedCharacters);
        scenario.clues = data.clues;
        scenario.endings = data.endings;
        scenario.stats = data.stats;
        scenario.metadata = data.metadata;
        
        return scenario;
    }

    /**
     * 重置剧本
     */
    reset() {
        this.state = ScenarioState.AVAILABLE;
        this.progress = {
            started: false,
            startTime: null,
            endTime: null,
            turnsPlayed: 0,
            phasesCompleted: [],
            percentage: 0
        };
        
        this.roles.forEach(role => {
            role.state = CharacterRoleState.AVAILABLE;
        });
        this.assignedCharacters.clear();
        
        this.clues.forEach(clue => {
            clue.state = ClueState.HIDDEN;
            clue.discoveredBy = null;
            clue.discoveredAt = null;
            clue.connections = [];
        });
        
        this.metadata.lastModified = Date.now();
        
        return { success: true, message: `剧本《${this.title}》已重置` };
    }
}

/**
 * 剧本进度管理器
 */
class ScenarioProgressManager {
    constructor() {
        this.playerProgress = new Map();  // 玩家 -> 剧本进度映射
        this.globalProgress = {
            totalScenarios: 0,
            completedScenarios: 0,
            masteredScenarios: 0,
            totalPlayTime: 0
        };
    }

    /**
     * 记录玩家开始剧本
     */
    recordStart(playerId, scenarioId) {
        if (!this.playerProgress.has(playerId)) {
            this.playerProgress.set(playerId, {
                scenarios: new Map(),
                totalPlayTime: 0,
                achievements: []
            });
        }
        
        const playerData = this.playerProgress.get(playerId);
        playerData.scenarios.set(scenarioId, {
            startedAt: Date.now(),
            completed: false,
            turns: 0,
            endings: []
        });
        
        return { success: true };
    }

    /**
     * 记录玩家完成剧本
     */
    recordCompletion(playerId, scenarioId, endingType) {
        const playerData = this.playerProgress.get(playerId);
        if (!playerData) {
            return { error: '玩家数据不存在' };
        }
        
        const scenarioData = playerData.scenarios.get(scenarioId);
        if (!scenarioData) {
            return { error: '剧本数据不存在' };
        }
        
        scenarioData.completed = true;
        scenarioData.completedAt = Date.now();
        scenarioData.playTime = scenarioData.completedAt - scenarioData.startedAt;
        scenarioData.endings.push(endingType);
        
        // 更新全局进度
        this.globalProgress.completedScenarios++;
        
        return { success: true, playTime: scenarioData.playTime };
    }

    /**
     * 获取玩家进度
     */
    getPlayerProgress(playerId) {
        const data = this.playerProgress.get(playerId);
        if (!data) {
            return {
                scenarios: [],
                totalPlayTime: 0,
                achievements: [],
                completionRate: 0
            };
        }
        
        const scenarios = Array.from(data.scenarios.entries()).map(([id, s]) => ({
            scenarioId: id,
            ...s
        }));
        
        const completed = scenarios.filter(s => s.completed).length;
        
        return {
            scenarios,
            totalPlayTime: data.totalPlayTime,
            achievements: data.achievements,
            completionRate: this.globalProgress.totalScenarios > 0 ? 
                           completed / this.globalProgress.totalScenarios : 0
        };
    }

    /**
     * 获取全局统计
     */
    getGlobalStats() {
        return {
            ...this.globalProgress,
            activePlayers: this.playerProgress.size
        };
    }

    /**
     * 导出进度数据
     */
    export() {
        return {
            playerProgress: Array.from(this.playerProgress.entries()).map(([id, data]) => ({
                playerId: id,
                scenarios: Array.from(data.scenarios.entries()),
                totalPlayTime: data.totalPlayTime,
                achievements: data.achievements
            })),
            globalProgress: this.globalProgress
        };
    }

    /**
     * 导入进度数据
     */
    import(data) {
        if (data.playerProgress) {
            data.playerProgress.forEach(p => {
                this.playerProgress.set(p.playerId, {
                    scenarios: new Map(p.scenarios),
                    totalPlayTime: p.totalPlayTime,
                    achievements: p.achievements
                });
            });
        }
        
        if (data.globalProgress) {
            this.globalProgress = data.globalProgress;
        }
        
        return { success: true };
    }
}

/**
 * 线索系统
 */
class ClueSystem {
    constructor() {
        this.clueRegistry = new Map();   // 所有线索注册表
        this.clueConnections = new Map(); // 线索关联图谱
        this.discoveryLog = [];           // 发现日志
    }

    /**
     * 注册线索
     */
    registerClue(clue) {
        this.clueRegistry.set(clue.id, {
            ...clue,
            registeredAt: Date.now()
        });
        
        if (!this.clueConnections.has(clue.id)) {
            this.clueConnections.set(clue.id, new Set());
        }
        
        return { success: true, clueId: clue.id };
    }

    /**
     * 发现线索
     */
    discoverClue(clueId, playerId, context = {}) {
        const clue = this.clueRegistry.get(clueId);
        if (!clue) {
            return { error: '线索未注册' };
        }
        
        if (clue.state !== ClueState.HIDDEN) {
            return { error: '线索已被发现', clue };
        }
        
        clue.state = ClueState.DISCOVERED;
        clue.discoveredBy = playerId;
        clue.discoveredAt = Date.now();
        clue.discoveryContext = context;
        
        // 记录日志
        this.discoveryLog.push({
            clueId,
            playerId,
            action: 'discover',
            timestamp: Date.now(),
            context
        });
        
        return {
            success: true,
            clue,
            message: `🔍 发现新线索！`
        };
    }

    /**
     * 分析线索
     */
    analyzeClue(clueId, playerId) {
        const clue = this.clueRegistry.get(clueId);
        if (!clue) {
            return { error: '线索未注册' };
        }
        
        if (clue.state !== ClueState.DISCOVERED) {
            return { error: '线索需要先发现才能分析' };
        }
        
        clue.state = ClueState.ANALYZED;
        clue.analyzedBy = playerId;
        clue.analyzedAt = Date.now();
        
        // 分析可能揭示隐藏关联
        const relatedClues = this._findRelatedClues(clue);
        
        this.discoveryLog.push({
            clueId,
            playerId,
            action: 'analyze',
            timestamp: Date.now()
        });
        
        return {
            success: true,
            clue,
            relatedClues,
            message: `📊 线索分析完成`
        };
    }

    /**
     * 查找相关线索
     */
    _findRelatedClues(clue) {
        const connections = this.clueConnections.get(clue.id) || new Set();
        return Array.from(connections).map(id => this.clueRegistry.get(id)).filter(Boolean);
    }

    /**
     * 关联线索
     */
    linkClues(clueId1, clueId2, playerId) {
        const clue1 = this.clueRegistry.get(clueId1);
        const clue2 = this.clueRegistry.get(clueId2);
        
        if (!clue1 || !clue2) {
            return { error: '线索不存在' };
        }
        
        if (clue1.state !== ClueState.ANALYZED || clue2.state !== ClueState.ANALYZED) {
            return { error: '两条线索都需要先分析才能关联' };
        }
        
        // 双向关联
        const connections1 = this.clueConnections.get(clueId1);
        const connections2 = this.clueConnections.get(clueId2);
        
        connections1.add(clueId2);
        connections2.add(clueId1);
        
        clue1.state = ClueState.LINKED;
        clue2.state = ClueState.LINKED;
        
        // 检查是否形成线索链
        const chainLength = this._calculateChainLength(clueId1);
        
        this.discoveryLog.push({
            clueId: clueId1,
            targetClueId: clueId2,
            playerId,
            action: 'link',
            timestamp: Date.now()
        });
        
        return {
            success: true,
            message: `🔗 线索已关联`,
            chainLength,
            isComplete: chainLength >= 3
        };
    }

    /**
     * 计算线索链长度
     */
    _calculateChainLength(startClueId, visited = new Set()) {
        if (visited.has(startClueId)) return 0;
        visited.add(startClueId);
        
        const connections = this.clueConnections.get(startClueId) || new Set();
        let maxLength = 1;
        
        for (const connectedId of connections) {
            const clue = this.clueRegistry.get(connectedId);
            if (clue && clue.state === ClueState.LINKED) {
                const length = this._calculateChainLength(connectedId, visited);
                maxLength = Math.max(maxLength, length + 1);
            }
        }
        
        return maxLength;
    }

    /**
     * 获取线索图谱
     */
    getClueMap() {
        const nodes = [];
        const edges = [];
        
        for (const [id, clue] of this.clueRegistry) {
            nodes.push({
                id,
                type: clue.type,
                state: clue.state,
                content: clue.content.substring(0, 50)
            });
            
            const connections = this.clueConnections.get(id) || new Set();
            for (const connectedId of connections) {
                edges.push({
                    source: id,
                    target: connectedId
                });
            }
        }
        
        return { nodes, edges };
    }

    /**
     * 获取发现日志
     */
    getDiscoveryLog(limit = 50) {
        return this.discoveryLog.slice(-limit);
    }

    /**
     * 重置线索系统
     */
    reset() {
        this.clueRegistry.forEach(clue => {
            clue.state = ClueState.HIDDEN;
            clue.discoveredBy = null;
            clue.discoveredAt = null;
            clue.analyzedBy = null;
            clue.analyzedAt = null;
        });
        
        this.discoveryLog = [];
        return { success: true };
    }
}

/**
 * 剧本系统主类
 */
class ScenarioSystem {
    constructor(config = {}) {
        this.config = {
            autoSave: config.autoSave !== false,
            maxActiveScenarios: config.maxActiveScenarios || 3,
            ...config
        };
        
        // 核心组件
        this.scenarios = new Map();          // 所有剧本
        this.progressManager = new ScenarioProgressManager();
        this.clueSystem = new ClueSystem();
        
        // 当前活跃剧本
        this.activeScenario = null;
        this.activeScenarios = new Map();    // 多剧本支持
        
        // 关联系统
        this.storyEngine = null;
        this.threeActStructure = null;
        this.characterSystem = null;
        
        // 状态
        this.initialized = false;
        this.zhenbenData = null;
    }

    /**
     * 加载针本剧本集
     */
    loadZhenbenData(zhenbenData) {
        if (!zhenbenData || !zhenbenData.大纲) {
            return { error: '无效的针本数据' };
        }
        
        this.zhenbenData = zhenbenData;
        
        // 创建剧本实例
        zhenbenData.大纲.forEach(scenarioData => {
            const scenario = new Scenario(scenarioData);
            this.scenarios.set(scenario.id, scenario);
            
            // 注册线索到线索系统
            scenario.clues.forEach(clue => {
                this.clueSystem.registerClue(clue);
            });
        });
        
        // 更新全局进度
        this.progressManager.globalProgress.totalScenarios = this.scenarios.size;
        
        this.initialized = true;
        
        return {
            success: true,
            count: this.scenarios.size,
            message: `📜 已加载 ${this.scenarios.size} 个剧本`
        };
    }

    /**
     * 关联剧情引擎
     */
    linkStoryEngine(storyEngine) {
        this.storyEngine = storyEngine;
        
        // 如果剧情引擎有三幕式结构，也关联
        if (storyEngine.threeActStructure) {
            this.threeActStructure = storyEngine.threeActStructure;
        }
        
        return { success: true };
    }

    /**
     * 关联角色系统
     */
    linkCharacterSystem(characterSystem) {
        this.characterSystem = characterSystem;
        return { success: true };
    }

    /**
     * 关联三幕式结构
     */
    linkThreeActStructure(threeActStructure) {
        this.threeActStructure = threeActStructure;
        return { success: true };
    }

    /**
     * 选择剧本
     */
    selectScenario(scenarioId) {
        const scenario = this.scenarios.get(scenarioId);
        if (!scenario) {
            return { error: '剧本不存在', scenarioId };
        }
        
        if (scenario.state === ScenarioState.IN_PROGRESS) {
            return { error: '剧本已在进行中', scenarioId };
        }
        
        this.activeScenario = scenario;
        
        // 如果关联了剧情引擎，同步选择
        if (this.storyEngine) {
            this.storyEngine.selectScenario(scenarioId);
        }
        
        return {
            success: true,
            scenario: scenario.getInfo(),
            message: `📖 已选择剧本：《${scenario.title}》`
        };
    }

    /**
     * 随机选择剧本
     */
    selectRandomScenario(filters = {}) {
        let candidates = Array.from(this.scenarios.values());
        
        // 应用过滤器
        if (filters.difficulty) {
            candidates = candidates.filter(s => s.difficulty === filters.difficulty);
        }
        
        if (filters.tags && filters.tags.length > 0) {
            candidates = candidates.filter(s => 
                filters.tags.some(tag => s.tags.includes(tag))
            );
        }
        
        if (filters.state) {
            candidates = candidates.filter(s => s.state === filters.state);
        }
        
        // 排除已完成的（可选）
        if (filters.excludeCompleted) {
            candidates = candidates.filter(s => s.state !== ScenarioState.COMPLETED);
        }
        
        if (candidates.length === 0) {
            return { error: '没有符合条件的剧本', filters };
        }
        
        // 随机选择
        const selected = candidates[Math.floor(Math.random() * candidates.length)];
        return this.selectScenario(selected.id);
    }

    /**
     * 按难度筛选剧本
     */
    getScenariosByDifficulty(difficulty) {
        return Array.from(this.scenarios.values())
            .filter(s => s.difficulty === difficulty)
            .map(s => s.getInfo());
    }

    /**
     * 按标签筛选剧本
     */
    getScenariosByTag(tag) {
        return Array.from(this.scenarios.values())
            .filter(s => s.tags.includes(tag))
            .map(s => s.getInfo());
    }

    /**
     * 开始当前剧本
     */
    startCurrentScenario() {
        if (!this.activeScenario) {
            return { error: '请先选择剧本' };
        }
        
        const result = this.activeScenario.start();
        
        if (result.success) {
            // 记录到活跃剧本
            this.activeScenarios.set(this.activeScenario.id, this.activeScenario);
            
            // 如果关联了剧情引擎，启动剧情
            if (this.storyEngine) {
                this.storyEngine.startStory(this.activeScenario.id);
            }
        }
        
        return result;
    }

    /**
     * 推进当前剧本
     */
    advanceCurrentScenario(turnData = {}) {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        const result = this.activeScenario.advance(turnData);
        
        // 同步推进剧情引擎
        if (this.storyEngine && result.success) {
            this.storyEngine.advanceStory(turnData.choice);
        }
        
        return result;
    }

    /**
     * 完成当前剧本
     */
    completeCurrentScenario(endingType = 'normal') {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        const result = this.activeScenario.complete(endingType);
        
        if (result.success) {
            // 从活跃列表移除
            this.activeScenarios.delete(this.activeScenario.id);
            
            // 如果关联了剧情引擎，结束剧情
            if (this.storyEngine) {
                this.storyEngine.reachStoryEnding(endingType);
            }
        }
        
        return result;
    }

    /**
     * 分配角色
     */
    assignRole(playerId, roleId) {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        return this.activeScenario.assignRole(playerId, roleId);
    }

    /**
     * 批量分配角色
     */
    assignRoles(assignments) {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        const results = [];
        for (const { playerId, roleId } of assignments) {
            results.push(this.activeScenario.assignRole(playerId, roleId));
        }
        
        return {
            success: results.every(r => r.success),
            results
        };
    }

    /**
     * 获取可用角色
     */
    getAvailableRoles() {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        return this.activeScenario.roles
            .filter(r => r.state === CharacterRoleState.AVAILABLE)
            .map(r => ({
                id: r.id,
                name: r.name,
                description: r.description
            }));
    }

    /**
     * 发现线索
     */
    discoverClue(clueId, playerId) {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        // 在剧本中记录
        const result = this.activeScenario.discoverClue(clueId, playerId);
        
        // 在线索系统中记录
        if (result.success) {
            this.clueSystem.discoverClue(clueId, playerId);
        }
        
        return result;
    }

    /**
     * 分析线索
     */
    analyzeClue(clueId, playerId) {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        // 在剧本中记录
        const result = this.activeScenario.analyzeClue(clueId);
        
        // 在线索系统中记录
        if (result.success) {
            this.clueSystem.analyzeClue(clueId, playerId);
        }
        
        return result;
    }

    /**
     * 关联线索
     */
    linkClues(clueId1, clueId2, playerId) {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        // 在剧本中记录
        const result = this.activeScenario.linkClues(clueId1, clueId2);
        
        // 在线索系统中记录
        if (result.success) {
            this.clueSystem.linkClues(clueId1, clueId2, playerId);
        }
        
        return result;
    }

    /**
     * 获取当前剧本线索
     */
    getCurrentClues() {
        if (!this.activeScenario) {
            return { error: '没有活跃的剧本' };
        }
        
        return {
            total: this.activeScenario.clues.length,
            discovered: this.activeScenario.clues
                .filter(c => c.state !== ClueState.HIDDEN)
                .map(c => ({
                    id: c.id,
                    type: c.type,
                    content: c.content,
                    state: c.state,
                    hint: c.hint
                })),
            hidden: this.activeScenario.clues
                .filter(c => c.state === ClueState.HIDDEN)
                .length
        };
    }

    /**
     * 获取线索图谱
     */
    getClueMap() {
        return this.clueSystem.getClueMap();
    }

    /**
     * 获取剧本列表
     */
    listScenarios(filters = {}) {
        let scenarios = Array.from(this.scenarios.values());
        
        if (filters.difficulty) {
            scenarios = scenarios.filter(s => s.difficulty === filters.difficulty);
        }
        
        if (filters.state) {
            scenarios = scenarios.filter(s => s.state === filters.state);
        }
        
        if (filters.tags) {
            scenarios = scenarios.filter(s => 
                filters.tags.some(tag => s.tags.includes(tag))
            );
        }
        
        return scenarios.map(s => s.getInfo());
    }

    /**
     * 获取剧本详情
     */
    getScenarioDetail(scenarioId) {
        const scenario = this.scenarios.get(scenarioId);
        if (!scenario) {
            return { error: '剧本不存在', scenarioId };
        }
        
        return {
            ...scenario.getInfo(),
            coreTransformation: scenario.coreTransformation,
            coreTrick: scenario.coreTrick,
            characterFeatures: scenario.characterFeatures,
            roles: scenario.roles,
            clues: scenario.clues.map(c => ({
                id: c.id,
                type: c.type,
                content: c.state !== ClueState.HIDDEN ? c.content : '???',
                state: c.state,
                hint: c.state !== ClueState.HIDDEN ? c.hint : null
            }))
        };
    }

    /**
     * 获取当前剧本状态
     */
    getCurrentScenarioStatus() {
        if (!this.activeScenario) {
            return { 
                active: false,
                message: '没有活跃的剧本' 
            };
        }
        
        return {
            active: true,
            ...this.activeScenario.getInfo()
        };
    }

    /**
     * 获取完整系统状态
     */
    getFullStatus() {
        return {
            initialized: this.initialized,
            totalScenarios: this.scenarios.size,
            activeScenario: this.activeScenario ? this.activeScenario.getInfo() : null,
            activeScenarios: this.activeScenarios.size,
            progressStats: this.progressManager.getGlobalStats(),
            clueStats: {
                total: this.clueSystem.clueRegistry.size,
                discovered: Array.from(this.clueSystem.clueRegistry.values())
                    .filter(c => c.state !== ClueState.HIDDEN).length
            }
        };
    }

    /**
     * 获取玩家进度
     */
    getPlayerProgress(playerId) {
        return this.progressManager.getPlayerProgress(playerId);
    }

    /**
     * 保存进度
     */
    saveProgress() {
        const data = {
            scenarios: Array.from(this.scenarios.values()).map(s => s.serialize()),
            activeScenarioId: this.activeScenario ? this.activeScenario.id : null,
            progressManager: this.progressManager.export(),
            clueSystem: {
                discoveryLog: this.clueSystem.discoveryLog
            },
            savedAt: Date.now()
        };
        
        return {
            success: true,
            data,
            message: '💾 进度已保存'
        };
    }

    /**
     * 加载进度
     */
    loadProgress(data) {
        if (!data.scenarios) {
            return { error: '无效的保存数据' };
        }
        
        // 恢复剧本状态
        data.scenarios.forEach(scenarioData => {
            const scenario = Scenario.deserialize(scenarioData);
            this.scenarios.set(scenario.id, scenario);
        });
        
        // 恢复活跃剧本
        if (data.activeScenarioId) {
            this.activeScenario = this.scenarios.get(data.activeScenarioId);
        }
        
        // 恢复进度管理器
        if (data.progressManager) {
            this.progressManager.import(data.progressManager);
        }
        
        // 恢复线索系统
        if (data.clueSystem) {
            this.clueSystem.discoveryLog = data.clueSystem.discoveryLog || [];
        }
        
        return {
            success: true,
            message: '📂 进度已加载',
            savedAt: data.savedAt
        };
    }

    /**
     * 重置剧本系统
     */
    reset() {
        this.scenarios.forEach(scenario => scenario.reset());
        this.activeScenario = null;
        this.activeScenarios.clear();
        this.clueSystem.reset();
        
        return {
            success: true,
            message: '🔄 剧本系统已重置'
        };
    }

    /**
     * 生成剧本报告
     */
    generateReport() {
        let report = '# 📜 剧本系统报告\n\n';
        
        // 总览
        const status = this.getFullStatus();
        report += `## 总览\n`;
        report += `- 总剧本数：${status.totalScenarios}\n`;
        report += `- 已完成：${status.progressStats.completedScenarios}\n`;
        report += `- 已精通：${status.progressStats.masteredScenarios}\n`;
        report += `- 活跃玩家：${status.progressStats.activePlayers}\n\n`;
        
        // 当前剧本
        if (this.activeScenario) {
            const info = this.activeScenario.getInfo();
            report += `## 当前剧本\n`;
            report += `- 名称：${info.title}\n`;
            report += `- 难度：${info.difficulty}\n`;
            report += `- 进度：${info.progress.percentage}%\n`;
            report += `- 线索：${info.clues.discovered}/${info.clues.total}\n`;
            report += `- 回合：${info.progress.turnsPlayed}\n\n`;
        }
        
        // 剧本列表（按难度分组）
        report += `## 剧本列表\n`;
        const difficulties = Object.values(DifficultyLevel);
        difficulties.forEach(diff => {
            const scenarios = Array.from(this.scenarios.values())
                .filter(s => s.difficulty === diff);
            
            if (scenarios.length > 0) {
                report += `\n### ${diff.toUpperCase()} (${scenarios.length})\n`;
                scenarios.forEach(s => {
                    const stateEmoji = s.state === ScenarioState.COMPLETED ? '✅' :
                                      s.state === ScenarioState.IN_PROGRESS ? '🎮' :
                                      s.state === ScenarioState.MASTERED ? '🏆' : '📖';
                    report += `- ${stateEmoji} ${s.number}. ${s.title}\n`;
                });
            }
        });
        
        return report;
    }
}

// 导出
module.exports = {
    ScenarioSystem,
    Scenario,
    ScenarioProgressManager,
    ClueSystem,
    ScenarioState,
    DifficultyLevel,
    ClueState,
    CharacterRoleState
};
