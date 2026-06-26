/**
 * 八字缘分匹配 - 匹配引擎 V2
 * 双向确认匹配逻辑
 */

const { 
  loadProfiles, 
  saveProfile, 
  getProfile,
  addMatch,
  getUserTodayMatch,
  loadMatches
} = require('./data');

const { calculateMatchScore, generateMatchReport, calculateColumnMatch } = require('./bazi');

// 匹配阈值
const MATCH_THRESHOLD = 70;

/**
 * 计算双向匹配分数
 * 返回 { scoreAToB, scoreBToA, isMutual, mutualScore }
 */
function calculateMutualScore(baziA, baziB) {
  const scoreAToB = calculateMatchScore(baziA, baziB);
  const scoreBToA = calculateMatchScore(baziB, baziA);
  
  const isMutual = scoreAToB >= MATCH_THRESHOLD && scoreBToA >= MATCH_THRESHOLD;
  const mutualScore = Math.min(scoreAToB, scoreBToA); // 取较低值作为共同分数
  
  return { scoreAToB, scoreBToA, isMutual, mutualScore };
}

/**
 * 为单个用户执行每日匹配
 */
function runDailyMatchForUser(userId) {
  const profile = getProfile(userId);
  if (!profile) {
    return { userId, success: false, error: '用户未报名' };
  }
  
  // 检查今日是否已匹配
  if (profile.todayMatchDone) {
    return { userId, success: false, error: '今日已匹配' };
  }
  
  // 获取今日未匹配的用户
  const candidates = getUnmatchedCandidates(userId, profile.preferredGender);
  
  if (candidates.length === 0) {
    return { userId, success: true, matched: false, noMatch: true };
  }
  
  // 只考虑同城匹配（异地直接排除）
  const sameCityMatches = [];
  
  for (const candidate of candidates) {
    if (candidate.city !== profile.city) continue; // 必须同城
    
    const result = calculateMutualScore(profile.bazi, candidate.bazi);
    
    if (result.isMutual) {
      sameCityMatches.push({
        candidate,
        scoreAToB: result.scoreAToB,
        scoreBToA: result.scoreBToA,
        mutualScore: result.mutualScore
      });
    }
  }
  
  // 必须有同城匹配
  if (sameCityMatches.length === 0) {
    return { userId, success: true, matched: false, noMatch: true };
  }
  
  // 按分数排序取最高
  sameCityMatches.sort((a, b) => b.mutualScore - a.mutualScore);
  const bestMatch = sameCityMatches[0];
  
  // 创建双向匹配记录
  const today = new Date().toISOString().split('T')[0];
  const matchId1 = `${userId}_${bestMatch.candidate.userId}_${Date.now()}`;
  const matchId2 = `${bestMatch.candidate.userId}_${userId}_${Date.now()}`;
  
  // 保存匹配记录（双向）
  addMatch({
    id: matchId1,
    userId1: userId,
    userId2: bestMatch.candidate.userId,
    compatibility: bestMatch.mutualScore,
    scoreAToB: bestMatch.scoreAToB,
    scoreBToA: bestMatch.scoreBToA,
    matchDate: today,
    reported: false,
    isMutual: true
  });
  
  addMatch({
    id: matchId2,
    userId1: bestMatch.candidate.userId,
    userId2: userId,
    compatibility: bestMatch.mutualScore,
    scoreAToB: bestMatch.scoreBToA,
    scoreBToA: bestMatch.scoreAToB,
    matchDate: today,
    reported: false,
    isMutual: true
  });
  
  // 更新两人的匹配状态
  profile.todayMatchDone = true;
  profile.todayMatchDate = today;
  profile.matchedWith = bestMatch.candidate.userId;
  // 添加到匹配历史（防止重复匹配）
  if (!profile.matchedWithHistory) profile.matchedWithHistory = [];
  profile.matchedWithHistory.push(bestMatch.candidate.userId);
  saveProfile(profile);
  
  bestMatch.candidate.todayMatchDone = true;
  bestMatch.candidate.todayMatchDate = today;
  bestMatch.candidate.matchedWith = userId;
  // 添加到匹配历史（防止重复匹配）
  if (!bestMatch.candidate.matchedWithHistory) bestMatch.candidate.matchedWithHistory = [];
  bestMatch.candidate.matchedWithHistory.push(userId);
  saveProfile(bestMatch.candidate);
  
  return {
    userId,
    success: true,
    matched: true,
    matchId: matchId1,
    partner: {
      userId: bestMatch.candidate.userId,
      name: bestMatch.candidate.name,
      phone: bestMatch.candidate.phone,
      city: bestMatch.candidate.city,
      photo: bestMatch.candidate.photo
    },
    mutualScore: bestMatch.mutualScore
  };
}

