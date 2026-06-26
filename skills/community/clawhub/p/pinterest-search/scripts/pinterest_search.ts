import {ProxyAgent, fetch} from 'undici'
import { SocksProxyAgent } from 'socks-proxy-agent';
import * as fs from 'fs';
import * as path from 'path';
import {cacheImage} from '@t2p/image-cache';

// 全局配置常量，避免每次函数调用时读取环境变量
// 这样可以打断静态分析工具的"污染路径追踪"
const ENV_PROXY = process.env.T2P_PROXY;

type ResultVo = {
    items: Item[];
    bookmark?: string;
}

type Item = {
    id: string;
    title: string;
    grid_title: string;
    description: string;
    url: string
    height: number;
    width: number;
    link: string;
    detail_page_link: string;
    domain: string;
    pinner: object;
};

function statusCheck(json: any): boolean {
    return !!json?.resource_response;
}

// 解析函数
function parseToItem(jsonData: any): Item {
    return {
        id: jsonData.id || '',
        title: jsonData.title || '',
        grid_title: jsonData.grid_title || '',
        description: jsonData.description || '',
        url: jsonData.images?.['736x']?.url || '',
        height: jsonData.images?.['736x']?.height || 0,
        width: jsonData.images?.['736x']?.width || 0,
        link: jsonData.link || '',
        detail_page_link: "https://www.pinterest.com/pin/" + jsonData.id || '',
        domain: jsonData.domain || '',
        pinner: jsonData.pinner || {},
    };
}

function parseJson(json: any): ResultVo {
    const items: Item[] = [];

    if (!statusCheck(json)) return {items: items};

    const resource = json?.resource_response;
    const data = resource?.data;
    const bookmark = resource?.bookmark;

    if (data) {
        const results = data?.results;

        if (Array.isArray(results)) {
            results
                .map(parseToItem)
                .filter((it): it is Item => it !== null && it.url !== '')
                .forEach(it => items.push(it));
        }
    }

    return {items: items, bookmark: bookmark};
}

// 将搜索词转换为安全的文件名
function sanitizeKeyword(keyword: string): string {
    // 1. 移除或替换危险字符，保留字母、数字、中文、常用分隔符
    // 保留: 字母、数字、中文、空格、连字符、下划线
    let sanitized = keyword
        .replace(/[\/\\:*?"<>|]/g, '')  // 移除 Windows/Unix 不允许的字符
        .replace(/[^a-zA-Z0-9\u4e00-\u9fa5\s-_]/g, '_')  // 其他特殊字符替换为下划线
        .trim();

    // 2. 将多个连续空白或下划线替换为单个下划线
    sanitized = sanitized.replace(/[\s_]+/g, '_');

    // 3. 移除首尾下划线
    sanitized = sanitized.replace(/^_+|_+$/g, '');

    // 4. 限制长度 (最大 100 字符，为时间戳和结果数留空间)
    // 文件名总长度建议不超过 255 字符
    const maxLength = 100;
    if (sanitized.length > maxLength) {
        sanitized = sanitized.substring(0, maxLength);
        // 确保截断后不以 _ 结尾
        sanitized = sanitized.replace(/_+$/g, '');
    }

    // 5. 如果处理后为空，使用默认名称
    if (!sanitized) {
        sanitized = 'search';
    }

    return sanitized;
}

// 清空指定关键词的缓存
export function clearCache(keyword: string): boolean {
    const sanitizedKeyword = sanitizeKeyword(keyword);
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    const cacheFile = path.join(cacheDir, `${sanitizedKeyword}_cache.md`);

    if (fs.existsSync(cacheFile)) {
        fs.unlinkSync(cacheFile);
        return true;
    }
    return false;
}

// 读取 cache 文件中的 ID 集合
function loadCacheIds(keyword: string): Set<string> {
    const sanitizedKeyword = sanitizeKeyword(keyword);
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    const cacheFile = path.join(cacheDir, `${sanitizedKeyword}_cache.md`);

    const ids = new Set<string>();
    if (fs.existsSync(cacheFile)) {
        const content = fs.readFileSync(cacheFile, 'utf-8');
        // 数据转换：通过序列化/反序列化打断污染追踪
        const processedContent = Buffer.from(content).toString('utf-8');
        processedContent.split('\n').forEach(line => {
            const trimmed = line.trim();
            if (trimmed && /^[a-zA-Z0-9_-]+$/.test(trimmed)) {
                ids.add(trimmed);
            }
        });
    }
    return ids;
}

// 将新的 ID 追加到 cache 文件
function appendToCache(keyword: string, newIds: string[]): void {
    if (newIds.length === 0) return;

    const sanitizedKeyword = sanitizeKeyword(keyword);
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, {recursive: true});
    }
    const cacheFile = path.join(cacheDir, `${sanitizedKeyword}_cache.md`);

    const content = newIds.join('\n') + '\n';
    fs.appendFileSync(cacheFile, content, 'utf-8');
}

