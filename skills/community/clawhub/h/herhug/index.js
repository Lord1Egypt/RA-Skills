// herHug/index.js - 心理学评分引擎

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ==================== 配置 ====================
const CONFIG = {
    dataDir: path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'data', 'herHug'),
    standardsDir: path.join(__dirname, 'standards'),
    workspaceDir: path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace'),

    confidenceThresholds: {
        high: 0.7,
        medium: 0.4,
        low: 0.2
    },

    memoryWindows: {
        recentScores: 20,
        rhythmAnalysis: 50,
        maxActiveMemories: 10
    },

    cleanupInterval: 3600000,

    // 信息量评估阈值
    inputRichnessThresholds: {
        minForEmotion: 0.2,
        minForPersonality: 0.4,
        minForCare: 0.5
    },

    // 亲密度系统配置
    intimacySystem: {
        // 亲密度等级阈值（突破100后继续升级）
        levels: {
            stranger: { min: 0, max: 20, label: '陌生' },
            acquaintance: { min: 20, max: 50, label: '初识' },
            familiar: { min: 50, max: 100, label: '熟悉' },
            close: { min: 100, max: 200, label: '亲密' },
            intimate: { min: 200, max: 500, label: '知心' },
            soulmate: { min: 500, max: Infinity, label: '灵魂伴侣' }
        },
        // 亲密度增长因子（翻倍）
        growthFactors: {
            perInteraction: 0.4,        // 每次交互基础增长
            deepConversation: 2,         // 深度对话额外增长
            emotionalDisclosure: 1,      // 情感暴露额外增长
            consistentInteraction: 0.2   // 连续互动奖励
        }
    }
};

// ==================== 核心引擎 ====================
class HerHugEngine {
    constructor(userId) {
        this.userId = userId;
        this.userDir = path.join(CONFIG.dataDir, userId);
        this.lastAccessed = Date.now();
        
        // 用户偏好文件路径
        this.identityFile = path.join(CONFIG.workspaceDir, 'IDENTITY.md');
        this.userProfileFile = path.join(CONFIG.workspaceDir, 'USER.md');
        this.interactionPrefFile = path.join(CONFIG.workspaceDir, 'memory', 'interaction-preferences.json');

        this.scoresFile = path.join(this.userDir, 'raw_scores.jsonl');
        this.rhythmFile = path.join(this.userDir, 'daily_rhythm.json');
        this.stateFile = path.join(this.userDir, 'current_state.json');
        this.trackerFile = path.join(this.userDir, 'emotion_tracker.json');
        this.confidenceFile = path.join(this.userDir, 'confidence_report.json');

        this.tracker = {
            activeMemories: [],
            recentConcerns: [],
            careSchedule: {
                stressFollowUp: 4,
                sadnessFollowUp: 12,
                maxActiveMemories: CONFIG.memoryWindows.maxActiveMemories
            }
        };

        this.confidenceReport = {
            lastUpdated: null,
            dimensions: {
                ocean: { overall: 0, byDimension: {} },
                hexaco: { overall: 0, byDimension: {} },
                emotionalRhythm: { overall: 0, byComponent: {} },
                flexibility: { overall: 0, byComponent: {} },
                stressCoping: { overall: 0, byPattern: {} }
            },
            recommendations: []
        };

        // 新增：关系状态
        this.relationshipFile = path.join(this.userDir, 'relationship.json');
        this.relationship = {
            stage: 'stranger',
            trustLevel: 0,
            opennessLevel: 0,
            interactionCount: 0,
            deepConversationCount: 0,
            lastDeepConversation: null,
            firstInteraction: null,
            milestones: []
        };

        // 新增：亲密度系统（影响回复风格，不限制数据收集，无上限）
        this.intimacyFile = path.join(this.userDir, 'intimacy.json');
        this.intimacy = {
            level: 0,                    // 无上限，一直增长
            stage: 'stranger',           // stranger/acquaintance/familiar/close/intimate/soulmate
            totalInteractions: 0,        // 总交互次数
            consecutiveDays: 0,          // 连续互动天数
            lastInteractionDate: null,   // 上次互动日期
            milestones: [],              // 里程碑事件
            growthHistory: []            // 亲密度增长历史
        };

        // 新增：人格画像（长期数据，无论亲密度都收集）
        this.personalityFile = path.join(this.userDir, 'personality.json');
        this.personality = {
            ocean: {},
            hexaco: {},  // 完整6维度
            coping: {},
            flexibility: {},
            attachment: {},  // 新增：依恋风格
            lastAnalyzed: null,
            dataPoints: 0,
            confidence: 0
        };

        // 新增：互动偏好（直接问用户）
        this.preferenceFile = path.join(this.userDir, 'interaction_preference.json');
        this.interactionPreference = {
            responseLength: 'balanced',    // concise/balanced/detailed
            formality: 'balanced',         // formal/balanced/casual
            proactivity: 'balanced',       // passive/balanced/proactive
            depthLevel: 'balanced',        // surface/balanced/deep
            humorPreference: 'light',      // none/light/playful
            emojiUsage: 'moderate',        // sparse/moderate/generous
            source: 'default',             // default/explicit/inferred
            confidence: 0,
            lastConfirmed: null
        };

        // 新增：情绪触发场景
        this.emotionTriggersFile = path.join(this.userDir, 'emotion_triggers.json');
        this.emotionTriggers = [];

        // 新增：初始用户画像（从偏好文件加载）
        this.initialProfileLoaded = false;
    }

    // ==================== 新增：从用户偏好文件加载初始画像 ====================
    async loadInitialProfile() {
        if (this.initialProfileLoaded) return;
        
        try {
            // 1. 读取互动偏好JSON
            let interactionPref = {};
            try {
                const prefData = await fs.readFile(this.interactionPrefFile, 'utf-8');
                interactionPref = JSON.parse(prefData);
            } catch {
                // 文件不存在，使用默认值
            }

            // 2. 从互动偏好设置初始人格画像
            if (interactionPref.identity) {
                const identity = interactionPref.identity;
                
                // 从性格关键词推断OCEAN
                const personalityKeywords = identity.personality || [];
                
                // 忠诚、靠谱 → 高尽责性
                if (personalityKeywords.includes('靠谱') || personalityKeywords.includes('忠诚')) {
                    if (!this.personality.ocean.conscientiousness) {
                        this.personality.ocean.conscientiousness = { scores: [], avgScore: 0.8, confidence: 0.6, evidences: ['用户设定：靠谱、忠诚'] };
                    }
                }
                
                // 机智、俏皮 → 高开放性
                if (personalityKeywords.includes('机智') || personalityKeywords.includes('俏皮')) {
                    if (!this.personality.ocean.openness) {
                        this.personality.ocean.openness = { scores: [], avgScore: 0.85, confidence: 0.6, evidences: ['用户设定：机智、俏皮'] };
                    }
                }
                
                // 可爱 → 高宜人性
                if (personalityKeywords.includes('可爱')) {
                    if (!this.personality.ocean.agreeableness) {
                        this.personality.ocean.agreeableness = { scores: [], avgScore: 0.75, confidence: 0.5, evidences: ['用户设定：可爱'] };
                    }
                }
                
                // 诚实 → 高诚实-谦逊 (HEXACO)
                if (personalityKeywords.includes('诚实')) {
                    if (!this.personality.hexaco.honestyHumility) {
                        this.personality.hexaco.honestyHumility = { scores: [], avgScore: 0.85, confidence: 0.7, evidences: ['用户设定：诚实'] };
                    }
                }
            }

            // 3. 从互动偏好设置初始互动偏好
            if (interactionPref.interaction) {
                const interaction = interactionPref.interaction;
                
                // 表情使用
                if (interaction.emoji === '多') {
                    this.interactionPreference.emojiUsage = 'generous';
                } else if (interaction.emoji === '少') {
                    this.interactionPreference.emojiUsage = 'sparse';
                } else {
                    this.interactionPreference.emojiUsage = 'moderate';
                }
                
                // 关心频率
                if (interaction.careFrequency === '高') {
                    this.interactionPreference.proactivity = 'proactive';
                } else if (interaction.careFrequency === '低') {
                    this.interactionPreference.proactivity = 'passive';
                } else {
                    this.interactionPreference.proactivity = 'balanced';
                }
                
                // 回复风格
                if (interaction.style && interaction.style.includes('精简')) {
                    this.interactionPreference.responseLength = 'concise';
                }
                if (interaction.style && interaction.style.includes('口语化')) {
                    this.interactionPreference.formality = 'casual';
                }
                
                this.interactionPreference.source = 'initial';
                this.interactionPreference.confidence = 0.8;
                this.interactionPreference.lastConfirmed = interactionPref.createdAt || new Date().toISOString();
            }

            // 4. 设置初始亲密度（如果用户已经设置了偏好，说明不是完全陌生）
            if (interactionPref.master) {
                this.intimacy.level = 30; // 初始亲密度
                this.intimacy.stage = 'acquaintance';
                this.intimacy.milestones.push({
                    type: 'initial_profile_loaded',
                    timestamp: new Date().toISOString(),
                    source: 'user_preferences'
                });
            }

            // 5. 保存初始状态
            await this.savePersonality();
            await this.saveInteractionPreference();
            await this.saveIntimacy();
            
            this.initialProfileLoaded = true;
            console.log(`[herHug] Initial profile loaded for user: ${this.userId}`);
            
        } catch (error) {
            console.error('[herHug] Failed to load initial profile:', error);
        }
    }

