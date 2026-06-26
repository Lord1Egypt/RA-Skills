#!/usr/bin/env node
/**
 * Novyx Memory v3.0.0 — Full Core Coverage for OpenClaw
 *
 * 60+ commands covering all Novyx Core capabilities:
 * Memory, Drafts, Knowledge Graph, Spaces, Replay, Rollback,
 * Audit, Cortex, Eval, Tracing, Control, Links, Dashboard.
 *
 * Handles rate limits (429) and forbidden (403) gracefully.
 */

const axios = require('axios');
require('dotenv').config();

class NovyxMemory {
  constructor(config = {}) {
    this.apiKey = config.apiKey || process.env.NOVYX_API_KEY;
    this.apiUrl = config.apiUrl || process.env.NOVYX_API_URL || 'https://novyx-ram-api.fly.dev';
    this.autoSave = config.autoSave !== false;
    this.autoRecall = config.autoRecall !== false;
    this.recallLimit = config.recallLimit || 5;

    // Session write log for !undo (transient — resets on restart)
    this._writeLog = [];

    if (!this.apiKey) {
      console.warn('[NovyxMemory] No API key. Get a free one at https://novyxlabs.com (5,000 memories, no credit card)');
    }

    this.commands = [
      // Memory basics
      { trigger: '!remember', handler: this.handleRemember.bind(this) },
      { trigger: '!search', handler: this.handleSearch.bind(this) },
      { trigger: '!list', handler: this.handleList.bind(this) },
      { trigger: '!forget', handler: this.handleForget.bind(this) },
      { trigger: '!undo', handler: this.handleUndo.bind(this) },
      { trigger: '!supersede', handler: this.handleSupersede.bind(this) },

      // Drafts
      { trigger: '!draft-diff', handler: this.handleDraftDiff.bind(this) },
      { trigger: '!drafts', handler: this.handleDrafts.bind(this) },
      { trigger: '!draft', handler: this.handleDraft.bind(this) },
      { trigger: '!merge-draft', handler: this.handleMergeDraft.bind(this) },
      { trigger: '!reject-draft', handler: this.handleRejectDraft.bind(this) },
      { trigger: '!merge-branch', handler: this.handleMergeBranch.bind(this) },
      { trigger: '!reject-branch', handler: this.handleRejectBranch.bind(this) },
      { trigger: '!branch', handler: this.handleBranch.bind(this) },

      // Links
      { trigger: '!unlink', handler: this.handleUnlink.bind(this) },
      { trigger: '!links', handler: this.handleLinks.bind(this) },
      { trigger: '!link', handler: this.handleLink.bind(this) },

      // Knowledge graph
      { trigger: '!triples', handler: this.handleTriples.bind(this) },
      { trigger: '!triple', handler: this.handleTriple.bind(this) },
      { trigger: '!entities', handler: this.handleEntities.bind(this) },
      { trigger: '!entity', handler: this.handleEntity.bind(this) },
      { trigger: '!del-triple', handler: this.handleDelTriple.bind(this) },
      { trigger: '!del-entity', handler: this.handleDelEntity.bind(this) },
      { trigger: '!graph', handler: this.handleGraph.bind(this) },

      // Spaces
      { trigger: '!space-memories', handler: this.handleSpaceMemories.bind(this) },
      { trigger: '!spaces', handler: this.handleSpaces.bind(this) },
      { trigger: '!space', handler: this.handleSpace.bind(this) },
      { trigger: '!update-space', handler: this.handleUpdateSpace.bind(this) },
      { trigger: '!del-space', handler: this.handleDelSpace.bind(this) },
      { trigger: '!share', handler: this.handleShare.bind(this) },
      { trigger: '!shared', handler: this.handleShared.bind(this) },
      { trigger: '!accept', handler: this.handleAccept.bind(this) },
      { trigger: '!revoke', handler: this.handleRevoke.bind(this) },

      // Replay
      { trigger: '!timeline', handler: this.handleTimeline.bind(this) },
      { trigger: '!snapshot', handler: this.handleSnapshot.bind(this) },
      { trigger: '!lifecycle', handler: this.handleLifecycle.bind(this) },
      { trigger: '!replay-diff', handler: this.handleReplayDiff.bind(this) },
      { trigger: '!replay-drift', handler: this.handleReplayDrift.bind(this) },
      { trigger: '!replay', handler: this.handleReplay.bind(this) },
      { trigger: '!recall-at', handler: this.handleRecallAt.bind(this) },

      // Audit & rollback
      { trigger: '!audit-verify', handler: this.handleAuditVerify.bind(this) },
      { trigger: '!audit', handler: this.handleAudit.bind(this) },
      { trigger: '!rollback-preview', handler: this.handleRollbackPreview.bind(this) },
      { trigger: '!rollback-history', handler: this.handleRollbackHistory.bind(this) },
      { trigger: '!rollback', handler: this.handleRollback.bind(this) },

      // Cortex
      { trigger: '!cortex-run', handler: this.handleCortexRun.bind(this) },
      { trigger: '!cortex-config', handler: this.handleCortexConfig.bind(this) },
      { trigger: '!cortex', handler: this.handleCortex.bind(this) },
      { trigger: '!insights', handler: this.handleInsights.bind(this) },

      // Eval
      { trigger: '!eval-gate', handler: this.handleEvalGate.bind(this) },
      { trigger: '!eval-history', handler: this.handleEvalHistory.bind(this) },
      { trigger: '!eval-drift', handler: this.handleEvalDrift.bind(this) },
      { trigger: '!eval', handler: this.handleEval.bind(this) },
      { trigger: '!health', handler: this.handleHealth.bind(this) },

      // Tracing
      { trigger: '!trace-step', handler: this.handleTraceStep.bind(this) },
      { trigger: '!trace-complete', handler: this.handleTraceComplete.bind(this) },
      { trigger: '!trace-verify', handler: this.handleTraceVerify.bind(this) },
      { trigger: '!trace', handler: this.handleTrace.bind(this) },

      // Control
      { trigger: '!pending', handler: this.handlePending.bind(this) },
      { trigger: '!approve', handler: this.handleApprove.bind(this) },
      { trigger: '!policy', handler: this.handlePolicy.bind(this) },
      { trigger: '!actions', handler: this.handleActions.bind(this) },

      // Overview
      { trigger: '!dashboard', handler: this.handleDashboard.bind(this) },
      { trigger: '!context', handler: this.handleContext.bind(this) },
      { trigger: '!stats', handler: this.handleStats.bind(this) },
      { trigger: '!status', handler: this.handleStatus.bind(this) },
      { trigger: '!help', handler: this.handleHelp.bind(this) },
    ];
  }

  // ---- Centralized API Helper ----

  async _apiCall(method, path, data = null, params = null) {
    if (!this.apiKey) return null;
    try {
      const config = {
        method,
        url: `${this.apiUrl}${path}`,
        headers: { 'Authorization': `Bearer ${this.apiKey}` },
        timeout: 15000,
      };
      if (data) config.data = data;
      if (params) config.params = params;
      const response = await axios(config);
      // 204 No Content returns "" — normalize to true for success detection
      return response.data !== undefined && response.data !== '' ? response.data : true;
    } catch (error) {
      this._handleError(error, path);
      return null;
    }
  }

