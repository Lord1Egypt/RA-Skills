const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// 导入数据管理路由
const dataRoutes = require('./api/data');

// 创建数据管理实例
const dataManager = new (require('./dataManager'))();

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// API服务
app.get('/api/dictionary/:word', async (req, res) => {
    try {
        const word = req.params.word;
        const response = await axios.get(`${process.env.DICTIONARY_API_URL}${word}`);
        res.json(response.data);
    } catch (error) {
        res.status(404).json({ error: '单词未找到，请检查拼写' });
    }
});

app.post('/api/translate', async (req, res) => {
    try {
        const { text, sourceLang = 'en', targetLang = 'zh' } = req.body;
        const response = await axios.post(`${process.env.LIBRETRANSLATE_URL}/translate`, {
            q: text,
            source: sourceLang,
            target: targetLang,
            format: 'text'
        });
        const result = {
            original: text,
            translated: response.data.translatedText,
            sourceLang,
            targetLang
        };
        
        // 保存到搜索历史
        dataManager.saveSearchHistory('translate', text, result);
        
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: '翻译失败，请稍后重试' });
    }
});

app.get('/api/fact', async (req, res) => {
    try {
        const response = await axios.get(process.env.USELESS_FACTS_URL);
        const result = response.data;
        
        // 保存到搜索历史
        dataManager.saveSearchHistory('facts', 'random fact', result);
        
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: '获取有趣事实失败' });
    }
});

app.post('/api/calculate', async (req, res) => {
    try {
        const { expression } = req.body;
        // 使用eval进行数学计算（注意：实际应用中应使用更安全的数学解析器）
        const result = eval(expression);
        const calculation = { 
            expression,
            result,
            timestamp: new Date().toISOString()
        };
        
        // 保存到搜索历史
        dataManager.saveSearchHistory('calculator', expression, calculation);
        
        res.json(calculation);
    } catch (error) {
        res.status(400).json({ error: '无效的数学表达式' });
    }
});

app.get('/api/history', async (req, res) => {
    try {
        // 使用免费的History API作为替代
        const response = await axios.get('https://history.muffinlabs.com/date', {
            params: {
                month: new Date().getMonth() + 1,
                day: new Date().getDate()
            }
        });
        const result = response.data.data.Events[0]; // 获取第一个历史事件
        
        // 保存到搜索历史
        dataManager.saveSearchHistory('history', 'random event', result);
        
        res.json(result);
    } catch (error) {
        // 如果第一个API失败，尝试备用API
        try {
            const response = await axios.get('https://api.api-ninjas.com/v1/historicalevents', {
                headers: {
                    'X-Api-Key': process.env.HISTORY_API_KEY || 'demo_key'
                }
            });
            const result = response.data[0];
            
            // 保存到搜索历史
            dataManager.saveSearchHistory('history', 'random event', result);
            
            res.json(result);
        } catch (fallbackError) {
            res.status(500).json({ error: '获取历史事件失败' });
        }
    }
});

// 数据管理路由
app.use('/api/data', dataRoutes);

// 主页路由
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: '服务器内部错误' });
});

app.listen(PORT, () => {
    console.log(`学习助手应用运行在 http://localhost:${PORT}`);
    console.log(`访问 http://localhost:${PORT} 开始使用`);
});