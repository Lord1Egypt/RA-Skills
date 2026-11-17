#!/usr/bin/env node
// bin/opphub-knowledge-discover.js · v4.0
// status: implemented (v4 P1-4 --name 强校验)
//
//   bot 全自动查工商/业务/招聘/项目/memory/wiki
//   输出 rawText (供阶段 2 拆卡用)
//
// 用法: bot 调
//   opphub knowledge-discover --name "睿驰嘉禾" --json
// 返 { ok, name, rawText, sources: [{category, name, status, snippet}], durationMs }
//
// 实现注意:
//   - 本 bin 是 wrapper, 真"查"在 OpenClaw skill turn 里调 web_search/web_fetch/memory_search/wiki_search
//   - 本 bin 把 rawText 拼成结构化字符串, 阶段 2 拆卡读这个
//
// skill turn 流程:
//   1. bot 调 web_search "<公司名> 工商 业务" 拿工商信息
//   2. bot 调 web_search "<公司名> 招聘" 拿岗位关键词
//   3. bot 调 web_search "<公司名> 案例 客户" 拿项目
//   4. bot 调 memory_search + wiki_search (本机参考)
//   5. bot 把所有结果拼成 rawText, 调本 bin --raw-text "<rawText>" --json
//   6. 本 bin 返 ok, rawText 透传 (本 bin 不做实际查询)
//
// 真正接入 LLM 工具是 skill turn 的事, 本 bin 只负责:
//   - 接受 bot 拼好的 rawText (--raw-text) 透传
//   - 或者 接受 bot 传的 --name 由本 bin 生成查询提示 (skill turn 据此调 LLM)
//
//
// 不做的事:
//   - 不真调 LLM/web (那是 skill turn 的活)
//   - 不入库 (阶段 5 才入库)

import { join } from "node:path";
import { homedir } from "node:os";
import { existsSync, readFileSync } from "node:fs";

