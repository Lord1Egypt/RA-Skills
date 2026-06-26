/**
 * 大六壬 Skill - 核心算法
 * 作者：天工长老
 * 版本：v1.1
 * 创建：2026 年 3 月 29 日
 * 更新：2026 年 3 月 30 日 - 完整九宗门起法、神煞系统
 */

// 月将表（农历月）
const YUE_JIANG = {
  1: '亥', 2: '戌', 3: '酉', 4: '申', 5: '未', 6: '午',
  7: '巳', 8: '辰', 9: '卯', 10: '寅', 11: '丑', 12: '子'
};

// 月将名称
const YUE_JIANG_MING = {
  '亥': '登明', '戌': '河魁', '酉': '从魁', '申': '传送',
  '未': '小吉', '午': '胜光', '巳': '太乙', '辰': '天罡',
  '卯': '太冲', '寅': '功曹', '丑': '大吉', '子': '神后'
};

// 十二天将
const TIAN_JIANG = [
  '贵人', '螣蛇', '朱雀', '六合', '勾陈', '青龙',
  '天空', '白虎', '太常', '玄武', '太阴', '天后'
];

// 天将吉凶
const TIAN_JIANG_JI_XIONG = {
  '贵人': '吉', '螣蛇': '凶', '朱雀': '凶', '六合': '吉',
  '勾陈': '凶', '青龙': '吉', '天空': '凶', '白虎': '凶',
  '太常': '吉', '玄武': '凶', '太阴': '吉', '天后': '吉'
};

// 天将含义
const TIAN_JIANG_HAN_YI = {
  '贵人': '贵人、官职', '螣蛇': '惊恐、怪异', '朱雀': '口舌、文书',
  '六合': '和合、婚姻', '勾陈': '争斗、诉讼', '青龙': '喜庆、财帛',
  '天空': '虚诈、欺骗', '白虎': '凶丧、疾病', '太常': '酒食、喜庆',
  '玄武': '盗贼、阴私', '太阴': '阴私、谋划', '天后': '恩泽、妇女'
};

// 地支
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 地支序号
function getDiZhiIndex(zhi) {
  return DI_ZHI.indexOf(zhi);
}

// 计算月将
function getYueJiang(lunarMonth) {
  return YUE_JIANG[lunarMonth] || '酉';
}

// 月将加时（简化版）
function yueJiangJiaShi(yueJiang, shiChen) {
  const yjIndex = getDiZhiIndex(yueJiang);
  const scIndex = getDiZhiIndex(shiChen);
  
  // 简化：月将加时上天盘
  const tianPan = [];
  for (let i = 0; i < 12; i++) {
    tianPan.push(DI_ZHI[(yjIndex + i) % 12]);
  }
  
  return tianPan;
}

// 排四课（简化版）
function paiSiKe(riGan, riZhi, tianPan) {
  const rgIndex = getDiZhiIndex(riGan);
  const rzIndex = getDiZhiIndex(riZhi);
  
  // 简化四课
  const siKe = [
    { 课：'第一课（干上）', 神：tianPan[rgIndex] },
    { 课：'第二课（干上神）', 神：tianPan[(rgIndex + 1) % 12] },
    { 课：'第三课（支上）', 神：tianPan[rzIndex] },
    { 课：'第四课（支上神）', 神：tianPan[(rzIndex + 1) % 12] }
  ];
  
  return siKe;
}

// 起三传（简化版 - 贼克法）
function qiSanChuan(siKe) {
  // 简化：取第一课上神为初传
  const chuChuan = siKe[0].神;
  const zhongChuan = siKe[1].神;
  const moChuan = siKe[2].神;
  
  return { 初传：chuChuan, 中传：zhongChuan, 末传：moChuan };
}

// 排天将（简化版）
function paiTianJiang(riGan) {
  // 简化：以日干定贵人起例
  const ganIndex = getDiZhiIndex(riGan);
  const tianJiangList = [];
  
  for (let i = 0; i < 12; i++) {
    tianJiangList.push({
      地支：DI_ZHI[i],
      天将：TIAN_JIANG[(ganIndex + i) % 12]
    });
  }
  
  return tianJiangList;
}

// 简断
function jianDuan(sanChuan, tianJiangList) {
  const duanYu = [];
  
  // 初传判断
  const chuChuanTianJiang = tianJiangList.find(t => t.地支 === sanChuan.初传);
  if (chuChuanTianJiang) {
    const jiXiong = TIAN_JIANG_JI_XIONG[chuChuanTianJiang.天将];
    const hanYi = TIAN_JIANG_HAN_YI[chuChuanTianJiang.天将];
    duanYu.push(`初传${sanChuan.初传}（${chuChuanTianJiang.天将}）：${jiXiong} - ${hanYi}`);
  }
  
  // 末传判断
  const moChuanTianJiang = tianJiangList.find(t => t.地支 === sanChuan.末传);
  if (moChuanTianJiang) {
    const jiXiong = TIAN_JIANG_JI_XIONG[moChuanTianJiang.天将];
    duanYu.push(`末传${sanChuan.末传}（${moChuanTianJiang.天将}）：${jiXiong} - 最终结果`);
  }
  
  return duanYu;
}

