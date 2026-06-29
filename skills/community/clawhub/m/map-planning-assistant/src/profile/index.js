/**
 * 用户画像模块
 * 实现用户画像自动描绘、标签管理、偏好统计
 */

const fs = require('fs');
const path = require('path');

// 数据存储路径
const DATA_DIR = path.join(__dirname, '../../data');
const PROFILE_FILE = path.join(DATA_DIR, 'profile.json');

// 确保数据目录存在
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// 加载用户画像
async function loadProfile(userId) {
  try {
    ensureDataDir();

    if (fs.existsSync(PROFILE_FILE)) {
      const data = fs.readFileSync(PROFILE_FILE, 'utf8');
      const allProfiles = JSON.parse(data);
      return allProfiles[userId] || createEmptyProfile();
    }

    return createEmptyProfile();
  } catch (error) {
    console.error('加载用户画像失败:', error);
    return createEmptyProfile();
  }
}

// 保存用户画像
async function saveProfile(userId, profile) {
  try {
    ensureDataDir();

    let allProfiles = {};
    if (fs.existsSync(PROFILE_FILE)) {
      const data = fs.readFileSync(PROFILE_FILE, 'utf8');
      allProfiles = JSON.parse(data);
    }

    allProfiles[userId] = profile;

    fs.writeFileSync(PROFILE_FILE, JSON.stringify(allProfiles, null, 2), 'utf8');
  } catch (error) {
    console.error('保存用户画像失败:', error);
    throw error;
  }
}

