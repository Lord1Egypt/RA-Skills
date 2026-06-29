#!/usr/bin/env node
/**
 * Free Search Engine - 免费搜索引擎（Node.js版本）
 * 无需 API Key，无需Python，安装即用
 * 支持引擎：必应中国、搜狗、360搜索
 */

const axios = require('axios');
const cheerio = require('cheerio');
const { URL } = require('url');

class FreeSearch {
    constructor() {
        this.session = axios.create({
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            },
            timeout: 15000,
            maxRedirects: 5
        });
    }

    /**
     * 必应中国搜索
     * @param {string} keyword 搜索关键词
     * @param {number} maxResults 最大结果数
     * @returns {Array} 搜索结果
     */
    async searchBingCn(keyword, maxResults = 10) {
        try {
            const url = `https://cn.bing.com/search?q=${encodeURIComponent(keyword)}&count=${maxResults}`;
            const response = await this.session.get(url);
            const $ = cheerio.load(response.data);
            
            const results = [];
            $('.b_algo').each((i, el) => {
                if (i >= maxResults) return false;
                const title = $(el).find('h2').text().trim();
                const url = $(el).find('h2 a').attr('href');
                const snippet = $(el).find('.b_caption p').text().trim();
                
                if (title && url && snippet) {
                    results.push({
                        title,
                        url,
                        snippet,
                        engine: 'bing-cn'
                    });
                }
            });
            
            return results;
        } catch (err) {
            console.log(`⚠️ 必应搜索失败: ${err.message}`);
            return [];
        }
    }

    /**
     * 搜狗搜索
     * @param {string} keyword 搜索关键词
     * @param {number} maxResults 最大结果数
     * @returns {Array} 搜索结果
     */
    async searchSogou(keyword, maxResults = 10) {
        try {
            const url = `https://www.sogou.com/web?query=${encodeURIComponent(keyword)}&num=${maxResults}`;
            const response = await this.session.get(url);
            const $ = cheerio.load(response.data);
            
            const results = [];
            $('.results .vrwrap').each((i, el) => {
                if (i >= maxResults) return false;
                const title = $(el).find('h3').text().trim();
                const url = $(el).find('h3 a').attr('href');
                const snippet = $(el).find('.fz-mid').text().trim();
                
                // 处理搜狗跳转链接
                if (url && url.startsWith('/link?')) {
                    const fullUrl = new URL(url, 'https://www.sogou.com').href;
                    results.push({
                        title,
                        url: fullUrl,
                        snippet,
                        engine: 'sogou'
                    });
                } else if (title && url && snippet) {
                    results.push({
                        title,
                        url,
                        snippet,
                        engine: 'sogou'
                    });
                }
            });
            
            return results;
        } catch (err) {
            console.log(`⚠️ 搜狗搜索失败: ${err.message}`);
            return [];
        }
    }

    /**
     * 360搜索
     * @param {string} keyword 搜索关键词
     * @param {number} maxResults 最大结果数
     * @returns {Array} 搜索结果
     */
    async searchSo360(keyword, maxResults = 10) {
        try {
            const url = `https://www.so.com/s?q=${encodeURIComponent(keyword)}&pn=1&num=${maxResults}`;
            const response = await this.session.get(url);
            const $ = cheerio.load(response.data);
            
            const results = [];
            $('.res-list').each((i, el) => {
                if (i >= maxResults) return false;
                const title = $(el).find('h3').text().trim();
                const url = $(el).find('h3 a').attr('href');
                const snippet = $(el).find('.res-desc').text().trim();
                
                if (title && url && snippet) {
                    results.push({
                        title,
                        url,
                        snippet,
                        engine: 'so360'
                    });
                }
            });
            
            return results;
        } catch (err) {
            console.log(`⚠️ 360搜索失败: ${err.message}`);
            return [];
        }
    }

    /**
     * 自动选择可用引擎搜索
     * @param {string} keyword 搜索关键词
     * @param {number} maxResults 最大结果数
     * @param {string} engine 指定引擎（可选：bing-cn/sogou/so360/free）
     * @returns {Array} 搜索结果
     */
    async search(keyword, maxResults = 10, engine = 'free') {
        const engines = [];
        
        if (engine === 'free' || engine === 'bing-cn') engines.push(this.searchBingCn(keyword, maxResults));
        if (engine === 'free' || engine === 'sogou') engines.push(this.searchSogou(keyword, maxResults));
        if (engine === 'free' || engine === 'so360') engines.push(this.searchSo360(keyword, maxResults));
        
        // 并发搜索所有引擎
        const allResults = await Promise.all(engines);
        let merged = allResults.flat();
        
        // 去重（按URL）
        const seen = new Set();
        merged = merged.filter(item => {
            if (seen.has(item.url)) return false;
            seen.add(item.url);
            return true;
        });
        
        // 按相关性排序（简单按长度权重）
        merged.sort((a, b) => {
            const scoreA = a.title.length + a.snippet.length;
            const scoreB = b.title.length + b.snippet.length;
            return scoreB - scoreA;
        });
        
        return merged.slice(0, maxResults);
    }
}

module.exports = FreeSearch;

// 直接运行测试
if (require.main === module) {
    (async () => {
        const fs = new FreeSearch();
        const results = await fs.search('OpenClaw 技能', 5);
        console.log(JSON.stringify(results, null, 2));
    })();
}
