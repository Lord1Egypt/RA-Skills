/**
 * LoveClaw - 本地数据模块 V1
 * 用于临时隔离用户数据，不上传到云端
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 本地缓存目录
const CACHE_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'loveclaw', 'data');
const PROFILES_FILE = path.join(CACHE_DIR, 'profiles.json');
const MATCHES_FILE = path.join(CACHE_DIR, 'matches.json');
const PHOTOS_DIR = path.join(CACHE_DIR, 'photos');

// 确保目录存在
function ensureDirs() {
  if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
  if (!fs.existsSync(PHOTOS_DIR)) fs.mkdirSync(PHOTOS_DIR, { recursive: true });
}

// 加载用户档案
function loadProfiles() {
  ensureDirs();
  if (!fs.existsSync(PROFILES_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(PROFILES_FILE, 'utf-8'));
  } catch (e) {
    return [];
  }
}

// 保存用户档案
function saveProfiles(profiles) {
  ensureDirs();
  fs.writeFileSync(PROFILES_FILE, JSON.stringify(profiles, null, 2));
}

// 获取单个用户档案
function getProfile(userId) {
  const profiles = loadProfiles();
  return profiles.find(p => p.userId === userId) || null;
}

// 保存用户档案
function saveProfile(profile) {
  const profiles = loadProfiles();
  const index = profiles.findIndex(p => p.userId === profile.userId);
  if (index >= 0) {
    profiles[index] = profile;
  } else {
    profiles.push(profile);
  }
  saveProfiles(profiles);
}

// 删除用户档案
function deleteProfile(userId) {
  let profiles = loadProfiles();
  profiles = profiles.filter(p => p.userId !== userId);
  saveProfiles(profiles);
}

// 获取所有档案
function getAllProfiles() {
  return loadProfiles();
}

// 加载匹配记录
function loadMatches() {
  ensureDirs();
  if (!fs.existsSync(MATCHES_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(MATCHES_FILE, 'utf-8'));
  } catch (e) {
    return [];
  }
}

// 保存匹配记录
function saveMatches(matches) {
  ensureDirs();
  fs.writeFileSync(MATCHES_FILE, JSON.stringify(matches, null, 2));
}

// 保存照片到本地
function savePhotoLocal(userId, photoData) {
  ensureDirs();
  const photoPath = path.join(PHOTOS_DIR, `${userId.replace(/[\/\:]/g, '_')}.jpg`);
  try {
    const buffer = Buffer.from(photoData, 'base64');
    fs.writeFileSync(photoPath, buffer);
    return photoPath;
  } catch (e) {
    console.error('保存照片失败:', e.message);
    return null;
  }
}

// 获取照片路径
function getPhotoPath(userId) {
  const photoPath = path.join(PHOTOS_DIR, `${userId.replace(/[\/\:]/g, '_')}.jpg`);
  return fs.existsSync(photoPath) ? photoPath : null;
}

// 占位函数（云端功能暂不可用）
async function sendVerificationCode(phone) {
  return { success: true, devCode: '123456', message: '开发模式：验证码为 123456' };
}

async function login(phone, code, userId) {
  return { success: true, userId: userId || 'local_user', token: 'local_token' };
}

async function uploadPhoto(userId, photoData) {
  const localPath = savePhotoLocal(userId, photoData);
  return { localPath, ossUrl: null };
}

module.exports = {
  getProfile,
  saveProfile,
  deleteProfile,
  getAllProfiles,
  savePhotoLocal,
  getPhotoPath,
  loadProfiles,
  saveProfiles,
  loadMatches,
  saveMatches,
  // 认证（本地模式）
  sendVerificationCode,
  login
};
