/**
 * SENSEN Feishu Task Notifier - Phase 4.1
 * 飞书任务卡片集成
 * 
 * 功能：
 * 1. 任务状态变更 → 推送飞书卡片
 * 2. 支持卡片按钮交互（审核通过/拒绝）
 * 3. 定时任务到期提醒
 */

const https = require('https');
const http = require('http');

// 飞书配置
const FEISHU_CONFIG = {
  // 飞书群ID（老板的飞书群）
  GROUP_ID: 'oc_589bdc6838e4b0a66ae088918ae29aab',
  // 机器人名称
  BOT_NAME: '森森',
  // API地址
  API_HOST: 'open.feishu.cn',
  API_PATH_PREFIX: '/open-apis'
};

// 状态到Emoji的映射
const STATUS_EMOJI = {
  inbox: '📥',
  planning: '📐',
  executing: '⚡',
  review: '👀',
  done: '✅',
  failed: '❌'
};

// 优先级颜色
const PRIORITY_COLOR = {
  P0: 'red',
  P1: 'orange', 
  P2: 'yellow',
  P3: 'grey'
};

/**
 * 发送飞书消息
 */
async function sendFeishuMessage(content, chatId = FEISHU_CONFIG.GROUP_ID) {
  const payload = {
    receive_id: chatId,
    msg_type: 'text',
    content: JSON.stringify({ text: content })
  };

  return await feishuRequest('/im/v1/messages', 'POST', payload);
}

/**
 * 发送飞书卡片消息
 */
async function sendFeishuCard(cardContent, chatId = FEISHU_CONFIG.GROUP_ID) {
  const payload = {
    receive_id: chatId,
    msg_type: 'interactive',
    content: JSON.stringify(cardContent)
  };

  return await feishuRequest('/im/v1/messages', 'POST', payload);
}

/**
 * 飞书 API 请求
 */
function feishuRequest(path, method = 'GET', payload = null) {
  return new Promise((resolve, reject) => {
    // 从环境变量获取token（需要在openclaw配置）
    const appToken = process.env.FEISHU_APP_TOKEN || '';
    const appSecret = process.env.FEISHU_APP_SECRET || '';

    // 如果没有配置，返回模拟成功
    if (!appToken || !appSecret) {
      console.log(`[FeishuNotifier] ⚠️ 飞书未配置，使用模拟模式`);
      console.log(`[FeishuNotifier]   请求: ${method} ${path}`);
      if (payload) console.log(`[FeishuNotifier]   数据:`, JSON.stringify(payload).slice(0, 200));
      resolve({ success: true, mock: true });
      return;
    }

    // 先获取tenant_access_token
    const tokenPath = '/auth/v3/tenant_access_token/internal';
    const tokenPayload = JSON.stringify({
      app_id: appToken,
      app_secret: appSecret
    });

    const tokenReq = http.request({
      hostname: FEISHU_CONFIG.API_HOST,
      path: tokenPath,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(tokenPayload)
      }
    }, (tokenRes) => {
      let data = '';
      tokenRes.on('data', chunk => data += chunk);
      tokenRes.on('end', () => {
        try {
          const tokenResult = JSON.parse(data);
          const accessToken = tokenResult.tenant_access_token;

          // 发送实际请求
          const body = payload ? JSON.stringify(payload) : '';
          const reqOptions = {
            hostname: FEISHU_CONFIG.API_HOST,
            path: FEISHU_CONFIG.API_PATH_PREFIX + path,
            method: method,
            headers: {
              'Content-Type': 'application/json',
              'Content-Length': Buffer.byteLength(body),
              'Authorization': `Bearer ${accessToken}`
            }
          };

          const req = http.request(reqOptions, (res) => {
            let resData = '';
            res.on('data', chunk => resData += chunk);
            res.on('end', () => {
              try {
                resolve(JSON.parse(resData));
              } catch (e) {
                resolve({ success: true, raw: resData });
              }
            });
          });

          req.on('error', reject);
          if (body) req.write(body);
          req.end();
        } catch (e) {
          reject(e);
        }
      });
    });

    tokenReq.on('error', reject);
    tokenReq.write(tokenPayload);
    tokenReq.end();
  });
}

/**
 * 构建任务状态卡片
 */
