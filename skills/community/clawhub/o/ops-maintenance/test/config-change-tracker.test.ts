/**
 * ConfigChangeTracker 单元测试
 */

import { existsSync, mkdirSync, unlinkSync } from 'fs'
import { join } from 'path'
import { ConfigChangeTracker, DEFAULT_TRACKED_FILES } from '../skills/ops-maintenance/src/utils/config-change-tracker'

const configDir = join(process.env.HOME || '~', '.config/ops-maintenance')
const trackerFile = join(configDir, 'config-tracker.json')
const historyFile = join(configDir, 'config-changes.json')

describe('ConfigChangeTracker', () => {
  let tracker: ConfigChangeTracker

  beforeEach(() => {
    // 清理测试文件
    for (const f of [trackerFile, historyFile]) {
      if (existsSync(f)) {
        try { unlinkSync(f) } catch {}
      }
    }
    tracker = new ConfigChangeTracker()
  })

  afterEach(() => {
    for (const f of [trackerFile, historyFile]) {
      if (existsSync(f)) {
        try { unlinkSync(f) } catch {}
      }
    }
  })

  it('应该正确初始化', () => {
    expect(tracker).toBeDefined()
  })

  it('应该返回默认追踪文件列表', () => {
    const files = tracker.getTrackedFiles()
    expect(files.length).toBeGreaterThan(0)
    expect(files[0].path).toBeTruthy()
  })

  it('应该能够添加文件到追踪列表', () => {
    tracker.addFile('/tmp/test.conf', 'test-config')
    const files = tracker.getTrackedFiles()
    const found = files.find(f => f.path === '/tmp/test.conf')
    expect(found).toBeDefined()
    expect(found?.alias).toBe('test-config')
  })

  it('应该能够移除文件', () => {
    tracker.addFile('/tmp/test.conf', 'test-config')
    const removed = tracker.removeFile('/tmp/test.conf')
    expect(removed).toBe(true)
    const files = tracker.getTrackedFiles()
    expect(files.find(f => f.path === '/tmp/test.conf')).toBeUndefined()
  })

  it('应该移除不存在的文件返回false', () => {
    const removed = tracker.removeFile('/nonexistent/path')
    expect(removed).toBe(false)
  })

  it('DEFAULT_TRACKED_FILES 应该包含关键配置文件', () => {
    const paths = DEFAULT_TRACKED_FILES.map(f => f.path)
    expect(paths).toContain('/etc/nginx/nginx.conf')
    expect(paths).toContain('/etc/ssh/sshd_config')
  })
})
