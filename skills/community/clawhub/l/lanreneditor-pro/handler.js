/**
 * OpenClaw Skill: 微信公众号排版与发布
 * 
 * 处理函数实现
 */

const crypto = require('crypto');
const axios = require('axios');

const WORKFLOW_SESSION_TTL_MS = 30 * 60 * 1000;
const MAX_WORKFLOW_SESSIONS = 200;
const workflowSessions = new Map();

// ═════════════════════════════════════════════════════════════════════════════
// 工具函数
// ═════════════════════════════════════════════════════════════════════════════

/**
 * 创建 API 客户端
 */
function createApiClient(config) {
  return axios.create({
    baseURL: config.apiBaseUrl,
    headers: {
      'X-API-Key': config.apiKey,
      'Content-Type': 'application/json'
    },
    timeout: 30000
  });
}

function buildErrorPayload(error, fallbackMessage) {
  const responseData = error.response && error.response.data;
  return {
    status: (error.response && error.response.status) || 500,
    success: false,
    error:
      (responseData && (responseData.message || responseData.error)) ||
      error.message ||
      fallbackMessage,
    code: responseData && responseData.code,
    data: responseData && responseData.data,
    retryAfter: responseData && responseData.retryAfter,
    upgradeUrl: responseData && responseData.upgradeUrl,
    manageUrl: responseData && responseData.manageUrl
  };
}

function sendApiError(res, error, fallbackMessage) {
  const payload = buildErrorPayload(error, fallbackMessage);
  return res.status(payload.status).json(payload);
}

