/**
 * Multiplayer Wuxia Game - 多人武侠冒险游戏
 * 支持多人协作/对抗的武侠世界
 */

const { MultiplayerGameEngine } = require('./multiplayer-engine');

class MultiplayerWuxiaGame {
    constructor() {
        this.engine = new MultiplayerGameEngine();
        this.story = new WuxiaStoryGenerator();
        this.chapter = 1;
        this.scene = null;
        this.worldState = {
            year: '大宋淳熙三年',
            location: '华山脚下',
            events: [],
            factions: {
                '少林': { reputation: 100, members: 500 },
                '武当': { reputation: 90, members: 300 },
                '峨眉': { reputation: 85, members: 200 },
                '丐帮': { reputation: 80, members: 1000 },
                '明教': { reputation: 50, members: 800 }
            }
        };
    }

    // 初始化游戏
    init(options = {}) {
        const mode = options.mode || 'coop'; // coop / vs / solo
        
        console.log('🗡️ 多人武侠游戏初始化...');
        
        return {
            status: 'initialized',
            mode: mode,
            message: `
═══════════════════════════════════════
    🗡️  多人武侠冒险  🗡️
═══════════════════════════════════════

欢迎来到江湖！

游戏模式：
• 👥 协作模式 - 共同书写江湖传奇
• ⚔️ 对抗模式 - 争夺武林盟主之位  
• 🔄 轮流模式 - 轮流体验剧情

请回复模式选择：
1. 协作模式（推荐）
2. 对抗模式
3. 轮流模式

然后邀请朋友加入！
═══════════════════════════════════════
            `
        };
    }

    // 设置游戏模式
    setMode(mode) {
        const validModes = ['coop', 'vs', 'solo'];
        if (!validModes.includes(mode)) {
            return { error: '无效的游戏模式' };
        }

        this.engine.gameMode = mode;
        return {
            success: true,
            mode: mode,
            modeName: this.engine.getModeName(mode),
            message: `游戏模式已设置为: ${this.engine.getModeName(mode)}`
        };
    }

    // 添加玩家
    addPlayer(playerId, playerName) {
        return this.engine.addPlayer(playerId, playerName);
    }

    // 移除玩家
    removePlayer(playerId) {
        return this.engine.removePlayer(playerId);
    }

    // 开始游戏
    startGame() {
        const result = this.engine.startGame();
        if (result.error) return result;

        const intro = this.story.getChapterIntro(1, this.engine.gameMode);
        
        return {
            ...result,
            scene: intro,
            worldState: this.worldState,
            hint: this.getControlHint()
        };
    }

