#!/usr/bin/env node

/**
 * OpenMAIC课程PPT导出脚本
 * 
 * 使用方法：
 * node export_ppt.js <课程ID或标题> [--openmaic-path <路径>] [--no-notes]
 * 
 * 示例：
 * node export_ppt.js LLFqDUArdk
 * node export_ppt.js "什么是 MCP 协议？"
 * node export_ppt.js LLFqDUArdk --openmaic-path /path/to/OpenMAIC
 * node export_ppt.js LLFqDUArdk --no-notes
 */

const fs = require('fs');
const path = require('path');

// 默认配置 - 动态获取OpenClaw目录
function getDefaultOpenMAICPath() {
  // 方法1：从环境变量获取
  if (process.env.OPENCLAW_HOME) {
    return path.join(process.env.OPENCLAW_HOME, 'workspace', 'OpenMAIC');
  }
  
  // 方法2：用户主目录下的.openclaw/workspace/OpenMAIC（最常见的位置）
  const homeDir = process.env.HOME || process.env.USERPROFILE;
  if (homeDir) {
    const workspaceOpenMAIC = path.join(homeDir, '.openclaw', 'workspace', 'OpenMAIC');
    if (fs.existsSync(workspaceOpenMAIC) && fs.statSync(workspaceOpenMAIC).isDirectory()) {
      return workspaceOpenMAIC;
    }
  }
  
  // 方法3：从当前工作目录向上查找
  let currentDir = process.cwd();
  const maxDepth = 10;
  
  for (let depth = 0; depth < maxDepth; depth++) {
    // 检查当前目录是否有OpenMAIC文件夹
    const openmaicPath = path.join(currentDir, 'OpenMAIC');
    if (fs.existsSync(openmaicPath) && fs.statSync(openmaicPath).isDirectory()) {
      return openmaicPath;
    }
    
    // 检查当前目录是否有.openclaw/workspace文件夹
    const openclawWorkspacePath = path.join(currentDir, '.openclaw', 'workspace');
    if (fs.existsSync(openclawWorkspacePath) && fs.statSync(openclawWorkspacePath).isDirectory()) {
      const openmaicInWorkspace = path.join(openclawWorkspacePath, 'OpenMAIC');
      if (fs.existsSync(openmaicInWorkspace) && fs.statSync(openmaicInWorkspace).isDirectory()) {
        return openmaicInWorkspace;
      }
    }
    
    // 向上移动一级
    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      break; // 到达根目录
    }
    currentDir = parentDir;
  }
  
  // 方法4：最终回退路径
  return '/path/to/your/OpenMAIC';
}

let OPENMAIC_PATH = getDefaultOpenMAICPath();

// 命令行参数解析
const args = process.argv.slice(2);
let courseIdentifier = null;
let includeNotes = true;

// 解析参数
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  
  if (arg === '--openmaic-path') {
    if (i + 1 < args.length) {
      OPENMAIC_PATH = args[i + 1];
      i++; // 跳过下一个参数
    } else {
      console.error('错误：--openmaic-path 参数需要指定路径');
      process.exit(1);
    }
  } else if (arg === '--no-notes') {
    includeNotes = false;
  } else if (!courseIdentifier) {
    courseIdentifier = arg;
  }
}

if (!courseIdentifier) {
  console.error('错误：请提供课程ID或标题');
  console.error('使用方法：node export_ppt.js <课程ID或标题> [--openmaic-path <路径>] [--no-notes]');
  process.exit(1);
}

// 显示OpenMAIC路径信息
console.log(`📁 使用的OpenMAIC路径: ${OPENMAIC_PATH}`);
if (!fs.existsSync(OPENMAIC_PATH)) {
  console.warn(`⚠️  警告：OpenMAIC路径不存在: ${OPENMAIC_PATH}`);
  console.warn(`   请使用 --openmaic-path 参数指定正确的路径`);
}

const CLASSROOMS_PATH = path.join(OPENMAIC_PATH, 'data/classrooms');

// 动态加载OpenMAIC中的pptxgenjs
const pptxgenPath = path.join(OPENMAIC_PATH, 'packages/pptxgenjs/dist/pptxgen.cjs.js');
let pptxgen;
try {
  pptxgen = require(pptxgenPath);
} catch (error) {
  console.error('错误：无法加载pptxgenjs，请确保OpenMAIC已正确安装');
  console.error('错误详情：', error.message);
  process.exit(1);
}

