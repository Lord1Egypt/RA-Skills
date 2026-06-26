const test = require('node:test')
const assert = require('node:assert')
const Resume = require('../src/core/resume')
const testData = {
  basicInfo: {
    name: '张三',
    phone: '13800138000',
    email: 'zhangsan@example.com',
    city: '北京',
    expectedPosition: '产品经理'
  },
  experiences: [
    {
      company: '互联网公司A',
      position: '高级产品经理',
      startTime: '2020-01',
      endTime: '至今',
      description: '负责C端产品的规划和迭代',
      achievements: [
        '主导用户增长项目，带动日活提升30%',
        '优化产品流程，用户转化率提升25%'
      ]
    }
  ],
  skills: {
    产品能力: ['需求分析', '产品规划', '用户研究', '数据分析'],
    工具: ['Axure', 'Figma', 'SQL', 'Tableau']
  }
}
const testJD = `
岗位名称：高级产品经理
岗位职责：
1. 负责C端产品规划和迭代
2. 主导用户增长相关项目
3. 跨团队协调推进产品落地
岗位要求：
1. 3年以上互联网产品经理经验
2. 有用户增长项目经验
3. 具备数据分析能力
`
test('人岗匹配度计算', async (t) => {
  const resume = new Resume()
  const result = await resume.calculateMatchScore(testJD, testData)
  assert(result.score >= 80) // 匹配度应该很高
  assert(result.reasons.length > 0)
})
test('简历生成功能', async (t) => {
  const resume = new Resume()
  // 通用生成
  const generalResume = await resume.generate(testData, { mode: 'general', template: 'balanced' })
  assert(generalResume.includes('张三'))
  assert(generalResume.includes('高级产品经理'))
  assert(generalResume.includes('用户增长'))
  // 定向生成
  const targetedResume = await resume.generate(testData, { mode: 'targeted', template: 'minimal', jobJD: testJD })
  assert(targetedResume.includes('用户增长'))
  assert(targetedResume.length < generalResume.length) // 极简版更短
})
test('求职信生成', async (t) => {
  const resume = new Resume()
  const coverLetter = await resume.generateCoverLetter(testData, testJD)
  assert(coverLetter.includes('张三'))
  assert(coverLetter.includes('高级产品经理'))
  assert(coverLetter.includes('用户增长'))
})
