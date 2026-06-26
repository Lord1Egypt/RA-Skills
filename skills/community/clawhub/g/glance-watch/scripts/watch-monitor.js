import { OpenClawPluginAdapter } from 'openclaw-glance-plugin';

const bridgeBase = 'ws://glanceup-pre.100credit.cn';
const token = process.env.OPENCLAW_WS_TOKEN;

const adapter = new OpenClawPluginAdapter({
  baseWsUrl: bridgeBase,
  token,
  enqueueIfDisconnected: true
});

// 监控触发回调
adapter.onTriggered((event) => {
  console.log('TRIGGERED:', JSON.stringify(event));
  
  // 解析触发事件
  const { product_code, product_type, message, market_data } = event;
  const price = market_data?.price;
  const changePercent = market_data?.change_percent;
  
  // TODO: 根据不同渠道发送提醒
  // 飞书群: message action=send to=chat:xxx
  // Telegram: message action=send channel=telegram
  // Discord: message action=send channel=discord
});

await adapter.start();

// 盯盘请求参数
const watchDemand = {
  // 产品代码
  productCode: 'BTCUSDT',        // 股票代码/指数代码/加密货币
  // 市场类型: stock(A股个股), index(A股指数), hk_stock(港股), crypto(比特币)
  productType: 'crypto',         
  // 条件表达式
  condition: 'price >= threshold and change_percent >= cp_threshold',
  // 变量
  variables: { 
    threshold: 73000,
    cp_threshold: 0.01,
    product_name: 'Bitcoin'
  },
  // openclaw 必传；email/call 可选
  channels: ['openclaw', 'email', 'call'],
  emailConfig: {
    to_address: 'demo@example.com',
    template_id: 4
  },
  callConfig: {
    phone: '13800138000',
    customer_name: 'Demo'
  }
};

const resp = await adapter.submitWatchDemand(watchDemand);
console.log('Created:', JSON.stringify(resp));
