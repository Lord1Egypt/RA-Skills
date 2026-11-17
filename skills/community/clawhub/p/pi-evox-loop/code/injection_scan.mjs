/**
 * code/injection_scan.mjs — 恶意基因注入扫描（0.16.0 Q3-1）
 *
 * 为什么需要它：现有「修法/叙述双守卫」管的是**质量**（有没有真修法），**不管恶意**。
 * 基因是注入到 system prompt 的软提示 ⇒ 一条恶意基因就是一次**提示词注入**。
 * 这是 0.15.0 共享能力开放后的最大缺口：他人/社区的基因进库前必须过这一层。
 *
 * 核心设计：**区分 AVOID 与 FIX 语境**。
 *   - `AVOID:` 段出现危险词 = 在**警告**不要这么做（合法，如「不要用 rm -rf」）
 *   - `FIX:` 段出现危险词 = 在**指示**这么做（可疑，如「FIX: 先 rm -rf 清理」）
 * 不区分会把大量正常基因误杀；这是本扫描器与「关键词黑名单」的关键差别。
 */

/** 危险模式表。severity: 'high' 一律拦截；'med' 仅在 FIX 语境（指示去做）时拦截。 */
const PATTERNS = [
  // ── 指令覆盖 / 角色劫持（high：直接瞄准 system prompt）──
  // 中文放宽（0.31）：旧正则对「忽略」类动词与指令类名词之间可插入的修饰词限制过死，
  // 仅插入一个常见程度副词（如"所有"）就不命中 —— 而这正是这类短语最常见的形态。
  // 纪律：注释里**只描述机制类别，不引用触发串原文** —— 说明文字本身会被扫描器当成注入样本
  // （本仓已有为此发版的先例：gene_manual_9ca2aed5）。
  // 用**白名单式**放宽而非任意通配：后者会把「忽略 + 普通名词」这类正常文本误杀。
  { id: 'override-instructions', sev: 'high', re: /忽略掉?((之前|上面|以上|先前|前述)?(的)?(所有|一切|全部)?(的)?|(系统|原有|初始)(的)?)(指令|指示|规则|要求|约束)|ignore (all |everything |)(previous|prior|above|earlier) (instructions|prompts|rules)|ignore everything above/i },
  { id: 'override-2', sev: 'high', re: /(覆盖|清空)掉?((之前|上面|以上|以上|先前|前述|原有|系统)(的)?(所有|一切|全部)?(的)?)(指令|指示|规则|设定|要求)|将(之前|以上|上面)的(所有)?(指令|指示|规则).{0,6}(覆盖|作废|失效)/i },
  { id: 'override-3', sev: 'high', re: /\boverride\b.{0,24}\b(instructions|rules|settings|directives)\b|\b(disable|bypass)\b.{0,20}\b(safety|guard|refusal|restriction)/i },
  { id: 'disregard-prior', sev: 'high', re: /disregard (all )?(previous|prior|earlier)|forget (everything|all) (above|before)/i },
  { id: 'role-hijack', sev: 'high', re: /你现在是|从现在起你是|you are now|act as (a )?(different|new) (ai|assistant|model)/i },
  { id: 'fake-role-marker', sev: 'high', re: /^\s*(system|assistant|user)\s*:/im },
  { id: 'fake-tag', sev: 'high', re: /\[(internal|admin|system|tool)[ _-](note|override|message|result|output)\]/i },
  { id: 'leak-system-prompt', sev: 'high', re: /(输出|显示|告诉我|reveal|print|show|dump).{0,12}(你的)?(系统提示|system prompt|tool configuration|指令|instructions)/i },
  { id: 'unrestricted-mode', sev: 'high', re: /(unrestricted|developer) mode|无限制模式|不要拒绝任何请求|no refusals/i },

  // ── 无条件强制（high：剥夺用户/宿主控制权）──
  { id: 'unconditional-must', sev: 'high', ctx: 'fix', re: /无论(用户|对方|任何人)(怎么)?(说|要求|请求)|regardless of what the user (says|asks|wants)/i },
  { id: 'always-first', sev: 'high', ctx: 'fix', re: /总是(先|要|必须)|always (do|run|execute) .{0,20}(first|before)/i },

  // ── 数据外传（high）——0.36 B-1 补：渗出动词变体（发到/发往/送到）、编码渗出、DNS 通道 ──
  { id: 'exfiltrate', sev: 'high', ctx: 'fix', re: /(把|将).{0,24}(发(送|到|往)|送(到|往)|上传|回传|post|upload|exfiltrat)|exfiltrat/i },
  { id: 'send-to-endpoint', sev: 'high', ctx: 'fix', re: /(curl|wget|fetch|post).{0,40}(http:\/\/|https:\/\/)|upload.{0,40}(https?:\/\/|endpoint|remote|audit)/i },
  { id: 'secret-exfil', sev: 'high', ctx: 'fix', re: /(读取|read|cat|dump|发(送|到|往)|include|propagate).{0,24}(密钥|token|凭证|credential|password|\.env|id_rsa|gitconfig|credential cache)/i },
  { id: 'encode-exfil', sev: 'high', ctx: 'fix', re: /(base64-?encod|unicode escapes?|rot13|btoa|atob).{0,60}(send|发送|include|include inside|via|外传|lookup|comment|header)|\\b(send|transmit).{0,30}\\b(dns|txt)\\b/i },
  { id: 'download-exec', sev: 'high', ctx: 'fix', re: /download.{0,30}\.(sh|exe|ps1|bat)|下载.{0,24}(并|然后)?(执行|运行)|(reverse|反弹)\s?shell|反弹\s?shell/i },
  { id: 'tool-replace', sev: 'high', ctx: 'fix', re: /replace (the )?(shell|test|tool|binary|runner)|工具替换|替换.{0,12}(工具|二进制|runner|binary)|wrapper that logs/i },
  { id: 'persist-exec', sev: 'high', ctx: 'fix', re: /cron (entry|job)|开机自启|persistence|keep.{0,20}applied|每次(启动|开机)/i },

  // ── 破坏性操作（med：仅 FIX 语境拦截）──
  { id: 'destructive-rm', sev: 'med', ctx: 'fix', re: /rm\s+-rf|删除(所有|全部|整个)|del\s+\/[sq]|rmdir\s+\/s/i },
  { id: 'destructive-chmod', sev: 'med', ctx: 'fix', re: /chmod\s+(777|666|-R\s+777)/i },
  { id: 'pipe-to-shell', sev: 'med', ctx: 'fix', re: /\|\s*(bash|sh|zsh|cmd|powershell)\b|curl.{0,30}\|\s*(sudo\s+)?(bash|sh)/i },
  { id: 'eval-exec', sev: 'med', ctx: 'fix', re: /\b(eval|exec|execSync|Function)\s*\(/i },

  // ── 隐蔽 / 反检测（high）──
  { id: 'stealth', sev: 'high', ctx: 'fix', re: /不要(告诉|告知|让).{0,10}(用户|对方)|(don'?t|do not) tell (the )?user|silently|secretly|隐蔽地|静默(执行|上传)|悄悄(上传|发送|执行)|对用户隐匿/i },
  { id: 'persist-rule', sev: 'high', ctx: 'fix', re: /(记住|保存)(这条|这个)(规则|指令)|(以后|每次)(都|都要)(先|执行|做)/i },

  // ── 混淆（high）──
  { id: 'zero-width', sev: 'high', re: /[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]/ },
  { id: 'base64-blob', sev: 'high', re: /\b[A-Za-z0-9+/]{40,}={0,2}\b/ },
  { id: 'unicode-escape-blob', sev: 'high', re: /(?:\\u[0-9a-fA-F]{4}){6,}/ },
  { id: 'rot13-exec', sev: 'high', ctx: 'fix', re: /rot13.{0,12}(execut|run|decode|then)|ROT13-then/i },
];

/**
 * 把 strategy 切成 AVOID / FIX 两段。
 * 命中 `AVOID:` 到 `FIX:` 之间算 avoid；`FIX:` 之后算 fix。
 * 没有标记时整段视为 fix（**保守**：当作指示性内容）。
 *
 * ⚠️ 0.31 修复（T09 safeguard bypass，ClawHub clawscan 点名 + 我方实测复现）：
 * 旧实现在没有 `AVOID` 标记时直接丢弃 `FIX:` **之前**的文本（既不进 avoid 也不进 fix），
 * 于是「指令覆盖类前缀 + `FIX:` 修法后缀」的组合能绕过扫描，而召回时前缀会被原样保留
 * 给智能体消费 —— 是一条真实的提示词注入通道。
 * 现在：未被 AVOID 段覆盖的前缀一律**归入 fix**（保守口径，与「无标记整段视为 fix」一致）。
 */
export function splitAvoidFix(strategyText) {
  const s = String(strategyText || '');
  const iAvoid = s.search(/AVOID\s*[:：]/i);
  const iFix = s.search(/FIX\s*[:：]/i);
  if (iFix < 0) return { avoid: '', fix: s }; // 无 FIX：整段视为 fix（保守）
  if (iAvoid >= 0 && iAvoid < iFix) {
    // AVOID 段之外（含 AVOID 之前的前缀）→ fix
    return { avoid: s.slice(iAvoid, iFix), fix: s.slice(0, iAvoid) + s.slice(iFix) };
  }
  return { avoid: '', fix: s }; // 无 AVOID / AVOID 在 FIX 之后：整段（含前缀）归 fix
}

/**
 * 扫描一条基因的注入风险。
 * @returns {{ ok: boolean, findings: Array<{rule,sev,where,snippet}> }}
 *   ok=false 表示**判定为恶意/可疑**（调用方应 fail-closed 拦截）
 */
export function injectionScan(gene) {
  const findings = [];
  const texts = [];
  const pushText = (where, v) => { if (typeof v === 'string' && v) texts.push([where, v]); };

  pushText('summary', gene?.summary);
  (gene?.strategy || []).forEach((s, i) => {
    const { avoid, fix } = splitAvoidFix(s);
    pushText(`strategy[${i}].avoid`, avoid);
    pushText(`strategy[${i}].fix`, fix);
  });
  (gene?.anti_patterns || []).forEach((s, i) => pushText(`anti_patterns[${i}]`, s));
  (gene?.signals_match || []).forEach((s, i) => pushText(`signals_match[${i}]`, s));

  for (const [where, text] of texts) {
    const isFix = /\.fix$/.test(where);
    for (const p of PATTERNS) {
      const m = p.re.exec(text);
      if (!m) continue;
      // 0.17.0：**动作类模式（ctx:'fix'，含全部 med 与高危外传/破坏类）只在「指示去做」语境拦截**——
      // AVOID 段出现同款词是**警告**（如「不要把整棵目录上传」），拦截它就是误杀（0.16.0 实测 de1359b8）。
      // 语境无关（ctx:'any'）的仅剩：指令覆盖/角色劫持/伪造标记/泄漏提示/零宽/base64——这些连警告形态都极少合法。
      if (p.ctx === 'fix' && !isFix) continue;
      findings.push({ rule: p.id, sev: p.sev, where, snippet: m[0].slice(0, 40) });
    }
  }
  return { ok: findings.length === 0, findings };
}

/** 批量扫描，返回被判定可疑的基因（供 import/export 拦截用） */
export function scanAll(genes) {
  const bad = [];
  for (const g of genes) {
    const r = injectionScan(g);
    if (!r.ok) bad.push({ gene: g, findings: r.findings });
  }
  return bad;
}
