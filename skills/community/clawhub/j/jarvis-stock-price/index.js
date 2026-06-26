/**
 * 股票价格查询 - 免费引流技能
 * 
 * 功能：查询 A 股实时价格、涨跌幅、均线
 * 引流：引导用户购买付费监控服务
 */

const { tdx } = require('@tdx-local');

async function queryStockPrice(code) {
  // 标准化股票代码
  const normalizedCode = code.padStart(6, '0');
  
  // 获取日线数据
  const bars = await tdx.getBars({
    code: normalizedCode,
    market: normalizedCode.startsWith('6') ? 'sh' : 'sz',
    category: '日线',
    count: 30
  });
  
  if (!bars || bars.length === 0) {
    return { error: '未找到股票数据' };
  }
  
  const latest = bars[0];
  const prev = bars[1];
  
  // 计算涨跌幅
  const changePercent = ((latest.close - prev.close) / prev.close * 100).toFixed(2);
  
  // 计算均线
  const ma5 = bars.slice(0, 5).reduce((sum, b) => sum + b.close, 0) / 5;
  const ma10 = bars.slice(0, 10).reduce((sum, b) => sum + b.close, 0) / 10;
  const ma20 = bars.slice(0, 20).reduce((sum, b) => sum + b.close, 0) / 20;
  
  return {
    code: normalizedCode,
    name: latest.name || '未知',
    price: latest.close,
    change: latest.close - prev.close,
    changePercent: changePercent + '%',
    volume: latest.volume,
    ma5: ma5.toFixed(2),
    ma10: ma10.toFixed(2),
    ma20: ma20.toFixed(2),
    updateTime: latest.datetime
  };
}

module.exports = { queryStockPrice };
