/**
 * 人文知识库模块
 * 实现景点/街区/地标的历史、民俗、典故讲解功能
 */

const amap = require('../utils/amap');

// 人文知识库数据
const CULTURE_DATABASE = {
  // 通用景点知识
  general: {
    park: {
      history: '公园作为城市公共空间，承载着市民休闲娱乐的功能。中国现代公园建设始于清末民初，经历了从皇家园林到公共空间的转变。',
      culture: '公园文化体现了城市的生活节奏和市民的精神追求，是城市文明的重要标志。',
      tips: ['建议清晨或傍晚前往', '注意保护园内植被', '遵守公园管理规定'],
      bestPhotoSpots: ['入口标志性建筑', '湖边倒影', '花丛小径']
    },
    temple: {
      history: '寺庙道观是中国传统宗教文化的重要载体，见证了千年的信仰传承和建筑艺术发展。',
      culture: '宗教场所承载着丰富的民俗文化，包括祭祀、庙会、节庆等传统活动。',
      tips: ['尊重宗教信仰和习俗', '穿着得体', '保持安静'],
      bestPhotoSpots: ['山门殿宇', '古树名木', '石碑雕刻']
    },
    street: {
      history: '老街巷是城市历史的活化石，记录着城市的发展变迁和市井生活的演变。',
      culture: '街巷文化反映了当地的商业传统、生活方式和邻里关系，是城市记忆的重要组成部分。',
      tips: ['慢慢漫步感受氛围', '与当地居民交流', '尝试街边小吃'],
      bestPhotoSpots: ['老字号店铺', '传统建筑', '市井生活场景']
    },
    museum: {
      history: '博物馆是保护和传承人类文明的重要机构，通过文物展示历史文化的精髓。',
      culture: '博物馆文化体现了对历史的尊重和对知识的追求，是提升文化素养的重要场所。',
      tips: ['提前预约', '跟随讲解员参观', '不要触摸展品'],
      bestPhotoSpots: ['博物馆建筑外观', '标志性展品', '特色展览']
    }
  },

  // 城市特色知识
  cities: {
    北京: {
      history: '北京是中国四大古都之一，有着三千多年的建城史和八百多年的建都史。从金中都、元大都到明清北京城，见证了中华文明的辉煌历程。',
      culture: '北京文化融合了皇家文化、士人文化和市井文化，形成了独特的京味儿文化。京剧、相声、胡同文化是北京文化的典型代表。',
      stories: [
        '故宫的建造历时14年，动用工匠23万人，是世界上现存规模最大、保存最完整的木质结构古建筑群',
        '胡同源自蒙古语，意为"水井"，是北京特有的城市肌理',
        '天坛是明清两代皇帝祭天祈谷的场所，其建筑设计体现了古人"天圆地方"的宇宙观'
      ],
      tips: ['春秋两季是最佳旅游季节', '提前预约热门景点', '体验老北京胡同文化'],
      bestPhotoSpots: ['故宫角楼', '景山万春亭', '颐和园十七孔桥']
    },
    上海: {
      history: '上海从一个小渔村发展成为国际化大都市，经历了开埠、租界、解放、改革开放等重要历史阶段，是中国近代史的缩影。',
      culture: '上海文化融合了江南文化、西方文化和现代都市文化，形成了独特的海派文化。石库门、旗袍、老洋房是海派文化的典型符号。',
      stories: [
        '外滩的万国建筑博览群见证了上海开埠后的百年沧桑',
        '石库门建筑是中西合璧的典范，承载了几代上海人的生活记忆',
        '南京路步行街是中国最早的商业街之一，被誉为"中华商业第一街"'
      ],
      tips: ['夜景是上海的精华', '体验弄堂里的市井生活', '品尝本帮菜和海派点心'],
      bestPhotoSpots: ['外滩夜景', '陆家嘴天际线', '武康路梧桐树']
    },
    杭州: {
      history: '杭州是南宋都城，有着八千年的文明史和五千年的建城史。西湖文化景观被列入世界文化遗产名录。',
      culture: '杭州文化以西湖文化为核心，融合了茶文化、丝绸文化、佛教文化等，形成了精致典雅的江南文化气质。',
      stories: [
        '西湖十景源于南宋画院的山水画题名，每个景点都有动人的传说',
        '灵隐寺始建于东晋，是中国佛教禅宗十大古刹之一',
        '龙井茶因产于西湖龙井村而得名，有着一千二百多年的历史'
      ],
      tips: ['春天赏花，秋天赏桂', '骑行环湖是最佳体验方式', '品尝龙井茶和杭帮菜'],
      bestPhotoSpots: ['断桥残雪', '雷峰夕照', '三潭印月']
    },
    成都: {
      history: '成都有四千五百年的文明史和两千多年的建城史，是古蜀文明的发祥地。历史上曾是多个政权的都城。',
      culture: '成都文化以休闲文化为核心，融合了蜀文化、茶文化、美食文化等，形成了独特的天府文化。成都人"巴适"的生活态度闻名全国。',
      stories: [
        '武侯祠是中国唯一的君臣合祀祠庙，纪念诸葛亮和刘备',
        '杜甫草堂是唐代诗人杜甫流寓成都时的故居，留下了240余首诗篇',
        '宽窄巷子是清朝时期的满城，现在是成都最具特色的文化街区'
      ],
      tips: ['体验成都的茶馆文化', '品尝正宗川菜和火锅', '看一场川剧变脸'],
      bestPhotoSpots: ['锦里夜景', '宽窄巷子', '大熊猫基地']
    },
    西安: {
      history: '西安古称长安，是十三朝古都，有着三千一百多年的建城史和一千多年的建都史。丝绸之路从这里起点。',
      culture: '西安文化以汉唐文化为核心，融合了关中文化、丝路文化等，形成了雄浑大气的古都气质。',
      stories: [
        '兵马俑是秦始皇陵的陪葬坑，被誉为"世界第八大奇迹"',
        '大雁塔是玄奘为保存从印度带回的经卷而修建的佛塔',
        '钟鼓楼是西安的标志性建筑，晨钟暮鼓的习俗延续了千年'
      ],
      tips: ['春秋两季是最佳旅游季节', '品尝羊肉泡馍和肉夹馍', '夜游大唐不夜城'],
      bestPhotoSpots: ['兵马俑', '古城墙', '大雁塔夜景']
    }
  },

  // 景点类型知识
  poiTypes: {
    '历史文化街区': {
      description: '历史文化街区是保存文物特别丰富、历史建筑集中成片、能够较完整和真实地体现传统格局和历史风貌的区域',
      significance: '承载着城市的历史记忆和文化基因，是城市文脉的重要组成部分'
    },
    '文博场馆': {
      description: '包括博物馆、美术馆、纪念馆等，是收藏、保护、研究、展示人类文化遗产的场所',
      significance: '传承历史文化，提升公众文化素养，促进文化交流'
    },
    '宗教场所': {
      description: '包括寺庙、道观、教堂等，是宗教信仰活动的场所',
      significance: '承载着丰富的宗教文化和建筑艺术，是人类精神文明的重要载体'
    },
    '名人故居': {
      description: '历史名人曾经居住生活的地方，是了解名人生活和思想的重要窗口',
      significance: '传承名人精神，弘扬优秀文化传统'
    }
  }
};

