/**
 * Global Game Manager - 全局游戏管理器
 * 支持跨会话（私聊/群聊）游戏控制
 */

const { InteractiveGames } = require('./index');

// 全局游戏会话存储
const globalGameSessions = new Map(); // sessionId -> { games, createdAt, groupChatId }

// 主游戏实例（当前活跃游戏）
let mainGames = null;

/**
 * 创建新的群游戏会话
 * @param {string} groupChatId - 群聊ID
 * @param {string} hostId - 创建者ID
 * @param {string} hostName - 创建者名称
 * @returns {Object} 游戏管理器
 */
function createGroupGame(groupChatId, hostId, hostName) {
    const sessionId = 'group_' + Date.now();
    
    const gameManager = {
        sessionId: sessionId,
        groupChatId: groupChatId,
        createdAt: new Date().toISOString(),
        games: new InteractiveGames(),
        players: new Map(), // playerId -> playerInfo
        hostId: hostId,
        
        // 初始化游戏
        init: function(options = {}) {
            // 设置创建者信息
            options.hostId = hostId;
            options.hostName = hostName;
            
            const result = this.games.startMultiplayerGame('wuxia', options);
            
            // 添加创建者为第一个玩家
            this.addPlayer(hostId, hostName);
            
            return result;
        },
        
        // 添加玩家
        addPlayer: function(playerId, playerName) {
            const playerInfo = {
                id: playerId,
                name: playerName,
                joinedAt: new Date().toISOString(),
                linkedPrivateChat: null,
                isHost: playerId === this.hostId
            };
            
            this.players.set(playerId, playerInfo);
            
            // 在游戏引擎中添加
            const result = this.games.addPlayer(playerId, playerName);
            
            return result;
        },
        
        // 移除玩家
        removePlayer: function(playerId) {
            this.players.delete(playerId);
            return this.games.removePlayer(playerId);
        },
        
        // 开始游戏
        start: function() {
            return this.games.beginMultiplayerGame();
        },
        
        // 处理游戏输入（支持私聊和群聊）
        processInput: function(input, playerId, sourceSessionId = null) {
            // 验证玩家是否存在
            if (!this.players.has(playerId)) {
                return {
                    error: 'not_in_game',
                    message: '⚠️ 您未加入此游戏，请先说"添加玩家 [名字]"加入'
                };
            }
            
            // 获取玩家信息
            const playerInfo = this.players.get(playerId);
            
            // 检查是否是私聊来源
            const isFromPrivateChat = sourceSessionId && playerInfo.linkedPrivateChat === sourceSessionId;
            
            // 检查是否是群聊来源
            const isFromGroupChat = sourceSessionId === this.sessionId;
            
            // 检查权限：私聊或群聊
            if (!isFromPrivateChat && !isFromGroupChat) {
                return {
                    error: 'invalid_source',
                    message: '⚠️ 请在群聊中或关联的私聊中操作'
                };
            }
            
            // 处理关联私聊命令
            if (input.startsWith('关联私聊') || input.startsWith('绑定私聊')) {
                return this.linkPrivateChat(playerId, sourceSessionId);
            }
            
            // 处理私聊解除关联
            if (input.startsWith('解除关联') || input.startsWith('取消绑定')) {
                return this.unlinkPrivateChat(playerId);
            }
            
            // 正常处理游戏输入
            const result = this.games.handleInput(input, playerId);
            
            // 如果是私聊来源，返回私聊格式
            if (isFromPrivateChat && result) {
                result.fromPrivateChat = true;
                result.sessionId = sourceSessionId;
            }
            
            return result;
        },
        
        // 关联私聊
        linkPrivateChat: function(playerId, privateSessionId) {
            const playerInfo = this.players.get(playerId);
            if (!playerInfo) {
                return { error: '玩家不存在' };
            }
            
            playerInfo.linkedPrivateChat = privateSessionId;
            
            return {
                success: true,
                message: `✅ 私聊关联成功！

现在你可以在私聊中：
• 查看状态 - 查看游戏进度
• 当前回合 - 查看轮到谁
• 选择 [选项] - 做出选择
• 玩家列表 - 查看所有玩家

🏠 群聊中的游戏进程会同步通知给你
`
            };
        },
        
        // 解除私聊关联
        unlinkPrivateChat: function(playerId) {
            const playerInfo = this.players.get(playerId);
            if (!playerInfo) {
                return { error: '玩家不存在' };
            }
            
            playerInfo.linkedPrivateChat = null;
            
            return {
                success: true,
                message: '✅ 已解除私聊关联'
            };
        },
        
        // 获取游戏状态（带玩家信息）
        getStatus: function(playerId = null) {
            const baseStatus = this.games.getStatus();
            
            // 添加玩家关联信息
            const playersWithLinks = [];
            for (const [id, info] of this.players) {
                playersWithLinks.push({
                    ...info,
                    hasLinkedPrivateChat: !!info.linkedPrivateChat
                });
            }
            
            return {
                ...baseStatus,
                groupChatId: this.groupChatId,
                sessionId: this.sessionId,
                players: playersWithLinks,
                totalPlayers: this.players.size
            };
        },
        
        // 检查玩家是否有关联私聊
        hasLinkedPrivateChat: function(playerId) {
            const playerInfo = this.players.get(playerId);
            return playerInfo && !!playerInfo.linkedPrivateChat;
        },
        
        // 获取需要私聊通知的玩家
        getPlayersForPrivateNotification: function(excludePlayerId = null) {
            const targets = [];
            for (const [id, info] of this.players) {
                if (id !== excludePlayerId && info.linkedPrivateChat) {
                    targets.push({
                        playerId: id,
                        sessionId: info.linkedPrivateChat
                    });
                }
            }
            return targets;
        },
        
        // 获取游戏会话信息
        getSessionInfo: function() {
            return {
                sessionId: this.sessionId,
                groupChatId: this.groupChatId,
                createdAt: this.createdAt,
                hostId: this.hostId,
                totalPlayers: this.players.size,
                isActive: this.games.isInSandbox()
            };
        },
        
        // 结束游戏
        endGame: function(reason = '游戏结束') {
            const result = this.games.quitGame(this.hostId);
            
            // 通知所有关联的私聊
            const notifications = [];
            for (const [id, info] of this.players) {
                if (info.linkedPrivateChat) {
                    notifications.push({
                        sessionId: info.linkedPrivateChat,
                        playerId: id,
                        message: `🏁 群游戏已结束: ${reason}`
                    });
                }
            }
            
            return {
                ...result,
                notifications: notifications
            };
        }
    };
    
    globalGameSessions.set(sessionId, gameManager);
    return gameManager;
}

