/**
 * 路线规划模块
 * 实现路线编排、多日行程拆分、天气/路况联动优化
 */

const amap = require('../utils/amap');
const scenes = require('../config/scenes');

// 交通方式
const TRANSPORT_MODES = {
  DRIVING: 'driving',
  WALKING: 'walking',
  TRANSIT: 'transit'
};

// 路线规划策略
const ROUTE_STRATEGIES = {
  SHORTEST: 'shortest',      // 最短距离
  FASTEST: 'fastest',        // 最快时间
  SCENIC: 'scenic',          // 风景最优
  BALANCED: 'balanced'       // 综合平衡
};

// 规划单场景路线
async function planSingleSceneRoutes(pois, city, district, sceneKey) {
  try {
    if (!pois || pois.length === 0) {
      return [];
    }

    const sceneConfig = scenes[sceneKey];
    const routes = [];

    // 按区域分组
    const groupedPois = groupPoisByDistrict(pois);

    for (const [districtName, districtPois] of Object.entries(groupedPois)) {
      // 每个区域规划一条路线
      const route = await planRouteForDistrict(districtPois, districtName, sceneConfig);

      if (route) {
        routes.push({
          name: `${districtName}${sceneConfig.name}`,
          district: districtName,
          scene: sceneKey,
          sceneName: sceneConfig.name,
          ...route
        });
      }
    }

    return routes;
  } catch (error) {
    console.error('规划单场景路线失败:', error);
    return [];
  }
}

// 规划全场景路线
async function planRoutes(data, city, district) {
  try {
    const routes = [];

    // 为每个场景规划路线
    for (const [sceneKey, pois] of Object.entries(data)) {
      if (pois && pois.length > 0) {
        const sceneRoutes = await planSingleSceneRoutes(pois, city, district, sceneKey);
        routes.push(...sceneRoutes);
      }
    }

    // 按区域整合路线
    const integratedRoutes = integrateRoutesByDistrict(routes);

    return integratedRoutes;
  } catch (error) {
    console.error('规划全场景路线失败:', error);
    return [];
  }
}

// 规划旅行路线
async function planTravelRoutes(params) {
  try {
    const { data, city, days, mode, weather, traffic } = params;

    // 收集所有POI
    const allPois = [];
    for (const [sceneKey, pois] of Object.entries(data)) {
      if (pois && pois.length > 0) {
        for (const poi of pois) {
          allPois.push({
            ...poi,
            scene: sceneKey,
            priority: calculatePoiPriority(poi, sceneKey)
          });
        }
      }
    }

    // 按优先级排序
    allPois.sort((a, b) => b.priority - a.priority);

    // 根据天气和路况调整POI
    const adjustedPois = adjustPoisByWeatherAndTraffic(allPois, weather, traffic);

    // 按天数分配POI
    const dailyPois = allocatePoisToDays(adjustedPois, days);

    // 为每天规划路线
    const routes = [];
    for (let day = 0; day < days; day++) {
      const dayPois = dailyPois[day] || [];
      if (dayPois.length > 0) {
        const dayRoute = await planDayRoute(dayPois, city, mode, day + 1);
        routes.push(dayRoute);
      }
    }

    return routes;
  } catch (error) {
    console.error('规划旅行路线失败:', error);
    return [];
  }
}

// 按区域分组POI
function groupPoisByDistrict(pois) {
  const groups = {};

  for (const poi of pois) {
    const district = poi.district || '其他区域';
    if (!groups[district]) {
      groups[district] = [];
    }
    groups[district].push(poi);
  }

  return groups;
}

