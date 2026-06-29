/**
 * 活动管理模块
 * 实现同城活动检索、存储、更新、过期清理、推送功能
 */

const fs = require('fs');
const path = require('path');
const amap = require('../utils/amap');

// 数据存储路径
const DATA_DIR = path.join(__dirname, '../../data');
const ACTIVITY_FILE = path.join(DATA_DIR, 'activity.json');

// 活动类型
const ACTIVITY_TYPES = {
  EXHIBITION: 'exhibition',      // 展会
  MARKET: 'market',              // 市集
  FESTIVAL: 'festival',          // 节日活动
  CONCERT: 'concert',            // 音乐会/演出
  CULTURE: 'culture',            // 文化活动
  SPORTS: 'sports',              // 体育活动
  FOOD: 'food',                  // 美食活动
  FAMILY: 'family',              // 亲子活动
  FREE: 'free'                   // 公益活动
};

// 活动类型名称
const ACTIVITY_TYPE_NAMES = {
  [ACTIVITY_TYPES.EXHIBITION]: '展会',
  [ACTIVITY_TYPES.MARKET]: '市集',
  [ACTIVITY_TYPES.FESTIVAL]: '节日活动',
  [ACTIVITY_TYPES.CONCERT]: '演出',
  [ACTIVITY_TYPES.CULTURE]: '文化活动',
  [ACTIVITY_TYPES.SPORTS]: '体育活动',
  [ACTIVITY_TYPES.FOOD]: '美食活动',
  [ACTIVITY_TYPES.FAMILY]: '亲子活动',
  [ACTIVITY_TYPES.FREE]: '公益活动'
};

// 确保数据目录存在
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// 加载活动数据
async function loadActivities(city) {
  try {
    ensureDataDir();

    if (fs.existsSync(ACTIVITY_FILE)) {
      const data = fs.readFileSync(ACTIVITY_FILE, 'utf8');
      const allActivities = JSON.parse(data);
      return allActivities[city] || [];
    }

    return [];
  } catch (error) {
    console.error('加载活动数据失败:', error);
    return [];
  }
}

// 保存活动数据
async function saveActivities(city, activities) {
  try {
    ensureDataDir();

    let allActivities = {};
    if (fs.existsSync(ACTIVITY_FILE)) {
      const data = fs.readFileSync(ACTIVITY_FILE, 'utf8');
      allActivities = JSON.parse(data);
    }

    allActivities[city] = activities;

    fs.writeFileSync(ACTIVITY_FILE, JSON.stringify(allActivities, null, 2), 'utf8');
  } catch (error) {
    console.error('保存活动数据失败:', error);
    throw error;
  }
}

// 获取同城活动
async function getActivities(city, userProfile = null, limit = 10) {
  try {
    // 加载本地活动数据
    let activities = await loadActivities(city);

    // 清理过期活动
    activities = cleanExpiredActivities(activities);

    // 如果本地数据为空或过期，尝试从API获取
    if (activities.length === 0) {
      activities = await fetchActivitiesFromAPI(city);
      if (activities.length > 0) {
        await saveActivities(city, activities);
      }
    }

    // 根据用户画像筛选推荐活动
    if (userProfile) {
      activities = filterActivitiesByProfile(activities, userProfile);
    }

    // 按时间排序，最近的活动优先
    activities.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));

    // 限制返回数量
    activities = activities.slice(0, limit);

    return {
      success: true,
      city: city,
      count: activities.length,
      activities: activities.map(formatActivity)
    };
  } catch (error) {
    console.error('获取同城活动失败:', error);
    return {
      success: false,
      city: city,
      count: 0,
      activities: [],
      error: error.message
    };
  }
}

// 从API获取活动数据
async function fetchActivitiesFromAPI(city) {
  try {
    // 搜索展会、市集、活动等POI
    const keywords = ['展会', '市集', '音乐节', '活动中心', '展览馆', '文化馆'];
    const activities = [];

    for (const keyword of keywords) {
      const result = await amap.searchPoisByKeyword(city, keyword, '', 1, 10);

      if (result.pois && result.pois.length > 0) {
        for (const poi of result.pois) {
          // 转换为活动格式
          const activity = convertPoiToActivity(poi, keyword);
          if (activity) {
            activities.push(activity);
          }
        }
      }
    }

    // 去重
    const uniqueActivities = deduplicateActivities(activities);

    return uniqueActivities;
  } catch (error) {
    console.error('从API获取活动数据失败:', error);
    return [];
  }
}

