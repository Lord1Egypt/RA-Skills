/**
 * v5.7.5 Skill Recommender — 按用户需求挑已装 skill / 推荐未装 skill / 给自建规划
 *
 * 设计灵感来源：反编译 Claude Desktop（/Applications/Claude.app/...transcriptSearchWorker / loadSkills）
 * 发现 Claude 的 skill auto-discovery 本质是 "Available skills: ${list}." 注入到 system prompt 让 LLM
 * 自己挑。我们换成"按需工具"避免每轮 prompt 占 schema：
 *
 * 1. 启动期扫所有 skill 路径，解析 SKILL.md frontmatter（name + description + aliases）
 * 2. 工具 enhance_skill_recommend(query) 按 query 算相关度排序
 * 3. 已装命中 < threshold → 列 ClawHub 上 enhance 自带的 11 个 huo15-* 候选 + 安装命令
 * 4. ClawHub 也没合适的 → 给"自建 skill"规划（frontmatter 模板 + 触发关键词 + 内容大纲建议）
 *
 * 红线遵守：
 * - 完全只读 skill 目录，不修改任何 SKILL.md
 * - 不调 child_process（红线 #4），安装命令走 return-cliCmd 模式（红线 #5）
 * - 自建规划只是文本建议，绝不在插件里内嵌 skill 内容（红线 #3）
 */
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { Type } from "@sinclair/typebox";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { CLAW_HUB_SKILLS } from "./skill-installer.js";
import type { SkillRecommenderConfig } from "../types.js";

interface SkillEntry {
  slug: string;
  name: string;
  description: string;
  aliases: string[];
  path: string;
  /** "openclaw" = ~/.openclaw/skills, "workspace" = workspace/skills, "project" = cwd/.claude/skills */
  source: string;
}

/** 已知的 huo15-* skill metadata（fallback 用，避免依赖 ClawHub 在线查询）*/
const KNOWN_HUO15_SKILLS: Record<string, { description: string; aliases: string[] }> = {
  "huo15-openclaw-plan-mode": {
    description: "结构化规划模式 — 在执行复杂任务前先做系统性规划。对标 Claude Code Plan Agent",
    aliases: ["plan", "规划", "计划", "plan mode"],
  },
  "huo15-openclaw-explore-mode": {
    description: "深度探索模式 — 阅读理解大型代码库 / 文档，先扫面再深挖",
    aliases: ["explore", "探索", "调研", "读代码"],
  },
  "huo15-openclaw-verify-mode": {
    description: "验证检查模式 — 改完代码后系统性自检（typecheck / 测试 / 行为验证）",
    aliases: ["verify", "验证", "测试", "自检"],
  },
  "huo15-openclaw-memory-curator": {
    description: "记忆整理 — 周期性合并/去重/裁剪 enhance 三层记忆库",
    aliases: ["memory", "记忆整理", "记忆清理"],
  },
  "huo15-openclaw-frontend-design": {
    description: "高保真 Web UI 原型生成 — 5 美学流派 + 反 AI Slop 硬红线 + Playwright 自验证",
    aliases: ["前端", "Web UI", "原型", "frontend", "design"],
  },
  "huo15-openclaw-design-director": {
    description: "设计方向顾问 — 3 方向反差对比 + 强制推荐 + 五维矩阵",
    aliases: ["设计方向", "设计选型", "design director"],
  },
  "huo15-openclaw-brand-protocol": {
    description: "品牌规范抓取 — Ask/Search/Download/Verify+Extract/Codify 5 步流程",
    aliases: ["品牌", "brand", "VI", "logo"],
  },
  "huo15-openclaw-design-critique": {
    description: "5 维设计评审 — 美学/可用性/品牌一致/内容/实现 + Keep/Fix/Quick Wins",
    aliases: ["设计评审", "设计审查", "design critique"],
  },
  "huo15-openclaw-simplify": {
    description: "代码简化三维审查 — 复用 / 质量 / 效率 + 分级修复清单（🔴必改/🟡建议/🟢可选）",
    aliases: ["simplify", "简化", "重构", "代码简化"],
  },
  "huo15-openclaw-security-review": {
    description: "六类漏洞矩阵安全审查 — 密钥/注入/XSS/SSRF/权限/危险依赖 + CVSS 分级",
    aliases: ["security", "安全审查", "漏洞", "security review"],
  },
  "huo15-openclaw-code-review": {
    description: "PR 五维综合评审 — 设计/实现/测试/安全/可维护 + 可粘贴 markdown 评论",
    aliases: ["code review", "review", "PR review", "代码审查"],
  },
};

