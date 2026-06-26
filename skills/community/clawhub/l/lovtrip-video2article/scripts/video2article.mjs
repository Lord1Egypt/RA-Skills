#!/usr/bin/env node

/**
 * video2article.mjs — 独立 Gemini 视频转文章脚本
 *
 * 用法:
 *   GEMINI_API_KEY=xxx node video2article.mjs <youtube-url> [language]
 *
 * 示例:
 *   node video2article.mjs "https://www.youtube.com/watch?v=..." "Chinese (Simplified)"
 *   node video2article.mjs "https://www.youtube.com/watch?v=..." "English"
 *
 * 依赖: 仅需 Node.js 18+（使用内置 fetch）
 */

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
if (!GEMINI_API_KEY) {
  console.error('Error: GEMINI_API_KEY 环境变量未设置');
  console.error('获取: https://aistudio.google.com/apikey');
  process.exit(1);
}

const videoUrl = process.argv[2];
if (!videoUrl) {
  console.error('用法: node video2article.mjs <youtube-url> [language]');
  console.error('示例: node video2article.mjs "https://www.youtube.com/watch?v=dQw4w9WgXcQ"');
  process.exit(1);
}

const language = process.argv[3] || 'Chinese (Simplified)';

const DEFAULT_PROMPT = `You are a helpful writing assistant. Your task is to watch a video and then write an article about it from a first-person perspective.

Imagine you've just watched the video and are sharing your key takeaways, insights, and what you learned. Use "I" and "my" to frame the content as a personal reflection. The article should be engaging, informative, and easy to read for someone who hasn't seen the video.

The article should have the following structure:
1.  A compelling and descriptive title that reflects a personal take on the video's content.
2.  A concise summary (2-4 sentences) that captures what you found to be the main points of the video.
3.  A detailed body that expands on the key concepts, explains important information, and provides context, all from your first-person viewpoint.

**Formatting guidelines for the 'body' field:**
- Use Markdown for formatting.
- Use '##' for main section headings.
- Use '**' to bold important keywords or phrases.
- Use '*' or '-' for bullet points in lists.

Provide the result as a single JSON object containing four fields: "title", "author", "summary", and "body". The "author" field should contain the name of the YouTube channel that created the video. The "body" field should contain the full text of the article in Markdown format.`;

async function main() {
  console.error(`Processing: ${videoUrl}`);
  console.error(`Language: ${language}`);
  console.error('');

  const finalPrompt = `${DEFAULT_PROMPT}\n\nIMPORTANT: The entire JSON response, including keys and values, must be in the following language: ${language}.`;

  const requestBody = {
    contents: [
      {
        role: 'user',
        parts: [
          { text: finalPrompt },
          {
            fileData: {
              mimeType: 'video/mp4',
              fileUri: videoUrl,
            },
          },
        ],
      },
    ],
    generationConfig: {
      temperature: 0.75,
      responseMimeType: 'application/json',
      responseSchema: {
        type: 'OBJECT',
        properties: {
          title: { type: 'STRING', description: 'Article title' },
          author: { type: 'STRING', description: 'YouTube channel name' },
          summary: { type: 'STRING', description: '2-4 sentence summary' },
          body: { type: 'STRING', description: 'Full article in Markdown' },
        },
        required: ['title', 'author', 'summary', 'body'],
      },
    },
  };

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${GEMINI_API_KEY}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const error = await response.text();
    console.error(`API Error (${response.status}): ${error}`);
    process.exit(1);
  }

  const data = await response.json();

  if (data.promptFeedback?.blockReason) {
    console.error(`Content blocked: ${data.promptFeedback.blockReason}`);
    process.exit(1);
  }

  if (!data.candidates || data.candidates.length === 0) {
    console.error('No response from Gemini');
    process.exit(1);
  }

  const candidate = data.candidates[0];
  if (candidate.finishReason && candidate.finishReason !== 'STOP') {
    console.error(`Generation stopped: ${candidate.finishReason}`);
    process.exit(1);
  }

  const text = candidate.content?.parts?.[0]?.text;
  if (!text) {
    console.error('Empty response');
    process.exit(1);
  }

  try {
    const article = JSON.parse(text);
    console.log(JSON.stringify(article, null, 2));
  } catch {
    // If not valid JSON, output raw text
    console.log(text);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
