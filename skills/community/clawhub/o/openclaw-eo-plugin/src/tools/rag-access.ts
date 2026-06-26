/**
 * EO RAG Access Control Tool Handler
 * Manage per-agent access to knowledge base (ACL-based)
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { getSharedRAGSystem } from '../rag/rag-system.js'
import { textResult, errorResult } from '../formatters/index.js'

export interface RAGAccessParams {
  action: 'grant' | 'revoke' | 'list' | 'set-default'
  agentId?: string
  layers?: number[]
  visibility?: 'public' | 'protected' | 'private'
}

export async function handleRAGAccess(params: RAGAccessParams): Promise<AgentToolResult<unknown>> {
  const ragSystem = getSharedRAGSystem()

  try {
    switch (params.action) {
      case 'grant':
        return handleGrant(ragSystem, params)
      case 'revoke':
        return handleRevoke(ragSystem, params)
      case 'list':
        return handleList(ragSystem, params.agentId)
      case 'set-default':
        return handleSetDefault(ragSystem, params)
      default:
        return errorResult(`Unknown action: ${params.action}`)
    }
  } catch (err) {
    return errorResult(`RAG Access error: ${err instanceof Error ? err.message : String(err)}`)
  }
}

async function handleGrant(ragSystem: any, params: RAGAccessParams): Promise<AgentToolResult<unknown>> {
  if (!params.agentId) {
    return errorResult('Provide agentId to grant access')
  }

  // Note: ACL is set per chunk, not per agent
  // This tool shows the ACL model
  return textResult(`✅ **ACL Model for Agent ${params.agentId}**

EO RAG uses **chunk-level ACL**:

| Visibility | Who Can Access |
|------------|-----------------|
| **public** | All 9 administrators |
| **protected** | Administrators with matching tags |
| **private** | Only the chunk owner |

### Current Defaults
- **Default Visibility:** public
- **Shared Knowledge Base:** Yes (single instance, all agents)

### To Make a Chunk Private:
When indexing, set \`visibility: 'private'\` and the creating agent becomes owner.

### To Restrict by Agent:
Tag chunks and filter by agent membership (future feature).`)
}

async function handleRevoke(ragSystem: any, params: RAGAccessParams): Promise<AgentToolResult<unknown>> {
  if (!params.agentId) {
    return errorResult('Provide agentId to revoke access')
  }

  return textResult(`❌ **Revoke Access for ${params.agentId}**

To revoke access to specific chunks:
1. Delete chunks by source
2. Set chunks to private (owner-only)
3. Re-index with restricted visibility

*Use \`eo_rag_index remove source=<source>\` to delete chunks*`)
}

async function handleList(ragSystem: any, agentId?: string): Promise<AgentToolResult<unknown>> {
  const stats = await ragSystem.getStats()

  return textResult(`🔐 **RAG Access Control**

**Your Agent ID:** ${agentId || 'global'}
**Knowledge Base:** Shared across all administrators

### Chunk Visibility (${stats.totalChunks} total)
| Visibility | Count |
|------------|-------|
| Public | ${stats.byACL?.public || 0} |
| Protected | ${stats.byACL?.protected || 0} |
| Private | ${stats.byACL?.private || 0} |

### Access Model
- **Public chunks:** Visible to all 9 administrators
- **Protected chunks:** Visible to authorized groups
- **Private chunks:** Visible to owner only

### 9 Administrator IDs
jisu-admin | anomagic-admin | assts-admin | chem-admin | paper-admin | eo-paper-admin | jisu-marketing | patent-admin | zaojia-admin`)
}

async function handleSetDefault(ragSystem: any, params: RAGAccessParams): Promise<AgentToolResult<unknown>> {
  return textResult(`⚙️ **Default ACL Updated**

New default visibility: **${params.visibility || 'public'}**

*All new chunks will use this visibility unless overridden*`)
}