// v4.0.9: rawText 顶部加版本头, 让 server 端能识别协议版本
//   v1 (当前): 自由文本, 不锁结构, 内容是 LLM 自由拼出来的 rawText
//   v2 (未来): 加结构化字段 (parseKeyFields 强校验)
function ensureVersionHeader(rawText) {
  if (!rawText) return rawText;
  if (rawText.startsWith("<!-- opphub-raw-text-v1 -->")) return rawText;
  return `<!-- opphub-raw-text-v1 -->\n${rawText}`;
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--name") args.name = argv[++i];
    else if (a === "--raw-text") args.rawText = argv[++i];
    else if (a === "--web-results") args.webResults = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

// 阶段 1 数据源骨架 (skill turn 按这个顺序调 LLM 工具)
const SOURCE_SKELETON = [
  { category: "web", name: "工商信息", query: "{name} 工商信息 法人 注册资本", purpose: "名称 / 法人 / 注册资本 / 行业 / 地址" },
  { category: "web", name: "业务描述", query: "{name} 业务 主营 产品 服务", purpose: "业务描述 / 公司大事记" },
  { category: "web", name: "招聘岗位", query: "{name} 招聘 岗位 任职要求", purpose: "岗位关键词推断业务 / 团队规模" },
  { category: "web", name: "项目案例", query: "{name} 项目 案例 客户 服务", purpose: "已服务客户 / 案例" },
  { category: "memory", name: "本机 memory", query: "{name}", purpose: "历史对话是否提过该公司 (仅参考)" },
  { category: "wiki", name: "本机 wiki", query: "{name}", purpose: "历史 wiki 是否有相关条目 (仅参考)" },
];

function buildQueryPlan(name) {
  return SOURCE_SKELETON.map((s) => ({
    category: s.category,
    name: s.name,
    query: s.query.replace(/\{name\}/g, name),
    purpose: s.purpose,
  }));
}

function buildRawTextSkeleton(name) {
  // skill turn 按这个骨架填入 LLM/web 调的实际结果
  const skeleton = `# ${name} · 自动画像 (skill turn 阶段 1 拼骨架)\n\n` +
    SOURCE_SKELETON.map((s, i) => `## ${i + 1}. ${s.name}\n(${s.purpose})\n\n`).join("");
  return `<!-- opphub-raw-text-v1 -->\n${skeleton}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  // v4.0.0 P1-4: 强校验 name + raw-text 必传
  //   之前: --name 缺也能跑 (会返 "未指定, 由 rawText 推断" 但 rawText 缺公司名会跑不下去)
  //   修: 两者必须同时传, --name 单独传走 query-plan 模式, --raw-text 单独传返 invalid_input
  if (!args.name) {
    const result = {
      ok: false,
      error: "missing_name",
      message: "需要 --name \"公司名\" (必填, v4.0.0 P1-4 强校验)",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  // raw-text 单独传 → 拒绝 (v4 强校验, rawText 必须跟 --name 一起)
  if (args.rawText && args.name && !args.rawText.trim()) {
    const result = {
      ok: false,
      error: "empty_raw_text",
      message: "--raw-text 传了但内容为空",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  const t0 = Date.now();

  // raw-text 透传模式 (必须 --name + --raw-text 同时存在)
  if (args.rawText) {
    let webResults = null;
    if (args.webResults) {
      try {
        webResults = JSON.parse(args.webResults);
      } catch {
        if (existsSync(args.webResults)) {
          try {
            webResults = JSON.parse(readFileSync(args.webResults, "utf8"));
          } catch {
            // ignore, webResults 保持 null
          }
        }
      }
    }
    const validation = validateRawText(args.name || "", args.rawText, webResults);
    const result = {
      ok: validation.ok,
      mode: "raw-text-passthrough",
      name: args.name,  // v4.0.0 P1-4: 必填, 不再是 "(未指定, 由 rawText 推断)"
      rawText: ensureVersionHeader(args.rawText),
      sources: [
        { category: "passthrough", name: "bot_skill_turn", status: "received" },
      ],
      validation: {
        ok: validation.ok,
        issues: validation.issues,
        warnings: validation.warnings,
        suggestions: validation.suggestions || [],
      },
      durationMs: Date.now() - t0,
      nextStep: validation.ok
        ? "knowledge-card --raw-text <rawText>"
        : (validation.suggestions && validation.suggestions.length > 0)
          ? "ask user to confirm suggested company name, then re-run with --name <correct>"
          : "ask user to re-input company name",
    };
    if (validation.issues.length > 0) {
      result.error = validation.issues.map((i) => i.message).join("; ");
    }
    if (wantJson) {
      console.log(JSON.stringify(result, null, 2));
      if (!validation.ok) process.exit(1);
    } else {
      if (validation.ok) {
        console.log(`✅ rawText received (${args.rawText.length} chars), next: knowledge-card`);
      } else {
        console.log(`❌ rawText 验证失败:`);
        for (const i of validation.issues) console.log(`  [${i.severity}] ${i.type}: ${i.message}`);
      }
      for (const w of validation.warnings) console.log(`  ⚠️ ${w.type}: ${w.message}`);
      if (validation.suggestions && validation.suggestions.length > 0) {
        console.log(`\n💡 拼写纠错候选 (top ${validation.suggestions.length}):`);
        for (const s of validation.suggestions) {
          console.log(`  📌 ${s.name} (相似度 ${(s.similarity * 100).toFixed(0)}%)`);
        }
      }
    }
    if (!validation.ok) process.exit(1);
    return;
  }

  // --name 模式: 返骨架 + 查询计划 + 强制搜索指令
  const queryPlan = buildQueryPlan(args.name);
  const rawTextSkeleton = buildRawTextSkeleton(args.name);
  const searchTasks = queryPlan.map((q, i) => `第${i + 1}步: 用 ${q.category === "web" ? "web_search" : q.category === "memory" ? "memory_search" : "wiki_search"} 搜 "${q.query}" → 填入 rawText 的 ## ${i + 1}. ${q.name} 节`);
  const result = {
    ok: true,
    mode: "query-plan",
    name: args.name,
    queryPlan,
    rawTextSkeleton,
    sources: queryPlan.map((q) => ({ ...q, status: "pending_skill_turn" })),
    durationMs: Date.now() - t0,
    nextStep: "skill turn 调 LLM/web 工具填骨架, 然后 --raw-text <filledRawText> 重跑",
    _explicitInstructions: [
      "‼️ 你必须执行以下搜索, 不能省略或跳过:",
      ...searchTasks,
      `第${queryPlan.length + 1}步: 把所有搜索结果拼成 rawText (每节搜到真实内容, 含业务描述/价格/案例)`,
      `第${queryPlan.length + 2}步: 调 opphub knowledge-discover --name "${args.name}" --raw-text "<rawText>" --json 验证`,
      "‼️ 禁止: 传空骨架或占位符通过! 校验会检测骨架填空内容并拒绝。必须搜到实际数据。",
      "‼️ 业务描述节: 必须包含具体能力介绍+价格(如 KOL投放单次5-50万, 月费2-5万等)",
      "‼️ 项目案例节: 列具体客户行业",
    ].join("\n"),
  };
  if (wantJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`📋 阶段 1 骨架生成: ${args.name}`);
    console.log(`queryPlan: ${queryPlan.length} 个数据源`);
    for (const q of queryPlan) {
      console.log(`  [${q.category}] ${q.name}: ${q.query}`);
    }
    console.log(`\n‼️ 你必须用 web_search 搜索每一节, 填入真实数据后重跑`);
    console.log(`  禁止: 传空骨架, 校验会拒绝`);
  }
}