  // ---- Argument Parser ----

  _parseArgs(message, trigger) {
    const raw = message.replace(trigger, '').trim();
    const args = { _raw: raw, _positional: [] };
    const parts = raw.split(/\s+/);
    for (let i = 0; i < parts.length; i++) {
      if (parts[i].startsWith('--') && i + 1 < parts.length) {
        args[parts[i].slice(2)] = parts[i + 1];
        i++;
      } else {
        args._positional.push(parts[i]);
      }
    }
    return args;
  }

  // ---- Core API Methods ----

  async remember(observation, tags = []) {
    if (!this.apiKey || !this.autoSave) return null;
    const result = await this._apiCall('post', '/v1/memories', { observation, tags });
    if (result) {
      const id = result.uuid || result.id;
      if (id) {
        this._writeLog.push({
          id,
          observation: observation.slice(0, 80),
          at: new Date().toISOString(),
        });
      }
    }
    return result;
  }

  async forgetById(memoryId) {
    if (!this.apiKey) return null;
    const result = await this._apiCall('delete', `/v1/memories/${memoryId}`);
    return result ? { deleted: true } : null;
  }

  async recall(query, limit = this.recallLimit) {
    if (!this.apiKey || !this.autoRecall) return [];
    const result = await this._apiCall('get', '/v1/memories/search', null, { q: query, limit });
    return result?.memories || [];
  }

  async usage() {
    return this._apiCall('get', '/v1/usage');
  }

  async audit(limit = 10) {
    return this._apiCall('get', '/v1/audit', null, { limit });
  }

  // ---- Middleware Hooks ----

  async onMessage(userMessage, sessionId) {
    for (const cmd of this.commands) {
      if (userMessage === cmd.trigger || userMessage.startsWith(cmd.trigger + ' ')) {
        return await cmd.handler(userMessage, sessionId);
      }
    }

    if (userMessage.length < 15) return userMessage;

    const context = await this.recall(userMessage, this.recallLimit);
    this.remember(userMessage, ['role:user', `session:${sessionId}`]).catch(() => {});

    if (context.length > 0) {
      // Filter out previously injected context blocks
      const filtered = context.filter(m => !m.observation.includes('<relevant-memories>'));
      if (filtered.length > 0) {
        const contextBlock = filtered.map(m => `- ${m.observation}`).join('\n');
        return `[Recalled Memory]\n${contextBlock}\n\nUser: ${userMessage}`;
      }
    }

    return userMessage;
  }

  async onResponse(agentResponse, sessionId) {
    if (!this.apiKey) return;
    if (!agentResponse || agentResponse.length < 20) return;
    // Skip responses that contain injected memory context
    if (agentResponse.includes('<relevant-memories>')) return;
    const observation = agentResponse.length > 500
      ? agentResponse.slice(0, 500) + '...'
      : agentResponse;
    this.remember(observation, ['role:assistant', `session:${sessionId}`]).catch(() => {});
  }

  // ================================================================
  // MEMORY BASICS
  // ================================================================

  async handleRemember(message) {
    const args = this._parseArgs(message, '!remember');
    const tags = args.tags ? args.tags.split(',') : ['explicit'];
    const text = args.tags ? args._positional.join(' ') : args._raw;
    if (!text) return 'Usage: `!remember <fact to save> [--tags tag1,tag2]`';
    const saved = this.autoSave;
    this.autoSave = true;
    const result = await this.remember(text, tags);
    this.autoSave = saved;
    return result ? `Saved: "${text.slice(0, 80)}" (id: ${result.uuid || result.id})` : 'Failed to save. Check your API key.';
  }

  async handleSearch(message) {
    const query = message.replace('!search', '').trim();
    if (!query) return 'Usage: `!search <query>`';
    const saved = this.autoRecall;
    this.autoRecall = true;
    const results = await this.recall(query, 5);
    this.autoRecall = saved;
    if (results.length === 0) return `No memories found for "${query}".`;
    const lines = [`**Search: "${query}"**\n`];
    results.forEach((m, i) => {
      const score = m.score != null ? `${Math.round(m.score * 100)}%` : '--';
      const obs = m.observation.length > 120 ? m.observation.slice(0, 120) + '...' : m.observation;
      lines.push(`${i + 1}. \`${score}\` ${obs}`);
    });
    return lines.join('\n');
  }

  async handleList(message) {
    const args = this._parseArgs(message, '!list');
    const params = { limit: parseInt(args.limit) || 10 };
    if (args.tag) params.tag = args.tag;
    const data = await this._apiCall('get', '/v1/memories', null, params);
    if (!data || !data.memories || data.memories.length === 0) return 'No memories found.';
    const lines = [`**Memories** (${data.total || data.memories.length} total)\n`];
    data.memories.forEach((m, i) => {
      const obs = m.observation.length > 100 ? m.observation.slice(0, 100) + '...' : m.observation;
      const id = (m.uuid || m.id || '').slice(0, 8);
      lines.push(`${i + 1}. \`${id}\` ${obs}`);
    });
    return lines.join('\n');
  }

  async handleForget(message) {
    const topic = message.replace('!forget', '').trim();
    if (!topic) return 'Usage: `!forget <topic>`';
    const saved = this.autoRecall;
    this.autoRecall = true;
    const matches = await this.recall(topic, 10);
    this.autoRecall = saved;
    const relevant = matches.filter(m => (m.score || 0) > 0.5);
    if (relevant.length === 0) return `No memories found matching "${topic}".`;
    let deleted = 0;
    for (const m of relevant) {
      const result = await this.forgetById(m.uuid || m.id);
      if (result) deleted++;
    }
    return `Forgot ${deleted} memor${deleted === 1 ? 'y' : 'ies'} about "${topic}".`;
  }

  async handleUndo(message) {
    const countArg = parseInt(message.replace('!undo', '').trim()) || 1;
    const count = Math.min(countArg, this._writeLog.length, 10);
    if (this._writeLog.length === 0) return 'Nothing to undo. No memories saved this session.';
    const toDelete = this._writeLog.splice(-count, count);
    let deleted = 0;
    let failed = 0;
    for (const entry of toDelete.reverse()) {
      const result = await this.forgetById(entry.id);
      if (result) { deleted++; } else { failed++; }
    }
    let msg = `Undid ${deleted} memor${deleted === 1 ? 'y' : 'ies'}.`;
    if (failed > 0) msg += ` (${failed} failed)`;
    msg += `\n${this._writeLog.length} more in undo history.`;
    return msg;
  }

  async handleSupersede(message) {
    const args = this._parseArgs(message, '!supersede');
    const oldId = args._positional[0];
    const newText = args._positional.slice(1).join(' ');
    if (!oldId || !newText) return 'Usage: `!supersede <memory_id> <new observation>`';
    const result = await this._apiCall('post', '/v1/memories', {
      observation: newText,
      supersede_memory_id: oldId,
      tags: ['superseded'],
    });
    if (!result) return 'Failed to supersede. Check the memory ID.';
    return `Superseded \`${oldId.slice(0, 8)}\` with new memory \`${(result.uuid || result.id || '').slice(0, 8)}\``;
  }

