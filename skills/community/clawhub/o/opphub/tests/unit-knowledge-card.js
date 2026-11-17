#!/usr/bin/env node
//
// unit tests for opphub-knowledge-card.js · v5.0
// 覆盖:
//   - parseRawText: 把 ### heading 拆成 (type, dimension, description)
//   - extractEvidenceCandidates: 纯 n-gram 频次排名, 无词表
//   - extractParsedFields: 工商信息节抽取 (法人/注册资本/城市)
//   - 占位符: rawText 含 <待 LLM 填写>
//
// 通过 spawn 卡生成 CLI, 读 rawText + 期望字段, 验证出卡正确.
//
// 用法: node --test tests/unit-knowledge-card.js

import test from "node:test";
import assert from "node:assert";
import { readFileSync } from "node:fs";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CARD_BIN = join(__dirname, "..", "bin", "opphub-knowledge-card.js");
const SKILL_CWD = join(__dirname, "..");
const CARD_SOURCE = readFileSync(CARD_BIN, "utf8")
  // 去掉 // 行注释, 剩下的才视为可执行代码
  .split("\n").filter(l => !l.trim().startsWith("//")).join("\n");
const execFileP = promisify(execFile);

async function runCard(name, rawText) {
  const { stdout } = await execFileP(
    "node",
    [CARD_BIN, "--name", name, "--raw-text", rawText, "--json"],
    { cwd: SKILL_CWD, timeout: 15000 },
  );
  return JSON.parse(stdout.toString());
}

function getCard(cards, dimension) {
  return cards.find(c => c.dimension === dimension);
}

// ────────────────────────────────────────────────────────────
// 通用性保证: 源码绝对不许有业务词
// ────────────────────────────────────────────────────────────
test("通用性: 源码不许写业务词表 (平台/服务/MCN)", () => {
  const forbidden = [
    "抖音", "快手", "小红书", "B 站",
    "MCN", "SaaS", "撮合引擎", "向量检索",
    "达人营销", "短视频内容制作", "平台代运营", "电商转化",
    "PLATFORM_TERMS", "TAIL_GENERIC", "MID_GENERIC", "GENERIC_TERMS",
    "INDUSTRY_TEMPLATES", "INDUSTRY_SIGNALS",
  ];
  const leaks = forbidden.filter(w => CARD_SOURCE.includes(w));
  assert.strictEqual(leaks.length, 0, `源码含业务词硬编码: ${leaks.join(", ")}`);
});

// ────────────────────────────────────────────────────────────
// parseRawText: ### heading 拆解
// ────────────────────────────────────────────────────────────
test("parseRawText: 多 ## 节 + 部分节没 ### 子标题也不能吞后面节", async () => {
  // bug 守卫: 之前 "## 1. 工商信息" 没 ###, 内层 j 循环跑到文件尾,
  // 吞掉后面所有 ## 节, 修后必须能正确切到下一节
  const d = await runCard("公司X", `
## 1. 工商信息
法人: 张三
注册资本: 1000万
## 2. 业务描述
### 能力A
做 A 的事
### 能力B
做 B 的事
## 3. 上游依赖
### 资源X
找资源 X
## 4. 下游客户
### 客户Y
找客户 Y
`);
  const byName = Object.fromEntries(d.cards.map(c => [c.dimension, c.type]));
  // 4 张卡必须全有
  assert.strictEqual(d.cards.length, 4, "4 个 ### 必须全出");
  assert.strictEqual(byName["能力A"], "ability");
  assert.strictEqual(byName["能力B"], "ability");
  assert.strictEqual(byName["资源X"], "upstream", `资源X 必是 upstream, 实际 ${byName["资源X"]}`);
  assert.strictEqual(byName["客户Y"], "downstream", `客户Y 必是 downstream, 实际 ${byName["客户Y"]}`);
});

test("parseRawText: ## 2. 业务描述 节下 ### 子标题全部出 ability 卡", async () => {
  const d = await runCard("上海睿驰", `
## 2. 业务描述
### 达人营销
从达人筛选, 商务谈判到投放执行。覆盖抖音等平台。
### 短视频内容制作
月产 100+ 条短视频。
`);
  assert.strictEqual(d.cards.length, 2);
  assert.strictEqual(d.cards[0].type, "ability");
  assert.strictEqual(d.cards[0].dimension, "达人营销");
  assert.strictEqual(d.cards[1].dimension, "短视频内容制作");
});

test("parseRawText: ### 上游/下游/同业 类型自动判定", async () => {
  const d = await runCard("上海睿驰", `
## 业务描述
### 达人营销
xxx
### 上游依赖
找 KOL 资源
### 下游客户
找品牌方
### 同业联盟
对标 MCN 同行
`);
  const byName = Object.fromEntries(d.cards.map(c => [c.dimension, c.type]));
  assert.strictEqual(byName["达人营销"], "ability");
  assert.strictEqual(byName["上游依赖"], "upstream");
  assert.strictEqual(byName["下游客户"], "downstream");
  assert.strictEqual(byName["同业联盟"], "peer");
});