const SKELETON_PATTERNS = [
  "名称 / 法人", "注册资本 / 行业", "业务描述 / 公司大事记",
  "岗位关键词推断业务", "已服务客户 / 案例",
  "历史对话是否提过该公司", "历史 wiki 是否有相关条目",
];

// raw-text 模式增加: 公司名验证 + rawText 完整性检查 + 拼写纠错候选
function validateRawText(name, rawText, webResults) {
  const issues = [];
  const warnings = [];
  let ok = true;

  // 0. 骨架检测: rawText 包含 skeleton placeholder 填空内容 → 拒绝
  for (const p of SKELETON_PATTERNS) {
    if (rawText.includes(p)) {
      issues.push({
        type: "skeleton_unfilled",
        severity: "error",
        message: `rawText 含骨架填空内容 "${p}"。禁止传空骨架通过。你必须用 web_search 搜真实数据填充每一节, 再重试。6 个搜索: 工商信息(法人/注册资本/行业/地址)、业务描述(主营/产品/服务/价格)、招聘岗位(岗位关键词/团队规模)、项目案例(客户/案例)、memory、wiki`,
      });
      ok = false;
      break;
    }
  }
  if (!ok) return { ok, issues, warnings, suggestions: [] };

  // 1. 公司名验证: rawText 里必须出现公司名核心 (>=4 字) 或其简体
  const nameCore = name.replace(/^(上海|北京|广州|深圳|杭州|成都|南京|武汉|苏州|天津|重庆)/, "").replace(/(有限公司|股份有限公司|集团|公司)$/, "").trim();
  let nameFound = false;
  if (nameCore && nameCore.length >= 2) {
    nameFound = rawText.includes(nameCore) || rawText.includes(name);
  }
  if (!nameFound && rawText.length > 0) {
    issues.push({
      type: "company_name_not_found",
      severity: "error",
      message: `rawText 里没找到公司名 "${name}" (核心: "${nameCore}"), 可能是拼错了公司名`,
    });
    ok = false;
  }

  // 2. rawText 完整性: 计算 "未找到 / 未搜到 / 拼写 / 疑似" 等关键词出现次数
  const missingKeywords = ["未找到", "未搜到", "拼写错误", "疑似拼错", "找不到", "no result", "not found"];
  const missingCount = missingKeywords.reduce((acc, kw) => {
    const matches = rawText.match(new RegExp(kw, "g"));
    return acc + (matches ? matches.length : 0);
  }, 0);
  const sectionCount = (rawText.match(/^##\s+\d+\./gm) || []).length;
  const missingRatio = sectionCount > 0 ? missingCount / sectionCount : 0;
  if (missingRatio > 0.5 && missingCount >= 2) {
    issues.push({
      type: "rawtext_incomplete",
      severity: "error",
      message: `rawText 里 ${missingCount} 个 "未找到" / "拼写错误" 等关键词, 占比 ${(missingRatio * 100).toFixed(0)}% (> 50%). skill turn 查不到数据, 不该拆卡入库`,
    });
    ok = false;
  } else if (missingCount >= 1) {
    warnings.push({
      type: "rawtext_partial",
      message: `rawText 含 ${missingCount} 个 "未找到" 关键词, skill turn 部分数据未查到`,
    });
  }

  let suggestions = [];
  if (!ok && webResults && Array.isArray(webResults)) {
    suggestions = suggestCorrections(name, webResults);
    if (suggestions.length > 0) {
      warnings.push({
        type: "spelling_suggestions",
        suggestions: suggestions.map((s) => ({ name: s.name, similarity: s.similarity })),
        message: `识别到 ${suggestions.length} 个相似公司名候选, 是否拼错了?`,
      });
    }
  }

  return { ok, issues, warnings, suggestions };
}

// 编辑距离 (Levenshtein)
function levenshtein(a, b) {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
  const m = [];
  for (let i = 0; i <= b.length; i++) m[i] = [i];
  for (let j = 0; j <= a.length; j++) m[0][j] = j;
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      m[i][j] = b[i - 1] === a[j - 1]
        ? m[i - 1][j - 1]
        : Math.min(m[i - 1][j - 1] + 1, m[i][j - 1] + 1, m[i - 1][j] + 1);
    }
  }
  return m[b.length][a.length];
}