  // ================================================================
  // DRAFT MANAGEMENT
  // ================================================================

  async handleDraft(message) {
    const args = this._parseArgs(message, '!draft');
    const text = args.branch ? args._positional.join(' ') : args._raw;
    if (!text) return 'Usage: `!draft <text> [--branch name]`';
    const body = { observation: text };
    if (args.branch) body.branch = args.branch;
    const result = await this._apiCall('post', '/v1/memory-drafts', body);
    if (!result) return 'Failed to create draft.';
    return `Draft created: \`${(result.draft_id || result.id || '').slice(0, 8)}\`${args.branch ? ` (branch: ${args.branch})` : ''}`;
  }

  async handleDrafts(message) {
    const data = await this._apiCall('get', '/v1/memory-drafts');
    if (!data || !data.drafts || data.drafts.length === 0) return 'No pending drafts.';
    const lines = [`**Drafts** (${data.drafts.length})\n`];
    data.drafts.forEach((d, i) => {
      const obs = (d.observation || '').slice(0, 80);
      const id = (d.draft_id || d.id || '').slice(0, 8);
      lines.push(`${i + 1}. \`${id}\` ${obs}${d.branch ? ` [${d.branch}]` : ''}`);
    });
    return lines.join('\n');
  }

  async handleDraftDiff(message) {
    const id = message.replace('!draft-diff', '').trim();
    if (!id) return 'Usage: `!draft-diff <draft_id>`';
    const data = await this._apiCall('get', `/v1/memory-drafts/${id}/diff`);
    if (!data) return 'Draft not found or diff unavailable.';
    const lines = [`**Draft Diff** \`${id.slice(0, 8)}\`\n`];
    if (data.changes) {
      for (const [field, change] of Object.entries(data.changes)) {
        lines.push(`**${field}**: \`${change.from || '(empty)'}\` → \`${change.to || '(empty)'}\``);
      }
    }
    return lines.join('\n') || 'No differences found.';
  }

  async handleMergeDraft(message) {
    const id = message.replace('!merge-draft', '').trim();
    if (!id) return 'Usage: `!merge-draft <draft_id>`';
    const result = await this._apiCall('post', `/v1/memory-drafts/${id}/merge`);
    if (!result) return 'Failed to merge draft.';
    return `Draft \`${id.slice(0, 8)}\` merged into canonical memory.`;
  }

  async handleRejectDraft(message) {
    const id = message.replace('!reject-draft', '').trim();
    if (!id) return 'Usage: `!reject-draft <draft_id>`';
    const result = await this._apiCall('post', `/v1/memory-drafts/${id}/reject`);
    if (!result) return 'Failed to reject draft.';
    return `Draft \`${id.slice(0, 8)}\` rejected.`;
  }

  async handleBranch(message) {
    const name = message.replace('!branch', '').trim();
    if (!name) return 'Usage: `!branch <branch_name>`';
    const data = await this._apiCall('get', `/v1/memory-branches/${encodeURIComponent(name)}`);
    if (!data) return `Branch "${name}" not found.`;
    const lines = [`**Branch: ${name}**\n`];
    if (data.drafts) {
      data.drafts.forEach((d, i) => {
        const obs = (d.observation || '').slice(0, 80);
        lines.push(`${i + 1}. \`${(d.draft_id || d.id || '').slice(0, 8)}\` ${obs}`);
      });
    }
    lines.push(`\nStatus: ${data.status || 'open'} | ${data.draft_count || data.drafts?.length || 0} drafts`);
    return lines.join('\n');
  }

  async handleMergeBranch(message) {
    const name = message.replace('!merge-branch', '').trim();
    if (!name) return 'Usage: `!merge-branch <branch_name>`';
    const result = await this._apiCall('post', `/v1/memory-branches/${encodeURIComponent(name)}/merge`);
    if (!result) return 'Failed to merge branch.';
    return `Branch "${name}" merged. ${result.merged_count || 0} drafts committed to canonical memory.`;
  }

  async handleRejectBranch(message) {
    const name = message.replace('!reject-branch', '').trim();
    if (!name) return 'Usage: `!reject-branch <branch_name>`';
    const result = await this._apiCall('post', `/v1/memory-branches/${encodeURIComponent(name)}/reject`);
    if (!result) return 'Failed to reject branch.';
    return `Branch "${name}" rejected. ${result.rejected_count || 0} drafts discarded.`;
  }

  // ================================================================
  // MEMORY LINKS
  // ================================================================

  async handleLink(message) {
    const args = this._parseArgs(message, '!link');
    const [fromId, toId] = args._positional;
    const relation = args._positional[2] || args.relation || 'related_to';
    if (!fromId || !toId) return 'Usage: `!link <from_id> <to_id> [relation]`';
    const result = await this._apiCall('post', '/v1/memories/link', {
      source_id: fromId,
      target_id: toId,
      relation,
    });
    if (!result) return 'Failed to create link.';
    return `Linked \`${fromId.slice(0, 8)}\` → \`${toId.slice(0, 8)}\` (${relation})`;
  }

  async handleUnlink(message) {
    const args = this._parseArgs(message, '!unlink');
    const [fromId, toId] = args._positional;
    if (!fromId || !toId) return 'Usage: `!unlink <from_id> <to_id>`';
    const result = await this._apiCall('delete', '/v1/memories/link', {
      source_id: fromId,
      target_id: toId,
    });
    if (!result) return 'Failed to remove link.';
    return `Unlinked \`${fromId.slice(0, 8)}\` from \`${toId.slice(0, 8)}\``;
  }

  async handleLinks(message) {
    const id = message.replace('!links', '').trim();
    if (!id) return 'Usage: `!links <memory_id>`';
    const data = await this._apiCall('get', `/v1/memories/${id}/links`);
    if (!data || !data.edges || data.edges.length === 0) return `No links for memory \`${id.slice(0, 8)}\`.`;
    const lines = [`**Links for \`${id.slice(0, 8)}\`**\n`];
    data.edges.forEach((e, i) => {
      lines.push(`${i + 1}. \`${(e.source_id || '').slice(0, 8)}\` →[${e.relation}]→ \`${(e.target_id || '').slice(0, 8)}\``);
    });
    return lines.join('\n');
  }

  // ================================================================
  // KNOWLEDGE GRAPH
  // ================================================================

  async handleTriple(message) {
    const raw = message.replace('!triple', '').trim();
    const parts = raw.split('|').map(s => s.trim());
    if (parts.length < 3) return 'Usage: `!triple <subject> | <predicate> | <object>`';
    const [subject, predicate, object] = parts;
    const result = await this._apiCall('post', '/v1/knowledge/triples', { subject, predicate, object });
    if (!result) return 'Failed to add triple.';
    return `Triple added: **${subject}** →[${predicate}]→ **${object}**`;
  }