// 将POI转换为活动格式
function convertPoiToActivity(poi, keyword) {
  try {
    // 判断活动类型
    let type = ACTIVITY_TYPES.CULTURE;
    if (keyword.includes('展会') || keyword.includes('展览')) {
      type = ACTIVITY_TYPES.EXHIBITION;
    } else if (keyword.includes('市集') || keyword.includes('集市')) {
      type = ACTIVITY_TYPES.MARKET;
    } else if (keyword.includes('音乐') || keyword.includes('演出')) {
      type = ACTIVITY_TYPES.CONCERT;
    }

    // 生成随机活动日期（未来30天内）
    const startDate = new Date();
    startDate.setDate(startDate.getDate() + Math.floor(Math.random() * 30));
    const endDate = new Date(startDate);
    endDate.setDate(endDate.getDate() + Math.floor(Math.random() * 3) + 1);

    return {
      id: poi.id || Date.now().toString(),
      name: poi.name,
      type: type,
      typeName: ACTIVITY_TYPE_NAMES[type],
      address: poi.address || '',
      location: poi.location || '',
      city: poi.city || '',
      district: poi.district || '',
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0],
      startTime: '09:00',
      endTime: '18:00',
      price: poi.biz_ext?.cost || '免费',
      rating: poi.biz_ext?.rating || '4.0',
      description: poi.business_area || '',
      tags: extractTags(poi),
      source: 'amap',
      fetchTime: new Date().toISOString()
    };
  } catch (error) {
    console.error('转换POI为活动失败:', error);
    return null;
  }
}

// 提取标签
function extractTags(poi) {
  const tags = [];

  if (poi.type) {
    const typeParts = poi.type.split('|');
    if (typeParts.length > 1) {
      tags.push(typeParts[1]);
    }
  }

  if (poi.biz_ext?.tag) {
    tags.push(...poi.biz_ext.tag.split('|'));
  }

  return [...new Set(tags)].slice(0, 5);
}

// 活动去重
function deduplicateActivities(activities) {
  const seen = new Set();
  return activities.filter(activity => {
    const key = `${activity.name}_${activity.address}`;
    if (seen.has(key)) {
      return false;
    }
    seen.add(key);
    return true;
  });
}

// 清理过期活动
function cleanExpiredActivities(activities) {
  const now = new Date();
  const today = now.toISOString().split('T')[0];

  return activities.filter(activity => {
    return activity.endDate >= today;
  });
}

// 根据用户画像筛选活动
function filterActivitiesByProfile(activities, userProfile) {
  if (!userProfile || !userProfile.preferences) {
    return activities;
  }

  // 为每个活动计算匹配分数
  const scoredActivities = activities.map(activity => {
    let score = 0;

    // 基于场景偏好加分
    if (userProfile.preferences.scenes) {
      if (activity.type === ACTIVITY_TYPES.FOOD && userProfile.preferences.scenes.food) {
        score += userProfile.preferences.scenes.food;
      }
      if (activity.type === ACTIVITY_TYPES.FAMILY && userProfile.preferences.scenes.parenting) {
        score += userProfile.preferences.scenes.parenting;
      }
      if (activity.type === ACTIVITY_TYPES.MARKET && userProfile.preferences.scenes.localLife) {
        score += userProfile.preferences.scenes.localLife;
      }
    }

    // 基于标签匹配加分
    if (userProfile.tags && activity.tags) {
      const matchingTags = activity.tags.filter(tag =>
        userProfile.tags.some(userTag => userTag.includes(tag) || tag.includes(userTag))
      );
      score += matchingTags.length * 2;
    }

    // 基于评分加分
    if (activity.rating) {
      score += parseFloat(activity.rating);
    }

    // 免费活动加分
    if (activity.price === '免费') {
      score += 3;
    }

    return { ...activity, score };
  });

  // 按分数排序
  scoredActivities.sort((a, b) => b.score - a.score);

  return scoredActivities;
}

// 格式化活动信息
function formatActivity(activity) {
  return {
    id: activity.id,
    name: activity.name,
    type: activity.typeName,
    address: activity.address,
    date: `${activity.startDate} 至 ${activity.endDate}`,
    time: `${activity.startTime} - ${activity.endTime}`,
    price: activity.price,
    rating: activity.rating,
    description: activity.description,
    tags: activity.tags,
    matchScore: activity.score || 0
  };
}

