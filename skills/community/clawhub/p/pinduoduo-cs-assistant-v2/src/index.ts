/**
 * 拼多多商家客服自动化助手
 * 
 * 核心功能：
 * 1. 浏览器自动化登录拼多多商家后台
 * 2. 智能读取买家消息
 * 3. 自动生成回复话术
 * 4. 快捷发送回复
 * 5. 售后订单处理
 */

import { browser } from '@openclaw/browser-tools'

// 配置
const CONFIG = {
  pddUrl: 'https://mms.pinduoduo.com',
  chatUrl: 'https://mms.pinduoduo.com/chat',
  checkInterval: 5000, // 消息检查间隔（毫秒）
  sessionTimeout: 86400000 // Session 超时（24 小时）
}

// 话术库
const TEMPLATES = {
  售前: [
    {
      keywords: ['有货吗', '还有货', '库存', '没货'],
      response: '亲，这款商品目前有现货的哦，您可以直接下单~'
    },
    {
      keywords: ['什么时候发货', '几天发', '发货时间'],
      response: '亲，我们一般在下单后 24-48 小时内发货，节假日顺延~'
    },
    {
      keywords: ['能便宜吗', '优惠', '打折', '包邮'],
      response: '亲，现在店铺有满减活动，满 99 减 10，满 199 减 30，很划算的哦~'
    },
    {
      keywords: ['什么材质', '质量怎么样', '好不好'],
      response: '亲，我们家都是精选优质材质，质量有保证的，支持 7 天无理由退换~'
    }
  ],
  物流: [
    {
      keywords: ['到哪了', '物流信息', '快递', '运输中'],
      response: '亲，帮您查了一下，您的包裹正在运输中，预计 2-3 天送达，请耐心等待~'
    },
    {
      keywords: ['怎么还没到', '太慢了', '好慢'],
      response: '亲，非常理解您的心情，我帮您催一下快递公司，有进展马上通知您~'
    },
    {
      keywords: ['发什么快递', '能指定快递吗'],
      response: '亲，我们默认发中通快递，如需指定请留言，我们会尽量安排~'
    }
  ],
  售后: [
    {
      keywords: ['退货', '退款', '不要了', '不想要'],
      response: '亲，支持 7 天无理由退换货的，您在订单页面申请一下，我们马上处理~'
    },
    {
      keywords: ['质量问题', '坏了', '破损', '有瑕疵'],
      response: '亲，非常抱歉给您带来不好的体验，您拍个照片，我们给您补发或全额退款~'
    },
    {
      keywords: ['差评', '投诉', '举报'],
      response: '亲，真的非常抱歉，您有什么问题随时联系我们，一定给您满意解决方案~'
    },
    {
      keywords: ['发票', '开票', '收据'],
      response: '亲，确认收货后在订单页面申请开票，电子发票会发送到您的邮箱~'
    }
  ]
}

/**
 * 登录拼多多商家后台
 */
async function login(shopName?: string) {
  console.log('🛒 正在打开拼多多商家后台...')
  
  // 打开登录页面
  await browser.open(CONFIG.pddUrl)
  
  // 等待页面加载
  await new Promise(resolve => setTimeout(resolve, 3000))
  
  // 获取页面快照
  const snapshot = await browser.snapshot({ refs: 'aria' })
  
  // 检测登录状态
  const isLoggedIn = await checkLoginStatus()
  
  if (isLoggedIn) {
    console.log('✅ 已登录状态')
    return true
  }
  
  console.log('⏳ 请扫码登录或使用账号密码登录')
  console.log('📱 打开手机拼多多扫描屏幕二维码')
  
  // 等待登录（轮询检测）
  return await waitForLogin()
}

/**
 * 检查登录状态
 */