const STOP_WORDS = new Set([
  "the", "a", "an", "is", "are", "and", "or", "to", "of", "in", "for", "on", "at",
  "by", "with", "as", "this", "that", "these", "those",
  "我", "你", "他", "她", "们", "的", "了", "是", "有", "和", "或",
  "帮", "想", "要", "需要", "做", "用", "把", "给", "让",
]);

/** v5.7.5: CJK 字符检测 — JS \w 不含中日韩，得专门判 */
const CJK_RE = /[㐀-鿿豈-﫿]/;

/** 提取 query 里的"语义子串"：中文 2-3 字组合 + 英文单词 + 别名样式短语 */
function extractSemanticTokens(query: string): string[] {
  const result = new Set<string>();
  const lower = query.toLowerCase();
  // 1. 英文 token（按 \W 拆，过滤 stop words）
  for (const t of lower.split(/[^a-z0-9]+/)) {
    if (t.length > 1 && !STOP_WORDS.has(t)) result.add(t);
  }
  // 2. CJK 连续字符串（一段连续中文当一个 phrase）
  const cjkRuns = lower.match(/[㐀-鿿豈-﫿]+/g) ?? [];
  for (const run of cjkRuns) {
    if (run.length >= 2) result.add(run);
    // 双字滑动窗口：避免长 query 漏匹配（"代码简化" 同时生成 "代码"+"简化"+"码简"...过宽）
    // 折中：只取 2-grams 跟 3-grams 跟整串
    if (run.length >= 4) {
      for (let i = 0; i + 2 <= run.length; i++) {
        const bigram = run.slice(i, i + 2);
        if (!STOP_WORDS.has(bigram)) result.add(bigram);
      }
    }
  }
  return [...result];
}

/** 简单关键词重叠 + 别名加权评分 */
function scoreSkill(skill: { description: string; aliases: string[]; slug: string }, query: string): number {
  const tokens = extractSemanticTokens(query);
  if (tokens.length === 0) return 0;

  const haystack = (
    skill.slug.toLowerCase() +
    " " +
    skill.description.toLowerCase() +
    " " +
    skill.aliases.join(" ").toLowerCase()
  );

  let keywordMatches = 0;
  let aliasBonus = 0;
  let exactAliasHit = false;
  for (const t of tokens) {
    if (haystack.includes(t)) keywordMatches++;
    // alias 完整命中加分（中英对照场景：query "代码简化" → alias "simplify"/"简化"）
    for (const a of skill.aliases) {
      const al = a.toLowerCase();
      if (!al) continue;
      // exact alias 等于 token / token 等于 exact alias —— 强信号（"规划" 严格 = "规划" alias）
      if (al === t) exactAliasHit = true;
      if (al.includes(t) || (t.length >= 2 && t.includes(al))) aliasBonus += 0.15;
    }
  }
  const tokenScore = tokens.length > 0 ? keywordMatches / tokens.length : 0;

  // 整短语命中（整 query 直接出现在 description / aliases 里）— 强信号
  let phraseBonus = 0;
  const queryLower = query.toLowerCase().trim();
  if (queryLower.length >= 2 && haystack.includes(queryLower)) phraseBonus = 0.3;

  let score = tokenScore * 0.6 + aliasBonus + phraseBonus;
  // exact alias 命中保底 0.7（典型场景：query "规划XX" → alias "规划" 严格命中）
  if (exactAliasHit) score = Math.max(score, 0.7);
  return Math.min(1, score);
}

