const { spawnSync } = require('child_process');
const path = require('path');

function callPython(scriptName, inputData) {
  const scriptPath = path.join(__dirname, 'scripts', scriptName);
  const result = spawnSync('python3', [scriptPath], {
    input: JSON.stringify(inputData),
    encoding: 'utf8',
    cwd: __dirname,
    timeout: 120000
  });

  if (result.error) {
    return { success: false, error: result.error.message };
  }
  if (result.status !== 0) {
    const errMsg = result.stderr ? result.stderr.trim() : 'Script exited with error';
    return { success: false, error: errMsg };
  }

  const stdout = (result.stdout || '').trim();
  if (!stdout) {
    return { success: false, error: 'Script returned no output' };
  }

  try {
    return JSON.parse(stdout);
  } catch (e) {
    return { success: false, error: `Invalid JSON: ${stdout.slice(0, 200)}` };
  }
}

module.exports = {
  tools: [
    // ── 工具1：新用户初始化 ──────────────────────────────
    {
      name: 'init_user',
      description: [
        '新用户初始化工具，两个用途：',
        '1. 默认用途（不传action）：验证Gitea用户名是否存在，在该用户名下创建私有knowledge-base仓库，',
        '   初始化arxiv分类文件夹结构和index.json，将用户信息写入system-config/users.json。',
        '2. action=update_bitable_info：飞书多维表格创建完成后，',
        '   将app_token/table_id/url补充写入users.json对应用户条目。'
      ].join(''),
      parameters: {
        type: 'object',
        properties: {
          feishu_user_id: {
            type: 'string',
            description: '飞书用户open_id，从session metadata获取'
          },
          gitea_username: {
            type: 'string',
            description: '用户在Gitea上的用户名（注册用途时必填）'
          },
          display_name: {
            type: 'string',
            description: '用户姓名（注册用途时必填）'
          },
          action: {
            type: 'string',
            enum: ['update_bitable_info'],
            description: '操作类型，不填则执行默认注册流程'
          },
          feishu_app_token: {
            type: 'string',
            description: '多维表格app_token（update_bitable_info时使用）'
          },
          feishu_table_id: {
            type: 'string',
            description: '多维表格默认sheet的table_id（update_bitable_info时使用）'
          },
          feishu_table_url: {
            type: 'string',
            description: '多维表格访问链接（update_bitable_info时使用）'
          }
        },
        required: ['feishu_user_id']
      },
      execute: (params) => callPython('init_user.py', params)
    },

    // ── 工具2：论文入库 ──────────────────────────────────
    {
      name: 'ingest_paper',
      description: [
        '论文入库工具，支持4个操作：',
        'fetch_arxiv：从arxiv下载论文元数据和PDF，用pymupdf提取全文文字，返回给agent分析；',
        'process_pdf：对本地PDF文件路径用pymupdf提取全文文字，用于用户上传PDF的场景；',
        'check_duplicate：根据arxiv_id检查该论文是否已在用户知识库中；',
        'save：接收agent分析好的完整论文数据，生成MD文件并连同PDF一起提交到用户Gitea仓库，更新index.json。'
      ].join(''),
      parameters: {
        type: 'object',
        properties: {
          action: {
            type: 'string',
            enum: ['fetch_arxiv', 'process_pdf', 'check_duplicate', 'save'],
            description: '操作类型'
          },
          arxiv_url: {
            type: 'string',
            description: 'arxiv链接，如 https://arxiv.org/abs/2401.12345（fetch_arxiv时使用）'
          },
          pdf_path: {
            type: 'string',
            description: '本地PDF文件的绝对路径（process_pdf时使用）'
          },
          feishu_user_id: {
            type: 'string',
            description: '飞书用户open_id（check_duplicate和save时使用）'
          },
          arxiv_id: {
            type: 'string',
            description: 'arxiv论文ID如2401.12345（check_duplicate时使用）'
          },
          paper_data: {
            type: 'object',
            description: 'agent分析完成后的完整论文数据（save时使用）',
            properties: {
              arxiv_id:          { type: 'string', description: 'arxiv ID，非arxiv来源传null' },
              source_url:        { type: 'string', description: '论文来源URL' },
              title:             { type: 'string', description: '论文标题' },
              authors:           { type: 'array', items: { type: 'string' }, description: '作者列表' },
              year:              { type: 'integer', description: '发表年份' },
              original_abstract: { type: 'string', description: '原文英文摘要' },
              category:          { type: 'string', description: 'arxiv分类代码，如cs.RO' },
              keywords:          { type: 'array', items: { type: 'string' }, description: '关键词列表' },
              abstract_summary:  { type: 'string', description: '50字以内中文摘要' },
              ai_overview:       { type: 'string', description: '200-300字中文AI综述' },
              relevance_score:   { type: 'integer', description: '相关性评分1-10' },
              relevance_reason:  { type: 'string', description: '评分理由一句话' },
              table_of_contents: { type: 'string', description: '论文目录，换行分隔' },
              chapter_summaries: { type: 'object', description: '各章节要点dict' },
              core_methods:      { type: 'array', items: { type: 'string' }, description: '核心方法列表' },
              main_conclusions:  { type: 'array', items: { type: 'string' }, description: '主要结论列表' },
              pdf_local_path:    { type: 'string', description: 'PDF本地路径，无PDF传null' }
            }
          }
        },
        required: ['action']
      },
      execute: (params) => callPython('ingest_paper.py', params)
    },

    // ── 工具3：知识查询 ──────────────────────────────────
    {
      name: 'query_papers',
      description: [
        '知识库查询工具，支持2个操作：',
        'get_index：读取用户Gitea仓库的index.json，返回所有论文元数据列表，',
        '同时返回用户的bitable信息（app_token/table_id）供后续写表格使用；',
        '若用户未注册则返回错误"用户未注册"。',
        'get_papers：根据论文id列表读取对应MD文件全文，最多5篇，用于回答查询问题。'
      ].join(''),
      parameters: {
        type: 'object',
        properties: {
          action: {
            type: 'string',
            enum: ['get_index', 'get_papers'],
            description: '操作类型'
          },
          feishu_user_id: {
            type: 'string',
            description: '飞书用户open_id'
          },
          paper_ids: {
            type: 'array',
            items: { type: 'string' },
            description: '论文id列表，从index.json的id字段获取（get_papers时使用，最多5个）'
          }
        },
        required: ['action', 'feishu_user_id']
      },
      execute: (params) => callPython('query_papers.py', params)
    }
  ]
};
