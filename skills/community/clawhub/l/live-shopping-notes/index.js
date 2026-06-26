/**
 * Live Shopping Notes - 直播选品速记
 */

const { LocalStore } = require('../../shared/storage/local-store');

class LiveShoppingNotes {
  constructor() {
    this.store = new LocalStore('live-shopping-notes');
    this.currentSession = null;
    this.itemCounter = 0;
  }

  /**
   * 开始直播记录
   */
  startSession(liveInfo) {
    const session = {
      id: `live_${Date.now()}`,
      platform: liveInfo.platform,
      host: liveInfo.host,
      title: liveInfo.title,
      startTime: new Date().toISOString(),
      endTime: null,
      items: [],
      highlights: [],
      totalItems: 0
    };
    
    this.currentSession = session;
    this.store.set(`session_${session.id}`, session);
    
    return session;
  }

  /**
   * 快速记录商品
   */
  quickAdd(itemInfo) {
    if (!this.currentSession) {
      return { error: '请先开始直播记录' };
    }
    
    const item = {
      id: `item_${Date.now()}_${++this.itemCounter}`,
      timestamp: new Date().toISOString(),
      name: itemInfo.name,
      price: itemInfo.price,
      originalPrice: itemInfo.originalPrice,
      discount: this.calculateDiscount(itemInfo.price, itemInfo.originalPrice),
      description: itemInfo.description,
      tags: itemInfo.tags || [],
      interest: itemInfo.interest || 3, // 1-5 感兴趣程度
      notes: itemInfo.notes || '',
      link: itemInfo.link || null,
      status: 'noted'
    };
    
    this.currentSession.items.push(item);
    this.currentSession.totalItems++;
    this.saveCurrentSession();
    
    return { success: true, item };
  }

  /**
   * 语音/快捷记录（简化输入）
   */
  quickCapture(text) {
    // 解析自然语言输入
    // 示例: "李佳琦推荐的那个面霜，299，买一送一，挺划算的"
    
    const parsed = this.parseQuickInput(text);
    return this.quickAdd(parsed);
  }

  parseQuickInput(text) {
    // 提取价格
    const priceMatch = text.match(/(\d+)(?:元|块)/);
    const price = priceMatch ? parseInt(priceMatch[1]) : null;
    
    // 提取优惠
    const discountPatterns = [
      { pattern: /买一送一/, tag: '买一送一', value: 0.5 },
      { pattern: /(\d+)折/, tag: '折扣', value: (m) => parseInt(m[1]) / 10 },
      { pattern: /减(\d+)/, tag: '满减', value: (m) => parseInt(m[1]) },
      { pattern: /送.+/, tag: '赠品' }
    ];
    
    const tags = [];
    for (const dp of discountPatterns) {
      if (dp.pattern.test(text)) {
        tags.push(dp.tag);
      }
    }
    
    // 提取商品名（简化处理）
    const name = text.split(/[,，。！!]/)[0];
    
    return {
      name: name.slice(0, 30),
      price,
      tags,
      notes: text,
      interest: text.includes('划算') || text.includes('便宜') ? 4 : 3
    };
  }

  /**
   * 标记高光时刻
   */
  addHighlight(type, note) {
    if (!this.currentSession) return { error: '没有活动中的直播记录' };
    
    const highlight = {
      timestamp: new Date().toISOString(),
      type, // 'deal', 'tip', 'coupon', 'reminder'
      note,
      itemCount: this.currentSession.totalItems
    };
    
    this.currentSession.highlights.push(highlight);
    this.saveCurrentSession();
    
    return { success: true, highlight };
  }

  /**
   * 结束直播记录
   */
  endSession() {
    if (!this.currentSession) return { error: '没有活动中的直播记录' };
    
    this.currentSession.endTime = new Date().toISOString();
    this.saveCurrentSession();
    
    const summary = this.generateSummary(this.currentSession);
    this.currentSession = null;
    
    return summary;
  }

  /**
   * 生成直播总结
   */
  generateSummary(session) {
    const items = session.items;
    const duration = session.endTime 
      ? (new Date(session.endTime) - new Date(session.startTime)) / (1000 * 60)
      : 0;
    
    // 排序：按感兴趣程度 + 折扣力度
    const sortedItems = [...items].sort((a, b) => {
      const scoreA = a.interest * (1 + (a.discount || 0));
      const scoreB = b.interest * (1 + (b.discount || 0));
      return scoreB - scoreA;
    });
    
    // 分类统计
    const categories = {};
    items.forEach(item => {
      item.tags.forEach(tag => {
        categories[tag] = (categories[tag] || 0) + 1;
      });
    });
    
    return {
      sessionId: session.id,
      platform: session.platform,
      host: session.host,
      duration: Math.round(duration),
      totalItems: items.length,
      topItems: sortedItems.slice(0, 5),
      categories,
      highlights: session.highlights,
      totalValue: items.reduce((s, i) => s + (i.price || 0), 0),
      potentialSavings: items.reduce((s, i) => {
        if (!i.originalPrice || !i.price || i.originalPrice <= i.price) return s;
        return s + (i.originalPrice - i.price);
      }, 0)
    };
  }

  /**
   * 生成购买决策清单
   */
  generateDecisionList(sessionId) {
    const session = this.store.get(`session_${sessionId}`);
    if (!session) return { error: '直播记录不存在' };
    
    const items = session.items;
    
    // 决策矩阵
    const decisions = items.map(item => {
      const urgency = this.calculateUrgency(item);
      const value = this.calculateValue(item);
      
      return {
        ...item,
        urgency,
        value,
        decision: this.makeDecision(urgency, value, item.interest),
        action: this.suggestAction(urgency, value)
      };
    });
    
    // 分类
    return {
      buyNow: decisions.filter(d => d.decision === 'buy_now'),
      consider: decisions.filter(d => d.decision === 'consider'),
      skip: decisions.filter(d => d.decision === 'skip'),
      all: decisions
    };
  }

  calculateUrgency(item) {
    let score = 0;
    if (item.tags.includes('限时')) score += 3;
    if (item.tags.includes('限量')) score += 2;
    if (item.discount > 0.3) score += 2;
    if (item.discount > 0.5) score += 1;
    return Math.min(score, 5);
  }

  calculateValue(item) {
    if (!item.originalPrice || !item.price) return 3;
    const discount = (item.originalPrice - item.price) / item.originalPrice;
    if (discount > 0.5) return 5;
    if (discount > 0.3) return 4;
    if (discount > 0.1) return 3;
    return 2;
  }

  makeDecision(urgency, value, interest) {
    const score = urgency + value + interest;
    if (score >= 10) return 'buy_now';
    if (score >= 6) return 'consider';
    return 'skip';
  }

  suggestAction(urgency, value) {
    if (urgency >= 4 && value >= 4) return '立即下单';
    if (urgency >= 3) return '尽快决定';
    if (value >= 4) return '值得考虑';
    return '可买可不买';
  }

  calculateDiscount(price, originalPrice) {
    if (!price || !originalPrice) return 0;
    return (originalPrice - price) / originalPrice;
  }

  saveCurrentSession() {
    if (this.currentSession) {
      this.store.set(`session_${this.currentSession.id}`, this.currentSession);
    }
  }
}

module.exports = { LiveShoppingNotes };
