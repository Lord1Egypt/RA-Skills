/**
 * 全能聚合地图规划助理 (All-In-One Multi-Scenario Map Planner)
 * 基于高德Web服务API打造的全场景、全周期LBS地图助理
 */

const amap = require('./utils/amap');
const scenes = require('./config/scenes');
const memory = require('./memory/index');
const profile = require('./profile/index');
const activity = require('./activity/index');
const route = require('./route/index');
const formatter = require('./output/formatter');
const culture = require('./culture/index');

// 主入口：处理用户请求
async function main(params) {
  const { userMessage, userId = 'default' } = params;

  // 解析用户意图
  const intent = parseIntent(userMessage);

  // 加载用户记忆和画像
  const userMemory = await memory.loadMemory(userId);
  const userProfile = await profile.loadProfile(userId);

  let result;

  switch (intent.type) {
    case 'full_map':
      // 全场景地图生成
      result = await generateFullMap(intent.city, intent.district, userId);
      break;
    case 'scene_map':
      // 单场景地图生成
      result = await generateSceneMap(intent.scene, intent.city, intent.district, userId);
      break;
    case 'profile':
      // 查看用户画像
      result = formatter.formatProfile(userProfile);
      break;
    case 'history':
      // 查看历史游历
      result = formatter.formatHistory(userMemory);
      break;
    case 'activity':
      // 推送本地活动
      result = await activity.getActivities(intent.city, userProfile);
      break;
    case 'travel':
      // 旅行模式
      result = await generateTravelMap(intent.city, intent.days, intent.mode, userId);
      break;
    case 'culture':
      // 人文讲解
      result = await culture.getCultureInfo(intent.place, intent.city);
      break;
    default:
      result = { type: 'error', message: '抱歉，我没能理解您的请求。请尝试以下指令：\n1. 生成XX市全能游玩地图\n2. 帮我做XX区溜娃地图\n3. 查看我的用户画像\n4. 推送本周本地活动' };
  }

  // 记录本次交互到记忆系统
  await memory.recordInteraction(userId, intent, result);

  // 更新用户画像
  await profile.updateProfile(userId, intent);

  return result;
}

// 解析用户意图
function parseIntent(message) {
  const text = message.trim();

  // 全场景地图生成
  const fullMapMatch = text.match(/(?:生成|制作|创建)(.+?)(?:全能|全功能|全套|全部)(?:游玩|休闲|旅行|地图)/);
  if (fullMapMatch) {
    const city = extractCity(fullMapMatch[1]);
    const district = extractDistrict(fullMapMatch[1]);
    return { type: 'full_map', city, district };
  }

  // 单场景地图生成
  for (const [sceneKey, sceneConfig] of Object.entries(scenes)) {
    const sceneMatch = text.match(new RegExp(`(?:生成|制作|创建|帮我做|帮我找)(.+?)(${sceneConfig.keywords.join('|')})(?:地图|清单|路线)?`));
    if (sceneMatch) {
      const city = extractCity(sceneMatch[1] + sceneMatch[2]);
      const district = extractDistrict(sceneMatch[1]);
      return { type: 'scene_map', scene: sceneKey, city, district };
    }
  }

  // 用户画像
  if (text.match(/(?:查看|显示|看看)(?:我的)?(?:用户画像|个人画像|偏好)/)) {
    return { type: 'profile' };
  }

  // 历史游历
  if (text.match(/(?:查看|显示|看看|调取)(?:我的)?(?:历史|游历|足迹|去过)/)) {
    return { type: 'history' };
  }

  // 本地活动
  if (text.includes('活动') || text.includes('展会') || text.includes('市集') || text.includes('演出')) {
    if (text.includes('推送') || text.includes('获取') || text.includes('查看') || text.includes('找') || text.includes('看看') || text.includes('本周') || text.includes('近期') || text.includes('最新') || text.includes('本地')) {
      const city = extractCity(text);
      return { type: 'activity', city };
    }
  }

  // 旅行模式
  const travelMatch = text.match(/(?:开启|进入)?(?:旅行模式)?(?:规划|安排)?(\d+)?(?:天|日).*?(自驾|步行|公交|旅行|游)/);
  if (travelMatch) {
    const city = extractCity(text);
    const days = parseInt(travelMatch[1]) || 3;
    let mode = '自驾';
    if (travelMatch[2]) {
      if (travelMatch[2].includes('步行')) mode = 'walking';
      else if (travelMatch[2].includes('公交')) mode = 'transit';
      else mode = 'driving';
    }
    return { type: 'travel', city, days, mode };
  }

  // 人文讲解
  const cultureMatch = text.match(/(?:讲解|介绍|说说|讲讲)(?:一下)?(.+?)(?:的)?(?:历史|人文|文化|典故|故事)/);
  if (cultureMatch) {
    const city = extractCity(text);
    return { type: 'culture', place: cultureMatch[1].trim(), city };
  }

  // 尝试提取城市和场景
  const city = extractCity(text);
  if (city) {
    // 检查是否包含场景关键词
    for (const [sceneKey, sceneConfig] of Object.entries(scenes)) {
      if (sceneConfig.keywords.some(kw => text.includes(kw))) {
        return { type: 'scene_map', scene: sceneKey, city, district: extractDistrict(text) };
      }
    }
    // 默认生成全场景地图
    return { type: 'full_map', city, district: extractDistrict(text) };
  }

  return { type: 'unknown' };
}

