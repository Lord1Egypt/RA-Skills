/**
 * OpenClaw PM2 配置文件
 * ecosystem.config.js
 *
 * 用法:
 *   pm2 start ecosystem.config.js
 *   pm2 save
 *   pm2 startup
 */
module.exports = {
  apps: [
    {
      name: 'openclaw-gateway',

      // 启动脚本
      script: 'openclaw',
      args: 'gateway start --no-daemon',
      cwd: '/home/openclaw/.openclaw',

      // 进程管理
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: 10000,       // 最少运行 10 秒才算稳定
      restart_delay: 10000,    // 重启间隔 10 秒

      // 资源限制
      node_args: '--expose-gc --max-old-space-size=2048',

      // 日志
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      error_file: '/var/log/openclaw/error.log',
      out_file: '/var/log/openclaw/out.log',
      log_file: '/var/log/openclaw/combined.log',
      merge_logs: true,
      log_type: 'json',

      // 环境变量
      env: {
        NODE_ENV: 'production',
        // 自行添加其他环境变量
      },

      // 内存监控（超过 1.5G 告警，超过 1.8G 重启）
      max_memory_restart: '1.8G',

      // kill 超时
      kill_timeout: 5000,

      // 创建日志文件（如果不存在）
      force: true,
    },
  ],
};
