#!/usr/bin/env node
/**
 * Search Pro - Content Extractor (Node.js 版本)
 * 无需Python环境，直接使用OpenClaw内置Node.js运行
 * 
 * Usage: node extract.js --url https://example.com
 */

const axios = require('axios');
const cheerio = require('cheerio');
const { URL } = require('url');
const dns = require('dns').promises;
const net = require('net');

// 内网IP范围
const PRIVATE_NETWORKS = [
    { start: '10.0.0.0', end: '10.255.255.255' },
    { start: '172.16.0.0', end: '172.31.255.255' },
    { start: '192.168.0.0', end: '192.168.255.255' },
    { start: '127.0.0.0', end: '127.255.255.255' },
    { start: '0.0.0.0', end: '0.255.255.255' },
    { start: '169.254.0.0', end: '169.254.255.255' }
];

// IP转数字
function ipToNum(ip) {
    return ip.split('.').reduce((acc, octet) => (acc << 8) + parseInt(octet, 10), 0);
}

// 检查是否为私有IP
function isPrivateIp(ip) {
    const ipNum = ipToNum(ip);
    return PRIVATE_NETWORKS.some(network => {
        return ipNum >= ipToNum(network.start) && ipNum <= ipToNum(network.end);
    });
}

// 解析并检查主机名
async function resolveAndCheckHostname(hostname) {
    try {
        const addresses = await dns.resolve4(hostname);
        for (const addr of addresses) {
            if (isPrivateIp(addr)) {
                console.log(`⚠️  警告：${hostname} 解析到内网 IP: ${addr}`);
                return true;
            }
        }
        return false;
    } catch (err) {
        console.log(`⚠️  警告：无法解析主机名 ${hostname}`);
        return true;
    }
}

// 验证URL安全
async function validateUrl(url) {
    try {
        const parsed = new URL(url);
        
        // 检查协议
        if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
            return { safe: false, error: `不支持的协议：${parsed.protocol}（仅支持 http/https）` };
        }
        
        const hostname = parsed.hostname;
        if (!hostname) {
            return { safe: false, error: '无效的主机名' };
        }
        
        // 检查本地主机名
        const localhostNames = ['localhost', 'localhost.localdomain', 'internal', 'intranet'];
        if (localhostNames.includes(hostname.toLowerCase())) {
            return { safe: false, error: `不允许访问内网主机：${hostname}` };
        }
        
        // 检查是否为IP地址
        if (net.isIP(hostname)) {
            if (isPrivateIp(hostname)) {
                return { safe: false, error: `不允许访问内网 IP: ${hostname}` };
            }
        } else {
            // 域名解析检查
            if (await resolveAndCheckHostname(hostname)) {
                return { safe: false, error: `域名解析到内网地址：${hostname}` };
            }
        }
        
        // 检查内网域名模式
        const internalPatterns = [/\.local$/, /\.internal$/, /\.intranet$/, /\.lan$/, /\.private$/];
        if (internalPatterns.some(pattern => pattern.test(hostname.toLowerCase()))) {
            return { safe: false, error: `检测到内网域名：${hostname}` };
        }
        
        return { safe: true };
    } catch (err) {
        return { safe: false, error: `URL 解析失败：${err.message}` };
    }
}

// 提取网页内容
async function extractFromUrl(url) {
    console.log("📄 Search Pro - Content Extractor (Node.js 版本)");
    console.log("=".repeat(50));
    console.log(`🔗 提取 URL: ${url}`);
    
    const validation = await validateUrl(url);
    if (!validation.safe) {
        console.log(`❌ 错误：${validation.error}`);
        console.log("\n安全限制:");
        console.log("  - 仅支持 http:// 和 https:// 协议");
        console.log("  - 不支持 file:// 或其他协议");
        console.log("  - 不访问内网地址（localhost, 127.x.x.x, 192.168.x.x 等）");
        console.log("  - 不访问 .local, .internal, .intranet 等内网域名");
        return false;
    }
    
    console.log("\n✅ URL 验证通过，正在提取内容...");
    
    try {
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            timeout: 10000,
            responseType: 'text'
        });
        
        const $ = cheerio.load(response.data);
        // 移除无用标签
        $('script, style, nav, footer, header, aside, iframe, noscript').remove();
        // 提取正文
        const text = $('body').text().replace(/\s+/g, ' ').trim();
        
        console.log("\n📝 提取内容摘要（前500字符）：");
        console.log(text.substring(0, 500) + (text.length > 500 ? "..." : ""));
        console.log(`\n✅ 提取完成，总字符数：${text.length}`);
        
        return true;
    } catch (err) {
        console.log(`❌ 提取失败：${err.message}`);
        return false;
    }
}

// 主函数
async function main() {
    const args = process.argv.slice(2);
    const urlIndex = args.indexOf('--url');
    
    if (urlIndex === -1 || !args[urlIndex + 1]) {
        console.log("用法：node extract.js --url <URL>");
        console.log("\n示例:");
        console.log("  node extract.js --url https://example.com");
        console.log("\n特点：无需Python环境，直接运行");
        return;
    }
    
    const url = args[urlIndex + 1];
    const success = await extractFromUrl(url);
    process.exit(success ? 0 : 1);
}

main().catch(err => {
    console.error("❌ 运行错误：", err);
    process.exit(1);
});
