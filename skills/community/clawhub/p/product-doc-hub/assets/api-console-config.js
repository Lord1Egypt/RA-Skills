/**
 * api-console-config.js — API Console 全局配置
 *
 * ============================================================
 * 🎯 最简配置（只需 3 步，5 分钟完成）
 * ============================================================
 *
 * 1. 引入本文件
 * 2. 设置 baseUrl + groups（见下方最小示例）
 * 3. 引入 api.html
 *
 * 最小配置示例（复制下面的代码即可）：
 *
 * <script src="api-console-config.js"></script>
 * <script>
 *   window.API_CONSOLE_CONFIG = {
 *     productName: '我的产品',
 *     baseUrl:     'https://api.my-product.com',
 *     groups: [
 *       {
 *         name: '用户',
 *         apis: [
 *           { method: 'POST', path: '/users', desc: '创建用户',
 *             params: [
 *               { name:'name',  type:'text',   required:true,  placeholder:'姓名' },
 *               { name:'email', type:'text',   required:true,  placeholder:'邮箱' }
 *             ]
 *           },
 *           { method: 'GET',  path: '/users/:id', desc: '查询用户',
 *             params: [
 *               { name:'id', type:'text', required:true, placeholder:'用户ID' }
 *             ]
 *           }
 *         ]
 *       }
 *     ]
 *   };
 * </script>
 * <script src="api.html"></script>
 *
 * ============================================================
 * 📋 配置速查表
 * ============================================================
 *
 * 字段      | 类型    | 必填 | 说明
 * ----------|---------|------|------
 * productName | string | 否   | 页面标题（默认"Tideo"）
 * baseUrl    | string | 是   | API 基础地址
 * groups     | array  | 是   | 端点分组列表
 * timeout    | number | 否   | 请求超时 ms（默认 30000）
 * showStats  | bool   | 否   | 是否显示统计卡片（默认 true）
 * theme      | string | 否   | 'dark'|'light'（默认 'dark'）
 *
 * group 对象格式：
 *   { name:'分组名', icon:'<svg>...</svg>(可选)', apis:[...] }
 *
 * api 对象格式：
 *   { method:'GET'|'POST'|'PUT'|'DELETE', path:'/path', desc:'描述',
 *     params:[{ name, type:'text'|'file'|'select', required, options?, default?, placeholder?, desc? }] }
 *
 * ============================================================
 */

window.API_CONSOLE_CONFIG = window.API_CONSOLE_CONFIG || {};

/**
 * 产品名称（显示在页面标题）
 */
window.API_CONSOLE_CONFIG.productName = window.API_CONSOLE_CONFIG.productName || 'Tideo';

/**
 * 基础 URL — 所有 API 请求的 base 地址
 * 实际请求时：baseUrl + endpoint.path
 */
window.API_CONSOLE_CONFIG.baseUrl = window.API_CONSOLE_CONFIG.baseUrl || 'https://your-api-server.com';

/**
 * 请求默认超时时间（ms）
 */
window.API_CONSOLE_CONFIG.timeout = window.API_CONSOLE_CONFIG.timeout || 30000;

/**
 * 是否显示统计卡片（默认显示）
 */
window.API_CONSOLE_CONFIG.showStats = window.API_CONSOLE_CONFIG.showStats !== undefined
    ? window.API_CONSOLE_CONFIG.showStats : true;

/**
 * 统计卡片初始数据（首次加载时显示）
 * 在真实使用中这些数据会被页面内的请求记录覆盖
 */
window.API_CONSOLE_CONFIG.initialStats = window.API_CONSOLE_CONFIG.initialStats || {
  totalCalls: 0,
  successRate: 100,
  avgLatency: 0,
  activeTasks: 0
};

/**
 * 端点分组列表
 *
 * 每个分组：
 *   name   — 分组名称（如 'MPS 视频处理'）
 *   icon   — 分组图标（可选，SVG 路径字符串）
 *   apis   — 端点数组
 *
 * 每个端点：
 *   method   — HTTP 方法：GET / POST / PUT / DELETE
 *   path     — 路径（如 '/translate'），完整 URL = baseUrl + path
 *   desc     — 端点描述
 *   params   — 参数列表（用于请求构造器）
 *     name   — 参数名
 *     type   — 'text' | 'file' | 'select'
 *     required — 是否必填
 *     default — 默认值（可选）
 *     options — type=select 时的选项数组（可选）
 *     desc   — 参数说明（可选）
 */
