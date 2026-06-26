// pages/price/price.js
const sortUtil = require('../../utils/sort.js');

Page({
  data: {
    currentCategory: 'foods',
    currentCurrency: 'gold',
    itemList: [],
    showAddModal: false,
    newItem: {
      name: '',
      price: ''
    },
    // 编辑前的价格快照，用于判断是否需要排序
    priceSnapshot: {}
  },

  onLoad() {
    console.log('[Price] onLoad 开始');
    this.loadPriceData();
    console.log('[Price] onLoad 完成');
  },

  onShow() {
    console.log('[Price] onShow');
    // 每次显示页面时重新加载数据
    this.loadPriceData();
  },

  /**
   * 加载价格数据并排序
   */
  loadPriceData() {
    console.log('[Price] loadPriceData 开始');
    
    const app = getApp();
    const basePrices = app.globalData.basePrices;
    
    if (!basePrices || !basePrices[this.data.currentCategory]) {
      console.log('[Price] 价格数据为空');
      this.setData({ itemList: [] });
      return;
    }
    
    const priceData = basePrices[this.data.currentCategory][this.data.currentCurrency] || {};
    console.log('[Price] 原始价格数据项数:', Object.keys(priceData).length);
    
    // 转换为数组并排序
    const sortedList = sortUtil.sortPriceData(priceData);
    console.log('[Price] 排序后列表项数:', sortedList.length);
    
    this.setData({ itemList: sortedList });
    
    // 保存价格快照
    this.savePriceSnapshot();
    
    console.log('[Price] loadPriceData 完成');
  },

  /**
   * 保存价格快照（用于判断是否需要排序）
   */
  savePriceSnapshot() {
    const snapshot = {};
    for (const item of this.data.itemList) {
      snapshot[item.name] = item.price;
    }
    this.data.priceSnapshot = snapshot;
    console.log('[Price] 价格快照已保存, 项数:', Object.keys(snapshot).length);
  },

  /**
   * 切换分类标签
   */
  onTabChange(e) {
    const category = e.currentTarget.dataset.category;
    const currency = e.currentTarget.dataset.currency;
    
    console.log('[Price] onTabChange: category=', category, 'currency=', currency);
    
    if (category === this.data.currentCategory && currency === this.data.currentCurrency) {
      console.log('[Price] 分类未变化，跳过');
      return;
    }
    
    this.setData({
      currentCategory: category,
      currentCurrency: currency
    });
    
    // 切换分类时重新加载并排序
    this.loadPriceData();
    
    console.log('[Price] onTabChange 完成');
  },

  /**
   * 价格输入框失去焦点
   * 注意：不立即排序，避免打断用户交互
   */
  onPriceBlur(e) {
    const name = e.currentTarget.dataset.name;
    const newPrice = parseInt(e.detail.value) || 0;
    
    console.log('[Price] onPriceBlur: name=', name, 'newPrice=', newPrice);
    
    // 更新本地数据
    const itemList = this.data.itemList.map(item => {
      if (item.name === name) {
        return { ...item, price: newPrice };
      }
      return item;
    });
    
    this.setData({ itemList });
    
    // 保存到全局数据
    this.savePriceToGlobal(name, newPrice);
    
    console.log('[Price] onPriceBlur 完成');
  },

  /**
   * 价格输入框确认
   * 用户确认后才进行排序
   */
  onPriceConfirm(e) {
    const name = e.currentTarget.dataset.name;
    const newPrice = parseInt(e.detail.value) || 0;
    
    console.log('[Price] onPriceConfirm: name=', name, 'newPrice=', newPrice);
    
    // 检查价格是否变化
    const oldPrice = this.data.priceSnapshot[name];
    if (oldPrice === newPrice) {
      console.log('[Price] 价格未变化，跳过排序');
      return;
    }
    
    // 重新排序
    const sortedList = sortUtil.sortItems(this.data.itemList);
    this.setData({ itemList: sortedList });
    
    // 更新价格快照
    this.savePriceSnapshot();
    
    console.log('[Price] onPriceConfirm 完成，已重新排序');
  },

  /**
   * 保存价格到全局数据
   */
  savePriceToGlobal(name, price) {
    console.log('[Price] savePriceToGlobal: name=', name, 'price=', price);
    
    const app = getApp();
    const basePrices = app.globalData.basePrices;
    
    if (!basePrices[this.data.currentCategory]) {
      basePrices[this.data.currentCategory] = {};
    }
    if (!basePrices[this.data.currentCategory][this.data.currentCurrency]) {
      basePrices[this.data.currentCategory][this.data.currentCurrency] = {};
    }
    
    basePrices[this.data.currentCategory][this.data.currentCurrency][name] = price;
    app.saveBasePrices(basePrices);
    
    console.log('[Price] savePriceToGlobal 完成');
  },

  /**
   * 删除物品
   */
  onDeleteItem(e) {
    const name = e.currentTarget.dataset.name;
    console.log('[Price] onDeleteItem: name=', name);
    
    wx.showModal({
      title: '确认删除',
      content: `确定要删除"${name}"吗？`,
      success: (res) => {
        if (res.confirm) {
          console.log('[Price] 用户确认删除');
          
          // 从列表中移除
          const itemList = this.data.itemList.filter(item => item.name !== name);
          this.setData({ itemList });
          
          // 从全局数据中移除
          const app = getApp();
          const basePrices = app.globalData.basePrices;
          delete basePrices[this.data.currentCategory][this.data.currentCurrency][name];
          app.saveBasePrices(basePrices);
          
          // 更新价格快照
          this.savePriceSnapshot();
          
          wx.showToast({
            title: '删除成功',
            icon: 'success'
          });
          
          console.log('[Price] onDeleteItem 完成');
        } else {
          console.log('[Price] 用户取消删除');
        }
      }
    });
  },

  /**
   * 添加物品
   */
  onAddItem() {
    console.log('[Price] onAddItem');
    this.setData({
      showAddModal: true,
      newItem: { name: '', price: '' }
    });
  },

  onNewNameInput(e) {
    console.log('[Price] onNewNameInput:', e.detail.value);
    this.setData({ 'newItem.name': e.detail.value });
  },

  onNewPriceInput(e) {
    console.log('[Price] onNewPriceInput:', e.detail.value);
    this.setData({ 'newItem.price': e.detail.value });
  },

  /**
   * 确认添加物品
   */
  onConfirmAdd() {
    const name = this.data.newItem.name.trim();
    const price = parseInt(this.data.newItem.price) || 0;
    
    console.log('[Price] onConfirmAdd: name=', name, 'price=', price);
    
    if (!name) {
      console.log('[Price] 物品名称为空');
      wx.showToast({
        title: '请输入物品名称',
        icon: 'none'
      });
      return;
    }
    
    if (price <= 0) {
      console.log('[Price] 价格无效');
      wx.showToast({
        title: '请输入有效价格',
        icon: 'none'
      });
      return;
    }
    
    // 检查是否已存在
    const exists = this.data.itemList.some(item => item.name === name);
    if (exists) {
      console.log('[Price] 物品已存在');
      wx.showToast({
        title: '物品已存在',
        icon: 'none'
      });
      return;
    }
    
    // 添加到列表
    const itemList = [...this.data.itemList, { name, price }];
    
    // 重新排序
    const sortedList = sortUtil.sortItems(itemList);
    this.setData({ 
      itemList: sortedList,
      showAddModal: false,
      newItem: { name: '', price: '' }
    });
    
    // 保存到全局数据
    this.savePriceToGlobal(name, price);
    
    // 更新价格快照
    this.savePriceSnapshot();
    
    wx.showToast({
      title: '添加成功',
      icon: 'success'
    });
    
    console.log('[Price] onConfirmAdd 完成');
  },

  onCloseModal() {
    console.log('[Price] onCloseModal');
    this.setData({ showAddModal: false });
  },

  stopPropagation() {
    // 阻止事件冒泡
  },

  /**
   * 恢复默认价格
   */
  onRestore() {
    console.log('[Price] onRestore 开始');
    
    wx.showModal({
      title: '确认恢复',
      content: '确定要恢复默认价格吗？当前修改将丢失。',
      success: (res) => {
        if (res.confirm) {
          console.log('[Price] 用户确认恢复');
          
          const app = getApp();
          const defaultPrices = app.getDefaultPrices();
          app.saveBasePrices(defaultPrices);
          
          // 重新加载数据
          this.loadPriceData();
          
          wx.showToast({
            title: '已恢复默认',
            icon: 'success'
          });
          
          console.log('[Price] onRestore 完成');
        } else {
          console.log('[Price] 用户取消恢复');
        }
      }
    });
  }
});
