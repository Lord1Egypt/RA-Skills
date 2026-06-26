"use strict";
// Micro Memory - Strength System
Object.defineProperty(exports, "__esModule", { value: true });
exports.calculateDecay = calculateDecay;
exports.updateStrength = updateStrength;
exports.reinforce = reinforce;
exports.getStrengthEmoji = getStrengthEmoji;
exports.getDecayWarning = getDecayWarning;
exports.getOptimalReviewInterval = getOptimalReviewInterval;
const utils_1 = require("./utils");
// Decay rates per day for each level
const DECAY_RATES = {
    critical: 5,
    weak: 3,
    stable: 1,
    strong: 0.5,
    permanent: 0.1,
};
// Reinforce boost multipliers
const BOOST_MULTIPLIERS = {
    1: 1.2,
    2: 1.5,
    3: 2.0,
};
function calculateDecay(memory) {
    const now = new Date();
    const lastReinforced = new Date(memory.strength.lastReinforced.replace(' ', 'T'));
    const days = (0, utils_1.daysBetween)(lastReinforced, now);
    const rate = DECAY_RATES[memory.strength.level] || 1;
    return Math.min(days * rate, memory.strength.score);
}
function updateStrength(memory) {
    const decay = calculateDecay(memory);
    const newScore = Math.max(0, memory.strength.score - decay);
    const level = (0, utils_1.getStrengthLevel)(newScore);
    return {
        level,
        score: Math.round(newScore),
        lastReinforced: memory.strength.lastReinforced,
    };
}
function reinforce(memory, boost = 1) {
    const multiplier = BOOST_MULTIPLIERS[boost] || 1.2;
    const newScore = Math.min(100, memory.strength.score * multiplier + 10);
    const level = (0, utils_1.getStrengthLevel)(newScore);
    return {
        level,
        score: Math.round(newScore),
        lastReinforced: (0, utils_1.formatTimestamp)(),
    };
}
function getStrengthEmoji(level) {
    const emojis = {
        permanent: '💎',
        strong: '💪',
        stable: '📊',
        weak: '⚠️',
        critical: '🔴',
    };
    return emojis[level] || '❓';
}
function getDecayWarning(memory) {
    const decay = calculateDecay(memory);
    if (decay > 20) {
        return `⚠️ 记忆即将衰减 ${decay.toFixed(0)} 点，建议复习！`;
    }
    if (memory.strength.level === 'critical') {
        return '🔴 记忆处于临界状态，急需复习！';
    }
    return null;
}
function getOptimalReviewInterval(level) {
    const intervals = {
        critical: 1,
        weak: 3,
        stable: 7,
        strong: 14,
        permanent: 30,
    };
    return intervals[level] || 7;
}
//# sourceMappingURL=strength.js.map