// 为单个区域规划路线
async function planRouteForDistrict(pois, districtName, sceneConfig) {
  try {
    if (pois.length === 0) {
      return null;
    }

    // 限制POI数量
    const limitedPois = pois.slice(0, 10);

    // 计算最佳访问顺序（贪心算法）
    const orderedPois = calculateOptimalOrder(limitedPois);

    // 计算总距离和时间
    let totalDistance = 0;
    let totalDuration = 0;
    const steps = [];

    for (let i = 0; i < orderedPois.length - 1; i++) {
      const origin = orderedPois[i].location;
      const destination = orderedPois[i + 1].location;

      if (origin && destination) {
        const routeResult = await amap.planRoute(origin, destination, 'walking');

        if (routeResult) {
          totalDistance += parseInt(routeResult.distance) || 0;
          totalDuration += parseInt(routeResult.duration) || 0;

          steps.push({
            from: orderedPois[i].name,
            to: orderedPois[i + 1].name,
            distance: routeResult.distance,
            duration: routeResult.duration
          });
        }
      }
    }

    // 生成路线描述
    const description = generateRouteDescription(orderedPois, sceneConfig);

    return {
      pois: orderedPois.map(poi => ({
        id: poi.id,
        name: poi.name,
        address: poi.address,
        location: poi.location,
        rating: poi.rating
      })),
      totalDistance: formatDistance(totalDistance),
      totalDuration: formatDuration(totalDuration),
      steps: steps,
      description: description,
      tips: sceneConfig.tips || []
    };
  } catch (error) {
    console.error('规划区域路线失败:', error);
    return null;
  }
}

// 计算最优访问顺序（贪心算法）
function calculateOptimalOrder(pois) {
  if (pois.length <= 1) {
    return pois;
  }

  const ordered = [pois[0]];
  const remaining = pois.slice(1);

  while (remaining.length > 0) {
    const current = ordered[ordered.length - 1];
    let nearestIndex = 0;
    let nearestDistance = Infinity;

    for (let i = 0; i < remaining.length; i++) {
      const distance = calculateDistance(current.location, remaining[i].location);
      if (distance < nearestDistance) {
        nearestDistance = distance;
        nearestIndex = i;
      }
    }

    ordered.push(remaining[nearestIndex]);
    remaining.splice(nearestIndex, 1);
  }

  return ordered;
}

// 计算两点之间的距离（米）
function calculateDistance(location1, location2) {
  if (!location1 || !location2) {
    return Infinity;
  }

  const [lng1, lat1] = location1.split(',').map(Number);
  const [lng2, lat2] = location2.split(',').map(Number);

  // Haversine公式
  const R = 6371000; // 地球半径（米）
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLng / 2) * Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
}

// 角度转弧度
function toRad(deg) {
  return deg * Math.PI / 180;
}

// 整合区域路线
function integrateRoutesByDistrict(routes) {
  const integrated = {};

  for (const route of routes) {
    const district = route.district;
    if (!integrated[district]) {
      integrated[district] = {
        name: `${district}游玩路线`,
        district: district,
        scenes: [],
        totalPois: 0,
        totalDistance: 0,
        totalDuration: 0
      };
    }

    integrated[district].scenes.push({
      scene: route.scene,
      sceneName: route.sceneName,
      pois: route.pois,
      distance: route.totalDistance,
      duration: route.totalDuration
    });

    integrated[district].totalPois += route.pois.length;
    integrated[district].totalDistance += parseDistance(route.totalDistance);
    integrated[district].totalDuration += parseDuration(route.totalDuration);
  }

  // 格式化输出
  return Object.values(integrated).map(route => ({
    ...route,
    totalDistance: formatDistance(route.totalDistance),
    totalDuration: formatDuration(route.totalDuration)
  }));
}

// 计算POI优先级
function calculatePoiPriority(poi, sceneKey) {
  let priority = 0;

  // 评分权重
  if (poi.rating) {
    priority += parseFloat(poi.rating) * 10;
  }

  // 场景匹配权重
  if (poi.type && poi.type.includes(sceneKey)) {
    priority += 20;
  }

  // 人气权重
  if (poi.popularity) {
    priority += parseInt(poi.popularity);
  }

  // 免费场所加分
  if (poi.price === '免费' || poi.price === '0') {
    priority += 5;
  }

  return priority;
}