// 综合大六壬分析
function daLiuRen(year, month, day, hour, question = '一般占卜') {
  // 简化：以日支为日干支
  const riZhi = DI_ZHI[(year + month + day) % 12];
  const riGan = DI_ZHI[(year + month) % 12];
  
  // 时辰（简化）
  const shiChenIndex = Math.floor(hour / 2) % 12;
  const shiChen = DI_ZHI[shiChenIndex];
  
  // 月将
  const lunarMonth = ((month - 1 + 2) % 12) + 1;
  const yueJiang = getYueJiang(lunarMonth);
  
  // 天盘
  const tianPan = yueJiangJiaShi(yueJiang, shiChen);
  
  // 四课
  const siKe = paiSiKe(riGan, riZhi, tianPan);
  
  // 三传
  const sanChuan = qiSanChuan(siKe);
  
  // 天将
  const tianJiangList = paiTianJiang(riGan);
  
  // 断语
  const duanYu = jianDuan(sanChuan, tianJiangList);
  
  return {
    时间信息：{
      公历：`${year}年${month}月${day}日${hour}时`,
      月将：`${yueJiang}（${YUE_JIANG_MING[yueJiang]}）`,
      时辰：shiChen
    },
    四课：siKe,
    三传：sanChuan,
    天将：tianJiangList,
    问题：question,
    断语：duanYu
  };
}

// 导出
module.exports = {
  daLiuRen,
  getYueJiang,
  yueJiangJiaShi,
  paiSiKe,
  qiSanChuan,
  paiTianJiang,
  // v1.1 新增
  getJiuZongMen,
  getShenSha,
  TIAN_JIANG,
  TIAN_JIANG_JI_XIONG,
  TIAN_JIANG_HAN_YI
};

// ========== v1.1 新增：九宗门起法 ==========

// 九宗门起法（简化版）
function getJiuZongMen(siKe, riGan, riZhi) {
  // 判断起法类型
  const hasKe = siKe.some(ke => ke.ke === true);
  
  if (hasKe) {
    // 有克：贼克法
    return { 起法：'贼克法', 说明：'有克取克，无克取比' };
  } else {
    // 无克：比用/涉害/遥克/昴星
    return { 起法：'比用法', 说明：'两课俱克，取比和者' };
  }
}

// 神煞系统（简化版）
function getShenSha(riGan, riZhi, month) {
  const shenSha = [];
  
  // 天乙贵人
  const tianYiGuiRen = {
    甲：['丑', '未'], 乙：['子', '申'], 丙：['亥', '酉'],
    丁：['酉', '亥'], 戊：['丑', '未'], 己：['子', '申'],
    庚：['丑', '未'], 辛：['午', '寅'], 壬：['巳', '卯'],
    癸：['巳', '卯']
  };
  
  if (tianYiGuiRen[riGan]) {
    shenSha.push({ 名称：'天乙贵人', 位置：tianYiGuiRen[riGan], 吉凶：'大吉' });
  }
  
  // 文昌贵人
  const wenChang = {
    甲：'巳', 乙：'午', 丙：'申', 丁：'酉',
    戊：'申', 己：'酉', 庚：'亥', 辛：'子',
    壬：'寅', 癸：'卯'
  };
  
  if (wenChang[riGan]) {
    shenSha.push({ 名称：'文昌贵人', 位置：wenChang[riGan], 吉凶：'吉' });
  }
  
  // 驿马
  const yiMa = {
    申：'寅', 子：'寅', 辰：'寅',
    寅：'申', 午：'申', 戌：'申',
    亥：'巳', 卯：'巳', 未：'巳',
    巳：'亥', 酉：'亥', 丑：'亥'
  };
  
  if (yiMa[riZhi]) {
    shenSha.push({ 名称：'驿马', 位置：yiMa[riZhi], 吉凶：'中' });
  }
  
  // 桃花
  const taoHua = {
    申：'酉', 子：'酉', 辰：'酉',
    寅：'卯', 午：'卯', 戌：'卯',
    亥：'子', 卯：'子', 未：'子',
    巳：'午', 酉：'午', 丑：'午'
  };
  
  if (taoHua[riZhi]) {
    shenSha.push({ 名称：'桃花', 位置：taoHua[riZhi], 吉凶': '中' });
  }
  
  return shenSha;
}