// 提取城市名称
function extractCity(text) {
  // 常见城市列表
  const cities = [
    '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '重庆', '武汉', '西安',
    '苏州', '天津', '郑州', '长沙', '青岛', '大连', '厦门', '昆明', '贵阳', '合肥',
    '福州', '济南', '哈尔滨', '长春', '沈阳', '南宁', '兰州', '银川', '西宁', '拉萨',
    '乌鲁木齐', '呼和浩特', '太原', '石家庄', '海口', '三亚', '珠海', '东莞', '佛山',
    '中山', '惠州', '无锡', '常州', '徐州', '温州', '宁波', '嘉兴', '绍兴', '金华',
    '台州', '泉州', '漳州', '南昌', '赣州', '洛阳', '开封', '许昌', '新乡', '安阳',
    '潍坊', '烟台', '威海', '济宁', '泰安', '临沂', '淄博', '德州', '聊城', '滨州',
    '菏泽', '枣庄', '日照', '芜湖', '马鞍山', '安庆', '蚌埠', '阜阳', '六安', '亳州',
    '宜昌', '荆州', '黄冈', '孝感', '十堰', '襄阳', '岳阳', '常德', '株洲', '湘潭',
    '衡阳', '邵阳', '郴州', '永州', '怀化', '娄底', '益阳', '张家界', '湘西'
  ];

  for (const city of cities) {
    if (text.includes(city)) {
      return city;
    }
  }

  // 尝试匹配XX市格式
  const cityMatch = text.match(/([一-龥]{2,4}市)/);
  if (cityMatch) {
    return cityMatch[1].replace('市', '');
  }

  return null;
}

// 提取区县名称
function extractDistrict(text) {
  const districtMatch = text.match(/([一-龥]{2,4}(?:区|县|市|镇))/);
  if (districtMatch) {
    return districtMatch[1];
  }
  return null;
}

// 生成全场景地图
async function generateFullMap(city, district, userId) {
  try {
    // 获取行政区划
    const districts = await amap.getDistricts(city);

    // 获取所有场景的POI
    const allPois = {};
    const sceneKeys = Object.keys(scenes);

    for (const sceneKey of sceneKeys) {
      const sceneConfig = scenes[sceneKey];
      const pois = await amap.searchPois(city, district, sceneConfig.types, sceneConfig.keywords);
      allPois[sceneKey] = pois;
    }

    // 数据加工：去重、排序、补充详情
    const processedData = await processData(allPois, city);

    // 生成路线
    const routes = await route.planRoutes(processedData, city, district);

    // 获取本地活动
    const activities = await activity.getActivities(city);

    // 统计总POI数量
    const totalPois = Object.values(processedData).reduce((sum, pois) => sum + pois.length, 0);

    // 根据点位数量选择创建方式
    let mapResult;
    if (totalPois > 50) {
      // 点位超过50个，分批创建
      mapResult = await amap.createBatchPersonalMaps(processedData);
    } else {
      // 点位不超过50个，单次创建
      mapResult = await amap.createPersonalMap(processedData);
    }

    // 格式化输出
    return formatter.formatFullMap({
      city,
      district,
      data: processedData,
      routes,
      activities,
      mapResult: mapResult
    });
  } catch (error) {
    console.error('生成全场景地图失败:', error);
    return { type: 'error', message: `生成地图时出错：${error.message}` };
  }
}

