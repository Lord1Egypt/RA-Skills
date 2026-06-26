/**
 * HTML 原型模块 v6.1.0（AI 驱动增强版）
 *
 * 重构核心：
 * - 不再用模板引擎拼接字段
 * - 不再只读 decomposition 的碎片数据
 * - AI 读 PRD 全文 + 设计系统 + UX 指南，直接生成完整 HTML 原型系统
 * - 页面结构、导航关系、跳转逻辑由 AI 根据业务逻辑自行判断
 *
 * v6.1.0: 接入 Chart.js CDN + 业务规则 JS 校验
 * v6.0.0: AI 驱动，一次生成完整原型系统
 * v5.0.0: 数据驱动渲染（已废弃）
 * v4.0.0: 多页面原型系统（已废弃）
 */

const fs = require('fs');
const path = require('path');

class PrototypeModule {
  constructor() {
    this.version = '6.1.0';
  }

  /**
   * 执行原型生成
   */
  async execute(options) {
    console.log('\n🎨 执行技能：HTML 原型生成 v6.1.0（AI 驱动增强版）');
    console.log('   读取产品上下文 → AI 生成完整原型系统（含图表+校验）...');

    const { dataBus, qualityGate, outputDir, aiExecutor } = options;

    // ========== Step 1: 读取产品上下文 ==========
    const context = await this.readProductContext(outputDir, dataBus);

    // ========== Step 2: 构建提示词 ==========
    const prompt = this.buildPrompt(context);

    // ========== Step 3: AI 生成原型 ==========
    console.log('\n   🤖 AI 生成原型系统...');
    const aiResult = await this.invokeAI(prompt, aiExecutor, outputDir);

    // ========== Step 4: 解析并写入文件 ==========
    console.log('   📝 写入 HTML 文件...');
    const pages = await this.parseAndWriteFiles(aiResult, outputDir);

    // ========== Step 5: 生成入口页 ==========
    const indexContent = this.generateIndexPage(context.productName);
    fs.writeFileSync(path.join(outputDir, 'index.html'), indexContent, 'utf8');
    pages.push({
      id: 'index',
      name: '入口页',
      type: 'index',
      htmlPath: 'index.html',
      absolutePath: path.join(outputDir, 'index.html')
    });

    // ========== 构建结果 ==========
    const result = {
      pages,
      pageCount: pages.length,
      designSystem: context.designTokens || {},
      version: this.version
    };

    const quality = {
      passed: pages.length > 0,
      pagesGenerated: pages.length
    };

    dataBus.write('prototype', result, quality, {
      fromPRD: 'prd.json',
      fromDesign: 'design.json'
    });

    if (qualityGate) {
      await qualityGate.pass('gate7_prototype', result);
    }

    console.log(`\n   ✅ 原型生成完成：${pages.length} 个页面`);

    return {
      ...result,
      quality,
      outputPath: path.join(outputDir, 'pages')
    };
  }

