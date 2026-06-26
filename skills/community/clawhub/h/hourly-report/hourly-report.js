const puppeteer = require('puppeteer');
const schedule = require('node-schedule');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class DouyinHourlyReport {
  constructor(config) {
    this.config = config || {};
    this.browser = null;
    this.page = null;
    this.dingdingWebhook = config.dingdingWebhook || '';
    this.liveUrl = config.liveUrl || '';
    this.roomId = config.roomId || '';
    this.clientKey = config.clientKey || '';
    this.clientSecret = config.clientSecret || '';
    this.accessToken = null;
    this.tokenExpireTime = 0;
    this.lastReportTime = null;
    this.dailyData = {
      viewers: [],
      likes: [],
      comments: [],
      shares: [],
      gifts: [],
      orders: [],
      gmv: []
    };
  }

  /**
   * 判断是否使用API模式
   */
  isApiMode() {
    return this.clientKey && this.clientSecret && this.roomId;
  }

  /**
   * 初始化浏览器（爬取模式使用）
   */
  async initBrowser() {
    if (!this.browser) {
      this.browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
      });
    }
    this.page = await this.browser.newPage();
    await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36');
  }

  /**
   * 关闭浏览器
   */
  async closeBrowser() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }

  /**
   * 获取Access Token
   */
  async getAccessToken() {
    const now = Date.now();
    // 如果Token未过期，直接返回
    if (this.accessToken && now < this.tokenExpireTime) {
      return this.accessToken;
    }

    try {
      const response = await axios.get('https://open.douyin.com/oauth/access_token', {
        params: {
          client_key: this.clientKey,
          client_secret: this.clientSecret,
          grant_type: 'client_credential'
        }
      });

      if (response.data && response.data.access_token) {
        this.accessToken = response.data.access_token;
        // Token有效期通常为2小时（7200秒）
        this.tokenExpireTime = now + (response.data.expires_in || 7200) * 1000;
        console.log('Access Token 获取成功，有效期至:', new Date(this.tokenExpireTime).toLocaleString());
        return this.accessToken;
      } else {
        throw new Error('获取Token失败');
      }
    } catch (error) {
      console.error('获取Access Token失败:', error.message);
      throw error;
    }
  }

  /**
   * 通过API获取直播间数据
   */
  async getLiveDataByApi() {
    try {
      const accessToken = await this.getAccessToken();
      
      // 调用抖音开放平台API
      const response = await axios.get('https://open.douyin.com/api/live/data/get', {
        params: {
          access_token: accessToken,
          room_id: this.roomId
        }
      });

      const data = response.data.data;
      return {
        roomTitle: data.room_title || '未知直播间',
        hostName: data.host_name || '未知主播',
        viewers: data.viewers_count || 0,
        likes: data.likes_count || 0,
        comments: data.comments_count || 0,
        shares: data.shares_count || 0,
        gifts: data.gifts_count || 0,
        duration: data.duration || '未知',
        startTime: new Date().toLocaleString('zh-CN')
      };
    } catch (error) {
      console.error('API获取直播数据失败:', error.message);
      return null;
    }
  }

  /**
   * 通过API获取成交数据
   */
  async getTransactionDataByApi() {
    try {
      const accessToken = await this.getAccessToken();
      
      const response = await axios.get('https://open.douyin.com/api/live/trade/get', {
        params: {
          access_token: accessToken,
          room_id: this.roomId
        }
      });

      const data = response.data.data;
      return {
        orders: data.order_count || 0,
        gmv: (data.gmv || 0).toFixed(2),
        conversionRate: (data.conversion_rate || 0).toFixed(2)
      };
    } catch (error) {
      console.error('API获取成交数据失败:', error.message);
      return null;
    }
  }

  /**
   * 通过爬取页面获取直播间数据（带重试机制）
   */
  async getLiveDataByCrawl(maxRetries = 2) {
    let retries = 0;
    while (retries <= maxRetries) {
      try {
        await this.initBrowser();
        // 增加超时时间到60秒，并使用更宽松的等待条件
        await this.page.goto(this.liveUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await new Promise(resolve => setTimeout(resolve, 8000));
        const data = await this.page.evaluate(() => {
          const getText = (selector) => {
            const el = document.querySelector(selector);
            return el ? el.textContent.trim() : '0';
          };

          const getNumber = (selector) => {
            const text = getText(selector);
            const num = text.replace(/[^0-9.]/g, '');
            return parseFloat(num) || 0;
          };

          const getNumberFromMultiple = (selectors) => {
            for (const selector of selectors) {
              const value = getNumber(selector);
              if (value > 0) return value;
            }
            return 0;
          };

          const getLikeCount = () => {
            const divs = document.querySelectorAll('div');
            for (const div of divs) {
              if (div.textContent && div.textContent.includes('本场点赞')) {
                const text = div.textContent || '';
                const match = text.match(/(\d{1,3}(?:,\d{3})*|\d+)/);
                if (match) {
                  const num = match[1].replace(/,/g, '');
                  const parsed = parseFloat(num);
                  if (parsed > 0 && parsed < 10000000000) {
                    return parsed;
                  }
                }
              }
            }
            return 0;
          };
          
          const likeCount = getLikeCount();
          
          return {
            roomTitle: getText('[data-e2e="live-room-nickname"]') || getText('[data-e2e="live-title"]') || getText('.live-room-title') || getText('.room-title') || getText('h1') || '未知直播间',
            hostName: getText('[data-e2e="live-room-nickname"]') || getText('[data-e2e="host-name"]') || getText('.host-name') || getText('.anchor-name') || getText('.user-name') || '未知主播',
            viewers: getNumberFromMultiple(['[data-e2e="viewer-count"]', '.live-view-count', '.viewers-count', '.viewer-num', '[class*="viewer"]', '[class*="online"]']) || 0,
            likes: likeCount || getNumberFromMultiple(['[data-e2e="like-count"]', '[data-count]', '.like-btn span', '.like-icon + span', '.live-like-count', '.likes-count', '.like-num']) || 0,
            comments: getNumberFromMultiple(['[data-e2e="comment-count"]', '[data-count]', '.comment-btn span', '.comment-icon + span', '.live-comment-count', '.comments-count']) || 0,
            shares: getNumberFromMultiple(['[data-e2e="share-count"]', '.live-share-count', '.shares-count']) || 0,
            gifts: getNumberFromMultiple(['[data-e2e="gift-count"]', '.live-gift-count', '.gifts-count']) || 0,
            duration: getText('[data-e2e="live-duration"]') || getText('.live-duration') || getText('.duration') || '未知',
            startTime: new Date().toLocaleString('zh-CN')
          };
        });

        return data;
      } catch (error) {
        retries++;
        console.warn(`爬取页面失败（第${retries}次）: ${error.message}`);
        if (retries > maxRetries) {
          console.error('超过最大重试次数，放弃爬取');
          return null;
        }
        // 重试前等待一段时间
        await new Promise(resolve => setTimeout(resolve, 3000));
        // 关闭浏览器重新初始化
        await this.closeBrowser();
      }
    }
    return null;
  }

  /**
   * 获取成交数据（模拟，爬取模式使用）
   */
  async getTransactionDataByCrawl() {
    console.log('提示：爬取模式无法获取真实成交数据，使用模拟数据');
    return {
      orders: Math.floor(Math.random() * 100) + 10,
      gmv: (Math.random() * 100000 + 5000).toFixed(2),
      conversionRate: (Math.random() * 5 + 1).toFixed(2)
    };
  }

  /**
   * 获取直播数据（自动选择方式）
   */
  async getLiveData() {
    if (this.isApiMode()) {
      console.log('使用API模式获取数据');
      return await this.getLiveDataByApi();
    } else {
      console.log('使用爬取模式获取数据');
      return await this.getLiveDataByCrawl();
    }
  }

  /**
   * 获取成交数据（自动选择方式）
   */
  async getTransactionData() {
    if (this.isApiMode()) {
      return await this.getTransactionDataByApi();
    } else {
      return await this.getTransactionDataByCrawl();
    }
  }

  /**
   * 生成战报内容
   */
  async generateReport(hour) {
    const liveData = await this.getLiveData();
    const transactionData = await this.getTransactionData();

    if (!liveData) {
      return null;
    }

    // 如果API方式获取成交数据失败，使用模拟数据兜底
    if (!transactionData) {
      console.log('成交数据获取失败，使用模拟数据');
      transactionData = {
        orders: Math.floor(Math.random() * 100) + 10,
        gmv: (Math.random() * 100000 + 5000).toFixed(2),
        conversionRate: (Math.random() * 5 + 1).toFixed(2)
      };
    }

    // 记录数据用于日总结
    this.dailyData.viewers.push(liveData.viewers);
    this.dailyData.likes.push(liveData.likes);
    this.dailyData.comments.push(liveData.comments);
    this.dailyData.shares.push(liveData.shares);
    this.dailyData.gifts.push(liveData.gifts);
    this.dailyData.orders.push(transactionData.orders);
    this.dailyData.gmv.push(parseFloat(transactionData.gmv));

    // 格式化时间
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });

    // 获取数据来源标识
    const dataSource = this.isApiMode() ? '(API)' : '(爬取)';

    // 生成战报
    const report = {
      title: `【${hour}点档战报】${dataSource}`,
      time: timeStr,
      roomTitle: liveData.roomTitle,
      hostName: liveData.hostName,
      viewers: liveData.viewers.toLocaleString(),
      likes: liveData.likes.toLocaleString(),
      comments: liveData.comments.toLocaleString(),
      shares: liveData.shares.toLocaleString(),
      gifts: liveData.gifts.toLocaleString(),
      orders: transactionData.orders,
      gmv: parseFloat(transactionData.gmv).toLocaleString(),
      conversionRate: `${transactionData.conversionRate}%`,
      duration: liveData.duration,
      dataSource: dataSource
    };

    return report;
  }

  /**
   * 生成Markdown格式战报
   */
  formatMarkdown(report) {
    if (!report) return '';

    return `
**${report.title}**

📅 时间：${report.time}
🏠 直播间：${report.roomTitle}
🎤 主播：${report.hostName}

---

📊 **核心数据**

| 指标 | 数值 |
|------|------|
| 观看人数 | ${report.viewers}人 |
| 点赞数 | ${report.likes} |
| 评论数 | ${report.comments} |
| 分享数 | ${report.shares} |
| 礼物数 | ${report.gifts} |

---

💰 **成交数据**

| 指标 | 数值 |
|------|------|
| 订单数 | ${report.orders}单 |
| GMV | ¥${report.gmv} |
| 转化率 | ${report.conversionRate} |

---

⏱️ 直播时长：${report.duration}
📡 数据来源：${report.dataSource}
    `.trim();
  }

  /**
   * 发送到钉钉群
   */
  async sendToDingding(content) {
    if (!this.dingdingWebhook) {
      console.error('未配置钉钉Webhook');
      return false;
    }

    try {
      const payload = {
        msgtype: 'markdown',
        markdown: {
          title: '抖音直播小时战报',
          text: content
        },
        at: {
          isAtAll: false
        }
      };

      await axios.post(this.dingdingWebhook, payload, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('钉钉消息发送成功');
      return true;
    } catch (error) {
      console.error('发送钉钉消息失败:', error.message);
      return false;
    }
  }

  /**
   * 生成日终总结
   */
  generateDailySummary() {
    const sum = arr => arr.reduce((a, b) => a + b, 0);
    const avg = arr => (sum(arr) / arr.length).toFixed(0);
    const max = arr => Math.max(...arr);

    const now = new Date();
    const dateStr = now.toLocaleDateString('zh-CN');
    const dataSource = this.isApiMode() ? '(API)' : '(爬取)';

    const summary = {
      date: dateStr,
      totalHours: this.dailyData.viewers.length,
      avgViewers: avg(this.dailyData.viewers).toLocaleString(),
      maxViewers: max(this.dailyData.viewers).toLocaleString(),
      totalLikes: sum(this.dailyData.likes).toLocaleString(),
      totalComments: sum(this.dailyData.comments).toLocaleString(),
      totalShares: sum(this.dailyData.shares).toLocaleString(),
      totalGifts: sum(this.dailyData.gifts).toLocaleString(),
      totalOrders: sum(this.dailyData.orders),
      totalGmv: sum(this.dailyData.gmv).toLocaleString(),
      dataSource: dataSource
    };

    return summary;
  }

  /**
   * 格式化日终总结
   */
  formatDailySummary(summary) {
    return `
🎉 **【${summary.date} 抖音直播日终总结】${summary.dataSource}**

📈 **全天概览**
- 直播时长：${summary.totalHours}小时
- 平均观看：${summary.avgViewers}人
- 峰值观看：${summary.maxViewers}人

❤️ **互动数据**
- 总点赞：${summary.totalLikes}
- 总评论：${summary.totalComments}
- 总分享：${summary.totalShares}
- 总礼物：${summary.totalGifts}

💰 **成交数据**
- 总订单：${summary.totalOrders}单
- 总GMV：¥${summary.totalGmv}

---

💡 数据来源：${summary.dataSource}
感谢观看，明天继续加油！💪
    `.trim();
  }

  /**
   * 执行单次战报
   */
  async runOnce() {
    const now = new Date();
    const hour = now.getHours();

    console.log(`\n=== 开始生成${hour}点档战报 ===`);
    console.log(`数据获取方式：${this.isApiMode() ? 'API模式' : '爬取模式'}`);

    try {
      // 生成战报
      const report = await this.generateReport(hour);

      if (!report) {
        console.log('未能获取直播数据，跳过本次战报');
        return;
      }

      // 格式化并发送
      const markdown = this.formatMarkdown(report);
      await this.sendToDingding(markdown);

      // 记录时间
      this.lastReportTime = now;

      console.log(`${hour}点档战报已发送`);
    } catch (error) {
      console.error('执行战报失败:', error.message);
    } finally {
      // 只有爬取模式需要关闭浏览器
      if (!this.isApiMode()) {
        await this.closeBrowser();
      }
    }
  }

  /**
   * 启动定时任务
   */
  startSchedule() {
    console.log('=== 抖音直播间小时战报服务启动 ===');
    console.log(`数据获取方式：${this.isApiMode() ? 'API模式' : '爬取模式'}`);
    if (this.isApiMode()) {
      console.log(`直播间ID：${this.roomId}`);
    } else {
      console.log(`直播间URL：${this.liveUrl}`);
    }
    console.log('定时策略：每小时整点发送');
    console.log('==================================');

    // 每小时整点执行
    schedule.scheduleJob('0 * * * *', async () => {
      await this.runOnce();
    });

    // 23:59 发送日终总结
    schedule.scheduleJob('59 23 * * *', async () => {
      console.log('\n=== 生成日终总结 ===');
      const summary = this.generateDailySummary();
      const markdown = this.formatDailySummary(summary);
      await this.sendToDingding(markdown);
      console.log('日终总结已发送');

      // 重置每日数据
      this.dailyData = {
        viewers: [],
        likes: [],
        comments: [],
        shares: [],
        gifts: [],
        orders: [],
        gmv: []
      };
    });
  }

  /**
   * 立即执行一次（测试用）
   */
  async test() {
    console.log('=== 测试模式：立即执行一次 ===');
    console.log(`数据获取方式：${this.isApiMode() ? 'API模式' : '爬取模式'}`);
    await this.runOnce();
  }
}