// 生成单场景地图
async function generateSceneMap(sceneKey, city, district, userId) {
  try {
    const sceneConfig = scenes[sceneKey];
    if (!sceneConfig) {
      return { type: 'error', message: '不支持的地图类型' };
    }

    // 获取行政区划
    const districts = await amap.getDistricts(city);

    // 搜索该场景的POI
    const pois = await amap.searchPois(city, district, sceneConfig.types, sceneConfig.keywords);

    // 补充POI详情
    const detailedPois = await amap.batchGetPoiDetails(pois);

    // 过滤和排序
    const filteredPois = filterAndSortPois(detailedPois, sceneConfig);

    // 生成路线
    const routes = await route.planSingleSceneRoutes(filteredPois, city, district, sceneKey);

    // 获取相关活动
    const activities = await activity.getActivities(city, sceneKey);

    // 生成个人地图
    const mapResult = await amap.createPersonalMap({ [sceneKey]: filteredPois });

    // 格式化输出
    return formatter.formatSceneMap({
      scene: sceneKey,
      sceneConfig,
      city,
      district,
      pois: filteredPois,
      routes,
      activities,
      mapResult: mapResult
    });
  } catch (error) {
    console.error('生成单场景地图失败:', error);
    return { type: 'error', message: `生成地图时出错：${error.message}` };
  }
}

// 生成旅行地图
async function generateTravelMap(city, days, mode, userId) {
  try {
    // 获取所有场景POI
    const allPois = {};
    for (const [sceneKey, sceneConfig] of Object.entries(scenes)) {
      const pois = await amap.searchPois(city, null, sceneConfig.types, sceneConfig.keywords);
      allPois[sceneKey] = pois;
    }

    // 获取天气信息
    const weather = await amap.getWeather(city);

    // 获取路况信息
    const traffic = await amap.getTraffic(city);

    // 数据加工
    const processedData = await processData(allPois, city);

    // 根据天气和路况优化路线
    const optimizedRoutes = await route.planTravelRoutes({
      data: processedData,
      city,
      days,
      mode,
      weather,
      traffic
    });

    // 统计总POI数量
    const totalPois = Object.values(processedData).reduce((sum, pois) => sum + pois.length, 0);

    // 根据点位数量选择创建方式
    let mapResult;
    if (totalPois > 50) {
      // 点位超过50个，分批创建
      mapResult = await amap.createBatchPersonalMaps(processedData);
    } else {
      // 点位不超过50个，单次创建
      mapResult = await amap.createPersonalMap(processedData);
    }

    // 格式化输出
    return formatter.formatTravelMap({
      city,
      days,
      mode,
      data: processedData,
      routes: optimizedRoutes,
      weather,
      mapResult: mapResult
    });
  } catch (error) {
    console.error('生成旅行地图失败:', error);
    return { type: 'error', message: `生成地图时出错：${error.message}` };
  }
}

// 数据加工：去重、排序、补充详情
async function processData(allPois, city) {
  const processed = {};

  for (const [sceneKey, pois] of Object.entries(allPois)) {
    // 去重
    const uniquePois = deduplicatePois(pois);

    // 补充详情
    const detailedPois = await amap.batchGetPoiDetails(uniquePois);

    // 过滤和排序
    const sceneConfig = scenes[sceneKey];
    const filteredPois = filterAndSortPois(detailedPois, sceneConfig);

    processed[sceneKey] = filteredPois;
  }

  return processed;
}

// POI去重
function deduplicatePois(pois) {
  const seen = new Set();
  return pois.filter(poi => {
    if (seen.has(poi.id)) {
      return false;
    }
    seen.add(poi.id);
    return true;
  });
}

// 过滤和排序POI
function filterAndSortPois(pois, sceneConfig) {
  return pois
    .filter(poi => {
      // 评分过滤
      if (poi.rating && parseFloat(poi.rating) < (sceneConfig.minRating || 4.0)) {
        return false;
      }
      // 状态过滤
      if (poi.status === 'closed' || poi.status === '停业') {
        return false;
      }
      return true;
    })
    .sort((a, b) => {
      // 按评分降序
      const ratingA = parseFloat(a.rating) || 0;
      const ratingB = parseFloat(b.rating) || 0;
      if (ratingB !== ratingA) {
        return ratingB - ratingA;
      }
      // 按人气/热度
      const popularityA = parseInt(a.popularity) || 0;
      const popularityB = parseInt(b.popularity) || 0;
      return popularityB - popularityA;
    })
    .slice(0, sceneConfig.maxResults || 20);
}

module.exports = { main, parseIntent };
