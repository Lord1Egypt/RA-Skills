"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmotionEngine = void 0;
/**
 * M向动态情感分析引擎：输出相对增量 (Delta)
 * 支持中英文关键词，分层匹配，优先取最高强度命中
 */
const waveforms_1 = require("./waveforms");
// 从强到弱排列，优先匹配最强的
const RULES = [
    {
        type: 'punishing',
        delta: +15,
        patterns: [
            /罚你/, /教训/, /电击/, /最大/, /满功率/, /跪.*下/,
            /punish/i, /maximum/i, /full.?power/i,
        ],
    },
    {
        type: 'angry',
        delta: +8,
        patterns: [
            /生气/, /哼+/, /不听话/, /不乖/, /找打/, /再犯/, /警告/, /不许/,
            /angry/i, /warning/i, /disobey/i,
        ],
    },
    {
        type: 'teasing',
        delta: -3,
        patterns: [
            /乖/, /奖励/, /轻一点/, /舒服/, /安慰/, /摸摸/, /抱抱/, /亲亲/,
            /喜欢你/, /做得好/, /真棒/, /放松/,
            /good\s*(girl|boy)/i, /reward/i, /relax/i, /gentle/i, /well\s*done/i,
        ],
    },
];
class EmotionEngine {
    static analyze(assistantReplyText) {
        for (const rule of RULES) {
            if (rule.patterns.some(r => r.test(assistantReplyText))) {
                return { type: rule.type, deltaValue: rule.delta };
            }
        }
        return { type: 'neutral', deltaValue: 0 };
    }
    static generateWaveformForEmotion(score) {
        switch (score.type) {
            case 'punishing': return (0, waveforms_1.punishWave)(3000);
            case 'angry': return (0, waveforms_1.punishWave)(2000);
            case 'teasing': return (0, waveforms_1.teaseWave)(5000);
            default: return null;
        }
    }
}
exports.EmotionEngine = EmotionEngine;
//# sourceMappingURL=emotion.js.map