// 获取景点人文知识
async function getCultureInfo(place, city) {
  try {
    // 先从本地知识库查找
    let cultureInfo = findInLocalDatabase(place, city);

    // 如果本地没有，尝试从API获取更多信息
    if (!cultureInfo) {
      cultureInfo = await fetchCultureFromAPI(place, city);
    }

    // 如果还是没有，生成通用讲解
    if (!cultureInfo) {
      cultureInfo = generateGenericCulture(place, city);
    }

    return {
      success: true,
      name: place,
      city: city,
      ...cultureInfo
    };
  } catch (error) {
    console.error('获取人文知识失败:', error);
    return {
      success: false,
      name: place,
      city: city,
      error: error.message
    };
  }
}

// 从本地知识库查找
function findInLocalDatabase(place, city) {
  // 查找城市特色知识
  if (CULTURE_DATABASE.cities[city]) {
    const cityData = CULTURE_DATABASE.cities[city];

    // 检查是否是该城市的知名景点
    if (cityData.stories) {
      const relatedStory = cityData.stories.find(story =>
        story.includes(place)
      );

      if (relatedStory) {
        return {
          history: cityData.history,
          culture: cityData.culture,
          stories: [relatedStory],
          tips: cityData.tips,
          bestPhotoSpots: cityData.bestPhotoSpots
        };
      }
    }

    // 返回城市通用知识
    return {
      history: cityData.history,
      culture: cityData.culture,
      stories: cityData.stories?.slice(0, 2) || [],
      tips: cityData.tips,
      bestPhotoSpots: cityData.bestPhotoSpots
    };
  }

  // 查找景点类型知识
  for (const [type, typeData] of Object.entries(CULTURE_DATABASE.poiTypes)) {
    if (place.includes(type)) {
      return {
        history: typeData.description,
        culture: typeData.significance,
        stories: [],
        tips: ['建议提前了解开放时间', '可以请导游讲解', '注意保护文物古迹'],
        bestPhotoSpots: ['建筑特色细节', '标志性景观', '文化元素']
      };
    }
  }

  // 查找通用景点知识
  if (place.includes('公园') || place.includes('花园')) {
    return CULTURE_DATABASE.general.park;
  } else if (place.includes('寺') || place.includes('庙') || place.includes('观')) {
    return CULTURE_DATABASE.general.temple;
  } else if (place.includes('街') || place.includes('巷') || place.includes('胡同')) {
    return CULTURE_DATABASE.general.street;
  } else if (place.includes('博物馆') || place.includes('纪念馆')) {
    return CULTURE_DATABASE.general.museum;
  }

  return null;
}

