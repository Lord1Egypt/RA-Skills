// app.js
App({
  globalData: {
    basePrices: null,
    history: []
  },

  onLaunch() {
    console.log('[App] onLaunch 开始');
    this.loadBasePrices();
    this.loadHistory();
    console.log('[App] onLaunch 完成');
  },

  loadBasePrices() {
    console.log('[App] loadBasePrices 开始');
    try {
      const data = wx.getStorageSync('basePrices');
      if (data) {
        console.log('[App] loadBasePrices 从缓存加载成功, 物品数:', 
          Object.keys(data.foods?.gold || {}).length + 
          Object.keys(data.foods?.diamond || {}).length +
          Object.keys(data.plants?.gold || {}).length +
          Object.keys(data.plants?.diamond || {}).length);
        this.globalData.basePrices = data;
      } else {
        console.log('[App] loadBasePrices 缓存为空，使用默认数据');
        this.globalData.basePrices = this.getDefaultPrices();
        this.saveBasePrices(this.globalData.basePrices);
      }
    } catch (e) {
      console.error('[App] loadBasePrices 错误:', e);
      this.globalData.basePrices = this.getDefaultPrices();
    }
    console.log('[App] loadBasePrices 完成');
  },

  saveBasePrices(data) {
    console.log('[App] saveBasePrices 开始');
    try {
      wx.setStorageSync('basePrices', data);
      this.globalData.basePrices = data;
      console.log('[App] saveBasePrices 保存成功');
    } catch (e) {
      console.error('[App] saveBasePrices 错误:', e);
    }
  },

  loadHistory() {
    console.log('[App] loadHistory 开始');
    try {
      const data = wx.getStorageSync('solveHistory');
      if (data) {
        console.log('[App] loadHistory 从缓存加载成功, 记录数:', data.length);
        this.globalData.history = data;
      } else {
        console.log('[App] loadHistory 缓存为空');
        this.globalData.history = [];
      }
    } catch (e) {
      console.error('[App] loadHistory 错误:', e);
      this.globalData.history = [];
    }
    console.log('[App] loadHistory 完成');
  },

  saveHistory(record) {
    console.log('[App] saveHistory 开始, 记录:', record);
    try {
      this.globalData.history.unshift(record);
      if (this.globalData.history.length > 50) {
        this.globalData.history = this.globalData.history.slice(0, 50);
      }
      wx.setStorageSync('solveHistory', this.globalData.history);
      console.log('[App] saveHistory 保存成功, 总记录数:', this.globalData.history.length);
    } catch (e) {
      console.error('[App] saveHistory 错误:', e);
    }
  },

  clearHistory() {
    console.log('[App] clearHistory 开始');
    this.globalData.history = [];
    wx.removeStorageSync('solveHistory');
    console.log('[App] clearHistory 完成');
  },

  getDefaultPrices() {
    console.log('[App] getDefaultPrices 返回默认价格数据');
    return {
      foods: {
        gold: {
          "幽兰秘制肉卷": 333,
          "蜂蜜烤羊腿": 443,
          "海鱼黄金焗饭": 403,
          "香草战斧牛排": 665,
          "香草风味烤扇贝": 443,
          "奶油蘑菇炖饭": 182,
          "盐烤海虾": 302,
          "红酒鹿肉炖汤": 443,
          "甜奶油蛋派": 271,
          "奶油蟹粉面": 484,
          "香煎怪肉排": 786,
          "烈焰香煎鹅肝": 786,
          "浓醇提拉米苏": 403,
          "香浓可可混莓果冻": 554,
          "迷迭香风味沙拉": 554
        },
        diamond: {
          "野心与荣耀之宴": 14,
          "霍格沃兹盛宴": 14,
          "智慧与风雅之宴": 14
        }
      },
      plants: {
        gold: {
          "火焰肉桂": 34,
          "曼德拉草": 24,
          "幽兰月桂": 34,
          "玫瑰": 42,
          "迷迭香": 56,
          "泡泡豆荚": 85,
          "鼠尾草": 56,
          "毒牙天竺葵": 12,
          "中国咬人甘蓝": 57,
          "羽衣草": 105
        },
        diamond: {
          "水仙": 2,
          "嗅幻草": 6,
          "嗅幻草-蓝": 1,
          "嗅幻草-紫": 3,
          "牡丹": 2,
          "红火焰藻": 3,
          "红火焰藻-紫": 2
        }
      }
    };
  }
});
