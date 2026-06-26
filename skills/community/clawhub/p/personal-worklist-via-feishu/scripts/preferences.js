/**
 * 用户偏好存储工具
 * 
 * 安全机制：
 * - 原子写入：先写 .tmp 文件再 rename，避免读到半文件
 * - 读时合并：读取当前数据后再写入，保留其他字段
 * 
 * 注意：当前为单用户设计，rename 组合在大多数场景足够安全
 *       若未来需多进程并发写入，需引入 lockfile npm 包
 */

const fs = require('fs');
const path = require('path');

// 偏好文件路径（相对于 workspace root）
const PREFERENCES_FILE = path.join(__dirname, '..', 'memory', 'preferences.json');
const TEMP_FILE = PREFERENCES_FILE + '.tmp';

/**
 * 读取用户偏好
 * @returns {object} 用户偏好数据
 */
function getPreferences() {
  try {
    if (fs.existsSync(PREFERENCES_FILE)) {
      const data = fs.readFileSync(PREFERENCES_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {
    console.error('[preferences] 读取偏好失败:', e.message);
  }
  return { language: null, lastUpdated: null };
}

/**
 * 保存用户偏好（原子写入）
 * @param {object} preferences 要保存的偏好数据
 * @returns {boolean} 是否保存成功
 */
function savePreferences(preferences) {
  try {
    // Step 1: 确保目录存在
    const memoryDir = path.dirname(PREFERENCES_FILE);
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }

    // Step 2: 读取当前数据（用于合并）
    let current = { language: null, lastUpdated: null };
    if (fs.existsSync(PREFERENCES_FILE)) {
      try {
        const raw = fs.readFileSync(PREFERENCES_FILE, 'utf8');
        current = JSON.parse(raw);
      } catch (e) {
        // 解析失败，使用空对象继续
      }
    }

    // Step 3: 合并更新（只覆盖 language 和 lastUpdated，保留其他字段）
    const updated = {
      ...current,
      ...preferences,
      lastUpdated: new Date().toISOString()
    };

    // Step 4: 原子写入（先写临时文件再 rename）
    const content = JSON.stringify(updated, null, 2);
    
    // 写临时文件
    fs.writeFileSync(TEMP_FILE, content, 'utf8');
    
    // 原子替换（OS 保证 rename 是原子的）
    fs.renameSync(TEMP_FILE, PREFERENCES_FILE);
    
    return true;
  } catch (e) {
    console.error('[preferences] 保存偏好失败:', e.message);
    
    // 清理可能残留的临时文件
    try {
      if (fs.existsSync(TEMP_FILE)) {
        fs.unlinkSync(TEMP_FILE);
      }
    } catch (cleanupError) {
      // 忽略清理失败
    }
    
    return false;
  }
}

/**
 * 获取语言偏好（中文/英文）
 * @returns {string|null} 'zh' / 'en' / null（未设置）
 */
function getLanguage() {
  const prefs = getPreferences();
  return prefs.language || null;
}

/**
 * 设置语言偏好
 * @param {string} lang 'zh' 或 'en'
 * @returns {boolean} 是否设置成功
 */
function setLanguage(lang) {
  if (lang !== 'zh' && lang !== 'en') {
    return false;
  }
  const prefs = getPreferences();
  prefs.language = lang;
  return savePreferences(prefs);
}

/**
 * 检查目录/文件权限是否正常
 * @returns {object} { writable: boolean, reason: string }
 */
function checkPermissions() {
  const memoryDir = path.dirname(PREFERENCES_FILE);
  
  // 检查目录是否存在
  if (!fs.existsSync(memoryDir)) {
    // 尝试创建
    try {
      fs.mkdirSync(memoryDir, { recursive: true });
      return { writable: true, reason: '目录已创建' };
    } catch (e) {
      return { writable: false, reason: `无法创建目录: ${e.message}` };
    }
  }
  
  // 检查目录是否可写
  try {
    const testFile = path.join(memoryDir, '.write_test');
    fs.writeFileSync(testFile, 'test');
    fs.unlinkSync(testFile);
    return { writable: true, reason: '目录可写' };
  } catch (e) {
    return { writable: false, reason: `目录不可写: ${e.message}` };
  }
}

module.exports = {
  getPreferences,
  savePreferences,
  getLanguage,
  setLanguage,
  checkPermissions
};