// 从API获取文化信息
async function fetchCultureFromAPI(place, city) {
  try {
    // 搜索景点信息
    const result = await amap.searchPoisByKeyword(city, place, '', 1, 5);

    if (result.pois && result.pois.length > 0) {
      const poi = result.pois[0];

      // 基于POI信息生成文化讲解
      return {
        history: `${place}是${city}的知名景点，位于${poi.address || '市中心区域'}。`,
        culture: `这里承载着当地的文化特色和历史记忆，是了解${city}文化的重要窗口。`,
        stories: [
          `${place}以其独特的魅力吸引着众多游客前来参观游览`,
          `这里是感受${city}本地文化的绝佳去处`
        ],
        tips: [
          '建议提前查看开放时间',
          '可以请导游讲解了解更多历史故事',
          '注意保护环境和文物古迹'
        ],
        bestPhotoSpots: [
          '入口标志性景观',
          '特色建筑细节',
          '文化元素展示区'
        ]
      };
    }

    return null;
  } catch (error) {
    console.error('从API获取文化信息失败:', error);
    return null;
  }
}

// 生成通用文化讲解
function generateGenericCulture(place, city) {
  return {
    history: `${place}是${city}的一处特色景点，承载着当地的历史文化和人文记忆。`,
    culture: `这里展现了${city}独特的地方特色和文化底蕴，是体验当地风情的好去处。`,
    stories: [
      `${place}有着悠久的历史和丰富的文化内涵`,
      `这里见证了${city}的发展变迁，是城市记忆的重要组成部分`
    ],
    tips: [
      '建议提前了解景点的开放时间和门票信息',
      '可以请导游讲解，深入了解历史故事',
      '注意保护环境，文明游览'
    ],
    bestPhotoSpots: [
      '标志性景观',
      '特色建筑',
      '文化元素'
    ]
  };
}

// 获取城市概览
function getCityOverview(city) {
  if (CULTURE_DATABASE.cities[city]) {
    const cityData = CULTURE_DATABASE.cities[city];
    return {
      success: true,
      city: city,
      history: cityData.history,
      culture: cityData.culture,
      topStories: cityData.stories?.slice(0, 3) || [],
      tips: cityData.tips,
      bestPhotoSpots: cityData.bestPhotoSpots
    };
  }

  return {
    success: false,
    city: city,
    message: `暂未收录${city}的详细文化信息`
  };
}

