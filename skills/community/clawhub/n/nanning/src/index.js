const data = {
  spots: [
    { name: "青秀山", type: "自然风光", level: "5A", description: "南宁市最高峰，国家5A级景区，有千年苏铁园、兰花园等特色园区", location: "南宁市青秀区凤岭南路", ticket: "门票约60元", rating: 4.7 },
    { name: "南湖公园", type: "城市公园", level: "4A", description: "市区内综合性公园，有李明瑞、韦拔群烈士纪念碑", location: "南宁市青秀区双拥路", ticket: "免费", rating: 4.5 },
    { name: "扬美古镇", type: "历史古迹", level: "4A", description: "始建于宋代，是南宁市保存最完整的古镇", location: "南宁市江南区扬美镇", ticket: "免费", rating: 4.4 },
    { name: "广西民族博物馆", type: "文化场馆", level: "免费", description: "展示广西12个世居民族的传统文化", location: "南宁市青秀区青环路", ticket: "免费", rating: 4.6 },
    { name: "南宁动物园", type: "主题公园", level: "4A", description: "广西唯一一家以观赏野生动物为主的公园", location: "南宁市西乡塘区大学东路", ticket: "门票约50元", rating: 4.3 },
    { name: "会展中心", type: "地标建筑", level: "地标", description: "中国-东盟博览会永久举办地，南宁地标性建筑", location: "南宁市青秀区民族大道", ticket: "展览另收费", rating: 4.5 },
    { name: "大明山", type: "自然风光", level: "4A", description: "桂中最高峰，冬季可观赏雾凇", location: "南宁市武鸣区两江镇", ticket: "门票约80元", rating: 4.6 },
    { name: "金花茶公园", type: "城市公园", level: "免费", description: "以观赏金花茶为主题的公园", location: "南宁市青秀区葛村路", ticket: "免费", rating: 4.2 }
  ],
  food: [
    { name: "老友粉", type: "粉面", description: "南宁最具代表性的特色小吃，酸辣可口", price: "10-20元", mustTry: true },
    { name: "柠檬鸭", type: "菜肴", description: "武鸣地区特色菜，酸柠檬与鸭肉完美结合", price: "40-60元", mustTry: true },
    { name: "卷筒粉", type: "粉面", description: "越南风味，米粉裹各种馅料，蘸酱食用", price: "5-15元", mustTry: true },
    { name: "酸嘢", type: "小吃", description: "酸味腌渍蔬果，生津开胃", price: "3-10元", mustTry: true },
    { name: "八仙粉", type: "粉面", description: "相传八仙所创，汤鲜味美", price: "10-20元", mustTry: false },
    { name: "横县鱼生", type: "菜肴", description: "横县特产，刀工精细，蘸料丰富", price: "30-50元", mustTry: true },
    { name: "高峰柠檬鸭", type: "菜肴", description: "武鸣高峰林场特色，土鸭配柠檬", price: "50-80元", mustTry: false },
    { name: "烤生蚝", type: "小吃", description: "南宁夜市必备，蒜香四溢", price: "3-8元/个", mustTry: true },
    { name: "复记老友粉", type: "粉面", description: "老友粉老字号，味道正宗", price: "15-25元", mustTry: true },
    { name: "六叔牛杂", type: "小吃", description: "南宁传统牛杂小店", price: "15-30元", mustTry: true }
  ],
  transport: {
    airport: {
      name: "南宁吴圩国际机场",
      code: "NNG",
      level: "4E",
      description: "广西最大的民用机场，年旅客吞吐量超1500万人次",
      location: "南宁市江南区吴圩镇",
      metro: "规划中的机场线连接市区",
      taxi: "距市中心约30公里，车程约40分钟",
      bus: "机场大巴多个线路覆盖市区"
    },
    railway: [
      { name: "南宁东站", type: "高铁站", level: "特等站", description: "广西最大高铁站，南广、贵广、渝贵等多条高铁交汇", location: "南宁市青秀区凤岭北路" },
      { name: "南宁站", type: "普高共用", level: "一等站", description: "历史悠久，兼顾普速和高铁", location: "南宁市西乡塘区中华路" },
      { name: "南宁西站", type: "高铁站", level: "中间站", description: "南昆客专站点", location: "南宁市西乡塘区金陵镇" }
    ],
    metro: {
      lines: 5,
      description: "南宁轨道交通已开通1-5号线，覆盖主要城区",
      popular: ["1号线", "2号线", "3号线"],
      note: "支持微信、支付宝扫码乘车"
    },
    bus: {
      description: "南宁公交线路密集，覆盖全市",
      types: ["普通公交", "BRT快速公交", "社区巴士"]
    }
  },
  culture: {
    ethnicGroups: "壮族、汉族、瑶族、苗族等12个民族聚居",
    language: "普通话、壮语、白话为主",
    festivals: [
      { name: "中国-东盟博览会", time: "每年9月", description: "国家级国际性盛会，促进中国与东盟合作" },
      { name: "壮族三月三", time: "农历三月初三", description: "壮族传统节日，歌圩盛会很热闹" },
      { name: "南宁国际民歌艺术节", time: "每年10月", description: "国内外民歌艺术交流平台" }
    ],
    history: [
      { period: "晋朝", event: "设晋兴县，为南宁建制之始" },
      { period: "唐朝", event: "改称邕州，邕江名称由此而来" },
      { period: "元朝", event: "设南宁路，从此有了\"南宁\"之名" },
      { period: "1958年", event: "广西壮族自治区成立，南宁成为首府" }
    ]
  },
  shopping: [
    { name: "朝阳广场商圈", type: "传统商圈", description: "南宁最老牌商业区，地下商业街发达", highlight: "档次齐全，从平价到高端都有" },
    { name: "万象城", type: "高端商场", description: "南宁顶级购物中心，国际品牌云集", highlight: "美食、影院、超市一应俱全" },
    { name: "会展中心商圈", type: "新兴商圈", description: "依托会展中心发展起来的高端商务区", highlight: "航洋城、会展航洋城购物中心" },
    { name: "青秀万达广场", type: "综合商场", description: "大型城市综合体", highlight: "餐饮、娱乐、购物全面覆盖" },
    { name: "三街两巷", type: "历史文化街区", description: "南宁老街区的改造典范，历史文化与现代商业结合", highlight: "可以感受老南宁的风情" },
    { name: "中山路美食街", type: "美食街", description: "南宁夜生活的代表，汇集各种小吃", highlight: "深夜食堂，凌晨依然热闹" }
  ],
  living: {
    weather: {
      climate: "亚热带季风气候",
      features: "夏长冬短，阳光充足，降水充沛",
      temperature: "年均气温21-22℃",
      clothing: "冬季无需羽绒服，夏季注意防晒"
    },
    cost: {
      housing: "新房均价10000-15000元/平方米",
      rent: "一室一厅约1500-2500元/月",
      food: "日常餐饮约30-50元/天",
      traffic: "地铁/公交月票约100-200元"
    },
    healthcare: [
      "广西医科大学第一附属医院（三甲）",
      "广西壮族自治区人民医院（三甲）",
      "南宁市第一人民医院（三甲）"
    ],
    education: [
      "广西大学（211工程）",
      "广西民族大学",
      "南宁师范大学",
      "多所优质中小学"
    ]
  }
};

