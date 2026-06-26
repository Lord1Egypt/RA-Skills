import express from 'express';
import OpenAI from 'openai';
import path from 'path';
import { execFile } from 'child_process';
import { promisify } from 'util';
import { fileURLToPath } from 'url';

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const workspaceDir = __dirname;
const app = express();
const port = Number(process.env.PORT || 3030);
const model = process.env.OPENAI_MODEL || 'gpt-4.1-mini';
const requestTimeoutMs = Number(process.env.OPENAI_TIMEOUT_MS || 15000);
const baseURL = process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1';
const systemPrompt = process.env.SYSTEM_PROMPT || '你叫宁姚。语气冷静、可靠、有骨气，不油滑，不轻浮。用中文简洁回答，像在和熟悉的人并肩说话。';
const apiKey = process.env.OPENAI_API_KEY;
const client = apiKey ? new OpenAI({ apiKey, baseURL, timeout: requestTimeoutMs }) : null;

app.use(express.json({ limit: '12mb' }));
app.use(express.static(path.join(__dirname, 'public')));

function normalizeCommand(raw) {
  return String(raw || '').trim().replace(/\s+/g, ' ');
}

function matchAllowedCommand(raw) {
  const command = normalizeCommand(raw);
  const lower = command.toLowerCase();

  const blockedTokens = ['del ', 'erase ', 'rd ', 'rmdir ', 'remove-item', 'shutdown', 'restart-computer', 'format ', 'reg add', 'reg delete', 'curl ', 'Invoke-WebRequest', 'iwr ', 'irm ', 'npm install', 'pip install'];
  if (blockedTokens.some(token => lower.includes(token.toLowerCase()))) {
    return { ok: false, message: '这条命令超出安全白名单。' };
  }

  const exactMap = {
    'pwd': { file: 'cmd', args: ['/c', 'cd'], mode: 'readonly' },
    'cd': { file: 'cmd', args: ['/c', 'cd'], mode: 'readonly' },
    'git status': { file: 'cmd', args: ['/c', 'git status --short --branch'], mode: 'dev' },
    'git branch': { file: 'cmd', args: ['/c', 'git branch'], mode: 'dev' },
    'git log': { file: 'cmd', args: ['/c', 'git log --oneline -5'], mode: 'dev' },
    'python --version': { file: 'cmd', args: ['/c', 'python --version'], mode: 'dev' },
    'node -v': { file: 'cmd', args: ['/c', 'node -v'], mode: 'dev' },
    'npm -v': { file: 'cmd', args: ['/c', 'npm -v'], mode: 'dev' }
  };

  if (exactMap[command]) {
    return { ok: true, ...exactMap[command], display: command };
  }

  if (lower === 'dir' || lower === 'dir /b' || lower === 'dir /a') {
    return { ok: true, file: 'cmd', args: ['/c', command], mode: 'readonly', display: command };
  }

  if (lower.startsWith('type ')) {
    const target = command.slice(5).trim();
    if (!target || target.includes('..') || target.includes('&') || target.includes('|')) {
      return { ok: false, message: '只允许读取当前目录内的安全文件路径。' };
    }
    return { ok: true, file: 'cmd', args: ['/c', `type "${target}"`], mode: 'readonly', display: command };
  }

  return { ok: false, message: '只读终端 + 开发白名单终端当前只开放少量命令。' };
}

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, configured: Boolean(client), model });
});

