/**
 * 统一 API 请求工具
 * 
 * 功能：
 * - Token 缓存 + 提前5分钟自动刷新
 * - 401 自动刷新 + 一次重试
 * - 3次指数退避重试（网络错误/5xx）
 * - 10秒超时控制
 * 
 * 使用方式：
 * const { apiGet, apiPost, apiPut } = require('./request');
 */

const axios = require('axios');
const { CONFIG } = require('./config');

// ==================== Token 缓存 ====================
let tokenCache = {
  token: null,
  expireAt: null  // 提前5分钟过期的时间戳
};

// 从 config 读取凭证
function getCredentials() {
  return {
    app_id: CONFIG.APP_ID,
    app_secret: CONFIG.APP_SECRET
  };
}

// 获取 Token（带缓存 + 提前刷新）
async function getAccessToken() {
  const now = Date.now();
  
  // 缓存有效（未到过期时间）→ 直接返回
  if (tokenCache.token && tokenCache.expireAt && now < tokenCache.expireAt) {
    return tokenCache.token;
  }
  
  // 需要刷新
  const credentials = getCredentials();
  if (!credentials.app_id || !credentials.app_secret) {
    throw new Error('APP_ID 或 APP_SECRET 未配置');
  }
  
  try {
    const response = await axios.post(
      'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
      {
        app_id: credentials.app_id,
        app_secret: credentials.app_secret
      },
      { timeout: 10000 }
    );
    
    if (response.data.tenant_access_token) {
      // expire_in 单位是秒，默认7200（2小时）
      const expireIn = response.data.expire_in || 7200;
      // 提前5分钟过期（如实际2小时，则1小时55分后刷新）
      tokenCache.token = response.data.tenant_access_token;
      tokenCache.expireAt = now + (expireIn * 1000) - 300000;
      
      return tokenCache.token;
    }
    
    throw new Error(response.data.msg || '获取 Token 失败');
  } catch (error) {
    // 清空缓存，下次重新尝试
    tokenCache.token = null;
    tokenCache.expireAt = null;
    throw error;
  }
}

// 强制刷新 Token（用于 401 后）
function forceRefreshToken() {
  tokenCache.token = null;
  tokenCache.expireAt = null;
}

// ==================== sleep 工具 ====================
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== 重试逻辑 ====================
const MAX_RETRIES = 3;
const RETRY_DELAYS = [1000, 2000, 4000];  // 1s, 2s, 4s 指数退避

// 判断是否可重试（网络错误或5xx）
function isRetryableError(error) {
  // 无响应（网络问题）
  if (!error.response) return true;
  // 5xx 服务器错误
  if (error.response.status >= 500) return true;
  // 429 Too Many Requests（频率限制）
  if (error.response.status === 429) return true;
  return false;
}

// 带重试的请求
async function fetchWithRetry(fn, retries = MAX_RETRIES, delays = RETRY_DELAYS) {
  let lastError;
  
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // 401 不重试，交给外层处理
      if (error.response?.status === 401) {
        throw error;
      }
      
      // 非可重试错误，直接抛出
      if (!isRetryableError(error)) {
        throw error;
      }
      
      // 还有重试机会
      if (i < retries - 1) {
        await sleep(delays[i]);
        continue;
      }
    }
  }
  
  throw lastError;
}

// ==================== 统一请求封装 ====================
async function apiRequest(method, path, data = null, options = {}) {
  const token = await getAccessToken();
  const url = `https://open.feishu.cn/open-apis${path}`;
  
  const requestFn = async () => {
    const config = {
      method,
      url,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: 10000,
      ...options
    };
    
    if (data) {
      config.data = data;
    }
    
    return axios(config);
  };
  
  try {
    const response = await fetchWithRetry(requestFn);
    return response.data;
  } catch (error) {
    // 401 错误：强制刷新 Token 后重试一次
    if (error.response?.status === 401) {
      forceRefreshToken();
      const newToken = await getAccessToken();
      
      const retryFn = async () => {
        const config = {
          method,
          url,
          headers: {
            Authorization: `Bearer ${newToken}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000,
          ...options
        };
        if (data) config.data = data;
        return axios(config);
      };
      
      const retryResponse = await retryFn();
      return retryResponse.data;
    }
    
    // 其他错误
    throw error;
  }
}

// ==================== 对外 API ====================
async function apiGet(path, options = {}) {
  return apiRequest('GET', path, null, options);
}

async function apiPost(path, data, options = {}) {
  return apiRequest('POST', path, data, options);
}

async function apiPut(path, data, options = {}) {
  return apiRequest('PUT', path, data, options);
}

async function apiDelete(path, options = {}) {
  return apiRequest('DELETE', path, null, options);
}

// ==================== 初始化检查 ====================
async function checkConnection() {
  try {
    const token = await getAccessToken();
    return { success: true, token };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

module.exports = {
  getAccessToken,
  forceRefreshToken,
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  checkConnection,
  fetchWithRetry
};