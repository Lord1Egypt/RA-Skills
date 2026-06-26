#!/usr/bin/env node
/**
 * Podcast Pre-Production Pipeline
 * 用法: node podcast-pre-production.cjs <episode_number> <topic> [guest_name]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CONFIG_PATH = path.join(__dirname, '../config/podcast-pipeline.json');
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));

const episodeNumber = process.argv[2];
const topic = process.argv[3];
const guestName = process.argv[4] || '';

if (!episodeNumber || !topic) {
  console.error('用法: node podcast-pre-production.cjs <episode_number> <topic> [guest_name]');
  process.exit(1);
}

console.log(`🎙️ 开始 Podcast 前期制作 - Episode ${episodeNumber}`);
console.log(`📝 话题: ${topic}`);
if (guestName) console.log(`👤 嘉宾: ${guestName}`);

const episodePath = path.join(config.storage_path, 'episodes', `ep${episodeNumber}`);
const prepPath = path.join(episodePath, 'prep');

// 创建目录
fs.mkdirSync(prepPath, { recursive: true });

// 使用 Tavily API 进行研究
async function research(query) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      api_key: config.apis.tavily,
      query: query,
      search_depth: 'advanced',
      max_results: 5,
      include_answer: true
    });

    const options = {
      hostname: 'api.tavily.com',
      port: 443,
      path: '/search',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// 生成节目大纲
async function generateOutline() {
  console.log('\n📊 正在研究话题...');
  const topicResearch = await research(`${topic} trends news insights 2026`);
  
  let guestResearch = null;
  if (guestName) {
    console.log('👤 正在研究嘉宾...');
    guestResearch = await research(`${guestName} background career achievements`);
  }

  // 生成大纲
  const outline = `# Episode ${episodeNumber}: ${topic}

${guestName ? `**嘉宾**: ${guestName}` : ''}

---

## 🎯 节目概述

**主题**: ${topic}

${topicResearch.answer ? `**研究摘要**: ${topicResearch.answer}` : ''}

---

## 📝 开场白 (30秒)

大家好，欢迎来到 ${config.podcast_name}！我是 ${config.host_name}。

今天我们要聊聊 ${topic}。

${guestName ? `我特别高兴邀请到 ${guestName} 来和我们一起探讨这个话题。` : ''}

---

## 🎙️ 采访问题 (5-7个)

### 开场问题 (建立融洽感)

1. **介绍自己**
   ${guestName ? `- 能不能先介绍一下你自己，你是怎么进入这个领域的？` : `- 让我们从基础开始，你是怎么对这个话题产生兴趣的？`}

### 核心问题 (深入探讨)

2. **核心观点**
   - 关于 ${topic}，你觉得目前最大的误解是什么？

3. **个人经验**
   ${guestName ? `- 在你的职业生涯中，有没有遇到特别相关的经历？` : `- 能不能分享一个特别有意思的案例或故事？`}

4. **趋势分析**
   - 你认为未来 12-18 个月，${topic} 会有什么变化？

5. **实用建议**
   - 对于我们的听众，你有什么实用的建议？

### 深度问题 (挑战观点)

6. **争议话题**
   - 有没有哪个观点是你觉得被过度吹捧或低估的？

7. **未来展望**
   - 如果你要预测 3 年后的情况，会是什么样？

### 备用问题 (防止冷场)

- 最近有没有什么让你觉得特别兴奋的新发展？
- 你觉得听众应该关注哪些信号或指标？
- 有没有推荐的资源或工具？

---

## 🔚 结束语 (30秒)

${guestName ? `非常感谢 ${guestName} 的精彩分享！` : `感谢大家的收听！`}

如果你觉得这期节目有价值，请记得订阅和分享！

我们下期再见！

---

## 📚 研究资料

### 话题研究

${topicResearch.results ? topicResearch.results.map((r, i) => 
  `${i + 1}. [${r.title}](${r.url})\n   ${r.content ? r.content.substring(0, 150) + '...' : ''}`
).join('\n\n') : '无结果'}

${guestResearch ? `
### 嘉宾研究

${guestResearch.results ? guestResearch.results.map((r, i) => 
  `${i + 1}. [${r.title}](${r.url})\n   ${r.content ? r.content.substring(0, 150) + '...' : ''}`
).join('\n\n') : '无结果'}
` : ''}

---

**生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;

  // 保存大纲
  const outlinePath = path.join(prepPath, 'outline.md');
  fs.writeFileSync(outlinePath, outline, 'utf-8');
  console.log(`\n✅ 节目大纲已保存: ${outlinePath}`);

  return outline;
}

// 发送消息到 Discord 线程
async function sendToDiscord(message) {
  return new Promise((resolve, reject) => {
    const token = process.env.OPENCLAW_GATEWAY_TOKEN || 'b8cb95b2fb220c2896a44dc6514f47ef4efed792bcd07c3f';
    
    const postData = JSON.stringify({
      channel: 'discord',
      action: 'send',
      channelId: config.discord_channel,
      message: message,
      silent: true
    });

    const options = {
      hostname: '127.0.0.1',
      port: 18789,
      path: '/api/v1/tools/message',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.ok || result.status === 'ok') {
            console.log('✅ 已发送到 Discord 线程');
            resolve(result);
          } else {
            console.log('⚠️ Discord 发送:', result.error || result.status || '未知');
            resolve(null);
          }
        } catch (error) {
          console.log('⚠️ Discord 响应:', data.substring(0, 100));
          resolve(null);
        }
      });
    });

    req.on('error', (error) => {
      console.log('⚠️ Discord 发送:', error.message);
      resolve(null);
    });
    req.write(postData);
    req.end();
  });
}

// 主函数
async function main() {
  try {
    await generateOutline();
    const outlinePath = path.join(prepPath, 'outline.md');
    
    // 构建 Discord 消息
    const discordMessage = `🎙️ **Episode ${episodeNumber} 前期制作完成！**

📝 **话题**: ${topic}
${guestName ? `👤 **嘉宾**: ${guestName}` : ''}

✅ 已生成节目大纲和采访问题
📁 **文件**: \`${path.basename(outlinePath)}\``;

    // 发送到 Discord 线程
    await sendToDiscord(discordMessage);
    
    console.log(`\n✅ 完成！文件保存在: ${outlinePath}`);

  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