// 根据天气和路况调整POI
function adjustPoisByWeatherAndTraffic(pois, weather, traffic) {
  if (!weather && !traffic) {
    return pois;
  }

  return pois.map(poi => {
    let adjustedPriority = poi.priority;

    // 天气调整
    if (weather) {
      const todayWeather = weather.casts?.[0];

      if (todayWeather) {
        // 雨天降低户外POI优先级
        if (todayWeather.dayweather.includes('雨') || todayWeather.nightweather.includes('雨')) {
          if (isOutdoorPoi(poi)) {
            adjustedPriority -= 15;
          } else {
            adjustedPriority += 10;
          }
        }

        // 高温天气降低户外POI优先级
        if (parseInt(todayWeather.daytemp) > 35) {
          if (isOutdoorPoi(poi)) {
            adjustedPriority -= 10;
          } else {
            adjustedPriority += 5;
          }
        }

        // 大风天气降低山顶、露天POI优先级
        if (todayWeather.daywind === '大风' || todayWeather.nightwind === '大风') {
          if (isExposedPoi(poi)) {
            adjustedPriority -= 20;
          }
        }
      }
    }

    // 路况调整
    if (traffic && traffic.roads) {
      // 检查POI附近是否有拥堵路段
      const isCongested = traffic.roads.some(road => {
        return road.status === '拥堵' && poi.address && poi.address.includes(road.name);
      });

      if (isCongested) {
        adjustedPriority -= 10;
      }
    }

    return { ...poi, priority: adjustedPriority };
  });
}

// 判断是否为户外POI
function isOutdoorPoi(poi) {
  const outdoorKeywords = ['公园', '步道', '跑道', '湖', '河', '山', '广场', '绿地'];
  return outdoorKeywords.some(keyword =>
    (poi.name && poi.name.includes(keyword)) ||
    (poi.type && poi.type.includes(keyword))
  );
}

// 判断是否为暴露POI
function isExposedPoi(poi) {
  const exposedKeywords = ['山顶', '观景台', '露天', '天台'];
  return exposedKeywords.some(keyword =>
    (poi.name && poi.name.includes(keyword)) ||
    (poi.type && poi.type.includes(keyword))
  );
}

// 将POI分配到各天
function allocatePoisToDays(pois, days) {
  const dailyPois = Array.from({ length: days }, () => []);

  // 按区域分组
  const groupedByDistrict = {};
  for (const poi of pois) {
    const district = poi.district || '其他';
    if (!groupedByDistrict[district]) {
      groupedByDistrict[district] = [];
    }
    groupedByDistrict[district].push(poi);
  }

  // 轮流分配各区域的POI到各天
  let currentDay = 0;
  for (const [district, districtPois] of Object.entries(groupedByDistrict)) {
    for (const poi of districtPois) {
      dailyPois[currentDay].push(poi);
      currentDay = (currentDay + 1) % days;
    }
  }

  return dailyPois;
}

