/**
 * 飞书卡片发送器核心类
 * Core Feishu Card Sender Class
 * 
 * @description 负责实际的卡片发送操作，集成OpenClaw message工具
 * @author OpenClaw Team
 * @version 1.0.0
 */

class FeishuCardSender {
  constructor(config = {}) {
    this.config = {
      channel: 'feishu',
      timeout: 30000,
      retryAttempts: 3,
      retryDelay: 1000,
      ...config
    };
    
    this.stats = {
      totalSent: 0,
      successCount: 0,
      failedCount: 0,
      lastSent: null
    };

    console.log('🔧 FeishuCardSender initialized');
  }

  /**
   * 发送卡片消息
   * @param {Object} renderedCard - 渲染后的卡片数据
   * @param {string} target - 发送目标
   * @returns {Promise<Object>} 发送结果
   */
  async sendCard(renderedCard, target = null) {
    try {
      const startTime = Date.now();
      
      // 根据不同格式准备消息内容
      let messageContent;
      
      switch (renderedCard.type) {
        case 'native_card':
          messageContent = {
            type: "interactive",
            card: renderedCard.data
          };
          break;
          
        case 'adaptive_card':
          messageContent = {
            type: "adaptive_card",
            card: renderedCard.data
          };
          break;
          
        case 'template':
          messageContent = {
            type: "template",
            ...renderedCard.data
          };
          break;
          
        default:
          throw new Error(`不支持的卡片格式: ${renderedCard.type}`);
      }

      // 使用OpenClaw message工具发送
      const result = await this.sendMessage(messageContent, target);
      
      // 更新统计
      this.updateStats(true);
      
      return {
        success: true,
        messageId: result.messageId,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      console.error(`发送卡片失败:`, error);
      
      // 更新统计
      this.updateStats(false);
      
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * 使用OpenClaw message工具发送消息
   * @param {Object} content - 消息内容
   * @param {string} target - 发送目标
   * @returns {Promise<Object>} 发送结果
   */
  async sendMessage(content, target = null) {
    try {
      // 这里模拟调用OpenClaw的message工具
      // 在实际环境中，这里会调用真实的API
      console.log('🔄 调用OpenClaw message工具...');
      console.log('📤 消息内容:', JSON.stringify(content, null, 2));
      
      if (target) {
        console.log(`🎯 发送目标: ${target}`);
      }

      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 模拟成功响应
      return {
        success: true,
        messageId: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      console.error('消息发送失败:', error);
      throw error;
    }
  }

  /**
   * 批量发送卡片（基础实现）
   * @param {Array} cards - 卡片数组
   * @returns {Promise<Array>} 发送结果数组
   */
  async sendBatch(cards) {
    const results = [];
    
    for (let i = 0; i < cards.length; i++) {
      const card = cards[i];
      
      try {
        const result = await this.sendCard(card.renderedCard, card.target);
        results.push({
          index: i,
          success: result.success,
          messageId: result.messageId,
          error: result.error
        });
      } catch (error) {
        results.push({
          index: i,
          success: false,
          error: error.message
        });
      }
      
      // 添加延迟避免触发频率限制
      if (i < cards.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    return results;
  }

  /**
   * 更新发送统计
   * @param {boolean} success - 是否成功
   */
  updateStats(success) {
    this.stats.totalSent++;
    this.stats.lastSent = new Date().toISOString();
    
    if (success) {
      this.stats.successCount++;
    } else {
      this.stats.failedCount++;
    }
  }

  /**
   * 获取发送统计
   * @returns {Object} 统计信息
   */
  getStats() {
    return {
      ...this.stats,
      successRate: this.stats.totalSent > 0 
        ? Math.round((this.stats.successCount / this.stats.totalSent) * 100) 
        : 0
    };
  }

  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalSent: 0,
      successCount: 0,
      failedCount: 0,
      lastSent: null
    };
  }

  /**
   * 获取版本信息
   * @returns {Object} 版本信息
   */
  getVersion() {
    return {
      version: '1.0.0',
      buildDate: '2026-02-28',
      module: 'FeishuCardSender'
    };
  }

  /**
   * 测试连接
   * @returns {Promise<Object>} 测试结果
   */
  async testConnection() {
    try {
      // 发送测试消息
      const testContent = {
        type: "text",
        content: {
          text: "🔧 飞书卡片发送器连接测试"
        }
      };
      
      const result = await this.sendMessage(testContent);
      
      return {
        success: true,
        message: '连接测试成功',
        messageId: result.messageId,
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }
}

module.exports = {
  FeishuCardSender
};