"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmbeddingModel = void 0;
// 本地 embedding 模型管理器
const ort = __importStar(require("onnxruntime-node"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
// 简单 tokenizer（避免额外依赖）
function tokenize(text) {
    const tokens = [];
    const words = text.toLowerCase().split(/\s+/);
    // 简单词表
    const vocab = {
        '[pad]': 0, '[unk]': 1, '[cls]': 2, '[sep]': 3, '[mask]': 4,
    };
    let vocabSize = 5;
    // 初始化常用词
    const commonWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'you', 'your', 'he', 'she', 'it', 'they', 'them',
        'like', 'love', 'hate', 'want', 'need', 'prefer', 'favorite', 'good', 'bad', 'great', 'nice', 'happy', 'sad',
        'python', 'java', 'javascript', 'go', 'rust', 'react', 'vue', 'node', 'programming', 'code', 'skill', 'expert',
        'fish', 'shrimp', 'meat', 'vegetable', 'rice', 'noodle', 'soup', 'fruit', 'dessert', 'pizza', 'hamburger',
        'chinese', 'english', 'american', 'japanese', 'korean', 'food', 'eat', 'drink', 'cook', 'restaurant',
        'work', 'job', 'career', 'company', 'team', 'boss', 'colleague', 'office', 'remote', 'freelance',
        'student', 'teacher', 'engineer', 'developer', 'designer', 'manager', 'director', 'ceo', 'founder',
        'learn', 'study', 'teach', 'practice', 'experience', 'year', 'month', 'week', 'day', 'hour', 'minute',
        'beijing', 'shanghai', 'shenzhen', 'hangzhou', 'guangzhou', 'chengdu', 'china', 'usa', 'uk', 'japan',
        'age', 'old', 'young', 'man', 'woman', 'boy', 'girl', 'name', 'call', 'from', 'live', 'stay', 'home',
        'think', 'know', 'believe', 'remember', 'forget', 'understand', 'learn', 'explain', 'tell', 'say', 'ask',
        'can', 'could', 'will', 'would', 'should', 'may', 'might', 'must', 'need', 'want', 'have', 'do', 'make',
        'very', 'really', 'quite', 'just', 'only', 'also', 'too', 'still', 'already', 'yet', 'never', 'always',
        'this', 'that', 'these', 'those', 'what', 'which', 'who', 'where', 'when', 'why', 'how', 'all', 'some',
        'not', 'no', 'yes', 'but', 'or', 'and', 'if', 'then', 'so', 'because', 'although', 'however'
    ];
    for (const w of commonWords) {
        vocab[w] = vocabSize++;
    }
    // Tokenize
    tokens.push(vocab['[cls]'] || 2);
    for (const word of words) {
        const cleanWord = word.replace(/[^a-z0-9]/g, '');
        if (cleanWord) {
            if (vocab[cleanWord] !== undefined) {
                tokens.push(vocab[cleanWord]);
            }
            else {
                tokens.push(vocab['[unk]'] || 1);
            }
        }
    }
    tokens.push(vocab['[sep]'] || 3);
    return tokens;
}
// 填充到固定长度
function pad(tokens, maxLength) {
    if (tokens.length >= maxLength) {
        return tokens.slice(0, maxLength);
    }
    const padding = new Array(maxLength - tokens.length).fill(0);
    return tokens.concat(padding);
}
// Debug mode toggle
const DEBUG_MODE = process.env.MEMORY_ENGINE_DEBUG === 'true' || process.env.MEMORY_ENGINE_DEBUG === '1';
const debugLog = (...args) => {
    if (DEBUG_MODE) {
        console.log('[embedding]', ...args);
    }
};
// 预定义标签
const TAG_DEFINITIONS = [
    // 偏好类
    { name: 'preference', keywords: ['我喜欢', '我爱', '我讨厌', '偏好', '喜欢', '讨厌'], category: 'preference' },
    { name: 'food', keywords: ['鱼', '虾', '肉', '菜', '饭', '面', '汤', '水果', '甜点', '披萨', '汉堡'], category: 'preference' },
    // 技能类
    { name: 'skill', keywords: ['擅长', '精通', '掌握', '会', '懂'], category: 'skill' },
    { name: 'programming', keywords: ['python', 'java', 'javascript', 'react', 'vue', 'node', 'go', 'rust', '代码', '编程'], category: 'skill' },
    // 经验类
    { name: 'experience', keywords: ['之前', '那次', '曾经', '以前', '经历过', '遇到过'], category: 'experience' },
    // 教训类
    { name: 'lesson', keywords: ['不要', '避免', '记住', '注意', '必须', '不能'], category: 'lesson' },
    // 事实类
    { name: 'age', keywords: ['岁', '年龄', '今年', 'born', '出生'], category: 'fact' },
    { name: 'identity', keywords: ['我是', '我在', '工作', '职业', '职位'], category: 'fact' },
    { name: 'location', keywords: ['住在', '来自', '在', '居住', '家乡'], category: 'fact' },
];
class EmbeddingModel {
    session = null;
    tagEmbeddings = new Map();
    modelPath;
    constructor(modelPath) {
        // 优先级：环境变量 > 配置 > 默认路径
        this.modelPath = modelPath ||
            process.env.MEMORY_ENGINE_MODEL_PATH ||
            path.join(__dirname, 'models', 'all-MiniLM-L6-v2.onnx');
    }
    // 加载模型
    async load() {
        try {
            // 检查模型文件是否存在
            if (!fs.existsSync(this.modelPath)) {
                debugLog('模型文件不存在，使用内存计算');
                // 使用内存计算模式，不加载模型
                return;
            }
            debugLog('加载模型:', this.modelPath);
            this.session = await ort.InferenceSession.create(this.modelPath);
            // 预计算标签 embedding
            await this.precomputeTagEmbeddings();
            debugLog('✅ 模型加载完成');
        }
        catch (error) {
            console.error('[embedding] ❌ 模型加载失败:', error);
            throw error;
        }
    }
    // 预计算标签 embedding
    async precomputeTagEmbeddings() {
        for (const tag of TAG_DEFINITIONS) {
            const text = `${tag.name} ${tag.keywords.join(' ')}`;
            const embedding = await this.getEmbedding(text);
            this.tagEmbeddings.set(tag.name, embedding);
        }
        debugLog('✅ 标签 embedding 预计算完成');
    }
    // 获取文本的 embedding
    async getEmbedding(text) {
        if (!this.session) {
            // 没有模型时使用简单哈希作为 embedding
            return this.simpleHashEmbedding(text);
        }
        try {
            // Tokenize 并填充到固定长度
            const seqLen = 384;
            const tokens = pad(tokenize(text), seqLen).map(x => BigInt(x));
            // 创建输入 tensor (batch_size=1, seq_len=384)
            const inputData = new BigInt64Array(tokens);
            const inputTensor = new ort.Tensor('int64', inputData, [1, seqLen]);
            // 创建 attention mask (全1)
            const attentionData = new BigInt64Array(seqLen).fill(1n);
            const attentionMask = new ort.Tensor('int64', attentionData, [1, seqLen]);
            // 创建 token_type_ids (全0)
            const tokenTypeData = new BigInt64Array(seqLen).fill(0n);
            const tokenTypeIds = new ort.Tensor('int64', tokenTypeData, [1, seqLen]);
            // 运行推理
            const results = await this.session.run({
                input_ids: inputTensor,
                attention_mask: attentionMask,
                token_type_ids: tokenTypeIds
            });
            // 提取 last_hidden_state (取[CLS]位置的输出作为句子embedding，即第一个token)
            const embeddingKey = 'last_hidden_state';
            const embedding = results[embeddingKey];
            if (!embedding) {
                console.error('[embedding] ONNX输出没有last_hidden_state，输出键:', Object.keys(results));
                return this.simpleHashEmbedding(text);
            }
            // 取第一个token的输出 (batch=0, position=0, hidden_dim=0:384)
            const dim = 384;
            const vector = [];
            let norm = 0;
            // 提取第一个token的所有维度
            const data = embedding.data;
            for (let i = 0; i < dim; i++) {
                const val = Number(data[i]);
                vector.push(val);
                norm += val * val;
            }
            norm = Math.sqrt(norm);
            // L2 归一化
            return vector.map(v => v / (norm || 1));
        }
        catch (error) {
            console.error('[embedding] ONNX推理失败，使用降级方案:', error);
            return this.simpleHashEmbedding(text);
        }
    }
    // 简单哈希 embedding（没有模型时的降级方案）
    simpleHashEmbedding(text) {
        const embedding = [];
        const normalized = text.toLowerCase();
        // 使用字符编码作为简单特征
        for (let i = 0; i < 50; i++) {
            const char = normalized[i];
            if (char) {
                embedding.push(char.charCodeAt(0) / 255);
            }
            else {
                embedding.push(0);
            }
        }
        return embedding;
    }
    // 计算余弦相似度
    cosineSimilarity(vec1, vec2) {
        if (vec1.length !== vec2.length)
            return 0;
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;
        for (let i = 0; i < vec1.length; i++) {
            dotProduct += vec1[i] * vec2[i];
            norm1 += vec1[i] * vec1[i];
            norm2 += vec2[i] * vec2[i];
        }
        if (norm1 === 0 || norm2 === 0)
            return 0;
        return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
    }
    // 从文本提取标签
    async extractTags(text) {
        const textEmbedding = await this.getEmbedding(text);
        const tags = [];
        const threshold = 0.1; // 降低阈值，让降级方案能工作
        for (const [tagName, tagEmbedding] of this.tagEmbeddings) {
            const similarity = this.cosineSimilarity(textEmbedding, tagEmbedding);
            if (similarity > threshold) {
                tags.push(tagName);
            }
        }
        // 如果没有匹配到任何标签，使用关键词匹配作为备用
        if (tags.length === 0) {
            return this.keywordMatch(text);
        }
        return tags;
    }
    // 关键词匹配备用方案
    keywordMatch(text) {
        const tags = [];
        const lowerText = text.toLowerCase();
        // 检查每个标签的关键词
        for (const tagDef of TAG_DEFINITIONS) {
            for (const keyword of tagDef.keywords) {
                if (lowerText.includes(keyword.toLowerCase())) {
                    tags.push(tagDef.name);
                    break;
                }
            }
        }
        return [...new Set(tags)];
    }
    // 获取所有标签定义
    getTagDefinitions() {
        return TAG_DEFINITIONS;
    }
}
exports.EmbeddingModel = EmbeddingModel;
//# sourceMappingURL=embedding.js.map