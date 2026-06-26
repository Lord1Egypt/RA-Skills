#!/usr/bin/env node
/**
 * PRD项目初始化脚本（交互式）
 * 创建完整的PRD项目骨架
 *
 * 用法：
 *   交互模式：node init-prd.js
 *   命令模式：node init-prd.js <项目目录> <产品名称>
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// 产品类型选项
const PRODUCT_TYPES = [
  { key: '1', name: '教育类', desc: '在线教育、学习工具、课程平台' },
  { key: '2', name: '电商类', desc: '商城、购物、订单、支付' },
  { key: '3', name: 'SaaS/B端', desc: '企业管理系统、办公协同' },
  { key: '4', name: '社交类', desc: '社交、聊天、社区、分享' },
  { key: '5', name: '内容类', desc: '资讯、文章、视频、推荐' },
  { key: '6', name: '工具类', desc: '效率工具、计算器、助手' },
  { key: '0', name: '其他', desc: '其他类型产品' }
];

// 创建readline接口
function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

// 提问函数
function ask(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

// 交互式初始化
async function interactiveInit() {
  const rl = createRL();

  console.log('╔════════════════════════════════════════╗');
  console.log('║     📦 PRD 项目初始化向导              ║');
  console.log('╚════════════════════════════════════════╝');
  console.log('');

  try {
    // 1. 产品名称
    let productName = await ask(rl, '请输入产品名称（如：学习打卡App）：');
    while (!productName) {
      console.log('❌ 产品名称不能为空');
      productName = await ask(rl, '请输入产品名称：');
    }

    // 2. 产品类型
    console.log('\n请选择产品类型：');
    PRODUCT_TYPES.forEach(type => {
      console.log(`  ${type.key}. ${type.name} - ${type.desc}`);
    });
    let typeKey = await ask(rl, '\n请输入数字（0-6）：');
    while (!PRODUCT_TYPES.find(t => t.key === typeKey)) {
      console.log('❌ 无效的选择');
      typeKey = await ask(rl, '请输入数字（0-6）：');
    }
    const productType = PRODUCT_TYPES.find(t => t.key === typeKey).name;

    // 3. 项目目录
    const defaultDir = `./prd-${productName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`;
    let projectDir = await ask(rl, `\n请输入项目目录（默认：${defaultDir}）：`);
    if (!projectDir) {
      projectDir = defaultDir;
    }

    // 4. 确认
    console.log('\n┌─ 确认信息 ─────────────────────────┐');
    console.log(`│ 产品名称：${productName.padEnd(28)}│`);
    console.log(`│ 产品类型：${productType.padEnd(28)}│`);
    console.log(`│ 项目目录：${projectDir.padEnd(28)}│`);
    console.log('└────────────────────────────────────┘');

    const confirm = await ask(rl, '\n确认创建？(y/n)：');
    if (confirm.toLowerCase() !== 'y') {
      console.log('\n❌ 已取消');
      rl.close();
      process.exit(0);
    }

    rl.close();

    // 执行创建
    await createProject(projectDir, productName, productType);

  } catch (error) {
    console.error('\n❌ 发生错误:', error.message);
    rl.close();
    process.exit(1);
  }
}

// 创建项目
async function createProject(projectDir, productName, productType) {
  // 获取当前日期
  const today = new Date().toISOString().split('T')[0];

  // 转换产品名为文件名格式
  const productSlug = productName
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '');

  // 获取脚本和模板目录路径
  const scriptDir = __dirname;
  const skillDir = path.dirname(scriptDir);
  const templatesDir = path.join(skillDir, 'templates');

  // 解析项目目录路径
  const resolvedProjectDir = path.resolve(projectDir);

  // 检查目录是否已存在且非空
  if (fs.existsSync(resolvedProjectDir)) {
    const files = fs.readdirSync(resolvedProjectDir);
    if (files.length > 0) {
      console.error(`\n❌ 目录已存在且非空: ${resolvedProjectDir}`);
      process.exit(1);
    }
  }

  console.log(`\n📦 初始化PRD项目: ${productName}`);
  console.log(`   目录: ${resolvedProjectDir}`);
  console.log(`   标识: ${productSlug}`);
  console.log(`   类型: ${productType}`);
  console.log('');

  // 创建目录结构
  const dirs = ['fragments', 'output', 'versions', 'research'];
  dirs.forEach(dir => {
    const dirPath = path.join(resolvedProjectDir, dir);
    fs.mkdirSync(dirPath, { recursive: true });
  });

  // 复制模板文件
  const filesToCopy = [
    { src: 'styles.css', dest: 'styles.css' },
    { src: 'build.js', dest: 'build.js' },
    { src: 'build-pdf.js', dest: 'build-pdf.js' },
    { src: 'update.js', dest: 'update.js' }
  ];

  filesToCopy.forEach(({ src, dest }) => {
    const srcPath = path.join(templatesDir, src);
    const destPath = path.join(resolvedProjectDir, dest);
    if (fs.existsSync(srcPath)) {
      fs.copyFileSync(srcPath, destPath);
    }
  });

  // 复制HTML片段模板
  const fragmentsDir = path.join(templatesDir, 'fragments');
  const destFragmentsDir = path.join(resolvedProjectDir, 'fragments');
  if (fs.existsSync(fragmentsDir)) {
    const fragmentFiles = fs.readdirSync(fragmentsDir).filter(f => f.endsWith('.html'));
    fragmentFiles.forEach(file => {
      const srcPath = path.join(fragmentsDir, file);
      const destPath = path.join(destFragmentsDir, file);
      fs.copyFileSync(srcPath, destPath);
    });
  }

  // 创建 status.json（状态追踪）
  const statusJson = {
    currentStep: 0,
    totalSteps: 10,
    productName: productName,
    productType: productType,
    createdAt: today,
    updatedAt: today,
    steps: [
      { step: 1, name: '需求探索', status: 'pending', completedAt: null },
      { step: 2, name: '产品定位', status: 'pending', completedAt: null },
      { step: 3, name: '功能蓝图', status: 'pending', completedAt: null },
      { step: 4, name: '市场分析与流程', status: 'pending', completedAt: null },
      { step: 5, name: '信息架构', status: 'pending', completedAt: null },
      { step: 6, name: '原型+UI', status: 'pending', completedAt: null },
      { step: 7, name: '功能+数据', status: 'pending', completedAt: null },
      { step: 8, name: '技术方案', status: 'pending', completedAt: null },
      { step: 9, name: '测试+埋点', status: 'pending', completedAt: null },
      { step: 10, name: '运营+计划', status: 'pending', completedAt: null }
    ]
  };
  fs.writeFileSync(
    path.join(resolvedProjectDir, 'status.json'),
    JSON.stringify(statusJson, null, 2) + '\n'
  );

  // 创建 version.json
  const versionJson = {
    version: '1.0.0',
    build: 0,
    lastUpdate: today,
    title: `prd-${productSlug}`,
    productName: productName,
    productType: productType
  };
  fs.writeFileSync(
    path.join(resolvedProjectDir, 'version.json'),
    JSON.stringify(versionJson, null, 2) + '\n'
  );

  // 创建 CHANGELOG.md
  const changelogContent = `# ${productName} PRD 更新日志

> 格式：\`[版本号] YYYY-MM-DD — 摘要\`
`;
  fs.writeFileSync(
    path.join(resolvedProjectDir, 'CHANGELOG.md'),
    changelogContent
  );

  // 创建 PROJECT.md
  const projectMdContent = `# ${productName} — PRD项目

> 产品标识：${productSlug}
> 产品类型：${productType}
> 状态：🟡 规划中（Step 0/10）
> 创建日期：${today}

---

## 产品信息

| 项目 | 内容 |
|------|------|
| 产品名称 | ${productName} |
| 产品类型 | ${productType} |
| 目标用户 | （待填写） |
| 核心痛点 | （待填写） |
| 核心价值 | （待填写） |

---

## PRD章节进度

| 章节 | 文件名 | 状态 | 备注 |
|------|--------|------|------|
| 封面 | 00-cover.html | ⏳ |  |
| 目录 | 01-toc.html | ⏳ |  |
| 概述 | 02-overview.html | ⏳ |  |
| 需求列表 | 03-requirements.html | ⏳ |  |
| 用户故事 | 04-user-stories.html | ⏳ |  |
| 功能规格 | 05-functional.html | ⏳ | 含流程图 |
| 交互说明 | 06-interaction.html | ⏳ |  |
| 数据埋点 | 07-data.html | ⏳ | 自动标准埋点 |
| 非功能需求 | 08-nonfunctional.html | ⏳ |  |
| 尾页 | 99-backpage.html | ⏳ |  |

---

## 迭代记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0.0 | ${today} | 初版创建 |

---

## 协作进度

使用 \`node status.js\` 查看当前进行到哪一步。

当用户描述产品想法后，执行以下步骤：

1. **需求分析**：提取5W2H，识别产品类型
2. **选择模板**：根据产品类型加载对应配置
3. **并行写作**：启动各章节Agent生成内容
4. **文档组装**：合并为完整PRD
5. **格式转换**：输出PDF + HTML + Markdown

如需迭代：用户可指定章节更新或描述新增内容
`;
  fs.writeFileSync(
    path.join(resolvedProjectDir, 'PROJECT.md'),
    projectMdContent
  );

  // 复制 status.js 到项目目录
  const statusJsSrc = path.join(scriptDir, 'status.js');
  if (fs.existsSync(statusJsSrc)) {
    fs.copyFileSync(statusJsSrc, path.join(resolvedProjectDir, 'status.js'));
  }

  console.log('✅ PRD项目创建成功！');
  console.log('');
  console.log('📁 项目结构:');
  console.log(`   ${resolvedProjectDir}/`);
  console.log('   ├── PROJECT.md          # 项目信息');
  console.log('   ├── status.json         # 协作进度追踪');
  console.log('   ├── status.js           # 查看进度命令');
  console.log('   ├── version.json        # 版本信息');
  console.log('   ├── CHANGELOG.md        # 更新日志');
  console.log('   ├── build.js            # HTML构建脚本');
  console.log('   ├── build-pdf.js        # PDF生成脚本');
  console.log('   ├── update.js           # 版本更新脚本');
  console.log('   ├── styles.css          # 共享样式');
  console.log('   ├── fragments/          # PRD内容片段');
  console.log('   ├── output/             # 输出目录');
  console.log('   └── research/           # 调研资料');
  console.log('');
  console.log('🚀 下一步：');
  console.log(`   cd ${projectDir}`);
  console.log('   在Claude对话中描述你的产品想法，AI将自动生成完整PRD');
}

// 命令行模式（保留向后兼容）
function commandMode() {
  const projectDir = process.argv[2];
  const productName = process.argv[3];

  if (!projectDir || !productName) {
    console.error('❌ 用法: node init-prd.js [项目目录] [产品名称]');
    console.error('   或: node init-prd.js（进入交互模式）');
    process.exit(1);
  }

  createProject(projectDir, productName, '未指定');
}

// 主入口
if (process.argv.length >= 4) {
  // 命令行模式
  commandMode();
} else if (process.argv.length === 2) {
  // 交互模式
  interactiveInit();
} else {
  console.error('❌ 用法: node init-prd.js [项目目录] [产品名称]');
  console.error('   或: node init-prd.js（进入交互模式）');
  process.exit(1);
}
