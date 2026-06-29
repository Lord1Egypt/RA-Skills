/**
 * 高德地图Web服务API工具模块
 * 封装行政区划、地理编码、POI检索、POI详情、天气、路况等API调用
 */

const https = require('https');
const querystring = require('querystring');

// 从环境变量获取API Key
const API_KEY = process.env.AMAP_API_KEY;

// API基础地址
const BASE_URL = 'https://restapi.amap.com/v3';

// 请求超时时间（毫秒）
const TIMEOUT = 8000;

// 重试次数
const MAX_RETRY = 1;

// 通用请求方法
async function request(url, params = {}) {
  params.key = API_KEY;

  const queryString = querystring.stringify(params);
  const fullUrl = `${BASE_URL}/${url}?${queryString}`;

  let retryCount = 0;

  while (retryCount <= MAX_RETRY) {
    try {
      const result = await new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          reject(new Error('请求超时'));
        }, TIMEOUT);

        https.get(fullUrl, (res) => {
          let data = '';

          res.on('data', (chunk) => {
            data += chunk;
          });

          res.on('end', () => {
            clearTimeout(timer);
            try {
              const jsonData = JSON.parse(data);
              if (jsonData.status === '1') {
                resolve(jsonData);
              } else {
                reject(new Error(jsonData.info || '请求失败'));
              }
            } catch (e) {
              reject(new Error('JSON解析失败'));
            }
          });
        }).on('error', (err) => {
          clearTimeout(timer);
          reject(err);
        });
      });

      return result;
    } catch (error) {
      retryCount++;
      if (retryCount > MAX_RETRY) {
        throw error;
      }
      // 等待200ms后重试
      await new Promise(resolve => setTimeout(resolve, 200));
    }
  }
}

// 获取行政区划
async function getDistricts(city, subdistrict = 2) {
  try {
    const result = await request('config/district', {
      keywords: city,
      subdistrict: subdistrict.toString(),
      extensions: 'base'
    });

    if (result.districts && result.districts.length > 0) {
      const cityData = result.districts[0];
      const districts = [];

      if (cityData.districts) {
        for (const district of cityData.districts) {
          districts.push({
            name: district.name,
            adcode: district.adcode,
            center: district.center,
            level: district.level
          });
        }
      }

      return {
        city: cityData.name,
        adcode: cityData.adcode,
        center: cityData.center,
        districts: districts
      };
    }

    return null;
  } catch (error) {
    console.error('获取行政区划失败:', error);
    throw error;
  }
}

// 地理编码：将地址转换为经纬度
async function geocode(address, city = '') {
  try {
    const params = {
      address: address
    };
    if (city) {
      params.city = city;
    }

    const result = await request('geocode/geo', params);

    if (result.geocodes && result.geocodes.length > 0) {
      const geocode = result.geocodes[0];
      return {
        location: geocode.location,
        formattedAddress: geocode.formatted_address,
        province: geocode.province,
        city: geocode.city,
        district: geocode.district,
        adcode: geocode.adcode
      };
    }

    return null;
  } catch (error) {
    console.error('地理编码失败:', error);
    throw error;
  }
}

// POI关键字搜索
async function searchPoisByKeyword(city, keywords, types = '', page = 1, pageSize = 20) {
  try {
    const params = {
      keywords: keywords,
      city: city,
      citylimit: 'true',
      offset: pageSize.toString(),
      page: page.toString(),
      extensions: 'all'
    };

    if (types) {
      params.types = types;
    }

    const result = await request('place/text', params);

    return {
      pois: result.pois || [],
      count: parseInt(result.count) || 0
    };
  } catch (error) {
    console.error('POI关键字搜索失败:', error);
    throw error;
  }
}

// POI周边搜索
async function searchPoisByLocation(location, radius = 3000, types = '', keywords = '', page = 1, pageSize = 20) {
  try {
    const params = {
      location: location,
      radius: radius.toString(),
      offset: pageSize.toString(),
      page: page.toString(),
      extensions: 'all'
    };

    if (types) {
      params.types = types;
    }

    if (keywords) {
      params.keywords = keywords;
    }

    const result = await request('place/around', params);

    return {
      pois: result.pois || [],
      count: parseInt(result.count) || 0
    };
  } catch (error) {
    console.error('POI周边搜索失败:', error);
    throw error;
  }
}

