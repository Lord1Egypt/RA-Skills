'use strict';

/**
 * project-init Skill - main.js
 * OpenClaw 对话入口：收集仓库信息，调用初始化脚本
 *
 * 对话状态机（6步）：
 *   idle → collecting_name → collecting_desc → collecting_creator
 *        → collecting_members → collecting_private → confirming → running
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const SKILL_DIR = __dirname;
const STATE_FILE = path.join(os.tmpdir(), 'project-init-state.json');

// ── 状态读写 ──────────────────────────────────────────────
function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { step: 'idle', data: {} };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
}

function clearState() {
  try { fs.unlinkSync(STATE_FILE); } catch {}
}

// ── 触发词检测 ────────────────────────────────────────────
function isInitTrigger(msg) {
  return /初始化|新建仓库|建.*仓库|create.*repo|init.*repo/i.test(msg);
}

function extractRepoName(msg) {
  const m = msg.match(/初始化\s+([\w\-]+)|建.*仓库.*[叫名为是]\s*([\w\-]+)|([\w\-]+)\s*仓库/);
  if (m) return m[1] || m[2] || m[3];
  return null;
}

// ── 调用初始化脚本 ─────────────────────────────────────────
function runInit(data) {
  const scriptPath = path.join(SKILL_DIR, 'scripts', 'init_repo.py');

  const args = [
    scriptPath,
    '--repo-name',   data.repoName,
    '--description', data.description,
    '--private',     data.isPrivate ? 'true' : 'false',
    '--creator',     data.creator,
  ];

  if (data.members && data.members.length > 0) {
    args.push('--members', data.members.join(','));
  }

  const result = spawnSync('python3', args, {
    encoding: 'utf8',
    timeout: 60000,
  });

  return {
    success: result.status === 0,
    stdout: result.stdout || '',
    stderr: result.stderr || '',
  };
}

// ── 主处理函数 ────────────────────────────────────────────
function handle(userMessage, context) {
  const msg = (userMessage || '').trim();
  let state = loadState();

  // 随时可取消
  if (/取消|cancel|退出|quit/i.test(msg) && state.step !== 'idle') {
    clearState();
    return '已取消仓库初始化。';
  }

  switch (state.step) {

    // ── Step 0: 检测触发词 ──────────────────────────────────
    case 'idle': {
      if (!isInitTrigger(msg)) return null;

      const extracted = extractRepoName(msg);
      state = { step: 'collecting_name', data: {} };

      if (extracted) {
        state.data.repoName = extracted;
        state.step = 'collecting_desc';
        saveState(state);
        return `好的，我来帮你初始化仓库 \`${extracted}\`。\n\n**第 1 步**：请给这个项目写一句简短的描述（会写入 README）：`;
      }

      saveState(state);
      return '好的，我来帮你创建并初始化仓库。\n\n**第 1 步**：请输入仓库名称（英文，用于 URL，例如：`dexterous-hand-tactile`）：';
    }

    // ── Step 1: 收集仓库名 ──────────────────────────────────
    case 'collecting_name': {
      if (!msg) return '仓库名称不能为空，请重新输入：';
      if (!/^[\w][\w\-]*$/.test(msg)) {
        return '仓库名称只能包含字母、数字和连字符（-），且不能以连字符开头，请重新输入：';
      }
      state.data.repoName = msg;
      state.step = 'collecting_desc';
      saveState(state);
      return `**第 2 步**：请输入项目描述（一两句话说明这个仓库是做什么的）：`;
    }

    // ── Step 2: 收集描述 ────────────────────────────────────
    case 'collecting_desc': {
      if (!msg) return '描述不能为空，请重新输入：';
      state.data.description = msg;
      state.step = 'collecting_creator';
      saveState(state);
      return `**第 3 步**：请输入你的 Gitea 用户名（将作为仓库负责人，拥有管理员权限）：`;
    }

    // ── Step 3: 收集创建者 ──────────────────────────────────
    case 'collecting_creator': {
      if (!msg) return '用户名不能为空，请重新输入：';
      state.data.creator = msg;
      state.step = 'collecting_members';
      saveState(state);
      return `**第 4 步**：请输入其他参与成员的 Gitea 用户名，多人用逗号分隔。\n（选填，成员将以只读权限加入仓库，并收到邮件通知。直接回车跳过）：`;
    }

    // ── Step 4: 收集成员 ────────────────────────────────────
    case 'collecting_members': {
      if (msg) {
        const members = msg.split(/[,，\s]+/).map(s => s.trim()).filter(Boolean);
        // 排除创建者本人，避免重复（创建者已单独设为 admin）
        state.data.members = members.filter(m => m !== state.data.creator);
      } else {
        state.data.members = [];
      }
      state.step = 'collecting_private';
      saveState(state);
      return `**第 5 步**：是否设为私有仓库？\n- 输入 \`y\` 或 \`是\` → 私有\n- 直接回车 → 公开（默认）`;
    }

    // ── Step 5: 收集可见性 ──────────────────────────────────
    case 'collecting_private': {
      const isPrivate = /^(y|yes|是|私有)$/i.test(msg);
      state.data.isPrivate = isPrivate;
      state.step = 'confirming';
      saveState(state);

      const membersStr = state.data.members.length > 0
        ? state.data.members.map(m => `@${m}`).join('、')
        : '（未指定）';

      return [
        '**请确认以下信息：**',
        '',
        `- 仓库名称：\`${state.data.repoName}\``,
        `- 项目描述：${state.data.description}`,
        `- 创建者（管理员）：@${state.data.creator}`,
        `- 其他成员（只读）：${membersStr}`,
        `- 可见性：${isPrivate ? '🔒 私有' : '🌐 公开'}`,
        '',
        '输入 `确认` 或 `ok` 开始初始化，输入 `取消` 退出。',
      ].join('\n');
    }

    // ── Step 6: 确认并执行 ─────────────────────────────────
    case 'confirming': {
      if (!/^(确认|ok|yes|是|开始|confirm)$/i.test(msg)) {
        return '请输入 `确认` 开始初始化，或 `取消` 退出。';
      }

      state.step = 'running';
      saveState(state);

      const data = state.data;
      const result = runInit(data);
      clearState();

      if (result.success) {
        let output = {};
        try { output = JSON.parse(result.stdout); } catch {}

        const giteaUrl = process.env.GITEA_URL || 'http://43.156.243.152:3000';
        const org = process.env.GITEA_ORG || 'HKU-AIFusion';
        const repoUrl = output.repoUrl || `${giteaUrl}/${org}/${data.repoName}`;

        const lines = [
          '🎉 **仓库初始化完成！**',
          '',
          `✅ 已创建仓库 \`${data.repoName}\``,
          '✅ 已生成标准目录结构（meeting/ docs/ src/ data/ reports/ profiles/）',
          '✅ 已生成 README.md 和 CONTRIBUTING.md',
          `✅ 已将 @${data.creator} 设为仓库管理员`,
        ];

        if (data.members && data.members.length > 0) {
          lines.push(`✅ 已将 ${data.members.map(m => `@${m}`).join('、')} 以只读权限加入仓库`);
          lines.push('✅ 已生成各成员档案文件（profiles/）');
          lines.push('✅ 已发送邮件通知给成员');
        }

        lines.push('✅ 已创建 2 个初始 Issue');

        if (output.emailErrors && output.emailErrors.length > 0) {
          lines.push(`⚠️  以下成员邮件发送失败，请手动通知：${output.emailErrors.join(', ')}`);
        }

        lines.push('', `📁 仓库地址：${repoUrl}`);
        return lines.join('\n');

      } else {
        return [
          '❌ **初始化过程中出现错误**',
          '',
          result.stderr || result.stdout || '未知错误',
          '',
          '已发送错误详情邮件，请检查后手动补全。',
        ].join('\n');
      }
    }

    default: {
      clearState();
      return null;
    }
  }
}

// ── OpenClaw 入口导出 ──────────────────────────────────────
module.exports = { handle };

// ── 命令行直接调用支持（调试用）──────────────────────────────
if (require.main === module) {
  const readline = require('readline');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  console.log('project-init Skill 调试模式（输入消息，Ctrl+C 退出）\n');
  const ask = () => {
    rl.question('你：', (line) => {
      const resp = handle(line, {});
      if (resp) console.log(`\nSkill：${resp}\n`);
      ask();
    });
  };
  ask();
}
