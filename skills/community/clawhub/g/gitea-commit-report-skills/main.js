import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 生成 Gitea 各仓库进度报告并发送邮件给管理员。
 * 脚本只负责取数据，AI 分析和发邮件由 OpenClaw 根据 skill.md 指示完成。
 * @param {Object} params
 * @param {string} params.repo - 指定仓库，格式：owner/reponame，不填则处理所有可见仓库
 * @param {number} params.hours - 最近 N 小时（会被换算成 since/until）
 * @param {string} params.since - 绝对开始时间（UTC+8），示例：2026-04-01 或 2026-04-01T00:00:00+08:00
 * @param {string} params.until - 绝对结束时间（UTC+8），示例：2026-04-07 或 2026-04-07T23:59:59+08:00
 */
export async function run({ repo = null, hours = 168, since = null, until = null }) {
  const escapeShellArg = (value) => String(value).replace(/["\\$`]/g, "\\$&");

  const toIsoUtcPlus8 = (date) => {
    const pad = (n) => String(n).padStart(2, "0");
    const utcPlus8Date = new Date(date.getTime() + 8 * 3600 * 1000);
    return `${utcPlus8Date.getUTCFullYear()}-${pad(utcPlus8Date.getUTCMonth() + 1)}-${pad(utcPlus8Date.getUTCDate())}T${pad(utcPlus8Date.getUTCHours())}:${pad(utcPlus8Date.getUTCMinutes())}:${pad(utcPlus8Date.getUTCSeconds())}+08:00`;
  };

  if ((!since && !until) && Number.isFinite(hours)) {
    const now = new Date();
    const sinceDate = new Date(now.getTime() - Number(hours) * 3600 * 1000);
    since = toIsoUtcPlus8(sinceDate);
    until = toIsoUtcPlus8(now);
  }

  let cmd = "python scripts/generate_report.py";
  if (since || until) {
    if (!since || !until) {
      return "生成报告失败：使用绝对时间段时，since 和 until 必须同时提供";
    }
    cmd += ` --since "${escapeShellArg(since)}" --until "${escapeShellArg(until)}"`;
  }

  if (repo) {
    cmd += ` --repo "${escapeShellArg(repo)}"`;
  }

  try {
    const output = execSync(cmd, {
      cwd: __dirname,
      encoding: "utf-8",
      timeout: 120000
    });

    const results = JSON.parse(output);

    // 把结构化数据返回给 OpenClaw
    // OpenClaw 会根据 skill.md 的指示自己分析并调用 imap-smtp-email 发邮件
    let response = `已获取 ${results.length} 个仓库的提交数据，请根据以下数据依次为每个仓库生成报告并发送邮件：\n\n`;

    for (const r of results) {
      response += JSON.stringify(r, null, 2);
      response += "\n\n---\n\n";
    }

    return response;

  } catch (error) {
    return `生成报告失败：${error.message}`;
  }
}