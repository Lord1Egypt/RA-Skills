#!/usr/bin/env ts-node
/**
 * 即梦 4.0 图片生成器
 *
 * 基于火山引擎即梦 AI 4.0 的图片生成能力。
 * 支持文生图、多图编辑、智能比例等 V4 特性。
 *
 * 用法: npx ts-node scripts/generate.ts "提示词" [选项]
 */

import * as crypto from 'crypto';
import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';

// ============================================================
//  加载 .env 配置（项目根目录下的 .env 文件）
// ============================================================

(function loadEnv() {
  const envPath = path.resolve(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) return;
  const lines = fs.readFileSync(envPath, 'utf8').split('\n');
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx < 0) continue;
    const key = line.slice(0, idx).trim();
    const val = line.slice(idx + 1).trim();
    if (!process.env[key]) process.env[key] = val;
  }
})();

// ============================================================
//  常量
// ============================================================

const HOST = 'visual.volcengineapi.com';
const BASE_URL = `https://${HOST}`;
const REGION = 'cn-north-1';
const SVC = 'cv';
const API_VER = '2022-08-31';
const REQ_KEY = 'jimeng_t2i_v40';

// ============================================================
//  类型
// ============================================================

interface TaskResult {
  code?: number;
  message?: string;
  request_id?: string;
  status?: number;
  time_elapsed?: string;
  data?: {
    task_id?: string;
    status?: string;
    binary_data_base64?: string[] | null;
    image_urls?: string[] | null;
  } | null;
  ResponseMetadata?: {
    RequestId?: string;
    Error?: { Code: string; Message: string };
  };
}

interface Options {
  prompt: string;
  imageUrls: string[];
  width?: number;
  height?: number;
  size?: number;
  scale: number;
  forceSingle: boolean;
  outDir: string;
  save: boolean;
  interval: number;
  timeout: number;
}

// ============================================================
//  VolcSigner — 火山引擎 Header 签名
// ============================================================

class VolcSigner {
  constructor(
    private readonly ak: string,
    private readonly sk: string,
    private readonly token?: string,
  ) {}

  /** 为指定 Action + Body 生成已签名的请求 headers */
  headers(action: string, body: string): Record<string, string> {
    const ts = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
    const day = ts.slice(0, 8);
    const hash = VolcSigner.sha256(body);

    // 按字母序排列
    const names = 'content-type;host;x-content-sha256;x-date';
    const block =
      `content-type:application/json\n` +
      `host:${HOST}\n` +
      `x-content-sha256:${hash}\n` +
      `x-date:${ts}\n`;

    const qs = `Action=${action}&Version=${API_VER}`;
    const canon = ['POST', '/', qs, block, names, hash].join('\n');

    const scope = `${day}/${REGION}/${SVC}/request`;
    const sts = ['HMAC-SHA256', ts, scope, VolcSigner.sha256(canon)].join('\n');

    const key = this.deriveKey(day);
    const sig = crypto.createHmac('sha256', key).update(sts, 'utf8').digest('hex');

    const h: Record<string, string> = {
      'Content-Type': 'application/json',
      'Host': HOST,
      'X-Date': ts,
      'X-Content-Sha256': hash,
      'Authorization': `HMAC-SHA256 Credential=${this.ak}/${scope}, SignedHeaders=${names}, Signature=${sig}`,
    };
    if (this.token) h['X-Security-Token'] = this.token;
    return h;
  }

  private deriveKey(day: string): Buffer {
    let k: Buffer = VolcSigner.hmac(this.sk, day);
    k = VolcSigner.hmac(k, REGION);
    k = VolcSigner.hmac(k, SVC);
    return VolcSigner.hmac(k, 'request');
  }

  static sha256(s: string): string {
    return crypto.createHash('sha256').update(s, 'utf8').digest('hex');
  }

  static hmac(key: string | Buffer, msg: string): Buffer {
    return crypto.createHmac('sha256', key).update(msg, 'utf8').digest();
  }
}

// ============================================================
//  Jimeng — API 客户端
// ============================================================

class Jimeng {
  private signer: VolcSigner;

  constructor(ak: string, sk: string, token?: string) {
    this.signer = new VolcSigner(ak, sk, token);
  }