// 获取景点类型介绍
function getPoiTypeIntro(poiType) {
  for (const [type, typeData] of Object.entries(CULTURE_DATABASE.poiTypes)) {
    if (poiType.includes(type)) {
      return {
        success: true,
        type: type,
        description: typeData.description,
        significance: typeData.significance
      };
    }
  }

  return {
    success: false,
    type: poiType,
    message: '暂无该类型景点的详细介绍'
  };
}

// 搜索文化知识
function searchCulture(keyword) {
  const results = {
    cities: [],
    poiTypes: [],
    general: []
  };

  // 搜索城市知识
  for (const [city, cityData] of Object.entries(CULTURE_DATABASE.cities)) {
    if (city.includes(keyword) || keyword.includes(city)) {
      results.cities.push({
        city: city,
        overview: cityData.history
      });
    }

    // 搜索城市内的故事
    if (cityData.stories) {
      const relatedStories = cityData.stories.filter(story =>
        story.includes(keyword)
      );
      if (relatedStories.length > 0) {
        results.cities.push({
          city: city,
          stories: relatedStories
        });
      }
    }
  }

  // 搜索景点类型
  for (const [type, typeData] of Object.entries(CULTURE_DATABASE.poiTypes)) {
    if (type.includes(keyword) || keyword.includes(type)) {
      results.poiTypes.push({
        type: type,
        description: typeData.description
      });
    }
  }

  // 搜索通用知识
  for (const [category, categoryData] of Object.entries(CULTURE_DATABASE.general)) {
    if (category.includes(keyword) || keyword.includes(category)) {
      results.general.push({
        category: category,
        data: categoryData
      });
    }
  }

  return results;
}

// 获取文化知识列表
function getCultureCategories() {
  return {
    cities: Object.keys(CULTURE_DATABASE.cities),
    poiTypes: Object.keys(CULTURE_DATABASE.poiTypes),
    general: Object.keys(CULTURE_DATABASE.general)
  };
}

// 添加自定义文化知识
async function addCustomCulture(place, city, cultureData) {
  try {
    // 这里可以扩展为将自定义知识保存到文件
    // 目前只是返回成功
    return {
      success: true,
      message: `已添加${place}的文化知识`,
      data: {
        place,
        city,
        ...cultureData,
        addedAt: new Date().toISOString()
      }
    };
  } catch (error) {
    console.error('添加文化知识失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// 格式化文化讲解输出
function formatCultureOutput(cultureData) {
  let output = '';

  output += `📚 **${cultureData.name}人文讲解**\n`;
  output += `📍 城市: ${cultureData.city}\n\n`;

  if (cultureData.history) {
    output += `🏛️ **历史沿革**\n${cultureData.history}\n\n`;
  }

  if (cultureData.culture) {
    output += `🎭 **文化特色**\n${cultureData.culture}\n\n`;
  }

  if (cultureData.stories && cultureData.stories.length > 0) {
    output += `📖 **历史典故**\n`;
    for (const story of cultureData.stories) {
      output += `• ${story}\n`;
    }
    output += '\n';
  }

  if (cultureData.tips && cultureData.tips.length > 0) {
    output += `💡 **游玩贴士**\n`;
    for (const tip of cultureData.tips) {
      output += `• ${tip}\n`;
    }
    output += '\n';
  }

  if (cultureData.bestPhotoSpots && cultureData.bestPhotoSpots.length > 0) {
    output += `📸 **最佳拍照点**\n`;
    for (const spot of cultureData.bestPhotoSpots) {
      output += `• ${spot}\n`;
    }
    output += '\n';
  }

  return output;
}

module.exports = {
  getCultureInfo,
  getCityOverview,
  getPoiTypeIntro,
  searchCulture,
  getCultureCategories,
  addCustomCulture,
  formatCultureOutput,
  CULTURE_DATABASE
};