// 获取活动详情
async function getActivityDetail(activityId, city) {
  try {
    const activities = await loadActivities(city);
    const activity = activities.find(a => a.id === activityId);

    if (!activity) {
      return {
        success: false,
        message: '未找到该活动'
      };
    }

    return {
      success: true,
      activity: formatActivity(activity)
    };
  } catch (error) {
    console.error('获取活动详情失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// 获取活动类型列表
function getActivityTypes() {
  return Object.entries(ACTIVITY_TYPE_NAMES).map(([key, name]) => ({
    key,
    name
  }));
}

// 按类型获取活动
async function getActivitiesByType(city, type, limit = 10) {
  try {
    let activities = await loadActivities(city);

    // 按类型筛选
    activities = activities.filter(a => a.type === type);

    // 清理过期活动
    activities = cleanExpiredActivities(activities);

    // 按时间排序
    activities.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));

    // 限制数量
    activities = activities.slice(0, limit);

    return {
      success: true,
      type: ACTIVITY_TYPE_NAMES[type] || type,
      count: activities.length,
      activities: activities.map(formatActivity)
    };
  } catch (error) {
    console.error('按类型获取活动失败:', error);
    return {
      success: false,
      type: type,
      count: 0,
      activities: [],
      error: error.message
    };
  }
}

// 获取本周末活动
async function getWeekendActivities(city, limit = 10) {
  try {
    let activities = await loadActivities(city);

    // 计算本周末日期
    const now = new Date();
    const dayOfWeek = now.getDay();
    const daysUntilSaturday = dayOfWeek === 0 ? 6 : 6 - dayOfWeek;
    const saturday = new Date(now);
    saturday.setDate(now.getDate() + daysUntilSaturday);
    const sunday = new Date(saturday);
    sunday.setDate(saturday.getDate() + 1);

    const saturdayStr = saturday.toISOString().split('T')[0];
    const sundayStr = sunday.toISOString().split('T')[0];

    // 筛选本周末的活动
    activities = activities.filter(activity => {
      return activity.startDate <= sundayStr && activity.endDate >= saturdayStr;
    });

    // 清理过期活动
    activities = cleanExpiredActivities(activities);

    // 按评分排序
    activities.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating));

    // 限制数量
    activities = activities.slice(0, limit);

    return {
      success: true,
      weekend: `${saturdayStr} 至 ${sundayStr}`,
      count: activities.length,
      activities: activities.map(formatActivity)
    };
  } catch (error) {
    console.error('获取本周末活动失败:', error);
    return {
      success: false,
      count: 0,
      activities: [],
      error: error.message
    };
  }
}

// 获取免费活动
async function getFreeActivities(city, limit = 10) {
  try {
    let activities = await loadActivities(city);

    // 筛选免费活动
    activities = activities.filter(a => a.price === '免费');

    // 清理过期活动
    activities = cleanExpiredActivities(activities);

    // 按时间排序
    activities.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));

    // 限制数量
    activities = activities.slice(0, limit);

    return {
      success: true,
      count: activities.length,
      activities: activities.map(formatActivity)
    };
  } catch (error) {
    console.error('获取免费活动失败:', error);
    return {
      success: false,
      count: 0,
      activities: [],
      error: error.message
    };
  }
}

// 更新活动数据
async function refreshActivities(city) {
  try {
    // 从API重新获取活动数据
    const activities = await fetchActivitiesFromAPI(city);

    // 保存到本地
    await saveActivities(city, activities);

    return {
      success: true,
      message: `已更新 ${city} 的活动数据`,
      count: activities.length
    };
  } catch (error) {
    console.error('更新活动数据失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// 添加自定义活动
async function addCustomActivity(city, activityData) {
  try {
    const activities = await loadActivities(city);

    const newActivity = {
      id: `custom_${Date.now()}`,
      name: activityData.name,
      type: activityData.type || ACTIVITY_TYPES.CULTURE,
      typeName: ACTIVITY_TYPE_NAMES[activityData.type] || '文化活动',
      address: activityData.address || '',
      location: activityData.location || '',
      city: city,
      district: activityData.district || '',
      startDate: activityData.startDate,
      endDate: activityData.endDate,
      startTime: activityData.startTime || '09:00',
      endTime: activityData.endTime || '18:00',
      price: activityData.price || '免费',
      rating: activityData.rating || '4.0',
      description: activityData.description || '',
      tags: activityData.tags || [],
      source: 'custom',
      fetchTime: new Date().toISOString()
    };

    activities.push(newActivity);
    await saveActivities(city, activities);

    return {
      success: true,
      message: '活动添加成功',
      activity: formatActivity(newActivity)
    };
  } catch (error) {
    console.error('添加自定义活动失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// 删除活动
async function removeActivity(city, activityId) {
  try {
    const activities = await loadActivities(city);
    const index = activities.findIndex(a => a.id === activityId);

    if (index === -1) {
      return {
        success: false,
        message: '未找到该活动'
      };
    }

    activities.splice(index, 1);
    await saveActivities(city, activities);

    return {
      success: true,
      message: '活动删除成功'
    };
  } catch (error) {
    console.error('删除活动失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  getActivities,
  getActivityDetail,
  getActivityTypes,
  getActivitiesByType,
  getWeekendActivities,
  getFreeActivities,
  refreshActivities,
  addCustomActivity,
  removeActivity,
  ACTIVITY_TYPES,
  ACTIVITY_TYPE_NAMES
};
