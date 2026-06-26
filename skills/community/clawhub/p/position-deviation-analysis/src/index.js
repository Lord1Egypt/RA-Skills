/**
 * 持仓偏离度分析 Skill 入口文件 (免费版本)
 * 作者：亚勇电脑
 * 版本：2.0.0-free
 * 
 * 功能：基于公开市场数据的均线偏离度计算工具
 * 
 * ⚠️ 免责声明：
 * 本工具仅提供数据计算功能，不构成任何投资建议。
 * 计算结果仅供参考，用户需自行承担投资风险。
 */

const { analyzeSingle, formatReport } = require('./analyze');

/**
 * Skill 主入口函数
 * @param {Object} params - OpenClaw 传入的参数
 * @param {string} params.userId - 用户ID
 * @param {string} params.message - 用户消息
 */
async function main(params) {
    const { userId, message } = params;

    // 1. 解析用户需求
    const tickers = parseTickers(message);
    
    if (tickers.length === 0) {
        return {
            code: 200,
            message: `
📊 **持仓偏离度分析工具**

请输入需要分析的标的代码，支持以下标的：
- **518850** (黄金产业ETF)
- **515180** (中证红利ETF)
- **512570** (全指现金流ETF)
- **159638** (稀有金属ETF)

📝 **示例命令**：
- 分析 518850
- 计算我的持仓偏离度：518850,515180
- 帮我分析 159638 的偏离度

---
⚠️ 本工具仅提供数据计算功能，不构成任何投资建议。市场有风险，投资需谨慎。
            `.trim()
        };
    }

    // 2. 执行分析
    try {
        console.log(`🔍 用户 ${userId} 请求分析偏离度`);
        console.log(`   标的: ${tickers.join(', ')}`);
        
        const results = tickers.map(code => analyzeSingle(code));
        const report = formatReport(results);

        return {
            code: 200,
            message: report,
            metadata: {
                analyzedCount: tickers.length,
                tickers: tickers,
                dataSource: '东方财富公开行情API',
                timestamp: new Date().toISOString()
            }
        };
    } catch (error) {
        console.error(`❌ 分析失败: ${error.message}`);
        return {
            code: 500,
            message: `分析失败：${error.message}\n\n请稍后重试，或检查标的代码是否正确。`
        };
    }
}

/**
 * 解析用户消息中的标的代码
 * @param {string} message - 用户消息
 * @returns {string[]} 标的代码数组
 */
function parseTickers(message) {
    if (!message) return [];
    
    // 清理消息文本
    let text = message.trim();
    
    // 移除常见前缀
    text = text.replace(/^(分析|计算|查看|查询|帮我分析|我想知道)\s*/i, '');
    
    // 支持的标的列表
    const knownTickers = ['518850', '515180', '512570', '159638'];
    
    // 提取标的代码
    const found = [];
    
    // 方式1: 逗号分隔的代码列表
    if (text.includes(',')) {
        const parts = text.split(/[,，\s]+/);
        parts.forEach(p => {
            const code = p.trim().replace(/[，。.]/g, '');
            if (knownTickers.includes(code)) {
                found.push(code);
            }
        });
    }
    
    // 方式2: 逐个匹配已知代码
    if (found.length === 0) {
        knownTickers.forEach(code => {
            if (text.includes(code)) {
                found.push(code);
            }
        });
    }
    
    // 方式3: 直接提取4-6位数字
    if (found.length === 0) {
        const numbers = text.match(/\d{4,6}/g);
        if (numbers) {
            numbers.forEach(n => {
                if (knownTickers.includes(n)) {
                    found.push(n);
                }
            });
        }
    }
    
    // 去重
    return [...new Set(found)];
}

// 导出模块
module.exports = { main };
