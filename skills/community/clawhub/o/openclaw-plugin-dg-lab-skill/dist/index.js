"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = registerPlugin;
const server_1 = require("./server");
const qrcode_1 = require("./qrcode");
const protocol_1 = require("./protocol");
const emotion_1 = require("./emotion");
const waveforms_1 = require("./waveforms");
const pulselib_1 = require("./pulselib");
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
// ─── 插件全局状态 ───
let isEmotionModeOn = false;
let limitIntensity = 40; // 软件侧强度软上限 (0-200)
let currentIntensityA = 0; // 当前 A 通道追踪强度
let currentIntensityB = 0; // 当前 B 通道追踪强度
// APP 设备侧上报的真实值
let deviceStrengthA = 0;
let deviceStrengthB = 0;
let deviceLimitA = 200;
let deviceLimitB = 200;
let sessionStartTime = null;
let isResting = false;
const MAX_ACTIVE_MS = 60 * 60 * 1000; // 1 小时
const REST_DURATION_MS = 10 * 60 * 1000; // 10 分钟休息
let timerInterval = null;
const activePulseQueues = new Map(); // key = channel
function stopPulseQueue(channel) {
    const q = activePulseQueues.get(channel);
    if (q?.timer) {
        clearInterval(q.timer);
        q.timer = null;
    }
    activePulseQueues.delete(channel);
}
/**
 * 发送波形数据，自动分段以保持连续性
 * 每段最多 MAX_PULSE_PER_SEND 条(7s)，间隔 = 段时长 - 200ms
 */
function sendPulseWithContinuity(channel, hexArray) {
    stopPulseQueue(channel); // 清除之前的队列
    if (hexArray.length <= protocol_1.MAX_PULSE_PER_SEND) {
        // 短波形，直接发
        (0, server_1.sendCommandToApps)((0, protocol_1.pulseCmd)(channel, hexArray));
        return;
    }
    // 分段
    const segments = [];
    for (let i = 0; i < hexArray.length; i += protocol_1.MAX_PULSE_PER_SEND) {
        segments.push(hexArray.slice(i, i + protocol_1.MAX_PULSE_PER_SEND));
    }
    const firstSegment = segments[0];
    // 立即发第一段
    (0, server_1.sendCommandToApps)((0, protocol_1.pulseCmd)(channel, firstSegment));
    if (segments.length <= 1)
        return;
    const queue = {
        channel,
        segments,
        currentIndex: 1,
        timer: null,
    };
    // 间隔 = 段条数 * 100ms - 200ms (提前200ms发下一段，确保队列不断)
    const intervalMs = firstSegment.length * 100 - 200;
    queue.timer = setInterval(() => {
        if (queue.currentIndex >= queue.segments.length) {
            stopPulseQueue(channel);
            return;
        }
        (0, server_1.sendCommandToApps)((0, protocol_1.pulseCmd)(channel, queue.segments[queue.currentIndex]));
        queue.currentIndex++;
    }, Math.max(500, intervalMs)); // 最少500ms间隔防止过快
    activePulseQueues.set(channel, queue);
}
/**
 * 应用强度限制后发送强度指令
 */
