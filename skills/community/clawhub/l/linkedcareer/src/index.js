#!/usr/bin/env node
const readline = require('readline/promises')
const Memory = require('./core/memory')
const Interview = require('./core/interview')
const Resume = require('./core/resume')
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})
const memory = new Memory()
const interview = new Interview()
const resume = new Resume()
async function main() {
  const command = process.argv[2]
  switch (command) {
    case 'init':
      console.log('👋 欢迎使用LinkedCareer，现在开始初始化你的职业生涯档案...')
      console.log('我会通过几个问题帮你完善档案，你只需要根据提示回答即可。\n')
      let question = await interview.startOnboarding()
      while (true) {
        const answer = await rl.question(`\n${question}\n> `)
        if (answer.trim() === 'exit' || answer.trim() === 'quit') {
          console.log('已退出初始化，下次可以继续使用 /linkedcareer init 继续填写')
          break
        }
        question = await interview.processAnswer(answer)
        console.log('')
        if (question.includes('✅ 初始化完成')) {
          console.log(question)
          // 保存收集到的数据
          const data = interview.getCollectedData()
          await memory.save(data)
          break
        }
      }
      break
    case 'record':
      const frequency = process.argv[3] || 'weekly'
      const recordQuestion = await interview.getReminderQuestion(frequency)
      console.log('📝 开始记录近期工作成长...\n')
      const recordAnswer = await rl.question(`${recordQuestion}\n> `)
      // 读取现有数据，添加记录
      const data = await memory.load()
      if (!data.records) data.records = []
      data.records.push({
        date: new Date().toISOString().split('T')[0],
        frequency,
        content: recordAnswer
      })
      await memory.save(data)
      console.log('\n✅ 记录已保存！')
      break
    case 'deepdive':
      console.log('🧠 苏格拉底式深度梳理')
      console.log('我会逐段梳理你的工作经历，通过提问帮你挖掘更多业绩亮点、能力成长和量化成果\n')
      // 后续实现深度梳理交互逻辑
      break
    case 'find':
      const subCommand = process.argv[3]
      if (subCommand === 'job') {
        console.log('🔍 岗位匹配功能')
        console.log('请粘贴你收集的岗位JD内容，多个JD用空行分隔：\n')
        const readline = require('readline/promises')
        const rl = readline.createInterface({
          input: process.stdin,
          output: process.stdout,
          terminal: false
        })
        // 读取用户输入的所有JD内容
        let jdText = ''
        rl.on('line', (line) => {
          jdText += line + '\n'
        })
        rl.on('close', async () => {
          const JobMatcher = require('./core/jobMatcher')
          const matcher = new JobMatcher()
          const Memory = require('./core/memory')
          const memory = new Memory()
          const careerData = await memory.load()
          // 解析JD列表
          const jdList = matcher.parseJdList(jdText)
          if (jdList.length === 0) {
            console.log('❌ 未识别到有效的岗位JD，请检查输入格式')
            return
          }
          console.log(`✅ 识别到 ${jdList.length} 个岗位，正在计算匹配度...\n`)
          // 批量匹配
          const results = await matcher.batchMatch(careerData, jdList)
          // 输出结果
          console.log(matcher.formatResults(results))
        })
      } else {
        console.log('可用命令：/linkedcareer find job  匹配适合你的岗位')
      }
      break
    case 'resume':
      console.log('📄 开始生成简历，请选择模板类型：')
      console.log('1. 🎩 旗舰商务版 | 深蓝稳重风格 | 适合高管/金融/民企岗位投递')
      console.log('2. 💻 现代双栏版 | 科技蓝侧边栏 | 适合互联网/科技行业岗位')
      console.log('3. 🏛️ 国企稳重版 | 深灰正式风格 | 适合央企/事业单位/体制内求职')
      console.log('4. 🎨 创意设计版 | 莫兰迪卡片式 | 适合设计/运营/市场创意类岗位')
      console.log('5. 📄 极简通用版 | 黑白一页纸 | 适合海投/初筛/校招通用场景')
      const templateChoice = await rl.question('请输入选项（1/2/3/4/5，默认1）：\n> ')
      const templateMap = {
        '1': 'executive',
        '2': 'modern',
        '3': 'soe',
        '4': 'creative',
        '5': 'minimal'
      }
      const template = templateMap[templateChoice] || 'executive'
      
      console.log('\n请选择输出格式：')
      console.log('1. Word格式（.docx，可编辑）')
      console.log('2. PDF格式（.pdf，和Word样式1:1一致）')
      console.log('3. Markdown格式（.md，可自定义）')
      const formatChoice = await rl.question('请输入选项（1/2/3，默认1）：\n> ')
      const formatMap = {
        '1': 'docx',
        '2': 'pdf',
        '3': 'md'
      }
      const format = formatMap[formatChoice] || 'docx'
      
      console.log('\n正在生成简历...\n')
      const careerData = await memory.load()
      
      if (format === 'docx') {
        // 生成Word格式
        const outputPath = `./resume_${template}_${new Date().toISOString().split('T')[0]}.docx`
        await resume.generateProfessionalWord(careerData, outputPath, { industry: 'internet' })
        console.log(`✅ Word版简历已生成并保存到：${outputPath}`)
      } else if (format === 'pdf') {
        console.log('⏳ PDF生成功能正在开发中，当前版本请先导出Word格式自行转换，感谢理解~')
      } else {
        // 生成Markdown格式
        const generatedResume = await resume.generate(careerData, { mode: 'general', template: 'balanced' })
        const outputPath = `./resume_${new Date().toISOString().split('T')[0]}.md`
        require('fs').writeFileSync(outputPath, generatedResume, 'utf8')
        console.log(`✅ Markdown版简历已生成并保存到：${outputPath}`)
      }
      
      // 询问是否需要导出提示
      console.log('\n💡 提示：生成的Word简历已内置所有商务样式，可直接使用，也可以替换头像、调整细节')
      break
    case 'import':
      const filePath = process.argv[3]
      if (!filePath) {
        console.log('请提供简历文件路径：/linkedcareer import <简历文件路径>')
        break
      }
      console.log('📥 正在导入简历...')
      const content = require('fs').readFileSync(filePath, 'utf8')
      const parsedData = await memory.importResume(content, 'text')
      console.log('✅ 简历导入完成，已提取以下信息：')
      console.log(`  姓名：${parsedData.basicInfo.name || '未识别'}`)
      console.log(`  电话：${parsedData.basicInfo.phone || '未识别'}`)
      console.log(`  邮箱：${parsedData.basicInfo.email || '未识别'}`)
      console.log(`  工作经历：${parsedData.experiences.length} 段`)
      break
    default:
      console.log('📋 LinkedCareer 可用命令:')
      console.log('  /linkedcareer init              初始化职业生涯档案')
      console.log('  /linkedcareer deepdive          深度梳理职业经历挖掘亮点')
      console.log('  /linkedcareer record [daily/weekly/monthly]  记录工作成长')
      console.log('  /linkedcareer resume [general/targeted] [minimal/balanced/detailed] [JD内容]  生成简历')
      console.log('  /linkedcareer import <文件路径>  导入已有简历')
  }
  rl.close()
}
main().catch(err => {
  console.error('❌ 运行出错：', err)
  rl.close()
})