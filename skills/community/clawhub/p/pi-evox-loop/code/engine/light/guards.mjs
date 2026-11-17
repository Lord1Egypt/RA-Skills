/**
 * engine/light/guards.mjs — 沉淀侧与召回侧**共享**的质量守卫（0.17.0）
 *
 * 为什么抽到这里：0.16.0 的 autoApprove 缺口实测实锤——retry-log 噪音与未填 FIX
 * 占位符的基因能过召回侧三道守卫被直接注入。根因是质检只发生在召回（消费侧），
 * 沉淀（生产侧）没有任何质检。本模块把守卫**前移到沉淀时**，并让两侧口径**一致**：
 *   - REPAIR_SIGNAL_RE / NARRATION_RE 原先只定义在 evolver-recall.mjs，现在共享；
 *   - depositionGate(strategy) 在 distill/draft --commit 时跑，fail-closed（拒绝入库）。
 */

/** 修法信号守卫：strategy 必须含修法信号词（0.14.x 起召回在用，现共享） */
export const REPAIR_SIGNAL_RE =
	/error|exception|traceback|failed|invalid|cannot|unable|missing|not found|wrong|instead|avoid|fix|encoding\s*[=:]|errors\s*=|utf-?8|gbk|gb18030|latin-1|\brb\b|except|skip/i;

/** 叙述守卫：旁白开场（"Now I understand..." 等）不是可执行修法 */
export const NARRATION_RE =
	/^\s*(now i (understand|see|have|know|remember|need|can)|let me\b|i'?(ll|ve|m)\b|i will\b|here'?s\b|done[.!…]|confirmed[:.]|the output matches|to summarize|summarize\b|first,? i\b|next,? i\b|alright\b|okay\b)/i;

/** 已知噪音签名：私有节点实测 15 条隔离基因的主流形态——"重试后成功"的日志复述 */
export const RETRY_LOG_RE = /retry with corrected args/i;

/** draft 预填但未编辑的占位符 */
const PLACEHOLDER_RE = /<在此填写可执行修法[^>]*>/;

/**
 * 沉淀质检（depositionGate，0.17.0）。
 * 在 distill / draft --commit 时调用；返回 { ok:false, reason } 时调用方必须**拒绝入库**。
 *
 * 设计：质检不过 ≠ 报错羞辱用户，而是给出「下一步怎么改」的可执行指引——
 * 占位符没填 → 去 draft 里补 FIX；retry 日志 → 写"为什么错、怎么改"而不是"重试了"。
 */
export function depositionGate(strategyText) {
	const s = String(strategyText || '');
	if (!s.trim()) return { ok: false, reason: 'strategy 为空：沉淀必须包含可执行修法（AVOID/FIX）', kind: 'empty' };
	if (PLACEHOLDER_RE.test(s)) {
		return { ok: false, kind: 'placeholder', reason: 'FIX 仍是未填写的占位符——请先在 draft 中补上真实修法再提交（占位符基因注入后对下游毫无价值）' };
	}
	if (RETRY_LOG_RE.test(s)) {
		return { ok: false, kind: 'retry-log', reason: '这是「重试后成功」的日志复述，不是修法——沉淀要写：为什么会错（AVOID）+ 以后怎么做才对（FIX），而不是"重试了然后好了"' };
	}
	if (NARRATION_RE.test(s.trim())) {
		return { ok: false, kind: 'narration', reason: '开场是会话旁白（推理流水），不是可执行修法——请直接写：AVOID: 什么坑。FIX: 怎么避开' };
	}
	if (!REPAIR_SIGNAL_RE.test(s)) {
		return { ok: false, kind: 'no-signal', reason: 'strategy 缺少修法信号词（error/fix/avoid/编码 等）——不像在描述一个坑与修法' };
	}
	// 0.22（2026-10-18 复审实证）：AVOID-only 半成品能过闸——REPAIR_SIGNAL_RE 含 avoid 单词，
	// 实测 3 条被截断的 deposit（13/34/62 字符）全是「有坑无修法」形态。有 AVOID 无 FIX 的基因
	// 注入后对下游毫无价值（正是本项目自己的核心结论），闸门必须fail-closed 拒绝。
	const hasFix = /\bfix\b|【FIX|修法/i.test(s);
	if (!hasFix) {
		return { ok: false, kind: 'no-fix', reason: 'strategy 有坑（AVOID）但没有修法（FIX）——半成品基因注入后毫无价值；请补上具体可执行的修法（参数/命令/编码），如「FIX: 用 encoding=gbk 打开」' };
	}
	return { ok: true };
}
