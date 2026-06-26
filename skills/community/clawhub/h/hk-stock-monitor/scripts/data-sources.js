/**
 * 多数据源股票数据获取模块
 * 
 * 数据源优先级：
 * 1. 新浪财经（免费，无需 API key）
 * 2. QVeris（需要 API key，付费）
 */

const { execSync } = require('child_process');
const http = require('http');
const https = require('https');

const CONFIG = {
  chatId: 'oc_c771930429ba9d9683b8a38fe3a9b3f9',
  qverisApiKey: process.env.QVERIS_API_KEY || 'sk-pQbZOXNY3p1gPIg4cXPRiM7k6_SfXpw190ZRO7ac5Gs',
  qverisScript: '/root/.openclaw/workspace/skills/qveris-official/scripts/qveris_tool.mjs',
  // 记录连续失败次数
  stateFile: '/root/.openclaw/workspace/stock-monitor/data/failure-state.json',
  // 连续失败多少次后告警
  alertThreshold: 3
};

const path = require('path');
const fs = require('fs');

function loadState() {
  try {
    if (fs.existsSync(CONFIG.stateFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf-8'));
    }
  } catch (e) {}
  return { consecutiveFailures: 0, lastAlertTime: null };
}

function saveState(state) {
  const dir = path.dirname(CONFIG.stateFile);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
}

function sendAlert(message) {
  const escapedMsg = message.replace(/"/g, '\\"').replace(/\n/g, '\\n');
  try {
    execSync(`openclaw message send --channel feishu --target ${CONFIG.chatId} --message "${escapedMsg}"`, { encoding: 'utf-8', timeout: 30000 });
    console.log('✅ 告警已发送');
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
  }
}

/**
 * 新浪财经数据源（免费）
 * 支持 A股和港股
 */
async function fetchFromSina(codes) {
  return new Promise((resolve) => {
    // 转换代码格式：000333.SZ -> sz000333, 3690.HK -> hk03690
    const sinaCodes = codes.map(code => {
      if (code.endsWith('.HK')) {
        const num = code.replace('.HK', '').padStart(5, '0');
        return `hk${num}`;
      } else if (code.endsWith('.SH')) {
        return `sh${code.replace('.SH', '')}`;
      } else if (code.endsWith('.SZ')) {
        return `sz${code.replace('.SZ', '')}`;
      }
      return code;
    });
    
    const url = `https://hq.sinajs.cn/list=${sinaCodes.join(',')}`;
    
    https.get(url, {
      headers: {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = [];
          const lines = data.split('\n').filter(l => l.trim());
          
          for (const line of lines) {
            const match = line.match(/var hq_str_(\w+)="(.*)"/);
            if (!match || !match[2]) continue;
            
            const sinaCode = match[1];
            const values = match[2].split(',');
            
            // 港股格式：名称,今开,昨收,最高,最低,最新,涨跌额,涨跌幅,成交量,成交额...
            // A股格式：名称,今开,昨收,最高,最低,最新,...
            
            if (sinaCode.startsWith('hk')) {
              // 港股
              const name = values[0];
              const latest = parseFloat(values[6]) || 0;
              const prevClose = parseFloat(values[3]) || latest;
              const changeRatio = prevClose > 0 ? ((latest - prevClose) / prevClose * 100) : 0;
              const volume = parseFloat(values[9]) || 0;
              
              // 转换回原代码格式
              const originalCode = codes.find(c => {
                const num = c.replace('.HK', '').padStart(5, '0');
                return `hk${num}` === sinaCode;
              });
              
              if (originalCode && latest > 0) {
                results.push({
                  thscode: originalCode,
                  name: name,
                  latest: latest,
                  changeRatio: parseFloat(changeRatio.toFixed(2)),
                  volume: volume,
                  vol_ratio: 1 // 新浪不提供量比
                });
              }
            } else {
              // A股
              const name = values[0];
              const latest = parseFloat(values[3]) || 0;
              const prevClose = parseFloat(values[2]) || latest;
              const changeRatio = prevClose > 0 ? ((latest - prevClose) / prevClose * 100) : 0;
              
              if (latest > 0) {
                let originalCode;
                if (sinaCode.startsWith('sh')) {
                  originalCode = `${sinaCode.slice(2)}.SH`;
                } else {
                  originalCode = `${sinaCode.slice(2)}.SZ`;
                }
                
                results.push({
                  thscode: originalCode,
                  name: name,
                  latest: latest,
                  changeRatio: parseFloat(changeRatio.toFixed(2)),
                  volume: parseFloat(values[8]) || 0,
                  vol_ratio: 1 // 新浪不提供量比
                });
              }
            }
          }
          
          resolve(results);
        } catch (e) {
          console.error('新浪数据解析失败:', e.message);
          resolve(null);
        }
      });
    }).on('error', (e) => {
      console.error('新浪请求失败:', e.message);
      resolve(null);
    });
  });
}

