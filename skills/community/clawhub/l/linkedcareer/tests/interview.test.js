const test = require('node:test')
const assert = require('node:assert')
const Interview = require('../src/core/interview')

test('初始化引导流程', async (t) => {
  const interview = new Interview()
  
  // 第一个问题应该是询问基本信息
  let question = await interview.startOnboarding()
  assert(question.includes('姓名'))
  // 回答姓名
  question = await interview.processAnswer('张三')
  assert(question.includes('电话'))
  // 回答电话
  question = await interview.processAnswer('13800138000')
  assert(question.includes('邮箱'))
})

test('定期记录引导', async (t) => {
  const interview = new Interview()
  const question = await interview.getReminderQuestion('weekly')
  assert(question.includes('本周'))
  assert(question.includes('项目'))
  assert(question.includes('技能'))
})