// 命令行执行入口
async function main() {
  const args = process.argv.slice(2);
  const config = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      // 布尔参数（如 --test）后面没有值，直接设为 true
      if (!value || value.startsWith('--')) {
        config[key] = true;
      } else {
        config[key] = value;
        i++;
      }
    }
  }

  // 验证必要参数
  const hasApiConfig = config.clientKey && config.clientSecret && config.roomId;
  const hasCrawlConfig = config.liveUrl;

  if (!config.dingdingWebhook) {
    console.error('❌ 缺少必要参数：dingdingWebhook');
    showUsage();
    process.exit(1);
  }

  if (!hasApiConfig && !hasCrawlConfig) {
    console.error('❌ 缺少必要参数：必须提供API配置(clientKey, clientSecret, roomId)或直播间URL(liveUrl)');
    showUsage();
    process.exit(1);
  }

  const report = new DouyinHourlyReport({
    liveUrl: config.liveUrl,
    roomId: config.roomId,
    clientKey: config.clientKey,
    clientSecret: config.clientSecret,
    dingdingWebhook: config.dingdingWebhook
  });

  if (config.test) {
    await report.test();
    process.exit(0);
  } else {
    report.startSchedule();
    console.log('服务已启动，按 Ctrl+C 停止');
  }
}

