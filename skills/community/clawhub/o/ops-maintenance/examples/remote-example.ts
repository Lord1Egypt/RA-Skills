/**
 * 远程运维使用示例
 * 
 * 使用前先在 ~/.config/ops-maintenance/servers.json 中配置服务器
 */

import { 
  executeRemoteOp, 
  checkRemoteHealth,
  checkRemotePort,
  checkRemoteProcess,
  checkRemoteDisk,
  uploadFile,
  downloadFile,
  listRemoteDirectory,
  type SSHConfig 
} from '../src/index.ts'

/**
 * 示例: 使用配置文件中的服务器
 */
export async function exampleWithConfig() {
  const { loadServers } = await import('../src/index.ts')
  const configs = await loadServers()
  
  for (const config of configs) {
    console.log(`\n=== 检查服务器: ${config.host} ===`)
    
    // 执行各种检查
    console.log(await checkRemoteHealth(config))
    console.log(await checkRemotePort(config, 80))
    console.log(await checkRemoteProcess(config, 'nginx'))
    console.log(await checkRemoteDisk(config))
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
 * 示例: 文件传输
 */
export async function exampleFileTransfer() {
  const server: SSHConfig = {
    host: 'your-server.com',
    port: 22,
    user: 'root',
    keyFile: '~/.ssh/id_rsa'
  }
  
  // 上传文件
  console.log(await uploadFile(server, './local-file.txt', '/tmp/remote-file.txt'))
  
  // 下载文件
  console.log(await downloadFile(server, '/tmp/remote-file.txt', './downloaded-file.txt'))
  
  // 列出目录
  console.log(await listRemoteDirectory(server, '/tmp'))
}

/**
 * 快速测试远程连接
 */
export async function testRemote(host: string) {
  const config: SSHConfig = { host }
  
  console.log(`测试连接: ${host}`)
  console.log(await checkRemoteHealth(config))
}
