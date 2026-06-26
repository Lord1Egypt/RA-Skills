/**
 * 持仓偏离度分析核心模块
 * 作者：亚勇电脑
 * 版本：2.0.0
 * 
 * 功能：基于东方财富API的均线偏离度计算工具
 */

const https = require('https');
const http = require('http');

// 支持的标的配置
const TICKERS = {
    "518850": { name: "黄金产业ETF", type: "大宗商品", market: "sh" },
    "515180": { name: "中证红利ETF", type: "宽基指数", market: "sh" },
    "512570": { name: "全指现金流ETF", type: "宽基指数", market: "sh" },
    "159638": { name: "稀有金属ETF", type: "行业主题", market: "sz" },
};

// 历史分位阈值
const THRESHOLDS = {
    "超卖": -2.0,
    "低估": -1.0,
    "合理": 1.0,
    "高估": 2.0,
    "超买": Infinity
};

/**
 * HTTP请求封装
 */
function httpRequest(url) {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https') ? https : http;
        const req = client.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(new Error('JSON解析失败'));
                }
            });
        });
        req.on('error', reject);
        req.setTimeout(10000, () => {
            req.destroy();
            reject(new Error('请求超时'));
        });
    });
}

/**
 * 获取实时价格（东方财富实时行情API）
 * @param {string} code - 标的代码
 * @returns {Promise<{price: number, change: number}>}
 */
async function getRealtimePrice(code) {
    const info = TICKERS[code];
    if (!info) {
        throw new Error(`不支持的标的代码: ${code}`);
    }

    // 上海ETF: 1.开头, 深圳ETF: 0.开头
    const secid = info.market === 'sh' ? `1.${code}` : `0.${code}`;
    const url = `https://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f44,f45,f46,f47,f48,f50,f57,f58,f170`;

    try {
        const data = await httpRequest(url);
        
        if (!data.data || !data.data.f43) {
            throw new Error(`未获取到 ${code} 的行情数据`);
        }

        return {
            price: parseFloat(data.data.f43) / 100, // f43是最新价（分）
            change: parseFloat(data.data.f170) || 0 // f170是涨跌幅
        };
    } catch (error) {
        throw new Error(`获取实时价格失败: ${error.message}`);
    }
}

/**
 * 获取20日均线（东方财富K线API）
 * @param {string} code - 标的代码
 * @returns {Promise<number>}
 */
async function get20dAverage(code) {
    const info = TICKERS[code];
    if (!info) {
        throw new Error(`不支持的标的代码: ${code}`);
    }

    // 上海ETF: 1.开头, 深圳ETF: 0.开头
    const secid = info.market === 'sh' ? `1.${code}` : `0.${code}`;
    // 获取最近20个交易日K线数据
    const url = `https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=${secid}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&beg=0&lmt=20`;

    try {
        const data = await httpRequest(url);
        
        if (!data.data || !data.data.klines || data.data.klines.length === 0) {
            throw new Error(`未获取到 ${code} 的K线数据`);
        }

        // f52 是收盘价，计算20日均价
        const closePrices = data.data.klines.map(kline => {
            const fields = kline.split(',');
            return parseFloat(fields[4]); // 收盘价
        });

        const avg = closePrices.reduce((sum, p) => sum + p, 0) / closePrices.length;
        return avg;
    } catch (error) {
        throw new Error(`获取20日均线失败: ${error.message}`);
    }
}

/**
 * 计算偏离度
 */
function calculateDeviation(current, avg) {
    return Math.round((current - avg) / avg * 10000) / 100; // 保留2位小数
}

/**
 * 根据偏离度给出参考建议
 */
function getSuggestion(deviation) {
    if (deviation < THRESHOLDS["超卖"]) {
        return "偏离度较大（仅供参考）";
    } else if (deviation < THRESHOLDS["低估"]) {
        return "偏离度偏低（仅供参考）";
    } else if (deviation < THRESHOLDS["合理"]) {
        return "偏离度正常";
    } else if (deviation < THRESHOLDS["高估"]) {
        return "偏离度偏高（仅供参考）";
    } else {
        return "偏离度较大（仅供参考）";
    }
}

/**
 * 计算历史分位位置
 */
function calculatePercentile(deviation) {
    const normalized = Math.min(Math.max(deviation, -5), 5);
    return Math.round((normalized + 5) / 10 * 100);
}

/**
 * 分析单个标的
 */
async function analyzeSingle(code) {
    const info = TICKERS[code] || {};

    try {
        const [priceData, avg] = await Promise.all([
            getRealtimePrice(code),
            get20dAverage(code)
        ]);

        const current = priceData.price;
        const deviation = calculateDeviation(current, avg);
        const percentile = calculatePercentile(deviation);
        const suggestion = getSuggestion(deviation);

        return {
            code: code,
            name: info.name || "未知",
            type: info.type || "未知",
            current_price: Math.round(current * 1000) / 1000,
            ma20: Math.round(avg * 1000) / 1000,
            deviation: deviation,
            change_pct: priceData.change,
            percentile: percentile,
            suggestion: suggestion,
            timestamp: new Date().toISOString()
        };
    } catch (error) {
        return {
            code: code,
            name: info.name || "未知",
            error: error.message
        };
    }
}

/**
 * 批量分析多个标的
 */
async function analyzeBatch(codes) {
    const validCodes = codes.filter(c => c in TICKERS);
    const results = await Promise.all(validCodes.map(code => analyzeSingle(code)));
    return results;
}

/**
 * 格式化输出报告
 */
function formatReport(results) {
    const lines = [];
    lines.push("## 📊 持仓偏离度分析报告");
    lines.push("");
    lines.push("⚠️ **数据仅供参考，不构成投资建议**");
    lines.push("");

    for (const r of results) {
        if (r.error) {
            lines.push(`### ${r.code} ${r.name}`);
            lines.push(`- ❌ **错误**: ${r.error}`);
            lines.push("");
            continue;
        }

        lines.push(`### ${r.code} ${r.name} (${r.type})`);
        lines.push(`- **当前价格**: ${r.current_price}`);
        if (r.change_pct !== undefined) {
            const arrow = r.change_pct >= 0 ? "📈" : "📉";
            lines.push(`- **今日涨跌**: ${arrow} ${r.change_pct >= 0 ? '+' : ''}${r.change_pct}%`);
        }
        lines.push(`- **20日均线**: ${r.ma20}`);
        lines.push(`- **偏离度**: ${r.deviation >= 0 ? '+' : ''}${r.deviation}%`);
        lines.push(`- **历史位置**: ${r.percentile}%分位`);
        lines.push(`- **参考**: ${r.suggestion}`);
        lines.push("");
    }

    lines.push("---");
    lines.push(`⏰ 计算时间：${new Date().toLocaleString('zh-CN')}`);
    lines.push(`📡 数据来源：东方财富公开API`);
    lines.push("");
    lines.push("⚠️ **数据仅供参考，不构成投资建议**");
    lines.push("⚠️ **用户需自行承担投资风险**");

    return lines.join("\n");
}

/**
 * 获取支持的标的列表
 */
function getSupportedTickers() {
    return Object.entries(TICKERS).map(([code, info]) => ({
        code,
        name: info.name,
        type: info.type
    }));
}

module.exports = {
    analyzeSingle,
    analyzeBatch,
    formatReport,
    getSupportedTickers,
    TICKERS,
    THRESHOLDS
};
