/**
 * Story Generator - 剧情生成器
 * 动态生成游戏剧情、对话、场景描述
 */

class StoryGenerator {
    constructor() {
        this.templates = {
            historical: this.getHistoricalTemplates(),
            wuxia: this.getWuxiaTemplates(),
            modern: this.getModernTemplates(),
            fantasy: this.getFantasyTemplates(),
            scifi: this.getScifiTemplates()
        };
    }

    // 生成场景描述
    generateScene(theme, context) {
        const template = this.templates[theme] || this.templates.historical;
        return template.scene.replace('{context}', context);
    }

    // 生成 NPC 对话
    generateDialogue(theme, character, emotion) {
        const template = this.templates[theme] || this.templates.historical;
        const dialogues = template.dialogues[emotion] || template.dialogues.neutral;
        return dialogues[Math.floor(Math.random() * dialogues.length)]
            .replace('{character}', character);
    }

    // 生成剧情分支
    generateBranch(currentSituation, playerChoice) {
        // 根据玩家选择生成不同剧情走向
        const branches = {
            'aggressive': '您选择了强硬的路线，局势变得紧张...',
            'diplomatic': '您选择了外交手段，双方开始谈判...',
            'cautious': '您选择了谨慎行事，先观察局势...',
            'bold': '您选择了大胆行动，风险与机遇并存...'
        };
        return branches[playerChoice] || branches.cautious;
    }

    // 历史题材模板
    getHistoricalTemplates() {
        return {
            scene: '【{context}】\n\n帐外战马嘶鸣，士兵操练声此起彼伏。您站在军帐中，思考着下一步行动...',
            dialogues: {
                respectful: [
                    '{character}深深一拜："先生高见！"',
                    '{character}拱手道："愿听先生教诲"',
                    '{character}眼中闪过敬佩之色'
                ],
                urgent: [
                    '{character}急道："军情紧急，请先生速速定夺！"',
                    '{character}面色凝重："此事关乎生死存亡"',
                    '{character}快步走来："先生，大事不妙！"'
                ],
                neutral: [
                    '{character}问道："先生以为如何？"',
                    '{character}沉思片刻，看向您',
                    '{character}等待您的回答'
                ]
            }
        };
    }

    // 武侠题材模板
    getWuxiaTemplates() {
        return {
            scene: '【{context}】\n\n江湖风雨，刀光剑影。您手持长剑，面对眼前的挑战...',
            dialogues: {
                respectful: [
                    '{character}抱拳："前辈武功盖世！"',
                    '{character}拱手："愿闻其详"',
                    '{character}眼中闪过敬佩之色'
                ],
                urgent: [
                    '{character}急道："大侠救命！"',
                    '{character}面色苍白："仇家追来了！"',
                    '{character}快步走来："不好了！"'
                ],
                neutral: [
                    '{character}问道："阁下高见？"',
                    '{character}沉思片刻，看向您',
                    '{character}等待您的回答'
                ]
            }
        };
    }

    // 现代题材模板
    getModernTemplates() {
        return {
            scene: '【{context}】\n\n城市霓虹闪烁，车水马龙。您站在街头，思考着下一步行动...',
            dialogues: {
                respectful: [
                    '{character}恭敬地说："您说得对"',
                    '{character}点头表示赞同',
                    '{character}眼中闪过认可之色'
                ],
                urgent: [
                    '{character}急道："出事了！"',
                    '{character}面色凝重："情况不妙"',
                    '{character}快步走来："有新线索！"'
                ],
                neutral: [
                    '{character}问道："你怎么看？"',
                    '{character}沉思片刻，看向您',
                    '{character}等待您的回答'
                ]
            }
        };
    }

    // 奇幻题材模板
    getFantasyTemplates() {
        return {
            scene: '【{context}】\n\n魔法光芒闪烁，巨龙在空中盘旋。您手握法杖，准备施展魔法...',
            dialogues: {
                respectful: [
                    '{character}鞠躬："法师阁下智慧无双"',
                    '{character}恭敬地说："愿听您的指挥"',
                    '{character}眼中闪过敬畏之色'
                ],
                urgent: [
                    '{character}急道："魔族大军压境！"',
                    '{character}面色苍白："封印松动了！"',
                    '{character}快步走来："紧急情况！"'
                ],
                neutral: [
                    '{character}问道："法师有何高见？"',
                    '{character}沉思片刻，看向您',
                    '{character}等待您的回答'
                ]
            }
        };
    }

    // 科幻题材模板
    getScifiTemplates() {
        return {
            scene: '【{context}】\n\n星舰引擎轰鸣，全息屏幕闪烁。您站在舰桥上，凝视着前方的星域...',
            dialogues: {
                respectful: [
                    '{character}敬礼："舰长英明！"',
                    '{character}点头："明白，舰长"',
                    '{character}眼中闪过敬佩之色'
                ],
                urgent: [
                    '{character}急道："舰长，敌舰接近！"',
                    '{character}面色凝重："护盾能量下降！"',
                    '{character}快步走来："收到求救信号！"'
                ],
                neutral: [
                    '{character}问道："舰长，您的命令？"',
                    '{character}沉思片刻，看向您',
                    '{character}等待您的指示'
                ]
            }
        };
    }
}

module.exports = { StoryGenerator };
