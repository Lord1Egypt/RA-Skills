#!/usr/bin/env node

const carriers = [
  {
    id: "deppon",
    name: "德邦快递",
    aliases: ["deppon", "debang", "德邦", "德邦物流"],
    hotline: "95353",
    serviceHours: "官网可见 24 小时客服公告，仍以当期官网公告为准",
    channels: ["官网", "App", "热线"],
    useCases: ["大件快递", "物流异常", "投诉反馈", "查件催件"],
    website: "https://www.deppon.com/",
    notes: ["大件件型场景较常见", "破损和送货上楼争议要尽早留证"],
  },
  {
    id: "ems",
    name: "中国邮政 EMS",
    aliases: ["ems", "邮政", "邮政快递", "中国邮政", "邮政速递", "中国邮政速递物流"],
    hotline: "11183",
    serviceHours: "以 EMS 官方页面和当地网点公告为准",
    channels: ["官网", "App", "热线"],
    useCases: ["国内国际邮件", "查件", "投诉", "改派咨询"],
    website: "https://www.ems.com.cn/",
    notes: ["国际件与国内件规则可能不同", "涉及海关或跨境场景要额外确认"],
  },
  {
    id: "jd",
    name: "京东快递",
    aliases: ["jd", "jingdong", "京东", "京东物流", "京东快递", "jdexpress"],
    hotline: "950616",
    serviceHours: "8:00-22:00（官方帮助中心检索到的物流热线时间）",
    channels: ["帮助中心", "在线客服", "热线"],
    useCases: ["京东物流查件", "催件", "异常反馈", "合作咨询"],
    website: "https://help.jd.com/user/issue/270-314.html",
    notes: ["要区分 950616（物流）和 950618（商城）", "商品售后通常还要同步找卖家或平台"],
  },
  {
    id: "jt",
    name: "极兔速递",
    aliases: ["jt", "j&t", "jtexpress", "极兔", "极兔速递"],
    hotline: "956025",
    serviceHours: "7x24 智能客服；人工一般 08:30-20:00，以官网公告为准",
    channels: ["官网", "在线客服", "热线"],
    useCases: ["催件", "投诉", "驿站代收争议", "理赔跟进"],
    website: "https://www.jtexpress.cn/",
    notes: ["官网有单独服务时间页面", "处理异常前先留运单截图和时间线"],
  },
  {
    id: "sf",
    name: "顺丰速运",
    aliases: ["sf", "s.f.", "sf-express", "顺丰", "顺丰速运"],
    hotline: "95338",
    serviceHours: "中国内地常见公告为 08:00-21:00，以顺丰最新页面为准",
    channels: ["官网", "App", "小程序", "热线"],
    useCases: ["查件", "催派", "投诉", "改派", "保价相关咨询"],
    website: "https://www.sf-express.com/cn/sc/",
    notes: ["国际件与内地热线说明不同", "保价和高价值件建议第一时间留证并建单"],
  },
  {
    id: "sto",
    name: "申通快递",
    aliases: ["sto", "shentong", "申通", "申通快递"],
    hotline: "95543",
    serviceHours: "以申通官网和网点公示为准",
    channels: ["官网", "微信查件", "热线"],
    useCases: ["查件", "催件", "网点投诉", "派送异常"],
    website: "https://www.sto.cn/",
    notes: ["很多查询页面和网点页都会展示 95543", "涉及网点问题时要留网点名称"],
  },
  {
    id: "yto",
    name: "圆通速递",
    aliases: ["yto", "yuantong", "圆通", "圆通速递"],
    hotline: "95554",
    serviceHours: "以圆通官网和最新公告为准",
    channels: ["官网", "App", "热线"],
    useCases: ["查件", "催件", "投诉", "异常反馈"],
    website: "https://www.yto.net.cn/",
    notes: ["热线号码常见于官网隐私政策和商城页面", "客服时间要以最新页面为准"],
  },
  {
    id: "yunda",
    name: "韵达速递",
    aliases: ["yunda", "yundaex", "韵达", "韵达速递"],
    hotline: "95546",
    serviceHours: "以韵达官网公告为准",
    channels: ["官网", "在线投诉", "热线"],
    useCases: ["查件", "催件", "投诉", "异常反馈"],
    website: "https://www.yundaex.com/",
    notes: ["官网联系页面可见客服热线", "在线投诉入口适合需要留痕的场景"],
  },
  {
    id: "zto",
    name: "中通快递",
    aliases: ["zto", "zhongtong", "中通", "中通快递"],
    hotline: "95311",
    serviceHours: "自助 7x24；人工常见为 08:30-20:00，以官网为准",
    channels: ["官网", "App", "热线"],
    useCases: ["查件", "催件", "投诉", "网点反馈"],
    website: "https://www.zto.com/",
    notes: ["官网服务详情页能看到查询服务说明", "人工时间和网点服务时间不是一回事"],
  },
];