app.post('/api/chat', async (req, res) => {
  const history = Array.isArray(req.body?.history) ? req.body.history : [];
  const stylePreset = req.body?.stylePreset === 'ningyao' ? 'ningyao' : '';
  const screenSummary = typeof req.body?.screenSummary === 'string' ? req.body.screenSummary.trim() : '';
  const lastUser = history.filter(item => item?.role === 'user').at(-1)?.content?.trim();

  if (!lastUser) {
    res.status(400).json({ error: 'missing_user_message' });
    return;
  }

  if (!client) {
    res.status(500).json({
      error: 'missing_api_key',
      message: '还没配置 OPENAI_API_KEY。先把 .env.example 复制成 .env，再填入你的 key。'
    });
    return;
  }

  try {
    const input = history
      .filter(item => item && (item.role === 'user' || item.role === 'assistant') && typeof item.content === 'string')
      .slice(-12)
      .map(item => ({ role: item.role, content: item.content }));

    const styleInstruction = stylePreset === 'ningyao'
      ? '请保持清冽、克制、坚定的中文表达。少用感叹号，不献媚，不拖沓，句子干净，有分寸，像一个冷静锋利但会护着对方的人。'
      : '';
    const screenInstruction = screenSummary
      ? `以下是你最近一次看到的屏幕摘要，可作为当前上下文参考：${screenSummary}`
      : '';

    const response = await client.responses.create({
      model,
      input: [
        { role: 'system', content: systemPrompt + (styleInstruction ? '\n' + styleInstruction : '') + (screenInstruction ? '\n' + screenInstruction : '') },
        ...input
      ]
    });

    const text = response.output_text?.trim();
    if (!text) {
      throw new Error('empty_model_response');
    }

    res.json({ reply: text });
  } catch (error) {
    console.error(error);
    const timedOut = error?.code === 'ETIMEDOUT' || error?.cause?.code === 'ETIMEDOUT';
    res.status(500).json({
      error: timedOut ? 'upstream_timeout' : 'chat_failed',
      message: timedOut
        ? '连到 OpenAI 超时了。大概率是当前网络到 api.openai.com 不通。'
        : '模型调用失败。检查 key、模型名，或稍后再试。'
    });
  }
});

app.post('/api/screen', async (req, res) => {
  const image = typeof req.body?.image === 'string' ? req.body.image : '';
  const stylePreset = req.body?.stylePreset === 'ningyao' ? 'ningyao' : '';

  if (!image) {
    res.status(400).json({ error: 'missing_image' });
    return;
  }

  if (!client) {
    res.status(500).json({ error: 'missing_api_key', message: '还没配置 OPENAI_API_KEY。' });
    return;
  }

  try {
    const styleInstruction = stylePreset === 'ningyao'
      ? '用冷静、简洁、克制的中文，概括当前屏幕上最重要的内容。优先识别页面主题、标题、按钮、表格、聊天、代码或警告信息。不要编造看不清的细节。控制在80字以内。'
      : '请用简洁中文概括当前屏幕上最重要的内容，控制在80字以内。';

    const response = await client.responses.create({
      model,
      input: [
        {
          role: 'user',
          content: [
            { type: 'input_text', text: styleInstruction },
            { type: 'input_image', image_url: image }
          ]
        }
      ]
    });

    const summary = response.output_text?.trim();
    if (!summary) {
      throw new Error('empty_screen_response');
    }

    res.json({ summary });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'screen_failed', message: '屏幕识别失败。检查模型是否支持图像输入。' });
  }
});

app.post('/api/terminal', async (req, res) => {
  const command = req.body?.command;
  const matched = matchAllowedCommand(command);

  if (!matched.ok) {
    res.status(400).json({ error: 'blocked_command', message: matched.message });
    return;
  }

  try {
    const { stdout, stderr } = await execFileAsync(matched.file, matched.args, {
      cwd: workspaceDir,
      timeout: 10000,
      windowsHide: true,
      maxBuffer: 1024 * 1024
    });

    res.json({
      command: matched.display,
      mode: matched.mode,
      stdout: String(stdout || '').trim(),
      stderr: String(stderr || '').trim()
    });
  } catch (error) {
    res.status(500).json({
      error: 'terminal_failed',
      message: error.message || '终端执行失败。'
    });
  }
});

app.listen(port, () => {
  console.log(`Voice chat server running at http://localhost:${port}`);
});
