/**
 * 多服务器集群配置示例
 * 
 * 使用方法:
 * 1. 运行此脚本添加服务器
 * 2. 使用 cluster 命令查看状态
 */

import {
  addServer,
  removeServer,
  getServersByTag,
  checkAllServersHealth,
  executeOnAllServers,
  getClusterSummary,
  loadServers,
  checkAllServersPasswordExpirationReport,
  type SSHConfig
} from '../src/index.ts'

/**
 * 初始化示例服务器配置
 */
export async function initExampleServers() {
  const servers: SSHConfig[] = [
    {
      host: '192.168.1.100',
      user: 'root',
      port: 22,
      name: 'web-1',
      tags: ['production', 'web', 'nginx']
    },
    {
      host: '192.168.1.101', 
      user: 'root',
      port: 22,
      name: 'web-2',
      tags: ['production', 'web', 'nginx']
    },
    {
      host: '192.168.1.200',
      user: 'admin',
      port: 22,
      name: 'db-master',
      tags: ['production', 'database', 'mysql']
    },
    {
      host: '192.168.1.201',
      user: 'admin', 
      port: 22,
      name: 'db-slave',
      tags: ['production', 'database', 'mysql']
    },
    {
      host: '192.168.1.50',
      user: 'dev',
      port: 22,
      name: 'dev-server',
      tags: ['development', 'test']
    }
  ]
  
  console.log('添加示例服务器配置...')
  for (const server of servers) {
    await addServer(server)
  }
  console.log('✅ 已添加', servers.length, '台服务器')
}

/**
 * 查看所有服务器
 */
export async function listServers() {
  const servers = await loadServers()
  console.log('\\n=== 服务器列表 ===')
  for (const s of servers) {
    console.log(`${s.name || s.host} (${s.user || 'default'}@${s.host}) [${s.tags?.join(', ')}]`)
  }
}

/**
 * 按标签查看服务器
 */
export async function listByTag(tag: string) {
  const servers = await getServersByTag(tag)
  console.log(`\\n=== ${tag} 组服务器 ===`)
  for (const s of servers) {
    console.log(`${s.name || s.host}`)
  }
}

/**
 * 集群健康检查
 */
export async function clusterHealth() {
  console.log(await getClusterSummary())
}

/**
 * 批量执行命令
 */
export async function batchExecute(cmd: string, tag?: string) {
  const tags = tag ? [tag] : undefined
  const results = await executeOnAllServers(cmd, tags)

  console.log('\\n=== 批量执行结果 ===')
  for (const r of results) {
    console.log(`\\n>>> ${r.server}:`)
    console.log(r.output)
  }
}

/**
 * 集群服务器密码过期检查
 */
export async function checkServersPassword() {
  console.log(await checkAllServersPasswordExpirationReport())
}

// 如果直接运行此脚本
// Deno: deno run --allow-all examples/cluster-example.ts
// Node: npx tsx examples/cluster-example.ts