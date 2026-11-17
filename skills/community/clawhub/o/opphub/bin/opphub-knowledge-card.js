#!/usr/bin/env node
// bin/opphub-knowledge-card.js · v5.0
//
// ⚠️ 不写死任何业务词 / 行业模板 / 平台字典 / 业务通用词
//   - 不写 INDUSTRY_TEMPLATES (mcn/saas/law/mfg 全删)
//   - 不写 INDUSTRY_SIGNALS (token 频率猜行业)
//   - 不写 PLATFORM_TERMS / GENERIC_TERMS / TAIL_GENERIC / MID_GENERIC
//   - 不写 hasEvidence + purpose 匹配
//
// skill 唯一职责:
//   1. 解析 rawText 里的 ### 维度标题 → 卡片
//   2. n-gram 频次排名 → 输出 30 候选词 (结构化, 无业务假设)
//   3. 把每张卡的"质量控制"包装成 LLM 任务包 (约束+候选+格式) 一并交给 LLM
//
// LLM 在对话里读完直接选候选词填写证据位. skill 不替 LLM 决定什么是"对的词".
//
// 用法:
//   opphub knowledge-card --name "公司" --raw-text "<rawText>" --json
//
// 输入 rawText 期望格式 (skill 不强制, 但 heading 解析依据这个):
//   # 公司名 · ...
//   ## 1. 工商信息
//   ...
//   ## 2. 业务描述
//   ### 维度名1
//   自然语言描述...
//   ### 维度名2
//   自然语言描述...
//   ## 3. 上游依赖 (可选, 同 heading 模式)
//   ## 4. 下游服务 (可选)
//   ## 5. 同行关系 (可选)
//
// 返:
//   {
//     ok, name, cards: [{
//       type, dimension, description, evidenceCandidates (30 个),
//       evidenceAnswerPrompt (LLM 任务包), text (含 <待 LLM 填写> 占位符),
//       ...
//     }],
//     parsedFields: { companyName, legalPerson, registeredCapital, ... },
//     cardCount, durationMs
//   }

import { join } from "node:path";
import { homedir } from "node:os";

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--name") args.name = argv[++i];
    else if (a === "--raw-text") args.rawText = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

