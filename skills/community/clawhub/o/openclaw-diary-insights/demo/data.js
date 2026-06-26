// ===== INSIGHT DATA =====
// 此文件由 note-extractor skill 自动生成
// 手动编辑会在下次生成时被覆盖

const thoughtCards = [
  {id:1,insight:"个人品牌的本质是信任的积累，AI 可以帮助放大但不能替代。",date:"2026-01-05",cat:"个人品牌",imp:5},
  {id:2,insight:"知识管理工具的问题不是功能不够，而是用户没有动力持续输入。",date:"2026-01-08",cat:"产品洞察",imp:5},
  {id:3,insight:"日记不只是记录过去，更是在训练未来的自己。",date:"2026-01-12",cat:"日记哲学",imp:4},
  {id:4,insight:"在 AI 时代，「提问能力」比「回答能力」更重要。",date:"2026-01-18",cat:"AI 认知",imp:5},
  {id:5,insight:"代码、媒体、资本都是杠杆。我目前最缺的是「媒体杠杆」。",date:"2026-01-22",cat:"个人策略",imp:5},
  {id:6,insight:"耐心是一种被低估的能力，无论是投资还是做产品。",date:"2026-02-10",cat:"人生智慧",imp:4},
  {id:7,insight:"Second Brain 不只是工具，它是一种生活方式的选择。",date:"2026-02-14",cat:"产品哲学",imp:4},
  {id:8,insight:"好的 prompt 本质上是清晰的思维表达。",date:"2026-02-18",cat:"AI 认知",imp:4},
  {id:9,insight:"LLM 是一种新的计算范式，不是传统软件的升级。",date:"2026-02-18",cat:"AI 认知",imp:5},
  {id:10,insight:"数据可视化的本质不是展示数据，而是讲故事。",date:"2026-03-07",cat:"产品洞察",imp:4},
  {id:11,insight:"持续性比质量更重要 ── Building in Public 的核心法则。",date:"2026-03-03",cat:"个人品牌",imp:4},
  {id:12,insight:"投资决策框架 v1：趋势 > 估值 > 情绪。",date:"2026-03-03",cat:"投资理财",imp:5}
];

const catStyles = {"个人品牌":"brand","产品洞察":"product","日记哲学":"life","AI 认知":"ai","个人策略":"brand","人生智慧":"life","产品哲学":"product","投资理财":"invest"};

