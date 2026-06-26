#!/usr/bin/env node

/**
 * MGTV 视频搜索与播放脚本
 * 
 * 功能：
 * 1. 使用芒果 TV 官方搜索 API 搜索视频资源
 * 2. 智能匹配最相关的视频
 * 3. 检测环境，人类用户无法正常观看时直接推送链接
 * 
 * 使用方法：
 * node search-mgtv.js --query "节目名称"
 */

const https = require('https');
const { spawn } = require('child_process');

// 解析命令行参数
function parseArgs(args) {
  const params = {
    query: '',
    directUrl: '',
    openFirst: false,
    showAll: false
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--query' && args[i + 1]) {
      params.query = args[i + 1];
      i++;
    } else if (args[i] === '--direct-url' && args[i + 1]) {
      params.directUrl = args[i + 1];
      i++;
    } else if (args[i] === '--open-first') {
      params.openFirst = true;
    } else if (args[i] === '--show-all') {
      params.showAll = true;
    }
  }
  
  return params;
}

// HTTP GET 请求
function httpGet(url) {
  return new Promise((resolve, reject) => {
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.mgtv.com/',
        'Origin': 'https://www.mgtv.com'
      }
    };
    
    https.get(url, options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`JSON 解析失败：${e.message}`));
        }
      });
    }).on('error', (e) => {
      reject(new Error(`请求失败：${e.message}`));
    });
  });
}

// 搜索芒果 TV 视频
async function searchMgtv(query) {
  // 芒果 TV 搜索 API
  const baseUrl = 'https://mobileso.bz.mgtv.com/pc/suggest/v1';
  
  // 生成随机 did
  const did = 'f92927c2-' + Math.random().toString(16).substr(2, 4) + '-' + 
              Math.random().toString(16).substr(2, 4) + '-' + 
              Math.random().toString(16).substr(2, 4) + '-' + 
              Math.random().toString(16).substr(2, 12);
  
  // 构建查询参数
  const params = new URLSearchParams({
    allowedRC: '1',
    src: 'mgtv',
    did: did,
    pc: '10',  // 返回 10 个结果
    q: query,
    _support: '10000000'
  });
  
  const url = `${baseUrl}?${params.toString()}`;
  console.log(`正在搜索：${query}...`);
  
  try {
    const result = await httpGet(url);
    
    if (result.code === 200 && result.data && result.data.suggest) {
      return result.data.suggest;
    } else {
      console.log('搜索结果为空或 API 返回错误');
      return [];
    }
  } catch (error) {
    console.error(`搜索失败：${error.message}`);
    return [];
  }
}

// 解析搜索结果，找到最佳播放 URL
function findBestVideoUrl(results, query) {
  if (!results || results.length === 0) {
    return null;
  }
  
  console.log(`\n找到 ${results.length} 个结果:`);
  console.log('='.repeat(60));
  
  // 寻找最佳结果
  let bestResult = null;
  let videoUrl = null;
  
  results.forEach((item, index) => {
    const title = item.showTitle || item.title || '未知';
    const type = item.typeName || `类型${item.type}`;
    
    console.log(`${index + 1}. ${title} (${type})`);
    
    // 优先选择有 videoList 的结果
    if (!bestResult && item.videoList && item.videoList.length > 0) {
      bestResult = item;
      // 获取第一个视频
      videoUrl = item.videoList[0].url;
      console.log(`   └─ 包含视频：${item.videoList[0].title}`);
    }
    
    // 如果没有 videoList，使用 url 字段
    if (!bestResult && item.url) {
      bestResult = item;
      videoUrl = item.url;
    }
    
    // 限制只显示前 5 个
    if (index >= 4) {
      if (results.length > 5) {
        console.log(`... 还有 ${results.length - 5} 个结果`);
      }
      return;
    }
  });
  
  console.log('='.repeat(60));
  
  // 返回 URL
  if (videoUrl) {
    // 转换为完整 URL
    if (videoUrl.startsWith('//')) {
      videoUrl = 'https:' + videoUrl;
    } else if (!videoUrl.startsWith('http')) {
      videoUrl = 'https://www.mgtv.com' + videoUrl;
    }
    
    console.log(`\n✓ 选择：${bestResult.showTitle || bestResult.title}`);
    return videoUrl;
  }
  
  return null;
}

// 检测是否为无头环境（人类用户无法正常观看视频）
function isHeadlessEnvironment() {
  // 检查常见无头环境变量
  if (process.env.HEADLESS === 'true') return true;
  if (process.env.CI === 'true') return true;  // CI/CD 环境
  if (process.env.DISPLAY === undefined && process.platform === 'linux') return true;  // Linux 无图形界面
  if (process.env.ELECTRON_RUN_AS_NODE === '1') return true;  // Electron 环境
  
  return false;
}

