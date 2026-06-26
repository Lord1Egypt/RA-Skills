const { LobsterOps } = require('../src/core/LobsterOps');
const { PIIFilter } = require('../src/core/PIIFilter');
const { Exporter } = require('../src/core/Exporter');
const { DebugConsole } = require('../src/core/DebugConsole');
const { Analytics } = require('../src/core/Analytics');
const { AlertManager } = require('../src/core/AlertManager');
const { OpenClawInstrumentation } = require('../src/core/OpenClawInstrumentation');
const { JsonFileStorage } = require('../src/storage/JsonFileStorage');
const { MemoryStorage } = require('../src/storage/MemoryStorage');
const { StorageFactory } = require('../src/storage/StorageFactory');

describe('LobsterOps Core Functionality', () => {
  let lobsterOps;
  const testDir = './test-lobsterops-data';

  beforeEach(async () => {
    // Clean up any previous test data
    const fs = require('fs').promises;
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (e) {
      // Ignore if directory doesn't exist
    }

    lobsterOps = new LobsterOps({
      storageType: 'json',
      storageConfig: {
        dataDir: testDir
      }
    });

    await lobsterOps.init();
  });

  afterEach(async () => {
    await lobsterOps.close();
    // Clean up test data
    const fs = require('fs').promises;
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (e) {
      // Ignore if directory doesn't exist
    }
  });

  describe('Initialization', () => {
    test('should initialize successfully with JSON storage', async () => {
      expect(lobsterOps.isReady()).toBe(true);
    });

    test('should be disabled when enabled: false', async () => {
      const disabledOps = new LobsterOps({ enabled: false });
      await disabledOps.init();
      expect(disabledOps.isReady()).toBe(false);
      await disabledOps.close();
    });
  });

  describe('Event Logging', () => {
    test('should log a basic event and return an ID', async () => {
      const event = {
        type: 'test-event',
        message: 'This is a test event',
        data: { key: 'value' }
      };

      const eventId = await lobsterOps.logEvent(event);

      expect(eventId).toBeDefined();
      expect(typeof eventId).toBe('string');
      expect(eventId.length).toBeGreaterThan(0);
    });

    test('should enrich events with metadata', async () => {
      const event = {
        type: 'enrichment-test',
        message: 'Testing event enrichment'
      };

      const eventId = await lobsterOps.logEvent(event);
      const retrievedEvent = await lobsterOps.getEvent(eventId);

      expect(retrievedEvent).toBeDefined();
      expect(retrievedEvent.id).toBe(eventId);
      expect(retrievedEvent.timestamp).toMatch(/\d{4}-\d{2}-\d{2}/); // ISO date format
      expect(retrievedEvent.lobsterOpsInstanceId).toBeDefined();
      expect(retrievedEvent.loggedAt).toMatch(/\d{4}-\d{2}-\d{2}/);
    });

    test('should preserve original event data', async () => {
      const originalEvent = {
        type: 'preservation-test',
        agentId: 'agent-123',
        action: 'test-action',
        input: { query: 'test query' },
        output: { result: 'success' },
        durationMs: 150
      };

      const eventId = await lobsterOps.logEvent(originalEvent);
      const retrievedEvent = await lobsterOps.getEvent(eventId);

      expect(retrievedEvent.agentId).toBe(originalEvent.agentId);
      expect(retrievedEvent.action).toBe(originalEvent.action);
      expect(retrievedEvent.input).toEqual(originalEvent.input);
      expect(retrievedEvent.output).toEqual(originalEvent.output);
      expect(retrievedEvent.durationMs).toBe(originalEvent.durationMs);
    });
  });

  describe('Event Querying', () => {
    test('should be able to query events by various criteria', async () => {
      // Log several test events
      const eventsToLog = [
        {
          type: 'query-test',
          agentId: 'agent-alpha',
          action: 'action-one',
          timestamp: '2026-03-18T10:00:00Z'
        },
        {
          type: 'query-test',
          agentId: 'agent-beta',
          action: 'action-two',
          timestamp: '2026-03-18T11:00:00Z'
        },
        {
          type: 'other-type',
          agentId: 'agent-alpha',
          action: 'action-three',
          timestamp: '2026-03-18T12:00:00Z'
        }
      ];

      const eventIds = [];
      for (const event of eventsToLog) {
        const id = await lobsterOps.logEvent(event);
        eventIds.push(id);
      }

      // Query by type
      const typeResults = await lobsterOps.queryEvents({ eventTypes: ['query-test'] });
      expect(typeResults).toHaveLength(2);

      // Query by agentId
      const agentResults = await lobsterOps.queryEvents({ agentIds: ['agent-alpha'] });
      expect(agentResults).toHaveLength(2);

      // Query by multiple criteria
      const combinedResults = await lobsterOps.queryEvents({
        eventTypes: ['query-test'],
        agentIds: ['agent-alpha']
      });
      expect(combinedResults).toHaveLength(1);
      expect(combinedResults[0].action).toBe('action-one');
    });

    test('should respect limit and offset parameters', async () => {
      // Log 5 events
      for (let i = 0; i < 5; i++) {
        await lobsterOps.logEvent({
          type: 'pagination-test',
          index: i
        });
      }

      // Get first 2
      const firstPage = await lobsterOps.queryEvents({
        eventTypes: ['pagination-test'],
        limit: 2,
        offset: 0
      });
      expect(firstPage).toHaveLength(2);

      // Get next 2
      const secondPage = await lobsterOps.queryEvents({
        eventTypes: ['pagination-test'],
        limit: 2,
        offset: 2
      });
      expect(secondPage).toHaveLength(2);

      // Get last 1
      const thirdPage = await lobsterOps.queryEvents({
        eventTypes: ['pagination-test'],
        limit: 2,
        offset: 4
      });
      expect(thirdPage).toHaveLength(1);
    });

    test('should sort results correctly', async () => {
      // Log events with specific timestamps
      const times = [
        '2026-03-18T10:00:00Z',
        '2026-03-18T12:00:00Z',
        '2026-03-18T11:00:00Z'
      ];

      for (const time of times) {
        await lobsterOps.logEvent({
          type: 'sort-test',
          timestamp: time
        });
      }

      // Ascending order
      const ascResults = await lobsterOps.queryEvents({
        eventTypes: ['sort-test'],
        sortBy: 'timestamp',
        sortOrder: 'asc'
      });

      expect(ascResults[0].timestamp).toBe('2026-03-18T10:00:00Z');
      expect(ascResults[1].timestamp).toBe('2026-03-18T11:00:00Z');
      expect(ascResults[2].timestamp).toBe('2026-03-18T12:00:00Z');

      // Descending order
      const descResults = await lobsterOps.queryEvents({
        eventTypes: ['sort-test'],
        sortBy: 'timestamp',
        sortOrder: 'desc'
      });

      expect(descResults[0].timestamp).toBe('2026-03-18T12:00:00Z');
      expect(descResults[1].timestamp).toBe('2026-03-18T11:00:00Z');
      expect(descResults[2].timestamp).toBe('2026-03-18T10:00:00Z');
    });
  });

  describe('Event Updates', () => {
    test('should be able to update an existing event', async () => {
      const event = {
        type: 'update-test',
        status: 'pending',
        progress: 0
      };

      const eventId = await lobsterOps.logEvent(event);

      // Update the event
      const updateResult = await lobsterOps.updateEvent(eventId, {
        status: 'completed',
        progress: 100,
        result: 'success'
      });

      expect(updateResult).toBe(true);

      // Verify the update
      const updatedEvent = await lobsterOps.getEvent(eventId);
      expect(updatedEvent.status).toBe('completed');
      expect(updatedEvent.progress).toBe(100);
      expect(updatedEvent.result).toBe('success');
      expect(updatedEvent.updatedAt).toBeDefined();
    });

    test('should return false when updating non-existent event', async () => {
      const result = await lobsterOps.updateEvent('non-existent-id', {
        status: 'updated'
      });
      expect(result).toBe(false);
    });
  });

  describe('Event Deletion', () => {
    test('should be able to delete events by criteria', async () => {
      // Log events to delete and keep
      await lobsterOps.logEvent({
        type: 'delete-test',
        agentId: 'to-delete',
        shouldKeep: false
      });

      await lobsterOps.logEvent({
        type: 'delete-test',
        agentId: 'to-keep',
        shouldKeep: true
      });

      await lobsterOps.logEvent({
        type: 'other-type',
        agentId: 'to-delete',
        shouldKeep: false
      });

      // Delete events with agentId: 'to-delete'
      const deletedCount = await lobsterOps.deleteEvents({
        agentIds: ['to-delete']
      });

      expect(deletedCount).toBe(2);

      // Verify only the keep event remains
      const remainingEvents = await lobsterOps.queryEvents({
        eventTypes: ['delete-test']
      });
      expect(remainingEvents).toHaveLength(1);
      expect(remainingEvents[0].agentId).toBe('to-keep');
    });
  });

  describe('Storage Statistics', () => {
    test('should return accurate storage statistics', async () => {
      // Log some events
      await lobsterOps.logEvent({ type: 'stats-test', count: 1 });
      await lobsterOps.logEvent({ type: 'stats-test', count: 2 });

      const stats = await lobsterOps.getStats();

      expect(stats.enabled).toBe(true);
      expect(stats.instanceId).toBeDefined();
      expect(stats.storageType).toBe('json');
      expect(stats.backend).toBe('json-file');
      expect(stats.totalEvents).toBeGreaterThanOrEqual(2);
      expect(stats.dataDir).toBe('./test-lobsterops-data');
    });
  });

  describe('Cleanup Functionality', () => {
    test('should be able to cleanup old events', async () => {
      // This test mainly verifies the cleanup method doesn't throw
      // Actual age-based cleanup would require manipulating timestamps
      const initialStats = await lobsterOps.getStats();

      const cleanedCount = await lobsterOps.cleanupOld();

      const finalStats = await lobsterOps.getStats();

      expect(typeof cleanedCount).toBe('number');
      expect(cleanedCount >= 0).toBe(true);
    });
  });

  describe('PII Filtering Integration', () => {
    test('should filter PII from logged events', async () => {
      const opsWithPII = new LobsterOps({
        storageType: 'json',
        storageConfig: { dataDir: testDir },
        piiFiltering: { enabled: true }
      });
      await opsWithPII.init();

      const eventId = await opsWithPII.logEvent({
        type: 'pii-test',
        message: 'Contact user@example.com for details',
        phone: 'Call 555-123-4567'
      });

      const event = await opsWithPII.getEvent(eventId);
      expect(event.message).not.toContain('user@example.com');
      expect(event.message).toContain('[REDACTED]');
      expect(event.phone).toContain('[REDACTED]');

      await opsWithPII.close();
    });

    test('should not filter when PII filtering is disabled', async () => {
      const opsNoPII = new LobsterOps({
        storageType: 'json',
        storageConfig: { dataDir: testDir },
        piiFiltering: { enabled: false }
      });
      await opsNoPII.init();

      const eventId = await opsNoPII.logEvent({
        type: 'no-pii-test',
        message: 'Contact user@example.com'
      });

      const event = await opsNoPII.getEvent(eventId);
      expect(event.message).toContain('user@example.com');

      await opsNoPII.close();
    });
  });

  describe('Export Integration', () => {
    test('should export events to CSV', async () => {
      await lobsterOps.logEvent({ type: 'export-test', agentId: 'agent-1', action: 'test' });
      await lobsterOps.logEvent({ type: 'export-test', agentId: 'agent-2', action: 'test2' });

      const csv = await lobsterOps.exportEvents('csv', { eventTypes: ['export-test'] });
      expect(csv).toContain('id');
      expect(csv).toContain('type');
      expect(csv).toContain('export-test');
      expect(csv.split('\n').length).toBeGreaterThanOrEqual(3); // header + 2 rows
    });

    test('should export events to Markdown', async () => {
      await lobsterOps.logEvent({ type: 'md-test', agentId: 'agent-1' });

      const md = await lobsterOps.exportEvents('markdown', { eventTypes: ['md-test'] }, { title: 'Test Report' });
      expect(md).toContain('# Test Report');
      expect(md).toContain('**Total Events:**');
      expect(md).toContain('md-test');
    });

    test('should export events to JSON', async () => {
      await lobsterOps.logEvent({ type: 'json-test' });

      const json = await lobsterOps.exportEvents('json', { eventTypes: ['json-test'] });
      const parsed = JSON.parse(json);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed.length).toBeGreaterThanOrEqual(1);
    });
  });

  describe('Debug Console Integration', () => {
    test('should create a debug console for an agent trace', async () => {
      await lobsterOps.logEvent({ type: 'agent-thought', agentId: 'debug-agent', thought: 'thinking...' });
      await lobsterOps.logEvent({ type: 'tool-call', agentId: 'debug-agent', toolName: 'search' });
      await lobsterOps.logEvent({ type: 'agent-decision', agentId: 'debug-agent', decision: 'done' });

      const debug = await lobsterOps.createDebugConsole('debug-agent');
      expect(debug).toBeInstanceOf(DebugConsole);
      expect(debug.length).toBe(3);
    });
  });

  describe('Analytics Integration', () => {
    test('should run analytics on events', async () => {
      await lobsterOps.logEvent({ type: 'tool-call', agentId: 'a1', success: true, durationMs: 100, cost: 0.01 });
      await lobsterOps.logEvent({ type: 'tool-call', agentId: 'a1', success: false, durationMs: 200, cost: 0.02 });
      await lobsterOps.logEvent({ type: 'agent-error', agentId: 'a1', errorType: 'timeout' });

      const report = await lobsterOps.analyze({ agentIds: ['a1'] });
      expect(report.totalEvents).toBe(3);
      expect(report.successRate.totalToolCalls).toBe(2);
      expect(report.successRate.successful).toBe(1);
      expect(report.successRate.failed).toBe(1);
    });
  });
});