  /**
   * 读取产品上下文
   */
  async readProductContext(outputDir, dataBus) {
    const context = {
      productName: '',
      prdContent: '',
      designTokens: null,
      masterMd: '',
      uxGuidelines: '',
      decomposition: null
    };

    // 1. 读 PRD 全文
    const prdPath = path.join(outputDir, 'PRD.md');
    if (fs.existsSync(prdPath)) {
      context.prdContent = fs.readFileSync(prdPath, 'utf8');
      const titleMatch = context.prdContent.match(/^# (.+)$/m);
      context.productName = titleMatch ? titleMatch[1].replace(/\s*PRD.*/i, '').trim() : '产品';
      console.log(`   ✅ 读取 PRD：${context.prdContent.length} 字`);
    } else {
      // fallback: 从 dataBus 读
      const prdRecord = dataBus.read('prd');
      if (prdRecord) {
        context.prdContent = prdRecord.data.content || '';
        context.productName = prdRecord.data.productName || '产品';
        console.log(`   ✅ 从 dataBus 读取 PRD：${context.prdContent.length} 字`);
      }
    }

    // 2. 读 design tokens
    const designRecord = dataBus.read('design');
    if (designRecord) {
      context.designTokens = designRecord.data;
      console.log('   ✅ 读取设计系统 tokens');
    }

    // 3. 读 design-system/MASTER.md
    const masterPath = this.findFile(path.join(outputDir, 'design-system'), 'MASTER.md');
    if (masterPath && fs.existsSync(masterPath)) {
      context.masterMd = fs.readFileSync(masterPath, 'utf8');
      console.log(`   ✅ 读取 MASTER.md：${context.masterMd.length} 字`);
    }

    // 4. 读 UX guidelines
    const uxPath = path.join(__dirname, '../../skills/ui-ux-pro-max/data/ux-guidelines.csv');
    if (fs.existsSync(uxPath)) {
      const raw = fs.readFileSync(uxPath, 'utf8');
      context.uxGuidelines = this.extractUXGuidelines(raw);
      console.log(`   ✅ 读取 UX guidelines：${context.uxGuidelines.length} 条`);
    }

    // 5. 读 decomposition（结构化摘要）
    const decompRecord = dataBus.read('decomposition');
    if (decompRecord) {
      context.decomposition = decompRecord.data;
      console.log(`   ✅ 读取需求拆解：${(decompRecord.data.features || []).length} 个功能`);
    }

    return context;
  }

  /**
   * 提取 UX guidelines，按页面类型组织
   */
  extractUXGuidelines(csvContent) {
    const lines = csvContent.split('\n').filter(l => l.trim());
    if (lines.length < 2) return '';

    // 解析 CSV 表头
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    const categoryIdx = headers.findIndex(h => h.toLowerCase().includes('category'));
    const doIdx = headers.findIndex(h => h.toLowerCase() === 'do' || h.toLowerCase().includes('best'));
    const dontIdx = headers.findIndex(h => h.toLowerCase() === 'don\'t' || h.toLowerCase().includes('avoid'));

    if (categoryIdx === -1) return '';

    // 按类别分组
    const byCategory = {};
    for (let i = 1; i < lines.length; i++) {
      const fields = this.parseCSVLine(lines[i]);
      if (fields.length <= categoryIdx) continue;
      const cat = fields[categoryIdx] || 'General';
      if (!byCategory[cat]) byCategory[cat] = { do: [], dont: [] };
      if (doIdx >= 0 && fields[doIdx]) byCategory[cat].do.push(fields[doIdx]);
      if (dontIdx >= 0 && fields[dontIdx]) byCategory[cat].dont.push(fields[dontIdx]);
    }

    return byCategory;
  }

  parseCSVLine(line) {
    const result = [];
    let current = '';
    let inQuotes = false;
    for (const char of line) {
      if (char === '"') { inQuotes = !inQuotes; continue; }
      if (char === ',' && !inQuotes) { result.push(current.trim()); current = ''; continue; }
      current += char;
    }
    result.push(current.trim());
    return result;
  }

  /**
   * 构建 AI 提示词
   *
   * 原则：
   * - 只注入上下文，不指示页面结构
   * - 不逐字段列出输入输出（会暗示 AI 每个功能=一个表单页）
   * - 不说"每个页面一个 HTML"、"包含导航"等微观指令
   * - 唯一要求：输出可运行的 HTML 文件到指定路径
   */
  buildPrompt(context) {
    const parts = [];

    // 唯一指令
    parts.push('请基于以下产品上下文，生成可交互的 HTML 原型系统。');
    parts.push('页面结构、导航关系、跳转逻辑由你根据业务逻辑自行判断。');
    parts.push('将生成的 HTML 文件输出到指定路径。');
    parts.push('');
    parts.push('技术要求：');
    parts.push('- 使用 Chart.js CDN（https://cdn.jsdelivr.net/npm/chart.js）渲染所有图表，不要用占位符。');
    parts.push('- PRD 中的业务规则必须内化为 JS 校验逻辑（如权重之和必须等于 100%、情景数量 2-5 个、表单提交前验证等），不要只展示规则文本。');
    parts.push('- 图表数据用 PRD 中的 example 值填充，确保数字合理可信。');
    parts.push('');
    parts.push('---');
    parts.push('');

    // PRD 全文 — 业务逻辑的唯一来源
    if (context.prdContent) {
      parts.push('## 产品需求文档\n');
      parts.push(context.prdContent.substring(0, 30000));
      parts.push('');
      parts.push('---');
      parts.push('');
    }

    // 设计系统
    if (context.masterMd) {
      parts.push('## 设计规范\n');
      parts.push(context.masterMd.substring(0, 10000));
      parts.push('');
      parts.push('---');
      parts.push('');
    } else if (context.designTokens) {
      parts.push('## 设计 Tokens\n');
      parts.push('颜色：' + JSON.stringify(context.designTokens.colors || {}));
      parts.push('字体：' + JSON.stringify(context.designTokens.typography || {}));
      parts.push('间距：' + JSON.stringify(context.designTokens.spacing || {}));
      parts.push('组件：' + JSON.stringify(context.designTokens.componentSpecs || {}));
      parts.push('');
      parts.push('---');
      parts.push('');
    }

    // UX guidelines
    if (context.uxGuidelines && Object.keys(context.uxGuidelines).length > 0) {
      parts.push('## UX 最佳实践\n');
      const cats = Object.keys(context.uxGuidelines).slice(0, 8);
      for (const cat of cats) {
        const g = context.uxGuidelines[cat];
        if (g.do.length > 0 || g.dont.length > 0) {
          parts.push(`### ${cat}`);
          if (g.do.length > 0) parts.push('- Do: ' + g.do.slice(0, 3).join('; '));
          if (g.dont.length > 0) parts.push("- Don't: " + g.dont.slice(0, 3).join('; '));
          parts.push('');
        }
      }
      parts.push('---');
      parts.push('');
    }

    // decomposition：只给功能名和优先级，不给字段细节
    if (context.decomposition && context.decomposition.features) {
      parts.push('## 功能范围\n');
      for (const f of context.decomposition.features) {
        const priority = f.priority || 'P0';
        const role = f.role ? `（${f.role}）` : '';
        parts.push(`- ${f.name} ${role} [${priority}]`);
      }
      parts.push('');
    }

    return parts.join('\n');
  }

  /**
   * 调用 AI 生成原型
   */
  async invokeAI(prompt, aiExecutor, outputDir) {
    // 优先使用传入的 aiExecutor
    if (aiExecutor && typeof aiExecutor === 'function') {
      try {
        console.log('   使用 aiExecutor 调用...');
        return await aiExecutor(prompt);
      } catch (e) {
        console.warn(`   ⚠️ aiExecutor 调用失败：${e.message}，使用 fallback`);
      }
    }

    // Fallback: sessions_spawn
    try {
      console.log('   使用 sessions_spawn 调用...');
      const result = await this.sessionsSpawn(prompt);
      return result;
    } catch (e) {
      console.warn(`   ⚠️ sessions_spawn 调用失败：${e.message}`);
      return '';
    }
  }

  /**
   * 调用子代理
   */
  async sessionsSpawn(prompt) {
    // 动态导入，避免循环依赖
    const { sessions_spawn } = require('openclaw');
    return await sessions_spawn({
      runtime: 'subagent',
      mode: 'run',
      task: prompt,
      timeoutSeconds: 300 // 5 分钟，原型生成需要时间
    });
  }

  /**
   * 解析 AI 返回内容并写入文件
   */
  async parseAndWriteFiles(aiResult, outputDir) {
    const pages = [];
    const pagesDir = path.join(outputDir, 'pages');
    if (!fs.existsSync(pagesDir)) {
      fs.mkdirSync(pagesDir, { recursive: true });
    }

    // AI 可能返回多种格式：
    // 1. Markdown 代码块：```html ... ```
    // 2. 多个代码块带文件名注释
    // 3. 纯 HTML
    // 4. JSON 格式的文件映射

    const files = this.extractFilesFromAIResult(aiResult);

    for (const [filename, content] of Object.entries(files)) {
      const htmlPath = path.join(pagesDir, filename);
      fs.writeFileSync(htmlPath, content, 'utf8');

      const pageId = filename.replace('.html', '').replace(/\s+/g, '-');
      pages.push({
        id: pageId,
        name: filename.replace('.html', ''),
        type: this.inferPageType(filename),
        htmlPath: `pages/${filename}`,
        absolutePath: htmlPath
      });

      console.log(`   ✅ 写入：${filename}`);
    }

    // 如果 AI 没返回任何文件，用 fallback
    if (pages.length === 0) {
      console.warn('   ⚠️ AI 未返回有效文件，使用 fallback');
      pages.push(...this.generateFallbackPages(outputDir, pagesDir));
    }

    return pages;
  }

  /**
   * 从 AI 返回内容中提取文件
   */
  extractFilesFromAIResult(result) {
    const files = {};

    if (!result || typeof result !== 'string') return files;

    // 模式 1: Markdown 代码块带文件名注释
    // <!-- file: home.html -->
    // ```html
    // ...
    // ```
    const fileBlockRegex = /<!--\s*file:\s*(.+?)\s*-->\s*```(?:html)?\s*([\s\S]*?)```/gi;
    let match;
    while ((match = fileBlockRegex.exec(result)) !== null) {
      files[match[1].trim()] = match[2].trim();
    }

    // 模式 2: JSON 格式
    if (Object.keys(files).length === 0) {
      try {
        // 尝试提取 JSON
        const jsonMatch = result.match(/\{[\s\S]*"files"[\s\S]*\}/);
        if (jsonMatch) {
          const json = JSON.parse(jsonMatch[0]);
          if (json.files && typeof json.files === 'object') {
            for (const [filename, content] of Object.entries(json.files)) {
              files[filename] = content;
            }
          }
        }
      } catch (e) {
        // 不是 JSON，忽略
      }
    }

    // 模式 3: 单个 HTML 文件
    if (Object.keys(files).length === 0) {
      const htmlMatch = result.match(/```(?:html)?\s*([\s\S]*?)```/);
      if (htmlMatch) {
        files['home.html'] = htmlMatch[1].trim();
      } else if (result.includes('<!DOCTYPE html') || result.includes('<html')) {
        files['home.html'] = result;
      }
    }

    return files;
  }

  /**
   * 推断页面类型
   */
  inferPageType(filename) {
    const name = filename.toLowerCase();
    if (name.includes('home') || name.includes('index')) return 'landing';
    if (name.includes('login') || name.includes('auth')) return 'login';
    if (name.includes('list') || name.includes('列表')) return 'list';
    if (name.includes('form') || name.includes('表单')) return 'form';
    if (name.includes('detail') || name.includes('详情')) return 'detail';
    if (name.includes('dashboard') || name.includes('看板')) return 'dashboard';
    return 'custom';
  }

  /**
   * Fallback 页面生成
   */
  generateFallbackPages(outputDir, pagesDir) {
    const pages = [];

    // 如果连 AI 调用都失败，至少生成一个入口页
    const content = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型占位</title>
  <style>body{font-family:system-ui;padding:40px;text-align:center;color:#666}</style>
</head>
<body>
  <h1>原型生成失败</h1>
  <p>AI 调用未返回有效结果，请检查 AI 执行器配置。</p>
</body>
</html>`;

    const path = require('path');
    const fallbackPath = path.join(pagesDir, 'fallback.html');
    fs.writeFileSync(fallbackPath, content, 'utf8');

    pages.push({
      id: 'fallback',
      name: '占位页',
      type: 'custom',
      htmlPath: 'pages/fallback.html',
      absolutePath: fallbackPath
    });

    return pages;
  }

  /**
   * 查找文件（递归）
   */
  findFile(dir, filename) {
    if (!fs.existsSync(dir)) return null;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name === filename) return path.join(dir, filename);
      if (entry.isDirectory()) {
        const found = this.findFile(path.join(dir, entry.name), filename);
        if (found) return found;
      }
    }
    return null;
  }

  /**
   * 生成入口页
   */
  generateIndexPage(productName) {
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url=pages/home.html">
  <title>${productName}</title>
</head>
<body>
  <p>正在跳转... <a href="pages/home.html">点击这里</a></p>
</body>
</html>`;
  }
}

module.exports = PrototypeModule;
