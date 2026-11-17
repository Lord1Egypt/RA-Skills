"use strict";
/**
 * CLI 命令解析器
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.CommandParser = void 0;
/**
 * 命令解析器
 */
class CommandParser {
    /**
     * 解析命令行参数
     */
    parse(args) {
        if (args.length === 0) {
            return { action: 'cluster', format: 'markdown' };
        }
        const [action, ...rest] = args;
        const actionLower = action.toLowerCase();
        // 验证动作
        if (!this.isValidAction(actionLower)) {
            throw new Error(`未知操作: ${action}。可用操作: ${this.VALID_ACTIONS.join(', ')}`);
        }
        // 解析剩余参数
        const result = this.parseRest(rest);
        return {
            action: actionLower,
            ...result,
            format: result.format ?? 'markdown'
        };
    }
    /**
     * 是否为有效操作
     */
    isValidAction(action) {
        return this.VALID_ACTIONS.includes(action);
    }
    /**
     * 解析剩余参数
     */
    parseRest(rest) {
        const result = {};
        const tags = [];
        for (let i = 0; i < rest.length; i++) {
            const arg = rest[i];
            // 检查是否为标签（以 @ 开头）
            if (arg.startsWith('@')) {
                tags.push(arg.substring(1));
                continue;
            }
            // 检查是否为格式参数
            if (arg === '--json' || arg === '-j') {
                result.format = 'json';
                continue;
            }
            // 检查是否为 target (user@host:port)
            if (arg.includes('@') && !result.target) {
                const target = this.parseTarget(arg);
                result.target = target;
                continue;
            }
            // 其他视为 action 的参数
            if (!result.arg) {
                result.arg = arg;
            }
        }
        if (tags.length > 0) {
            result.tags = tags;
        }
        return result;
    }
    /**
     * 解析目标服务器 (user@host:port)
     */
    parseTarget(targetStr) {
        const parts = targetStr.split('@');
        if (parts.length !== 2) {
            throw new Error(`无效的目标格式: ${targetStr}，期望 user@host[:port]`);
        }
        const user = parts[0];
        const hostPort = parts[1].split(':');
        return {
            user,
            host: hostPort[0],
            port: hostPort[1] ? parseInt(hostPort[1]) : undefined
        };
    }
    /**
     * 获取帮助信息
     */
    getHelp() {
        const lines = [];
        lines.push('## 运维助手命令参考\n');
        lines.push('### 基本格式');
        lines.push('```');
        lines.push('/ops-maintenance <action> [target] [arg] [@tag...] [--json]');
        lines.push('```\n');
        lines.push('### 可用操作');
        lines.push('| 操作 | 说明 | 参数 |');
        lines.push('|------|------|------|');
        lines.push('| `health` / `check` | 健康检查 | 无');
        lines.push('| `logs` / `log` | 日志分析 | 关键词 (默认: error)');
        lines.push('| `perf` / `performance` | 性能监控 | 无');
        lines.push('| `ports` / `port` | 端口检查 | 端口号 (可选)');
        lines.push('| `process` / `proc` | 进程检查 | 进程名 (可选)');
        lines.push('| `disk` / `space` | 磁盘检查 | 无');
        lines.push('| `password` / `passwd` | 密码过期检查 | 无');
        lines.push('| `email-config` | 邮件配置测试 | 发送测试邮件');
        lines.push('| `cluster` | 集群状态 | 无 (默认)\\n');
        lines.push('### 示例');
        lines.push('```');
        lines.push('/ops-maintenance health                    # 集群健康检查');
        lines.push('/ops-maintenance health @production        # 生产环境服务器');
        lines.push('/ops-maintenance logs error --json         # JSON 格式日志');
        lines.push('/ops-maintenance process nginx             # 检查 nginx 进程');
        lines.push('/ops-maintenance port 80 root@host:2222   # 远程端口检查');
        lines.push('```');
        return lines.join('\n');
    }
}
exports.CommandParser = CommandParser;
CommandParser.VALID_ACTIONS = [
    'health', 'check',
    'logs', 'log',
    'perf', 'performance',
    'ports', 'port',
    'process', 'proc',
    'disk', 'space',
    'password', 'passwd', 'expire',
    'email-config'
];
//# sourceMappingURL=CommandDispatcher.js.map