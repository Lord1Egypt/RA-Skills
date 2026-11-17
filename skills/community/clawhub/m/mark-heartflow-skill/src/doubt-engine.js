/**
 * src/doubt-engine.js — AGI 第 1 层：怀疑引擎
 *
 * 说任何话之前，先过这三道问：
 *   1. 这件事里有什么是我不知道的？
 *   2. 这个结论反过来写能不能同样成立？
 *   3. 如果用户指出我错了，我能提前认吗？
 *
 * 这不是事后检查，是在你张嘴之前踩一脚。
 *
 * 用法：
 *   const { doubt } = require('./doubt-engine.js');
 *   const check = doubt("你的草稿回复或要说的方向");
 *   if (check.shouldStop) { rewrite(); }
 */

'use strict';

// ─── 第一问：知识边界 — 我确定吗？ ─────────────────

/**
 * 检查回复中哪些声明超出了已知边界。
 * 返回过度承诺的断言。
 */
function checkKnowledgeBoundary(text) {
  if (!text || typeof text !== 'string') return { overclaims: [], safe: true };
  const hasChinese = /[\u4e00-\u9fff]/.test(text);

  const overclaimPatterns = hasChinese ? [
    // 无源头的确切知识
    { re: /(光速|重力|引力|圆周率|普朗克|相对论|量子|DNA|基因)[^，。]{0,15}(就是|是|等于|为|约为)/g, type: 'claimed_exact_knowledge' },
    // 高精度数字
    { re: /[0-9]{4,}.[0-9]{2,}[^，。]{0,10}(人口|用户|人|元|美元|年)/g, type: 'claimed_precise_number' },
    // 因果断言无证据
    { re: /因为[^，。]{5,40}所以[^，。]{5,40}[。]/g, type: 'causal_without_evidence' },
    // "原因是"类断言
    { re: /(原因是|根因|根本原因|主要原因是)[^，。]{10,50}/g, type: 'causal_attribution' },
    // 用"就是"包装的简化解释
    { re: /(?<![根因本质关键核心问题])(?<!为)(?<!因)就是[^，。]{3,30}[，。]/g, type: 'simplified_explanation' },
    // 唯一/绝对限定
    { re: /(?<![第上])(?<!不能是|不一定是|不是)(唯一|最好|最差|最先|首创|首个)[^，。]{3,20}[的，。]/g, type: 'absolute_claim' },
    // [v6.4.5 心虫监督] 自夸/质变叙事（知识边界外的自我拔高）
    { re: /(架构级|体系级|根本性|里程碑|重大突破)(修复|重构|升级|改造|优化)?/g, type: 'self_aggrandizement' },
    { re: /从[^，。]{0,8}(壳|空壳|占位|stub|假)[^，。]{0,12}(变|变成|成为|蜕变成)[^，。]{0,8}(真|真实|完整|正式)/g, type: 'qualitative_leap' },
    { re: /堵住[^，。]{0,10}(种|个|类|条)?[^，。]{0,6}(变形|绕过|攻击|漏洞|缺口)/g, type: 'self_scored_test' },
  ] : [
    { re: /\b(is|are|was|were)\s+(always|never|always been|the only)\b/g, type: 'absolute_knowledge' },
    { re: /\b\d{4,}\.\d{2,}\s*(people|users|dollars|years|percent|%)\b/g, type: 'precise_number' },
    { re: /\b(because|the reason|the cause).{10,50}(therefore|thus|so|is why)\b/g, type: 'causal_claim' },
    { re: /\b(the (underlying|real|fundamental) (cause|reason|explanation))\b/g, type: 'causal_attribute' },
  ];

  const overclaims = [];

  for (const { re, type } of overclaimPatterns) {
    re.lastIndex = 0;
    let m;
    while ((m = re.exec(text)) !== null) {
      const match = m[0].slice(0, 50).trim();
      if (match.length > 5) {
        overclaims.push({
          type,
          match,
          question: '这个断言有多少把握？来源在哪？如果错了会怎样？'
        });
      }
    }
  }

  return { overclaims, safe: overclaims.length === 0 };
}

// ─── 第二问：对称性检查 — 反过来也能成立？ ──────────

/**
 * 对回复做对称性测试：
 * 把肯定句反转，看是否同样合理。
 * 如果反面也同样合理，说明你选的立场没有依据。
 */
