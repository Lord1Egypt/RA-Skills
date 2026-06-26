/**
 * EO RAG Query Tool Handler v2
 * Uses shared RAG system with access control
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { getSharedRAGSystem } from '../rag/rag-system.js'
import { textResult, errorResult } from '../formatters/index.js'

export interface RAGQueryParams {
  query: string
  topK?: number
  strategy?: 'expert_retrieval' | 'pattern_retrieval' | 'checkpoint_retrieval' | 'history_retrieval' | 'hybrid'
}

export async function handleRAGQuery(params: RAGQueryParams, agentId?: string): Promise<AgentToolResult<unknown>> {
  try {
    const ragSystem = getSharedRAGSystem()
    
    // Set agent context for access control
    if (agentId) {
      ragSystem.setAgentContext(agentId)
    }

    const result = await ragSystem.quickSearch(params.query || '', params.topK || 5)

    if (result.chunks.length === 0) {
      return textResult(`🔍 RAG Results (0): No matching knowledge found.\n\nTry different keywords or use \`eo_list_experts\` to browse experts.`)
    }

    const formattedResults = result.chunks.map((chunk, i) => {
      const layerNames = ['', 'Expert', 'Pattern', 'Checkpoint', 'ETP', 'Session']
      const layer = layerNames[chunk.layer] || `L${chunk.layer}`
      const preview = chunk.content.substring(0, 150) + (chunk.content.length > 150 ? '...' : '')
      return `${i + 1}. **[${layer}]** ${preview}`
    }).join('\n')

    const output = `🔍 **RAG Knowledge Base Results**

**Query:** "${params.query}"
**Found:** ${result.chunks.length} results (${result.queryTimeMs}ms)

${formattedResults}`

    return textResult(output)

  } catch (err) {
    return errorResult(`RAG error: ${err instanceof Error ? err.message : String(err)}`)
  }
}
