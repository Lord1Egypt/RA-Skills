#!/usr/bin/env node

/**
 * PRD 验证脚本
 * 检查PRD文档的完整性、一致性和质量
 *
 * 用法: node validate.js [项目目录]
 * 默认检查当前目录
 */

const fs = require('fs');
const path = require('path');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 验证结果收集
const results = {
  passed: [],
  warnings: [],
  errors: [],
};

function pass(message) {
  results.passed.push(message);
  log(`  ✅ ${message}`, 'green');
}

function warn(message) {
  results.warnings.push(message);
  log(`  ⚠️  ${message}`, 'yellow');
}

function error(message) {
  results.errors.push(message);
  log(`  ❌ ${message}`, 'red');
}

// 主验证函数
async function validate(projectDir = '.') {
  log('\n📋 PRD 文档验证\n', 'cyan');
  log(`项目目录: ${path.resolve(projectDir)}\n`, 'blue');

  const fragmentsDir = path.join(projectDir, 'fragments');
  const versionFile = path.join(projectDir, 'version.json');

  // 1. 检查基本结构
  log('1. 检查基本结构...', 'blue');
  await checkBasicStructure(projectDir, fragmentsDir, versionFile);

  // 2. 检查章节完整性
  log('\n2. 检查章节完整性...', 'blue');
  await checkChapterCompleteness(fragmentsDir);

  // 3. 检查版本信息
  log('\n3. 检查版本信息...', 'blue');
  await checkVersionInfo(versionFile);

  // 4. 检查内容质量
  log('\n4. 检查内容质量...', 'blue');
  await checkContentQuality(fragmentsDir);

  // 5. 检查一致性
  log('\n5. 检查一致性...', 'blue');
  await checkConsistency(fragmentsDir);

  // 输出总结
  printSummary();

  // 返回退出码
  return results.errors.length === 0 ? 0 : 1;
}

// 检查基本结构
async function checkBasicStructure(projectDir, fragmentsDir, versionFile) {
  // 检查 fragments 目录
  if (!fs.existsSync(fragmentsDir)) {
    error('fragments/ 目录不存在');
    return;
  }
  pass('fragments/ 目录存在');

  // 检查 version.json
  if (!fs.existsSync(versionFile)) {
    warn('version.json 不存在，将使用默认配置');
  } else {
    pass('version.json 存在');
  }

  // 检查关键脚本
  const buildJs = path.join(projectDir, 'build.js');
  if (fs.existsSync(buildJs)) {
    pass('build.js 存在');
  } else {
    warn('build.js 不存在');
  }
}

// 检查章节完整性
async function checkChapterCompleteness(fragmentsDir) {
  const requiredChapters = [
    '00-cover.html',
    '01-toc.html',
    '02-overview.html',
    '03-requirements.html',
  ];

  const optionalChapters = [
    '04-user-stories.html',
    '05-functional.html',
    '06-interaction.html',
    '07-data.html',
    '08-nonfunctional.html',
    '09-market.html',
    '10-architecture.html',
    '11-prototype.html',
    '12-tech.html',
    '13-testing.html',
    '14-operation.html',
    '15-project-plan.html',
    '99-backpage.html',
  ];

  const existingFiles = fs.readdirSync(fragmentsDir).filter(f => f.endsWith('.html'));

  // 检查必需章节
  for (const chapter of requiredChapters) {
    const filePath = path.join(fragmentsDir, chapter);
    if (fs.existsSync(filePath)) {
      pass(`${chapter} 存在`);
    } else {
      error(`${chapter} 缺失（必需章节）`);
    }
  }

  // 检查可选章节
  let optionalCount = 0;
  for (const chapter of optionalChapters) {
    const filePath = path.join(fragmentsDir, chapter);
    if (fs.existsSync(filePath)) {
      optionalCount++;
    }
  }

  if (optionalCount > 0) {
    pass(`可选章节: ${optionalCount}/${optionalChapters.length} 个已填充`);
  }

  // 统计总完成度
  const totalChapters = requiredChapters.length + optionalChapters.length;
  const completedChapters = requiredChapters.filter(c =>
    fs.existsSync(path.join(fragmentsDir, c))
  ).length + optionalCount;

  const completionRate = Math.round((completedChapters / totalChapters) * 100);
  log(`\n  文档完成度: ${completionRate}% (${completedChapters}/${totalChapters})`, 'cyan');
}

// 检查版本信息
async function checkVersionInfo(versionFile) {
  if (!fs.existsSync(versionFile)) {
    return;
  }

  try {
    const content = fs.readFileSync(versionFile, 'utf-8');
    const version = JSON.parse(content);

    // 检查必需字段
    if (!version.title) {
      error('version.json 缺少 title 字段');
    } else {
      pass(`产品名称: ${version.title}`);
    }

    if (!version.version) {
      error('version.json 缺少 version 字段');
    } else {
      // 验证版本号格式
      const versionRegex = /^\d+\.\d+\.\d+$/;
      if (versionRegex.test(version.version)) {
        pass(`版本号: ${version.version}`);
      } else {
        warn(`版本号格式不规范: ${version.version}，建议使用 x.x.x 格式`);
      }
    }

    if (!version.lastUpdate) {
      warn('version.json 缺少 lastUpdate 字段');
    } else {
      pass(`最后更新: ${version.lastUpdate}`);
    }

  } catch (e) {
    error(`version.json 解析失败: ${e.message}`);
  }
}

