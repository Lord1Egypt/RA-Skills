#!/usr/bin/env node
/**
 * Human-Like Memory CLI for OpenClaw Skill
 *
 * Usage:
 *   node memory.mjs recall "query"
 *   node memory.mjs save "user message" "assistant response"
 *   node memory.mjs save-batch                    # reads JSON from stdin
 *   node memory.mjs search "query"
 *   node memory.mjs config
 */

import { createInterface } from 'readline';
import { buildConfig, buildMissingApiKeyError } from './config.mjs';
import { httpRequest } from './client.mjs';

const SKILL_VERSION = '1.0.12';

function truncate(text, maxLen) {
  if (!text || text.length <= maxLen) return text || '';
  return text.substring(0, maxLen - 3) + '...';
}

function formatLogValue(value, maxLen = 48) {
  if (value === undefined || value === null || value === '') return '-';
  if (Array.isArray(value)) {
    if (value.length === 0) return '-';
    const items = value.slice(0, 3).map((item) => truncate(String(item), 24));
    return items.join(',') + (value.length > 3 ? ',...' : '');
  }
  return truncate(String(value), maxLen);
}

function maskSecretForLog(value, prefix = 10, suffix = 6) {
  const text = String(value || '').trim();
  if (!text) return '-';
  if (text.length <= prefix + suffix) return text;
  return `${text.slice(0, prefix)}...${text.slice(-suffix)}`;
}

function buildRequestId(prefix = 'openclaw-skill') {
  return `${prefix}-${Date.now()}`;
}

function memoryPreviewItem(memory, rank) {
  if (!memory || typeof memory !== 'object') {
    return `#${rank} id=- text="-"`;
  }
  const parts = [
    `#${rank}`,
    `id=${formatLogValue(memory.id, 8)}`,
  ];
  if (typeof memory.score === 'number' && Number.isFinite(memory.score)) {
    parts.push(`s=${memory.score.toFixed(6)}`);
  }
  parts.push(`text="${truncate(memory.description || memory.event || memory.content || '', 80)}"`);
  return parts.join(' ');
}

function memoryPreviewSummary(memories, limit = 3) {
  if (!Array.isArray(memories) || memories.length === 0) return '-';
  return memories.slice(0, limit).map((memory, index) => memoryPreviewItem(memory, index + 1)).join(' | ');
}

function logSkillStage(stage, fields = {}) {
  const content = Object.entries(fields)
    .map(([key, value]) => `${key}=${formatLogValue(value, key === 'top' ? 240 : 96)}`)
    .join(' ');
  console.error(`[OpenClaw Skill][${stage}] ${content}`.trim());
}

function extractText(content) {
  if (content === undefined || content === null) return '';
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item && typeof item === 'object') {
          if (typeof item.text === 'string') return item.text;
          if (typeof item.content === 'string') return item.content;
        }
        return '';
      })
      .filter(Boolean)
      .join('\n');
  }
  if (typeof content === 'object') {
    if (typeof content.text === 'string') return content.text;
    if (typeof content.content === 'string') return content.content;
    try {
      return JSON.stringify(content);
    } catch {
      return String(content);
    }
  }
  return String(content);
}

function normalizeMessageContent(content) {
  return extractText(content).trim();
}

function cloneToolCall(toolCall) {
  if (!toolCall || typeof toolCall !== 'object') return null;
  const functionName = toolCall.function?.name || toolCall.name;
  const functionArgs = toolCall.function?.arguments ?? toolCall.arguments ?? '{}';
  if (!functionName) return null;
  return {
    id: toolCall.id || null,
    type: toolCall.type || 'function',
    function: {
      name: functionName,
      arguments: typeof functionArgs === 'string' ? functionArgs : JSON.stringify(functionArgs),
    },
  };
}

function getMessageToolCalls(message) {
  if (!Array.isArray(message?.tool_calls)) return [];
  return message.tool_calls.map(cloneToolCall).filter(Boolean);
}

