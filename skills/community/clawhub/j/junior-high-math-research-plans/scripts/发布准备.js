/**
 * 初中数学研学案技能包发布准备脚本
 * 用于检查和准备技能包发布
 */

const fs = require('fs');
const path = require('path');

class PublishPreparer {
  constructor() {
    this.skillDir = path.join(__dirname, '..');
    this.requiredFiles = [
      'SKILL.md',
      'package.json',
      'skills/教学资源查找.js',
      'skills/教学计划生成.js',
      'resources/七年级资源索引.md',
      'resources/八年级资源索引.md',
      'resources/九年级资源索引.md',
      'templates/教学计划模板.md',
      'templates/学案模板.md'
    ];
  }

  /**
   * 检查技能包完整性
   */
  checkIntegrity() {
    console.log('🔍 检查技能包完整性...\n');
    
    const results = {
      passed: [],
      missing: [],
      errors: []
    };

    for (const file of this.requiredFiles) {
      const filePath = path.join(this.skillDir, file);
      try {
        if (fs.existsSync(filePath)) {
          const stats = fs.statSync(filePath);
          if (stats.isFile()) {
            results.passed.push({
              file,
              size: stats.size,
              modified: stats.mtime
            });
            console.log(`✅ ${file} (${stats.size} bytes)`);
          } else if (stats.isDirectory()) {
            results.passed.push({
              file,
              type: 'directory',
              modified: stats.mtime
            });
            console.log(`✅ ${file}/ (目录)`);
          }
        } else {
          results.missing.push(file);
          console.log(`❌ ${file} (缺失)`);
        }
      } catch (error) {
        results.errors.push({
          file,
          error: error.message
        });
        console.log(`⚠️ ${file} (检查错误: ${error.message})`);
      }
    }

    console.log('\n📊 检查结果汇总:');
    console.log(`✅ 通过: ${results.passed.length} 个文件`);
    console.log(`❌ 缺失: ${results.missing.length} 个文件`);
    console.log(`⚠️ 错误: ${results.errors.length} 个文件`);

    return results;
  }

  /**
   * 验证package.json配置
   */
  validatePackageJson() {
    console.log('\n📦 验证package.json配置...');
    
    const packagePath = path.join(this.skillDir, 'package.json');
    if (!fs.existsSync(packagePath)) {
      console.log('❌ package.json 文件不存在');
      return false;
    }

    try {
      const packageContent = fs.readFileSync(packagePath, 'utf-8');
      const packageJson = JSON.parse(packageContent);
      
      const requiredFields = ['name', 'version', 'description', 'author'];
      const missingFields = [];
      
      for (const field of requiredFields) {
        if (!packageJson[field]) {
          missingFields.push(field);
        }
      }
      
      if (missingFields.length > 0) {
        console.log(`❌ 缺少必要字段: ${missingFields.join(', ')}`);
        return false;
      }
      
      console.log(`✅ 包名: ${packageJson.name}`);
      console.log(`✅ 版本: ${packageJson.version}`);
      console.log(`✅ 描述: ${packageJson.description}`);
      console.log(`✅ 作者: ${packageJson.author}`);
      
      // 检查OpenClaw技能配置
      if (packageJson.openclaw) {
        console.log('✅ OpenClaw技能配置: 存在');
        console.log(`   - 分类: ${packageJson.openclaw.category || '未指定'}`);
        console.log(`   - 标签: ${packageJson.openclaw.tags?.join(', ') || '未指定'}`);
      } else {
        console.log('⚠️ OpenClaw技能配置: 缺失（建议添加）');
      }
      
      return true;
    } catch (error) {
      console.log(`❌ 解析package.json失败: ${error.message}`);
      return false;
    }
  }

  /**
   * 验证SKILL.md文档
   */
  validateSkillDoc() {
    console.log('\n📖 验证SKILL.md文档...');
    
    const skillPath = path.join(this.skillDir, 'SKILL.md');
    if (!fs.existsSync(skillPath)) {
      console.log('❌ SKILL.md 文件不存在');
      return false;
    }

    try {
      const content = fs.readFileSync(skillPath, 'utf-8');
      const lines = content.split('\n');
      
      // 检查必要章节
      const requiredSections = ['## 概述', '## 功能特性', '## 包含内容', '## 使用方法'];
      const missingSections = [];
      
      for (const section of requiredSections) {
        if (!content.includes(section)) {
          missingSections.push(section);
        }
      }
      
      if (missingSections.length > 0) {
        console.log(`⚠️ 缺少文档章节: ${missingSections.join(', ')}`);
      } else {
        console.log('✅ 文档结构完整');
      }
      
      console.log(`✅ 文档大小: ${content.length} 字符`);
      console.log(`✅ 文档行数: ${lines.length} 行`);
      
      return missingSections.length === 0;
    } catch (error) {
      console.log(`❌ 读取SKILL.md失败: ${error.message}`);
      return false;
    }
  }