function buildTaskCard(task, action = 'update') {
  const emoji = STATUS_EMOJI[task.status] || '📋';
  const color = PRIORITY_COLOR[task.priority] || 'grey';
  const statusText = {
    inbox: '待处理',
    planning: '规划中',
    executing: '执行中',
    review: '待审核',
    done: '已完成',
    failed: '失败'
  }[task.status] || task.status;

  // 根据操作类型构建不同标题
  let title = '';
  let description = '';

  if (action === 'created') {
    title = `📝 新任务创建`;
    description = `**${task.title}**`;
  } else if (action === 'status_change') {
    title = `${emoji} 任务状态更新`;
    description = `**${task.title}**\n状态: ${statusText}`;
  } else if (action === 'timeout') {
    title = `⏰ 任务超时提醒`;
    description = `**${task.title}**\n⚠️ 已在 ${statusText} 状态超过限制时间`;
  } else if (action === 'reminder') {
    title = `🔔 任务到期提醒`;
    description = `**${task.title}**`;
  } else {
    title = `${emoji} 任务更新`;
    description = `**${task.title}**`;
  }

  const card = {
    schema: "2.0",
    config: {
      "wide_screen_mode": true
    },
    elements: [
      {
        tag: "markdown",
        content: title
      },
      {
        tag: "hr"
      },
      {
        tag: "markdown",
        content: description
      },
      {
        tag: "column_set",
        flex_mode: "富",
        horizontal_spacing: "富",
        elements: [
          {
            tag: "column",
            width: "auto",
            elements: [
              {
                tag: "markdown",
                content: `**优先级**\n\`${task.priority}\``
              }
            ]
          },
          {
            tag: "column",
            width: "auto",
            elements: [
              {
                tag: "markdown",
                content: `**状态**\n\`${statusText}\``
              }
            ]
          },
          {
            tag: "column",
            width: "auto",
            elements: [
              {
                tag: "markdown",
                content: `**负责人**\n@${task.assignedTo || '未分配'}`
              }
            ]
          }
        ]
      }
    ]
  };

  // 添加详情（如果有）
  if (task.description) {
    card.elements.splice(3, 0, {
      tag: "markdown",
      content: `📌 ${task.description.slice(0, 100)}${task.description.length > 100 ? '...' : ''}`
    });
  }

  // 添加按钮（用于review状态）
  if (task.status === 'review') {
    card.elements.push({
      tag: "hr"
    });
    card.elements.push({
      tag: "action",
      actions: [
        {
          tag: "button",
          text: {
            tag: "plain_text",
            content: "✅ 审核通过"
          },
          type: "primary",
          value: {
            action: "approve",
            taskId: task.id
          }
        },
        {
          tag: "button",
          text: {
            tag: "plain_text",
            content: "❌ 需要修改"
          },
          type: "danger",
          value: {
            action: "reject", 
            taskId: task.id
          }
        },
        {
          tag: "button",
          text: {
            tag: "plain_text",
            content: "👀 查看详情"
          },
          type: "default",
          value: {
            action: "detail",
            taskId: task.id
          }
        }
      ]
    });
  }

  // 添加结果（如果已完成）
  if (task.result) {
    card.elements.push({
      tag: "hr"
    });
    card.elements.push({
      tag: "markdown",
      content: `**结果**\n${task.result}`
    });
  }

  // 添加时间信息
  const createdAt = new Date(task.createdAt).toLocaleString('zh-CN', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
  card.elements.push({
    tag: "note",
    elements: [
      {
        tag: "plain_text",
        content: `创建时间: ${createdAt} | 任务ID: ${task.id.slice(-8)}`
      }
    ]
  });

  return card;
}

/**
 * 发送任务创建通知
 */
async function notifyTaskCreated(task) {
  console.log(`[FeishuNotifier] 📝 发送任务创建通知: ${task.title}`);
  const card = buildTaskCard(task, 'created');
  return await sendFeishuCard(card);
}

/**
 * 发送任务状态变更通知
 */
async function notifyTaskStatusChange(task, oldStatus, newStatus) {
  console.log(`[FeishuNotifier] ${STATUS_EMOJI[newStatus]} 发送状态变更通知: ${task.title} (${oldStatus} → ${newStatus})`);
  const card = buildTaskCard(task, 'status_change');
  return await sendFeishuCard(card);
}

/**
 * 发送任务超时提醒
 */
async function notifyTaskTimeout(task) {
  console.log(`[FeishuNotifier] ⏰ 发送超时提醒: ${task.title}`);
  const card = buildTaskCard(task, 'timeout');
  return await sendFeishuCard(card);
}

/**
 * 发送任务到期提醒
 */
async function notifyTaskReminder(task, minutesUntilDue) {
  console.log(`[FeishuNotifier] 🔔 发送到期提醒: ${task.title} (还有${minutesUntilDue}分钟)`);
  const card = buildTaskCard(task, 'reminder');
  return await sendFeishuCard(card);
}

/**
 * 发送任务完成通知
 */
async function notifyTaskDone(task) {
  console.log(`[FeishuNotifier] ✅ 发送完成通知: ${task.title}`);
  const card = buildTaskCard(task, 'done');
  return await sendFeishuCard(card);
}

/**
 * 发送每日任务汇总
 */
async function sendDailySummary(tasks) {
  console.log(`[FeishuNotifier] 📊 发送每日任务汇总`);

  const pendingTasks = tasks.filter(t => !['done', 'failed'].includes(t.status));
  const doneTasks = tasks.filter(t => t.status === 'done');

  const card = {
    schema: "2.0",
    config: {
      wide_screen_mode: true
    },
    elements: [
      {
        tag: "markdown",
        content: `📊 **森森任务日报** | ${new Date().toLocaleDateString('zh-CN')}`
      },
      {
        tag: "hr"
      },
      {
        tag: "markdown",
        content: `📥 **待处理**: ${pendingTasks.length} 个任务`
      },
      ...pendingTasks.slice(0, 5).map(t => ({
        tag: "markdown",
        content: `${STATUS_EMOJI[t.status]} [${t.priority}] ${t.title} → @${t.assignedTo || '未分配'}`
      })),
      {
        tag: "hr"
      },
      {
        tag: "markdown",
        content: `✅ **已完成**: ${doneTasks.length} 个任务`
      },
      ...doneTasks.slice(0, 3).map(t => ({
        tag: "markdown",
        content: `${STATUS_EMOJI[t.status]} ${t.title}`
      })),
      {
        tag: "note",
        elements: [
          {
            tag: "plain_text",
            content: `由 ${FEISHU_CONFIG.BOT_NAME} 自动发送`
          }
        ]
      }
    ]
  };

  return await sendFeishuCard(card);
}

/**
 * 发送超时任务汇总
 */
async function sendTimeoutSummary(timeoutTasks) {
  if (timeoutTasks.length === 0) return;

  console.log(`[FeishuNotifier] ⏰ 发送超时任务汇总: ${timeoutTasks.length}个`);

  const card = {
    schema: "2.0",
    elements: [
      {
        tag: "markdown",
        content: `⏰ **超时任务提醒** | ${timeoutTasks.length} 个任务超时`
      },
      {
        tag: "hr"
      },
      ...timeoutTasks.slice(0, 10).map(t => ({
        tag: "markdown",
        content: `⚠️ **[${t.level}]** ${t.title}\n   状态: ${t.status} | 超时: ${t.elapsedMinutes}分钟`
      })),
      {
        tag: "note",
        elements: [
          {
            tag: "plain_text",
            content: `请及时处理这些任务`
          }
        ]
      }
    ]
  };

  return await sendFeishuCard(card);
}

/**
 * 集成到 TaskManager
 * 返回包装了飞书通知的TaskManager
 */
function wrapTaskManagerWithFeishu(TaskManager) {
  const originalCreate = TaskManager.createTask.bind(TaskManager);
  const originalUpdateState = TaskManager.updateTaskState.bind(TaskManager);

  // 包装创建任务
  TaskManager.createTask = function(...args) {
    const task = originalCreate(...args);
    // 异步发送通知，不阻塞
    notifyTaskCreated(task).catch(e => console.error('[FeishuNotifier] 创建通知失败:', e.message));
    return task;
  };

  // 包装状态更新
  TaskManager.updateTaskState = function(...args) {
    const [taskId, newState, extra] = args;
    const task = this.loadTask(taskId);
    const oldState = task?.status;
    
    const result = originalUpdateState(...args);
    
    if (result && oldState !== newState) {
      // 异步发送通知
      notifyTaskStatusChange(result, oldState, newState)
        .catch(e => console.error('[FeishuNotifier] 状态变更通知失败:', e.message));
    }
    
    return result;
  };

  // 添加飞书通知方法
  TaskManager.notifyTimeout = async function(timeoutTasks) {
    return await sendTimeoutSummary(timeoutTasks);
  };

  TaskManager.sendDailySummary = async function() {
    const tasks = this.getAllTasks();
    return await sendDailySummary(tasks);
  };

  return TaskManager;
}

// 导出模块
module.exports = {
  sendFeishuMessage,
  sendFeishuCard,
  buildTaskCard,
  notifyTaskCreated,
  notifyTaskStatusChange,
  notifyTaskTimeout,
  notifyTaskReminder,
  notifyTaskDone,
  sendDailySummary,
  sendTimeoutSummary,
  wrapTaskManagerWithFeishu,
  FEISHU_CONFIG,
  STATUS_EMOJI
};
