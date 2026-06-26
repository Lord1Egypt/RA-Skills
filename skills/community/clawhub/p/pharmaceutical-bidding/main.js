#!/usr/bin/env node

/**
 * Pharmaceutical System Bidding Information Collector
 * 自动收集药学系统相关的招标信息
 */

const axios = require('axios');
const cheerio = require('cheerio');
const cron = require('node-cron');
const moment = require('moment');
const WeChatWorkAPI = require('./wechat-api');

class PharmaceuticalBiddingCollector {
  constructor(config) {
    this.config = config || {};
    this.procurementUrls = [
      'https://www.ccgp.gov.cn', // 中央政府采购网
      'https://www.zfcg.gov.cn',   // 中国政府采购网
      // 添加省级招标网站
    ];
    
    this.keywords = ['药学系统', '医院药学', '药房管理系统', '药品管理系统'];
    this.minBudget = 1000000; // 100万
    this.hospitalTypes = ['三级医院', '县人民医院'];
    
    // 初始化企业微信API
    this.wechatAPI = new WeChatWorkAPI(this.config.wechatWork || {});
  }

  /**
   * 步骤1: 搜索省级招标网站获取药学系统相关招标信息
   */
  async searchProcurementWebsites() {
    console.log('开始搜索招标网站...');
    const results = [];
    
    for (const url of this.procurementUrls) {
      try {
        const searchResults = await this.searchWebsite(url);
        results.push(...searchResults);
      } catch (error) {
        console.error(`搜索网站失败: ${url}`, error.message);
      }
    }
    
    return results;
  }

  /**
   * 步骤2: 验证和筛选符合要求的招标信息
   */
  async filterBiddingInfo(biddingInfos) {
    console.log('开始验证和筛选招标信息...');
    const validInfos = [];
    
    for (const info of biddingInfos) {
      try {
        // 验证条件1: 招标的产品是药学系统
        const isPharmaceutical = this.isPharmaceuticalSystem(info);
        
        // 验证条件2: 获取招标文件的截止时间 > 2天
        const hasValidDeadline = this.hasValidDeadline(info);
        
        if (isPharmaceutical && hasValidDeadline) {
          validInfos.push(info);
        }
      } catch (error) {
        console.error(`验证信息失败: ${info.title}`, error.message);
      }
    }
    
    return validInfos;
  }

  /**
   * 步骤3: 如果出处地址无法收集有效信息，通过搜索引擎二次查询
   */
  async secondarySearch(infos) {
    console.log('开始二次搜索...');
    const enhancedInfos = [];
    
    for (const info of infos) {
      try {
        if (!this.hasCompleteInfo(info)) {
          const enhanced = await this.searchEngineEnhance(info);
          enhancedInfos.push(enhanced);
        } else {
          enhancedInfos.push(info);
        }
      } catch (error) {
        console.error(`二次搜索失败: ${info.title}`, error.message);
      }
    }
    
    return enhancedInfos;
  }

  /**
   * 步骤4: 记录挂网的关键信息到企微智能表格
   */
  async recordToWeChatWork(infos) {
    console.log('记录信息到企微智能表格...');
    
    for (const info of infos) {
      try {
        const record = {
          购标截止日期: info.deadline,
          开标日期: info.openingDate,
          招标单位: info.biddingUnit,
          项目名称: info.title,
          预算金额: info.budget,
          涉及产品范围: info.productScope,
          对应负责销售: this.assignSalesPerson(info),
          项目状态: this.evaluateProject(info)
        };
        
        // 这里需要实现企微API调用
        await this.postToWeChatWork(record);
        console.log(`已记录: ${info.title}`);
      } catch (error) {
        console.error(`记录到企微失败: ${info.title}`, error.message);
      }
    }
  }

  /**
   * 步骤5: 评估招标文件并给出投标建议
   */
  async evaluateBidding(info) {
    console.log(`评估招标项目: ${info.title}`);
    
    let suggestion = '';
    let riskLevel = 'low';
    
    try {
      if (info.hasBiddingDoc) {
        // 解读招标文件
        const docAnalysis = await this.analyzeBiddingDocument(info);
        suggestion = this.generateBiddingSuggestion(docAnalysis);
      } else {
        // 基于可用信息评估
        suggestion = this.generateBasicSuggestion(info);
      }
      
      return {
        suggestion,
        riskLevel,
        shouldParticipate: this.shouldParticipate(info)
      };
    } catch (error) {
      console.error(`评估失败: ${info.title}`, error.message);
      return {
        suggestion: '评估失败，请手动审核',
        riskLevel: 'unknown',
        shouldParticipate: false
      };
    }
  }

