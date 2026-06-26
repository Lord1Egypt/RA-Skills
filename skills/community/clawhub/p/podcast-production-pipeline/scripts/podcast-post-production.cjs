#!/usr/bin/env node
/**
 * Podcast Post-Production Pipeline
 * 用法: node podcast-post-production.cjs <episode_number> <transcript_file>
 */

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, '../config/podcast-pipeline.json');
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));

const episodeNumber = process.argv[2];
const transcriptFile = process.argv[3];

if (!episodeNumber) {
  console.error('用法: node podcast-post-production.cjs <episode_number> [transcript_file]');
  process.exit(1);
}

console.log(`🎬 开始 Podcast 后期制作 - Episode ${episodeNumber}`);

const episodePath = path.join(config.storage_path, 'episodes', `ep${episodeNumber}`);
const publishPath = path.join(episodePath, 'publish');

fs.mkdirSync(publishPath, { recursive: true });

// 读取转录文本
let transcript = '';
if (transcriptFile && fs.existsSync(transcriptFile)) {
  transcript = fs.readFileSync(transcriptFile, 'utf-8');
} else {
  console.log('⚠️  未提供转录文件，将生成模板');
  transcript = '[请在此处粘贴转录文本]';
}

// 生成节目笔记
function generateShowNotes() {
  return `# Episode ${episodeNumber} - Show Notes

**发布日期**: ${new Date().toLocaleDateString('zh-CN')}
**时长**: [待填写]

---

## 📌 关键要点

1. **[00:00]** 开场介绍
2. **[XX:XX]** [第一个主要话题]
3. **[XX:XX]** [第二个主要话题]
4. **[XX:XX]** [第三个主要话题]
5. **[XX:XX]** 结束语

---

## 🔗 提到的资源

- [ ] [资源名称](URL) - 描述
- [ ] [工具名称](URL) - 描述
- [ ] [书籍/文章](URL) - 描述

---

## 💡 金句摘录

> "这里放嘉宾的金句或核心观点" - [嘉宾名字]

> "第二个重要观点" - [嘉宾名字]

---

## 🎯 听众收获

听完这期节目，你将了解到：
- ✅ 要点 1
- ✅ 要点 2
- ✅ 要点 3

---

## 📚 延伸阅读

1. [相关文章标题](URL)
2. [相关书籍](URL)

---

**生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;
}

// 生成节目描述（SEO 优化）
function generateDescription() {
  return `# Episode ${episodeNumber} - SEO 描述

## Spotify / Apple Podcasts 描述 (200 字以内)

在本期节目中，我们深入探讨了 [主要话题]。${config.host_name} ${guestName ? `与 ${guestName} 一起` : ''}分享了关于 [核心观点] 的独到见解。

**主要内容包括**:
• [要点 1]
• [要点 2]
• [要点 3]

无论你是 [目标听众 1] 还是 [目标听众 2]，这期节目都能给你带来实用的启发。

**关键词**: ${topic}, [关键词2], [关键词3], [关键词4], [关键词5]

---

## YouTube 描述 (更长版本)

**标题**: [Episode ${episodeNumber}] ${topic} | ${config.podcast_name}

**描述**:

欢迎回到 ${config.podcast_name}！在本期节目中，我们深入探讨了 ${topic}。

${guestName ? `我的嘉宾是 ${guestName}，他/她分享了...` : `我分享了关于...`}

**时间戳**:
0:00 - 开场
XX:XX - [第一个话题]
XX:XX - [第二个话题]
XX:XX - [第三个话题]
XX:XX - 结束语

**提到的资源**:
• [资源 1](URL)
• [资源 2](URL)

**订阅频道**: [订阅链接]
**关注我**: [社交媒体链接]

#${topic.replace(/\s+/g, '')} #Podcast #${config.podcast_name.replace(/\s+/g, '')}

---

**生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;
}

