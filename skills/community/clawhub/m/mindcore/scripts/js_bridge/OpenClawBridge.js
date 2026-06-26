/**
 * OpenClawBridge.js — The Integration Master Script
 * 
 * Ties together the Python Mind Engine outputs and the local OpenClaw Gateway.
 * It listens for 'autonomous_thought' events from MindObserver,
 * formats them as a System Prompt injection, and delegates to OpenClaw.
 * 
 * All Telegram communication goes through OpenClaw CLI — we never touch
 * the Telegram Bot API directly, to avoid conflicts.
 */

const { spawn } = require('child_process');
const MindObserver = require('./MindObserver');
const SensorWriter = require('./SensorWriter');
const BridgeRateLimiter = require('./BridgeRateLimiter');

// Configuration for OpenClaw integration
const TARGET_PHONE_OR_GROUP = process.env.OPENCLAW_TARGET || '+1234567890';
const MOCK_MODE = process.env.MOCK_MODE === 'true';

class OpenClawBridge {
    constructor() {
        this.observer = new MindObserver();
        this.sensor = new SensorWriter();
        this.rateLimiter = new BridgeRateLimiter();

        // Listen for new thoughts from the Python Subconscious
        this.observer.on('autonomous_thought', (thoughtData) => {
            this.handleAutonomousThought(thoughtData);
        });
    }

    start() {
        console.log("=========================================================");
        console.log("  🌉 Mind Engine <-> OpenClaw Bridge Activated");
        console.log(`  Mock Mode: ${MOCK_MODE ? "ON (Console Only)" : "OFF (Will call openclaw CLI)"}`);
        console.log("=========================================================\n");

        this.observer.start();

        // Example: simulate user interaction on start to clear loneliness
        this.sensor.recordUserInteraction();
    }

    stop() {
        this.observer.stop();
        this.rateLimiter.shutdown();
        console.log("[Bridge] 🛑 Bridge Shutdown.");
    }

    handleAutonomousThought(thought) {
        const intensityName = thought.intensity_level ? thought.intensity_level.level_name : "unknown";
        const prompt = thought.system_prompt_injection || "No prompt generated.";

        console.log(`\n[Bridge] 🧠 RECEIVED AUTONOMOUS THOUGHT!`);
        console.log(`   Intensity: [${intensityName.toUpperCase()}]`);
        console.log(`   Internal State Payload: \n${prompt}\n`);

        if (MOCK_MODE) {
            console.log(`[Bridge-Mock] Would have sent to OpenClaw: \n${prompt}`);
            return;
        }

        // W3: 通过 5 层频率控制投递，deliverFn 接收 confirm 回调
        const result = this.rateLimiter.attempt(prompt, (msg, confirm) => {
            this._doSendToOpenClaw(msg, confirm);
        });

        if (!result.allowed) {
            const status = this.rateLimiter.getStatus();
            console.log(`[Bridge] 🛡️ 频率控制拦截 (原因: ${result.reason}) | 窗口: ${status.deliveriesInWindow}/${status.maxPerHour}/h | 队列: ${status.queueLength}/${status.queueMax}`);
        }
    }

    /**
     * 实际投递到 OpenClaw Gateway（内部方法，由 rateLimiter 回调）
     * W3: 接受 confirm 回调，投递成功后才记录配额；失败则重新入队
     */
    _doSendToOpenClaw(message, confirm) {
        const wrappedMessage = `[SYSTEM: The following is your current internal state from your Subconscious Engine. Please react to this and express yourself autonomously in character.]\n\n${message}`;

        console.log(`[OpenClaw] 🚀 Dispatching to Gateway...`);

        const openclawCommand = process.env.OPENCLAW_COMMAND || 'openclaw';

        const args = [
            'agent',
            '--channel', 'telegram',
            '--to', TARGET_PHONE_OR_GROUP,
            '--message', wrappedMessage,
            '--deliver'
        ];

        const child = spawn(openclawCommand, args, { stdio: 'inherit' });

        child.on('error', (err) => {
            console.error(`[OpenClaw] ❌ Failed to start subprocess:`, err);
            // 投递失败，不消耗配额，消息重新入队
            this.rateLimiter.requeue(message);
        });

        child.on('exit', (code) => {
            if (code === 0) {
                console.log(`[OpenClaw] ✅ Successfully pushed autonomous message.`);
                // W3: 投递成功，调用 confirm 记录配额
                if (confirm) confirm();
                this.sensor.recordUserInteraction();
            } else {
                console.error(`[OpenClaw] ⚠️ Exited with code ${code}. Check if Gateway is running or Target is correct.`);
                // W3: 投递失败，不消耗配额，消息重新入队
                this.rateLimiter.requeue(message);
            }
        });
    }
}

// Run the bridge directly if executed via Node
if (require.main === module) {
    const bridge = new OpenClawBridge();

    // Handle graceful shutdown
    process.on('SIGINT', () => {
        bridge.stop();
        process.exit();
    });

    bridge.start();
}

module.exports = OpenClawBridge;
