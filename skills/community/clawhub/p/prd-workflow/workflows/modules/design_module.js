/**
 * UI/UX 设计模块 v3.0.0
 * 
 * 调用 ui-ux-pro-max 生成完整设计系统，并持久化到输出目录
 * 生成 MASTER.md + 页面级 overrides 供 prototype_module 使用
 * 
 * v3.0.0: 持久化设计系统到 design-system/ 目录，供下游模块读取
 * v2.5.0: 生成设计系统 tokens
 */

const fs = require('fs');
const path = require('path');

class DesignModule {
  /**
   * 执行 UI/UX 设计
   */
  async execute(options) {
    console.log('\n🎨 执行技能：UI/UX 设计 v3.0.0');
    
    const { dataBus, qualityGate, outputDir } = options;
    
    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }
    
    const prd = prdRecord.data;
    
    // 调用 ui-ux-pro-max 生成完整设计系统（持久化）
    console.log('   调用 ui-ux-pro-max 生成设计系统...');
    const designResult = await this.generateDesignSystem(prd, outputDir);
    
    // 质量验证
    const quality = this.validateDesign(designResult);
    
    // 写入数据总线
    const filepath = dataBus.write('design', designResult, quality, {
      fromPRD: 'prd.json'
    });
    
    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate6_design', designResult);
    }
    
    return {
      ...designResult,
      quality: quality,
      outputPath: filepath
    };
  }
  
  /**
   * 调用 ui-ux-pro-max 生成设计系统（v3.0.0 持久化版）
   * 
   * 生成并持久化完整设计系统到 design-system/ 目录：
   * - design-system/<project>/MASTER.md（全局规则）
   * - design-system/<project>/pages/<page>.md（页面级覆盖）
   * - design-system/<project>/tokens.json（结构化 tokens）
   */
  async generateDesignSystem(prd, outputDir) {
    const { execSync } = require('child_process');
    
    // ui-ux-pro-max 脚本路径
    const designSystemPath = path.join(__dirname, '../../skills/ui-ux-pro-max/scripts/design_system.py');
    
    // 检查脚本是否存在
    if (!fs.existsSync(designSystemPath)) {
      console.warn('⚠️  ui-ux-pro-max 脚本不存在，使用备用方案');
      return this.generateFallbackDesign(prd);
    }
    
    // 从 PRD 提取产品类型和产品名称
    const content = prd.content || '';
    const productType = this.extractProductType(content);
    const projectName = this.extractProductName(content);
    
    console.log(`   调用 ui-ux-pro-max：产品类型="${productType}", 项目="${projectName}"`);
    
    try {
      // 设计系统输出目录
      const designDir = path.join(outputDir, 'design-system');
      if (!fs.existsSync(designDir)) {
        fs.mkdirSync(designDir, { recursive: true });
      }

      // Step 1: 用 markdown 格式获取设计系统推荐
      const mdResult = execSync(
        `python3 "${designSystemPath}" "${productType}" --project-name "${projectName}" --format markdown`,
        { encoding: 'utf8', stdio: 'pipe' }
      );

      // Step 2: 用 persist 模式生成完整设计系统文件
      const persistResult = execSync(
        `python3 -c "
import sys; sys.path.insert(0, '${path.dirname(designSystemPath)}')
from design_system import generate_design_system
result = generate_design_system('${productType}', project_name='${projectName}', output_format='ascii', persist=True, output_dir='${outputDir}')
import json; print(json.dumps(result))
"`,
        { encoding: 'utf8', stdio: 'pipe' }
      );

      // Step 3: 解析结构化结果
      const persistInfo = JSON.parse(persistResult);
      
      // Step 4: 解析 markdown 输出为结构化 tokens
      const tokens = this.parseMarkdownToTokens(mdResult, productType);
      
      // Step 5: 保存结构化 tokens JSON（供 prototype_module 直接读取）
      const tokensPath = path.join(designDir, projectName.toLowerCase().replace(/[^a-z0-9]/g, '-'), 'tokens.json');
      const tokensDir = path.dirname(tokensPath);
      if (!fs.existsSync(tokensDir)) {
        fs.mkdirSync(tokensDir, { recursive: true });
      }
      fs.writeFileSync(tokensPath, JSON.stringify(tokens, null, 2), 'utf8');

      console.log('   ✅ 设计系统生成成功');
      console.log(`   📁 输出目录：${persistInfo.design_system_dir || designDir}`);
      console.log(`   📄 生成文件：${(persistInfo.created_files || []).length} 个`);
      
      return {
        ...tokens,
        rawMarkdown: mdResult,
        designSystemDir: persistInfo.design_system_dir || designDir,
        createdFiles: persistInfo.created_files || [],
        masterMdPath: this.findMasterMd(designDir, projectName),
        tokensJsonPath: tokensPath
      };
      
    } catch (error) {
      console.warn('⚠️  ui-ux-pro-max 调用失败，使用备用方案');
      console.warn('   错误:', error.message);
      return this.generateFallbackDesign(prd);
    }
  }
  
  /**
   * 备用设计系统生成（当 ui-ux-pro-max 不可用时）
   */
  generateFallbackDesign(prd) {
    const content = prd.content || '';

    let primaryColor = '#1890FF';
    if (content.includes('金融') || content.includes('养老')) {
      primaryColor = '#1677FF';
    } else if (content.includes('电商')) {
      primaryColor = '#FF6B35';
    }

    return {
      colors: {
        primary: primaryColor,
        success: '#52C41A',
        warning: '#FAAD14',
        error: '#F5222D',
        neutral: ['#000000', '#595959', '#8C8C8C', '#BFBFBF', '#D9D9D9', '#F0F0F0', '#FAFAFA']
      },
      typography: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial',
        fontSizes: [12, 14, 16, 18, 20, 24, 30, 36, 48],
        lineHeights: [1.5, 1.6, 1.8]
      },
      spacing: {
        unit: 8,
        scale: [0, 4, 8, 12, 16, 24, 32, 48, 64, 80, 96]
      },
      components: {
        button: {
          height: 32,
          padding: '0 16px',
          borderRadius: 4
        },
        input: {
          height: 32,
          padding: '4px 11px',
          borderRadius: 4
        }
      }
    };
  }

  /**
   * 从 markdown 解析为结构化 design tokens
   */
  parseMarkdownToTokens(markdown, productType) {
    // 从表格格式提取颜色（按 Role 映射）
    const colors = this.extractColorsFromTable(markdown);
    
    // 提取字体
    const headingFont = this.extractFont(markdown, 'Heading') || 'Inter';
    const bodyFont = this.extractFont(markdown, 'Body') || headingFont;
    
    // 提取样式名称
    const styleMatch = markdown.match(/\*\*Name:\*\*\s*(.+?)\n/);
    const styleName = styleMatch ? styleMatch[1].trim() : 'Minimalism';
    
    // 提取效果
    const effectsMatch = markdown.match(/### Key Effects\n([\s\S]*?)(?=###|$)/);
    const keyEffects = effectsMatch ? effectsMatch[1].trim() : '';
    
    // 提取反模式
    const antiMatch = markdown.match(/### Avoid[\s\S]*?\n([\s\S]*?)(?=###|$)/);
    const antiPatterns = antiMatch ? antiMatch[1].trim() : '';

    return {
      style: {
        name: styleName,
        effects: keyEffects,
        antiPatterns: antiPatterns
      },
      colors: {
        ...colors,
        success: '#22C55E',
        warning: '#F59E0B',
        error: '#EF4444',
        muted: '#94A3B8'
      },
      typography: {
        headingFont: headingFont,
        bodyFont: bodyFont,
        fontFamily: `"${headingFont}", "${bodyFont}", system-ui, -apple-system, sans-serif`,
        fontSizes: [12, 14, 16, 18, 20, 24, 30, 36, 48]
      },
      spacing: {
        unit: 8,
        scale: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32, '2xl': 48, '3xl': 64 }
      },
      shadow: {
        sm: '0 1px 2px rgba(0,0,0,0.05)',
        md: '0 4px 6px rgba(0,0,0,0.1)',
        lg: '0 10px 15px rgba(0,0,0,0.1)',
        xl: '0 20px 25px rgba(0,0,0,0.15)'
      },
      componentSpecs: {
        button: {
          borderRadius: 8,
          padding: '12px 24px',
          fontWeight: 600,
          transition: 'all 200ms ease'
        },
        card: {
          borderRadius: 12,
          padding: 24,
          shadow: 'var(--shadow-md)'
        },
        input: {
          borderRadius: 8,
          padding: '12px 16px',
          fontSize: 16
        }
      },
      checklist: [
        'No emojis as icons (use SVG: Heroicons/Lucide)',
        'cursor-pointer on all clickable elements',
        'Hover states with smooth transitions (150-300ms)',
        'Light mode: text contrast 4.5:1 minimum',
        'Focus states visible for keyboard nav',
        'prefers-reduced-motion respected',
        'Responsive: 375px, 768px, 1024px, 1440px'
      ]
    };
  }

  /**
   * 从 markdown 表格提取颜色（按 Role 映射）
   */
  extractColorsFromTable(markdown) {
    const defaults = {
      primary: '#2563EB', secondary: '#3B82F6', cta: '#F97316',
      background: '#F8FAFC', text: '#1E293B'
    };
    
    // 查找 Colors 表格
    const colorSection = markdown.match(/### Colors\n([\s\S]*?)(?=###|$)/);
    if (!colorSection) return defaults;
    
    const section = colorSection[1];
    const colors = { ...defaults };
    
    // 匹配表格行：| Role | #HEX |
    const rowPattern = /\|\s*(Primary|Secondary|CTA|Background|Text)\s*\|\s*(#[0-9A-Fa-f]{6})\s*\|/g;
    let match;
    while ((match = rowPattern.exec(section)) !== null) {
      const role = match[1].toLowerCase();
      const hex = match[2];
      if (role === 'primary') colors.primary = hex;
      else if (role === 'secondary') colors.secondary = hex;
      else if (role === 'cta') colors.cta = hex;
      else if (role === 'background') colors.background = hex;
      else if (role === 'text') colors.text = hex;
    }
    
    return colors;
  }

  /**
   * 从 markdown 提取字体名称
   */
  extractFont(markdown, role) {
    const pattern = new RegExp(`\\*\\*${role}.*?Font:\\*\\*\\s*(.+?)\\n`, 'i');
    const match = markdown.match(pattern);
    return match ? match[1].trim() : null;
  }

  /**
   * 查找 MASTER.md 路径
   */
  findMasterMd(designDir, projectName) {
    const projectSlug = projectName.toLowerCase().replace(/[^a-z0-9]/g, '-');
    const candidate = path.join(designDir, projectSlug, 'MASTER.md');
    if (fs.existsSync(candidate)) return candidate;
    
    // 搜索子目录
    try {
      const subdirs = fs.readdirSync(designDir, { withFileTypes: true })
        .filter(d => d.isDirectory())
        .map(d => d.name);
      for (const subdir of subdirs) {
        const p = path.join(designDir, subdir, 'MASTER.md');
        if (fs.existsSync(p)) return p;
      }
    } catch {}
    
    return null;
  }

  /**
   * 从 PRD 提取产品类型
   */
  extractProductType(content) {
    if (content.includes('金融') || content.includes('养老') || content.includes('理财')) {
      return 'financial';
    }
    if (content.includes('电商') || content.includes('购物')) {
      return 'ecommerce';
    }
    if (content.includes('社交') || content.includes('社区')) {
      return 'social';
    }
    return 'default';
  }

  /**
   * 从 PRD 提取产品名称
   */
  extractProductName(content) {
    const match = content.match(/^#\s+(.+)$/m);
    if (match) {
      return match[1].trim();
    }
    return '产品';
  }

  /**
   * 验证设计系统
   */
  async validateDesign(designResult) {
    const errors = [];
    
    // 检查颜色
    if (!designResult.colors || !designResult.colors.primary) {
      errors.push('缺少主色调');
    }
    
    // 检查字体
    if (!designResult.typography || !designResult.typography.fontFamily) {
      errors.push('缺少字体配置');
    }
    
    // 检查间距
    if (!designResult.spacing || !designResult.spacing.unit) {
      errors.push('缺少间距单位');
    }
    
    return {
      passed: errors.length === 0,
      errors: errors,
      tokensComplete: errors.length === 0
    };
  }
}

module.exports = DesignModule;