describe('Storage Factory', () => {
  test('should create JSON storage by default', () => {
    const storage = StorageFactory.createStorage();
    expect(storage).toBeInstanceOf(JsonFileStorage);
  });

  test('should create memory storage when requested', () => {
    const storage = StorageFactory.createStorage('memory');
    expect(storage).toBeInstanceOf(MemoryStorage);
  });

  test('should throw error for unsupported storage type', () => {
    expect(() => StorageFactory.createStorage('unsupported-type'))
      .toThrow('Unsupported storage type');
  });

  test('should auto-detect storage in test environment', () => {
    process.env.NODE_ENV = 'test';
    const storage = StorageFactory.createAutoStorage();
    expect(storage).toBeInstanceOf(MemoryStorage);
    delete process.env.NODE_ENV;
  });

  test('should respect explicit type over auto-detection', () => {
    process.env.NODE_ENV = 'test';
    const storage = StorageFactory.createAutoStorage({ type: 'json' });
    expect(storage).toBeInstanceOf(JsonFileStorage);
    delete process.env.NODE_ENV;
  });

  test('should list supported storage types', () => {
    const types = StorageFactory.getSupportedTypes();
    expect(types).toContain('json');
    expect(types).toContain('memory');
  });
});

describe('PIIFilter', () => {
  test('should redact email addresses', () => {
    const filter = new PIIFilter();
    expect(filter.filterString('Email me at user@example.com'))
      .toBe('Email me at [REDACTED]');
  });

  test('should redact phone numbers', () => {
    const filter = new PIIFilter();
    expect(filter.filterString('Call 555-123-4567'))
      .toBe('Call [REDACTED]');
  });

  test('should redact SSNs', () => {
    const filter = new PIIFilter();
    expect(filter.filterString('SSN: 123-45-6789'))
      .toBe('SSN: [REDACTED]');
  });

  test('should redact API keys', () => {
    const filter = new PIIFilter();
    expect(filter.filterString('Use key sk_live_abc123def456ghi789jkl0'))
      .toBe('Use key [REDACTED]');
  });

  test('should filter nested objects', () => {
    const filter = new PIIFilter();
    const result = filter.filter({
      name: 'Test',
      contact: { email: 'user@example.com', note: 'valid' },
      list: ['test@test.com', 'plain text']
    });
    expect(result.contact.email).toBe('[REDACTED]');
    expect(result.contact.note).toBe('valid');
    expect(result.list[0]).toBe('[REDACTED]');
    expect(result.list[1]).toBe('plain text');
  });

  test('should respect enabled flag', () => {
    const filter = new PIIFilter({ enabled: false });
    expect(filter.filterString('user@example.com')).toBe('user@example.com');
  });

  test('should allow selecting specific patterns', () => {
    const filter = new PIIFilter({ patterns: ['email'] });
    const result = filter.filterString('Email: user@example.com, Phone: 555-123-4567');
    expect(result).toContain('[REDACTED]');
    expect(result).toContain('555-123-4567');
  });

  test('should use custom replacement text', () => {
    const filter = new PIIFilter({ replacement: '***' });
    expect(filter.filterString('user@example.com')).toBe('***');
  });
});