  /**
   * 生成发布检查报告
   */
  generateReport() {
    console.log('\n📋 生成发布检查报告...\n');
    
    const integrity = this.checkIntegrity();
    const packageValid = this.validatePackageJson();
    const skillDocValid = this.validateSkillDoc();
    
    const report = {
      timestamp: new Date().toISOString(),
      skillName: '初中数学研学案技能包',
      checks: {
        integrity: {
          passed: integrity.passed.length,
          missing: integrity.missing.length,
          errors: integrity.errors.length,
          details: {
            passed: integrity.passed.map(p => p.file),
            missing: integrity.missing,
            errors: integrity.errors
          }
        },
        packageJson: {
          valid: packageValid
        },
        skillDoc: {
          valid: skillDocValid
        }
      },
      overall: integrity.missing.length === 0 && integrity.errors.length === 0 && packageValid && skillDocValid
    };
    
    // 保存报告
    const reportPath = path.join(this.skillDir, '发布检查报告.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), 'utf-8');
    
    console.log(`📄 报告已保存: ${reportPath}`);
    
    if (report.overall) {
      console.log('\n🎉 所有检查通过！技能包可以发布。');
      console.log('\n📦 发布步骤:');
      console.log('1. 确保技能包文件夹名称规范（英文或拼音）');
      console.log('2. 压缩为ZIP文件：初中数学研学案技能包.zip');
      console.log('3. 登录ClawdHub网站（https://clawhub.com）');
      console.log('4. 点击"发布技能"，上传ZIP文件');
      console.log('5. 填写技能信息，提交审核');
      console.log('6. 等待审核通过后即可公开使用');
    } else {
      console.log('\n⚠️ 存在一些问题需要修复：');
      if (integrity.missing.length > 0) {
        console.log(`   - 缺失文件: ${integrity.missing.join(', ')}`);
      }
      if (integrity.errors.length > 0) {
        console.log(`   - 检查错误: ${integrity.errors.map(e => e.file).join(', ')}`);
      }
      if (!packageValid) {
        console.log('   - package.json配置有问题');
      }
      if (!skillDocValid) {
        console.log('   - SKILL.md文档不完整');
      }
      console.log('\n🔧 请修复上述问题后重新检查。');
    }
    
    return report;
  }

  /**
   * 创建发布包
   */
  createReleasePackage() {
    console.log('\n📦 创建发布包...');
    
    const report = this.generateReport();
    if (!report.overall) {
      console.log('❌ 存在未通过检查，无法创建发布包');
      return false;
    }
    
    // 创建ZIP文件的说明
    console.log('\n📋 发布包创建说明:');
    console.log('1. 手动将以下文件夹压缩为ZIP文件:');
    console.log(`   源文件夹: ${this.skillDir}`);
    console.log('2. ZIP文件应包含以下结构:');
    console.log('   初中数学研学案技能包.zip');
    console.log('   ├── SKILL.md');
    console.log('   ├── package.json');
    console.log('   ├── skills/');
    console.log('   ├── resources/');
    console.log('   ├── templates/');
    console.log('   └── scripts/');
    console.log('\n3. 建议ZIP文件命名: junior-high-math-research-plans-v1.0.0.zip');
    
    // 生成版本说明
    const changelog = this.generateChangelog();
    const changelogPath = path.join(this.skillDir, 'CHANGELOG.md');
    fs.writeFileSync(changelogPath, changelog, 'utf-8');
    console.log(`\n📝 已生成更新日志: ${changelogPath}`);
    
    return true;
  }

  /**
   * 生成更新日志
   */
  generateChangelog() {
    return `# 更新日志

## v1.0.0 (2026-02-25)

### 🎉 初始发布
- 完整的初中数学研学案技能包
- 包含七年级、八年级、九年级全套教学资源
- 基于人教版2024新版教材

### ✨ 核心功能
1. **教学资源查找**
   - 按年级、章节快速定位资源
   - 详细的资源索引和说明
   - 支持关键词搜索

2. **教学计划生成**
   - 单课时教学计划
   - 章节教学计划
   - 学期教学计划
   - 完整的课时安排表

3. **模板系统**
   - 教学计划模板
   - 学案模板
   - 可自定义的模板变量

### 📁 资源内容
- **七年级**: 一元一次方程、图形的初步、有理数、整式的加减
- **八年级**: 三角形、全等三角形、轴对称、整式的乘法与因式分解、分式
- **九年级**: 二次函数、旋转、圆、概率、一元二次方程、中考复习

### 🛠 技术特性
- 模块化设计，易于扩展
- 完整的错误处理
- 详细的文档说明
- 发布检查工具

### 📋 系统要求
- OpenClaw 环境
- Node.js >= 18.0.0
- 基本的文件读写权限

### 👥 适用对象
- 初中数学教师
- 教学研究人员
- 教育培训机构
- 学生和家长

---
*技能包设计：阿锋*
*发布日期：2026年2月25日*`;
  }
}

// 命令行接口
if (require.main === module) {
  const preparer = new PublishPreparer();
  
  const command = process.argv[2] || 'report';
  
  switch (command) {
    case 'check':
      preparer.checkIntegrity();
      break;
    case 'package':
      preparer.validatePackageJson();
      break;
    case 'doc':
      preparer.validateSkillDoc();
      break;
    case 'report':
      preparer.generateReport();
      break;
    case 'release':
      preparer.createReleasePackage();
      break;
    case 'all':
      preparer.checkIntegrity();
      preparer.validatePackageJson();
      preparer.validateSkillDoc();
      preparer.generateReport();
      break;
    default:
      console.log('可用命令:');
      console.log('  node 发布准备.js check     - 检查文件完整性');
      console.log('  node 发布准备.js package   - 验证package.json');
      console.log('  node 发布准备.js doc       - 验证SKILL.md文档');
      console.log('  node 发布准备.js report    - 生成完整报告（默认）');
      console.log('  node 发布准备.js release   - 创建发布包');
      console.log('  node 发布准备.js all       - 执行所有检查');
  }
}

module.exports = PublishPreparer;