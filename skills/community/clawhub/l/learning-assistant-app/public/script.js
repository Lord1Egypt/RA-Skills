// 学习助手应用JavaScript

// 全局变量
let currentTab = 'dictionary';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    loadRandomFactOnLoad();
    loadHistoricalEventOnLoad();
});

// 初始化标签页
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // 更新按钮状态
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // 更新内容显示
            tabPanes.forEach(pane => pane.classList.remove('active'));
            document.getElementById(targetTab).classList.add('active');
            
            currentTab = targetTab;
        });
    });
}

// 词典查询功能
async function searchWord() {
    const wordInput = document.getElementById('wordInput');
    const word = wordInput.value.trim();
    
    if (!word) {
        showResult('dictionaryResult', '请输入要查询的单词', 'error');
        return;
    }
    
    showResult('dictionaryResult', '<div class="loading"></div> 正在查询...', 'loading');
    
    try {
        const response = await fetch(`/api/dictionary/${word}`);
        const data = await response.json();
        
        if (response.ok) {
            displayDictionaryResult(data);
        } else {
            showResult('dictionaryResult', data.error || '查询失败', 'error');
        }
    } catch (error) {
        showResult('dictionaryResult', '网络错误，请检查连接', 'error');
    }
}

// 显示词典查询结果
function displayDictionaryResult(data) {
    let html = '<h3>🔤 查询结果</h3>';
    
    if (data.length > 0) {
        const firstResult = data[0];
        
        if (firstResult.meanings) {
            firstResult.meanings.forEach(meaning => {
                html += `<div class="word-info">`;
                html += `<h4>${meaning.partOfSpeech || '词性'}</h4>`;
                
                if (meaning.definitions) {
                    meaning.definitions.forEach((definition, index) => {
                        html += `<p><strong>定义 ${index + 1}:</strong> ${definition.definition}</p>`;
                        if (definition.example) {
                            html += `<p><em>例句:</em> ${definition.example}</p>`;
                        }
                    });
                }
                
                html += `</div>`;
            });
        }
        
        if (firstResult.phonetics) {
            const phonetic = firstResult.phonetics.find(p => p.text);
            if (phonetic) {
                html += `<p><strong>发音:</strong> ${phonetic.text}</p>`;
            }
        }
    }
    
    showResult('dictionaryResult', html, 'success');
}

// 翻译功能
async function translateText() {
    const translateInput = document.getElementById('translateInput');
    const sourceLang = document.getElementById('sourceLang').value;
    const targetLang = document.getElementById('targetLang').value;
    const text = translateInput.value.trim();
    
    if (!text) {
        showResult('translationResult', '请输入要翻译的文本', 'error');
        return;
    }
    
    showResult('translationResult', '<div class="loading"></div> 正在翻译...', 'loading');
    
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                sourceLang: sourceLang,
                targetLang: targetLang
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayTranslationResult(data);
        } else {
            showResult('translationResult', data.error || '翻译失败', 'error');
        }
    } catch (error) {
        showResult('translationResult', '网络错误，请检查连接', 'error');
    }
}

// 显示翻译结果
function displayTranslationResult(data) {
    const langNames = {
        'en': '英语',
        'zh': '中文',
        'es': '西班牙语',
        'fr': '法语',
        'de': '德语'
    };
    
    let html = '<h3>🌍 翻译结果</h3>';
    html += `<div class="translation-info">`;
    html += `<p><strong>原文 (${langNames[data.sourceLang]}):</strong> ${data.original}</p>`;
    html += `<p><strong>译文 (${langNames[data.targetLang]}):</strong> ${data.translated}</p>`;
    html += `</div>`;
    
    showResult('translationResult', html, 'success');
}

// 获取随机事实
async function getRandomFact() {
    showResult('factResult', '<div class="loading"></div> 正在获取有趣事实...', 'loading');
    
    try {
        const response = await fetch('/api/fact');
        const data = await response.json();
        
        if (response.ok) {
            displayFactResult(data);
        } else {
            showResult('factResult', data.error || '获取事实失败', 'error');
        }
    } catch (error) {
        showResult('factResult', '网络错误，请检查连接', 'error');
    }
}

// 显示事实结果
function displayFactResult(data) {
    let html = '<h3>💡 有趣事实</h3>';
    html += `<div class="fact-card">`;
    html += `<p>${data.text}</p>`;
    html += `<p><small>来源: ${data.source || '未知'}</small></p>`;
    html += `</div>`;
    
    showResult('factResult', html, 'success');
}

// 页面加载时显示随机事实
function loadRandomFactOnLoad() {
    getRandomFact();
}

// 数学计算功能
async function calculateExpression() {
    const mathInput = document.getElementById('mathInput');
    const expression = mathInput.value.trim();
    
    if (!expression) {
        showResult('calculatorResult', '请输入数学表达式', 'error');
        return;
    }
    
    showResult('calculatorResult', '<div class="loading"></div> 正在计算...', 'loading');
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                expression: expression
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayCalculatorResult(data);
        } else {
            showResult('calculatorResult', data.error || '计算失败', 'error');
        }
    } catch (error) {
        showResult('calculatorResult', '计算错误，请检查表达式', 'error');
    }
}

// 显示计算结果
function displayCalculatorResult(data) {
    let html = '<h3>🔢 计算结果</h3>';
    html += `<p><strong>表达式:</strong> ${data.expression}</p>`;
    html += `<p><strong>结果:</strong> ${data.result}</p>`;
    html += `<p><small>计算时间: ${new Date(data.timestamp).toLocaleString()}</small></p>`;
    
    showResult('calculatorResult', html, 'success');
}

// 获取历史事件
async function getHistoricalEvent() {
    showResult('historyResult', '<div class="loading"></div> 正在获取历史事件...', 'loading');
    
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (response.ok && data.length > 0) {
            displayHistoricalEvent(data[0]);
        } else {
            showResult('historyResult', '获取历史事件失败', 'error');
        }
    } catch (error) {
        showResult('historyResult', '网络错误，请检查连接', 'error');
    }
}

// 显示历史事件
function displayHistoricalEvent(event) {
    let html = '<h3>📜 历史事件</h3>';
    html += `<div class="history-card">`;
    html += `<p><strong>事件:</strong> ${event.event}</p>`;
    html += `<p><strong>日期:</strong> ${event.year}年${event.month}月${event.day}日</p>`;
    
    if (event.link) {
        html += `<p><strong>更多信息:</strong> <a href="${event.link}" target="_blank">查看详情</a></p>`;
    }
    
    html += `</div>`;
    
    showResult('historyResult', html, 'success');
}

// 页面加载时显示历史事件
function loadHistoricalEventOnLoad() {
    getHistoricalEvent();
}

// 显示结果的通用函数
function showResult(elementId, content, type = '') {
    const element = document.getElementById(elementId);
    element.innerHTML = content;
    
    // 添加样式类
    element.className = 'result-area';
    if (type) {
        element.classList.add(type);
    }
}

// 键盘事件处理
document.addEventListener('keydown', function(event) {
    // Enter键触发查询
    if (event.key === 'Enter') {
        const activeElement = document.activeElement;
        
        if (activeElement.id === 'wordInput') {
            searchWord();
        } else if (activeElement.id === 'translateInput') {
            translateText();
        } else if (activeElement.id === 'mathInput') {
            calculateExpression();
        }
    }
});

// 复制功能
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('已复制到剪贴板');
    }).catch(err => {
        console.error('复制失败:', err);
    });
}

// 添加复制按钮到结果区域
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('copy-btn')) {
        const text = event.target.getAttribute('data-text');
        copyToClipboard(text);
    }
});