function formatSpots(spots) {
  if (!spots || spots.length === 0) return '未找到相关景点';
  return spots.map(s => 
    `【${s.name}】${s.type} ${s.level}\n` +
    `  ${s.description}\n` +
    `  📍${s.location} | 🎫${s.ticket} | ⭐${s.rating}`
  ).join('\n\n');
}

function formatFood(foods) {
  if (!foods || foods.length === 0) return '未找到相关美食';
  return foods.map(f =>
    `【${f.name}】${f.type} ${f.mustTry ? '🔥必吃' : ''}\n` +
    `  ${f.description}\n` +
    `  💰约${f.price}`
  ).join('\n\n');
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    command: 'info',
    query: '',
    detail: false
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    switch (arg) {
      case 'spots':
      case 'attractions':
      case '景点':
        options.command = 'spots';
        break;
      case 'food':
      case '美食':
        options.command = 'food';
        if (args[i + 1] === '--popular') {
          options.query = 'popular';
          i++;
        }
        break;
      case 'transport':
      case '交通':
        options.command = 'transport';
        break;
      case 'metro':
      case '地铁':
        options.command = 'metro';
        break;
      case 'airport':
      case '机场':
        options.command = 'airport';
        break;
      case 'culture':
      case '文化':
        options.command = 'culture';
        break;
      case 'festivals':
      case '节庆':
        options.command = 'festivals';
        break;
      case 'history':
      case '历史':
        options.command = 'history';
        break;
      case 'shopping':
      case '购物':
        options.command = 'shopping';
        break;
      case 'malls':
      case '商场':
        options.command = 'malls';
        break;
      case 'living':
      case '宜居':
        options.command = 'living';
        break;
      case 'weather':
      case '天气':
        options.command = 'weather';
        break;
      case 'cost':
      case '成本':
        options.command = 'cost';
        break;
      case 'info':
      case 'help':
      case '帮助':
        options.command = 'info';
        break;
      default:
        if (['spots', 'attractions', 'food', 'transport', 'culture', 'shopping', 'living'].includes(options.command)) {
          options.query = arg;
        }
    }
    i++;
  }

  return options;
}

