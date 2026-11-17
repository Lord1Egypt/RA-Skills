#!/usr/bin/env node
/**
 * 简单的服务器健康检查脚本
 * 使用 ssh2 库进行密码认证
 */

const { Client } = require('ssh2');
const fs = require('fs');
const path = require('path');

// 加载服务器配置
const configPath = path.join(process.env.HOME || 'C:\\Users\\9007081', '.config/ops-maintenance/servers.json');
const servers = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

console.log('# 🖥️ 服务器健康检查报告\n');
console.log(`检查时间: ${new Date().toLocaleString()}\n`);

async function checkServer(server) {
  const name = server.name || server.host;
  console.log(`## 检查: ${name} (${server.host}:${server.port || 22})`);

  return new Promise((resolve) => {
    const conn = new Client();

    const startTime = Date.now();

    conn.on('ready', async () => {
      try {
        // 并行执行检查命令
        const [uptime, mem, disk, processes] = await Promise.all([
          execCommand(conn, 'uptime'),
          execCommand(conn, 'free -h 2>/dev/null || echo "N/A"'),
          execCommand(conn, 'df -h / | tail -1'),
          execCommand(conn, 'ps aux --sort=-%cpu | head -10 2>/dev/null || echo "N/A"')
        ]);

        const duration = Date.now() - startTime;

        console.log('```');
        console.log(`连接耗时: ${duration}ms`);
        console.log(uptime.trim());
        console.log('');
        console.log('【内存】');
        console.log(mem.trim());
        console.log('');
        console.log('【磁盘】');
        console.log(disk.trim());
        console.log('');
        console.log('【Top 进程】');
        console.log(processes.trim());
        console.log('```\n');

        // 分析状态
        const diskUsage = disk.includes('%') ? parseInt(disk.match(/(\d+)%/)?.[1] || '0') : 0;
        const status = diskUsage > 90 ? '❌ 磁盘使用率过高' : diskUsage > 80 ? '⚠️ 磁盘警告' : '✅ 健康';

        console.log(`**状态**: ${status}\n`);
        conn.end();
        resolve();
      } catch (err) {
        console.log(`错误: ${err.message}\n`);
        conn.end();
        resolve();
      }
    });

    conn.on('error', (err) => {
      console.log(`❌ 连接失败: ${err.message}\n`);
      resolve();
    });

    conn.on('close', () => {
      // console.log('连接关闭');
    });

    conn.connect({
      host: server.host,
      port: server.port || 22,
      username: server.user,
      password: server.password,
      tryKeyboard: true,
      readyTimeout: 10000,
      keepaliveInterval: 5000,
      keepaliveCountMax: 3
    });
  });
}

function execCommand(conn, command) {
  return new Promise((resolve, reject) => {
    conn.exec(command, (err, stream) => {
      if (err) {
        reject(err);
        return;
      }

      let output = '';
      stream.on('data', (data) => {
        output += data.toString();
      }).on('close', () => {
        resolve(output);
      });
    });
  });
}

// 执行检查
(async () => {
  for (const server of servers) {
    try {
      await checkServer(server);
    } catch (err) {
      console.log(`检查失败: ${err.message}\n`);
    }
  }
  console.log('---');
  console.log('检查完成！');
})();