/**
 * memory-auto-manager
 * Automatic memory management based on built-in memory-lancedb-local-storage
 * Auto-extract key points after session ends, write to MEMORY.md, update vector index
 */

import fs from 'fs';
import path from 'path';

function activate(ctx) {
  // 触发时机1：会话真正结束（网关退出/会话销毁）
  ctx.hooks.on('session:end', async (session) => {
    ctx.log.info('[memory-auto-manager] Session ended, starting automatic memory processing...');
    try {
      await processSession(session, ctx);
      ctx.log.info('[memory-auto-manager] ✅ Automatic memory processing completed');
    } catch (err) {
      ctx.log.error('[memory-auto-manager] ❌ Error processing memory:', err);
    }
  });

  // 触发时机2：用户执行 /new 命令切换会话（旧会话归档）
  ctx.hooks.on('command:new', async ({ oldSession }) => {
    if (oldSession) {
      ctx.log.info('[memory-auto-manager] Detected /new command, processing previous session...');
      try {
        await processSession(oldSession, ctx);
        ctx.log.info('[memory-auto-manager] ✅ Previous session memory processing completed');
      } catch (err) {
        ctx.log.error('[memory-auto-manager] ❌ Error processing previous session memory:', err);
      }
    }
  });

  // Add CLI command for manual trigger: openclaw memory-auto-manager process-all
  ctx.registerCommand('process-all', async (args, ctx) => {
    ctx.log.info('[memory-auto-manager] Manual trigger: processing all closed sessions...');
    // For now, process current context's available sessions
    // Daily cron will catch remaining
    const sessions = await ctx.listSessions({ closedOnly: true, sinceHours: 24 });
    let processed = 0;
    for (const session of sessions) {
      try {
        if (!session.meta?.processedByAutoManager) {
          await processSession(session, ctx);
          processed++;
          ctx.log.info(`[memory-auto-manager] Processed session ${session.id}`);
        }
      } catch (err) {
        ctx.log.error(`[memory-auto-manager] Failed to process session ${session.id}:`, err);
      }
    }
    ctx.log.info(`[memory-auto-manager] ✅ Manual processing completed, ${processed} sessions processed`);
    return { processed };
  });

  // Register daily cron trigger for all closed sessions
  if (ctx.cron && ctx.cron.schedule) {
    // Run daily at 00:00 UTC
    ctx.cron.schedule('0 0 * * *', async () => {
      ctx.log.info('[memory-auto-manager] Daily automatic memory processing started...');
      try {
        const { processed } = await ctx.invokeCommand('memory-auto-manager process-all');
        ctx.log.info(`[memory-auto-manager] ✅ Daily processing completed, ${processed} sessions processed`);
      } catch (err) {
        ctx.log.error('[memory-auto-manager] ❌ Daily processing failed:', err);
      }
    });
    ctx.log.info('[memory-auto-manager] Registered daily cron job (00:00 UTC)');
  }
}

async function processSession(session, ctx) {
  // Get all messages from session
  const messages = session.messages || [];
  
  // Skip if too few messages
  if (messages.length < 2) {
    ctx.log.info('[memory-auto-manager] Skipping: too few messages');
    return;

  }

  // Format conversation for LLM
  const conversation = messages
    .filter(m => m.content && m.content.trim().length > 0)
    .map(m => `**${m.role}**: ${m.content}`)
    .join('\n\n');

  // Call LLM to extract key points
  const prompt = getExtractionPrompt(conversation);
  const result = await ctx.invokeLLM(prompt);
  
  // Parse result
  let extracted;
  try {
    // Try to extract JSON from response
    const jsonMatch = result.match(/```json\n([\s\S]*)\n```/) || result.match(/{[\s\S]*}/);
    const jsonStr = jsonMatch ? jsonMatch[1] || jsonMatch[0] : result;
    extracted = JSON.parse(jsonStr.trim());
  } catch (err) {
    ctx.log.error('[memory-auto-manager] Failed to parse LLM response:', err);
    // Fallback: treat entire response as keyPoints
    extracted = {
      keyPoints: result.trim(),
      category: 'fact'
    };
  }

  const { keyPoints, category = 'fact' } = extracted;

  // Check if worth retaining
  if (!keyPoints || typeof keyPoints !== 'string' || keyPoints.trim().length < 20) {
    ctx.log.info('[memory-auto-manager] Skipping: content too short or empty');
    return;
  }

  // Write to MEMORY.md
  const memoryPath = path.join(ctx.workspace, 'MEMORY.md');
  const date = new Date().toISOString().split('T')[0];
  const timestamp = new Date().toISOString();
  
  const content = `
---
### ${timestamp}
### ${date} / ${category}
${keyPoints.trim()}

---
`;

  await fs.promises.appendFile(memoryPath, content, 'utf8');
  ctx.log.info(`[memory-auto-manager] ✉️ Wrote key points to MEMORY.md (timestamp: ${timestamp})`);

  // Update vector index
  ctx.log.info('[memory-auto-manager] 🔄 Updating vector memory index...');
  await ctx.exec('openclaw memory index --force');

  ctx.log.info('[memory-auto-manager] ✅ All done!');
}

function getExtractionPrompt(conversation) {
  return `你是一个记忆整理助手，请帮我整理下面这段对话，提取核心要点：

要求：
1. 去掉所有闲聊、重复、无意义的内容，只保留真正重要的信息
2. 提炼要点，保持简洁
3. 分类：decision(重要决策)/fact(事实信息)/preference(用户偏好)/entity(实体信息)
4. 输出JSON格式：
{
  "keyPoints": "提炼后的核心内容",
  "category": "decision/fact/preference/entity"
}

对话内容：
${conversation}
`;
}

module.exports = { activate };