function showHelp() {
  console.log(`
🏙️ Nanning 技能包 - 南宁城市信息查询

用法: nanning <命令> [选项]

【景点】
  nanning spots [关键词]     查询南宁景点
  nanning attractions       列出所有景点

【美食】
  nanning food             列出南宁特色美食
  nanning food --popular   显示人气美食榜单

【交通】
  nanning transport        交通总览
  nanning metro            地铁信息
  nanning airport          机场信息

【文化】
  nanning culture           文化介绍
  nanning festivals        节庆活动
  nanning history          历史沿革

【购物】
  nanning shopping          购物指南
  nanning malls             商场推荐

【宜居】
  nanning living            宜居信息
  nanning weather           气候特点
  nanning cost              生活成本

【帮助】
  nanning info             显示帮助信息
  nanning help

示例:
  nanning spots 青秀山
  nanning food 老友粉
  nanning transport
  nanning culture
  `);
}

function showIntro() {
  console.log(`
🏙️ 欢迎使用 Nanning 技能包！

南宁，别称"绿城"、"邕城"，是广西壮族自治区首府，
北部湾经济区核心城市，中国-东盟博览会永久举办地。

输入 "nanning help" 查看所有可用命令。
  `);
}

function searchSpots(query) {
  if (!query) return data.spots;
  const lowerQuery = query.toLowerCase();
  return data.spots.filter(s => 
    s.name.toLowerCase().includes(lowerQuery) ||
    s.type.toLowerCase().includes(lowerQuery) ||
    s.description.toLowerCase().includes(lowerQuery)
  );
}

function searchFood(query, popular) {
  let foods = [...data.food];
  if (popular) {
    foods = foods.filter(f => f.mustTry);
  }
  if (!query || query === 'popular') return foods;
  const lowerQuery = query.toLowerCase();
  return foods.filter(f =>
    f.name.toLowerCase().includes(lowerQuery) ||
    f.type.toLowerCase().includes(lowerQuery) ||
    f.description.toLowerCase().includes(lowerQuery)
  );
}