// 搜索POI（自动选择关键字或周边搜索）
async function searchPois(city, district, types, keywords) {
  try {
    let allPois = [];
    let page = 1;
    let hasMore = true;

    // 如果指定了区县，先获取区县的中心坐标
    let location = null;
    if (district) {
      const geocodeResult = await geocode(district, city);
      if (geocodeResult) {
        location = geocodeResult.location;
      }
    }

    // 分页获取所有POI
    while (hasMore) {
      let result;

      if (location) {
        // 使用周边搜索
        result = await searchPoisByLocation(location, 5000, types, keywords.join(' '), page);
      } else {
        // 使用关键字搜索
        result = await searchPoisByKeyword(city, keywords.join(' '), types, page);
      }

      if (result.pois && result.pois.length > 0) {
        allPois = allPois.concat(result.pois);
        page++;

        // 检查是否还有更多数据
        if (allPois.length >= result.count || result.pois.length < 20) {
          hasMore = false;
        }
      } else {
        hasMore = false;
      }

      // 限制单次请求最多获取100条数据
      if (allPois.length >= 100) {
        hasMore = false;
      }
    }

    return allPois;
  } catch (error) {
    console.error('搜索POI失败:', error);
    throw error;
  }
}

// 获取POI详情
async function getPoiDetail(poiId) {
  try {
    const result = await request('place/detail', {
      id: poiId,
      extensions: 'all'
    });

    if (result.pois && result.pois.length > 0) {
      return result.pois[0];
    }

    return null;
  } catch (error) {
    console.error('获取POI详情失败:', error);
    throw error;
  }
}

// 批量获取POI详情
async function batchGetPoiDetails(pois, batchSize = 5) {
  const detailedPois = [];

  for (let i = 0; i < pois.length; i += batchSize) {
    const batch = pois.slice(i, i + batchSize);
    const promises = batch.map(poi => {
      if (poi.id) {
        return getPoiDetail(poi.id).catch(() => poi);
      }
      return Promise.resolve(poi);
    });

    const results = await Promise.all(promises);
    detailedPois.push(...results);

    // 避免请求过快
    if (i + batchSize < pois.length) {
      await new Promise(resolve => setTimeout(resolve, 200));
    }
  }

  return detailedPois;
}

// 获取天气信息
async function getWeather(city) {
  try {
    const result = await request('weather/weatherInfo', {
      city: city,
      extensions: 'all',
      output: 'JSON'
    });

    if (result.forecasts && result.forecasts.length > 0) {
      const forecast = result.forecasts[0];
      return {
        city: forecast.city,
        adcode: forecast.adcode,
        province: forecast.province,
        reporttime: forecast.reporttime,
        casts: forecast.casts.map(cast => ({
          date: cast.date,
          week: cast.week,
          dayweather: cast.dayweather,
          nightweather: cast.nightweather,
          daytemp: cast.daytemp,
          nighttemp: cast.nighttemp,
          daywind: cast.daywind,
          nightwind: cast.nightwind,
          daypower: cast.daypower,
          nightpower: cast.nightpower
        }))
      };
    }

    return null;
  } catch (error) {
    console.error('获取天气信息失败:', error);
    throw error;
  }
}

// 获取实时路况
async function getTraffic(city) {
  try {
    // 先获取城市中心坐标
    const geocodeResult = await geocode(city);
    if (!geocodeResult) {
      return null;
    }

    const result = await request('traffic/status/rectangle', {
      rectangle: geocodeResult.location + '|' + geocodeResult.location,
      extensions: 'all'
    });

    if (result.trafficinfo && result.trafficinfo.roads) {
      return {
        city: city,
        roads: result.trafficinfo.roads.map(road => ({
          name: road.name,
          status: road.status,
          direction: road.direction,
          speed: road.speed,
          lcodes: road.lcodes
        }))
      };
    }

    return null;
  } catch (error) {
    console.error('获取路况信息失败:', error);
    throw error;
  }
}

