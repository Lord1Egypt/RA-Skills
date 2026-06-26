/**
 * CDB 数据库配置
 * 
 * 用于存储：
 * 1. 买家会话记录
 * 2. 话术使用统计
 * 3. 客服接待数据
 * 4. 店铺配置信息
 */

import { ConvexClient } from 'convex/browser'
import { api } from './_generated/api'

// CDB 配置
export const CDB_CONFIG = {
  // 数据库表定义
  tables: {
    // 会话记录表
    conversations: {
      fields: {
        conversationId: 'string',
        buyerId: 'string',
        buyerName: 'string',
        shopId: 'string',
        messages: 'array', // 消息数组
        startTime: 'number', // 时间戳
        endTime: 'number',
        status: 'string', // active, closed, transferred
        tags: 'array', // 会话标签
        rating: 'number', // 买家评分（1-5）
        createdAt: 'number',
        updatedAt: 'number'
      }
    },

    // 消息记录表
    messages: {
      fields: {
        messageId: 'string',
        conversationId: 'string',
        senderType: 'string', // buyer, seller, system
        content: 'string',
        messageType: 'string', // text, image, order, logistics
        timestamp: 'number',
        isRead: 'boolean',
        isReplied: 'boolean',
        replyTemplateId: 'string', // 使用的回复话术 ID
        createdAt: 'number'
      }
    },

    // 话术使用统计表
    templateStats: {
      fields: {
        templateId: 'string',
        templateCategory: 'string',
        usageCount: 'number',
        successRate: 'number', // 使用后买家满意度
        avgResponseTime: 'number',
        lastUsedAt: 'number',
        createdAt: 'number',
        updatedAt: 'number'
      }
    },

    // 客服接待统计表
    serviceStats: {
      fields: {
        shopId: 'string',
        date: 'string', // YYYY-MM-DD
        totalConversations: 'number',
        totalMessages: 'number',
        avgResponseTime: 'number', // 平均响应时间（秒）
        replyRate: 'number', // 回复率
        satisfactionRate: 'number', // 满意度
        conversionRate: 'number', // 转化率
        createdAt: 'number',
        updatedAt: 'number'
      }
    },

    // 店铺配置表
    shopConfigs: {
      fields: {
        shopId: 'string',
        shopName: 'string',
        autoReplyEnabled: 'boolean',
        workingHours: 'object', // { start: '09:00', end: '22:00' }
        welcomeMessage: 'string',
        defaultTemplates: 'array',
        notificationSettings: 'object',
        createdAt: 'number',
        updatedAt: 'number'
      }
    },

    // 买家信息表
    buyers: {
      fields: {
        buyerId: 'string',
        nickname: 'string',
        avatar: 'string',
        totalOrders: 'number',
        totalSpent: 'number',
        lastContactAt: 'number',
        tags: 'array', // 买家标签（VIP、常客等）
        notes: 'string', // 客服备注
        createdAt: 'number',
        updatedAt: 'number'
      }
    }
  },

  // 索引定义
  indexes: {
    conversations: [
      'by_buyer_id',
      'by_shop_id',
      'by_status',
      'by_created_at'
    ],
    messages: [
      'by_conversation_id',
      'by_timestamp',
      'by_sender_type'
    ],
    templateStats: [
      'by_category',
      'by_usage_count'
    ],
    serviceStats: [
      'by_shop_id',
      'by_date'
    ]
  }
}

// CDB 初始化
export class CDB {
  private client: ConvexClient
  private shopId: string

  constructor(shopId: string) {
    this.shopId = shopId
    this.client = new ConvexClient(process.env.CDB_URL!)
  }

  /**
   * 保存会话记录
   */
  async saveConversation(conversation: any) {
    return await this.client.mutation(api.conversations.create, {
      ...conversation,
      shopId: this.shopId
    })
  }

  /**
   * 保存消息记录
   */
  async saveMessage(message: any) {
    return await this.client.mutation(api.messages.create, {
      ...message,
      shopId: this.shopId
    })
  }

  /**
   * 更新话术使用统计
   */
  async updateTemplateStats(templateId: string, success: boolean) {
    return await this.client.mutation(api.templateStats.update, {
      templateId,
      success,
      shopId: this.shopId
    })
  }

  /**
   * 查询买家历史会话
   */
  async getBuyerHistory(buyerId: string) {
    return await this.client.query(api.conversations.getByBuyerId, {
      buyerId,
      shopId: this.shopId
    })
  }

  /**
   * 获取今日接待统计
   */
  async getTodayStats() {
    const today = new Date().toISOString().split('T')[0]
    return await this.client.query(api.serviceStats.getByDate, {
      shopId: this.shopId,
      date: today
    })
  }

  /**
   * 获取热门话术
   */
  async getTopTemplates(limit: number = 10) {
    return await this.client.query(api.templateStats.getTop, {
      shopId: this.shopId,
      limit
    })
  }
}

// 导出 CDB 实例
export function createCDB(shopId: string): CDB {
  return new CDB(shopId)
}
