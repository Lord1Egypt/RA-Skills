const test = require('node:test')
const assert = require('node:assert')
const fs = require('fs/promises')
const path = require('path')
const Memory = require('../src/core/memory')
test('Memory模块基础读写功能', async (t) => {
  const testDir = path.join(__dirname, 'test_data')
  await fs.mkdir(testDir, { recursive: true })
  const memory = new Memory(testDir)
  
  // 测试保存和读取数据
  const testData = {
    basicInfo: { name: '张三', phone: '13800138000' },
    experiences: [{ company: '测试公司', position: '产品经理' }]
  }
  
  await memory.save(testData)
  const loadedData = await memory.load()
  
  assert.deepEqual(loadedData, testData)
  
  // 测试Markdown导出
  const markdown = await memory.exportMarkdown()
  assert(markdown.includes('张三'))
  assert(markdown.includes('测试公司'))
  
  await fs.rm(testDir, { recursive: true })
})
test('简历导入功能', async (t) => {
  const memory = new Memory(path.join(__dirname, 'test_data'))
  const resumeText = `
# 张三
## 联系方式
电话：13800138000
## 工作经历
### 测试公司 产品经理 2020-至今
负责产品设计和需求管理
  `
  const parsedData = await memory.importResume(resumeText, 'text')
  assert.equal(parsedData.basicInfo.name, '张三')
  assert.equal(parsedData.basicInfo.phone, '13800138000')
  assert.equal(parsedData.experiences[0].company, '测试公司')
})