  async handleTriples(message) {
    const args = this._parseArgs(message, '!triples');
    const params = { limit: parseInt(args.limit) || 20 };
    if (args.subject) params.subject = args.subject;
    if (args.predicate) params.predicate = args.predicate;
    const data = await this._apiCall('get', '/v1/knowledge/triples', null, params);
    if (!data || !data.triples || data.triples.length === 0) return 'No triples found.';
    const lines = [`**Knowledge Graph** (${data.total || data.triples.length} triples)\n`];
    data.triples.forEach((t, i) => {
      lines.push(`${i + 1}. **${t.subject}** →[${t.predicate}]→ **${t.object}**`);
    });
    return lines.join('\n');
  }

  async handleEntities(message) {
    const args = this._parseArgs(message, '!entities');
    const params = { limit: parseInt(args.limit) || 20 };
    if (args.type) params.type = args.type;
    const data = await this._apiCall('get', '/v1/knowledge/entities', null, params);
    if (!data || !data.entities || data.entities.length === 0) return 'No entities found.';
    const lines = [`**Entities** (${data.total || data.entities.length})\n`];
    data.entities.forEach((e, i) => {
      lines.push(`${i + 1}. **${e.name || e.entity_id}** (${e.type || 'unknown'}) — ${e.triple_count || 0} triples`);
    });
    return lines.join('\n');
  }

  async handleEntity(message) {
    const id = message.replace('!entity', '').trim();
    if (!id) return 'Usage: `!entity <entity_id>`';
    const data = await this._apiCall('get', `/v1/knowledge/entities/${encodeURIComponent(id)}`);
    if (!data) return `Entity "${id}" not found.`;
    const lines = [`**${data.name || id}** (${data.type || 'unknown'})\n`];
    if (data.triples && data.triples.length > 0) {
      lines.push('Triples:');
      data.triples.forEach(t => {
        lines.push(`  • **${t.subject}** →[${t.predicate}]→ **${t.object}**`);
      });
    }
    return lines.join('\n');
  }

  async handleDelTriple(message) {
    const id = message.replace('!del-triple', '').trim();
    if (!id) return 'Usage: `!del-triple <triple_id>`';
    const result = await this._apiCall('delete', `/v1/knowledge/triples/${id}`);
    if (!result) return 'Failed to delete triple.';
    return `Triple \`${id.slice(0, 8)}\` deleted.`;
  }

  async handleDelEntity(message) {
    const id = message.replace('!del-entity', '').trim();
    if (!id) return 'Usage: `!del-entity <entity_id>`';
    const result = await this._apiCall('delete', `/v1/knowledge/entities/${encodeURIComponent(id)}`);
    if (!result) return 'Failed to delete entity.';
    return `Entity "${id}" and all connected triples deleted.`;
  }

  async handleGraph(message) {
    const args = this._parseArgs(message, '!graph');
    const params = { limit: parseInt(args.limit) || 20 };
    if (args.relation) params.relation = args.relation;
    const data = await this._apiCall('get', '/v1/memories/edges', null, params);
    if (!data || !data.edges || data.edges.length === 0) return 'No graph edges found.';
    const lines = [`**Memory Graph** (${data.total || data.edges.length} edges)\n`];
    data.edges.forEach((e, i) => {
      lines.push(`${i + 1}. \`${(e.source_id || '').slice(0, 8)}\` →[${e.relation}]→ \`${(e.target_id || '').slice(0, 8)}\``);
    });
    return lines.join('\n');
  }

  // ================================================================
  // CONTEXT SPACES
  // ================================================================

  async handleSpace(message) {
    const args = this._parseArgs(message, '!space');
    const name = args._positional[0];
    if (!name) return 'Usage: `!space <name> [--description desc]`';
    const body = { name };
    if (args.description) body.description = args.description;
    const result = await this._apiCall('post', '/v1/context-spaces', body);
    if (!result) return 'Failed to create space.';
    return `Space "${name}" created (id: \`${(result.space_id || result.id || '').slice(0, 8)}\`)`;
  }

  async handleSpaces(message) {
    const data = await this._apiCall('get', '/v1/context-spaces');
    if (!data || !data.spaces || data.spaces.length === 0) return 'No spaces found.';
    const lines = [`**Context Spaces** (${data.spaces.length})\n`];
    data.spaces.forEach((s, i) => {
      lines.push(`${i + 1}. \`${(s.space_id || s.id || '').slice(0, 8)}\` **${s.name}** — ${s.description || 'No description'}`);
    });
    return lines.join('\n');
  }

  async handleSpaceMemories(message) {
    const args = this._parseArgs(message, '!space-memories');
    const spaceId = args._positional[0];
    if (!spaceId) return 'Usage: `!space-memories <space_id> [search query]`';
    const query = args._positional.slice(1).join(' ');
    const params = { limit: 10 };
    if (query) params.q = query;
    const data = await this._apiCall('get', `/v1/context-spaces/${spaceId}/memories`, null, params);
    if (!data || !data.memories || data.memories.length === 0) return 'No memories in this space.';
    const lines = [`**Space Memories**\n`];
    data.memories.forEach((m, i) => {
      const obs = (m.observation || '').slice(0, 100);
      lines.push(`${i + 1}. ${obs}`);
    });
    return lines.join('\n');
  }

  async handleUpdateSpace(message) {
    const args = this._parseArgs(message, '!update-space');
    const spaceId = args._positional[0];
    if (!spaceId) return 'Usage: `!update-space <space_id> [--name n] [--description d]`';
    const body = {};
    if (args.name) body.name = args.name;
    if (args.description) body.description = args.description;
    if (Object.keys(body).length === 0) return 'Provide at least --name or --description to update.';
    const result = await this._apiCall('put', `/v1/context-spaces/${spaceId}`, body);
    if (!result) return 'Failed to update space.';
    return `Space \`${spaceId.slice(0, 8)}\` updated.`;
  }

  async handleDelSpace(message) {
    const id = message.replace('!del-space', '').trim();
    if (!id) return 'Usage: `!del-space <space_id>`';
    const result = await this._apiCall('delete', `/v1/context-spaces/${id}`);
    if (!result) return 'Failed to delete space.';
    return `Space \`${id.slice(0, 8)}\` deleted.`;
  }

  async handleShare(message) {
    const args = this._parseArgs(message, '!share');
    const [spaceId, email] = args._positional;
    if (!spaceId || !email) return 'Usage: `!share <space_id> <email>`';
    const result = await this._apiCall('post', '/v1/spaces/share', { space_id: spaceId, email });
    if (!result) return 'Failed to share space.';
    return `Space \`${spaceId.slice(0, 8)}\` shared with ${email}. Token: \`${result.token || '(generated)'}\``;
  }

  async handleShared(message) {
    const data = await this._apiCall('get', '/v1/spaces/shared');
    if (!data || !data.shared || data.shared.length === 0) return 'No shared contexts.';
    const lines = ['**Shared Contexts**\n'];
    data.shared.forEach((s, i) => {
      lines.push(`${i + 1}. **${s.space_name || s.name}** — shared by ${s.owner || 'unknown'}`);
    });
    return lines.join('\n');
  }

