// PPT Generator - 主逻辑文件
const fs = require('fs');
const path = require('path');

/**
 * 生成PPT的主要函数
 * @param {string} content - 用户输入的演讲内容
 * @param {Object} options - 配置选项
 * @returns {string} - 生成的HTML文件路径
 */
async function generatePPT(content, options = {}) {
    // 默认配置
    const config = {
        title: options.title || '我的演示文稿',
        author: options.author || 'OpenClaw PPT生成器',
        style: options.style || 'jobs-style', // 乔布斯风格
        backgroundColor: options.backgroundColor || '#000000',
        textColor: options.textColor || '#ffffff',
        accentColor: options.accentColor || '#007aff',
        ...options
    };

    // 将内容分割成幻灯片
    const slides = splitIntoSides(content);
    
    // 生成HTML
    const html = generateHTML(slides, config);
    
    // 保存文件
    const outputPath = path.join(process.cwd(), `presentation-${Date.now()}.html`);
    fs.writeFileSync(outputPath, html, 'utf8');
    
    return outputPath;
}

/**
 * 将文本分割成幻灯片
 * @param {string} text - 输入的演讲内容
 * @returns {Array} - 幻灯片数组
 */
function splitIntoSides(text) {
    // 简单的分割逻辑：按段落分割
    const paragraphs = text.split(/\n\s*\n/);
    
    return paragraphs.map((para, index) => ({
        id: index + 1,
        title: `Slide ${index + 1}`,
        content: para.trim(),
        type: determineSideType(para)
    }));
}

/**
 * 确定幻灯片类型
 * @param {string} text - 幻灯片内容
 * @returns {string} - 幻灯片类型
 */
function determineSideType(text) {
    if (text.length < 100) return 'title';
    if (text.includes('•') || text.includes('- ') || text.includes('* ')) return 'bullets';
    if (text.split('\n').length > 3) return 'quote';
    return 'content';
}

/**
 * 生成HTML
 * @param {Array} slides - 幻灯片数组
 * @param {Object} config - 配置对象
 * @returns {string} - HTML字符串
 */
function generateHTML(slides, config) {
    const template = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${config.title}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: ${config.backgroundColor};
            color: ${config.textColor};
            height: 100vh;
            overflow: hidden;
        }
        
        .slides-container {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px;
        }
        
        .slide {
            display: none;
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        
        .slide.active {
            display: block;
            animation: fadeIn 0.8s ease-in-out;
        }
        
        h1 {
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: -0.02em;
            color: ${config.accentColor};
        }
        
        h2 {
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 30px;
            letter-spacing: -0.01em;
        }
        
        p {
            font-size: 1.8rem;
            line-height: 1.5;
            margin-bottom: 20px;
            opacity: 0.9;
        }
        
        .bullets {
            text-align: left;
            margin: 0 auto;
            max-width: 600px;
        }
        
        .bullets li {
            font-size: 1.6rem;
            line-height: 1.6;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        
        .controls {
            position: fixed;
            bottom: 30px;
            left: 0;
            right: 0;
            text-align: center;
            z-index: 100;
        }
        
        button {
            background: ${config.accentColor};
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            margin: 0 10px;
            transition: opacity 0.2s;
        }
        
        button:hover {
            opacity: 0.9;
        }
        
        .slide-counter {
            position: fixed;
            top: 20px;
            right: 20px;
            font-size: 1.2rem;
            opacity: 0.7;
        }
        
        .author {
            position: fixed;
            top: 20px;
            left: 20px;
            font-size: 1rem;
            opacity: 0.5;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="author">${config.author}</div>
    <div class="slide-counter">Slide <span id="current">1</span> of ${slides.length}</div>
    
    <div class="slides-container">
        ${slides.map((slide, index) => `
            <div class="slide ${index === 0 ? 'active' : ''}" id="slide-${slide.id}">
                ${slide.type === 'title' ? `
                    <h1>${slide.content}</h1>
                ` : slide.type === 'bullets' ? `
                    <h2>${slide.title}</h2>
                    <ul class="bullets">
                        ${slide.content.split(/[•\-*]/).filter(item => item.trim()).map(item => `
                            <li>${item.trim()}</li>
                        `).join('')}
                    </ul>
                ` : `
                    <h2>${slide.title}</h2>
                    <p>${slide.content}</p>
                `}
            </div>
        `).join('')}
    </div>
    
    <div class="controls">
        <button id="prev">上一页</button>
        <button id="next">下一页</button>
        <button id="fullscreen">全屏</button>
    </div>
    
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        
        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            slides[index].classList.add('active');
            document.getElementById('current').textContent = index + 1;
            currentSlide = index;
        }
        
        document.getElementById('next').addEventListener('click', () => {
            if (currentSlide < slides.length - 1) {
                showSlide(currentSlide + 1);
            }
        });
        
        document.getElementById('prev').addEventListener('click', () => {
            if (currentSlide > 0) {
                showSlide(currentSlide - 1);
            }
        });
        
        document.getElementById('fullscreen').addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.log('全屏请求失败:', err);
                });
            } else {
                document.exitFullscreen();
            }
        });
        
        // 键盘控制
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                if (currentSlide < slides.length - 1) {
                    showSlide(currentSlide + 1);
                }
            } else if (e.key === 'ArrowLeft') {
                if (currentSlide > 0) {
                    showSlide(currentSlide - 1);
                }
            } else if (e.key === 'f') {
                if (!document.fullscreenElement) {
                    document.documentElement.requestFullscreen();
                } else {
                    document.exitFullscreen();
                }
            }
        });
        
        // 触摸滑动
        let touchStartX = 0;
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
        });
        
        document.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > 50) {
                if (diff > 0 && currentSlide < slides.length - 1) {
                    showSlide(currentSlide + 1); // 向左滑动
                } else if (diff < 0 && currentSlide > 0) {
                    showSlide(currentSlide - 1); // 向右滑动
                }
            }
        });
    </script>
</body>
</html>`;
    
    return template;
}

// 导出函数
module.exports = { generatePPT };

// 如果直接运行此文件，则执行示例
if (require.main === module) {
    const exampleContent = `
欢迎使用OpenClaw PPT生成器

这是一个演示文稿的示例
展示了乔布斯风格的极简设计

• 特色功能一：智能内容分割
• 特色功能二：响应式设计
• 特色功能三：键盘和触摸控制

感谢使用我们的PPT生成器
希望它能为您的演示增色不少
`;
    
    generatePPT(exampleContent, {
        title: 'OpenClaw PPT生成器演示',
        author: 'OpenClaw AI助手',
        backgroundColor: '#1d1d1f',
        textColor: '#f5f5f7',
        accentColor: '#007aff'
    }).then(outputPath => {
        console.log('PPT已生成:', outputPath);
        console.log('请在浏览器中打开此文件查看效果');
    }).catch(error => {
        console.error('生成PPT时出错:', error);
    });
}