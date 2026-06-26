// pages/history/history.js

Page({
  data: {
    historyList: []
  },

  onLoad() {
    console.log('[History] onLoad 开始');
    this.loadHistory();
    console.log('[History] onLoad 完成');
  },

  onShow() {
    console.log('[History] onShow');
    this.loadHistory();
  },

  /**
   * 加载历史记录
   */
  loadHistory() {
    console.log('[History] loadHistory 开始');
    
    const app = getApp();
    const history = app.globalData.history || [];
    
    console.log('[History] 历史记录数:', history.length);
    
    // 格式化显示时间
    const formattedHistory = history.map(item => {
      const date = new Date(item.timestamp);
      const displayTime = `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
      
      return {
        ...item,
        displayTime
      };
    });
    
    this.setData({ historyList: formattedHistory });
    
    console.log('[History] loadHistory 完成');
  },

  /**
   * 应用历史记录
   */
  onApplyHistory(e) {
    const index = e.currentTarget.dataset.index;
    console.log('[History] onApplyHistory: index=', index);
    
    const item = this.data.historyList[index];
    if (!item) {
      console.log('[History] 历史记录不存在');
      return;
    }
    
    // 保存参数到缓存
    try {
      wx.setStorageSync('solveParams', {
        targetGold: item.targetGold.toString(),
        targetDiamond: item.targetDiamond.toString(),
        multiplierP: item.multiplierP.toString(),
        multiplierQ: item.multiplierQ.toString()
      });
      console.log('[History] 参数已保存到缓存');
    } catch (e) {
      console.error('[History] 保存参数失败:', e);
    }
    
    // 跳转到求解页面
    wx.switchTab({
      url: '/pages/index/index',
      success: () => {
        console.log('[History] 跳转到求解页面成功');
        wx.showToast({
          title: '参数已应用',
          icon: 'success'
        });
      },
      fail: (err) => {
        console.error('[History] 跳转失败:', err);
      }
    });
  },

  /**
   * 清空历史
   */
  onClearHistory() {
    console.log('[History] onClearHistory 开始');
    
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有历史记录吗？',
      success: (res) => {
        if (res.confirm) {
          console.log('[History] 用户确认清空');
          
          const app = getApp();
          app.clearHistory();
          
          this.setData({ historyList: [] });
          
          wx.showToast({
            title: '已清空',
            icon: 'success'
          });
          
          console.log('[History] onClearHistory 完成');
        } else {
          console.log('[History] 用户取消清空');
        }
      }
    });
  }
});