// 创建个人地图
async function createPersonalMap(data, options = {}) {
  try {
    // 提取所有POI的坐标
    const points = [];

    for (const [sceneKey, pois] of Object.entries(data)) {
      for (const poi of pois) {
        if (poi.location) {
          // 确保经纬度格式正确（经度,纬度）
          const [lng, lat] = poi.location.split(',').map(Number);
          if (!isNaN(lng) && !isNaN(lat) && lng >= 73 && lng <= 135 && lat >= 3 && lat <= 53) {
            points.push({
              name: poi.name || '未知地点',
              location: `${lng},${lat}`,
              address: poi.address || '',
              poiid: poi.id || '',
              type: sceneKey
            });
          }
        }
      }
    }

    if (points.length === 0) {
      return {
        success: false,
        message: '没有有效的POI坐标可用于创建地图',
        url: '',
        qrCode: ''
      };
    }

    // 高德API限制单次最多50个点位
    const maxPoints = options.maxPoints || 50;
    const limitedPoints = points.slice(0, maxPoints);

    // 调用个人地图创建API
    // sceneType=2: 仅创建资源点（打卡点位标记模式）
    const result = await request('maps_schema_personal_map', {
      sceneType: '2',
      points: JSON.stringify(limitedPoints)
    });

    // 构建返回结果
    const mapResult = {
      success: true,
      url: result.url || '',
      qrCode: result.qr_code || '',
      pointCount: limitedPoints.length,
      totalPoints: points.length,
      truncated: points.length > maxPoints
    };

    // 如果有截断，提示用户
    if (mapResult.truncated) {
      mapResult.message = `已创建包含前${maxPoints}个点位的地图（共${points.length}个点位）`;
    } else {
      mapResult.message = `已创建包含${limitedPoints.length}个点位的地图`;
    }

    return mapResult;
  } catch (error) {
    console.error('创建个人地图失败:', error);
    return {
      success: false,
      message: `创建地图失败: ${error.message}`,
      url: '',
      qrCode: '',
      error: error.message
    };
  }
}

