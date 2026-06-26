/**
 * 云端数据存储 - 阿里云 FC API 客户端
 * 单层鉴权：LOVECLAW_API_TOKEN，用户端点附带 X-Loveclaw-User。
 * 匹配/报告运算由 FC 服务端执行，skill 端仅触发与接收结果。
 */

const API_BASE =
  process.env.LOVECLAW_API_BASE || 'https://loveclaw-cgbnqltfhd.cn-hangzhou.fcapp.run';
const API_TIMEOUT = 15000;
const API_TOKEN = process.env.LOVECLAW_API_TOKEN || process.env.API_TOKEN || '';

// ==================== 底层请求 ====================

async function rawFetch(path, { method = 'GET', body, headers = {}, timeoutMs = API_TIMEOUT } = {}) {
  const resp = await fetch(`${API_BASE}${path}`, {
    method,
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(timeoutMs),
  });
  const data = await resp.json();
  if (!resp.ok) {
    throw new Error(`${data.error || 'API error: ' + resp.status} (HTTP ${resp.status})`);
  }
  return data;
}

function apiRequest(path, options = {}) {
  if (!API_TOKEN) {
    throw new Error('LOVECLAW_API_TOKEN 未设置，请在 ~/.openclaw/workspace/.env 中配置');
  }
  const { headers = {}, ...rest } = options;
  return rawFetch(path, {
    ...rest,
    headers: {
      'Authorization': 'Bearer ' + API_TOKEN,
      ...headers,
    },
  });
}

function userApiRequest(path, userId, options = {}) {
  const { headers = {}, ...rest } = options;
  return apiRequest(path, {
    ...rest,
    headers: {
      'X-Loveclaw-User': String(userId || ''),
      ...headers,
    },
  });
}

// ==================== 用户级操作 ====================

async function getProfile(phone) {
  if (!phone) return null;
  try {
    const data = await userApiRequest(`/api/profile/${phone}`, phone);
    if (!data.success) return null;
    return data.profile || null;
  } catch (e) {
    if (e.message.includes('404') || e.message.includes('not found') || e.message.includes('timeout') || e.message.includes('network') || e.message.includes('fetch') || e.message.includes('AbortError') || e.message.includes('用户不存在')) {
      return null;
    }
    throw e;
  }
}

async function saveProfile(profile) {
  const uid = profile.phone || profile.userId;
  return userApiRequest('/api/register', uid, { method: 'POST', body: profile });
}

async function updateProfile(phone, updates) {
  const existing = await getProfile(phone);
  if (!existing) throw new Error('Profile not found');
  const updated = { ...existing, ...updates };
  return userApiRequest('/api/register', phone, { method: 'POST', body: updated });
}

async function deleteProfile(phone) {
  try {
    await userApiRequest('/api/profile/' + phone, phone, { method: 'DELETE' });
    return { success: true };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

async function uploadPhoto(phone, photoData) {
  let body;
  if (typeof photoData === 'string' && (photoData.startsWith('http://') || photoData.startsWith('https://'))) {
    body = { userId: phone, phone, photoUrl: photoData };
  } else if (typeof photoData === 'string' && photoData.startsWith('data:')) {
    const comma = photoData.indexOf(',');
    body = { userId: phone, phone, photoData: comma >= 0 ? photoData.slice(comma + 1) : photoData };
  } else if (typeof photoData === 'string') {
    body = { userId: phone, phone, photoData: photoData };
  } else {
    body = { userId: phone, phone, photoData: photoData.toString('base64') };
  }

  let lastErr;
  for (let i = 0; i < 2; i++) {
    try {
      const data = await userApiRequest('/api/photo', phone, { method: 'POST', body, timeoutMs: 120000 });
      if (!data.success) throw new Error(data.error || '照片上传失败');
      return data.url;
    } catch (e) {
      lastErr = e;
      const msg = String(e && e.message ? e.message : e);
      if (i === 0 && msg.includes('412')) {
        await new Promise(r => setTimeout(r, 1500));
        continue;
      }
      throw e;
    }
  }
  throw lastErr;
}

async function getMyReport(userId) {
  try {
    return await userApiRequest('/api/my-report', userId);
  } catch (e) {
    console.error('[getMyReport]', e.message);
    return { success: false, status: 'error' };
  }
}

async function getMatchHistory(phone) {
  const profile = await getProfile(phone);
  if (!profile) return [];
  return profile.matchedWithHistory || [];
}

// ==================== 触发操作（cron 调用） ====================

async function triggerMatch() {
  return apiRequest('/api/run-match', { method: 'POST', timeoutMs: 120000 });
}

module.exports = {
  getProfile,
  saveProfile,
  updateProfile,
  deleteProfile,
  getMatchHistory,
  getMyReport,
  uploadPhoto,
  triggerMatch,
  apiRequest,
  userApiRequest,
};