function getToolResultCallId(message) {
  return message?.tool_call_id || message?.toolCallId || message?.call_id || null;
}

function getToolResultName(message) {
  return message?.name || message?.tool_name || message?.toolName || undefined;
}

function normalizeInputMessage(message) {
  if (!message || typeof message !== 'object') {
    return { error: 'Each message must be an object with "role" and "content" fields' };
  }

  const role = String(message.role || '').trim();
  if (!['user', 'assistant', 'tool'].includes(role)) {
    return { error: 'Role must be "user", "assistant", or "tool"' };
  }

  if (role === 'user') {
    const content = normalizeMessageContent(message.content);
    if (!content) return { message: null };
    return { message: { role, content } };
  }

  if (role === 'assistant') {
    const content = normalizeMessageContent(message.content);
    const toolCalls = getMessageToolCalls(message);
    if (!content && toolCalls.length === 0) return { message: null };
    return {
      message: {
        role,
        content: content || '',
        tool_calls: toolCalls.length > 0 ? toolCalls : undefined,
      },
    };
  }

  const content = normalizeMessageContent(message.content);
  const toolCallId = getToolResultCallId(message);
  const name = getToolResultName(message);
  if (!content && !toolCallId && !name) return { message: null };
  return {
    message: {
      role: 'tool',
      content: content || '',
      tool_call_id: toolCallId || undefined,
      name,
    },
  };
}

function normalizeMessages(messages) {
  if (!Array.isArray(messages) || messages.length === 0) {
    return { error: 'Messages must be a non-empty array' };
  }

  const normalized = [];
  for (const message of messages) {
    const result = normalizeInputMessage(message);
    if (result.error) {
      return { error: result.error, invalid: message };
    }
    if (result.message) {
      normalized.push(result.message);
    }
  }

  if (normalized.length === 0) {
    return { error: 'No non-empty user, assistant, or tool messages to save' };
  }

  return { messages: normalized };
}

function getLatestUserMessageText(messages) {
  if (!Array.isArray(messages)) return '';
  for (let i = messages.length - 1; i >= 0; i -= 1) {
    if (messages[i]?.role === 'user') return messages[i].content || '';
  }
  return '';
}

function buildWorkflowMetadata(cfg, sessionId, agentId) {
  return {
    user_ids: [cfg.userId],
    agent_ids: [agentId],
    session_id: sessionId,
    scenario: cfg.scenario || 'openclaw-plugin',
  };
}

function stripToolMessagesForV1(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .filter((message) => message && message.role !== 'tool' && message.role !== 'system')
    .map((message) => ({
      role: message.role,
      content: message.content,
    }));
}

function isErrorResult(text) {
  if (!text) return false;
  const lower = String(text).toLowerCase();
  return lower.includes('error')
    || lower.includes('exception')
    || lower.includes('failed')
    || lower.includes('traceback')
    || lower.includes('enoent')
    || lower.includes('permission denied');
}

function extractToolCalls(messages) {
  if (!Array.isArray(messages) || messages.length === 0) return [];

  const calls = [];
  for (const message of messages) {
    if (message.role === 'assistant') {
      const toolCalls = getMessageToolCalls(message);
      for (const toolCall of toolCalls) {
        calls.push({
          tool_name: toolCall.function?.name || toolCall.name || 'unknown',
          arguments: toolCall.function?.arguments || toolCall.arguments || '{}',
          call_id: toolCall.id || null,
          result: null,
          success: null,
          duration_ms: null,
        });
      }
    }

    if (message.role !== 'tool') continue;

    const toolCallId = getToolResultCallId(message);
    const toolName = getToolResultName(message);
    const match = calls.find((call) =>
      (toolCallId && call.call_id === toolCallId) ||
      (!toolCallId && toolName && call.tool_name === toolName && call.result == null)
    );

    if (match) {
      const resultText = extractText(message.content);
      match.result = truncate(resultText, 2000);
      match.success = !isErrorResult(resultText);
    }
  }

  return calls;
}

