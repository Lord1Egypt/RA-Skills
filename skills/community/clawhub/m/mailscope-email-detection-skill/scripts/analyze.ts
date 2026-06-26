/**
 * Mailscope Email Security Analyzer
 *
 * 邮件安全检测脚本 - 上传 .eml 文件到分析平台并生成安全报告。
 *
 * Usage: npx tsx scripts/analyze.ts <path/to/email.eml>
 */

import { readFileSync, existsSync } from "node:fs";
import { resolve, basename } from "node:path";

// ── Constants ──────────────────────────────────────────────────────────

/** API 服务地址 (内部固定，不对外暴露配置) */
const API_BASE_URL = "https://x.lizhisec.com";

/** 轮询间隔 (毫秒) */
const POLL_INTERVAL_MS = 3000;

/** 最大轮询次数 (超时时间 = MAX_POLLS * POLL_INTERVAL_MS) */
const MAX_POLLS = 100;

// ── Helpers ────────────────────────────────────────────────────────────

function loadApiKey(): string {
  const skillRoot = resolve(import.meta.dirname, "..");
  const configPath = resolve(skillRoot, "config.json");
  const examplePath = resolve(skillRoot, "config.json.example");

  if (!existsSync(configPath)) {
    console.error("❌ 配置文件未找到: config.json");
    console.error(`   请将 ${examplePath} 复制为 config.json 并填入你的 API Key`);
    console.error("   API Key 申请地址: https://x.lizhisec.com");
    process.exit(1);
  }

  let config: { api_key?: string };
  try {
    config = JSON.parse(readFileSync(configPath, "utf-8"));
  } catch {
    console.error("❌ 配置文件格式错误: config.json 不是有效的 JSON");
    process.exit(1);
  }

  if (!config.api_key || config.api_key === "msk_your_api_key_here") {
    console.error("❌ 请先在 config.json 中填入你的 API Key");
    console.error("   API Key 申请地址: https://x.lizhisec.com");
    process.exit(1);
  }

  return config.api_key;
}

function fmtTs(ts: number | null | undefined): string {
  if (!ts) return "未知";
  try {
    return new Date(ts * 1000).toLocaleString("zh-CN", {
      timeZone: "Asia/Shanghai",
    });
  } catch {
    return String(ts);
  }
}

// ── API Client ─────────────────────────────────────────────────────────

async function uploadEmail(
  filePath: string,
  apiKey: string,
): Promise<{ record_id: number; file_hash: string }> {
  const fileBuffer = readFileSync(filePath);
  const blob = new Blob([fileBuffer]);
  const form = new FormData();
  form.append("file", blob, basename(filePath));

  const res = await fetch(`${API_BASE_URL}/api/v1/workspace/upload`, {
    method: "POST",
    headers: { "X-API-Key": apiKey },
    body: form,
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(
      `上传失败 (HTTP ${res.status}): ${body}`,
    );
  }

  const data = await res.json();
  if (!data.record_id) {
    throw new Error(`上传返回异常: ${JSON.stringify(data)}`);
  }

  return { record_id: data.record_id, file_hash: data.file_hash };
}

async function pollAnalysis(
  recordId: number,
  apiKey: string,
): Promise<unknown> {
  for (let i = 0; i < MAX_POLLS; i++) {
    const res = await fetch(
      `${API_BASE_URL}/api/v1/analysis/records/${recordId}`,
      { headers: { "X-API-Key": apiKey } },
    );

    if (!res.ok) {
      throw new Error(
        `查询分析结果失败 (HTTP ${res.status}): ${await res.text()}`,
      );
    }

    const data = await res.json();

    if (data.status === "succeeded") {
      return data;
    }

    if (data.status === "failed") {
      const msg = data.message || data.error || "未知错误";
      throw new Error(`邮件分析失败: ${msg}`);
    }

    // 仍在排队 / 分析中
    const elapsed = (i + 1) * (POLL_INTERVAL_MS / 1000);
    process.stdout.write(
      `\r⏳ 分析中... (${elapsed}s) [${"·".repeat((i % 3) + 1)}]  `,
    );

    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));
  }

  throw new Error(
    `分析超时: 已等待 ${(MAX_POLLS * POLL_INTERVAL_MS) / 1000}s, 仍未完成`,
  );
}

// ── Type helpers ────────────────────────────────────────────────────────

interface EmailMeta {
  subject: string;
  from_display: string;
  from_address: string;
  return_path: string;
  to: string[];
  cc: string[];
  date_str: string;
  date_ts: number;
  message_id: string;
  reply_to: string;
}

