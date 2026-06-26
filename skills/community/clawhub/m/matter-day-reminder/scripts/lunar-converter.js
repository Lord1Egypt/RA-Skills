const { Lunar, Solar } = require('lunar-javascript');

/**
 * 农历转换工具
 * 使用 lunar-javascript 库进行农历和阳历之间的转换
 */

/**
 * 将农历日期转换为阳历日期
 * @param {number} lunarYear - 农历年
 * @param {number} lunarMonth - 农历月（1-12）
 * @param {number} lunarDay - 农历日（1-30）
 * @param {boolean} isLeapMonth - 是否为闰月
 * @returns {Object} 阳历日期对象 {year, month, day}
 */
function lunarToSolar(lunarYear, lunarMonth, lunarDay, isLeapMonth = false) {
  try {
    const lunar = Lunar.fromYmd(lunarYear, lunarMonth, lunarDay);
    const solar = lunar.getSolar();
    
    return {
      year: solar.getYear(),
      month: solar.getMonth(),
      day: solar.getDay(),
      isLeapMonth: lunar.getMonth() < 0  // 负数表示闰月
    };
  } catch (error) {
    throw new Error(`农历日期转换失败: ${error.message}`);
  }
}

/**
 * 将阳历日期转换为农历日期
 * @param {number} solarYear - 阳历年
 * @param {number} solarMonth - 阳历月（1-12）
 * @param {number} solarDay - 阳历日（1-31）
 * @returns {Object} 农历日期对象 {year, month, day, isLeapMonth}
 */
function solarToLunar(solarYear, solarMonth, solarDay) {
  try {
    const solar = Solar.fromYmd(solarYear, solarMonth, solarDay);
    const lunar = solar.getLunar();
    
    return {
      year: lunar.getYear(),
      month: Math.abs(lunar.getMonth()),  // 取绝对值
      day: lunar.getDay(),
      isLeapMonth: lunar.getMonth() < 0,  // 负数表示闰月
      monthInChinese: lunar.getMonthInChinese(),
      dayInChinese: lunar.getDayInChinese()
    };
  } catch (error) {
    throw new Error(`阳历日期转换失败: ${error.message}`);
  }
}

/**
 * 获取指定农历日期在当前年的阳历日期
 * @param {number} lunarMonth - 农历月
 * @param {number} lunarDay - 农历日
 * @param {number} currentYear - 当前年（可选，默认为今年）
 * @returns {Object} 阳历日期对象
 */
function getThisYearSolarDate(lunarMonth, lunarDay, currentYear = null) {
  const year = currentYear || new Date().getFullYear();
  return lunarToSolar(year, lunarMonth, lunarDay);
}

/**
 * 检查今年是否为闰月年，以及闰哪个月
 * @param {number} year - 年份
 * @returns {Object|null} 闰月信息或 null
 */
function getLeapMonth(year) {
  try {
    const lunarYear = Lunar.fromYmd(year, 1, 1);
    const leapMonth = lunarYear.getLeapMonth();
    
    if (leapMonth === 0) {
      return null;
    }
    
    return {
      year: year,
      leapMonth: leapMonth,  // 闰几月
      monthName: getMonthName(leapMonth)
    };
  } catch (error) {
    throw new Error(`获取闰月信息失败: ${error.message}`);
  }
}

/**
 * 获取农历月份名称
 * @param {number} month - 月份数字
 * @returns {string} 月份中文名称
 */
function getMonthName(month) {
  const monthNames = [
    '正', '二', '三', '四', '五', '六',
    '七', '八', '九', '十', '冬', '腊'
  ];
  return monthNames[Math.abs(month) - 1] + '月';
}

/**
 * 格式化农历日期字符串
 * @param {number} month - 农历月
 * @param {number} day - 农历日
 * @param {boolean} isLeapMonth - 是否为闰月
 * @returns {string} 格式化后的字符串，如"农历八月初五"或"农历闰八月初五"
 */
function formatLunarDate(month, day, isLeapMonth = false) {
  const monthStr = isLeapMonth ? `闰${getMonthName(month)}` : getMonthName(month);
  const dayNames = [
    '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
    '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
  ];
  const dayStr = dayNames[day - 1];
  
  return `农历${monthStr}${dayStr}`;
}

