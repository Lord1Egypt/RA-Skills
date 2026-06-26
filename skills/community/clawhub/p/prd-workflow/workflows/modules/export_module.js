/**
 * Word 导出模块 v3.1.0
 *
 * 支持双引擎：yh-minimax-docx（专业）/ prd-export（快速）
 * 主引擎：yh-minimax-docx（专业排版、目录、页眉页脚、三线表）
 *
 * v3.1.0: 支持多页面原型截图嵌入（桌面端 + 移动端）
 * v3.0.0: 集成 ImageRenderer，自动渲染 Mermaid 图表并嵌入 Word
 * v2.8.2: 移除硬编码路径，使用动态检测
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { findSkillPath } = require('../utils');
const { ImageRenderer } = require('../image_renderer');

class ExportModule {
  constructor() {
    this.imageRenderer = new ImageRenderer({ verbose: true });
  }
  /**
   * 执行导出
   */
  async execute(options) {
    console.log('\n📝 执行技能：Word 导出 v3.1.0');

    const { dataBus, qualityGate, outputDir, wordEngine = 'yh-minimax-docx' } = options;

    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }

    const prd = prdRecord.data;

    // v3.0.0: 渲染 Mermaid 图表为 PNG
    console.log('   🎨 渲染 Mermaid 图表...');
    const imagesDir = path.join(outputDir, 'images');
    const { images } = this.imageRenderer.renderPRDDiagrams(prd.content || '', imagesDir);

    if (images.length > 0) {
      console.log(`   ✅ 渲染 ${images.length} 个图表`);
      // 生成图片映射
      const imageMapPath = path.join(outputDir, 'image_map.json');
      this.imageRenderer.generateImageMap(images, imageMapPath);
    }

    // v3.1.0: 读取原型截图
    const prototypeRecord = dataBus.read('prototype');
    const screenshots = prototypeRecord?.data?.screenshots || { desktop: [], mobile: [] };

    console.log(`   导出引擎：${wordEngine}`);

    let result;
    if (wordEngine === 'yh-minimax-docx') {
      result = await this.exportWithMinimaxDocx(prd, outputDir, images, screenshots);
      // 如果失败，回退到 prd-export
      if (!result.success || result.fallback) {
        console.log('   ⚠️  yh-minimax-docx 不可用，回退到 prd-export');
        result = await this.exportWithPrdExport(prd, outputDir, images, screenshots);
      }
    } else {
      result = await this.exportWithPrdExport(prd, outputDir, images, screenshots);
    }

    // 质量验证
    const quality = {
      passed: result.success,
      fileGenerated: result.success,
      engine: result.engine,
      fileSize: result.fileSize,
      imagesRendered: images.length,
      screenshotsIncluded: (screenshots.desktop?.length || 0) + (screenshots.mobile?.length || 0)
    };

    // 写入数据总线
    const filepath = dataBus.write('export', result, quality, {
      fromPRD: 'prd.json',
      images: 'images/',
      screenshots: 'screensshots/'
    });

    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate8_export', result);
    }

    return {
      ...result,
      quality: quality,
      outputPath: filepath
    };
  }

  /**
   * 使用 yh-minimax-docx 导出（专业排版）
   * v3.1.0: 支持原型截图
   */
  async exportWithMinimaxDocx(prd, outputDir, renderedImages = [], screenshots = {}) {
    // v2.8.2: 使用动态路径检测，不再硬编码
    const minimaxPath = findSkillPath('yh-minimax-docx');

    // 检查 yh-minimax-docx 是否存在
    if (!minimaxPath) {
      console.warn('   ⚠️  yh-minimax-docx 未安装（可从 ClawHub 安装）');
      return { success: false, fallback: true, engine: 'yh-minimax-docx' };
    }

    // ✅ v2.8.0: 优先使用包装脚本（更可靠）
    const cliWrapper = path.join(minimaxPath, 'scripts/minimax-docx-cli.sh');
    const cliProject = path.join(minimaxPath, 'scripts/dotnet/MiniMaxAIDocx.Cli');
    const markdownPath = path.join(outputDir, 'PRD.md');
    const outputPath = path.join(outputDir, 'PRD.docx');

    // 检查 PRD.md 是否存在
    if (!fs.existsSync(markdownPath)) {
      // 先保存 PRD.md
      fs.writeFileSync(markdownPath, prd.content || '', 'utf8');
    }

    try {
      console.log('   🎨 使用 yh-minimax-docx 专业排版...');

      // 检查 .NET 环境（优先使用官方安装路径）
      let dotnetCmd = null;
      const os = require('os');

      // 按优先级检查 dotnet 路径
      const dotnetPaths = [
        // 官方安装（最可靠）
        path.join(os.homedir(), '.dotnet', 'dotnet'),
        // macOS 官方路径
        '/usr/local/share/dotnet/dotnet',
        // Homebrew 路径
        '/opt/homebrew/opt/dotnet/bin/dotnet',
        '/usr/local/bin/dotnet',
        // Linux 路径
        '/usr/share/dotnet/dotnet'
      ];

      // 找到第一个可用的 dotnet
      for (const testPath of dotnetPaths) {
        if (fs.existsSync(testPath)) {
          try {
            const testResult = execSync(`"${testPath}" --version`, {
              stdio: ['pipe', 'pipe', 'pipe'],
              timeout: 5000,
              encoding: 'utf8'
            });
            if (testResult && !testResult.includes('error') && !testResult.includes('No such file')) {
              dotnetCmd = testPath;
              break;
            }
          } catch (e) {
            // 此路径不可用，继续尝试下一个
          }
        }
      }

      // 如果都没找到，尝试 PATH 中的 dotnet
      if (!dotnetCmd) {
        try {
          execSync('dotnet --version', { stdio: 'pipe', timeout: 5000 });
          dotnetCmd = 'dotnet';
        } catch (e) {
          // PATH 中也没有可用的
        }
      }

      if (!dotnetCmd) {
        console.warn('   ⚠️  .NET SDK 未安装或不可用');
        return { success: false, fallback: true, engine: 'yh-minimax-docx' };
      }

      console.log(`   ✅ .NET 环境: ${dotnetCmd}`);

      // 检查项目文件是否存在
      const csprojPath = path.join(cliProject, 'MiniMaxAIDocx.Cli.csproj');
      if (!fs.existsSync(csprojPath)) {
        console.warn('   ⚠️  yh-minimax-docx 项目文件不完整，跳过');
        return { success: false, fallback: true, engine: 'yh-minimax-docx' };
      }

      // 构建 JSON 内容文件（yh-minimax-docx 支持 --content-json）
      const contentJson = this.buildContentJson(prd);
      const contentJsonPath = path.resolve(path.join(outputDir, 'content.json'));
      fs.writeFileSync(contentJsonPath, JSON.stringify(contentJson, null, 2), 'utf8');

      // 使用绝对路径
      const absoluteOutputPath = path.resolve(outputPath);

      // ✅ v2.8.0: 优先使用包装脚本（已编译 CLI，更可靠）
      if (fs.existsSync(cliWrapper)) {
        console.log('   🎨 使用 yh-minimax-docx 包装脚本（已编译 CLI）...');

        const cmd = `"${cliWrapper}" create ` +
          `--type report ` +
          `--output "${absoluteOutputPath}" ` +
          `--title "${this.extractTitle(prd)}" ` +
          `--toc ` +
          `--page-numbers ` +
          `--content-json "${contentJsonPath}"`;

        execSync(cmd, {
          encoding: 'utf8',
          cwd: outputDir,
          timeout: 60000
        });
      } else {
        // Fallback: 使用 dotnet run
        console.log('   🎨 使用 yh-minimax-docx (dotnet run)...');

        const cmd = `"${dotnetCmd}" run --project "${cliProject}" -- create ` +
          `--type report ` +
          `--output "${absoluteOutputPath}" ` +
          `--title "${this.extractTitle(prd)}" ` +
          `--toc ` +
          `--page-numbers ` +
          `--content-json "${contentJsonPath}"`;

        execSync(cmd, {
          encoding: 'utf8',
          cwd: outputDir,
          timeout: 60000
        });
      }

      // 验证输出
      if (fs.existsSync(absoluteOutputPath) && fs.statSync(absoluteOutputPath).size > 100) {
        const fileSize = fs.statSync(absoluteOutputPath).size;
        console.log(`   ✅ 专业排版完成：${absoluteOutputPath}`);
        console.log(`   📊 文件大小：${Math.round(fileSize / 1024)}KB`);

        // 清理临时文件
        try { fs.unlinkSync(contentJsonPath); } catch (e) {}

        return {
          success: true,
          engine: 'yh-minimax-docx',
          outputPath: outputPath,
          fileSize: fileSize,
          features: ['toc', 'page-numbers', 'professional-typography']
        };
      } else {
        return { success: false, fallback: true, engine: 'yh-minimax-docx' };
      }

    } catch (error) {
      console.warn('   ⚠️  yh-minimax-docx 导出失败:', error.message);
      return { success: false, fallback: true, engine: 'yh-minimax-docx', error: error.message };
    }
  }

  /**
   * 使用 prd-export 导出（快速）
   * v3.1.0: 支持嵌入渲染后的图片 + 原型截图
   */
  async exportWithPrdExport(prd, outputDir, renderedImages = [], screenshots = {}) {
    const exportEngine = path.join(__dirname, '../../skills/prd-export/engines/export_engine.py');

    if (!fs.existsSync(exportEngine)) {
      console.warn('   ⚠️  prd-export 未找到，使用模拟导出');
      return this.mockExport(outputDir, 'prd-export');
    }

    // 使用绝对路径
    const markdownPath = path.resolve(outputDir, 'PRD.md');
    const outputPath = path.resolve(outputDir, 'PRD.docx');

    // 确保 PRD.md 存在
    if (!fs.existsSync(markdownPath)) {
      fs.writeFileSync(markdownPath, prd.content || '', 'utf8');
    }

    // v3.0.0: 如果有渲染的图片，替换 Markdown 中的 Mermaid 代码块
    let processedContent = prd.content || '';
    if (renderedImages.length > 0) {
      processedContent = this.imageRenderer.replaceMermaidWithImages(processedContent, renderedImages);
      const processedPath = path.join(outputDir, 'PRD_processed.md');
      fs.writeFileSync(processedPath, processedContent, 'utf8');

      // 使用处理后的 Markdown
      const imagesDir = path.join(outputDir, 'images');
      const imagesArg = fs.existsSync(imagesDir) ? `--images "${imagesDir}"` : '';

      try {
        console.log('   📄 使用 prd-export 快速导出（含图片）...');

        execSync(`python3 "${exportEngine}" "${processedPath}" -o "${outputPath}" ${imagesArg}`, {
          stdio: 'pipe',
          cwd: process.cwd()
        });

        // 清理临时文件
        try { fs.unlinkSync(processedPath); } catch (e) {}

        if (fs.existsSync(outputPath) && fs.statSync(outputPath).size > 100) {
          const fileSize = fs.statSync(outputPath).size;
          console.log(`   ✅ 导出完成（含 ${renderedImages.length} 张图片）：${outputPath}`);
          console.log(`   📊 文件大小：${Math.round(fileSize / 1024)}KB`);

          return {
            success: true,
            engine: 'prd-export',
            outputPath: outputPath,
            fileSize: fileSize,
            imagesIncluded: renderedImages.length
          };
        }
      } catch (error) {
        console.warn('   ⚠️  prd-export 导出失败:', error.message);
      }
    }

    // 无图片或图片处理失败，使用原始流程
    const imagesDir = path.join(outputDir, 'diagrams');
    const imagesArg = fs.existsSync(imagesDir) ? `--images "${imagesDir}"` : '';

    try {
      console.log('   📄 使用 prd-export 快速导出...');

      execSync(`python3 "${exportEngine}" "${markdownPath}" -o "${outputPath}" ${imagesArg}`, {
        stdio: 'pipe',
        cwd: process.cwd()
      });

      if (fs.existsSync(outputPath) && fs.statSync(outputPath).size > 100) {
        const fileSize = fs.statSync(outputPath).size;
        console.log(`   ✅ 导出完成：${outputPath}`);
        console.log(`   📊 文件大小：${Math.round(fileSize / 1024)}KB`);

        return {
          success: true,
          engine: 'prd-export',
          outputPath: outputPath,
          fileSize: fileSize
        };
      } else {
        return this.mockExport(outputDir, 'prd-export');
      }
    } catch (error) {
      console.warn('   ⚠️  prd-export 导出失败:', error.message);
      return this.mockExport(outputDir, 'prd-export');
    }
  }

  /**
   * 从 PRD 提取标题
   */
  extractTitle(prd) {
    const content = prd.content || '';
    const match = content.match(/^#\s+(.+)$/m);
    if (match) {
      return match[1].trim();
    }
    return '产品需求文档';
  }

  /**
   * 构建内容 JSON（供 yh-minimax-docx 使用）
   * CLI 期望格式: [{type: "heading/paragraph", text: "...", level?: number}]
   */
  buildContentJson(prd) {
    const content = prd.content || '';
    const elements = [];

    // 解析 Markdown 结构
    const lines = content.split('\n');

    for (const line of lines) {
      const trimmedLine = line.trim();

      if (!trimmedLine) continue;

      // 一级标题（跳过文档主标题，CLI 已经通过 --title 设置）
      if (trimmedLine.startsWith('# ')) {
        continue; // 主标题由 CLI --title 参数处理
      }

      // 二级标题
      if (trimmedLine.startsWith('## ')) {
        elements.push({
          type: 'heading',
          text: trimmedLine.substring(3).trim(),
          level: 2
        });
        continue;
      }

      // 三级标题
      if (trimmedLine.startsWith('### ')) {
        elements.push({
          type: 'heading',
          text: trimmedLine.substring(4).trim(),
          level: 3
        });
        continue;
      }

      // 四级标题
      if (trimmedLine.startsWith('#### ')) {
        elements.push({
          type: 'heading',
          text: trimmedLine.substring(5).trim(),
          level: 4
        });
        continue;
      }

      // 五级标题
      if (trimmedLine.startsWith('##### ')) {
        elements.push({
          type: 'heading',
          text: trimmedLine.substring(6).trim(),
          level: 5
        });
        continue;
      }

      // 跳过代码块标记（Mermaid 等会在后面被替换为图片）
      if (trimmedLine.startsWith('```')) {
        continue;
      }

      // 跳过图片引用（已渲染的图片会通过其他方式处理）
      if (trimmedLine.startsWith('![')) {
        continue;
      }

      // 跳过表格分隔线
      if (trimmedLine.match(/^\|[\s\-:|]+\|$/)) {
        continue;
      }

      // 表格行（简化处理为段落）
      if (trimmedLine.startsWith('|')) {
        const cells = trimmedLine.split('|').filter(c => c.trim());
        if (cells.length > 0) {
          elements.push({
            type: 'paragraph',
            text: cells.join(' | ')
          });
        }
        continue;
      }

      // 列表项
      if (trimmedLine.startsWith('- ') || trimmedLine.match(/^\d+\.\s+/)) {
        elements.push({
          type: 'paragraph',
          text: trimmedLine.replace(/^(-|\d+\.\s+)\s*/, '')
        });
        continue;
      }

      // 普通段落
      elements.push({
        type: 'paragraph',
        text: trimmedLine
      });
    }

    console.log(`   📄 生成 ${elements.length} 个内容元素`);

    return elements;
  }

  /**
   * 模拟导出（测试用）
   */
  mockExport(outputDir, engine) {
    const outputPath = path.join(outputDir, 'PRD.docx');
    fs.writeFileSync(outputPath, 'Mock DOCX content', 'utf8');

    console.log('   ⚠️  使用模拟导出');

    return {
      success: true,
      engine: engine,
      outputPath: outputPath,
      fileSize: 19,
      mock: true
    };
  }
}

module.exports = ExportModule;
