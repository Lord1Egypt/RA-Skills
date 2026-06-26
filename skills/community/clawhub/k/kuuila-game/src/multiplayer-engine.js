/**
 * Multiplayer Game Engine - 多人游戏引擎
 * 支持多玩家、轮流决策、团队协作
 */

class MultiplayerGameEngine {
    constructor() {
        this.players = new Map(); // 玩家列表
        this.currentPlayerIndex = 0; // 当前行动玩家索引
        this.gameMode = 'coop'; // 游戏模式: coop(协作) / vs(对抗) / solo(轮流)
        this.sharedState = null; // 共享游戏状态(协作模式)
        this.playerStates = new Map(); // 各玩家独立状态(对抗模式)
        this.gameHistory = []; // 游戏历史记录
        this.currentGame = null; // 当前游戏实例
        this.isActive = false; // 游戏是否进行中
        this.turnOrder = []; // 行动顺序
        this.votes = new Map(); // 投票记录
        this.sandboxMode = true; // 沙箱模式：游戏进行中只响应游戏命令
        this.authorizedPlayerIds = new Set(); // 授权玩家ID列表
        this.gameHostId = null; // 游戏创建者（有最高权限）
        
        // 跨会话支持
        this.gameSessionId = this.generateSessionId(); // 游戏会话ID
        this.linkedSessions = new Map(); // 关联的私聊会话
        this.commandSources = new Map(); // 命令来源追踪
    }

