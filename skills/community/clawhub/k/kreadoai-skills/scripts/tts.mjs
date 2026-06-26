#!/usr/bin/env node
/**
 * KreadoAI — 文字转语音：查询语言、查询声音、提交合成任务
 */
import { kreadoPost, kreadoGet } from './shared/client.mjs';
import { parseArgs, getTokenOrExit } from './shared/args.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const API_GET_LANGUAGES = '/apis/open/voice/v3/getVoiceLanguage';
const API_GET_VOICES = '/apis/open/voice/v3/getVoiceList';
const API_TEXT_TO_SPEECH = '/apis/open/voice/v3/textToSpeech';

function printHelp() {
  console.log(`KreadoAI tts — 文字转语音

用法：
  node kreado.mjs tts [选项]

操作：
  --languages            列出支持的语言
  --voices               列出可用声音
  --synthesize           提交文字转语音任务

--voices 参数：
  --language <name>      语言（英文名称，如 "Chinese"）（必填）
  --language_city <type> 方言/地区
  --gender <f|m>         "female" 或 "male"
  --age <group>          "children", "young", "middle-aged", "old"
  --voice_clone <0|1>    0=否，1=是（必填）
  --voice_source <n>     1=微软, 3=阿里巴巴, 4=字节跳动, 5=MiniMax, 6=谷歌, 21=ElevenLabs
  --page <n>             页码（默认：1）
  --page_size <n>        每页数量（默认：10）

--synthesize 参数：
  --language_id <id>     语言 ID（必填）
  --content <text>       文本内容（必填）
  --voice_id <id>        声音 ID（必填）
  --voice_clone <0|1>    0=否，1=是（必填）
  --voice_source <n>     声音来源（必填）
  --style_id <id>        风格 ID
  --volume <n>           音量（范围取决于 voice_source）
  --speed <n>            语速
  --pitch <n>            音调

示例：
  node kreado.mjs tts --languages
  node kreado.mjs tts --voices --language "Chinese" --voice_clone 0 --voice_source 3 --gender "male"
  node kreado.mjs tts --synthesize --language_id "1767068435675340832" --content "你好世界" --voice_id "zhida" --voice_clone 0 --voice_source 3`);
}

async function getLanguages(token) {
  const data = await kreadoGet(API_GET_LANGUAGES, token);
  console.log(JSON.stringify(data, null, 2));
}

async function getVoices(args, token) {
  if (!args.language) { console.error('错误：--language 为必填项'); process.exit(1); }

  const body = {
    language: args.language,
    voiceClone: parseInt(args.voice_clone || '0', 10),
    voiceSource: parseInt(args.voice_source || '1', 10),
    pageIndex: parseInt(args.page || '1', 10),
    pageSize: parseInt(args.page_size || '10', 10),
  };
  if (args.language_city) body.languageCityType = args.language_city;
  if (args.gender) body.gender = args.gender;
  if (args.age) body.ageGroup = args.age;

  const data = await kreadoPost(API_GET_VOICES, body, token);
  console.log(JSON.stringify(data, null, 2));
}

async function synthesize(args, token) {
  if (!args.language_id) { console.error('错误：--language_id 为必填项'); process.exit(1); }
  if (!args.content) { console.error('错误：--content 为必填项'); process.exit(1); }
  if (!args.voice_id) { console.error('错误：--voice_id 为必填项'); process.exit(1); }

  const body = {
    languageId: args.language_id,
    content: args.content,
    voiceId: args.voice_id,
    voiceClone: parseInt(args.voice_clone || '0', 10),
    voiceSource: parseInt(args.voice_source || '1', 10),
  };
  if (args.style_id) body.styleId = args.style_id;
  if (args.volume) body.volume = parseInt(args.volume, 10);
  if (args.speed) body.prosodyRate = parseInt(args.speed, 10);
  if (args.pitch) body.prosodyPitch = parseInt(args.pitch, 10);

  const data = await kreadoPost(API_TEXT_TO_SPEECH, body, token);
  console.error('✓ 语音合成完成');
  console.log(JSON.stringify(data, null, 2));
}

export async function main() {
  const args = parseArgs(process.argv, ['languages', 'voices', 'synthesize']);

  if (args.help) {
    printHelp();
    return;
  }

  const token = getTokenOrExit();

  if (args.languages) {
    await getLanguages(token);
  } else if (args.voices) {
    await getVoices(args, token);
  } else if (args.synthesize) {
    await synthesize(args, token);
  } else {
    printHelp();
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`错误：${e?.message || e}`);
    process.exit(1);
  });
}