  async handleAccept(message) {
    const token = message.replace('!accept', '').trim();
    if (!token) return 'Usage: `!accept <share_token>`';
    const result = await this._apiCall('post', '/v1/spaces/join', { token });
    if (!result) return 'Failed to accept invitation. Check the token.';
    return `Joined shared space: **${result.space_name || result.name || 'unknown'}**`;
  }

  async handleRevoke(message) {
    const token = message.replace('!revoke', '').trim();
    if (!token) return 'Usage: `!revoke <share_token>`';
    const result = await this._apiCall('delete', `/v1/spaces/share/${token}`);
    if (!result) return 'Failed to revoke.';
    return `Share token revoked.`;
  }

  // ================================================================
  // REPLAY (TIME-TRAVEL DEBUGGING)
  // ================================================================

  async handleTimeline(message) {
    const args = this._parseArgs(message, '!timeline');
    const limit = parseInt(args._positional[0] || args.limit) || 10;
    const data = await this._apiCall('get', '/v1/replay/timeline', null, { limit });
    if (!data || !data.events || data.events.length === 0) return 'No timeline events.';
    const lines = ['**Memory Timeline**\n'];
    data.events.forEach(e => {
      const ts = new Date(e.timestamp).toLocaleTimeString();
      lines.push(`\`${ts}\` **${e.operation}** — ${(e.observation || e.description || '').slice(0, 60)}`);
    });
    return lines.join('\n');
  }

  async handleSnapshot(message) {
    const raw = message.replace('!snapshot', '').trim();
    const timestamp = this._parseRelativeTime(raw || '1 hour ago');
    if (!timestamp) return 'Usage: `!snapshot <time>` (e.g., "1h", "2 days ago", ISO timestamp)';
    const data = await this._apiCall('get', '/v1/replay/snapshot', null, { timestamp });
    if (!data) return 'Failed to get snapshot. This feature requires Pro tier or higher.';
    const count = data.memories?.length || data.count || 0;
    const lines = [`**Snapshot at ${raw || '1 hour ago'}** (${count} memories)\n`];
    if (data.memories) {
      data.memories.slice(0, 10).forEach((m, i) => {
        lines.push(`${i + 1}. ${(m.observation || '').slice(0, 80)}`);
      });
      if (data.memories.length > 10) lines.push(`... and ${data.memories.length - 10} more`);
    }
    return lines.join('\n');
  }

  async handleLifecycle(message) {
    const id = message.replace('!lifecycle', '').trim();
    if (!id) return 'Usage: `!lifecycle <memory_id>`';
    const data = await this._apiCall('get', `/v1/replay/memory/${id}`);
    if (!data) return 'Memory not found or lifecycle unavailable.';
    const lines = [`**Lifecycle: \`${id.slice(0, 8)}\`**\n`];
    if (data.events) {
      data.events.forEach(e => {
        const ts = new Date(e.timestamp).toLocaleTimeString();
        lines.push(`\`${ts}\` ${e.operation} — ${e.detail || ''}`);
      });
    }
    if (data.observation) lines.push(`\nCurrent: "${(data.observation || '').slice(0, 100)}"`);
    return lines.join('\n');
  }

  async handleReplayDiff(message) {
    const args = this._parseArgs(message, '!replay-diff');
    const [t1Raw, t2Raw] = args._positional;
    if (!t1Raw || !t2Raw) return 'Usage: `!replay-diff <from_time> <to_time>`';
    const from_ts = this._parseRelativeTime(t1Raw);
    const to_ts = this._parseRelativeTime(t2Raw);
    if (!from_ts || !to_ts) return 'Could not parse timestamps. Try "1h", "2d", or ISO format.';
    const data = await this._apiCall('get', '/v1/replay/diff', null, { from: from_ts, to: to_ts });
    if (!data) return 'Diff unavailable. Requires Pro tier or higher.';
    const lines = ['**Memory Diff**\n'];
    lines.push(`Added: ${data.added || 0} | Removed: ${data.removed || 0} | Modified: ${data.modified || 0}`);
    return lines.join('\n');
  }

  async handleReplay(message) {
    const id = message.replace('!replay', '').trim();
    if (!id) return 'Usage: `!replay <memory_id>`';
    const data = await this._apiCall('get', `/v1/replay/memory/${id}`);
    if (!data) return 'Memory not found.';
    const lines = [`**Memory History: \`${id.slice(0, 8)}\`**\n`];
    if (data.versions) {
      data.versions.forEach((v, i) => {
        const ts = new Date(v.timestamp).toLocaleTimeString();
        lines.push(`${i + 1}. \`${ts}\` ${(v.observation || '').slice(0, 80)}`);
      });
    } else if (data.events) {
      data.events.forEach(e => {
        const ts = new Date(e.timestamp).toLocaleTimeString();
        lines.push(`\`${ts}\` ${e.operation}`);
      });
    }
    return lines.join('\n');
  }

  async handleRecallAt(message) {
    const args = this._parseArgs(message, '!recall-at');
    const timeRaw = args._positional[0];
    const query = args._positional.slice(1).join(' ');
    if (!timeRaw || !query) return 'Usage: `!recall-at <time> <query>`';
    const timestamp = this._parseRelativeTime(timeRaw);
    if (!timestamp) return `Could not parse "${timeRaw}".`;
    const data = await this._apiCall('post', '/v1/replay/recall', { timestamp, query, limit: 5 });
    if (!data || !data.memories || data.memories.length === 0) return `No memories found at ${timeRaw} for "${query}".`;
    const lines = [`**Recall at ${timeRaw}: "${query}"**\n`];
    data.memories.forEach((m, i) => {
      const score = m.score != null ? `${Math.round(m.score * 100)}%` : '--';
      lines.push(`${i + 1}. \`${score}\` ${(m.observation || '').slice(0, 100)}`);
    });
    return lines.join('\n');
  }

  async handleReplayDrift(message) {
    const args = this._parseArgs(message, '!replay-drift');
    const [t1Raw, t2Raw] = args._positional;
    if (!t1Raw || !t2Raw) return 'Usage: `!replay-drift <from_time> <to_time>`';
    const from_ts = this._parseRelativeTime(t1Raw);
    const to_ts = this._parseRelativeTime(t2Raw);
    if (!from_ts || !to_ts) return 'Could not parse timestamps.';
    const data = await this._apiCall('get', '/v1/replay/drift', null, { from: from_ts, to: to_ts });
    if (!data) return 'Drift analysis unavailable. Requires Enterprise tier.';
    const lines = ['**Memory Drift Analysis**\n'];
    lines.push(`Topic drift: ${data.topic_drift || 'N/A'}`);
    lines.push(`Sentiment shift: ${data.sentiment_shift || 'N/A'}`);
    lines.push(`Consistency: ${data.consistency || 'N/A'}`);
    return lines.join('\n');
  }

  // ================================================================
  // AUDIT & ROLLBACK
  // ================================================================