describe('Exporter', () => {
  const sampleEvents = [
    { id: '1', type: 'tool-call', agentId: 'agent-1', action: 'search', timestamp: '2026-03-18T10:00:00Z' },
    { id: '2', type: 'agent-error', agentId: 'agent-1', action: 'fetch', timestamp: '2026-03-18T11:00:00Z' }
  ];

  test('should export to JSON', () => {
    const json = Exporter.toJSON(sampleEvents);
    const parsed = JSON.parse(json);
    expect(parsed).toHaveLength(2);
    expect(parsed[0].id).toBe('1');
  });

  test('should export to CSV', () => {
    const csv = Exporter.toCSV(sampleEvents);
    const lines = csv.split('\n');
    expect(lines.length).toBe(3); // header + 2 rows
    expect(lines[0]).toContain('id');
    expect(lines[0]).toContain('type');
  });

  test('should export to CSV with custom columns', () => {
    const csv = Exporter.toCSV(sampleEvents, { columns: ['id', 'type'] });
    const lines = csv.split('\n');
    expect(lines[0]).toBe('id,type');
  });

  test('should export to Markdown', () => {
    const md = Exporter.toMarkdown(sampleEvents, { title: 'Report' });
    expect(md).toContain('# Report');
    expect(md).toContain('**Total Events:** 2');
    expect(md).toContain('| id | type |');
  });

  test('should handle empty events', () => {
    expect(Exporter.toCSV([])).toBe('');
    expect(Exporter.toMarkdown([])).toBe('No events found.\n');
    expect(Exporter.toJSON([])).toBe('[]');
  });

  test('should escape CSV values with commas and quotes', () => {
    const events = [{ id: '1', message: 'hello, "world"' }];
    const csv = Exporter.toCSV(events, { columns: ['id', 'message'] });
    expect(csv).toContain('"hello, ""world"""');
  });
});

