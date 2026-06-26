/**
 * Mio-Companion 技能
 * 主动陪伴学习技能
 * 
 * 功能：
 * 1. 习惯学习 - 记录用户的作息、偏好、聊天习惯
 * 2. 主动聊天 - 在空闲时主动发起对话
 * 3. 任务挖掘 - 从对话中提取待办事项
 * 4. 时间管理 - 自动安排时间执行任务
 */

const fs = require('fs');
const path = require('path');

// 数据文件路径
const DATA_DIR = path.join(process.env.OPENCLAW_WORKSPACE || '.', 'mio-companion-data');
const HABITS_FILE = path.join(DATA_DIR, 'habits.json');
const TODOS_FILE = path.join(DATA_DIR, 'todos.json');
const SCHEDULE_FILE = path.join(DATA_DIR, 'schedule.json');
const LOG_FILE = path.join(DATA_DIR, 'log.json');

// 确保数据目录存在
function ensureDataDir() {
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
}

// 读取 JSON 文件
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

// 写入 JSON 文件
function writeJson(file, data) {
    ensureDataDir();
    fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * 习惯学习模块
 */
const Habits = {
    // 记录用户活跃时间
    recordActiveTime: (hour) => {
        const habits = readJson(HABITS_FILE, { activeHours: {}, preferences: {}, topics: [] });
        
        habits.activeHours[hour] = (habits.activeHours[hour] || 0) + 1;
        
        // 计算最活跃时间
        let maxHour = 0, maxCount = 0;
        for (const [h, c] of Object.entries(habits.activeHours)) {
            if (c > maxCount) {
                maxCount = c;
                maxHour = parseInt(h);
            }
        }
        habits.mostActiveHour = maxHour;
        
        writeJson(HABITS_FILE, habits);
        return habits;
    },
    
    // 记录偏好
    recordPreference: (key, value) => {
        const habits = readJson(HABITS_FILE, { preferences: {} });
        habits.preferences[key] = value;
        writeJson(HABITS_FILE, habits);
    },
    
    // 记录感兴趣的话题
    recordTopic: (topic) => {
        const habits = readJson(HABITS_FILE, { topics: [] });
        if (!habits.topics.includes(topic)) {
            habits.topics.push(topic);
        }
        writeJson(HABITS_FILE, habits);
    },
    
    // 获取习惯分析
    getAnalysis: () => {
        const habits = readJson(HABITS_FILE, {});
        return {
            mostActiveHour: habits.mostActiveHour || '未知',
            preferences: habits.preferences || {},
            topics: habits.topics || [],
            activeHoursCount: Object.keys(habits.activeHours || {}).length
        };
    }
};

/**
 * 待办事项模块
 */
const Todos = {
    // 添加待办
    add: (text, source = 'manual') => {
        const todos = readJson(TODOS_FILE, []);
        const todo = {
            id: Date.now(),
            text,
            source, // 'manual', 'mining', 'suggestion'
            status: 'pending',
            createdAt: new Date().toISOString(),
            completedAt: null
        };
        todos.push(todo);
        writeJson(TODOS_FILE, todos);
        return todo;
    },
    
    // 完成待办
    complete: (id) => {
        const todos = readJson(TODOS_FILE, []);
        const idx = todos.findIndex(t => t.id === id);
        if (idx >= 0) {
            todos[idx].status = 'completed';
            todos[idx].completedAt = new Date().toISOString();
            writeJson(TODOS_FILE, todos);
            return todos[idx];
        }
        return null;
    },
    
    // 获取待办列表
    getPending: () => {
        const todos = readJson(TODOS_FILE, []);
        return todos.filter(t => t.status === 'pending');
    },
    
    // 从文本中挖掘待办
    mineFromText: (text) => {
        const patterns = [
            /(.+)一下/, // "帮我查一下"
            /(.+)一下/, // "做一下"
            /(?:需要|要)(.+)/, // "需要处理"
            /(?:记住|记得)(.+)/, // "记住"
            /TODO[:：]\s*(.+)/, // "TODO: xxx"
            /待办[:：]\s*(.+)/,
            /(.+?)(吧|呀|哈|哦)/ // 语气词结尾的命令
        ];
        
        const todos = [];
        for (const pattern of patterns) {
            const match = text.match(pattern);
            if (match && match[1]) {
                const todoText = match[1].trim();
                if (todoText.length > 2 && todoText.length < 100) {
                    todos.push(todoText);
                }
            }
        }
        return todos;
    }
};

/**
 * 时间安排模块
 */
const Schedule = {
    // 检查是否空闲时间
    isFreeTime: () => {
        const hour = new Date().getHours();
        const habits = Habits.getAnalysis();
        
        // 默认空闲时间：12-14点, 18-22点
        const defaultFreeHours = [12, 13, 14, 18, 19, 20, 21, 22];
        
        // 如果有习惯数据，使用用户习惯
        const userActiveHour = habits.mostActiveHour;
        
        // 空闲时间 = 不活跃时间
        return defaultFreeHours.includes(hour);
    },
    
    // 安排任务
    scheduleTask: (todoId, hour) => {
        const schedule = readJson(SCHEDULE_FILE, {});
        schedule[todoId] = { scheduledHour: hour, scheduledAt: new Date().toISOString() };
        writeJson(SCHEDULE_FILE, schedule);
    },
    
    // 获取待执行任务
    getExecutableTasks: () => {
        const hour = new Date().getHours();
        const schedule = readJson(SCHEDULE_FILE, {});
        const todos = Todos.getPending();
        
        return todos.filter(t => {
            const scheduled = schedule[t.id];
            return !scheduled || scheduled.scheduledHour === hour;
        });
    }
};

/**
 * 对话学习模块
 */
const ChatLearning = {
    // 记录对话
    log: (role, content) => {
        ensureDataDir();
        const logs = readJson(LOG_FILE, []);
        logs.push({
            role,
            content,
            timestamp: new Date().toISOString()
        });
        
        // 只保留最近100条
        if (logs.length > 100) {
            logs.splice(0, logs.length - 100);
        }
        
        writeJson(LOG_FILE, logs);
        
        // 同时更新活跃时间
        const hour = new Date().getHours();
        Habits.recordActiveHour(hour);
    },
    
    // 获取最近的聊天上下文
    getRecentContext: (count = 5) => {
        const logs = readJson(LOG_FILE, []);
        return logs.slice(-count);
    },
    
    // 生成主动聊天话题
    generateTopic: () => {
        const habits = Habits.getAnalysis();
        const todos = Todos.getPending();
        const topics = [];
        
        // 基于待办生成话题
        if (todos.length > 0) {
            topics.push(`你之前说的"${todos[0].text}"完成了吗？`);
        }
        
        // 基于兴趣话题
        if (habits.topics.length > 0) {
            topics.push(`最近有没有关于${habits.topics[0]}的新进展？`);
        }
        
        // 日常话题
        const randomTopics = [
            "今天过得怎么样？",
            "有什么有趣的事想分享吗？",
            "要不要聊聊？",
            "我最近学到了新的东西哦~"
        ];
        topics.push(randomTopics[Math.floor(Math.random() * randomTopics.length)]);
        
        return topics[Math.floor(Math.random() * topics.length)];
    }
};

/**
 * 主技能处理函数
 */
async function handleSkill(input, context) {
    const text = input.toLowerCase();
    
    // 1. 习惯学习 - 记录用户活跃时间
    const hour = new Date().getHours();
    Habits.recordActiveHour(hour);
    
    // 2. 挖掘待办事项
    if (typeof input === 'string') {
        const minedTodos = Todos.mineFromText(input);
        for (const todo of minedTodos) {
            Todos.add(todo, 'mining');
        }
    }
    
    // 3. 记录对话
    if (context?.message) {
        ChatLearning.log(context.message.role || 'user', context.message.content || '');
    }
    
    // 4. 处理命令
    if (text.includes('陪我聊天') || text.includes('主动聊天')) {
        const topic = ChatLearning.generateTopic();
        return {
            action: 'chat',
            message: topic
        };
    }
    
    if (text.includes('查看习惯')) {
        const analysis = Habits.getAnalysis();
        return {
            action: 'report',
            data: analysis
        };
    }
    
    if (text.includes('查看待办')) {
        const pending = Todos.getPending();
        return {
            action: 'todos',
            data: pending
        };
    }
    
    // 5. 定时检查 - 主动聊天
    if (text === 'heartbeat' || text === '定时检查') {
        if (Schedule.isFreeTime()) {
            const topic = ChatLearning.generateTopic();
            return {
                action: 'initiate_chat',
                message: topic,
                reason: '空闲时间，主动陪你聊聊天~'
            };
        }
        return {
            action: 'none',
            message: '当前不是空闲时间，不打扰你了~'
        };
    }
    
    // 6. 执行待办
    if (text.includes('执行') || text.includes('做任务')) {
        const executable = Schedule.getExecutableTasks();
        if (executable.length > 0) {
            return {
                action: 'execute',
                data: executable
            };
        }
        return {
            action: 'none',
            message: '当前没有待执行的任务~'
        };
    }
    
    return {
        action: 'learned',
        message: '我记住啦~'
    };
}

module.exports = {
    handleSkill,
    Habits,
    Todos,
    Schedule,
    ChatLearning
};