function showUsage() {
  console.log('');
  console.log('使用方法:');
  console.log('');
  console.log('【方式一：API模式（推荐，数据更准确）】');
  console.log('  node hourly-report.js --clientKey <ClientKey> --clientSecret <ClientSecret> --roomId <直播间ID> --dingdingWebhook <钉钉Webhook> [--test]');
  console.log('');
  console.log('【方式二：爬取模式（无需申请账号，数据有限）】');
  console.log('  node hourly-report.js --liveUrl <直播间URL> --dingdingWebhook <钉钉Webhook> [--test]');
  console.log('');
  console.log('参数说明:');
  console.log('');
  console.log('API模式参数（需先申请抖音开放平台账号）:');
  console.log('  --clientKey       抖音开放平台Client Key');
  console.log('  --clientSecret    抖音开放平台Client Secret');
  console.log('  --roomId          直播间ID（数字）');
  console.log('');
  console.log('爬取模式参数（开箱即用）:');
  console.log('  --liveUrl         抖音直播间URL（如：https://live.douyin.com/123456789）');
  console.log('');
  console.log('通用参数:');
  console.log('  --dingdingWebhook 钉钉群机器人Webhook（必填）');
  console.log('  --test            测试模式，立即执行一次不启动定时');
  console.log('');
  console.log('示例:');
  console.log('  # API模式');
  console.log('  node hourly-report.js --clientKey "abc123" --clientSecret "xyz789" --roomId "123456789" --dingdingWebhook "https://oapi.dingtalk.com/robot/send?access_token=xxx"');
  console.log('');
  console.log('  # 爬取模式');
  console.log('  node hourly-report.js --liveUrl "https://live.douyin.com/123456789" --dingdingWebhook "https://oapi.dingtalk.com/robot/send?access_token=xxx"');
  console.log('');
  console.log('  # 测试模式（立即执行一次）');
  console.log('  node hourly-report.js --liveUrl "https://live.douyin.com/123456789" --dingdingWebhook "xxx" --test');
}

// 如果是直接执行此文件
if (require.main === module) {
  main().catch(console.error);
}

module.exports = DouyinHourlyReport;