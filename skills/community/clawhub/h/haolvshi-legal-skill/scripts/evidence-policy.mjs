// 这段文字会附在每一次命令输出上，因此只保留模型执行下一步所需的约束；
// 完整、可机读的边界仍由 currentTaskEvidencePolicy 返回。
export const CURRENT_TASK_EVIDENCE_INSTRUCTION = '仅以当前任务信息和同一 sessionId 作答；禁用全局记忆、其他任务和猜测，缺信息即询问用户。';

const ALLOWED_SOURCES = [
  'current_task_user_messages',
  'current_task_user_materials',
  'current_session_saved_answers',
  'current_task_explicit_corrections'
];

const FORBIDDEN_SOURCES = [
  'persistent_or_global_memory',
  'memory_tools_or_memory_search',
  'user_profile_or_persona_memory',
  'other_tasks',
  'other_threads_or_conversations',
  'old_cases_or_reports_not_supplied_in_current_task',
  'skill_examples',
  'evaluation_cases',
  'handoff_documents',
  'test_records_or_logs'
];

export function currentTaskEvidencePolicy(sessionId = null) {
  return {
    mode: 'current_task_only',
    scope: 'current_task_thread',
    sessionId: sessionId || null,
    allowedSources: [...ALLOWED_SOURCES],
    forbiddenSources: [...FORBIDDEN_SOURCES],
    globalMemoryAllowed: false,
    memoryToolAllowed: false,
    crossTaskMemoryAllowed: false,
    otherConversationHistoryAllowed: false,
    userProfileMemoryAllowed: false,
    examplesAreEvidence: false,
    currentUserMessageMustRemainLiteral: true,
    currentUserQueryMustNotBeExpandedWithMemory: true,
    reuseSavedAnswersOnlyForExactSessionId: true,
    onMissingCurrentTaskEvidence: 'ask_user'
  };
}

export function prependCurrentTaskEvidenceInstruction(prompt = '') {
  const text = String(prompt || '').trim();
  return text ? `${CURRENT_TASK_EVIDENCE_INSTRUCTION}\n\n${text}` : CURRENT_TASK_EVIDENCE_INSTRUCTION;
}
