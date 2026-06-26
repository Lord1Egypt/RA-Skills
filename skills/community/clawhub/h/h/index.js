
class HSkill {
  constructor() {
    this.name = 'h';
    this.version = '1.0.0';
    this.favorites = [];
    this.history = [];
    
    this.skillsDB = [
      { name: 'q', description: '智能多面手工具箱', tags: ['productivity', 'query', 'toolkit'], downloads: 12500, rating: 4.8 },
      { name: 'git-helper', description: 'Git 命令助手', tags: ['git', 'version-control', 'devops'], downloads: 8900, rating: 4.6 },
      { name: 'data-viz', description: '数据可视化工具', tags: ['visualization', 'charts', 'data'], downloads: 7200, rating: 4.7 },
      { name: 'code-review', description: '代码审查助手', tags: ['code-review', 'quality', 'dev'], downloads: 6500, rating: 4.5 },
      { name: 'doc-gen', description: '文档生成器', tags: ['documentation', 'markdown', 'automation'], downloads: 5800, rating: 4.4 },
      { name: 'test-buddy', description: '测试助手', tags: ['testing', 'qa', 'automation'], downloads: 5200, rating: 4.6 },
      { name: 'api-maker', description: 'API 设计工具', tags: ['api', 'rest', 'backend'], downloads: 4800, rating: 4.5 },
      { name: 'style-guide', description: '代码风格指南', tags: ['style', 'lint', 'format'], downloads: 4500, rating: 4.3 }
    ];
  }

  search(keywords) {
    const keywordList = keywords.toLowerCase().split(' ');
    const results = this.skillsDB.filter(skill =&gt; {
      const text = `${skill.name} ${skill.description} ${skill.tags.join(' ')}`.toLowerCase();
      return keywordList.some(kw =&gt; text.includes(kw));
    });
    
    this.addToHistory(`search:${keywords}`);
    
    if (results.length === 0) {
      return `🔍 搜索 "${keywords}" 未找到相关技能\n尝试使用更广泛的关键词或 /h hot 查看热门技能`;
    }
    
    return `🔍 搜索 "${keywords}" 找到 ${results.length} 个技能：\n${results.map((s, i) =&gt; 
      `${i + 1}. ${s.name} - ${s.description} (⭐${s.rating}, ⬇️${s.downloads})`
    ).join('\n')}`;
  }

  hot() {
    const hotSkills = [...this.skillsDB].sort((a, b) =&gt; b.downloads - a.downloads).slice(0, 5);
    this.addToHistory('hot');
    return `🔥 今日热门技能榜：\n${hotSkills.map((s, i) =&gt; 
      `${i + 1}. ${s.name} - ${s.description}\n   ⬇️ ${s.downloads} 下载 | ⭐ ${s.rating}`
    ).join('\n')}`;
  }

  new() {
    const newSkills = this.skillsDB.slice(-4).reverse();
    this.addToHistory('new');
    return `🆕 最新上线技能：\n${newSkills.map((s, i) =&gt; 
      `${i + 1}. ${s.name} - ${s.description}\n   标签: ${s.tags.join(', ')}`
    ).join('\n')}`;
  }

  trending() {
    const trendingSkills = [...this.skillsDB].sort((a, b) =&gt; b.rating - a.rating).slice(0, 5);
    this.addToHistory('trending');
    return `📈 上升最快技能：\n${trendingSkills.map((s, i) =&gt; 
      `${i + 1}. ${s.name} - ⭐ ${s.rating} 评分`
    ).join('\n')}`;
  }

  recommend() {
    this.addToHistory('recommend');
    return `🎯 为你推荐：\n1. q - 智能多面手工具箱（必备神器）\n2. git-helper - Git 命令助手（开发者首选）\n3. data-viz - 数据可视化工具（数据党最爱）\n\n根据你的使用习惯，还可以试试：\n- /h search 你的需求关键词\n- /h hot 查看大家都在用什么`;
  }