async function checkLoginStatus(): Promise<boolean> {
  try {
    const result = await browser.evaluate(() => {
      // 检测用户头像或商家名称
      const avatar = document.querySelector('.user-avatar')
      const shopName = document.querySelector('.shop-name')
      return !!(avatar || shopName)
    })
    return result
  } catch (e) {
    return false
  }
}

/**
 * 等待登录完成
 */
async function waitForLogin(maxWaitTime = 120000): Promise<boolean> {
  const startTime = Date.now()
  
  while (Date.now() - startTime < maxWaitTime) {
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const isLoggedIn = await checkLoginStatus()
    if (isLoggedIn) {
      console.log('✅ 登录成功！')
      return true
    }
  }
  
  console.log('❌ 登录超时，请重试')
  return false
}

/**
 * 进入客服工作台
 */
async function enterChatWorkbench() {
  console.log('📬 正在进入客服工作台...')
  
  // 点击客服工作台入口
  await browser.act({
    kind: 'click',
    ref: '客服',
    timeoutMs: 10000
  })
  
  // 或者使用选择器
  await browser.act({
    kind: 'click',
    selector: '[data-type="chat"], .chat-entry',
    timeoutMs: 10000
  })
  
  console.log('✅ 已进入客服工作台')
}

/**
 * 获取未读消息列表
 */
async function getUnreadMessages() {
  try {
    const messages = await browser.evaluate(() => {
      const messageElements = document.querySelectorAll('.message-item.unread')
      return Array.from(messageElements).map(el => ({
        id: el.getAttribute('data-id'),
        buyerName: el.querySelector('.buyer-name')?.textContent,
        lastMessage: el.querySelector('.last-message')?.textContent,
        time: el.querySelector('.time')?.textContent
      }))
    })
    
    return messages
  } catch (e) {
    console.error('获取消息失败:', e)
    return []
  }
}

/**
 * 读取会话详情
 */
async function getConversationDetail(conversationId: string) {
  // 点击进入会话
  await browser.act({
    kind: 'click',
    ref: conversationId,
    timeoutMs: 5000
  })
  
  // 获取历史消息
  const history = await browser.evaluate(() => {
    const messages = document.querySelectorAll('.chat-message')
    return Array.from(messages).map(el => ({
      type: el.classList.contains('from-buyer') ? 'buyer' : 'seller',
      content: el.querySelector('.message-content')?.textContent,
      time: el.querySelector('.message-time')?.textContent
    }))
  })
  
  return history
}

/**
 * 智能匹配回复话术
 */
function matchTemplate(message: string): string {
  // 简单关键词匹配
  for (const category in TEMPLATES) {
    const templates = TEMPLATES[category as keyof typeof TEMPLATES]
    for (const template of templates) {
      for (const keyword of template.keywords) {
        if (message.includes(keyword)) {
          return template.response
        }
      }
    }
  }
  
  // 默认回复
  return '亲，您好，有什么可以帮您的吗？'
}

/**
 * 发送消息
 */
async function sendMessage(conversationId: string, message: string) {
  console.log(`📤 发送消息到会话 ${conversationId}`)
  
  // 聚焦输入框
  await browser.act({
    kind: 'click',
    selector: '.chat-input textarea',
    timeoutMs: 5000
  })
  
  // 输入消息
  await browser.act({
    kind: 'type',
    text: message,
    slowly: true
  })
  
  // 点击发送
  await browser.act({
    kind: 'click',
    selector: '.send-button',
    timeoutMs: 5000
  })
  
  console.log('✅ 消息发送成功')
}

/**
 * 智能回复（自动匹配 + 发送）
 */