// 输出播放链接（人类用户手动打开）
function outputVideoLink(url, message = '播放链接：') {
  console.log('\n' + '='.repeat(60));
  console.log('📺 ' + message);
  console.log('='.repeat(60));
  console.log(url);
  console.log('='.repeat(60));
  console.log('\n💡 提示：');
  console.log('  1. 复制上面的链接');
  console.log('  2. 在浏览器中打开');
  console.log('  3. 享受观看！');
  console.log('='.repeat(60) + '\n');
}

// 在系统浏览器中打开 URL（无头环境直接推送链接）
function openInBrowser(url) {
  // 如果是无头环境，直接推送链接
  if (isHeadlessEnvironment()) {
    console.log('\n检测到无头环境，无法打开浏览器');
    outputVideoLink(url, '请在浏览器中打开以下链接观看视频：');
    return false;
  }

  const platform = process.platform;
  const command = platform === 'darwin' ? 'open'
                  : platform === 'win32'  ? 'cmd'
                  : platform === 'linux'  ? 'xdg-open'
                  : null;

  if (!command) {
    console.error(`不支持的操作系统：${platform}`);
    outputVideoLink(url, '请在浏览器中打开以下链接观看视频：');
    return false;
  }

  console.log(`\n正在打开浏览器：${url}`);

  const args = platform === 'win32' ? ['/c', 'start', '', url] : [url];
  const child = spawn(command, args, { stdio: 'ignore', detached: true });

  child.on('error', (err) => {
    console.error(`打开浏览器失败：${err.message}`);
    outputVideoLink(url, '请在浏览器中打开以下链接观看视频：');
  });

  child.unref();
  console.log('✓ 已在浏览器中打开');
  return true;
}

// 解析芒果 TV 播放页面 URL
function parseMgtvUrl(inputUrl) {
  // 如果已经是芒果 TV 的 URL，直接返回
  if (inputUrl.includes('mgtv.com')) {
    if (inputUrl.startsWith('//')) {
      return 'https:' + inputUrl;
    }
    return inputUrl;
  }
  
  // 尝试提取视频 ID 并构建 URL
  const match = inputUrl.match(/b\/(\d+)\/(\d+)/);
  if (match) {
    return `https://www.mgtv.com/b/${match[1]}/${match[2]}.html`;
  }
  
  return null;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);
  
  console.log('='.repeat(60));
  console.log('MGTV - 芒果 TV 视频搜索与播放');
  console.log('='.repeat(60));
  
  let targetUrl;
  
  if (params.directUrl) {
    // 直接打开指定的 URL
    console.log(`打开指定 URL: ${params.directUrl}`);
    targetUrl = parseMgtvUrl(params.directUrl) || params.directUrl;
    
    console.log('='.repeat(60));
    
    // 在浏览器中打开或推送链接
    const success = await openInBrowser(targetUrl);
    
    if (success) {
      console.log('\n✓ 操作完成！正在播放视频，享受观看！');
    } else {
      console.log('\n⚠️  已推送链接，请手动打开。');
    }
    
  } else if (params.query) {
    // 搜索并打开
    console.log(`搜索关键词：${params.query}`);
    console.log('='.repeat(60));
    
    // 搜索视频
    const results = await searchMgtv(params.query);
    
    if (!results || results.length === 0) {
      console.log('\n未找到相关视频，请尝试其他关键词');
      process.exit(0);
    }
    
    // 找到最佳视频 URL
    targetUrl = findBestVideoUrl(results, params.query);
    
    if (!targetUrl) {
      console.log('\n无法获取视频播放地址');
      console.log('\n正在打开搜索页面...');
      targetUrl = `https://www.mgtv.com/?q=${encodeURIComponent(params.query)}`;
    }
    
    console.log('='.repeat(60));
    
    // 如果使用了 --show-all，打开搜索页面让用户选择
    if (params.showAll) {
      targetUrl = `https://www.mgtv.com/?q=${encodeURIComponent(params.query)}`;
    }
    
    // 在浏览器中打开或推送链接
    const success = await openInBrowser(targetUrl);
    
    if (success) {
      console.log('\n✓ 操作完成！');
      if (params.showAll || !findBestVideoUrl(results, params.query)) {
        console.log('已在芒果 TV 搜索页面中显示结果，请选择想要观看的视频。');
      } else {
        console.log('正在播放视频，享受观看！');
      }
    } else {
      console.log('\n⚠️  已推送链接，请手动打开。');
    }
    
  } else {
    console.error('错误：必须提供 --query 或 --direct-url 参数');
    console.error('使用方法：');
    console.error('  node search-mgtv.js --query "节目名称"');
    console.error('  node search-mgtv.js --direct-url "https://www.mgtv.com/b/xxx/xxx.html"');
    console.error('示例：');
    console.error('  node search-mgtv.js --query "乘风破浪的姐姐"');
    process.exit(1);
  }
}

// 运行主函数
main().catch(error => {
  console.error('发生错误:', error.message);
  process.exit(1);
});