// 检查内容质量
async function checkContentQuality(fragmentsDir) {
  const files = fs.readdirSync(fragmentsDir).filter(f => f.endsWith('.html'));

  let totalWordCount = 0;
  let hasMermaidDiagram = false;
  let hasTables = false;

  for (const file of files) {
    const filePath = path.join(fragmentsDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');

    // 统计字数
    const textContent = content.replace(/<[^>]+>/g, '');
    const wordCount = textContent.length;
    totalWordCount += wordCount;

    // 检查是否有流程图
    if (content.includes('class="mermaid"') || content.includes('mermaid')) {
      hasMermaidDiagram = true;
    }

    // 检查是否有表格
    if (content.includes('<table')) {
      hasTables = true;
    }

    // 检查是否有 TODO/占位符
    const placeholders = content.match(/【[^】]+】/g) || [];
    if (placeholders.length > 10) {
      warn(`${file} 包含 ${placeholders.length} 个占位符，需要填充`);
    }
  }

  // 输出统计
  const kbSize = Math.round(totalWordCount / 1024);
  pass(`总内容量: ~${kbSize} KB`);

  if (hasMermaidDiagram) {
    pass('包含流程图 (Mermaid)');
  } else {
    warn('未检测到流程图，建议添加');
  }

  if (hasTables) {
    pass('包含数据表格');
  } else {
    warn('未检测到表格，建议添加');
  }

  // 内容量评估
  if (totalWordCount < 5000) {
    warn('文档内容较少，建议补充详细说明');
  } else if (totalWordCount > 50000) {
    pass('文档内容充实');
  }
}

// 检查一致性
async function checkConsistency(fragmentsDir) {
  const files = fs.readdirSync(fragmentsDir).filter(f => f.endsWith('.html'));

  const allContent = [];
  for (const file of files) {
    const filePath = path.join(fragmentsDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    allContent.push({ file, content });
  }

  // 检查功能编号连续性
  const functionIds = [];
  const idRegex = /F(\d{2,3})/g;

  for (const { file, content } of allContent) {
    let match;
    while ((match = idRegex.exec(content)) !== null) {
      functionIds.push(parseInt(match[1]));
    }
  }

  if (functionIds.length > 0) {
    functionIds.sort((a, b) => a - b);
    const uniqueIds = [...new Set(functionIds)];

    if (uniqueIds.length !== functionIds.length) {
      warn('功能编号存在重复');
    } else {
      pass(`功能编号: ${uniqueIds.length} 个，无重复`);
    }

    // 检查连续性
    const expectedIds = Array.from({ length: uniqueIds[uniqueIds.length - 1] }, (_, i) => i + 1);
    const missingIds = expectedIds.filter(id => !uniqueIds.includes(id));

    if (missingIds.length > 0 && missingIds.length < 5) {
      warn(`功能编号不连续，缺失: F${missingIds.map(id => String(id).padStart(2, '0')).join(', F')}`);
    }
  }

  // 检查术语一致性
  const termVariations = {
    '登录': ['登陆'],
    '账户': ['帐户'],
    '验证码': ['校验码'],
  };

  for (const [correct, wrongs] of Object.entries(termVariations)) {
    for (const wrong of wrongs) {
      const regex = new RegExp(wrong, 'g');
      for (const { file, content } of allContent) {
        if (regex.test(content)) {
          warn(`${file} 中使用 '${wrong}'，建议统一为 '${correct}'`);
        }
      }
    }
  }
}

// 输出总结
function printSummary() {
  log('\n' + '='.repeat(50), 'cyan');
  log('验证总结', 'cyan');
  log('='.repeat(50) + '\n', 'cyan');

  const total = results.passed.length + results.warnings.length + results.errors.length;

  log(`✅ 通过: ${results.passed.length} 项`, 'green');
  log(`⚠️  警告: ${results.warnings.length} 项`, 'yellow');
  log(`❌ 错误: ${results.errors.length} 项\n`, 'red');

  if (results.errors.length === 0) {
    if (results.warnings.length === 0) {
      log('🎉 所有检查通过！PRD文档质量良好。', 'green');
    } else {
      log('✅ 检查通过，但存在一些警告，建议优化。', 'yellow');
    }
  } else {
    log('❌ 检查未通过，请修复错误后重试。', 'red');
  }

  log('\n提示:', 'blue');
  log('  • 运行 node build.js 构建HTML');
  log('  • 运行 node build-pdf.js 生成PDF');
  log('  • 查看 checklists/prd-review-checklist.md 获取完整检查清单');
  log('');
}

// 主入口
const projectDir = process.argv[2] || '.';
validate(projectDir).then(exitCode => {
  process.exit(exitCode);
}).catch(err => {
  log(`验证失败: ${err.message}`, 'red');
  process.exit(1);
});