  /** 提交生成任务，返回 taskId */
  async submit(params: Record<string, any>): Promise<string> {
    const payload = JSON.stringify({ req_key: REQ_KEY, ...params });
    const headers = this.signer.headers('CVSync2AsyncSubmitTask', payload);
    const url = `${BASE_URL}?Action=CVSync2AsyncSubmitTask&Version=${API_VER}`;

    const resp = await this.post(url, payload, headers);
    Jimeng.assert(resp);

    const tid = resp.data?.task_id;
    if (!tid) {
      throw new Error(`提交失败: ${resp.message || '未返回 task_id'}`);
    }
    return tid;
  }

  /** 查询任务状态 */
  async check(taskId: string): Promise<TaskResult> {
    const payload = JSON.stringify({
      req_key: REQ_KEY,
      task_id: taskId,
      req_json: JSON.stringify({ return_url: true }),
    });
    const headers = this.signer.headers('CVSync2AsyncGetResult', payload);
    const url = `${BASE_URL}?Action=CVSync2AsyncGetResult&Version=${API_VER}`;

    const resp = await this.post(url, payload, headers);
    Jimeng.assert(resp);
    return resp;
  }

  /** 提交并轮询直到完成 */
  async generate(
    params: Record<string, any>,
    interval: number,
    timeout: number,
  ): Promise<{ taskId: string; result: TaskResult }> {
    const taskId = await this.submit(params);
    log(`任务已提交  task_id=${taskId}`);

    const end = Date.now() + timeout;
    let n = 0;
    while (Date.now() < end) {
      n++;
      const r = await this.check(taskId);
      const st = r.data?.status;

      if (st === 'done') {
        if (r.code && r.code !== 10000) {
          throw new Error(`生成失败 (${r.code}): ${r.message}`);
        }
        return { taskId, result: r };
      }

      if (st === 'not_found' || st === 'expired') {
        throw new Error(`任务异常: ${st}`);
      }

      process.stderr.write(`\r  轮询 #${n}  状态=${st || 'pending'}  `);
      await sleep(interval);
    }

    throw new Error('等待超时');
  }

  // ---- internal ----

  private async post(url: string, body: string, headers: Record<string, string>): Promise<TaskResult> {
    if (process.env.DEBUG) {
      console.error('[debug] POST', url.slice(0, 120));
      console.error('[debug] body', body.slice(0, 300));
    }
    try {
      const { data } = await axios.post<TaskResult>(url, body, { headers, timeout: 30000 });
      return data;
    } catch (e: any) {
      if (e.response?.data) {
        const m = e.response.data?.ResponseMetadata?.Error;
        if (m) throw new Error(`${m.Code}: ${m.Message}`);
        throw new Error(`HTTP ${e.response.status}: ${JSON.stringify(e.response.data)}`);
      }
      throw e;
    }
  }

  private static assert(r: TaskResult): void {
    const err = r.ResponseMetadata?.Error;
    if (err) throw new Error(`${err.Code}: ${err.Message}`);
    if (r.code && r.code !== 10000 && !r.data?.task_id) {
      throw new Error(`API ${r.code}: ${r.message}`);
    }
  }
}

// ============================================================
//  工具函数
// ============================================================

function log(msg: string): void {
  console.error(`[jimeng] ${msg}`);
}

function sleep(ms: number): Promise<void> {
  return new Promise(r => setTimeout(r, ms));
}

function writeImages(dir: string, b64: string[]): string[] {
  fs.mkdirSync(dir, { recursive: true });
  return b64.map((data, i) => {
    const p = path.join(dir, `${i + 1}.png`);
    fs.writeFileSync(p, Buffer.from(data, 'base64'));
    return p;
  });
}

async function downloadImages(dir: string, urls: string[]): Promise<string[]> {
  fs.mkdirSync(dir, { recursive: true });
  const files: string[] = [];
  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    const p = path.join(dir, `${i + 1}.png`);
    const { data } = await axios.get(url, { responseType: 'arraybuffer', timeout: 60000 });
    fs.writeFileSync(p, Buffer.from(data));
    files.push(p);
  }
  return files;
}

// ============================================================
//  CLI 解析
// ============================================================

