#!/usr/bin/env node
// bin/opphub-find-peers.js · v1.0
// 找同行: 根据当前 OPC 的行业 + 能力关键词, 匹配其他 OPC 的 PUBLIC 公开画像
//
// 用法:
//   opphub find-peers --api-base <url> --token <jwt> --user-id <userId> [--json]
// 返 { ok, myIndustry, myAbilities, peers: [{companyName, industry, userId, matchScore, matchedDimensions: string[]}], total }
//
// 依赖:
//   - API GET /api/knowledge?scope=public&entryType=ability

import { argv, exit } from "node:process";

const args = parseArgs(argv.slice(2));
const API_BASE = args.apiBase || "https://api.opphub.ruiplus.cn";
const TOKEN = args.token || "";
const USER_ID = args.userId || "";
const WANT_JSON = args.json;
const MIN_SCORE = parseFloat(args.minScore || "0.3");

if (!TOKEN || !USER_ID) {
  out({ ok: false, error: "missing_args", message: "--token 和 --user-id 必填" }, WANT_JSON);
  exit(1);
}

async function main() {
  // 1. 获取自己的 ability 维度
  const myResp = await fetch(`${API_BASE}/api/knowledge?userId=me`, {
    headers: { authorization: "Bearer " + TOKEN },
  });
  const myData = await myResp.json();
  if (!myData.ok) {
    out({ ok: false, error: "my_query_failed", message: myData.message || "查自己失败" }, WANT_JSON);
    exit(1);
  }

  const myAbilities = (myData.data || []).filter(e => e.entryType === "ability").map(e => e.entryDimension).filter(Boolean);
  const myProfile = (myData.data || []).find(e => e.entryType === "ability" || e.entryType === "downstream");
  const myIndustry = myProfile?.parsedFields?.industry?.name || "";
  const myCity = myProfile?.parsedFields?.city || "";

  // 2. 查其他 OPC 的 PUBLIC ability
  const pubResp = await fetch(`${API_BASE}/api/knowledge?scope=public&entryType=ability`, {
    headers: { authorization: "Bearer " + TOKEN },
  });
  const pubData = await pubResp.json();
  if (!pubData.ok) {
    out({ ok: false, error: "public_query_failed", message: pubData.message || "查公开条目失败" }, WANT_JSON);
    exit(1);
  }

  // 3. 按 userId 分组, 算匹配分
  const grouped = new Map();
  for (const e of pubData.data || []) {
    if (!e.userId || !e.entryDimension) continue;
    if (!grouped.has(e.userId)) {
      grouped.set(e.userId, { userId: e.userId, companyName: e.parsedFields?.companyName || "未知公司", industry: e.parsedFields?.industry?.name || "", city: e.parsedFields?.city || "", abilities: [], entries: [] });
    }
    const g = grouped.get(e.userId);
    g.abilities.push(e.entryDimension);
    g.entries.push(e);
    // 补全公司信息
    if (e.parsedFields?.companyName) g.companyName = e.parsedFields.companyName;
    if (e.parsedFields?.industry?.name) g.industry = e.parsedFields.industry.name;
    if (e.parsedFields?.city) g.city = e.parsedFields.city;
  }

  const peers = [];
  for (const g of grouped.values()) {
    // 行业重叠
    let industryMatch = 0;
    if (myIndustry && g.industry && myIndustry.includes(g.industry) || g.industry.includes(myIndustry)) {
      industryMatch = 0.4;
    }

    // 能力重叠
    const matchedDims = myAbilities.filter(a => g.abilities.some(pa => pa.includes(a) || a.includes(pa)));
    const abilityScore = myAbilities.length > 0 ? matchedDims.length / myAbilities.length : 0;

    // 城市加分
    const cityBonus = (myCity && g.city && (myCity.includes(g.city) || g.city.includes(myCity))) ? 0.15 : 0;

    const matchScore = Math.min(1, industryMatch + abilityScore * 0.5 + cityBonus);

    if (matchScore >= MIN_SCORE) {
      peers.push({ companyName: g.companyName, industry: g.industry, city: g.city, userId: g.userId, matchScore: Math.round(matchScore * 100) / 100, matchedDimensions: matchedDims, totalAbilities: g.abilities });
    }
  }

  peers.sort((a, b) => b.matchScore - a.matchScore);

  out({ ok: true, myIndustry, myCity, myAbilities, peers, total: peers.length }, WANT_JSON);
}

main().catch(e => {
  out({ ok: false, error: "fatal", message: e?.message || String(e) }, WANT_JSON);
  exit(1);
});

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--api-base") args.apiBase = argv[++i];
    else if (a === "--token") args.token = argv[++i];
    else if (a === "--user-id") args.userId = argv[++i];
    else if (a === "--min-score") args.minScore = argv[++i];
    else if (!a.startsWith("--")) args._ = args._ || [], args._.push(a);
  }
  return args;
}

function out(obj, wantJson) {
  const txt = JSON.stringify(obj, null, 2);
  if (wantJson) console.log(txt);
  else console.log(txt);
}