/**
 * 解析农历日期字符串
 * @param {string} dateStr - 日期字符串，如"八月初五"或"8-15"
 * @returns {Object|null} 解析结果 {month, day, isLeapMonth}
 */
function parseLunarDate(dateStr) {
  // 移除常见的前缀（农历、阴历、旧历）
  let cleanStr = dateStr.replace(/^(农历|阴历|旧历)\s*/g, '');
  
  // 移除括号内的农历标注，如 "8-15（农历）"
  cleanStr = cleanStr.replace(/[（(]农历[)）]/g, '');
  
  // 处理 "闰八月" 格式
  const leapMatch = cleanStr.match(/闰([一二三四五六七八九十]+)月/);
  const isLeapMonth = !!leapMatch;
  
  // 移除"闰"字进行后续解析
  cleanStr = cleanStr.replace(/闰/g, '');
  
  // 处理 "八月初五" 格式（支持腊、冬、正等特殊月份）
  // 日期部分支持：初一到三十、十一到二十、廿一到廿九、二十一到二十九
  const chineseMatch = cleanStr.match(/^([正一二三四五六七八九十腊冬]+)月([初一初二初三初四初五初六初七初八初九初十十一十二十三十四十五十六十七十八十九二十廿一廿二廿三廿四廿五廿六廿七廿八廿九三十二十一二二十二三十二十四二十五二十六二十七二十八二十九]+)$/);
  if (chineseMatch) {
    const monthMap = {
      '正': 1, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
      '七': 7, '八': 8, '九': 9, '十': 10, '冬': 11, '腊': 12
    };
    const dayMap = {
      '初一': 1, '初二': 2, '初三': 3, '初四': 4, '初五': 5,
      '初六': 6, '初七': 7, '初八': 8, '初九': 9, '初十': 10,
      '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
      '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
      '廿一': 21, '廿二': 22, '廿三': 23, '廿四': 24, '廿五': 25,
      '廿六': 26, '廿七': 27, '廿八': 28, '廿九': 29, '三十': 30,
      // 支持替代写法（如"二十三"等同于"廿三"）
      '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
      '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29
    };
    
    const month = monthMap[chineseMatch[1]];
    const day = dayMap[chineseMatch[2]];
    
    if (month && day) {
      return {
        month: month,
        day: day,
        isLeapMonth: isLeapMonth
      };
    }
  }
  
  // 处理 "8-15" 或 "8月15日" 或 "6月8日" 格式
  const numMatch = cleanStr.match(/(\d{1,2})[-/月](\d{1,2})/);
  if (numMatch) {
    return {
      month: parseInt(numMatch[1]),
      day: parseInt(numMatch[2]),
      isLeapMonth: isLeapMonth
    };
  }
  
  return null;
}

/**
 * 获取下一个农历生日对应的阳历日期
 * @param {number} lunarMonth - 农历月
 * @param {number} lunarDay - 农历日
 * @param {number} referenceYear - 参考年份（出生年）
 * @returns {Object} 下一个生日日期
 */
function getNextLunarBirthday(lunarMonth, lunarDay, referenceYear = null) {
  const currentYear = new Date().getFullYear();
  const currentDate = new Date();
  
  // 尝试今年的日期
  let solarDate = getThisYearSolarDate(lunarMonth, lunarDay, currentYear);
  let solarDateTime = new Date(solarDate.year, solarDate.month - 1, solarDate.day);
  
  // 如果今年的日期已过，使用明年的
  if (solarDateTime < currentDate) {
    solarDate = getThisYearSolarDate(lunarMonth, lunarDay, currentYear + 1);
  }
  
  return {
    ...solarDate,
    age: referenceYear ? (solarDate.year - referenceYear) : null,
    daysUntil: Math.ceil((new Date(solarDate.year, solarDate.month - 1, solarDate.day) - currentDate) / (1000 * 60 * 60 * 24))
  };
}

module.exports = {
  lunarToSolar,
  solarToLunar,
  getThisYearSolarDate,
  getLeapMonth,
  getMonthName,
  formatLunarDate,
  parseLunarDate,
  getNextLunarBirthday
};
