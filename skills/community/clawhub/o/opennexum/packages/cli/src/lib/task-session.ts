import { TaskStatus, type Task } from '@nexum/core';

export type TaskSessionRole = 'generator' | 'evaluator';

export interface TaskSessionSnapshot {
  role: TaskSessionRole;
  sessionKey?: string;
  streamLog?: string;
}

type TaskSessionFields = Pick<
  Task,
  | 'status'
  | 'acp_session_key'
  | 'acp_stream_log'
  | 'generator_acp_session_key'
  | 'generator_acp_stream_log'
  | 'evaluator_acp_session_key'
  | 'evaluator_acp_stream_log'
>;

export function getTaskSession(task: TaskSessionFields, role: TaskSessionRole): TaskSessionSnapshot {
  if (role === 'generator') {
    return {
      role,
      sessionKey:
        task.generator_acp_session_key ??
        (task.evaluator_acp_session_key ? undefined : task.acp_session_key),
      streamLog:
        task.generator_acp_stream_log ??
        (task.evaluator_acp_stream_log ? undefined : task.acp_stream_log),
    };
  }

  return {
    role,
    sessionKey:
      task.evaluator_acp_session_key ??
      (task.status === TaskStatus.Evaluating ? task.acp_session_key : undefined),
    streamLog:
      task.evaluator_acp_stream_log ??
      (task.status === TaskStatus.Evaluating ? task.acp_stream_log : undefined),
  };
}

export function getDisplaySession(task: TaskSessionFields): TaskSessionSnapshot {
  if (task.status === TaskStatus.Running) {
    return getTaskSession(task, 'generator');
  }

  const evaluatorSession = getTaskSession(task, 'evaluator');
  if (evaluatorSession.sessionKey || evaluatorSession.streamLog) {
    return evaluatorSession;
  }

  return getTaskSession(task, 'generator');
}

export function getTrackedSessions(task: TaskSessionFields): TaskSessionSnapshot[] {
  return (['generator', 'evaluator'] as const)
    .map((role) => getTaskSession(task, role))
    .filter((session) => Boolean(session.sessionKey || session.streamLog));
}