/**
 * 获取未匹配的用户列表
 */
function getUnmatchedCandidates(userId, preferredGender) {
  const profiles = loadProfiles();
  const userProfile = profiles.find(p => p.userId === userId);
  const history = userProfile?.matchedWithHistory || [];
  
  return profiles.filter(p => {
    if (p.userId === userId) return false;
    if (p.gender !== preferredGender) return false;
    if (p.todayMatchDone) return false;
    if (history.includes(p.userId)) return false; // 排除已匹配过的用户
    return true;
  });
}

/**
 * 执行所有用户的每日匹配
 */
function runAllDailyMatches() {
  const profiles = loadProfiles();
  const results = [];
  const noMatchUsers = [];
  
  for (const profile of profiles) {
    if (!profile.todayMatchDone) {
      const result = runDailyMatchForUser(profile.userId);
      if (result.matched) {
        results.push(result);
      } else if (result.noMatch) {
        noMatchUsers.push(profile.userId);
      }
    }
  }
  
  return { matched: results, noMatch: noMatchUsers };
}

const reportTemplates = require('./report-templates');

/**
 * 生成匹配报告消息（文案写死在 report-templates.js）
 * @param {*} profile 当前用户档案
 * @param {*} partner 对方档案（含 name, city, phone）
 * @param {number} score 总匹配度（双向取低或综合分）
 * @param {object|string} report bazi.generateMatchReport 结果，或解读字符串
 */
function formatMatchReport(profile, partner, score, report) {
  const pct = typeof score === 'object' ? score.mutualScore : score;
  const text = typeof report === 'object' ? (report.interpretation || '') : (report || '');
  const phone = partner.phone || partner.userId || '未知';
  const city = partner.city || '未知';
  const displayPct = typeof pct === 'number' ? Math.round(pct * 10) / 10 : pct;
  return reportTemplates.formatEveningMatchSuccess(partner.name, city, phone, displayPct, text);
}

/**
 * 生成无匹配消息
 */
function formatNoMatchMessage(user) {
  return reportTemplates.formatEveningMatchFail(user?.name);
}

/**
 * 获取今日未匹配的用户ID列表
 */
function getTodayNoMatchUserIds() {
  const profiles = loadProfiles();
  const today = new Date().toISOString().split('T')[0];
  
  return profiles
    .filter(p => !p.todayMatchDone || p.todayMatchDate !== today)
    .map(p => p.userId);
}

/**
 * 重置匹配状态（新的一天）
 */
function resetDailyStatus() {
  const profiles = loadProfiles();
  const today = new Date().toISOString().split('T')[0];
  
  profiles.forEach(p => {
    // 只有昨天的才重置
    if (p.todayMatchDate !== today) {
      p.todayMatchDone = false;
      p.matchedWith = null;
    }
  });
  
  saveProfiles(profiles);
}

// 需要从 data.js 导出 saveProfiles
function saveProfiles(profiles) {
  const fs = require('fs');
  const path = require('path');
  const DATA_DIR = path.join(process.cwd(), 'workspace/bazi-match/data');
  const PROFILES_FILE = path.join(DATA_DIR, 'profiles.json');
  
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(PROFILES_FILE, JSON.stringify(profiles, null, 2));
}

module.exports = {
  runDailyMatchForUser,
  runAllDailyMatches,
  calculateMutualScore,
  formatMatchReport,
  formatNoMatchMessage,
  getTodayNoMatchUserIds,
  resetDailyStatus,
  MATCH_THRESHOLD,
  calculateMatchScore,
  generateMatchReport,
};