describe('DebugConsole', () => {
  const events = [
    { type: 'agent-thought', agentId: 'a1', thought: 'thinking', timestamp: '2026-03-18T10:00:00Z' },
    { type: 'tool-call', agentId: 'a1', toolName: 'search', toolInput: { q: 'test' }, toolOutput: { results: [] }, success: true, durationMs: 100, timestamp: '2026-03-18T10:01:00Z' },
    { type: 'agent-decision', agentId: 'a1', decision: 'use result', confidence: 0.9, timestamp: '2026-03-18T10:02:00Z' },
    { type: 'agent-error', agentId: 'a1', errorType: 'timeout', errorMessage: 'API timed out', severity: 'medium', recovered: true, timestamp: '2026-03-18T10:03:00Z' }
  ];

  test('should step forward and backward', () => {
    const debug = new DebugConsole(events);
    expect(debug.length).toBe(4);

    const first = debug.stepForward();
    expect(first.type).toBe('agent-thought');

    const second = debug.stepForward();
    expect(second.type).toBe('tool-call');

    const back = debug.stepBackward();
    expect(back.type).toBe('agent-thought');
  });

  test('should return null at boundaries', () => {
    const debug = new DebugConsole(events);
    expect(debug.stepBackward()).toBeNull(); // at start, can't go back

    debug.jumpToEnd();
    expect(debug.stepForward()).toBeNull(); // at end, can't go forward
  });

  test('should jump to positions', () => {
    const debug = new DebugConsole(events);
    const event = debug.jumpTo(2);
    expect(event.type).toBe('agent-decision');

    debug.jumpToStart();
    expect(debug.current().type).toBe('agent-thought');

    debug.jumpToEnd();
    expect(debug.current().type).toBe('agent-error');
  });

  test('should inspect events with type-specific details', () => {
    const debug = new DebugConsole(events);

    // Inspect thought
    debug.jumpTo(0);
    const thoughtInspection = debug.inspect();
    expect(thoughtInspection.thought.content).toBe('thinking');
    expect(thoughtInspection.position).toBe('1/4');

    // Inspect tool call
    debug.jumpTo(1);
    const toolInspection = debug.inspect();
    expect(toolInspection.toolCall.toolName).toBe('search');
    expect(toolInspection.toolCall.success).toBe(true);

    // Inspect decision
    debug.jumpTo(2);
    const decisionInspection = debug.inspect();
    expect(decisionInspection.decision.confidence).toBe(0.9);

    // Inspect error
    debug.jumpTo(3);
    const errorInspection = debug.inspect();
    expect(errorInspection.error.errorType).toBe('timeout');
    expect(errorInspection.error.recovered).toBe(true);
  });

  test('should search for events', () => {
    const debug = new DebugConsole(events);
    const errors = debug.search({ type: 'agent-error' });
    expect(errors).toHaveLength(1);
    expect(errors[0].index).toBe(3);

    const textSearch = debug.search({ text: 'search' });
    expect(textSearch.length).toBeGreaterThanOrEqual(1);
  });

  test('should generate a summary', () => {
    const debug = new DebugConsole(events);
    const summary = debug.summary();
    expect(summary.totalEvents).toBe(4);
    expect(summary.agents).toContain('a1');
    expect(summary.errorCount).toBe(1);
    expect(summary.eventTypes['tool-call']).toBe(1);
    expect(summary.eventTypes['agent-thought']).toBe(1);
  });

  test('should get tool calls and errors', () => {
    const debug = new DebugConsole(events);
    expect(debug.getToolCalls()).toHaveLength(1);
    expect(debug.getErrors()).toHaveLength(1);
    expect(debug.getDecisions()).toHaveLength(1);
  });

  test('should handle empty events', () => {
    const debug = new DebugConsole([]);
    expect(debug.length).toBe(0);
    expect(debug.stepForward()).toBeNull();
    expect(debug.summary().totalEvents).toBe(0);
  });
});