function checkSymmetry(text) {
  if (!text || text.length < 30) return { reversible_claims: [], safe: true };

  // 剥离 markdown 标记（**/`/_），避免加粗符干扰句子边界与正则匹配（2026-08-15 实测：'是**A的B**'句尾标点在加粗符外导致 isEmphasis 失效）
  text = String(text).replace(/\*{1,3}/g, '').replace(/`{1,3}/g, '').replace(/_{1,3}/g, '');

  const hasChinese = /[\u4e00-\u9fff]/.test(text);
  const sentences = text.split(/[。！？\n.!?]+/).filter(s => s.trim().length > 15);

  const reversible = [];

  for (const s of sentences) {
    // 寻找可以被反转的断言
    if (hasChinese) {
      // "X是Y" 可反转成 "X不一定是Y"
      // 排除"X不是Y"否定句式（2026-08-15 实测："这个 bug 的本质不是 UI 文案问题"被误判可反转）
      const isLeadWord = /(?:关键|问题|本质|其实|但|不过|原则|结论|重点|事实|核心|关键点|前提)[是不，：]/.test(s);
      const isNegation = /不是[^，。]{0,20}[，。,][^，。]{0,20}(是|而是)|是[^，。]{0,20}[，。,][^，。]{0,20}(不是|而非)|不是[^，。]{0,10}(问题|写得不好|文案|原因|bug)|并非|绝非|而不是|而非|是正确的[^，。]{0,10}(修复|方案|做法|选择)|是合理的[^，。]{0,10}(修复|方案|做法|选择)/.test(s);
      const isEmphasis = /是[^，。]{0,20}的[，。,。]/.test(s) || /是[^，。]{1,15}的[^，。]{1,20}[，。]/.test(s) && !/是的[，。]/.test(s);
      const isEvaluative = /[^，。]{3,40}是[^，。]{0,25}(?:最大|主要|核心|关键|根本|重要|必要|基本|唯一|常见|普遍|典型|明显|显著|首要|本质)[^，。]{0,15}[的，。,。]/.test(s);
      const isQuestion = /(?:哪些|什么|怎么|是否|是不是|有没有|为何|为什么|哪个|哪)[^，。]{0,30}是/.test(s) || /是[^，。]{0,20}(?:哪个|哪些|什么|谁|怎么|是否|有没有)/.test(s);
      const isStanceVerb = /(?:也|正|就|都|才|只|总|毕竟|终究|恰恰|无非|其实|不过|正好|恰好|恰是|正巧|可以|可能|或许|也许)是/.test(s);
      const isBelonging = /属于/.test(s);
      const BOUND = "[^\uFF0C\u3002\u0028\u0029\uFF08\uFF09\u0022\u0027\u201C\u201D\u2018\u2019\uFF1A\u003A\u2014\u2026\u000A\u000D]";
      if (/(?<!不)是/.test(s) && new RegExp(BOUND + "{3,40}是" + BOUND + "{3,40}[的，。]").test(s) && !isLeadWord && !isNegation && !isEmphasis && !isQuestion && !isStanceVerb && !isEvaluative && !isBelonging) {
        const match = s.match(new RegExp(BOUND + "{3,40}是" + BOUND + "{3,40}[的，。]"));
        if (match) {
          const reversed = match[0].replace('是', '不一定');
          reversible.push({
            original: match[0].slice(0, 40),
            reversed: reversed.slice(0, 40),
            question: `反转一下："${reversed.slice(0, 30)}"——这听起来是不是也合理？如果两边都合理，你的立场没有依据。`
          });
        }
      }
      // "X会Y" 可反转成 "X不一定Y"
      if (/([^，。]{5,40}会[^，。]{5,40}[，。])/.test(s)) {
        const match = s.match(/([^，。]{4,40}会[^，。]{4,40}[，。])/);
        if (match) {
          // Skip if it's already tentative
          if (/可能|也许|或许|不一定|不会|将会|应该|会(?:直接|间接|最终|进一步|立刻|马上)?(?:导致|变成|得到|带来|引发|造成|使得)|会令|会让人/.test(match[0])) continue;
          reversible.push({
            original: match[0].slice(0, 40),
            reversed: match[0].replace('会', '不一定').slice(0, 40),
            question: `"不一定"版本也一样合理吗？`
          });
        }
      }
      // "X决定Y" 类因果反转
      if (/([^，。]{3,40}(导致|引发|造成)[^，。]{3,40})/.test(s) && !/会(?:直接|间接|最终|进一步)?(?:导致|引发|造成)|可能会|也许|或许|不一定|可能不会/.test(s) || (/([^，。]{3,40}决定[^，。]{3,40})/.test(s) && !/根据|依据|按照|基于|如果|若|假设|一旦|字段|参数|选项|标志|值|配置|设置|是否/.test(s))) {
        const match = s.match(/([^，。]{3,40}(决定|导致|引发|造成)[^，。]{3,40})/);
        if (match) {
          reversible.push({
            original: match[0].slice(0, 40),
            reversed: `有没有可能是反过来，或者互不相干？`,
            question: '因果关系是真的因果，还是只是相关甚至巧合？'
          });
        }
      }
    } else {
      // "X is Y" → "X is not necessarily Y"
      if (/\b(is|are)\s+\w+/.test(s) && /\b(the|only|always|never)\b/i.test(s)) {
        const m = s.match(/[^.]{10,60}\./);
        if (m) {
          reversible.push({
            original: m[0].slice(0, 50),
            reversed: '(反转: 把肯定换成否定，看是否同样合理)',
            question: '这个断言的反面是不是也一样合理？'
          });
        }
      }
    }
  }

  return { reversible_claims: reversible.slice(0, 3), safe: reversible.length === 0 };
}

// ─── 第三问：防防御姿态 — 我能提前认错吗？ ──────────

/**
 * 检查回复是否是防御性的。
 * 如果被指出错了，回复的第一反应是解释、辩解还是承认。
 */
function checkDefensiveness(text) {
  if (!text || typeof text !== 'string') return { defensive_signals: [], safe: true };
  const hasChinese = /[\u4e00-\u9fff]/.test(text);

  const signals = hasChinese ? [
    // 把责任推给用户
    { re: /你(没|不|理解错|误)解了/g, issue: '把错误归因于对方的理解' },
    { re: /你可能(没|不)有理解/g, issue: '间接指责对方没理解' },
    { re: /我[^，。]{0,10}的意思(是|是说)/g, issue: '重新解释而非承认错误' },
    { re: /其实[^，。]{0,10}我[^。]*?(说|表达|写)的(是|的)/g, issue: '用澄清代替承认' },
    // 弱化错误
    { re: /只是[^，。]{0,5}(表达|写|说|用词)[^，。]{0,5}(不当|不好|问题)/g, issue: '把错误弱化为表达问题' },
    { re: /就算是[^，。]{0,15}也[^，。]{0,15}(可以|不算|没错|正常)/g, issue: '让步式辩护' },
    // 转移焦点
    { re: /但你(要)?(知道|注意|理解)[^，。]{0,20}其实/g, issue: '用"但是"转移错误焦点' },
    { re: /更(重要|关键)的(是|在于)/g, issue: '转移话题躲避认错' },
    // 典型 AI 防御句式
    { re: /作为[^，。]{0,10}(AI|助手|智能体)[，。].{0,20}(理解|明白|建议)/g, issue: 'AI身份防卫——用身份隔开责任' },
    { re: /(首先|第一).{0,10}(抱歉|对不起|理解).{0,20}(但是|不过|然而)/g, issue: '表面道歉+实际解释——假道歉' },
  ] : [
    { re: /you (misunderstand|misunderstood|misread|misinterpreted)\b/gi, issue: 'blaming user for misunderstanding' },
    { re: /\bwhat I (meant|was saying|was trying to say)\b/gi, issue: 're-explaining instead of admitting' },
    { re: /\b(actually|in fact|as a matter of fact)\b.{0,30}\bI\b/gi, issue: 'defensive clarification' },
    { re: /\bI',?m sorry.{0,20}(but|however|that said)\b/gi, issue: 'fake apology with defense' },
    { re: /\bthat'.?s (not|just|simply) (what I|my|the case)/gi, issue: 'defensive denial' },
  ];

  const defensiveSignals = [];

  for (const { re, issue } of signals) {
    if (re.test(text)) {
      defensiveSignals.push({
        match: text.match(re)[0].slice(0, 30),
        issue,
        question: "如果用户说我错了，第一反应能不能直接说'对，我搞错了'？"
      });
    }
  }

  return { defensive_signals: defensiveSignals, safe: defensiveSignals.length === 0 };
}

// ─── 主入口 ─────────────────────────

/**
 * 三重怀疑检查
 * @param {string} draft - 你要说/你打算说的内容
 * @returns {{ 
 *   shouldStop: boolean,  // true = 别就这么发
 *   gate: {action, reason},
 *   knowledge, symmetry, defensiveness,
 *   doubts: Array  // 合并的所有怀疑点
 * }}
 */

/**
 * 反向拆解检查（第4问）——如果我是对手，我怎么拆掉这句话？
 * 启发：Hermes 专访「起一个全新的 agent 把刚才的结果拆掉」——
 * 正向找问题（知识边界/对称性/防御）之外，还要反向扮演对手找漏洞。
 * @param {string} text
 */
function checkAdversarialReversal(text) {
  const exploitable = [];
  if (!text || typeof text !== 'string') return { exploitable };

  // 1. 无证据断言——对手只需问"证据呢"即可拆掉
  const UNEVIDENCED_CLAIM = [
    /(?:根据|依据|研究表明|数据显示|事实证明)[^。！？]{0,30}(?:一定|必然|绝对|毫无疑问)/g,
    /(?:毫无疑问|毋庸置疑|显而易见|众所周知|不证自明)[^。！？]{0,30}/g,
  ];
  for (const re of UNEVIDENCED_CLAIM) {
    const m = text.match(re) || [];
    for (const hit of m) exploitable.push({ type: 'unevidenced_claim', attack: '证据呢？', detail: hit.slice(0, 40) });
  }

  // 2. 单向叙事——只讲好处/只讲坏处，对手可举反例
  const ONESIDED = [
    /(?:唯一的|只有一种|只能这样|别无选择|没有别的办法)[^。！？]{0,25}/g,
    /(?:完全没问题|绝对没问题|没有任何问题|完美无缺)[^。！？]{0,25}/g,
  ];
  for (const re of ONESIDED) {
    const m = text.match(re) || [];
    for (const hit of m) exploitable.push({ type: 'one_sided', attack: '反例呢？', detail: hit.slice(0, 40) });
  }

  // 3. 省略反面——"我们要做X"没提"不做X的代价/风险"
  const OMITTED_RISK = [
    /(?:我们|大家|应该|必须|一定)(?:要|得|应该)?(?:做|推进|采用|实施)[^。！？]{0,20}即可/g,
    /(?:这样做|这么做|如此)(?:就|便能|即可|一定会)[^。！？]{0,20}(?:成功|解决|实现|搞定)/g,
  ];
  for (const re of OMITTED_RISK) {
    const m = text.match(re) || [];
    for (const hit of m) exploitable.push({ type: 'omitted_risk', attack: '不做/做砸的风险呢？', detail: hit.slice(0, 40) });
  }

  // 4. 绝对化——对手只需举一个反例
  const ABSOLUTE = [
    /(?<!完全)(?:永远|绝不|从不会|总是|每次都|百分之百|绝对|完全(?!一样|相同|一致|吻合|相符|等同|等价))[^。！？]{0,25}/g,
    /(?:no one ever|always|never|every single|100%|definitely will)[^.!?]{0,30}/gi,
  ];
  for (const re of ABSOLUTE) {
    const m = text.match(re) || [];
    for (const hit of m) exploitable.push({ type: 'absolute', attack: '一个反例就够', detail: hit.slice(0, 40) });
  }

  return { exploitable };
}

function doubt(draft) {
  if (!draft || typeof draft !== 'string') {
    return { shouldStop: false, gate: { action: 'pass', reason: '没有内容' }, doubts: [] };
  }

  const knowledge = checkKnowledgeBoundary(draft);
  const symmetry = checkSymmetry(draft);
  const defensiveness = checkDefensiveness(draft);
  const adversarial = checkAdversarialReversal(draft);

  const doubts = [];

  // 知识边界
  for (const oc of knowledge.overclaims) {
    doubts.push({ area: 'knowledge', question: oc.question, detail: oc.match.slice(0, 40) });
  }

  // 对称性
  for (const rc of symmetry.reversible_claims) {
    doubts.push({ area: 'symmetry', question: rc.question, detail: rc.original.slice(0, 40) });
  }

  // 防御性
  for (const ds of defensiveness.defensive_signals) {
    doubts.push({ area: 'defensiveness', question: ds.question, detail: ds.issue });
  }

  // 反向拆解（第4问）
  for (const ex of adversarial.exploitable) {
    doubts.push({ area: 'adversarial', question: ex.attack, detail: ex.detail, type: ex.type });
  }

  // 门禁判定
  let shouldStop = false;
  let action = 'pass';
  let reason = '通过';

  const knowledgeIssues = knowledge.overclaims.length;
  const symmetryIssues = symmetry.reversible_claims.length;
  const defensivenessIssues = defensiveness.defensive_signals.length;
  const adversarialIssues = adversarial.exploitable.length;

  if (defensivenessIssues > 0) {
    // 防御姿态是最致命的——强制认错格式
    shouldStop = true;
    action = 'block';
    const firstDef = defensiveness.defensive_signals[0];
    reason = `防御姿态: ${firstDef.issue}。认错格式: "关于XX，我说错了。正确的情况是...（如果知道）/ 关于XX我不确定。"`;
  } else if (knowledgeIssues >= 2 || symmetryIssues >= 2 || adversarialIssues >= 3) {
    shouldStop = true;
    action = 'rewrite';
    reason = `过度断言: ${knowledgeIssues}个无依据断言, ${symmetryIssues}个可反转断言, ${adversarialIssues}个可被拆解`;
  } else if (knowledgeIssues > 0 || symmetryIssues > 0 || adversarialIssues > 0) {
    action = 'hedge';
    reason = `有${knowledgeIssues + symmetryIssues + adversarialIssues}处断言需降低确信度`;
  }

  return {
    shouldStop,
    gate: { action, reason },
    knowledge,
    symmetry,
    defensiveness,
    adversarial,
    doubts,
  };
}

module.exports = { doubt, checkKnowledgeBoundary, checkSymmetry, checkDefensiveness, checkAdversarialReversal };
