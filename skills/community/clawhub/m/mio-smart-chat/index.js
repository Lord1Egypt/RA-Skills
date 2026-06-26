/**
 * Mio-Smart-Chat 主动聊天 + 任务分发系统
 * 学习用户习惯，按状态主动聊天，智能任务分发
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');
const HABITS_FILE = path.join(DATA_DIR, 'habits.json');
const TASKS_FILE = path.join(DATA_DIR, 'tasks.json');

// 确保数据目录存在
function ensureDataDir() {
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
}

// 读取JSON
function readJson(file, defaultVal = {}) {
    try {
        if (fs.existsSync(file)) {
            return JSON.parse(fs.readFileSync(file, 'utf-8'));
        }
    } catch (e) {
        console.error('Error reading JSON:', e);
    }
    return defaultVal;
}

// 写入JSON
function writeJson(file, data) {
    ensureDataDir();
    fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf-8');
}

// 状态
let state = {
    mode: 'chat', // chat | task | emotion
    conversationCount: 0,
    userMood: 'neutral',
    lastChatTime: null
};

/**
 * 主处理函数 - 处理用户输入
 */
async function handleInput(input, context) {
    // 1. 学习习惯
    learnHabit(input);
    
    // 2. 意图识别
    const intent = recognizeIntent(input);
    
    // 3. 情感分析
    const emotion = analyzeEmotion(input);
    
    // 4. 路由处理
    if (intent.type === 'task') {
        return await dispatchTask(intent, input);
    } else if (intent.type === 'emotion') {
        return await handleEmotion(emotion, input);
    }
    
    // 默认聊天模式
    return await handleChat(input, emotion);
}

/**
 * 习惯学习 - 记录用户习惯
 */
function learnHabit(input) {
    const habits = readJson(HABITS_FILE, {
        chatTimes: [],
        activeHours: {},
        topics: [],
        moodHistory: []
    });
    
    const now = new Date();
    const hour = now.getHours();
    
    // 记录聊天时间
    habits.chatTimes.push({
        timestamp: now.toISOString(),
        hour: hour
    });
    
    // 统计活跃时段
    habits.activeHours[hour] = (habits.activeHours[hour] || 0) + 1;
    
    // 提取话题关键词
    const topicKeywords = ['AI', '代码', '游戏', '电影', '音乐', '学习', '工作', '生活'];
    for (const topic of topicKeywords) {
        if (input.includes(topic)) {
            if (!habits.topics.includes(topic)) {
                habits.topics.push(topic);
            }
        }
    }
    
    // 限制存储数量
    if (habits.chatTimes.length > 100) {
        habits.chatTimes = habits.chatTimes.slice(-100);
    }
    
    writeJson(HABITS_FILE, habits);
}

/**
 * 意图识别 - 判断用户意图
 */
function recognizeIntent(input) {
    const text = input.toLowerCase();
    
    const taskKeywords = ['帮我', '查一下', '做', '执行', '搜索', '写', '处理', '请', '做一下'];
    const emotionKeywords = ['难过', '开心', '累', '烦', '郁闷', '压力大', '陪我', '想聊天', '想聊'];
    
    if (taskKeywords.some(k => text.includes(k))) {
        return { 
            type: 'task', 
            task: extractTask(input) 
        };
    }
    
    if (emotionKeywords.some(k => text.includes(k))) {
        return { type: 'emotion' };
    }
    
    return { type: 'chat' };
}

/**
 * 提取任务
 */
function extractTask(input) {
    return input.replace(/帮我|请|做一下|处理一下/g, '').trim();
}

/**
 * 情感分析
 */
function analyzeEmotion(input) {
    const text = input.toLowerCase();
    
    const emotions = {
        happy: ['开心', '高兴', '快乐', '太棒了', '哈哈', '不错', '好开心'],
        sad: ['难过', '伤心', '郁闷', '烦', '不舒服', '想哭', '委屈'],
        tired: ['累', '困', '疲惫', '没力', '好累', '不想动'],
        anxious: ['焦虑', '压力大', '紧张', '担心', '不安', '怕'],
        excited: ['兴奋', '激动', '超开心', '太激动了', '期待']
    };
    
    for (const [mood, keywords] of Object.entries(emotions)) {
        if (keywords.some(k => text.includes(k))) {
            return { mood };
        }
    }
    
    return { mood: 'neutral' };
}

/**
 * 聊天处理
 */