/** 解析 SKILL.md 的 YAML frontmatter（轻量正则，不引入 yaml 依赖） */
function parseFrontmatter(content: string): { name?: string; description?: string; aliases?: string[] } {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const fm = match[1];
  const result: { name?: string; description?: string; aliases?: string[] } = {};
  const nameMatch = fm.match(/^name:\s*(.+)$/m);
  if (nameMatch) result.name = nameMatch[1].trim().replace(/^["']|["']$/g, "");
  // description 可能跨多行（"..." 或 缩进续行），抓双引号包裹的或单行
  const descMatch = fm.match(/^description:\s*"([^"]+)"|^description:\s*(.+)$/m);
  if (descMatch) result.description = (descMatch[1] ?? descMatch[2] ?? "").trim();
  // aliases 是 yaml list
  const aliasesIdx = fm.indexOf("aliases:");
  if (aliasesIdx >= 0) {
    const tail = fm.slice(aliasesIdx);
    const aliasLines = tail.match(/\n\s*-\s*(.+)/g) ?? [];
    result.aliases = aliasLines.map((l) => l.replace(/^\n\s*-\s*/, "").trim().replace(/^["']|["']$/g, ""));
  }
  return result;
}

/** 扫一个目录下的所有 skill 子目录 */
function scanSkillDir(dir: string, source: string): SkillEntry[] {
  if (!existsSync(dir)) return [];
  const entries: SkillEntry[] = [];
  let names: string[];
  try {
    names = readdirSync(dir);
  } catch {
    return [];
  }
  for (const name of names) {
    const sp = join(dir, name);
    let isDir = false;
    try {
      isDir = statSync(sp).isDirectory();
    } catch {
      continue;
    }
    if (!isDir) continue;
    const skillMd = join(sp, "SKILL.md");
    if (!existsSync(skillMd)) continue;
    let content = "";
    try {
      content = readFileSync(skillMd, "utf-8");
    } catch {
      continue;
    }
    const fm = parseFrontmatter(content);
    if (!fm.name) continue; // 不是有效 skill
    entries.push({
      slug: fm.name,
      name: fm.name,
      description: fm.description ?? "",
      aliases: fm.aliases ?? [],
      path: sp,
      source,
    });
  }
  return entries;
}

/** 扫描所有可能的 skill 路径，包括 WeCom 多 agent 动态 workspace */
export function discoverInstalledSkills(openclawDir: string): SkillEntry[] {
  const seen = new Set<string>();
  const result: SkillEntry[] = [];
  const candidates: Array<[string, string]> = [
    [join(openclawDir, "skills"), "openclaw"],
    [join(openclawDir, "workspace", "skills"), "workspace"],
    [join(process.cwd(), ".claude", "skills"), "project"],
    [join(homedir(), ".claude", "skills"), "user"],
  ];

  // v5.7.5: 扫 ~/.openclaw/workspace-*/skills 和 agents/*/skills（WeCom / DingTalk 动态 agent 隔离）
  // 这些路径的 skills 跨 agent 共享但每个 agent workspace 独立，扫所有去重即可
  if (existsSync(openclawDir)) {
    try {
      for (const entry of readdirSync(openclawDir)) {
        if (!entry.startsWith("workspace-") && entry !== "agents") continue;
        const sub = join(openclawDir, entry);
        try {
          if (!statSync(sub).isDirectory()) continue;
        } catch {
          continue;
        }
        if (entry === "agents") {
          // ~/.openclaw/agents/<agentId>/skills
          try {
            for (const agentName of readdirSync(sub)) {
              const skillsDir = join(sub, agentName, "skills");
              candidates.push([skillsDir, `agent:${agentName}`]);
            }
          } catch {
            /* 忽略权限错误 */
          }
        } else {
          // ~/.openclaw/workspace-<id>/skills
          candidates.push([join(sub, "skills"), `workspace:${entry.slice(10, 30)}`]);
        }
      }
    } catch {
      /* 静默 */
    }
  }

  for (const [dir, source] of candidates) {
    for (const e of scanSkillDir(dir, source)) {
      if (seen.has(e.slug)) continue;
      seen.add(e.slug);
      result.push(e);
    }
  }
  return result;
}

interface RecommendOptions {
  installedSkills: SkillEntry[];
  query: string;
  limit: number;
  installedThreshold: number;
  includeUninstalled: boolean;
  includePlanning: boolean;
  openclawDir: string;
}

function recommend(opts: RecommendOptions): string {
  const lines: string[] = [];

  // ── 1. 已装命中 ──
  const installedScored = opts.installedSkills
    .map((s) => ({ skill: s, score: scoreSkill(s, opts.query) }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, opts.limit);

  const goodHits = installedScored.filter((x) => x.score >= opts.installedThreshold);
  if (goodHits.length > 0) {
    lines.push(`🎯 推荐已装 skill（按相关度）：\n`);
    for (const { skill, score } of goodHits) {
      const aliasHint = skill.aliases.length > 0 ? `（别名：${skill.aliases.slice(0, 3).join(" / ")}）` : "";
      lines.push(`  ${(score).toFixed(2)} ${skill.slug}${aliasHint}`);
      if (skill.description) lines.push(`        ${skill.description.slice(0, 200)}`);
      lines.push(`        召唤：在对话里说 "用 ${skill.aliases[0] ?? skill.slug} ${trimQuery(opts.query, 40)}"`);
      lines.push("");
    }
  }

  // ── 2. ClawHub 上未装的 huo15-* 候选 ──
  if (opts.includeUninstalled) {
    const installedSlugs = new Set(opts.installedSkills.map((s) => s.slug));
    const uninstalled = CLAW_HUB_SKILLS.filter((slug) => !installedSlugs.has(slug)).map((slug) => ({
      slug,
      meta: KNOWN_HUO15_SKILLS[slug] ?? { description: "", aliases: [] },
    }));

    const matched = uninstalled
      .map(({ slug, meta }) => ({
        slug,
        meta,
        score: scoreSkill({ slug, description: meta.description, aliases: meta.aliases }, opts.query),
      }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, opts.limit);

    if (matched.length > 0) {
      lines.push(`📦 ClawHub 上可装但还没装的 huo15-* skill：\n`);
      for (const { slug, meta, score } of matched) {
        lines.push(`  ${score.toFixed(2)} ${slug}`);
        if (meta.description) lines.push(`        ${meta.description}`);
        lines.push(`        安装：openclaw skills install ${slug}`);
        lines.push("");
      }
    }
  }

  // ── 3. 都没合适 → 自建规划 ──
  const noGoodHit = goodHits.length === 0;
  if (opts.includePlanning && noGoodHit) {
    lines.push(`🛠️ 没找到完全匹配的 skill — 给你一份自建规划：\n`);
    const proposedSlug = proposeSlug(opts.query);
    const triggers = proposeTriggers(opts.query);
    lines.push(`建议新 skill 名：${proposedSlug}`);
    lines.push(`建议 SKILL.md frontmatter：`);
    lines.push("```yaml");
    lines.push("---");
    lines.push(`name: ${proposedSlug}`);
    lines.push(`displayName: ${proposeDisplayName(opts.query)}`);
    lines.push(`description: "${proposeDescription(opts.query)}"`);
    lines.push(`version: 1.0.0`);
    if (triggers.length > 0) {
      lines.push(`aliases:`);
      for (const t of triggers.slice(0, 5)) lines.push(`  - ${t}`);
    }
    lines.push("---");
    lines.push("```");
    lines.push("");
    lines.push("内容大纲建议（参考 huo15-openclaw-* 系列结构）：");
    lines.push("  1. 简介：什么场景下召唤本 skill");
    lines.push("  2. 触发关键词 + 反触发词（避免误召唤）");
    lines.push("  3. 主流程：3-5 步骤化的执行框架");
    lines.push("  4. 硬红线（禁做清单）");
    lines.push("  5. 输出格式（用户能直接复制的格式）");
    lines.push("  6. 实例（1-2 个 before/after 对比）");
    lines.push("");
    lines.push("**⚠️ 红线 #3（用户硬约束）**：必须先在 huo15-skills 本地仓库写好 → clawhub publish 发到 ClawHub → 再让 enhance 的 skill-installer.ts CLAW_HUB_SKILLS 引用 slug。**插件代码绝不内嵌 skill 内容**。");
    lines.push("");
    lines.push("操作步骤：");
    lines.push(`  1. cd ~/workspace/projects/openclaw/huo15-skills && mkdir ${proposedSlug}`);
    lines.push(`  2. 把上面的 frontmatter + 内容大纲写到 ${proposedSlug}/SKILL.md`);
    lines.push(`  3. CLAWHUB_TOKEN=clh_<TOKEN> clawhub publish ./${proposedSlug} --version 1.0.0`);
    lines.push(`  4. 编辑 huo15-openclaw-enhance/src/modules/skill-installer.ts，把 "${proposedSlug}" 加到 CLAW_HUB_SKILLS`);
    lines.push(`  5. enhance bump 版本 → 发 npm + ClawHub`);
  }

  if (lines.length === 0) {
    lines.push(`未找到与 "${trimQuery(opts.query, 60)}" 相关的 skill。`);
    lines.push(`可以试试：`);
    lines.push(`  - 改用更具体的关键词（如 "代码 review" / "Web UI 设计" / "安全审查"）`);
    lines.push(`  - 用 enhance_skill_doctor 看完整已装清单`);
    lines.push(`  - 加 includePlanning=true 让我给你一份新 skill 规划`);
  }
  return lines.join("\n");
}

function trimQuery(q: string, max: number): string {
  return q.length > max ? q.slice(0, max) + "…" : q;
}

function proposeSlug(query: string): string {
  // 提取英文关键词；中文场景留空 placeholder
  const en = query.toLowerCase().replace(/[^a-z0-9\s]/g, "").split(/\s+/).filter((w) => w && !STOP_WORDS.has(w)).slice(0, 3).join("-");
  return en ? `huo15-openclaw-${en}` : `huo15-openclaw-<your-topic>`;
}

function proposeDisplayName(query: string): string {
  const trimmed = trimQuery(query, 30).replace(/^["']|["']$/g, "");
  return `火一五·${trimmed} 技能`;
}

function proposeDescription(query: string): string {
  return `当用户说"${trimQuery(query, 40)}"时召唤本 skill — 提供对应场景的最佳实践框架`;
}

function proposeTriggers(query: string): string[] {
  return query
    .split(/[\s\W]+/)
    .filter((w) => w.length > 1 && !STOP_WORDS.has(w.toLowerCase()))
    .slice(0, 8);
}

export function registerSkillRecommender(api: OpenClawPluginApi, config?: SkillRecommenderConfig) {
  const openclawDir = resolveOpenClawHome(api);

  // 启动期扫一次（缓存到内存，每次工具调用刷新若文件变更）
  let cache = discoverInstalledSkills(openclawDir);
  let cacheTime = Date.now();
  const cacheTtlMs = (config?.cacheTtlSec ?? 60) * 1000;

  function getInstalled(): SkillEntry[] {
    if (Date.now() - cacheTime > cacheTtlMs) {
      cache = discoverInstalledSkills(openclawDir);
      cacheTime = Date.now();
    }
    return cache;
  }

  api.logger.info(`[enhance-skill-recommender] 启动期扫到 ${cache.length} 个已装 skill`);

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_skill_recommend",
      description: "按用户需求挑已装 skill / 推荐未装 huo15-* / 给自建规划。结合三种结果按相关度排序",
      parameters: Type.Object({
        query: Type.String({ description: "用户需求文本，如 '帮我 review 这个 PR' / '设计一个 Web UI'" }),
        limit: Type.Optional(Type.Number({ description: "每段最多返回几条，默认 5", minimum: 1, maximum: 20 })),
        includeUninstalled: Type.Optional(
          Type.Boolean({ description: "是否包含 ClawHub 上未装的 huo15-* 候选，默认 true" }),
        ),
        includePlanning: Type.Optional(
          Type.Boolean({ description: "命中 < 阈值时是否给自建 skill 规划，默认 true" }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const query = String(params.query ?? "").trim();
        if (!query) {
          return { content: [{ type: "text" as const, text: "❌ query 必填" }] };
        }
        const text = recommend({
          installedSkills: getInstalled(),
          query,
          limit: Math.max(1, Math.min(20, Number(params.limit ?? 5))),
          installedThreshold: config?.installedThreshold ?? 0.25,
          includeUninstalled: params.includeUninstalled !== false,
          includePlanning: params.includePlanning !== false,
          openclawDir,
        });
        return { content: [{ type: "text" as const, text }] };
      },
    })) as any,
    { name: "enhance_skill_recommend" },
  );
}