// 辅助函数：查找课程文件
function findCourseFile(identifier) {
  // 首先检查是否是直接的文件名
  const directPath = path.join(CLASSROOMS_PATH, `${identifier}.json`);
  if (fs.existsSync(directPath)) {
    return directPath;
  }
  
  // 如果不是，搜索所有课程文件
  const files = fs.readdirSync(CLASSROOMS_PATH);
  for (const file of files) {
    if (file.endsWith('.json')) {
      const filePath = path.join(CLASSROOMS_PATH, file);
      try {
        const content = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(content);
        
        // 检查课程标题是否匹配
        if (data.stage && data.stage.name === identifier) {
          return filePath;
        }
        
        // 检查课程ID是否匹配（文件名去掉.json）
        const courseId = file.replace('.json', '');
        if (courseId === identifier) {
          return filePath;
        }
      } catch (err) {
        console.warn(`警告：无法解析文件 ${file}:`, err.message);
      }
    }
  }
  
  return null;
}

// 辅助函数：格式化颜色
function formatColor(color) {
  if (!color) return { alpha: 0, color: '#000000' };
  
  if (color.startsWith('#')) {
    return { alpha: 1, color: color };
  }
  
  if (color.startsWith('rgba')) {
    const match = color.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/);
    if (match) {
      const r = parseInt(match[1]);
      const g = parseInt(match[2]);
      const b = parseInt(match[3]);
      const alpha = parseFloat(match[4]);
      const hexColor = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
      return { alpha, color: hexColor };
    }
  }
  
  if (color.startsWith('rgb')) {
    const match = color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (match) {
      const r = parseInt(match[1]);
      const g = parseInt(match[2]);
      const b = parseInt(match[3]);
      const hexColor = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
      return { alpha: 1, color: hexColor };
    }
  }
  
  return { alpha: 1, color: '#000000' };
}

// 辅助函数：提取HTML中的纯文本
function extractTextFromHTML(html) {
  if (!html) return '';
  
  return html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]*>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