describe('Analytics', () => {
  const events = [
    { type: 'tool-call', agentId: 'a1', success: true, durationMs: 100, cost: 0.01, timestamp: '2026-03-18T10:00:00Z' },
    { type: 'tool-call', agentId: 'a1', success: true, durationMs: 200, cost: 0.02, timestamp: '2026-03-18T10:01:00Z' },
    { type: 'tool-call', agentId: 'a2', success: false, durationMs: 500, cost: 0.05, timestamp: '2026-03-18T10:02:00Z' },
    { type: 'agent-error', agentId: 'a1', errorType: 'timeout', severity: 'medium', timestamp: '2026-03-18T10:03:00Z' },
    { type: 'agent-error', agentId: 'a1', errorType: 'timeout', severity: 'high', timestamp: '2026-03-18T10:04:00Z' },
    { type: 'agent-thought', agentId: 'a1', thought: 'thinking', timestamp: '2026-03-18T10:05:00Z' }
  ];

  test('should calculate event type breakdown', () => {
    const breakdown = Analytics.eventTypeBreakdown(events);
    expect(breakdown['tool-call']).toBe(3);
    expect(breakdown['agent-error']).toBe(2);
    expect(breakdown['agent-thought']).toBe(1);
  });

  test('should calculate agent breakdown', () => {
    const agents = Analytics.agentBreakdown(events);
    expect(agents['a1'].eventCount).toBe(5);
    expect(agents['a1'].errors).toBe(2);
    expect(agents['a2'].eventCount).toBe(1);
  });

  test('should calculate success rate', () => {
    const rate = Analytics.successRate(events);
    expect(rate.totalToolCalls).toBe(3);
    expect(rate.successful).toBe(2);
    expect(rate.failed).toBe(1);
    expect(rate.rate).toBeCloseTo(66.67, 0);
  });

  test('should calculate performance metrics', () => {
    const metrics = Analytics.performanceMetrics(events);
    expect(metrics.minDurationMs).toBe(100);
    expect(metrics.maxDurationMs).toBe(500);
    expect(metrics.avgDurationMs).toBeCloseTo(267, 0);
    expect(metrics.totalMeasured).toBe(3);
  });

  test('should detect loops', () => {
    const loopEvents = [];
    for (let i = 0; i < 12; i++) {
      loopEvents.push({ type: i % 2 === 0 ? 'tool-call' : 'agent-thought', timestamp: new Date().toISOString() });
    }
    const loops = Analytics.detectLoops(loopEvents, { minRepetitions: 3, windowSize: 3 });
    expect(loops.length).toBeGreaterThan(0);
  });

  test('should identify failure patterns', () => {
    const patterns = Analytics.failurePatterns(events);
    expect(patterns.length).toBeGreaterThan(0);
    expect(patterns[0].type).toBe('timeout');
    expect(patterns[0].count).toBe(2);
  });

  test('should analyze costs', () => {
    const costs = Analytics.costAnalysis(events);
    expect(costs.totalCost).toBeCloseTo(0.08, 2);
    expect(costs.eventCount).toBe(3);
    expect(costs.costByAgent['a1']).toBeCloseTo(0.03, 2);
    expect(costs.costByAgent['a2']).toBeCloseTo(0.05, 2);
  });

  test('should produce full analysis report', () => {
    const report = Analytics.analyze(events);
    expect(report.totalEvents).toBe(6);
    expect(report.eventTypeBreakdown).toBeDefined();
    expect(report.successRate).toBeDefined();
    expect(report.performanceMetrics).toBeDefined();
    expect(report.costAnalysis).toBeDefined();
  });

  test('should handle empty events', () => {
    const report = Analytics.analyze([]);
    expect(report.totalEvents).toBe(0);
    expect(report.successRate).toBeNull();
  });
});

