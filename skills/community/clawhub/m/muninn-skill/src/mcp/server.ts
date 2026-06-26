/**
 * OpenClaw Memory System - MCP Server
 * Provides memory tools to OpenClaw agents
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { KNOWLEDGE_TOOLS, KNOWLEDGE_HANDLERS } from './knowledge-tools.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { MemoryStore, Memory, MemoryType, Procedure } from '../storage/index.js';
import { extract, routeContent } from '../extractors/index.js';
import { consolidate } from '../consolidation/index.js';
import { cohesionQuery } from '../retrieval/session-priming.js';

// Audit System Imports
import { 
  createComprehensiveAuditWrappers,
  createAuditWrappers,
  calculateStaleness,
  type StalenessInfo,
  type RetrievalAuditResult
} from '../storage/audit-integration.js';
import { 
  ContradictionStore, 
  type MemoryContradiction 
} from '../reasoning/memory-contradiction.js';
import { 
  IntegrityStore, 
  formatIntegrityReport,
  type IntegrityReport
} from '../storage/integrity.js';

// Initialize store
const store = new MemoryStore();

// Initialize Audit System (Phase 1-4)
// Note: We create wrappers that use the store's internal DB
let auditWrappers: ReturnType<typeof createComprehensiveAuditWrappers> | null = null;
let auditHelper: ReturnType<typeof createAuditWrappers> | null = null;
let contradictionStore: ContradictionStore | null = null;
let integrityStore: IntegrityStore | null = null;

function getAuditSystem() {
  if (!auditWrappers) {
    // Get the internal database from the store
    const db = (store as any).db;
    if (db) {
      auditWrappers = createComprehensiveAuditWrappers(db);
      auditHelper = createAuditWrappers(auditWrappers.audit);
      contradictionStore = auditWrappers.contradiction;
      integrityStore = auditWrappers.integrity;
    }
  }
  return { auditWrappers, auditHelper, contradictionStore, integrityStore };
}

// Server instance
const server = new Server(
  {
    name: 'openclaw-memory',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions
const tools = [
  {
    name: 'memory_remember',
    description: 'Store a memory with auto-extraction of entities and topics. Automatically classifies as episodic, semantic, or procedural. Use sessionDate for temporal resolution (e.g., "2023-05-08" to resolve "yesterday" to "2023-05-07").',
    inputSchema: {
      type: 'object',
      properties: {
        content: {
          type: 'string',
          description: 'The content to remember'
        },
        type: {
          type: 'string',
          enum: ['episodic', 'semantic', 'procedural'],
          description: 'Memory type (auto-detected if not specified)'
        },
        title: {
          type: 'string',
          description: 'Optional title for the memory'
        },
        context: {
          type: 'string',
          description: 'Additional context for routing'
        },
        sessionDate: {
          type: 'string',
          description: 'Reference date for temporal resolution (ISO format: YYYY-MM-DD or "1:56 pm on 8 May, 2023")'
        }
      },
      required: ['content']
    }
  },
  {
    name: 'memory_recall',
    description: 'Retrieve relevant memories via semantic search across all memory types.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Search query'
        },
        types: {
          type: 'array',
          items: { type: 'string', enum: ['episodic', 'semantic', 'procedural'] },
          description: 'Filter by memory types'
        },
        entities: {
          type: 'array',
          items: { type: 'string' },
          description: 'Filter by entities'
        },
        limit: {
          type: 'number',
          description: 'Maximum results to return',
          default: 10
        },
        verify_integrity: {
          type: 'boolean',
          description: 'Verify integrity of returned memories (detect tampering)',
          default: false
        }
      },
      required: ['query']
    }
  },
  {
    name: 'memory_briefing',
    description: 'Get a structured session briefing with key facts, commitments, and recent activity.',
    inputSchema: {
      type: 'object',
      properties: {
        context: {
          type: 'string',
          description: 'Context for the briefing (e.g., "morning standup")'
        },
        limit: {
          type: 'number',
          description: 'Number of recent memories to include',
          default: 10
        }
      }
    }
  },
  {
    name: 'memory_stats',
    description: 'Get vault statistics - memory counts by type, entity count, and graph edges.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'memory_entities',
    description: 'List all tracked entities with memory counts.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'memory_forget',
    description: 'Forget a memory (soft delete by default, hard delete with force flag).',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'string',
          description: 'Memory ID to forget'
        },
        hard: {
          type: 'boolean',
          description: 'Hard delete (permanent) vs soft delete',
          default: false
        }
      },
      required: ['id']
    }
  },
  {
    name: 'memory_procedure_create',
    description: 'Create a new procedure/workflow with steps.',
    inputSchema: {
      type: 'object',
      properties: {
        title: {
          type: 'string',
          description: 'Procedure title'
        },
        description: {
          type: 'string',
          description: 'Optional description'
        },
        steps: {
          type: 'array',
          items: { type: 'string' },
          description: 'Array of step descriptions'
        }
      },
      required: ['title', 'steps']
    }
  },
  {
    name: 'memory_procedure_feedback',
    description: 'Record success or failure for a procedure. Failures auto-create new versions.',
    inputSchema: {
      type: 'object',
      properties: {
        procedureId: {
          type: 'string',
          description: 'Procedure ID'
        },
        success: {
          type: 'boolean',
          description: 'Whether the procedure succeeded'
        },
        failedAtStep: {
          type: 'number',
          description: 'Step number that failed (if any)'
        },
        context: {
          type: 'string',
          description: 'Additional context about what happened'
        }
      },
      required: ['procedureId', 'success']
    }
  },
  {
    name: 'memory_procedure_list',
    description: 'List all procedures.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'memory_connect',
    description: 'Create a relationship between two memories in the knowledge graph.',
    inputSchema: {
      type: 'object',
      properties: {
        sourceId: {
          type: 'string',
          description: 'Source memory ID'
        },
        targetId: {
          type: 'string',
          description: 'Target memory ID'
        },
        relationship: {
          type: 'string',
          description: 'Relationship type (e.g., "related_to", "causes", "depends_on")'
        }
      },
      required: ['sourceId', 'targetId', 'relationship']
    }
  },
  {
    name: 'memory_neighbors',
    description: 'Get connected memories (graph neighbors) for a given memory.',
    inputSchema: {
      type: 'object',
      properties: {
        memoryId: {
          type: 'string',
          description: 'Memory ID'
        },
        depth: {
          type: 'number',
          description: 'Graph traversal depth',
          default: 1
        }
      },
      required: ['memoryId']
    }
  },
  {
    name: 'memory_consolidate',
    description: 'Run memory consolidation - distills episodes into facts, discovers entities, finds contradictions.',
    inputSchema: {
      type: 'object',
      properties: {
        batchSize: {
          type: 'number',
          description: 'Number of memories to process',
          default: 10
        }
      }
    }
  },
  // ========== AUDIT SYSTEM TOOLS ==========
  {
    name: 'memory_audit',
    description: 'Get audit trail for a memory or session - retrieve access logs, decision traces, and staleness info.',
    inputSchema: {
      type: 'object',
      properties: {
        memoryId: {
          type: 'string',
          description: 'Specific memory ID to get audit trail for'
        },
        sessionId: {
          type: 'string',
          description: 'Session ID to get audit trail for'
        },
        limit: {
          type: 'number',
          description: 'Maximum number of events to return',
          default: 50
        }
      }
    }
  },
  {
    name: 'memory_integrity',
    description: 'Verify integrity of stored memories - detect tampering, corruption, or hash mismatches.',
    inputSchema: {
      type: 'object',
      properties: {
        memoryId: {
          type: 'string',
          description: 'Specific memory ID to verify (optional - if omitted, generates full report)'
        },
        fullReport: {
          type: 'boolean',
          description: 'Generate full integrity report for all memories',
          default: false
        }
      }
    }
  },
  {
    name: 'memory_contradictions',
    description: 'List flagged contradictions for review - get unresolved content contradictions needing attention.',
    inputSchema: {
      type: 'object',
      properties: {
        memoryId: {
          type: 'string',
          description: 'Get contradictions for a specific memory'
        },
        unresolvedOnly: {
          type: 'boolean',
          description: 'Only return unresolved contradictions',
          default: true
        },
        limit: {
          type: 'number',
          description: 'Maximum contradictions to return',
          default: 20
        }
      }
    }
  },
  {
    name: 'access_patterns',
    description: 'Get access statistics for memories - retrieval stats, actor patterns, query performance.',
    inputSchema: {
      type: 'object',
      properties: {
        actor: {
          type: 'string',
          description: 'Filter by specific actor (agent/user ID)'
        },
        memoryId: {
          type: 'string',
          description: 'Get access patterns for a specific memory'
        },
        timeRangeHours: {
          type: 'number',
          description: 'Time range in hours for stats (default: 24)',
          default: 24
        }
      }
    }
  }
];

// Handle tool calls
async function handleToolCall(name: string, args: any): Promise<any> {
  switch (name) {
    case 'memory_remember': {
      const { content, type, title, context, sessionDate } = args;
      
      // Auto-route if no type specified
      let memoryType: MemoryType = type || 'semantic';
      if (!type) {
        const routing = await routeContent(content, context);
        if (routing.episodic) memoryType = 'episodic';
        else if (routing.procedural) memoryType = 'procedural';
        else memoryType = 'semantic';
      }
      
      // Parse sessionDate if provided (handles "1:56 pm on 8 May, 2023" format)
      let parsedSessionDate: Date | undefined;
      if (sessionDate) {
        // Try ISO format first
        const isoDate = new Date(sessionDate);
        if (!isNaN(isoDate.getTime())) {
          parsedSessionDate = isoDate;
        } else {
          // Try LOCOMO format: "1:56 pm on 8 May, 2023"
          const locomMatch = sessionDate.match(/(\d{1,2}):(\d{2})\s*(am|pm)?\s*on\s+(\d{1,2})\s+(\w+),?\s*(\d{4})/i);
          if (locomMatch) {
            const months = ['january', 'february', 'march', 'april', 'may', 'june', 
                           'july', 'august', 'september', 'october', 'november', 'december'];
            const month = months.indexOf(locomMatch[5].toLowerCase());
            const day = parseInt(locomMatch[4]);
            const year = parseInt(locomMatch[6]);
            if (month >= 0) {
              parsedSessionDate = new Date(year, month, day);
            }
          }
        }
      }
      
      const result = await store.remember(content, memoryType, { 
        title,
        sessionDate: parsedSessionDate
      });
      
      // Check if temporal resolution happened
      const hasResolved = (result as any).resolved_content !== null;
      
      // Audit: Log memory store operation
      const { auditWrappers: wrappers } = getAuditSystem();
      if (wrappers?.accessLog) {
        wrappers.accessLog.logStore(result.id, 'agent', undefined, {
          memory_type: result.type,
          has_title: !!title,
          temporal_resolved: hasResolved
        });
        
        // Initialize integrity record
        if (wrappers.integrity) {
          wrappers.integrity.initializeMemoryIntegrity(
            result.id, 
            result.content, 
            result.entities || []
          );
        }
      }
      
      return {
        success: true,
        id: result.id,
        type: result.type,
        message: `Memory stored as ${result.type}${hasResolved ? ' (temporal resolved)' : ''}`
      };
    }
    
    case 'memory_recall': {
      const { query, types, entities, limit, verify_integrity } = args;
      const startTime = Date.now();
      const memories = await store.recall(query, { types, entities, limit });
      const durationMs = Date.now() - startTime;
      
      // Audit: Log recall operation
      const { auditWrappers: wrappers, auditHelper: helper } = getAuditSystem();
      if (wrappers?.accessLog) {
        wrappers.accessLog.logRecall(
          'agent',
          query,
          memories.length,
          'hybrid', // Could be enhanced to detect actual path
          undefined,
          durationMs,
          memories.map(m => m.id)
        );
        
        // Log query metrics
        wrappers.accessLog.logQueryMetrics({
          query,
          retrieval_path: 'hybrid',
          result_count: memories.length,
          duration_ms: durationMs
        });
      }
      
      // Audit: Record retrieval decision trace
      if (helper) {
        helper.auditRecallSuccess(query, memories, {
          path_type: 'hybrid',
          duration_ms: durationMs
        });
      }
      
      // Optional: Verify integrity on recall
      let integrityResults: any = null;
      if (verify_integrity && wrappers?.integrity) {
        integrityResults = memories.map(m => {
          const entities = typeof m.entities === 'string' ? JSON.parse(m.entities) : m.entities;
          const result = wrappers.integrity!.verifyMemoryIntegrity(m.id, m.content, entities);
          return {
            memory_id: m.id,
            status: result.status,
            verified: result.status === 'valid'
          };
        });
      }
      
      return {
        count: memories.length,
        memories: memories.map(m => ({
          id: m.id,
          type: m.type,
          content: m.content,
          title: m.title,
          summary: m.summary,
          entities: m.entities,
          topics: m.topics,
          salience: m.salience,
          created_at: m.created_at
        })),
        retrieval_time_ms: durationMs,
        integrity_results: integrityResults
      };
    }
    
    case 'memory_briefing': {
      const { context, limit } = args;
      const recentMemories = await store.recall(context || '', { limit: limit || 10 });
      
      // Separate by type
      const keyFacts = recentMemories.filter(m => m.type === 'semantic');
      const recentActivity = recentMemories.filter(m => m.type === 'episodic');
      const procedures = recentMemories.filter(m => m.type === 'procedural');
      
      // P7.3: Session Priming - Get stale-but-important entities
      const priming = await cohesionQuery(
        store.getEntityStore(),
        store.getRelationshipStore(),
        async (q: string, opts?: any) => store.recall(q, opts),
        { minMentions: 3, staleHours: 48, maxEntities: 5, memoriesPerEntity: 2 }
      );
      
      // Generate summary
      const summary = `Session context: ${context || 'general'}. Found ${keyFacts.length} key facts, ${recentActivity.length} recent events, ${procedures.length} relevant procedures.`;
      
      return {
        summary,
        keyFacts: keyFacts.map(f => ({ content: f.content, salience: f.salience })),
        recentActivity: recentActivity.map(a => ({ content: a.content, timestamp: a.created_at })),
        relevantProcedures: procedures.map(p => ({ title: p.title, summary: p.summary })),
        // P7.3: Active Context - Stale but important entities
        activeContext: {
          primedMemories: priming.primedMemories.map(m => ({
            content: m.content,
            entity: m.entities[0],
            salience: m.salience
          })),
          staleEntities: priming.staleEntities.map(e => ({
            name: e.entity.name,
            type: e.entity.type,
            mentions: e.entity.mentions,
            hoursSinceMention: Math.round(e.hoursSinceMention)
          })),
          summary: priming.summary
        }
      };
    }
    
    case 'memory_stats': {
      return store.getStats();
    }
    
    case 'memory_entities': {
      const entities = store.getEntities();
      return { count: entities.length, entities };
    }
    
    case 'memory_forget': {
      const { id, hard } = args;
      const deleted = store.forget(id, hard);
      return { success: deleted, id, hard };
    }
    
    case 'memory_procedure_create': {
      const { title, description, steps } = args;
      const procedure = await store.createProcedure(title, steps, description);
      return {
        success: true,
        id: procedure.id,
        version: procedure.version,
        message: `Procedure "${title}" created (v${procedure.version})`
      };
    }
    
    case 'memory_procedure_feedback': {
      const { procedureId, success, failedAtStep, context } = args;
      const procedure = await store.procedureFeedback(procedureId, success, failedAtStep, context);
      return {
        success: true,
        id: procedure.id,
        version: procedure.version,
        success_count: procedure.success_count,
        failure_count: procedure.failure_count,
        is_reliable: procedure.is_reliable,
        message: success 
          ? `Success recorded. Total: ${procedure.success_count}. ${procedure.is_reliable ? 'Promoted to reliable!' : ''}`
          : `Failure recorded. New version v${procedure.version} created.`
      };
    }
    
    case 'memory_procedure_list': {
      const procedures = store.getAllProcedures();
      return {
        count: procedures.length,
        procedures: procedures.map(p => ({
          id: p.id,
          title: p.title,
          description: p.description,
          version: p.version,
          success_count: p.success_count,
          failure_count: p.failure_count,
          is_reliable: p.is_reliable,
          steps: p.steps.map(s => s.description),
          created_at: p.created_at,
          updated_at: p.updated_at
        }))
      };
    }
    
    case 'memory_connect': {
      const { sourceId, targetId, relationship } = args;
      const edge = store.connect(sourceId, targetId, relationship);
      return { success: true, edge };
    }
    
    case 'memory_neighbors': {
      const { memoryId, depth } = args;
      const neighbors = store.getNeighbors(memoryId, depth);
      return {
        count: neighbors.length,
        memories: neighbors.map(m => ({
          id: m.id,
          type: m.type,
          content: m.content,
          title: m.title
        }))
      };
    }
    
    case 'memory_consolidate': {
      const { batchSize } = args;
      const result = await consolidate(store, { batchSize });
      return {
        success: true,
        ...result
      };
    }
    
    // ========== AUDIT SYSTEM TOOL HANDLERS ==========
    
    case 'memory_audit': {
      const { memoryId, sessionId, limit } = args;
      const { auditHelper: helper } = getAuditSystem();
      
      if (!helper) {
        return { error: 'Audit system not initialized' };
      }
      
      const events: any[] = [];
      
      if (memoryId) {
        // Get events for specific memory
        const staleness = helper.getRetrievalStats(7);
        const memsNeedingVerification = helper.getMemoriesNeedingVerification();
        
        // Get staleness info for this memory
        const db = (store as any).db;
        if (db) {
          const stalenessStmt = db.prepare('SELECT * FROM staleness_tracker WHERE memory_id = ?');
          const stalenessRow = stalenessStmt.get(memoryId) as any;
          
          events.push({
            type: 'staleness',
            memory_id: memoryId,
            staleness_score: stalenessRow?.staleness_score || 0,
            requires_verification: stalenessRow?.requires_verification || false
          });
        }
        
        return {
          memory_id: memoryId,
          staleness_events: events,
          needs_verification: memsNeedingVerification.includes(memoryId),
          retrieval_stats: staleness
        };
      } else if (sessionId) {
        // Get session audit trail
        const { auditWrappers: wrappers } = getAuditSystem();
        if (wrappers?.accessLog) {
          const trail = wrappers.accessLog.getSessionAuditTrail(sessionId);
          return {
            session_id: sessionId,
            audit_trail: trail.map(e => ({
              action: e.action,
              actor: e.actor,
              memory_id: e.memory_id,
              query: e.query,
              result_count: e.result_count,
              duration_ms: e.duration_ms,
              created_at: e.created_at
            })),
            total_events: trail.length
          };
        }
      }
      
      // Default: return general retrieval stats
      const stats = helper.getRetrievalStats(7);
      const needingVerification = helper.getMemoriesNeedingVerification();
      
      return {
        retrieval_stats: stats,
        memories_needing_verification: needingVerification,
        total_needing_verification: needingVerification.length
      };
    }
    
    case 'memory_integrity': {
      const { memoryId, fullReport } = args;
      const { integrityStore: integrity } = getAuditSystem();
      
      if (!integrity) {
        return { error: 'Integrity store not initialized' };
      }
      
      if (memoryId) {
        // Verify specific memory
        const memory = store.getMemory(memoryId);
        if (!memory) {
          return { error: 'Memory not found', memory_id: memoryId };
        }
        
        const entities = typeof memory.entities === 'string' 
          ? JSON.parse(memory.entities) 
          : memory.entities;
        
        const result = integrity.verifyMemoryIntegrity(memoryId, memory.content, entities);
        
        // Get verification history
        const history = integrity.getVerificationHistory(memoryId, 10);
        
        return {
          memory_id: memoryId,
          status: result.status,
          stored_hash: result.stored_hash,
          computed_hash: result.computed_hash,
          error: result.error,
          verification_history: history
        };
      }
      
      if (fullReport) {
        // Generate full integrity report
        const getMemories = () => {
          const db = (store as any).db;
          if (!db) return [];
          return db.prepare(`
            SELECT id, content, entities FROM memories
            WHERE deleted_at IS NULL
          `).all() as any[];
        };
        
        const report = integrity.generateIntegrityReport(getMemories);
        return {
          report: {
            generated_at: report.generated_at,
            total_memories: report.total_memories,
            verified_count: report.verified_count,
            invalid_count: report.invalid_count,
            missing_hash_count: report.missing_hash_count,
            by_status: report.by_status,
            corrupted_memories: report.corrupted_memories,
            verification_time_ms: report.verification_time_ms
          }
        };
      }
      
      // Default: return invalid memories count
      const invalidMemories = integrity.getInvalidMemories();
      return {
        invalid_count: invalidMemories.length,
        invalid_memories: invalidMemories
      };
    }
    
    case 'memory_contradictions': {
      const { memoryId, unresolvedOnly, limit } = args;
      const { contradictionStore: contradictions } = getAuditSystem();
      
      if (!contradictions) {
        return { error: 'Contradiction store not initialized' };
      }
      
      let resultContradictions: MemoryContradiction[] = [];
      
      if (memoryId) {
        // Get contradictions for specific memory
        resultContradictions = contradictions.getContradictionsForMemory(memoryId);
      } else if (unresolvedOnly) {
        // Get all unresolved
        resultContradictions = contradictions.getUnresolvedContradictions(limit || 20);
      } else {
        // Get stats only
        const stats = contradictions.getStats();
        return {
          stats: {
            total: stats.total,
            unresolved: stats.unresolved,
            auto_resolved: stats.auto_resolved,
            human_resolved: stats.human_resolved,
            ignored: stats.ignored,
            avg_contradiction_score: stats.avg_contradiction_score
          }
        };
      }
      
      return {
        count: resultContradictions.length,
        contradictions: resultContradictions.map(c => ({
          id: c.id,
          memory_a_id: c.memory_a_id,
          memory_b_id: c.memory_b_id,
          entity: c.entity,
          value_a: c.value_a,
          value_b: c.value_b,
          similarity_score: c.similarity_score,
          contradiction_score: c.contradiction_score,
          resolution_status: c.resolution_status,
          created_at: c.created_at
        }))
      };
    }
    
    case 'access_patterns': {
      const { actor, memoryId, timeRangeHours } = args;
      const { auditWrappers: wrappers } = getAuditSystem();
      
      if (!wrappers?.accessLog) {
        return { error: 'Access log not initialized' };
      }
      
      const hours = timeRangeHours || 24;
      
      if (memoryId) {
        // Get access logs for specific memory
        const logs = wrappers.accessLog.getAccessLogsForMemory(memoryId, 50);
        return {
          memory_id: memoryId,
          access_count: logs.length,
          recent_access: logs.map(l => ({
            actor: l.actor,
            action: l.action,
            query: l.query,
            result_count: l.result_count,
            created_at: l.created_at
          }))
        };
      }
      
      if (actor) {
        // Get access pattern for actor
        const pattern = wrappers.accessLog.getAccessPattern(actor, hours);
        const logs = wrappers.accessLog.getAccessLogsByActor(actor, 20);
        
        return {
          actor,
          time_range_hours: hours,
          total_actions: pattern.count,
          action_breakdown: logs.reduce((acc: Record<string, number>, l) => {
            acc[l.action] = (acc[l.action] || 0) + 1;
            return acc;
          }, {}),
          recent_actions: logs.map(l => ({
            action: l.action,
            memory_id: l.memory_id,
            query: l.query,
            created_at: l.created_at
          }))
        };
      }
      
      // Default: get overall query stats and most active
      const queryStats = wrappers.accessLog.getQueryStats(undefined, hours);
      const mostActive = wrappers.accessLog.getMostActiveActors(10);
      const mostAccessed = wrappers.accessLog.getMostAccessedMemories(10);
      const recentQueries = wrappers.accessLog.getRecentQueries(10);
      
      return {
        time_range_hours: hours,
        query_stats: {
          avg_duration_ms: Math.round(queryStats.avg_duration_ms),
          total_queries: queryStats.total_queries,
          avg_results: Math.round(queryStats.avg_results * 10) / 10,
          p95_duration_ms: queryStats.p95_duration_ms
        },
        most_active_actors: mostActive,
        most_accessed_memories: mostAccessed,
        recent_queries: recentQueries.map(q => ({
          query: q.query,
          retrieval_path: q.retrieval_path,
          result_count: q.result_count,
          duration_ms: q.duration_ms,
          timestamp: q.timestamp
        }))
      };
    }
      throw new Error(`Unknown tool: ${name}`);
  }
}

// Register handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    const result = await handleToolCall(name, args);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }
      ]
    };
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ error: error.message }, null, 2)
        }
      ],
      isError: true
    };
  }
});

// Start server
async function main() {
  console.log('🧠 OpenClaw Memory System v1 - MCP Server');
  console.log('Starting server...');
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.log('✅ MCP Server ready');
}

main().catch(console.error);
