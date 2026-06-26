import type { MailFindResult } from "../types/contracts";
import type { TriggerDecision } from "../parsers/trigger";

export interface ReplyFormatOptions {
  maxBodyPreviewChars: number;
  includeSubject: boolean;
  includeFrom: boolean;
  includeReceivedAt: boolean;
}

function truncate(input: string, limit: number): string {
  if (input.length <= limit) {
    return input;
  }
  return `${input.slice(0, Math.max(0, limit - 1))}...`;
}

export function formatMailReply(
  email: string,
  result: MailFindResult,
  options: ReplyFormatOptions
): string {
  if (!result.found) {
    if (result.reason === "timeout") {
      return `监控超时，邮箱 ${email} 在等待窗口内没有匹配的新邮件。`;
    }
    return `未找到匹配邮件：${email}`;
  }

  const lines: string[] = [];
  lines.push("已找到最新邮件");
  lines.push(`邮箱：${email}`);
  if (options.includeSubject && result.subject) {
    lines.push(`主题：${result.subject}`);
  }
  if (options.includeFrom && result.from) {
    lines.push(`发件人：${result.from}`);
  }
  if (options.includeReceivedAt && result.receivedAt) {
    lines.push(`时间：${result.receivedAt}`);
  }
  if (result.bodyPreview) {
    lines.push(`内容：${truncate(result.bodyPreview, options.maxBodyPreviewChars)}`);
  }
  if (result.extractedFields?.code) {
    lines.push(`验证码：${result.extractedFields.code}`);
  }
  return lines.join("\n");
}

export function formatClarificationMessage(decision: TriggerDecision): string {
  if (decision.kind !== "clarify") {
    return "无法解析输入，请提供一个邮箱地址。";
  }
  if (decision.reason === "multiple_emails" && decision.emails?.length) {
    return `检测到多个邮箱：${decision.emails.join("，")}。请只发送一个邮箱。`;
  }
  if (decision.reason === "missing_email") {
    return "未检测到邮箱地址，请按示例发送：/mail someone@example.com";
  }
  return "无法解析输入，请按示例发送：/mail someone@example.com";
}