interface SenderIdentity {
  header_from_domain: string;
  return_path_domain: string;
  domains_match: boolean;
  spoofing_risk: boolean;
  spf: { result: string; detail: string };
  dkim: { result: string; detail: string };
  dmarc: { result: string; detail: string };
  sender_ip: string;
  domain_profile: {
    domain: string;
    registered_at: number;
    expires_at: number;
    updated_at: number | null;
    internet_info: string;
  };
}

interface Attachment {
  filename: string;
  sha256: string;
  md5: string;
  file_type_label: string;
  mime_type: string;
  is_archive: boolean;
  is_document: boolean;
  has_vba: boolean;
  macros: unknown[];
  archive_entries: unknown[];
  children: unknown[];
  error: string | null;
  minio_path: string;
}

interface AIAnalysis {
  classification: string;
  summary: string;
  analysis: {
    identity_verification: string;
    behavior_relationship: string;
    intent_recognition: string;
    comprehensive_judgment: string;
  };
  confidence: number;
}

interface ReceivedHop {
  from_host: string;
  by_host: string;
  ip: string;
  timestamp: number;
}

interface AnalysisResult {
  record_id: number;
  email_meta: EmailMeta;
  sender_identity: SenderIdentity;
  received_chain: ReceivedHop[];
  body: { content_type: string; markdown: string; text_preview: string; qrcodes: unknown[] };
  urls: unknown[];
  attachments: Attachment[];
  ai_analysis: AIAnalysis;
}

interface AnalysisResponse {
  record_id: number;
  status: string;
  subject?: string;
  from_address?: string;
  security_tier?: string;
  result: AnalysisResult;
}

// ── Report Renderer ────────────────────────────────────────────────────