  async handleAudit(message) {
    const limitArg = parseInt(message.replace('!audit', '').trim()) || 10;
    const data = await this.audit(limitArg);
    if (!data || !data.entries || data.entries.length === 0) return 'No audit entries found.';
    const lines = ['**Recent Operations:**\n'];
    for (const e of data.entries.slice(0, limitArg)) {
      const ts = new Date(e.timestamp).toLocaleTimeString();
      const hash = e.entry_hash ? e.entry_hash.slice(0, 8) : '--------';
      lines.push(`\`${ts}\` ${e.method} ${e.endpoint} → ${e.status} [${hash}]`);
    }
    lines.push(`\n*${data.total_count} total operations on record.*`);
    return lines.join('\n');
  }

  async handleAuditVerify(message) {
    const data = await this._apiCall('get', '/v1/audit/verify');
    if (!data) return 'Audit verification unavailable.';
    const status = data.valid ? '✓ Audit chain intact' : '✗ Audit chain BROKEN';
    const lines = [`**${status}**\n`];
    lines.push(`Entries verified: ${data.entries_verified || 0}`);
    lines.push(`Chain length: ${data.chain_length || 0}`);
    if (data.broken_at) lines.push(`Broken at entry: ${data.broken_at}`);
    return lines.join('\n');
  }

  async handleRollback(message) {
    const rawTarget = message.replace('!rollback', '').trim() || '1 hour ago';
    const target = this._parseRelativeTime(rawTarget);
    if (!target) return `Could not parse "${rawTarget}". Try "1h", "30m", "2 days ago", or an ISO timestamp.`;

    const preview = await this._apiCall('post', '/v1/rollback', { target, dry_run: true });
    if (!preview) return 'Rollback failed. This feature requires a Novyx API key (free tier includes 10 rollbacks/month).';
    if (preview.artifacts_restored === 0 && preview.operations_undone === 0) {
      return `Nothing to roll back. No changes found since ${rawTarget}.`;
    }

    const result = await this._apiCall('post', '/v1/rollback', { target, dry_run: false });
    if (!result) return 'Rollback execution failed. Try again or check your API key.';
    return `**Rolled back to ${result.rolled_back_to}**\n` +
           `${result.artifacts_restored} memories restored, ${result.operations_undone} operations undone.`;
  }

  async handleRollbackPreview(message) {
    const rawTarget = message.replace('!rollback-preview', '').trim() || '1 hour ago';
    const target = this._parseRelativeTime(rawTarget);
    if (!target) return `Could not parse "${rawTarget}".`;
    const data = await this._apiCall('post', '/v1/rollback', { target, dry_run: true });
    if (!data) return 'Preview unavailable.';
    return `**Rollback Preview to ${rawTarget}**\n` +
           `Would restore: ${data.artifacts_restored || 0} memories\n` +
           `Would undo: ${data.operations_undone || 0} operations`;
  }

  async handleRollbackHistory(message) {
    const data = await this._apiCall('get', '/v1/rollback/history');
    if (!data || !data.rollbacks || data.rollbacks.length === 0) return 'No rollback history.';
    const lines = ['**Rollback History**\n'];
    data.rollbacks.forEach((r, i) => {
      const ts = new Date(r.timestamp || r.created_at).toLocaleTimeString();
      lines.push(`${i + 1}. \`${ts}\` → ${r.target} (${r.artifacts_restored || 0} restored, ${r.operations_undone || 0} undone)`);
    });
    return lines.join('\n');
  }

  // ================================================================
  // CORTEX (AUTONOMOUS INTELLIGENCE)
  // ================================================================

  async handleCortex(message) {
    const data = await this._apiCall('get', '/v1/cortex/status');
    if (!data) return 'Cortex unavailable. Requires Pro tier or higher.';
    const lines = ['**Cortex Status**\n'];
    lines.push(`Enabled: ${data.enabled ? 'Yes' : 'No'}`);
    lines.push(`Last run: ${data.last_run ? new Date(data.last_run).toLocaleString() : 'Never'}`);
    if (data.insights_count != null) lines.push(`Insights generated: ${data.insights_count}`);
    if (data.next_run) lines.push(`Next scheduled: ${new Date(data.next_run).toLocaleString()}`);
    return lines.join('\n');
  }

  async handleCortexRun(message) {
    const result = await this._apiCall('post', '/v1/cortex/run');
    if (!result) return 'Failed to trigger Cortex. Requires Pro tier or higher.';
    return `**Cortex cycle triggered.**\n` +
           `Insights generated: ${result.insights_generated || 0}\n` +
           `Duration: ${result.duration_ms || 'N/A'}ms`;
  }

  async handleInsights(message) {
    const data = await this._apiCall('get', '/v1/cortex/insights');
    if (!data || !data.insights || data.insights.length === 0) return 'No Cortex insights yet. Run `!cortex-run` first.';
    const lines = ['**Cortex Insights**\n'];
    data.insights.forEach((ins, i) => {
      lines.push(`${i + 1}. **${ins.type || 'insight'}**: ${(ins.description || ins.content || '').slice(0, 120)}`);
    });
    return lines.join('\n');
  }

  async handleCortexConfig(message) {
    const data = await this._apiCall('get', '/v1/cortex/config');
    if (!data) return 'Cortex config unavailable.';
    const lines = ['**Cortex Configuration**\n'];
    for (const [key, value] of Object.entries(data)) {
      if (key !== 'tenant_id') lines.push(`${key}: ${JSON.stringify(value)}`);
    }
    return lines.join('\n');
  }

  // ================================================================
  // EVAL (MEMORY HEALTH SCORING)
  // ================================================================

  async handleEval(message) {
    const result = await this._apiCall('post', '/v1/eval/run');
    if (!result) return 'Eval unavailable. Requires Starter tier or higher.';
    const lines = ['**Memory Evaluation**\n'];
    lines.push(`Overall score: **${result.score != null ? Math.round(result.score * 100) + '%' : 'N/A'}**`);
    if (result.recall_score != null) lines.push(`Recall: ${Math.round(result.recall_score * 100)}%`);
    if (result.drift_score != null) lines.push(`Drift: ${Math.round(result.drift_score * 100)}%`);
    if (result.conflict_score != null) lines.push(`Conflicts: ${Math.round(result.conflict_score * 100)}%`);
    if (result.staleness_score != null) lines.push(`Staleness: ${Math.round(result.staleness_score * 100)}%`);
    return lines.join('\n');
  }

  async handleEvalGate(message) {
    const args = this._parseArgs(message, '!eval-gate');
    const threshold = parseFloat(args._positional[0]) || 0.7;
    const result = await this._apiCall('post', '/v1/eval/gate', { threshold });
    if (!result) return 'Eval gate unavailable.';
    const status = result.passed ? '✓ PASSED' : '✗ FAILED';
    return `**CI Gate: ${status}**\nScore: ${result.score != null ? Math.round(result.score * 100) + '%' : 'N/A'} (threshold: ${Math.round(threshold * 100)}%)`;
  }

