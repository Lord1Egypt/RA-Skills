#!/usr/bin/env node

/**
 * 企业微信API工具类
 * 提供企业微信消息推送和智能表格记录功能
 */

const axios = require('axios');
const crypto = require('crypto');

class WeChatWorkAPI {
  constructor(config) {
    this.config = config;
    this.baseUrl = 'https://qyapi.weixin.qq.com';
  }

  /**
   * 发送消息到企业微信群
   * @param {Object} message - 消息内容
   * @param {string} webhookUrl - Webhook URL（可选，如果不使用则配置文件中的）
   */
  async sendMessage(message, webhookUrl = null) {
    const url = webhookUrl || this.config.webhookUrl;
    
    if (!url) {
      throw new Error('企业微信Webhook URL未配置');
    }

    try {
      const response = await axios.post(url, message, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      if (response.data.errcode !== 0) {
        throw new Error(`企业微信API错误: ${response.data.errmsg} (错误码: ${response.data.errcode})`);
      }

      return response.data;
    } catch (error) {
      console.error('发送企业微信消息失败:', error.message);
      throw error;
    }
  }

  /**
   * 发送文本消息
   * @param {string} content - 消息内容
   * @param {string} webhookUrl - Webhook URL
   */
  async sendText(content, webhookUrl = null) {
    const message = {
      msgtype: 'text',
      text: {
        content: content
      }
    };
    return this.sendMessage(message, webhookUrl);
  }

  /**
   * 发送Markdown消息
   * @param {string} content - Markdown格式内容
   * @param {string} webhookUrl - Webhook URL
   */
  async sendMarkdown(content, webhookUrl = null) {
    const message = {
      msgtype: 'markdown',
      markdown: {
        content: content
      }
    };
    return this.sendMessage(message, webhookUrl);
  }

  /**
   * 发送卡片消息
   * @param {Object} card - 卡片内容
   * @param {string} webhookUrl - Webhook URL
   */
  async sendCard(card, webhookUrl = null) {
    const message = {
      msgtype: 'template_card',
      template_card: card
    };
    return this.sendMessage(message, webhookUrl);
  }

  /**
   * 记录数据到智能表格
   * @param {Object} data - 数据记录
   * @param {string} smartTableId - 智能表格ID
   */
  async recordToSmartTable(data, smartTableId = null) {
    const tableId = smartTableId || this.config.smartTableId;
    
    if (!tableId) {
      throw new Error('企业微信智能表格ID未配置');
    }

    if (!this.config.apiToken) {
      throw new Error('企业微信API Token未配置');
    }

    try {
      const url = `${this.baseUrl}/cgi-bin/smarttable/add?access_token=${this.config.apiToken}`;
      
      const formData = {
        formid: tableId,
        data: JSON.stringify([data])
      };

      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 10000
      });

      if (response.data.errcode !== 0) {
        throw new Error(`智能表格API错误: ${response.data.errmsg} (错误码: ${response.data.errcode})`);
      }

      return response.data;
    } catch (error) {
      console.error('记录到智能表格失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取访问令牌
   * @param {string} corpId - 企业ID
   * @param {string} corpSecret - 应用Secret
   */
  async getAccessToken(corpId, corpSecret) {
    try {
      const url = `${this.baseUrl}/cgi-bin/gettoken?corpid=${corpId}&corpsecret=${corpSecret}`;
      const response = await axios.get(url, { timeout: 10000 });
      
      if (response.data.errcode !== 0) {
        throw new Error(`获取访问令牌失败: ${response.data.errmsg}`);
      }

      return response.data.access_token;
    } catch (error) {
      console.error('获取访问令牌失败:', error.message);
      throw error;
    }
  }

  /**
   * 验证回调URL
   * @param {string} msgSignature - 签名
   * @param {string} timestamp - 时间戳
   * @param {string} nonce - 随机数
   * @param {string} echoStr - 随机字符串
   */
  verifyCallback(msgSignature, timestamp, nonce, echoStr) {
    if (!this.config.encodingAESKey) {
      throw new Error('企业微信EncodingAESKey未配置');
    }

    const token = this.config.token || '';
    const list = [token, timestamp, nonce, echoStr].sort();
    const sha1 = crypto.createHash('sha1');
    sha1.update(list.join(''));
    const signature = sha1.digest('hex');

    return signature === msgSignature;
  }

  /**
   * 解密回调消息
   * @param {string} encryptedMsg - 加密消息
   */
  decryptCallbackMessage(encryptedMsg) {
    if (!this.config.encodingAESKey) {
      throw new Error('企业微信EncodingAESKey未配置');
    }

    // 这里需要实现具体的解密逻辑
    // 由于解密需要特定的库，这里提供基本框架
    console.log('解密回调消息:', encryptedMsg);
    return encryptedMsg; // 实际使用时需要实现解密
  }
}

module.exports = WeChatWorkAPI;