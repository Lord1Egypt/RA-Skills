/**
 * 远程运维使用示例
 * 
 * 使用前先在 ~/.ssh/config 中配置服务器
 */

import {
  loadSSHConfig,
  executeRemoteOp,
  checkRemoteHealth,
  checkRemotePort,
  checkRemoteProcess,
  checkRemoteDisk,
  type SSHConfig
} from '../src/index.ts'

/**
 * 示例: 使用 SSH config 中配置的服务器
 */
export async function exampleWithSSHConfig() {
  // 从 ~/.ssh/config 加载配置
  const configs = await loadSSHConfig()

  for (const config of configs) {
    console.log(`\n=== 检查服务器: ${config.host} ===`)

    // 执行各种检查
    console.log(await checkRemoteHealth(config))
    console.log(await checkRemotePort(config, 80))
    console.log(await checkRemoteProcess(config, 'nginx'))
    console.log(await checkRemoteDisk(config))
    // 密码过期检查请使用: /ops-maintenance password
  }
}

/**
 * 示例: 手动指定服务器
 */
export async function exampleManualConfig() {
  const server: SSHConfig = {
    host: 'your-server.com',
    port: 22,
    user: 'root',
    keyFile: '~/.ssh/id_rsa'
  }

  console.log(await executeRemoteOp('health', server))
  console.log(await executeRemoteOp('ports', server, '8080'))
  console.log(await executeRemoteOp('disk', server))
}

/**
 * 快速测试远程连接
 */
export async function testRemote(host: string) {
  const config: SSHConfig = { host }
  
  console.log(`测试连接: ${host}`)
  console.log(await checkRemoteHealth(config))
}