function buildV2ConversationMessages(messages, captureToolCalls) {
  return messages
    .filter((message) => message && message.role !== 'system')
    .filter((message) => captureToolCalls || message.role !== 'tool')
    .map((message) => {
      if (message.role === 'tool') {
        return {
          role: 'tool',
          content: message.content || '',
          tool_call_id: message.tool_call_id || undefined,
          name: message.name,
        };
      }

      return {
        role: message.role,
        content: message.content || '',
        tool_calls: captureToolCalls && Array.isArray(message.tool_calls) && message.tool_calls.length > 0
          ? message.tool_calls
          : undefined,
      };
    })
    .filter((message) => {
      if (!message) return false;
      if (message.role === 'tool') {
        return !!(message.content || message.tool_call_id || message.name);
      }
      return !!(message.content || (Array.isArray(message.tool_calls) && message.tool_calls.length > 0));
    });
}

function collectContextBlocks(messages, cfg) {
  const blocks = [];
  const conversationMessages = buildV2ConversationMessages(messages, cfg.captureToolCalls !== false);
  if (conversationMessages.length > 0) {
    blocks.push({
      type: 'conversation',
      data: { messages: conversationMessages },
    });
  }

  if (cfg.captureToolCalls !== false) {
    const toolCalls = extractToolCalls(messages);
    if (toolCalls.length > 0) {
      blocks.push({
        type: 'tool_calls',
        data: { calls: toolCalls },
      });
    }
  }

  return blocks;
}

async function addMemoryV1(messages, cfg, sessionId, requestId) {
  const agentId = cfg.agentId || 'main';
  const url = `${cfg.baseUrl}/api/plugin/v1/add/message`;
  const payload = {
    user_id: cfg.userId,
    conversation_id: sessionId,
    messages: stripToolMessagesForV1(messages),
    agent_id: agentId,
    scenario: cfg.scenario || 'openclaw-plugin',
    tags: ['openclaw-skill'],
    async_mode: true,
    custom_workflows: {
      stream_params: {
        metadata: JSON.stringify(buildWorkflowMetadata(cfg, sessionId, agentId)),
      },
    },
  };

  const result = await httpRequest(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cfg.apiKey,
      'x-request-id': requestId,
      'x-plugin-version': SKILL_VERSION,
      'x-client-type': 'skill',
    },
    body: JSON.stringify(payload),
  }, cfg.timeoutMs);

  return { result, protocol: 'v1', url, payload };
}

async function addContextV2(messages, cfg, sessionId, requestId) {
  const agentId = cfg.agentId || 'main';
  const url = `${cfg.baseUrl}/api/plugin/v2/add/context`;
  const contextBlocks = collectContextBlocks(messages, cfg);
  if (contextBlocks.length === 0) {
    throw new Error('No context blocks to save');
  }

  const payload = {
    user_id: cfg.userId,
    conversation_id: sessionId,
    agent_id: agentId,
    scenario: cfg.scenario || 'openclaw-plugin',
    async_mode: true,
    protocol_version: '2.0',
    context_blocks: contextBlocks,
    custom_workflows: {
      stream_params: {
        metadata: JSON.stringify(buildWorkflowMetadata(cfg, sessionId, agentId)),
      },
    },
  };

  const result = await httpRequest(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cfg.apiKey,
      'x-request-id': requestId,
      'x-plugin-version': SKILL_VERSION,
      'x-client-type': 'skill',
    },
    body: JSON.stringify(payload),
  }, cfg.timeoutMs);

  return { result, protocol: 'v2', url, payload };
}

