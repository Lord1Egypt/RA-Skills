/**
 * 八字缘分匹配 - 八字计算模块
 * 根据出生日期时间计算八字
 */

// 天干
const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 地支
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 天干对应的五行
const TG_WUXING = {
  '甲': '木', '乙': '木',
  '丙': '火', '丁': '火',
  '戊': '土', '己': '土',
  '庚': '金', '辛': '金',
  '壬': '水', '癸': '水'
};

// 地支对应的五行
const DZ_WUXING = {
  '子': '水', '丑': '土', '寅': '木', '卯': '木',
  '辰': '土', '巳': '火', '午': '火', '未': '土',
  '申': '金', '酉': '金', '戌': '土', '亥': '水'
};

// 地支藏干表
const DZ_CANG_GAN = {
  '子': ['癸'],
  '丑': ['己', '癸', '辛'],
  '寅': ['甲', '丙', '戊'],
  '卯': ['乙'],
  '辰': ['戊', '乙', '癸'],
  '巳': ['丙', '庚', '戊'],
  '午': ['丁', '己'],
  '未': ['己', '丁', '乙'],
  '申': ['庚', '壬', '戊'],
  '酉': ['辛'],
  '戌': ['戊', '辛', '丁'],
  '亥': ['壬', '甲']
};

// 五行
const WUXING = ['木', '火', '土', '金', '水'];

// 五行相生关系
const WUXING_SHENG = {
  '木': '火',
  '火': '土',
  '土': '金',
  '金': '水',
  '水': '木'
};

// 五行相克关系
const WUXING_KE = {
  '木': '土',
  '火': '金',
  '土': '水',
  '金': '木',
  '水': '火'
};

// 节气对应地支（简化）
const JIE_QI_DZ = {
  '立春': '寅', '雨水': '寅',
  '惊蛰': '卯', '春分': '卯',
  '清明': '辰', '谷雨': '辰',
  '立夏': '巳', '小满': '巳',
  '芒种': '午', '夏至': '午',
  '小暑': '未', '大暑': '未',
  '立秋': '申', '处暑': '申',
  '白露': '酉', '秋分': '酉',
  '寒露': '戌', '霜降': '戌',
  '立冬': '亥', '小雪': '亥',
  '大雪': '子', '冬至': '子',
  '小寒': '丑', '大寒': '丑'
};

/**
 * 计算指定年份的天干
 */
function getYearGan(year) {
  // 1984年是甲子年
  const offset = (year - 1984) % 10;
  return offset >= 0 ? TIAN_GAN[offset] : TIAN_GAN[offset + 10];
}

/**
 * 计算指定年份的地支
 */
function getYearZhi(year) {
  // 1984年是子年
  const offset = (year - 1984) % 12;
  return offset >= 0 ? DI_ZHI[offset] : DI_ZHI[offset + 12];
}

/**
 * 计算月干（需要年干配合）
 * @param yearGan 年干
 * @param month 月份（1-12）
 */
function getMonthGan(yearGan, month) {
  // 五虎遁年起月表
  const monthGanIndex = {
    '甲': 2, '乙': 3, '丙': 4, '丁': 5, '戊': 6,
    '己': 7, '庚': 8, '辛': 9, '壬': 10, '癸': 0
  };
  
  const startIndex = monthGanIndex[yearGan];
  const ganIndex = (startIndex + month - 1) % 10;
  return TIAN_GAN[ganIndex];
}

/**
 * 获取月支
 */
function getMonthZhi(month) {
  // 正月为寅
  return DI_ZHI[(month + 1) % 12];
}

/**
 * 计算日干（简化版，需要考虑闰年）
 * 这里使用一个简化算法，实际应该用万年历
 */
function getDayGan(dayOfYear, year) {
  // 假设1月1日为甲子日
  const offset = (dayOfYear - 1) % 10;
  return TIAN_GAN[offset];
}

/**
 * 获取日支
 */
function getDayZhi(dayOfYear, year) {
  const offset = (dayOfYear - 1) % 12;
  return DI_ZHI[offset];
}

/**
 * 计算时干（需要日干配合）
 * @param dayGan 日干
 * @param hour 小时（0-23）
 */
function getHourGan(dayGan, hour) {
  // 五鼠遁日起时表
  const hourGanIndex = {
    '甲': 0, '乙': 1, '丙': 2, '丁': 3, '戊': 4,
    '己': 5, '庚': 6, '辛': 7, '壬': 8, '癸': 9
  };
  
  // 时支索引（子时=23-1点，对应索引0）
  const hourZhiIndex = Math.floor((hour + 1) / 2) % 12;
  
  const startIndex = hourGanIndex[dayGan];
  const ganIndex = (startIndex + hourZhiIndex) % 10;
  return TIAN_GAN[ganIndex];
}

/**
 * 获取时支
 */
function getHourZhi(hour) {
  const hourZhiIndex = Math.floor((hour + 1) / 2) % 12;
  return DI_ZHI[hourZhiIndex];
}

/**
 * 计算八字
 * @param birthDate 出生日期 YYYY-MM-DD
 * @param birthHour 出生小时 0-23
 */
