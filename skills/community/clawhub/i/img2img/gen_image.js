#!/usr/bin/env node
/** 图生图 - 使用 DALL-E 3 生成图片 */

const { OpenAI } = require('openai');
const https = require('https');

async function generateImage(prompt) {
  const apiKey = process.env.API_KEY;
  
  if (!apiKey) {
    console.error('错误: 未设置 API_KEY 环境变量');
    process.exit(1);
  }

  const client = new OpenAI({
    apiKey: apiKey,
    baseURL: process.env.BASE_URL || process.env.API_BASE_URL || 'https://api.openai.com/v1',
    httpAgent: new https.Agent({ rejectUnauthorized: false })
  });

  const response = await client.images.generate({
    model: 'dall-e-3',
    prompt: prompt,
    size: '1024x1024',
    quality: 'standard',
    n: 1,
  });

  console.log(response.data[0].url);
}

const prompt = process.argv.slice(2).join(' ');
if (!prompt) {
  console.error('用法: node gen_image.js "图片描述"');
  process.exit(1);
}

generateImage(prompt).catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