function inferTitleFromContent(content) {
  if (!content || typeof content !== 'string') {
    return '';
  }

  const headingMatch = content.match(/^#\s+(.+)$/m);
  if (headingMatch) {
    return headingMatch[1].trim();
  }

  const firstLine = content
    .split('\n')
    .map(line => line.trim())
    .find(line => line && !/^[-*>`]/.test(line));

  return firstLine ? firstLine.slice(0, 60) : '';
}

function now() {
  return Date.now();
}

function cleanupExpiredWorkflowSessions() {
  const currentTime = now();
  for (const [sessionId, session] of workflowSessions.entries()) {
    if (!session || currentTime - session.updatedAt > WORKFLOW_SESSION_TTL_MS) {
      workflowSessions.delete(sessionId);
    }
  }
}

function getWorkflowSession(sessionId) {
  if (!sessionId) {
    return null;
  }

  cleanupExpiredWorkflowSessions();
  const session = workflowSessions.get(sessionId);
  if (!session) {
    return null;
  }

  session.updatedAt = now();
  return session;
}

function saveWorkflowSession(sessionId, state) {
  cleanupExpiredWorkflowSessions();

  const nextSessionId = sessionId || `wf_${crypto.randomBytes(8).toString('hex')}`;
  const existingSession = workflowSessions.get(nextSessionId);
  const currentTime = now();
  const session = {
    id: nextSessionId,
    createdAt: existingSession ? existingSession.createdAt : currentTime,
    updatedAt: currentTime,
    state: {
      ...(existingSession ? existingSession.state : {}),
      ...state
    }
  };

  workflowSessions.set(nextSessionId, session);

  // 超过上限时淘汰最老的会话
  if (workflowSessions.size > MAX_WORKFLOW_SESSIONS) {
    const oldest = workflowSessions.keys().next().value;
    workflowSessions.delete(oldest);
  }

  return session;
}

function clearWorkflowSession(sessionId) {
  if (sessionId) {
    workflowSessions.delete(sessionId);
  }
}

function buildWorkflowPayload(session, overrides = {}) {
  return {
    workflowSessionId: session.id,
    workflowStage: session.state.workflowStage,
    ...overrides
  };
}

function findTemplate(templates, templateValue) {
  if (!templateValue) {
    return null;
  }

  const normalizedValue = String(templateValue).trim().toLowerCase();
  return templates.find(template => {
    return (
      template.id === templateValue ||
      template.id.toLowerCase() === normalizedValue ||
      template.name.toLowerCase() === normalizedValue ||
      template.name.toLowerCase().includes(normalizedValue) ||
      template.category === templateValue ||
      template.category.toLowerCase() === normalizedValue
    );
  }) || null;
}

/**
 * 根据模板的组件声明生成 AI 排版指引
 */
function buildComponentInstructions(template) {
  if (!template || !template.components || !Array.isArray(template.components) || template.components.length === 0) {
    return '';
  }

  const rules = template.components
    .filter(c => c.className && c.trigger)
    .map(c => `- 当内容涉及「${c.trigger}」时，请使用 ::: ${c.className} 语法包裹对应内容`)
    .join('\n');

  if (!rules) return '';

  return `\n\n【排版规范】\n该用户选择的模板定义了以下自定义排版组件，请优先输出能够命中 CSS 的 HTML 结构，避免只写普通 Markdown 导致样式无法匹配：\n${rules}\n\n强制要求：\n1. 当某一段内容需要使用模板的自定义样式时，优先使用 HTML 结构并带上对应 class，例如 <section class="intro-box">...</section> 或 <div class="tip-card">...</div>。\n2. 如果你更适合用 ::: 容器语法，也可以使用 ::: className 包裹内容，系统会自动转换为对应 HTML。\n3. 不要把需要套用自定义样式的内容只写成普通 blockquote、普通列表或普通段落，否则 CSS 可能不会命中。\n4. 文章可以混合使用标准 Markdown 和少量 HTML；凡是依赖模板 className 的内容，一律优先用 HTML 结构明确表达。\n\nHTML 示例：\n\`\`\`html\n<section class="intro-box">\n  <p>这里是导读内容</p>\n</section>\n\n<div class="tip-card">\n  <p>这里是提示信息</p>\n</div>\n\`\`\`\n\n容器语法示例：\n\`\`\`\n::: intro-box\n这里是导读内容\n:::\n\`\`\`\n系统会自动将 ::: className 转换为对应的 HTML 结构并应用模板样式。除了这些自定义容器，其余内容请使用标准 Markdown 语法。`;
}

function buildHtmlStructureInstructions(template) {
  const templateName = template && template.name ? template.name : '当前模板';
  const componentCount = template && Array.isArray(template.components) ? template.components.length : 0;

  let instructions = `【生成约束】请优先生成能够让 CSS 真正命中的内容结构，而不是只输出基础 Markdown。当前目标模板是「${templateName}」。`;
  instructions += '\n- 凡是依赖模板自定义样式的内容，优先输出带 class 的 HTML 结构，例如 <section class="xxx">...</section>、<div class="xxx">...</div>。';
  instructions += '\n- 如果上游支持 ::: className 容器语法，也可以使用 ::: 容器，但不要把这类内容退化成普通引用块、普通列表或普通段落。';
  instructions += '\n- 普通正文、普通标题、普通列表可以继续使用 Markdown；只有组件化内容必须显式包裹 HTML/class 或 ::: 容器。';
  instructions += '\n- 核心原则：模板组件优先输出 HTML，确保最终渲染后的 DOM 结构能命中模板 CSS。';

  if (componentCount > 0) {
    instructions += `\n- 该模板当前检测到 ${componentCount} 个组件声明，生成内容时应优先为这些组件产出显式 HTML 结构。`;
  }

  return instructions;
}

function findAccount(accounts, accountValue) {
  if (!accountValue) {
    return null;
  }

  const normalizedValue = String(accountValue).trim().toLowerCase();
  return accounts.find(account => {
    const appId = String(account.appId || '').trim().toLowerCase();
    const appName = String(account.appName || account.name || '').trim().toLowerCase();
    const originalId = String(account.originalId || '').trim().toLowerCase();

    return (
      appId === normalizedValue ||
      appName === normalizedValue ||
      originalId === normalizedValue ||
      appName.includes(normalizedValue) ||
      originalId.includes(normalizedValue)
    );
  }) || null;
}

/**
 * 格式化模板卡片
 */
function formatTemplateCard(template) {
  // 生成标签
  let tags = [];
  if (template.isUserTemplate) {
    tags.push('🎨 我的模板');
  } else if (template.isPremium) {
    tags.push('⭐ 高级');
  } else {
    tags.push('📋 免费');
  }
  
  return {
    type: 'card',
    title: `${template.emoji} ${template.name}`,
    description: template.description,
    footer: tags.join(' · '),
    data: {
      templateId: template.id,
      category: template.category,
      isUserTemplate: template.isUserTemplate || false
    }
  };
}

/**
 * 格式化公众号卡片
 */
function formatAccountCard(account) {
  const originalId = account.originalId || account.authorizerAppId || '';
  return {
    type: 'card',
    title: account.appName,
    description: originalId ? `AppID: ${account.appId} · 原始ID: ${originalId}` : `AppID: ${account.appId}`,
    image: account.appLogo,
    data: {
      appId: account.appId,
      originalId
    }
  };
}

function invokeHandler(handler, req, config) {
  return new Promise(resolve => {
    let settled = false;
    const finish = (payload) => {
      if (!settled) {
        settled = true;
        resolve(payload);
      }
    };

    const res = {
      json(payload) {
        finish(payload);
        return payload;
      },
      status(statusCode) {
        return {
          json(payload) {
            finish({
              ...payload,
              status: statusCode,
              success: payload && typeof payload.success === 'boolean' ? payload.success : false
            });
            return payload;
          }
        };
      }
    };

    Promise.resolve(handler(req, res, config))
      .then(result => {
        if (result !== undefined) {
          finish(result);
        }
      })
      .catch(error => {
        finish({
          success: false,
          error: error.message || '请求失败'
        });
      });
  });
}

// ═════════════════════════════════════════════════════════════════════════════
// 端点处理函数
// ═════════════════════════════════════════════════════════════════════════════

/**
 * GET /templates - 获取模板列表
 */
async function getTemplates(req, res, config) {
  try {
    const api = createApiClient(config);
    const { category, search } = req.query;
    
    const response = await api.get('/api/skill/templates', {
      params: { category, search, limit: 50 }
    });
    
    if (!response.data.success) {
      return res.status(400).json({
        success: false,
        error: response.data.error || '获取模板失败'
      });
    }
    
    // 格式化为 OpenClaw 卡片格式
    const cards = response.data.data.list.map(formatTemplateCard);
    
    return res.json({
      success: true,
      data: {
        templates: response.data.data.list,
        cards: cards,
        pagination: response.data.data.pagination
      }
    });
    
  } catch (error) {
    console.error('[Skill] 获取模板失败:', error.message);
    return sendApiError(res, error, '获取模板列表失败');
  }
}

/**
 * GET /accounts - 获取公众号列表
 */
async function getAccounts(req, res, config) {
  try {
    const api = createApiClient(config);
    
    const response = await api.get('/api/skill/accounts');
    
    if (!response.data.success) {
      return res.status(400).json({
        success: false,
        error: response.data.error || '获取公众号失败'
      });
    }
    
    // 格式化为卡片
    const cards = response.data.data.map(formatAccountCard);
    
    return res.json({
      success: true,
      data: {
        accounts: response.data.data,
        cards: cards
      }
    });
    
  } catch (error) {
    console.error('[Skill] 获取公众号失败:', error.message);
    return sendApiError(res, error, '获取公众号列表失败');
  }
}

/**
 * POST /publish - 发布文章
 */
async function publishArticle(req, res, config) {
  try {
    const api = createApiClient(config);
    const {
      content,
      title,
      author,
      templateId,
      accountId,
      digest,
      coverImage,
      contentSourceUrl,
      autoGenerateCover  // 新增：是否自动生成封面图
    } = req.body;
    
    // 参数验证
    if (!content) {
      return res.status(400).json({
        success: false,
        error: '缺少文章内容'
      });
    }
    
    if (!templateId) {
      return res.status(400).json({
        success: false,
        error: '缺少模板 ID'
      });
    }
    
    const response = await api.post('/api/skill/publish', {
      content,
      title,
      author,
      templateId,
      accountId,
      digest,
      coverImage,
      contentSourceUrl,
      autoGenerateCover: autoGenerateCover !== false  // 默认为 true
    });
    
    if (!response.data.success) {
      return res.status(400).json({
        success: false,
        error: response.data.error || '创建发布任务失败'
      });
    }
    
    return res.json({
      success: true,
      data: {
        taskId: response.data.data.taskId,
        status: response.data.data.status,
        message: '发布任务已创建，正在处理中...'
      }
    });
    
  } catch (error) {
    console.error('[Skill] 发布文章失败:', error.message);
    return sendApiError(res, error, '发布文章失败');
  }
}

/**
 * GET /status - 查询发布状态
 */
async function getPublishStatus(req, res, config) {
  try {
    const api = createApiClient(config);
    const { taskId } = req.query;
    
    if (!taskId) {
      return res.status(400).json({
        success: false,
        error: '缺少任务 ID'
      });
    }
    
    const response = await api.get('/api/skill/publish/status', {
      params: { taskId }
    });
    
    if (!response.data.success) {
      return res.status(400).json({
        success: false,
        error: response.data.error || '查询状态失败'
      });
    }
    
    const task = response.data.data;
    
    // 格式化状态信息
    let statusMessage = '';
    if (task.status === 'pending') {
      statusMessage = '⏳ 等待处理...';
    } else if (task.status === 'processing') {
      statusMessage = `${task.step} (${task.progress}%)`;
    } else if (task.status === 'completed') {
      statusMessage = '✅ 发布成功！';
    } else if (task.status === 'failed') {
      statusMessage = '❌ 发布失败: ' + task.error;
    }
    
    return res.json({
      success: true,
      data: {
        ...task,
        statusMessage
      }
    });
    
  } catch (error) {
    console.error('[Skill] 查询状态失败:', error.message);
    return sendApiError(res, error, '查询发布状态失败');
  }
}

/**
 * GET /quota - 查询用户调用额度及公众号额度
 */
async function getQuota(req, res, config) {
  try {
    const api = createApiClient(config);
    const response = await api.get('/api/skill/quota');
    if (!response.data.success) {
      return res.status(400).json({ success: false, error: response.data.error || '查询额度失败' });
    }
    const d = response.data.data;
    return res.json({
      success: true,
      data: {
        planName: d.planName,
        publishRemaining: d.publish.remaining,
        publishTotal: d.publish.total,
        accountsRemaining: d.accounts.remaining,
        accountsTotal: d.accounts.total,
        statusMessage: `⭐️ 当前套餐：${d.planName}\n\n📝 本月发布额度：${d.publish.remaining === -1 ? '不限量' : '剩余 ' + d.publish.remaining + ' 次 (共 ' + d.publish.total + ' 次)'}\n📱 公众号授权：${d.accounts.total === -1 ? '可绑不限量' : '已绑 ' + d.accounts.used + ' 个 (限制 ' + d.accounts.total + ' 个)'}`
      }
    });
  } catch (error) {
    console.error('[Skill] 获取额度失败:', error.message);
    return sendApiError(res, error, '查询额度失败');
  }
}

/**
 * POST /preview - 预览文章内嵌HTML
 */
async function previewArticle(req, res, config) {
  try {
    const api = createApiClient(config);
    const { content, templateId } = req.body;
    if (!content || !templateId) {
      return res.status(400).json({ success: false, error: '缺少内容或模板ID' });
    }
    const response = await api.post('/api/skill/preview', { content, templateId });
    if (!response.data.success) {
      return res.status(400).json({ success: false, error: response.data.error || '生成预览失败' });
    }
    
    const htmlUrl = `data:text/html;charset=utf-8,${encodeURIComponent(response.data.data.html)}`;
    
    return res.json({
      success: true,
      data: {
        htmlUrl,
        message: '预览卡片已生成'
      }
    });
  } catch (error) {
    console.error('[Skill] 预览文章失败:', error.message);
    return sendApiError(res, error, '生成预览失败');
  }
}

// ═════════════════════════════════════════════════════════════════════════════
// 工作流处理函数
// ═════════════════════════════════════════════════════════════════════════════

/**
 * 主工作流：生成并发布文章
 */
async function generateAndPublishWorkflow(context, config) {
  const { message, args = {}, history } = context;
  const workflowSessionId = args.workflowSessionId || args.sessionId;
  const workflowSession = getWorkflowSession(workflowSessionId);
  const persistedState = workflowSession ? workflowSession.state : {};
  
  // Step 1: 提取或生成内容
  let content = args.content || args.markdown || args.articleContent || persistedState.content;
  let title = args.title || persistedState.title || inferTitleFromContent(content);
  let author = args.author || persistedState.author || '';
  let digest = args.digest || persistedState.digest || '';
  let contentSourceUrl = args.contentSourceUrl || args.sourceUrl || persistedState.contentSourceUrl || '';
  let coverImage = args.coverImage || persistedState.coverImage || '';
  let templateValue = args.templateId || args.template || persistedState.templateId || persistedState.template;
  let requestedAccountValue = args.accountId || args.appId || args.accountName || args.account || persistedState.accountId || persistedState.accountName || persistedState.account;

  if (!content && workflowSessionId) {
    return {
      type: 'error',
      content: '当前发布会话已失效，请重新发送文章内容并开始发布流程。'
    };
  }
  
  if (!content) {
    // 需要从对话历史中提取内容
    // 或者调用 LLM 生成
    return {
      type: 'text',
      content: '请提供文章内容，或告诉我你想写什么主题的文章？'
    };
  }
  
  // Step 2: 获取模板列表
  const api = createApiClient(config);
  let templatesRes;
  try {
    templatesRes = await api.get('/api/skill/templates', { params: { limit: 20 } });
  } catch (err) {
    return {
      type: 'error',
      content: '无法连接到排版平台，请检查配置。'
    };
  }
  
  if (!templatesRes.data.success) {
    return {
      type: 'error',
      content: '获取模板失败: ' + templatesRes.data.error
    };
  }
  
  const templates = templatesRes.data.data.list;
  
  // Step 3: 如果用户指定了模板，直接使用
  let selectedTemplate = findTemplate(templates, templateValue);
  
  // Step 4: 如果没有指定或没找到，展示模板选择
  if (!selectedTemplate) {
    const session = saveWorkflowSession(workflowSessionId, {
      content,
      title,
      author,
      digest,
      contentSourceUrl,
      coverImage,
      workflowStage: 'await_template'
    });

    // 分类展示：用户模板在前
    const sortedTemplates = [...templates].sort((a, b) => {
      if (a.isUserTemplate && !b.isUserTemplate) return -1;
      if (!a.isUserTemplate && b.isUserTemplate) return 1;
      return 0;
    });
    
    return {
      type: 'interactive',
      content: '文章已生成！请选择一个排版模板（包含系统模板和你保存的模板）：',
      options: {
        type: 'cards',
        items: sortedTemplates.map(t => {
          let tags = [];
          if (t.isUserTemplate) {
            tags.push('🎨 我的模板');
          } else if (t.isPremium) {
            tags.push('⭐ 高级');
          } else {
            tags.push('📋 免费');
          }
          return {
            id: t.id,
            title: `${t.emoji} ${t.name}`,
            description: t.description,
            tags: tags,
            data: {
              ...buildWorkflowPayload(session, {
                templateId: t.id,
                template: t.id,
                templateConfirmed: true
              }),
              isUserTemplate: t.isUserTemplate
            }
          };
        }),
        action: 'select_template'
      }
    };
  }

  // 如果模板有组件但内容缺少 ::: 容器语法，在确认消息中提示
  const hasContainers = /^:::\s*[\w-]/m.test(content);
  const templateComponents = selectedTemplate.components || [];
  let componentTip = '';
  if (templateComponents.length > 0 && !hasContainers) {
    componentTip = '\n\n> 💡 该模板包含自定义排版组件，系统会自动为引用块匹配合适的组件样式。如需完全发挥模板效果，建议在写文章时指定模板名称，AI 会自动使用组件排版。';
  }

  if (workflowSessionId) {
    saveWorkflowSession(workflowSessionId, {
      content,
      title,
      author,
      digest,
      contentSourceUrl,
      coverImage,
      templateId: selectedTemplate.id,
      template: selectedTemplate.id,
      workflowStage: 'template_selected'
    });
  }
  
  // Step 5: 获取公众号列表
  let accountsRes;
  try {
    accountsRes = await api.get('/api/skill/accounts');
  } catch (err) {
    return {
      type: 'error',
      content: '获取公众号列表失败，请确保已绑定公众号。'
    };
  }
  
  const accounts = accountsRes.data.data;
  
  if (accounts.length === 0) {
    return {
      type: 'error',
      content: '你还没有绑定任何公众号，请先授权绑定。'
    };
  }
  
  // Step 6: 始终让用户确认公众号选择（即使只有一个）
  let targetAccount = requestedAccountValue
    ? findAccount(accounts, requestedAccountValue)
    : null;

  if (requestedAccountValue && !targetAccount) {
    return {
      type: 'error',
      content: '你选择的公众号不存在或当前 API Key 无权访问。'
    };
  }

  // 如果用户没有指定公众号，必须询问确认
  if (!targetAccount) {
    const session = saveWorkflowSession(workflowSessionId, {
      content,
      title,
      author,
      digest,
      contentSourceUrl,
      coverImage,
      templateId: selectedTemplate.id,
      template: selectedTemplate.id,
      workflowStage: 'await_account'
    });

    // 即使只有一个公众号，也展示让用户确认
    const promptText = accounts.length === 1
      ? `已选择模板：**${selectedTemplate.name}**${componentTip}\n\n你只有一个已授权的公众号，请确认发布到 **${accounts[0].appName}**：`
      : `已选择模板：**${selectedTemplate.name}**${componentTip}\n\n请选择要发布的公众号：`;

    return {
      type: 'interactive',
      content: promptText,
      options: {
        type: 'cards',
        items: accounts.map(a => ({
          id: a.appId,
          title: a.appName,
          description: a.originalId ? `原始ID: ${a.originalId}` : `AppID: ${a.appId}`,
          image: a.appLogo,
          data: { 
            ...buildWorkflowPayload(session, {
              templateId: selectedTemplate.id,
              template: selectedTemplate.id,
              templateConfirmed: true,
              accountId: a.appId,
              accountName: a.appName,
              accountConfirmed: true,
              author: author || a.appName
            })
          }
        })),
        action: 'select_account'
      }
    };
  }

  const resolvedAuthor = author || targetAccount.appName || targetAccount.name || '';

  if (workflowSessionId) {
    saveWorkflowSession(workflowSessionId, {
      content,
      title,
      author: resolvedAuthor,
      digest,
      contentSourceUrl,
      coverImage,
      templateId: selectedTemplate.id,
      template: selectedTemplate.id,
      accountId: targetAccount.appId,
      accountName: targetAccount.appName || targetAccount.name,
      workflowStage: args.action === 'preview' || context.intent === 'preview_article' ? 'preview_ready' : 'ready_publish'
    });
  }
  
  // Step 7: 执行发布 (如果是 preview，直接返回生成的卡片)
  if (args.action === 'preview' || context.intent === 'preview_article') {
    const previewResult = await invokeHandler(previewArticle, { body: { content, templateId: selectedTemplate.id } }, config);
    if (!previewResult.success) {
      return {
        type: 'error',
        content: previewResult.error || '生成预览失败'
      };
    }
    return {
      type: 'success',
      content: `✅ 文章预览生成成功！\n此预览带有内嵌样式，由于展示限制请点击链接查看效果：\n[🔎 点击这里查看文章真实排版预览](${previewResult.data.htmlUrl})\n\n确认无误后可以回复“确认发布”或选择重选模板。`
    };
  }

  const publishResult = await executePublish(api, {
    content,
    title,
    author: resolvedAuthor,
    digest,
    contentSourceUrl,
    coverImage,
    templateId: selectedTemplate.id,
    accountId: targetAccount.appId
  });

  if (publishResult && publishResult.type === 'success') {
    clearWorkflowSession(workflowSessionId);
  }
  return publishResult;
}

/**
 * 执行发布
 */
async function executePublish(api, params) {
  try {
    const response = await api.post('/api/skill/publish', params);
    
    if (!response.data.success) {
      return {
        type: 'error',
        content: '发布失败: ' + response.data.error
      };
    }
    
    const { taskId } = response.data.data;
    
    // 轮询等待完成
    let attempts = 0;
    const maxAttempts = 60; // 最多等待 3 分钟
    let lastProgress = null;
    
    while (attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const statusRes = await api.get('/api/skill/publish/status', {
        params: { taskId }
      });
      
      if (!statusRes.data.success) {
        continue;
      }
      
      const task = statusRes.data.data;
      lastProgress = {
        taskId,
        progress: task.progress,
        step: task.step,
        status: task.status,
        logs: task.logs
      };
      
      if (task.status === 'completed') {
        return {
          type: 'success',
          content: `✅ 文章已成功发布到 **${task.result.accountName}**！`,
          actions: [
            {
              type: 'link',
              label: '查看草稿',
              url: task.result.draftUrl
            },
            {
              type: 'button',
              label: '再写一篇',
              action: 'restart'
            }
          ]
        };
      }
      
      if (task.status === 'failed') {
        return {
          type: 'error',
          content: '❌ 发布失败: ' + task.error
        };
      }

      attempts++;
    }
    
    return {
      type: 'timeout',
      content: '发布任务超时，请稍后查询状态。',
      data: lastProgress || { taskId }
    };
    
  } catch (error) {
    const payload = buildErrorPayload(error, '发布请求失败');
    return {
      type: 'error',
      content: payload.error,
      data: {
        code: payload.code,
        upgradeUrl: payload.upgradeUrl,
        manageUrl: payload.manageUrl,
        retryAfter: payload.retryAfter,
        details: payload.data
      }
    };
  }
}

// ═════════════════════════════════════════════════════════════════════════════
// 意图处理函数
// ═════════════════════════════════════════════════════════════════════════════

/**
 * 处理自然语言意图
 */
async function handleIntent(context, config) {
  const { message, intent, entities } = context;

  // 1. 查询额度意图
  if (message.includes('查询额度') || message.includes('剩余额度') || message.includes('还能发几篇') || message.includes('还能发多') || message.includes('我的额度') || message.includes('剩余发布次数')) {
    const quotaResult = await invokeHandler(getQuota, { query: {} }, config);
    if (!quotaResult.success) {
      return {
        type: 'error',
        content: quotaResult.error || '查询额度失败'
      };
    }
    return {
      type: 'text',
      content: quotaResult.data.statusMessage
    };
  }

  // 2. 纯粹预览意图
  if (message.includes('预览一下') || message.includes('文章预览') || message.includes('生成预览')) {
    return generateAndPublishWorkflow({ ...context, intent: 'preview_article' }, config);
  }

  // 3. 唤起技能意图
  const isWakeUp = /^(使用)?懒人编辑器(技能)?$/.test(message.trim()) || message.includes('启动懒人编辑器') || message.includes('打开懒人编辑器') || message.includes('调用懒人编辑器');
  if (isWakeUp) {
    return {
      type: 'text',
      content: '👋 你好！我是懒人编辑器技能助理。\n\n我可以帮你将内容排版并自动发布到你的微信公众号。你可以对我说：\n- 「帮我写一篇关于人工智能的文章并发布到公众号」\n- 「查询额度」\n- 「预览一下」\n\n请直接告诉我你想写什么主题！'
    };
  }

  // 提取文章主题（去除常用动词）
  const topic = entities.topic || message.replace(/(发布到公众号|发到公众号|排版发布|微信发布|生成文章.*发布|写文章.*公众号|发到微信|推送到公众号|同步到微信|微信文章|写一篇.*文章|帮我写.*文案|生成.*文章|创作.*内容|排版.*公众号|样式.*发布|markdown.*微信|使用懒人编辑器|懒人编辑器技能助理|懒人编辑器)/g, '').replace(/请帮我|给我|现在|立刻/g, '').trim();

  if (!topic) {
    return {
      type: 'question',
      content: '你想写什么主题的文章？请告诉我具体内容或主题。'
    };
  }

  // 提取模板偏好
  let templateHint = null;
  if (message.includes('科技') || message.includes('技术')) {
    templateHint = 'tech';
  } else if (message.includes('美食')) {
    templateHint = 'food';
  } else if (message.includes('商务') || message.includes('专业')) {
    templateHint = 'business';
  } else if (message.includes('教育')) {
    templateHint = 'education';
  }

  // 提取高级元数据支持（正则表达式粗略提取）
  let author = undefined;
  let digest = undefined;
  let contentSourceUrl = undefined;
  let coverImage = undefined;
  let account = undefined;

  const authorMatch = message.match(/作者(?:是|为)?\s*([^\s,，;；。]+)/);
  if (authorMatch) author = authorMatch[1];

  const digestMatch = message.match(/摘要(?:包含|是|为)?\s*[:：\\s]*([^\n。；]+)/);
  if (digestMatch) digest = digestMatch[1];

  const urlMatch = message.match(/(?:获取原文|阅读原文).*?(https?:\/\/[^\s]+)/);
  if (urlMatch) contentSourceUrl = urlMatch[1];

  // 封面的AI生成提示词提取
  const coverMatch = message.match(/(?:封面图|封面)(?:需要是|画一个|生成一个|用)?\s*([^\n。；]+)/);
  if (coverMatch) coverImage = coverMatch[1];

  const accountMatch = message.match(/(?:发布到|发到|推送到|同步到)\s*([^\s,，;；。]+?)(?:公众号|草稿箱)/);
  if (accountMatch) account = accountMatch[1];

  // 返回生成内容的指令
  // 尝试从模板列表中获取组件指引（如果用户消息中隐含了模板选择）
  let componentInstructions = '';
  let htmlStructureInstructions = buildHtmlStructureInstructions(null);
  if (templateHint) {
    try {
      const api = createApiClient(config);
      const templatesRes = await api.get('/api/skill/templates', { params: { limit: 20 } });
      if (templatesRes.data.success) {
        const matchedTpl = findTemplate(templatesRes.data.data.list, templateHint);
        if (matchedTpl) {
          componentInstructions = buildComponentInstructions(matchedTpl);
          htmlStructureInstructions = buildHtmlStructureInstructions(matchedTpl);
        }
      }
    } catch (e) { /* 非关键路径，忽略错误 */ }
  }

  return {
    type: 'action',
    action: 'generate_content',
    params: {
      topic,
      templateHint,
      htmlStructureInstructions,
      componentInstructions,
      author,
      account,
      digest,
      contentSourceUrl,
      coverImage,
      nextStep: 'publish'
    },
    content: `好的，我来为你写一篇关于「${topic}」的文章${coverImage ? '，并生成匹配的封面图' : ''}，并发布到公众号。\n\n【生成要求 - 内容结构优先级】\n${htmlStructureInstructions}${componentInstructions ? `\n\n${componentInstructions}` : ''}`
  };
}

/**
 * 处理命令
 */
async function handleCommand(context, config) {
  const { command, args } = context;

  if (command === 'publish') {
    return generateAndPublishWorkflow(context, config);
  }

  if (command === 'quota') {
    const quotaResult = await invokeHandler(getQuota, { query: {} }, config);
    if (!quotaResult.success) {
      return {
        type: 'error',
        content: quotaResult.error || '查询额度失败'
      };
    }

    return {
      type: 'text',
      content: quotaResult.data.statusMessage,
      data: quotaResult.data
    };
  }

  if (command === 'preview') {
    return generateAndPublishWorkflow({ ...context, intent: 'preview_article' }, config);
  }

  if (command === 'status') {
    const response = await invokeHandler(getPublishStatus, { query: { taskId: args && args.taskId } }, config);

    if (!response.success) {
      return {
        type: 'error',
        content: response.error || '查询发布状态失败'
      };
    }

    return {
      type: 'success',
      content: response.data.statusMessage,
      data: response.data
    };
  }

  return {
    type: 'error',
    content: `未知命令: ${command}`
  };
}

// ═════════════════════════════════════════════════════════════════════════════
// 导出
// ═════════════════════════════════════════════════════════════════════════════

module.exports = {
  // 端点处理函数
  getTemplates,
  getAccounts,
  publishArticle,
  getPublishStatus,
  getQuota,
  previewArticle,
  
  // 工作流处理函数
  generateAndPublishWorkflow,
  executePublish,
  
  // 意图和命令处理
  handleIntent,
  handleCommand
};