describe('AlertManager', () => {
  test('should add and list rules', () => {
    const mgr = new AlertManager();
    const ruleId = mgr.addRule({
      name: 'test-rule',
      type: 'threshold',
      condition: { field: 'cost', operator: '>', value: 1.0 },
      severity: 'high'
    });
    expect(typeof ruleId).toBe('string');
    expect(mgr.getRules()).toHaveLength(1);
  });

  test('should remove rules', () => {
    const mgr = new AlertManager();
    const ruleId = mgr.addRule({ name: 'temp', type: 'threshold', condition: { field: 'cost', operator: '>', value: 1 } });
    expect(mgr.removeRule(ruleId)).toBe(true);
    expect(mgr.getRules()).toHaveLength(0);
    expect(mgr.removeRule('nonexistent')).toBe(false);
  });

  test('should trigger threshold alerts', () => {
    const mgr = new AlertManager();
    mgr.addRule({
      name: 'high-cost',
      type: 'threshold',
      condition: { field: 'cost', operator: '>', value: 0.5 },
      severity: 'high',
      message: 'Cost too high for {type}'
    });

    const alerts1 = mgr.evaluate({ type: 'tool-call', cost: 0.3, id: '1', timestamp: new Date().toISOString() });
    expect(alerts1).toHaveLength(0);

    const alerts2 = mgr.evaluate({ type: 'tool-call', cost: 1.5, id: '2', timestamp: new Date().toISOString() });
    expect(alerts2).toHaveLength(1);
    expect(alerts2[0].severity).toBe('high');
    expect(alerts2[0].message).toContain('tool-call');
  });

  test('should trigger pattern alerts', () => {
    const mgr = new AlertManager();
    mgr.addRule({
      name: 'error-pattern',
      type: 'pattern',
      condition: { eventType: 'agent-error', field: 'errorMessage', regex: 'timeout' },
      severity: 'medium'
    });

    const alerts = mgr.evaluate({ type: 'agent-error', errorMessage: 'API timeout occurred', id: '1', timestamp: new Date().toISOString() });
    expect(alerts).toHaveLength(1);
  });

  test('should call listeners when alerts fire', () => {
    const mgr = new AlertManager();
    const received = [];
    mgr.onAlert(alert => received.push(alert));

    mgr.addRule({
      name: 'listener-test',
      type: 'threshold',
      condition: { field: 'cost', operator: '>=', value: 0 },
      severity: 'low'
    });

    mgr.evaluate({ type: 'test', cost: 5, id: '1', timestamp: new Date().toISOString() });
    expect(received).toHaveLength(1);
  });

  test('should get and clear alerts', () => {
    const mgr = new AlertManager();
    mgr.addRule({
      name: 'test',
      type: 'threshold',
      condition: { field: 'cost', operator: '>', value: 0 },
      severity: 'high'
    });
    mgr.evaluate({ type: 'test', cost: 1, id: '1', timestamp: new Date().toISOString() });

    expect(mgr.getAlerts()).toHaveLength(1);
    expect(mgr.getAlerts({ severity: 'high' })).toHaveLength(1);
    expect(mgr.getAlerts({ severity: 'low' })).toHaveLength(0);

    mgr.clearAlerts();
    expect(mgr.getAlerts()).toHaveLength(0);
  });

  test('should evaluate all events in bulk', () => {
    const mgr = new AlertManager();
    mgr.addRule({
      name: 'bulk-test',
      type: 'threshold',
      condition: { field: 'cost', operator: '>', value: 0.5 },
      severity: 'medium'
    });

    const events = [
      { type: 'test', cost: 0.1, id: '1', timestamp: new Date().toISOString() },
      { type: 'test', cost: 1.0, id: '2', timestamp: new Date().toISOString() },
      { type: 'test', cost: 0.2, id: '3', timestamp: new Date().toISOString() },
      { type: 'test', cost: 2.0, id: '4', timestamp: new Date().toISOString() }
    ];

    const alerts = mgr.evaluateAll(events);
    expect(alerts).toHaveLength(2);
  });
});

