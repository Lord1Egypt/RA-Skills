import { afterEach, describe, expect, it } from 'vitest'
import { existsSync, unlinkSync } from 'node:fs'
import { TaskDetector, TaskLedger, AnalyticsEngine, createTaskRecord, VERSION } from '../src/index.js'

const dbFiles = new Set()

afterEach(() => {
  for (const base of dbFiles) {
    for (const suffix of ['', '-shm', '-wal']) {
      const file = `${base}${suffix}`
      if (existsSync(file)) unlinkSync(file)
    }
  }
  dbFiles.clear()
})

describe('OpenClaw Tally', () => {
  it('exports the release version and validates records', () => {
    expect(VERSION).toBe('0.3.2')
    const task = createTaskRecord({ task_id: 'tsk_123456789012' })
    expect(task.status).toBe('in_progress')
    expect(task.complexity_level).toBe('L1')
  })

  it('detects task boundaries and computes bounded complexity', async () => {
    const detector = new TaskDetector()
    expect((await detector.detect('Please build a report')).event).toBe('TASK_START')
    expect((await detector.detect('Done and delivered')).event).toBe('TASK_COMPLETE')
    expect(detector.computeComplexity({ toolsCalled: 30, subAgents: 5 })).toEqual({
      score: 100,
      level: 'L4',
    })
  })

  it('persists task metadata locally and computes TES', () => {
    const dbPath = `/tmp/openclaw-tally-${process.pid}-${Date.now()}.db`
    dbFiles.add(dbPath)
    const ledger = new TaskLedger(dbPath).init()

    ledger.startTask('tsk_123456789012', {
      complexity_score: 20,
      complexity_level: 'L2',
      models_used: ['test/model'],
    })
    ledger.attributeCost('tsk_123456789012', 1200, 0.02, 'test/model', 'main')
    ledger.completeTask('tsk_123456789012', 0.9, 'verified')

    const task = ledger.getTask('tsk_123456789012')
    const tes = new AnalyticsEngine(ledger).computeTES(task)
    expect(task.total_tokens).toBe(1200)
    expect(task.total_cost_usd).toBeCloseTo(0.02)
    expect(tes).toBeGreaterThan(0)
    ledger.db.close()
  })

  it('rejects database paths outside the declared local boundary', () => {
    expect(() => new TaskLedger('/var/tmp/tally.db')).toThrow(
      'Database path must be within ~/.openclaw/tally/ or /tmp/'
    )
  })
})
