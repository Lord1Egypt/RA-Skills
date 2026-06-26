export enum ErrorCode {
  TASK_NOT_FOUND = "TASK_NOT_FOUND",
  CONTRACT_NOT_FOUND = "CONTRACT_NOT_FOUND",
  INVALID_VERDICT = "INVALID_VERDICT",
  CONFIG_INVALID = "CONFIG_INVALID",
  GIT_ERROR = "GIT_ERROR",
  SESSION_TIMEOUT = "SESSION_TIMEOUT",
}

export class NexumError extends Error {
  code: string;

  constructor(message: string, code: ErrorCode) {
    super(message);
    this.name = "NexumError";
    this.code = code;
  }
}