const issues = {
  delay: {
    title: "延误 / 催件",
    when: "物流明显慢于承诺时效，或已到本地但长时间未派送。",
    steps: [
      "先看最近一条轨迹停在哪个节点：揽收、中转、本地网点、派送中。",
      "准备运单号、手机号后四位、下单平台和承诺时效截图。",
      "先找承运快递客服建单催件，并记录工单号和承诺回电时间。",
      "如果是平台订单，同步找卖家或平台客服，避免只催快递没人兜底。",
      "超过客服承诺时限仍无进展，再升级投诉并补截图留痕。",
    ],
    watchouts: [
      "大促、天气、安检、交通管制会影响时效。",
      "不要只说“快点”，要明确问卡在哪个节点、谁负责回电、多久给结果。",
    ],
  },
  "no-update": {
    title: "轨迹长时间不更新",
    when: "物流轨迹停留在同一节点超过用户可接受范围，常见于揽收后或中转中。",
    steps: [
      "先确认是不是电子面单已出但实际未揽收。",
      "截图最近完整轨迹，尤其是最后一次更新时间。",
      "联系客服时直接问：包裹是否真实揽收、是否滞留、是否丢失排查中。",
      "如果是卖家刚发货，同步找卖家确认是否已实际交给快递。",
      "客服无法解释停滞原因时，要求建立异常件排查工单。",
    ],
    watchouts: [
      "“已下单/已出单”不等于已被快递员拿走。",
      "跨省或偏远线路需要避免过早下丢件结论。",
    ],
  },
  "delivered-missing": {
    title: "显示已签收但本人未收到",
    when: "系统显示签收、已投递、已妥投，但收件人实际没有拿到。",
    steps: [
      "先问清签收时间、签收人、投递位置、是否投驿站或快递柜。",
      "检查短信、门口、物业、驿站、小区前台和监控。",
      "立即联系客服发起签收争议，要求核实派件员、签收底单或投递照片。",
      "若未经同意放代收点，可按未按约定派送投诉。",
      "证据充分时，同步通知卖家或平台，防止超出售后时效。",
    ],
    watchouts: [
      "这类问题越早报越容易调监控和定位派件员。",
      "不要只说“没收到”，要明确问“谁签收、放哪了、有没有照片”。",
    ],
  },
  "station-dropoff": {
    title: "未经同意投放驿站 / 快递柜 / 代收点",
    when: "用户要求送货上门或未授权代收，但快递被直接放到代收点。",
    steps: [
      "保留取件短信、驿站照片、聊天记录或下单页配送要求截图。",
      "先联系快递客服，明确投诉点是“未经同意代收/未按约定上门”。",
      "要求重新配送、说明责任网点，并记录工单号。",
      "如果涉及生鲜、药品、贵重物品，要同步强调损失风险和时效性。",
      "必要时升级投诉，并同步卖家或平台售后。",
    ],
    watchouts: [
      "先区分是否是平台页默认勾选了驿站代收。",
      "涉及老人、孕妇、行动不便等场景时，描述清楚更容易升级处理。",
    ],
  },
  damaged: {
    title: "破损 / 少件 / 外包装异常",
    when: "包裹外箱破损、内件损坏、少件、液体泄漏或明显挤压变形。",
    steps: [
      "优先拍开箱视频或至少拍外包装六面、面单、破损细节、内件状态。",
      "不要急着丢包装，保留箱体、填充物、面单和签收凭证。",
      "联系客服时明确是破损还是少件，是否当面验收、是否签收异常。",
      "如果是平台购物，同步发给卖家售后；物流责任和商品售后可能并行。",
      "高价值件或保价件，第一时间走正式理赔流程，不要只口头沟通。",
    ],
    watchouts: [
      "没有留包装和面单会显著削弱后续举证。",
      "食品、生鲜、易碎品要特别记录开箱时间和状态。",
    ],
  },
  lost: {
    title: "疑似丢件",
    when: "轨迹异常停滞后客服确认无法定位，或包裹在末端、中转环节失踪。",
    steps: [
      "先要求客服明确状态：滞留、排查中、破损分拣、丢失。",
      "保留客服工单号、客服承诺、轨迹截图和商品价值证明。",
      "如果有保价，按保价流程提交材料；如果没有，也要先走企业理赔流程。",
      "平台订单同步通知卖家或平台，防止退款/补发链路卡住。",
      "企业长时间不处理时，再升级监管申诉渠道。",
    ],
    watchouts: [
      "不要在未确认前直接认定永久丢失。",
      "商品价值证明最好准备订单页、付款页、发票或商品链接。",
    ],
  },
  "refusal-return": {
    title: "拒收 / 退回 / 逆向件卡住",
    when: "用户拒收后迟迟未退回，或退货件长期不动、商家未收到。",
    steps: [
      "先确认是正向件拒收，还是电商退货逆向件。",
      "截取拒收时间、退回时间、最新轨迹和平台售后单状态。",
      "联系客服问清是卡在派送网点、中转、揽退还是仓库签收环节。",
      "平台退货件要同步卖家和平台，避免退款时效被动超时。",
      "如果是拒收后还显示签收，要立刻发起轨迹核实。",
    ],
    watchouts: [
      "“拒收”不等于系统立刻原路返回。",
      "平台退货通常还涉及售后单和仓库签收，不是纯快递问题。",
    ],
  },
  "fraud-check": {
    title: "诈骗短信 / 诈骗电话 / 可疑取件码核验",
    when: "用户收到陌生链接、异常赔付电话、假冒客服退款、可疑取件码通知。",
    steps: [
      "先不要点链接、不要报验证码、不要共享屏幕、不要下载陌生 App。",
      "核对短信或电话里提到的快递公司是否真实存在、运单号是否匹配。",
      "通过官方 App、官网或官方热线反查，不要回拨短信里的私人号码。",
      "如果对方声称理赔、改址、海关扣件、包裹涉案，先按诈骗高风险处理。",
      "已泄露验证码、银行卡或转账时，立刻联系银行和平台并报警。",
    ],
    watchouts: [
      "正规快递客服一般不会通过陌生链接让你输入银行卡和验证码。",
      "“快递丢失双倍赔付”“快件异常请点链接修改地址”是高风险套路。",
    ],
  },
};