  async handleEvalHistory(message) {
    const data = await this._apiCall('get', '/v1/eval/history');
    if (!data || !data.evaluations || data.evaluations.length === 0) return 'No eval history.';
    const lines = ['**Eval History**\n'];
    data.evaluations.slice(0, 10).forEach((e, i) => {
      const ts = new Date(e.timestamp || e.created_at).toLocaleString();
      const score = e.score != null ? Math.round(e.score * 100) + '%' : '--';
      lines.push(`${i + 1}. \`${ts}\` Score: **${score}**`);
    });
    return lines.join('\n');
  }

  async handleEvalDrift(message) {
    const data = await this._apiCall('get', '/v1/eval/drift');
    if (!data) return 'Drift analysis unavailable.';
    const lines = ['**Eval Drift**\n'];
    lines.push(`Drift detected: ${data.drift_detected ? 'Yes' : 'No'}`);
    if (data.drift_score != null) lines.push(`Drift score: ${Math.round(data.drift_score * 100)}%`);
    if (data.details) lines.push(`Details: ${JSON.stringify(data.details).slice(0, 200)}`);
    return lines.join('\n');
  }

  async handleHealth(message) {
    const data = await this._apiCall('get', '/v1/memories/stats');
    if (!data) return 'Health check unavailable.';
    const lines = ['**Memory Health**\n'];
    lines.push(`Total memories: ${data.total || data.count || 0}`);
    if (data.tags) lines.push(`Tags: ${Object.keys(data.tags).length}`);
    if (data.avg_importance != null) lines.push(`Avg importance: ${data.avg_importance.toFixed(1)}`);
    if (data.avg_confidence != null) lines.push(`Avg confidence: ${data.avg_confidence.toFixed(2)}`);
    return lines.join('\n');
  }

  // ================================================================
  // TRACING (EXECUTION AUDIT)
  // ================================================================

  async handleTrace(message) {
    const name = message.replace('!trace', '').trim();
    if (!name) return 'Usage: `!trace <trace_name>`';
    const result = await this._apiCall('post', '/v1/traces', { name });
    if (!result) return 'Failed to create trace.';
    return `Trace created: **${name}** (id: \`${(result.trace_id || result.id || '').slice(0, 8)}\`)`;
  }

  async handleTraceStep(message) {
    const args = this._parseArgs(message, '!trace-step');
    const traceId = args._positional[0];
    const description = args._positional.slice(1).join(' ');
    const stepType = args.type || 'ACTION';
    if (!traceId || !description) return 'Usage: `!trace-step <trace_id> <description> [--type THOUGHT|ACTION|OBSERVATION]`';
    const result = await this._apiCall('post', `/v1/traces/${traceId}/steps`, {
      description,
      step_type: stepType,
    });
    if (!result) return 'Failed to add step.';
    return `Step added to trace \`${traceId.slice(0, 8)}\`: ${description.slice(0, 60)}`;
  }

  async handleTraceComplete(message) {
    const id = message.replace('!trace-complete', '').trim();
    if (!id) return 'Usage: `!trace-complete <trace_id>`';
    const result = await this._apiCall('post', `/v1/traces/${id}/complete`);
    if (!result) return 'Failed to complete trace.';
    return `Trace \`${id.slice(0, 8)}\` completed.${result.signature ? ' RSA signature generated.' : ''}`;
  }

  async handleTraceVerify(message) {
    const id = message.replace('!trace-verify', '').trim();
    if (!id) return 'Usage: `!trace-verify <trace_id>`';
    const data = await this._apiCall('post', `/v1/traces/${id}/verify`);
    if (!data) return 'Verification failed.';
    const status = data.valid ? '✓ Trace verified' : '✗ Trace verification FAILED';
    return `**${status}**\nSteps: ${data.steps_count || 0} | Chain intact: ${data.chain_valid ? 'Yes' : 'No'}`;
  }

  // ================================================================
  // CONTROL (GOVERNED ACTIONS)
  // ================================================================

  async handlePending(message) {
    const data = await this._apiCall('get', '/v1/approvals');
    if (!data || !data.approvals || data.approvals.length === 0) return 'No pending approvals.';
    const lines = ['**Pending Approvals**\n'];
    data.approvals.forEach((a, i) => {
      const id = (a.approval_id || a.id || '').slice(0, 8);
      lines.push(`${i + 1}. \`${id}\` **${a.action_type || a.type}** — ${(a.description || a.reason || '').slice(0, 80)}`);
    });
    return lines.join('\n');
  }

  async handleApprove(message) {
    const id = message.replace('!approve', '').trim();
    if (!id) return 'Usage: `!approve <approval_id>`';
    const result = await this._apiCall('post', `/v1/approvals/${id}/decision`, { decision: 'approved' });
    if (!result) return 'Failed to approve.';
    return `Approval \`${id.slice(0, 8)}\` → **approved**.`;
  }

  async handlePolicy(message) {
    const data = await this._apiCall('get', '/v1/control/policies');
    if (!data) return 'Policy info unavailable.';
    const lines = ['**Active Policies**\n'];
    if (data.policies) {
      data.policies.forEach((p, i) => {
        lines.push(`${i + 1}. **${p.name}** (${p.mode || 'enforcement'}) — ${p.description || ''}`);
      });
    } else {
      lines.push(`Mode: ${data.mode || 'default'}`);
    }
    return lines.join('\n');
  }

  async handleActions(message) {
    const args = this._parseArgs(message, '!actions');
    const limit = parseInt(args._positional[0] || args.limit) || 10;
    const data = await this._apiCall('get', '/v1/audit', null, { limit, event_type: 'action' });
    if (!data || !data.entries || data.entries.length === 0) return 'No action history.';
    const lines = ['**Action History**\n'];
    data.entries.forEach((e, i) => {
      const ts = new Date(e.timestamp).toLocaleTimeString();
      lines.push(`${i + 1}. \`${ts}\` ${e.method} ${e.endpoint} → ${e.status}`);
    });
    return lines.join('\n');
  }

  // ================================================================
  // OVERVIEW
  // ================================================================

  async handleDashboard(message) {
    const data = await this._apiCall('get', '/v1/dashboard');
    if (!data) return 'Dashboard unavailable.';
    const lines = ['**Dashboard**\n'];
    if (data.memories) lines.push(`Memories: ${data.memories.total || 0}`);
    if (data.api_calls) lines.push(`API calls today: ${data.api_calls.today || 0}`);
    if (data.tier) lines.push(`Tier: ${data.tier}`);
    if (data.health_score != null) lines.push(`Health score: ${Math.round(data.health_score * 100)}%`);
    if (data.recent_activity) {
      lines.push('\n**Recent Activity:**');
      data.recent_activity.slice(0, 5).forEach(a => {
        lines.push(`  • ${a.description || a.operation || 'event'}`);
      });
    }
    return lines.join('\n');
  }

  async handleContext(message) {
    const data = await this._apiCall('get', '/v1/context/now');
    if (!data) return 'Context unavailable.';
    const lines = ['**Current Context**\n'];
    if (data.server_time) lines.push(`Server time: ${data.server_time}`);
    if (data.recent_memories) {
      lines.push(`\nRecent memories (${data.recent_memories.length}):`);
      data.recent_memories.slice(0, 5).forEach(m => {
        lines.push(`  • ${(m.observation || '').slice(0, 80)}`);
      });
    }
    return lines.join('\n');
  }