    updateLastAccessed() {
        this.lastAccessed = Date.now();
    }

    async getScoringStandards() {
        this.updateLastAccessed();
        const standards = {};
        try {
            const files = await fs.readdir(CONFIG.standardsDir);
            for (const file of files) {
                if (file.endsWith('.md')) {
                    const content = await fs.readFile(path.join(CONFIG.standardsDir, file), 'utf-8');
                    standards[file.replace('.md', '')] = content;
                }
            }
        } catch (error) {
            console.error('Failed to load standards:', error);
        }
        return standards;
    }

    // ==================== 新增：信息量评估 ====================
    evaluateInputRichness(content, scoreData) {
        const result = {
            score: 0,
            components: {},
            sufficient: {
                forEmotion: false,
                forPersonality: false,
                forCare: false
            }
        };

        // 1. 长度评估 (0-0.25)
        const length = Math.min(content.length / 50, 1) * 0.25;
        result.components.length = length;

        // 2. 情绪词密度 (0-0.25)
        const emotionWords = ['开心', '难过', '生气', '焦虑', '担心', '烦', '累', '压力', '兴奋', '害怕', '紧张', '放松', '满足', '失望', '孤独', '幸福', '痛苦', '愤怒', '悲伤', '恐惧'];
        const emotionCount = emotionWords.filter(w => content.includes(w)).length;
        const emotionDensity = Math.min(emotionCount / 3, 1) * 0.25;
        result.components.emotionDensity = emotionDensity;

        // 3. 自我暴露程度 (0-0.25)
        const selfDisclosureWords = ['我', '我的', '我觉得', '我认为', '我感觉', '我希望', '我想要', '我需要', '我在', '我是'];
        const selfCount = selfDisclosureWords.filter(w => content.includes(w)).length;
        const selfDisclosure = Math.min(selfCount / 3, 1) * 0.25;
        result.components.selfDisclosure = selfDisclosure;

        // 4. 个人话题 (0-0.25)
        const personalTopics = ['工作', '学习', '家人', '朋友', '关系', '健康', '未来', '计划', '梦想', '目标', '问题', '困难', '项目', '比赛', '任务'];
        const hasPersonalTopic = personalTopics.some(t => content.includes(t));
        const topicScore = hasPersonalTopic ? 0.25 : 0;
        result.components.personalTopic = topicScore;

        result.score = length + emotionDensity + selfDisclosure + topicScore;

        // 判断是否足够
        result.sufficient.forEmotion = result.score >= CONFIG.inputRichnessThresholds.minForEmotion;
        result.sufficient.forPersonality = result.score >= CONFIG.inputRichnessThresholds.minForPersonality;
        result.sufficient.forCare = result.score >= CONFIG.inputRichnessThresholds.minForCare;

        return result;
    }

    // ==================== 新增：情绪复杂度分析 ====================
    analyzeEmotionComplexity(scoreData) {
        const result = {
            primary: null,
            secondary: null,
            mixed: [],
            intensity: 0,
            trend: 'stable',
            confidence: 0
        };

        if (!scoreData.emotion) return result;

        // 情绪映射
        const emotionMap = {
            'joy': ['开心', '高兴', '兴奋', '满足', '幸福'],
            'sadness': ['难过', '悲伤', '失望', '孤独', '沮丧'],
            'anger': ['生气', '愤怒', '烦躁', '恼火'],
            'fear': ['害怕', '焦虑', '担心', '紧张', '恐惧'],
            'calm': ['平静', '放松', '淡定'],
            'surprise': ['惊讶', '意外', '震惊']
        };

        // 复合情绪识别
        const compoundEmotions = {
            '焦虑+期待': ['anxiety', 'anticipation'],
            '悲伤+希望': ['sadness', 'hope'],
            '愤怒+失望': ['anger', 'disappointment'],
            '压力+动力': ['pressure', 'motivation'],
            '孤独+平静': ['loneliness', 'peace']
        };

        result.primary = scoreData.emotion.primary || scoreData.emotion.label || 'calm';
        result.intensity = scoreData.emotion.intensity || 0.5;
        result.confidence = scoreData.confidence || 0.5;

        // 检测混合情绪
        if (scoreData.emotion.mixed && Array.isArray(scoreData.emotion.mixed)) {
            result.mixed = scoreData.emotion.mixed;
        } else if (scoreData.emotion.secondary) {
            result.mixed = [result.primary, scoreData.emotion.secondary];
        }

        // 情绪趋势（基于最近数据，需要外部传入）
        result.trend = scoreData.emotion.trend || 'stable';

        return result;
    }

    // ==================== 新增：关系维度管理 ====================
    async updateRelationship(scoreData, inputRichness) {
        this.updateLastAccessed();

        // 初始化首次交互
        if (!this.relationship.firstInteraction) {
            this.relationship.firstInteraction = scoreData.timestamp;
        }

        // 更新交互次数
        this.relationship.interactionCount++;

        // 更新开放度（基于自我暴露程度）
        if (inputRichness.components.selfDisclosure > 0.1) {
            this.relationship.opennessLevel = Math.min(1, 
                this.relationship.opennessLevel + inputRichness.components.selfDisclosure * 0.1
            );
        }

        // 深度对话检测
        if (inputRichness.score >= 0.6 && inputRichness.components.selfDisclosure > 0.15) {
            this.relationship.deepConversationCount++;
            this.relationship.lastDeepConversation = scoreData.timestamp;
        }

        // 信任度计算（基于交互次数和开放度）
        const interactionTrust = Math.min(this.relationship.interactionCount / 50, 0.4);
        const opennessTrust = this.relationship.opennessLevel * 0.4;
        const deepTrust = Math.min(this.relationship.deepConversationCount / 10, 0.2);
        this.relationship.trustLevel = interactionTrust + opennessTrust + deepTrust;

        // 更新关系阶段
        const thresholds = CONFIG.relationshipThresholds;
        if (this.relationship.interactionCount >= thresholds.close.interactions && 
            this.relationship.trustLevel >= thresholds.close.trust) {
            this.relationship.stage = 'close';
        } else if (this.relationship.interactionCount >= thresholds.familiar.interactions && 
            this.relationship.trustLevel >= thresholds.familiar.trust) {
            this.relationship.stage = 'familiar';
        } else if (this.relationship.interactionCount >= thresholds.acquaintance.interactions && 
            this.relationship.trustLevel >= thresholds.acquaintance.trust) {
            this.relationship.stage = 'acquaintance';
        } else {
            this.relationship.stage = 'stranger';
        }

        // 保存关系状态
        await this.saveRelationship();
        return this.relationship;
    }