async function saveNormalizedMessages(messages, cfg) {
  const sessionId = `session-${Date.now()}`;
  const agentId = cfg.agentId || 'main';
  const requestId = buildRequestId();
  const requestStart = Date.now();
  const lastUser = getLatestUserMessageText(messages);
  const contextBlocks = cfg.useV2Protocol ? collectContextBlocks(messages, cfg) : [];
  const startUrl = cfg.useV2Protocol
    ? `${cfg.baseUrl}/api/plugin/v2/add/context`
    : `${cfg.baseUrl}/api/plugin/v1/add/message`;

  logSkillStage('Add][START', {
    req: requestId,
    url: startUrl,
    protocol: cfg.useV2Protocol ? 'v2' : 'v1',
    user_id: cfg.userId,
    agent_id: agentId,
    conversation_id: sessionId,
    messages: messages.length,
    roles: messages.map((message) => message.role),
    blocks: contextBlocks.map((block) => block.type),
    last_user: `"${truncate(lastUser, 80)}"`,
    scenario: cfg.scenario,
    api_key: maskSecretForLog(cfg.apiKey),
  });

  try {
    let saved;
    if (cfg.useV2Protocol) {
      try {
        saved = await addContextV2(messages, cfg, sessionId, requestId);
      } catch (error) {
        logSkillStage('Add][FALLBACK', {
          req: requestId,
          from: 'v2',
          to: 'v1',
          error: `"${truncate(error.message || String(error), 160)}"`,
        });
        saved = await addMemoryV1(messages, cfg, sessionId, requestId);
        saved.fallbackFrom = 'v2';
      }
    } else {
      saved = await addMemoryV1(messages, cfg, sessionId, requestId);
    }

    logSkillStage('Add][END', {
      req: requestId,
      success: true,
      protocol: saved.protocol,
      fallback_from: saved.fallbackFrom || '-',
      total_ms: Date.now() - requestStart,
      count: saved.result.memories_count || 0,
      server_req: saved.result.request_id,
      message: `"${truncate(saved.result.message || 'Memory saved successfully', 120)}"`,
    });

    return {
      ...saved,
      sessionId,
    };
  } catch (error) {
    logSkillStage('Add][END', {
      req: requestId,
      success: false,
      total_ms: Date.now() - requestStart,
      error: `"${truncate(error.message || String(error), 160)}"`,
    });
    throw error;
  }
}

/**
 * Recall memories based on query
 */
async function recallMemory(query) {
  const cfg = await buildConfig();

  if (!cfg.apiKey) {
    console.error(JSON.stringify(buildMissingApiKeyError()));
    process.exit(1);
  }

  if (!cfg.recallEnabled) {
    console.log(JSON.stringify({
      success: true,
      count: 0,
      memories: [],
      message: 'Memory recall is disabled via HUMAN_LIKE_MEM_RECALL_ENABLED=false',
    }, null, 2));
    return;
  }

  const url = `${cfg.baseUrl}/api/plugin/v1/search/memory`;
  const requestId = buildRequestId();
  const requestStart = Date.now();
  const payload = {
    query: query,
    user_id: cfg.userId,
    agent_id: cfg.agentId,
    memory_limit_number: cfg.memoryLimitNumber,
    min_score: cfg.minScore,
    scenario: cfg.scenario,
    scenarios: cfg.scenario ? [cfg.scenario] : [],
  };
  logSkillStage('Search][START', {
    req: requestId,
    url,
    query: `"${truncate(query, 80)}"`,
    qlen: query.length,
    user_id: cfg.userId,
    agent_id: cfg.agentId,
    scenario: cfg.scenario,
    limit: cfg.memoryLimitNumber,
    min_score: cfg.minScore,
    api_key: maskSecretForLog(cfg.apiKey),
  });

  try {
    const result = await httpRequest(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': cfg.apiKey,
        'x-request-id': requestId,
        'x-plugin-version': SKILL_VERSION,
        'x-client-type': 'skill',
      },
      body: JSON.stringify(payload),
    }, cfg.timeoutMs);

    if (!result.success) {
      logSkillStage('Search][END', {
        req: requestId,
        success: false,
        total_ms: Date.now() - requestStart,
        error: `"${truncate(result.error || 'Memory retrieval failed', 160)}"`,
      });
      console.error(JSON.stringify({
        success: false,
        error: result.error || 'Memory retrieval failed',
      }));
      process.exit(1);
    }

    const memories = result.memories || [];

    // Format output for agent consumption
    const output = {
      success: true,
      count: memories.length,
      memories: memories.map(m => ({
        content: m.description || m.event || '',
        timestamp: m.timestamp,
        score: m.score,
      })),
    };

    // Also output human-readable format for context injection
    if (memories.length > 0) {
      output.context = formatMemoriesForContext(memories);
    }

    logSkillStage('Search][END', {
      req: requestId,
      success: true,
      count: memories.length,
      total_ms: Date.now() - requestStart,
      top: memoryPreviewSummary(memories),
    });
    console.log(JSON.stringify(output, null, 2));
  } catch (error) {
    logSkillStage('Search][END', {
      req: requestId,
      success: false,
      total_ms: Date.now() - requestStart,
      error: `"${truncate(error.message || String(error), 160)}"`,
    });
    console.error(JSON.stringify({
      success: false,
      error: error.message,
    }));
    process.exit(1);
  }
}

