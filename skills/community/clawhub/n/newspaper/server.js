const express = require('express');
const Handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');
const { generateImage, checkAvailability } = require('./comfy-client');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use('/output', express.static(path.join(__dirname, 'output')));

// 确保 output 目录存在
const outputDir = path.join(__dirname, 'output');
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// 读取模板
const templatePath = path.join(__dirname, 'templates', 'newspaper.html');
const templateSource = fs.readFileSync(templatePath, 'utf-8');
const template = Handlebars.compile(templateSource);

// 自定义 helper：分割段落
Handlebars.registerHelper('splitParagraphs', function(text) {
    if (!text) return [];
    return text.split(/\n+/).filter(p => p.trim().length > 0);
});

// 生成唯一 ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

// 获取当前日期
function getCurrentDate() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const weekday = weekdays[now.getDay()];
    return `${year}年${month}月${day}日 ${weekday}`;
}

// 验证输入
function validateInput(data) {
    const errors = [];
    
    if (!data.title || typeof data.title !== 'string' || data.title.trim().length === 0) {
        errors.push('缺少必需的 title 字段');
    }
    
    if (!data.articles || !Array.isArray(data.articles)) {
        errors.push('缺少必需的 articles 数组');
    } else if (data.articles.length === 0) {
        errors.push('articles 数组不能为空');
    } else {
        data.articles.forEach((article, index) => {
            if (!article.headline || typeof article.headline !== 'string') {
                errors.push(`文章 ${index + 1} 缺少 headline 字段`);
            }
            if (!article.body || typeof article.body !== 'string') {
                errors.push(`文章 ${index + 1} 缺少 body 字段`);
            }
        });
    }
    
    // 检查单图限制：最多只能有 1 个 imagePrompt
    const imagePromptCount = data.articles.filter(a => a.imagePrompt && a.imagePrompt.trim()).length;
    if (imagePromptCount > 1) {
        errors.push('最多只能有 1 个 article 包含 imagePrompt（单图限制）');
    }
    
    return errors;
}

// 查找包含 imagePrompt 的文章索引
function findImagePromptArticle(articles) {
    return articles.findIndex(a => a.imagePrompt && a.imagePrompt.trim());
}

// POST /render 端点
app.post('/render', async (req, res) => {
    console.log('[INFO] 收到渲染请求');
    console.log('[INFO] 标题:', req.body.title, '| 文章数量:', req.body.articles?.length || 0);
    
    // 验证输入
    const errors = validateInput(req.body);
    if (errors.length > 0) {
        console.log('[ERROR] 验证失败:', errors);
        return res.status(400).json({
            success: false,
            errors: errors
        });
    }
    
    try {
        // 生成唯一 ID
        const id = generateId();
        
        // 准备模板数据
        const templateData = {
            title: req.body.title,
            subtitle: req.body.subtitle || '',
            articles: req.body.articles,
            date: getCurrentDate(),
            year: new Date().getFullYear()
        };
        
        // 处理 ComfyUI 图片生成
        const comfyOptions = req.body.comfyOptions || {};
        const imageStatus = {
            generated: false,
            prompt: null,
            imageUrl: null,
            articleIndex: -1,
            error: null
        };
        
        // 检查是否启用 ComfyUI 且有 imagePrompt
        const imagePromptIndex = findImagePromptArticle(req.body.articles);
        
        if (comfyOptions.enabled !== false && imagePromptIndex >= 0) {
            const article = req.body.articles[imagePromptIndex];
            imageStatus.prompt = article.imagePrompt;
            imageStatus.articleIndex = imagePromptIndex;
            
            console.log('[INFO] 检测到 imagePrompt，准备调用 ComfyUI 生成图片');
            
            // 检查 ComfyUI 可用性
            const comfyAvailable = await checkAvailability();
            
            if (comfyAvailable) {
                try {
                    const generateOptions = {
                        timeout: comfyOptions.timeout || 120000,
                        interval: comfyOptions.interval || 2000,
                        width: comfyOptions.width || 1024,
                        height: comfyOptions.height || 1024
                    };
                    
                    const result = await generateImage(article.imagePrompt, generateOptions);
                    
                    imageStatus.generated = true;
                    imageStatus.imageUrl = result.imageUrl;
                    
                    // 更新文章中的图片信息
                    req.body.articles[imagePromptIndex].imageUrl = result.imageUrl;
                    templateData.articles[imagePromptIndex].imageUrl = result.imageUrl;
                    
                    console.log('[INFO] ComfyUI 图片生成成功:', result.imageUrl);
                    
                } catch (genError) {
                    console.error('[ERROR] ComfyUI 生成失败:', genError.message);
                    imageStatus.error = genError.message;
                    // 不抛出错误，继续渲染（使用占位图）
                }
            } else {
                console.warn('[WARN] ComfyUI 服务不可用，将使用占位图');
                imageStatus.error = 'ComfyUI 服务不可用';
            }
        }
        
        // 渲染 HTML
        const html = template(templateData);
        
        // 保存文件
        const outputPath = path.join(outputDir, `${id}.html`);
        fs.writeFileSync(outputPath, html, 'utf-8');
        
        // 生成 URL
        const url = `http://localhost:${PORT}/output/${id}.html`;
        
        console.log('[INFO] 渲染成功，文件已保存:', outputPath);
        console.log('[INFO] 访问 URL:', url);
        
        const response = {
            success: true,
            id: id,
            url: url
        };
        
        // 如果有图片生成状态，添加到响应中
        if (imageStatus.prompt) {
            response.imageStatus = imageStatus;
        }
        
        res.json(response);
        
    } catch (error) {
        console.log('[ERROR] 渲染失败:', error.message);
        res.status(500).json({
            success: false,
            error: '渲染失败：' + error.message
        });
    }
});

// GET /health 健康检查端点
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// GET / 欢迎页面
app.get('/', (req, res) => {
    res.json({
        name: 'AI Newspaper Rendering Service',
        version: '1.0.0',
        endpoints: {
            'POST /render': '渲染报纸 HTML',
            'GET /health': '健康检查',
            'GET /output/{id}.html': '查看渲染结果'
        }
    });
});

// 启动服务器
app.listen(PORT, () => {
    console.log('========================================');
    console.log('AI Newspaper Rendering Service 已启动');
    console.log(`服务地址：http://localhost:${PORT}`);
    console.log(`渲染输出目录：${outputDir}`);
    console.log('========================================');
    console.log('API 端点:');
    console.log(`  POST http://localhost:${PORT}/render`);
    console.log(`  GET  http://localhost:${PORT}/health`);
    console.log('========================================');
});