/**
 * QVeris 数据源（付费）
 */
async function fetchFromQveris(codes) {
  const scriptDir = path.dirname(CONFIG.qverisScript);
  const codesStr = codes.join(',');
  
  try {
    const searchCmd = `cd ${scriptDir} && QVERIS_API_KEY="${CONFIG.qverisApiKey}" node ${CONFIG.qverisScript} search "China stock real-time price" --limit 5`;
    const searchResult = execSync(searchCmd, { encoding: 'utf-8', timeout: 30000 });
    const searchIdMatch = searchResult.match(/Search ID: ([a-f0-9-]+)/);
    if (!searchIdMatch) return null;
    const searchId = searchIdMatch[1];
    
    const execCmd = `cd ${scriptDir} && QVERIS_API_KEY="${CONFIG.qverisApiKey}" node ${CONFIG.qverisScript} execute ths_ifind.real_time_quotation.v1 --search-id ${searchId} --params '{"codes":"${codesStr}"}'`;
    const result = execSync(execCmd, { encoding: 'utf-8', timeout: 60000 });
    
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const data = JSON.parse(jsonMatch[0]);
      return data.data ? data.data.flat() : null;
    }
    return null;
  } catch (error) {
    console.error('QVeris 获取失败:', error.message);
    return null;
  }
}

/**
 * 主数据获取函数
 * 优先使用免费数据源，失败后尝试 QVeris
 * 全部失败时发送告警
 */
async function fetchStockData(stocks) {
  const codes = stocks.map(s => s.code);
  const state = loadState();
  
  // 1. 尝试新浪财经（免费）
  console.log('📡 尝试新浪财经数据源...');
  let data = await fetchFromSina(codes);
  
  if (data && data.length > 0) {
    console.log(`✅ 新浪财经成功获取 ${data.length} 只股票数据`);
    // 重置失败计数
    if (state.consecutiveFailures > 0) {
      state.consecutiveFailures = 0;
      saveState(state);
    }
    return data;
  }
  
  console.log('⚠️ 新浪财经失败，尝试 QVeris...');
  
  // 2. 尝试 QVeris（付费）
  data = await fetchFromQveris(codes);
  
  if (data && data.length > 0) {
    console.log(`✅ QVeris 成功获取 ${data.length} 只股票数据`);
    // 重置失败计数
    if (state.consecutiveFailures > 0) {
      state.consecutiveFailures = 0;
      saveState(state);
    }
    return data;
  }
  
  // 3. 全部失败，更新状态并发送告警
  console.log('❌ 所有数据源均失败');
  state.consecutiveFailures++;
  const now = new Date().toISOString();
  
  // 检查是否需要发送告警
  if (state.consecutiveFailures >= CONFIG.alertThreshold) {
    const lastAlert = state.lastAlertTime ? new Date(state.lastAlertTime) : null;
    const hoursSinceLastAlert = lastAlert ? (Date.now() - lastAlert.getTime()) / 3600000 : 999;
    
    // 每小时最多告警一次
    if (hoursSinceLastAlert >= 1) {
      const alertMsg = `🚨 **数据源告警** ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n\n` +
        `股票监控连续 ${state.consecutiveFailures} 次获取数据失败\n` +
        `- 新浪财经：不可用\n` +
        `- QVeris：不可用\n\n` +
        `请检查网络连接或数据源状态`;
      sendAlert(alertMsg);
      state.lastAlertTime = now;
    }
  }
  
  saveState(state);
  return null;
}

module.exports = { fetchStockData, fetchFromSina, fetchFromQveris };