    // 生成游戏会话ID
    generateSessionId() {
        return 'game_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // 关联私聊会话
    linkPrivateSession(playerId, sessionId, sessionType = 'private') {
        if (!this.players.has(playerId)) {
            return { error: '玩家未加入游戏' };
        }

        this.linkedSessions.set(playerId, {
            sessionId: sessionId,
            type: sessionType,
            linkedAt: new Date().toISOString()
        });

        return {
            success: true,
            message: `✅ 私聊会话已关联！\n现在你可以在私聊中控制群游戏。`,
            gameSessionId: this.gameSessionId,
            availableCommands: [
                '查看状态 - 查看游戏状态',
                '当前回合 - 查看轮到谁',
                '选择 [选项] - 做出选择',
                '玩家列表 - 查看所有玩家',
                '退出游戏 - 结束游戏'
            ]
        };
    }

    // 取消关联私聊会话
    unlinkPrivateSession(playerId) {
        if (this.linkedSessions.has(playerId)) {
            this.linkedSessions.delete(playerId);
            return { success: true, message: '私聊会话已取消关联' };
        }
        return { error: '没有关联的私聊会话' };
    }

    // 检查命令来源是否合法（支持群聊和私聊）
    isValidCommandSource(playerId, sourceSessionId) {
        // 群聊来源总是合法的
        if (!sourceSessionId) return true;

        // 检查是否是该玩家关联的私聊会话
        const linkedSession = this.linkedSessions.get(playerId);
        if (linkedSession && linkedSession.sessionId === sourceSessionId) {
            return true;
        }

        return false;
    }

    // 获取玩家的会话信息
    getPlayerSessionInfo(playerId) {
        const player = this.players.get(playerId);
        if (!player) return null;

        const linkedSession = this.linkedSessions.get(playerId);
        
        return {
            player: player,
            hasLinkedSession: !!linkedSession,
            linkedSession: linkedSession
        };
    }

    // 广播消息到所有关联会话
    broadcastToAllSessions(message, excludePlayerId = null) {
        const destinations = [];
        
        // 群聊（原始会话）
        destinations.push({ type: 'group', message: message });
        
        // 所有关联的私聊会话
        for (const [playerId, session] of this.linkedSessions) {
            if (playerId !== excludePlayerId) {
                destinations.push({
                    type: 'private',
                    sessionId: session.sessionId,
                    playerId: playerId,
                    message: message
                });
            }
        }
        
        return destinations;
    }

    // 通知特定玩家
    notifyPlayer(playerId, message) {
        const session = this.linkedSessions.get(playerId);
        if (session) {
            return {
                type: 'private',
                sessionId: session.sessionId,
                playerId: playerId,
                message: message
            };
        }
        return null;
    }

    // 允许的游戏命令白名单
    static ALLOWED_COMMANDS = [
        '启动多人武侠游戏', '启动多人游戏', '开始游戏', '开始',
        '添加玩家', '移除玩家', '退出游戏', '退出',
        '选择', '投票', '查看状态', '当前回合', '玩家列表',
        '设置模式', '存档', '读档', '游戏帮助',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', // 快捷选择
        '少林', '武当', '峨眉', '丐帮', '明教', // 门派名称
        '协作', '对抗', '轮流', 'coop', 'vs', 'solo' // 模式名称
    ];

    // 检查命令是否允许在沙箱模式执行
    isCommandAllowed(input) {
        if (!this.sandboxMode || !this.isActive) return true;
        
        const normalizedInput = input.trim().toLowerCase();
        
        // 检查白名单
        for (const cmd of MultiplayerGameEngine.ALLOWED_COMMANDS) {
            if (normalizedInput.startsWith(cmd.toLowerCase()) || 
                normalizedInput === cmd.toLowerCase()) {
                return true;
            }
        }
        
        return false;
    }

    // 检查玩家是否已加入游戏
    isPlayerInGame(playerId) {
        return this.players.has(playerId) || playerId === this.gameHostId;
    }

    // 设置游戏创建者
    setGameHost(playerId) {
        this.gameHostId = playerId;
        this.authorizedPlayerIds.add(playerId);
    }

    // 获取沙箱拒绝消息
    getSandboxRejectMessage() {
        return {
            error: 'sandbox_restricted',
            message: `
⚠️ 游戏进行中，当前仅响应游戏命令。

可用命令：
• 选择 [选项] - 做出选择
• 查看状态 - 查看游戏状态
• 当前回合 - 查看轮到谁
• 退出游戏 - 退出当前游戏

如需其他功能，请先退出游戏。
            `.trim()
        };
    }

    // 初始化多人游戏
    initMultiplayerGame(gameType, options = {}) {
        this.gameMode = options.mode || 'coop';
        this.currentGame = gameType;
        this.isActive = true;
        
        console.log(`🎮 多人游戏启动`);
        console.log(`模式: ${this.getModeName(this.gameMode)}`);
        console.log(`类型: ${gameType}`);
        
        return {
            status: 'initialized',
            mode: this.gameMode,
            players: Array.from(this.players.values()),
            message: '游戏初始化完成，等待玩家加入...'
        };
    }

    // 获取模式名称
    getModeName(mode) {
        const names = {
            'coop': '👥 团队协作',
            'vs': '⚔️ 玩家对抗',
            'solo': '🔄 轮流体验'
        };
        return names[mode] || mode;
    }

    // 添加玩家
    addPlayer(playerId, playerName, options = {}) {
        if (this.players.has(playerId)) {
            return { error: '玩家已存在' };
        }

        const player = {
            id: playerId,
            name: playerName,
            joinedAt: new Date().toISOString(),
            role: options.role || 'adventurer',
            color: options.color || this.getPlayerColor(this.players.size),
            stats: {
                decisions: 0,
                achievements: []
            }
        };

        this.players.set(playerId, player);
        this.turnOrder.push(playerId);

        // 如果是独立模式，为每个玩家创建独立状态
        if (this.gameMode === 'vs') {
            this.playerStates.set(playerId, this.createPlayerState(playerName));
        }

        console.log(`👤 玩家加入: ${playerName} (${playerId})`);
        
        return {
            success: true,
            player: player,
            totalPlayers: this.players.size,
            message: `${playerName} 加入了游戏！`
        };
    }

    // 移除玩家
    removePlayer(playerId) {
        const player = this.players.get(playerId);
        if (!player) {
            return { error: '玩家不存在' };
        }

        this.players.delete(playerId);
        this.turnOrder = this.turnOrder.filter(id => id !== playerId);
        this.playerStates.delete(playerId);

        // 调整当前玩家索引
        if (this.currentPlayerIndex >= this.turnOrder.length) {
            this.currentPlayerIndex = 0;
        }

        return {
            success: true,
            message: `${player.name} 离开了游戏`,
            remainingPlayers: this.players.size
        };
    }

    // 获取玩家颜色
    getPlayerColor(index) {
        const colors = ['🔴', '🔵', '🟢', '🟡', '🟣', '🟠', '⚪', '⚫'];
        return colors[index % colors.length];
    }

    // 创建玩家状态
    createPlayerState(playerName) {
        return {
            name: playerName,
            health: 100,
            inventory: [],
            relationships: {},
            achievements: [],
            location: '起始点',
            score: 0
        };
    }

    // 开始游戏
    startGame() {
        if (this.players.size < 1) {
            return { error: '至少需要 1 名玩家' };
        }

        if (this.gameMode === 'coop') {
            // 协作模式：创建共享状态
            this.sharedState = this.createPlayerState('团队');
        }

        this.isActive = true;
        this.currentPlayerIndex = 0;

        const currentPlayer = this.players.get(this.turnOrder[0]);
        
        console.log(`🚀 游戏开始！`);
        console.log(`当前回合: ${currentPlayer.color} ${currentPlayer.name}`);

        return {
            status: 'started',
            currentPlayer: currentPlayer,
            mode: this.gameMode,
            message: `游戏开始！${currentPlayer.color} ${currentPlayer.name} 的回合`,
            totalPlayers: this.players.size
        };
    }

    // 获取当前玩家
    getCurrentPlayer() {
        if (this.turnOrder.length === 0) return null;
        return this.players.get(this.turnOrder[this.currentPlayerIndex]);
    }

    // 切换到下一个玩家
    nextTurn() {
        if (this.turnOrder.length === 0) return null;

        this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.turnOrder.length;
        const nextPlayer = this.players.get(this.turnOrder[this.currentPlayerIndex]);

        console.log(`🔄 轮到: ${nextPlayer.color} ${nextPlayer.name}`);
        
        return {
            currentPlayer: nextPlayer,
            turnNumber: this.gameHistory.length + 1,
            message: `轮到 ${nextPlayer.color} ${nextPlayer.name} 了！`
        };
    }

    // 处理玩家决策
    processDecision(playerId, decision) {
        const player = this.players.get(playerId);
        if (!player) {
            return { error: '玩家不存在' };
        }

        // 检查是否轮到该玩家
        const currentPlayer = this.getCurrentPlayer();
        if (currentPlayer && currentPlayer.id !== playerId && this.gameMode !== 'vs') {
            return {
                error: '不是您的回合',
                currentPlayer: currentPlayer.name,
                message: `请等待 ${currentPlayer.color} ${currentPlayer.name} 完成决策`
            };
        }

        // 记录决策
        const record = {
            timestamp: new Date().toISOString(),
            player: player,
            decision: decision,
            turn: this.gameHistory.length + 1
        };
        this.gameHistory.push(record);

        // 更新玩家统计
        player.stats.decisions++;

        // 根据游戏模式更新状态
        let result;
        if (this.gameMode === 'coop') {
            result = this.processCoopDecision(player, decision);
        } else if (this.gameMode === 'vs') {
            result = this.processVsDecision(player, decision);
        } else {
            result = this.processSoloDecision(player, decision);
        }

        // 如果不是对抗模式，切换到下一个玩家
        if (this.gameMode !== 'vs') {
            const next = this.nextTurn();
            result.nextPlayer = next;
        }

        return result;
    }

    // 协作模式处理
    processCoopDecision(player, decision) {
        // 更新共享状态
        if (decision.type === 'add_item') {
            this.sharedState.inventory.push(decision.item);
        } else if (decision.type === 'change_health') {
            this.sharedState.health += decision.value;
        }

        return {
            mode: 'coop',
            player: player.name,
            decision: decision,
            sharedState: this.sharedState,
            message: `${player.color} ${player.name} 决定: ${decision.description || decision}`,
            teamMessage: `团队状态已更新！`
        };
    }

    // 对抗模式处理
    processVsDecision(player, decision) {
        const state = this.playerStates.get(player.id);
        
        if (decision.type === 'add_item') {
            state.inventory.push(decision.item);
        } else if (decision.type === 'change_health') {
            state.health += decision.value;
        } else if (decision.type === 'attack') {
            // 攻击其他玩家
            const target = this.players.get(decision.target);
            if (target) {
                const targetState = this.playerStates.get(decision.target);
                targetState.health -= decision.damage;
            }
        }

        return {
            mode: 'vs',
            player: player.name,
            decision: decision,
            playerState: state,
            message: `${player.color} ${player.name} 执行了行动！`
        };
    }

    // 轮流模式处理
    processSoloDecision(player, decision) {
        return {
            mode: 'solo',
            player: player.name,
            decision: decision,
            message: `${player.color} ${player.name} 做出了选择！`
        };
    }

    // 投票系统（用于团队决策）
    startVote(voteId, options, timeout = 60) {
        this.votes.set(voteId, {
            options: options,
            votes: new Map(),
            startTime: Date.now(),
            timeout: timeout * 1000
        });

        return {
            voteId: voteId,
            options: options,
            timeout: timeout,
            message: `📊 开始投票！请玩家选择：\n${options.map((o, i) => `${i + 1}. ${o}`).join('\n')}`
        };
    }

    // 提交投票
    submitVote(playerId, voteId, choice) {
        const vote = this.votes.get(voteId);
        if (!vote) {
            return { error: '投票不存在' };
        }

        if (Date.now() - vote.startTime > vote.timeout) {
            return { error: '投票已结束' };
        }

        vote.votes.set(playerId, choice);

        const player = this.players.get(playerId);
        return {
            success: true,
            message: `${player.name} 已投票 ✓`,
            totalVotes: vote.votes.size,
            remaining: this.players.size - vote.votes.size
        };
    }

    // 结束投票并统计结果
    endVote(voteId) {
        const vote = this.votes.get(voteId);
        if (!vote) {
            return { error: '投票不存在' };
        }

        const results = new Map();
        for (const [playerId, choice] of vote.votes) {
            results.set(choice, (results.get(choice) || 0) + 1);
        }

        // 找出最多票
        let winner = null;
        let maxVotes = 0;
        for (const [choice, count] of results) {
            if (count > maxVotes) {
                maxVotes = count;
                winner = choice;
            }
        }

        this.votes.delete(voteId);

        return {
            winner: winner,
            results: Array.from(results.entries()),
            totalVotes: vote.votes.size,
            message: `📊 投票结果：${vote.options[winner]} (${maxVotes}票)`
        };
    }

    // 获取游戏状态
    getGameStatus() {
        const currentPlayer = this.getCurrentPlayer();
        
        return {
            isActive: this.isActive,
            mode: this.gameMode,
            modeName: this.getModeName(this.gameMode),
            totalPlayers: this.players.size,
            players: Array.from(this.players.values()).map(p => ({
                ...p,
                isCurrent: currentPlayer && p.id === currentPlayer.id
            })),
            currentPlayer: currentPlayer,
            turnNumber: this.gameHistory.length + 1,
            sharedState: this.sharedState,
            playerStates: this.gameMode === 'vs' ? 
                Array.from(this.playerStates.entries()) : null
        };
    }

    // 保存多人游戏
    saveGame(slot = 'multiplayer_autosave') {
        const saveData = {
            slot,
            timestamp: new Date().toISOString(),
            gameMode: this.gameMode,
            players: Array.from(this.players.entries()),
            sharedState: this.sharedState,
            playerStates: Array.from(this.playerStates.entries()),
            gameHistory: this.gameHistory,
            currentPlayerIndex: this.currentPlayerIndex,
            turnOrder: this.turnOrder
        };

        console.log(`💾 多人游戏已保存: ${slot}`);
        return saveData;
    }

    // 加载多人游戏
    loadGame(saveData) {
        this.gameMode = saveData.gameMode;
        this.players = new Map(saveData.players);
        this.sharedState = saveData.sharedState;
        this.playerStates = new Map(saveData.playerStates);
        this.gameHistory = saveData.gameHistory;
        this.currentPlayerIndex = saveData.currentPlayerIndex;
        this.turnOrder = saveData.turnOrder;

        console.log(`📂 多人游戏已加载: ${saveData.slot}`);
        return this.getGameStatus();
    }

    // 结束游戏
    endGame(reason = '游戏结束') {
        this.isActive = false;
        
        // 生成游戏总结
        const summary = {
            totalTurns: this.gameHistory.length,
            players: Array.from(this.players.values()).map(p => ({
                name: p.name,
                decisions: p.stats.decisions,
                achievements: p.stats.achievements
            })),
            topPlayer: this.getTopPlayer()
        };

        console.log(`🏁 ${reason}`);
        
        return {
            status: 'ended',
            reason: reason,
            summary: summary,
            message: `${reason}！感谢各位玩家参与！`
        };
    }

    // 获取最佳玩家
    getTopPlayer() {
        let topPlayer = null;
        let maxScore = 0;

        for (const [id, player] of this.players) {
            const score = player.stats.decisions + player.stats.achievements.length * 10;
            if (score > maxScore) {
                maxScore = score;
                topPlayer = player;
            }
        }

        return topPlayer;
    }
}

module.exports = { MultiplayerGameEngine };