// 批量创建个人地图（当点位超过50个时分批创建）
async function createBatchPersonalMaps(data, options = {}) {
  try {
    // 提取所有POI的坐标
    const allPoints = [];

    for (const [sceneKey, pois] of Object.entries(data)) {
      for (const poi of pois) {
        if (poi.location) {
          const [lng, lat] = poi.location.split(',').map(Number);
          if (!isNaN(lng) && !isNaN(lat) && lng >= 73 && lng <= 135 && lat >= 3 && lat <= 53) {
            allPoints.push({
              name: poi.name || '未知地点',
              location: `${lng},${lat}`,
              address: poi.address || '',
              poiid: poi.id || '',
              type: sceneKey
            });
          }
        }
      }
    }

    if (allPoints.length === 0) {
      return {
        success: false,
        message: '没有有效的POI坐标可用于创建地图',
        maps: []
      };
    }

    // 每批最多50个点位
    const batchSize = options.batchSize || 50;
    const maps = [];

    // 分批创建地图
    for (let i = 0; i < allPoints.length; i += batchSize) {
      const batch = allPoints.slice(i, i + batchSize);
      const batchIndex = Math.floor(i / batchSize) + 1;

      try {
        const result = await request('maps_schema_personal_map', {
          sceneType: '2',
          points: JSON.stringify(batch)
        });

        maps.push({
          batchIndex,
          pointCount: batch.length,
          url: result.url || '',
          qrCode: result.qr_code || '',
          points: batch.map(p => p.name)
        });

        // 避免请求过快
        if (i + batchSize < allPoints.length) {
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      } catch (error) {
        console.error(`创建第${batchIndex}批地图失败:`, error);
        maps.push({
          batchIndex,
          pointCount: batch.length,
          error: error.message,
          points: batch.map(p => p.name)
        });
      }
    }

    return {
      success: true,
      totalPoints: allPoints.length,
      batchCount: maps.length,
      maps: maps,
      message: `已分${maps.length}批创建地图，共${allPoints.length}个点位`
    };
  } catch (error) {
    console.error('批量创建地图失败:', error);
    return {
      success: false,
      message: `批量创建地图失败: ${error.message}`,
      maps: [],
      error: error.message
    };
  }
}

// 生成地图分享链接
function generateMapShareUrl(qrCode) {
  if (!qrCode) return '';

  // 如果是高德短链接，直接返回
  if (qrCode.startsWith('https://a.amap.com/')) {
    return qrCode;
  }

  // 否则构建高德App分享链接
  return `https://uri.amap.com/marker?position=${qrCode}`;
}

// 格式化地图结果为文本
function formatMapResult(mapResult) {
  if (!mapResult.success) {
    return `❌ ${mapResult.message}`;
  }

  let output = `📱 **高德个人地图**\n`;
  output += `📍 点位数量: ${mapResult.pointCount}个\n`;

  if (mapResult.truncated) {
    output += `⚠️ 注意: 已截取前${mapResult.pointCount}个点位（共${mapResult.totalPoints}个）\n`;
  }

  if (mapResult.url) {
    output += `🔗 地图链接: ${mapResult.url}\n`;
  }

  if (mapResult.qrCode) {
    output += `📸 二维码: ${mapResult.qrCode}\n`;
  }

  output += `\n💡 使用说明:\n`;
  output += `• 扫描二维码或点击链接可在高德App中查看全部打卡点位\n`;
  output += `• 支持一键导航到任意点位\n`;
  output += `• 可分享给好友或保存到相册\n`;

  return output;
}

// 格式化批量地图结果为文本
function formatBatchMapResult(batchResult) {
  if (!batchResult.success) {
    return `❌ ${batchResult.message}`;
  }

  let output = `📱 **高德个人地图（分批创建）**\n`;
  output += `📍 总点位数量: ${batchResult.totalPoints}个\n`;
  output += `📦 批次数量: ${batchResult.batchCount}批\n\n`;

  for (const map of batchResult.maps) {
    output += `**第${map.batchIndex}批** (${map.pointCount}个点位)\n`;

    if (map.error) {
      output += `❌ 创建失败: ${map.error}\n`;
    } else {
      if (map.url) {
        output += `🔗 地图链接: ${map.url}\n`;
      }
      if (map.qrCode) {
        output += `📸 二维码: ${map.qrCode}\n`;
      }
      output += `📍 包含点位: ${map.points.slice(0, 3).join('、')}`;
      if (map.points.length > 3) {
        output += `等${map.points.length}个`;
      }
      output += '\n';
    }
    output += '\n';
  }

  output += `💡 使用说明:\n`;
  output += `• 每张地图包含最多50个点位\n`;
  output += `• 扫描对应二维码可在高德App中查看该批次点位\n`;
  output += `• 所有地图可分别导航和分享\n`;

  return output;
}

// 路径规划
async function planRoute(origin, destination, mode = 'driving') {
  try {
    let url;
    const params = {
      origin: origin,
      destination: destination
    };

    switch (mode) {
      case 'driving':
        url = 'direction/driving';
        params.strategy = '10'; // 综合最优
        break;
      case 'walking':
        url = 'direction/walking';
        break;
      case 'transit':
        url = 'direction/transit/integrated';
        params.city = '010'; // 默认北京，需要根据实际情况修改
        break;
      default:
        url = 'direction/driving';
    }

    const result = await request(url, params);

    if (result.route) {
      return {
        distance: result.route.distance,
        duration: result.route.duration,
        steps: result.route.paths ? result.route.paths[0]?.steps : []
      };
    }

    return null;
  } catch (error) {
    console.error('路径规划失败:', error);
    throw error;
  }
}

module.exports = {
  getDistricts,
  geocode,
  searchPoisByKeyword,
  searchPoisByLocation,
  searchPois,
  getPoiDetail,
  batchGetPoiDetails,
  getWeather,
  getTraffic,
  createPersonalMap,
  planRoute
};
