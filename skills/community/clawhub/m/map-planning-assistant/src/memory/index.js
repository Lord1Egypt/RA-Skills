/**
 * 记忆系统模块
 * 实现永久/长期/临时三级记忆存储、记忆索引、记忆复用功能
 */

const fs = require('fs');
const path = require('path');

// 数据存储路径
const DATA_DIR = path.join(__dirname, '../../data');
const MEMORY_FILE = path.join(DATA_DIR, 'memory.json');

// 记忆层级
const MEMORY_LEVELS = {
  PERMANENT: 'permanent',    // 永久记忆
  LONG_TERM: 'long_term',    // 长期记忆
  TEMPORARY: 'temporary'     // 临时记忆
};

// 临时记忆过期时间（7天）
const TEMPORARY_EXPIRY = 7 * 24 * 60 * 60 * 1000;

// 确保数据目录存在
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// 加载用户记忆
async function loadMemory(userId) {
  try {
    ensureDataDir();

    if (fs.existsSync(MEMORY_FILE)) {
      const data = fs.readFileSync(MEMORY_FILE, 'utf8');
      const allMemory = JSON.parse(data);
      return allMemory[userId] || createEmptyMemory();
    }

    return createEmptyMemory();
  } catch (error) {
    console.error('加载记忆失败:', error);
    return createEmptyMemory();
  }
}

// 保存用户记忆
async function saveMemory(userId, memory) {
  try {
    ensureDataDir();

    let allMemory = {};
    if (fs.existsSync(MEMORY_FILE)) {
      const data = fs.readFileSync(MEMORY_FILE, 'utf8');
      allMemory = JSON.parse(data);
    }

    allMemory[userId] = memory;

    fs.writeFileSync(MEMORY_FILE, JSON.stringify(allMemory, null, 2), 'utf8');
  } catch (error) {
    console.error('保存记忆失败:', error);
    throw error;
  }
}

