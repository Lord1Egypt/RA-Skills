#!/usr/bin/env node

/**
 * 观远数据 API Skill
 * 功能：
 * 1. 用户登录（配置从 ~/.guanyuan/config.json 读取）
 * 2. Token 自动管理和刷新（保存在 ~/.guanyuan/user.token）
 * 3. 获取指定卡片ID的数据
 * 4. 导出卡片数据为CSV格式（支持采样和保存到文件）
 *
 * 配置文件格式 (~/.guanyuan/config.json):
 * {
 *   "baseUrl": "api.guandata.com",
 *   "domain": "your-domain",
 *   "loginId": "your-login-id",
 *   "password": "your-password"
 * }
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 配置文件路径
const CONFIG_DIR = path.join(process.env.HOME, '.guanyuan');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');
const TOKEN_FILE = path.join(CONFIG_DIR, 'user.token');

// 默认配置
const DEFAULT_CONFIG = {
    baseUrl: 'api.guandata.com',
    domain: '',
    loginId: '',
    password: '',
    token: ''
};

// 确保配置目录存在
function ensureConfigDir() {
    if (!fs.existsSync(CONFIG_DIR)) {
        fs.mkdirSync(CONFIG_DIR, { recursive: true });
    }
}

// 读取配置文件
function loadConfig() {
    ensureConfigDir();

    if (!fs.existsSync(CONFIG_FILE)) {
        console.error('错误：配置文件不存在，请先创建 ~/.guanyuan/config.json');
        console.error('');
        console.error('配置文件格式（方式一：使用账号密码登录）：');
        console.error(JSON.stringify({
            baseUrl: 'https://your-guanyuan-domain.com',
            domain: 'your-domain',
            loginId: 'your-login-id',
            password: 'your-password'
        }, null, 2));
        console.error('');
        console.error('配置文件格式（方式二：直接使用Token）：');
        console.error(JSON.stringify({
            baseUrl: 'https://your-guanyuan-domain.com',
            domain: 'your-domain',
            token: 'your-token'
        }, null, 2));
        console.error('');
        console.error('创建命令：');
        console.error('  mkdir -p ~/.guanyuan');
        console.error('  cat > ~/.guanyuan/config.json << \'EOF\'');
        console.error('  {');
        console.error('    "baseUrl": "https://your-guanyuan-domain.com",');
        console.error('    "domain": "your-domain",');
        console.error('    "loginId": "your-login-id",');
        console.error('    "password": "your-password"');
        console.error('  }');
        console.error('  EOF');
        process.exit(1);
    }

    try {
        const content = fs.readFileSync(CONFIG_FILE, 'utf-8');
        const config = JSON.parse(content);

        // 验证必需字段
        if (!config.baseUrl || !config.domain) {
            console.error('错误：配置文件缺少必需字段');
            console.error('必需字段：baseUrl, domain');
            console.error('可选字段（二选一）：');
            console.error('  - loginId 和 password（用于自动登录）');
            console.error('  - token（直接使用token）');
            process.exit(1);
        }

        // 检查是否有认证信息
        const hasLogin = config.loginId && config.password;
        const hasConfigToken = config.token;
        const hasTokenFile = fs.existsSync(TOKEN_FILE);

        if (!hasLogin && !hasConfigToken && !hasTokenFile) {
            console.error('错误：配置文件需要提供认证信息');
            console.error('');
            console.error('请选择以下方式之一：');
            console.error('方式一：提供 loginId 和 password 进行自动登录');
            console.error('方式二：提供 token 直接使用');
            console.error('方式三：运行 "guanyuan token" 命令手动设置token');
            console.error('');
            process.exit(1);
        }

        return config;
    } catch (e) {
        console.error('错误：解析配置文件失败:', e.message);
        process.exit(1);
    }
}

// Base64 编码
function base64Encode(str) {
    return Buffer.from(str).toString('base64');
}

// 解析 baseUrl，提取 hostname
function parseBaseUrl(baseUrl) {
    // 移除协议前缀 (http:// 或 https://)
    let hostname = baseUrl.replace(/^https?:\/\//, '');
    // 移除端口号和路径
    hostname = hostname.split('/')[0].split(':')[0];
    return hostname;
}

// HTTPS 请求封装
function httpsRequest(options, data = null) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    const response = JSON.parse(body);
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve(response);
                    } else {
                        reject(new Error(`HTTP ${res.statusCode}: ${body}`));
                    }
                } catch (e) {
                    reject(new Error(`解析响应失败: ${body}`));
                }
            });
        });

        req.on('error', reject);

        if (data) {
            req.write(JSON.stringify(data));
        }

        req.end();
    });
}

// 读取保存的 Token
function readToken() {
    try {
        if (fs.existsSync(TOKEN_FILE)) {
            const content = fs.readFileSync(TOKEN_FILE, 'utf-8');
            const data = JSON.parse(content);
            // 检查 token 是否过期
            if (data.expireAt) {
                // 如果有过期时间，检查是否过期
                if (new Date(data.expireAt) > new Date()) {
                    return data.token;
                }
            } else {
                // 如果没有过期时间，直接返回token（用户手动设置的token）
                return data.token;
            }
        }
    } catch (e) {
        // 忽略读取错误
    }
    return null;
}

// 保存 Token
function saveToken(token, expireAt = null) {
    ensureConfigDir();
    try {
        const tokenData = { token };
        if (expireAt) {
            tokenData.expireAt = expireAt;
        }
        fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokenData));
        console.log(`Token 已保存到: ${TOKEN_FILE}`);
    } catch (e) {
        console.error('警告：保存 token 失败:', e.message);
    }
}

// 用户登录
async function signIn(config) {
    console.log(`正在登录观远数据...`);
    console.log(`  服务地址: ${config.baseUrl}`);
    console.log(`  域名: ${config.domain}`);
    console.log(`  用户: ${config.loginId}`);

    const options = {
        hostname: parseBaseUrl(config.baseUrl),
        port: 443,
        path: '/public-api/sign-in',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const data = {
        domain: config.domain,
        loginId: config.loginId,
        password: base64Encode(config.password)
    };

    try {
        const response = await httpsRequest(options, data);
        if (response.result === 'ok' && response.response) {
            const { token, expireAt } = response.response;
            saveToken(token, expireAt);
            console.log('登录成功！');
            console.log(`  过期时间: ${expireAt}`);
            return token;
        } else {
            throw new Error('登录失败：' + JSON.stringify(response));
        }
    } catch (e) {
        console.error('登录错误:', e.message);
        throw e;
    }
}

// 获取有效的 Token（自动刷新）
async function getValidToken(config) {
    // 1. 先尝试从文件读取token
    let token = readToken();
    if (token) {
        return token;
    }

    // 2. 文件中没有token，检查config中是否有token
    if (config.token) {
        console.log('使用配置文件中的Token...');
        // 保存config中的token到文件
        saveToken(config.token);
        return config.token;
    }

    // 3. config中也没有token，尝试使用loginId和password登录
    if (config.loginId && config.password) {
        return await signIn(config);
    }

    // 4. 都没有，报错
    console.error('错误：无法获取Token');
    console.error('');
    console.error('请选择以下方式之一：');
    console.error('方式一：在配置文件中提供 loginId 和 password');
    console.error('方式二：在配置文件中提供 token');
    console.error('方式三：运行 "guanyuan token" 命令手动设置token');
    console.error('');
    process.exit(1);
}

// 获取卡片数据
async function getCardData(cardId, options = {}, config) {
    console.log(`正在获取卡片数据... (卡片ID: ${cardId})`);

    const token = await getValidToken(config);

    const requestOptions = {
        hostname: parseBaseUrl(config.baseUrl),
        port: 443,
        path: `/public-api/card/${cardId}/data`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
    };

    const requestBody = {
        dynamicParams: options.dynamicParams || [],
        filters: options.filters || [],
        offset: options.offset || 0,
        limit: options.limit || 100,
        view: options.view || 'GRAPH'
    };

    try {
        const response = await httpsRequest(requestOptions, requestBody);
        if (response.result === 'ok') {
            console.log('获取卡片数据成功！');
            return response;
        } else {
            // 尝试刷新 token 并重试
            console.log('Token 可能已失效，尝试重新登录...');
            const newToken = await signIn(config);
            requestOptions.headers['X-Auth-Token'] = newToken;
            const retryResponse = await httpsRequest(requestOptions, requestBody);
            if (retryResponse.result === 'ok') {
                console.log('获取卡片数据成功！');
                return retryResponse;
            } else {
                throw new Error('获取卡片数据失败：' + JSON.stringify(retryResponse));
            }
        }
    } catch (e) {
        // 如果是 token 相关错误，尝试重新登录并重试
        if (e.message.includes('401') || e.message.includes('403')) {
            console.log('Token 已失效，尝试重新登录...');
            try {
                const newToken = await signIn(config);
                requestOptions.headers['X-Auth-Token'] = newToken;
                const retryResponse = await httpsRequest(requestOptions, requestBody);
                if (retryResponse.result === 'ok') {
                    console.log('获取卡片数据成功！');
                    return retryResponse;
                }
            } catch (retryError) {
                // 忽略重试错误
            }
        }
        console.error('获取卡片数据错误:', e.message);
        throw e;
    }
}

// CSV 转义函数
function escapeCSV(str) {
    if (str === null || str === undefined) {
        return '';
    }
    const s = String(str);
    // 如果包含逗号、引号、换行符，需要用引号包裹并转义引号
    if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
        return `"${s.replace(/"/g, '""')}"`;
    }
    return s;
}

// 将卡片数据转换为CSV格式
function convertToCSV(cardData, sampleRows = null) {
    const response = cardData.response;
    const chartMain = response.chartMain;

    // 获取行字段（维度）
    const rowMeta = chartMain.row?.meta || [];
    const rowValues = chartMain.row?.values || [];

    // 获取列字段（度量）
    const colMeta = chartMain.column?.meta || [];
    const colValues = chartMain.column?.values || [];

    // 构建表头
    const headers = [];

    // 添加维度列标题
    rowMeta.forEach(field => {
        headers.push(field.title);
    });

    // 添加度量列标题
    colValues.forEach(col => {
        if (Array.isArray(col)) {
            col.forEach(c => {
                headers.push(c.title || c.originTitle || '度量');
            });
        } else {
            headers.push(col.title || col.originTitle || '度量');
        }
    });

    // 构建数据行
    const rows = [];
    const dataLength = rowValues.length;

    // 确定要输出的行数
    const outputRows = sampleRows ? Math.min(dataLength, sampleRows) : dataLength;

    for (let i = 0; i < outputRows; i++) {
        const row = [];

        // 添加维度值
        const rowData = rowValues[i] || [];
        rowMeta.forEach((field, index) => {
            row.push(rowData[index]?.title || '');
        });

        // 添加度量值
        const dataValue = chartMain.data?.[i];
        if (dataValue) {
            if (Array.isArray(dataValue)) {
                dataValue.forEach(v => {
                    row.push(v?.v !== undefined ? v.v : '');
                });
            } else {
                row.push(dataValue?.v !== undefined ? dataValue.v : '');
            }
        } else {
            // 如果没有数据值，根据列数添加空值
            const colCount = colValues.length || 1;
            for (let j = 0; j < colCount; j++) {
                row.push('');
            }
        }

        rows.push(row);
    }

    // 转换为CSV字符串
    const csvRows = [];

    // 添加表头
    csvRows.push(headers.map(h => escapeCSV(h)).join(','));

    // 添加数据行
    rows.forEach(row => {
        csvRows.push(row.map(r => escapeCSV(r)).join(','));
    });

    return csvRows.join('\n');
}

// 提取卡片数据的元数据
function extractMetadata(cardData) {
    const response = cardData.response;
    const chartMain = response.chartMain;

    // 获取行字段（维度）元数据
    const rowMeta = chartMain.row?.meta || [];

    // 获取列字段（度量）元数据
    const colValues = chartMain.column?.values || [];

    const fields = [];

    // 添加维度字段
    rowMeta.forEach(field => {
        fields.push({
            name: field.title,
            originalName: field.originTitle,
            type: field.fdType,
            metaType: field.metaType,
            fieldType: 'dimension',
            fieldId: field.fdId,
            granularity: field.granularity,
            alias: field.alias,
            annotation: field.annotation
        });
    });

    // 添加度量字段
    colValues.forEach(col => {
        if (Array.isArray(col)) {
            col.forEach(c => {
                fields.push({
                    name: c.title || c.originTitle || '度量',
                    originalName: c.originTitle,
                    type: c.fdType,
                    metaType: 'METRIC',
                    fieldType: 'metric',
                    fieldId: c.fdId,
                    alias: c.alias,
                    annotation: c.annotation,
                    format: {
                        specifier: c.fmt_idx,
                        numberFormat: c.numberFormat
                    }
                });
            });
        } else {
            fields.push({
                name: col.title || col.originTitle || '度量',
                originalName: col.originTitle,
                type: col.fdType,
                metaType: 'METRIC',
                fieldType: 'metric',
                fieldId: col.fdId,
                alias: col.alias,
                annotation: col.annotation
            });
        }
    });

    return {
        cardId: null, // 将在调用时设置
        cardType: response.cardType,
        chartType: response.chartType,
        view: response.view,
        exportTime: new Date().toISOString(),
        totalRows: chartMain.count || rowMeta.length,
        dataLimit: chartMain.limit,
        hasMoreData: chartMain.hasMoreData,
        fields: fields
    };
}

// 保存CSV到文件（同时保存元数据）
function saveCSVWithMetadata(csvContent, filename, metadata, cardId) {
    try {
        // 设置卡片ID到元数据
        metadata.cardId = cardId;

        // 保存CSV文件
        fs.writeFileSync(filename, csvContent, 'utf-8');
        console.log(`CSV已保存到: ${filename}`);

        // 生成元数据文件名（同名但扩展名为_meta.json）
        const metaFilename = filename.replace(/\.csv$/i, '') + '_meta.json';

        // 保存元数据文件
        fs.writeFileSync(metaFilename, JSON.stringify(metadata, null, 2), 'utf-8');
        console.log(`元数据已保存到: ${metaFilename}`);

        return true;
    } catch (e) {
        console.error('保存文件失败:', e.message);
        return false;
    }
}

// 显示配置状态
function showConfigStatus() {
    console.log('观远数据配置状态');
    console.log('');

    if (fs.existsSync(CONFIG_FILE)) {
        console.log(`配置文件: ${CONFIG_FILE}`);
        try {
            const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
            console.log(`  服务地址: ${config.baseUrl}`);
            console.log(`  域名: ${config.domain}`);
            console.log(`  用户: ${config.loginId}`);
            console.log(`  密码: ${config.password ? '***已设置***' : '未设置'}`);
        } catch (e) {
            console.log('  (解析失败)');
        }
    } else {
        console.log(`配置文件: 不存在 (${CONFIG_FILE})`);
    }

    console.log('');

    if (fs.existsSync(TOKEN_FILE)) {
        console.log(`Token 文件: ${TOKEN_FILE}`);
        try {
            const tokenData = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf-8'));
            console.log(`  Token: ${tokenData.token ? '***已设置***' : '未设置'}`);
            console.log(`  过期时间: ${tokenData.expireAt || '未知'}`);

            // 检查是否过期
            if (tokenData.expireAt) {
                const expireDate = new Date(tokenData.expireAt);
                const isExpired = expireDate <= new Date();
                console.log(`  状态: ${isExpired ? '已过期' : '有效'}`);
            }
        } catch (e) {
            console.log('  (解析失败)');
        }
    } else {
        console.log(`Token 文件: 不存在 (${TOKEN_FILE})`);
    }
}

// 主函数
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
        case 'login':
        case 'signin': {
            const loginConfig = loadConfig();
            if (!loginConfig.loginId || !loginConfig.password) {
                console.error('错误：配置文件中没有提供 loginId 和 password');
                console.error('');
                console.error('登录需要以下配置：');
                console.error('  - loginId: 登录用户ID');
                console.error('  - password: 登录密码');
                console.error('');
                console.error('如果您想直接使用token，请使用 "guanyuan token" 命令');
                process.exit(1);
            }
            await signIn(loginConfig);
            break;
        }

        case 'token': {
            // 手动设置token命令
            console.log('设置观远数据Token');
            console.log('');

            const userToken = args[1];

            if (userToken) {
                // 从命令行参数获取token
                saveToken(userToken);
                console.log('Token设置成功！');
            } else {
                // 提示用户输入token
                console.log('请输入您的Token（按Enter确认）：');
                console.log('提示：您可以从观远数据Web界面获取Token');
                console.log('');

                // 使用readline从标准输入读取
                const readline = require('readline');
                const rl = readline.createInterface({
                    input: process.stdin,
                    output: process.stdout
                });

                rl.question('Token: ', (token) => {
                    if (token && token.trim()) {
                        saveToken(token.trim());
                        console.log('Token设置成功！');
                        rl.close();
                    } else {
                        console.error('错误：Token不能为空');
                        rl.close();
                        process.exit(1);
                    }
                });

                // 等待用户输入
                return;
            }
            break;
        }

        case 'card':
        case 'get-card': {
            const cardConfig = loadConfig();
            if (!args[1]) {
                console.error('错误：请提供卡片ID');
                console.log('用法: guanyuan card <卡片ID> [选项]');
                console.log('');
                console.log('选项:');
                console.log('  --view <GRAPH|GRID>  数据获取方式（默认: GRAPH）');
                console.log('  --limit <数字>        获取数据条数（默认: 100）');
                console.log('  --offset <数字>       数据起始位置（默认: 0）');
                process.exit(1);
            }

            const cardId = args[1];
            const options = {
                view: 'GRAPH',
                limit: 100,
                offset: 0
            };

            // 解析选项
            for (let i = 2; i < args.length; i++) {
                if (args[i] === '--view' && args[i + 1]) {
                    options.view = args[++i];
                } else if (args[i] === '--limit' && args[i + 1]) {
                    options.limit = parseInt(args[++i]);
                } else if (args[i] === '--offset' && args[i + 1]) {
                    options.offset = parseInt(args[++i]);
                }
            }

            const result = await getCardData(cardId, options, cardConfig);
            console.log('');
            console.log(JSON.stringify(result, null, 2));
            break;
        }

        case 'csv':
        case 'export-csv': {
            const csvConfig = loadConfig();
            if (!args[1]) {
                console.error('错误：请提供卡片ID');
                console.log('用法: guanyuan csv <卡片ID> [选项]');
                console.log('');
                console.log('选项:');
                console.log('  --output <文件名>    输出CSV到文件（默认: 输出到终端）');
                console.log('  --sample <数字>      采样指定行数（默认: 输出所有行）');
                console.log('  --limit <数字>       获取数据条数（默认: 100）');
                console.log('  --view <GRAPH|GRID>  数据获取方式（默认: GRAPH）');
                console.log('');
                console.log('示例:');
                console.log('  guanyuan csv abc123 --output data.csv');
                console.log('  guanyuan csv abc123 --sample 10');
                console.log('  guanyuan csv abc123 --output data.csv --sample 50 --limit 1000');
                process.exit(1);
            }

            const csvCardId = args[1];
            const csvOptions = {
                view: 'GRAPH',
                limit: 100,
                offset: 0
            };
            let outputFile = null;
            let sampleRows = null;

            // 解析选项
            for (let i = 2; i < args.length; i++) {
                if (args[i] === '--output' && args[i + 1]) {
                    outputFile = args[++i];
                } else if (args[i] === '--sample' && args[i + 1]) {
                    sampleRows = parseInt(args[++i]);
                } else if (args[i] === '--view' && args[i + 1]) {
                    csvOptions.view = args[++i];
                } else if (args[i] === '--limit' && args[i + 1]) {
                    csvOptions.limit = parseInt(args[++i]);
                } else if (args[i] === '--offset' && args[i + 1]) {
                    csvOptions.offset = parseInt(args[++i]);
                }
            }

            const csvResult = await getCardData(csvCardId, csvOptions, csvConfig);
            const csvContent = convertToCSV(csvResult, sampleRows);
            const metadata = extractMetadata(csvResult);

            if (outputFile) {
                saveCSVWithMetadata(csvContent, outputFile, metadata, csvCardId);
            } else {
                console.log('');
                console.log(csvContent);
            }
            break;
        }

        case 'status':
            showConfigStatus();
            break;

        case 'config':
        case 'init':
            console.log('初始化观远数据配置');
            console.log('');
            console.log('请创建配置文件: ~/.guanyuan/config.json');
            console.log('');
            console.log('方式一：使用账号密码登录（推荐）');
            console.log('  cat > ~/.guanyuan/config.json << \'EOF\'');
            console.log('  {');
            console.log('    "baseUrl": "https://your-guanyuan-domain.com",');
            console.log('    "domain": "your-domain",');
            console.log('    "loginId": "your-login-id",');
            console.log('    "password": "your-password"');
            console.log('  }');
            console.log('  EOF');
            console.log('');
            console.log('方式二：直接使用Token');
            console.log('  cat > ~/.guanyuan/config.json << \'EOF\'');
            console.log('  {');
            console.log('    "baseUrl": "https://your-guanyuan-domain.com",');
            console.log('    "domain": "your-domain",');
            console.log('    "token": "your-token-here"');
            console.log('  }');
            console.log('  EOF');
            console.log('');
            console.log('方式三：不提供认证信息，使用 "guanyuan token" 命令手动设置');
            console.log('  cat > ~/.guanyuan/config.json << \'EOF\'');
            console.log('  {');
            console.log('    "baseUrl": "https://your-guanyuan-domain.com",');
            console.log('    "domain": "your-domain"');
            console.log('  }');
            console.log('  EOF');
            console.log('  guanyuan token your-token-here');
            console.log('');
            console.log('创建完成后：');
            console.log('  - 使用账号密码：运行 "guanyuan login"');
            console.log('  - 使用token：直接使用 "guanyuan card" 或 "guanyuan csv" 等命令');
            break;

        case 'help':
        case '--help':
        case '-h':
            console.log('观远数据 API 工具');
            console.log('');
            console.log('配置文件: ~/.guanyuan/config.json');
            console.log('Token 文件: ~/.guanyuan/user.token');
            console.log('');
            console.log('认证方式：');
            console.log('  方式一：在配置文件中提供 loginId 和 password，自动登录获取token');
            console.log('  方式二：在配置文件中直接提供 token');
            console.log('  方式三：使用 "guanyuan token" 命令手动设置token');
            console.log('');
            console.log('命令：');
            console.log('  guanyuan init            初始化配置（显示配置说明）');
            console.log('  guanyuan login          使用账号密码登录并获取 token');
            console.log('  guanyuan token [token]  手动设置token（可从参数或交互式输入）');
            console.log('  guanyuan card <id>      获取指定卡片的数据');
            console.log('  guanyuan csv <id>       导出卡片数据为CSV格式');
            console.log('  guanyuan status         显示配置和 token 状态');
            console.log('  guanyuan help           显示帮助信息');
            console.log('');
            console.log('获取卡片数据选项：');
            console.log('  --view <GRAPH|GRID>  数据获取方式（默认: GRAPH）');
            console.log('  --limit <数字>        获取数据条数（默认: 100）');
            console.log('  --offset <数字>       数据起始位置（默认: 0）');
            console.log('');
            console.log('导出CSV选项：');
            console.log('  --output <文件名>    输出CSV到文件（默认: 输出到终端）');
            console.log('  --sample <数字>      采样指定行数（默认: 输出所有行）');
            console.log('');
            console.log('示例：');
            console.log('  guanyuan init');
            console.log('  guanyuan login');
            console.log('  guanyuan token eyJ0eXAiOiJKV1QiLCJhbGci...');
            console.log('  guanyuan card abc123 --view GRID --limit 50');
            console.log('  guanyuan csv abc123 --output data.csv');
            console.log('  guanyuan csv abc123 --sample 10');
            console.log('  guanyuan csv abc123 --output data.csv --sample 50 --limit 1000');
            console.log('  guanyuan status');
            break;

        default:
            if (!command) {
                console.log('使用 "guanyuan help" 查看帮助');
            } else {
                console.error('未知命令:', command);
                console.log('使用 "guanyuan help" 查看帮助');
            }
            process.exit(1);
    }
}

// 运行主函数
main().catch(e => {
    console.error('发生错误:', e.message);
    process.exit(1);
});