/**
 * Save messages to memory
 */
async function saveMemory(userMessage, assistantResponse) {
  const cfg = await buildConfig();

  if (!cfg.apiKey) {
    console.error(JSON.stringify(buildMissingApiKeyError()));
    process.exit(1);
  }

  if (!cfg.addEnabled) {
    console.log(JSON.stringify({
      success: true,
      message: 'Memory storage is disabled via HUMAN_LIKE_MEM_ADD_ENABLED=false',
    }));
    return;
  }

  const rawMessages = [];

  if (userMessage) {
    rawMessages.push({ role: 'user', content: userMessage });
  }
  if (assistantResponse) {
    rawMessages.push({ role: 'assistant', content: assistantResponse });
  }

  const normalizedResult = normalizeMessages(rawMessages);
  if (normalizedResult.error) {
    console.error(JSON.stringify({
      success: false,
      error: normalizedResult.error,
      invalid: normalizedResult.invalid,
    }));
    process.exit(1);
  }

  try {
    const saved = await saveNormalizedMessages(normalizedResult.messages, cfg);
    const output = {
      success: true,
      message: 'Memory saved successfully',
      memoriesCount: saved.result.memories_count || 0,
      protocol: saved.protocol,
      fallbackFrom: saved.fallbackFrom || null,
    };
    console.log(JSON.stringify(output));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
    }));
    process.exit(1);
  }
}

/**
 * Search memories (alias for recall with different output format)
 */
async function searchMemory(query) {
  await recallMemory(query);
}

/**
 * Read JSON from stdin
 */
async function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    const rl = createInterface({
      input: process.stdin,
      terminal: false,
    });

    rl.on('line', (line) => {
      data += line;
    });

    rl.on('close', () => {
      resolve(data.trim());
    });

    rl.on('error', reject);

    // Timeout after 5 seconds if no input
    setTimeout(() => {
      rl.close();
      if (!data) {
        reject(new Error('No input received from stdin'));
      }
    }, 5000);
  });
}

/**
 * Save batch messages to memory (from stdin JSON)
 */
