/**
 * Game Engine - 游戏引擎核心
 * 通用游戏框架，管理游戏状态、存档、用户输入等
 */

class GameEngine {
    constructor() {
        this.currentGame = null;
        this.gameHistory = [];
        this.saveData = {};
    }

    // 启动游戏
    startGame(gameType, options = {}) {
        console.log(`🎮 启动游戏：${gameType}`);
        this.gameHistory.push({
            type: gameType,
            startTime: new Date().toISOString(),
            options
        });
    }

    // 保存游戏
    saveGame(slot = 'autosave') {
        const saveData = {
            slot,
            timestamp: new Date().toISOString(),
            gameType: this.currentGame?.type,
            state: this.currentGame?.getState()
        };
        this.saveData[slot] = saveData;
        console.log(`💾 游戏已保存到插槽：${slot}`);
        return saveData;
    }

    // 读取游戏
    loadGame(slot = 'autosave') {
        if (this.saveData[slot]) {
            console.log(`📂 读取游戏：${slot}`);
            return this.saveData[slot];
        }
        console.log('❌ 未找到存档');
        return null;
    }

    // 处理用户输入
    handleInput(input) {
        if (this.currentGame) {
            return this.currentGame.processInput(input);
        }
        return { error: '没有活跃的游戏' };
    }

    // 获取游戏状态
    getStatus() {
        return {
            activeGame: this.currentGame?.type || null,
            history: this.gameHistory.length,
            saves: Object.keys(this.saveData).length
        };
    }
}

module.exports = { GameEngine };
