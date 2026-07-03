/**
 * kids-points-v2 skill - OpenClaw Agent 集成入口
 *
 * V2 入口 (2026-06-20 老王拍板升级):
 * - OpenClaw 平台自动 dispatch 飞书消息给本 handler
 * - 群聊 + 单聊 全量响应 (chatType == group / topic_group / p2p / private 都接)
 * - V1 已封存为 kids-points.disabled-20260620, skills.entries.kids-points.enabled = false
 * - subprocess 调 V2 cli.py (V2 runtime), V2 cli.py 写 V2 SQLite
 * - V2 reply 字符串返给 OpenClaw, OpenClaw 发回飞书
 *
 * 硬约束: V2 不动 V1 历史数据 (V1 已 disable, 双保险)
 */

const { spawn } = require('child_process');
const path = require('path');

// V2 runtime 路径解析（优先级）:
//   1. 环境变量 KIDS_POINTS_RUNTIME_DIR  （推荐：本地生产可指向原路径）
//   2. 默认 fallback: skill 包内的 runtime/ 目录（ClawHub 安装后的标准位置）
//
// 这样：
//   - 本地 ~/.openclaw/openclaw.json 设 KIDS_POINTS_RUNTIME_DIR 指向原生产路径，零干扰
//   - 其他用户 ClawHub install 后不设 env，自动用 skill 内嵌 runtime，开箱即用
const V2_RUNTIME_DIR = process.env.KIDS_POINTS_RUNTIME_DIR
  || path.join(__dirname, 'runtime');
const V2_CLI = path.join(V2_RUNTIME_DIR, 'cli.py');


/**
 * 处理飞书消息 (OpenClaw 平台自动 dispatch).
 * @param {Object} context - OpenClaw 飞书消息 context
 *   - message (str): 飞书消息文本
 *   - messageId (str): 飞书消息 ID
 *   - chatType (str): 'p2p' | 'group' | 'topic_group' | 'private'
 *   - senderId, senderOpenId, chatId, ... (其他 OpenClaw 字段)
 * @returns {Promise<string|null>} V2 reply 文本, 或 null 让其他 skill 处理
 */
async function handleFeishuMessage(context) {
  // ── Gate 1: 文本消息必须有内容 ─────────────────────────────────
  // 2026-06-20 老王拍板: V2 全量接管 (群聊 + 单聊), 不再按 chat_type 分流
  const message = (context?.message || '').trim();
  if (!message) {
    return null; // 纯图片/语音 → 当前 V2 不处理
  }

  const messageId = context?.messageId || '';

  // ── 调 V2 cli.py 单条消息模式 ───────────────────────────────────
  return new Promise((resolve) => {
    const args = [V2_CLI, message];
    let py;
    try {
      py = spawn('python3', args, {
        cwd: V2_RUNTIME_DIR,
        env: { ...process.env },  // 继承 LLM API key 等环境变量
        timeout: 30000,
      });
    } catch (e) {
      return resolve(`⚠️ V2 spawn 失败: ${e.message}`);
    }

    let stdout = '';
    let stderr = '';
    let killed = false;

    // 30s 超时 (跟 handle_feishu.py 一致)
    const timer = setTimeout(() => {
      killed = true;
      py.kill('SIGKILL');
      resolve('⚠️ V2 处理超时 (30s), 请重试');
    }, 30000);

    py.stdout.on('data', (d) => { stdout += d.toString(); });
    py.stderr.on('data', (d) => { stderr += d.toString(); });
    py.on('error', (err) => {
      clearTimeout(timer);
      resolve(`⚠️ V2 spawn 错误: ${err.message}`);
    });
    py.on('close', (code) => {
      clearTimeout(timer);
      if (killed) return; // 已被超时分支处理

      if (code !== 0) {
        const errMsg = (stderr || stdout || '').trim() || '未知错误';
        console.error(`[kids-points-v2] V2 cli.py exit ${code}: ${errMsg.slice(0, 300)}`);
        return resolve(`⚠️ V2 错误 (rc=${code}): ${errMsg.slice(0, 300)}`);
      }

      const reply = stdout.trim();
      if (messageId) {
        console.log(`[kids-points-v2] ${messageId} → ${reply.slice(0, 80)}`);
      }
      resolve(reply || '✅ V2 已处理 (无返回内容)');
    });
  });
}


module.exports = {
  handleFeishuMessage,
};
