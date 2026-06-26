/**
 * Multi-Expert Trigger Rules - 强制多专家协作触发引擎
 *
 * 核心原则：满足以下条件的任务必须强制触发多专家协作
 *
 * 触发条件：
 * 1. 任务涉及多个专业领域（frontend + backend + db等）
 * 2. 任务预估时间超过15分钟
 * 3. 任务包含"复杂"关键词
 * 4. 任务涉及安全/架构/性能关键决策
 * 5. 用户明确要求"多专家"或"团队协作"
 */
/**
 * Multi-Expert Trigger Engine
 */
export class MultiExpertTriggerEngine {
    rules = [];
    constructor() {
        this.initializeRules();
    }
    /**
     * Initialize default trigger rules
     */
    initializeRules() {
        // Rule 1: Multi-domain detection (REQUIRED)
        this.rules.push({
            id: 'multi_domain',
            name: 'Multi-Domain Task',
            description: 'Task spans multiple technical domains',
            condition: (task, ctx) => {
                if (!ctx?.domains || ctx.domains.length < 2)
                    return false;
                return ctx.domains.length >= 2;
            },
            requiredExperts: ['architect', 'planner'],
            priority: 'required',
        });
        // Rule 2: Long-duration task (REQUIRED)
        this.rules.push({
            id: 'long_duration',
            name: 'Long Duration Task',
            description: 'Task estimated to take more than 15 minutes',
            condition: (task, ctx) => {
                return (ctx?.estimatedMinutes ?? 0) > 15;
            },
            requiredExperts: ['planner', 'architect'],
            priority: 'required',
        });
        // Rule 3: Architecture decision (REQUIRED)
        this.rules.push({
            id: 'architecture',
            name: 'Architecture Decision',
            description: 'Task involves system architecture or design',
            condition: (task) => {
                const keywords = ['架构', 'architecture', '设计', '方案', '技术选型', 'tech stack'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['architect', 'planner'],
            priority: 'required',
        });
        // Rule 4: Security-sensitive (REQUIRED)
        this.rules.push({
            id: 'security',
            name: 'Security Sensitive',
            description: 'Task involves authentication, authorization, encryption, etc.',
            condition: (task) => {
                const keywords = ['安全', 'security', '认证', 'auth', '加密', 'encrypt', '权限', 'permission', '密码', 'password', 'token', 'jwt', 'oauth'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['security', 'backend', 'architect'],
            priority: 'required',
        });
        // Rule 5: Database migration (REQUIRED)
        this.rules.push({
            id: 'database',
            name: 'Database Operation',
            description: 'Task involves database schema changes or migrations',
            condition: (task) => {
                const keywords = ['database', 'db', 'sql', 'mongodb', 'migration', 'schema', '表', '数据库', '迁移'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['backend', 'architect'],
            priority: 'required',
        });
        // Rule 6: Performance critical (REQUIRED)
        this.rules.push({
            id: 'performance',
            name: 'Performance Critical',
            description: 'Task involves performance optimization',
            condition: (task) => {
                const keywords = ['performance', 'optimize', '优化', '性能', '慢', 'slow', '缓存', 'cache', 'redis', 'memory'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['backend', 'architect'],
            priority: 'required',
        });
        // Rule 7: Complex task (REQUIRED)
        this.rules.push({
            id: 'complex',
            name: 'Complex Task',
            description: 'Task marked as complex or difficult',
            condition: (task) => {
                const keywords = ['complex', '复杂', '困难', 'difficult', '挑战', 'challenge', '重构', 'refactor'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['architect', 'planner', 'codeReviewer'],
            priority: 'required',
        });
        // Rule 8: Full-stack task (REQUIRED)
        this.rules.push({
            id: 'fullstack',
            name: 'Full-Stack Task',
            description: 'Task involves both frontend and backend',
            condition: (task) => {
                const hasFrontend = ['frontend', 'ui', '界面', '前端', 'react', 'vue', 'angular', '页面', 'component']
                    .some(k => task.toLowerCase().includes(k));
                const hasBackend = ['backend', 'api', 'server', '后端', 'service', '接口', 'database', 'db']
                    .some(k => task.toLowerCase().includes(k));
                return hasFrontend && hasBackend;
            },
            requiredExperts: ['frontend', 'backend', 'architect'],
            priority: 'required',
        });
        // Rule 9: Testing required (RECOMMENDED)
        this.rules.push({
            id: 'testing',
            name: 'Testing Recommended',
            description: 'Task should have testing involvement',
            condition: (task) => {
                const keywords = ['test', 'testing', '测试', 'spec', 'e2e', 'unit'];
                const hasTestKeyword = keywords.some(k => task.toLowerCase().includes(k));
                const hasCode = !['analyze', 'search', '查询', '分析'].some(k => task.toLowerCase().includes(k));
                return hasTestKeyword && hasCode;
            },
            requiredExperts: ['qa'],
            priority: 'recommended',
        });
        // Rule 10: Deployment task (REQUIRED)
        this.rules.push({
            id: 'deployment',
            name: 'Deployment Task',
            description: 'Task involves deployment or infrastructure',
            condition: (task) => {
                const keywords = ['deploy', '部署', 'docker', 'kubernetes', 'k8s', 'ci/cd', 'pipeline', 'release', '发布'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['devops', 'backend'],
            priority: 'required',
        });
        // Rule 11: Explicit multi-expert request (REQUIRED)
        this.rules.push({
            id: 'explicit',
            name: 'Explicit Request',
            description: 'User explicitly asks for multi-expert collaboration',
            condition: (task) => {
                const keywords = ['多专家', 'multi-expert', '团队', 'team', '协作', 'collaborate', '军团', 'army'];
                return keywords.some(k => task.toLowerCase().includes(k));
            },
            requiredExperts: ['architect', 'planner', 'frontend', 'backend', 'qa'],
            priority: 'required',
        });
        // Rule 12: New project (REQUIRED)
        this.rules.push({
            id: 'new_project',
            name: 'New Project',
            description: 'Task involves creating new project or significant new functionality',
            condition: (task) => {
                const keywords = ['new project', '新项目', '新功能', 'new feature', 'create', '创建', '开发'];
                return keywords.some(k => task.toLowerCase().includes(k)) &&
                    (task.toLowerCase().includes('project') || task.toLowerCase().includes('项目'));
            },
            requiredExperts: ['architect', 'planner', 'frontend', 'backend'],
            priority: 'required',
        });
    }
    /**
     * Check if task should trigger multi-expert collaboration
     */
    check(task, context) {
        const matchedRules = [];
        for (const rule of this.rules) {
            if (rule.condition(task, context)) {
                const experts = new Set(rule.requiredExperts);
                matchedRules.push({ rule, experts });
            }
        }
        if (matchedRules.length === 0) {
            return {
                shouldTrigger: false,
                reason: 'Task does not meet any trigger conditions for multi-expert collaboration',
                priority: 'optional',
                suggestedExperts: [],
            };
        }
        // Combine all required experts
        const allExperts = new Set();
        let highestPriority = 'optional';
        for (const { rule, experts } of matchedRules) {
            experts.forEach(e => allExperts.add(e));
            if (rule.priority === 'required' && highestPriority !== 'required') {
                highestPriority = 'required';
            }
            else if (rule.priority === 'recommended' && highestPriority === 'optional') {
                highestPriority = 'recommended';
            }
        }
        const reason = matchedRules
            .map(m => `${m.rule.name} (${m.rule.description})`)
            .join('; ');
        return {
            shouldTrigger: true,
            reason,
            priority: highestPriority,
            suggestedExperts: Array.from(allExperts),
            alternativeTrigger: this.getTriggerCommand(Array.from(allExperts)),
        };
    }
    /**
     * Get the trigger command based on required experts
     */
    getTriggerCommand(experts) {
        // Map to EO tool names
        const hasArchitect = experts.includes('architect');
        const hasPlanner = experts.includes('planner');
        if (hasArchitect) {
            return '/eo_architect';
        }
        if (hasPlanner) {
            return '/eo_plan';
        }
        return '/eo_collab';
    }
    /**
     * Add custom rule
     */
    addRule(rule) {
        this.rules.push({
            ...rule,
            id: `custom_${Date.now()}`,
        });
    }
    /**
     * Get all rules
     */
    getRules() {
        return [...this.rules];
    }
    /**
     * Detect domains from task description
     */
    static detectDomains(task) {
        const domains = [];
        const lower = task.toLowerCase();
        const domainPatterns = [
            { domain: 'web', patterns: ['web', 'html', 'css', 'frontend', 'react', 'vue', 'angular', '页面', '前端'] },
            { domain: 'mobile', patterns: ['mobile', 'ios', 'android', '小程序', 'miniprogram', 'app'] },
            { domain: 'backend', patterns: ['backend', 'server', 'api', '后端', 'node', 'python', 'java', 'go'] },
            { domain: 'database', patterns: ['database', 'db', 'sql', 'mongodb', 'redis', '数据库'] },
            { domain: 'devops', patterns: ['docker', 'k8s', 'kubernetes', 'ci/cd', 'deploy', '部署', 'devops'] },
            { domain: 'security', patterns: ['security', 'auth', '加密', '安全', 'jwt', 'oauth', 'permission'] },
            { domain: 'data', patterns: ['data', 'analytics', 'big data', 'ml', 'ai', '数据', '机器学习'] },
            { domain: 'blockchain', patterns: ['blockchain', 'web3', 'nft', 'crypto', '以太坊', '区块链'] },
        ];
        for (const { domain, patterns } of domainPatterns) {
            if (patterns.some(p => lower.includes(p))) {
                domains.push(domain);
            }
        }
        return domains;
    }
}
// Export singleton
export const multiExpertTrigger = new MultiExpertTriggerEngine();
//# sourceMappingURL=multi-expert-trigger.js.map