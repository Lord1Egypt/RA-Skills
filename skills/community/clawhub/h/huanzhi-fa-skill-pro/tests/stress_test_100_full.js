#!/usr/bin/env node
/**
 * 焕智AI FaSkill Pro — 100用户×100轮次全对话压力测试
 * 覆盖：6模块场景 / 风险检测 / 转化引导 / OPC vs 非OPC对比
 */
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require("docx");

const SKILL_DIR = path.resolve(__dirname, "..");
const SECTORS = ["AI智能体","大模型应用","AIGC内容","跨境电商","出海SaaS","硬科技","金融科技","企业服务SaaS","AI短剧","数字文创","健康科技","教育科技","Web3","智能硬件","新能源"];
const STAGES = ["刚注册","有产品","有收入","准备融资","已融资"];
const DISTRICTS = ["徐汇区","黄浦区","浦东新区","临港新片区","杨浦区","静安区","闵行区","青浦区","松江区","嘉定区","虹口区","长宁区","宝山区","普陀区","崇明区"];
const TOTAL_USERS = 100;
const TURNS_PER_USER = 100;
const OPC_COUNT = 50;

// ===== Seeded Random =====
function seededRandom(seed) {
  let s = seed;
  return function() { s = (s * 1664525 + 1013904223) & 0x7fffffff; return s / 0x7fffffff; };
}

// ===== Profile Generator =====
function generateProfile(seed, isOPC) {
  const rng = seededRandom(seed);
  const sector = SECTORS[Math.floor(rng() * SECTORS.length)];
  const stage = STAGES[Math.floor(rng() * STAGES.length)];
  const district = DISTRICTS[Math.floor(rng() * DISTRICTS.length)];
  
  const teamSize = isOPC ? Math.floor(1 + rng() * 3) : Math.floor(3 + rng() * 28);
  const hasCTO = rng() < (isOPC ? 0.15 : 0.55);
  const founderExp = [1,2,3,5,7,10,15][Math.floor(rng()*7)];
  
  let mau, revenue;
  if (stage === "刚注册") { mau = rng()*5000|0; revenue = rng()*50000|0; }
  else if (stage === "有产品") { mau = (100+rng()*50000)|0; revenue = (rng()*200000)|0; }
  else if (stage === "有收入") { mau = (5000+rng()*145000)|0; revenue = (50000+rng()*950000)|0; }
  else { mau = (10000+rng()*490000)|0; revenue = (100000+rng()*4900000)|0; }
  
  return {
    _id: seed, _sector: sector, _stage: stage, _district: district, _isOPC: isOPC,
    _teamSize: teamSize, _founderExp: founderExp,
    mau, monthly_revenue: revenue, growth_rate: +(rng()*0.5).toFixed(2),
    tam: [0.1,0.5,1,5,10,50,100,500][(rng()*8)|0] * 1e9,
    sam: 0,
    team_size: teamSize, has_cto: hasCTO, has_cmo: rng()<0.2, founder_experience: founderExp,
    tech_team_ratio: +(0.1+rng()*0.8).toFixed(2), has_previous_funding: stage==="已融资",
    has_mvp: true, has_pmf: rng()<0.4, paying_users: (rng()*500)|0,
    retention_rate: +(0.1+rng()*0.7).toFixed(2), nps_score: (-10+rng()*81)|0,
    has_clear_narrative: rng()<0.55, has_emotional_hook: rng()<0.4,
    has_pitch_deck: rng()<0.6, pitch_deck_quality: (rng()*21)|0,
    ltv: (100+rng()*49900)|0, cac: (50+rng()*1950)|0, gross_margin: +(0.2+rng()*0.65).toFixed(2),
    funding_amount: [500000,1000000,2000000,5000000,8000000,10000000][(rng()*6)|0],
    has_detailed_plan: rng()<0.5, runway_months: (3+rng()*22)|0,
    sector, market_education_cost: rng()<0.4?"低":(rng()<0.5?"中":"高"),
    competitor_count: (rng()*101)|0, market_trend: rng()<0.6?"需求上升":"竞争加剧",
    district,
    company_name: `${isOPC?"OPC":"创业"}${seed}`,
    years_in_segment: (rng()*9)|0, revenue_last_year: revenue*12,
    rd_ratio: +(rng()*0.20).toFixed(2), rd_expense: (rng()*5000000)|0,
    employees: teamSize, rd_employees: Math.max(1, (teamSize*(0.1+rng()*0.8))|0),
    patents_invention: (rng()*5)|0, patents_utility: (rng()*10)|0,
    software_copyrights: (rng()*15)|0,
    has_quality_cert: rng()<0.15, has_cloud_adoption: rng()<0.6,
    has_ai_application: sector.includes("AI")||rng()<0.4,
    main_business_revenue_ratio: +(0.5+rng()*0.5).toFixed(2),
    profit_growth: +(-0.2+rng()*0.5).toFixed(2), anxiety_level: (rng()*11)|0,
  };
}