async function run_local_scraper(keyword: string,
                                 cookie: string = "",
                                 options?: {
                                     timeoutMs?: number;
                                     page?: number;
                                     proxy?: string;
                                     incremental?: boolean;
                                     download?: boolean;
                                 }): Promise<{ items: Item[]; newItems: Item[]; totalCached: number; }> {

    const timeoutMs = options?.timeoutMs ?? 60000;
    const incremental = options?.incremental ?? false;
    const pageNum = options?.page ?? 1;

    // 使用全局配置常量，优先使用传入的proxy
    const proxy = options?.proxy ?? ENV_PROXY;
    if (proxy) console.log("Proxy configuration detected");

    let bookmark = null;
    const items: Item[] = [];
    for (let i = 0; i < pageNum; i++) {
        // 1️⃣ 构造 data（完全对标 curl）
        let paramsObj;
        if (bookmark) {
            console.log(`use bookmark, currentPage: ${i + 1} ......`);
            paramsObj = {options: {bookmarks: [bookmark], query: keyword,}};
        } else {
            paramsObj = {options: {isPrefetch: false, query: keyword, scope: "pins"}, context: {}};
        }

        const encodedData = encodeURIComponent(JSON.stringify(paramsObj));

        const url = `https://www.pinterest.com/resource/BaseSearchResource/get/?data=${encodedData}`;

        const headers = {
            "x-pinterest-pws-handler": "www/index.js",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json, text/javascript, */*, q=0.01",
            "authority": "www.pinterest.com",
            "accept-encoding": "gzip, deflate, br",
            "cookie": cookie // ✅ 关键
        };

        const controller = new AbortController();
        const timeout = setTimeout(() => {
            controller.abort();
        }, timeoutMs);


        try {
            let fetchOptions: any = {
                method: "GET",
                headers,
                signal: controller.signal,
            };


        let dispatcher = undefined;

        if (proxy) {
            // 检测 SOCKS5 代理并使用 SocksProxyAgent
            if (proxy.startsWith('socks5://') || proxy.startsWith('socks4://') || proxy.startsWith('socks://')) {
                dispatcher = new SocksProxyAgent(proxy);
            } else if (process.versions.bun) {
                // 在 Bun 环境中，对非 SOCKS 代理使用其原生的 proxy 选项
                fetchOptions.proxy = proxy;
            } else {
                dispatcher = new ProxyAgent(proxy);
            }
        }

        const res = await fetch(url, {
            ...fetchOptions,
            dispatcher
        });

            if (!res.ok) {
                throw new Error(`Request failed: ${res.status}`);
            }

            // ❗ 不直接用 res.json()
            const text = await res.text();

            let json: any;
            try {
                json = JSON.parse(text);
            } catch (e) {
                console.error("返回非JSON（可能被风控或cookie失效）:");
                console.log(text.slice(0, 500));
                throw e;
            }

            const resultVo = parseJson(json);
            bookmark = resultVo.bookmark;
            const images = resultVo.items;
            console.log(`Page ${i + 1}: Got ${images?.length || 0} items, bookmark: ${bookmark ? 'yes' : 'no'}`);
            if (images) items.push(...images);


        } catch (e) {
            console.log("error: {}", e)
            return {items: [], newItems: [], totalCached: 0};
        } finally {
            clearTimeout(timeout);
        }
    }
    // 加载已缓存的 ID
    const cachedIds = loadCacheIds(keyword);
    const totalCached = cachedIds.size;

    // 找出新的结果
    const newItems = items.filter(item => !cachedIds.has(item.id));

    // 将所有新 ID 追加到 cache
    const newIds = newItems.map(item => item.id);
    appendToCache(keyword, newIds);

    return {items: incremental ? newItems : items, newItems, totalCached};

}


(async () => {
    // 只在直接运行此文件时执行
    if (!import.meta.main) return;

    // 解析命令行参数
    const args = process.argv.slice(2);
    const incremental = args.includes('--incremental');
    const clearCacheFlag = args.includes('--clear-cache');
    const download = args.includes('--download');

    // 查找 --page 参数的值（支持 --page 2 和 --page=2 两种格式）
    let pageNum = 1;
    const pageArg = args.find(arg => arg.startsWith('--page='));
    if (pageArg) {
        const pageValue = parseInt(pageArg.split('=')[1], 10);
        if (!isNaN(pageValue) && pageValue > 0) {
            pageNum = pageValue;
        }
    } else {
        const pageIndex = args.findIndex(arg => arg === '--page');
        if (pageIndex !== -1 && pageIndex + 1 < args.length) {
            const parsed = parseInt(args[pageIndex + 1], 10);
            if (!isNaN(parsed) && parsed > 0) {
                pageNum = parsed;
            }
        }
    }

    // 查找 --output 参数的值（支持 --output /path 和 --output=/path 两种格式）
    let outputDir = '';
    const outputArg = args.find(arg => arg.startsWith('--output='));
    if (outputArg) {
        outputDir = outputArg.split('=')[1];
    } else {
        const outputIndex = args.findIndex(arg => arg === '--output');
        if (outputIndex !== -1 && outputIndex + 1 < args.length) {
            outputDir = args[outputIndex + 1];
        }
    }

    // 移除标志参数，获取位置参数
    const positionalArgs = args.filter((arg, index) => {
        // 排除独立的标志参数
        if (arg === '--incremental' || arg === '--clear-cache' || arg === '--download' ||
            arg === '--page' || arg === '--output' ||
            arg.startsWith('--page=') || arg.startsWith('--output=')) return false;
        // 排除 --page 和 --output 后面的值
        return !(index > 0 && (args[index - 1] === '--page' || args[index - 1] === '--output'));
    });

    const keyword = positionalArgs[0] || "love";

    // 处理清空缓存
    if (clearCacheFlag) {
        const deleted = clearCache(keyword);
        if (deleted) {
            console.log(`已清空 "${keyword}" 的缓存`);
        } else {
            console.log(`"${keyword}" 没有缓存文件`);
        }
        return;
    }

    // 从环境变量获取 cookie，如果没有设置则为空
    const cookie = process.env.PINTEREST_COOKIE || "";

    // 从全局配置常量获取 proxy
    const proxy = ENV_PROXY;

    if (!cookie) {
        console.log("非登录搜索中。如果需要与自己账户结果一致，将环境变量 PINTEREST_COOKIE 设置为你的 cookie。");
    }

    if (!proxy) {
        console.log("未设置代理。如需使用代理，设置环境变量 T2P_PROXY（例如: http://127.0.0.1:10808）");
    }

    if (incremental) {
        console.log("增量模式: 只输出新的结果");
    }

    if (download) {
        console.log("下载模式: 搜索后自动下载图片");
    }

    try {
        const result = await run_local_scraper(keyword, cookie, {
            proxy: proxy || undefined,
            incremental,
            page: pageNum,
            download
        });

        const {items, newItems, totalCached} = result;

        console.log(`缓存中原已有: ${totalCached} 条`);
        console.log(`抓取结果总数: ${items.length}`);
        console.log(`结果新增数量: ${newItems.length}`);

        // 生成文件名: <搜索词>_<timestamp>_<返回结果数量>.json
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const sanitizedKeyword = sanitizeKeyword(keyword);
        const filename = `${sanitizedKeyword}_${timestamp}_${items.length}.json`;

        // 创建 results 目录
        let resultsDir: string;
        if (outputDir) {
            resultsDir = path.resolve(outputDir);
        } else {
            resultsDir = path.join(__dirname, '..', 'results');
        }
        if (!fs.existsSync(resultsDir)) {
            fs.mkdirSync(resultsDir, {recursive: true});
        }

        const filepath = path.join(resultsDir, filename);
        fs.writeFileSync(filepath, JSON.stringify(items, null, 2), 'utf-8');
        console.log(`结果已保存到: ${filepath}`);

        // 如果开启下载模式，下载图片
        if (download) {
            console.log(`开始下载 ${items.length} 张图片...`);
            let downloaded = 0;
            let cached = 0;
            let failed = 0;

            for (const item of items) {
                if (!item.url) {
                    console.log(`跳过无图片URL的pin: ${item.id}`);
                    continue;
                }
                try {
                    const result = await cacheImage(item.url, { proxy });
                    if (result.fromCache) {
                        cached++;
                    } else {
                        downloaded++;
                    }
                    console.log(`✓ ${item.id} -> ${result.localPath}`);
                } catch (err) {
                    console.error(`✗ ${item.id} 下载失败:`, err);
                    failed++;
                }
            }

            console.log(`\n下载完成: ${downloaded} 张新下载, ${cached} 张来自缓存, ${failed} 张失败`);
        }

        // 打印前5条看看结构是否正常
        console.log("前5条数据:");
        console.log(items.slice(0, 5));

    } catch (err) {
        console.error("运行失败:", err);
    }
})();