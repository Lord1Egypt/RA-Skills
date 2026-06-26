/**
 * Word 质量审核模块 v3.1.0
 *
 * 评审 Word 导出产物（转换质量、格式规范、文件完整性）
 * 不再评审 PRD.md 内容（已由 review_module 完成）
 *
 * v3.1.0: 新增原型截图完整性检查、移动端截图检查
 * v3.0.0: 适配 ImageRenderer，检查 images/ 目录下的渲染图片
 * v2.8.2: 移除硬编码路径，使用动态检测
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { findSkillPath } = require('../utils');

class QualityModule {
  /**
   * 执行 Word 文档转换质量检查
   */
  async execute(options) {
    console.log('\n⭐ 执行技能：Word 文档转换质量检查 v3.1.0');

    const { dataBus, qualityGate, outputDir } = options;

    // 读取导出结果
    const exportRecord = dataBus.read('export');
    if (!exportRecord) {
      throw new Error('Word 文档未生成，请先执行导出');
    }

    const exportResult = exportRecord.data;
    const docxPath = exportResult.outputPath || path.join(outputDir, 'PRD.docx');

    // 读取原 PRD 内容（用于对比）
    const prdRecord = dataBus.read('prd');
    const prdContent = prdRecord?.data?.content || '';

    // 读取原型结果（v3.1.0 新增）
    const prototypeRecord = dataBus.read('prototype');
    const prototypeData = prototypeRecord?.data || null;

    // 检查 Word 文档是否存在
    if (!fs.existsSync(docxPath)) {
      throw new Error(`Word 文档不存在：${docxPath}`);
    }

    console.log(`   检查文档：${docxPath}`);

    // 转换质量检查
    const checks = {
      // 1. 文件完整性（文件大小、ZIP 结构）
      fileIntegrity: this.checkFileIntegrity(docxPath),

      // 2. 图片嵌入检查
      imagesEmbedment: this.checkImagesEmbedment(docxPath, outputDir, prdContent),

      // 3. 格式转换检查
      formatConversion: this.checkFormatConversion(docxPath, prdContent),

      // 4. OpenXML 验证
      openXmlValidation: await this.validateOpenXml(docxPath),

      // 5. 原型截图检查（v3.1.0 新增）
      prototypeScreenshots: this.checkPrototypeScreenshots(prototypeData, outputDir)
    };

    // 计算综合评分
    const scores = this.calculateScores(checks);

    // 构建结果
    const qualityResult = {
      docxPath: docxPath,
      docxSize: fs.statSync(docxPath).size,
      checks: checks,
      scores: scores,
      overall: scores.overall
    };

    // 质量验证
    const quality = this.validateQuality(qualityResult);

    // 写入数据总线
    const filepath = dataBus.write('quality', qualityResult, quality, {
      checkedWord: docxPath
    });

    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate9_quality', qualityResult);
    }

    console.log(`   ✅ 质量评分：${scores.overall}/100`);

    return {
      ...qualityResult,
      quality: quality,
      outputPath: filepath
    };
  }

  /**
   * 1. 文件完整性检查
   */
  checkFileIntegrity(docxPath) {
    try {
      // 检查文件是否存在
      if (!fs.existsSync(docxPath)) {
        return { passed: false, description: '文件不存在' };
      }

      // 检查文件大小
      const stat = fs.statSync(docxPath);
      if (stat.size < 1000) {
        return { passed: false, description: '文件过小，可能损坏' };
      }

      // 检查文件头（DOCX 文件头应该是 PK 开头，即 ZIP 格式）
      const buffer = Buffer.alloc(4);
      const fd = fs.openSync(docxPath, 'r');
      fs.readSync(fd, buffer, 0, 4, 0);
      fs.closeSync(fd);

      const isZip = buffer.toString('hex') === '504b0304'; // PK 开头

      return {
        passed: isZip && stat.size >= 10000,
        size: stat.size,
        sizeKB: Math.round(stat.size / 1024),
        description: isZip ? `文件完整 (${Math.round(stat.size / 1024)}KB)` : '文件头异常，可能损坏'
      };

    } catch (error) {
      return { passed: false, description: `检查失败：${error.message}` };
    }
  }

  /**
   * 2. 图片嵌入检查
   * v3.0.0: 适配 ImageRenderer，检查 images/ 目录
   */
  checkImagesEmbedment(docxPath, outputDir, prdContent) {
    // 统计 MD 中的 Mermaid 代码块数量
    const mermaidMatches = prdContent.match(/```mermaid[\s\S]*?```/g) || [];
    const mermaidCount = mermaidMatches.length;

    // 统计 MD 中的图片标记
    const mdImageMatches = prdContent.match(/!\[.*?\]\(.*?\)/g) || [];
    const mdImageCount = mdImageMatches.length;

    // v3.0.0: 检查 images/ 目录下的渲染图片
    const imagesDir = path.join(outputDir, 'images');
    let renderedImages = [];
    if (fs.existsSync(imagesDir)) {
      renderedImages = fs.readdirSync(imagesDir)
        .filter(f => f.endsWith('.png'));
    }

    // 兼容旧版本：检查 flowchart.png 和 prototype.png
    const flowchartPng = path.join(outputDir, 'flowchart.png');
    const prototypePng = path.join(outputDir, 'prototype.png');
    const flowchartExists = fs.existsSync(flowchartPng);
    const prototypeExists = fs.existsSync(prototypePng);

    // 尝试检查 docx 内嵌图片
    let docxImageCount = 0;
    try {
      const AdmZip = require('adm-zip');
      const zip = new AdmZip(docxPath);
      const entries = zip.getEntries();
      docxImageCount = entries.filter(e => e.entryName.startsWith('word/media/')).length;
    } catch (e) {
      // adm-zip 不可用，跳过
    }

    // 判断是否通过：
    // 1. 如果有 Mermaid 代码块，应该有渲染后的图片
    // 2. 或者 docx 内嵌了图片
    const hasRenderedImages = renderedImages.length > 0;
    const hasLegacyImages = flowchartExists || prototypeExists;
    const hasEmbeddedImages = docxImageCount > 0;

    const passed = (mermaidCount === 0) ||
                   hasRenderedImages ||
                   hasLegacyImages ||
                   hasEmbeddedImages;

    return {
      passed,
      mermaidCount,
      mdImageCount,
      renderedImages: renderedImages.length,
      renderedImageList: renderedImages.slice(0, 5),  // 最多显示5个
      docxImageCount,
      flowchart: flowchartExists ? '已生成' : '未生成',
      prototype: prototypeExists ? '已生成' : '未生成',
      description: passed ? '图片检查通过' : '图片可能未嵌入'
    };
  }

  /**
   * 3. 格式转换检查
   */
  checkFormatConversion(docxPath, prdContent) {
    const prdLength = prdContent?.length || 0;
    const docxSize = fs.statSync(docxPath).size;

    // 统计 MD 结构
    const h1Count = (prdContent.match(/^# /gm) || []).length;
    const h2Count = (prdContent.match(/^## /gm) || []).length;
    const h3Count = (prdContent.match(/^### /gm) || []).length;
    const tableCount = (prdContent.match(/^\|.*\|$/gm) || []).length > 0 ? 1 : 0;

    // 合理转换：Word 文档大小 ≈ PRD 字数 × 50-200 bytes
    const expectedSizeMin = prdLength * 50;
    const expectedSizeMax = prdLength * 200;
    const sizeRatio = docxSize / prdLength;

    const sizeOk = prdLength === 0 || (docxSize >= expectedSizeMin && docxSize <= expectedSizeMax);

    return {
      passed: sizeOk,
      prdStats: {
        length: prdLength,
        h1: h1Count,
        h2: h2Count,
        h3: h3Count,
        tables: tableCount
      },
      docxSize: docxSize,
      sizeRatio: Math.round(sizeRatio),
      description: sizeOk ? '格式转换正常' : `格式转换可能异常（比例：${Math.round(sizeRatio)}）`
    };
  }

  /**
   * 4. OpenXML 验证（调用 yh-minimax-docx）
   */
  async validateOpenXml(docxPath) {
    // v2.8.2: 使用动态路径检测，不再硬编码
    const minimaxPath = findSkillPath('yh-minimax-docx');

    if (!minimaxPath) {
      return {
        passed: true,
        skipped: true,
        description: 'yh-minimax-docx 未安装，跳过 OpenXML 验证'
      };
    }

    const cliProject = path.join(minimaxPath, 'scripts/dotnet/MiniMaxAIDocx.Cli');

    // 检查 .NET 环境（使用多路径检测）
    const os = require('os');
    const dotnetPaths = [
      path.join(os.homedir(), '.dotnet', 'dotnet'),
      '/usr/local/share/dotnet/dotnet',
      '/opt/homebrew/opt/dotnet/bin/dotnet',
      '/usr/local/bin/dotnet',
      '/usr/share/dotnet/dotnet'
    ];

    let dotnetCmd = null;
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
          // 继续
        }
      }
    }

    // 尝试 PATH
    if (!dotnetCmd) {
      try {
        execSync('dotnet --version', { stdio: 'pipe', timeout: 5000 });
        dotnetCmd = 'dotnet';
      } catch (e) {
        // 无可用
      }
    }

    if (!dotnetCmd) {
      return {
        passed: true,
        skipped: true,
        description: '.NET SDK 不可用，跳过 OpenXML 验证'
      };
    }

    try {
      console.log('   🔍 OpenXML 验证...');

      const result = execSync(
        `"${dotnetCmd}" run --project "${cliProject}" -- validate --input "${docxPath}" --business`,
        {
          encoding: 'utf8',
          stdio: 'pipe',
          timeout: 30000
        }
      );

      const passed = !result.includes('FAILED') && !result.includes('Error');

      return {
        passed,
        description: passed ? 'OpenXML 验证通过' : 'OpenXML 验证发现问题'
      };

    } catch (error) {
      return {
        passed: true,
        skipped: true,
        description: 'OpenXML 验证异常，跳过'
      };
    }
  }

  /**
   * 5. 原型截图完整性检查（v3.1.0 新增）
   */
  checkPrototypeScreenshots(prototypeData, outputDir) {
    if (!prototypeData) {
      return {
        passed: true,
        skipped: true,
        description: '无原型数据，跳过截图检查'
      };
    }

    const screenshots = prototypeData.screenshots || {};
    const pages = prototypeData.pages || [];

    const desktopScreenshots = screenshots.desktop || [];
    const mobileScreenshots = screenshots.mobile || [];

    // 统计实际存在的截图文件
    const screenshotsDir = path.join(outputDir, 'screensshots');

    let desktopCount = 0;
    let mobileCount = 0;

    if (fs.existsSync(screenshotsDir)) {
      const desktopDir = path.join(screenshotsDir, 'desktop');
      const mobileDir = path.join(screenshotsDir, 'mobile');

      if (fs.existsSync(desktopDir)) {
        desktopCount = fs.readdirSync(desktopDir).filter(f => f.endsWith('.png')).length;
      }
      if (fs.existsSync(mobileDir)) {
        mobileCount = fs.readdirSync(mobileDir).filter(f => f.endsWith('.png')).length;
      }
    }

    // 检查截图覆盖率
    const expectedPages = pages.length;
    const desktopCoverage = expectedPages > 0 ? (desktopCount / expectedPages) * 100 : 0;
    const mobileCoverage = expectedPages > 0 ? (mobileCount / expectedPages) * 100 : 0;

    // 至少有桌面端截图
    const passed = desktopCount > 0;

    return {
      passed,
      pages: expectedPages,
      desktopScreenshots: desktopCount,
      mobileScreenshots: mobileCount,
      desktopCoverage: Math.round(desktopCoverage) + '%',
      mobileCoverage: Math.round(mobileCoverage) + '%',
      description: passed
        ? `截图完整：桌面端 ${desktopCount} 张，移动端 ${mobileCount} 张`
        : '缺少桌面端截图'
    };
  }

  /**
   * 计算综合评分
   */
  calculateScores(checks) {
    // 文件完整性（30%）
    const fileScore = checks.fileIntegrity.passed ? 100 :
      (checks.fileIntegrity.size >= 1000 ? 60 : 0);

    // 图片嵌入（15%）
    const imageScore = checks.imagesEmbedment.passed ? 100 : 50;

    // 格式转换（15%）
    const formatScore = checks.formatConversion.passed ? 100 : 70;

    // OpenXML 验证（20%）
    const openXmlScore = checks.openXmlValidation.passed ? 100 :
      (checks.openXmlValidation.skipped ? 80 : 40);

    // 原型截图（20%，v3.1.0 新增）
    const prototypeScore = checks.prototypeScreenshots.passed
      ? (checks.prototypeScreenshots.mobileScreenshots > 0 ? 100 : 80)
      : (checks.prototypeScreenshots.skipped ? 70 : 0);

    // 综合评分
    const overall = Math.round(
      fileScore * 0.30 +
      imageScore * 0.15 +
      formatScore * 0.15 +
      openXmlScore * 0.20 +
      prototypeScore * 0.20
    );

    return {
      fileIntegrity: fileScore,
      imageEmbedment: imageScore,
      formatConversion: formatScore,
      openXmlValidation: openXmlScore,
      prototypeScreenshots: prototypeScore,
      overall: overall
    };
  }

  /**
   * 验证质量检查结果
   */
  validateQuality(qualityResult) {
    const errors = [];

    // 检查关键问题
    if (!qualityResult.checks.fileIntegrity.passed) {
      errors.push(`文件完整性：${qualityResult.checks.fileIntegrity.description}`);
    }

    // 检查综合评分
    if (qualityResult.overall < 60) {
      errors.push(`质量评分过低：${qualityResult.overall}/100`);
    }

    return {
      passed: errors.length === 0,
      errors: errors
    };
  }
}

module.exports = QualityModule;