async function main() {
  const options = parseArgs();

  switch (options.command) {
    case 'spots':
      console.log('\n🗺️  南宁景点推荐\n');
      console.log(formatSpots(searchSpots(options.query)));
      console.log();
      break;

    case 'food':
      console.log('\n🍜 南宁美食指南\n');
      const popular = options.query === 'popular';
      console.log(formatFood(searchFood(options.query, popular)));
      console.log();
      break;

    case 'transport':
      console.log('\n🚄 南宁交通指南\n');
      const t = data.transport;
      console.log(`【航空】${t.airport.name} (${t.airport.code})`);
      console.log(`  ${t.airport.description}`);
      console.log(`  📍${t.airport.location}`);
      console.log(`  🚕距市中心约30公里 | 🚌机场大巴覆盖全市\n`);
      console.log('【铁路】');
      t.railway.forEach(r => {
        console.log(`  ${r.name} (${r.type}) - ${r.description}`);
        console.log(`  📍${r.location}`);
      });
      console.log('\n【地铁】');
      console.log(`  已开通${t.metro.lines}条线路：${t.metro.popular.join('、')}`);
      console.log(`  ${t.metro.note}\n`);
      console.log('【公交】】');
      console.log(`  ${t.bus.description}`);
      console.log(`  类型：${t.bus.types.join('、')}\n`);
      break;

    case 'metro':
      console.log('\n🚇 南宁地铁信息\n');
      console.log(`已开通 ${data.transport.metro.lines} 条线路：${data.transport.metro.popular.join('、')}`);
      console.log(`${data.transport.metro.note}`);
      console.log();
      break;

    case 'airport':
      console.log('\n✈️  南宁吴圩国际机场\n');
      const a = data.transport.airport;
      console.log(`等级：${a.level}级国际机场`);
      console.log(`简介：${a.description}`);
      console.log(`位置：${a.location}`);
      console.log(`交通：${a.taxi}\n  ${a.bus}\n`);
      break;

    case 'culture':
    case 'festivals':
      if (options.command === 'festivals') {
        console.log('\n🎉 南宁节庆活动\n');
        data.culture.festivals.forEach(f => {
          console.log(`【${f.name}】${f.time}`);
          console.log(`  ${f.description}`);
        });
      } else {
        console.log('\n🎭 南宁文化介绍\n');
        console.log(`民族构成：${data.culture.ethnicGroups}`);
        console.log(`语言：${data.culture.language}`);
        console.log('\n主要节庆：');
        data.culture.festivals.forEach(f => {
          console.log(`  - ${f.name} (${f.time})`);
        });
      }
      console.log();
      break;

    case 'history':
      console.log('\n📜 南宁历史沿革\n');
      data.culture.history.forEach(h => {
        console.log(`【${h.period}】${h.event}`);
      });
      console.log();
      break;

    case 'shopping':
    case 'malls':
      console.log('\n🛍️ 南宁购物指南\n');
      data.shopping.forEach(s => {
        console.log(`【${s.name}】${s.type}`);
        console.log(`  ${s.description}`);
        console.log(`  ✨${s.highlight}`);
      });
      console.log();
      break;

    case 'living':
    case 'weather':
      if (options.command === 'weather') {
        console.log('\n🌤️ 南宁气候特点\n');
        const w = data.living.weather;
        console.log(`气候类型：${w.climate}`);
        console.log(`气候特点：${w.features}`);
        console.log(`年均温度：${w.temperature}`);
        console.log(`穿衣建议：${w.clothing}\n`);
      } else {
        console.log('\n🏠 南宁宜居指南\n');
        console.log('【气候】');
        const w = data.living.weather;
        console.log(`  ${w.climate} | ${w.features}`);
        console.log(`  ${w.temperature}\n`);
        console.log('【医疗资源】');
        data.living.healthcare.forEach(h => console.log(`  🏥 ${h}`));
        console.log('\n【教育资源】');
        data.living.education.forEach(e => console.log(`  🎓 ${e}`));
        console.log();
      }
      break;

    case 'cost':
      console.log('\n💰 南宁生活成本\n');
      const c = data.living.cost;
      console.log(`住房：${c.housing}`);
      console.log(`租房：${c.rent}`);
      console.log(`餐饮：${c.food}`);
      console.log(`交通：${c.traffic}\n`);
      break;

    case 'info':
    case 'help':
    default:
      if (options.command === 'info' && !options.query) {
        showIntro();
      } else {
        showHelp();
      }
  }
}

main();