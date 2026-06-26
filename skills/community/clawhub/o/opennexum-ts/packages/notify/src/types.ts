export enum NotifyLevel {
  info = "info",
  warn = "warn",
  error = "error",
}

export interface DispatchNotification {
  type: "dispatch";
  level: NotifyLevel;
  taskId: string;
  taskName: string;
  agentId: string;
  scopeCount: number;
  deliverablesCount: number;
  progress: string;
}

export interface CompleteNotification {
  type: "complete";
  level: NotifyLevel;
  taskId: string;
  taskName: string;
  elapsedMs: number;
  iteration: number;
  passCount: number;
  totalCount: number;
  unlockedTasks: string[];
  progress: string;
}

export interface FailNotification {
  type: "fail";
  level: NotifyLevel;
  taskId: string;
  taskName: string;
  iteration: number;
  passCount: number;
  totalCount: number;
  failCount: number;
  failedCriteria: string[];
  feedbackExcerpt: string;
}

export interface BatchDoneNotification {
  type: "batch_done";
  level: NotifyLevel;
  projectName: string;
  tasks: Array<{
    taskId: string;
    taskName: string;
    status: "done" | "fail";
    elapsedMs: number;
  }>;
}