const diaryEntries = {
  "2026-01-05":{mood:"curious",label:"好奇",entries:[{time:"09:15",type:"主动记录",content:"今天开始研究 AI Agent 的商业化路径，感觉 B2B2C 可能是最靠谱的方向。"},{time:"14:30",type:"陪读",content:"读了 a16z 关于 AI Agent 的报告，里面提到 Agent 的核心价值在于减少人类的认知负担。"},{time:"22:00",type:"主动记录",content:"晚上散步时想到，个人品牌的本质是信任的积累，AI 可以帮助放大但不能替代。"}]},
  "2026-01-08":{mood:"energetic",label:"充沛",entries:[{time:"10:00",type:"协作",content:"和团队讨论了 Second Brain 的产品定位，大家一致认为「倾倒式记录」是核心体验。"},{time:"16:45",type:"主动记录",content:"突然意识到，知识管理工具的问题不是功能不够，而是用户没有动力持续输入。"}]},
  "2026-01-12":{mood:"focused",label:"专注",entries:[{time:"08:30",type:"主动记录",content:"早起看了一篇关于 PARA 方法论的文章，觉得可以借鉴但需要简化。"},{time:"13:00",type:"陪读",content:"研究了 Mem.ai 和 Notion AI 的产品逻辑，发现它们都在往「AI 自动组织」方向走。"},{time:"19:30",type:"主动记录",content:"今天投资组合涨了 3%，主要是 AI 板块带动。需要重新评估仓位配置。"},{time:"23:00",type:"主动记录",content:"睡前想到一个点：日记不只是记录过去，更是在训练未来的自己。"}]},
  "2026-01-15":{mood:"determined",label:"坚定",entries:[{time:"09:00",type:"主动记录",content:"决定开始 Building in Public，先从每周写一篇 AI 观察开始。"},{time:"15:00",type:"协作",content:"帮同事梳理了一个 Agent Workflow 的设计，发现自己在这方面的经验已经可以输出了。"}]},
  "2026-01-18":{mood:"tired",label:"疲惫",entries:[{time:"11:00",type:"主动记录",content:"看到一个观点：在 AI 时代，「提问能力」比「回答能力」更重要。深以为然。"},{time:"20:00",type:"主动记录",content:"今天情绪有点低落，可能是连续加班的疲惫感。需要注意休息。"}]},
  "2026-01-22":{mood:"enlightened",label:"开悟",entries:[{time:"09:30",type:"陪读",content:"读完了《纳瓦尔宝典》，最大的收获是「杠杆」的概念 ── 代码、媒体、资本都是杠杆。"},{time:"14:00",type:"主动记录",content:"把纳瓦尔的杠杆理论和自己的情况对照，发现我目前最缺的是「媒体杠杆」。"},{time:"21:00",type:"主动记录",content:"和朋友聊了创业的想法，他建议我先做一个 MVP 验证需求再说。"}]},
  "2026-01-26":{mood:"energetic",label:"充沛",entries:[{time:"10:00",type:"协作",content:"参加了一个 AI Hackathon 的线上分享，认识了几个很厉害的独立开发者。"},{time:"17:00",type:"主动记录",content:"开始整理自己的投资笔记，发现过去半年的决策逻辑其实很混乱，需要建立框架。"}]},
  "2026-02-01":{mood:"determined",label:"坚定",entries:[{time:"08:00",type:"主动记录",content:"新的一个月，给自己定了三个目标：1.完成 Second Brain MVP 2.发布第一篇公开文章 3.建立投资决策框架"},{time:"14:00",type:"陪读",content:"研究了 LangChain 和 CrewAI 的架构，觉得多 Agent 协作是未来的方向。"},{time:"22:30",type:"主动记录",content:"写了第一篇草稿《为什么每个人都需要一个 AI 分身》，还不太满意，明天继续改。"}]},
  "2026-02-05":{mood:"proud",label:"自豪",entries:[{time:"09:00",type:"主动记录",content:"文章改了三版终于满意了，发到了即刻上，收到了不少正面反馈。"},{time:"16:00",type:"主动记录",content:"有人私信问我怎么搭建个人知识体系，看来这个需求确实存在。"}]},
  "2026-02-10":{mood:"calm",label:"平静",entries:[{time:"10:30",type:"主动记录",content:"投资组合这个月回撤了 5%，但我按照新框架分析后决定不动，保持纪律。"},{time:"15:00",type:"协作",content:"和 DK 讨论了数据导入的方案，飞书的 API 比想象中好用。"},{time:"21:00",type:"主动记录",content:"今天的收获：耐心是一种被低估的能力，无论是投资还是做产品。"}]},
  "2026-02-14":{mood:"warm",label:"温暖",entries:[{time:"12:00",type:"主动记录",content:"情人节，和另一半聊了未来的规划，发现我们对「好生活」的定义越来越一致了。"},{time:"20:00",type:"主动记录",content:"突然想到，Second Brain 不只是工具，它是一种生活方式的选择。"}]},
  "2026-02-18":{mood:"exhausted",label:"疲惫",entries:[{time:"09:00",type:"主动记录",content:"开始系统学习 Prompt Engineering，发现好的 prompt 本质上是清晰的思维表达。"},{time:"14:30",type:"陪读",content:"看了 Andrej Karpathy 的演讲，他说 LLM 是一种新的计算范式，不是传统软件的升级。"},{time:"23:00",type:"主动记录",content:"连续高强度学习了两周，需要给自己放个假。身体是革命的本钱。"}]},
  "2026-02-22":{mood:"refreshed",label:"焕新",entries:[{time:"10:00",type:"主动记录",content:"休息了两天感觉好多了。重新审视了自己的目标，决定聚焦在 Second Brain 这一件事上。"},{time:"16:00",type:"主动记录",content:"第二篇文章《AI 时代的个人护城河》写完了，这次写得更顺畅了。"}]},
  "2026-02-28":{mood:"grateful",label:"感恩",entries:[{time:"09:00",type:"主动记录",content:"二月复盘：三个目标完成了两个，投资框架还在迭代中。整体满意。"},{time:"15:00",type:"协作",content:"Hackathon 团队确定了分工，我负责可视化和后处理部分，很兴奋。"},{time:"21:00",type:"主动记录",content:"回顾这两个月的日记，发现自己的思考确实在变得更系统化。日记的力量。"}]},
  "2026-03-03":{mood:"determined",label:"坚定",entries:[{time:"08:30",type:"主动记录",content:"三月的主题：执行力。想法够多了，现在需要把它们变成现实。"},{time:"13:00",type:"陪读",content:"研究了几个成功的 Building in Public 案例，发现持续性比质量更重要。"},{time:"19:00",type:"主动记录",content:"今天把投资决策框架 v1 整理出来了，核心是：趋势 > 估值 > 情绪。"}]},
  "2026-03-07":{mood:"flow",label:"心流",entries:[{time:"10:00",type:"协作",content:"和 Yitong 对齐了 Diary Skill 的接口，我的 note-extractor 可以直接读取日记文件。"},{time:"15:30",type:"主动记录",content:"在做可视化原型时想到，数据可视化的本质不是展示数据，而是讲故事。"},{time:"22:00",type:"主动记录",content:"今天状态很好，进入了心流状态，连续编码了 4 个小时。"}]},
  "2026-03-10":{mood:"confident",label:"自信",entries:[{time:"09:00",type:"主动记录",content:"开始思考 AI Agent 如何帮助普通人建立个人品牌，这可能是我下一篇文章的主题。"},{time:"14:00",type:"主动记录",content:"投资组合本月已经回升了 8%，框架在起作用。继续观察。"},{time:"20:00",type:"主动记录",content:"和一个做独立开发的朋友深聊了三小时，他的经历让我更坚定了做 Second Brain 的方向。"}]},
  "2026-03-14":{mood:"proud",label:"自豪",entries:[{time:"09:30",type:"主动记录",content:"Hackathon 倒计时，今天要把可视化 demo 做出来。压力就是动力。"},{time:"16:00",type:"协作",content:"团队 sync，大家的进度都不错。Onboarding 和 Diary 已经可以跑通了。"},{time:"23:00",type:"主动记录",content:"回顾这三个月，从一个模糊的想法到一个可以 demo 的产品，这就是执行力的意义。"}]}
};