async function saveBatchMemory() {
  const cfg = await buildConfig();

  if (!cfg.apiKey) {
    console.error(JSON.stringify(buildMissingApiKeyError()));
    process.exit(1);
  }

  if (!cfg.addEnabled) {
    console.log(JSON.stringify({
      success: true,
      message: 'Memory storage is disabled via HUMAN_LIKE_MEM_ADD_ENABLED=false',
    }));
    return;
  }

  let inputData;
  try {
    inputData = await readStdin();
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: `Failed to read stdin: ${error.message}`,
      usage: 'echo \'[{"role":"user","content":"..."}, {"role":"assistant","content":"..."}]\' | node memory.mjs save-batch',
    }));
    process.exit(1);
  }

  let messages;
  try {
    messages = JSON.parse(inputData);
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: `Invalid JSON: ${error.message}`,
      received: inputData.substring(0, 200),
    }));
    process.exit(1);
  }

  if (!Array.isArray(messages) || messages.length === 0) {
    console.error(JSON.stringify({
      success: false,
      error: 'Messages must be a non-empty array',
    }));
    process.exit(1);
  }

  const maxMessages = cfg.saveMaxMessages;
  const messagesToSave = messages.slice(-maxMessages);
  const normalizedResult = normalizeMessages(messagesToSave);
  if (normalizedResult.error) {
    console.error(JSON.stringify({
      success: false,
      error: normalizedResult.error,
      invalid: normalizedResult.invalid,
    }));
    process.exit(1);
  }

  try {
    const saved = await saveNormalizedMessages(normalizedResult.messages, cfg);
    const dialogueMessages = normalizedResult.messages.filter((message) => message.role !== 'tool');
    const turnCount = Math.floor(dialogueMessages.length / 2);
    const output = {
      success: true,
      message: `Saved ${turnCount} turns (${normalizedResult.messages.length} messages) to memory`,
      memoriesCount: saved.result.memories_count || 0,
      protocol: saved.protocol,
      fallbackFrom: saved.fallbackFrom || null,
      config: {
        saveMaxMessages: cfg.saveMaxMessages,
      },
    };
    console.log(JSON.stringify(output));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
    }));
    process.exit(1);
  }
}

/**
 * Show current configuration (without sensitive data)
 */
async function showConfig() {
  const cfg = await buildConfig();

  console.log(JSON.stringify({
    baseUrl: cfg.baseUrl,
    userId: cfg.userId,
    agentId: cfg.agentId,
    scenario: cfg.scenario,
    apiKeyConfigured: !!cfg.apiKey,
    memoryLimitNumber: cfg.memoryLimitNumber,
    minScore: cfg.minScore,
    recallEnabled: cfg.recallEnabled,
    addEnabled: cfg.addEnabled,
    autoSaveEnabled: cfg.autoSaveEnabled,
    saveTriggerTurns: cfg.saveTriggerTurns,
    saveMaxMessages: cfg.saveMaxMessages,
    useV2Protocol: cfg.useV2Protocol,
    captureToolCalls: cfg.captureToolCalls,
    mode: 'agent-smart',
  }, null, 2));
}

/**
 * Format memories for context injection (aligned with plugin format)
 */
function formatMemoriesForContext(memories) {
  if (!memories || memories.length === 0) return '';

  const now = Date.now();
  const nowText = formatTime(now);

  const memoryLines = memories
    .map(m => {
      const date = formatTime(m.timestamp);
      const content = m.description || m.event || '';
      const score = m.score ? ` (${(m.score * 100).toFixed(0)}%)` : '';
      if (!content) return '';
      if (date) return `   -[${date}] ${content}${score}`;
      return `   - ${content}${score}`;
    })
    .filter(Boolean);

  if (memoryLines.length === 0) return '';

  const lines = [
    '# Role',
    '',
    'You are an intelligent assistant with long-term memory capabilities. Your goal is to combine retrieved memory fragments to provide highly personalized, accurate, and logically rigorous responses.',
    '',
    '# System Context',
    '',
    `* Current Time: ${nowText} (Use this as the baseline for freshness checks)`,
    '',
    '# Memory Data',
    '',
    'Below are **episodic memory summaries** retrieved from long-term memory.',
    '',
    '* **Memory Type**: All memories are episodic summaries - they represent contextual information from past conversations.',
    '* **Special Note**: If content is tagged with \'[assistant_opinion]\' or \'[model_summary]\', it represents **past AI inference**, **not** direct user statements.',
    '',
    '```text',
    '<memories>',
    ...memoryLines,
    '</memories>',
    '```',
    '',
    '# Critical Protocol: Memory Safety',
    '',
    '1. **Source Verification**: Distinguish direct user statements from AI inference. AI summaries are reference-only.',
    '2. **Attribution Check**: Never attribute third-party info to the user.',
    '3. **Strong Relevance Check**: Only use memories that directly help answer the current query.',
    '4. **Freshness Check**: Prioritize the current query over conflicting memories.',
    '',
    '# Instructions',
    '',
    '1. **Review**: Read the episodic memory summaries and apply the protocol above to remove noise.',
    '2. **Execute**: Use only memories that pass filtering as context.',
    '3. **Output**: Answer directly. Never mention internal terms such as "memory store", "retrieval", or "AI opinions".',
  ];

  return lines.join('\n');
}