// 规划单日路线
async function planDayRoute(pois, city, mode, dayNumber) {
  try {
    // 计算最优顺序
    const orderedPois = calculateOptimalOrder(pois);

    // 根据时间段安排POI
    const morningPois = [];
    const afternoonPois = [];
    const eveningPois = [];

    for (const poi of orderedPois) {
      const timeRecommendation = getPoiTimeRecommendation(poi);
      if (timeRecommendation === 'morning') {
        morningPois.push(poi);
      } else if (timeRecommendation === 'evening') {
        eveningPois.push(poi);
      } else {
        afternoonPois.push(poi);
      }
    }

    // 合并时间段
    const timeSlots = [];
    if (morningPois.length > 0) {
      timeSlots.push({
        time: '上午 (9:00-12:00)',
        pois: morningPois
      });
    }
    if (afternoonPois.length > 0) {
      timeSlots.push({
        time: '下午 (13:00-17:00)',
        pois: afternoonPois
      });
    }
    if (eveningPois.length > 0) {
      timeSlots.push({
        time: '傍晚/晚上 (17:00-21:00)',
        pois: eveningPois
      });
    }

    // 计算总距离和时间
    let totalDistance = 0;
    let totalDuration = 0;

    for (let i = 0; i < orderedPois.length - 1; i++) {
      const origin = orderedPois[i].location;
      const destination = orderedPois[i + 1].location;

      if (origin && destination) {
        const routeResult = await amap.planRoute(origin, destination, mode);
        if (routeResult) {
          totalDistance += parseInt(routeResult.distance) || 0;
          totalDuration += parseInt(routeResult.duration) || 0;
        }
      }
    }

    return {
      day: dayNumber,
      date: getDateForDay(dayNumber),
      timeSlots: timeSlots,
      totalPois: orderedPois.length,
      totalDistance: formatDistance(totalDistance),
      totalDuration: formatDuration(totalDuration),
      transportMode: mode,
      tips: getDayTips(mode, weather)
    };
  } catch (error) {
    console.error('规划单日路线失败:', error);
    return null;
  }
}

// 获取POI推荐访问时间
function getPoiTimeRecommendation(poi) {
  const name = poi.name || '';
  const type = poi.type || '';

  // 景点、公园适合上午
  if (name.includes('公园') || name.includes('景点') || name.includes('博物馆')) {
    return 'morning';
  }

  // 美食、餐厅适合中午或晚上
  if (name.includes('餐厅') || name.includes('美食') || type.includes('餐饮')) {
    return 'afternoon';
  }

  // 夜市、夜景适合晚上
  if (name.includes('夜市') || name.includes('夜景') || name.includes('酒吧')) {
    return 'evening';
  }

  // 默认下午
  return 'afternoon';
}

// 获取第N天的日期
function getDateForDay(dayNumber) {
  const date = new Date();
  date.setDate(date.getDate() + dayNumber - 1);
  return date.toISOString().split('T')[0];
}

// 获取每日提示
function getDayTips(mode, weather) {
  const tips = [];

  // 交通方式提示
  switch (mode) {
    case 'driving':
      tips.push('建议提前查看停车位');
      tips.push('注意避开高峰时段');
      break;
    case 'walking':
      tips.push('请穿着舒适的鞋子');
      tips.push('注意补充水分');
      break;
    case 'transit':
      tips.push('建议提前规划公交/地铁线路');
      tips.push('注意末班车时间');
      break;
  }

  // 天气提示
  if (weather) {
    const todayWeather = weather.casts?.[0];
    if (todayWeather) {
      if (todayWeather.dayweather.includes('雨')) {
        tips.push('今天有雨，请携带雨具');
      }
      if (parseInt(todayWeather.daytemp) > 30) {
        tips.push('今天气温较高，请注意防暑');
      }
      if (parseInt(todayWeather.daytemp) < 10) {
        tips.push('今天气温较低，请注意保暖');
      }
    }
  }

  return tips;
}

// 生成路线描述
function generateRouteDescription(pois, sceneConfig) {
  if (pois.length === 0) {
    return '暂无路线';
  }

  const poiNames = pois.slice(0, 3).map(poi => poi.name).join('、');
  const moreText = pois.length > 3 ? `等${pois.length}个地点` : '';

  return `从${poiNames}${moreText}出发，按照${sceneConfig.name}主题规划的最佳路线游览。`;
}

// 格式化距离
function formatDistance(meters) {
  if (meters >= 1000) {
    return `${(meters / 1000).toFixed(1)}公里`;
  }
  return `${meters}米`;
}

