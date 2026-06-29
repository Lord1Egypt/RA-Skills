/**
 * 输出格式化模块
 * 实现标准化输出模板渲染
 */

const scenes = require('../config/scenes');

// 格式化全场景地图输出
function formatFullMap(data) {
  const { city, district, data: sceneData, routes, activities, mapResult } = data;

  let output = '';

  // 头部信息
  output += `🗺️ **${city}全能游玩地图**\n`;
  output += `📍 区域: ${district || '全市'}\n`;
  output += `👥 适配人群: 全年龄段\n`;
  output += `⏰ 建议游玩时长: 2-3天\n\n`;

  // 统计模块
  const totalPois = Object.values(sceneData).reduce((sum, pois) => sum + pois.length, 0);
  output += `📊 **打卡统计**\n`;
  output += `• 点位总数: ${totalPois}个\n`;
  output += `• 覆盖场景: ${Object.keys(sceneData).length}个\n`;
  output += `• 覆盖区域: ${routes ? routes.length : 0}个\n\n`;

  // 分场景TOP5点位
  output += `📍 **优质点位推荐**\n\n`;

  for (const [sceneKey, pois] of Object.entries(sceneData)) {
    if (pois && pois.length > 0) {
      const sceneConfig = scenes[sceneKey];
      output += `${sceneConfig.icon} **${sceneConfig.name}**\n`;

      const top5 = pois.slice(0, 5);
      for (let i = 0; i < top5.length; i++) {
        const poi = top5[i];
        output += `${i + 1}. ${poi.name}`;
        if (poi.rating) output += ` ⭐${poi.rating}`;
        if (poi.address) output += `\n   📍 ${poi.address}`;
        if (poi.biz_ext?.cost) output += `\n   💰 人均: ${poi.biz_ext.cost}`;
        output += '\n';
      }
      output += '\n';
    }
  }

  // 路线模块
  if (routes && routes.length > 0) {
    output += `🚗 **游玩路线**\n\n`;

    for (const route of routes) {
      output += `📍 **${route.name}**\n`;
      output += `• 总距离: ${route.totalDistance}\n`;
      output += `• 预计用时: ${route.totalDuration}\n`;
      output += `• 游览点位: ${route.totalPois}个\n`;

      if (route.scenes) {
        output += `• 涵盖场景: ${route.scenes.map(s => s.sceneName).join('、')}\n`;
      }
      output += '\n';
    }
  }

  // 活动推荐
  if (activities && activities.success && activities.activities.length > 0) {
    output += `🎉 **同城近期活动**\n\n`;

    const top3 = activities.activities.slice(0, 3);
    for (const activity of top3) {
      output += `• ${activity.name}\n`;
      output += `  📍 ${activity.address}\n`;
      output += `  📅 ${activity.date}\n`;
      output += `  💰 ${activity.price}\n\n`;
    }
  }

  // 个人地图模块
  if (mapResult) {
    if (mapResult.success) {
      // 单个地图
      if (mapResult.url || mapResult.qrCode) {
        output += `📱 **高德个人地图**\n`;
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
        output += `💡 扫描二维码或点击链接可在高德App中查看全部打卡点位\n`;
        output += `• 支持一键导航到任意点位\n`;
        output += `• 可分享给好友或保存到相册\n\n`;
      }
    } else if (mapResult.maps) {
      // 批量地图
      output += `📱 **高德个人地图（分批创建）**\n`;
      output += `📍 总点位数量: ${mapResult.totalPoints}个\n`;
      output += `📦 批次数量: ${mapResult.batchCount}批\n\n`;

      for (const map of mapResult.maps) {
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
      output += `• 所有地图可分别导航和分享\n\n`;
    } else if (!mapResult.success) {
      output += `📱 **高德个人地图**\n`;
      output += `❌ ${mapResult.message}\n\n`;
    }
  }

  // 底部提示
  output += `---\n`;
  output += `💡 温馨提示:\n`;
  output += `• 建议提前查看各点位营业时间\n`;
  output += `• 热门景点建议错峰出行\n`;
  output += `• 注意查看天气预报，合理安排行程\n`;

  return {
    type: 'text',
    content: output,
    data: {
      city,
      district,
      totalPois,
      routeCount: routes ? routes.length : 0,
      activityCount: activities?.activities?.length || 0,
      mapResult: mapResult
    }
  };
}

// 格式化单场景地图输出
function formatSceneMap(data) {
  const { scene, sceneConfig, city, district, pois, routes, activities, mapResult } = data;

  let output = '';

  // 头部信息
  output += `${sceneConfig.icon} **${city}${sceneConfig.name}**\n`;
  output += `📍 区域: ${district || '全市'}\n`;
  output += `📝 ${sceneConfig.description}\n\n`;

  // 统计模块
  output += `📊 **统计信息**\n`;
  output += `• 点位总数: ${pois.length}个\n`;
  output += `• 评分范围: ${getRatingRange(pois)}\n`;
  output += `• 区域分布: ${getDistrictDistribution(pois)}\n\n`;

  // TOP点位推荐
  output += `📍 **TOP${Math.min(pois.length, 10)}优质点位**\n\n`;

  const topPois = pois.slice(0, 10);
  for (let i = 0; i < topPois.length; i++) {
    const poi = topPois[i];
    output += `${i + 1}. **${poi.name}**\n`;
    if (poi.rating) output += `   ⭐ 评分: ${poi.rating}\n`;
    if (poi.address) output += `   📍 地址: ${poi.address}\n`;
    if (poi.biz_ext?.cost) output += `   💰 人均: ${poi.biz_ext.cost}\n`;
    if (poi.tel) output += `   📞 电话: ${poi.tel}\n`;
    output += '\n';
  }

  // 时间推荐
  if (sceneConfig.timeRecommendation) {
    output += `⏰ **最佳游玩时间**\n`;
    for (const [key, value] of Object.entries(sceneConfig.timeRecommendation)) {
      output += `• ${value}\n`;
    }
    output += '\n';
  }

  // 路线规划
  if (routes && routes.length > 0) {
    output += `🚗 **推荐路线**\n\n`;

    for (const route of routes) {
      output += `📍 **${route.name}**\n`;
      output += `• 总距离: ${route.totalDistance}\n`;
      output += `• 预计用时: ${route.totalDuration}\n`;
      output += `• 游览点位: ${route.pois.length}个\n`;

      if (route.pois.length > 0) {
        output += `• 路线: ${route.pois.slice(0, 3).map(p => p.name).join(' → ')}`;
        if (route.pois.length > 3) output += ` → ...等${route.pois.length}个点位`;
        output += '\n';
      }
      output += '\n';
    }
  }

  // 活动推荐
  if (activities && activities.success && activities.activities.length > 0) {
    output += `🎉 **相关活动推荐**\n\n`;

    const top2 = activities.activities.slice(0, 2);
    for (const activity of top2) {
      output += `• ${activity.name}\n`;
      output += `  📍 ${activity.address}\n`;
      output += `  📅 ${activity.date}\n\n`;
    }
  }

  // 个人地图模块
  if (mapResult) {
    if (mapResult.success) {
      // 单个地图
      if (mapResult.url || mapResult.qrCode) {
        output += `📱 **高德个人地图**\n`;
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
        output += `💡 扫描二维码或点击链接可在高德App中查看全部打卡点位\n`;
        output += `• 支持一键导航到任意点位\n`;
        output += `• 可分享给好友或保存到相册\n\n`;
      }
    } else if (mapResult.maps) {
      // 批量地图
      output += `📱 **高德个人地图（分批创建）**\n`;
      output += `📍 总点位数量: ${mapResult.totalPoints}个\n`;
      output += `📦 批次数量: ${mapResult.batchCount}批\n\n`;

      for (const map of mapResult.maps) {
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
      output += `• 所有地图可分别导航和分享\n\n`;
    } else if (!mapResult.success) {
      output += `📱 **高德个人地图**\n`;
      output += `❌ ${mapResult.message}\n\n`;
    }
  }

  // 温馨提示
  if (sceneConfig.tips && sceneConfig.tips.length > 0) {
    output += `💡 **温馨提示**\n`;
    for (const tip of sceneConfig.tips) {
      output += `• ${tip}\n`;
    }
    output += '\n';
  }

  return {
    type: 'text',
    content: output,
    data: {
      scene,
      sceneName: sceneConfig.name,
      city,
      district,
      poiCount: pois.length,
      routeCount: routes ? routes.length : 0,
      mapResult: mapResult
    }
  };
}

// 格式化旅行地图输出
function formatTravelMap(data) {
  const { city, days, mode, data: sceneData, routes, weather, mapResult } = data;

  let output = '';

  // 头部信息
  output += `✈️ **${city}${days}天${mode}旅行规划**\n\n`;

  // 天气信息
  if (weather && weather.casts) {
    output += `🌤️ **天气预报**\n`;
    const forecast = weather.casts.slice(0, days);
    for (const cast of forecast) {
      output += `• ${cast.date} (${cast.week}): ${cast.dayweather}/${cast.nightweather} ${cast.daytemp}°C/${cast.nighttemp}°C\n`;
    }
    output += '\n';
  }

  // 统计模块
  const totalPois = Object.values(sceneData).reduce((sum, pois) => sum + pois.length, 0);
  output += `📊 **行程统计**\n`;
  output += `• 总天数: ${days}天\n`;
  output += `• 交通方式: ${getModeName(mode)}\n`;
  output += `• 点位总数: ${totalPois}个\n`;
  output += `• 涵盖场景: ${Object.keys(sceneData).length}个\n\n`;

  // 每日行程
  if (routes && routes.length > 0) {
    output += `📅 **每日行程安排**\n\n`;

    for (const dayRoute of routes) {
      output += `📆 **第${dayRoute.day}天** (${dayRoute.date})\n`;
      output += `📍 总距离: ${dayRoute.totalDistance}\n`;
      output += `⏰ 预计用时: ${dayRoute.totalDuration}\n\n`;

      if (dayRoute.timeSlots) {
        for (const slot of dayRoute.timeSlots) {
          output += `**${slot.time}**\n`;
          for (const poi of slot.pois) {
            output += `  • ${poi.name}`;
            if (poi.address) output += ` (${poi.address})`;
            output += '\n';
          }
          output += '\n';
        }
      }

      if (dayRoute.tips && dayRoute.tips.length > 0) {
        output += `💡 提示: ${dayRoute.tips[0]}\n`;
      }

      output += '\n';
    }
  }

  // 个人地图模块
  if (mapResult) {
    if (mapResult.success) {
      // 单个地图
      if (mapResult.url || mapResult.qrCode) {
        output += `📱 **高德个人地图**\n`;
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
        output += `💡 扫描二维码或点击链接可在高德App中查看全部行程点位\n`;
        output += `• 支持一键导航到任意点位\n`;
        output += `• 可分享给好友或保存到相册\n\n`;
      }
    } else if (mapResult.maps) {
      // 批量地图
      output += `📱 **高德个人地图（分批创建）**\n`;
      output += `📍 总点位数量: ${mapResult.totalPoints}个\n`;
      output += `📦 批次数量: ${mapResult.batchCount}批\n\n`;

      for (const map of mapResult.maps) {
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
      output += `• 所有地图可分别导航和分享\n\n`;
    } else if (!mapResult.success) {
      output += `📱 **高德个人地图**\n`;
      output += `❌ ${mapResult.message}\n\n`;
    }
  }

  // 旅行提示
  output += `💡 **旅行温馨提示**\n`;
  output += `• 提前预订住宿和热门景点门票\n`;
  output += `• 保存好电子票务和酒店确认信息\n`;
  output += `• 注意查看目的地天气，准备合适衣物\n`;
  output += `• 保持手机电量充足，备好充电宝\n`;

  return {
    type: 'text',
    content: output,
    data: {
      city,
      days,
      mode,
      totalPois,
      routeCount: routes ? routes.length : 0,
      mapResult: mapResult
    }
  };
}

// 格式化用户画像输出
function formatProfile(profileData) {
  const { profile, stats } = profileData;

  let output = '';

  output += `👤 **我的用户画像**\n\n`;

  // 基础信息
  output += `📋 **基础信息**\n`;
  output += `• 常驻城市: ${profile.basic.homeCity || '未设置'}\n`;
  output += `• 加入时间: ${formatDate(profile.basic.joinDate)}\n`;
  output += `• 用户标签: ${profile.tags.length > 0 ? profile.tags.join('、') : '暂无'}\n\n`;

  // 偏好统计
  output += `📊 **偏好分析**\n`;

  // 场景偏好
  if (stats && stats.scenePreferences) {
    const topScenes = Object.entries(stats.scenePreferences)
      .sort(([,a], [,b]) => b.percentage - a.percentage)
      .slice(0, 3);

    if (topScenes.length > 0) {
      output += `• 喜爱场景: ${topScenes.map(([scene, data]) => {
        const sceneConfig = scenes[scene];
        return `${sceneConfig ? sceneConfig.icon : ''}${sceneConfig ? sceneConfig.name : scene}(${data.percentage}%)`;
      }).join('、')}\n`;
    }
  }

  // 时间偏好
  if (stats && stats.timePreferences) {
    const topTime = Object.entries(stats.timePreferences)
      .sort(([,a], [,b]) => b.percentage - a.percentage)[0];

    if (topTime) {
      const timeNames = {
        morning: '早晨',
        afternoon: '下午',
        evening: '傍晚',
        night: '夜晚'
      };
      output += `• 活跃时段: ${timeNames[topTime[0]] || topTime[0]}(${topTime[1].percentage}%)\n`;
    }
  }

  // 常去城市
  if (stats && stats.topCities && stats.topCities.length > 0) {
    output += `• 常去城市: ${stats.topCities.join('、')}\n`;
  }

  output += '\n';

  // 使用统计
  if (stats && stats.statistics) {
    output += `📈 **使用统计**\n`;
    output += `• 总交互次数: ${stats.statistics.totalInteractions}次\n`;
    output += `• 创建地图数: ${stats.statistics.totalMaps}张\n`;
    output += `• 规划路线数: ${stats.statistics.totalRoutes}条\n`;
    output += `• 游历城市数: ${stats.statistics.totalCities}个\n`;
    output += `• 收藏点位数: ${stats.statistics.favoriteCount}个\n\n`;
  }

  // 操作提示
  output += `💡 **操作提示**\n`;
  output += `• 说"设置常驻城市为XX"可更新常驻城市\n`;
  output += `• 说"查看历史游历"可查看去过的地方\n`;
  output += `• 说"重置画像"可重新开始\n`;

  return {
    type: 'text',
    content: output,
    data: profile
  };
}

// 格式化历史记录输出
function formatHistory(memoryData) {
  const { memory, stats } = memoryData;

  let output = '';

  output += `🗺️ **我的游历足迹**\n\n`;

  // 统计概览
  if (stats) {
    output += `📊 **游历统计**\n`;
    output += `• 游历城市: ${stats.cityCount}个\n`;
    output += `• 创建地图: ${stats.mapCount}张\n`;
    output += `• 规划路线: ${stats.routeCount}条\n`;
    output += `• 收藏点位: ${stats.favoriteCount}个\n\n`;
  }

  // 游历城市列表
  if (memory.long_term.visitedCities.length > 0) {
    output += `🌆 **游历城市**\n`;
    for (const city of memory.long_term.visitedCities) {
      output += `• ${city}\n`;
    }
    output += '\n';
  }

  // 最近创建的地图
  if (memory.long_term.createdMaps.length > 0) {
    output += `🗺️ **最近创建的地图**\n`;
    const recentMaps = memory.long_term.createdMaps.slice(0, 5);
    for (const map of recentMaps) {
      const sceneConfig = scenes[map.scene];
      output += `• ${map.city} ${sceneConfig ? sceneConfig.name : '全能地图'}`;
      if (map.district) output += ` (${map.district})`;
      output += ` - ${formatDate(map.timestamp)}\n`;
    }
    output += '\n';
  }

  // 收藏点位
  if (memory.long_term.favoritePois.length > 0) {
    output += `❤️ **收藏点位**\n`;
    const favorites = memory.long_term.favoritePois.slice(0, 5);
    for (const fav of favorites) {
      output += `• ${fav.name}`;
      if (fav.city) output += ` (${fav.city})`;
      output += '\n';
    }
    if (memory.long_term.favoritePois.length > 5) {
      output += `• ...等共${memory.long_term.favoritePois.length}个点位\n`;
    }
    output += '\n';
  }

  // 最近交互
  if (memory.temporary.recentInteractions.length > 0) {
    output += `📝 **最近活动**\n`;
    const recentInteractions = memory.temporary.recentInteractions.slice(0, 3);
    for (const interaction of recentInteractions) {
      const intent = interaction.intent;
      let description = '';
      if (intent.type === 'full_map') {
        description = `生成${intent.city}全能地图`;
      } else if (intent.type === 'scene_map') {
        const sceneConfig = scenes[intent.scene];
        description = `生成${intent.city}${sceneConfig ? sceneConfig.name : ''}`;
      } else if (intent.type === 'travel') {
        description = `规划${intent.city}旅行`;
      } else {
        description = intent.type;
      }
      output += `• ${description} - ${formatDate(interaction.timestamp)}\n`;
    }
    output += '\n';
  }

  // 操作提示
  output += `💡 **操作提示**\n`;
  output += `• 说"搜索XX"可搜索历史记忆\n`;
  output += `• 说"查看XX地图"可重新生成地图\n`;

  return {
    type: 'text',
    content: output,
    data: memory
  };
}

// 格式化活动列表
function formatActivityList(activities) {
  let output = '';

  output += `🎉 **同城近期活动**\n`;
  output += `📍 城市: ${activities.city}\n`;
  output += `📊 活动数量: ${activities.count}个\n\n`;

  if (activities.activities.length === 0) {
    output += `暂无近期活动推荐\n`;
    return {
      type: 'text',
      content: output,
      data: activities
    };
  }

  for (let i = 0; i < activities.activities.length; i++) {
    const activity = activities.activities[i];
    output += `${i + 1}. **${activity.name}**\n`;
    output += `   📍 ${activity.address}\n`;
    output += `   📅 ${activity.date}\n`;
    output += `   ⏰ ${activity.time}\n`;
    output += `   💰 ${activity.price}\n`;
    if (activity.rating) output += `   ⭐ 评分: ${activity.rating}\n`;
    output += '\n';
  }

  return {
    type: 'text',
    content: output,
    data: activities
  };
}

// 格式化人文讲解
function formatCultureInfo(cultureData) {
  let output = '';

  output += `📚 **${cultureData.name}人文讲解**\n\n`;

  if (cultureData.history) {
    output += `🏛️ **历史沿革**\n${cultureData.history}\n\n`;
  }

  if (cultureData.culture) {
    output += `🎭 **文化特色**\n${cultureData.culture}\n\n`;
  }

  if (cultureData.stories) {
    output += `📖 **历史典故**\n`;
    for (const story of cultureData.stories) {
      output += `• ${story}\n`;
    }
    output += '\n';
  }

  if (cultureData.tips) {
    output += `💡 **游玩贴士**\n`;
    for (const tip of cultureData.tips) {
      output += `• ${tip}\n`;
    }
    output += '\n';
  }

  if (cultureData.bestPhotoSpots) {
    output += `📸 **最佳拍照点**\n`;
    for (const spot of cultureData.bestPhotoSpots) {
      output += `• ${spot}\n`;
    }
    output += '\n';
  }

  return {
    type: 'text',
    content: output,
    data: cultureData
  };
}

// 格式化错误信息
function formatError(message) {
  return {
    type: 'error',
    content: `❌ ${message}`,
    data: null
  };
}

// 格式化成功信息
function formatSuccess(message, data = null) {
  return {
    type: 'success',
    content: `✅ ${message}`,
    data: data
  };
}

// 辅助函数：获取评分范围
function getRatingRange(pois) {
  const ratings = pois
    .filter(p => p.rating)
    .map(p => parseFloat(p.rating));

  if (ratings.length === 0) return '暂无评分';

  const min = Math.min(...ratings).toFixed(1);
  const max = Math.max(...ratings).toFixed(1);

  return `${min} - ${max}`;
}

// 辅助函数：获取区域分布
function getDistrictDistribution(pois) {
  const districts = {};
  for (const poi of pois) {
    const district = poi.district || '其他';
    districts[district] = (districts[district] || 0) + 1;
  }

  return Object.entries(districts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 3)
    .map(([district, count]) => `${district}(${count})`)
    .join('、');
}

// 辅助函数：获取交通方式名称
function getModeName(mode) {
  const modeNames = {
    driving: '自驾',
    walking: '步行',
    transit: '公共交通'
  };
  return modeNames[mode] || mode;
}

// 辅助函数：格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

module.exports = {
  formatFullMap,
  formatSceneMap,
  formatTravelMap,
  formatProfile,
  formatHistory,
  formatActivityList,
  formatCultureInfo,
  formatError,
  formatSuccess
};
