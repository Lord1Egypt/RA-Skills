/**
 * KreadoAI CLI 辅助工具（零外部依赖）
 * 参数解析、鉴权
 */
import { getApiToken, CredentialsMissingError, setSkillVersion } from './auth.mjs';

function consumeSkillVersionArgv(argv) {
  for (let i = 2; i < argv.length - 1; i++) {
    if (argv[i] === '--skill-version') {
      setSkillVersion(argv[i + 1]);
      argv.splice(i, 2);
      return;
    }
  }
}

/**
 * 解析命令行参数
 * @param {string[]} argv process.argv
 * @param {string[]} [booleanFlags] 布尔标志名
 * @returns {object} 参数键值对
 */
export function parseArgs(argv, booleanFlags = []) {
  consumeSkillVersionArgv(argv);
  const boolSet = new Set(['help', 'download', 'wait', 'no-wait', ...booleanFlags]);
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith('--')) continue;
    const name = key.slice(2);
    if (name === 'no-wait') { args.wait = false; continue; }
    if (boolSet.has(name)) { args[name] = true; continue; }
    const val = argv[i + 1];
    if (val !== undefined && !val.startsWith('--')) {
      args[name] = val; i++;
    } else {
      args[name] = true;
    }
  }
  return args;
}

/**
 * 获取 API Token 或退出
 */
export function getTokenOrExit() {
  try {
    return getApiToken();
  } catch (e) {
    if (e instanceof CredentialsMissingError || e?.name === 'CredentialsMissingError') {
      console.error(`\n错误：${e.message}`);
      console.error('\n配置方法：');
      console.error('  1. 设置环境变量：export KREADO_API_TOKEN="your_token"');
      console.error('  2. 或运行：node kreado.mjs account --configure');
      console.error('  3. 获取 Token：https://www.kreadoai.com/ -> 账号 -> API 设置\n');
      process.exit(1);
    }
    throw e;
  }
}

/**
 * 轮询异步任务直到完成
 * @param {function} queryFn 查询函数，返回 { status, ...data }
 * @param {object} opts 选项
 */
export async function pollTask(queryFn, opts = {}) {
  const interval = opts.interval || 5000;
  const timeout = opts.timeout || 600000;
  const deadline = Date.now() + timeout;

  while (Date.now() < deadline) {
    const result = await queryFn();
    const status = Number(result.status);
    if (status === 3) return result;
    if (status === 4) throw new Error('任务失败');
    if (status === 5) throw new Error('任务超时');
    console.error(`  状态：${statusText(status)} ... 等待 ${interval / 1000} 秒`);
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error('轮询超时');
}

function statusText(status) {
  const map = { 1: '等待中', 2: '处理中', 3: '成功', 4: '失败', 5: '超时' };
  return map[status] || `未知(${status})`;
}
