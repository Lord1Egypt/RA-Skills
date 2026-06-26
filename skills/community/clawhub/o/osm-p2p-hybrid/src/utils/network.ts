/**
 * 网络工具函数
 */

import { networkInterfaces } from 'os';
import type { NodeAddress } from '../types.js';

interface NetworkIP {
  address: string;
  type: 'local' | 'vpn' | 'public';
}

/**
 * 获取本机所有网络 IP
 */
export function getNetworkIPs(): NetworkIP[] {
  const interfaces = networkInterfaces();
  const ips: NetworkIP[] = [];

  for (const [name, addrs] of Object.entries(interfaces)) {
    if (!addrs) continue;

    for (const addr of addrs) {
      // 只取 IPv4
      if (addr.family !== 'IPv4' || addr.internal) continue;

      const ip = addr.address;
      let type: 'local' | 'vpn' | 'public' = 'public';

      // 判断类型
      if (ip.startsWith('127.')) {
        continue; // 跳过本地回环
      } else if (
        ip.startsWith('10.') ||
        ip.startsWith('192.168.') ||
        (ip.startsWith('172.') && parseInt(ip.split('.')[1]) >= 16 && parseInt(ip.split('.')[1]) <= 31)
      ) {
        type = 'local';
      } else if (
        ip.startsWith('100.') ||
        ip.startsWith('fd00:') ||
        ip.startsWith('fc00:')
      ) {
        type = 'vpn'; // Tailscale/ZeroTier
      }

      ips.push({ address: ip, type });
    }
  }

  return ips;
}

/**
 * 检查 IP 是否在同一个局域网
 */
export function isSameLAN(ip1: string, ip2: string): boolean {
  // 简单实现：检查前三个 octet 是否相同
  const parts1 = ip1.split('.');
  const parts2 = ip2.split('.');
  
  if (parts1.length !== 4 || parts2.length !== 4) return false;
  
  return parts1[0] === parts2[0] && 
         parts1[1] === parts2[1] && 
         parts1[2] === parts2[2];
}

/**
 * 生成随机 ID
 */
export function generateId(length: number = 8): string {
  return Math.random().toString(36).substring(2, 2 + length);
}

/**
 * 延迟函数
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