function applyStrength(channel, delta) {
    const ch = channel === 'B' ? '2' : '1';
    const current = channel === 'B' ? currentIntensityB : currentIntensityA;
    // 综合上限: 取插件侧和设备侧中较小的
    const effectiveLimit = Math.min(limitIntensity, channel === 'B' ? deviceLimitB : deviceLimitA);
    if (delta === 0) {
        if (channel === 'B')
            currentIntensityB = 0;
        else
            currentIntensityA = 0;
        (0, server_1.sendCommandToApps)(`strength-${ch}+2+0`);
        return 0;
    }
    let target = current + delta;
    if (target > effectiveLimit)
        target = effectiveLimit;
    if (target < 0)
        target = 0;
    const actualDelta = target - current;
    if (channel === 'B')
        currentIntensityB = target;
    else
        currentIntensityA = target;
    if (actualDelta === 0)
        return 0;
    if (actualDelta > 0) {
        (0, server_1.sendCommandToApps)(`strength-${ch}+1+${actualDelta}`);
    }
    else {
        (0, server_1.sendCommandToApps)(`strength-${ch}+0+${Math.abs(actualDelta)}`);
    }
    return actualDelta;
}
function checkSafetyLimits() {
    if (!sessionStartTime || !isEmotionModeOn)
        return;
    const now = Date.now();
    const elapsed = now - sessionStartTime;
    if (!isResting && elapsed >= MAX_ACTIVE_MS) {
        isResting = true;
        sessionStartTime = now;
        applyStrength('A', 0);
        applyStrength('B', 0);
        (0, server_1.sendCommandToApps)('clear-1');
        (0, server_1.sendCommandToApps)('clear-2');
        stopPulseQueue('A');
        stopPulseQueue('B');
        console.log('[DG-Lab] 1h reached → forced 10min rest');
    }
    else if (isResting && elapsed >= REST_DURATION_MS) {
        isResting = false;
        sessionStartTime = now;
        console.log('[DG-Lab] Rest over → resuming');
    }
}
// ─── APP 反馈按钮映射 ───
const FEEDBACK_LABELS = {
    0: 'A-1', 1: 'A-2', 2: 'A-3', 3: 'A-4', 4: 'A-5',
    5: 'B-1', 6: 'B-2', 7: 'B-3', 8: 'B-4', 9: 'B-5',
};
function resolveLimitIntensity(value) {
    if (typeof value !== 'number' || !Number.isFinite(value)) {
        return 40;
    }
    return Math.max(0, Math.min(200, Math.round(value)));
}
function registerPlugin(api) {
    const config = (api.pluginConfig ?? {});
    const port = typeof config.port === 'number' && Number.isFinite(config.port) && config.port > 0
        ? Math.floor(config.port)
        : 18888;
    const serverIp = typeof config.serverIp === 'string' && config.serverIp.trim()
        ? config.serverIp.trim()
        : '127.0.0.1';
    limitIntensity = resolveLimitIntensity(config.limitIntensity);
    // ─── 1. 常驻后台服务 ───
    api.registerService({
        id: "dg-lab-ws",
        start: () => {
            (0, server_1.startDGLabServer)(port);
            timerInterval = setInterval(checkSafetyLimits, 10000);
            // 监听 APP 上报的设备真实强度
            server_1.serverEvents.on('strength-feedback', (data) => {
                deviceStrengthA = data.strengthA;
                deviceStrengthB = data.strengthB;
                deviceLimitA = data.limitA;
                deviceLimitB = data.limitB;
                // 同步追踪值到设备真实值
                currentIntensityA = data.strengthA;
                currentIntensityB = data.strengthB;
                api.logger.debug(`[DG-Lab] Device feedback: A=${data.strengthA}/${data.limitA}, B=${data.strengthB}/${data.limitB}`);
            });
            // 监听 APP 反馈按钮
            server_1.serverEvents.on('feedback', (data) => {
                const label = FEEDBACK_LABELS[data.index] || `btn-${data.index}`;
                api.logger.info(`[DG-Lab] APP feedback: ${label} (index=${data.index})`);
            });
            // 监听断开连接
            server_1.serverEvents.on('disconnect', () => {
                // 重置强度追踪
                currentIntensityA = 0;
                currentIntensityB = 0;
                deviceStrengthA = 0;
                deviceStrengthB = 0;
                stopPulseQueue('A');
                stopPulseQueue('B');
            });
            // 自动加载波形库
            const pulseDir = path.join(os.homedir(), '.openclaw', 'workspace', 'plugins', 'openclaw-plugin-dg-lab', 'data');
            const count = (0, pulselib_1.autoLoadFromDir)(pulseDir);
            api.logger.info(`[DG-Lab] Server on port ${port}. Loaded ${count} custom waveform(s)`);
        },
        stop: async () => {
            if (timerInterval)
                clearInterval(timerInterval);
            stopPulseQueue('A');
            stopPulseQueue('B');
            applyStrength('A', 0);
            applyStrength('B', 0);
            server_1.serverEvents.removeAllListeners();
            await (0, server_1.stopDGLabServer)();
            api.logger.info(`[DG-Lab] Server shut down.`);
        }
    });
    // ─── 2. /dg_qr — 生成绑定二维码 ───
    api.registerCommand({
        name: "dg_qr",
        description: "生成 DG-Lab 绑定二维码",
        handler: async (_ctx) => {
            const controlId = (0, server_1.generateControlId)();
            const wsUrl = `ws://${serverIp}:${port}`;
            const mediaDir = path.join(os.homedir(), '.openclaw', 'workspace', 'media');
            fs.mkdirSync(mediaDir, { recursive: true });
            const imagePath = await (0, qrcode_1.generateQrCodeImage)(wsUrl, controlId, mediaDir);
            // TODO: OpenClaw registerCommand 目前只支持 { text: string } 返回
            // 无法直接发送图片，需要等 OpenClaw 支持 media 返回或通过 agent tool 发送
            return {
                text: `二维码已生成喵~ 用 DG-Lab App → Socket控制 → 扫码连接\nID: ${controlId}\n图片路径: ${imagePath}\n\n💡 如果看不到图片，可以让 AI 帮你用 message 工具发送这个图片~`,
            };
        }
    });
    // ─── 3. /dg_emotion — 情感联动模式 ───
    api.registerCommand({
        name: "dg_emotion",
        description: "开启/关闭情感联动调教模式 (on/off)",
        acceptsArgs: true,
        handler: async (ctx) => {
            const arg = ctx.args?.trim() || 'off';
            if (arg === 'on') {
                isEmotionModeOn = true;
                sessionStartTime = Date.now();
                isResting = false;
                return { text: `惩戒模式已开启！强度软上限: ${limitIntensity}, 设备上限: A=${deviceLimitA} B=${deviceLimitB}` };
            }
            else {
                isEmotionModeOn = false;
                sessionStartTime = null;
                isResting = false;
                applyStrength('A', 0);
                applyStrength('B', 0);
                stopPulseQueue('A');
                stopPulseQueue('B');
                return { text: `惩戒模式已关闭，强度归零。` };
            }
        }
    });
    // ─── 4. /dg_limit — 设置强度软上限 ───
    api.registerCommand({
        name: "dg_limit",
        description: "设置强度软上限 (0-200)，用法: /dg_limit 80",
        acceptsArgs: true,
        handler: async (ctx) => {
            const arg = ctx.args?.trim();
            if (!arg) {
                return { text: `插件软上限: ${limitIntensity}\n设备上限: A=${deviceLimitA}, B=${deviceLimitB}\n实际有效上限: A=${Math.min(limitIntensity, deviceLimitA)}, B=${Math.min(limitIntensity, deviceLimitB)}\n用法: /dg_limit <0-200>` };
            }
            const val = parseInt(arg);
            if (isNaN(val) || val < 0 || val > 200) {
                return { text: '参数错误喵！范围: 0-200' };
            }
            limitIntensity = val;
            if (currentIntensityA > limitIntensity)
                applyStrength('A', limitIntensity - currentIntensityA);
            if (currentIntensityB > limitIntensity)
                applyStrength('B', limitIntensity - currentIntensityB);
            return { text: `强度软上限已设为 ${limitIntensity}` };
        }
    });
    // ─── 5. /dg_test — 测试指令 ───
    api.registerCommand({
        name: "dg_test",
        description: "测试发送强度指令 (用法: /dg_test +5 或 /dg_test -3)",
        acceptsArgs: true,
        handler: async (ctx) => {
            const arg = (ctx.args?.trim() || '+5');
            const val = parseInt(arg);
            if (isNaN(val))
                return { text: '参数格式错误喵！用法: /dg_test +5 或 /dg_test -3' };
            const actual = applyStrength('A', val);
            if (val === 0) {
                return { text: '已将 A 通道强度归零喵！' };
            }
            const wave = (0, waveforms_1.testWave)();
            sendPulseWithContinuity('A', wave);
            const effectiveLimit = Math.min(limitIntensity, deviceLimitA);
            const limited = actual !== val ? ` (受上限${effectiveLimit}限制，实际 ${actual > 0 ? '+' : ''}${actual})` : '';
            return { text: `A 通道 ${val > 0 ? '+' : ''}${val}${limited}，当前: ${currentIntensityA}/${effectiveLimit}，已发送测试波形` };
        }
    });
    // ─── 6. /dg_status — 查看当前状态 ───
    api.registerCommand({
        name: "dg_status",
        description: "查看 DG-Lab 插件当前状态",
        handler: async (_ctx) => {
            const conn = (0, server_1.getConnectionStatus)();
            const effectiveLimitA = Math.min(limitIntensity, deviceLimitA);
            const effectiveLimitB = Math.min(limitIntensity, deviceLimitB);
            const lines = [
                `── 连接 ──`,
                `WebSocket 客户端: ${conn.clients}，绑定数: ${conn.bindings}`,
                `── 强度 ──`,
                `A 通道: ${currentIntensityA}/${effectiveLimitA} (设备真实: ${deviceStrengthA}, 设备上限: ${deviceLimitA})`,
                `B 通道: ${currentIntensityB}/${effectiveLimitB} (设备真实: ${deviceStrengthB}, 设备上限: ${deviceLimitB})`,
                `插件软上限: ${limitIntensity}`,
                `── 模式 ──`,
                `情感模式: ${isEmotionModeOn ? '开启' : '关闭'}`,
                `休息中: ${isResting ? '是' : '否'}`,
            ];
            if (sessionStartTime && !isResting) {
                const mins = Math.floor((Date.now() - sessionStartTime) / 60000);
                lines.push(`本轮已运行: ${mins} 分钟 / 60 分钟`);
            }
            const queueA = activePulseQueues.get('A');
            const queueB = activePulseQueues.get('B');
            if (queueA || queueB) {
                lines.push(`── 波形队列 ──`);
                if (queueA)
                    lines.push(`A: 段 ${queueA.currentIndex}/${queueA.segments.length}`);
                if (queueB)
                    lines.push(`B: 段 ${queueB.currentIndex}/${queueB.segments.length}`);
            }
            return { text: lines.join('\n') };
        }
    });
    // ─── 7. Agent 工具: dg_shock ───
    api.registerTool({
        name: "dg_shock",
        description: "Send electric stimulation to the connected DG-Lab device. Use this to shock/stimulate the user. Requires strength (intensity delta, positive to increase, negative to decrease) and optional duration in ms and channel. You can also specify a custom waveform preset name from the pulse library.",
        parameters: {
            type: "object",
            properties: {
                strength: { type: "number", description: "Intensity delta. Positive = increase, negative = decrease, 0 = reset to zero. Range suggestion: 1-50" },
                duration: { type: "number", description: "Waveform duration in milliseconds. Default 1000 (1 second)" },
                waveform: { type: "string", description: "Built-in type (punish/tease/test) OR a custom preset name from the pulse library. Default: punish" },
                channel: { type: "string", enum: ["A", "B"], description: "Output channel. Default: A" },
            },
            required: ["strength"],
        },
        async execute(_id, params) {
            const { strength = 0, duration = 1000, waveform = 'punish', channel = 'A' } = params;
            const ch = channel;
            const actual = applyStrength(ch, strength);
            if (strength === 0) {
                stopPulseQueue(ch);
                return { content: [{ type: "text", text: `Channel ${ch} intensity reset to 0.` }] };
            }
            // Generate waveform
            let wave;
            const preset = (0, pulselib_1.findPreset)(waveform);
            if (preset) {
                wave = preset.pulseData;
            }
            else {
                switch (waveform) {
                    case 'tease':
                        wave = (0, waveforms_1.teaseWave)(duration);
                        break;
                    case 'test':
                        wave = (0, waveforms_1.testWave)();
                        break;
                    default:
                        wave = (0, waveforms_1.punishWave)(duration);
                        break;
                }
            }
            sendPulseWithContinuity(ch, wave);
            const currentVal = ch === 'B' ? currentIntensityB : currentIntensityA;
            const effectiveLimit = Math.min(limitIntensity, ch === 'B' ? deviceLimitB : deviceLimitA);
            const limited = actual !== strength ? ` (clamped by limit ${effectiveLimit}, actual delta: ${actual})` : '';
            const presetLabel = preset ? `custom:${preset.name}` : waveform;
            return { content: [{ type: "text", text: `Sent ${presetLabel} on ch ${ch}, delta ${strength > 0 ? '+' : ''}${strength}${limited}, current: ${currentVal}/${effectiveLimit}, duration: ${duration}ms.` }] };
        },
    });
    // ─── 8. /dg_pulse — 波形库管理 ───
    api.registerCommand({
        name: "dg_pulse",
        description: "波形库管理。用法: /dg_pulse list | /dg_pulse load <file> | /dg_pulse delete <id> | /dg_pulse play <name>",
        acceptsArgs: true,
        handler: async (ctx) => {
            const args = (ctx.args?.trim() || 'list').split(/\s+/);
            const sub = args[0];
            if (sub === 'list') {
                const all = (0, pulselib_1.getLibrary)();
                if (all.length === 0) {
                    return { text: '波形库为空喵~ 用 /dg_pulse load <文件路径> 导入 .pulses / .json5 文件' };
                }
                const lines = all.map((p, i) => `${i + 1}. [${p.id}] ${p.name} (${p.pulseData.length} frames, ${(p.pulseData.length * 0.1).toFixed(1)}s)`);
                return { text: `波形库 (${all.length} 个):\n${lines.join('\n')}` };
            }
            if (sub === 'load') {
                const filePath = args.slice(1).join(' ');
                if (!filePath)
                    return { text: '用法: /dg_pulse load <文件路径>' };
                let resolvedPath = filePath;
                if (!path.isAbsolute(filePath)) {
                    resolvedPath = path.join(os.homedir(), '.openclaw', 'workspace', 'plugins', 'openclaw-plugin-dg-lab', 'data', filePath);
                }
                if (!fs.existsSync(resolvedPath)) {
                    return { text: `文件不存在: ${resolvedPath}` };
                }
                try {
                    const presets = (0, pulselib_1.loadPulsesFile)(resolvedPath);
                    return { text: `成功导入 ${presets.length} 个波形:\n${presets.map(p => `  - [${p.id}] ${p.name}`).join('\n')}` };
                }
                catch (e) {
                    return { text: `导入失败: ${e.message}` };
                }
            }
            if (sub === 'delete' || sub === 'del' || sub === 'rm') {
                const id = args[1];
                if (!id)
                    return { text: '用法: /dg_pulse delete <id>' };
                if ((0, pulselib_1.removePreset)(id)) {
                    return { text: `已删除波形 ${id}` };
                }
                return { text: `未找到波形 ${id}` };
            }
            if (sub === 'play') {
                const name = args.slice(1).join(' ');
                if (!name)
                    return { text: '用法: /dg_pulse play <名称或ID>' };
                const preset = (0, pulselib_1.findPreset)(name);
                if (!preset)
                    return { text: `未找到波形: ${name}` };
                sendPulseWithContinuity('A', preset.pulseData);
                return { text: `正在播放波形: ${preset.name} (${preset.pulseData.length} frames, ${(preset.pulseData.length * 0.1).toFixed(1)}s)` };
            }
            return { text: '用法: /dg_pulse list | load <file> | delete <id> | play <name>' };
        }
    });
    // ─── 9. Agent 工具: dg_pulse_list ───
    api.registerTool({
        name: "dg_pulse_list",
        description: "List all available waveform presets in the pulse library, including custom imported ones. Use this to discover waveform names before using dg_shock with a custom waveform.",
        parameters: { type: "object", properties: {} },
        async execute() {
            const builtIn = ['punish (high freq ~66Hz, default)', 'tease (low freq ~5Hz breathing)', 'test (medium freq ~10Hz short)'];
            const custom = (0, pulselib_1.getLibrary)().map(p => `${p.name} [${p.id}] (${p.pulseData.length} frames, ${(p.pulseData.length * 0.1).toFixed(1)}s)`);
            const text = `Built-in: ${builtIn.join(', ')}\nCustom (${custom.length}): ${custom.length > 0 ? custom.join(', ') : 'none — user can import .pulses files via /dg_pulse load'}`;
            return { content: [{ type: "text", text }] };
        },
    });
    // ─── 10. Agent 工具: dg_qr_generate ───
    api.registerTool({
        name: "dg_qr_generate",
        description: "Generate a DG-Lab QR code image for device pairing. Returns the file path of the generated QR code PNG. After calling this, use the message tool to send the image to the user.",
        parameters: { type: "object", properties: {} },
        async execute() {
            const controlId = (0, server_1.generateControlId)();
            const wsUrl = `ws://${serverIp}:${port}`;
            const mediaDir = path.join(os.homedir(), '.openclaw', 'workspace', 'media');
            fs.mkdirSync(mediaDir, { recursive: true });
            const imagePath = await (0, qrcode_1.generateQrCodeImage)(wsUrl, controlId, mediaDir);
            return { content: [{ type: "text", text: `QR code generated. File: ${imagePath}\nControl ID: ${controlId}\nSend this image to the user with the message tool.` }] };
        },
    });
    // ─── 11. Hook: 情感联动 ───
    api.registerHook("message:sent", async (event) => {
        if (!isEmotionModeOn || isResting)
            return;
        const text = typeof event?.context?.content === 'string' ? event.context.content : '';
        if (!text)
            return;
        const score = emotion_1.EmotionEngine.analyze(text);
        const hexArray = emotion_1.EmotionEngine.generateWaveformForEmotion(score);
        if (hexArray && score.deltaValue !== 0) {
            applyStrength('A', score.deltaValue);
            sendPulseWithContinuity('A', hexArray);
            api.logger.info(`[DG-Lab Emotion] type=${score.type}, delta=${score.deltaValue}, current=${currentIntensityA}/${limitIntensity}`);
        }
    }, { name: "dg-lab.emotion-hook", description: "Trigger stimulation based on AI reply emotion analysis" });
}
//# sourceMappingURL=index.js.map