describe('OpenClawInstrumentation', () => {
  let ops;
  const testDir = './test-instrumentation-data';

  beforeEach(async () => {
    const fs = require('fs').promises;
    try { await fs.rm(testDir, { recursive: true, force: true }); } catch (e) {}
    ops = new LobsterOps({ storageType: 'json', storageConfig: { dataDir: testDir } });
    await ops.init();
  });

  afterEach(async () => {
    await ops.close();
    const fs = require('fs').promises;
    try { await fs.rm(testDir, { recursive: true, force: true }); } catch (e) {}
  });

  test('should create instrumentation and activate/deactivate', () => {
    const inst = new OpenClawInstrumentation(ops);
    expect(inst.isActive()).toBe(false);
    inst.activate();
    expect(inst.isActive()).toBe(true);
    inst.deactivate();
    expect(inst.isActive()).toBe(false);
  });

  test('should instrument tool calls', async () => {
    const inst = new OpenClawInstrumentation(ops);
    inst.activate();

    const eventId = await inst.instrumentToolCall({
      agentId: 'test-agent',
      toolName: 'web-search',
      input: { q: 'test' },
      output: { results: [] },
      durationMs: 100,
      success: true
    });

    expect(eventId).toBeDefined();
    const event = await ops.getEvent(eventId);
    expect(event.type).toBe('tool-call');
    expect(event.toolName).toBe('web-search');
  });

  test('should instrument spawns', async () => {
    const inst = new OpenClawInstrumentation(ops);
    inst.activate();

    const eventId = await inst.instrumentSpawn({
      parentId: 'parent-agent',
      childId: 'child-agent',
      type: 'research',
      task: 'analyze data'
    });

    expect(eventId).toBeDefined();
    const event = await ops.getEvent(eventId);
    expect(event.type).toBe('agent-spawn');
  });

  test('should instrument lifecycle events', async () => {
    const inst = new OpenClawInstrumentation(ops);
    inst.activate();

    const eventId = await inst.instrumentLifecycle({
      agentId: 'test-agent',
      action: 'startup',
      status: 'healthy'
    });

    expect(eventId).toBeDefined();
    const event = await ops.getEvent(eventId);
    expect(event.type).toBe('agent-lifecycle');
  });

  test('should respect capture options', async () => {
    const inst = new OpenClawInstrumentation(ops, { captureToolCalls: false });
    inst.activate();

    const result = await inst.instrumentToolCall({ toolName: 'test' });
    expect(result).toBeNull();
  });

  test('should not instrument when inactive', async () => {
    const inst = new OpenClawInstrumentation(ops);
    // Not activated
    const result = await inst.instrumentToolCall({ toolName: 'test' });
    expect(result).toBeNull();
  });

  test('should create from config', () => {
    const inst = OpenClawInstrumentation.fromConfig(ops, {
      captureFileChanges: true,
      captureGitOps: true
    });
    expect(inst).toBeInstanceOf(OpenClawInstrumentation);
    expect(inst.options.captureFileChanges).toBe(true);
  });
});