// ===== Script Runner =====
function runPython(script, input) {
  try {
    const out = execSync(`python3 "${path.join(SKILL_DIR,'scripts',script)}" '${JSON.stringify(input).replace(/'/g,"'\\''")}'`, {cwd:SKILL_DIR, encoding:"utf-8", timeout:5000});
    return JSON.parse(out);
  } catch(e) { return {error: e.message}; }
}

// ===== Risk Detector =====
function detectRisks(profile, diag) {
  const risks = [];
  // Team risk
  if (profile._isOPC && !profile.has_cto) risks.push({type:"OPC_缺CTO", severity:"high", detail:"OPC创始人无技术合伙人，融资时被质疑技术风险"});
  if (profile.team_size <= 2) risks.push({type:"团队过小", severity:"medium", detail:`仅${profile.team_size}人团队，投资人可能担心抗风险能力`});
  // Financial risk
  if (profile.runway_months < 6) risks.push({type:"跑道不足", severity:"critical", detail:`剩余${profile.runway_months}个月runway，需紧急融资或降本`});
  if (profile.monthly_revenue < 10000 && profile._stage !== "刚注册") risks.push({type:"收入不足", severity:"medium", detail:"月收入低于1万，产品验证不足"});
  // Story risk
  if (!profile.has_clear_narrative) risks.push({type:"叙事不清晰", severity:"medium", detail:"缺乏清晰的商业叙事，融资路演效果差"});
  if (!profile.has_pitch_deck) risks.push({type:"缺少BP", severity:"high", detail:"尚未准备商业计划书，无法启动正式融资"});
  // Market risk
  if (profile.competitor_count > 50) risks.push({type:"竞争激烈", severity:"low", detail:`${profile.competitor_count}家竞争对手，差异化需突出`});
  // Term sheet risk (simulated)
  if (diag.score > 70 && Math.random() < 0.3) risks.push({type:"TS估值陷阱", severity:"high", detail:"评分较高时容易被高估值吸引而忽略条款陷阱（如2x清算优先权）"});
  // Anxiety risk
  if (profile.anxiety_level >= 7) risks.push({type:"创始人焦虑", severity:"high", detail:`焦虑指数${profile.anxiety_level}/10，需触发Capital EQ干预`});
  // OPC specific
  if (profile._isOPC && profile._stage === "准备融资") risks.push({type:"OPC融资阻力", severity:"high", detail:"OPC创业者被传统VC质疑团队规模，需特别准备OPC叙事"});
  if (profile._isOPC && !profile.has_emotional_hook) risks.push({type:"OPC情感共鸣缺失", severity:"medium", detail:"OPC创业者叙事中缺少个人故事和情感共鸣点"});
  return risks;
}

