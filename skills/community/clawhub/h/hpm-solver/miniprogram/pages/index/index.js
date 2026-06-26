// pages/index/index.js
const solver = require('../../utils/solver.js');

Page({
  data: {
    targetGold: '',
    targetDiamond: '',
    multiplierP: '1.0',
    multiplierQ: '1.0',
    solution: null
  },

  onLoad() {
    console.log('[Index] onLoad 开始');
    this.loadDefaultParams();
    console.log('[Index] onLoad 完成');
  },

  onShow() {
    console.log('[Index] onShow');
  },

  loadDefaultParams() {
    console.log('[Index] loadDefaultParams');
    // 可以从缓存加载上次使用的参数
    try {
      const params = wx.getStorageSync('solveParams');
      if (params) {
        console.log('[Index] 从缓存加载参数:', params);
        this.setData({
          targetGold: params.targetGold || '',
          targetDiamond: params.targetDiamond || '',
          multiplierP: params.multiplierP || '1.0',
          multiplierQ: params.multiplierQ || '1.0'
        });
      }
    } catch (e) {
      console.error('[Index] 加载参数失败:', e);
    }
  },

  saveParams() {
    console.log('[Index] saveParams');
    try {
      wx.setStorageSync('solveParams', {
        targetGold: this.data.targetGold,
        targetDiamond: this.data.targetDiamond,
        multiplierP: this.data.multiplierP,
        multiplierQ: this.data.multiplierQ
      });
      console.log('[Index] 参数保存成功');
    } catch (e) {
      console.error('[Index] 保存参数失败:', e);
    }
  },

  onGoldInput(e) {
    console.log('[Index] onGoldInput:', e.detail.value);
    this.setData({ targetGold: e.detail.value });
  },

  onDiamondInput(e) {
    console.log('[Index] onDiamondInput:', e.detail.value);
    this.setData({ targetDiamond: e.detail.value });
  },

  onPInput(e) {
    console.log('[Index] onPInput:', e.detail.value);
    this.setData({ multiplierP: e.detail.value });
  },

  onQInput(e) {
    console.log('[Index] onQInput:', e.detail.value);
    this.setData({ multiplierQ: e.detail.value });
  },

  onReset() {
    console.log('[Index] onReset 开始');
    this.setData({
      targetGold: '',
      targetDiamond: '',
      multiplierP: '1.0',
      multiplierQ: '1.0',
      solution: null
    });
    wx.removeStorageSync('solveParams');
    console.log('[Index] onReset 完成');
    wx.showToast({
      title: '已恢复默认',
      icon: 'success'
    });
  },

  onSolve() {
    console.log('[Index] onSolve 开始');
    
    const targetGold = parseInt(this.data.targetGold) || 0;
    const targetDiamond = parseInt(this.data.targetDiamond) || 0;
    const multiplierP = parseFloat(this.data.multiplierP) || 1.0;
    const multiplierQ = parseFloat(this.data.multiplierQ) || 1.0;
    
    console.log('[Index] 求解参数: gold=', targetGold, 'diamond=', targetDiamond, 'p=', multiplierP, 'q=', multiplierQ);
    
    if (targetGold === 0 && targetDiamond === 0) {
      console.log('[Index] 目标金额为0，提示用户');
      wx.showToast({
        title: '请输入目标金额',
        icon: 'none'
      });
      return;
    }
    
    // 保存参数
    this.saveParams();
    
    // 显示加载
    wx.showLoading({
      title: '求解中...',
      mask: true
    });
    
    // 获取价格数据
    const app = getApp();
    const basePrices = app.globalData.basePrices;
    
    console.log('[Index] basePrices 加载完成');
    
    // 求解
    const result = {
      gold: null,
      diamond: null
    };
    
    if (targetGold > 0) {
      console.log('[Index] 开始求解金币');
      const goldItems = [
        ...solver.buildItems(basePrices, 'foods', 'gold', multiplierP),
        ...solver.buildItems(basePrices, 'plants', 'gold', multiplierQ)
      ];
      console.log('[Index] 金币物品数:', goldItems.length);
      result.gold = solver.solve(targetGold, goldItems);
      console.log('[Index] 金币求解结果:', result.gold ? '找到解' : '无解');
    }
    
    if (targetDiamond > 0) {
      console.log('[Index] 开始求解宝石');
      const diamondItems = [
        ...solver.buildItems(basePrices, 'foods', 'diamond', multiplierP),
        ...solver.buildItems(basePrices, 'plants', 'diamond', multiplierQ)
      ];
      console.log('[Index] 宝石物品数:', diamondItems.length);
      result.diamond = solver.solve(targetDiamond, diamondItems);
      console.log('[Index] 宝石求解结果:', result.diamond ? '找到解' : '无解');
    }
    
    wx.hideLoading();
    
    // 格式化结果
    const solution = this.formatSolution(result);
    
    console.log('[Index] 求解完成, solution:', solution ? '有结果' : '无结果');
    
    this.setData({ solution });
    
    // 保存历史
    if (result.gold || result.diamond) {
      const historyRecord = {
        timestamp: new Date().toISOString(),
        targetGold,
        targetDiamond,
        multiplierP,
        multiplierQ,
        solution: solution,
        isPerfect: (result.gold?.isPerfect ?? true) && (result.diamond?.isPerfect ?? true)
      };
      app.saveHistory(historyRecord);
      console.log('[Index] 历史记录已保存');
    }
    
    // 显示结果提示
    if (solution) {
      wx.showToast({
        title: '求解完成',
        icon: 'success'
      });
    } else {
      wx.showToast({
        title: '未找到解',
        icon: 'none'
      });
    }
    
    console.log('[Index] onSolve 完成');
  },

  formatSolution(result) {
    console.log('[Index] formatSolution 开始');
    
    const solution = {};
    
    if (result.gold) {
      solution.gold = {
        isPerfect: result.gold.isPerfect,
        totalCost: result.gold.totalCost,
        residual: result.gold.residual,
        groups: result.gold.groups.map(([group, qty]) => ({
          names: group.items.join(' | '),
          qty,
          price: group.actualPrice,
          subtotal: qty * group.actualPrice
        })).sort((a, b) => b.subtotal - a.subtotal)
      };
      console.log('[Index] 金币结果格式化完成, 组数:', solution.gold.groups.length);
    }
    
    if (result.diamond) {
      solution.diamond = {
        isPerfect: result.diamond.isPerfect,
        totalCost: result.diamond.totalCost,
        residual: result.diamond.residual,
        groups: result.diamond.groups.map(([group, qty]) => ({
          names: group.items.join(' | '),
          qty,
          price: group.actualPrice,
          subtotal: qty * group.actualPrice
        })).sort((a, b) => b.subtotal - a.subtotal)
      };
      console.log('[Index] 宝石结果格式化完成, 组数:', solution.diamond.groups.length);
    }
    
    console.log('[Index] formatSolution 完成');
    return solution.gold || solution.diamond ? solution : null;
  }
});