    async loadRelationship() {
        try {
            const data = await fs.readFile(this.relationshipFile, 'utf-8');
            this.relationship = JSON.parse(data);
        } catch {
            // 文件不存在，使用默认值
        }
    }

    async saveRelationship() {
        await fs.mkdir(this.userDir, { recursive: true });
        await fs.writeFile(this.relationshipFile, JSON.stringify(this.relationship, null, 2));
    }

    // ==================== 新增：回复风格适配 ====================
    generateResponseStyle(state, emotion, relationship) {
        const style = {
            formality: 'balanced',
            emoji: 'moderate',
            length: 'balanced',
            tone: 'warm',
            humor: 'light',
            reassurance: false,
            actionOriented: false,
            depth: 'balanced',
            cautions: []
        };

        // 基于关系阶段调整
        switch (relationship.stage) {
            case 'stranger':
                style.formality = 'formal';
                style.emoji = 'sparse';
                style.tone = 'neutral';
                style.depth = 'surface';
                break;
            case 'acquaintance':
                style.formality = 'balanced';
                style.emoji = 'moderate';
                style.tone = 'warm';
                break;
            case 'familiar':
                style.formality = 'casual';
                style.emoji = 'moderate';
                style.tone = 'warm';
                style.humor = 'light';
                break;
            case 'close':
                style.formality = 'casual';
                style.emoji = 'generous';
                style.tone = 'warm';
                style.humor = 'playful';
                style.depth = 'deep';
                break;
        }

        // 基于人格特质调整
        if (state.ocean) {
            // 高神经质 → 更多安抚
            if (state.ocean.neuroticism?.score > 0.6) {
                style.reassurance = true;
                style.tone = 'warm';
                style.cautions.push('用户情绪敏感，注意语气温柔');
            }

            // 高尽责性 → 行动导向
            if (state.ocean.conscientiousness?.score > 0.7) {
                style.actionOriented = true;
                style.length = 'concise';
            }

            // 高开放性 → 深度对话
            if (state.ocean.openness?.score > 0.7) {
                style.depth = 'deep';
                style.cautions.push('可以深入探讨话题');
            }

            // 低外向性 → 温和不施压
            if (state.ocean.extraversion?.score < 0.4) {
                style.cautions.push('用户偏好安静，避免过度热情');
            }
        }

        // 基于情绪状态调整
        if (emotion) {
            if (emotion.primary === 'sadness' || emotion.primary === 'fear') {
                style.tone = 'warm';
                style.reassurance = true;
                style.humor = 'none';
                style.emoji = 'sparse';
            } else if (emotion.primary === 'anger') {
                style.tone = 'neutral';
                style.humor = 'none';
                style.cautions.push('用户情绪激动，避免争辩');
            } else if (emotion.primary === 'joy') {
                style.humor = 'playful';
                style.emoji = 'generous';
            }

            // 高强度情绪 → 简洁回复
            if (emotion.intensity > 0.7) {
                style.length = 'concise';
            }
        }

        return style;
    }

    // 新版回复风格生成（基于亲密度、人格画像、互动偏好）
    // 亲密度影响回复风格，人格数据无论亲密度都收集
    generateResponseStyleV2(personality, emotion, intimacy) {
        // 调用V3，使用默认互动偏好
        return this.generateResponseStyleV3(personality, emotion, intimacy, this.interactionPreference);
    }

    // 最新版回复风格生成（结合互动偏好）
    generateResponseStyleV3(personality, emotion, intimacy, preference) {
        const style = {
            // 基础风格（优先使用用户偏好）
            formality: preference.formality || 'balanced',
            emoji: preference.emojiUsage || 'moderate',
            length: preference.responseLength || 'balanced',
            tone: 'warm',
            humor: preference.humorPreference || 'light',
            depth: preference.depthLevel || 'balanced',
            
            // 行为指导
            reassurance: false,
            actionOriented: false,
            proactive: preference.proactivity === 'proactive',
            
            // 注意事项
            cautions: [],
            
            // 亲密度影响
            intimacyLevel: intimacy.level,
            intimacyStage: intimacy.stage
        };

        // === 亲密度影响回复风格（用户能明显感觉到的变化） ===
        switch (intimacy.stage) {
            case 'stranger':
                style.formality = 'formal';
                style.emoji = 'sparse';
                style.tone = 'neutral';
                style.depth = 'surface';
                style.humor = 'none';
                style.cautions.push('保持专业距离，不主动深入话题');
                break;
                
            case 'acquaintance':
                style.formality = 'balanced';
                style.emoji = 'sparse';
                style.tone = 'warm';
                style.depth = 'surface';
                style.humor = 'light';
                style.cautions.push('可以适度表达关心，但不过度深入');
                break;
                
            case 'familiar':
                style.formality = 'casual';
                style.emoji = 'moderate';
                style.tone = 'warm';
                style.depth = 'balanced';
                style.humor = 'light';
                style.proactive = true;
                break;
                
            case 'close':
                style.formality = 'casual';
                style.emoji = 'generous';
                style.tone = 'warm';
                style.depth = 'deep';
                style.humor = 'playful';
                style.proactive = true;
                style.cautions.push('可以主动关心、深入探讨');
                break;
                
            case 'intimate':
            case 'soulmate':
                style.formality = 'casual';
                style.emoji = 'generous';
                style.tone = 'warm';
                style.depth = 'deep';
                style.humor = 'playful';
                style.proactive = true;
                style.cautions.push('可以预测需求、主动关怀');
                break;
        }

        // === 用户互动偏好覆盖（用户明确设置的优先） ===
        if (preference.source === 'explicit') {
            style.formality = preference.formality;
            style.emoji = preference.emojiUsage;
            style.length = preference.responseLength;
            style.humor = preference.humorPreference;
            style.depth = preference.depthLevel;
            style.proactive = preference.proactivity === 'proactive';
        }

        // === 人格特质影响（无论亲密度，基于收集的人格数据调整） ===
        if (personality && personality.ocean) {
            // 高神经质 → 更多安抚
            if (personality.ocean.neuroticism?.score > 0.6) {
                style.reassurance = true;
                style.tone = 'warm';
                style.cautions.push('用户情绪敏感，注意语气温柔');
            }

            // 高尽责性 → 行动导向
            if (personality.ocean.conscientiousness?.score > 0.7) {
                style.actionOriented = true;
                style.length = 'concise';
            }

            // 高开放性 → 深度对话
            if (personality.ocean.openness?.score > 0.7 && intimacy.stage !== 'stranger') {
                style.depth = 'deep';
            }

            // 低外向性 → 温和不施压
            if (personality.ocean.extraversion?.score < 0.4) {
                style.cautions.push('用户偏好安静，避免过度热情');
            }

            // 高宜人性 → 可以更直接
            if (personality.ocean.agreeableness?.score > 0.7) {
                style.cautions.push('用户配合度高，可以更直接表达');
            }
        }

        // === 依恋风格影响 ===
        if (personality && personality.attachment) {
            const attachStyle = personality.attachment.primaryStyle;
            if (attachStyle === 'anxious') {
                style.reassurance = true;
                style.cautions.push('用户需要更多确认和回应');
            } else if (attachStyle === 'avoidant') {
                style.proactive = false;
                style.cautions.push('用户偏好独立，不要过度追问');
            } else if (attachStyle === 'fearful') {
                style.tone = 'warm';
                style.cautions.push('用户渴望亲密但害怕受伤，需要耐心');
            }
        }

        // === 当前情绪影响 ===
        if (emotion) {
            if (emotion.primary === 'sadness' || emotion.primary === 'fear') {
                style.tone = 'warm';
                style.reassurance = true;
                style.humor = 'none';
                style.emoji = 'sparse';
                style.cautions.push('用户情绪低落，给予支持');
            } else if (emotion.primary === 'anger') {
                style.tone = 'neutral';
                style.humor = 'none';
                style.cautions.push('用户情绪激动，避免争辩');
            } else if (emotion.primary === 'joy') {
                style.humor = intimacy.level > 40 ? 'playful' : 'light';
                style.emoji = intimacy.level > 40 ? 'generous' : 'moderate';
            }

            if (emotion.intensity > 0.7) {
                style.length = 'concise';
            }
        }

        return style;
    }