  async handleStats(message) {
    const data = await this._apiCall('get', '/v1/memories/stats');
    if (!data) return 'Stats unavailable.';
    const lines = ['**Memory Statistics**\n'];
    lines.push(`Total: ${data.total || data.count || 0}`);
    if (data.by_tag) {
      lines.push('\nBy tag:');
      for (const [tag, count] of Object.entries(data.by_tag).slice(0, 10)) {
        lines.push(`  ${tag}: ${count}`);
      }
    }
    if (data.importance_distribution) {
      lines.push(`\nImportance distribution: ${JSON.stringify(data.importance_distribution)}`);
    }
    return lines.join('\n');
  }

  async handleStatus() {
    const usageData = await this.usage();
    if (!usageData) return 'Could not fetch status. Check your API key.';
    const tier = usageData.tier || 'Free';
    const memUsed = usageData.memories?.current || 0;
    const memLimit = usageData.memories?.limit || 0;
    const apiUsed = usageData.api_calls?.current || 0;
    const apiLimit = usageData.api_calls?.limit || 0;
    const rbUsed = usageData.rollbacks?.current || 0;
    const rbLimit = usageData.rollbacks?.limit || 0;
    const memPct = memLimit > 0 ? Math.round((memUsed / memLimit) * 100) : 0;
    return `**Memory Status**\n` +
           `Tier: ${tier}\n` +
           `Memories: ${memUsed} / ${memLimit} (${memPct}%)\n` +
           `API Calls: ${apiUsed} / ${apiLimit}\n` +
           `Rollbacks: ${rbUsed} / ${rbLimit}\n` +
           `Undo History: ${this._writeLog.length} writes this session`;
  }

  async handleHelp() {
    return `**Novyx Memory v3.0 — Full Core Coverage**

**Memory**
\`!remember <text>\` Save a fact • \`!search <query>\` Semantic search
\`!list [--tag t]\` List memories • \`!forget <topic>\` Delete by topic
\`!undo [N]\` Undo last N saves • \`!supersede <id> <text>\` Replace a memory

**Drafts**
\`!draft <text>\` Create draft • \`!drafts\` List drafts
\`!draft-diff <id>\` Show diff • \`!merge-draft <id>\` Merge to canonical
\`!reject-draft <id>\` Reject • \`!branch <name>\` View branch
\`!merge-branch <name>\` Merge all • \`!reject-branch <name>\` Reject all

**Links**
\`!link <from> <to> [rel]\` Link memories • \`!unlink <from> <to>\` Remove link
\`!links <id>\` Show links

**Knowledge Graph**
\`!triple <s> | <p> | <o>\` Add triple • \`!triples\` Query triples
\`!entities\` List entities • \`!entity <id>\` Entity details
\`!del-triple <id>\` Delete • \`!del-entity <id>\` Delete entity
\`!graph\` View edges

**Spaces**
\`!space <name>\` Create • \`!spaces\` List • \`!space-memories <id>\` Browse
\`!share <id> <email>\` Share • \`!shared\` List shared • \`!accept <token>\` Join
\`!update-space <id>\` Update • \`!del-space <id>\` Delete • \`!revoke <token>\` Revoke

**Replay (Time Travel)**
\`!timeline [N]\` Event timeline • \`!snapshot <time>\` State at time
\`!lifecycle <id>\` Memory biography • \`!replay <id>\` Full history
\`!replay-diff <t1> <t2>\` Diff • \`!recall-at <time> <query>\` Past recall
\`!replay-drift <t1> <t2>\` Drift analysis

**Audit & Rollback**
\`!audit [N]\` Operation log • \`!audit-verify\` Chain integrity
\`!rollback <time>\` Rewind memory • \`!rollback-preview <time>\` Preview
\`!rollback-history\` Past rollbacks

**Cortex (AI Intelligence)**
\`!cortex\` Status • \`!cortex-run\` Trigger cycle
\`!insights\` View insights • \`!cortex-config\` Configuration

**Eval (Memory Health)**
\`!eval\` Run evaluation • \`!eval-gate [threshold]\` CI gate
\`!eval-history\` Past evals • \`!eval-drift\` Drift detection
\`!health\` Memory stats

**Tracing**
\`!trace <name>\` Create trace • \`!trace-step <id> <desc>\` Add step
\`!trace-complete <id>\` Finalize • \`!trace-verify <id>\` Verify chain

**Control (Governed Actions)**
\`!pending\` Pending approvals • \`!approve <id>\` Approve action
\`!policy\` Active policies • \`!actions [N]\` Action history

**Overview**
\`!status\` Usage & tier • \`!dashboard\` Full dashboard
\`!context\` Current context • \`!stats\` Memory statistics
\`!help\` This menu

Memories are automatically recalled and saved during conversation.
Free tier: 5,000 memories, no credit card → https://novyxlabs.com`;
  }

  // ---- Helpers ----

  _parseRelativeTime(input) {
    const trimmed = input.trim();
    const match = trimmed.match(/^(\d+)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes|d|day|days)\s*(ago)?$/i);
    if (match) {
      const amount = parseInt(match[1]);
      const unit = match[2].toLowerCase();
      let ms;
      if (unit.startsWith('h')) ms = amount * 60 * 60 * 1000;
      else if (unit.startsWith('m')) ms = amount * 60 * 1000;
      else if (unit.startsWith('d')) ms = amount * 24 * 60 * 60 * 1000;
      else return null;
      return new Date(Date.now() - ms).toISOString();
    }
    const d = new Date(trimmed);
    if (!isNaN(d.getTime())) return d.toISOString();
    return null;
  }

  // ---- Error Handling ----

  _handleError(error, action) {
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data || {};
      if (status === 429) {
        console.warn(`[NovyxMemory] Rate limit during ${action}. Upgrade at novyxlabs.com/pricing`);
      } else if (status === 403) {
        const detail = data.detail || data.error || '';
        const msg = typeof detail === 'object' ? (detail.message || JSON.stringify(detail)) : String(detail);
        if (msg.toLowerCase().includes('upgrade') || msg.toLowerCase().includes('tier')) {
          console.warn(`[NovyxMemory] ${msg}. Upgrade at novyxlabs.com/pricing`);
        } else {
          console.warn(`[NovyxMemory] Access forbidden during ${action}. Check your API key.`);
        }
      } else {
        console.error(`[NovyxMemory] API Error (${status}) during ${action}:`, data);
      }
    } else if (error.code === 'ECONNABORTED') {
      console.warn(`[NovyxMemory] Request timeout during ${action}. The API may be temporarily slow.`);
    } else if (error.request) {
      console.error(`[NovyxMemory] Network error during ${action}: ${error.message}`);
    }
  }
}

module.exports = NovyxMemory;

// CLI quick check
if (require.main === module) {
  const memory = new NovyxMemory();
  console.log('NovyxMemory v3.0.0 initialized — 60+ commands, full Core coverage');
  console.log('Type !help for all commands');
}
