#!/usr/bin/env node
/**
 * 股票波动告警检查脚本 v3.0
 * 
 * 规则：
 * 1. 上涨超过4.9%时告警
 * 2. 下跌超过4.9%时告警
 * 3. 每只股票每天最多告警1次
 * 4. 无告警时不发送任何消息
 */

const { execSync } = require('child_process');
const { fetchStockData } = require('./data-sources');
const path = require('path');
const fs = require('fs');

const CONFIG = {
  threshold: 4.9, // 告警阈值 4.9%
  chatId: 'oc_c771930429ba9d9683b8a38fe3a9b3f9',
  stateFile: '/root/.openclaw/workspace/stock-monitor/data/alert-state.json',
  stocks: [
    // A股
    { name: '美的集团', code: '000333.SZ' },
    { name: '中控技术', code: '688777.SH' },
    { name: '工商银行', code: '601398.SH' },
    { name: '中国中车', code: '601766.SH', volumeAlert: true }, // 放量告警
    { name: '长安汽车', code: '000625.SZ' },
    { name: '爱尔眼科', code: '300015.SZ' },
    { name: '宋城演艺', code: '300144.SZ' },
    { name: '青岛啤酒', code: '600600.SH', priceTargets: [65] }, // 价格告警
    // 港股
    { name: '美团-W', code: '3690.HK', priceTargets: [80.3, 83.3, 85] }, // 价格告警
    { name: '阿里巴巴-SW', code: '9988.HK' },
    { name: '腾讯控股', code: '0700.HK' },
    { name: '吉利汽车', code: '0175.HK' },
    { name: '山高控股', code: '0412.HK' },
    { name: '华润燃气', code: '1193.HK' },
    { name: '顺丰控股', code: '6936.HK' },
    { name: '海尔智家', code: '6690.HK' }
  ]
};

function getBeijingTime() {
  return new Date();
}

function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

function getTodayStr() {
  return formatDate(getBeijingTime()).split(' ')[0];
}

function loadState() {
  try {
    if (fs.existsSync(CONFIG.stateFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf-8'));
    }
  } catch (e) {}
  return { date: getTodayStr(), alerted: {} };
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
    return true;
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    return false;
  }
}

async function main() {
  const beijing = getBeijingTime();
  const dayOfWeek = beijing.getDay();
  const today = getTodayStr();
  
  // 周末不检查
  if (dayOfWeek === 0 || dayOfWeek === 6) {
    return;
  }
  
  // 检查交易时间 (9:30-16:00)
  const hour = beijing.getHours();
  const minute = beijing.getMinutes();
  const timeNum = hour * 100 + minute;
  if (timeNum < 930 || timeNum > 1600) {
    return;
  }
  
  // 获取股票数据
  const rawData = await fetchStockData(CONFIG.stocks);
  if (!rawData || rawData.length === 0) {
    return;
  }
  
  // 加载状态，如果是新的一天则重置
  let state = loadState();
  if (state.date !== today) {
    state = { date: today, alerted: {} };
  }
  
  const alerts = [];
  
  for (const stock of CONFIG.stocks) {
    const data = rawData.find(d => d.thscode === stock.code);
    if (!data) continue;
    
    const changeRatio = data.changeRatio || 0;
    const price = data.latest;
    const alertKey = `${stock.code}`;
    
    // 1. 涨跌幅告警
    if (Math.abs(changeRatio) >= CONFIG.threshold) {
      if (!state.alerted[`${alertKey}_change`]) {
        alerts.push({
          type: 'change',
          name: stock.name,
          code: stock.code,
          price: price,
          change: changeRatio
        });
        state.alerted[`${alertKey}_change`] = true;
      }
    }
    
    // 2. 价格告警
    if (stock.priceTargets && stock.priceTargets.length > 0) {
      for (const targetPrice of stock.priceTargets) {
        const priceKey = `${alertKey}_price_${targetPrice}`;
        // 检查价格是否触及目标价（允许0.5%误差）
        const diff = Math.abs(price - targetPrice) / targetPrice;
        if (diff <= 0.005 && !state.alerted[priceKey]) {
          alerts.push({
            type: 'price',
            name: stock.name,
            code: stock.code,
            price: price,
            targetPrice: targetPrice,
            direction: price >= targetPrice ? 'up' : 'down'
          });
          state.alerted[priceKey] = true;
        }
      }
    }
    
    // 3. 放量告警（需要成交量数据）
    if (stock.volumeAlert && data.volume) {
      const volumeKey = `${alertKey}_volume`;
      // 放量定义：今日成交量是昨日的1.5倍以上，且涨跌超过2%
      // 注：新浪数据可能没有昨成交量，这里简化为检查涨跌+是否有成交量
      if (Math.abs(changeRatio) >= 2 && !state.alerted[volumeKey]) {
        alerts.push({
          type: 'volume',
          name: stock.name,
          code: stock.code,
          price: price,
          change: changeRatio,
          volume: data.volume
        });
        state.alerted[volumeKey] = true;
      }
    }
  }
  
  // 保存状态
  saveState(state);
  
  // 无告警时静默退出
  if (alerts.length === 0) {
    return;
  }
  
  // 构建告警消息
  let message = `🚨 **股票告警** ${formatDate(beijing)}\n\n`;
  
  // 按类型分组
  const changeAlerts = alerts.filter(a => a.type === 'change');
  const priceAlerts = alerts.filter(a => a.type === 'price');
  const volumeAlerts = alerts.filter(a => a.type === 'volume');
  
  // 涨跌幅告警
  if (changeAlerts.length > 0) {
    message += `📊 **波动告警** (${CONFIG.threshold}%阈值)\n`;
    for (const alert of changeAlerts) {
      const isUp = alert.change >= 0;
      const emoji = isUp ? '🔴📈' : '🟢📉';
      const changeStr = isUp ? `+${alert.change.toFixed(2)}%` : `${alert.change.toFixed(2)}%`;
      message += `${emoji} **${alert.name}** | ¥${alert.price.toFixed(2)} | **${changeStr}**\n`;
    }
    message += '\n';
  }
  
  // 价格告警
  if (priceAlerts.length > 0) {
    message += `🎯 **价格告警**\n`;
    for (const alert of priceAlerts) {
      const emoji = alert.direction === 'up' ? '🔴' : '🟢';
      message += `${emoji} **${alert.name}** | 当前 ¥${alert.price.toFixed(2)} | 目标 ¥${alert.targetPrice}\n`;
    }
    message += '\n';
  }
  
  // 放量告警
  if (volumeAlerts.length > 0) {
    message += `📈 **放量告警** (涨跌>2%)\n`;
    for (const alert of volumeAlerts) {
      const isUp = alert.change >= 0;
      const emoji = isUp ? '🔴📈' : '🟢📉';
      const changeStr = isUp ? `+${alert.change.toFixed(2)}%` : `${alert.change.toFixed(2)}%`;
      message += `${emoji} **${alert.name}** | ¥${alert.price.toFixed(2)} | **${changeStr}**\n`;
    }
    message += '\n';
  }
  
  sendAlert(message);
}

main().catch(() => {});