test("parseRawText: 任何公司名, rawText 里写啥就拆啥", async () => {
  // 律所
  const d1 = await runCard("北京金杜律师事务所", `
## 业务描述
### 公司诉讼
代理知识产权侵权诉讼, 客户年案值 5000 万+。
### 公司合规
合同审查 200+ 客户, 平均 3-5 个工作日交付。
`);
  assert.strictEqual(d1.cards.length, 2);
  assert.strictEqual(d1.cards[0].dimension, "公司诉讼");
  // 餐饮
  const d2 = await runCard("海底捞", `
## 业务描述
### 火锅堂食
全国 1300+ 门店, 单店日均客流 800+。
### 外卖配送
30 分钟覆盖 5 公里, 月单量 2000 万+。
`);
  assert.strictEqual(d2.cards.length, 2);
  assert.strictEqual(d2.cards[1].dimension, "外卖配送");
});

// ────────────────────────────────────────────────────────────
// extractEvidenceCandidates: 纯 n-gram 排名, 无业务词表
// ────────────────────────────────────────────────────────────
test("extractEvidenceCandidates: 上限 30 个, 频次优先", async () => {
  const d = await runCard("公司X", `
## 业务描述
### 达人营销
我们做达人筛选, 达人筛选, 商务谈判。覆盖抖音, 快手, 小红书。
`);
  const card = getCard(d.cards, "达人营销");
  assert.ok(card, "卡必出");
  assert.ok(card.evidenceCandidates.length > 0, "至少 1 个候选");
  assert.ok(card.evidenceCandidates.length <= 30, "不超过 30");
  // 频次高的 "达人筛选" 出现 2 次, 排名靠前
  const idx = card.evidenceCandidates.indexOf("达人筛选");
  assert.ok(idx >= 0, "达人筛选必在候选列表里");
  assert.ok(idx < 5, `"达人筛选" 应排在前面, 实际 idx=${idx}`);
});

test("extractEvidenceCandidates: 律所/餐饮关键词也能提取 (通用)", async () => {
  const d = await runCard("测试公司", `
## 业务描述
### 公司诉讼
知识产权侵权诉讼代理。客户包括 字节跳动, 腾讯, 阿里。仲裁 商业合同争议 案件。
`);
  const card = getCard(d.cards, "公司诉讼");
  // 候选里应该有 "诉讼", "知识产权", "客户包括字节跳动" 等
  const c = card.evidenceCandidates.join(" ");
  assert.ok(c.includes("诉讼"), `候选必含 "诉讼", 实际: ${c.slice(0, 200)}`);
});

// ────────────────────────────────────────────────────────────
// rawText 占位符: <待 LLM 填写>
// ────────────────────────────────────────────────────────────
test("rawText 占位符: 每张卡含 (证据词: <待 LLM 填写>)", async () => {
  const d = await runCard("公司", `
## 业务描述
### 达人营销
xxx 内容
`);
  assert.ok(d.cards[0].text.includes("(证据词: <待 LLM 填写>)"),
    `占位符必在 rawText 里, 实际: ${d.cards[0].text.slice(0, 200)}`);
});

// ────────────────────────────────────────────────────────────
// LLM 任务包: 一次性给约束+候选+格式
// ────────────────────────────────────────────────────────────
test("evidenceAnswerPrompt: 含约束+候选+输出格式", async () => {
  const d = await runCard("公司", `
## 业务描述
### 达人营销
xxx 内容
`);
  const prompt = d.cards[0].evidenceAnswerPrompt;
  assert.ok(prompt.includes("LLM 任务"), "开头必有 LLM 任务");
  assert.ok(prompt.includes("证据词") || prompt.includes("evidence"), "必含证据词提法");
  assert.ok(prompt.includes("evidenceCandidates") || /\d 个/.test(prompt),
    "必含候选词引用");
  assert.ok(prompt.includes('"evidence"'), "必含 JSON 输出格式定义");
});

test("llmInstruction (顶层): 引导 LLM 一次性完成, 不分多步", async () => {
  const d = await runCard("公司", "## 业务描述\n### 达人营销\nxxx\n");
  assert.ok(d.llmInstruction.includes("一次性"), "顶层 instruction 强调一次性");
  assert.ok(!d.llmInstruction.includes("先 skill 输出"), "不应提分多步流程");
});

// ────────────────────────────────────────────────────────────
// extractParsedFields: 公司级结构化字段
// ────────────────────────────────────────────────────────────
test("extractParsedFields legalPerson / registeredCapital: 标准格式", async () => {
  const d = await runCard("测试法代", `
## 1. 工商信息
法人: 张三
注册资本: 1000万元
## 业务描述
### 达人营销
xxx
`);
  assert.strictEqual(d.parsedFields.legalPerson, "张三");
  assert.strictEqual(d.parsedFields.registeredCapital, "1000万元");
});

test("extractParsedFields city: 不被同业联盟里的 '北京' 污染", async () => {
  const d = await runCard("武汉测试", `
## 1. 工商信息
地址: 武汉光谷

## 业务描述
### 同业联盟
无忧传媒(北京抖音头部MCN), 热度传媒(北京短视频MCN)
`);
  assert.strictEqual(d.parsedFields.city, "武汉");
});