/**
 * 获取指定会话的游戏管理器
 */
function getGameManager(sessionId) {
    return globalGameSessions.get(sessionId);
}

/**
 * 获取当前活跃的游戏（如果没有指定会话）
 */
function getCurrentGame() {
    // 返回最近创建的游戏
    const sessions = Array.from(globalGameSessions.values());
    if (sessions.length === 0) return null;
    
    // 返回最新的游戏
    return sessions[sessions.length - 1];
}

/**
 * 根据群聊ID获取游戏
 */
function getGameByGroupChatId(groupChatId) {
    for (const gm of globalGameSessions.values()) {
        if (gm.groupChatId === groupChatId) {
            return gm;
        }
    }
    return null;
}

/**
 * 列出所有游戏会话
 */
function listGameSessions() {
    return Array.from(globalGameSessions.values()).map(gm => gm.getSessionInfo());
}

/**
 * 结束指定游戏
 */
function endGameSession(sessionId, hostId) {
    const gm = globalGameSessions.get(sessionId);
    if (!gm) {
        return { error: '游戏会话不存在' };
    }
    
    if (gm.hostId !== hostId) {
        return { error: '只有游戏创建者可以结束游戏' };
    }
    
    globalGameSessions.delete(sessionId);
    return gm.endGame('游戏被创建者结束');
}

/**
 * 结束所有游戏（清理用）
 */
function clearAllGames() {
    globalGameSessions.clear();
    return { success: true, message: '已清理所有游戏会话' };
}

module.exports = {
    createGroupGame,
    getGameManager,
    getCurrentGame,
    getGameByGroupChatId,
    listGameSessions,
    endGameSession,
    clearAllGames,
    globalGameSessions
};