// 生成社交媒体帖子
function generateSocialMedia() {
  return `# Episode ${episodeNumber} - 社交媒体发布包

---

## 🐦 Twitter/X (3 条推文)

### 推文 1: 金句 (280 字符以内)

💡 "${guestName || config.host_name} 的新观点"

[金句内容]

听完整期节目: [链接]

#${topic.replace(/\s+/g, '')} #Podcast

---

### 推文 2: 核心洞察 (280 字符以内)

🔥 关于 ${topic} 的关键洞察:

• [洞察 1]
• [洞察 2] 
• [洞察 3]

Episode ${episodeNumber} 现已上线: [链接]

---

### 推文 3: 互动问题 (280 字符以内)

❓ 你对 ${topic} 有什么看法?

A) 观点 1
B) 观点 2  
C) 其他（评论告诉我）

听听我们的讨论: [链接]

---

## 💼 LinkedIn (1 条帖子)

**标题**: ${topic} - 我在最新一期播客中讨论的关键见解

刚刚发布了 ${config.podcast_name} 的第 ${episodeNumber} 期！

${guestName ? `与 ${guestName} 的对话中，` : `在这期节目中，`}我们深入探讨了 ${topic}。

**3 个关键收获**:

1️⃣ [收获 1]

2️⃣ [收获 2]

3️⃣ [收获 3]

这期节目适合:
• [目标听众 1]
• [目标听众 2]
• [目标听众 3]

收听链接: [URL]

#${topic.replace(/\s+/g, '')} #Podcast #ProfessionalDevelopment

---

## 📸 Instagram (1 条帖子)

**图片建议**: [嘉宾照片/节目标题图/金句卡片]

**Caption**:

🎙️ 新一期播客上线！

Episode ${episodeNumber}: ${topic}

${guestName ? `与 ${guestName} 的精彩对话` : `我的深度分享`}

💡 本期金句:
"[金句内容]"

🎧 收听方式:
• Spotify: [链接]
• Apple Podcasts: [链接]
• YouTube: [链接]

👇 你对 ${topic} 有什么看法？评论区告诉我！

.
.
.
#${topic.replace(/\s+/g, '')} #播客 #学习成长 #自我提升

---

**生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;
}

// 生成精华片段
function generateHighlights() {
  return `# Episode ${episodeNumber} - 精华片段

**适合做成短视频/转发的 3 个片段**:

---

## 🎬 片段 1: [标题]

**时间戳**: [XX:XX - XX:XX]
**时长**: [XX 秒]

**内容**: 
[片段描述]

**为什么重要**: 
[解释为什么这个片段值得单独分享]

**适合平台**: 
- ✅ TikTok
- ✅ Instagram Reels
- ✅ YouTube Shorts

---

## 🎬 片段 2: [标题]

**时间戳**: [XX:XX - XX:XX]
**时长**: [XX 秒]

**内容**: 
[片段描述]

**为什么重要**: 
[解释]

**适合平台**: 
- ✅ Twitter/X
- ✅ LinkedIn

---

## 🎬 片段 3: [标题]

**时间戳**: [XX:XX - XX:XX]
**时长**: [XX 秒]

**内容**: 
[片段描述]

**为什么重要**: 
[解释]

**适合平台**: 
- ✅ Instagram Stories
- ✅ Facebook

---

**生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;
}

// 主函数
async function main() {
  try {
    // 生成所有文件
    const showNotes = generateShowNotes();
    const description = generateDescription();
    const socialMedia = generateSocialMedia();
    const highlights = generateHighlights();

    // 保存文件
    fs.writeFileSync(path.join(publishPath, 'show-notes.md'), showNotes, 'utf-8');
    fs.writeFileSync(path.join(publishPath, 'description.md'), description, 'utf-8');
    fs.writeFileSync(path.join(publishPath, 'social-media.md'), socialMedia, 'utf-8');
    fs.writeFileSync(path.join(publishPath, 'highlights.md'), highlights, 'utf-8');

    console.log('\n✅ 后期制作文件已生成:');
    console.log(`   📄 show-notes.md`);
    console.log(`   📄 description.md`);
    console.log(`   📄 social-media.md`);
    console.log(`   📄 highlights.md`);

    console.log('\n---DISCORD_MESSAGE_START---');
    console.log(`🎬 **Episode ${episodeNumber} 后期制作完成！**`);
    console.log(`\n✅ 已生成以下文件:`);
    console.log(`• 📝 节目笔记`);
    console.log(`• 📄 SEO 描述`);
    console.log(`• 📱 社交媒体帖子`);
    console.log(`• 🎬 精华片段`);
    console.log(`\n📁 **路径**: \`${publishPath}\``);
    console.log('\n---DISCORD_MESSAGE_END---');

  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