async function smartReply(conversationId: string) {
  console.log(`🤖 处理智能回复：${conversationId}`)
  
  // 获取会话历史
  const history = await getConversationDetail(conversationId)
  
  // 获取买家最后一条消息
  const lastBuyerMessage = history
    .filter(msg => msg.type === 'buyer')
    .pop()
  
  if (!lastBuyerMessage) {
    console.log('⚠️ 未找到买家消息')
    return
  }
  
  // 匹配回复话术
  const reply = matchTemplate(lastBuyerMessage.content || '')
  
  console.log(`💬 买家：${lastBuyerMessage.content}`)
  console.log(`🤖 回复：${reply}`)
  
  // 发送回复（需确认）
  console.log('⏳ 准备发送回复...（3 秒后发送，按 Ctrl+C 取消）')
  await new Promise(resolve => setTimeout(resolve, 3000))
  
  await sendMessage(conversationId, reply)
}

/**
 * 监听消息（轮询）
 */
async function listenMessages(duration: number = 3600) {
  console.log(`👂 开始监听消息，持续时间：${duration}秒`)
  
  const endTime = Date.now() + (duration * 1000)
  let processedMessages = new Set<string>()
  
  while (Date.now() < endTime) {
    try {
      const unreadMessages = await getUnreadMessages()
      
      for (const msg of unreadMessages) {
        if (msg.id && !processedMessages.has(msg.id)) {
          console.log(`\n📩 新消息来自：${msg.buyerName}`)
          console.log(`   内容：${msg.lastMessage}`)
          console.log(`   时间：${msg.time}`)
          
          // 标记为已处理
          processedMessages.add(msg.id)
          
          // 可选：自动智能回复
          // await smartReply(msg.id)
        }
      }
    } catch (e) {
      console.error('监听消息出错:', e)
    }
    
    await new Promise(resolve => setTimeout(resolve, CONFIG.checkInterval))
  }
  
  console.log('\n✅ 监听结束')
}

/**
 * 查看话术库
 */
function listTemplates(category?: string) {
  console.log('📚 话术库\n')
  
  const categories = category ? [category] : Object.keys(TEMPLATES)
  
  for (const cat of categories) {
    console.log(`\n【${cat}】`)
    const templates = TEMPLATES[cat as keyof typeof TEMPLATES]
    templates.forEach((t, i) => {
      console.log(`  ${i + 1}. 关键词：${t.keywords.join(', ')}`)
      console.log(`     回复：${t.response}`)
    })
  }
}

/**
 * 添加话术
 */
function addTemplate(category: string, keywords: string[], response: string) {
  if (!TEMPLATES[category as keyof typeof TEMPLATES]) {
    TEMPLATES[category as keyof typeof TEMPLATES] = []
  }
  
  TEMPLATES[category as keyof typeof TEMPLATES].push({
    keywords,
    response
  })
  
  console.log(`✅ 话术已添加到【${category}】分类`)
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2)
  const command = args[0]
  
  console.log('🛒 拼多多客服助手 v1.0.0\n')
  
  switch (command) {
    case 'login':
      await login()
      break
      
    case 'listen':
      const duration = parseInt(args.find(a => a.includes('--duration'))?.split('=')[1] || '3600')
      await listenMessages(duration)
      break
      
    case 'messages':
      await login()
      const msgs = await getUnreadMessages()
      console.log(`📩 未读消息：${msgs.length}条`)
      msgs.forEach(m => console.log(`  - ${m.buyerName}: ${m.lastMessage}`))
      break
      
    case 'reply':
      await login()
      const convId = args.find(a => a.includes('--conversation'))?.split('=')[1] || ''
      await smartReply(convId)
      break
      
    case 'templates':
      if (args.includes('--list')) {
        listTemplates()
      } else if (args.includes('--add')) {
        // 添加话术逻辑
        console.log('请使用：--category "分类" --keywords "关键词" --response "回复内容"')
      }
      break
      
    default:
      console.log('用法:')
      console.log('  login              - 登录商家后台')
      console.log('  listen             - 监听消息')
      console.log('  messages           - 查看未读消息')
      console.log('  reply              - 智能回复')
      console.log('  templates --list   - 查看话术库')
      console.log('  templates --add    - 添加话术')
  }
}

// 运行
main().catch(console.error)