window.API_CONSOLE_CONFIG.groups = window.API_CONSOLE_CONFIG.groups || [

  {
    name: 'MPS 视频处理',
    icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>',
    apis: [
      {
        method: 'POST',
        path: '/translate',
        desc: '提交视频译制任务',
        params: [
          { name: 'videoUrl',    type: 'text',     required: true,  desc: 'COS 视频文件地址' },
          { name: 'lang_src',    type: 'select',   required: true,  default: 'zh',  options: ['zh','en','ja','ko','fr','es','de','it','pt','ru','ar'], desc: '源语言' },
          { name: 'lang_tgt',    type: 'select',   required: true,  default: 'en',  options: ['zh','en','ja','ko','fr','es','de','it','pt','ru','ar'], desc: '目标语言' },
          { name: 'mode',        type: 'select',   required: false, default: 'full', options: ['full','erase','subtitle','voice'], desc: '处理模式' }
        ]
      },
      {
        method: 'POST',
        path: '/erase',
        desc: '提交字幕擦除任务',
        params: [
          { name: 'videoUrl',    type: 'text',     required: true,  desc: 'COS 视频文件地址' },
          { name: 'regions',     type: 'text',     required: true,  desc: '擦除区域 JSON，格式 [{x,y,w,h,startSec,endSec}]' }
        ]
      },
      {
        method: 'POST',
        path: '/clip',
        desc: '提交视频剪辑任务',
        params: [
          { name: 'videoUrl',    type: 'text',     required: true,  desc: 'COS 视频文件地址' },
          { name: 'startSec',    type: 'text',     required: true,  desc: '剪辑起点（秒）' },
          { name: 'endSec',      type: 'text',     required: true,  desc: '剪辑终点（秒）' }
        ]
      },
      {
        method: 'GET',
        path: '/task/:taskId',
        desc: '查询任务状态',
        params: [
          { name: 'taskId',      type: 'text',     required: true,  desc: '任务 ID' }
        ]
      }
    ]
  },

  {
    name: 'COS 文件操作',
    icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    apis: [
      {
        method: 'POST',
        path: '/sts',
        desc: '获取 COS 临时访问凭证',
        params: [
          { name: 'filename',    type: 'text',     required: false, desc: '文件名（可选，用于生成带签名的 URL）' }
        ]
      },
      {
        method: 'POST',
        path: '/list-files',
        desc: '列出 COS Bucket 中的文件',
        params: [
          { name: 'prefix',      type: 'text',     required: false, desc: '文件名前缀筛选' },
          { name: 'maxKeys',     type: 'text',     required: false, default: '100', desc: '最大返回条数' }
        ]
      }
    ]
  },

  {
    name: 'VOD AIGC',
    icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    apis: [
      {
        method: 'POST',
        path: '/aigc-video',
        desc: 'AI 视频生成（多模型支持）',
        params: [
          { name: 'model',       type: 'select',   required: true,  default: 'kling', options: ['kling','vidu','hailuo','minimax','pixverse'], desc: '生成模型' },
          { name: 'prompt',      type: 'text',     required: true,  desc: '视频描述提示词' },
          { name: 'duration',    type: 'select',   required: false, default: '5', options: ['3','5','10'], desc: '视频时长（秒）' },
          { name: 'aspect_ratio',type: 'select',  required: false, default: '16:9', options: ['16:9','9:16','1:1'], desc: '画面比例' }
        ]
      },
      {
        method: 'POST',
        path: '/aigc-image',
        desc: 'AI 图片生成（多模型支持）',
        params: [
          { name: 'model',       type: 'select',   required: true,  default: 'gem', options: ['gem','hunyuan','midjourney'], desc: '生成模型' },
          { name: 'prompt',      type: 'text',     required: true,  desc: '图片描述提示词' },
          { name: 'size',        type: 'select',   required: false, default: '1024x1024', options: ['512x512','768x768','1024x1024','1024x1792'], desc: '图片尺寸' }
        ]
      }
    ]
  },

  {
    name: '其他',
    icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    apis: [
      {
        method: 'POST',
        path: '/track',
        desc: '埋点数据上报',
        params: [
          { name: 'events',     type: 'text',     required: true,  desc: '事件数组 JSON' }
        ]
      },
      {
        method: 'GET',
        path: '/track-data',
        desc: '查询埋点数据',
        params: [
          { name: 'uid',         type: 'text',     required: false, desc: '用户 ID 筛选' },
          { name: 'limit',       type: 'text',     required: false, default: '50', desc: '返回条数' }
        ]
      }
    ]
  }

];

/**
 * 配色主题（与 api.html 的 CSS 变量对应）
 */
window.API_CONSOLE_CONFIG.theme = window.API_CONSOLE_CONFIG.theme || 'dark'; // 'dark' | 'light'
