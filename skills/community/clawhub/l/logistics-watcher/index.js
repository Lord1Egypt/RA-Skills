/**
 * Logistics Watcher - 物流异常预警
 */

let LocalStore;
try {
  ({ LocalStore } = require('../../shared/storage/local-store'));
} catch (error) {
  const fs = require('fs');
  const os = require('os');
  const path = require('path');

  LocalStore = class {
    constructor(namespace) {
      const baseDir = path.join(os.homedir(), '.openclaw', 'data', namespace);
      fs.mkdirSync(baseDir, { recursive: true });
      this.file = path.join(baseDir, 'store.json');
    }

    readAll() {
      try {
        return JSON.parse(fs.readFileSync(this.file, 'utf8'));
      } catch (readError) {
        return {};
      }
    }

    writeAll(data) {
      fs.writeFileSync(this.file, JSON.stringify(data, null, 2));
    }

    get(key, fallback) {
      const data = this.readAll();
      return Object.prototype.hasOwnProperty.call(data, key) ? data[key] : fallback;
    }

    set(key, value) {
      const data = this.readAll();
      data[key] = value;
      this.writeAll(data);
    }
  };
}

class LogisticsWatcher {
  constructor() {
    this.store = new LocalStore('logistics-watcher');
    this.STORAGE_KEY = 'tracked_packages';
    
    // 快递公司配置
    this.couriers = {
      'sf': { name: '顺丰速运', api: 'sf-express' },
      'jd': { name: '京东物流', api: 'jd-logistics' },
      'zto': { name: '中通快递', api: 'zto' },
      'yto': { name: '圆通速递', api: 'yto' },
      'yunda': { name: '韵达快递', api: 'yunda' },
      'ems': { name: 'EMS', api: 'ems' },
      'jt': { name: '极兔速递', api: 'jtexpress' }
    };
    
    // 异常状态关键词
    this.abnormalKeywords = [
      '异常', '退回', '拒收', '无法联系', '地址不详',
      '破损', '丢失', '滞留', '积压', '疫情管控'
    ];
    
    // 正常流转状态
    this.normalStatuses = [
      '已揽收', '运输中', '到达', '派送中', '已签收'
    ];
  }

  /**
   * 识别快递公司
   */
  detectCourier(trackingNo) {
    const patterns = {
      'sf': /^SF/i,
      'jd': /^JD/i,
      'jt': /^JT/i,
      'ems': /^EMS|^10/i,
      'zto': /^7|^5|^1[0-9]{11}$/,
      'yto': /^YT|^8|^6|^1[0-9]{12}$/,
      'yunda': /^YT|^3|^4|^12[0-9]{11}$/
    };
    
    for (const [code, pattern] of Object.entries(patterns)) {
      if (pattern.test(trackingNo)) {
        return this.couriers[code];
      }
    }
    
    return { name: '未知快递', api: null };
  }

  /**
   * 添加追踪
   */
  addTracking(trackingNo, options = {}) {
    const courier = this.detectCourier(trackingNo);
    const items = this.store.get(this.STORAGE_KEY, {});
    
    if (items[trackingNo]) {
      return { success: false, error: '该单号已在追踪列表' };
    }
    
    const newItem = {
      trackingNo,
      courier,
      name: options.name || '未命名包裹',
      addedAt: new Date().toISOString(),
      lastCheckAt: null,
      status: 'pending',
      history: [],
      alerts: [],
      alertRules: options.alertRules || [
        { type: 'stuck', hours: 48, enabled: true },
        { type: 'abnormal', enabled: true }
      ]
    };
    
    items[trackingNo] = newItem;
    this.store.set(this.STORAGE_KEY, items);
    
    return { success: true, item: newItem };
  }

  /**
   * 检查异常
   */
  checkAbnormal(history) {
    const alerts = [];
    const now = new Date();
    
    if (!history || history.length === 0) {
      return alerts;
    }
    
    const latest = history[0];
    const latestTime = new Date(latest.time);
    
    // 检查停滞
    const hoursSinceUpdate = (now - latestTime) / (1000 * 60 * 60);
    if (hoursSinceUpdate > 48) {
      alerts.push({
        type: 'stuck',
        severity: hoursSinceUpdate > 72 ? 'high' : 'medium',
        message: `物流${Math.floor(hoursSinceUpdate)}小时未更新，可能停滞`,
        suggestion: '建议联系快递公司或卖家查询'
      });
    }
    
    // 检查异常状态
    const latestStatus = latest.status || '';
    for (const keyword of this.abnormalKeywords) {
      if (latestStatus.includes(keyword)) {
        alerts.push({
          type: 'abnormal',
          severity: 'high',
          message: `检测到异常状态: ${latestStatus}`,
          suggestion: '建议立即联系快递客服处理'
        });
        break;
      }
    }
    
    // 检查长时间运输
    if (history.length >= 2) {
      const firstTime = new Date(history[history.length - 1].time);
      const daysInTransit = (now - firstTime) / (1000 * 60 * 60 * 24);
      
      if (daysInTransit > 5 && !latestStatus.includes('签收')) {
        alerts.push({
          type: 'delayed',
          severity: daysInTransit > 7 ? 'high' : 'medium',
          message: `运输已${Math.floor(daysInTransit)}天，可能延误`,
          suggestion: '建议查询是否有特殊情况导致延误'
        });
      }
    }
    
    return alerts;
  }

  /**
   * 生成物流报告
   */
  generateReport(trackingNo) {
    const items = this.store.get(this.STORAGE_KEY, {});
    const item = items[trackingNo];
    
    if (!item) {
      return { success: false, error: '单号不存在' };
    }
    
    const alerts = this.checkAbnormal(item.history);
    const latest = item.history[0];
    
    // 预估到达（简化版）
    let estimatedArrival = null;
    if (latest && !latest.status.includes('签收')) {
      const lastUpdate = new Date(latest.time);
      estimatedArrival = new Date(lastUpdate.getTime() + 2 * 24 * 60 * 60 * 1000);
    }
    
    return {
      success: true,
      trackingNo,
      courier: item.courier.name,
      status: latest ? latest.status : '暂无信息',
      latestUpdate: latest ? latest.time : null,
      location: latest ? latest.location : null,
      estimatedArrival,
      alerts,
      history: item.history.slice(0, 10),
      isAbnormal: alerts.length > 0,
      riskLevel: alerts.some(a => a.severity === 'high') ? 'high' : alerts.length > 0 ? 'medium' : 'low'
    };
  }

  /**
   * 批量检查所有
   */
  checkAll() {
    const items = this.store.get(this.STORAGE_KEY, {});
    const results = [];
    
    for (const trackingNo of Object.keys(items)) {
      const report = this.generateReport(trackingNo);
      results.push(report);
    }
    
    const abnormal = results.filter(r => r.isAbnormal);
    
    return {
      total: results.length,
      normal: results.length - abnormal.length,
      abnormal: abnormal.length,
      abnormalList: abnormal,
      all: results
    };
  }
}

module.exports = { LogisticsWatcher };