// 格式化时间
function formatDuration(seconds) {
  if (seconds >= 3600) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}小时${minutes}分钟`;
  }
  const minutes = Math.floor(seconds / 60);
  return `${minutes}分钟`;
}

// 解析距离字符串
function parseDistance(distanceStr) {
  if (!distanceStr) return 0;
  const match = distanceStr.match(/([\d.]+)(公里|米)/);
  if (match) {
    const value = parseFloat(match[1]);
    return match[2] === '公里' ? value * 1000 : value;
  }
  return 0;
}

// 解析时间字符串
function parseDuration(durationStr) {
  if (!durationStr) return 0;
  const hourMatch = durationStr.match(/(\d+)小时/);
  const minuteMatch = durationStr.match(/(\d+)分钟/);
  let seconds = 0;
  if (hourMatch) seconds += parseInt(hourMatch[1]) * 3600;
  if (minuteMatch) seconds += parseInt(minuteMatch[1]) * 60;
  return seconds;
}

// 优化路线（考虑实时因素）
async function optimizeRoute(route, options = {}) {
  try {
    const { weather, traffic, timeOfDay } = options;

    // 获取实时路况
    let trafficData = traffic;
    if (!trafficData && route.city) {
      trafficData = await amap.getTraffic(route.city);
    }

    // 根据实时因素调整路线
    const optimizedPois = route.pois.map(poi => {
      let adjustedPoi = { ...poi };

      // 时间因素
      if (timeOfDay === 'morning') {
        // 早晨优先安排户外活动
        if (isOutdoorPoi(poi)) {
          adjustedPoi.priority = (adjustedPoi.priority || 0) + 5;
        }
      } else if (timeOfDay === 'evening') {
        // 傍晚优先安排夜景、美食
        if (poi.name.includes('夜景') || poi.name.includes('美食')) {
          adjustedPoi.priority = (adjustedPoi.priority || 0) + 10;
        }
      }

      // 路况因素
      if (trafficData && trafficData.roads) {
        const isCongested = trafficData.roads.some(road => {
          return road.status === '拥堵' && poi.address && poi.address.includes(road.name);
        });
        if (isCongested) {
          adjustedPoi.priority = (adjustedPoi.priority || 0) - 10;
        }
      }

      return adjustedPoi;
    });

    // 重新排序
    optimizedPois.sort((a, b) => (b.priority || 0) - (a.priority || 0));

    return {
      ...route,
      pois: optimizedPois,
      optimized: true,
      optimizationFactors: {
        weather: weather ? '已考虑' : '未获取',
        traffic: trafficData ? '已考虑' : '未获取',
        timeOfDay: timeOfDay || '未指定'
      }
    };
  } catch (error) {
    console.error('优化路线失败:', error);
    return route;
  }
}

// 导出路线为文本
function exportRouteAsText(route) {
  let text = `📍 ${route.name}\n`;
  text += `📍 区域: ${route.district}\n`;
  text += `📍 总距离: ${route.totalDistance}\n`;
  text += `📍 预计用时: ${route.totalDuration}\n\n`;

  if (route.timeSlots) {
    for (const slot of route.timeSlots) {
      text += `⏰ ${slot.time}\n`;
      for (const poi of slot.pois) {
        text += `  • ${poi.name}`;
        if (poi.address) text += ` (${poi.address})`;
        text += '\n';
      }
      text += '\n';
    }
  } else if (route.pois) {
    text += '📍 游览顺序:\n';
    for (let i = 0; i < route.pois.length; i++) {
      text += `  ${i + 1}. ${route.pois[i].name}`;
      if (route.pois[i].address) text += ` (${route.pois[i].address})`;
      text += '\n';
    }
  }

  if (route.tips && route.tips.length > 0) {
    text += '\n💡 温馨提示:\n';
    for (const tip of route.tips) {
      text += `  • ${tip}\n`;
    }
  }

  return text;
}

module.exports = {
  planSingleSceneRoutes,
  planRoutes,
  planTravelRoutes,
  optimizeRoute,
  exportRouteAsText,
  TRANSPORT_MODES,
  ROUTE_STRATEGIES
};