function renderReport(data: AnalysisResponse): string {
  const r = data.result;
  const meta = r.email_meta;
  const ident = r.sender_identity;
  const dp = ident.domain_profile;
  const ai = r.ai_analysis;

  const tierLabel = data.security_tier?.toUpperCase() || "UNKNOWN";
  const tierIcon =
    data.security_tier === "clean"
      ? "🟢"
      : data.security_tier === "risky"
        ? "🔴"
        : "🟡";

  const confidencePct = ai.confidence ? `${(ai.confidence * 100).toFixed(0)}%` : "N/A";

  // 基本行
  const lines: string[] = [];

  lines.push("");
  lines.push("════════════════════════════════════════════════════════════");
  lines.push("                 邮 件 安 全 分 析 报 告");
  lines.push("════════════════════════════════════════════════════════════");
  lines.push("");
  lines.push(`  ${tierIcon} 风险等级: ${ai.classification || tierLabel}   置信度: ${confidencePct}`);
  lines.push("");

  // ── 基本信息
  lines.push("━━━ 基本信息 ━━━");
  lines.push("");
  const fromDisplay = meta.from_display || `${meta.from_address}`;
  const toDisplay = meta.to?.join("; ") || "无";
  lines.push(`  发件人:      ${fromDisplay}`);
  lines.push(`  收件人:      ${toDisplay}`);
  lines.push(`  主题:        ${meta.subject || "无主题"}`);
  lines.push(`  发送时间:    ${meta.date_str || "未知"}`);
  if (meta.message_id) lines.push(`  邮件 ID:     ${meta.message_id}`);
  if (meta.reply_to) lines.push(`  回复地址:    ${meta.reply_to}`);
  if (meta.return_path) lines.push(`  退信路径:    ${meta.return_path}`);
  lines.push("");

  // ── 发送方身份认证
  lines.push("━━━ 发送方身份认证 ━━━");
  lines.push("");
  lines.push(`  发件域名:      ${ident.header_from_domain || "无"}`);
  lines.push(`  退信域名:      ${ident.return_path_domain || "(空)"}`);
  lines.push(`  域名一致性:    ${ident.domains_match ? "✅ 一致" : "⚠️ 不一致"}`);
  lines.push(`  伪造风险:      ${ident.spoofing_risk ? "⚠️ 存在伪造风险" : "✅ 未检测到伪造"}`);
  lines.push("");
  lines.push("  ┌── 邮件认证 ──────────────");
  lines.push(`  │ SPF:    ${ident.spf?.result || "unknown"} ${ident.spf?.detail ? "- " + ident.spf.detail : ""}`);
  lines.push(`  │ DKIM:   ${ident.dkim?.result || "unknown"} ${ident.dkim?.detail ? "- " + ident.dkim.detail : ""}`);
  lines.push(`  │ DMARC:  ${ident.dmarc?.result || "unknown"} ${ident.dmarc?.detail ? "- " + ident.dmarc.detail : ""}`);
  lines.push("  └──────────────────────────");
  lines.push("");
  if (ident.sender_ip) lines.push(`  发送 IP:       ${ident.sender_ip}`);
  lines.push("");
  lines.push("  ┌── 域名信息 ──────────────");
  lines.push(`  │ 域名:         ${dp.domain || "无"}`);
  lines.push(`  │ 注册时间:     ${fmtTs(dp.registered_at)}`);
  lines.push(`  │ 过期时间:     ${fmtTs(dp.expires_at)}`);
  lines.push(`  │ ICP 备案:     ${dp.internet_info || "未查询到"}`);
  lines.push("  └──────────────────────────");
  lines.push("");

  // ── 传输链路
  if (r.received_chain?.length) {
    lines.push("━━━ 邮件传输链路 ━━━");
    lines.push("");
    for (let i = 0; i < r.received_chain.length; i++) {
      const hop = r.received_chain[i];
      const arrow = i === 0 ? "  ╭──" : "  ├──";
      lines.push(`${arrow} ${hop.from_host || "?"} → ${hop.by_host || "?"}`);
      lines.push(`  │   时间: ${fmtTs(hop.timestamp)}    IP: ${hop.ip || "未知"}`);
    }
    lines.push("  ╰── 到达");
    lines.push("");
  }

  // ── 邮件正文
  lines.push("━━━ 邮件正文内容 ━━━");
  lines.push("");
  const body = r.body;
  if (body?.text_preview) {
    const preview = body.text_preview.length > 2000
      ? body.text_preview.slice(0, 2000) + "\n  ...(内容已截断)"
      : body.text_preview;
    // 添加缩进
    for (const line of preview.split("\n")) {
      lines.push(`  │ ${line}`);
    }
  } else {
    lines.push("  (无正文内容)");
  }
  lines.push("");
  if (body?.content_type) {
    lines.push(`  正文类型: ${body.content_type}`);
    lines.push("");
  }

  // ── URL 列表
  if (r.urls?.length) {
    lines.push("━━━ 包含 URL ━━━");
    lines.push("");
    for (const u of r.urls) {
      lines.push(`  🔗 ${String(u)}`);
    }
    lines.push("");
  } else {
    lines.push("━━━ 包含 URL ━━━");
    lines.push("");
    lines.push("  (未发现 URL 链接)");
    lines.push("");
  }

  // ── 附件分析
  if (r.attachments?.length) {
    lines.push("━━━ 附件分析 ━━━");
    for (const att of r.attachments) {
      lines.push("");
      lines.push(`  文件名:       ${att.filename}`);
      lines.push(`  类型:         ${att.file_type_label || "未知"} (${att.mime_type || "未知"})`);
      lines.push(`  SHA256:       ${att.sha256}`);
      lines.push(`  MD5:          ${att.md5}`);
      if (att.is_document) lines.push(`  文档类型:     是`);
      if (att.is_archive) lines.push(`  压缩包:       是`);
      if (att.has_vba) lines.push(`  ⚠️ 含 VBA 宏:  是 - 高风险`);
      if (att.macros?.length) lines.push(`  宏信息:       ${JSON.stringify(att.macros)}`);
      if (att.error) lines.push(`  ⚠️ 解析错误:   ${att.error}`);

      // 检查文件名与实际类型是否伪装
      const ext = att.filename?.split(".").pop()?.toLowerCase();
      const typeLabel = att.file_type_label?.toLowerCase();
      if (ext && typeLabel && ext !== typeLabel) {
        const knownMismatches: Record<string, string> = {
          docx: "Word 文档 (.docx)",
          doc: "Word 文档 (.doc)",
          xlsx: "Excel 表格 (.xlsx)",
          xls: "Excel 表格 (.xls)",
          pdf: "PDF 文档",
          zip: "ZIP 压缩包",
          rar: "RAR 压缩包",
        };
        const extDesc = knownMismatches[ext] || `.${ext}`;
        const typeDesc = knownMismatches[typeLabel] || typeLabel;
        lines.push(`  🔴 类型伪装:   文件扩展名为 ${extDesc}，实际类型为 ${typeDesc}`);
      }
    }
    lines.push("");
  } else {
    lines.push("━━━ 附件分析 ━━━");
    lines.push("");
    lines.push("  (无附件)");
    lines.push("");
  }

  // ── AI 综合分析
  lines.push("━━━ AI 综合分析 ━━━");
  lines.push("");
  lines.push(`  分类:  ${ai.classification}`);
  lines.push("");
  lines.push(`  【摘要】`);
  lines.push(`  ${wrapText(ai.summary, 68)}`);
  lines.push("");
  lines.push(`  【身份验证分析】`);
  lines.push(`  ${wrapText(ai.analysis.identity_verification, 68)}`);
  lines.push("");
  lines.push(`  【行为关联分析】`);
  lines.push(`  ${wrapText(ai.analysis.behavior_relationship, 68)}`);
  lines.push("");
  lines.push(`  【意图识别分析】`);
  lines.push(`  ${wrapText(ai.analysis.intent_recognition, 68)}`);
  lines.push("");
  lines.push(`  【综合判断】`);
  lines.push(`  ${wrapText(ai.analysis.comprehensive_judgment, 68)}`);
  lines.push("");

  // ── 建议
  lines.push("━━━ 建议措施 ━━━");
  lines.push("");
  const tier = data.security_tier;
  if (tier === "clean") {
    lines.push("  ✅ 该邮件经检测为安全邮件，可正常处理。");
  } else if (tier === "risky") {
    lines.push("  ⚠️  该邮件存在安全风险，建议采取以下措施：");
    lines.push("");
    lines.push("  1. 立即隔离该邮件，不要转发或打开附件");
    lines.push("  2. 将发件人域名加入黑名单");
    lines.push("  3. 通知收件人及相关人员注意防范");
    lines.push("  4. 如需进一步取证分析请保留原始 .eml 文件");
    if (r.attachments?.length) {
      lines.push("  5. 切勿尝试打开附件或输入邮件中提供的密码");
    }
  } else {
    lines.push("  请结合上述分析内容自行判断。");
  }
  lines.push("");
  lines.push("════════════════════════════════════════════════════════════");
  lines.push("");

  return lines.join("\n");
}