    // 获取控制提示
    getControlHint() {
        const current = this.engine.getCurrentPlayer();
        if (!current) return '';
        
        return `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮 当前回合: ${current.color} ${current.name}
💡 输入数字或描述来做出选择
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;
    }

    // 处理玩家选择
    processChoice(playerId, choice) {
        const player = this.engine.players.get(playerId);
        if (!player) {
            return { error: '玩家不存在，请先加入游戏' };
        }

        // 检查回合（协作和轮流模式）
        const currentPlayer = this.engine.getCurrentPlayer();
        if (this.engine.gameMode !== 'vs' && currentPlayer.id !== playerId) {
            return {
                error: '不是您的回合',
                currentPlayer: currentPlayer.name,
                message: `请等待 ${currentPlayer.color} ${currentPlayer.name} 完成选择`
            };
        }

        // 记录选择
        const decision = {
            chapter: this.chapter,
            scene: this.scene,
            choice: choice,
            timestamp: new Date().toISOString()
        };

        // 处理选择并生成下一场景
        const result = this.engine.processDecision(playerId, decision);
        const nextScene = this.story.generateNextScene(this.chapter, choice, this.engine.gameMode, this.engine.players);
        
        this.chapter++;
        this.scene = nextScene;

        // 更新世界状态
        this.updateWorldState(choice, player);

        return {
            ...result,
            scene: nextScene,
            chapter: this.chapter,
            worldState: this.worldState,
            hint: this.getControlHint()
        };
    }

    // 更新世界状态
    updateWorldState(choice, player) {
        // 根据选择影响世界
        if (choice.faction) {
            const faction = this.worldState.factions[choice.faction];
            if (faction) {
                faction.reputation += 5;
            }
        }
        
        this.worldState.events.push({
            chapter: this.chapter,
            player: player.name,
            action: choice.description || choice
        });
    }

    // 获取游戏状态
    getStatus() {
        return {
            ...this.engine.getGameStatus(),
            chapter: this.chapter,
            worldState: this.worldState
        };
    }

    // 保存游戏
    saveGame(slot = 'wuxia_multiplayer') {
        const engineSave = this.engine.saveGame(slot);
        return {
            ...engineSave,
            chapter: this.chapter,
            worldState: this.worldState
        };
    }

    // 加载游戏
    loadGame(saveData) {
        this.engine.loadGame(saveData);
        this.chapter = saveData.chapter;
        this.worldState = saveData.worldState;
        return this.getStatus();
    }

    // 结束游戏
    endGame(reason = '江湖传说落幕') {
        return this.engine.endGame(reason);
    }
}

// 武侠故事生成器
class WuxiaStoryGenerator {
    constructor() {
        this.templates = this.initTemplates();
    }

    initTemplates() {
        return {
            chapter1: {
                coop: `
📖 第一章：初入江湖

华山脚下，云雾缭绕。

你们二人并肩而立，身后是师父的坟茔。师父临终前留下遗言：
> "江湖险恶，人心难测。你们二人需同生共死，方能在这乱世中立足..."

师父交给你们一封信，上面写着：
"此信交给洛阳城内的'醉仙楼'掌柜，自会明白一切。"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择你们的门派：
1. 🏛️ 少林 - 武林泰斗，内功深厚
2. ☯️ 武当 - 太极剑法，以柔克刚  
3. 🌸 峨眉 - 剑法精妙，轻功卓越
4. 🎋 丐帮 - 打狗棒法，遍布天下
5. 🌙 明教 - 圣火令下，教众万千

💡 提示：两位玩家可以讨论后，由当前回合玩家做出选择
`,
                vs: `
⚔️ 第一章：武林大会

江湖传言，武林盟主之位即将易主。
各路英雄齐聚华山，争夺这天下第一的名号。

你们二人，一个来自北方，一个来自南方。
今日，将在华山之巅一决高下！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择你的门派：
1. 🏛️ 少林 - 武林泰斗
2. ☯️ 武当 - 太极剑法
3. 🌸 峨眉 - 峨眉剑法
4. 🎋 丐帮 - 降龙十八掌
5. 🌙 明教 - 圣火令

💡 每位玩家独立选择，可以相同或不同
`,
                solo: `
🗡️ 第一章：江湖初现

华山脚下，你独自一人背负长剑。

远处走来另一位侠客，你们四目相对...
"这位兄台，可愿同行一程？"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择你的门派：
1. 🏛️ 少林 - 武林泰斗
2. ☯️ 武当 - 太极剑法
3. 🌸 峨眉 - 峨眉剑法
4. 🎋 丐帮 - 降龙十八掌
5. 🌙 明教 - 圣火令

💡 轮流模式：每位玩家轮流做出选择
`
            }
        };
    }

    getChapterIntro(chapter, mode) {
        if (chapter === 1) {
            return this.templates.chapter1[mode] || this.templates.chapter1.coop;
        }
        return this.generateNextScene(chapter - 1, {}, mode, new Map());
    }

    generateNextScene(chapter, choice, mode, players) {
        // 根据章节和选择生成剧情
        const scenes = this.getScenesForChapter(chapter + 1, mode);
        return scenes[Math.floor(Math.random() * scenes.length)];
    }

    getScenesForChapter(chapter, mode) {
        const baseScenes = [
            {
                title: `📖 第${chapter}章：江湖路远`,
                content: `
你们行至一处茶寮，见几位江湖人士低声交谈。

"听说了吗？魔教最近在江南一带活动频繁..."
"据说他们在寻找一件上古神器..."

茶博士过来招呼："二位客官，要来点什么？"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择：
1. 🍵 点茶歇息，顺便打听消息
2. 🚶 继续赶路，不多停留
3. 🗣️ 主动搭话那几位江湖人士
4. 🔍 悄悄跟踪他们
`,
                choices: ['点茶歇息', '继续赶路', '搭话', '跟踪']
            },
            {
                title: `📖 第${chapter}章：风雨欲来`,
                content: `
夜幕降临，你们在一座破庙中避雨。

突然，庙外传来马蹄声和呼喊声：
"别让他们跑了！那东西就在他们身上！"

庙门被撞开，一群黑衣人冲了进来！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择：
1. ⚔️ 拔剑迎战
2. 🏃 从后门突围
3. 🗣️ 询问对方来意
4. 🎭 假装不知情
`,
                choices: ['迎战', '突围', '询问', '假装']
            },
            {
                title: `📖 第${chapter}章：奇遇`,
                content: `
你们在山路上遇到一位白发老者。

老者打量你们一番，笑道：
"好苗子，好苗子...老夫有一套武功，想传于有缘人。"

说罢，老者从怀中取出一本泛黄的书册。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择：
1. 📚 虚心求教
2. 🤔 询问老者身份
3. 🙏 礼貌婉拒
4. 🎁 以物易物
`,
                choices: ['求教', '询问', '婉拒', '交换']
            }
        ];

        if (mode === 'vs') {
            // 对抗模式的特殊场景
            baseScenes.push({
                title: `📖 第${chapter}章：狭路相逢`,
                content: `
你们在前方路口相遇。

空气中弥漫着紧张的气氛...
"今日，便要分出高下！"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择：
1. ⚔️ 正面挑战
2. 🎯 设下陷阱
3. 🗣️ 言语试探
4. 🏃 暂时撤退
`,
                choices: ['挑战', '陷阱', '试探', '撤退']
            });
        }

        return baseScenes;
    }
}

module.exports = { MultiplayerWuxiaGame, WuxiaStoryGenerator };
