#!/usr/bin/env node
/**
 * minimax-tts skill entry point
 * 提供两个工具函数：
 *   1. design_voice - 设计音色
 *   2. tts_and_send - 生成语音并发送到飞书
 */

const { spawn } = require('child_process');
const path = require('path');

const scriptPath = path.join(__dirname, 'scripts', 'tts_wrapper.sh');

/**
 * 调用 Python 脚本执行 TTS
 */
function execPython(args) {
    return new Promise((resolve, reject) => {
        const proc = spawn('python3', [scriptPath, ...args], { cwd: __dirname });
        let stdout = '', stderr = '';
        proc.stdout.on('data', d => stdout += d);
        proc.stderr.on('data', d => stderr += d);
        proc.on('close', code => {
            if (code === 0) resolve(stdout.trim());
            else reject(new Error(stderr || `exit ${code}: ${stdout}`));
        });
    });
}

/**
 * 设计音色并生成语音发送
 * @param {string} prompt - 音色描述
 * @param {string} previewText - 试听文本
 * @param {string} text - 要说的内容
 */
async function designVoice(prompt, previewText, text) {
    return execPython(['design', prompt, previewText, text]);
}

/**
 * 直接生成语音发送
 * @param {string} text - 要说的内容
 * @param {string} voiceId - 音色ID
 */
async function speak(text, voiceId = 'male-qn-qingse') {
    return execPython(['tts', text, voiceId]);
}

module.exports = { designVoice, speak };
