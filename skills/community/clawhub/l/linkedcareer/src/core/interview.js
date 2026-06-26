class Interview {
  constructor() {
    this.step = 0
    this.data = {}
    // 基础信息字段定义，按匹配优先级排序
    this.basicInfoFields = [
      { key: 'phone', label: '联系电话', required: true, pattern: /1[3-9]\d{9}/ },
      { key: 'email', label: '邮箱', required: true, pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/ },
      { key: 'gender', label: '性别', required: false, pattern: /(?:^|\s)(男|女)(?:$|\s)/ },
      { key: 'age', label: '年龄', required: false, pattern: /(?:^|\D)(\d{1,2})岁(?:$|\D)/i },
      { key: 'name', label: '姓名', required: true, pattern: /(?:叫|姓名|名字|我是)[：:]?\s*([\u4e00-\u9fa5]{2,4})(?:$|\s|，|。)/i },
      { key: 'city', label: '所在城市', required: true, pattern: /(?:在|住|城市|所在地)[：:]?\s*([\u4e00-\u9fa5]{2,10}?)(?:市|省|自治区|$|\s|，|。)/i }
    ]
    this.onboardingSteps = [
      { 
        key: 'basicInfoCollect', 
        question: `### 请提供你的基本信息：
你可以直接用一段话描述，我会自动提取信息：
- 姓名
- 联系电话
- 邮箱地址
- 所在城市
- （可选）性别、年龄
- 如果你有旧简历，可以直接发给我，我会自动导入所有信息~

例如：我叫张三，电话13800138000，邮箱zhangsan@example.com，现在在北京，今年35岁。`,
        field: ['_meta', 'basicInfoRaw']
      },
      { key: 'educationStart', question: '接下来我们来记录教育经历，请问你最高学历的学校名称是什么？', field: ['education', 0, 'school'] },
      { key: 'educationMajor', question: '请问你所学的专业是什么？', field: ['education', 0, 'major'] },
      { key: 'educationTime', question: '请问你入学和毕业的时间是？（格式：2016-09 - 2020-06）', field: ['education', 0, 'time'] },
      { key: 'experienceStart', question: '接下来我们来记录工作经历，请问你最近一份工作的公司名称是什么？', field: ['experiences', 0, 'company'] },
      { key: 'experiencePosition', question: '请问你在这家公司担任的岗位是什么？', field: ['experiences', 0, 'position'] },
      { key: 'experienceTime', question: '请问你入职和离职的时间是？（格式：2020-07 - 至今）', field: ['experiences', 0, 'time'] },
      { key: 'experienceDesc', question: '请简单描述下你在这家公司的主要工作职责？', field: ['experiences', 0, 'description'] },
      { key: 'experienceAchievements', question: '请问你在这家公司取得的主要业绩有哪些？（可以分点说明）', field: ['experiences', 0, 'achievements'] },
      { key: 'addMoreExperience', question: '请问你还有其他工作经历需要记录吗？（是/否）', field: ['_meta', 'addMoreExperience'] },
      { key: 'deepDiveConfirm', question: '✅ 基础职业生涯档案已经收集完成！\n请问你是否需要进行深度梳理？我会像面试官一样通过提问帮你挖掘更多业绩亮点、能力成长和量化成果，让你的职业经历更有说服力。（是/否）', field: ['_meta', 'deepDiveEnabled'] }
    ]
    // 深度梳理的问题模板（苏格拉底式提问）
    this.deepDiveQuestions = [
      {
        key: 'project_challenge',
        question: '在这段工作经历中，你主导的最有挑战性的项目是什么？\nA. 技术攻坚类项目 B. 跨部门协作类项目 C. 新业务从0到1搭建 D. 成本/效率优化类项目 E. 其他',
        field: ['deepDive', 'challenge']
      },
      {
        key: 'project_result',
        question: '这个项目最终取得了什么量化成果？比如收入增长XX%、效率提升XX%、成本下降XX元等，请尽量用数字描述。',
        field: ['deepDive', 'result']
      },
      {
        key: 'core_contribution',
        question: '你在这个项目中的核心贡献是什么？哪些成果是因为你的决策或行动直接带来的？',
        field: ['deepDive', 'contribution']
      },
      {
        key: 'ability_growth',
        question: '通过这个项目，你获得了哪些关键能力提升？或者总结出了什么可复用的方法论？',
        field: ['deepDive', 'growth']
      }
    ]
    // 用来存储缺失的基础信息字段
    this.missingBasicFields = []
    // 当前深度梳理的工作经历索引
    this.currentDeepDiveExpIndex = 0
    // 当前深度梳理的问题索引
    this.currentDeepDiveQuestionIndex = 0
    // 是否正在进行深度梳理
    this.isDeepDiving = false
    // 深度梳理的经历列表（优先最近5年）
    this.deepDiveExpList = []
    // 是否已经完成最近5年的梳理，待确认是否继续更早的经历
    this.needConfirmMoreDive = false
  }
  // 从用户输入中提取基础信息
  extractBasicInfo(text) {
    const info = {}
    // 按优先级匹配字段，避免冲突
    for (const field of this.basicInfoFields) {
      const match = text.match(field.pattern)
      if (match) {
        if (field.key === 'age') {
          // 年龄只保留数字
          info[field.key] = match[1].replace(/\D/g, '')
        } else if (field.key === 'name' || field.key === 'city') {
          // 姓名和城市取捕获组，去除空白和前缀
          info[field.key] = match[1].trim()
          // 城市去掉可能的"在"、"住"等前缀残留
          info[field.key] = info[field.key].replace(/^(在|住)\s*/, '')
        } else {
          info[field.key] = match[0].trim()
        }
      }
    }
    return info
  }
  async startOnboarding() {
    this.step = 0
    this.data = {
      basicInfo: {},
      education: [],
      experiences: [],
      _meta: {}
    }
    this.missingBasicFields = []
    this.currentDeepDiveExpIndex = 0
    this.currentDeepDiveQuestionIndex = 0
    this.isDeepDiving = false
    return this.onboardingSteps[0].question
  }
  async processAnswer(answer) {
    const currentStep = this.onboardingSteps[this.step]
    // 如果正在深度梳理，单独处理
    if (this.isDeepDiving) {
      // 如果是待确认是否继续梳理更早的经历
      if (this.needConfirmMoreDive) {
        if (answer.trim() === '是' || answer.trim() === 'yes') {
          // 加载更早的经历继续梳理
          const currentYear = new Date().getFullYear()
          this.deepDiveExpList = this.data.experiences.filter(exp => {
            const endYear = exp.endTime === '至今' ? currentYear : parseInt(exp.endTime?.split('-')[0] || 0)
            return endYear < currentYear - 5
          })
          this.currentDeepDiveExpIndex = 0
          this.currentDeepDiveQuestionIndex = 0
          this.needConfirmMoreDive = false
          if (this.deepDiveExpList.length === 0) {
            this.isDeepDiving = false
            return '✅ 深度梳理完成！没有更早的工作经历需要梳理了，你的职业生涯档案已经非常完善了~'
          }
          // 开始第一段更早经历的深度梳理
          const exp = this.deepDiveExpList[this.currentDeepDiveExpIndex]
          return `### 开始深度梳理更早的工作经历（第${this.currentDeepDiveExpIndex+1}/${this.deepDiveExpList.length}段）：${exp.company} - ${exp.position}\n${this.deepDiveQuestions[this.currentDeepDiveQuestionIndex].question}`
        } else {
          // 不继续梳理，结束
          this.isDeepDiving = false
          return '✅ 深度梳理完成！你的职业生涯档案已经非常完善了，随时可以生成简历或记录新的工作成长~'
        }
      }

      const currentExp = this.deepDiveExpList[this.currentDeepDiveExpIndex]
      const currentQuestion = this.deepDiveQuestions[this.currentDeepDiveQuestionIndex]
      // 保存回答到对应工作经历的深度信息中
      if (!currentExp.deepDive) currentExp.deepDive = {}
      currentExp.deepDive[currentQuestion.field[1]] = answer.trim()
      // 如果是成果类回答，自动添加到业绩列表中
      if (currentQuestion.key === 'project_result' || currentQuestion.key === 'core_contribution') {
        if (!currentExp.achievements) currentExp.achievements = []
        currentExp.achievements.push(answer.trim())
      }
      // 下一个问题
      this.currentDeepDiveQuestionIndex++
      if (this.currentDeepDiveQuestionIndex < this.deepDiveQuestions.length) {
        // 继续问当前工作经历的下一个问题
        return this.deepDiveQuestions[this.currentDeepDiveQuestionIndex].question
      } else {
        // 当前工作经历梳理完成，下一段经历
        this.currentDeepDiveExpIndex++
        this.currentDeepDiveQuestionIndex = 0
        if (this.currentDeepDiveExpIndex < this.deepDiveExpList.length) {
          // 开始下一段工作经历的深度梳理
          const nextExp = this.deepDiveExpList[this.currentDeepDiveExpIndex]
          return `### 开始深度梳理第${this.currentDeepDiveExpIndex+1}/${this.deepDiveExpList.length}段工作经历：${nextExp.company} - ${nextExp.position}\n${this.deepDiveQuestions[this.currentDeepDiveQuestionIndex].question}`
        } else {
          // 最近5年的经历已经梳理完成，询问是否继续梳理更早的经历
          const currentYear = new Date().getFullYear()
          const hasOlderExperiences = this.data.experiences.some(exp => {
            const endYear = exp.endTime === '至今' ? currentYear : parseInt(exp.endTime?.split('-')[0] || 0)
            return endYear < currentYear - 5
          })
          if (hasOlderExperiences) {
            this.needConfirmMoreDive = true
            return `✅ 最近5年的工作经历已经深度梳理完成！\n你还有更早的工作经历，是否需要继续进行深度梳理？（是/否）`
          } else {
            // 所有工作经历梳理完成
            this.isDeepDiving = false
            return '✅ 深度梳理完成！你的职业生涯档案已经非常完善了，随时可以生成简历或记录新的工作成长~'
          }
        }
      }
    }
    // 处理基础信息收集阶段（合并提问+智能提取+缺失追问）
    if (currentStep.key === 'basicInfoCollect' || this.missingBasicFields.length > 0) {
      // 提取用户输入的所有基础信息
      const extracted = this.extractBasicInfo(answer)
      // 合并到已有基础信息中
      this.data.basicInfo = { ...this.data.basicInfo, ...extracted }
      // 如果是第一次提交基础信息，检查必填字段是否缺失
      if (currentStep.key === 'basicInfoCollect') {
        this.missingBasicFields = this.basicInfoFields.filter(field => 
          field.required && !this.data.basicInfo[field.key]
        )
      } else {
        // 是补充缺失字段的回答，更新缺失列表
        this.missingBasicFields = this.missingBasicFields.filter(field => 
          field.required && !this.data.basicInfo[field.key]
        )
      }
      // 如果还有缺失字段，生成追问问题
      if (this.missingBasicFields.length > 0) {
        const missingLabels = this.missingBasicFields.map(f => f.label).join('、')
        return `请补充以下必填信息：${missingLabels}`
      } else {
        // 基础信息收集完成，进入下一步
        this.step++
        return this.onboardingSteps[this.step].question
      }
    }
    // 普通步骤的回答存储
    if (currentStep.field.length === 2) {
      const [parentKey, childKey] = currentStep.field
      if (!this.data[parentKey]) this.data[parentKey] = {}
      this.data[parentKey][childKey] = answer.trim()
    } else if (currentStep.field.length === 3) {
      const [parentKey, index, childKey] = currentStep.field
      if (!this.data[parentKey]) this.data[parentKey] = []
      if (!this.data[parentKey][index]) this.data[parentKey][index] = {}
      this.data[parentKey][index][childKey] = answer.trim()
    }
    this.step++
    // 判断是否还有下一步
    if (this.step < this.onboardingSteps.length) {
      const nextStep = this.onboardingSteps[this.step]
      // 处理添加更多工作经历的逻辑
      if (currentStep.key === 'addMoreExperience') {
        if (answer.trim() === '是' || answer.trim() === 'yes') {
          const expIndex = this.data.experiences.length
          // 插入新的工作经历步骤
          this.onboardingSteps.splice(this.step, 0,
            { key: `experience_${expIndex}_company`, question: `请问你第${expIndex+1}份工作的公司名称是什么？`, field: ['experiences', expIndex, 'company'] },
            { key: `experience_${expIndex}_position`, question: `请问你在这家公司担任的岗位是什么？`, field: ['experiences', expIndex, 'position'] },
            { key: `experience_${expIndex}_time`, question: `请问你入职和离职的时间是？`, field: ['experiences', expIndex, 'time'] },
            { key: `experience_${expIndex}_desc`, question: `请简单描述下你在这家公司的主要工作职责？`, field: ['experiences', expIndex, 'description'] },
            { key: `experience_${expIndex}_achievements`, question: `请问你在这家公司取得的主要业绩有哪些？`, field: ['experiences', expIndex, 'achievements'] },
            { key: 'addMoreExperience', question: '请问你还有其他工作经历需要记录吗？（是/否）', field: ['_meta', 'addMoreExperience'] }
          )
        }
      }
      // 处理深度梳理确认
      if (nextStep.key === 'deepDiveConfirm') {
        return nextStep.question
      }
      // 处理深度梳理确认的回答
      if (currentStep.key === 'deepDiveConfirm') {
        if (answer.trim() === '是' || answer.trim() === 'yes') {
          this.data._meta.deepDiveEnabled = true
          this.isDeepDiving = true
          this.currentDeepDiveExpIndex = 0
          this.currentDeepDiveQuestionIndex = 0
          this.needConfirmMoreDive = false
          // 优先筛选最近5年的工作经历进行深度梳理
          const currentYear = new Date().getFullYear()
          this.deepDiveExpList = this.data.experiences.filter(exp => {
            const endYear = exp.endTime === '至今' ? currentYear : parseInt(exp.endTime?.split('-')[0] || 0)
            return endYear >= currentYear - 5
          })
          // 如果没有最近5年的经历，用全部经历
          if (this.deepDiveExpList.length === 0) {
            this.deepDiveExpList = [...this.data.experiences]
          }
          // 开始第一段工作经历的深度梳理
          const exp = this.deepDiveExpList[this.currentDeepDiveExpIndex]
          return `### 开始深度梳理最近5年工作经历（第${this.currentDeepDiveExpIndex+1}/${this.deepDiveExpList.length}段）：${exp.company} - ${exp.position}\n${this.deepDiveQuestions[this.currentDeepDiveQuestionIndex].question}`
        } else {
          // 不进行深度梳理，结束引导
          return '✅ 初始化完成！你的职业生涯档案已经建立好了，你可以随时使用 /linkedcareer record 记录工作成长，或者 /linkedcareer resume 生成简历。'
        }
      }
      return nextStep.question
    }
    return '✅ 初始化完成！'
  }
  async getReminderQuestion(frequency = 'weekly') {
    const questions = {
      daily: '今天你完成了哪些重要工作？有没有掌握新的技能或者取得什么成果？',
      weekly: '本周你完成了哪些重要项目？有没有技能提升或者值得记录的业绩？遇到了什么挑战，是怎么解决的？',
      monthly: '本月你在工作上取得了哪些进展？能力上有什么提升？职业规划上有没有什么调整？'
    }
    return questions[frequency] || questions.weekly
  }
  getCollectedData() {
    // 移除元数据
    const { _meta, ...cleanData } = this.data
    // 移除工作经历中的深度梳理临时字段
    if (cleanData.experiences) {
      cleanData.experiences = cleanData.experiences.map(exp => {
        const { deepDive, ...rest } = exp
        return rest
      })
    }
    return cleanData
  }
}
module.exports = Interview