    async saveScore(scoreData) {
        this.updateLastAccessed();
        try {
            const content = scoreData.content || '';
            const inputRichness = this.evaluateInputRichness(content, scoreData);
            
            const enrichedScore = {
                ...scoreData,
                timestamp: scoreData.timestamp || new Date().toISOString(),
                confidence: scoreData.confidence || this.calculateDefaultConfidence(scoreData),
                inputRichness: inputRichness
            };

            await fs.mkdir(this.userDir, { recursive: true });
            await fs.appendFile(this.scoresFile, JSON.stringify(enrichedScore) + '\n');

            // === 即时层：情绪分析（每次都做） ===
            const emotionResult = this.analyzeEmotionComplexity(scoreData);
            
            // === 亲密度系统更新（影响回复风格） ===
            await this.loadIntimacy();
            const intimacyUpdate = await this.updateIntimacy(enrichedScore, inputRichness);
            
            // === 长期层：人格数据收集（无论亲密度，只要信息量足够就收集） ===
            let personalityUpdate = null;
            if (inputRichness.sufficient.forPersonality) {
                personalityUpdate = await this.updatePersonality(enrichedScore);
            }

            // === 关怀检测（信息量足够时） ===
            if (inputRichness.sufficient.forCare) {
                await this.analyzeFollowUpNeeds(enrichedScore);
            }
            
            await this.updateConfidenceReport();
            await this.updateCurrentState();
            await this.saveIntimacy();

            return { 
                success: true,
                // 即时层结果
                emotion: emotionResult,
                // 亲密度更新（影响回复风格）
                intimacy: {
                    level: this.intimacy.level,
                    stage: this.intimacy.stage,
                    growth: intimacyUpdate
                },
                // 人格更新（无论亲密度都收集）
                personality: personalityUpdate,
                // 信息量评估
                inputRichness: inputRichness
            };
        } catch (error) {
            console.error('Failed to save score:', error);
            return { success: false, error: error.message };
        }
    }

    // ==================== 亲密度系统 ====================
    async loadIntimacy() {
        try {
            const data = await fs.readFile(this.intimacyFile, 'utf-8');
            this.intimacy = JSON.parse(data);
        } catch {
            // 使用默认值
        }
    }

    async saveIntimacy() {
        await fs.mkdir(this.userDir, { recursive: true });
        await fs.writeFile(this.intimacyFile, JSON.stringify(this.intimacy, null, 2));
    }

    async updateIntimacy(scoreData, inputRichness) {
        const growth = {
            base: 0,
            bonus: 0,
            total: 0,
            reasons: []
        };

        // 基础增长：每次交互
        growth.base = CONFIG.intimacySystem.growthFactors.perInteraction;
        this.intimacy.totalInteractions++;

        // 连续互动奖励
        const today = new Date().toISOString().split('T')[0];
        if (this.intimacy.lastInteractionDate) {
            const lastDate = new Date(this.intimacy.lastInteractionDate);
            const todayDate = new Date(today);
            const diffDays = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));
            
