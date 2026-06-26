// link-saver 链接收藏夹
const fs = require('fs');
const path = require('path');

const SKILL_DIR = __dirname;
const DATA_FILE = path.join(SKILL_DIR, 'links.json');

// 初始化数据文件
function initFile() {
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify([], null, 2));
  }
}

// 读取数据
function loadData() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  } catch {
    return [];
  }
}

// 保存数据
function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// 提取URL
function extractUrl(text) {
  const urlRegex = /https?:\/\/[^\s]+/g;
  const match = text.match(urlRegex);
  return match ? match[0] : null;
}

// 提取描述
function extractDescription(text, url) {
  return text.replace(url, '').replace(/保存|收藏|添加|书签/g, '').trim() || '无描述';
}

module.exports = {
  name: 'link-saver',
  description: '链接收藏夹，保存和整理有用的网页链接',
  version: '1.0.0',
  author: '黄豆豆',
  
  // 激活条件
  activate(message) {
    const keywords = ['链接', '收藏', '书签', '保存', '网站'];
    return keywords.some(k => message.includes(k));
  },
  
  async handle(context) {
    const message = context.message || '';
    const lowerMessage = message.toLowerCase();
    
    initFile();
    
    // 保存链接
    if (lowerMessage.includes('保存') || lowerMessage.includes('收藏') || lowerMessage.includes('添加')) {
      return this.saveLink(message);
    }
    
    // 查看链接
    if (lowerMessage.includes('查看') || lowerMessage.includes('列表') || lowerMessage.includes('所有')) {
      return this.listLinks();
    }
    
    // 搜索链接
    if (lowerMessage.includes('搜索') || lowerMessage.includes('找')) {
      return this.searchLinks(message);
    }
    
    // 删除链接
    if (lowerMessage.includes('删除') || lowerMessage.includes('移除')) {
      return this.deleteLink(message);
    }
    
    // 默认显示帮助
    return this.showHelp();
  },
  
  saveLink(message) {
    const url = extractUrl(message);
    
    if (!url) {
      return { message: '❌ 请提供有效的URL链接\n\n例如：保存 https://example.com 我的收藏' };
    }
    
    const links = loadData();
    const description = extractDescription(message, url);
    
    const link = {
      id: Date.now(),
      url: url,
      description: description,
      created: new Date().toISOString()
    };
    
    links.push(link);
    saveData(links);
    
    return {
      success: true,
      message: `✅ 链接已保存！\n\n🔗 ${url}\n📝 ${description}\n\n输入"查看链接"可查看所有收藏`
    };
  },
  
  listLinks() {
    const links = loadData();
    
    if (links.length === 0) {
      return {
        message: `📂 暂无收藏的链接\n\n输入"保存 https://xxx.com 描述"添加链接`
      };
    }
    
    let msg = `📂 链接收藏夹 (${links.length}个)\n\n`;
    
    links.forEach((link, i) => {
      msg += `${i + 1}. ${link.description}\n`;
      msg += `   🔗 ${link.url}\n\n`;
    });
    
    msg += `\n💡 输入"搜索 xxx"查找链接\n输入"删除 1"删除链接`;
    
    return { message: msg };
  },
  
  searchLinks(message) {
    const query = message.replace(/搜索|找/g, '').trim();
    const links = loadData();
    
    if (!query) {
      return { message: '请输入搜索关键词\n例如：搜索 Python' };
    }
    
    const results = links.filter(link => 
      link.url.includes(query) || 
      link.description.includes(query)
    );
    
    if (results.length === 0) {
      return { message: `未找到包含"${query}"的链接` };
    }
    
    let msg = `🔍 搜索结果：${results.length}个\n\n`;
    
    results.forEach((link, i) => {
      msg += `${i + 1}. ${link.description}\n`;
      msg += `   🔗 ${link.url}\n\n`;
    });
    
    return { message: msg };
  },
  
  deleteLink(message) {
    const idMatch = message.match(/\d+/);
    
    if (!idMatch) {
      return { message: '请指定要删除的链接编号\n例如：删除 1' };
    }
    
    const links = loadData();
    const index = parseInt(idMatch[0]) - 1;
    
    if (index < 0 || index >= links.length) {
      return { message: '链接编号不存在' };
    }
    
    const deleted = links.splice(index, 1)[0];
    saveData(links);
    
    return {
      success: true,
      message: `✅ 已删除：${deleted.description}\n🔗 ${deleted.url}`
    };
  },
  
  showHelp() {
    return {
      message: `📂 链接收藏夹使用方法：

1. 保存链接：保存 https://xxx.com 描述
2. 查看列表：查看链接 / 查看所有
3. 搜索：搜索 关键词
4. 删除：删除 编号

示例：
- 保存 https://github.com GitHub
- 查看链接
- 搜索 Python
- 删除 1`
    };
  }
};