// 相似度 (0-1, 1=完全相同)
function similarity(a, b) {
  if (!a || !b) return 0;
  const dist = levenshtein(a, b);
  const maxLen = Math.max(a.length, b.length);
  return 1 - dist / maxLen;
}

// webResults: bot web_search 返回的 [{title, link, snippet}, ...]
// 提取 title/snippet 里的公司名 (正则: Xxx公司 / Xxx有限公司 / Xxx集团 / Xxx工作室)
function suggestCorrections(name, webResults) {
  const seen = new Set();
  const candidates = [];
  for (const r of webResults) {
    const text = `${r.title || ""} ${r.snippet || ""}`;
    const matches = text.match(/[\u4e00-\u9fa5（）()A-Za-z0-9·]{2,30}(?:有限公司|股份有限公司|集团|公司|工作室|事务所)/g) || [];
    for (const m of matches) {
      const cleanName = m.replace(/[（）()]/g, "").trim();
      if (cleanName === name || seen.has(cleanName)) continue;
      seen.add(cleanName);
      // 去前缀 + 去后缀
      const stripCore = (s) => {
        let r = s.replace(/^(上海|北京|广州|深圳|杭州|成都|南京|武汉|苏州|天津|重庆)/, "");
        for (const suf of ["有限公司", "股份有限公司", "集团", "事务所", "工作室"]) {
          r = r.replace(new RegExp(suf + "$"), "");
        }
        return r.trim();
      };
      const nameCore = stripCore(name);
      const candCore = stripCore(cleanName);
      // 组合相似度: 取 max(核心对比, 首 4 字对比)
      //   - 核心对比: 防业务后缀 (数字传媒科技) 拉低相似度
      //   - 首 4 字: 防全名太长让小差异被淹没 (睿驰佳禾 vs 睿驰嘉禾数字传媒科技 4字差异)
      const simCore = similarity(nameCore, candCore);
      const simPrefix = nameCore.length >= 3 && candCore.length >= 3
        ? similarity(nameCore.slice(0, 4), candCore.slice(0, 4))
        : 0;
      const containMatch = nameCore.length >= 2 && candCore.includes(nameCore);
      const containMatch2 = candCore.length >= 2 && nameCore.includes(candCore);
      const finalSim = containMatch || containMatch2 ? Math.max(simCore, simPrefix, 0.9) : Math.max(simCore, simPrefix);
      if (finalSim >= 0.5) {
        candidates.push({ name: cleanName, similarity: finalSim });
      }
    }
  }
  candidates.sort((a, b) => b.similarity - a.similarity);
  return candidates.slice(0, 3);
}

main().catch((e) => {
  console.error("opphub-knowledge-discover fatal:", e?.message ?? e);
  process.exit(1);
});
