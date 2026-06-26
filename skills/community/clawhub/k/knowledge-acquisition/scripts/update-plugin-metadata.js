// 批量更新插件元数据脚本
const fs = require('fs');
const path = require('path');

// 插件元数据定义
const pluginMetas = {
  'content-extractor.js': {
    meta: {
      name: 'content-extractor',
      version: '2.0.0',
      capabilities: ['basic', 'advanced'],
      tier: 'core',
      supportedPlatforms: ['generic-web'],
      features: ['content-extraction', 'generic-web', 'basic-classification'],
      description: '通用网页内容提取器',
      dependencies: ['axios', 'cheerio']
    },
    prepend: true // 添加到文件开头
  },
  'zhihu.js': {
    meta: {
      name: 'zhihu',
      version: '1.0.0',
      capabilities: ['advanced'],
      tier: 'advanced',
      supportedPlatforms: ['zhihu'],
      features: ['content-extraction', 'advanced-classification', 'qa-content'],
      description: '知乎内容提取',
      dependencies: ['axios', 'cheerio']
    },
    prepend: true
  },
  'bilibili.js': {
    meta: {
      name: 'bilibili',
      version: '1.0.0',
      capabilities: ['advanced'],
      tier: 'advanced',
      supportedPlatforms: ['bilibili'],
      features: ['video-extraction', 'subtitle-extraction', 'video-info'],
      description: 'B站视频内容提取',
      dependencies: ['axios', 'fluent-ffmpeg']
    },
    prepend: true
  },
  'github.js': {
    meta: {
      name: 'github',
      version: '1.0.0',
      capabilities: ['advanced'],
      tier: 'advanced',
      supportedPlatforms: ['github'],
      features: ['repo-extraction', 'readme-analysis', 'project-info'],
      description: 'GitHub项目信息提取',
      dependencies: ['axios']
    },
    prepend: true
  },
  'xiaohongshu.js': {
    meta: {
      name: 'xiaohongshu',
      version: '1.0.0',
      capabilities: ['expert'],
      tier: 'expert',
      supportedPlatforms: ['xiaohongshu'],
      features: ['ocr-extraction', 'advanced-content-analysis', 'image-processing'],
      description: '小红书内容提取（需要Puppeteer）',
      dependencies: ['puppeteer', 'cheerio']
    },
    prepend: true
  }
};

// 更新单个插件文件
function updatePluginFile(filePath, metaInfo) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');

    // 构建元数据字符串
    const metaString = `// 插件元数据
const pluginMeta = ${JSON.stringify(metaInfo.meta, null, 2)};

`;

    // 移除原有的元数据（如果存在）
    content = content.replace(/\/\/ 插件元数据[\s\S]*?const pluginMeta = [\s\S]*?;\n\n/, '');

    if (metaInfo.prepend) {
      // 在开头添加元数据
      content = metaString + content;
    }

    // 检查是否有模块导出
    if (!content.includes('module.exports')) {
      // 在文件末尾添加模块导出
      const className = metaInfo.meta.name.charAt(0).toUpperCase() + metaInfo.meta.name.slice(1);
      content += `

// 导出插件
module.exports = {
  ${className},
  pluginMeta,
  // 提取器实例
  instance: new ${className}()
};
`;
    } else {
      // 更新现有的模块导出
      const exportRegex = /(module\.exports = \{[\s\S]*?\})/;
      const match = content.match(exportRegex);
      if (match) {
        let exportContent = match[1];
        // 如果没有pluginMeta，添加它
        if (!exportContent.includes('pluginMeta')) {
          const className = metaInfo.meta.name.charAt(0).toUpperCase() + metaInfo.meta.name.slice(1);
          exportContent = exportContent.replace(
            'module.exports = {',
            `module.exports = {
  pluginMeta,`
          );
        }
        content = content.replace(exportRegex, exportContent);
      }
    }

    // 确保有 handlePlatform 方法（如果没有的话）
    if (!content.includes('handlePlatform')) {
      // 在类的最后一个方法后添加 handlePlatform
      const classEndRegex = /\n\s*}\s*$/;
      if (classEndRegex.test(content)) {
        const className = metaInfo.meta.name.charAt(0).toUpperCase() + metaInfo.meta.name.slice(1);
        const handleMethod = `
  // 处理平台内容 - 统一接口
  async handlePlatform(platform, url, options = {}) {
    if (!this.supportedPlatforms.includes(platform)) {
      throw new Error(\`不支持的平台: \${platform}\`);
    }

    // 根据平台调用相应的提取方法
    switch (platform) {
      case '${metaInfo.meta.supportedPlatforms[0]}':
        return await this.${metaInfo.meta.supportedPlatforms[0]}Extract(url, options);
      default:
        throw new Error(\`未实现平台 \${platform} 的处理逻辑\`);
    }
  }

  // 插件初始化钩子
  async initialize() {
    console.log('${metaInfo.meta.name}插件初始化完成');
  }`;

        content = content.replace(classEndRegex, handleMethod + '\n}');
      }
    }

    // 添加平台支持数组
    if (!content.includes('this.supportedPlatforms')) {
      const constructorRegex = /(constructor\(options = \{\}\) \{[\s\S]*?})/;
      const match = content.match(constructorRegex);
      if (match) {
        const constructor = match[1];
        const updatedConstructor = constructor.replace(
          'constructor(options = {}) {',
          `constructor(options = {}) {
    this.supportedPlatforms = ${JSON.stringify(metaInfo.meta.supportedPlatforms)};`
        );
        content = content.replace(constructorRegex, updatedConstructor);
      }
    }

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ 更新插件: ${path.basename(filePath)}`);
  } catch (error) {
    console.error(`✗ 更新插件失败 ${filePath}:`, error);
  }
}

// 主函数
function main() {
  console.log('开始批量更新插件元数据...\n');

  const pluginsDir = path.join(__dirname, '../plugins');

  // 遍历所有需要更新的插件
  for (const [filename, metaInfo] of Object.entries(pluginMetas)) {
    // 查找文件位置（可能在子目录中）
    const possiblePaths = [
      path.join(pluginsDir, filename),
      path.join(pluginsDir, 'core', filename),
      path.join(pluginsDir, 'advanced', filename),
      path.join(pluginsDir, 'expert', filename)
    ];

    for (const filePath of possiblePaths) {
      if (fs.existsSync(filePath)) {
        updatePluginFile(filePath, metaInfo);
        break;
      }
    }
  }

  console.log('\n批量更新完成！');
}

// 运行脚本
if (require.main === module) {
  main();
}

module.exports = { updatePluginFile, pluginMetas };