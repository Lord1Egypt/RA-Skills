// 自然语言查询预处理层
// 从用户输入中提取医院名关键词，去除常见干扰词

const STOP_PHRASES = [
  // 预约动作词
  '怎么预约', '如何预约', '预约流程', '怎么挂号', '在哪预约', '预约',
  '怎么去', '怎么联系', '联系方式', '地址', '电话',
  '我想约一下', '我想预约', '我要预约', '想预约', '要预约',
  '帮我预约', '帮我查', '帮我找', '帮我',

  // 意图前缀词（新增）
  '我现在在', '我打算去', '我想去', '我要去', '我打算', '我想在',
  '我要做', '我想做', '打算做', '想去做', '要去做',
  '我想', '我要', '想去', '打算',

  // 地域词（新增）——放在意图词后面，避免"在韩国"残留"在"
  '在韩国', '去韩国', '在首尔', '去首尔', '到韩国', '到首尔',
  '韩国', '首尔',

  // 项目/品类通用词（新增）——这些词独立存在时是品类，不是医院名
  '皮肤管理', '做脸', '整形手术', '美容手术', '医美项目',
  '双眼皮', '隆鼻', '吸脂', '注射', '激光', '光子',
  '做皮肤', '做美容', '做整形',
  '美容', '整形', '皮肤科',

  // 推荐询问词（新增）
  '哪家好', '哪里好', '哪个好', '哪家比较好', '推荐一下', '推荐',
  '哪家', '哪里', '好不好', '靠谱吗', '怎么样',
  '有啥推荐', '有什么推荐', '有哪些',

  // 通用机构词——独立存在时无意义，清洗掉避免误匹配医院名
  '整形外科医院', '整形医院', '皮肤科医院', '医美医院', '医美机构',
  '机构', '诊所', '医院',

  // 单独的询问词"好"会误匹配含"好"的医院名（如"好手艺医院"）
  // 必须放在复合词（哪家好/好不好）之后，单独的"好"才清洗
  '好',

  // 礼貌用语
  '请问', '你好', '您好', '谢谢', '谢谢啦', '谢谢啊',

  // 语气词
  '的', '了', '呢', '啊', '呀', '吧', '哦'
]

// 按长度降序排序，优先匹配长短语
const SORTED_STOP_PHRASES = [...STOP_PHRASES].sort((a, b) => b.length - a.length)

/**
 * 从自然语言查询中提取医院名关键词
 * @param {string} query 用户原始输入
 * @returns {string} 清理后的关键词
 */
function extractHospitalKeyword(query) {
  if (!query || typeof query !== 'string') return ''
  
  let cleaned = query.trim()
  
  // 1. 移除常见干扰短语
  for (const phrase of SORTED_STOP_PHRASES) {
    const regex = new RegExp(phrase, 'gi')
    cleaned = cleaned.replace(regex, '')
  }
  
  // 2. 移除多余空格和标点
  cleaned = cleaned
    .replace(/[，,。.!?？、；;]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()

  // 3. 去除清洗后开头残留的单字介词/动词（如"去CNP"→"CNP"，"做CNP"→"CNP"）
  cleaned = cleaned.replace(/^[去在到做]\s*/u, '').trim()
  
  // 3. 如果清理后为空，说明没有医院名关键词，返回空字符串
  // ⚠️ 不要回退到原始 query，否则 resolver 会对无意义的通用词做误匹配
  return cleaned
}

/**
 * 测试用例
 */
function testPreprocessor() {
  const cases = [
    'CNP皮肤科怎么预约',
    '我想约一下JD皮肤科',
    '请问JD皮肤科的联系方式',
    'CNP狎鸥亭店地址',
    'JD Skin Clinic appointment',
    'cnp',
    '韩国jd',
    '皮', // 单字
    '不存在医院怎么预约'
  ]
  
  console.log('=== 预处理测试 ===')
  for (const q of cases) {
    const extracted = extractHospitalKeyword(q)
    console.log(`"${q}" → "${extracted}"`)
  }
}

// 导出供测试
if (require.main === module) {
  testPreprocessor()
}

module.exports = { extractHospitalKeyword }