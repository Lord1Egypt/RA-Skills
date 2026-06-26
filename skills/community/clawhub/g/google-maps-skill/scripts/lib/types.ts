import { isRecord } from "./config.ts";

export interface FlagDef {
  description: string;
  required: boolean;
  placeholder: string;
  validate?: (value: string) => string | null;
}

export interface HttpResult {
  status: number;
  payload: unknown;
}

export interface CommandDef {
  name: string;
  description: string;
  usage: string;
  method: "GET" | "POST";
  url: string;
  auth: "query" | "header";
  fieldMask?: string;
  flags: Record<string, FlagDef>;
  buildUrl?: (flags: Record<string, string>) => string;
  buildRequest: (flags: Record<string, string>) => { params?: Record<string, string>; body?: unknown };
  checkSuccess: (httpStatus: number, payload: unknown) => boolean;
  getErrorMessage: (payload: unknown) => string;
}

export function checkLegacySuccess(_httpStatus: number, payload: unknown): boolean {
  if (!isRecord(payload)) {
    return false;
  }
  return payload.status === "OK";
}

export function checkNewApiSuccess(httpStatus: number, _payload: unknown): boolean {
  return httpStatus >= 200 && httpStatus < 300;
}

export function getLegacyErrorMessage(payload: unknown): string {
  if (!isRecord(payload)) {
    return "Unknown API response format";
  }
  if (typeof payload.error_message === "string" && payload.error_message.length > 0) {
    return payload.error_message;
  }
  if (typeof payload.status === "string" && payload.status.length > 0) {
    return payload.status;
  }
  return "Unknown API error";
}

export function getNewApiErrorMessage(payload: unknown): string {
  if (!isRecord(payload)) {
    return "Unknown API response format";
  }
  if (isRecord(payload.error) && typeof payload.error.message === "string") {
    return payload.error.message;
  }
  if (typeof payload.message === "string" && payload.message.length > 0) {
    return payload.message;
  }
  return "Unknown API error";
}
