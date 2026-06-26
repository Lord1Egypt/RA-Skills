/**
 * LoveClaw - API 客户端
 * 所有云端操作通过这个客户端调用中心化 API
 */

const API_BASE =
  process.env.LOVECLAW_API_BASE || 'https://loveclaw-cgbnqltfhd.cn-hangzhou.fcapp.run';

/**
 * 发送 HTTP 请求
 */
async function request(path, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  
  if (body) {
    options.body = JSON.stringify(body);
  }
  
  const url = path.startsWith('http') ? path : API_BASE + path;
  
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    return data;
  } catch (e) {
    console.error('API 请求失败:', e.message);
    return { error: e.message };
  }
}

// ==========================================
// 用户档案 API
// ==========================================

/**
 * 保存用户档案
 */
async function saveProfile(profile) {
  return await request('/api/profile', 'POST', profile);
}

/**
 * 获取用户档案
 */
async function getProfile(userId) {
  return await request(`/api/profile/${encodeURIComponent(userId)}`);
}

/**
 * 获取所有用户档案
 */
async function getAllProfiles() {
  return await request('/api/profiles');
}

/**
 * 删除用户档案
 */
async function deleteProfile(userId) {
  return await request(`/api/profile/${encodeURIComponent(userId)}`, 'DELETE');
}

// ==========================================
// 照片 API
// ==========================================

/**
 * 上传照片
 */
async function uploadPhoto(userId, photoData) {
  return await request(`/api/photo/${encodeURIComponent(userId)}`, 'POST', { photoData });
}

/**
 * 获取照片 URL
 */
async function getPhotoUrl(userId) {
  return await request(`/api/photo/${encodeURIComponent(userId)}`);
}

// ==========================================
// 匹配 API
// ==========================================

/**
 * 保存匹配记录
 */
async function saveMatch(userId1, userId2, compatibility, mutualScore) {
  return await request('/api/match', 'POST', {
    userId1,
    userId2,
    compatibility,
    mutualScore
  });
}

/**
 * 获取用户今日匹配
 */
async function getUserTodayMatch(userId) {
  return await request(`/api/match/${encodeURIComponent(userId)}/today`);
}

module.exports = {
  saveProfile,
  getProfile,
  getAllProfiles,
  deleteProfile,
  uploadPhoto,
  getPhotoUrl,
  saveMatch,
  getUserTodayMatch
};