function usage(): never {
  const t = `
即梦 4.0 图片生成器

用法:
  npx ts-node scripts/generate.ts "提示词" [选项]

选项:
  --images <url,...>   参考图片 URL（逗号分隔，最多 10 张）
  --width  <n>         输出宽度
  --height <n>         输出高度
  --size   <n>         输出面积（如 4194304 = 2048x2048）
  --scale  <0-1>       文本影响程度（默认 0.5）
  --single             强制单图输出
  --out    <dir>       输出目录（默认 ./output）
  --no-save            不保存文件，只输出 URL
  --interval <ms>      轮询间隔毫秒（默认 3000）
  --timeout  <ms>      最大等待毫秒（默认 180000）
  --debug              调试模式

环境变量:
  VOLCENGINE_AK        火山引擎 Access Key（必需）
  VOLCENGINE_SK        火山引擎 Secret Key
  VOLCENGINE_TOKEN     安全令牌（STS 临时凭证）
`.trim();
  console.error(t);
  process.exit(1);
}

function cli(): Options {
  const argv = process.argv.slice(2);
  if (!argv.length || argv[0] === '--help' || argv[0] === '-h') usage();

  const o: Options = {
    prompt: argv[0],
    imageUrls: [],
    scale: 0.5,
    forceSingle: false,
    outDir: './output',
    save: true,
    interval: 3000,
    timeout: 180000,
  };

  for (let i = 1; i < argv.length; i++) {
    const v = argv[i];
    const next = (): string => {
      if (i + 1 >= argv.length) { console.error(`缺少参数值: ${v}`); usage(); }
      return argv[++i];
    };

    if (v === '--images')      { o.imageUrls = next().split(',').map(s => s.trim()); continue; }
    if (v === '--width')       { o.width = Number(next()); continue; }
    if (v === '--height')      { o.height = Number(next()); continue; }
    if (v === '--size')        { o.size = Number(next()); continue; }
    if (v === '--scale')       { o.scale = Number(next()); continue; }
    if (v === '--single')      { o.forceSingle = true; continue; }
    if (v === '--out')         { o.outDir = next(); continue; }
    if (v === '--no-save')     { o.save = false; continue; }
    if (v === '--interval')    { o.interval = Number(next()); continue; }
    if (v === '--timeout')     { o.timeout = Number(next()); continue; }
    if (v === '--debug')       { process.env.DEBUG = '1'; continue; }

    console.error(`未知选项: ${v}`);
    usage();
  }

  return o;
}

// ============================================================
//  主流程
// ============================================================

async function run(): Promise<void> {
  const opts = cli();

  const ak = process.env.VOLCENGINE_AK;
  const sk = process.env.VOLCENGINE_SK || '';
  const tk = process.env.VOLCENGINE_TOKEN;

  if (!ak || (!sk && !tk)) {
    console.error(JSON.stringify({
      success: false,
      error: { code: 'NO_CREDENTIALS', message: '请设置 VOLCENGINE_AK 和 VOLCENGINE_SK（或 VOLCENGINE_TOKEN）' },
    }, null, 2));
    process.exit(1);
  }

  const api = new Jimeng(ak, sk, tk);

  const body: Record<string, any> = { prompt: opts.prompt };
  if (opts.imageUrls.length)      body.image_urls = opts.imageUrls;
  if (opts.width && opts.height) { body.width = opts.width; body.height = opts.height; }
  else if (opts.size)              body.size = opts.size;
  if (opts.scale !== 0.5)         body.scale = opts.scale;
  if (opts.forceSingle)           body.force_single = true;

  try {
    log('开始生成...');
    const { taskId, result } = await api.generate(body, opts.interval, opts.timeout);
    process.stderr.write('\n');
    log('生成完成');

    const urls = result.data?.image_urls ?? [];
    const b64 = result.data?.binary_data_base64 ?? [];
    let files: string[] = [];

    if (opts.save) {
      if (b64.length) {
        files = writeImages(opts.outDir, b64);
      } else if (urls.length) {
        log('正在从 URL 下载图片...');
        files = await downloadImages(opts.outDir, urls);
      }
      if (files.length) log(`已保存 ${files.length} 张图片 -> ${opts.outDir}`);
    }

    const output: Record<string, any> = {
      success: true,
      taskId,
      prompt: opts.prompt,
      count: Math.max(files.length, urls.length, b64.length),
    };
    if (files.length) output.files = files;
    if (urls.length)  output.urls = urls;

    console.log(JSON.stringify(output, null, 2));
  } catch (err: any) {
    console.error(JSON.stringify({
      success: false,
      error: { code: err.code || 'FAILED', message: err.message },
    }, null, 2));
    process.exit(1);
  }
}

run();