// 辅助函数：提取样式信息
function extractStyleFromHTML(html) {
  const style = {
    fontSize: 14,
    color: '#333333',
    align: 'left',
    bold: false,
    italic: false
  };
  
  if (!html) return style;
  
  const fontSizeMatch = html.match(/font-size:\s*(\d+)px/);
  if (fontSizeMatch) {
    style.fontSize = parseInt(fontSizeMatch[1]);
  }
  
  const colorMatch = html.match(/color:\s*(#[0-9a-fA-F]+|rgb\([^)]+\)|rgba\([^)]+\))/);
  if (colorMatch) {
    style.color = colorMatch[1];
  }
  
  const alignMatch = html.match(/text-align:\s*(\w+)/);
  if (alignMatch) {
    style.align = alignMatch[1];
  }
  
  style.bold = html.includes('<strong>') || html.includes('font-weight: bold');
  style.italic = html.includes('<em>') || html.includes('<i>') || html.includes('font-style: italic');
  
  return style;
}

// 主函数
async function exportCoursePPT(courseFilePath) {
  try {
    // 读取课程数据
    const courseData = JSON.parse(fs.readFileSync(courseFilePath, 'utf8'));
    const courseId = path.basename(courseFilePath, '.json');
    const courseName = courseData.stage.name;
    
    console.log(`📚 课程: ${courseName}`);
    console.log(`📋 ID: ${courseId}`);
    console.log(`🎬 场景数量: ${courseData.scenes.length}`);
    
    // 提取幻灯片数据和对应的讲稿
    const slideScenes = courseData.scenes.filter(scene => scene.content.type === 'slide');
    const slides = slideScenes.map(scene => scene.content.canvas);
    
    // 提取每个场景的讲稿
    const sceneSpeeches = slideScenes.map(scene => {
      const speeches = [];
      if (scene.actions) {
        scene.actions.forEach(action => {
          if (action.type === 'speech' && action.text) {
            speeches.push(action.text);
          }
        });
      }
      return speeches;
    });
    
    console.log(`📊 幻灯片数量: ${slides.length}`);
    console.log(`🗣️  讲稿数量: ${sceneSpeeches.reduce((sum, s) => sum + s.length, 0)}`);
    if (!includeNotes) {
      console.log(`⚠️  讲稿导出已禁用 (使用 --no-notes 参数)`);
    }
    
    // 创建PPT
    const pptx = new pptxgen();
    
    // 设置PPT属性
    pptx.author = 'OpenMAIC';
    pptx.company = 'OpenMAIC';
    pptx.revision = '1';
    pptx.subject = courseName;
    pptx.title = courseName;
    
    // 设置布局
    const firstSlide = slides[0];
    if (firstSlide) {
      const viewportRatio = firstSlide.viewportRatio || 0.5625;
      if (viewportRatio === 0.625) pptx.layout = 'LAYOUT_16x10';
      else if (viewportRatio === 0.75) pptx.layout = 'LAYOUT_4x3';
      else pptx.layout = 'LAYOUT_16x9';
    }
    
    // 转换比例
    const ratioPx2Inch = 96 * (firstSlide.viewportSize / 960);
    const ratioPx2Pt = (96 / 72) * (firstSlide.viewportSize / 960);
    
    console.log(`📐 转换比例 - px转inch: ${ratioPx2Inch}, px转pt: ${ratioPx2Pt}`);
    
    // 为每个幻灯片创建页面
    slides.forEach((slide, slideIndex) => {
      const pptxSlide = pptx.addSlide();
      const scene = slideScenes[slideIndex];
      const speeches = sceneSpeeches[slideIndex];
      
      console.log(`\n📄 处理幻灯片 ${slideIndex + 1}: ${scene?.title || '无标题'}`);
      console.log(`  元素数量: ${slide.elements?.length || 0}`);
      
      // 设置幻灯片备注（讲稿）
      if (includeNotes && speeches.length > 0) {
        const notesText = speeches.join('\n\n');
        pptxSlide.addNotes(notesText);
        console.log(`  添加讲稿: ${speeches.length} 条`);
      }
      
      // 设置幻灯片背景
      if (slide.theme && slide.theme.backgroundColor) {
        const bgColor = formatColor(slide.theme.backgroundColor);
        pptxSlide.background = {
          color: bgColor.color,
          transparency: (1 - bgColor.alpha) * 100
        };
      }
      
      // 按z-index排序（假设后出现的元素在上层）
      const elements = slide.elements || [];
      
      // 处理每个元素
      elements.forEach((element, elementIndex) => {
        try {
          // 计算位置（转换为英寸）
          const x = element.left / ratioPx2Inch;
          const y = element.top / ratioPx2Inch;
          const w = element.width / ratioPx2Inch;
          const h = element.height / ratioPx2Inch;
          
          // ── SHAPE 元素 ──
          if (element.type === 'shape') {
            // 创建矩形形状
            const shapeOptions = {
              x: x,
              y: y,
              w: w,
              h: h,
              fill: { color: 'FFFFFF', transparency: 100 },
              line: false
            };
            
            // 设置填充颜色
            if (element.fill) {
              const fillColor = formatColor(element.fill);
              shapeOptions.fill = {
                color: fillColor.color.replace('#', ''),
                transparency: (1 - fillColor.alpha) * 100
              };
            }
            
            // 设置边框 - 只有有outline属性时才添加边框
            if (element.outline) {
              const outlineColor = formatColor(element.outline.color || '#000000');
              shapeOptions.line = {
                color: outlineColor.color.replace('#', ''),
                transparency: (1 - outlineColor.alpha) * 100,
                width: (element.outline.width || 1) / ratioPx2Pt
              };
            }
            
            pptxSlide.addShape('rect', shapeOptions);
          }
          
          // ── TEXT 元素 ──
          else if (element.type === 'text') {
            const textContent = extractTextFromHTML(element.content);
            if (!textContent.trim()) return;
            
            const style = extractStyleFromHTML(element.content);
            
            const textOptions = {
              x: x,
              y: y,
              w: w,
              h: h,
              fontSize: style.fontSize / ratioPx2Pt,
              align: style.align,
              bold: style.bold,
              italic: style.italic,
              color: style.color.replace('#', ''),
              fontFace: element.defaultFontName || 'Microsoft YaHei',
              valign: 'middle'
            };
            
            // 设置文本颜色
            if (element.defaultColor) {
              const textColor = formatColor(element.defaultColor);
              textOptions.color = textColor.color.replace('#', '');
            }
            
            // 设置文本背景色（如果有fill属性）
            if (element.fill) {
              const fillColor = formatColor(element.fill);
              textOptions.fill = {
                color: fillColor.color.replace('#', ''),
                transparency: (1 - fillColor.alpha) * 100
              };
            }
            
            pptxSlide.addText(textContent, textOptions);
          }
          
          // ── LINE 元素 ──
          else if (element.type === 'line') {
            // 创建简单的线条
            const lineOptions = {
              x: x,
              y: y,
              w: w,
              h: 0.05,
              fill: { color: '000000' },
              line: false
            };
            
            if (element.color) {
              const lineColor = formatColor(element.color);
              lineOptions.fill.color = lineColor.color.replace('#', '');
            }
            
            pptxSlide.addShape('rect', lineOptions);
          }
          
        } catch (err) {
          console.error(`  处理元素 ${elementIndex} 时出错:`, err.message);
        }
      });
    });
    
    // 生成文件名
    const safeCourseName = courseName.replace(/[<>:"/\\|?*]/g, '_');
    const outputFileName = `${safeCourseName}_${Date.now()}.pptx`;
    
    // 优先保存到用户指定的工作目录，如果没有则保存到workspace目录
    const workspacePath = path.join(process.env.HOME, '.openclaw/workspace');
    const outputPath = path.join(workspacePath, outputFileName);
    
    // 保存PPT文件
    console.log(`\n💾 正在生成PPT文件: ${outputFileName}`);
    console.log(`📁 保存到: ${outputPath}`);
    await pptx.writeFile({ fileName: outputPath });
    
    const fileStats = fs.statSync(outputPath);
    console.log(`✅ PPT文件已生成: ${outputPath}`);
    console.log(`📦 文件大小: ${(fileStats.size / 1024).toFixed(2)} KB`);
    
    return {
      success: true,
      courseName,
      courseId,
      slideCount: slides.length,
      speechCount: sceneSpeeches.reduce((sum, s) => sum + s.length, 0),
      outputPath,
      fileSize: fileStats.size
    };
    
  } catch (error) {
    console.error('❌ 导出失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

// 主程序
async function main() {
  console.log('🚀 OpenMAIC课程PPT导出工具');
  console.log('='.repeat(50));
  
  // 检查OpenMAIC目录
  if (!fs.existsSync(OPENMAIC_PATH)) {
    console.error(`❌ OpenMAIC目录不存在: ${OPENMAIC_PATH}`);
    console.error('请先安装OpenMAIC或检查路径配置');
    process.exit(1);
  }
  
  if (!fs.existsSync(CLASSROOMS_PATH)) {
    console.error(`❌ 课程目录不存在: ${CLASSROOMS_PATH}`);
    console.error('请检查OpenMAIC安装');
    process.exit(1);
  }
  
  // 查找课程文件
  console.log(`🔍 查找课程: "${courseIdentifier}"`);
  const courseFilePath = findCourseFile(courseIdentifier);
  
  if (!courseFilePath) {
    console.error(`❌ 未找到课程: "${courseIdentifier}"`);
    console.error('请检查课程ID或标题是否正确');
    process.exit(1);
  }
  
  console.log(`📁 找到课程文件: ${courseFilePath}`);
  
  // 导出PPT
  const result = await exportCoursePPT(courseFilePath);
  
  if (result.success) {
    console.log('\n🎉 导出完成！');
    console.log('='.repeat(50));
    console.log(`课程: ${result.courseName}`);
    console.log(`ID: ${result.courseId}`);
    console.log(`幻灯片: ${result.slideCount} 页`);
    console.log(`讲稿: ${result.speechCount} 条`);
    console.log(`文件: ${result.outputPath}`);
    console.log(`大小: ${(result.fileSize / 1024).toFixed(2)} KB`);
  } else {
    console.error('\n❌ 导出失败！');
    process.exit(1);
  }
}

// 运行主程序
main().catch(error => {
  console.error('❌ 程序执行失败:', error);
  process.exit(1);
});