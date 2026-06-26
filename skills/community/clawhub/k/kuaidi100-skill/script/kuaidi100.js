const https = require('https');
const querystring = require('querystring');
const fs = require('fs');
const path = require('path');

// API 基础地址
const BASE_URL = 'api.kuaidi100.com';
const BASE_PATH = '/stdio';

// 配置文件路径（位于项目根目录）
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

// 读取配置文件
function loadConfig() {
    try {
        if (fs.existsSync(CONFIG_FILE)) {
            const content = fs.readFileSync(CONFIG_FILE, 'utf-8');
            return JSON.parse(content);
        }
    } catch (error) {
        // 配置文件读取失败，忽略
    }
    return {};
}

// 获取 Key（优先从配置文件读取，其次读取系统环境变量）
function getKey() {
    const config = loadConfig();
    if (config.apiKey && config.apiKey.trim() !== '') {
        return config.apiKey.trim();
    }
    return process.env.KUAIDI100_API_KEY || 'null';
}

// 发起 HTTPS GET 请求
function makeRequest(path, params) {
    return new Promise((resolve, reject) => {
        const queryStr = querystring.stringify(params);
        const fullPath = `${BASE_PATH}${path}?${queryStr}`;
        
        const options = {
            hostname: BASE_URL,
            path: fullPath,
            method: 'GET'
        };
        
        const req = https.request(options, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                resolve(data);
            });
        });
        
        req.on('error', (error) => {
            reject(error);
        });
        
        req.end();
    });
}

// 1. 查询快递物流轨迹
async function queryTrace(kuaidiNum, phone = null) {
    const params = {
        key: getKey(),
        kuaidiNum: kuaidiNum
    };
    
    if (phone) {
        params.phone = phone;
    }
    
    return await makeRequest('/queryTrace', params);
}

// 2. 识别快递公司
async function autoNumber(kuaidiNum) {
    const params = {
        key: getKey(),
        kuaidiNum: kuaidiNum
    };
    
    return await makeRequest('/autoNumber', params);
}

// 3. 估算运费
async function estimatePrice(kuaidicom, recAddr, sendAddr, weight = '1') {
    const params = {
        key: getKey(),
        kuaidicom: kuaidicom,
        recAddr: recAddr,
        sendAddr: sendAddr,
        weight: weight
    };
    
    return await makeRequest('/estimatePrice', params);
}

// 4. 预估寄件送达时间
async function estimateTime(kuaidicom, from, to, orderTime = null, expType = null) {
    const params = {
        key: getKey(),
        kuaidicom: kuaidicom,
        from: from,
        to: to
    };
    
    if (orderTime) {
        params.orderTime = orderTime;
    }
    
    if (expType) {
        params.expType = expType;
    }
    
    return await makeRequest('/estimateTime', params);
}

// 5. 预估在途快递送达时间
async function estimateTimeWithLogistic(kuaidicom, from, to, orderTime, logistic) {
    const params = {
        key: getKey(),
        kuaidicom: kuaidicom,
        from: from,
        to: to,
        orderTime: orderTime,
        logistic: logistic
    };
    
    return await makeRequest('/estimateTime', params);
}

// 主函数 - 解析命令行参数并调用对应方法
async function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('用法: node kuaidi100.js <方法名> [参数...]');
        console.log('');
        console.log('支持的方法:');
        console.log('  queryTrace <快递单号> [手机号]');
        console.log('  autoNumber <快递单号>');
        console.log('  estimatePrice <快递公司编码> <收件地址> <寄件地址> [重量]');
        console.log('  estimateTime <快递公司编码> <出发地> <目的地> [下单时间] [业务类型]');
        console.log('  estimateTimeWithLogistic <快递公司编码> <出发地> <目的地> <下单时间> <物流轨迹JSON>');
        process.exit(1);
    }
    
    const method = args[0];
    
    try {
        let result;
        
        switch (method) {
            case 'queryTrace':
                if (args.length < 2) {
                    console.error('错误: queryTrace 需要快递单号参数');
                    process.exit(1);
                }
                result = await queryTrace(args[1], args[2] || null);
                break;
                
            case 'autoNumber':
                if (args.length < 2) {
                    console.error('错误: autoNumber 需要快递单号参数');
                    process.exit(1);
                }
                result = await autoNumber(args[1]);
                break;
                
            case 'estimatePrice':
                if (args.length < 4) {
                    console.error('错误: estimatePrice 需要快递公司编码、收件地址、寄件地址参数');
                    process.exit(1);
                }
                result = await estimatePrice(args[1], args[2], args[3], args[4] || '1');
                break;
                
            case 'estimateTime':
                if (args.length < 4) {
                    console.error('错误: estimateTime 需要快递公司编码、出发地、目的地参数');
                    process.exit(1);
                }
                result = await estimateTime(args[1], args[2], args[3], args[4] || null, args[5] || null);
                break;
                
            case 'estimateTimeWithLogistic':
                if (args.length < 6) {
                    console.error('错误: estimateTimeWithLogistic 需要快递公司编码、出发地、目的地、下单时间、物流轨迹JSON参数');
                    process.exit(1);
                }
                result = await estimateTimeWithLogistic(args[1], args[2], args[3], args[4], args[5]);
                break;
                
            default:
                console.error(`错误: 未知方法 "${method}"`);
                process.exit(1);
        }
        
        console.log(result);
        
    } catch (error) {
        console.error('请求失败:', error.message);
        process.exit(1);
    }
}

main();
