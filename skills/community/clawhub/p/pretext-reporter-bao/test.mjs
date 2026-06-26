/**
 * Pretext 基础导入测试
 * 验证 Pretext 模块是否可以正常导入
 */

async function runTests() {
  console.log('🧪 Pretext 基础导入测试\n')
  console.log('=' .repeat(50))

  // 测试 1: 导入 Pretext
  console.log('\n📦 测试 1: 导入 Pretext 模块')
  try {
    const pretext = await import('./pretext/dist/layout.js')
    console.log(`   ✅ 成功导入 Pretext`)
    console.log(`   可用函数:`)
    if (pretext.prepare) console.log(`     - prepare`)
    if (pretext.layout) console.log(`     - layout`)
    if (pretext.layoutWithLines) console.log(`     - layoutWithLines`)
    if (pretext.clearCache) console.log(`     - clearCache`)
  } catch (error) {
    console.log(`   ❌ 失败: ${error}`)
    return
  }

  // 测试 2: 导入 Inline Flow
  console.log('\n📦 测试 2: 导入 Inline Flow 模块')
  try {
    const inlineFlow = await import('./pretext/dist/inline-flow.js')
    console.log(`   ✅ 成功导入 Inline Flow`)
  } catch (error) {
    console.log(`   ❌ 失败: ${error}`)
    return
  }

  console.log('\n' + '='.repeat(50))
  console.log('\n✨ 导入测试完成！\n')
  console.log('⚠️  注意: Pretext 的完整功能需要浏览器环境（Canvas API）')
  console.log('💡 建议: 在浏览器控制台或使用 Puppeteer/Playwright 进行功能测试\n')
  console.log('🔧 浏览器测试示例:')
  console.log(`
  // 在浏览器控制台中运行:
  import { prepare, layout } from './skills/pretext-reporter-bao/pretext/dist/layout.js'

  const prepared = prepare('你好世界 🚀', '16px Inter')
  const { height, width, lines } = layout(prepared, 320, 24)
  console.log(\`高度: \${height}px, 行数: \${lines}\`)
  `)
}

runTests().catch(console.error)