// 创建空画像结构
function createEmptyProfile() {
  return {
    basic: {
      homeCity: '',           // 常驻城市
      nickname: '',           // 昵称
      joinDate: new Date().toISOString()  // 加入日期
    },
    preferences: {
      scenes: {},             // 场景偏好 {scene: count}
      timeSlots: {},          // 时间段偏好 {timeSlot: count}
      transportModes: {},     // 交通方式偏好 {mode: count}
      priceRanges: {},        // 价格区间偏好 {range: count}
      styles: {}              // 风格偏好 {style: count}
    },
    tags: [],                 // 用户标签
    statistics: {
      totalInteractions: 0,   // 总交互次数
      totalMaps: 0,           // 创建地图数
      totalRoutes: 0,         // 规划路线数
      totalCities: 0,         // 游历城市数
      favoriteCount: 0        // 收藏点位数
    },
    history: {
      recentScenes: [],       // 近期使用的场景
      recentCities: [],       // 近期访问的城市
      recentTimeSlots: []     // 近期活跃时间段
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  };
}

// 更新用户画像
async function updateProfile(userId, intent) {
  try {
    const profile = await loadProfile(userId);

    // 更新场景偏好
    if (intent.scene) {
      profile.preferences.scenes[intent.scene] = (profile.preferences.scenes[intent.scene] || 0) + 1;
    }

    // 更新城市偏好
    if (intent.city) {
      // 更新近期城市记录
      profile.history.recentCities = [
        intent.city,
        ...profile.history.recentCities.filter(c => c !== intent.city)
      ].slice(0, 10);
    }

    // 更新时间段偏好
    const hour = new Date().getHours();
    let timeSlot;
    if (hour >= 5 && hour < 12) timeSlot = 'morning';
    else if (hour >= 12 && hour < 18) timeSlot = 'afternoon';
    else if (hour >= 18 && hour < 22) timeSlot = 'evening';
    else timeSlot = 'night';

    profile.preferences.timeSlots[timeSlot] = (profile.preferences.timeSlots[timeSlot] || 0) + 1;

    // 更新近期时间段记录
    profile.history.recentTimeSlots = [
      timeSlot,
      ...profile.history.recentTimeSlots.filter(t => t !== timeSlot)
    ].slice(0, 20);

    // 更新统计信息
    profile.statistics.totalInteractions++;

    if (intent.type === 'full_map' || intent.type === 'scene_map') {
      profile.statistics.totalMaps++;
    }

    if (intent.type === 'travel') {
      profile.statistics.totalRoutes++;
    }

    // 更新标签
    updateTags(profile);

    // 更新时间戳
    profile.metadata.updatedAt = new Date().toISOString();

    // 保存画像
    await saveProfile(userId, profile);

    return profile;
  } catch (error) {
    console.error('更新用户画像失败:', error);
    throw error;
  }
}

// 更新用户标签
function updateTags(profile) {
  const tags = [];

  // 基于场景偏好的标签
  const topScene = Object.entries(profile.preferences.scenes)
    .sort(([,a], [,b]) => b - a)[0];

  if (topScene) {
    const sceneNames = {
      dogWalking: '爱遛狗',
      running: '运动达人',
      parenting: '亲子达人',
      food: '美食爱好者',
      localLife: '市井生活家',
      checkIn: '打卡达人',
      camping: '露营爱好者',
      travel: '旅行达人'
    };
    tags.push(sceneNames[topScene[0]] || topScene[0]);
  }

  // 基于时间段偏好的标签
  const topTimeSlot = Object.entries(profile.preferences.timeSlots)
    .sort(([,a], [,b]) => b - a)[0];

  if (topTimeSlot) {
    const timeSlotNames = {
      morning: '早起鸟',
      afternoon: '午后达人',
      evening: '傍晚活动家',
      night: '夜猫子'
    };
    tags.push(timeSlotNames[topTimeSlot[0]] || topTimeSlot[0]);
  }

  // 基于城市偏好的标签
  if (profile.history.recentCities.length > 0) {
    tags.push(`${profile.history.recentCities[0]}常客`);
  }

  // 基于交互频率的标签
  if (profile.statistics.totalInteractions > 100) {
    tags.push('资深用户');
  } else if (profile.statistics.totalInteractions > 50) {
    tags.push('活跃用户');
  } else if (profile.statistics.totalInteractions > 10) {
    tags.push('成长用户');
  }

  // 基于地图创建数的标签
  if (profile.statistics.totalMaps > 20) {
    tags.push('地图达人');
  } else if (profile.statistics.totalMaps > 10) {
    tags.push('规划爱好者');
  }

  profile.tags = [...new Set(tags)].slice(0, 5);
}

// 获取用户偏好统计
async function getPreferenceStats(userId) {
  try {
    const profile = await loadProfile(userId);

    // 计算场景偏好百分比
    const totalSceneInteractions = Object.values(profile.preferences.scenes)
      .reduce((sum, count) => sum + count, 0);

    const scenePreferences = {};
    for (const [scene, count] of Object.entries(profile.preferences.scenes)) {
      scenePreferences[scene] = {
        count: count,
        percentage: totalSceneInteractions > 0 ? Math.round((count / totalSceneInteractions) * 100) : 0
      };
    }

    // 计算时间段偏好百分比
    const totalTimeInteractions = Object.values(profile.preferences.timeSlots)
      .reduce((sum, count) => sum + count, 0);

    const timePreferences = {};
    for (const [slot, count] of Object.entries(profile.preferences.timeSlots)) {
      timePreferences[slot] = {
        count: count,
        percentage: totalTimeInteractions > 0 ? Math.round((count / totalTimeInteractions) * 100) : 0
      };
    }

    return {
      scenePreferences,
      timePreferences,
      topCities: profile.history.recentCities.slice(0, 5),
      tags: profile.tags,
      statistics: profile.statistics
    };
  } catch (error) {
    console.error('获取偏好统计失败:', error);
    return null;
  }
}

// 设置用户常驻城市
async function setHomeCity(userId, city) {
  try {
    const profile = await loadProfile(userId);
    profile.basic.homeCity = city;
    profile.metadata.updatedAt = new Date().toISOString();
    await saveProfile(userId, profile);
  } catch (error) {
    console.error('设置常驻城市失败:', error);
    throw error;
  }
}

// 获取用户常驻城市
async function getHomeCity(userId) {
  try {
    const profile = await loadProfile(userId);
    return profile.basic.homeCity;
  } catch (error) {
    console.error('获取常驻城市失败:', error);
    return null;
  }
}

// 添加用户标签
async function addTag(userId, tag) {
  try {
    const profile = await loadProfile(userId);

    if (!profile.tags.includes(tag)) {
      profile.tags.push(tag);
      profile.tags = profile.tags.slice(0, 10); // 最多10个标签
    }

    profile.metadata.updatedAt = new Date().toISOString();
    await saveProfile(userId, profile);
  } catch (error) {
    console.error('添加标签失败:', error);
    throw error;
  }
}

// 移除用户标签
async function removeTag(userId, tag) {
  try {
    const profile = await loadProfile(userId);
    profile.tags = profile.tags.filter(t => t !== tag);
    profile.metadata.updatedAt = new Date().toISOString();
    await saveProfile(userId, profile);
  } catch (error) {
    console.error('移除标签失败:', error);
    throw error;
  }
}

// 获取用户画像摘要
async function getProfileSummary(userId) {
  try {
    const profile = await loadProfile(userId);

    const topScene = Object.entries(profile.preferences.scenes)
      .sort(([,a], [,b]) => b - a)[0];

    const topTimeSlot = Object.entries(profile.preferences.timeSlots)
      .sort(([,a], [,b]) => b - a)[0];

    const sceneNames = {
      dogWalking: '遛狗',
      running: '跑步',
      parenting: '亲子',
      food: '美食',
      localLife: '市井',
      checkIn: '打卡',
      camping: '露营',
      travel: '旅行'
    };

    const timeSlotNames = {
      morning: '早晨',
      afternoon: '下午',
      evening: '傍晚',
      night: '夜晚'
    };

    return {
      homeCity: profile.basic.homeCity || '未设置',
      topScene: topScene ? sceneNames[topScene[0]] || topScene[0] : '暂无',
      topTimeSlot: topTimeSlot ? timeSlotNames[topTimeSlot[0]] || topTimeSlot[0] : '暂无',
      tags: profile.tags,
      statistics: profile.statistics,
      recentCities: profile.history.recentCities.slice(0, 3)
    };
  } catch (error) {
    console.error('获取画像摘要失败:', error);
    return null;
  }
}

// 重置用户画像
async function resetProfile(userId) {
  try {
    const emptyProfile = createEmptyProfile();
    await saveProfile(userId, emptyProfile);
    return { success: true, message: '画像已重置' };
  } catch (error) {
    console.error('重置画像失败:', error);
    throw error;
  }
}

// 导出用户画像数据
async function exportProfile(userId) {
  try {
    const profile = await loadProfile(userId);
    return {
      success: true,
      data: profile
    };
  } catch (error) {
    console.error('导出画像失败:', error);
    return { success: false, error: error.message };
  }
}

module.exports = {
  loadProfile,
  saveProfile,
  updateProfile,
  getPreferenceStats,
  setHomeCity,
  getHomeCity,
  addTag,
  removeTag,
  getProfileSummary,
  resetProfile,
  exportProfile
};