  /**
   * 步骤6: 判断是否标记为可参与项目
   */
  shouldParticipate(info) {
    const currentDate = moment();
    const openingDate = moment(info.openingDate);
    const deadline = moment(info.deadline);
    
    // 条件1: 开标时间-当日日期>10天，且可以购买或领取标书-当日日期>2天
    const condition1 = openingDate.diff(currentDate, 'days') > 10 && 
                      deadline.diff(currentDate, 'days') > 2;
    
    // 条件2: 项目预算金额>100万
    const condition2 = info.budget > this.minBudget;
    
    // 条件3: 招标单位为三级医院或县人民医院
    const condition3 = this.hospitalTypes.some(type => 
      info.biddingUnit.includes(type)
    );
    
    return condition1 || condition2 || condition3;
  }

  // 辅助方法
  isPharmaceuticalSystem(info) {
    return this.keywords.some(keyword => 
      info.title.includes(keyword) || info.description.includes(keyword)
    );
  }

  hasValidDeadline(info) {
    const deadline = moment(info.deadline);
    const now = moment();
    return deadline.diff(now, 'days') > 2;
  }

  hasCompleteInfo(info) {
    return info.biddingUnit && info.budget && info.openingDate;
  }

  assignSalesPerson(info) {
    // 根据项目类型和地区分配销售人员
    // 这里需要实现具体的分配逻辑
    return '待分配';
  }

  async postToWeChatWork(record) {
    try {
      // 发送Markdown格式的消息到企微
      const markdownContent = `## 📋 新招标信息通知

**项目名称**: ${record['项目名称'] || '未知'}
**招标单位**: ${record['招标单位'] || '未知'}
**预算金额**: ${record['预算金额'] || '未知'}
**购标截止日期**: ${record['购标截止日期'] || '未知'}
**开标日期**: ${record['开标日期'] || '未知'}
**涉及产品范围**: ${record['涉及产品范围'] || '未知'}
**对应负责销售**: ${record['对应负责销售'] || '待分配'}
**项目状态**: ${record['项目状态'] || '待评估'}

---

*此消息由药学系统招标信息自动收集系统发送*`;

      await this.wechatAPI.sendMarkdown(markdownContent);
      
      // 如果配置了智能表格，同时记录到表格
      if (this.config.wechatWork.smartTableId) {
        await this.wechatAPI.recordToSmartTable(record);
      }
      
      console.log('成功发送到企业微信:', record['项目名称']);
    } catch (error) {
      console.error('发送到企业微信失败:', error.message);
      throw error;
    }
  }

  async analyzeBiddingDocument(info) {
    // 分析招标文件
    return {
      qualifications: '满足',
      technicalParams: '符合',
      budget: '充足',
      timeline: '合理'
    };
  }

  generateBiddingSuggestion(analysis) {
    if (analysis.qualifications === '满足' && analysis.budget === '充足') {
      return '建议投标，项目条件良好';
    } else if (analysis.qualifications === '满足' && analysis.budget === '紧张') {
      return '可考虑投标，但需注意预算控制';
    } else {
      return '不建议投标，条件不符合要求';
    }
  }

  generateBasicSuggestion(info) {
    if (this.shouldParticipate(info)) {
      return '建议投标，项目符合参与条件';
    } else {
      return '需进一步评估，暂不建议投标';
    }
  }

  // 定时任务
  startScheduledTask() {
    // 每天早上8:30执行
    cron.schedule('30 8 * * *', async () => {
      console.log('开始执行定时招标信息收集任务...');
      try {
        await this.executeFullWorkflow();
      } catch (error) {
        console.error('定时任务执行失败:', error.message);
      }
    });
  }

  // 完整工作流程
  async executeFullWorkflow() {
    try {
      // 1. 搜索招标信息
      const biddingInfos = await this.searchProcurementWebsites();
      
      // 2. 验证筛选
      const filteredInfos = await this.filterBiddingInfo(biddingInfos);
      
      // 3. 二次搜索
      const enhancedInfos = await this.secondarySearch(filteredInfos);
      
      // 4. 记录到企微
      await this.recordToWeChatWork(enhancedInfos);
      
      // 5. 评估每个项目
      for (const info of enhancedInfos) {
        const evaluation = await this.evaluateBidding(info);
        console.log(`项目评估结果 - ${info.title}: ${evaluation.suggestion}`);
      }
      
      console.log('招标信息收集任务完成');
    } catch (error) {
      console.error('工作流程执行失败:', error.message);
      throw error;
    }
  }
}

// 使用示例
if (require.main === module) {
  // 从配置文件加载配置
  const fs = require('fs');
  const configPath = './config.json';
  
  let config = {};
  try {
    if (fs.existsSync(configPath)) {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
  } catch (error) {
    console.error('读取配置文件失败:', error.message);
  }
  
  const collector = new PharmaceuticalBiddingCollector(config);
  
  // 启动定时任务
  collector.startScheduledTask();
  
  // 立即执行一次（用于测试）
  collector.executeFullWorkflow().catch(console.error);
}

module.exports = PharmaceuticalBiddingCollector;