/**
 * 八字缘分匹配 - 数据管理模块
 * 管理用户档案和匹配记录
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.cwd(), 'workspace/loveclaw/data');
const PROFILES_FILE = path.join(DATA_DIR, 'profiles.json');
const MATCHES_FILE = path.join(DATA_DIR, 'matches.json');
const PHOTOS_DIR = path.join(DATA_DIR, 'photos');

// 确保目录存在
function ensureDirectories() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(PHOTOS_DIR)) fs.mkdirSync(PHOTOS_DIR, { recursive: true });
}

// 加载用户档案
function loadProfiles() {
  ensureDirectories();
  if (!fs.existsSync(PROFILES_FILE)) return [];
  try {
    const data = fs.readFileSync(PROFILES_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (e) {
    console.error('加载档案失败:', e);
    return [];
  }
}

// 保存用户档案
function saveProfiles(profiles) {
  ensureDirectories();
  fs.writeFileSync(PROFILES_FILE, JSON.stringify(profiles, null, 2));
}

// 获取单个用户档案
function getProfile(userId) {
  const profiles = loadProfiles();
  return profiles.find(p => p.userId === userId);
}

// 创建或更新用户档案
function saveProfile(profile) {
  const profiles = loadProfiles();
  const index = profiles.findIndex(p => p.userId === profile.userId);
  
  if (index >= 0) {
    profiles[index] = { ...profiles[index], ...profile };
  } else {
    profiles.push(profile);
  }
  
  saveProfiles(profiles);
  return profile;
}

// 删除用户档案
function deleteProfile(userId) {
  const profiles = loadProfiles();
  const filtered = profiles.filter(p => p.userId !== userId);
  saveProfiles(filtered);
  
  // 删除照片
  const photoPath = path.join(PHOTOS_DIR, `${userId.replace(/[\/\:]/g, '_')}.jpg`);
  if (fs.existsSync(photoPath)) {
    fs.unlinkSync(photoPath);
  }
}

// 保存用户照片
function savePhoto(userId, photoData) {
  ensureDirectories();
  const photoPath = path.join(PHOTOS_DIR, `${userId.replace(/[\/\:]/g, '_')}.jpg`);
  const buffer = Buffer.from(photoData, 'base64');
  fs.writeFileSync(photoPath, buffer);
  return photoPath;
}

// 获取用户照片路径
function getPhotoPath(userId) {
  const photoPath = path.join(PHOTOS_DIR, `${userId.replace(/[\/\:]/g, '_')}.jpg`);
  return fs.existsSync(photoPath) ? photoPath : null;
}

// 加载匹配记录
function loadMatches() {
  ensureDirectories();
  if (!fs.existsSync(MATCHES_FILE)) return [];
  try {
    const data = fs.readFileSync(MATCHES_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (e) {
    console.error('加载匹配记录失败:', e);
    return [];
  }
}

// 保存匹配记录
function saveMatches(matches) {
  ensureDirectories();
  fs.writeFileSync(MATCHES_FILE, JSON.stringify(matches, null, 2));
}

// 添加匹配记录
function addMatch(match) {
  const matches = loadMatches();
  matches.push(match);
  saveMatches(matches);
  return match;
}

// 获取用户今日匹配
function getUserTodayMatch(userId) {
  const matches = loadMatches();
  const today = new Date().toISOString().split('T')[0];
  return matches.find(m => 
    (m.userId1 === userId || m.userId2 === userId) && 
    m.matchDate === today
  );
}

// 重置每日匹配状态
function resetDailyMatchStatus() {
  const profiles = loadProfiles();
  profiles.forEach(p => {
    p.todayMatchDone = false;
  });
  saveProfiles(profiles);
}

// 获取未发送报告的匹配
function getUnreportedMatches() {
  const matches = loadMatches();
  return matches.filter(m => !m.reported);
}

// 标记匹配已报告
function markMatchReported(matchId) {
  const matches = loadMatches();
  const match = matches.find(m => m.id === matchId);
  if (match) {
    match.reported = true;
    saveMatches(matches);
  }
}

// 获取所有待匹配用户（排除今日已匹配的）
function getUnmatchedProfiles(userId, preferredGender) {
  const profiles = loadProfiles();
  const today = new Date().toISOString().split('T')[0];
  
  return profiles.filter(p => {
    if (p.userId === userId) return false;
    if (p.gender !== preferredGender) return false;
    if (p.todayMatchDone) return false;
    
    // 检查今日是否已有匹配记录
    const hasMatch = getUserTodayMatch(p.userId);
    if (hasMatch) return false;
    
    return true;
  });
}

module.exports = {
  loadProfiles,
  saveProfile,
  getProfile,
  deleteProfile,
  savePhoto,
  getPhotoPath,
  loadMatches,
  addMatch,
  getUserTodayMatch,
  resetDailyMatchStatus,
  getUnreportedMatches,
  markMatchReported,
  getUnmatchedProfiles,
  ensureDirectories
};
