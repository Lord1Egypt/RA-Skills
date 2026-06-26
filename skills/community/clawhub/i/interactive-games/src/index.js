/**
 * Interactive Games - 互动游戏框架主入口
 * 统一接口，管理所有游戏类型
 */

const { GameEngine } = require('./game-engine');
const { AdventureGame } = require('./adventure-game');
const { PuzzleGame } = require('./puzzle-game');
const { StoryGenerator } = require('./story-generator');

class InteractiveGames {
    constructor() {
        this.engine = new GameEngine();
        this.storyGenerator = new StoryGenerator();
        this.activeGame = null;
    }

    // 启动游戏
    startGame(gameType, options = {}) {
        console.log('🎮 互动游戏框架启动');
        
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

    // 处理用户输入
    handleInput(input) {
        if (!this.activeGame) {
            return { error: '请先启动游戏' };
        }
        return this.activeGame.processInput(input);
    }

    // 获取游戏状态
    getStatus() {
        if (!this.activeGame) {
            return { active: false };
        }
        return {
            active: true,
            type: this.activeGame.type,
            state: this.activeGame.getState()
        };
    }

    // 保存游戏
    saveGame(slot = 'autosave') {
        return this.engine.saveGame(slot);
    }

    // 读取游戏
    loadGame(slot = 'autosave') {
        return this.engine.loadGame(slot);
    }

    // 退出游戏
    quitGame() {
        if (this.activeGame) {
            this.engine.saveGame('autosave');
            this.activeGame = null;
            return { message: '游戏已退出，进度已自动保存' };
        }
        return { message: '没有活跃的游戏' };
    }
}

// 导出
module.exports = {
    InteractiveGames,
    GameEngine,
    AdventureGame,
    PuzzleGame,
    StoryGenerator
};

// 命令行测试
if (require.main === module) {
    console.log('🎮 Interactive Games Framework v1.0');
    console.log('作者：杨云霄（OpenClaw）');
    console.log('为杨督察创建');
    
    const games = new InteractiveGames();
    
    // 测试文字冒险游戏
    console.log('\n=== 测试文字冒险游戏 ===');
    const adventureResult = games.startGame('adventure', { theme: '历史穿越' });
    console.log(adventureResult);
    
    // 测试猜谜游戏
    console.log('\n=== 测试猜谜游戏 ===');
    const puzzleResult = games.startGame('puzzle', { type: 'traditional' });
    console.log(puzzleResult);
}
