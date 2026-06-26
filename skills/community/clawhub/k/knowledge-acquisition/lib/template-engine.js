// 快乐小狗专用模板引擎
class HappyDogTemplateEngine {
  constructor() {
    this.templates = {
      // 标准知识模板（原有功能）
      knowledge: {
        standard: (data) => this.generateKnowledgeNote(data, 'standard'),
        detailed: (data) => this.generateKnowledgeNote(data, 'detailed'),
        minimal: (data) => this.generateKnowledgeNote(data, 'minimal')
      },

      // 视频内容模板（新增）
      video: {
        standard: (data) => this.generateVideoNote(data, 'standard'),
        detailed: (data) => this.generateVideoNote(data, 'detailed'),
        minimal: (data) => this.generateVideoNote(data, 'minimal')
      },

      // GitHub仓库模板（新增）
      repository: {
        standard: (data) => this.generateRepositoryNote(data, 'standard'),
        detailed: (data) => this.generateRepositoryNote(data, 'detailed'),
        minimal: (data) => this.generateRepositoryNote(data, 'minimal')
      },

      // 社交内容模板（新增）
      social: {
        standard: (data) => this.generateSocialNote(data, 'standard'),
        detailed: (data) => this.generateSocialNote(data, 'detailed'),
        minimal: (data) => this.generateSocialNote(data, 'minimal')
      }
    };
  }

  /**
   * 生成知识笔记（原有功能优化）
   */
  generateKnowledgeNote(data, format = 'standard') {
    const { title, content, category, sourceUrl, author, publishTime, media, summary, classification, traceId } = data;
    const dateStr = this.getDateStr();

    const baseTemplate = {
      title: `${title}+${dateStr}`,
      metadata: {
        category: category || '未分类',
        confidence: classification?.confidence || 0,
        platform: data.platform || '未知',
        traceId: traceId || this.makeTraceId()
      },
      source: {
        url: sourceUrl || '',
        author: author || '未知',
        publishTime: publishTime || new Date().toISOString()
      }
    };

    switch (format) {
      case 'detailed':
        return this.generateDetailedKnowledge(baseTemplate, content, media, summary, classification);
      case 'minimal':
        return this.generateMinimalKnowledge(baseTemplate, content);
      default:
        return this.generateStandardKnowledge(baseTemplate, content, media, summary, classification);
    }
  }

  /**
   * 生成视频笔记
   */
  generateVideoNote(data, format = 'standard') {
    const { title, description, author, duration, subtitles, url, platform } = data;
    const dateStr = this.getDateStr();

    switch (format) {
      case 'detailed':
        return `# 🎬 ${title}+${dateStr}

## 视频信息
- **平台:** ${platform.toUpperCase()}
- **作者:** ${author}
- **时长:** ${this.formatDuration(duration)}
- **链接:** [观看视频](${url})

## 视频描述
${description || '暂无描述'}

## 字幕内容
${subtitles?.map(s => `- [${s.timestamp}] ${s.text}`).join('\n') || '暂无字幕'}

## 核心要点
${this.extractKeyPoints(subtitles || []).map(p => `- ${p}`).join('\n')}

## 思考与行动
- [ ] 总结视频核心观点
- [ ] 提炼可实践的内容
- [ ] 制定后续行动计划

---
*生成时间: ${new Date().toLocaleString()}*`;

      case 'minimal':
        return `# ${title}
平台: ${platform} | 时长: ${this.formatDuration(duration)}
${subtitles?.slice(0, 5).map(s => s.text).join(' ') || ''}...`;

      default:
        return `# ${title}+${dateStr}

## 📹 视频摘要
${description || '暂无描述'}

**作者:** ${author} | **时长:** ${this.formatDuration(duration)}
**字幕精华:** ${subtitles?.slice(0, 3).map(s => s.text).join(' ') || ''}

---
[观看原视频](${url})`;
    }
  }

