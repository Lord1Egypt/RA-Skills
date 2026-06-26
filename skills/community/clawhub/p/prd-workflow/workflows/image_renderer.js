/**
 * 图片渲染服务 v1.0
 *
 * 统一的图片渲染模块，支持：
 * - Mermaid → PNG（使用 mermaid-cli mmdc）
 * - HTML → PNG（使用 htmlPrototype 截图）
 * - 批量渲染
 * - 缓存管理
 *
 * v3.0.0 新增模块
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

class ImageRenderer {
  constructor(options = {}) {
    this.version = '1.0';
    this.outputDir = options.outputDir || './output/images';
    this.cacheDir = options.cacheDir || './output/.cache';
    this.verbose = options.verbose !== false;

    // 默认渲染配置
    this.config = {
      mermaid: {
        width: 1600,
        height: 1200,
        backgroundColor: 'white',
        theme: 'default'
      },
      html: {
        width: 1440,
        height: 900,
        format: 'png'
      }
    };

    // 初始化 Puppeteer 配置（使用系统 Chrome）
    this.puppeteerConfigPath = this.initPuppeteerConfig();
  }

  /**
   * 初始化 Puppeteer 配置文件（使用系统 Chrome）
   */
  initPuppeteerConfig() {
    const configDir = this.cacheDir;
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }

    const configPath = path.join(configDir, 'puppeteer-config.json');

    // 检测系统 Chrome 路径
    const chromePaths = this.getChromePaths();
    const chromePath = chromePaths.find(p => fs.existsSync(p));

    const config = {
      executablePath: chromePath || undefined,
      headless: true
    };

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');

    if (this.verbose && chromePath) {
      console.log(`   🌐 使用系统 Chrome: ${chromePath}`);
    }

    return configPath;
  }

  /**
   * 获取可能的 Chrome 路径
   */
  getChromePaths() {
    const platform = os.platform();
    const homeDir = os.homedir();

    const paths = [];

    // Puppeteer 缓存目录中的 chrome-headless-shell
    const puppeteerCachePaths = [
      path.join(homeDir, '.cache', 'puppeteer', 'chrome-headless-shell'),
      path.join(homeDir, 'Library', 'Caches', 'puppeteer', 'chrome-headless-shell')
    ];

    for (const cachePath of puppeteerCachePaths) {
      if (fs.existsSync(cachePath)) {
        // 查找最新的版本目录
        const versions = fs.readdirSync(cachePath).filter(v =>
          v.startsWith('mac-') || v.startsWith('linux-') || v.startsWith('win-')
        );
        for (const version of versions) {
          const shellPath = path.join(cachePath, version, 'chrome-headless-shell');
          if (fs.existsSync(shellPath)) {
            paths.push(shellPath);
          }
          // macOS .app 格式
          const appPath = path.join(cachePath, version, 'Google Chrome for Testing.app', 'Contents', 'MacOS', 'Google Chrome for Testing');
          if (fs.existsSync(appPath)) {
            paths.push(appPath);
          }
        }
      }
    }

    // 系统 Chrome
    if (platform === 'darwin') {
      paths.push(
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
      );
    } else if (platform === 'win32') {
      paths.push(
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'
      );
    } else {
      paths.push(
        '/usr/bin/google-chrome',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium'
      );
    }

    return paths;
  }

  /**
   * 渲染 Mermaid 代码为 PNG
   *
   * @param {string} mermaidCode - Mermaid 代码
   * @param {string} outputPath - 输出路径（不含扩展名）
   * @param {Object} options - 渲染选项
   * @returns {Object} - { success, path, error }
   */
  renderMermaid(mermaidCode, outputPath, options = {}) {
    const config = { ...this.config.mermaid, ...options };

    // 确保 mermaid-cli 可用
    if (!this.checkMmdc()) {
      return { success: false, error: 'mermaid-cli (mmdc) 未安装' };
    }

    // 创建临时 .mmd 文件
    const tempMmd = this.getTempPath('mermaid', '.mmd');
    fs.writeFileSync(tempMmd, mermaidCode, 'utf8');

    // 确定输出路径
    const pngPath = outputPath.endsWith('.png') ? outputPath : `${outputPath}.png`;

    try {
      if (this.verbose) {
        console.log(`   🎨 渲染 Mermaid → PNG...`);
      }

      // 使用 mmdc 渲染（带 Puppeteer 配置）
      const cmd = `mmdc -i "${tempMmd}" -o "${pngPath}" ` +
        `-w ${config.width} -H ${config.height} ` +
        `-b "${config.backgroundColor}" -t ${config.theme} ` +
        `-p "${this.puppeteerConfigPath}"`;

      execSync(cmd, { stdio: this.verbose ? 'inherit' : 'pipe', timeout: 30000 });

      // 清理临时文件
      this.cleanupTemp(tempMmd);

      // 验证输出
      if (fs.existsSync(pngPath) && fs.statSync(pngPath).size > 100) {
        if (this.verbose) {
          console.log(`   ✅ 渲染成功：${pngPath}`);
        }
        return { success: true, path: pngPath };
      } else {
        return { success: false, error: '输出文件无效' };
      }

    } catch (error) {
      this.cleanupTemp(tempMmd);
      return { success: false, error: error.message };
    }
  }

  /**
   * 批量渲染 Mermaid 图表
   *
   * @param {Array} diagrams - [{ name, code }] 数组
   * @param {string} outputDir - 输出目录
   * @returns {Array} - 渲染结果数组
   */
  renderMermaidBatch(diagrams, outputDir) {
    const results = [];

    for (const diagram of diagrams) {
      const outputPath = path.join(outputDir, `${diagram.name}.png`);
      const result = this.renderMermaid(diagram.code, outputPath);
      results.push({
        name: diagram.name,
        ...result
      });
    }

    return results;
  }

  /**
   * 从 PRD Markdown 提取并渲染所有 Mermaid 图表
   *
   * @param {string} markdown - PRD Markdown 内容
   * @param {string} outputDir - 输出目录
   * @returns {Object} - { diagrams: [], images: [] }
   */
  renderPRDDiagrams(markdown, outputDir) {
    // 提取所有 Mermaid 代码块
    const mermaidBlocks = this.extractMermaidBlocks(markdown);

    if (mermaidBlocks.length === 0) {
      if (this.verbose) {
        console.log('   ℹ️  未找到 Mermaid 图表');
      }
      return { diagrams: [], images: [] };
    }

    // ⭐ 确保 outputDir 存在
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
      if (this.verbose) {
        console.log(`   ✅ 创建图片目录：${outputDir}`);
      }
    }

    if (this.verbose) {
      console.log(`   📊 发现 ${mermaidBlocks.length} 个 Mermaid 图表`);
    }

    // 渲染每个图表
    const images = [];
    for (let i = 0; i < mermaidBlocks.length; i++) {
      const block = mermaidBlocks[i];
      const name = block.title || `diagram_${i + 1}`;
      const outputPath = path.join(outputDir, `${name}.png`);

      const result = this.renderMermaid(block.code, outputPath);
      if (result.success) {
        images.push({
          name,
          path: result.path,
          title: block.title,
          section: block.section
        });
      }
    }

    return { diagrams: mermaidBlocks, images };
  }

  /**
   * 从 Markdown 提取 Mermaid 代码块
   *
   * @param {string} markdown - Markdown 内容
   * @returns {Array} - [{ code, title, section }]
   */
  extractMermaidBlocks(markdown) {
    const blocks = [];
    const lines = markdown.split('\n');

    let currentSection = '';
    let inMermaid = false;
    let mermaidCode = '';
    let mermaidTitle = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // 检测章节标题
      if (line.match(/^##+ /)) {
        currentSection = line.replace(/^##+ /, '').trim();
      }

      // 检测 Mermaid 开始
      if (line.trim() === '```mermaid') {
        inMermaid = true;
        mermaidCode = '';
        // 从前面的标题获取图表名称
        if (i > 0 && lines[i - 1].match(/^###+ /)) {
          mermaidTitle = lines[i - 1].replace(/^###+ /, '').trim();
        } else {
          mermaidTitle = `diagram_${blocks.length + 1}`;
        }
        continue;
      }

      // 检测 Mermaid 结束
      if (inMermaid && line.trim() === '```') {
        inMermaid = false;
        if (mermaidCode.trim()) {
          blocks.push({
            code: mermaidCode.trim(),
            title: this.sanitizeFilename(mermaidTitle),
            section: currentSection
          });
        }
        continue;
      }

      // 收集 Mermaid 代码
      if (inMermaid) {
        mermaidCode += line + '\n';
      }
    }

    return blocks;
  }

  /**
   * 检查 mmdc 是否可用
   */
  checkMmdc() {
    try {
      execSync('mmdc --version', { stdio: 'pipe' });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 获取临时文件路径
   */
  getTempPath(prefix, ext) {
    const tempDir = this.cacheDir;
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
    return path.join(tempDir, `${prefix}_${Date.now()}${ext}`);
  }

  /**
   * 清理临时文件
   */
  cleanupTemp(tempPath) {
    try {
      if (fs.existsSync(tempPath)) {
        fs.unlinkSync(tempPath);
      }
    } catch {
      // 忽略清理错误
    }
  }

  /**
   * 清理文件名（移除特殊字符）
   */
  sanitizeFilename(name) {
    return name
      .replace(/[^\w\u4e00-\u9fa5]/g, '_')  // 保留中文、字母、数字、下划线
      .replace(/_+/g, '_')                   // 合并连续下划线
      .replace(/^_|_$/, '')                  // 移除首尾下划线
      .toLowerCase()
      .slice(0, 50);                         // 限制长度
  }

  /**
   * 生成图片映射文件（用于 Word 导出）
   *
   * @param {Array} images - 图片数组
   * @param {string} outputPath - 输出路径
   */
  generateImageMap(images, outputPath) {
    const imageMap = {
      version: '1.0',
      generated: new Date().toISOString(),
      images: images.map(img => ({
        name: img.name,
        file: img.path,
        caption: img.title || img.name,
        section: img.section || ''
      }))
    };

    fs.writeFileSync(outputPath, JSON.stringify(imageMap, null, 2), 'utf8');
    if (this.verbose) {
      console.log(`   ✅ 图片映射已保存：${outputPath}`);
    }

    return imageMap;
  }

  /**
   * 替换 Markdown 中的 Mermaid 代码块为图片引用
   *
   * @param {string} markdown - Markdown 内容
   * @param {Array} images - 图片数组 [{ name, path, title }]
   * @returns {string} - 替换后的 Markdown
   */
  replaceMermaidWithImages(markdown, images) {
    let result = markdown;
    const blocks = this.extractMermaidBlocks(markdown);

    for (let i = 0; i < blocks.length; i++) {
      const block = blocks[i];
      const image = images.find(img => img.name === block.title || img.name === `diagram_${i + 1}`);

      if (image) {
        // 构建图片引用
        const imageRef = `\n![${image.title || block.title}](${image.path})\n`;

        // 替换 Mermaid 代码块
        const mermaidBlock = '```mermaid\n' + block.code + '\n```';
        result = result.replace(mermaidBlock, imageRef);
      }
    }

    return result;
  }
}

module.exports = { ImageRenderer };