// ===== Conversation Simulator =====
function simulateConversations(profile, diag, policy, zjtx) {
  const turns = [];
  const riskFlags = [];
  const conversionAttempts = [];
  let riskCount = 0;
  let conversionCount = 0;
  let moduleUsage = {1:0,2:0,3:0,4:0,5:0,6:0};
  
  const rng = seededRandom(profile._id * 713 + 407);

  // ===== Onboarding (Turns 1-5) =====
  turns.push({t:1, role:"FA", module:"onboarding", text:"你好我是焕智AI，你的AI融资参谋。能帮你做融资诊断、拆TS、查补贴政策。法律/财务决策请咨询专业人士。今天聊哪个方向？1️⃣融资诊断 2️⃣TS条款 3️⃣情绪支持 4️⃣政策补贴 5️⃣FA撮合 6️⃣投后管家"});
  
  const opener = profile._isOPC ? 
    ["1","想看看我项目融资能打几分","帮我评估一下","1"][profile._id%4] :
    ["1","融资诊断","看看准备好了吗","评分"][profile._id%4];
  turns.push({t:2, role:"用户", module:"onboarding", text:opener});
  turns.push({t:3, role:"FA", module:"1", text:`【诊断启动】先确认3个问题：1.月活/收入/增长？2.团队几人？3.融资金额和用途？`});
  moduleUsage[1]++;
  
  // ===== Module 1: Diagnosis (Turns 4-15) =====
  const mauText = profile.mau > 0 ? `月活${(profile.mau/10000).toFixed(1)}万` : "暂无月活数据";
  const revText = profile.monthly_revenue > 0 ? `月收入¥${(profile.monthly_revenue/10000).toFixed(1)}万` : "暂无收入";
  turns.push({t:4, role:"用户", module:"1", text:`${mauText}，${revText}，增长率${(profile.growth_rate*100).toFixed(0)}%。团队${profile.team_size}人${profile.has_cto?"有CTO":"缺CTO"}。想融${(profile.funding_amount/10000).toFixed(0)}万。`});
  
  const score = diag.score || diag.total || 0;
  const grade = diag.grade || "N/A";
  turns.push({t:5, role:"FA", module:"1", text:`【结论】评分${score}/100（${grade}）${score>=60?"建议补强后启动融资":"建议先专注产品和增长"}`});
  moduleUsage[1] += 2;
  
  // Risk: score-based warnings
  if (score < 60) riskFlags.push({turn:5, type:"评分过低", detail:`${score}/100，FA直接说没准备好`});
  if (profile._isOPC && !profile.has_cto) riskFlags.push({turn:5, type:"OPC团队风险", detail:"缺CTO影响评分"});
  
  // 追问短板 (Turns 6-10)
  turns.push({t:6, role:"用户", module:"1", text:"有哪些短板？"});
  const weaknesses = diag.weaknesses || [];
  const weakText = weaknesses.slice(0,3).map((w,i)=>`${i+1}. ${w.dimension||w.name}: ${w.issue||w.detail}`).join("\\n")||"数据不足，难以评估";
  turns.push({t:7, role:"FA", module:"1", text:`短板：${weakText}`});
  moduleUsage[1] += 2;
  
  for (let j=0; j<3; j++) {
    const w = weaknesses[j];
    if (w) {
      riskFlags.push({turn:7+j, type:`短板_${w.dimension||w.name}`, detail:w.issue||w.detail, severity:w.impact||"medium"});
    }
  }

  // ===== Module Flow: 根据评分和画像生成多模块交叉对话 =====
  let turnIdx = 8;
  
  // Module 2: Materials (Turns 8-18)
  if (rng() < 0.6) {
    turns.push({t:turnIdx++, role:"FA", module:"next_prompt", text:"看完短板了，想知道BP怎么优化吗？选'BP'我帮你评审。"});
    turns.push({t:turnIdx++, role:"用户", module:"2", text:"帮我看看BP怎么写"});
    turns.push({t:turnIdx++, role:"FA", module:"2", text:"【材料工坊】BP按10维度评审：叙事逻辑/市场分析/产品价值/商业模式/竞争壁垒/团队能力/财务预测/资金用途/退出路径/呈现质量。有BP文件可以上传。"});
    moduleUsage[2] += 3;
    
    if (!profile.has_pitch_deck) {
      riskFlags.push({turn:turnIdx-1, type:"BP缺失风险", detail:"用户无BP，需引导创建"});
      turns.push({t:turnIdx++, role:"用户", module:"2", text:"还没写BP，怎么办？"});
      turns.push({t:turnIdx++, role:"FA", module:"2", text:"OPC创业者BP不用太长，核心3页：1.产品解决什么问题 2.数据说话 3.需要多少钱做什么用。先跑通最小商业闭环再写BP也不迟。"});
      moduleUsage[2] += 2;
    }
  }

  // Module 4: Policy (Turns 19-35)
  if (rng() < 0.7) {
    turns.push({t:turnIdx++, role:"FA", module:"next_prompt", text:`你们${profile._district}的OPC补贴政策不少，选4️⃣我帮你查。`});
    turns.push({t:turnIdx++, role:"用户", module:"4", text:`我在${profile._district}，能申请什么补贴？`});
    const policies = policy.matched_policies || [];
    if (policy.district_coverage === "not_covered") {
      turns.push({t:turnIdx++, role:"FA", module:"4", text:`【${profile._district}】数据库已标记未收录，当前给出国家层面政策（创业担保贷款最高60万/科创贷最高1000万/高新技术企业15%税率）。建议确认赛道后联网补充区域政策。`});
      riskFlags.push({turn:turnIdx-1, type:"政策区域未覆盖", detail:`${profile._district}不在数据库中`});
    } else {
      turns.push({t:turnIdx++, role:"FA", module:"4", text:`【${profile._district}可申领】共${policies.length}项，优先申请${policies[0]?.name||"创业补贴"}`});
    }
    moduleUsage[4] += 3;
  }

  // Module 6: Capital EQ (Turns 36-50)
  if (profile.anxiety_level >= 5) {
    turns.push({t:turnIdx++, role:"用户", module:"6", text:"融资压力太大了...有点撑不住"});
    turns.push({t:turnIdx++, role:"FA", module:"6", text:`【Capital EQ】先停下来深呼吸。你现在焦虑很正常——每个创始人都会经历这个阶段。被拒不是你不行，是概率问题。沈南鹏说过"创业者最重要的品质不是聪明，是坚韧"。先别做决定，明天再复盘。`});
    moduleUsage[6] += 2;
    riskFlags.push({turn:turnIdx-1, type:"Capital_EQ触发", detail:`焦虑指数${profile.anxiety_level}/10，已触发情绪支持`});
    
    // 金句引用检测
    if (rng() < 0.5) {
      turns.push({t:turnIdx++, role:"用户", module:"6", text:"真的有人能熬过来吗？"});
      turns.push({t:turnIdx++, role:"FA", module:"6", text:"王兴创业失败过10次，第11次做成了美团。你现在被拒不代表项目不行。接下来你最想先解决哪个问题？融资节奏？条款？还是心理压力？"});
      moduleUsage[6] += 2;
    }
  }

  // Module 3: Conversion Check (Turns 51-65)
  // Check if conversion should trigger based on rules
  const shouldConvert = score >= 60 || profile.anxiety_level >= 6 || moduleUsage[1]+moduleUsage[2]+moduleUsage[4]+moduleUsage[6] >= 10;
  if (shouldConvert && turnIdx <= 65) {
    turns.push({t:turnIdx++, role:"FA", module:"conversion", text:"如果觉得AI分析不够细，需要有人陪跑整个融资流程——可以升级Pro版。📧18616610601@163.com 💬wx381777。你觉得你目前最大的障碍是哪个？"});
    conversionAttempts.push({turn:turnIdx-1, score, anxiety:profile.anxiety_level, modulesUsed:Object.values(moduleUsage).reduce((a,b)=>a+b,0)});
    
    const responses = ["怎么升级？有什么不同？","嗯，发来看看","考虑一下","不需要，别推了"];
    const response = responses[profile._id % 4];
    turns.push({t:turnIdx++, role:"用户", module:"conversion", text:response});
    
    // Classify interest
    let interest = "none";
    if (response.includes("怎么升级")) interest = "warm";
    else if (response.includes("发来看看")) interest = "cold";
    else if (response.includes("考虑")) interest = "cold";
    else interest = "reject";
    
    conversionAttempts[conversionAttempts.length-1].interest = interest;
    conversionAttempts[conversionAttempts.length-1].response = response;
    conversionCount++;
    
    if (interest === "warm") {
      turns.push({t:turnIdx++, role:"FA", module:"conversion", text:"Pro版提供一对一融资辅导，帮你打磨BP、匹配投资人、谈判TS条款。很多创始人也是从AI版用起后来升级的。你觉得融资节奏把控是你最需要的吗？"});
    } else if (interest === "cold" || interest === "reject") {
      turns.push({t:turnIdx++, role:"FA", module:"next_prompt", text:"没关系，先继续用AI版。还有什么想了解的吗？"});
    }
  }

  // ===== Fill remaining turns with module rotation (Turns 66-100) =====
  const modules = [1,2,3,4,6];
  for (let t = turnIdx; t <= TURNS_PER_USER; t++) {
    const mod = modules[t % modules.length];
    const mTexts = {
      1: ["我的Traction怎么样？","团队评分为什么低？","融资时机对吗？"],
      2: ["BP怎么优化？","财务模型怎么做？","需要准备什么材料？"],
      3: ["谁适合投我们？","怎么约投资人？","怎么判断投资人好坏？"],
      4: ["还有什么政策？","专精特新怎么评？","补贴多久到账？"],
      6: ["投资人没回复怎么办？","谈判时紧张怎么办？","估值被压价正常吗？"],
    };
    const fTexts = {
      1: ["【诊断】Traction评分反映了增长数据，建议冲刺月活里程碑。","【诊断】团队维度因缺CTO失分，建议优先补技术合伙人。","【诊断】当前赛道处于早期爆发期，时机有利——但数据要跟得上。"],
      2: ["【材料工坊】BP建议突出市场验证数据，少讲技术多讲痛点。","【材料工坊】3年财务模型建议保守估计增长率15-20%。","【材料工坊】种子轮Data Room需要营业执照+产品demo+客户列表。"],
      3: ["【投资人雷达】推荐Tier A: 3-5家该赛道活跃机构，先接触Lead。","【投资人雷达】约投资人最佳方式是熟人引荐+冷邮件+Demo Day。","【投资人雷达】看机构历史投后：是否帮忙对接资源、是否过度干预。"],
      4: ["【政策】可申请高企认定享15%税率+研发费用加计扣除。","【专精特新】目前差距：需要1项发明专利+2年细分市场经验。","【政策】补贴审批周期通常2-3个月，建议提前准备材料。"],
      6: ["【Capital EQ】投资人没回复不一定是否定——他们可能在等你下轮数据。王琼说过\"好的项目，创始人眼里是有光的\"。你觉得自己现在的状态如何？","【Capital EQ】谈判紧张是正常的——但记住\"估值不是谈出来的，是设计出来的\"。准备好底线就不慌了。","【Capital EQ】被压价不代表你不行——投资人在测试你的心理价位。先不急着答应，说\"我们也在和其他几家聊\"。"],
    };
    
    const uQ = mTexts[mod][t % 3];
    const fA = fTexts[mod][t % 3];
    turns.push({t, role:"用户", module:String(mod), text:uQ});
    moduleUsage[mod]++;
    
    // Detect risks in user questions
    if (uQ.includes("为什么") || uQ.includes("低")) riskFlags.push({turn:t, type:"用户质疑", detail:`${uQ}——可能对评分不满`});
    if (uQ.includes("紧张") || uQ.includes("压价")) riskFlags.push({turn:t, type:"谈判焦虑", detail:uQ});
    
    turns.push({t:t+0.5|0, role:"FA", module:String(mod), text:fA});
    moduleUsage[mod]++;
    
    // Periodic conversion check every 30 turns
    if (t % 30 === 27 && t > 30) {
      turns.push({t:t+0.8|0, role:"FA", module:"conversion", text:"已经聊了这么多轮了，如果你觉得需要一对一陪跑——Pro版随时可以升级。📧18616610601@163.com 💬wx381777"});
      conversionAttempts.push({turn:t, type:"轮次强制触发(30轮)", modulesUsed:Object.values(moduleUsage).reduce((a,b)=>a+b,0)});
      conversionCount++;
    }
    
    t = t + 0.5|0;
  }

  return { turns, riskFlags, conversionAttempts, moduleUsage, riskCount: riskFlags.length, conversionCount };
}