// 创建空记忆结构
function createEmptyMemory() {
  return {
    permanent: {
      homeCity: '',           // 常驻城市
      preferences: [],        // 固定出行偏好
      commonTimeSlots: [],    // 常驻出行时间段
      coreTags: []            // 核心喜好标签
    },
    long_term: {
      createdMaps: [],        // 创建过的地图
      historyRoutes: [],      // 历史规划路线
      favoritePois: [],       // 收藏点位
      visitedCities: [],      // 游历城市列表
      interactionCount: 0     // 交互总次数
    },
    temporary: {
      recentInteractions: [], // 近7天交互记录
      recentSearches: [],     // 近期搜索记录
      lastActive: null        // 最后活跃时间
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  };
}

// 记录交互
async function recordInteraction(userId, intent, result) {
  try {
    const memory = await loadMemory(userId);

    // 更新临时记忆
    const interaction = {
      timestamp: new Date().toISOString(),
      intent: intent,
      resultType: result.type,
      city: intent.city || null,
      scene: intent.scene || null
    };

    memory.temporary.recentInteractions.unshift(interaction);

    // 只保留最近50条交互
    if (memory.temporary.recentInteractions.length > 50) {
      memory.temporary.recentInteractions = memory.temporary.recentInteractions.slice(0, 50);
    }

    // 更新最后活跃时间
    memory.temporary.lastActive = new Date().toISOString();

    // 更新长期记忆
    memory.long_term.interactionCount++;

    // 记录访问的城市
    if (intent.city && !memory.long_term.visitedCities.includes(intent.city)) {
      memory.long_term.visitedCities.push(intent.city);
    }

    // 记录创建的地图
    if (intent.type === 'full_map' || intent.type === 'scene_map') {
      memory.long_term.createdMaps.push({
        timestamp: new Date().toISOString(),
        city: intent.city,
        scene: intent.scene || 'full',
        district: intent.district || null
      });

      // 只保留最近100条地图记录
      if (memory.long_term.createdMaps.length > 100) {
        memory.long_term.createdMaps = memory.long_term.createdMaps.slice(0, 100);
      }
    }

    // 更新时间戳
    memory.metadata.updatedAt = new Date().toISOString();

    // 保存记忆
    await saveMemory(userId, memory);

    // 清理过期临时记忆
    await cleanExpiredMemory(userId);

  } catch (error) {
    console.error('记录交互失败:', error);
  }
}

// 清理过期临时记忆
async function cleanExpiredMemory(userId) {
  try {
    const memory = await loadMemory(userId);
    const now = Date.now();

    // 过滤掉超过7天的交互记录
    memory.temporary.recentInteractions = memory.temporary.recentInteractions.filter(interaction => {
      const interactionTime = new Date(interaction.timestamp).getTime();
      return (now - interactionTime) < TEMPORARY_EXPIRY;
    });

    // 过滤掉超过7天的搜索记录
    memory.temporary.recentSearches = memory.temporary.recentSearches.filter(search => {
      const searchTime = new Date(search.timestamp).getTime();
      return (now - searchTime) < TEMPORARY_EXPIRY;
    });

    await saveMemory(userId, memory);
  } catch (error) {
    console.error('清理过期记忆失败:', error);
  }
}

// 搜索记忆
async function searchMemory(userId, keyword) {
  try {
    const memory = await loadMemory(userId);
    const results = {
      maps: [],
      routes: [],
      cities: [],
      interactions: []
    };

    // 搜索地图记录
    results.maps = memory.long_term.createdMaps.filter(map => {
      return map.city.includes(keyword) ||
             (map.scene && map.scene.includes(keyword)) ||
             (map.district && map.district.includes(keyword));
    });

    // 搜索路线记录
    results.routes = memory.long_term.historyRoutes.filter(route => {
      return route.name.includes(keyword) ||
             route.city.includes(keyword) ||
             route.description.includes(keyword);
    });

    // 搜索城市
    results.cities = memory.long_term.visitedCities.filter(city => {
      return city.includes(keyword);
    });

    // 搜索交互记录
    results.interactions = memory.temporary.recentInteractions.filter(interaction => {
      return (interaction.city && interaction.city.includes(keyword)) ||
             (interaction.scene && interaction.scene.includes(keyword)) ||
             (interaction.intent && interaction.intent.type &&
              interaction.intent.type.includes(keyword));
    });

    return results;
  } catch (error) {
    console.error('搜索记忆失败:', error);
    return { maps: [], routes: [], cities: [], interactions: [] };
  }
}

// 获取用户常驻城市
async function getHomeCity(userId) {
  try {
    const memory = await loadMemory(userId);
    return memory.permanent.homeCity;
  } catch (error) {
    console.error('获取常驻城市失败:', error);
    return null;
  }
}

// 设置用户常驻城市
async function setHomeCity(userId, city) {
  try {
    const memory = await loadMemory(userId);
    memory.permanent.homeCity = city;
    memory.metadata.updatedAt = new Date().toISOString();
    await saveMemory(userId, memory);
  } catch (error) {
    console.error('设置常驻城市失败:', error);
    throw error;
  }
}

// 添加收藏点位
async function addFavoritePoi(userId, poi) {
  try {
    const memory = await loadMemory(userId);

    // 检查是否已收藏
    const exists = memory.long_term.favoritePois.some(fav => fav.id === poi.id);
    if (exists) {
      return { success: false, message: '该点位已收藏' };
    }

    memory.long_term.favoritePois.push({
      id: poi.id,
      name: poi.name,
      address: poi.address,
      location: poi.location,
      city: poi.city,
      type: poi.type,
      rating: poi.rating,
      timestamp: new Date().toISOString()
    });

    memory.metadata.updatedAt = new Date().toISOString();
    await saveMemory(userId, memory);

    return { success: true, message: '收藏成功' };
  } catch (error) {
    console.error('添加收藏失败:', error);
    throw error;
  }
}

// 移除收藏点位
async function removeFavoritePoi(userId, poiId) {
  try {
    const memory = await loadMemory(userId);

    const index = memory.long_term.favoritePois.findIndex(fav => fav.id === poiId);
    if (index === -1) {
      return { success: false, message: '未找到该收藏点位' };
    }

    memory.long_term.favoritePois.splice(index, 1);
    memory.metadata.updatedAt = new Date().toISOString();
    await saveMemory(userId, memory);

    return { success: true, message: '取消收藏成功' };
  } catch (error) {
    console.error('移除收藏失败:', error);
    throw error;
  }
}

// 获取收藏列表
async function getFavorites(userId) {
  try {
    const memory = await loadMemory(userId);
    return memory.long_term.favoritePois;
  } catch (error) {
    console.error('获取收藏列表失败:', error);
    return [];
  }
}

// 记录路线
async function saveRoute(userId, route) {
  try {
    const memory = await loadMemory(userId);

    memory.long_term.historyRoutes.push({
      id: Date.now().toString(),
      name: route.name,
      city: route.city,
      scene: route.scene,
      description: route.description,
      pois: route.pois,
      distance: route.distance,
      duration: route.duration,
      timestamp: new Date().toISOString()
    });

    // 只保留最近50条路线
    if (memory.long_term.historyRoutes.length > 50) {
      memory.long_term.historyRoutes = memory.long_term.historyRoutes.slice(0, 50);
    }

    memory.metadata.updatedAt = new Date().toISOString();
    await saveMemory(userId, memory);

    return { success: true, message: '路线保存成功' };
  } catch (error) {
    console.error('保存路线失败:', error);
    throw error;
  }
}

// 获取历史路线
async function getHistoryRoutes(userId) {
  try {
    const memory = await loadMemory(userId);
    return memory.long_term.historyRoutes;
  } catch (error) {
    console.error('获取历史路线失败:', error);
    return [];
  }
}

// 获取游历城市列表
async function getVisitedCities(userId) {
  try {
    const memory = await loadMemory(userId);
    return memory.long_term.visitedCities;
  } catch (error) {
    console.error('获取游历城市失败:', error);
    return [];
  }
}

// 获取交互统计
async function getInteractionStats(userId) {
  try {
    const memory = await loadMemory(userId);

    return {
      totalCount: memory.long_term.interactionCount,
      mapCount: memory.long_term.createdMaps.length,
      routeCount: memory.long_term.historyRoutes.length,
      favoriteCount: memory.long_term.favoritePois.length,
      cityCount: memory.long_term.visitedCities.length,
      recentCount: memory.temporary.recentInteractions.length
    };
  } catch (error) {
    console.error('获取交互统计失败:', error);
    return null;
  }
}

// 夜间自主学习
async function performNightLearning(userId) {
  try {
    const memory = await loadMemory(userId);

    // 分析用户偏好
    const sceneCount = {};
    const cityCount = {};
    const timeSlotCount = {};

    memory.temporary.recentInteractions.forEach(interaction => {
      // 统计场景偏好
      if (interaction.scene) {
        sceneCount[interaction.scene] = (sceneCount[interaction.scene] || 0) + 1;
      }

      // 统计城市偏好
      if (interaction.city) {
        cityCount[interaction.city] = (cityCount[interaction.city] || 0) + 1;
      }

      // 统计时间段偏好
      const hour = new Date(interaction.timestamp).getHours();
      let timeSlot;
      if (hour >= 5 && hour < 12) timeSlot = 'morning';
      else if (hour >= 12 && hour < 18) timeSlot = 'afternoon';
      else if (hour >= 18 && hour < 22) timeSlot = 'evening';
      else timeSlot = 'night';
      timeSlotCount[timeSlot] = (timeSlotCount[timeSlot] || 0) + 1;
    });

    // 更新永久记忆中的标签
    const topScenes = Object.entries(sceneCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([scene]) => scene);

    const topCities = Object.entries(cityCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([city]) => city);

    const topTimeSlots = Object.entries(timeSlotCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 2)
      .map(([slot]) => slot);

    memory.permanent.preferences = topScenes;
    memory.permanent.commonTimeSlots = topTimeSlots;

    // 更新核心标签
    const coreTags = [];
    if (topCities.length > 0) coreTags.push(`${topCities[0]}常客`);
    if (topScenes.length > 0) {
      const sceneNames = {
        dogWalking: '爱遛狗',
        running: '爱运动',
        parenting: '亲子达人',
        food: '美食爱好者',
        localLife: '市井生活家',
        checkIn: '打卡达人',
        camping: '露营爱好者',
        travel: '旅行达人'
      };
      coreTags.push(sceneNames[topScenes[0]] || topScenes[0]);
    }
    memory.permanent.coreTags = coreTags;

    // 清理无效记忆
    memory.long_term.createdMaps = memory.long_term.createdMaps.filter(map => {
      return map.city && map.timestamp;
    });

    memory.metadata.updatedAt = new Date().toISOString();
    await saveMemory(userId, memory);

    console.log(`用户 ${userId} 夜间学习完成`);
    return { success: true };
  } catch (error) {
    console.error('夜间学习失败:', error);
    return { success: false, error: error.message };
  }
}

module.exports = {
  loadMemory,
  saveMemory,
  recordInteraction,
  searchMemory,
  getHomeCity,
  setHomeCity,
  addFavoritePoi,
  removeFavoritePoi,
  getFavorites,
  saveRoute,
  getHistoryRoutes,
  getVisitedCities,
  getInteractionStats,
  performNightLearning,
  MEMORY_LEVELS
};
