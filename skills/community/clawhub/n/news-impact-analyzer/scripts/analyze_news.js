const https = require('https');
const http = require('http');

/**
 * 清理环境变量：移除空格、换行、引号以及不可见字符
 */
function cleanEnvVar(val) {
    if (!val) return "";
    return val.trim()
        .replace(/^["']|["']$/g, '') // 移除首尾引号
        .replace(/[\x00-\x1F\x7F-\x9F]/g, "") // 移除不可见控制字符
        .trim();
}

// 读取环境变量并清洗
const EASYALPHA_API_KEY = cleanEnvVar(process.env.EASYALPHA_API_KEY);
const NEWS_EXTRACTOR_SERVER_URL = cleanEnvVar(process.env.NEWS_EXTRACTOR_SERVER_URL) || "https://easyalpha.duckdns.org";

if (!EASYALPHA_API_KEY) {
    console.error("Error: Environment variable EASYALPHA_API_KEY is not set.");
    process.exit(1);
}

// 获取命令行参数作为新闻内容
const args = process.argv.slice(2);
if (args.length === 0) {
    console.error("Error: Please provide the news content as a command-line argument.");
    console.log("Usage: node analyze_news.js \"<news content here>\"");
    process.exit(1);
}

const newsContent = args.join(' ');

async function analyzeNews(content) {
    console.log(`Analyzing news impact... (this may take a few seconds)`);

    // 确定是使用 HTTP 还是 HTTPS
    const isHttps = NEWS_EXTRACTOR_SERVER_URL.startsWith('https://');
    const httpModule = isHttps ? https : http;

    try {
        // 构建请求选项
        const serverUrl = new URL(NEWS_EXTRACTOR_SERVER_URL);
        const requestData = JSON.stringify({ news_content: content });

        const endpoint = '/api/v1/analyze';

        const options = {
            hostname: serverUrl.hostname,
            port: serverUrl.port || (isHttps ? 443 : 80),
            path: endpoint,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(requestData),
                'X-EasyAlpha-API-Key': EASYALPHA_API_KEY,
                'Authorization': `Bearer ${EASYALPHA_API_KEY}`
            },
            // 默认跳过 SSL 验证以简化用户操作 (尤其是针对 duckdns 等自动证书可能导致的验证问题)
            // 如果用户显式设置了 ALLOW_INSECURE_SSL='false'，则开启验证
            rejectUnauthorized: process.env.ALLOW_INSECURE_SSL === 'false' ? true : false
        };

        const req = httpModule.request(options, (res) => {
            let responseData = '';

            res.on('data', (chunk) => {
                responseData += chunk;
            });

            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    let parsedData;
                    try {
                        parsedData = JSON.parse(responseData);
                    } catch (e) {
                        // Response is not valid JSON; treat it as Markdown / text output
                    }

                    if (parsedData && typeof parsedData === 'object') {
                        formatAndPrintResult(parsedData);
                    } else {
                        console.log("API returned non-JSON response (treated as Markdown/text):\n");
                        console.log(responseData);
                    }
                } else {
                    console.error(`API request failed with status code ${res.statusCode}: ${responseData}`);
                }
            });
        });

        req.on('error', (e) => {
            console.error(`Problem with request to ${NEWS_EXTRACTOR_SERVER_URL}: ${e.message}`);
        });

        // 写入数据并发送请求
        req.write(requestData);
        req.end();

    } catch (error) {
        if (error.code === 'ERR_INVALID_URL') {
            console.error(`Invalid URL provided for NEWS_EXTRACTOR_SERVER_URL: ${NEWS_EXTRACTOR_SERVER_URL}`);
        } else {
            console.error(`Error setting up the request: ${error.message}`);
        }
    }
}

function formatAndPrintResult(result) {
    console.log("\n=============================");
    console.log("    News Impact Analysis     ");
    console.log("=============================\n");

    if (result.summary) {
        console.log(`Summary: ${result.summary}\n`);
    }

    if (result.impacts && Array.isArray(result.impacts) && result.impacts.length > 0) {
        console.log("Detailed Impacts:");
        console.log("-----------------");
        result.impacts.forEach((impact, index) => {
            const typeLabel = impact.type === 'sector' ? 'Sector' : (impact.type === 'concept' ? 'Concept' : impact.type);
            const directionLabel = impact.direction.toUpperCase();
            // 可以根据看多看空添加简单的颜色标记 (可选 ANSI)
            console.log(`${index + 1}. [${typeLabel}] ${impact.name} -> ${directionLabel}`);
            console.log(`   Logic: ${impact.logic}\n`);
        });
    } else {
        console.log("No specific sector or concept impacts identified.");
    }
}

// 启动分析
analyzeNews(newsContent);