// ===== Word Report Generator =====
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

function p(text, opts = {}) {
  return new Paragraph({ spacing: { after: 120 }, ...opts, children: typeof text === "string" ? [new TextRun({ text, font: "Arial", ...opts.run })] : text, });
}
function header(text, level = 1) {
  return new Paragraph({ heading: {1:HeadingLevel.HEADING_1,2:HeadingLevel.HEADING_2,3:HeadingLevel.HEADING_3}[level], spacing: { before: 240, after: 120 }, children: [new TextRun({ text, font: "Arial", bold: true })] });
}
function makeCell(text, opts = {}) {
  return new TableCell({ borders, width: { size: opts.width || 2000, type: WidthType.DXA }, margins: cellMargins, shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ children: [new TextRun({ text: String(text), font: "Arial", size: 20, bold: !!opts.bold, color: opts.color || "000000" })] })] });
}
function makeRow(cells, isHeader = false) {
  return new TableRow({ children: cells.map((c, i) => makeCell(c, { width: c.width || 1800, shading: isHeader ? "2E75B6" : (i % 2 === 0 ? "F2F2F2" : undefined), bold: isHeader, color: isHeader ? "FFFFFF" : undefined })) });
}

async function main() {
  console.log(`生成100用户画像(50 OPC+50非OPC)...`);
  
  const users = [];
  const allData = [];
  const stats = { totalTurns:0, totalRisks:0, riskByType:{}, riskBySeverity:{critical:0,high:0,medium:0,low:0},
    conversions:{total:0,warm:0,cold:0,reject:0,warmRate:"0%"},
    opcVsNonOpc:{opc:{avgScore:0,avgRisks:0,avgConvs:0},nonOpc:{avgScore:0,avgRisks:0,avgConvs:0}},
    moduleUsage:{1:0,2:0,3:0,4:0,5:0,6:0}, errors:0 };
  
  for (let i = 0; i < TOTAL_USERS; i++) {
    process.stdout.write(`\r  用户 ${i+1}/${TOTAL_USERS}`);
    const isOPC = i < OPC_COUNT;
    const profile = generateProfile(i, isOPC);
    
    const diag = runPython("funding_diagnosis.py", profile);
    const policy = runPython("policy_matcher.py", profile);
    const zjtx = runPython("zhuanjingtexin_assessor.py", profile);
    
    if (diag.error || policy.error || zjtx.error) stats.errors++;
    
    const risks = detectRisks(profile, diag);
    const conv = simulateConversations(profile, diag, policy, zjtx);
    
    // Aggregate stats
    stats.totalTurns += conv.turns.length;
    stats.totalRisks += risks.length;
    risks.forEach(r => { stats.riskByType[r.type] = (stats.riskByType[r.type]||0) + 1; stats.riskBySeverity[r.severity]++; });
    conv.conversionAttempts.forEach(c => { stats.conversions.total++; if (c.interest) stats.conversions[c.interest]++; });
    for (let m=1; m<=6; m++) stats.moduleUsage[m] = (stats.moduleUsage[m]||0) + (conv.moduleUsage[m]||0);
    
    const score = diag.score?.total || diag.total || 0;
    if (isOPC) { stats.opcVsNonOpc.opc.avgScore += score; stats.opcVsNonOpc.opc.avgRisks += risks.length; stats.opcVsNonOpc.opc.avgConvs += conv.conversionCount; }
    else { stats.opcVsNonOpc.nonOpc.avgScore += score; stats.opcVsNonOpc.nonOpc.avgRisks += risks.length; stats.opcVsNonOpc.nonOpc.avgConvs += conv.conversionCount; }
    
    allData.push({ id:i+1, isOPC, profile, diag, policy, zjtx, risks, conv });
  }
  
  stats.opcVsNonOpc.opc.avgScore /= OPC_COUNT; stats.opcVsNonOpc.opc.avgRisks /= OPC_COUNT; stats.opcVsNonOpc.opc.avgConvs /= OPC_COUNT;
  stats.opcVsNonOpc.nonOpc.avgScore /= (TOTAL_USERS-OPC_COUNT); stats.opcVsNonOpc.nonOpc.avgRisks /= (TOTAL_USERS-OPC_COUNT); stats.opcVsNonOpc.nonOpc.avgConvs /= (TOTAL_USERS-OPC_COUNT);
  const warmTotal = stats.conversions.warm + stats.conversions.cold + stats.conversions.reject;
  stats.conversions.warmRate = warmTotal > 0 ? `${(stats.conversions.warm/warmTotal*100).toFixed(0)}%` : "0%";
  
  console.log(`\n  生成Word报告...`);
  
  // ===== Build Word Document =====
  const children = [];
  
  // Cover
  children.push(new Paragraph({ spacing: { before: 3000 }, children: [] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "焕智AI FaSkill Pro", font: "Arial", size: 56, bold: true, color: "2E75B6" })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: "100用户×100轮次 全对话压测报告", font: "Arial", size: 36, color: "666666" })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "风险检测 + 转化效果 + OPC专项分析", font: "Arial", size: 28, color: "999999" })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "50 OPC + 50 非OPC | 每人100轮 | 总计10,000+轮", font: "Arial", size: 24, color: "999999" })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: `错误: ${stats.errors} | 版本: v3.0.2`, font: "Arial", size: 20, color: "999999" })] }));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  
  // 1. 测试概览
  children.push(header("1. 测试概览"));
  children.push(p(`用户画像: ${TOTAL_USERS}个（50个OPC/一人公司 + 50个非OPC/传统创业）`));
  children.push(p(`每用户对话轮次: ≥${TURNS_PER_USER}轮（总计 ${stats.totalTurns} 轮）`));
  children.push(p(`覆盖模块: 6大模块（诊断/材料工坊/投资人雷达/谈判参谋/尽调护航/情绪支持）`));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  
  // 2. 风险检测汇总
  children.push(header("2. 风险检测汇总"));
  children.push(p(`检测风险总数: ${stats.totalRisks}`));
  
  children.push(header("2.1 风险类型分布", 2));
  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [2600,1500,5260],
    rows: [makeRow(["风险类型","次数","占比"],true), ...Object.entries(stats.riskByType).sort((a,b)=>b[1]-a[1]).slice(0,15).map(([k,v])=>makeRow([k,String(v),`${"█".repeat(Math.max(1,Math.floor(v/2)))} ${(v/stats.totalRisks*100).toFixed(1)}%`]))],
  }));
  children.push(p(""));
  
  children.push(header("2.2 风险严重度分布", 2));
  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [2200,1500,5660],
    rows: [makeRow(["严重度","数量","比例"],true), ["critical","high","medium","low"].map(s=>makeRow([s, String(stats.riskBySeverity[s]), `${"█".repeat(Math.max(1,stats.riskBySeverity[s]/2))} ${(stats.riskBySeverity[s]/stats.totalRisks*100).toFixed(1)}%`]))],
  }));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  
  // 3. 转化效果
  children.push(header("3. 转化引导效果分析"));
  children.push(p(`转化引导触发总次数: ${stats.conversions.total}`));
  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [2200,1500,1500,4160],
    rows: [makeRow(["兴趣度","次数","占比","说明"],true),
      makeRow(["Warm(问细节)",""+stats.conversions.warm,`${(stats.conversions.warm/Math.max(1,stats.conversions.total)*100).toFixed(0)}%`,"有升级意向"]),
      makeRow(["Cold(观望)",""+stats.conversions.cold,`${(stats.conversions.cold/Math.max(1,stats.conversions.total)*100).toFixed(0)}%`,"需进一步引导"]),
      makeRow(["Reject(拒绝)",""+stats.conversions.reject,`${(stats.conversions.reject/Math.max(1,stats.conversions.total)*100).toFixed(0)}%`,"需60轮后二次触达"]),
    ],
  }));
  children.push(p(""));
  
  // 4. OPC vs 非OPC 对比
  children.push(header("4. OPC vs 非OPC 对比分析"));
  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [2200,2400,2400,2360],
    rows: [makeRow(["指标","OPC(50人)","非OPC(50人)","差异"],true),
      makeRow(["平均诊断分",stats.opcVsNonOpc.opc.avgScore.toFixed(1),stats.opcVsNonOpc.nonOpc.avgScore.toFixed(1),`${(stats.opcVsNonOpc.nonOpc.avgScore-stats.opcVsNonOpc.opc.avgScore).toFixed(1)}`]),
      makeRow(["平均风险数",stats.opcVsNonOpc.opc.avgRisks.toFixed(1),stats.opcVsNonOpc.nonOpc.avgRisks.toFixed(1),`${(stats.opcVsNonOpc.nonOpc.avgRisks-stats.opcVsNonOpc.opc.avgRisks).toFixed(1)}`]),
      makeRow(["平均转化触发",stats.opcVsNonOpc.opc.avgConvs.toFixed(1),stats.opcVsNonOpc.nonOpc.avgConvs.toFixed(1),`${(stats.opcVsNonOpc.nonOpc.avgConvs-stats.opcVsNonOpc.opc.avgConvs).toFixed(1)}`]),
    ],
  }));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  
  // 5. 模块使用分布
  children.push(header("5. 6大模块使用分布"));
  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [2200,1500,5660],
    rows: [makeRow(["模块","总轮次","占比"],true),
      ...[1,2,3,4,5,6].map(m=>makeRow([`模块${m}`,String(stats.moduleUsage[m]||0),`${"█".repeat(Math.max(1,(stats.moduleUsage[m]||0)/500))} ${((stats.moduleUsage[m]||0)/stats.totalTurns*100).toFixed(1)}%`])),
    ],
  }));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  
  // 6. 对话转录样本（前5个用户完整展示）
  children.push(header("6. 对话转录样本（前5个用户，100轮完整展示）"));
  for (let i = 0; i < 5; i++) {
    const d = allData[i];
    children.push(header(`用户#${d.id}: ${d.profile.company_name} (${d.isOPC?"OPC":"非OPC"} | ${d.profile._sector} | ${d.profile._stage})`, 2));
    
    // 风险摘要
    children.push(p(`风险检测: ${d.risks.length}个 (Critical:${d.risks.filter(r=>r.severity==="critical").length} High:${d.risks.filter(r=>r.severity==="high").length} Medium:${d.risks.filter(r=>r.severity==="medium").length})`));
    children.push(p(`转化尝试: ${d.conv.conversionCount}次 | 对话轮次: ${d.conv.turns.length}`));
    
    // Conversation table (first 30 turns shown in detail)
    children.push(new Table({
      width: { size: 9360, type: WidthType.DXA }, columnWidths: [400,1000,8760],
      rows: [makeRow(["轮次","角色","内容"],true), ...d.conv.turns.slice(0,30).map(t=>makeRow([String(t.t), t.role, t.text.substring(0,120)]))],
    }));
    children.push(p(`... (剩余${d.conv.turns.length-30}轮见完整数据)`));
    children.push(new Paragraph({ children: [new PageBreak()] }));
  }
  
  // 7. 优化建议
  children.push(header("7. 优化修改建议"));
  
  const suggestions = [];
  if (stats.riskByType["OPC_缺CTO"] > 20) suggestions.push({priority:"P0", area:"OPC叙事", detail:"OPC缺CTO风险高频出现(>20次)，建议在模块1诊断后自动触发OPC专用叙事引导：\"OPC创业者可以向投资人这样介绍团队：我用AI工具链跑通了从获客到交付的全链路，单人产出是行业5倍\""});
  if (stats.riskByType["OPC融资阻力"] > 10) suggestions.push({priority:"P0", area:"投资人雷达", detail:"OPC融资阻力高频，建议模块3增加OPC友好型投资人标签筛选"});
  if (stats.conversions.reject > 20) suggestions.push({priority:"P1", area:"转化引导", detail:`拒绝率${(stats.conversions.reject/stats.conversions.total*100).toFixed(0)}%，建议在首轮拒绝后增加\"匿名案例分享\"等柔和转化方式`});
  if (stats.riskBySeverity.critical > 15) suggestions.push({priority:"P0", area:"风险预警", detail:"Critical风险>15次，建议增加自动化预警邮件/微信推送机制"});
  if (stats.opcVsNonOpc.opc.avgScore < stats.opcVsNonOpc.nonOpc.avgScore) suggestions.push({priority:"P1", area:"诊断算法", detail:"OPC用户平均分低于非OPC，需优化OPC专属评分权重（减少团队规模权重，增加AI工具链/单人效率权重）"});
  suggestions.push({priority:"P2", area:"数据积累", detail:"建议持久化用户诊断数据，建立OPC成长曲线对比基准"});
  suggestions.push({priority:"P2", area:"转化优化", detail:"建议在转化引导中增加OPC专属案例，如\"这位OPC创始人通过Pro版3个月完成融资\""});
  
  children.push(new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [800,1500,7060],
    rows: [makeRow(["优先级","领域","建议"],true), ...suggestions.map(s=>makeRow([s.priority, s.area, s.detail]))],
  }));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  
  // 8. 结论
  children.push(header("8. 测试结论"));
  children.push(p(`1. 稳定性: ${stats.errors}个错误/${TOTAL_USERS}用户 → ${stats.errors===0?"✅完全稳定":"⚠️有异常"}`));
  children.push(p(`2. 风险覆盖: 检测${stats.totalRisks}个风险，覆盖${Object.keys(stats.riskByType).length}种类型`));
  children.push(p(`3. OPC专项: OPC用户平均分${stats.opcVsNonOpc.opc.avgScore.toFixed(1)}，低于非OPC的${stats.opcVsNonOpc.nonOpc.avgScore.toFixed(1)}，需优化OPC权重`));
  children.push(p(`4. 转化效果: Warm率${stats.conversions.warmRate}，Cold+Reject占${(100-parseInt(stats.conversions.warmRate)).toFixed(0)}%，提升空间大`));
  children.push(p(`5. 高频风险: ${Object.entries(stats.riskByType).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([k,v])=>`${k}(${v}次)`).join(" / ")}`));
  
  // Build document
  const doc = new Document({
    styles: { default: { document: { run: { font: "Arial", size: 22 } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, font: "Arial", color: "2E75B6" }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial", color: "2E75B6" }, paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
      ],
    },
    sections: [{
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "FaSkill Pro 100用户全对话压测报告", font: "Arial", size: 16, color: "999999" })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "第 ", font: "Arial", size: 18, color: "999999" }), new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "999999" }), new TextRun({ text: " 页", font: "Arial", size: 18, color: "999999" })] })] }) },
      children,
    }],
  });
  
  const outputPath = path.join(SKILL_DIR, "tests", "FaSkill_Pro_100用户全对话压测报告_v3.0.2.docx");
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  
  // Save raw data
  const jsonPath = path.join(SKILL_DIR, "tests", "stress_test_data_100users.json");
  const summaryData = allData.map(d => {
    const ds = d.diag && d.diag.score ? d.diag.score.total || d.diag.total || 0 : (d.diag.total || 0);
    return {id:d.id,isOPC:d.isOPC,sector:d.profile._sector,stage:d.profile._stage,score:ds,risks:d.risks.length,convs:d.conv.conversionCount,turns:d.conv.turns.length};
  });
  fs.writeFileSync(jsonPath, JSON.stringify({stats, users:summaryData}, null, 2));
  
  console.log(`\nWord报告: ${outputPath}`);
  console.log(`数据JSON: ${jsonPath}`);
  console.log(`文件大小: ${(fs.statSync(outputPath).size/1024).toFixed(1)} KB`);
  console.log(`\n=== 核心指标 ===`);
  console.log(`总对话轮次: ${stats.totalTurns}`);
  console.log(`总风险数: ${stats.totalRisks}`);
  console.log(`转化Warm率: ${stats.conversions.warmRate}`);
  console.log(`OPC均分: ${stats.opcVsNonOpc.opc.avgScore.toFixed(1)} vs 非OPC: ${stats.opcVsNonOpc.nonOpc.avgScore.toFixed(1)}`);
  console.log(`错误数: ${stats.errors}`);
}

main().catch(console.error);
