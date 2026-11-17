/**
 * SSH 客户端 - 简化可运行版本
 */

import { Client } from 'ssh2'
import type { Server, ISSHClient, SSHCredentials, ICredentialsProvider } from '../config/schemas'
import { readFileSync } from 'fs'

export class SSHClient implements ISSHClient {
  private connections: Map<string, any> = new Map()
  private credentialsProvider?: ICredentialsProvider

  setCredentialsProvider(provider: ICredentialsProvider): void {
    this.credentialsProvider = provider
  }

  async execute(server: Server, command: string, timeout: number = 30000): Promise<string> {
    const conn = await this.getConnection(server)

    return new Promise((resolve, reject) => {
      conn.exec(command, (err: any, stream: any) => {
        if (err) {
          this.closeConnection(server)
          return reject(new Error(`SSH 执行失败: ${err.message}`))
        }

        let output = ''
        stream.on('data', (data: Buffer) => output += data.toString())
        stream.on('close', (code?: number) => {
          if (code !== 0) {
            reject(new Error(`退出码 ${code}: ${output.substring(0, 200)}`))
          } else {
            resolve(output.trim())
          }
        })
      })

      setTimeout(() => {
        if (conn.isAuthenticated && conn.isAuthenticated()) {
          conn.requestForcePseudoTerminal((err: any) => { if (!err) conn.end() })
        }
        reject(new Error(`超时: ${command}`))
      }, timeout)
    })
  }

  async testConnection(server: Server): Promise<boolean> {
    try {
      const conn = await this.connect(server)
      this.connections.set(server.getKey(), conn)
      return true
    } catch { return false }
  }

  private async getConnection(server: Server): Promise<any> {
    const key = server.getKey()
    let conn = this.connections.get(key)

    if (conn && this.isAlive(conn)) return conn

    conn = await this.connect(server)
    this.connections.set(key, conn)
    return conn
  }

  private async connect(server: Server): Promise<any> {
    return new Promise((resolve, reject) => {
      const conn = new Client()

      const connectOptions: any = {
        host: server.host,
        port: server.port,
        username: server.user,
        readyTimeout: 30000,
        keepaliveInterval: 10000
      }

      ;(async () => {
        try {
          if (this.credentialsProvider) {
            const credentials = await this.credentialsProvider.getCredentials(server)
            if (credentials) {
              if (credentials.keyContent) {
                connectOptions.privateKey = Buffer.from(credentials.keyContent)
              } else if (credentials.keyFile) {
                connectOptions.privateKey = readFileSync(credentials.keyFile)
              } else if (credentials.password) {
                connectOptions.password = credentials.password
              }
            }
          }
          conn.connect(connectOptions)
        } catch (err: any) {
          reject(new Error(`连接失败: ${err.message}`))
        }
      })()

      conn.on('ready', () => resolve(conn))
      conn.on('error', (err: any) => reject(new Error(`SSH错误: ${err.message}`)))
      conn.on('close', () => this.connections.delete(server.getKey()))
    })
  }

  private isAlive(conn: any): boolean {
    return conn.isAuthenticated && conn.isAuthenticated() && !conn.isDestroyed
  }

  async disconnect(server: Server): Promise<void> {
    const key = server.getKey()
    const conn = this.connections.get(key)
    if (conn) {
      conn.end()
      this.connections.delete(key)
    }
  }

  async disconnectAll(): Promise<void> {
    for (const [_, conn] of this.connections) conn.end()
    this.connections.clear()
  }

  getActiveConnectionsCount(): number {
    return this.connections.size
  }
}