/**
 * 热点雷达 - 数据采集器 v4
 * 微博: 官方API
 * 知乎/抖音/B站: 洛樱云API
 * 小红书: 60s API (v2/rednote)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  dataDir: path.join(__dirname, '../data'),
  historyDir: path.join(__dirname, '../data/history'),
  configDir: path.join(__dirname, '../config'),
  // API接口地址
  API: {
    // 微博官方API
    WEIBO: 'https://weibo.com/ajax/statuses/hot_band',
    // 洛樱云API - 知乎、抖音、B站
    LUOYING: 'https://apiserver.alcex.cn/daily-hot/',
  }
};

// 确保目录存在
function ensureDirs() {
  var dirs = [
    CONFIG.dataDir,
    CONFIG.historyDir,
    path.join(CONFIG.historyDir, 'weibo'),
    path.join(CONFIG.historyDir, 'zhihu'),
    path.join(CONFIG.historyDir, 'bilibili'),
    path.join(CONFIG.historyDir, 'douyin'),
    path.join(CONFIG.historyDir, 'xiaohongshu'),
    path.join(CONFIG.dataDir, 'trends'),
    CONFIG.configDir,
  ];
  dirs.forEach(function(dir) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// HTTP请求封装
function fetch(url, options) {
  return new Promise(function(resolve, reject) {
    var protocol = url.startsWith('https') ? https : require('http');
    var requestOptions = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html',
        'Referer': 'https://weibo.com',
      },
      timeout: 15000,
    };

    protocol.get(url, requestOptions, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data });
        }
      });
    }).on('error', function(err) {
      reject(err);
    });
  });
}

// 获取微博热搜
async function fetchWeibo() {
  try {
    console.log('  [微博] 开始获取...');
    var data = await fetch(CONFIG.API.WEIBO);
    var items = data.data && data.data.band_list ? data.data.band_list : [];
    var result = items.map(function(item, idx) {
      return {
        rank: idx + 1,
        topic: item.word || item.topic_name,
        hotValue: item.raw_hot || item.num || 0,
        label: item.label_name || '',
        url: 'https://s.weibo.com/weibo?q=' + encodeURIComponent(item.word || item.topic_name)
      };
    });
    console.log('  [微博] 获取成功: ' + result.length + '条');
    return result;
  } catch (e) {
    console.log('  [微博] 获取失败: ' + e.message);
    return [];
  }
}

// 获取知乎热搜 - 使用洛樱云API
async function fetchZhihu() {
  try {
    console.log('  [知乎] 开始获取...');
    var data = await fetch(CONFIG.API.LUOYING + 'zhihu');
    if (data.code === 200 && data.data) {
      var result = data.data.map(function(item, idx) {
        return {
          rank: idx + 1,
          topic: item.title,
          hotValue: item.hot || 0,
          label: '',
          url: item.url || ''
        };
      });
      console.log('  [知乎] 获取成功: ' + result.length + '条');
      return result;
    }
    console.log('  [知乎] 接口返回异常');
    return [];
  } catch (e) {
    console.log('  [知乎] 获取失败: ' + e.message);
    return [];
  }
}

// 获取B站热搜 - 使用洛樱云API
async function fetchBilibili() {
  try {
    console.log('  [B站] 开始获取...');
    var data = await fetch(CONFIG.API.LUOYING + 'bilibili');
    if (data.code === 200 && data.data) {
      var result = data.data.map(function(item, idx) {
        return {
          rank: idx + 1,
          topic: item.title,
          hotValue: item.hot || 0,
          label: item.desc || '',
          url: item.url || ''
        };
      });
      console.log('  [B站] 获取成功: ' + result.length + '条');
      return result;
    }
    console.log('  [B站] 接口返回异常');
    return [];
  } catch (e) {
    console.log('  [B站] 获取失败: ' + e.message);
    return [];
  }
}

// 获取抖音热搜 - 使用洛樱云API
async function fetchDouyin() {
  try {
    console.log('  [抖音] 开始获取...');
    var data = await fetch(CONFIG.API.LUOYING + 'douyin');
    if (data.code === 200 && data.data) {
      var result = data.data.map(function(item, idx) {
        return {
          rank: idx + 1,
          topic: item.title,
          hotValue: item.hot || 0,
          label: '',
          url: item.url || ''
        };
      });
      console.log('  [抖音] 获取成功: ' + result.length + '条');
      return result;
    }
    console.log('  [抖音] 接口返回异常');
    return [];
  } catch (e) {
    console.log('  [抖音] 获取失败: ' + e.message);
    return [];
  }
}

// 获取小红书热搜 - 使用60s API (v2)
async function fetchXiaohongshu() {
  try {
    console.log('  [小红书] 开始获取...');
    var data = await fetch('https://60s.viki.moe/v2/rednote');
    if (data.code === 200 && data.data) {
      var result = data.data.map(function(item, idx) {
        return {
          rank: item.rank || idx + 1,
          topic: item.title,
          hotValue: item.score || 0,
          label: item.word_type || '',
          url: item.link || ''
        };
      });
      console.log('  [小红书] 获取成功: ' + result.length + '条');
      return result;
    }
    console.log('  [小红书] 接口返回异常');
    return [];
  } catch (e) {
    console.log('  [小红书] 获取失败: ' + e.message);
    return [];
  }
}

// 获取所有平台热榜
async function fetchAll() {
  console.log('\n开始采集全网热榜...\n');

  var results = await Promise.all([
    fetchWeibo(),
    fetchZhihu(),
    fetchBilibili(),
    fetchDouyin(),
    fetchXiaohongshu()
  ]);

  var data = {
    weibo: results[0] || [],
    zhihu: results[1] || [],
    bilibili: results[2] || [],
    douyin: results[3] || [],
    xiaohongshu: results[4] || [],
    timestamp: new Date().toISOString()
  };

  console.log('\n采集完成:', {
    weibo: data.weibo.length,
    zhihu: data.zhihu.length,
    bilibili: data.bilibili.length,
    douyin: data.douyin.length,
    xiaohongshu: data.xiaohongshu.length
  });

  return data;
}

// 保存历史数据
function saveHistory(data) {
  var today = new Date().toISOString().split('T')[0];
  var platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];

  platforms.forEach(function(platform) {
    var filePath = path.join(CONFIG.historyDir, platform, today + '.json');
    fs.writeFileSync(filePath, JSON.stringify(data[platform], null, 2), 'utf-8');
  });

  // 保存完整快照
  var snapshotPath = path.join(CONFIG.dataDir, 'trends', today + '.json');
  fs.writeFileSync(snapshotPath, JSON.stringify(data, null, 2), 'utf-8');

  console.log('历史数据已保存: ' + today);
}

// 主函数
async function main() {
  ensureDirs();
  var data = await fetchAll();
  saveHistory(data);

  console.log('\n========== 今日热榜汇总 ==========');
  console.log('- 微博: ' + data.weibo.length + '条');
  console.log('- 知乎: ' + data.zhihu.length + '条');
  console.log('- B站: ' + data.bilibili.length + '条');
  console.log('- 抖音: ' + data.douyin.length + '条');
  console.log('- 小红书: ' + data.xiaohongshu.length + '条');
  console.log('================================\n');

  return data;
}

// 导出
module.exports = {
  fetchAll: fetchAll,
  saveHistory: saveHistory,
  fetchWeibo: fetchWeibo,
  fetchZhihu: fetchZhihu,
  fetchBilibili: fetchBilibili,
  fetchDouyin: fetchDouyin,
  fetchXiaohongshu: fetchXiaohongshu,
  ensureDirs: ensureDirs
};

// 直接运行
if (require.main === module) {
  main().then(function(data) {
    console.log('数据采集完成');
    process.exit(0);
  }).catch(function(e) {
    console.error('采集失败:', e);
    process.exit(1);
  });
}
