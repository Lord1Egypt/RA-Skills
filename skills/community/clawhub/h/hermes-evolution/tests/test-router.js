/**
 * PM Router 测试用例 - Phase 1 Updated
 */

const { SensenPMRouter } = require('./sensen-pm-router')

async function runTests() {
  console.log('🧪 Sensen PM Router 测试\n')

  const router = new SensenPMRouter()

  const testCases = [
    // Marketing - 全平台内容
    { input: '帮我写一篇小红书，关于AI时代HR如何转型', expected: 'Marketing', desc: '小红书内容' },
    { input: '帮我写一个知乎回答，关于职业规划', expected: 'Marketing', desc: '知乎内容' },
    { input: '帮我写一个抖音视频脚本', expected: 'Marketing', desc: '抖音脚本' },

    // RD - 小说平台
    { input: '@rd 帮我生成第三章的草稿', expected: 'RD', desc: '小说章节生成' },
    { input: '帮我设计一个新世界观', expected: 'RD', desc: '世界观设计' },
    { input: '@novel 生成一个发布包', expected: 'RD', desc: '发布包生成' },

    // Product - 产品管理
    { input: '@product 帮我规划一下Novel Studio的下一步', expected: 'Product', desc: '产品规划' },
    { input: '这个功能优先级是什么', expected: 'Product', desc: '优先级判断' },
    { input: '帮我分析一下产品的PMF', expected: 'Product', desc: 'PMF分析' },

    // Strategy - 战略
    { input: '帮我分析一下，现在做AI+HR咨询的市场机会', expected: 'Strategy', desc: '市场机会分析' },
    { input: '@strategy 最近有什么新的财富机会吗', expected: 'Strategy', desc: '财富机会' },

    // CEO - 汇报/协调
    { input: '帮我看看最近各Agent都在干什么', expected: 'CEO', desc: 'Agent状态汇报' },
    { input: '帮我检查一下Gateway的状态', expected: 'RD', desc: '运维检查（Gateway）' },

    // HR招聘
    { input: '帮我筛选一下这份简历', expected: 'CEO', desc: '简历筛选' },

    // 显式指定
    { input: '@内容 帮我写一篇公众号', expected: 'Marketing', desc: '@内容显式指定' },
    { input: '@产品 Roadmap怎么定', expected: 'Product', desc: '@产品显式指定' },
  ]

  let passed = 0, failed = 0

  for (const tc of testCases) {
    try {
      const result = await router.route(tc.input)
      const actual = result.decision.agent
      const ok = actual === tc.expected

      if (ok) {
        console.log(`✅ ${tc.desc}`)
        console.log(`   "${tc.input}"`)
        console.log(`   → ${actual} (${result.decision.intent})`)
        passed++
      } else {
        console.log(`❌ ${tc.desc}`)
        console.log(`   "${tc.input}"`)
        console.log(`   期望: ${tc.expected}, 实际: ${actual} (${result.decision.intent})`)
        failed++
      }
    } catch (err) {
      console.log(`❌ ${tc.desc} 错误: ${err.message}`)
      failed++
    }
  }

  console.log(`\n======================================`)
  console.log(`结果: ${passed} 通过, ${failed} 失败`)
}

runTests()