const moodPositive = ["inspired","energetic","eureka","confident","proud","validated","excited","hopeful","enlightened","accomplished","flow","refreshed","grateful","warm","creative","optimistic","reinforced"];
const moodNeutral = ["curious","focused","analytical","reflective","philosophical","strategic","calm","productive","wise","determined","persistent","satisfied","mind-blown"];

const dimensionScores = {
  "一月":{职业技能:75,学习成长:80,投资理财:40,社交关系:50,健康平衡:30,创造输出:45},
  "二月":{职业技能:80,学习成长:85,投资理财:60,社交关系:55,健康平衡:45,创造输出:70},
  "三月":{职业技能:85,学习成长:75,投资理财:70,社交关系:60,健康平衡:50,创造输出:80}
};

const nodeData = [
  {id:"Vivi",group:"person",desc:"产品经理 / AI 探索者",size:28},
  {id:"AI Agent",group:"topic",desc:"商业化路径、B2B2C、多Agent协作",size:22},
  {id:"个人品牌",group:"topic",desc:"信任积累、媒体杠杆、辨识度",size:20},
  {id:"知识管理",group:"topic",desc:"PARA方法论、AI自动组织",size:18},
  {id:"投资理财",group:"topic",desc:"趋势>估值>情绪、纪律",size:18},
  {id:"Building in Public",group:"topic",desc:"持续性 > 质量、每周输出",size:18},
  {id:"Second Brain",group:"topic",desc:"倾倒式记录、生活方式",size:22},
  {id:"写作",group:"topic",desc:"AI分身、个人护城河",size:16},
  {id:"阅读",group:"topic",desc:"纳瓦尔宝典、Karpathy",size:14},
  {id:"Hackathon",group:"topic",desc:"可视化、团队协作",size:16},
  {id:"健康",group:"topic",desc:"休息、平衡、身体是本钱",size:14},
  {id:"杠杆理论",group:"concept",desc:"代码 / 媒体 / 资本",size:16},
  {id:"LLM 范式",group:"concept",desc:"新计算范式，非传统软件升级",size:14},
  {id:"提问能力",group:"concept",desc:"比回答能力更重要",size:14},
  {id:"执行力",group:"concept",desc:"想法→现实的桥梁",size:14},
  {id:"心流",group:"concept",desc:"最佳创造状态",size:12},
  {id:"DK",group:"person",desc:"数据导入、飞书API",size:14},
  {id:"Yitong",group:"person",desc:"核心系统、Diary Skill",size:14}
];

const linkData = [
  {s:"Vivi",t:"AI Agent"},{s:"Vivi",t:"个人品牌"},{s:"Vivi",t:"Second Brain"},
  {s:"Vivi",t:"投资理财"},{s:"Vivi",t:"Building in Public"},{s:"Vivi",t:"写作"},
  {s:"Vivi",t:"健康"},{s:"AI Agent",t:"LLM 范式"},{s:"个人品牌",t:"杠杆理论"},
  {s:"个人品牌",t:"Building in Public"},{s:"知识管理",t:"Second Brain"},
  {s:"投资理财",t:"杠杆理论"},{s:"阅读",t:"杠杆理论"},
  {s:"写作",t:"Building in Public"},{s:"写作",t:"心流"},
  {s:"AI Agent",t:"提问能力"},{s:"Hackathon",t:"执行力"},
  {s:"DK",t:"Second Brain"},{s:"Yitong",t:"Second Brain"},
  {s:"Vivi",t:"Hackathon"},{s:"DK",t:"Hackathon"},{s:"Yitong",t:"Hackathon"},
  {s:"Second Brain",t:"知识管理"},{s:"杠杆理论",t:"写作"}
];
