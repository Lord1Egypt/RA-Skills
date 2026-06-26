const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\Admin\\.openclaw\\workspace-robotB\\feishu-worklist\\SKILL.md', 'utf8');
const marker = '\uFEFF';
const cleanContent = content.startsWith(marker) ? content.slice(1) : content;
const lines = cleanContent.split('\n');

let startIdx = lines.findIndex(l => l.startsWith('---'));
let endIdx = lines.findIndex((l, i) => i > startIdx && l.startsWith('---'));

const rest = lines.slice(endIdx).join('\n');

const newHeader = `---
name: feishu-worklist
description: |
  飞书多维表格个人工作台账管理系统。帮助用户在 OpenClaw + 飞书环境下搭建个人工作清单管理台账。

  **【强制】触发后必读规则:**
  听到以下任意触发词后，**必须先读取本 SKILL.md 全文并严格按文档流程执行**，不得跳过文档直接处理：
  - 中文: "创建个人工作台账" / "记一下这个工作" + 任务内容
  - English: "create worklist" / "add task" + task content

  **强触发词(直接执行):**
  - 中文: "创建个人工作台账" / "记一下这个工作" + 任务内容
  - English: "create worklist" / "add task" + task content

  **弱触发词(询问确认):**
  - 中文: 用户发送工作相关内容(时间节点、优先级、任务描述等)→ 询问"是否要录入工作台账?"
  - English: User sends work-related content (time, priority, task description) → ask "Would you like to add this to your worklist?"

  **异常诊断触发:**
  - 中文: "台账不工作了" / "数据没更新" / "操作没反应" / "诊断"
  - English: "worklist not working" / "data not updated" / "no response" / "diagnose"
  → 触发 health_check.js 执行5项快速诊断(网络/凭证/表格/字段)

  **排除条件:**
  - 与工作任务无关的内容不录入
  - 用户明确表示不需要记录的内容不录入
  - 非工作相关的闲聊不处理

  **🚨 系统操作红线(强制):**
  - 本 skill 全生命周期内,任何涉及修改用户电脑配置、OpenClaw 配置、系统环境变量的操作,**必须经用户明确确认后方可实施**
  - 未获确认前,此类操作严格禁止,违者视为违反使用规范
  - 可安全执行的操作(读写文件、调用飞书 API、数据处理)不受此限
---`;

fs.writeFileSync('C:\\Users\\Admin\\.openclaw\\workspace-robotB\\feishu-worklist\\SKILL.md', newHeader + '\n' + rest, 'utf8');
console.log('done');