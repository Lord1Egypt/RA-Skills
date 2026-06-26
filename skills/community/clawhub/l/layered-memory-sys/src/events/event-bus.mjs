// event-bus.mjs - 事件总线 (v2.0)
// 支持其他技能/插件订阅记忆变更

const _listeners = new Map();

// 订阅事件
export function on(event, callback) {
  if (!_listeners.has(event)) _listeners.set(event, new Set());
  _listeners.get(event).add(callback);

  // 返回取消订阅函数
  return () => off(event, callback);
}

// 取消订阅
export function off(event, callback) {
  const listeners = _listeners.get(event);
  if (listeners) listeners.delete(callback);
}

// 触发事件
export function emit(event, data) {
  const listeners = _listeners.get(event);
  if (!listeners) return;

  for (const cb of listeners) {
    try {
      cb(data);
    } catch (e) {
      console.error(`事件处理错误 [${event}]:`, e.message);
    }
  }
}

// 一次性订阅
export function once(event, callback) {
  const wrapper = (data) => {
    callback(data);
    off(event, wrapper);
  };
  return on(event, wrapper);
}

// 获取所有事件监听器（调试用）
export function getListeners() {
  const result = {};
  for (const [event, set] of _listeners) {
    result[event] = set.size;
  }
  return result;
}

// 清空所有监听器
export function clearAll() {
  _listeners.clear();
}

// 预定义事件类型
export const EVENTS = {
  MEMORY_CREATED: 'memory:created',
  MEMORY_UPDATED: 'memory:updated',
  MEMORY_DELETED: 'memory:deleted',
  MEMORY_MERGED: 'memory:merged',
  MEMORY_ARCHIVED: 'memory:archived',
  MEMORY_RECALLED: 'memory:recalled',
  MEMORY_CONSOLIDATED: 'memory:consolidated',
  DREAM_COMPLETED: 'dream:completed',
  REMINDER_TRIGGERED: 'reminder:triggered',
};