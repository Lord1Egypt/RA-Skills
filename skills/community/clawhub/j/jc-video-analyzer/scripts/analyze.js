/**
 * AI 分析脚本：读取转写文本，调用中转站 GPT-5.5 进行深度分析
 *
 * 用法：node analyze.js <transcript.txt> <output.md>
 * 环境：需要 OpenClaw 的 SU2_API_KEY（自动从 openclaw.json 读取）
 */

const fs = require('fs');
const path = require('path');

// ─── 加载 API 配置 ───────────────────────────
const cfgPath = path.join(process.env.USERPROFILE || '', '.openclaw', 'openclaw.json');
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
const apiKey = cfg.env?.SU2_API_KEY;
const baseUrl = cfg.models?.providers?.zhongzhuan?.baseUrl || 'https://claude-zhongzhuan.cloud/v1';

if (!apiKey) {
  console.error('ERROR: SU2_API_KEY not found in openclaw.json env.');
  process.exit(1);
}

// ─── CLI 参数 ─────────────────────────────────
const inputPath = process.argv[2];
const outputPath = process.argv[3];

if (!inputPath || !outputPath) {
  console.error('用法：node analyze.js <transcript.txt> <output.md>');
  process.exit(1);
}

const transcript = fs.readFileSync(inputPath, 'utf-8');

// ─── 分析提示词 ───────────────────────────────
const ANALYSIS_PROMPT = `你是一位技术分析师。以下是一段视频转写文本（可能有同音错误，如"洋龙虾"=OpenClaw、"喝门死"=Hermes）。

请根据上下文修正错误词汇并产出：

## 1. 修正后的文字稿
修复所有同音/错别字，保留时间戳 [xx.xs - xx.xs]。

## 2. 核心观点总结（5-8条）
每条：观点 + 视频依据。

## 3. 结构化对比分析
用表格或要点对比视频中讨论的对象。

## 4. 最终结论

## 5. 对我的启示
我是名叫坦坦的 AI agent，这个视频对我有什么启示？

原始转写文本：
${transcript}`;

async function main() {
  console.log(`Transcript: ${transcript.length} chars`);
  console.log(`Calling GPT-5.5 (${baseUrl})...`);

  const res = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'gpt-5.5',
      messages: [
        { role: 'system', content: '你是一位专业的技术分析助理。' },
        { role: 'user', content: ANALYSIS_PROMPT },
      ],
      max_tokens: 8192,
      temperature: 0.3,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API ${res.status}: ${err.slice(0, 300)}`);
  }

  const data = await res.json();
  const analysis = data.choices?.[0]?.message?.content;

  if (!analysis) {
    throw new Error('Empty response from API');
  }

  fs.writeFileSync(outputPath, analysis, 'utf-8');
  console.log(`Saved: ${outputPath} (${analysis.length} chars)`);
  console.log('');
  console.log('=== PREVIEW (first 400 chars) ===');
  console.log(analysis.slice(0, 400));
}

main().catch((e) => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
