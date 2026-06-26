const fs = require('fs/promises')
const path = require('path')
class Memory {
  constructor(dataDir = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw/workspace/LinkedCareer/user_data')) {
    this.dataDir = dataDir
    this.jsonPath = path.join(dataDir, 'career_data.json')
    this.mdPath = path.join(dataDir, 'career_records.md')
  }
  async ensureDir() {
    await fs.mkdir(this.dataDir, { recursive: true })
  }
  async save(data) {
    await this.ensureDir()
    await fs.writeFile(this.jsonPath, JSON.stringify(data, null, 2), 'utf8')
    await this.generateMarkdown(data)
  }
  async load() {
    try {
      const content = await fs.readFile(this.jsonPath, 'utf8')
      return JSON.parse(content)
    } catch (e) {
      return {
        basicInfo: {},
        education: [],
        experiences: [],
        skills: [],
        projects: []
      }
    }
  }
  async generateMarkdown(data) {
    let md = '# 职业生涯档案\n\n'
    md += '## 基本信息\n'
    for (const [key, value] of Object.entries(data.basicInfo || {})) {
      md += `- ${key}: ${value}\n`
    }
    md += '\n## 教育经历\n'
    for (const edu of data.education || []) {
      md += `### ${edu.school} - ${edu.major} (${edu.startTime} - ${edu.endTime})\n`
      if (edu.description) md += `${edu.description}\n`
      md += '\n'
    }
    md += '## 工作经历\n'
    for (const exp of data.experiences || []) {
      md += `### ${exp.company} - ${exp.position} (${exp.startTime} - ${exp.endTime || '至今'})\n`
      if (exp.description) md += `${exp.description}\n`
      if (exp.achievements && exp.achievements.length > 0) {
        md += '#### 主要业绩\n'
        for (const achievement of exp.achievements) {
          md += `- ${achievement}\n`
        }
      }
      md += '\n'
    }
    md += '## 项目经验\n'
    for (const project of data.projects || []) {
      md += `### ${project.name} (${project.time})\n`
      md += `- 角色：${project.role}\n`
      md += `- 描述：${project.description}\n`
      if (project.achievements && project.achievements.length > 0) {
        md += '- 成果：\n'
        for (const achievement of project.achievements) {
          md += `  - ${achievement}\n`
        }
      }
      md += '\n'
    }
    md += '## 技能栈\n'
    for (const [category, skills] of Object.entries(data.skills || {})) {
      md += `### ${category}\n`
      md += skills.join(', ') + '\n\n'
    }
    await fs.writeFile(this.mdPath, md, 'utf8')
    return md
  }
  async exportMarkdown() {
    try {
      return await fs.readFile(this.mdPath, 'utf8')
    } catch (e) {
      const data = await this.load()
      return await this.generateMarkdown(data)
    }
  }
  async importResume(content, type = 'text') {
    const data = await this.load()
    // 简单解析简历文本，后续可以优化解析逻辑
    // 解析姓名
    const nameMatch = content.match(/(?:姓名|名字)[：:]\s*([^\n\r]+)/) || content.match(/^\s*#\s*([^\n\r]+)/m)
    if (nameMatch) data.basicInfo.name = nameMatch[1].trim()
    // 解析电话
    const phoneMatch = content.match(/(?:电话|手机|联系方式)[：:]\s*([1][3-9]\d{9})/)
    if (phoneMatch) data.basicInfo.phone = phoneMatch[1].trim()
    // 解析邮箱
    const emailMatch = content.match(/(?:邮箱|email)[：:]\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/i)
    if (emailMatch) data.basicInfo.email = emailMatch[1].trim()
    // 解析工作经历
    const expMatches = content.matchAll(/(?:工作经历|工作经验)\s*([\s\S]*?)(?=\n##|\n#|$)/g)
    for (const expMatch of expMatches) {
      const expContent = expMatch[1]
      // 匹配两种格式："### 公司 - 职位 (时间)" 和 "### 公司 职位 时间"
      const expItems = expContent.matchAll(/###?\s*([^\n]+?)(?:\s*[-|至]\s*|\s+)([^\n(]+?)\s*(?:\(([^)]+)\)|([\d-]+至今))?/g)
      for (const item of expItems) {
        const company = item[1].trim()
        const position = item[2].trim()
        const time = item[3] || item[4] || ''
        data.experiences.push({
          company,
          position,
          startTime: time.split('-')[0]?.trim() || '',
          endTime: time.split('-')[1]?.trim() || '至今'
        })
      }
    }
    await this.save(data)
    return data
  }
}
module.exports = Memory
