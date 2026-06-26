/**
 * IdentityManager - 身份管理器
 * 管理节点身份、密钥和名片
 */

import { randomBytes, createHash } from 'crypto';
import { writeFile, readFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import type { NodeIdentity, NodeAddress, NodeCard } from '../types.js';
import { getNetworkIPs } from '../utils/network.js';

export class IdentityManager {
  private identity: NodeIdentity | null = null;
  private dataDir: string;
  private identityPath: string;

  constructor(dataDir: string) {
    this.dataDir = dataDir;
    this.identityPath = join(dataDir, 'identity.json');
  }

  /**
   * 初始化身份
   * @param nodeId 节点ID
   * @param name 显示名称
   */
  async init(nodeId: string, name: string): Promise<NodeIdentity> {
    // 确保目录存在
    if (!existsSync(this.dataDir)) {
      await mkdir(this.dataDir, { recursive: true });
    }

    // 尝试加载已有身份
    if (existsSync(this.identityPath)) {
      try {
        const data = await readFile(this.identityPath, 'utf-8');
        const saved = JSON.parse(data);
        
        // 更新动态信息
        this.identity = {
          ...saved,
          nodeId: nodeId || saved.nodeId,
          name: name || saved.name,
          addrs: await this.getCurrentAddresses(),
          lastSeen: Date.now(),
        };
        
        console.log(`✓ 加载已有身份: ${this.identity.nodeId}`);
      } catch (e) {
        console.log('! 身份文件损坏，创建新身份');
      }
    }

    // 创建新身份
    if (!this.identity) {
      this.identity = await this.createNewIdentity(nodeId, name);
      await this.save();
      console.log(`✓ 创建新身份: ${this.identity.nodeId}`);
    }

    return this.identity;
  }

  /**
   * 创建新身份
   */
  private async createNewIdentity(nodeId: string, name: string): Promise<NodeIdentity> {
    // 生成 Nostr 密钥对
    const { getPublicKey, generateSecretKey } = await import('nostr-tools');
    const privateKey = generateSecretKey();
    const pubkey = getPublicKey(privateKey);

    return {
      nodeId: nodeId || `node-${this.generateRandomId()}`,
      name: name || 'Anonymous',
      nostr: {
        pubkey,
        privateKey,
      },
      addrs: await this.getCurrentAddresses(),
      capabilities: ['chat', 'file', 'gossip'],
      version: '1.0.0',
      lastSeen: Date.now(),
    };
  }

  /**
   * 获取当前网络地址
   */
  private async getCurrentAddresses(): Promise<NodeAddress[]> {
    const ips = getNetworkIPs();
    return ips.map(ip => ({
      ip: ip.address,
      port: 37291,
      type: ip.type,
    }));
  }

  /**
   * 获取身份
   */
  getIdentity(): NodeIdentity {
    if (!this.identity) {
      throw new Error('Identity not initialized');
    }
    return this.identity;
  }

  /**
   * 获取 Nostr 公钥
   */
  getPubkey(): string | undefined {
    return this.identity?.nostr?.pubkey;
  }

  /**
   * 获取 Nostr 私钥
   */
  getPrivateKey(): Uint8Array | undefined {
    return this.identity?.nostr?.privateKey;
  }

  /**
   * 更新地址列表
   */
  async updateAddresses(): Promise<void> {
    if (!this.identity) return;
    
    this.identity.addrs = await this.getCurrentAddresses();
    this.identity.lastSeen = Date.now();
    await this.save();
  }

  /**
   * 添加能力
   */
  addCapability(cap: string): void {
    if (!this.identity) return;
    if (!this.identity.capabilities.includes(cap)) {
      this.identity.capabilities.push(cap);
    }
  }

  /**
   * 生成名片 (osm:// URL)
   */
  generateCard(vipPort?: number): string {
    if (!this.identity) {
      throw new Error('Identity not initialized');
    }

    const card: NodeCard = {
      n: this.identity.name,
      i: this.identity.addrs.map(a => a.ip),
      p: 37291,
    };

    if (this.identity.nostr) {
      card.pub = this.identity.nostr.pubkey;
    }

    if (vipPort) {
      card.pubp = vipPort;
    }

    const json = JSON.stringify(card);
    const base64 = Buffer.from(json).toString('base64');
    return `osm://${base64}`;
  }

  /**
   * 解析名片
   */
  static parseCard(url: string): NodeCard | null {
    try {
      if (!url.startsWith('osm://')) {
        return null;
      }

      const base64 = url.slice(6);
      const json = Buffer.from(base64, 'base64').toString('utf-8');
      return JSON.parse(json);
    } catch (e) {
      return null;
    }
  }

  /**
   * 保存身份到文件
   */
  private async save(): Promise<void> {
    if (!this.identity) return;

    // 转换私钥为 base64 以便 JSON 序列化
    const data = {
      ...this.identity,
      nostr: this.identity.nostr ? {
        pubkey: this.identity.nostr.pubkey,
        privateKey: Buffer.from(this.identity.nostr.privateKey).toString('base64'),
      } : undefined,
    };

    await writeFile(this.identityPath, JSON.stringify(data, null, 2));
  }

  /**
   * 生成随机 ID
   */
  private generateRandomId(): string {
    return randomBytes(4).toString('hex');
  }
}
