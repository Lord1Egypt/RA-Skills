/**
 * lark-mention - 飞书 @ 提及消息发送模块
 *
 * 使用方式:
 *   import { sendMention } from './lark-mention.mjs';
 *   await sendMention({ chatId: 'oc_xxx', text: '大家好', members: [{ open_id: 'ou_xxx', name: '张三' }] });
 */

const LARK_BRIDGE_URL = 'http://localhost:18780/proactive';

/**
 * @param {Object} options
 * @param {string} options.chatId - 目标群ID
 * @param {string} options.text - 消息文本（在 at 标签之后的部分）
 * @param {Array<{open_id: string, name: string}>} options.members - 要 @ 的成员列表
 * @returns {Promise<Object>} API 响应结果
 */
export async function sendMention({ chatId, text, members }) {
  // 构建 <at user_id="...">display_name</at> 标签
  const atTags = members.map(m =>
    `<at user_id="${m.open_id}">${m.name}</at>`
  ).join(' ');

  // 完整消息文本 = @标签 + 空格 + 内容
  const fullText = atTags + (text ? ' ' + text : '');

  // 构建 mentions 数组（key 必须和 user_id 完全一致）
  const mentions = members.map(m => ({
    key: m.open_id,
    id: { open_id: m.open_id, id_type: 'open_id' },
    name: m.name
  }));

  // 构造 Lark 消息 content
  const content = JSON.stringify({ text: fullText, mentions });

  // 构造 API 请求体
  const payload = {
    chatId,
    msgType: 'text',
    text: content
  };

  // 发送请求
  const response = await fetch(LARK_BRIDGE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const result = await response.json();
  return result;
}

/**
 * 快捷方法：艾特所有成员
 * @param {string} chatId
 * @param {string} text
 * @param {Array<{open_id: string, name: string}>} allMembers
 */
export async function sendMentionAll(chatId, text, allMembers) {
  return sendMention({ chatId, text, members: allMembers });
}

/**
 * 快捷方法：艾特单个成员
 * @param {string} chatId
 * @param {string} text
 * @param {string} openId
 * @param {string} name
 */
export async function sendMentionOne(chatId, text, openId, name) {
  return sendMention({ chatId, text, members: [{ open_id: openId, name }] });
}
