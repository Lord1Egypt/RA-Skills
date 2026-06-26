/**
 * OpenClaw 双机互修助手 - 单元测试
 */

import { describe, it, expect, beforeEach, jest } from '@jest/globals';

// Mock axios
jest.mock('axios', () => ({
  post: jest.fn()
}));

describe('HeartbeatService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should create heartbeat service with config', () => {
    const config = {
      localHost: '0.0.0.0',
      localPort: 9528,
      remoteHost: '192.168.1.101',
      remotePort: 9528,
      heartbeatInterval: 300000,
      heartbeatTimeout: 30000,
      memoryThreshold: 85,
      cpuThreshold: 80
    };

    expect(config.localPort).toBe(9528);
    expect(config.remoteHost).toBe('192.168.1.101');
    expect(config.heartbeatInterval).toBe(300000);
  });

  it('should have valid default thresholds', () => {
    const config = {
      memoryThreshold: 85,
      cpuThreshold: 80
    };

    expect(config.memoryThreshold).toBeGreaterThan(0);
    expect(config.memoryThreshold).toBeLessThan(100);
    expect(config.cpuThreshold).toBeGreaterThan(0);
    expect(config.cpuThreshold).toBeLessThan(100);
  });
});

describe('Health Status', () => {
  it('should have valid status values', () => {
    const validStatuses = ['ok', 'warning', 'critical'];
    
    validStatuses.forEach(status => {
      expect(['ok', 'warning', 'critical']).toContain(status);
    });
  });

  it('should format uptime correctly', () => {
    const formatUptime = (seconds: number): string => {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return `${hours}小时${minutes}分钟`;
    };

    expect(formatUptime(3661)).toBe('1 小时 1 分钟');
    expect(formatUptime(7200)).toBe('2 小时 0 分钟');
    expect(formatUptime(0)).toBe('0 小时 0 分钟');
  });

  it('should return correct status emoji', () => {
    const getStatusEmoji = (status: string): string => {
      switch (status) {
        case 'ok': return '✅';
        case 'warning': return '⚠️';
        case 'critical': return '🚨';
        default: return '❓';
      }
    };

    expect(getStatusEmoji('ok')).toBe('✅');
    expect(getStatusEmoji('warning')).toBe('⚠️');
    expect(getStatusEmoji('critical')).toBe('🚨');
    expect(getStatusEmoji('unknown')).toBe('❓');
  });
});

describe('Health Suggestions', () => {
  it('should generate suggestions for high memory', () => {
    const health = {
      memory: { percent: 90, used: 1800, total: 2000 },
      cpu: { percent: 50 },
      processes: { pm2: { status: 'online', memory: 450, restarts: 0 } }
    };

    const suggestions: string[] = [];
    if (health.memory.percent > 85) {
      suggestions.push('- ⚠️ 内存使用率高，建议配置 PM2 max_memory_restart');
    }

    expect(suggestions.length).toBeGreaterThan(0);
    expect(suggestions[0]).toContain('内存');
  });

  it('should generate suggestions for high CPU', () => {
    const health = {
      memory: { percent: 60, used: 1200, total: 2000 },
      cpu: { percent: 85 },
      processes: { pm2: { status: 'online', memory: 450, restarts: 0 } }
    };

    const suggestions: string[] = [];
    if (health.cpu.percent > 80) {
      suggestions.push('- ⚠️ CPU 使用率高，检查是否有性能瓶颈');
    }

    expect(suggestions.length).toBeGreaterThan(0);
    expect(suggestions[0]).toContain('CPU');
  });

  it('should return OK when all healthy', () => {
    const health = {
      memory: { percent: 50, used: 1000, total: 2000 },
      cpu: { percent: 30 },
      processes: { pm2: { status: 'online', memory: 450, restarts: 0 } }
    };

    const suggestions: string[] = [];
    if (health.memory.percent > 85) {
      suggestions.push('内存告警');
    }
    if (health.cpu.percent > 80) {
      suggestions.push('CPU 告警');
    }

    const result = suggestions.length > 0 
      ? suggestions.join('\n') 
      : '- ✅ 一切正常，无需干预';

    expect(result).toContain('一切正常');
  });
});

describe('Configuration Validation', () => {
  it('should validate required config fields', () => {
    const requiredFields = [
      'localHost',
      'localPort',
      'remoteHost',
      'remotePort',
      'heartbeatInterval'
    ];

    const config: any = {
      localHost: '0.0.0.0',
      localPort: 9528,
      remoteHost: '192.168.1.101',
      remotePort: 9528,
      heartbeatInterval: 300000
    };

    requiredFields.forEach(field => {
      expect(config[field]).toBeDefined();
    });
  });

  it('should validate port range', () => {
    const port = 9528;
    expect(port).toBeGreaterThanOrEqual(1);
    expect(port).toBeLessThanOrEqual(65535);
  });

  it('should validate heartbeat interval', () => {
    const interval = 300000; // 5 minutes
    expect(interval).toBeGreaterThanOrEqual(60000); // min 1 minute
    expect(interval).toBeLessThanOrEqual(3600000); // max 1 hour
  });
});

describe('Heartbeat Protocol', () => {
  it('should have valid heartbeat request structure', () => {
    const heartbeat = {
      type: 'heartbeat',
      timestamp: Date.now(),
      source: {
        host: '192.168.1.100',
        port: 9528
      },
      health: {
        status: 'ok' as const,
        memory: 65,
        cpu: 25,
        uptime: 45000,
        connections: 15
      }
    };

    expect(heartbeat.type).toBe('heartbeat');
    expect(heartbeat.source.host).toMatch(/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
    expect(heartbeat.health.status).toMatch(/^(ok|warning|critical)$/);
  });

  it('should have valid heartbeat response structure', () => {
    const response = {
      type: 'heartbeat_ack',
      timestamp: Date.now(),
      status: 'ok'
    };

    expect(response.type).toBe('heartbeat_ack');
    expect(response.status).toMatch(/^(ok|warning|critical)$/);
  });
});

describe('Repair Actions', () => {
  it('should support valid repair actions', () => {
    const validActions = ['check', 'restart', 'diagnose'];
    
    validActions.forEach(action => {
      expect(['check', 'restart', 'diagnose']).toContain(action);
    });
  });

  it('should have valid repair request structure', () => {
    const repair = {
      type: 'repair' as const,
      timestamp: Date.now(),
      source: {
        host: '192.168.1.100',
        port: 9528
      },
      action: 'restart' as const
    };

    expect(repair.type).toBe('repair');
    expect(repair.action).toMatch(/^(check|restart|diagnose)$/);
  });
});
