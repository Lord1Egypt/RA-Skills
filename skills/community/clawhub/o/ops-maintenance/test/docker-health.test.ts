/**
 * Docker 健康检查单元测试
 */

import { DockerHealthChecker } from '../skills/ops-maintenance/src/utils/docker-health-checker'

describe('DockerHealthChecker', () => {
  let checker: DockerHealthChecker

  beforeEach(() => {
    checker = new DockerHealthChecker()
  })

  it('应该正确初始化', () => {
    expect(checker).toBeDefined()
  })

  it('检测 Docker 可用性', async () => {
    const available = await checker.isDockerAvailable()
    // Docker 可能在某些环境下不可用，应该返回 boolean 而不是抛出异常
    expect(typeof available).toBe('boolean')
  })

  it('获取容器列表', async () => {
    const containers = await checker.getAllContainers()
    expect(Array.isArray(containers)).toBe(true)
  })

  it('运行完整巡检', async () => {
    const result = await checker.runFullInspection()
    expect(result).toBeDefined()
    expect(result).toHaveProperty('summary')
  })
})
