/* One catalogue for presets, composable tokens and source attribution. No vendor-specific renderer. */
(function(scope){
  'use strict';
  const sources=[
    {id:'xmind',name:'Xmind',url:'https://xmind.com/user-guide/applying-global-format',feature:'骨架、节点形态与配色分离；有序的层级边界。'},
    {id:'mindnode',name:'MindNode',url:'https://www.mindnode.com/themes',feature:'清透描边、自然彩枝、石板暗底、霓虹、彩块与暗夜粉彩。'},
    {id:'ayoa',name:'Ayoa',url:'https://support.ayoa.com/formatting-organic-branches',feature:'曲线分支和有机形态；提炼为从粗到细的渐细曲枝。'},
    {id:'coggle',name:'Coggle',url:'https://coggle.help/article/45-change-the-colour-of-a-branch',feature:'无框文字分支，以及分支颜色向后代继承。'},
    {id:'markmap',name:'Markmap',url:'https://markmap.js.org/docs/json-options',feature:'紧凑文字阅读、分支配色、初始展开深度和折叠。'},
    {id:'mindmeister',name:'MindMeister',url:'https://support.mindmeister.com/hc/en-us/articles/360017494280-Customize-Your-Map-s-Appearance',feature:'统一主题、节点形态、边框、字体和背景的协调。'},
    {id:'original',name:'枝序原创',url:null,feature:'组合编码、索引卡片和纸面阅读配方。'}
  ];
  const axes={
    L:{name:'展开结构',items:[
      {code:'L01',id:'balanced',name:'左右展开'}, {code:'L02',id:'right',name:'向右展开'},
      {code:'L03',id:'down',name:'向下层级'}, {code:'L04',id:'brace',name:'括号分解'}, {code:'L05',id:'outline',name:'缩进大纲'}
    ]},
    N:{name:'节点形态',items:[
      {code:'N01',id:'underline',name:'文字下划线',description:'实底根节点，轻量文字与下划线子节点。'},
      {code:'N02',id:'outline',name:'清透描边',description:'根节点与子节点保留圆角边框和清透底色。'},
      {code:'N03',id:'solid',name:'实色方块',description:'子节点直接使用分支颜色，文字自动选择深浅对比。'},
      {code:'N04',id:'pill',name:'柔色胶囊',description:'胶囊主节点与同族圆角子节点。'},
      {code:'N05',id:'paper',name:'纸面卡片',description:'柔和浅色卡片，适合长时间阅读。'},
      {code:'N06',id:'text',name:'无框文字',description:'减少节点外框，把注意力交给文字与连线。'},
      {code:'N07',id:'sketch',name:'手绘贴片',description:'轻微双轮廓与断续边框，呈现贴片质感。'},
      {code:'N08',id:'index',name:'索引卡片',description:'卡片边缘的颜色条为各分支建立视觉索引。'},
      {code:'N09',id:'fold',name:'折角纸签',description:'切角轮廓与翻折纸角，让节点像可整理的纸签。'},
      {code:'N10',id:'frame',name:'双框书签',description:'内外双线边界，形成克制的书签和印刷感。'},
      {code:'N11',id:'tag',name:'切口标签',description:'切口与小孔构成标签轮廓，用于分类阅读。'},
      {code:'N12',id:'header',name:'页眉卡片',description:'顶部色带与留白卡片，突出分支的归属。'}
    ]},
    E:{name:'连线语言',items:[
      {code:'E01',id:'curve',name:'轻柔曲线'}, {code:'E02',id:'elbow',name:'秩序折线'},
      {code:'E03',id:'organic',name:'渐细曲枝'}, {code:'E04',id:'straight',name:'直线连接'},
      {code:'E05',id:'dash',name:'断续笔触'}, {code:'E06',id:'dotted',name:'点状连线'},
      {code:'E07',id:'rounded',name:'圆角折线'}, {code:'E08',id:'double',name:'双线连接'}
    ]},
    C:{name:'分支配色',items:[
      {code:'C01',id:'graphite',name:'石墨单色',accent:'#303b3d',colors:['#56656a']},
      {code:'C02',id:'olive',name:'自然草木',accent:'#436639',colors:['#6d993c','#a5b853','#e0ba52','#c77a50','#859e6d','#4c856a']},
      {code:'C03',id:'navy',name:'海军蓝阶',accent:'#234765',colors:['#2b5b87','#426d87','#53668c','#3d7280']},
      {code:'C04',id:'teal',name:'青绿冷调',accent:'#2c7978',colors:['#378b96','#388a78','#5e879c','#5c6d87']},
      {code:'C05',id:'rainbow',name:'明亮彩虹',accent:'#38869c',colors:['#168fc3','#ee8a48','#7458c9','#00a786','#e6b936','#db6497']},
      {code:'C06',id:'neon',name:'夜光彩枝',accent:'#a2b8f1',colors:['#f3a571','#6fd4da','#b0a0ee','#ef94ae','#a8d7a8','#f2d28b']},
      {code:'C07',id:'pastel',name:'粉彩色群',accent:'#8974a3',colors:['#a9d6a4','#f1d48a','#f4b2d2','#b8b4ec','#8cced0','#e7a075']},
      {code:'C08',id:'seafoam',name:'海盐珊瑚',accent:'#cd796e',colors:['#2e8d9b','#4b647b','#32978f','#5b7d89']},
      {code:'C09',id:'earth',name:'大地暖色',accent:'#95664a',colors:['#b17e53','#8b995c','#b16d66','#928270']},
      {code:'C10',id:'citrus',name:'柑橘实验',accent:'#5f7363',colors:['#8cba40','#dc9d3b','#49a9b0','#df7d61','#7a91c1']},
      {code:'C11',id:'cobalt',name:'钴蓝留白',accent:'#27599c',colors:['#3269b4','#6f8ac4','#318fa8','#526b8a']},
      {code:'C12',id:'berry',name:'莓果茶色',accent:'#984e70',colors:['#a75d82','#bf7b73','#866b9e','#a18b62']},
      {code:'C13',id:'vermilion',name:'朱墨山色',accent:'#9c4036',colors:['#394a48','#9c4036','#7b8569','#9b805d']},
      {code:'C14',id:'lagoon',name:'海湾薄荷',accent:'#287c7b',colors:['#318e94','#6aa99a','#4d7fa5','#b4a15e']}
    ]},
    B:{name:'画布材质',items:[
      {code:'B01',id:'white',name:'纯净白',bg:'#ffffff',surface:'#ffffff',ink:'#293b40',dark:false},
      {code:'B02',id:'paper',name:'暖纸面',bg:'#f5f2e9',surface:'#fffdf7',ink:'#3d4438',dark:false},
      {code:'B03',id:'slate',name:'石板灰',bg:'#435c67',surface:'#f3f2ec',ink:'#eef4f4',dark:true,rootFill:'#f3f2ec',rootInk:'#34474b'},
      {code:'B04',id:'black',name:'深夜黑',bg:'#0c0e13',surface:'#23272f',ink:'#eef4f8',dark:true,rootFill:'#191d24',rootInk:'#eef4f8',rootStroke:'#e5edf2'},
      {code:'B05',id:'bluegrid',name:'深蓝网格',bg:'#152333',surface:'#203449',ink:'#e3edf7',dark:true,pattern:'grid'},
      {code:'B06',id:'dotpaper',name:'点阵便笺',bg:'#faf8f2',surface:'#fffefa',ink:'#3b4141',dark:false,pattern:'dots'},
      {code:'B07',id:'lilac',name:'浅雾紫',bg:'#f6f3fa',surface:'#fffaff',ink:'#443c52',dark:false},
      {code:'B08',id:'mist',name:'柔雾灰',bg:'#f1f3f1',surface:'#ffffff',ink:'#293c38',dark:false},
      {code:'B09',id:'chalk',name:'森林黑板',bg:'#233e35',surface:'#304d42',ink:'#eef4e8',dark:true,rootFill:'#e6eddb',rootInk:'#304135'},
      {code:'B10',id:'linen',name:'米白方格',bg:'#f5f3eb',surface:'#fffdf8',ink:'#39423e',dark:false,pattern:'grid'},
      {code:'B11',id:'rose',name:'浅玫瑰纸',bg:'#f8eff0',surface:'#fffafb',ink:'#503b45',dark:false}
    ]},
    T:{name:'字体气质',items:[
      {code:'T01',id:'sans',name:'清晰无衬线',font:"-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif"},
      {code:'T02',id:'serif',name:'书卷衬线',font:"'Songti SC','STSong',Georgia,serif"},
      {code:'T03',id:'mono',name:'技术等宽',font:"ui-monospace,'SFMono-Regular',Consolas,'PingFang SC',monospace"}
    ]},
    D:{name:'阅读疏密',items:[
      {code:'D01',id:'compact',name:'紧凑',rowGap:10,colGap:60},
      {code:'D02',id:'standard',name:'标准',rowGap:18,colGap:85},
      {code:'D03',id:'airy',name:'舒展',rowGap:32,colGap:112}
    ]}
  };
  // Shared components extracted from the official static theme definitions.
  axes.N.items.push({"code": "N13", "id": "hierarchy", "name": "层级曲枝", "description": "圆润中心、轻量关键词与逐层细化的分支。"},{"code": "N14", "id": "silk", "name": "轻盈彩卡", "description": "主分支柔色卡片，末级节点降低填色与边界强度。"},{"code": "N15", "id": "fine", "name": "细线圆框", "description": "清透留白与细圆角边框，保持文字清晰。"});
  axes.C.items.push({"code": "C15", "id": "theme-palette-0", "name": "雅致色群", "accent": "#ffffff", "colors": ["#1287de", "#26bbd1", "#389337", "#dc2228", "#fdb60d", "#922aa5"]},{"code": "C16", "id": "theme-palette-1", "name": "清新色群", "accent": "#add524", "colors": ["#48b04c", "#36bbb1", "#269cbb", "#ee695f", "#eea600", "#ffe52b"]},{"code": "C17", "id": "theme-palette-2", "name": "彩虹经典色群", "accent": "#ffffff", "colors": ["#af50c8", "#5a5ad2", "#64c8cd", "#00aa7a", "#ffcd3c", "#ff965a", "#ff6068", "#fd5ba7"]},{"code": "C18", "id": "theme-palette-3", "name": "石板经典色群", "accent": "#ffffff", "colors": ["#ffcd3c", "#ff5f69", "#64c8cd", "#ff965a", "#af50c8", "#64aae1"]},{"code": "C19", "id": "theme-palette-4", "name": "青碧经典色群", "accent": "#ffffff", "colors": ["#ffeeb9", "#ff8f96", "#b4f5f0", "#bb6ad0", "#ffd7a0", "#cdebff"]},{"code": "C20", "id": "theme-palette-5", "name": "冰蓝色群", "accent": "#ffffff", "colors": ["#294a70", "#294a70", "#294a70", "#294a70", "#294a70", "#294a70"]},{"code": "C21", "id": "theme-palette-6", "name": "日光黄色群", "accent": "#ffffff", "colors": ["#f0a330", "#f0a330", "#f0a330", "#f0a330", "#f0a330", "#f0a330"]},{"code": "C22", "id": "theme-palette-7", "name": "薄荷绿色群", "accent": "#ffffff", "colors": ["#115462", "#115462", "#115462", "#115462", "#115462", "#115462"]},{"code": "C23", "id": "theme-palette-8", "name": "樱花粉色群", "accent": "#ffffff", "colors": ["#ba2d33", "#ba2d33", "#ba2d33", "#ba2d33", "#ba2d33", "#ba2d33"]},{"code": "C24", "id": "theme-palette-9", "name": "浅藤紫色群", "accent": "#ffffff", "colors": ["#343b71", "#343b71", "#343b71", "#343b71", "#343b71", "#343b71"]},{"code": "C25", "id": "theme-palette-10", "name": "杏橙色群", "accent": "#ffffff", "colors": ["#ef6840", "#ef6840", "#ef6840", "#ef6840", "#ef6840", "#ef6840"]},{"code": "C26", "id": "theme-palette-11", "name": "自然色群", "accent": "#cee397", "colors": ["#bf211e", "#f2a359", "#fed766", "#cee397", "#abcc60", "#629926"]},{"code": "C27", "id": "theme-palette-12", "name": "柔色夜幕色群", "accent": "#2a9d8f", "colors": ["#e76f51", "#f4a261", "#e9c46a", "#8ab17d", "#2a9d8f", "#287271", "#e76f51"]},{"code": "C28", "id": "theme-palette-13", "name": "怡然色群", "accent": "#577590", "colors": ["#f94144", "#f3722c", "#f8961e", "#f9c74f", "#90be6d", "#43aa8b"]},{"code": "C29", "id": "theme-palette-14", "name": "微型图形色群", "accent": "#002f5b", "colors": ["#9636af", "#af50c8", "#9636af", "#7c1d95", "#ff5f69", "#64c8cd"]},{"code": "C30", "id": "theme-palette-15", "name": "远景色群", "accent": "#99adba", "colors": ["#3282bd", "#79e6e6", "#b0eb55", "#a078ff", "#ff51af", "#cd913c"]},{"code": "C31", "id": "theme-palette-16", "name": "纯黑色群", "accent": "#ffffff", "colors": ["#64c8cd", "#5abedc", "#64aae1", "#9191e1", "#ff8f96", "#ffa069"]},{"code": "C32", "id": "theme-palette-17", "name": "经典色群", "accent": "#808080", "colors": ["#ffcc66", "#ccff66", "#66ffcc", "#66ccff", "#cc66ff", "#ffe680"]},{"code": "C33", "id": "theme-palette-18", "name": "现代色群", "accent": "#808080", "colors": ["#7700d9", "#009bd8", "#00d9ab", "#00da00", "#d1d600", "#e73634"]},{"code": "C34", "id": "theme-palette-19", "name": "灵感沙盒色群", "accent": "#663300", "colors": ["#ff6600", "#ffcc00", "#999900", "#99cccc", "#009999", "#663300"]},{"code": "C35", "id": "theme-palette-20", "name": "热可可色群", "accent": "#808080", "colors": ["#a27a54", "#5a2113", "#502a06", "#fdba4f", "#864e05", "#9d732a"]},{"code": "C36", "id": "theme-palette-21", "name": "悦色色群", "accent": "#f6f6f6", "colors": ["#b037f3", "#25abff", "#ffbd0a", "#23cee0", "#d21559", "#31bb48"]},{"code": "C37", "id": "theme-palette-22", "name": "卡布奇诺色群", "accent": "#808080", "colors": ["#fdba4f", "#2e0d02", "#3c2202", "#a27a54", "#9d732a", "#864e05"]},{"code": "C38", "id": "theme-palette-23", "name": "暗夜粉彩色群", "accent": "#595959", "colors": ["#9a6088", "#6265a1", "#00787d", "#a64c12", "#99781e", "#4b8350"]},{"code": "C39", "id": "theme-palette-24", "name": "极简色群", "accent": "#ee695f", "colors": ["#002e49", "#005f7c", "#00716a", "#00716a", "#269cbb", "#0084a3"]},{"code": "C40", "id": "theme-palette-25", "name": "路线图色群", "accent": "#ee695f", "colors": ["#005493", "#009193", "#009051", "#941100", "#ff9300", "#ffd479"]},{"code": "C41", "id": "theme-palette-26", "name": "冬日色群", "accent": "#f2f4f4", "colors": ["#91a5d1", "#91a5d1", "#91a5d1", "#91a5d1", "#91a5d1", "#91a5d1", "#91a5d1"]},{"code": "C42", "id": "theme-palette-27", "name": "冬夜色群", "accent": "#ffffff", "colors": ["#91a5d1", "#91a5d1", "#91a5d1", "#91a5d1"]});
  axes.B.items.push({"code": "B12", "id": "theme-canvas-0", "name": "雅致画布", "bg": "#e7ebee", "surface": "#ffffff", "ink": "#435b66", "dark": false, "rootFill": "#ffffff", "rootInk": "#1a5569", "rootStroke": "#ffffff"},{"code": "B13", "id": "theme-canvas-1", "name": "清新画布", "bg": "#ffffff", "surface": "#ffffff", "ink": "#47443d", "dark": false, "rootFill": "#ffffff", "rootInk": "#526437", "rootStroke": "#add524"},{"code": "B14", "id": "theme-canvas-2", "name": "彩虹经典画布", "bg": "#f3f3f3", "surface": "#ffffff", "ink": "#ffffff", "dark": false, "rootFill": "#ffffff", "rootInk": "#74c8fe", "rootStroke": "#ffffff"},{"code": "B15", "id": "theme-canvas-3", "name": "石板经典画布", "bg": "#455a64", "surface": "#f3f3f3", "ink": "#eef2ef", "dark": true, "rootFill": "#f3f3f3", "rootInk": "#4b4b4b", "rootStroke": "#ffffff"},{"code": "B16", "id": "theme-canvas-4", "name": "青碧经典画布", "bg": "#64c8cd", "surface": "#ffffff", "ink": "#ffffff", "dark": false, "rootFill": "#ffffff", "rootInk": "#4b4b4b", "rootStroke": "#ffffff"},{"code": "B17", "id": "theme-canvas-5", "name": "冰蓝画布", "bg": "#e7f3ff", "surface": "#ffffff", "ink": "#1d1d20", "dark": false, "rootFill": "#ffffff", "rootInk": "#294a70", "rootStroke": "#ffffff"},{"code": "B18", "id": "theme-canvas-6", "name": "日光黄画布", "bg": "#fdf5dc", "surface": "#ffffff", "ink": "#1d1d20", "dark": false, "rootFill": "#ffffff", "rootInk": "#f0a330", "rootStroke": "#ffffff"},{"code": "B19", "id": "theme-canvas-7", "name": "薄荷绿画布", "bg": "#e2fffe", "surface": "#ffffff", "ink": "#1d1d20", "dark": false, "rootFill": "#ffffff", "rootInk": "#115462", "rootStroke": "#ffffff"},{"code": "B20", "id": "theme-canvas-8", "name": "樱花粉画布", "bg": "#feeeef", "surface": "#ffffff", "ink": "#1d1d20", "dark": false, "rootFill": "#ffffff", "rootInk": "#ba2d33", "rootStroke": "#ffffff"},{"code": "B21", "id": "theme-canvas-9", "name": "浅藤紫画布", "bg": "#f9f2ff", "surface": "#ffffff", "ink": "#1d1d20", "dark": false, "rootFill": "#ffffff", "rootInk": "#343b71", "rootStroke": "#ffffff"},{"code": "B22", "id": "theme-canvas-10", "name": "杏橙画布", "bg": "#fdeee5", "surface": "#ffffff", "ink": "#1d1d20", "dark": false, "rootFill": "#ffffff", "rootInk": "#ef6840", "rootStroke": "#ffffff"},{"code": "B23", "id": "theme-canvas-11", "name": "自然画布", "bg": "#f2f2f2", "surface": "#fffbf1", "ink": "#595959", "dark": false, "rootFill": "#fffbf1", "rootInk": "#156904", "rootStroke": "#cee397"},{"code": "B24", "id": "theme-canvas-12", "name": "柔色夜幕画布", "bg": "#264653", "surface": "#287271", "ink": "#eef2ef", "dark": true, "rootFill": "#287271", "rootInk": "#2fb1a2", "rootStroke": "#2a9d8f"},{"code": "B25", "id": "theme-canvas-13", "name": "怡然画布", "bg": "#eef6f4", "surface": "#cdd6db", "ink": "#636363", "dark": false, "rootFill": "#cdd6db", "rootInk": "#438b8b", "rootStroke": "#577590"},{"code": "B26", "id": "theme-canvas-14", "name": "微型图形画布", "bg": "#ffffff", "surface": "#ffffff", "ink": "#000000", "dark": false, "rootFill": "#ffffff", "rootInk": "#000000", "rootStroke": "#002f5b"},{"code": "B27", "id": "theme-canvas-15", "name": "远景画布", "bg": "#f7f7f7", "surface": "#99adba", "ink": "#636363", "dark": false, "rootFill": "#99adba", "rootInk": "#ffffff", "rootStroke": "#99adba"},{"code": "B28", "id": "theme-canvas-16", "name": "纯黑画布", "bg": "#000000", "surface": "#191919", "ink": "#eef2ef", "dark": true, "rootFill": "#191919", "rootInk": "#ffffff", "rootStroke": "#ffffff"},{"code": "B29", "id": "theme-canvas-17", "name": "经典画布", "bg": "#ffffff", "surface": "#ffffff", "ink": "#000000", "dark": false, "rootFill": "#ffffff", "rootInk": "#000000", "rootStroke": "#808080"},{"code": "B30", "id": "theme-canvas-18", "name": "现代画布", "bg": "#ffffff", "surface": "#ffffff", "ink": "#000000", "dark": false, "rootFill": "#ffffff", "rootInk": "#000000", "rootStroke": "#808080"},{"code": "B31", "id": "theme-canvas-19", "name": "灵感沙盒画布", "bg": "#fff5dc", "surface": "#ffffff", "ink": "#666666", "dark": false, "rootFill": "#ffffff", "rootInk": "#666666", "rootStroke": "#663300"},{"code": "B32", "id": "theme-canvas-20", "name": "热可可画布", "bg": "#2d2019", "surface": "#1b1613", "ink": "#eef2ef", "dark": true, "rootFill": "#1b1613", "rootInk": "#fee7bd", "rootStroke": "#808080"},{"code": "B33", "id": "theme-canvas-21", "name": "悦色画布", "bg": "#f4f6f4", "surface": "#ffffff", "ink": "#5b5b5b", "dark": false, "rootFill": "#ffffff", "rootInk": "#167b97", "rootStroke": "#f6f6f6"},{"code": "B34", "id": "theme-canvas-22", "name": "卡布奇诺画布", "bg": "#fee7bd", "surface": "#ffffff", "ink": "#2d2019", "dark": false, "rootFill": "#ffffff", "rootInk": "#2d2019", "rootStroke": "#808080"},{"code": "B35", "id": "theme-canvas-23", "name": "暗夜粉彩画布", "bg": "#222529", "surface": "#a6a6a6", "ink": "#eef2ef", "dark": true, "rootFill": "#a6a6a6", "rootInk": "#000000", "rootStroke": "#595959"},{"code": "B36", "id": "theme-canvas-24", "name": "极简画布", "bg": "#ffffff", "surface": "#ffffff", "ink": "#47443d", "dark": false, "rootFill": "#ffffff", "rootInk": "#526336", "rootStroke": "#ee695f"},{"code": "B37", "id": "theme-canvas-25", "name": "路线图画布", "bg": "#ffffff", "surface": "#ffffff", "ink": "#47443d", "dark": false, "rootFill": "#ffffff", "rootInk": "#526336", "rootStroke": "#ee695f"},{"code": "B38", "id": "theme-canvas-26", "name": "冬日画布", "bg": "#acd5ff", "surface": "#6684ba", "ink": "#0d2a4d", "dark": false, "rootFill": "#6684ba", "rootInk": "#ffffff", "rootStroke": "#f2f4f4"},{"code": "B39", "id": "theme-canvas-27", "name": "冬夜画布", "bg": "#acd5ff", "surface": "#6684ba", "ink": "#4b6088", "dark": false, "rootFill": "#6684ba", "rootInk": "#ffffff", "rootStroke": "#ffffff"});
  sources.push({id:'excalidraw',name:'Excalidraw',url:'https://github.com/excalidraw/excalidraw',feature:'手绘白板的松弛轮廓、复笔连线与轻量色块，转为原创 SVG 笔触组件。'});
  axes.N.items.push({"code": "N16", "id": "pencilbox", "name": "铅笔手绘框"},{"code": "N17", "id": "bubble", "name": "随手圈圈"},{"code": "N18", "id": "marker", "name": "脑洞涂鸦"});
  axes.E.items.push({"code": "E09", "id": "pencil", "name": "铅笔随行线"});
  axes.C.items.push({"code": "C43", "id": "sketchink", "name": "钢笔与蜡笔", "accent": "#38443f", "colors": ["#42796c", "#b3754c", "#6975a0", "#ad6578"]},{"code": "C44", "id": "playful", "name": "果冻彩笔", "accent": "#80577c", "colors": ["#4b8f89", "#c79038", "#a66d8b", "#7a7cba"]},{"code":"C45","id":"chalkpastel","name":"暖灰杏彩","accent":"#916044","mark":"#d99670","colors":["#657e89","#987052","#7d788f","#748478"]});
  axes.B.items.push({"code": "B40", "id": "sketchpaper", "name": "速写本", "bg": "#fbf9f1", "surface": "#fffdf6", "ink": "#37423f", "dark": false},{"code": "B41", "id": "notebook", "name": "横线手账", "bg": "#fffdf7", "surface": "#fffdf7", "ink": "#41483d", "dark": false, "pattern": "ruled"},{"code":"B42","id":"sketchslate","name":"浮生蓝灰","bg":"#ccd9de","surface":"#e8edec","ink":"#292d32","dark":false,"rootFill":"#e8edec","rootInk":"#292d32","rootStroke":"#292d32"});
  axes.T.items.push({"code": "T04", "id": "casual", "name": "随手笔记", "font": "'Kaiti SC','STKaiti','KaiTi','Comic Sans MS',cursive"});
  axes.N.items.push({code:'N19',id:'capsule-outline',name:'饱满圆角描边',description:'通透背景、饱满圆角与清晰彩色轮廓。'},{code:'N20',id:'colorblock',name:'明亮实色卡',description:'鲜明彩块与留白中心，适合轻快展示。'},{code:'N21',id:'pastel-patch',name:'粉彩手作贴片',description:'柔和实色、轻微起伏边缘与短虚线缝边。'});
  axes.E.items.push({code:'E10',id:'roundbranch',name:'圆润彩枝'});
  axes.T.items.push({code:'T05',id:'editorial',name:'优雅 · 思源宋体',font:"'Atlas Elegant','Songti SC',serif",category:'优雅阅读',embedded:true},{code:'T06',id:'professional',name:'商务 · 思源黑体',font:"'Atlas Business','PingFang SC',sans-serif",category:'商务清晰',embedded:true},{code:'T07',id:'brush',name:'个性 · 马善政毛笔',font:"'Atlas Brush','Kaiti SC',cursive",category:'笔墨手作',embedded:true},{code:'T08',id:'playful',name:'有趣 · 站酷快乐体',font:"'Atlas Playful','PingFang SC',cursive",category:'轻松有趣',embedded:true});
  axes.C.items.find(c=>c.code==='C38').colors=["#f5b5e0", "#b3b3f5", "#64c8cd", "#ff965a", "#ffd479", "#a2dea5"];
  axes.T.items.push({"code": "T09", "id": "wenkai", "name": "中文 · 霞鹜文楷", "font": "'Atlas WenKai','Atlas Business',sans-serif", "language": "zh", "category": "常用 · 手写阅读", "embedded": true, "file": "wenkai", "family": "LXGW WenKai TC"},{"code": "T10", "id": "inter", "name": "English · Inter", "font": "'Atlas Inter','Atlas Business',sans-serif", "language": "en", "category": "常用 · 商务界面", "embedded": true, "file": "inter", "family": "Inter"},{"code": "T11", "id": "lora", "name": "English · Lora", "font": "'Atlas Lora','Atlas Elegant',serif", "language": "en", "category": "常用 · 阅读衬线", "embedded": true, "file": "lora", "family": "Lora"},{"code": "T12", "id": "jetbrains", "name": "English · JetBrains Mono", "font": "'Atlas JetBrains','Atlas Business',monospace", "language": "en", "category": "常用 · 代码等宽", "embedded": true, "file": "jetbrains", "family": "JetBrains Mono"},{"code": "T13", "id": "excalifont", "name": "English · Excalifont", "font": "'Atlas Excali','Atlas WenKai','Atlas Business',cursive", "language": "en", "category": "趣味 · 手绘白板", "embedded": true, "file": "excalifont", "family": "Excalifont"});
  for(const [code,name,category,file,family] of [['T06','中文 · Noto Sans SC','常用 · 商务清晰','business','Noto Sans SC'],['T05','中文 · Noto Serif SC','常用 · 优雅宋体','elegant','Noto Serif SC'],['T08','中文 · 站酷快乐体','趣味 · 活泼圆体','playful','ZCOOL KuaiLe']])Object.assign(axes.T.items.find(t=>t.code===code),{name,category,file,family,language:'zh'});
  const rows=[
    ['P01','黑白细线','轻量阅读','L01-N01-E01-C01-B01-T01-D02',['xmind','markmap'],'用最少的边界，留下清楚的层次。'],
    ['P02','暖纸阅读','轻量阅读','L02-N05-E01-C02-B02-T02-D02',['mindnode','original'],'暖纸色、书卷文字与柔和卡片。'],
    ['P03','海军蓝商务','专业结构','L03-N08-E02-C03-B08-T01-D02',['xmind','original'],'索引卡片与折线，让职责与分类更整齐。'],
    ['P04','蓝图技术','暗色专注','L02-N02-E02-C08-B05-T03-D01',['mindnode','xmind'],'在暗蓝网格上展开清晰的系统结构。'],
    ['P05','多彩分支','明亮多色','L01-N01-E03-C05-B01-T01-D02',['xmind','mindnode'],'让颜色沿主分支延伸，细节保持轻盈。'],
    ['P06','柔和彩块','明亮多色','L01-N04-E01-C07-B07-T01-D03',['mindnode','mindmeister'],'低饱和色群与圆润形态，适合分享灵感。'],
    ['P07','清透描边','轻量阅读','L01-N02-E01-C08-B01-T01-D02',['mindnode','coggle'],'珊瑚色根节点与青绿色空心节点。'],
    ['P08','自然生长','自然分支','L01-N01-E03-C02-B02-T02-D03',['mindnode','ayoa'],'草木配色，树枝从粗到细自然舒展。'],
    ['P09','石板彩枝','暗色专注','L01-N01-E03-C05-B03-T01-D02',['mindnode','xmind'],'石板灰背景托起明亮分支与浅色中心。'],
    ['P10','黑夜霓虹','暗色专注','L01-N01-E03-C06-B04-T01-D02',['mindnode','ayoa'],'黑色画布、浅色描边中心和发亮彩枝。'],
    ['P11','彩虹方块','明亮多色','L01-N03-E03-C05-B08-T01-D02',['mindnode','mindmeister'],'把颜色装进节点，用实色方块建立分区。'],
    ['P12','暗夜粉彩','暗色专注','L01-N07-E01-C07-B04-T01-D03',['mindnode','original'],'暗底上的粉彩贴片与断续边框。'],
    ['P13','有机灵感','自然分支','L01-N06-E03-C05-B02-T01-D03',['ayoa','coggle'],'保留轻量关键词，让渐细曲枝成为主体。'],
    ['P14','轻盈流线','自然分支','L01-N06-E01-C08-B01-T01-D03',['coggle','mindnode'],'去掉外框，用细曲线串起文字。'],
    ['P15','紧凑知识树','轻量阅读','L02-N01-E01-C05-B01-T01-D01',['markmap','coggle'],'向右阅读、紧凑间距与可折叠文字分支。'],
    ['P16','圆润协作','明亮多色','L01-N04-E01-C08-B08-T01-D02',['mindmeister','mindnode'],'胶囊形节点搭配克制的海盐配色。'],
    ['P17','点阵索引','专业结构','L02-N08-E02-C09-B06-T01-D02',['original','xmind'],'点阵纸上，以分支色条整理工作知识。'],
    ['P18','书页大纲','轻量阅读','L05-N06-E02-C01-B02-T02-D01',['mindmeister','markmap'],'按缩进逐行阅读，深层内容也有清楚的顺序。'],
    ['P19','青绿架构','专业结构','L03-N02-E02-C04-B05-T03-D03',['xmind','mindmeister'],'从上向下展开，轮廓节点强调系统层级。'],
    ['P20','柑橘便笺','明亮多色','L01-N04-E01-C10-B01-T01-D02',['original','mindnode'],'明快的柑橘色群，搭配轻松的圆角形态。'],
    ['P21','折角手记','纸面手作','L02-N09-E07-C09-B06-T02-D02',['original'],'折角纸签、点阵纸与暖色圆角折线。'],
    ['P22','双框书签','编辑排版','L02-N10-E07-C09-B06-T02-D01',['original'],'双线边框配合紧凑阅读，像书页中的知识索引。'],
    ['P23','标签索引','专业结构','L02-N11-E07-C11-B01-T01-D02',['original'],'切口标签与钴蓝层级，清晰整理分类。'],
    ['P24','页眉卡片','专业结构','L03-N12-E07-C03-B08-T01-D02',['original'],'用顶部色带标记分支，以圆角折线连接层级。'],
    ['P25','森林黑板','暗色专注','L01-N01-E03-C07-B09-T02-D03',['original'],'深绿黑板上铺开粉彩枝条与书卷文字。'],
    ['P26','莓果便签','纸面手作','L01-N09-E01-C12-B11-T01-D03',['original'],'浅玫瑰纸上的莓果色折角便签。'],
    ['P27','钴蓝图谱','专业结构','L02-N02-E08-C11-B01-T03-D02',['original'],'双线连接、蓝色轮廓与等宽文字。'],
    ['P28','朱墨书画','编辑排版','L01-N10-E04-C13-B02-T02-D03',['original'],'朱红与墨绿，双框节点搭配利落直线。'],
    ['P29','海湾档案','专业结构','L02-N12-E07-C14-B10-T01-D02',['original'],'米白方格上的页眉卡片，分支呈现海湾色群。'],
    ['P30','夜航轨道','暗色专注','L01-N02-E08-C06-B04-T03-D03',['original'],'深色轮廓节点之间，连接平行的夜光双线。'],
    ['P31','研究卡片','编辑排版','L02-N12-E02-C01-B10-T03-D01',['original'],'单色页眉与紧凑方格，服务于材料梳理。'],
    ['P32','杂志目录','编辑排版','L05-N10-E02-C12-B01-T02-D02',['original'],'双框书签沿缩进展开，构成逐行可读的目录。'],
    ['P33','薄荷标签','明亮多色','L01-N11-E01-C14-B01-T01-D03',['original'],'清新的切口标签，以舒展曲线组织灵感。'],
    ['P34','胶片剪贴','纸面手作','L01-N09-E05-C07-B04-T01-D03',['original'],'暗底粉彩纸签与断续笔触，突出拼贴感。'],
    ['P35','冷静提纲','轻量阅读','L05-N06-E06-C11-B08-T01-D02',['original'],'无框文字与点状导线，逐行梳理长内容。'],
    ['P36','暖调圆线','自然分支','L01-N05-E07-C09-B10-T02-D03',['original'],'暖色卡片与柔和转角，留下舒展阅读空间。']
  ];
  rows.push(["P37", "雅致 · Elegant", "轻量阅读", "L01-N13-E03-C15-B12-T01-D03", ["mindnode", "original"], "Elegant 参考配方：舒展彩枝与轻量文字。"],["P38", "清新 · Fresh", "轻量阅读", "L01-N13-E03-C16-B13-T01-D03", ["mindnode", "original"], "Fresh 参考配方：舒展彩枝与轻量文字。"],["P39", "彩虹经典 · Rainbow (Legacy)", "明亮多色", "L01-N20-E10-C17-B14-T08-D03", ["mindnode", "original"], "Rainbow (Legacy) 参考配方：柔和层级与精细节点边界。"],["P40", "石板经典 · Slate (Legacy)", "暗色专注", "L01-N13-E10-C18-B15-T06-D03", ["mindnode", "original"], "Slate (Legacy) 参考配方：舒展彩枝与轻量文字。"],["P41", "青碧经典 · Teal (Legacy)", "轻量阅读", "L01-N13-E03-C19-B16-T01-D03", ["mindnode", "original"], "Teal (Legacy) 参考配方：舒展彩枝与轻量文字。"],["P42", "冰蓝 · iMac Blue", "明亮多色", "L01-N13-E03-C20-B17-T01-D03", ["mindnode", "original"], "iMac Blue 参考配方：舒展彩枝与轻量文字。"],["P43", "日光黄 · iMac Yellow", "明亮多色", "L01-N13-E03-C21-B18-T01-D03", ["mindnode", "original"], "iMac Yellow 参考配方：舒展彩枝与轻量文字。"],["P44", "薄荷绿 · iMac Green", "明亮多色", "L01-N13-E03-C22-B19-T01-D03", ["mindnode", "original"], "iMac Green 参考配方：舒展彩枝与轻量文字。"],["P45", "樱花粉 · iMac Pink", "明亮多色", "L01-N13-E03-C23-B20-T01-D03", ["mindnode", "original"], "iMac Pink 参考配方：舒展彩枝与轻量文字。"],["P46", "浅藤紫 · iMac Purple", "明亮多色", "L01-N13-E03-C24-B21-T01-D03", ["mindnode", "original"], "iMac Purple 参考配方：舒展彩枝与轻量文字。"],["P47", "杏橙 · iMac Orange", "明亮多色", "L01-N13-E03-C25-B22-T01-D03", ["mindnode", "original"], "iMac Orange 参考配方：舒展彩枝与轻量文字。"],["P48", "自然 · Natural", "轻量阅读", "L01-N13-E10-C26-B23-T05-D03", ["mindnode", "original"], "Natural 参考配方：舒展彩枝与轻量文字。"],["P49", "柔色夜幕 · Pale", "暗色专注", "L01-N13-E03-C27-B24-T01-D03", ["mindnode", "original"], "Pale 参考配方：舒展彩枝与轻量文字。"],["P50", "怡然 · Pleasant", "轻量阅读", "L01-N13-E03-C28-B25-T01-D03", ["mindnode", "original"], "Pleasant 参考配方：舒展彩枝与轻量文字。"],["P51", "微型图形 · Small Graphics", "明亮多色", "L01-N14-E01-C29-B26-T01-D03", ["mindnode", "original"], "Small Graphics 参考配方：柔和层级与精细节点边界。"],["P52", "远景 · Vision", "轻量阅读", "L01-N13-E03-C30-B27-T01-D03", ["mindnode", "original"], "Vision 参考配方：舒展彩枝与轻量文字。"],["P53", "纯黑 · Black", "暗色专注", "L01-N13-E10-C31-B28-T08-D03", ["mindnode", "original"], "Black 参考配方：舒展彩枝与轻量文字。"],["P54", "经典 · Classic", "轻量阅读", "L01-N13-E03-C32-B29-T01-D03", ["mindnode", "original"], "Classic 参考配方：舒展彩枝与轻量文字。"],["P55", "现代 · Modern", "轻量阅读", "L01-N13-E03-C33-B30-T01-D03", ["mindnode", "original"], "Modern 参考配方：舒展彩枝与轻量文字。"],["P56", "灵感沙盒 · Idea Sandbox", "轻量阅读", "L01-N13-E03-C34-B31-T01-D03", ["mindnode", "original"], "Idea Sandbox 参考配方：舒展彩枝与轻量文字。"],["P57", "热可可 · Hot Cocoa", "暗色专注", "L01-N13-E03-C35-B32-T02-D03", ["mindnode", "original"], "Hot Cocoa 参考配方：舒展彩枝与轻量文字。"],["P58", "悦色 · Delight", "轻量阅读", "L01-N13-E03-C36-B33-T01-D03", ["mindnode", "original"], "Delight 参考配方：舒展彩枝与轻量文字。"],["P59", "卡布奇诺 · Cappuccino", "轻量阅读", "L01-N13-E03-C37-B34-T02-D03", ["mindnode", "original"], "Cappuccino 参考配方：舒展彩枝与轻量文字。"],["P60", "暗夜粉彩 · Goth Pastel", "暗色专注", "L01-N21-E01-C38-B35-T08-D03", ["mindnode", "original"], "Goth Pastel 参考配方：柔和层级与精细节点边界。"],["P61", "极简 · Minimalist", "轻量阅读", "L01-N19-E01-C39-B36-T06-D03", ["mindnode", "original"], "Minimalist 参考配方：柔和层级与精细节点边界。"],["P62", "路线图 · Roadmap", "轻量阅读", "L01-N15-E01-C40-B37-T01-D03", ["mindnode", "original"], "Roadmap 参考配方：柔和层级与精细节点边界。"],["P63", "冬日 · Winter Day", "明亮多色", "L01-N14-E01-C41-B38-T01-D03", ["mindnode", "original"], "Winter Day 参考配方：柔和层级与精细节点边界。"],["P64", "冬夜 · Winter Night", "轻量阅读", "L01-N13-E03-C42-B39-T01-D03", ["mindnode", "original"], "Winter Night 参考配方：舒展彩枝与轻量文字。"]);
  rows.push(["P65", "随手画画", "手绘趣味", "L01-N16-E09-C43-B40-T04-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P66", "彩笔脑洞", "手绘趣味", "L01-N17-E09-C44-B01-T04-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P67", "脑洞涂鸦", "手绘趣味", "L02-N18-E09-C43-B41-T04-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P68", "浮生小趣", "手绘趣味", "L01-N16-E09-C45-B42-T04-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P69", "白板讨论", "手绘趣味", "L02-N16-E09-C01-B01-T01-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P70", "圈住好点子", "手绘趣味", "L01-N17-E09-C43-B40-T01-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P71", "荧光备忘", "手绘趣味", "L01-N18-E09-C44-B40-T01-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"],["P72", "竖向涂鸦", "手绘趣味", "L03-N16-E09-C44-B41-T04-D03", ["excalidraw", "xmind", "original"], "略带起伏的笔触、轻松的留白与清晰的文字。"]);
  for(const [id,font] of Object.entries({P61:'T06',P48:'T05',P40:'T10',P39:'T11',P60:'T08',P65:'T09',P67:'T12',P68:'T13'})){const row=rows.find(r=>r[0]===id),parts=row[3].split('-');parts[5]=font;row[3]=parts.join('-');}
  sources.push({id:'miro',name:'Miro',url:'https://miro.com/templates/mind-maps/?page=1',feature:'模板累计复制量提供用途信号，转化为商务、便签、项目与分组的原创配方。'},{id:'processon',name:'ProcessOn',url:'https://www.processon.com/template/all/cc',feature:'克隆最多入口中的正式风格、学习提纲与组织架构作为补充参考；未获取具体复制量。'});
  rows.push(["P73", "商务蓝图", "专业结构", "L02-N19-E07-C03-B36-T06-D02", ["miro", "processon", "original"], "白底蓝线，清楚整理业务层次与汇报要点。"],["P74", "知识提纲", "清晰阅读", "L05-N06-E02-C39-B40-T05-D01", ["miro", "mindmeister", "original"], "无框文字与紧凑缩进，让长内容按阅读顺序展开。"],["P75", "组织分层", "专业结构", "L03-N20-E02-C03-B36-T10-D02", ["miro", "processon", "original"], "自上而下的实色层级，用于分类、职责和模块拆解。"],["P76", "便签共创", "手绘趣味", "L01-N16-E04-C38-B40-T08-D03", ["miro", "excalidraw", "original"], "粉彩便签、手绘轮廓与直线，适合发散想法。"],["P77", "概念分组", "专业结构", "L02-N19-E04-C26-B23-T11-D02", ["miro", "original"], "细框与直线减少装饰，逐层比较概念与依据。"],["P78", "项目分解", "专业结构", "L03-N19-E07-C39-B14-T12-D02", ["miro", "xmind", "original"], "向下展开的圆角折线，把项目要点拆成可读层级。"],["P79", "语义索引", "清晰阅读", "L05-N13-E02-C26-B23-T09-D01", ["miro", "markmap", "original"], "文字彩线与缩进索引，用于学习材料和主题梳理。"],["P80", "彩色研讨", "明亮多色", "L04-N20-E01-C17-B36-T13-D02", ["miro", "xmind", "original"], "用彩色分类和括号归组，整理讨论中的不同视角。"]);
  const provenance={
    N01:['markmap','coggle','xmind'],N02:['mindnode','mindmeister'],N03:['mindnode','mindmeister'],N04:['mindnode','mindmeister'],N05:['original','mindnode'],N06:['coggle','ayoa'],N07:['mindnode','original'],N08:['original','xmind'],
    E01:['coggle','mindnode'],E02:['xmind','mindmeister'],E03:['ayoa','mindnode'],E04:['xmind'],E05:['original'],E06:['original'],
    C01:['original'],C02:['mindnode'],C03:['original','xmind'],C04:['original'],C05:['xmind','mindnode'],C06:['mindnode'],C07:['mindnode'],C08:['original','mindnode'],C09:['original'],C10:['original'],
    L01:['xmind','mindnode','mindmeister'],L02:['xmind','markmap'],L03:['xmind','mindmeister'],L04:['xmind'],L05:['mindmeister'],
    B01:['original'],B02:['original'],B03:['mindnode'],B04:['mindnode'],B05:['original'],B06:['original'],B07:['original'],B08:['original']
  };
  Object.values(axes).forEach(axis=>axis.items.forEach(item=>{item.sourceIds=provenance[item.code]||((item.code[0]==='C'&&Number(item.code.slice(1))>=15)||(item.code[0]==='B'&&Number(item.code.slice(1))>=12)||(item.code[0]==='N'&&Number(item.code.slice(1))>=13)?['mindnode','original']:['original']);}));
  for(const code of ['N16','N17','N18','E09','C43','C44','C45','B40','B41','B42','T04']){const item=axes[code[0]].items.find(x=>x.code===code);item.sourceIds=['excalidraw','original'];}
  const presets=rows.map(([id,name,family,code,sourceIds,description])=>({id,name,family,code,sourceIds,description,referenceTheme:Number(id.slice(1))>=37?{"P37": "Elegant", "P38": "Fresh", "P39": "Rainbow (Legacy)", "P40": "Slate (Legacy)", "P41": "Teal (Legacy)", "P42": "iMac Blue", "P43": "iMac Yellow", "P44": "iMac Green", "P45": "iMac Pink", "P46": "iMac Purple", "P47": "iMac Orange", "P48": "Natural", "P49": "Pale", "P50": "Pleasant", "P51": "Small Graphics", "P52": "Vision", "P53": "Black", "P54": "Classic", "P55": "Modern", "P56": "Idea Sandbox", "P57": "Hot Cocoa", "P58": "Delight", "P59": "Cappuccino", "P60": "Goth Pastel", "P61": "Minimalist", "P62": "Roadmap", "P63": "Winter Day", "P64": "Winter Night"}[id]:null,collection:Number(id.slice(1))>=21?'新增':'经典'}));
  const usageEvidence={"P73": {"reference": "Business Mindmap", "copies": "5.3K", "likes": "865", "url": "https://miro.com/templates/business-mindmap/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P74": {"reference": "Mindmapping", "copies": "2.4K", "likes": "384", "url": "https://miro.com/templates/atlassian-mindmapping/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P75": {"reference": "Business Plan Mind Map Template", "copies": "1.6K", "likes": "30", "url": "https://miro.com/templates/business-plan-mind-map/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P76": {"reference": "Brainwriting Template", "copies": "875", "likes": "23", "url": "https://miro.com/templates/brainwriting-basic/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P77": {"reference": "Concept Map Template", "copies": "4.7K", "likes": "35", "url": "https://miro.com/templates/concept-map-basic/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P78": {"reference": "Project Planning Mind Map", "copies": "989", "likes": "12", "url": "https://miro.com/templates/project-planning-mind-map/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P79": {"reference": "Semantic Map Template", "copies": "3.7K", "likes": "22", "url": "https://miro.com/templates/semantic-map/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}, "P80": {"reference": "Six Thinking Hats Mind Map", "copies": "938", "likes": "18", "url": "https://miro.com/templates/six-thinking-hats-mind-map-by-aryanna-martin/", "retrieved": "2026-10-20", "metric": "cumulative template copies; not style usage"}};
  presets.forEach(p=>{if(usageEvidence[p.id])p.usageEvidence=usageEvidence[p.id];});
  const journal=presets.find(p=>p.id==='P67');journal.code=journal.code.replace(/^L02-/,'L01-').replace('-B41-','-B40-');journal.name='脑洞涂鸦';journal.description='32枚原创笔触，豆芽搭子与纸片陪你把脑洞画出来。';
  const signatureDescriptions={
    P61:'通透圆角与海盐色细线，把重点留给想法。',
    P48:'奶油色中心与舒展彩枝，像一段慢慢生长的思路。',
    P40:'沉静石板底色托起明亮彩枝，适合专注构思。',
    P39:'轻快的实色卡片，主次分明，也保留一点热情。',
    P60:'柔软粉彩与手作缝边，在深色画布上轻轻发光。',
    P65:'纸色、细墨线与一笔橙色，留住随手画下的想法。',
    P68:'蓝灰纸面、暖灰小毛驴与一笔杏色，把生活里的小心思轻轻画出来。',
    P73:'白底、蓝线与从容留白，让复杂业务有清楚的层次。',
    P74:'像一本排版清爽的笔记，用分节与缩进梳理长内容。',
    P75:'深蓝主干与轻色子层，清楚看见组织与职责的归属。',
    P76:'柔彩便签与小段纸胶带，让每一个点子都有落脚处。',
    P77:'自然色细框串起概念，在层层展开中比较与理解。',
    P78:'圆角折线与清晰索引，把一个项目分解成下一步。',
    P79:'文楷、彩色页标与轻导线，让知识读起来有节奏。',
    P80:'用明亮色块和轻巧括号，收拢讨论里的不同视角。'
  };
  presets.forEach(p=>{if(signatureDescriptions[p.id])p.description=signatureDescriptions[p.id];});
  const recommendations={"reviewedAt":"2026-10-20","basis":"近期官方产品动向、公开模板用途与本产品任务适配；人工精选，不是用户使用率排名。","items":[{"preset":"P61","scenario":"资料速读","badge":"上手首选","reason":"左右展开、清晰细框与舒展留白，适合先看懂资料或已有 AI 笔记的主张与依据。","signals":["xmind-2026-ai","miro-template-library"]},{"preset":"P74","scenario":"长文精读","badge":"阅读推荐","reason":"缩进大纲、无框文字与紧凑分节，适合长文、研究资料和多层笔记的逐层回看。","signals":["xmind-2026-ai","mindmapai-2026-workflows"]},{"preset":"P40","scenario":"代码理解","badge":"技术推荐","reason":"石板底色配明亮分支，帮助看清已有代码笔记中的入口、业务和数据层。","signals":["mindmapai-2026-workflows"]},{"preset":"P73","scenario":"业务汇报","badge":"工作推荐","reason":"向右展开、蓝色细框与圆角折线，适合按现状、原因和行动讲清业务。","signals":["miro-template-library"]},{"preset":"P78","scenario":"项目规划","badge":"执行推荐","reason":"向下层级与圆角连接，把目标拆成范围、制作和交付等工作项。","signals":["miro-template-library"]},{"preset":"P65","scenario":"写作草稿","badge":"表达推荐","reason":"手绘纸面与文楷，让零散想法先形成主张、例子与收尾。","signals":["xmind-2026-consulting"]},{"preset":"P67","scenario":"自由脑洞","badge":"趣味推荐","reason":"原创小搭子、纸片和圈注，适合自由联想，再逐步收拢可尝试的点子。","signals":["xmind-2026-ai"]},{"preset":"P76","scenario":"点子收集","badge":"构思推荐","reason":"柔彩便签与直线连接，让不同方向的点子各有位置，方便归类回看。","signals":["miro-template-library"]}],"signals":[{"id":"xmind-2026-ai","url":"https://xmind.com/whats-new","date":"2026-06-11","type":"official product update","observation":"新版AI支持资料、网页与文件上下文，并可重组分支；代表产品投入方向，不代表采用率。"},{"id":"mindmapai-2026-workflows","url":"https://mindmapai.app/blog/","date":"2026-09","type":"official tutorial topics","observation":"官网近期教程覆盖Notion资料、代码库与Codex、会议笔记；教程选题不等于用户使用量。"},{"id":"miro-template-library","url":"https://miro.com/templates/mind-maps/?page=1","date":null,"type":"official template catalogue","observation":"模板覆盖业务、计划、概念梳理与头脑风暴；常设用途不当作近期增长趋势。"},{"id":"xmind-2026-consulting","url":"https://xmind.com/user-stories/how-to-use-mind-mapping-to-navigate-complexity","date":"2026-01-22","type":"official user story","observation":"案例提及咨询、写作与研究论证；单一案例不外推人群规模。"}]};
  const tasks=[{"id":"read","name":"阅读学习","prompt":"我想看懂一份资料","hint":"文章 · 书籍 · 研究笔记","start":"P61","pick":"文章先选极简，长文试试知识提纲"},{"id":"work","name":"工作规划","prompt":"我想理清一件工作","hint":"业务 · 项目 · 代码文档","start":"P73","pick":"业务先选商务蓝图，代码试试石板经典"},{"id":"write","name":"写作表达","prompt":"我想把观点讲清楚","hint":"写作 · 选题 · 演示提纲","start":"P65","pick":"草稿先选随手画画，讲解试试概念分组"},{"id":"idea","name":"灵感构思","prompt":"我想让点子冒出来","hint":"脑洞 · 教学 · 观点收集","start":"P67","pick":"自由构思先选脑洞涂鸦，收集试试便签共创"}];
  const positioning={"P61":{"task":"read","useCase":"文章速读","outcome":"抓住主张与依据","intent":"通透细框突出主次，先看懂一篇文章的骨架。","audience":"读者 · 分析师","specimens":{"zh":"```mermaid\nmindmap\n  root((文章速读))\n    核心主张\n      作者观点\n      适用条件\n    论证依据\n      关键事实\n      证据边界\n    我的判断\n      待查问题\n      行动启发\n```","en":"```mermaid\nmindmap\n  root((Quick read))\n    Main claim\n      Argument\n      Conditions\n    Evidence\n      Key facts\n      Limits\n    My take\n      Open question\n      Next action\n```"}},"P48":{"task":"read","useCase":"读书消化","outcome":"把章节连成理解","intent":"书卷字形与自然彩枝，把章节知识连成自己的理解。","audience":"读书者 · 学习者","specimens":{"zh":"```mermaid\nmindmap\n  root((读书笔记))\n    核心概念\n      一句解释\n      关联知识\n    章节脉络\n      关键转折\n      作者论证\n    实践启发\n      今天试试\n      复盘问题\n```","en":"```mermaid\nmindmap\n  root((Book notes))\n    Core idea\n      Definition\n      Connections\n    Chapter arc\n      Turning point\n      Argument\n    Apply it\n      Small step\n      Review\n```"}},"P40":{"task":"work","useCase":"代码理解","outcome":"看清模块与职责","intent":"沉静石板配明亮分支，专注看清代码中的模块归属。","audience":"开发者 · 技术写作者","specimens":{"zh":"```mermaid\nmindmap\n  root((代码导览))\n    入口层\n      接收请求\n      输入校验\n    业务层\n      处理规则\n      业务用例\n    数据层\n      读写存储\n      数据模型\n```","en":"```mermaid\nmindmap\n  root((Code map))\n    Entry layer\n      Requests\n      Input checks\n    Domain layer\n      Rules\n      Use cases\n    Data layer\n      Storage\n      Data models\n```"}},"P39":{"task":"write","useCase":"演示提纲","outcome":"让观众跟上逻辑","intent":"鲜明卡片分隔论点，适合分享前整理讲述顺序。","audience":"讲述者 · 内容创作者","specimens":{"zh":"```mermaid\nmindmap\n  root((分享提纲))\n    提出问题\n      真实困惑\n      为何现在\n    给出观点\n      关键理由\n      支持证据\n    走向行动\n      下一步\n      带走什么\n```","en":"```mermaid\nmindmap\n  root((Talk outline))\n    The question\n      Pain point\n      Why now\n    Our insight\n      Key reason\n      Evidence\n    Take action\n      Next step\n      Takeaway\n```"}},"P60":{"task":"write","useCase":"选题孵化","outcome":"为选题找到角度","intent":"暗底粉彩区分创作方向，留住有辨识度的选题。","audience":"创作者 · 策划","specimens":{"zh":"```mermaid\nmindmap\n  root((选题孵化))\n    读者关心\n      一个困惑\n      真实场景\n    独特角度\n      亲身观察\n      新的问题\n    表达形式\n      故事开场\n      标题尝试\n```","en":"```mermaid\nmindmap\n  root((Story seeds))\n    Audience\n      A question\n      Context\n    Fresh angle\n      Observation\n      New question\n    Format\n      Opening\n      Headline\n```"}},"P65":{"task":"write","useCase":"写作草稿","outcome":"先把想法写松一点","intent":"纸色与细墨线容纳未完成的思路，适合打磨第一稿。","audience":"写作者 · 笔记者","specimens":{"zh":"```mermaid\nmindmap\n  root((写作草稿))\n    想说什么\n      核心句子\n      读者问题\n    怎么说明\n      一个例子\n      一条证据\n    如何收尾\n      读者行动\n      留个问题\n```","en":"```mermaid\nmindmap\n  root((First draft))\n    Main point\n      One sentence\n      Reader need\n    Explain it\n      An example\n      Evidence\n    Close it\n      Reader action\n      Open question\n```"}},"P67":{"task":"idea","useCase":"自由脑洞","outcome":"边画边想，不急着定论","intent":"32枚趣味笔触，小搭子与纸片陪你自由发散，再慢慢收拢。","audience":"自由构思者 · 创作者","specimens":{"zh":"```mermaid\nmindmap\n  root((脑洞游乐场))\n    如果反过来\n      试个反例\n      想个例外\n    奇怪的联想\n      两个点子\n      画条联系\n    马上试一笔\n      小小实验\n      再试一次\n```","en":"```mermaid\nmindmap\n  root((Idea playground))\n    What if\n      Reverse it\n      An exception\n    Odd link\n      Mix two ideas\n      Draw a link\n    Try it\n      Tiny experiment\n      Try again\n```"}},"P68":{"task":"idea","useCase":"生活随想","outcome":"把现实想得轻巧一点","intent":"8个小毛驴与8枚纸笺记号，陪你梳理工作、求职和AI时代的小心思。","audience":"打工人 · 求职者 · 日常记录者","specimens":{"zh":"```mermaid\nmindmap\n  root((把日子想得轻巧一点))\n    工作里的分寸\n      借力不丢方向\n      帮忙也留边界\n    前路的期待\n      继续试一小步\n      等一个懂的人\n    留给自己的\n      生活的小园子\n      今天的小收获\n```","en":"```mermaid\nmindmap\n  root((A little lighter))\n    Work with care\n      Use help wisely\n      Keep boundaries\n    A little hope\n      Try one step\n      Find your people\n    Room for life\n      Keep a garden\n      Notice small joys\n```"}},"P73":{"task":"work","useCase":"业务汇报","outcome":"把判断讲清楚","intent":"蓝线、白底与顺向层级，让业务结论和行动清楚落位。","audience":"产品 · 运营 · 顾问","specimens":{"zh":"```mermaid\nmindmap\n  root((业务复盘))\n    现状判断\n      观察信号\n      用户变化\n    关键原因\n      主要阻力\n      影响范围\n    下一步\n      验证方向\n      负责人选\n```","en":"```mermaid\nmindmap\n  root((Business review))\n    Current state\n      Signals\n      User shift\n    Root cause\n      Main blocker\n      Impact\n    Next move\n      Validate\n      Owner\n```"}},"P74":{"task":"read","useCase":"长文精读","outcome":"沿着论证逐层读","intent":"紧凑分节与无框文字，适合长文逐层阅读和回看。","audience":"研究者 · 深度读者","specimens":{"zh":"```mermaid\nmindmap\n  root((长文精读))\n    问题背景\n      研究范围\n      已有共识\n    论证过程\n      证据边界\n      反向证据\n    结论回看\n      我的疑问\n      待查来源\n```","en":"```mermaid\nmindmap\n  root((Deep reading))\n    Context\n      Scope\n      Consensus\n    Argument\n      Evidence limits\n      Counterpoint\n    Review\n      Questions\n      Sources\n```"}},"P75":{"task":"work","useCase":"职责梳理","outcome":"分清谁负责哪一层","intent":"自上而下的色块层级，突出团队职责与归属。","audience":"项目负责人 · 管理者","specimens":{"zh":"```mermaid\nmindmap\n  root((职责分层))\n    产品方向\n      需求梳理\n      方向规划\n    交付实现\n      开发测试\n      质量把关\n    运营支持\n      上线反馈\n      答疑支持\n```","en":"```mermaid\nmindmap\n  root((Team roles))\n    Product\n      Discovery\n      Roadmap\n    Delivery\n      Build and test\n      Quality\n    Operations\n      Feedback\n      Support\n```"}},"P76":{"task":"idea","useCase":"点子收集","outcome":"每个点子都有位置","intent":"柔彩便签保留平等的表达空间，用来收拢零散想法。","audience":"策划 · 设计师","specimens":{"zh":"```mermaid\nmindmap\n  root((点子收集))\n    用户愿望\n      更省一步\n      意外惊喜\n    意外点子\n      换个入口\n      新的组合\n    可行尝试\n      快速验证\n      留下疑问\n```","en":"```mermaid\nmindmap\n  root((Idea board))\n    User wish\n      Less effort\n      Delight\n    Wild idea\n      New entry\n      Remix\n    Small bet\n      Quick check\n      Question\n```"}},"P77":{"task":"write","useCase":"概念讲解","outcome":"讲清概念与例子","intent":"自然色细框按层拆开定义和例子，辅助清楚表达。","audience":"作者 · 讲师 · 分析师","specimens":{"zh":"```mermaid\nmindmap\n  root((概念讲解))\n    它是什么\n      一句定义\n      常见误解\n    如何区分\n      边界条件\n      一个反例\n    怎样应用\n      一个实例\n      练习一次\n```","en":"```mermaid\nmindmap\n  root((Explain a concept))\n    Definition\n      Plain words\n      Not this\n    Distinction\n      Boundaries\n      Counterexample\n    Application\n      Example\n      Practice\n```"}},"P78":{"task":"work","useCase":"项目拆解","outcome":"把目标拆成可做的事","intent":"圆角折线连接交付层级，把目标拆成清楚的工作项。","audience":"产品经理 · 项目负责人","specimens":{"zh":"```mermaid\nmindmap\n  root((上线计划))\n    项目范围\n      交付目标\n      范围边界\n    制作阶段\n      原型验证\n      质量评审\n    上线交付\n      发布清单\n      用户反馈\n```","en":"```mermaid\nmindmap\n  root((Launch plan))\n    Scope\n      Goals\n      Boundaries\n    Build\n      Prototype\n      Review\n    Release\n      Checklist\n      Feedback\n```"}},"P79":{"task":"read","useCase":"知识复习","outcome":"按线索找回记忆","intent":"文楷与彩色页标保留索引节奏，适合复习和查找。","audience":"学习者 · 知识整理者","specimens":{"zh":"```mermaid\nmindmap\n  root((知识索引))\n    概念卡片\n      一句回忆\n      关联条目\n    容易混淆\n      区别要点\n      反例提醒\n    应用场景\n      例题线索\n      复习问题\n```","en":"```mermaid\nmindmap\n  root((Knowledge index))\n    Core terms\n      Recall\n      Related terms\n    Confusions\n      Distinctions\n      Counterexample\n    Use cases\n      Practice\n      Quiz\n```"}},"P80":{"task":"idea","useCase":"观点归类","outcome":"让不同意见各就各位","intent":"明亮色块与结构括号，把讨论观点按主题归组。","audience":"组织者 · 讨论参与者","specimens":{"zh":"```mermaid\nmindmap\n  root((讨论归类))\n    已知事实\n      已有信息\n      尚待确认\n    可行方案\n      新想法\n      替代路径\n    主要顾虑\n      未解风险\n      取舍条件\n```","en":"```mermaid\nmindmap\n  root((Discussion map))\n    Facts\n      Known data\n      Unknowns\n    Options\n      New ideas\n      Alternatives\n    Concerns\n      Open risks\n      Tradeoffs\n```"}}};
  const alternatives={P61:['P48','P74'],P48:['P61','P79'],P74:['P61','P79'],P79:['P48','P74'],P40:['P73','P78'],P73:['P78','P75'],P75:['P78','P73'],P78:['P73','P75'],P39:['P77','P65'],P60:['P65','P39'],P65:['P77','P60'],P77:['P39','P65'],P67:['P76','P68'],P68:['P67','P80'],P76:['P67','P80'],P80:['P76','P68']};
  presets.forEach(p=>{if(positioning[p.id]){p.positioning={...positioning[p.id],alternatives:alternatives[p.id]};p.description=p.positioning.intent;}});
  // Deep examples keep the original task and add explicit checks, rather than more templates.
  const depthDetails={
    read:{zh:['核对原文依据','回看上下文','保留适用范围'],en:['Check the evidence','Read its context','Keep the scope']},
    work:{zh:['明确验收条件','核对前置依赖','安排一次验证'],en:['Set acceptance criteria','Check dependencies','Plan a verification']},
    write:{zh:['补充具体例子','核实材料出处','收紧表达范围'],en:['Add a concrete example','Verify its source','Refine the claim']},
    idea:{zh:['试一个小方案','记录实际反馈','调整下一步'],en:['Try a small version','Record feedback','Adjust the next step']}
  };
  presets.forEach(p=>{if(!p.positioning)return;p.positioning.depthSpecimens={};for(const lang of ['zh','en']){
    const lines=p.positioning.specimens[lang].split('\n'),at=lines.findIndex(line=>/^      \S/.test(line));
    const extra=depthDetails[p.positioning.task][lang].map((label,i)=>'  '.repeat(i+4)+label);
    p.positioning.depthSpecimens[lang]=[...lines.slice(0,at+1),...extra,...lines.slice(at+1)].join('\n');
  }});
  axes.C.items.find(c=>c.code==='C43').mark='#e57446';
  const legacy={ink:'P01',paper:'P02',business:'P03',blueprint:'P04',spectrum:'P05',pastel:'P06'};
  const order=['L','N','E','C','B','T','D'];
  // Append-only public identities: never derive these from menu order or recycle them.
  const styleUIDs=Object.freeze({MMK0V1:'P61',MMR0C2:'P48',MMT0H3:'P40',MMB0Q4:'P39',MMW0F5:'P60',MMD0N6:'P65',MMP0A7:'P67',MMH0S8:'P68',MMC0Y9:'P73',MMV0EA:'P74',MMF0KB:'P75',MMQ0DC:'P76',MMN0WD:'P77',MMA0RE:'P78',MMS0BF:'P79',MME0TG:'P80'});
  for(const [uid,id] of Object.entries(styleUIDs)){
    const preset=presets.find(p=>p.id===id);
    if(!/^MM[A-Z][0-9A-Z][A-Z][0-9A-Z]$/.test(uid)||!preset||preset.uid)throw new Error('Invalid style UID registry: '+uid);
    preset.uid=uid;
  }
  function resolvePreset(value){
    const text=String(value).normalize('NFKC').trim().toUpperCase();
    const identity=presets.find(p=>p.id===text||p.uid===text);if(identity)return identity;
    const byName=[...presets.filter(p=>p.uid),...presets.filter(p=>!p.uid)];
    return byName.find(p=>[p.name,...p.name.split(' · '),...(p.uid?[p.uid+' · '+p.name.split(' · ')[0]]:[]),p.id+' · '+p.name.split(' · ')[0]].some(name=>name.toUpperCase()===text))||null;
  }
  function resolveRecipe(value){
    let text=String(value||'P07').trim().toUpperCase();
    if(['粉笔夜谈','P68 · 粉笔夜谈','MMH0S8 · 粉笔夜谈'].includes(text))text='P68';
    const preset=resolvePreset(text);
    const parts=(preset?preset.code:text).split('-');
    if(parts.length!==order.length)throw new Error(`请输入样式 UID（如 MMK0V1）、名称或完整的 L-N-E-C-B-T-D 组合代号；旧 P 代号仍可使用。`);
    const tokens={};
    order.forEach((axis,index)=>{
      const item=axes[axis].items.find(i=>i.code===parts[index]);
      if(!item)throw new Error(`${axes[axis].name}代号无效：${parts[index]}。`);
      tokens[axis]=item;
    });
    if(!allowedEdges(tokens.L.id).includes(tokens.E.code))throw new Error(`${tokens.L.name}保留其结构连线，请选择 ${allowedEdges(tokens.L.id).join('、')}。`);
    const code=order.map(k=>tokens[k].code).join('-');
    const match=presets.find(p=>p.code===code);
    return {code,tokens,preset:match||null};
  }
  function allowedEdges(layout){return layout==='brace'?['E01','E05','E06']:layout==='outline'?['E02','E05','E06']:axes.E.items.map(i=>i.code);}
  function edgeLabel(layout,code){
    const labels={brace:{E01:'实线括号',E05:'断续括号',E06:'点状括号'},outline:{E02:'提纲折线',E05:'断续导线',E06:'点状导线'}};
    return labels[layout]?.[code]||axes.E.items.find(e=>e.code===code)?.name||code;
  }
  function replaceToken(recipe,axis,value){
    if(!order.includes(axis))throw new Error('未知样式维度');
    const codes=order.map(k=>k===axis?value:recipe.tokens[k].code);
    const layout=axes.L.items.find(l=>l.code===codes[0]);
    if(!layout)throw new Error('未知布局');
    const validEdges=allowedEdges(layout.id);
    if(!validEdges.includes(codes[2]))codes[2]=validEdges[0];
    return resolveRecipe(codes.join('-'));
  }
  function luminance(hex){
    const rgb=hex.replace('#','').match(/../g).map(x=>parseInt(x,16)/255).map(v=>v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4));
    return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;
  }
  function contrast(a,b){const x=luminance(a),y=luminance(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
  function readableText(bg){const best=contrast(bg,'#18242b')>=contrast(bg,'#ffffff')?'#18242b':'#ffffff';return contrast(bg,best)>=4.5?best:'#000000';}
  function mix(a,b,ratio){
    const rgb=h=>h.slice(1).match(/../g).map(s=>parseInt(s,16));const x=rgb(a),y=rgb(b);
    return '#'+x.map((v,i)=>Math.round(v*(1-ratio)+y[i]*ratio).toString(16).padStart(2,'0')).join('');
  }
  function themeFor(recipe){
    const {N,E,C,B,T,D}=recipe.tokens;
    const fusheng=N.code==='N16'&&C.code==='C45'&&B.code==='B42';
    return {id:recipe.code,name:recipe.preset?.name||'自定义配方',...(fusheng?{family:'fusheng'}:{}),bg:B.bg,ink:contrast(B.bg,B.ink)>=4.5?B.ink:readableText(B.bg),surface:B.surface,dark:B.dark,root:B.rootFill||C.accent,rootText:B.rootInk||readableText(C.accent),rootStroke:B.rootStroke||C.accent,palette:C.colors,accent:C.accent,node:N.id,line:E.id,canvas:B,font:T.font,density:{...D,...(fusheng?{rowGap:D.code==='D03'?62:D.code==='D02'?34:14,rootMinHeight:68,nodeMinHeight:50}:{}),...(recipe.tokens.L.id==='outline'?{sectionGap:10}:{}),...(N.id==='marker'?{rootMinWidth:220,rootMinHeight:100,nodeMinHeight:60,rootPadding:56}:{}),...(['capsule-outline','colorblock','pastel-patch'].includes(N.id)?{rootMinWidth:140,rootMinHeight:66,nodeMinWidth:90,nodeMinHeight:46}:{})},recipe};
  }
  const selection={"presets": ["P61", "P48", "P40", "P39", "P60", "P65", "P67", "P68", "P73", "P74", "P75", "P76", "P77", "P78", "P79", "P80"], "axes": {"L": ["L01", "L02", "L03", "L04", "L05"], "N": ["N06", "N13", "N19", "N20", "N21", "N16", "N18"], "E": ["E01", "E02", "E04", "E07", "E09", "E10"], "C": ["C03", "C17", "C18", "C26", "C38", "C39", "C43", "C45"], "B": ["B36", "B23", "B15", "B14", "B35", "B40", "B41", "B42"], "T": ["T06", "T05", "T09", "T08", "T10", "T11", "T12", "T13"], "D": ["D01", "D02", "D03"]}};
  selection.presetLimit=16;selection.componentLimit=8;
  function selectedItems(axis,current){
    const list=selection.axes[axis].map(code=>axes[axis].items.find(item=>item.code===code));
    if(current&&!list.some(item=>item.code===current)){const old=axes[axis].items.find(item=>item.code===current);if(old){if(list.length===8)list.pop();list.push(old);}}
    return list;
  }
  function selectedPresets(){return selection.presets.map(id=>presets.find(p=>p.id===id));}
  function pencilBox(x,y,w,h,seed=0,pass=0){
    const jitter=i=>Math.sin((seed+1)*12.9898+i*7.233+pass*4.37)*1.35;
    const a=jitter(1),b=jitter(2),c=jitter(3),d=jitter(4),o=pass*.65;
    return `M${x+4+o},${y+a+o}Q${x+w*.5},${y+b-1} ${x+w-3},${y+o}Q${x+w+c},${y+2} ${x+w+o},${y+5}Q${x+w+d},${y+h*.5} ${x+w-1},${y+h-3}Q${x+w},${y+h+o} ${x+w-5},${y+h+o}Q${x+w*.5},${y+h+c+1} ${x+3},${y+h}Q${x-1},${y+h} ${x+o},${y+h-5}Q${x+a-1},${y+h*.5} ${x},${y+4}Q${x},${y} ${x+4+o},${y+a+o}Z`;
  }
  function pencilCurve(x1,y1,x2,y2,vertical,seed=0,pass=0){
    const j=Math.sin(seed*7.23+pass*4.71)*3,o=pass*.9;
    if(vertical){const m=(y1+y2)/2;return `M${x1},${y1}C${x1+j+o},${m} ${x2-j-o},${m} ${x2},${y2}`;}
    const m=(x1+x2)/2;return `M${x1},${y1}C${m},${y1+j+o} ${m},${y2-j-o} ${x2},${y2}`;
  }
  const api={styleUIDs,resolvePreset,recommendations,tasks,selection,selectedItems,selectedPresets,pencilBox,pencilCurve,version:1,axes,order,presets,sources,legacy,resolveRecipe,replaceToken,allowedEdges,edgeLabel,themeFor,contrast,readableText,mix};
  if(typeof module!=='undefined')module.exports=api;else scope.StyleLibrary=api;
})(typeof globalThis!=='undefined'?globalThis:this);
