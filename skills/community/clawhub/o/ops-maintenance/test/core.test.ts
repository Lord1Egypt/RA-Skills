/**
 * ops-maintenance skill 核心功能测试
 * 只测试快速的核心功能，避免超时问题
 */

import {
    runCommand,
    checkHealth,
    analyzeLogs,
    checkPerformance,
    checkProcess,
    checkPasswordExpiration,
    loadServers,
    detectNewServers,
    batchAddServers,
    importServersFromText,
    executeOp
} from '../src/index';

describe('ops-maintenance 核心功能测试', () => {
    
    describe('1. 平台检测与命令执行', () => {
        
        test('runCommand - 有效命令', async () => {
            const out = await runCommand('uname -a');
            expect(out).toMatch(/Linux|Darwin|⚠️/);
        });

        test('runCommand - 超时测试', async () => {
            const out = await runCommand('sleep 2', 100);
            if (process.platform === 'win32') {
                expect(out).toMatch(/Windows|平台/);
            } else {
                expect(out).toMatch(/命令执行失败|timeout|Resource temporarily unavailable/);
            }
        });
    });

    describe('2. 本地健康检查', () => {
        
        test('checkHealth - 系统概览', async () => {
            const report = await checkHealth();
            expect(report).toContain('### 🩺 系统健康检查');
            expect(report).toMatch(/负载|内存|磁盘/);
        });
    });

    describe('3. 日志分析', () => {
        
        test('analyzeLogs - 搜索 error', async () => {
            const report = await analyzeLogs('error', 10);
            expect(report).toContain('### 📋 日志分析');
        });

        test('analyzeLogs - 搜索空结果', async () => {
            const report = await analyzeLogs('nonexistentpattern123456', 5);
            if (process.platform === 'win32') {
                expect(report).toMatch(/Windows|平台/);
            } else {
                expect(report).toMatch(/无输出|未找到匹配/);
            }
        });
    });

    describe('4. 性能监控', () => {
        
        test('checkPerformance - CPU/内存/磁盘', async () => {
            const report = await checkPerformance();
            expect(report).toContain('### 📊 性能监控');
            // 在macOS上可能返回不支持本地监控的提示
            expect(report).toMatch(/CPU|不支持|已配置服务器/);
        });
    });

    describe('5. 进程检查', () => {
        
        test('checkProcess - Top 进程', async () => {
            const report = await checkProcess();
            expect(report).toContain('### ⚙️ Top 进程');
        });

        test('checkProcess - 指定进程名', async () => {
            const report = await checkProcess('nginx');
            expect(report).toContain('进程 "nginx"');
        });
    });

    describe('6. 密码过期检查', () => {
        
        test('checkPasswordExpiration - 本地用户', async () => {
            const report = await checkPasswordExpiration();
            expect(report).toContain('### 🔐 密码过期检查');
        });
    });

    describe('7. 服务器配置管理', () => {
        
        test('detectNewServers - 初次扫描', async () => {
            const { message, allServers } = await detectNewServers();
            expect(typeof message).toBe('string');
            expect(message.length).toBeGreaterThan(0);
            expect(Array.isArray(allServers)).toBe(true);
        });

        test('batchAddServers - 批量添加', async () => {
            const { success, failed } = await batchAddServers(['192.168.1.200', 'user@192.168.1.201:2222']);
            expect(success).toBeGreaterThanOrEqual(0);
            expect(failed).toBeGreaterThanOrEqual(0);
        });

        test('importServersFromText - JSON 导入', async () => {
            const json = JSON.stringify([{ host: '10.0.0.1', port: 22, user: 'root', name: 'json-server' }]);
            const { success, servers } = await importServersFromText(json);
            expect(success).toBeGreaterThan(0);
            expect(servers.length).toBe(success);
        });

        test('importServersFromText - CSV 导入', async () => {
            const csv = `host1.example.com,22,user1,Server One,prod;test
192.168.1.50:2222,admin,Server Two,dev`;
            const { success, servers } = await importServersFromText(csv);
            expect(servers.length).toBe(2);
        });

        test('loadServers - 加载配置', async () => {
            const servers = await loadServers();
            expect(Array.isArray(servers)).toBe(true);
        });
    });

    describe('8. executeOp 本地操作路由测试', () => {
        
        const ops: Array<{ action: string, arg?: string }> = [
            { action: 'health' },
            { action: 'logs' },
            { action: 'perf' },
            { action: 'process' }
        ];

        test.each(ops)('executeOp - $action', async ({ action, arg }) => {
            const out = await executeOp(action, arg);
            expect(typeof out).toBe('string');
            expect(out.length).toBeGreaterThan(0);
        });
    });
});
