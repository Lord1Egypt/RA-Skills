/**
 * Muninn v2 - MCP Server
 * Provides memory tools to OpenClaw agents
 * 
 * Key differences from v1:
 * - Fact-based storage (not session-based)
 * - Bi-temporal model (valid_from/valid_until + created_at/invalidated_at)
 * - Structured retrieval (facts → graph → events → semantic)
 * - Profile abstraction (static + dynamic facts)
 * - Auto-forgetting (temporal facts expire)
 * - Token budget retrieval
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { Muninn } from './index.js';
import type { Fact, Event } from './types.js';
import { buildProfile, formatProfile, getProfile } from './profile/index.js';
import { 
  retrieveWithBudget, 
  formatForContext,
  memoryBriefingWithBudget 
} from './retrieval/budget.js';
import {
  detectTemporalFact,
  classifyMemoryType,
  runForgettingCycle,
  getExpiringFacts
} from './forgetting/index.js';

// Initialize Muninn v2
const dbPath = process.env.MUNINN_DB_PATH || '/tmp/muninn-v2.db';
const muninn = new Muninn(dbPath);

// Server instance
const server = new Server(
  {
    name: 'muninn-v2',
    version: '2.0.0',
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
    description: 'Store a memory with automatic fact extraction. Extracts entities, facts, events, and relationships. Supports temporal expressions (e.g., "yesterday", "last week") with sessionDate for resolution.',
    inputSchema: {
      type: 'object',
      properties: {
        content: {
          type: 'string',
          description: 'The content to remember'
        },
        source: {
          type: 'string',
          description: 'Source of the memory (e.g., "conversation", "document")'
        },
        actor: {
          type: 'string',
          description: 'Who said/wrote this content'
        },
        sessionDate: {
          type: 'string',
          description: 'Reference date for temporal resolution (ISO format: YYYY-MM-DD)'
        }
      },
      required: ['content']
    }
  },
  {
    name: 'memory_recall',
    description: 'Retrieve memories using structured queries. Priority: facts → graph traversal → events → semantic. Use for questions like "What is X?", "How did Y change?", "Who does Z work with?"',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Natural language query'
        },
        limit: {
          type: 'number',
          description: 'Maximum results',
          default: 10
        },
        maxTokens: {
          type: 'number',
          description: 'Maximum tokens to return (budget-aware retrieval)',
          default: 500
        }
      },
      required: ['query']
    }
  },
  {
    name: 'memory_briefing',
    description: 'Get a structured session briefing with static profile, dynamic context, and relevant memories. Token-efficient (100-200 tokens vs 5000+ for raw memories).',
    inputSchema: {
      type: 'object',
      properties: {
        context: {
          type: 'string',
          description: 'Context for the briefing (e.g., "morning standup", "project review")'
        },
        maxTokens: {
          type: 'number',
          description: 'Maximum tokens for briefing (default: 500)',
          default: 500
        }
      }
    }
  },
  {
    name: 'memory_profile',
    description: 'Get user profile (static facts + dynamic context). Fast (~50ms) for system prompt injection. Returns distilled facts, not raw memories.',
    inputSchema: {
      type: 'object',
      properties: {
        maxStaticFacts: {
          type: 'number',
          description: 'Maximum static facts to return (default: 10)',
          default: 10
        },
        maxDynamicFacts: {
          type: 'number',
          description: 'Maximum dynamic facts to return (default: 5)',
          default: 5
        }
      }
    }
  },
  {
    name: 'memory_forget',
    description: 'Manually forget expired facts or decay old episodes. Also shows facts expiring soon.',
    inputSchema: {
      type: 'object',
      properties: {
        action: {
          type: 'string',
          enum: ['expire', 'decay', 'list'],
          description: 'Action: expire (remove expired), decay (reduce old episode strength), list (show expiring)'
        }
      }
    }
  },
  {
    name: 'memory_evolution',
    description: 'Get how an entity changed over time. Returns all state transitions for an entity.',
    inputSchema: {
      type: 'object',
      properties: {
        entity: {
          type: 'string',
          description: 'Entity name to query'
        },
        from: {
          type: 'string',
          description: 'Start date (ISO format, optional)'
        },
        to: {
          type: 'string',
          description: 'End date (ISO format, optional)'
        }
      },
      required: ['entity']
    }
  },
  {
    name: 'memory_path',
    description: 'Find relationship path between two entities. Returns multi-hop connections.',
    inputSchema: {
      type: 'object',
      properties: {
        from: {
          type: 'string',
          description: 'Starting entity'
        },
        to: {
          type: 'string',
          description: 'Target entity'
        },
        maxDepth: {
          type: 'number',
          description: 'Maximum path length',
          default: 3
        }
      },
      required: ['from', 'to']
    }
  },
  {
    name: 'memory_contradictions',
    description: 'Get unresolved contradictions in memory. Returns conflicting facts for resolution.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'memory_stats',
    description: 'Get memory statistics - entity count, fact count, relationship count, event count.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }
];

// Handle tool calls
async function handleToolCall(name: string, args: any): Promise<any> {
  switch (name) {
    case 'memory_remember': {
      const { content, source, actor, sessionDate } = args;
      
      // Detect temporal fact
      const expiresAt = detectTemporalFact(content);
      const memoryType = classifyMemoryType(content);
      
      const result = await muninn.remember(content, {
        source,
        actor,
        sessionDate,
        memoryType,
        expiresAt
      });
      
      return {
        success: true,
        episodeId: result.episodeId,
        factsCreated: result.factsCreated,
        entitiesCreated: result.entitiesCreated,
        eventsCreated: result.eventsCreated,
        contradictions: result.contradictions,
        memoryType,
        expiresAt: expiresAt?.toISOString() || null,
        message: `Stored ${result.factsCreated} facts (${memoryType}${expiresAt ? ', expires ' + expiresAt.toDateString() : ''})`
      };
    }
    
    case 'memory_recall': {
      const { query, limit, maxTokens } = args;
      
      if (maxTokens) {
        // Budget-aware retrieval
        const db = muninn['db'];
        const result = await retrieveWithBudget(db, query, { maxTokens });
        return {
          source: 'budget',
          profile: result.profile,
          memories: result.memories,
          tokensUsed: result.tokensUsed,
          tokensRemaining: result.tokensRemaining,
          formatted: formatForContext(result)
        };
      }
      
      // Standard retrieval
      const result = await muninn.recall(query, { limit: limit || 10 });
      
      return {
        source: result.source,
        facts: result.facts?.map(formatFact),
        path: result.path?.map(p => ({
          entity: p.entity,
          relationship: p.relationship,
          relatedEntity: p.relatedEntity,
          depth: p.depth
        })),
        events: result.events?.map(formatEvent),
        memories: result.memories
      };
    }
    
    case 'memory_briefing': {
      const { context, maxTokens } = args;
      const db = muninn['db'];
      
      // Use budget-aware briefing
      const briefing = await memoryBriefingWithBudget(db, context || 'session start', maxTokens || 500);
      
      return {
        context: context || 'session start',
        briefing,
        tokenCount: Math.ceil(briefing.length / 4)
      };
    }
    
    case 'memory_profile': {
      const { maxStaticFacts, maxDynamicFacts } = args;
      const db = muninn['db'];
      
      const profile = await getProfile(db, {
        maxStaticFacts: maxStaticFacts || 10,
        maxDynamicFacts: maxDynamicFacts || 5
      });
      
      return {
        static: profile.static,
        dynamic: profile.dynamic,
        tokenCount: profile.tokenCount,
        formatted: formatProfile(profile)
      };
    }
    
    case 'memory_forget': {
      const { action } = args;
      const db = muninn['db'];
      
      if (action === 'list') {
        const expiring = await getExpiringFacts(db, 7);
        return {
          action: 'list',
          expiringCount: expiring.length,
          facts: expiring.map(f => ({
            content: f.content,
            expiresAt: f.expires_at?.toISOString(),
            type: f.memory_type
          }))
        };
      }
      
      if (action === 'expire' || action === 'decay') {
        const result = await runForgettingCycle(db);
        return {
          action,
          ...result,
          message: `Forgot ${result.totalForgotten} facts (${result.expired} expired, ${result.decayed} decayed)`
        };
      }
      
      return { error: 'Invalid action. Use: expire, decay, or list' };
    }
    
    case 'memory_evolution': {
      const { entity, from, to } = args;
      
      const fromDate = from ? new Date(from) : undefined;
      const toDate = to ? new Date(to) : undefined;
      
      const events = await muninn.getEvolution(entity, fromDate, toDate);
      
      return {
        entity,
        events: events.map(formatEvent),
        count: events.length
      };
    }
    
    case 'memory_path': {
      const { from, to, maxDepth } = args;
      
      const result = await muninn.traverseGraph(from, maxDepth || 3);
      const pathResult = await muninn.recall(`How is ${from} connected to ${to}?`);
      
      return {
        from,
        to,
        found: pathResult.source === 'graph',
        path: pathResult.path
      };
    }
    
    case 'memory_contradictions': {
      const contradictions = await muninn.getContradictions();
      
      return {
        count: contradictions.length,
        contradictions: contradictions.map(c => ({
          id: c.id,
          type: c.type,
          severity: c.severity,
          factA: formatFact(c.factA),
          factB: formatFact(c.factB),
          reason: c.reason
        }))
      };
    }
    
    case 'memory_stats': {
      // Get stats from database
      const db = muninn['db'];
      const stats = db.getStats();
      
      return {
        entities: stats.entityCount,
        facts: stats.factCount,
        events: stats.eventCount,
        relationships: stats.relationshipCount,
        contradictions: stats.contradictionCount
      };
    }
    
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

// Helper functions
function formatFact(fact: Fact): any {
  return {
    subject: fact.subjectEntityId,
    predicate: fact.predicate,
    object: fact.objectEntityId || fact.objectValue,
    confidence: fact.confidence,
    validFrom: fact.validFrom,
    validUntil: fact.validUntil,
    evidence: fact.evidence
  };
}

function formatEvent(event: Event): any {
  return {
    entity: event.entityId,
    attribute: event.attribute,
    oldValue: event.oldValue,
    newValue: event.newValue,
    cause: event.cause,
    occurredAt: event.occurredAt
  };
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
  console.log('🧠 Muninn v2 - MCP Server');
  console.log('Starting server...');
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.log('✅ MCP Server ready');
}

main().catch(console.error);