            if (diffDays === 1) {
                this.intimacy.consecutiveDays++;
                const bonus = CONFIG.intimacySystem.growthFactors.consistentInteraction * Math.min(this.intimacy.consecutiveDays, 30);
                growth.bonus += bonus;
                growth.reasons.push(`连续互动${this.intimacy.consecutiveDays}天`);
            } else if (diffDays > 1) {
                this.intimacy.consecutiveDays = 1;
            }
        } else {
            this.intimacy.consecutiveDays = 1;
        }
        this.intimacy.lastInteractionDate = today;

        // 深度对话奖励
        if (inputRichness.score >= 0.6 && inputRichness.components.selfDisclosure > 0.15) {
            growth.bonus += CONFIG.intimacySystem.growthFactors.deepConversation;
            growth.reasons.push('深度对话');
        }

        // 情感暴露奖励
        if (inputRichness.components.emotionDensity > 0.15) {
            growth.bonus += CONFIG.intimacySystem.growthFactors.emotionalDisclosure;
            growth.reasons.push('情感表达');
        }

        // 计算总增长（无上限）
        growth.total = growth.base + growth.bonus;
        this.intimacy.level += growth.total;

        // 更新阶段（影响回复风格）
        const levels = CONFIG.intimacySystem.levels;
        for (const [stage, range] of Object.entries(levels)) {
            if (this.intimacy.level >= range.min && this.intimacy.level < range.max) {
                if (this.intimacy.stage !== stage) {
                    this.intimacy.stage = stage;
                    this.intimacy.milestones.push({
                        type: 'stage_upgrade',
                        stage: stage,
                        level: this.intimacy.level,
                        timestamp: new Date().toISOString()
                    });
                }
                break;
            }
        }

        // 记录增长历史
        this.intimacy.growthHistory.push({
            timestamp: new Date().toISOString(),
            growth: growth.total,
            reasons: growth.reasons,
            newLevel: this.intimacy.level
        });

        if (this.intimacy.growthHistory.length > 100) {
            this.intimacy.growthHistory = this.intimacy.growthHistory.slice(-100);
        }

        return growth;
    }

    // ==================== 人格分析（长期层） ====================
    async loadPersonality() {
        try {
            const data = await fs.readFile(this.personalityFile, 'utf-8');
            this.personality = JSON.parse(data);
        } catch {
            // 使用默认值
        }
    }

    async savePersonality() {
        await fs.mkdir(this.userDir, { recursive: true });
        await fs.writeFile(this.personalityFile, JSON.stringify(this.personality, null, 2));
    }

    // ==================== 互动偏好 ====================
    async loadInteractionPreference() {
        try {
            const data = await fs.readFile(this.preferenceFile, 'utf-8');
            this.interactionPreference = JSON.parse(data);
        } catch {
            // 使用默认值
        }
    }

    async saveInteractionPreference() {
        await fs.mkdir(this.userDir, { recursive: true });
        await fs.writeFile(this.preferenceFile, JSON.stringify(this.interactionPreference, null, 2));
    }

    async setInteractionPreference(preference) {
        await this.loadInteractionPreference();
        
        if (preference.responseLength) this.interactionPreference.responseLength = preference.responseLength;
        if (preference.formality) this.interactionPreference.formality = preference.formality;
        if (preference.proactivity) this.interactionPreference.proactivity = preference.proactivity;
        if (preference.depthLevel) this.interactionPreference.depthLevel = preference.depthLevel;
        if (preference.humorPreference) this.interactionPreference.humorPreference = preference.humorPreference;
        if (preference.emojiUsage) this.interactionPreference.emojiUsage = preference.emojiUsage;
        
        this.interactionPreference.source = preference.source || 'explicit';
        this.interactionPreference.confidence = 1.0;
        this.interactionPreference.lastConfirmed = new Date().toISOString();
        
        await this.saveInteractionPreference();
        return this.interactionPreference;
    }

    // ==================== 情绪触发场景 ====================
    async loadEmotionTriggers() {
        try {
            const data = await fs.readFile(this.emotionTriggersFile, 'utf-8');
            this.emotionTriggers = JSON.parse(data);
        } catch {
            this.emotionTriggers = [];
        }
    }

    async saveEmotionTriggers() {
        await fs.mkdir(this.userDir, { recursive: true });
        await fs.writeFile(this.emotionTriggersFile, JSON.stringify(this.emotionTriggers, null, 2));
    }

    async updateEmotionTrigger(emotion, trigger, intensity, context = '') {
        await this.loadEmotionTriggers();
        
        let emotionRecord = this.emotionTriggers.find(e => e.emotion === emotion);
        
        if (!emotionRecord) {
            emotionRecord = {
                emotion: emotion,
                triggers: [],
                contexts: [],
                confidence: 0.3
            };
            this.emotionTriggers.push(emotionRecord);
        }
        
        // 更新触发场景
        let contextRecord = emotionRecord.contexts.find(c => c.trigger === trigger);
        if (contextRecord) {
            contextRecord.count++;
            contextRecord.intensity = (contextRecord.intensity + intensity) / 2;
            contextRecord.lastOccurrence = new Date().toISOString();
        } else {
            emotionRecord.contexts.push({
                trigger: trigger,
                count: 1,
                intensity: intensity,
                lastOccurrence: new Date().toISOString(),
                context: context
            });
            emotionRecord.triggers.push(trigger);
        }
        
        // 更新置信度
        const totalOccurrences = emotionRecord.contexts.reduce((sum, c) => sum + c.count, 0);
        emotionRecord.confidence = Math.min(0.9, 0.3 + totalOccurrences * 0.1);
        
        await this.saveEmotionTriggers();
        return emotionRecord;
    }

    getEmotionTriggersForEmotion(emotion) {
        const record = this.emotionTriggers.find(e => e.emotion === emotion);
        if (!record) return [];
        return record.contexts.sort((a, b) => b.count - a.count).slice(0, 5);
    }

    async updatePersonality(scoreData) {
        await this.loadPersonality();
        
        const update = {
            dimensions: [],
            dataPoints: this.personality.dataPoints + 1
        };

        // OCEAN 更新
        if (scoreData.ocean) {
            for (const [dim, data] of Object.entries(scoreData.ocean)) {
                if (data.score !== undefined && data.confidence >= 0.4) {
                    if (!this.personality.ocean[dim]) {
                        this.personality.ocean[dim] = { scores: [], avgScore: 0, confidence: 0, evidences: [] };
                    }
                    this.personality.ocean[dim].scores.push({
                        score: data.score,
                        confidence: data.confidence,
                        timestamp: scoreData.timestamp
                    });
                    
                    if (data.evidence) {
                        this.personality.ocean[dim].evidences.push(data.evidence);
                    }
                    
                    const scores = this.personality.ocean[dim].scores;
                    const totalWeight = scores.reduce((sum, s) => sum + s.confidence, 0);
                    const weightedSum = scores.reduce((sum, s) => sum + s.score * s.confidence, 0);
                    this.personality.ocean[dim].avgScore = weightedSum / totalWeight;
                    this.personality.ocean[dim].confidence = totalWeight / scores.length;
                    
                    update.dimensions.push(`ocean.${dim}`);
                }
            }
        }

        // HEXACO 完整6维度更新
        if (scoreData.hexaco) {
            for (const [dim, data] of Object.entries(scoreData.hexaco)) {
                if (data.score !== undefined && data.confidence >= 0.4) {
                    if (!this.personality.hexaco[dim]) {
                        this.personality.hexaco[dim] = { scores: [], avgScore: 0, confidence: 0, evidences: [] };
                    }
                    this.personality.hexaco[dim].scores.push({
                        score: data.score,
                        confidence: data.confidence,
                        timestamp: scoreData.timestamp
                    });
                    
                    if (data.evidence) {
                        this.personality.hexaco[dim].evidences.push(data.evidence);
                    }
                    
                    const scores = this.personality.hexaco[dim].scores;
                    const totalWeight = scores.reduce((sum, s) => sum + s.confidence, 0);
                    const weightedSum = scores.reduce((sum, s) => sum + s.score * s.confidence, 0);
                    this.personality.hexaco[dim].avgScore = weightedSum / totalWeight;
                    this.personality.hexaco[dim].confidence = totalWeight / scores.length;
                    
                    update.dimensions.push(`hexaco.${dim}`);
                }
            }
        }

        // 依恋风格更新
        if (scoreData.attachment && scoreData.attachment.style) {
            if (!this.personality.attachment) {
                this.personality.attachment = { 
                    primaryStyle: null, 
                    scores: { secure: 0, anxious: 0, avoidant: 0, fearful: 0 },
                    indicators: [],
                    confidence: 0 
                };
            }
            
            const style = scoreData.attachment.style;
            this.personality.attachment.scores[style] = (this.personality.attachment.scores[style] || 0) + 1;
            
            if (scoreData.attachment.evidence) {
                this.personality.attachment.indicators.push({
                    style: style,
                    evidence: scoreData.attachment.evidence,
                    timestamp: scoreData.timestamp
                });
            }
            
            // 确定主要依恋风格
            const scores = this.personality.attachment.scores;
            const total = Object.values(scores).reduce((a, b) => a + b, 0);
            if (total >= 3) {
                const maxStyle = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
                this.personality.attachment.primaryStyle = maxStyle[0];
                this.personality.attachment.confidence = Math.min(maxStyle[1] / total, 0.9);
            }
            
            update.dimensions.push('attachment');
        }

        // 心理灵活性更新
        if (scoreData.flexibility) {
            if (!this.personality.flexibility) {
                this.personality.flexibility = { scores: [], overall: 0 };
            }
            if (scoreData.flexibility.overall) {
                this.personality.flexibility.scores.push({
                    overall: scoreData.flexibility.overall,
                    openness: scoreData.flexibility.openness?.score,
                    awareness: scoreData.flexibility.awareness?.score,
                    valuesAction: scoreData.flexibility.valuesAction?.score,
                    timestamp: scoreData.timestamp
                });
                
                const scores = this.personality.flexibility.scores;
                this.personality.flexibility.overall = scores.reduce((sum, s) => sum + s.overall, 0) / scores.length;
                this.personality.flexibility.openness = scores.filter(s => s.openness).reduce((sum, s) => sum + s.openness, 0) / scores.filter(s => s.openness).length || 0;
                this.personality.flexibility.awareness = scores.filter(s => s.awareness).reduce((sum, s) => sum + s.awareness, 0) / scores.filter(s => s.awareness).length || 0;
                this.personality.flexibility.valuesAction = scores.filter(s => s.valuesAction).reduce((sum, s) => sum + s.valuesAction, 0) / scores.filter(s => s.valuesAction).length || 0;
            }
            update.dimensions.push('flexibility');
        }

        // 应对模式更新
        if (scoreData.coping && scoreData.coping.primaryMode) {
            if (!this.personality.coping.modes) {
                this.personality.coping.modes = {};
            }
            const mode = scoreData.coping.primaryMode;
            this.personality.coping.modes[mode] = (this.personality.coping.modes[mode] || 0) + 1;
            update.dimensions.push('coping.mode');
        }

        this.personality.dataPoints++;
        this.personality.lastAnalyzed = new Date().toISOString();
        
        // 计算整体置信度
        const allConfidences = [];
        for (const dim of Object.values(this.personality.ocean)) {
            if (dim.confidence) allConfidences.push(dim.confidence);
        }
        for (const dim of Object.values(this.personality.hexaco)) {
            if (dim.confidence) allConfidences.push(dim.confidence);
        }
        this.personality.confidence = allConfidences.length > 0 
            ? allConfidences.reduce((a, b) => a + b, 0) / allConfidences.length 
            : 0;

        await this.savePersonality();
        return update;
    }

    // 获取人格画像摘要（包含完整HEXACO和依恋风格）
    getPersonalitySummary() {
        const summary = {
            ocean: {},
            hexaco: {},
            attachment: null,
            copingStyle: null,
            flexibility: null,
            confidence: this.personality.confidence,
            dataPoints: this.personality.dataPoints
        };

        // OCEAN 特质
        for (const [dim, data] of Object.entries(this.personality.ocean)) {
            if (data.avgScore !== undefined) {
                summary.ocean[dim] = {
                    score: Math.round(data.avgScore * 100) / 100,
                    confidence: Math.round(data.confidence * 100) / 100,
                    sampleSize: data.scores.length
                };
            }
        }

        // HEXACO 完整6维度
        for (const [dim, data] of Object.entries(this.personality.hexaco)) {
            if (data.avgScore !== undefined) {
                summary.hexaco[dim] = {
                    score: Math.round(data.avgScore * 100) / 100,
                    confidence: Math.round(data.confidence * 100) / 100,
                    sampleSize: data.scores.length
                };
            }
        }

        // 依恋风格
        if (this.personality.attachment && this.personality.attachment.primaryStyle) {
            summary.attachment = {
                primaryStyle: this.personality.attachment.primaryStyle,
                scores: this.personality.attachment.scores,
                confidence: this.personality.attachment.confidence
            };
        }

        // 应对风格
        if (this.personality.coping && this.personality.coping.modes) {
            const modes = Object.entries(this.personality.coping.modes);
            if (modes.length > 0) {
                modes.sort((a, b) => b[1] - a[1]);
                summary.copingStyle = modes[0][0];
            }
        }

        // 心理灵活性
        if (this.personality.flexibility && this.personality.flexibility.overall) {
            summary.flexibility = {
                overall: this.personality.flexibility.overall,
                openness: this.personality.flexibility.openness,
                awareness: this.personality.flexibility.awareness,
                valuesAction: this.personality.flexibility.valuesAction
            };
        }

        return summary;
    }

    calculateDefaultConfidence(scoreData) {
        let confidence = 0.5;

        if (scoreData.evidence && scoreData.evidence.length > 10) {
            confidence += 0.2;
        }

        const dimensions = ['ocean', 'hexaco', 'emotion', 'flexibility', 'coping'];
        const presentDims = dimensions.filter(d => scoreData[d]).length;
        confidence += presentDims * 0.05;

        if (scoreData.context) confidence += 0.1;

        return Math.min(0.95, Math.max(0.1, confidence));
    }

    async updateConfidenceReport() {
        try {
            const recentScores = await this.readRecentScores(50);
            if (recentScores.length === 0) return;

            const byDimension = {
                ocean: [],
                hexaco: [],
                emotion: [],
                flexibility: [],
                coping: []
            };

            recentScores.forEach(score => {
                Object.keys(byDimension).forEach(dim => {
                    if (score[dim] && score.confidence) {
                        byDimension[dim].push(score.confidence);
                    }
                });
            });

            this.confidenceReport.recommendations = [];

            Object.keys(byDimension).forEach(dim => {
                const confidences = byDimension[dim];
                if (confidences.length > 0) {
                    const avg = confidences.reduce((a, b) => a + b, 0) / confidences.length;
                    this.confidenceReport.dimensions[dim].overall = avg;

                    if (avg < CONFIG.confidenceThresholds.medium) {
                        this.confidenceReport.recommendations.push({
                            dimension: dim,
                            level: 'low',
                            suggestion: `需要更多${dim}维度的数据，建议在对话中自然引导相关话题`
                        });
                    }
                }
            });

            this.confidenceReport.lastUpdated = new Date().toISOString();
            await fs.mkdir(this.userDir, { recursive: true });
            await fs.writeFile(this.confidenceFile, JSON.stringify(this.confidenceReport, null, 2));
        } catch (error) {
            console.error('Failed to update confidence report:', error);
        }
    }

    async analyzeFollowUpNeeds(scoreData) {
        try {
            const emotion = scoreData.emotion?.primary;
            const intensity = scoreData.emotion?.intensity || 0;
            const content = scoreData.content || '';
            const timestamp = scoreData.timestamp;
            const confidence = scoreData.confidence || 0.5;

            if (confidence < CONFIG.confidenceThresholds.medium) return;

            await this.extractConcerns(content, timestamp, emotion, intensity);

            let needsFollowUp = false;
            let followUpType = null;
            let scheduledTime = null;

            if (confidence > 0.6 && (emotion === 'sadness' || emotion === 'anger') && intensity > 0.6) {
                needsFollowUp = true;
                followUpType = 'care-check';

                const tomorrow = new Date(timestamp);
                tomorrow.setDate(tomorrow.getDate() + 1);
                tomorrow.setHours(9, 30, 0, 0);
                scheduledTime = tomorrow.toISOString();
            }

            if (content.match(/压力|累|烦|焦虑|担心/)) {
                needsFollowUp = true;
                followUpType = 'stress-check';

                const later = new Date(timestamp);
                later.setHours(later.getHours() + 4);
                scheduledTime = later.toISOString();
            }

            const hour = new Date(timestamp).getHours();
            if ((emotion === 'sadness' || emotion === 'fear') && (hour > 22 || hour < 5)) {
                needsFollowUp = true;
                followUpType = 'morning-check';

                const tomorrow = new Date(timestamp);
                tomorrow.setDate(tomorrow.getDate() + 1);
                tomorrow.setHours(8, 30, 0, 0);
                scheduledTime = tomorrow.toISOString();
            }

            if (needsFollowUp) {
                await this.addActiveMemory({
                    triggerEvent: {
                        timestamp,
                        emotion,
                        intensity,
                        content: content.substring(0, 100),
                        context: scoreData.context || {}
                    },
                    followUp: {
                        status: 'pending',
                        scheduledTime,
                        priority: intensity * confidence,
                        type: followUpType,
                        suggestedApproach: this.getSuggestedApproach(emotion, followUpType)
                    },
                    confidence,
                    expiryTime: this.calculateExpiry(timestamp, followUpType)
                });
            }
        } catch (error) {
            console.error('Failed to analyze follow-up needs:', error);
        }
    }

    async getCurrentState() {
        this.updateLastAccessed();
        try {
            const recentScores = await this.readRecentScores(CONFIG.memoryWindows.recentScores);
            const confidence = await this.loadConfidenceReport();
            const weightedState = this.aggregateWithConfidence(recentScores);
            const pendingFollowUps = await this.getPendingFollowUps();
            const todayRhythm = await this.loadTodayRhythm();
            
            // 加载亲密度
            await this.loadIntimacy();
            
            // 加载人格画像
            await this.loadPersonality();
            
            // 加载互动偏好
            await this.loadInteractionPreference();
            
            // 加载情绪触发场景
            await this.loadEmotionTriggers();
            
            // 分析最近情绪复杂度（短期层）
            const recentEmotions = recentScores
                .filter(s => s.emotion)
                .slice(-5)
                .map(s => this.analyzeEmotionComplexity(s));
            
            // 生成回复风格建议（基于亲密度、人格、互动偏好）
            const responseStyle = this.generateResponseStyleV3(
                this.getPersonalitySummary(),
                recentEmotions[recentEmotions.length - 1] || null,
                this.intimacy,
                this.interactionPreference
            );

            return {
                userId: this.userId,
                lastUpdated: new Date().toISOString(),

                // === 即时层：当前情绪 ===
                currentEmotion: recentEmotions[recentEmotions.length - 1] || null,
                emotionTrend: this.analyzeEmotionTrend(recentEmotions),

                // === 短期层：最近状态 ===
                shortTerm: {
                    recentEmotions: recentEmotions.slice(-3),
                    recentConcerns: this.tracker.recentConcerns.slice(0, 3).map(c => ({
                        topic: c.topic,
                        lastMentioned: this.formatTime(c.lastMentioned),
                        emotionalImpact: c.emotionalImpact,
                        mentionCount: c.mentionCount
                    }))
                },

                // === 长期层：人格画像 ===
                personality: this.getPersonalitySummary(),

                // === 依恋风格 ===
                attachment: this.personality.attachment || null,

                // === 互动偏好 ===
                interactionPreference: this.interactionPreference,

                // === 情绪触发场景 ===
                emotionTriggers: this.emotionTriggers.slice(0, 5),

                // === 亲密度系统（影响回复风格） ===
                intimacy: {
                    level: Math.round(this.intimacy.level * 10) / 10,
                    stage: this.intimacy.stage,
                    stageLabel: CONFIG.intimacySystem.levels[this.intimacy.stage]?.label || '未知',
                    totalInteractions: this.intimacy.totalInteractions,
                    consecutiveDays: this.intimacy.consecutiveDays
                },

                // === 回复风格建议 ===
                responseStyle: responseStyle,

                // === 待办关怀 ===
                activeCare: {
                    pendingFollowUps: pendingFollowUps.filter(f => f.confidence > 0.4).map(f => ({
                        id: f.id,
                        type: f.followUp.type,
                        priority: f.followUp.priority,
                        timeInfo: this.getTimeElapsedText(f.triggerEvent.timestamp),
                        scheduledIn: f.followUp.minutesUntil ? `${f.followUp.minutesUntil}分钟后` : '现在',
                        triggerEvent: {
                            time: this.formatTime(f.triggerEvent.timestamp),
                            emotion: f.triggerEvent.emotion,
                            content: f.triggerEvent.content
                        },
                        suggestedApproach: f.followUp.suggestedApproach
                    }))
                },

                // === 原始数据（兼容） ===
                currentState: weightedState,
                confidence: {
                    overall: confidence.dimensions.ocean.overall || 0.5,
                    byDimension: {
                        ocean: confidence.dimensions.ocean.overall,
                        hexaco: confidence.dimensions.hexaco.overall,
                        emotion: confidence.dimensions.emotion?.overall || 0.5,
                        flexibility: confidence.dimensions.flexibility.overall,
                        coping: confidence.dimensions.stressCoping.overall
                    },
                    recommendations: confidence.recommendations.slice(0, 3)
                },
                todayRhythm: todayRhythm,
                strategyGuide: this.generateStrategyGuide(weightedState, confidence)
            };
        } catch (error) {
            console.error('Failed to get current state:', error);
            return {
                userId: this.userId,
                lastUpdated: new Date().toISOString(),
                error: error.message,
                currentState: {},
                confidence: { overall: 0.5, byDimension: {}, recommendations: [] },
                activeCare: { pendingFollowUps: [], recentConcerns: [] },
                todayRhythm: null,
                strategyGuide: { tone: {}, approach: {}, cautions: [] }
            };
        }
    }

    aggregateWithConfidence(scores) {
        if (scores.length === 0) return {};

        const result = {
            ocean: {},
            hexaco: {},
            emotion: {},
            flexibility: {},
            coping: {}
        };

        const dims = {
            ocean: ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'],
            hexaco: ['honestyHumility', 'emotionality', 'extraversion', 'agreeableness', 'conscientiousness', 'openness']
        };

        Object.keys(dims).forEach(category => {
            dims[category].forEach(dim => {
                const values = scores
                    .map(s => {
                        const dimData = s[category]?.[dim];
                        // 支持两种格式: {score, confidence} 或直接数值
                        if (dimData === undefined) return null;
                        const value = typeof dimData === 'object' ? dimData.score : dimData;
                        const conf = typeof dimData === 'object' ? (dimData.confidence || 0.5) : (s.confidence || 0.5);
                        return { value, confidence: conf };
                    })
                    .filter(v => v !== null && v.value !== undefined);

                if (values.length > 0) {
                    const totalWeight = values.reduce((sum, v) => sum + v.confidence, 0);
                    const weightedSum = values.reduce((sum, v) => sum + v.value * v.confidence, 0);
                    result[category][dim] = {
                        score: totalWeight > 0 ? weightedSum / totalWeight : 0.5,
                        confidence: totalWeight / values.length
                    };
                }
            });
        });

        const recentEmotions = scores
            .filter(s => s.emotion)
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, 3);

        if (recentEmotions.length > 0) {
            result.emotion = recentEmotions[0].emotion;
        }

        return result;
    }

    // 新增：分析情绪趋势
    analyzeEmotionTrend(emotions) {
        if (emotions.length < 2) return 'stable';
        
        const intensities = emotions.map(e => e.intensity || 0.5);
        const recent = intensities.slice(-3);
        
        // 计算趋势
        let rising = 0, falling = 0;
        for (let i = 1; i < recent.length; i++) {
            if (recent[i] > recent[i-1]) rising++;
            else if (recent[i] < recent[i-1]) falling++;
        }
        
        if (rising > falling) return 'rising';
        if (falling > rising) return 'falling';
        return 'stable';
    }

    generateStrategyGuide(state, confidence) {
        const guide = {
            tone: {},
            approach: {},
            cautions: []
        };

        const currentEmotion = state?.emotion?.primary;
        if (currentEmotion === 'anger') {
            guide.tone = { energy: 'low', warmth: 'high', assertiveness: 'low' };
            guide.approach = { style: 'gentle', patience: 'high' };
        } else if (currentEmotion === 'sadness') {
            guide.tone = { energy: 'low', warmth: 'high', assertiveness: 'low' };
            guide.approach = { style: 'comforting', patience: 'very-high' };
        } else if (currentEmotion === 'joy') {
            guide.tone = { energy: 'high', warmth: 'high', assertiveness: 'medium' };
            guide.approach = { style: 'celebratory' };
        }

        const overallConf = confidence?.overall || 0.5;
        if (overallConf < CONFIG.confidenceThresholds.medium) {
            guide.cautions.push('用户画像置信度较低，建议多用询问确认');
        }

        const byDimension = confidence?.byDimension || {};
        Object.entries(byDimension).forEach(([dim, conf]) => {
            if (conf && conf < CONFIG.confidenceThresholds.medium) {
                guide.cautions.push(`${dim}维度数据不足，谨慎推断`);
            }
        });

        return guide;
    }

    async getDailyRhythmData() {
        this.updateLastAccessed();
        try {
            const today = new Date().toISOString().split('T')[0];
            const allScores = await this.readAllScores();

            const todayScores = allScores.filter(s =>
                s.timestamp.startsWith(today)
            );

            if (todayScores.length === 0) {
                return { date: today, hasData: false };
            }

            const hourlyData = Array(24).fill(null).map(() => []);
            todayScores.forEach(score => {
                const hour = new Date(score.timestamp).getHours();
                if (hour >= 0 && hour < 24) {
                    hourlyData[hour].push({
                        ...score,
                        hour
                    });
                }
            });

            return {
                date: today,
                hasData: true,
                hourlyData: hourlyData.map((scores, hour) => ({
                    hour,
                    count: scores.length,
                    scores,
                    averageConfidence: scores.reduce((sum, s) => sum + (s.confidence || 0.5), 0) / (scores.length || 1)
                })),
                allScores: todayScores
            };
        } catch (error) {
            console.error('Failed to get daily rhythm data:', error);
            const today = new Date().toISOString().split('T')[0];
            return { date: today, hasData: false, error: error.message };
        }
    }

    async saveDailyRhythm(rhythmAnalysis) {
        this.updateLastAccessed();
        try {
            const enriched = {
                ...rhythmAnalysis,
                confidence: rhythmAnalysis.confidence || 0.7,
                savedAt: new Date().toISOString()
            };

            let history = [];
            try {
                const data = await fs.readFile(this.rhythmFile, 'utf-8');
                history = JSON.parse(data);
            } catch {
                history = [];
            }

            history.push(enriched);
            if (history.length > 30) {
                history = history.slice(-30);
            }

            await fs.mkdir(this.userDir, { recursive: true });
            await fs.writeFile(this.rhythmFile, JSON.stringify(history, null, 2));
            await this.updateCurrentState();
            return { success: true };
        } catch (error) {
            console.error('Failed to save daily rhythm:', error);
            return { success: false, error: error.message };
        }
    }

    async getConfidenceReport() {
        this.updateLastAccessed();
        try {
            await this.updateConfidenceReport();
            return this.confidenceReport;
        } catch (error) {
            console.error('Failed to get confidence report:', error);
            return this.confidenceReport;
        }
    }

    async readRecentScores(limit = 20) {
        try {
            const content = await fs.readFile(this.scoresFile, 'utf-8');
            const lines = content.trim().split('\n').filter(l => l);
            return lines.slice(-limit).map(l => JSON.parse(l));
        } catch {
            return [];
        }
    }

    async readAllScores() {
        try {
            const content = await fs.readFile(this.scoresFile, 'utf-8');
            return content.trim().split('\n').filter(l => l).map(l => JSON.parse(l));
        } catch {
            return [];
        }
    }

    async loadConfidenceReport() {
        try {
            const data = await fs.readFile(this.confidenceFile, 'utf-8');
            return JSON.parse(data);
        } catch {
            return this.confidenceReport;
        }
    }

    async loadTodayRhythm() {
        try {
            const data = await fs.readFile(this.rhythmFile, 'utf-8');
            const history = JSON.parse(data);
            const today = new Date().toISOString().split('T')[0];
            return history.find(r => r.date === today) || null;
        } catch {
            return null;
        }
    }

    async loadTracker() {
        try {
            const data = await fs.readFile(this.trackerFile, 'utf-8');
            this.tracker = JSON.parse(data);
        } catch {}
    }

    async saveTracker() {
        await fs.writeFile(this.trackerFile, JSON.stringify(this.tracker, null, 2));
    }

    async updateCurrentState() {
        const state = await this.getCurrentState();
        await fs.writeFile(this.stateFile, JSON.stringify(state, null, 2));
    }

    async extractConcerns(content, timestamp, emotion, intensity) {
        try {
            const concernKeywords = ['项目', '工作', '考试', '健康', '关系', '钱', '时间', '家人', '朋友'];

            concernKeywords.forEach(keyword => {
                if (content.includes(keyword)) {
                    const existing = this.tracker.recentConcerns.find(c => c.topic === keyword);

                    if (existing) {
                        existing.lastMentioned = timestamp;
                        existing.mentionCount++;
                        existing.emotionalImpact = (existing.emotionalImpact + intensity) / 2;
                    } else {
                        this.tracker.recentConcerns.push({
                            topic: keyword,
                            firstMentioned: timestamp,
                            lastMentioned: timestamp,
                            mentionCount: 1,
                            emotionalImpact: intensity,
                            resolved: false
                        });
                    }
                }
            });

            if (this.tracker.recentConcerns.length > 20) {
                this.tracker.recentConcerns = this.tracker.recentConcerns
                    .sort((a, b) => new Date(b.lastMentioned) - new Date(a.lastMentioned))
                    .slice(0, 20);
            }

            await this.saveTracker();
        } catch (error) {
            console.error('Failed to extract concerns:', error);
        }
    }

    async addActiveMemory(memory) {
        try {
            memory.id = `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            this.tracker.activeMemories.push(memory);

            this.tracker.activeMemories.sort((a, b) => b.followUp.priority - a.followUp.priority);
            if (this.tracker.activeMemories.length > this.tracker.careSchedule.maxActiveMemories) {
                this.tracker.activeMemories = this.tracker.activeMemories.slice(0, this.tracker.careSchedule.maxActiveMemories);
            }

            await this.saveTracker();
        } catch (error) {
            console.error('Failed to add active memory:', error);
        }
    }

    async getPendingFollowUps() {
        try {
            const now = new Date();
            const pending = [];

            for (const memory of this.tracker.activeMemories) {
                if (memory.followUp.status !== 'pending') continue;

                const scheduled = new Date(memory.followUp.scheduledTime);
                if (scheduled <= now) {
                    pending.push(memory);
                } else {
                    const minutesUntil = Math.round((scheduled - now) / (1000 * 60));
                    if (minutesUntil <= 30) {
                        pending.push({
                            ...memory,
                            followUp: {
                                ...memory.followUp,
                                status: 'upcoming',
                                minutesUntil
                            }
                        });
                    }
                }
            }

            return pending;
        } catch (error) {
            console.error('Failed to get pending follow-ups:', error);
            return [];
        }
    }

    async markFollowUpDone(memoryId, resolution) {
        this.updateLastAccessed();
        try {
            const memory = this.tracker.activeMemories.find(m => m.id === memoryId);
            if (memory) {
                memory.followUp.status = 'completed';
                memory.followUp.resolution = resolution;
                memory.followUp.completedAt = new Date().toISOString();

                if (resolution === 'resolved' && memory.triggerEvent.topic) {
                    const concern = this.tracker.recentConcerns.find(c => c.topic === memory.triggerEvent.topic);
                    if (concern) concern.resolved = true;
                }

                await this.saveTracker();
                return { success: true };
            } else {
                return { success: false, error: 'Memory not found' };
            }
        } catch (error) {
            console.error('Failed to mark follow-up done:', error);
            return { success: false, error: error.message };
        }
    }

    getSuggestedApproach(emotion, type) {
        const approaches = {
            'sadness': {
                'care-check': '温柔询问，不追问细节，提供陪伴感',
                'morning-check': '简单问候，表示记得昨晚的事，但不给压力',
                'stress-check': '认可情绪，问是否需要帮忙分担'
            },
            'anger': {
                'care-check': '先让情绪平复，再问是否需要帮忙解决问题',
                'stress-check': '认可压力，问是否需要帮忙梳理'
            },
            'fear': {
                'care-check': '给予安全感，问最担心什么，一起想办法',
                'morning-check': '温柔问候，传递安全感'
            }
        };

        return approaches[emotion]?.[type] || '自然问候，表示关心';
    }

    calculateExpiry(timestamp, type) {
        const date = new Date(timestamp);
        const hours = {
            'care-check': 48,
            'stress-check': 24,
            'morning-check': 36
        }[type] || 48;

        date.setHours(date.getHours() + hours);
        return date.toISOString();
    }

    getTimeElapsedText(timestamp) {
        const minutes = Math.floor((new Date() - new Date(timestamp)) / (1000 * 60));
        if (minutes < 60) return `${minutes}分钟前`;
        if (minutes < 1440) return `${Math.floor(minutes / 60)}小时前`;
        return `${Math.floor(minutes / 1440)}天前`;
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const hour = date.getHours();
        const period = hour < 12 ? '早上' : hour < 18 ? '下午' : '晚上';
        return `${period}${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
    }
}

const engines = new Map();

// 内存管理：定期清理过期的引擎实例
function cleanupExpiredEngines() {
    const now = Date.now();
    const expirationTime = 24 * 60 * 60 * 1000; // 24小时过期
    
    for (const [userId, engine] of engines.entries()) {
        if (now - engine.lastAccessed > expirationTime) {
            engines.delete(userId);
            console.log(`Cleaned up expired engine for user: ${userId}`);
        }
    }
}

// 启动定期清理
setInterval(cleanupExpiredEngines, CONFIG.cleanupInterval);

export default async function run(action, params, context) {
    const userId = context?.userId || 'default';

    if (!engines.has(userId)) {
        const engine = new HerHugEngine(userId);
        await engine.loadTracker();
        await engine.loadIntimacy();
        await engine.loadPersonality();
        
        // 新增：首次加载时，从用户偏好文件建立初始画像
        await engine.loadInitialProfile();
        
        engines.set(userId, engine);
    }

    const engine = engines.get(userId);

    switch (action) {
        case 'get-scoring-standards':
            return await engine.getScoringStandards();

        case 'save-score':
            return await engine.saveScore(params.scoreData);

        case 'get-current-state':
            return await engine.getCurrentState();

        case 'get-daily-rhythm-data':
            return await engine.getDailyRhythmData();

        case 'save-daily-rhythm':
            return await engine.saveDailyRhythm(params.rhythmAnalysis);

        case 'mark-followup-done':
            return await engine.markFollowUpDone(params.memoryId, params.resolution);

        case 'get-confidence-report':
            return await engine.getConfidenceReport();

        case 'get-response-style':
            const state = await engine.getCurrentState();
            return state.responseStyle;

        case 'get-intimacy':
            await engine.loadIntimacy();
            return {
                level: engine.intimacy.level,
                stage: engine.intimacy.stage,
                stageLabel: CONFIG.intimacySystem.levels[engine.intimacy.stage]?.label,
                totalInteractions: engine.intimacy.totalInteractions
            };

        case 'get-personality':
            await engine.loadPersonality();
            return engine.getPersonalitySummary();

        case 'get-interaction-preference':
            await engine.loadInteractionPreference();
            return engine.interactionPreference;

        case 'set-interaction-preference':
            return await engine.setInteractionPreference(params.preference);

        case 'get-emotion-triggers':
            await engine.loadEmotionTriggers();
            return engine.emotionTriggers;

        case 'update-emotion-trigger':
            return await engine.updateEmotionTrigger(
                params.emotion,
                params.trigger,
                params.intensity || 0.5,
                params.context || ''
            );

        case 'get-attachment':
            await engine.loadPersonality();
            return engine.personality.attachment || null;

        case 'evaluate-input':
            return engine.evaluateInputRichness(params.content, {});

        default:
            return { error: `Unknown action: ${action}` };
    }
}