/**
 * Format timestamp for display
 */
function formatTime(value) {
  if (!value) return '';
  if (typeof value === 'number') {
    const date = new Date(value);
    if (isNaN(date.getTime())) return '';
    const pad = (v) => String(v).padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
  }
  return String(value);
}

/**
 * Print usage information
 */
function printUsage() {
  console.log(`
Human-Like Memory CLI for OpenClaw

Usage:
  node memory.mjs <command> [arguments]

Commands:
  recall <query>                    Retrieve relevant memories for a query
  save <user_msg> [assistant_msg]   Save single conversation turn to memory
  save-batch                        Save multiple turns from stdin (JSON array)
  search <query>                    Search memories (alias for recall)
  config                            Show current configuration

Examples:
  node memory.mjs recall "What projects am I working on?"
  node memory.mjs save "I'm working on Project X" "Great, I'll remember that."
  node memory.mjs search "meeting notes"
  node memory.mjs config

  # Save batch (pipe JSON array of messages):
  echo '[{"role":"user","content":"Hi"},{"role":"assistant","content":"Hello!"}]' | node memory.mjs save-batch

Configuration:
  Configure via OpenClaw config or environment variables:
  - HUMAN_LIKE_MEM_API_KEY (required)
  - HUMAN_LIKE_MEM_BASE_URL (optional, default: https://plugin.human-like.me)
  - HUMAN_LIKE_MEM_USER_ID (optional, default: openclaw-user)
  - HUMAN_LIKE_MEM_AGENT_ID (optional, default: main)
  - HUMAN_LIKE_MEM_LIMIT_NUMBER (optional, default: 6)
  - HUMAN_LIKE_MEM_MIN_SCORE (optional, default: 0.0)
  - HUMAN_LIKE_MEM_RECALL_ENABLED (optional, default: true)
  - HUMAN_LIKE_MEM_ADD_ENABLED (optional, default: true)
  - HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED (optional, default: true)
  - HUMAN_LIKE_MEM_SAVE_TRIGGER_TURNS (optional, default: 5)
  - HUMAN_LIKE_MEM_SAVE_MAX_MESSAGES (optional, default: 20)
  - HUMAN_LIKE_MEM_SCENARIO (optional, default: openclaw-plugin)
  - HUMAN_LIKE_MEM_USE_V2_PROTOCOL (optional, default: true)
  - HUMAN_LIKE_MEM_CAPTURE_TOOL_CALLS (optional, default: true)
`);
}

async function main() {
  const [,, command, ...args] = process.argv;

  switch (command) {
    case 'recall':
      if (!args[0]) {
        console.error('Error: Query is required for recall command');
        process.exit(1);
      }
      await recallMemory(args.join(' '));
      break;

    case 'save':
      if (!args[0]) {
        console.error('Error: At least one message is required for save command');
        process.exit(1);
      }
      await saveMemory(args[0], args[1]);
      break;

    case 'save-batch':
      await saveBatchMemory();
      break;

    case 'search':
      if (!args[0]) {
        console.error('Error: Query is required for search command');
        process.exit(1);
      }
      await searchMemory(args.join(' '));
      break;

    case 'config':
      await showConfig();
      break;

    case 'help':
    case '--help':
    case '-h':
      printUsage();
      break;

    default:
      if (command) {
        console.error(`Unknown command: ${command}`);
      }
      printUsage();
      process.exit(1);
  }
}

await main().catch((error) => {
  console.error(JSON.stringify({
    success: false,
    error: error.message || String(error),
  }));
  process.exit(1);
});