function calculateBazi(birthDate, birthHour) {
  const date = new Date(birthDate);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  // 计算年中第几天
  const startOfYear = new Date(year, 0, 0);
  const dayOfYear = Math.floor((date - startOfYear) / (1000 * 60 * 60 * 24));
  
  // 年柱
  const yearGan = getYearGan(year);
  const yearZhi = getYearZhi(year);
  
  // 月柱
  const monthGan = getMonthGan(yearGan, month);
  const monthZhi = getMonthZhi(month);
  
  // 日柱（简化版）
  const dayGan = getDayGan(dayOfYear, year);
  const dayZhi = getDayZhi(dayOfYear, year);
  
  // 时柱
  const hourGan = getHourGan(dayGan, birthHour);
  const hourZhi = getHourZhi(birthHour);
  
  return {
    year: yearGan + yearZhi,
    month: monthGan + monthZhi,
    day: dayGan + dayZhi,
    hour: hourGan + hourZhi,
    yearGan, yearZhi,
    monthGan, monthZhi,
    dayGan, dayZhi,
    hourGan, hourZhi
  };
}

/**
 * 获取五行
 */
function getWuxing(tianGan, diZhi) {
  return {
    tg: TG_WUXING[tianGan],
    dz: DZ_WUXING[diZhi]
  };
}

/**
 * 计算两柱之间的匹配度
 */
function calculateColumnMatch(tg1, dz1, tg2, dz2) {
  const w1 = getWuxing(tg1, dz1);
  const w2 = getWuxing(tg2, dz2);
  
  // 主要看日干的五行
  const dayWuxing1 = w1.tg;
  const dayWuxing2 = w2.tg;
  
  // 相生
  if (WUXING_SHENG[dayWuxing1] === dayWuxing2 || WUXING_SHENG[dayWuxing2] === dayWuxing1) {
    return 100;
  }
  
  // 比和
  if (dayWuxing1 === dayWuxing2) {
    return 80;
  }
  
  // 相克
  if (WUXING_KE[dayWuxing1] === dayWuxing2 || WUXING_KE[dayWuxing2] === dayWuxing1) {
    return 50;
  }
  
  return 40;
}

/**
 * 计算整体匹配度
 */
function calculateMatchScore(bazi1, bazi2) {
  // 年柱 20%
  const yearScore = calculateColumnMatch(
    bazi1.yearGan, bazi1.yearZhi,
    bazi2.yearGan, bazi2.yearZhi
  ) * 0.2;
  
  // 月柱 25%
  const monthScore = calculateColumnMatch(
    bazi1.monthGan, bazi1.monthZhi,
    bazi2.monthGan, bazi2.monthZhi
  ) * 0.25;
  
  // 日柱 30%（最重要）
  const dayScore = calculateColumnMatch(
    bazi1.dayGan, bazi1.dayZhi,
    bazi2.dayGan, bazi2.dayZhi
  ) * 0.3;
  
  // 时柱 25%
  const hourScore = calculateColumnMatch(
    bazi1.hourGan, bazi1.hourZhi,
    bazi2.hourGan, bazi2.hourZhi
  ) * 0.25;
  
  return yearScore + monthScore + dayScore + hourScore;
}

/**
 * 纯规则扩写：按总分 + 四柱单项分生成多段解读（不调大模型）
 */
