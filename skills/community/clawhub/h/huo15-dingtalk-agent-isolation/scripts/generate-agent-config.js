#!/usr/bin/env node
/**
 * generate-agent-config.js
 *
 * 为钉钉用户生成 Agent 级隔离的 openclaw.json 配置片段
 *
 * 用法:
 *   node generate-agent-config.js --user "张三" --staff-id "abc123" [--agent-id "dingtalk-zhangsan"]
 *   node generate-agent-config.js --batch users.json
 *
 * users.json 格式:
 *   [
 *     { "name": "张三", "staffId": "abc123" },
 *     { "name": "李四", "staffId": "def456" }
 *   ]
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--user") opts.user = args[++i];
    else if (args[i] === "--staff-id") opts.staffId = args[++i];
    else if (args[i] === "--agent-id") opts.agentId = args[++i];
    else if (args[i] === "--batch") opts.batch = args[++i];
    else if (args[i] === "--channel") opts.channel = args[++i] || "dingtalk-connector";
    else if (args[i] === "--account-id") opts.accountId = args[++i] || "default";
    else if (args[i] === "--output") opts.output = args[++i];
    else if (args[i] === "--help" || args[i] === "-h") {
      console.log(`用法:
  node generate-agent-config.js --user "张三" --staff-id "abc123"
  node generate-agent-config.js --batch users.json

选项:
  --user        用户名称（用于生成 agent ID）
  --staff-id    钉钉 senderStaffId
  --agent-id    自定义 Agent ID（可选，默认自动生成）
  --channel     渠道 ID（默认: dingtalk-connector）
  --account-id  账号 ID（默认: default）
  --batch       批量导入，传入 JSON 文件路径
  --output      输出文件路径（可选，默认打印到终端）
`);
      process.exit(0);
    }
  }
  return opts;
}

function slugify(name) {
  // 中文直接保留，英文转小写
  return name
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9\u4e00-\u9fff-]/g, "");
}

function generateAgent(name, staffId, opts) {
  const agentId = opts.agentId || `dingtalk-${slugify(name)}`;
  const workspace = `~/.openclaw/workspace-${agentId}`;
  const agentDir = `~/.openclaw/agents/${agentId}/agent`;

  return {
    agent: {
      id: agentId,
      workspace,
      agentDir,
    },
    binding: {
      agentId,
      match: {
        channel: opts.channel || "dingtalk-connector",
        accountId: opts.accountId || "default",
        peer: { kind: "direct", id: staffId },
      },
    },
  };
}

function main() {
  const opts = parseArgs();

  let users = [];
  if (opts.batch) {
    users = JSON.parse(fs.readFileSync(opts.batch, "utf-8"));
  } else if (opts.user && opts.staffId) {
    users = [{ name: opts.user, staffId: opts.staffId }];
  } else {
    console.error("请提供 --user 和 --staff-id，或使用 --batch 批量导入");
    process.exit(1);
  }

  const agents = [];
  const bindings = [];
  const mkdirCommands = [];

  for (const user of users) {
    const result = generateAgent(user.name, user.staffId, { ...opts, agentId: user.agentId });
    agents.push(result.agent);
    bindings.push(result.binding);
    mkdirCommands.push(`mkdir -p ${result.agent.workspace.replace("~", "$HOME")}`);
    mkdirCommands.push(`mkdir -p ${result.agent.agentDir.replace("~", "$HOME")}`);
  }

  const output = {
    agents: agents,
    bindings: bindings,
    setup_commands: mkdirCommands,
  };

  const json = JSON.stringify(output, null, 2);

  if (opts.output) {
    fs.writeFileSync(opts.output, json + "\n");
    console.log(`配置已写入: ${opts.output}`);
  } else {
    console.log(json);
  }

  console.error("\n--- 操作步骤 ---");
  console.error("1. 将上面的 agents 合并到 openclaw.json 的 agents.list 中");
  console.error("2. 将上面的 bindings 合并到 openclaw.json 的 bindings 数组中");
  console.error("3. 运行以下命令创建目录:");
  console.error(mkdirCommands.join("\n"));
  console.error("4. 重启 OpenClaw: openclaw restart");
}

main();
