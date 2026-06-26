/**
 * Session End Hook
 * Analyzes session, triggers continuous learning loop
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'

import { PLUGIN_VERSION } from '../config.js'
import { createContinuousLoop } from '../continuous/index.js'
import { proactiveNotifier } from '../continuous/proactive-notifier.js'
import { createMemoryAutoTrigger } from '../memory/auto-trigger.js'

export interface SessionEndData {
  toolsUsed: string[]
  messageCount: number
  lastMessage: string
  feishuChatId?: string    // Chat ID for Feishu notifications
}

export async function onSessionEnd(api: OpenClawPluginApi, data: SessionEndData) {
  api.logger.debug(`[EO SessionEnd v${PLUGIN_VERSION}] Session end: ${data.messageCount} messages`)

  // Auto-trigger: session_end event
  const autoTrigger = createMemoryAutoTrigger(api, process.cwd())
  await autoTrigger.processEvent('session_end', {
    messageCount: data.messageCount,
    lastMessage: data.lastMessage
  })

  // Create continuous learning loop
  const loop = createContinuousLoop(api, process.cwd())

  // Execute the continuous learning loop
  const result = await loop.execute({
    toolsUsed: data.toolsUsed,
    messageCount: data.messageCount,
    lastMessage: data.lastMessage,
  })

  // Build summary for Feishu notification
  const summary = {
    messageCount: data.messageCount,
    patternsExtracted: result.patternsExtracted,
    ragUpdated: result.ragUpdated,
    weightsAdjusted: result.weightsAdjusted,
    dreamTriggered: result.dreamTriggered,
    success: result.success,
    timestamp: new Date().toISOString(),
  }

  if (result.success) {
    api.logger.debug(
      `[EO SessionEnd] Loop completed: patterns=${result.patternsExtracted}, ragUpdated=${result.ragUpdated}, weights=${result.weightsAdjusted}`
    )

    // If errors accumulated, note it
    if (result.dreamTriggered) {
      api.logger.info(`[EO SessionEnd] Dream triggered by continuous learning loop`)
    }

    // Send Feishu notification if chat_id is available
    if (data.feishuChatId) {
      const lines = [
        `📊 会话结束 - 记忆同步报告`,
        ``,
        `• 消息数：${summary.messageCount}`,
        `• Pattern提取：${summary.patternsExtracted}个`,
        `• 知识库更新：${summary.ragUpdated ? '✅' : '❌'}`,
        `• 专家权重调整：${summary.weightsAdjusted ? '✅' : '❌'}`,
        `• Dream触发：${summary.dreamTriggered ? '🌙 已触发' : '❌ 未触发'}`,
        ``,
        `⏰ ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`,
      ]
      try {
        await proactiveNotifier.notify(
          'info',
          'EO 记忆同步完成',
          lines.join('\n'),
          ['feishu'],
          { feishuChatId: data.feishuChatId }
        )
      } catch (e) {
        api.logger.warn(`[EO SessionEnd] Feishu notification failed: ${e}`)
      }
    }
  } else {
    api.logger.warn(`[EO SessionEnd] Loop completed with errors: ${result.errors.join(', ')}`)

    // Send error notification to Feishu
    if (data.feishuChatId) {
      try {
        await proactiveNotifier.notify(
          'warning',
          '⚠️ EO 记忆同步异常',
          `会话记忆同步完成，但有错误：\n${result.errors.join('\n')}`,
          ['feishu'],
          { feishuChatId: data.feishuChatId }
        )
      } catch (e) {
        api.logger.warn(`[EO SessionEnd] Feishu notification failed: ${e}`)
      }
    }
  }
}

export function createSessionEndHook(api: OpenClawPluginApi) {
  return {
    id: 'eo_session_end',
    name: 'EO Session End',
    description: 'Analyzes session and triggers continuous learning loop',
    handle: async (event: any) => {
      const context = event.context as Record<string, unknown>
      // Extract chat_id from event context - could be in different places depending on channel
      let feishuChatId: string | undefined
      const ctx = context as Record<string, any>
      const chatIdSources = [
        ctx?.chatId as string,
        ctx?.peer?.id as string,
        ctx?.channel?.chatId as string,
        event?.chatId as string,
        event?.peer as string,
      ]
      for (const src of chatIdSources) {
        if (src && typeof src === 'string' && src.startsWith('oc_')) {
          feishuChatId = src
          break
        }
      }

      await onSessionEnd(api, {
        toolsUsed: (context?.toolsUsed as string[]) || [],
        messageCount: (context?.messageCount as number) || 0,
        lastMessage: (context?.lastMessage as string) || '',
        feishuChatId,
      })
    },
  }
}