/** 中文友好文本折行 (按指定宽度) */
function wrapText(text: string, width: number): string {
  if (!text) return "(无)";
  // 简单策略: 按标点分割，"连贯块"挨个放，在宽度处折行
  const parts = text.split(/(?<=[。，；：、！？])/);
  const out: string[] = [];
  let line = "";
  for (const part of parts) {
    if ((line + part).length <= width) {
      line += part;
    } else {
      if (line) out.push(line);
      line = part;
    }
  }
  if (line) out.push(line);
  return out.join("\n  ");
}

// ── Main ───────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error("Usage: npx tsx scripts/analyze.ts <path/to/email.eml>");
    process.exit(1);
  }

  const filePath = resolve(args[0]);

  if (!existsSync(filePath)) {
    console.error(`❌ 文件不存在: ${filePath}`);
    process.exit(1);
  }

  const apiKey = loadApiKey();

  // 1. 上传邮件
  console.log(`\n📤 正在上传: ${basename(filePath)}`);
  let uploadResult: { record_id: number; file_hash: string };
  try {
    uploadResult = await uploadEmail(filePath, apiKey);
  } catch (e) {
    console.error(
      `\n❌ 上传失败: ${e instanceof Error ? e.message : String(e)}`,
    );
    process.exit(1);
  }

  console.log(`✅ 上传成功 (record_id: ${uploadResult.record_id})`);
  console.log(`   file_hash: ${uploadResult.file_hash}`);
  console.log("");

  // 2. 轮询结果
  let analysisData: AnalysisResponse;
  try {
    analysisData = (await pollAnalysis(
      uploadResult.record_id,
      apiKey,
    )) as AnalysisResponse;
  } catch (e) {
    console.error(
      `\n❌ 分析失败: ${e instanceof Error ? e.message : String(e)}`,
    );
    process.exit(1);
  }

  console.log("\r✅ 分析完成!" + " ".repeat(30));
  console.log("");

  // 3. 移除 raw_headers 和 raw_source 字段
  if (analysisData.result) {
    delete (analysisData.result as Record<string, unknown>).raw_headers;
    delete (analysisData.result as Record<string, unknown>).raw_source;
    delete (analysisData.result as Record<string, unknown>).preview_screenshot_path;
  }

  // 4. 渲染并输出报告
  console.log(renderReport(analysisData));
}

main().catch((e) => {
  console.error(`\n❌ 未预期的错误: ${e instanceof Error ? e.message : String(e)}`);
  process.exit(1);
});
