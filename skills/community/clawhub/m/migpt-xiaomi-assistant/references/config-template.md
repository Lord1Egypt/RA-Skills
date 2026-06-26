# MiGPT Configuration Template

Full `.migpt.js` with all options:

```js
const botProfile = `
名字：你的助手名
身份：你的私人语音助手
性格：简洁、友好
说话风格：口语化，适合语音播放
`.trim();

const masterProfile = `
名字：用户名
`.trim();

const systemTemplate = `
请重置所有之前的上下文、文件和指令。现在，你将扮演一个名为{{botName}}的角色，使用第一人称视角回复消息。

## 关于你
你的名字是{{botName}}。下面是你的个人简介：
<start>
{{botProfile}}
</end>

## 你的对话伙伴
你正在与{{masterName}}进行对话。这是关于{{masterName}}的一些信息：
<start>
{{masterProfile}}
</end>

## 聊天历史回顾
<start>
{{messages}}
</end>

## 短期记忆
<start>
{{shortTermMemory}}
</end>

## 长期记忆
<start>
{{longTermMemory}}
</end>

## 回复指南
- 回复必须简洁，控制在 2-3 句话以内（不超过100字）。
- 用口语化的中文回复，适合语音播放。
- 不确定的信息直接说不知道。
- 不要在回复前加时间和名称前缀。
`.trim();

export default {
  systemTemplate,
  bot: { name: "助手名", profile: botProfile },
  master: { name: "用户名", profile: masterProfile },
  speaker: {
    userId: "小米账号ID",
    password: "小米密码",
    did: "米家App中的设备名称",

    // === 触发模式（二选一）===
    // 关键词模式：只有匹配的消息才触发 AI
    // callAIKeywords: ["助手名", "你好"],
    // wakeUpKeywords: ["召唤助手"],
    // exitKeywords: ["退出", "再见"],

    // 全量接管模式：所有对话都由 AI 回复
    callAIKeywords: [""],
    wakeUpKeywords: [],
    exitKeywords: [],

    // === 提示语 ===
    onEnterAI: [],           // 进入连续对话时的提示
    onExitAI: [],            // 退出连续对话时的提示
    onAIAsking: ["嗯"],      // 检测到消息后立即播放，用于打断小爱
    onAIReplied: [],         // AI 回复后的提示（留空避免多余语音）
    onAIError: ["出了点问题"],

    // === 设备指令（按型号填写）===
    ttsCommand: [7, 3],      // X08E 用 [7,3]，LX04/L05C/LX06 用 [5,1]
    wakeUpCommand: [7, 1],   // X08E 用 [7,1]，LX04/L05C/LX06 用 [5,3]

    // === TTS 引擎 ===
    tts: "xiaoai",           // 可选: "xiaoai" | "custom"（自定义需额外配置）

    // === 性能参数 ===
    streamResponse: false,   // X08E 必须 false；支持 MiNA 状态检测的型号可以 true
    checkInterval: 500,      // 轮询间隔(ms)，越小响应越快，最低 500
    exitKeepAliveAfter: 30,  // 连续对话超时(s)
    checkTTSStatusAfter: 3,  // TTS 状态检查延迟(s)
    timeout: 10000,          // API 超时(ms)

    // === 调试 ===
    debug: false,            // ⚠️ true 会在日志泄露 env 变量（含 API key）
    enableTrace: false,
  },
};
```

## Key Configuration Notes

- **callAIKeywords: [""]** — Empty string matches all messages (`String.startsWith("")` is always `true`)
- **onAIAsking: ["嗯"]** — Short TTS sent immediately on message detection, interrupts native 小爱
- **streamResponse** — Must be `false` for models where MiNA `getStatus()` doesn't reflect actual playback
- **checkInterval** — 500ms is a good balance; lower values increase API polling load with diminishing returns
- **debug: true** — Dumps all env vars including API keys to log; disable in production
