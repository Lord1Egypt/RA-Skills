/**
 * Adventure Game - 文字冒险游戏模块
 * 支持多题材：武侠/都市/奇幻/科幻/历史
 */

class AdventureGame {
    constructor(theme = '历史穿越') {
        this.type = 'adventure';
        this.theme = theme;
        this.chapter = 1;
        this.playerState = {
            name: '玩家',
            health: 100,
            inventory: [],
            relationships: {}
        };
        this.storyPath = [];
        this.currentScene = null;
    }

    // 游戏开始
    start() {
        const intro = this.getIntro(this.theme);
        console.log(intro);
        return intro;
    }

    // 获取题材介绍
    getIntro(theme) {
        const intros = {
            '历史穿越': `
📖 第一章：穿越时空

您正在工作，突然一阵眩晕...
醒来时，您身穿古代长袍，手持羽扇，站在大帐之中。

脑海中涌入记忆：
- 现在是东汉末年，公元 196 年
- 您是一位谋士，名叫"云霄先生"
- 天下大乱，群雄逐鹿

请选择您辅佐的主公：
1. 曹操 - 雄才大略，挟天子以令诸侯
2. 刘备 - 仁德之名天下知，汉室宗亲
3. 孙权 - 据守江东，兵精粮足
4. 吕布 - 天下第一猛将
5. 自定义主公
`,
            '古代武侠': `
🗡️ 第一章：初入江湖

您站在华山脚下，背负长剑，身着青衫。
师父临终前交给您一本秘籍，嘱咐您...

请选择您的门派：
1. 少林 - 武林泰斗，内功深厚
2. 武当 - 太极剑法，以柔克刚
3. 峨眉 - 剑法精妙，女子门派
4. 自创门派
`,
            '现代都市': `
🏙️ 第一章：神秘委托

您是一名私家侦探，坐在办公室里。
电话响起，一个神秘声音说...

请选择案件类型：
1. 失踪案 - 富商女儿离奇失踪
2. 谋杀案 - 企业家被杀家中
3. 商业间谍 - 公司机密泄露
4. 自定义案件
`,
            '奇幻魔法': `
🧙 第一章：魔法觉醒

您发现自己能操控火焰，周围人惊恐地看着您。
一位老法师走过来，说您是百年一遇的天才...

请选择您的魔法系别：
1. 火焰系 - 强大的攻击魔法
2. 冰霜系 - 控制与防御
3. 自然系 - 治愈与召唤
4. 黑暗系 - 禁忌魔法
`,
            '科幻太空': `
🚀 第一章：星际航行

您是星际飞船"开拓者号"的船长。
收到未知星球的求救信号...

请选择行动：
1. 前往救援 - 可能发现新文明
2. 继续航行 - 执行原任务
3. 调查信号来源 - 谨慎行事
4. 返回基地 - 上报情况
`
        };
        return intros[theme] || intros['历史穿越'];
    }

    // 处理玩家选择
    processInput(input) {
        this.storyPath.push(input);
        
        // 根据选择生成下一段剧情
        const nextScene = this.generateScene(input);
        return nextScene;
    }

    // 生成剧情场景
    generateScene(choice) {
        // 简化版本，实际应该根据选择动态生成
        return {
            chapter: this.chapter++,
            scene: `第${this.chapter}章：新的征程\n\n根据您的选择，故事继续发展...`,
            choices: ['选项 1', '选项 2', '选项 3']
        };
    }

    // 获取游戏状态
    getState() {
        return {
            type: this.type,
            theme: this.theme,
            chapter: this.chapter,
            playerState: this.playerState,
            storyPath: this.storyPath
        };
    }

    // 设置玩家名称
    setPlayerName(name) {
        this.playerState.name = name;
    }

    // 添加物品
    addItem(item) {
        this.playerState.inventory.push(item);
    }

    // 修改关系值
    modifyRelationship(character, value) {
        if (!this.playerState.relationships[character]) {
            this.playerState.relationships[character] = 0;
        }
        this.playerState.relationships[character] += value;
    }
}

module.exports = { AdventureGame };