  similar(skillName) {
    const skill = this.skillsDB.find(s =&gt; s.name === skillName);
    if (!skill) {
      return `❌ 未找到技能 "${skillName}"`;
    }
    
    const similar = this.skillsDB.filter(s =&gt; 
      s.name !== skillName &amp;&amp; 
      s.tags.some(t =&gt; skill.tags.includes(t))
    );
    
    this.addToHistory(`similar:${skillName}`);
    
    if (similar.length === 0) {
      return `🔗 与 "${skillName}" 相似的技能暂未找到\n试试 /h hot 发现更多技能`;
    }
    
    return `🔗 与 "${skillName}" 相似的技能：\n${similar.map((s, i) =&gt; 
      `${i + 1}. ${s.name} - ${s.description}`
    ).join('\n')}`;
  }

  info(skillName) {
    const skill = this.skillsDB.find(s =&gt; s.name === skillName);
    if (!skill) {
      return `❌ 未找到技能 "${skillName}"`;
    }
    this.addToHistory(`info:${skillName}`);
    return `📋 ${skill.name} 详情：\n━━━━━━━━━━━━━━━━━━━━\n📝 描述：${skill.description}\n🏷️  标签：${skill.tags.join(', ')}\n⬇️  下载：${skill.downloads}\n⭐  评分：${skill.rating}\n━━━━━━━━━━━━━━━━━━━━\n使用 /h install ${skill.name} 快速安装`;
  }

  install(skillName) {
    const skill = this.skillsDB.find(s =&gt; s.name === skillName);
    if (!skill) {
      return `❌ 未找到技能 "${skillName}"`;
    }
    this.addToHistory(`install:${skillName}`);
    return `✅ 正在安装 ${skill.name}...\n安装成功！现在可以使用 ${skill.name} 了`;
  }

  favorites() {
    this.addToHistory('favorites');
    if (this.favorites.length === 0) {
      return `⭐ 我的收藏（空）\n使用 /h info [skill-name] 查看技能详情后可以收藏`;
    }
    return `⭐ 我的收藏：\n${this.favorites.map((s, i) =&gt; `${i + 1}. ${s}`).join('\n')}`;
  }

  history() {
    if (this.history.length === 0) {
      return `📜 使用历史（空）\n开始使用 h 搜索技能吧！`;
    }
    return `📜 最近使用：\n${this.history.slice(-10).reverse().map((h, i) =&gt; `${i + 1}. ${h}`).join('\n')}`;
  }

  tags(filter = '') {
    const allTags = [...new Set(this.skillsDB.flatMap(s =&gt; s.tags))];
    this.addToHistory('tags');
    
    if (filter) {
      const filteredSkills = this.skillsDB.filter(s =&gt; s.tags.includes(filter));
      if (filteredSkills.length === 0) {
        return `🏷️  未找到标签 "${filter}" 相关技能`;
      }
      return `🏷️  标签 "${filter}" 下的技能：\n${filteredSkills.map((s, i) =&gt; 
        `${i + 1}. ${s.name} - ${s.description}`
      ).join('\n')}`;
    }
    
    return `🏷️  所有可用标签：\n${allTags.join(', ')}\n\n使用 /h tags [标签名] 查看该标签下的技能`;
  }

  help() {
    return `👋 欢迎使用 h - Skill 发现中心！\n━━━━━━━━━━━━━━━━━━━━\n🔍 搜索：/h search [关键词]\n🔥 热门：/h hot\n🆕 最新：/h new\n📈 趋势：/h trending\n🎯 推荐：/h recommend\n🔗 相似：/h similar [skill]\n📋 详情：/h info [skill]\n✅ 安装：/h install [skill]\n⭐ 收藏：/h favorites\n📜 历史：/h history\n🏷️  标签：/h tags [标签]\n━━━━━━━━━━━━━━━━━━━━\n输入 /h [命令] 开始使用！`;
  }

  addToHistory(action) {
    const timestamp = new Date().toLocaleTimeString();
    this.history.push(`${timestamp} - ${action}`);
  }

  execute(command, args) {
    switch (command) {
      case 'search':
        return this.search(args.join(' '));
      case 'hot':
        return this.hot();
      case 'new':
        return this.new();
      case 'trending':
        return this.trending();
      case 'recommend':
        return this.recommend();
      case 'similar':
        return this.similar(args[0]);
      case 'info':
        return this.info(args[0]);
      case 'install':
        return this.install(args[0]);
      case 'favorites':
        return this.favorites();
      case 'history':
        return this.history();
      case 'tags':
        return this.tags(args[0]);
      case 'help':
      default:
        return this.help();
    }
  }
}

module.exports = HSkill;
