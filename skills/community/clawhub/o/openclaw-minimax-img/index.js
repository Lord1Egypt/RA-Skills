const axios = require('axios');

// Auto-prompt optimization function
function optimizePrompt(input) {
    // Remove conversational parts and extract core subject
    let prompt = input.trim();
    
    // Common Chinese patterns to remove
    const removePatterns = [
        /^帮我画/,
        /^画一个/,
        /^生成/,
        /^创建一个/,
        /^画/,
        /的图片?/,
        /的图片?/,
        /的画?/,
        /能不能/,
        /可以帮我/,
        /请帮我/,
        /我想/,
        /我要/,
        /给?我/,
    ];
    
    removePatterns.forEach(pattern => {
        prompt = prompt.replace(pattern, '');
    });
    
    // Add quality keywords
    const qualityKeywords = 'highly detailed, 4K, cinematic lighting, high quality';
    
    // If prompt is already in English, just add quality keywords
    if (/^[a-zA-Z0-9\s,]+$/.test(prompt)) {
        return prompt + ', ' + qualityKeywords;
    }
    
    // Map common Chinese subjects to English
    const subjectMap = {
        '橘猫': 'orange cat, fluffy, cute',
        '猫': 'cat, realistic photo',
        '狗': 'dog, realistic photo',
        '城市': 'cityscape, urban',
        '夜景': 'night scene, city lights',
        '霓虹灯': 'neon lights, glowing',
        '赛博朋克': 'cyberpunk, futuristic',
        '未来': 'futuristic, sci-fi',
        '高楼': 'tall skyscrapers, buildings',
        '科技': 'technology, futuristic',
        '山水': 'landscape, mountains and rivers',
        '海边': 'seaside, ocean, beach',
        '日出': 'sunrise, morning glow',
        '日落': 'sunset, golden hour',
        '花': 'flowers, blooming',
        '森林': 'forest, trees, nature',
        '雪': 'snow, snowy landscape',
        '雨': 'rainy, rain drops',
        '星空': 'starry night, stars',
        '人物': 'portrait, person',
        '女孩': 'beautiful girl, portrait',
        '男孩': 'handsome boy, portrait',
        '动漫': 'anime style, cartoon',
        '油画': 'oil painting style',
        '水彩': 'watercolor painting',
        '插画': 'illustration, digital art',
    };
    
    // Apply mappings
    Object.keys(subjectMap).forEach(key => {
        if (prompt.includes(key)) {
            prompt = prompt.replace(key, subjectMap[key]);
        }
    });
    
    // Add style keywords based on context
    if (prompt.includes('动漫') || prompt.includes('卡通')) {
        prompt = 'anime style, ' + prompt;
    }
    
    // Final cleanup and add quality keywords
    prompt = prompt.replace(/\s+/g, ' ').trim();
    
    // If still mostly Chinese, create a simple English prompt
    if (/[\u4e00-\u9fa5]/.test(prompt)) {
        // Keep subject, add English quality terms
        prompt = prompt + ', highly detailed, 4K, cinematic';
    } else {
        prompt = prompt + ', ' + qualityKeywords;
    }
    
    return prompt;
}

module.exports = async function(context) {
    const API_KEY = process.env.MINIMAX_API_KEY || process.env.AIMLAPI_API_KEY;
    if (!API_KEY) {
        return { text: "❌ 未找到 API Key，请设置 MINIMAX_API_KEY 或 AIMLAPI_API_KEY 环境变量。" };
    }

    const API_URL = "https://api.minimaxi.com/v1/image_generation";

    // Get user input
    let userInput = context.args.join(' ').trim();
    if (!userInput && context.stdin) {
        userInput = context.stdin.trim();
    }
    if (!userInput) {
        return { text: "请提供图片描述。例如：/minimax 一只可爱的橘猫" };
    }

    // Optimize the prompt
    const optimizedPrompt = optimizePrompt(userInput);
    
    console.log('Original prompt:', userInput);
    console.log('Optimized prompt:', optimizedPrompt);

    try {
        const response = await axios.post(API_URL, {
            model: "image-01",
            prompt: optimizedPrompt,
            aspect_ratio: "16:9",
            n: 1
        }, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        const data = response.data;
        if (data.base_resp && data.base_resp.status_code === 0 && data.data && data.data.length > 0) {
            const imageUrl = data.data[0].url;
            return {
                text: `✅ 优化提示词: ${optimizedPrompt}\n\n![生成的图片](${imageUrl})`,
                attachments: [{ type: 'image', url: imageUrl }]
            };
        } else {
            const errorMsg = data.base_resp?.status_msg || '未知错误';
            return { text: `图片生成失败：${errorMsg}` };
        }
    } catch (error) {
        console.error(error);
        return { text: `调用 MiniMax API 出错：${error.message}` };
    }
};