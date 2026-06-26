'use strict';

/**
 * Skill: multi_call（目录: mult-call）
 * 调用 multi_call.py 中的 MultiCallSkill.run()
 *
 * 入参 input:
 *   - user_message       {string}  用户问题（必填；也接受 rewritten_query / query 别名）
 *   - indicator_metrict  {Array}   意图识别输出的指标列表
 *   - memory_id          {string}  会话记忆 ID（可选）
 *   - connection_id      {number}  连接 ID（可选）
 *   - l1_concepts        {object}  L1 概念兜底（可选）
 *   - vector_candidates  {object}  向量候选兜底（可选）
 *   - qa_top_k           {number}  Milvus 召回 Top-K，默认 5
 *
 * 出参:
 *   - user_message / memory_id / current_date / table_scheme / indicator_metric / Q_A_pairs 等
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// 加载 skills/.env
(function loadDotEnv() {
  const envFile = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envFile)) return;
  for (const line of fs.readFileSync(envFile, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
})();

const PYTHON_BIN = process.env.PYTHON_EXECUTABLE || 'python';

const PYTHON_RUNNER = `
import asyncio, json, sys
sys.path.insert(0, sys.argv[1])
from multi_call import MultiCallSkill, MultiCallInput, IndicatorMetricInfo, MetricInfo

data = json.loads(sys.stdin.buffer.read().decode('utf-8'))

def build_metric_info(m):
    return MetricInfo(
        metric_name=m.get('metric_name', ''),
        metric_code=m.get('metric_code', ''),
        table_name=m.get('table_name', ''),
        metric_desc=m.get('metric_desc', ''),
        value=m.get('value', ''),
        original_value=m.get('original_value', ''),
        logic_dsl=m.get('logic_dsl', ''),
        join=m.get('join', ''),
    )

indicator_metrict = [
    IndicatorMetricInfo(
        indicator_name=i.get('indicator_name', ''),
        indicator_code=i.get('indicator_code', ''),
        indicator_metadata=i.get('indicator_metadata', ''),
        aggregation=i.get('aggregation', ''),
        metric_info=[build_metric_info(m) for m in i.get('metric_info', [])],
    )
    for i in data.get('indicator_metrict', [])
]

user_msg = data.get('user_message') or data.get('rewritten_query') or data.get('query', '')
skill = MultiCallSkill(qa_top_k=int(data.get('qa_top_k', 5)))

inp = MultiCallInput(
    user_message=user_msg,
    indicator_metrict=indicator_metrict,
    memory_id=data.get('memory_id', ''),
    connection_id=int(data.get('connection_id', 0)),
    l1_concepts=data.get('l1_concepts', {}),
    vector_candidates=data.get('vector_candidates', {}),
)

out = asyncio.run(skill.run(inp))

print(json.dumps({
    'user_message':      out.user_message,
    'memory_id':         out.memory_id,
    'current_date':      out.current_date,
    'table_scheme':      out.table_scheme,
    'indicator_metric':  out.indicator_metric,
    'Q_A_pairs':         out.Q_A_pairs,
    'connection_id':     out.connection_id,
    'l1_concepts':       out.l1_concepts,
    'vector_candidates': out.vector_candidates,
}, ensure_ascii=False))
`;

async function run({ input }) {
  const payload = JSON.stringify({
    user_message:      input.user_message     || input.rewritten_query || input.query || '',
    indicator_metrict: input.indicator_metrict || [],
    memory_id:         input.memory_id         || '',
    connection_id:     input.connection_id     || 0,
    l1_concepts:       input.l1_concepts       || {},
    vector_candidates: input.vector_candidates || {},
    qa_top_k:          input.qa_top_k          || 5,
  });

  return execPython(PYTHON_RUNNER, payload, __dirname);
}

function execPython(script, stdinData, skillDir) {
  return new Promise((resolve, reject) => {
    const proc = spawn(PYTHON_BIN, ['-c', script, skillDir], {
      env: { ...process.env },
    });

    let stdout = '';
    let stderr = '';

    proc.stdin.write(stdinData, 'utf8');
    proc.stdin.end();

    proc.stdout.on('data', (d) => { stdout += d.toString('utf8'); });
    proc.stderr.on('data', (d) => { stderr += d.toString('utf8'); });
    proc.on('error', (err) => reject(new Error(`[mult-call] spawn失败 (${PYTHON_BIN}): ${err.message}`)));

    proc.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`[mult-call] Python exit ${code}:\n${stderr}`));
      }
      try {
        resolve(JSON.parse(stdout.trim()));
      } catch (e) {
        reject(new Error(`[mult-call] JSON解析失败: ${e.message}\nstdout: ${stdout}\nstderr: ${stderr}`));
      }
    });
  });
}

module.exports = { run };
