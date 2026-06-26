"use strict";
/**
 * 个人目标追踪系统
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.PersonalGoalSystem = void 0;
class PersonalGoalSystem {
    constructor(memory) {
        this.systemName = 'goal';
        this.memory = memory;
    }
    analyzeMotivation(goal, userResponses) {
        const motivations = [];
        for (const level of ['safety', 'social', 'esteem', 'self-actualization', 'meaning']) {
            if (userResponses[level]) {
                motivations.push({ level, description: userResponses[level], strength: 'medium' });
            }
        }
        this.memory.addToL2(`动机解析_${goal.name}`, { goal: goal.name, motivations }, 'insight', 4, ['motivation', 'goal'], this.systemName);
        return motivations;
    }
    buildGoalNetwork(goals) {
        const relations = [];
        for (let i = 0; i < goals.length; i++) {
            for (let j = i + 1; j < goals.length; j++) {
                const goalA = goals[i];
                const goalB = goals[j];
                if (goalA.priority > 7 && goalB.priority > 7) {
                    relations.push({ goalA: goalA.name, goalB: goalB.name, relation: 'competitive', reason: '两个高优先级目标可能争夺资源' });
                }
                else if (Math.abs(goalA.priority - goalB.priority) < 2) {
                    relations.push({ goalA: goalA.name, goalB: goalB.name, relation: 'synergistic', reason: '优先级相近，可能相互促进' });
                }
            }
        }
        this.memory.addToL3({
            id: '', level: 'L3', category: 'goal', key: '目标网络', value: { goals, relations },
            tags: ['goal-network'], importance: 5, system: this.systemName,
            createdAt: new Date().toISOString(), accessedAt: new Date().toISOString(), accessCount: 0
        });
        return { goals, relations };
    }
    analyzeEnergyAllocation(timeLog, idealAllocation) {
        const totalHours = Object.values(timeLog).reduce((sum, h) => sum + h, 0);
        const allocations = [];
        const dimensions = ['career', 'family', 'health', 'learning', 'social', 'leisure'];
        for (const dimension of dimensions) {
            const actualHours = timeLog[dimension] || 0;
            const actualPercentage = (actualHours / totalHours) * 100;
            const idealPercentage = idealAllocation[dimension] || 0;
            allocations.push({ dimension, actualHours, actualPercentage, idealPercentage, gap: actualPercentage - idealPercentage });
        }
        this.memory.addToL2('精力分配分析', { allocations, date: new Date().toISOString() }, 'insight', 3, ['energy', 'allocation'], this.systemName);
        return allocations;
    }
    discoverBlindSpots(goals, energyAllocation, statedPriorities) {
        const blindSpots = [];
        for (const allocation of energyAllocation) {
            const statedPriority = statedPriorities[allocation.dimension] || 5;
            const actualPriority = allocation.actualPercentage / 10;
            if (Math.abs(statedPriority - actualPriority) > 2) {
                blindSpots.push({
                    type: '优先级盲点',
                    description: `声称${allocation.dimension}优先级为${statedPriority}，但实际投入${allocation.actualPercentage.toFixed(1)}%`,
                    impact: '言行不一可能导致目标难以达成',
                    suggestion: `建议重新评估${allocation.dimension}的真实优先级`
                });
            }
        }
        const goalsWithoutDeepMotivation = goals.filter(g => !g.motivations.some(m => m.level === 'meaning' || m.level === 'self-actualization'));
        if (goalsWithoutDeepMotivation.length > 0) {
            blindSpots.push({
                type: '动机盲点',
                description: `目标 ${goalsWithoutDeepMotivation.map(g => g.name).join('、')} 缺乏深层动机`,
                impact: '可能难以长期坚持',
                suggestion: '建议深入思考这些目标对你的真正意义'
            });
        }
        for (const spot of blindSpots) {
            this.memory.addToL2(`认知盲点_${spot.type}`, spot, 'insight', 4, ['blind-spot', 'cognitive'], this.systemName);
        }
        return blindSpots;
    }
    generateAIMirrorLetter(observations, progress, concerns, challenges, possibilities, recommendations) {
        const letter = {
            observations, progress, concerns, challenges, possibilities, recommendations,
            closing: '作为你的AI伙伴，我会持续陪伴你的成长旅程。期待看到你下周的变化。'
        };
        this.memory.addToL4({
            id: '', level: 'L4', category: 'insight', key: `AI镜像_${new Date().toISOString().split('T')[0]}`,
            value: letter, tags: ['ai-mirror', 'insight'], importance: 5, system: this.systemName,
            createdAt: new Date().toISOString(), accessedAt: new Date().toISOString(), accessCount: 0
        });
        return letter;
    }
    predictFutureSelf(goals, energyAllocation, behaviorPatterns) {
        const predictions = [
            { timeframe: '3个月后', capabilityState: '基于当前学习模式，能力将稳步提升', energyState: '如果保持当前精力分配，可能面临某些领域投入不足', goalProgress: '预计完成部分短期目标' },
            { timeframe: '6个月后', capabilityState: '能力将有显著提升，特别是在持续投入的领域', energyState: '建议调整精力分配以避免倦怠', goalProgress: '预计完成大部分中期目标' },
            { timeframe: '1年后', capabilityState: '将成为当前专注领域的专家', energyState: '需要重新评估人生优先级', goalProgress: '预计完成大部分年度目标', lifeTrajectory: '当前模式将带你走向一个明确的方向' }
        ];
        this.memory.addToL4({
            id: '', level: 'L4', category: 'wisdom', key: `未来预测_${new Date().toISOString().split('T')[0]}`,
            value: { predictions, basedOn: { goals: goals.length, patterns: behaviorPatterns } },
            tags: ['prediction', 'future'], importance: 4, system: this.systemName,
            createdAt: new Date().toISOString(), accessedAt: new Date().toISOString(), accessCount: 0
        });
        return predictions;
    }
    generateWeeklySelfAwarenessReport(period, goals, timeLog, idealAllocation, statedPriorities) {
        const energyAllocation = this.analyzeEnergyAllocation(timeLog, idealAllocation);
        const blindSpots = this.discoverBlindSpots(goals, energyAllocation, statedPriorities);
        const goalProgress = goals.map(g => ({ goal: g.name, weeklyProgress: Math.random() * 10, totalProgress: g.progress }));
        const mirrorFeedback = this.generateAIMirrorLetter('本周我观察到你在多个领域都有投入', goalProgress.filter(g => g.weeklyProgress > 5).map(g => `目标"${g.goal}"有进展`), blindSpots.map(bs => ({ observation: bs.description, concern: bs.impact, suggestion: bs.suggestion })), ['你是否思考过这些目标对你的真正意义？'], ['基于你的能力，我看到了更多可能性'], ['建议下周重点关注精力分配的平衡']);
        const nextWeekSuggestions = blindSpots.length > 0 ? ['关注发现的认知盲点', '调整精力分配', '关注核心目标'] : ['调整精力分配', '关注核心目标'];
        return {
            period, keywords: ['成长', '平衡', '专注'], stateScores: { overall: 7, energy: 6, emotion: 7, progress: 7 },
            energyAllocation, goalProgress, blindSpots, mirrorFeedback, nextWeekSuggestions
        };
    }
    syncToOtherSystems() {
        const profile = this.memory.queryL3('goal');
        const values = this.memory.queryL4('value');
        this.memory.syncToSystem('signal', [...profile, ...values]);
        this.memory.syncToSystem('workflow', [...profile, ...values]);
    }
}
exports.PersonalGoalSystem = PersonalGoalSystem;
//# sourceMappingURL=goal.js.map