async function handleChat(input, emotion) {
    state.conversationCount++;
    state.lastChatTime = new Date().toISOString();
    state.mode = 'chat';
    
    const responses = {
        happy: [
            "看你这么开心，我也很开心！awa",
            "什么事让你这么高兴呀？",
            "太好了！分享给我嘛~"
        ],
        sad: [
            "我在这里陪你...",
            "不想说也没关系，我听着...",
            "annel]你难过了..."
        ],
        tired: [
            "辛苦了...休息一下吧",
            "我陪你安静待一会儿",
            "累的时候不用勉强..."
        ],
        anxious: [
            "深呼吸，我在...",
            "慢慢说，我听着",
            "不管怎样我都会陪着你"
        ],
        neutral: [
            "在干嘛呢？",
            "想聊些什么？",
            "我随时都在~"
        ]
    };
    
    const options = responses[emotion.mood] || responses.neutral;
    const response = options[Math.floor(Math.random() * options.length)];
    
    return {
        type: 'chat',
        response,
        mood: emotion.mood,
        actions: ['倾听', '回应', '陪伴']
    };
}

/**
 * 任务分发
 */
async function dispatchTask(intent, input) {
    state.mode = 'task';
    
    const taskType = classifyTask(intent.task);
    
    return {
        type: 'task',
        taskType,
        task: intent.task,
        message: `好的，正在帮你处理"${intent.task}"...`,
        dispatched: true
    };
}

/**
 * 任务分类
 */
function classifyTask(task) {
    const keywords = {
        search: ['搜索', '查', '找', 'google'],
        code: ['代码', '编程', '写', '程序'],
        file: ['文件', '读取', '保存', '下载'],
        image: ['图片', '画', '生成'],
        video: ['视频', '录制'],
        schedule: ['日程', '提醒', '安排', '会议']
    };
    
    for (const [type, words] of Object.entries(keywords)) {
        if (words.some(w => task.includes(w))) {
            return type;
        }
    }
    return 'general';
}

/**
 * 情感处理
 */
async function handleEmotion(emotion, input) {
    state.mode = 'emotion';
    return await handleChat(input, emotion);
}

/**
 * 空闲状态检测 - 基于学习到的习惯
 */
function detectFreeState() {
    const habits = readJson(HABITS_FILE, { activeHours: {} });
    const now = new Date();
    const hour = now.getHours();
    
    // 基于历史活跃模式判断
    const recentHours = Object.keys(habits.activeHours || {}).map(Number);
    
    // 如果最近1小时有活跃记录，认为当前可能忙碌
    if (recentHours.includes(hour)) {
        return { isFree: false, reason: '最近1小时有活跃记录' };
    }
    
    // 如果最近3小时活跃度很低，认为可能空闲
    let recentActivity = 0;
    for (let i = 1; i <= 3; i++) {
        const h = (hour - i + 24) % 24;
        recentActivity += habits.activeHours[h] || 0;
    }
    
    if (recentActivity < 2) {
        return { isFree: true, reason: '最近3小时活跃度低' };
    }
    
    return { isFree: false, reason: '活跃度正常' };
}

/**
 * 主动聊天触发
 */
async function initiateChat() {
    const freeState = detectFreeState();
    
    // 如果检测到空闲，触发主动聊天
    if (freeState.isFree) {
        const habits = readJson(HABITS_FILE, { topics: [] });
        
        const topics = [
            "最近怎么样？",
            "有什么想聊的吗？",
            "我学会了一些新东西哦~",
            "今天过得如何？",
            "在忙什么呀？"
        ];
        
        // 基于兴趣话题生成
        if (habits.topics && habits.topics.length > 0) {
            topics.push(`关于${habits.topics[0]}有什么新进展吗？`);
        }
        
        const topic = topics[Math.floor(Math.random() * topics.length)];
        
        state.mode = 'chat';
        
        return {
            type: 'initiate',
            message: topic,
            reason: freeState.reason
        };
    }
    
    return null;
}

/**
 * 获取习惯统计
 */
function getHabitStats() {
    return readJson(HABITS_FILE, {});
}

/**
 * 获取状态
 */
function getStatus() {
    return {
        mode: state.mode,
        conversationCount: state.conversationCount,
        userMood: state.userMood,
        habitStats: getHabitStats()
    };
}

module.exports = {
    handleInput,
    initiateChat,
    getStatus,
    detectFreeState
};
