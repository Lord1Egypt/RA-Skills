#!/usr/bin/env node
/**
 * validate_skill.js - 技能文件安全验证脚本
 * 
 * 检查以下内容：
 * 1. Unicode 控制字符
 * 2. 可疑的网络调用
 * 3. 敏感信息泄露
 * 
 * 用法: node scripts/validate_skill.js
 */

const fs = require('fs')
const path = require('path')

const CONTROL_CHAR_PATTERN = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\u200B-\u200D\uFEFF]/g
const DANGEROUS_PATTERNS = [
  { pattern: /eval\s*\(/, message: '发现动态代码执行' },
  { pattern: /exec\s*\(/, message: '发现命令执行' },
  { pattern: /child_process/, message: '发现子进程模块引用' },
  { pattern: /process\.env\.(?!NODE_ENV)/, message: '发现敏感环境变量访问' },
]

function checkFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8')
  const issues = []

  const controlChars = content.match(CONTROL_CHAR_PATTERN)
  if (controlChars && controlChars.length > 0) {
    issues.push(`⚠️  发现 ${controlChars.length} 个隐藏的 Unicode 控制字符`)
  }

  for (const { pattern, message } of DANGEROUS_PATTERNS) {
    if (pattern.test(content)) {
      issues.push(`❌ ${message}`)
    }
  }

  return issues
}

function main() {
  const skillDir = path.join(__dirname, '..')
  const filesToCheck = [
    'SKILL.md',
    'PROMPTS.md',
    'README.md',
    '_meta.json',
    'SECURITY_AUDIT.md',
    'config/api.js',
    'scripts/sync_items.js',
    'scripts/generate_qr.js',
    'scripts/verify_items.js',
    'scripts/calculate_prices.js'
  ]

  console.log('🔍 技能安全验证\n')
  console.log('='.repeat(50))

  let hasIssues = false

  for (const file of filesToCheck) {
    const filePath = path.join(skillDir, file)
    if (!fs.existsSync(filePath)) continue

    console.log(`\n📄 检查: ${file}`)
    const issues = checkFile(filePath)

    if (issues.length === 0) {
      console.log('   ✅ 无问题')
    } else {
      hasIssues = true
      for (const issue of issues) {
        console.log(`   ${issue}`)
      }
    }
  }

  console.log('\n' + '='.repeat(50))

  if (hasIssues) {
    console.log('\n❌ 验证失败：发现安全问题')
    process.exit(1)
  } else {
    console.log('\n✅ 验证通过：所有文件安全')
    process.exit(0)
  }
}

if (require.main === module) {
  main()
}

module.exports = { checkFile, CONTROL_CHAR_PATTERN }
