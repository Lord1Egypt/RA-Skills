const fs = require('fs/promises')
const path = require('path')
class Resume {
  constructor() {
    this.templateDir = path.join(__dirname, '../../templates')
  }
  async loadTemplate(name) {
    const templatePath = path.join(this.templateDir, `${name}.md`)
    return await fs.readFile(templatePath, 'utf8')
  }
  async calculateMatchScore(jobJD, careerData) {
    let score = 0
    const reasons = []
    // 简单关键词匹配，后续可以优化为更智能的匹配
    const jdLower = jobJD.toLowerCase()
    // 匹配岗位名称
    if (jdLower.includes(careerData.basicInfo.expectedPosition?.toLowerCase() || '')) {
      score += 20
      reasons.push('岗位方向匹配')
    }
    // 匹配经验要求
    if (jdLower.includes('3年') || jdLower.includes('三年')) {
      const expYears = this.calculateExperienceYears(careerData)
      if (expYears >= 3) {
        score += 20
        reasons.push(`工作经验匹配（${expYears}年相关经验）`)
      }
    }
    // 匹配技能关键词
    const allSkills = []
    for (const skills of Object.values(careerData.skills || {})) {
      allSkills.push(...skills.map(s => s.toLowerCase()))
    }
    for (const skill of allSkills) {
      if (jdLower.includes(skill)) {
        score += 5
        reasons.push(`具备岗位要求的技能：${skill}`)
      }
    }
    // 匹配工作经历描述和职位
    for (const exp of careerData.experiences || []) {
      // 匹配职位
      if (exp.position && jdLower.includes(exp.position.toLowerCase())) {
        score += 15
        reasons.push(`岗位经验匹配：${exp.position}`)
      }
      // 匹配工作描述（中文优化：去掉"的"再匹配）
      if (exp.description) {
        const descClean = exp.description.toLowerCase().replace(/的/g, '')
        const jdClean = jdLower.replace(/的/g, '')
        if (jdClean.includes(descClean)) {
          score += 15
          reasons.push(`工作内容匹配：${exp.description}`)
        }
      }
    }
    // 匹配项目/业绩关键词（中文优化：取前6个字符匹配）
    const allAchievements = []
    for (const exp of careerData.experiences || []) {
      allAchievements.push(...(exp.achievements || []).map(a => a.toLowerCase()))
    }
    for (const achievement of allAchievements) {
      if (jdLower.includes(achievement.slice(0, 6))) {
        score += 10
        reasons.push(`有相关项目经验：${achievement}`)
      }
    }
    score = Math.min(score, 100)
    return {
      score,
      reasons,
      isRecommended: score >= 60
    }
  }
  calculateExperienceYears(careerData) {
    if (!careerData.experiences || careerData.experiences.length === 0) return 0
    let totalYears = 0
    for (const exp of careerData.experiences) {
      const startYear = parseInt(exp.startTime?.split('-')[0] || 0)
      const endYear = exp.endTime === '至今' ? new Date().getFullYear() : parseInt(exp.endTime?.split('-')[0] || startYear)
      totalYears += (endYear - startYear)
    }
    return Math.max(totalYears, 0)
  }
  sortByRelevance(items, jobJD) {
    const jdLower = jobJD.toLowerCase()
    return items.sort((a, b) => {
      const scoreA = this.calculateItemRelevance(a, jdLower)
      const scoreB = this.calculateItemRelevance(b, jdLower)
      return scoreB - scoreA
    })
  }
  calculateItemRelevance(item, jdLower) {
    let score = 0
    // 检查描述
    if (item.description && jdLower.includes(item.description.toLowerCase())) score += 10
    // 检查成就
    if (item.achievements) {
      for (const ach of item.achievements) {
        if (jdLower.includes(ach.toLowerCase())) score += 15
      }
    }
    // 检查职位/角色
    if (item.position && jdLower.includes(item.position.toLowerCase())) score += 5
    if (item.role && jdLower.includes(item.role.toLowerCase())) score += 5
    return score
  }
  async generate(careerData, options = {}) {
    const { mode = 'general', template = 'balanced', jobJD = null } = options
    // 加载模板
    let templateContent = await this.loadTemplate(`resume_${template}`)
    // 准备数据
    let data = { ...careerData.basicInfo }
    data.experiences = careerData.experiences || []
    data.projects = careerData.projects || []
    data.education = careerData.education || []
    data.skills = careerData.skills || {}
    // 如果是定向生成，优先展示匹配的内容
    if (mode === 'targeted' && jobJD) {
      const matchResult = await this.calculateMatchScore(jobJD, careerData)
      // 过滤经验和项目，优先展示匹配的
      data.experiences = this.sortByRelevance(data.experiences, jobJD)
      data.projects = this.sortByRelevance(data.projects, jobJD)
    }
    // 简单模板渲染，后续可以集成完整的模板引擎
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        templateContent = templateContent.replace(new RegExp(`{{${key}}}`, 'g'), value)
      }
    }
    // 渲染工作经历（使用贪婪匹配，因为有嵌套的endfor）
    const expMatch = templateContent.match(/{% for exp in experiences %}(.*){% endfor %}/s)
    if (expMatch) {
      let expContent = ''
      const expTemplate = expMatch[1]
      for (const exp of data.experiences) {
        let itemContent = expTemplate
        for (const [key, value] of Object.entries(exp)) {
          if (typeof value === 'string') {
            itemContent = itemContent.replace(new RegExp(`{{exp.${key}}}`, 'g'), value)
          }
        }
        // 单独处理成就列表（解决中文匹配问题）
        if (exp.achievements && exp.achievements.length > 0) {
          let achievementsContent = ''
          for (const ach of exp.achievements) {
            achievementsContent += `- ${ach}\n`
          }
          // 精确替换模板中的成就循环
          const forTag = '{% for achievement in exp.achievements %}'
          const endforTag = '{% endfor %}'
          const startIndex = itemContent.indexOf(forTag)
          const endIndex = itemContent.indexOf(endforTag, startIndex)
          if (startIndex !== -1 && endIndex !== -1) {
            itemContent = itemContent.substring(0, startIndex) + achievementsContent + itemContent.substring(endIndex + endforTag.length)
          }
          // 处理带slice的成就循环（用于极简模板）
          const sliceForTag = '{% for achievement in exp.achievements.slice(0, 2) %}'
          const sliceStartIndex = itemContent.indexOf(sliceForTag)
          const sliceEndIndex = itemContent.indexOf(endforTag, sliceStartIndex)
          if (sliceStartIndex !== -1 && sliceEndIndex !== -1) {
            let sliceContent = ''
            for (const ach of exp.achievements.slice(0, 2)) {
              sliceContent += `- ${ach}\n`
            }
            itemContent = itemContent.substring(0, sliceStartIndex) + sliceContent + itemContent.substring(sliceEndIndex + endforTag.length)
          }
          // 移除多余的endfor标签
          itemContent = itemContent.replace(/{%\s*endfor\s*%}/g, '')
        }
        expContent += itemContent
      }
      templateContent = templateContent.replace(expMatch[0], expContent)
    }
    // 渲染项目经验（如果有项目的话）
    if (data.projects && data.projects.length > 0) {
      const projectMatch = templateContent.match(/{% for project in projects.slice\\((\\d+),\\s*(\\d+)\\) %}(.*?){% endfor %}/s) || templateContent.match(/{% for project in projects %}(.*?){% endfor %}/s)
      if (projectMatch) {
        let projectContent = ''
        const projectTemplate = projectMatch[projectMatch.length - 1]
        const sliceMatch = projectMatch[0].match(/slice\((\d+),\s*(\d+)\)/)
        let projects = data.projects
        if (sliceMatch) {
          const start = parseInt(sliceMatch[1])
          const end = parseInt(sliceMatch[2])
          projects = projects.slice(start, end)
        }
        for (const project of projects) {
          let itemContent = projectTemplate
          for (const [key, value] of Object.entries(project)) {
            if (typeof value === 'string') {
              itemContent = itemContent.replace(new RegExp(`{{project.${key}}}`, 'g'), value)
            } else if (Array.isArray(value)) {
              const arrayMatch = itemContent.match(new RegExp(`{% for achievement in project.${key} %}(.*?){% endfor %}`, 's'))
              if (arrayMatch) {
                const arrayTemplate = arrayMatch[1]
                let arrayContent = ''
                for (const item of value) {
                  arrayContent += arrayTemplate.replace(`{{achievement}}`, item)
                }
                itemContent = itemContent.replace(arrayMatch[0], arrayContent)
              }
            }
          }
          projectContent += itemContent
        }
        templateContent = templateContent.replace(projectMatch[0], projectContent)
      }
    } else {
      // 没有项目经验，移除整个项目经验模块
      templateContent = templateContent.replace(/---\s*## 项目经验.*?(?=---|$)/s, '')
    }
    // 渲染教育经历
    const eduMatch = templateContent.match(/{% for edu in education %}(.*?){% endfor %}/s)
    if (eduMatch) {
      let eduContent = ''
      const eduTemplate = eduMatch[1]
      for (const edu of data.education) {
        let itemContent = eduTemplate
        for (const [key, value] of Object.entries(edu)) {
          if (typeof value === 'string') {
            itemContent = itemContent.replace(new RegExp(`{{edu.${key}}}`, 'g'), value)
          }
        }
        eduContent += itemContent
      }
      templateContent = templateContent.replace(eduMatch[0], eduContent)
    }
    // 渲染技能
    const skillMatch = templateContent.match(/{% for category, skills in skills %}(.*?){% endfor %}/s)
    if (skillMatch && data.skills && Object.keys(data.skills).length > 0) {
      let skillContent = ''
      const skillTemplate = skillMatch[1]
      for (const [category, skills] of Object.entries(data.skills)) {
        let itemContent = skillTemplate
        itemContent = itemContent.replace('{{category}}', category)
        // 处理技能数组
        const arrayMatch = itemContent.match(/{% for skill in skills %}(.*?){% endfor %}/s)
        if (arrayMatch) {
          const arrayTemplate = arrayMatch[1]
          let arrayContent = ''
          for (const skill of skills) {
            arrayContent += arrayTemplate.replace('{{skill}}', skill)
          }
          itemContent = itemContent.replace(arrayMatch[0], arrayContent)
        } else {
          // 处理join形式
          itemContent = itemContent.replace('{{skills.join(\', \')}}', skills.join(', '))
          itemContent = itemContent.replace('{{skills.join(\'、\')}}', skills.join('、'))
        }
        skillContent += itemContent
      }
      templateContent = templateContent.replace(skillMatch[0], skillContent)
    } else {
      // 没有技能，移除技能模块
      templateContent = templateContent.replace(/---\s*## 核心技能.*?(?=---|$)/s, '')
    }
    return templateContent
  }
  async generateCoverLetter(careerData, jobJD) {
    const templateContent = await this.loadTemplate('cover_letter')
    const matchResult = await this.calculateMatchScore(jobJD, careerData)
    const experienceYears = this.calculateExperienceYears(careerData)
    const currentDate = new Date().toLocaleDateString('zh-CN')
    // 准备数据
    let data = {
      ...careerData.basicInfo,
      experienceYears,
      currentDate,
      matchingHighlights: matchResult.reasons
    }
    // 渲染基本变量
    let rendered = templateContent
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string' || typeof value === 'number') {
        rendered = rendered.replace(new RegExp(`{{${key}}}`, 'g'), value)
      }
    }
    // 渲染匹配亮点
    const highlightMatch = rendered.match(/{% for highlight in matchingHighlights %}(.*?){% endfor %}/s)
    if (highlightMatch) {
      let highlightContent = ''
      const highlightTemplate = highlightMatch[1]
      for (const highlight of data.matchingHighlights) {
        highlightContent += highlightTemplate.replace('{{highlight}}', highlight)
      }
      rendered = rendered.replace(highlightMatch[0], highlightContent)
    }
    return rendered
  }

  // 生成导出格式提示
  getExportTips() {
    return `
---
### 📄 导出格式支持
已生成Markdown格式简历，可通过以下方式导出为PDF/Word：
1. **本地导出**：调用已安装的 \`pdf-generator\` 和 \`word-generator\` 技能，可直接生成符合商务排版标准的文件
2. **飞书发送**：申请飞书权限后，可直接发送PDF/Word版本到你的飞书账号
3. **专业排版优化说明**：
   - 采用行业标准简历页边距：上下2.5cm，左右2cm
   - 使用商务首选字体：中文（微软雅黑/思源黑体）、英文（Arial/Calibri）
   - 层级清晰：标题加粗放大，项目符号统一，行距1.25倍
   - 自动优化分页，避免重要内容被截断

需要导出其他格式或调整排版风格可以随时告诉我~
`
  }

  // 获取专业排版方案说明
  getProfessionalFormattingPlan() {
    return {
      pdf: {
        recommendedTool: 'puppeteer + wkhtmltopdf',
        template: '专业商务简历模板（支持自定义配色）',
        features: [
          '支持页眉页脚配置，可添加个人logo/联系方式',
          '矢量字体渲染，打印无锯齿',
          '自动压缩文件大小，方便邮件发送',
          '支持水印、页码等高级功能'
        ]
      },
      word: {
        recommendedTool: 'pandoc + docx-templates',
        template: '符合HR阅读习惯的标准简历模板',
        features: [
          '生成可编辑的Word文件，方便用户后续自行调整',
          '样式与Markdown完全对应，无格式错乱',
          '支持自定义样式集，匹配不同行业风格（互联网/金融/国企等）',
          '自动生成目录和标题层级'
        ]
      },
      commonOptimizations: [
        '关键信息前置：个人信息+求职意向放在最前面',
        '经历按倒序排列，最近经历优先展示',
        '量化成就突出显示，使用数字加粗效果',
        '避免花哨设计，整体风格简洁专业，符合ATS系统识别标准'
      ]
    }
  }

  // 自动提取核心亮点
  extractCoreHighlights(careerData) {
    const highlights = []
    // 提取荣誉
    if (careerData.basicInfo.honors) {
      highlights.push(...careerData.basicInfo.honors)
    }
    // 提取管理规模
    careerData.experiences.forEach(exp => {
      exp.achievements.forEach(ach => {
        // 匹配百亿、十亿、亿、千万级业绩
        if (ach.includes('亿') || ach.includes('千万') || ach.includes('百亿') || ach.includes('团队') || ach.includes('合伙人')) {
          highlights.push(ach)
        }
      })
    })
    // 最多取5个核心亮点
    return highlights.slice(0, 5)
  }

  // 生成专业PDF简历【开发中，下版本上线】
  async generateProfessionalPDF(careerData, outputPath, options = {}) {
    throw new Error('PDF生成功能正在开发中，当前版本支持导出Markdown和Word格式，感谢您的理解~')
  }

  // 生成专业Word简历
  async generateProfessionalWord(careerData, outputPath, options = { industry: 'internet' }) {
    const fs = require('fs/promises')
    const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle } = require('docx')

    // 构建文档内容
    const doc = new Document({
      styles: {
        default: {
          heading1: {
            run: {
              size: 28,
              bold: true,
              color: "2E86AB",
            },
            paragraph: {
              spacing: { after: 200 },
              alignment: AlignmentType.CENTER,
            }
          },
          heading2: {
            run: {
              size: 24,
              bold: true,
              color: "2E86AB",
            },
            paragraph: {
              spacing: { before: 300, after: 100 },
              border: {
                bottom: {
                  color: "2E86AB",
                  space: 1,
                  size: 6,
                  style: BorderStyle.SINGLE,
                }
              }
            }
          },
        },
        paragraphStyles: [
          {
            id: "contactInfo",
            name: "Contact Info",
            run: { size: 20 },
            paragraph: { alignment: AlignmentType.CENTER, spacing: { after: 200 } }
          },
          {
            id: "jobTitle",
            name: "Job Title",
            run: { size: 22, bold: true },
            paragraph: { spacing: { before: 200, after: 100 } }
          },
          {
            id: "jobMeta",
            name: "Job Meta",
            run: { size: 20, color: "666666" },
            paragraph: { spacing: { after: 100 } }
          },
          {
            id: "listItem",
            name: "List Item",
            run: { size: 20 },
            paragraph: { indent: { left: 360 }, spacing: { after: 60 } }
          }
        ]
      },
      sections: [{
        properties: {
          page: {
            margin: {
              top: 1440, right: 1134, bottom: 1440, left: 1134 // 2.5cm上下，2cm左右
            }
          }
        },
        children: [
          // 姓名
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun(careerData.basicInfo.name)]
          }),
          // 联系方式
          new Paragraph({
            style: "contactInfo",
            children: [
              new TextRun(`电话：${careerData.basicInfo.phone} | 邮箱：${careerData.basicInfo.email} | 所在城市：${careerData.basicInfo.city} | 期望岗位：${careerData.basicInfo.expectedPosition || ''}`)
            ]
          }),
          // 核心亮点
          new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("核心亮点")] }),
          ...this.extractCoreHighlights(careerData).map(h => new Paragraph({
            style: "listItem",
            children: [new TextRun("• " + h)]
          })),
          // 工作经历
          new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("工作经历")] }),
          ...careerData.experiences.flatMap(exp => [
            new Paragraph({
              style: "jobTitle",
              children: [new TextRun(`${exp.company} · ${exp.position}`)]
            }),
            new Paragraph({
              style: "jobMeta",
              children: [new TextRun(`时间：${exp.startTime} - ${exp.endTime}`)]
            }),
            new Paragraph({
              children: [new TextRun({ text: "工作职责：", bold: true }), new TextRun(exp.description)]
            }),
            new Paragraph({ children: [new TextRun({ text: "主要业绩：", bold: true })] }),
            ...exp.achievements.map(ach => new Paragraph({
              style: "listItem",
              children: [new TextRun("• " + ach)]
            }))
          ]),
          // 核心技能
          new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("核心技能")] }),
          ...Object.entries(careerData.skills || {}).map(([category, skills]) => new Paragraph({
            children: [new TextRun({ text: `${category}：`, bold: true }), new TextRun(skills.join('、'))]
          })),
          // 教育经历
          new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("教育经历")] }),
          ...careerData.education.map(edu => new Paragraph({
            style: "listItem",
            children: [new TextRun(`• ${edu.school} · ${edu.major} · ${edu.degree || '本科'}（${edu.startTime} - ${edu.endTime}）`)]
          }))
        ]
      }]
    })

    // 生成并保存Word文件
    const buffer = await Packer.toBuffer(doc)
    await fs.writeFile(outputPath, buffer)
    return outputPath
  }
}
module.exports = Resume
