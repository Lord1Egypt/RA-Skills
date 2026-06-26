"use strict";
/**
 * OpenClaw Memory System - MCP Server
 * Provides memory tools to OpenClaw agents
 */
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var index_js_1 = require("@modelcontextprotocol/sdk/server/index.js");
var stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
var types_js_1 = require("@modelcontextprotocol/sdk/types.js");
var index_js_2 = require("../storage/index.js");
var index_js_3 = require("../extractors/index.js");
var index_js_4 = require("../consolidation/index.js");
var session_priming_js_1 = require("../retrieval/session-priming.js");
// Initialize store
var store = new index_js_2.MemoryStore();
// Server instance
var server = new index_js_1.Server({
    name: 'openclaw-memory',
    version: '1.0.0',
}, {
    capabilities: {
        tools: {},
    },
});
// Tool definitions
var tools = [
    {
        name: 'memory_remember',
        description: 'Store a memory with auto-extraction of entities and topics. Automatically classifies as episodic, semantic, or procedural.',
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
    }
];
// Handle tool calls
function handleToolCall(name, args) {
    return __awaiter(this, void 0, void 0, function () {
        var _a, content, type, title, context, memoryType, routing, result, query, types, entities, limit, memories, context, limit, recentMemories, keyFacts, recentActivity, procedures, priming, summary, entities, id, hard, deleted, title, description, steps, procedure, procedureId, success, failedAtStep, context, procedure, procedures, sourceId, targetId, relationship, edge, memoryId, depth, neighbors, batchSize, result;
        var _this = this;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    _a = name;
                    switch (_a) {
                        case 'memory_remember': return [3 /*break*/, 1];
                        case 'memory_recall': return [3 /*break*/, 5];
                        case 'memory_briefing': return [3 /*break*/, 7];
                        case 'memory_stats': return [3 /*break*/, 10];
                        case 'memory_entities': return [3 /*break*/, 11];
                        case 'memory_forget': return [3 /*break*/, 12];
                        case 'memory_procedure_create': return [3 /*break*/, 13];
                        case 'memory_procedure_feedback': return [3 /*break*/, 15];
                        case 'memory_procedure_list': return [3 /*break*/, 17];
                        case 'memory_connect': return [3 /*break*/, 18];
                        case 'memory_neighbors': return [3 /*break*/, 19];
                        case 'memory_consolidate': return [3 /*break*/, 20];
                    }
                    return [3 /*break*/, 22];
                case 1:
                    content = args.content, type = args.type, title = args.title, context = args.context;
                    memoryType = type || 'semantic';
                    if (!!type) return [3 /*break*/, 3];
                    return [4 /*yield*/, (0, index_js_3.routeContent)(content, context)];
                case 2:
                    routing = _b.sent();
                    if (routing.episodic)
                        memoryType = 'episodic';
                    else if (routing.procedural)
                        memoryType = 'procedural';
                    else
                        memoryType = 'semantic';
                    _b.label = 3;
                case 3: return [4 /*yield*/, store.remember(content, memoryType, { title: title })];
                case 4:
                    result = _b.sent();
                    return [2 /*return*/, {
                            success: true,
                            id: result.id,
                            type: result.type,
                            message: "Memory stored as ".concat(result.type)
                        }];
                case 5:
                    query = args.query, types = args.types, entities = args.entities, limit = args.limit;
                    return [4 /*yield*/, store.recall(query, { types: types, entities: entities, limit: limit })];
                case 6:
                    memories = _b.sent();
                    return [2 /*return*/, {
                            count: memories.length,
                            memories: memories.map(function (m) { return ({
                                id: m.id,
                                type: m.type,
                                content: m.content,
                                title: m.title,
                                summary: m.summary,
                                entities: m.entities,
                                topics: m.topics,
                                salience: m.salience,
                                created_at: m.created_at
                            }); })
                        }];
                case 7:
                    context = args.context, limit = args.limit;
                    return [4 /*yield*/, store.recall(context || '', { limit: limit || 10 })];
                case 8:
                    recentMemories = _b.sent();
                    keyFacts = recentMemories.filter(function (m) { return m.type === 'semantic'; });
                    recentActivity = recentMemories.filter(function (m) { return m.type === 'episodic'; });
                    procedures = recentMemories.filter(function (m) { return m.type === 'procedural'; });
                    return [4 /*yield*/, (0, session_priming_js_1.cohesionQuery)(store.getEntityStore(), store.getRelationshipStore(), function (q, opts) { return __awaiter(_this, void 0, void 0, function () { return __generator(this, function (_a) {
                            return [2 /*return*/, store.recall(q, opts)];
                        }); }); }, { minMentions: 3, staleHours: 48, maxEntities: 5, memoriesPerEntity: 2 })];
                case 9:
                    priming = _b.sent();
                    summary = "Session context: ".concat(context || 'general', ". Found ").concat(keyFacts.length, " key facts, ").concat(recentActivity.length, " recent events, ").concat(procedures.length, " relevant procedures.");
                    return [2 /*return*/, {
                            summary: summary,
                            keyFacts: keyFacts.map(function (f) { return ({ content: f.content, salience: f.salience }); }),
                            recentActivity: recentActivity.map(function (a) { return ({ content: a.content, timestamp: a.created_at }); }),
                            relevantProcedures: procedures.map(function (p) { return ({ title: p.title, summary: p.summary }); }),
                            // P7.3: Active Context - Stale but important entities
                            activeContext: {
                                primedMemories: priming.primedMemories.map(function (m) { return ({
                                    content: m.content,
                                    entity: m.entities[0],
                                    salience: m.salience
                                }); }),
                                staleEntities: priming.staleEntities.map(function (e) { return ({
                                    name: e.entity.name,
                                    type: e.entity.type,
                                    mentions: e.entity.mentions,
                                    hoursSinceMention: Math.round(e.hoursSinceMention)
                                }); }),
                                summary: priming.summary
                            }
                        }];
                case 10:
                    {
                        return [2 /*return*/, store.getStats()];
                    }
                    _b.label = 11;
                case 11:
                    {
                        entities = store.getEntities();
                        return [2 /*return*/, { count: entities.length, entities: entities }];
                    }
                    _b.label = 12;
                case 12:
                    {
                        id = args.id, hard = args.hard;
                        deleted = store.forget(id, hard);
                        return [2 /*return*/, { success: deleted, id: id, hard: hard }];
                    }
                    _b.label = 13;
                case 13:
                    title = args.title, description = args.description, steps = args.steps;
                    return [4 /*yield*/, store.createProcedure(title, steps, description)];
                case 14:
                    procedure = _b.sent();
                    return [2 /*return*/, {
                            success: true,
                            id: procedure.id,
                            version: procedure.version,
                            message: "Procedure \"".concat(title, "\" created (v").concat(procedure.version, ")")
                        }];
                case 15:
                    procedureId = args.procedureId, success = args.success, failedAtStep = args.failedAtStep, context = args.context;
                    return [4 /*yield*/, store.procedureFeedback(procedureId, success, failedAtStep, context)];
                case 16:
                    procedure = _b.sent();
                    return [2 /*return*/, {
                            success: true,
                            id: procedure.id,
                            version: procedure.version,
                            success_count: procedure.success_count,
                            failure_count: procedure.failure_count,
                            is_reliable: procedure.is_reliable,
                            message: success
                                ? "Success recorded. Total: ".concat(procedure.success_count, ". ").concat(procedure.is_reliable ? 'Promoted to reliable!' : '')
                                : "Failure recorded. New version v".concat(procedure.version, " created.")
                        }];
                case 17:
                    {
                        procedures = store.getAllProcedures();
                        return [2 /*return*/, {
                                count: procedures.length,
                                procedures: procedures.map(function (p) { return ({
                                    id: p.id,
                                    title: p.title,
                                    description: p.description,
                                    version: p.version,
                                    success_count: p.success_count,
                                    failure_count: p.failure_count,
                                    is_reliable: p.is_reliable,
                                    steps: p.steps.map(function (s) { return s.description; }),
                                    created_at: p.created_at,
                                    updated_at: p.updated_at
                                }); })
                            }];
                    }
                    _b.label = 18;
                case 18:
                    {
                        sourceId = args.sourceId, targetId = args.targetId, relationship = args.relationship;
                        edge = store.connect(sourceId, targetId, relationship);
                        return [2 /*return*/, { success: true, edge: edge }];
                    }
                    _b.label = 19;
                case 19:
                    {
                        memoryId = args.memoryId, depth = args.depth;
                        neighbors = store.getNeighbors(memoryId, depth);
                        return [2 /*return*/, {
                                count: neighbors.length,
                                memories: neighbors.map(function (m) { return ({
                                    id: m.id,
                                    type: m.type,
                                    content: m.content,
                                    title: m.title
                                }); })
                            }];
                    }
                    _b.label = 20;
                case 20:
                    batchSize = args.batchSize;
                    return [4 /*yield*/, (0, index_js_4.consolidate)(store, { batchSize: batchSize })];
                case 21:
                    result = _b.sent();
                    return [2 /*return*/, __assign({ success: true }, result)];
                case 22: throw new Error("Unknown tool: ".concat(name));
            }
        });
    });
}
// Register handlers
server.setRequestHandler(types_js_1.ListToolsRequestSchema, function () { return __awaiter(void 0, void 0, void 0, function () {
    return __generator(this, function (_a) {
        return [2 /*return*/, { tools: tools }];
    });
}); });
server.setRequestHandler(types_js_1.CallToolRequestSchema, function (request) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, name, args, result, error_1;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = request.params, name = _a.name, args = _a.arguments;
                _b.label = 1;
            case 1:
                _b.trys.push([1, 3, , 4]);
                return [4 /*yield*/, handleToolCall(name, args)];
            case 2:
                result = _b.sent();
                return [2 /*return*/, {
                        content: [
                            {
                                type: 'text',
                                text: JSON.stringify(result, null, 2)
                            }
                        ]
                    }];
            case 3:
                error_1 = _b.sent();
                return [2 /*return*/, {
                        content: [
                            {
                                type: 'text',
                                text: JSON.stringify({ error: error_1.message }, null, 2)
                            }
                        ],
                        isError: true
                    }];
            case 4: return [2 /*return*/];
        }
    });
}); });
// Start server
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var transport;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log('🧠 OpenClaw Memory System v1 - MCP Server');
                    console.log('Starting server...');
                    transport = new stdio_js_1.StdioServerTransport();
                    return [4 /*yield*/, server.connect(transport)];
                case 1:
                    _a.sent();
                    console.log('✅ MCP Server ready');
                    return [2 /*return*/];
            }
        });
    });
}
main().catch(console.error);