// ───────────────────────────────────────────────────────────
// rawText 解析: 把 ### heading 拆成 (type, dimension, description)
// heading 上游/下游/同行 节 (## 3, ## 4, ## 5) 决定 type
// 其它 (## 2 业务描述) 下的 ### heading 默认 type=ability
// (但 ### 子标题名含 "上游/下游/同行" 也判定对应类型)
// ───────────────────────────────────────────────────────────
function parseRawText(rawText) {
  if (!rawText) return { sections: [], cards: [] };

  // 通用关键词映射 (按标题中的关键字判定类型, 不写死行业词)
  function inferTypeFromTitle(title) {
    if (/上游|我的依赖|依赖/.test(title)) return "upstream";
    if (/下游|我想找|客户|服务方/.test(title)) return "downstream";
    if (/同[行业]|同行|同业|竞品|对标|参考/.test(title)) return "peer";
    return "ability";
  }

  const sections = [];
  const lines = rawText.split("\n");
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const h2 = line.match(/^##\s+(.+?)\s*$/);
    if (!h2) { i++; continue; }
    const sectionTitle = h2[1].trim();
    const sectionType = inferTypeFromTitle(sectionTitle);

    // 在这个 ## 块里找所有 ### 子标题 (遇到下一个 ## 就停, 别吞后面节)
    let j = i + 1;
    while (j < lines.length) {
      const h3 = lines[j].match(/^###\s+(.+?)\s*$/);
      if (h3) {
        const dimension = h3[1].trim();
        // 抓取内容直到下一个 ### 或 ## 或 文件尾
        let k = j + 1;
        const contentLines = [];
        while (k < lines.length) {
          const l = lines[k];
          if (l.match(/^#{1,3}\s/)) break;
          contentLines.push(l);
          k++;
        }
        const description = contentLines.join("\n").trim();
        // ### 子标题名也可决定类型 (e.g. ## 2 下, ## ### 上游依赖 → upstream)
        const dimType = inferTypeFromTitle(dimension);
        const finalType = dimType !== "ability" ? dimType : sectionType;
        sections.push({ sectionTitle, type: finalType, dimension, description });
        j = k;
      } else if (lines[j].match(/^##\s/)) {
        // 遇到下一个 ## 段头, 跳出当前 ## 块的扫描
        break;
      } else {
        j++;
      }
    }
    i = j;
  }
  return { sections };
}

// ───────────────────────────────────────────────────────────
// n-gram 候选词提取 (纯结构, 不假设业务词)
//   - 标点切分
//   - 2-8 字长度
//   - 频次排名
// ───────────────────────────────────────────────────────────
function extractEvidenceCandidates(description) {
  if (!description) return [];
  const freq = new Map();

  // 拆标点 + 空白
  const tokens = description.split(/[,，。、；：:.\s\n]+/).filter(Boolean);

  for (const tok of tokens) {
    // 单 token 本身: 2-8 字, 含中文或英文, 不纯数字
    if (tok.length >= 2 && tok.length <= 8) {
      if (!/^\d+$/.test(tok)) {
        freq.set(tok, (freq.get(tok) || 0) + 1);
      }
    }
    // 长 token 滑动窗口: 切 2-8 字 n-gram
    if (tok.length > 8) {
      for (let i = 0; i <= tok.length - 2; i++) {
        for (let n = 2; n <= 8 && i + n <= tok.length; n++) {
          const w = tok.slice(i, i + n);
          if (/^\d+$/.test(w)) continue;
          freq.set(w, (freq.get(w) || 0) + 1);
        }
      }
    }
  }

  // 排序: 频次降序, 长度降序, 取前 30 候选
  return [...freq.entries()]
    .sort((a, b) => b[1] - a[1] || b[0].length - a[0].length)
    .slice(0, 30)
    .map(([term]) => term);
}

// ───────────────────────────────────────────────────────────
// LLM 任务包: 一次性把约束 + 候选 + 输出格式 给到大模型
// ───────────────────────────────────────────────────────────
function buildAnswerPrompt(type, dimension, description, candidates) {
  return [
    `## LLM 任务 (一次性完成)`,
    `你是偶合录入的 LLM 助理. 本张卡片由 skill 自动生成, 证据词由你做最后质量把控.`,
    ``,
    `卡片主题: ${type}.${dimension}`,
    `描述: ${description || "(rawText 里没找到独立的描述段)"}`,
    `候选词 (skill 从描述里 n-gram 频次排名得出, ${candidates.length} 个): ${candidates.join(", ")}`,
    ``,
    `你的选择规则:`,
    `- 必须从候选词列表里挑, 不准生造 (生造词会脱离 rawText 原意)`,
    `- 挑 3-5 个最直接相关 "${dimension}" 主题的`,
    `- 不要的: 与 ${dimension} 主题不符的 / 通用动词残留 / 噪音字符`,
    `- 兜底: 如候选全不相关, 回退 ["${dimension}"] 自身`,
    ``,
    `输出严格按 JSON 格式 (直接 print 到 stdout, 不要 markdown 代码块包裹):`,
    `{`,
    `  "evidence": ["kw1", "kw2", "kw3"]`,
    `}`,
  ].join("\n");
}

// ───────────────────────────────────────────────────────────
// 公司结构化字段 (从 ## 1. 工商信息 节 + ## 2. 业务描述 节 抽)
// ───────────────────────────────────────────────────────────
function extractParsedFields(name, rawText) {
  const ingestedAt = new Date().toISOString();
  const source = `im:skill-extract:${ingestedAt}`;
  const pairs = [["companyName", name]];

  const fields = ["法人", "注册资本", "信用代码", "统一社会信用代码",
                  "团队规模", "规模", "人数", "地址"];
  for (const f of fields) {
    const m = rawText.match(new RegExp(`${f}[:：]\\s*([^\\n]+)`));
    if (m) {
      const key = ({
        "法人": "legalPerson",
        "注册资本": "registeredCapital",
        "信用代码": "creditCode",
        "统一社会信用代码": "creditCode",
        "团队规模": "teamSize",
        "规模": "teamSize",
        "人数": "teamSize",
        "地址": "address",
      })[f];
      if (key && !pairs.find(p => p[0] === key)) {
        const v = m[1].trim();
        const limit = key === "address" ? 100 : 50;
        pairs.push([key, v.slice(0, limit)]);
      }
    }
  }

  // 城市限定: 地址字段 || 工商信息节
  const addressField = pairs.find(p => p[0] === "address")?.[1] || "";
  const bizSection = rawText.match(/##\s*1\.\s*工商信息\s*\n+([\s\S]*?)(?=\n##\s|\s*$)/);
  const searchText = addressField || (bizSection ? bizSection[1] : "");
  const cities = ["上海", "北京", "深圳", "广州", "杭州", "成都", "南京", "武汉", "苏州", "天津", "重庆"];
  for (const c of cities) {
    if (searchText.includes(c)) { pairs.push(["city", c]); break; }
  }

  // 业务描述: ## 2. 业务描述 整段
  const bizMatch = rawText.match(/##\s*2\.\s*业务描述\s*\n+([\s\S]*?)(?=\n##\s|\s*$)/);
  if (bizMatch) pairs.push(["businessDescription", bizMatch[1].trim().slice(0, 500)]);

  const fieldsObj = {};
  const sources = {};
  for (const [key, value] of pairs) {
    fieldsObj[key] = value;
    sources[key] = {
      current: value,
      userOverride: null,
      userOverrideAt: null,
      candidates: [{ value, source, sourceType: "im", ingestedAt }],
    };
  }
  fieldsObj._sources = sources;
  return fieldsObj;
}

// ───────────────────────────────────────────────────────────
// 主生成函数
// ───────────────────────────────────────────────────────────
function generateCards(name, rawText) {
  const { sections } = parseRawText(rawText);
  const cards = [];

  for (const sec of sections) {
    const description = sec.description;
    const candidates = extractEvidenceCandidates(description);
    const answerPrompt = buildAnswerPrompt(sec.type, sec.dimension, description, candidates);

    // rawText 占位符: <待 LLM 填写>, 让 LLM 在对话里把 (证据词: ...) 整行替换
    const labelMap = { ability: "能力卡片", upstream: "上游依赖", downstream: "下游服务", peer: "同行关系" };
    const label = labelMap[sec.type] || sec.type;
    const cardText = description
      ? `<!-- opphub-raw-text-v1 -->\n${name} · ${label} · ${sec.dimension}\n\n描述: ${description}\n\n(证据词: <待 LLM 填写>)`
      : `<!-- opphub-raw-text-v1 -->\n${name} · ${label} · ${sec.dimension}\n\n(描述: rawText 里没找到该维度的独立描述段)\n\n(证据词: <待 LLM 填写>)`;

    cards.push({
      type: sec.type,
      dimension: sec.dimension,
      description,
      evidenceCandidates: candidates,
      evidenceAnswerPrompt: answerPrompt,
      text: cardText,
    });
  }

  return { cards, sectionsCount: sections.length };
}

// ───────────────────────────────────────────────────────────
// LLM 总任务包 (整个公司级别, 一次性交付)
// ───────────────────────────────────────────────────────────
function buildGlobalPrompt(name, cards) {
  return [
    `## LLM 任务 (一次性完成: 给所有卡片选证据词)`,
    `你是偶合录入的 LLM 助理. skill 已从 "${name}" 的 rawText 拆出 ${cards.length} 张卡片, 每张卡的证据词由你做最后质量把控.`,
    ``,
    `流程:`,
    `1. 逐卡读 cards[].description + cards[].evidenceCandidates`,
    `2. 按 cards[].evidenceAnswerPrompt 里的规则, 给每张卡的 "evidence" 字段赋值`,
    `3. 把 cards[i].text 里的 "(证据词: <待 LLM 填写>)" 整行替换为 "(证据词: kw1, kw2, kw3)"`,
    `4. 调用 opphub knowledge-submit --cards <填写完整 rawText 的 cards.json>`,
    ``,
    `⚠️ 切勿分成 "skill 先输出 → 等用户确认 → 再审" 的多步流程. skill 给的本题包已含 evidenceCandidates, 你读 + 选 + 重写 + 提交, 一次性完成.`,
  ].join("\n");
}

// ───────────────────────────────────────────────────────────
// main
// ───────────────────────────────────────────────────────────
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  if (!args.rawText) {
    const result = {
      ok: false,
      error: "missing_raw_text",
      message: "需要 --raw-text (stage 1 discover 填好的)",
      nextStep: "opphub knowledge-card --raw-text '<filled rawText>' --json",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.error(result.message);
    return;
  }

  const t0 = Date.now();
  const name = args.name || extractNameFromRawText(args.rawText);
  const { cards } = generateCards(name, args.rawText);
  const fields = extractParsedFields(name, args.rawText);

  const result = {
    ok: cards.length > 0,
    warning: cards.length === 0 ? "rawText 里没解析到任何 ### heading, 没法拆卡 — 检查 rawText 格式或重新跑 discover" : null,
    name,
    cards,
    parsedFields: fields,
    cardCount: cards.length,
    durationMs: Date.now() - t0,
    llmInstruction: buildGlobalPrompt(name, cards),
    nextStep: cards.length === 0
      ? "检查 rawText 格式, 在 ## 2. 业务描述 节用 ### heading 列维度"
      : "LLM 读 llmInstruction + cards[].evidenceAnswerPrompt, 逐卡填 (证据词:) 占位符, 然后调用 opphub knowledge-submit --cards <填写完成 cards.json>",
  };

  if (cards.length === 0) {
    result.error = "no_section_headings_found";
  }

  if (wantJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`📋 ${name}: ${cards.length} 张卡片 (parsed from ### heading)`);
    for (const c of cards) {
      console.log(`  ${c.type === "ability" ? "✅" : c.type === "upstream" ? "⬆️" : c.type === "downstream" ? "⬇️" : "🔗"} [${c.type}] ${c.dimension} — 候选 ${c.evidenceCandidates.length} 个`);
    }
    console.log(`\n下一步: ${result.nextStep}`);
  }
  if (cards.length === 0 && wantJson) process.exit(1);
}

function extractNameFromRawText(rawText) {
  const m = (rawText || "").match(/^#\s+(.+?)\s+·/);
  return m ? m[1].trim() : "(未指定公司名)";
}

main().catch((e) => {
  console.error("opphub-knowledge-card fatal:", e?.message ?? e);
  process.exit(1);
});