function printUsage() {
  console.log(`快递助手脚本

用法:
  node kuaidi.js list
  node kuaidi.js carrier <公司名或别名> [--json]
  node kuaidi.js issue <问题类型> [--json]

问题类型:
  delay
  no-update
  delivered-missing
  station-dropoff
  damaged
  lost
  refusal-return
  fraud-check
`);
}

function normalize(input) {
  return String(input || "").trim().toLowerCase();
}

function findCarrier(query) {
  const q = normalize(query);
  if (!q) return null;
  return (
    carriers.find((carrier) => carrier.id === q) ||
    carriers.find((carrier) => normalize(carrier.name) === q) ||
    carriers.find((carrier) =>
      carrier.aliases.some((alias) => normalize(alias) === q),
    ) ||
    carriers.find(
      (carrier) =>
        normalize(carrier.name).includes(q) ||
        carrier.aliases.some((alias) => normalize(alias).includes(q)),
    )
  );
}

function output(value, asJson) {
  if (asJson) {
    console.log(JSON.stringify(value, null, 2));
    return;
  }

  if (Array.isArray(value)) {
    for (const item of value) {
      console.log(`${item.name} | ${item.hotline} | ${item.website}`);
    }
    return;
  }

  if (value.hotline) {
    console.log(`${value.name}`);
    console.log(`热线: ${value.hotline}`);
    console.log(`服务时间: ${value.serviceHours}`);
    console.log(`渠道: ${value.channels.join("、")}`);
    console.log(`适用: ${value.useCases.join("、")}`);
    console.log(`官网: ${value.website}`);
    if (value.notes.length) {
      console.log("备注:");
      for (const note of value.notes) {
        console.log(`- ${note}`);
      }
    }
    return;
  }

  if (value.steps) {
    console.log(`${value.title}`);
    console.log(`适用场景: ${value.when}`);
    console.log("建议步骤:");
    value.steps.forEach((step, index) => {
      console.log(`${index + 1}. ${step}`);
    });
    if (value.watchouts.length) {
      console.log("注意:");
      for (const tip of value.watchouts) {
        console.log(`- ${tip}`);
      }
    }
  }
}

const args = process.argv.slice(2);
const command = args[0];
const asJson = args.includes("--json");

if (!command || command === "help" || command === "--help" || command === "-h") {
  printUsage();
  process.exit(0);
}

if (command === "list") {
  output(carriers, asJson);
  process.exit(0);
}

if (command === "carrier") {
  const query = args[1];
  const carrier = findCarrier(query);
  if (!carrier) {
    console.error("未找到对应快递公司。先运行 `node kuaidi.js list` 查看支持列表。");
    process.exit(1);
  }
  output(carrier, asJson);
  process.exit(0);
}

if (command === "issue") {
  const key = args[1];
  const issue = issues[key];
  if (!issue) {
    console.error("未知问题类型。运行 `node kuaidi.js help` 查看支持列表。");
    process.exit(1);
  }
  output(issue, asJson);
  process.exit(0);
}

console.error("未知命令。运行 `node kuaidi.js help` 查看用法。");
process.exit(1);