function buildExpandedInterpretation(score, columnScores) {
  const { year, month, day, hour } = columnScores;

  const opening =
    score >= 85
      ? '你们整体契合度较高，缘分明朗、互动较顺。'
      : score >= 70
        ? '你们整体较为合拍，有较好的相处基础。'
        : score >= 55
          ? '你们存在一定差异，更需要耐心磨合，而不是一味加速推进。'
          : '你们契合度偏低，不必强求节奏完全一致；从轻松、低压的互动开始更稳。';

  const colLine = (label, sc) => {
    if (sc >= 100) return `${label}五行气机相生，对关系整体有加分。`;
    if (sc >= 80) return `${label}同质相助，价值观与日常习惯更容易对齐。`;
    if (sc >= 50) return `${label}带有一定克制感，沟通时尽量避免硬碰硬。`;
    return `${label}差异较明显，适合循序渐进建立信任。`;
  };

  const matchPoints = [
    `1) ${colLine('日柱', day)}`,
    `2) ${colLine('月柱', month)}`,
    `3) ${colLine('时柱', hour)}`,
    `4) ${colLine('年柱', year)}`,
  ].join('\n');

  let getAlong = '';
  if (score >= 85) {
    getAlong =
      '【相处建议】\n' +
      '- 关系升温不妨配合稳定节奏：既保留仪式感，也给彼此留白。\n' +
      '- 遇到分歧先对齐目标，再讨论细节，更容易一条心。\n' +
      '- 把「互相欣赏的点」常说出口，小成本高回报。';
  } else if (score >= 70) {
    getAlong =
      '【相处建议】\n' +
      '- 重要事项尽量说清楚预期，减少「我以为你懂」的落差。\n' +
      '- 争执时先降温再复盘：谁先给台阶不重要，重要的是别隔夜冷暴力。\n' +
      '- 安排一些共同完成的小事（旅行计划、兴趣打卡），利于积累默契。';
  } else if (score >= 55) {
    getAlong =
      '【相处建议】\n' +
      '- 前期宁可慢一点：把边界、频率、联络方式对齐，会省很多误会。\n' +
      '- 差异不等于不对，关键是把期待调成可执行的小步骤。\n' +
      '- 给对方反馈时用「事实 + 感受 + 请求」，比指责更容易听进去。';
  } else {
    getAlong =
      '【相处建议】\n' +
      '- 若以长期关系为目标，建议先当稳定的朋友相处一段，再谈承诺。\n' +
      '- 不强求「立刻同频」，保留各自节奏，反而更不容易透支耐心。\n' +
      '- 明确哪些是可商量、哪些是底线，减少反复试探的内耗。';
  }

  const entries = [
    { key: '年柱', sc: year },
    { key: '月柱', sc: month },
    { key: '日柱', sc: day },
    { key: '时柱', sc: hour },
  ];
  const weakest = entries.reduce((a, b) => (a.sc <= b.sc ? a : b));
  const strongest = entries.reduce((a, b) => (a.sc >= b.sc ? a : b));
  const allColEqual = entries.every(e => e.sc === entries[0].sc);

  let watchOut;
  if (allColEqual || weakest.key === strongest.key) {
    watchOut =
      '【需要注意】\n' +
      '- 四柱单项在当前规则下没有明显「拖后腿」的一柱；摩擦往往来自习惯、节奏或期待差。\n' +
      '- 不必把一次争执定义为「不合适」，先区分是情绪还是原则问题再处理。\n' +
      '- 当出现对立感时，先从「我们能共同接受的一条小规则」切入，比争输赢更有效。';
  } else {
    watchOut =
      '【需要注意】\n' +
      `- 当前四柱里相对吃力的是「${weakest.key}」：相处中这里更容易触发拉扯感。\n` +
      `- 不必把一次摩擦上升为「不合适」；把它当成需要额外沟通成本的区域即可。\n` +
      `- 「${strongest.key}」是你们相对顺的一柱，可从共同点切入，降低对立情绪。`;
  }

  let boost;
  if (score >= 70) {
    boost =
      '【提升方向】\n' +
      (allColEqual || weakest.key === strongest.key
        ? '- 用「可重复」的小仪式（固定约会、固定复盘时间）巩固默契，比一次大张旗鼓的承诺更稳。\n'
        : `- 围绕「${strongest.key}」的长处多创造正向体验，会带动整体氛围。\n`) +
      '- 生活作息、社交半径、消费观这三块若有分歧，越早坦诚越容易找到折中。\n' +
      '- 保持各自成长：关系稳定往往来自两个人都能喘口气、走得动。';
  } else {
    boost =
      '【提升方向】\n' +
      (allColEqual || weakest.key === strongest.key
        ? '- 先把「联络频率、回应预期、金钱边界」这几件事对齐，能显著降低误会。\n'
        : `- 优先补强「${weakest.key}」对应的沟通方式：多说具体需求，少做笼统否定。\n`) +
      '- 用小约定（例如固定联络窗口）建立可预测性，焦虑感会明显下降。\n' +
      '- 若长期在同一问题上卡死，说明需要调整沟通方式或节奏，而不是单纯加大音量。';
  }

  return [opening, '【匹配要点】\n' + matchPoints, getAlong, watchOut, boost].join('\n\n');
}

/**
 * 生成匹配报告详情
 */
function generateMatchReport(bazi1, bazi2, score) {
  const yearScore = calculateColumnMatch(
    bazi1.yearGan, bazi1.yearZhi,
    bazi2.yearGan, bazi2.yearZhi
  );
  
  const monthScore = calculateColumnMatch(
    bazi1.monthGan, bazi1.monthZhi,
    bazi2.monthGan, bazi2.monthZhi
  );
  
  const dayScore = calculateColumnMatch(
    bazi1.dayGan, bazi1.dayZhi,
    bazi2.dayGan, bazi2.dayZhi
  );
  
  const hourScore = calculateColumnMatch(
    bazi1.hourGan, bazi1.hourZhi,
    bazi2.hourGan, bazi2.hourZhi
  );
  
  const interpretation = buildExpandedInterpretation(score, {
    year: yearScore,
    month: monthScore,
    day: dayScore,
    hour: hourScore,
  });
  
  return {
    score: Math.round(score * 10) / 10,
    columns: {
      year: { score: yearScore, bazi1: bazi1.year, bazi2: bazi2.year },
      month: { score: monthScore, bazi1: bazi1.month, bazi2: bazi2.month },
      day: { score: dayScore, bazi1: bazi1.day, bazi2: bazi2.day },
      hour: { score: hourScore, bazi1: bazi1.hour, bazi2: bazi2.hour }
    },
    interpretation
  };
}

module.exports = {
  calculateBazi,
  calculateMatchScore,
  generateMatchReport,
  calculateColumnMatch,
  TIAN_GAN,
  DI_ZHI,
  TG_WUXING,
  DZ_WUXING
};