  /**
   * 生成GitHub仓库笔记
   */
  generateRepositoryNote(data, format = 'standard') {
    const { name, fullName, description, language, stars, forks, readme, topics, url, cloneUrl } = data;
    const dateStr = this.getDateStr();

    switch (format) {
      case 'detailed':
        return `# 📦 ${fullName}+${dateStr}

## 仓库信息
- **名称:** ${name}
- **描述:** ${description || '暂无描述'}
- **语言:** ${language || '未知'}
- **Stars:** ${stars}
- **Forks:** ${forks}
- **主题标签:** ${topics?.join(', ') || '无'}

## 快速开始
\`\`\`bash
git clone ${cloneUrl}
\`\`\`

## README 预览
${readme || '暂无README'}

## 相关链接
- [GitHub仓库](${url})
- [Issues](${url}/issues)
- [Pull Requests](${url}/pulls)

## 学习要点
- [ ] 理解项目架构
- [ ] 阅读核心代码
- [ ] 运行示例项目
- [ ] 贡献代码

---
*生成时间: ${new Date().toLocaleString()}*`;

      case 'minimal':
        return `# ${name}
${language} ⭐ ${stars} - ${description || '暂无描述'}
${cloneUrl}`;

      default:
        return `# ${fullName}+${dateStr}

**${language}**⭐ ${stars} 🍴 ${forks}

${description || '暂无描述'}

**主题:** ${topics?.map(t => `\`${t}\``).join(' ') || '无'}
👉 [访问仓库](${url})`;
    }
  }

  /**
   * 生成社交媒体笔记
   */
  generateSocialNote(data, format = 'standard') {
    const { title, author, platform, content, likes, tags, url } = data;
    const dateStr = this.getDateStr();

    switch (format) {
      case 'detailed':
        return `# 🔥 ${title}+${dateStr}

## 内容详情
**平台:** ${platform}
**作者:** ${author}
**互动:** ${likes || 0} 个赞

## 正文内容
${content}

## 标签
${tags?.map(t => `#${t}`).join(' ') || '无标签'}

## 深度思考
- [ ] 提取核心观点
- [ ] 关联已有知识
- [ ] 思考应用场景

## 行动清单
- [ ] 实践其中的建议
- [ ] 分享给相关的人
- [ ] 持续关注作者

---
*来源: ${url}*`;

      case 'minimal':
        return `# ${title}
${platform} - ${author}
${content.substring(0, 100)}...`;

      default:
        return `# ${title}+${dateStr}

**@${author}** 在 **${platform}** 发布

${content}

${likes ? `💕 ${likes} 个赞` : ''} ${tags?.map(t => `#${t}`).join(' ') || ''}

👉 [查看原文](${url})`;
    }
  }

  /**
   * 标准知识模板（优化版）
   */
  generateStandardKnowledge(template, content, media, summary, classification) {
    const { title, metadata, source } = template;

    const mediaLines = [
      ...(media.images || []).map(img => `- 图片: ${img.url}`),
      ...(media.videos || []).map(video => `- 视频: ${video.url}`)
    ];

    const subtitleBlock = (media.subtitles || []).length
      ? media.subtitles.map(item => `- [${item.timestamp}] ${item.text}`).join('\n')
      : '- 无';

    return `# ${title}

## 📋 分类标签
- ${metadata.category}
- 置信度: ${metadata.confidence}%
- 平台: ${metadata.platform}

## 🎯 关键摘要
${(summary || ['待补充摘要']).map(item => `- ${item}`).join('\n')}

## 📍 原文出处
- 链接: [查看原文](${source.url})
- 作者: ${source.author}
- 发布时间: ${source.publishTime}

## 📎 媒体资源
${mediaLines.length ? mediaLines.join('\n') : '- 无'}

## 🎬 视频字幕
${subtitleBlock}

## 💭 思考与行动
- 提炼 1 个可执行实验并在 24 小时内验证
- 将结论同步到周复盘并补充下一步指标

## 📊 分类依据
- trace_id: ${metadata.traceId}
- 关键词: ${(classification?.evidence || []).join('、') || '无'}

---
*生成时间: ${new Date().toLocaleString()}*`;
  }

  /**
   * 详细知识模板
   */
  generateDetailedKnowledge(template, content, media, summary, classification) {
    const { title, metadata, source } = template;

    return `# 📚 ${title}

## 📋 属性信息
- **分类:** ${metadata.category}
- **置信度:** ${metadata.confidence}%
- **平台:** ${metadata.platform}
- **作者:** ${source.author}
- **发布时间:** ${source.publishTime}
- **原文链接:** [点击查看](${source.url})

## 📖 内容全文
${content}

## 🎯 核心摘要
${(summary || ['待补充摘要']).map((item, i) => `${i + 1}. ${item}`).join('\n')}

## 🎬 视频转录
${this.renderSubtitles(media.subtitles || [])}

## 🖼️ 媒体资源
${this.renderMedia(media)}

## 🔍 深度分析
### 关键洞察
- 待补充关键洞察

### 知识关联
- 待补充相关知识

### 实践计划
1. [ ]
2. [ ]
3. [ ]

## 📊 元数据
- **trace_id:** ${metadata.traceId}
- **提取时间:** ${new Date().toISOString()}
- **分类关键词:** ${(classification?.evidence || []).join('、')}

---

*此文档由快乐小狗信息整理器自动生成`;
  }

  /**
   * 简洁知识模板
   */
  generateMinimalKnowledge(template, content) {
    const { title, metadata, source } = template;

    return `## ${title}
**${metadata.category}** | ${metadata.confidence}%

${content.substring(0, 100)}...

📎 ${source.url}`;
  }

  /**
   * 渲染字幕
   */
  renderSubtitles(subtitles) {
    if (!subtitles.length) return '无字幕';
    return subtitles.slice(0, 20).map(s => `- **${s.timestamp}** ${s.text}`).join('\n');
  }

  /**
   * 渲染媒体资源
   */
  renderMedia(media) {
    const sections = [];

    if (media.images?.length) {
      sections.push('### 图片资源\n' + media.images.map(img => `- [${img.alt || '图片'}](${img.url})`).join('\n'));
    }

    if (media.videos?.length) {
      sections.push('### 视频资源\n' + media.videos.map(video => `- [视频](${video.url})`).join('\n'));
    }

    return sections.length ? sections.join('\n\n') : '无媒体资源';
  }

  /**
   * 提取视频核心要点
   */
  extractKeyPoints(subtitles) {
    // 简单的要点提取逻辑
    const importantText = subtitles.filter(s =>
      s.text.includes('要点') ||
      s.text.includes('总结') ||
      s.text.length > 20
    ).slice(0, 3);

    if (importantText.length) {
      return importantText.map(s => s.text);
    }

    // 如果没有明显的要点，返回前几句作为参考
    return subtitles.slice(0, 3).map(s => s.text);
  }

  /**
   * 格式化时长
   */
  formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  }

  /**
   * 获取日期字符串
   */
  getDateStr() {
    const now = new Date();
    return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`;
  }

  /**
   * 生成trace_id
   */
  makeTraceId() {
    return `dog-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`;
  }

  /**
   * 渲染内容（主入口）
   */
  render(content, options = {}) {
    const { type = 'knowledge', format = 'standard' } = options;

    if (!this.templates[type] || !this.templates[type][format]) {
      throw new Error(`无效的模板类型或格式: ${type}.${format}`);
    }

    return this.templates[type][format](content);
  }

  /**
   * 获取可用模板列表
   */
  getAvailableTemplates() {
    return {
      types: Object.keys(this.templates),
      formats: ['standard', 'detailed', 'minimal']
    };
  }

  /**
   * 自动选择最佳模板
   */
  autoSelectTemplate(data) {
    // 根据内容类型自动选择模板
    if (data.type === 'video' || data.duration) {
      return { type: 'video', format: 'standard' };
    }

    if (data.type === 'repository') {
      return { type: 'repository', format: 'standard' };
    }

    if (data.platform && ['zhihu', 'xhs', 'bilibili'].includes(data.platform)) {
      return { type: 'social', format: 'standard' };
    }

    // 默认使用知识模板
    return { type: 'knowledge', format: 'standard' };
  }
}

module.exports = HappyDogTemplateEngine;