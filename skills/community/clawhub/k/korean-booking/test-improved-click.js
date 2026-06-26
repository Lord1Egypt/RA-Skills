/**
 * 测试改进后的 clickConsultButton 函数
 */
const skill = require('./api/skill.js')
const hospitals = require('./data/hospitals.json')

async function testImprovedClick() {
  console.log('\n🧪 测试改进后的咨询按钮点击\n')

  // 构造输入
  const jdHospital = hospitals.find(h => h.name.includes('JD') || h.name.includes('皮肤科'))
  const input = {
    query: '咨询客服',
    lang: 'zh',
    context: {
      hospital: jdHospital
    }
  }

  console.log(`🏥 医院: ${jdHospital.name}`)
  console.log(`📍 URL: ${jdHospital.url}`)
  console.log(`💬 查询: ${input.query}\n`)

  try {
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`⏳ 调用 skill 函数...`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const result = await skill(input)

    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📋 Skill 返回结果`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)
    console.log(result)

  } catch (err) {
    console.error('❌ 错误:', err.message)
    console.error(err.stack)
  }

  console.log('\n✅ 测试完成')
}

testImprovedClick()
