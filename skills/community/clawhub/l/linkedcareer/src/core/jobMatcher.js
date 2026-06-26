const fs = require('fs/promises')
const path = require('path')
const Resume = require('./resume')
class JobMatcher {
  constructor() {
    this.resume = new Resume()
  }
  // 批量匹配多个JD
  async batchMatch(careerData, jdList, options = {}) {
    const results = []
    console.log(`🔍 正在匹配 ${jdList.length} 个岗位...\n`)
    for (let i = 0; i < jdList.length; i++) {
      const jd = jdList[i]
      const matchResult = await this.resume.calculateMatchScore(jd.content, careerData)
      results.push({
        id: i + 1,
        title: jd.title || `岗位${i+1}`,
        company: jd.company || '未知公司',
        location: jd.location || '未知地点',
        salary: jd.salary || '薪资面议',
        jdContent: jd.content,
        matchScore: matchResult.score,
        matchReasons: matchResult.reasons,
        isRecommended: matchResult.isRecommended
      })
    }
    // 按匹配度从高到低排序
    results.sort((a, b) => b.matchScore - a.matchScore)
    return results
  }
  // 解析用户粘贴的JD文本，自动分割多个JD
  parseJdList(rawText) {
    // 简单分割：按照"岗位名称"、"公司名称"、"【岗位】"、"===="等关键词分割
    const jdList = []
    // 先按换行分割
    const lines = rawText.split('\n').map(line => line.trim()).filter(line => line.length > 0)
    let currentJd = { title: '', company: '', content: '' }
    for (const line of lines) {
      // 判断是否是新JD的开头
      if (
        line.includes('岗位') || 
        line.includes('招聘') || 
        line.includes('【') || 
        line.includes('公司名称') ||
        line.match(/^.{2,10}[-|一|到]?\d*k/i) // 匹配薪资开头，比如"20-30K"
      ) {
        if (currentJd.content.length > 100) {
          jdList.push({ ...currentJd })
        }
        currentJd = { title: line, company: '', content: line + '\n' }
        // 尝试提取公司名称
        const companyMatch = line.match(/(?:公司|企业)名称?[：:]?\s*([^\n，。；]+)/)
        if (companyMatch) currentJd.company = companyMatch[1]
        // 尝试提取薪资
        const salaryMatch = line.match(/(\d{1,2}[-|到|至]\d{1,2}k)/i)
        if (salaryMatch) currentJd.salary = salaryMatch[1]
        // 尝试提取工作地点
        const locationMatch = line.match(/(?:工作地点|地点|城市)[：:]?\s*([^\n，。；]+)/)
        if (locationMatch) currentJd.location = locationMatch[1]
      } else {
        currentJd.content += line + '\n'
      }
    }
    if (currentJd.content.length > 100) {
      jdList.push({ ...currentJd })
    }
    return jdList
  }
  // 输出匹配结果
  formatResults(results, topN = 5) {
    let output = '📋 岗位匹配结果（按匹配度从高到低排序）：\n\n'
    const topResults = results.slice(0, topN)
    topResults.forEach((result, index) => {
      output += `🏆 第${index+1}名：${result.title} @ ${result.company}\n`
      output += `   匹配度：${result.matchScore}/100 ${result.isRecommended ? '✅ 推荐投递' : '⚠️ 谨慎投递'}\n`
      output += `   薪资：${result.salary} | 地点：${result.location}\n`
      output += `   匹配亮点：\n`
      result.matchReasons.forEach(reason => {
        output += `     ✅ ${reason}\n`
      })
      output += '\n'
    })
    if (results.length > topN) {
      output += `... 还有${results.length - topN}个岗位，匹配度从${results[topN]?.matchScore || 0}分往下\n`
    }
    output += `\n💡 提示：可以直接选择匹配度最高的岗位，生成定向适配的简历和求职信哦~`
    return output
  }
}
module.exports = JobMatcher
