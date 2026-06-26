/**
 * Enhanced Controller Example - 增强控制器使用示例
 * 演示如何使用 EnhancedMainController 进行任务管理和 Agent 调度
 */

const { EnhancedMainController } = require('../src/core/enhanced-main-controller');

async function main() {
    console.log('=== Enhanced Controller Example ===\n');

    // 1. 创建控制器实例
    const controller = new EnhancedMainController({
        dbPath: './github-collab.db',
        maxParallelAgents: 3,
        agentTimeout: 300,
        autoRecovery: true,
        autoProcessQueue: true,
        defaultModel: 'ollama/qwen3.5-code'
    });

    try {
        // 2. 初始化控制器
        console.log('Initializing controller...');
        const initResult = await controller.initialize();
        
        if (!initResult.success) {
            console.error('Failed to initialize controller:', initResult.error);
            return;
        }

        console.log('✓ Controller initialized successfully\n');

        // 3. 启动控制器
        console.log('Starting controller...');
        await controller.start();
        console.log('✓ Controller started\n');

        // 4. 创建任务示例
        console.log('=== Creating Tasks ===');
        
        const task1 = await controller.createTask({
            title: '实现用户登录功能',
            description: '实现基于 JWT 的用户登录功能，包括注册、登录、令牌验证',
            priority: 1,
            status: 'pending'
        });

        if (task1.success) {
            console.log(`✓ Task 1 created: ${task1.task.id} - ${task1.task.title}\n`);
        }

        const task2 = await controller.createTask({
            title: '实现数据缓存系统',
            description: '实现基于 Redis 的数据缓存系统，支持 TTL 和自动过期',
            priority: 2,
            status: 'pending'
        });

        if (task2.success) {
            console.log(`✓ Task 2 created: ${task2.task.id} - ${task2.task.title}\n`);
        }

        // 5. 获取任务统计
        console.log('=== Task Statistics ===');
        const stats = await controller.getTaskStats();
        console.log(`Total tasks: ${stats.total}`);
        console.log(`Pending: ${stats.pending}`);
        console.log(`In Progress: ${stats.in_progress}`);
        console.log(`Completed: ${stats.completed}\n`);

        // 6. 获取活跃 Agent 列表
        console.log('=== Active Agents ===');
        const agents = await controller.getActiveAgents();
        if (agents.length > 0) {
            agents.forEach(agent => {
                console.log(`- ${agent.label} (${agent.type}): ${agent.status}`);
            });
        } else {
            console.log('No active agents\n');
        }

        // 7. 等待任务处理
        console.log('\n=== Waiting for Task Processing ===');
        console.log('Tasks will be automatically processed by the queue processor...');
        
        // 等待 10 秒查看任务处理状态
        await new Promise(resolve => setTimeout(resolve, 10000));

        // 8. 再次获取统计
        const updatedStats = await controller.getTaskStats();
        console.log('\nUpdated Statistics:');
        console.log(`Total tasks: ${updatedStats.total}`);
        console.log(`Pending: ${updatedStats.pending}`);
        console.log(`In Progress: ${updatedStats.in_progress}`);
        console.log(`Completed: ${updatedStats.completed}\n`);

        console.log('=== Example Complete ===');
        console.log('Controller will continue running and processing tasks...');

        // 保持运行
        console.log('\nPress Ctrl+C to stop the controller');

    } catch (error) {
        console.error('Error running example:', error);
    }
}

// 处理优雅退出
process.on('SIGINT', async () => {
    console.log('\nReceived SIGINT, shutting down...');
    process.exit(0);
});

// 运行示例
main().catch(console.error);
