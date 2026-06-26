/**
 * AI 图表提取器 v2.0
 *
 * 从 PRD 数据中提取图表信息：
 * - 业务流程（从 inputs/outputs 推断）
 * - 原型布局（从 inputs/outputs 生成）
 * - 架构信息（从 PRD 提取）→ 架构图 Mermaid
 * - 功能结构（从 features 生成）→ 功能框架图 Mermaid
 *
 * v2.0 新增：
 * - architectureToMermaid() 架构图生成
 * - generatePrototypeConfig() 原型配置生成
 */

const path = require('path');

class AIDiagramExtractor {
  constructor() {
    this.version = '2.0';
  }

  /**
   * 从功能信息推断业务流程
   *
   * @param {Object} feature - 功能信息 { name, inputs, outputs, businessRules }
   * @returns {Object} - 流程数据 { steps, connections }
   */
  async extractFlow(feature) {
    const inputs = feature.inputs || [];
    const outputs = feature.outputs || [];
    const rules = feature.businessRules || [];
    const featureName = feature.name || '功能';

    // 构建 AI 提示词
    const prompt = this.buildFlowPrompt(featureName, inputs, outputs, rules);

    // 调用 AI 或使用规则推断
    const flowData = await this.inferFlow(inputs, outputs, rules, featureName);

    return flowData;
  }

  /**
   * 构建流程提取提示词
   */
  buildFlowPrompt(featureName, inputs, outputs, rules) {
    return `
根据以下功能信息，生成业务流程图数据：

功能名称：${featureName}

输入字段：
${inputs.map(i => `- ${i.field}（${i.type}，${i.required ? '必填' : '可选'}）：${i.description || ''}`).join('\n')}

输出字段：
${outputs.map(o => `- ${o.field}（${o.type}）：${o.description || ''}`).join('\n')}

业务规则：
${rules.map(r => `- ${r.name}：${r.description}`).join('\n')}

请返回 JSON 格式的流程数据：
{
  "steps": [
    { "id": "start", "name": "开始", "type": "start" },
    { "id": "input", "name": "用户输入", "type": "action" },
    ...
  ],
  "connections": [
    { "from": "start", "to": "input" },
    ...
  ]
}
`;
  }

  /**
   * 推断流程（规则 + AI 混合）
   * 注：此方法为同步方法，便于在模板中直接调用
   */
  inferFlow(inputs, outputs, rules, featureName) {
    const steps = [];
    const connections = [];

    // 1. 开始节点
    steps.push({ id: 'start', name: '用户打开页面', type: 'start' });

    // 2. 输入步骤（根据 inputs 生成）
    if (inputs.length > 0) {
      const inputStep = {
        id: 'input',
        name: `输入${inputs.map(i => i.field).join('、')}`,
        type: 'action',
        description: `用户输入${inputs.length}个字段`
      };
      steps.push(inputStep);
      connections.push({ from: 'start', to: 'input' });
    }

    // 3. 校验步骤（根据 businessRules 生成）
    if (rules.length > 0) {
      const validateStep = {
        id: 'validate',
        name: '参数校验',
        type: 'decision',
        description: `校验${rules.length}条规则`
      };
      steps.push(validateStep);

      if (inputs.length > 0) {
        connections.push({ from: 'input', to: 'validate' });
      } else {
        connections.push({ from: 'start', to: 'validate' });
      }

      // 校验失败分支
      const errorStep = {
        id: 'error',
        name: '显示错误提示',
        type: 'action'
      };
      steps.push(errorStep);
      connections.push({ from: 'validate', to: 'error', label: '失败' });
      connections.push({ from: 'error', to: 'input' }); // 返回修改
    }

    // 4. 处理步骤
    const processStep = {
      id: 'process',
      name: `执行${featureName}`,
      type: 'action',
      description: '调用后端接口处理'
    };
    steps.push(processStep);

    if (rules.length > 0) {
      connections.push({ from: 'validate', to: 'process', label: '通过' });
    } else if (inputs.length > 0) {
      connections.push({ from: 'input', to: 'process' });
    } else {
      connections.push({ from: 'start', to: 'process' });
    }

    // 5. 输出步骤
    if (outputs.length > 0) {
      const outputStep = {
        id: 'output',
        name: `展示${outputs.slice(0, 2).map(o => o.description || o.field).join('、')}等结果`,
        type: 'action'
      };
      steps.push(outputStep);
      connections.push({ from: 'process', to: 'output' });
    }

    // 6. 结束节点
    steps.push({ id: 'end', name: '结束', type: 'end' });
    if (outputs.length > 0) {
      connections.push({ from: 'output', to: 'end' });
    } else {
      connections.push({ from: 'process', to: 'end' });
    }

    return { steps, connections };
  }

  /**
   * 流程数据转 Mermaid 代码
   *
   * @param {Object} flowData - { steps, connections }
   * @returns {string} - Mermaid 代码
   */
  flowToMermaid(flowData) {
    const { steps, connections } = flowData;

    let code = 'flowchart TD\n';

    // 添加节点
    for (const step of steps) {
      const safeName = step.name.replace(/"/g, "'");
      if (step.type === 'start' || step.type === 'end') {
        code += `    ${step.id}(["${safeName}"])\n`;
      } else if (step.type === 'decision') {
        code += `    ${step.id}{"${safeName}"}\n`;
      } else {
        code += `    ${step.id}["${safeName}"]\n`;
      }
    }

    // 添加连接
    for (const conn of connections) {
      if (conn.label) {
        const safeLabel = conn.label.replace(/"/g, "'");
        code += `    ${conn.from} -->|"${safeLabel}"| ${conn.to}\n`;
      } else {
        code += `    ${conn.from} --> ${conn.to}\n`;
      }
    }

    return code;
  }

  /**
   * 从 inputs/outputs 提取原型布局信息
   *
   * @param {Object} feature - 功能信息
   * @returns {Object} - 布局数据 { formFields, tableColumns, layout }
   */
  async extractPrototypeLayout(feature) {
    const inputs = feature.inputs || [];
    const outputs = feature.outputs || [];
    const featureName = feature.name || '功能';

    // 表单字段 = inputs
    const formFields = inputs.map(input => ({
      label: input.field,
      type: this.mapInputType(input.type),
      required: input.required,
      placeholder: `请输入${input.field}`,
      validation: input.validation,
      error: input.error
    }));

    // 表格列 = outputs + 操作列
    const tableColumns = outputs.map(output => ({
      field: output.field,
      label: output.description || output.field,
      type: output.type,
      example: output.example
    }));
    tableColumns.push({ field: 'actions', label: '操作', type: 'actions' });

    // 生成 ASCII 布局
    const layout = this.generateLayout(featureName, formFields, tableColumns);

    return {
      formFields,
      tableColumns,
      layout
    };
  }

  /**
   * 映射输入类型到表单类型
   */
  mapInputType(inputType) {
    const typeMap = {
      '整数': 'number',
      '数字': 'number',
      '数字 (2位小数)': 'number',
      '字符串': 'text',
      '文本': 'textarea',
      '日期': 'date',
      '日期时间': 'datetime-local',
      '百分比': 'number',
      '百分比 (1位小数)': 'number',
      '下拉选择': 'select',
      '布尔': 'checkbox'
    };
    return typeMap[inputType] || 'text';
  }

  /**
   * 生成 ASCII 布局图
   */
  generateLayout(featureName, formFields, tableColumns) {
    const lines = [];

    // 头部
    lines.push('┌' + '─'.repeat(41) + '┐');
    lines.push('│' + this.centerText(`← 返回     ${featureName}`, 41) + '│');
    lines.push('├' + '─'.repeat(41) + '┤');

    if (formFields.length > 0) {
      // 表单区域
      const displayFields = formFields.slice(0, 4);
      for (const field of displayFields) {
        const labelText = `${field.label}${field.required ? ' *' : ''}`;
        const inputText = field.type === 'select' ? '[请选择              ▼]' : '[                    ]';
        lines.push('│' + this.padText(`  ${labelText}`, 41) + '│');
        lines.push('│' + this.padText(`  ${inputText}`, 41) + '│');
        lines.push('│' + ' '.repeat(41) + '│');
      }

      // 提交按钮
      lines.push('├' + '─'.repeat(41) + '┤');
      lines.push('│' + this.centerText(`[ ${featureName} ]`, 41) + '│');
      lines.push('├' + '─'.repeat(41) + '┤');
    }

    // 结果/表格区域
    if (tableColumns.length > 1) {
      lines.push('│' + this.centerText('结果展示', 41) + '│');
      lines.push('├' + '─'.repeat(41) + '┤');

      const displayColumns = tableColumns.slice(0, 3);
      for (const col of displayColumns) {
        if (col.field !== 'actions') {
          const example = col.example || '-';
          lines.push('│' + this.padText(`  ${col.label}：${example}`, 41) + '│');
        }
      }
    }

    lines.push('└' + '─'.repeat(41) + '┘');

    return '```\n' + lines.join('\n') + '\n```';
  }

  /**
   * 文本居中
   */
  centerText(text, width) {
    const textWidth = this.getDisplayWidth(text);
    const padding = Math.max(0, width - textWidth);
    const leftPad = Math.floor(padding / 2);
    const rightPad = padding - leftPad;
    return ' '.repeat(leftPad) + text + ' '.repeat(rightPad);
  }

  /**
   * 文本左对齐填充
   */
  padText(text, width) {
    const textWidth = this.getDisplayWidth(text);
    const padding = Math.max(0, width - textWidth);
    return text + ' '.repeat(padding);
  }

  /**
   * 计算显示宽度（中文算2，英文算1）
   */
  getDisplayWidth(text) {
    let width = 0;
    for (const char of text) {
      width += char.charCodeAt(0) > 127 ? 2 : 1;
    }
    return width;
  }

  /**
   * 从 PRD 内容提取架构信息
   *
   * @param {string} prdContent - PRD Markdown 内容
   * @returns {Object} - 架构数据 { system, users, externals, containers }
   */
  async extractArchitecture(prdContent) {
    const arch = {
      system: { name: '', description: '' },
      users: [],
      externals: [],
      containers: []
    };

    // 提取系统名称
    const titleMatch = prdContent.match(/^# (.+)$/m);
    if (titleMatch) {
      arch.system.name = titleMatch[1].replace(/\s*PRD.*/i, '').trim();
    }

    // 提取目标用户
    const userMatch = prdContent.match(/\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|/g);
    if (userMatch) {
      for (const match of userMatch.slice(0, 3)) {
        const parts = match.split('|').map(p => p.trim()).filter(p => p);
        if (parts.length >= 1 && parts[0] !== '用户类型') {
          arch.users.push({
            name: parts[0],
            description: parts[3] || ''
          });
        }
      }
    }

    // 从内容推断外部系统
    const externalKeywords = ['微信', '支付宝', '银行', 'API', '接口', 'SDK', '数据库', '缓存', '消息队列', 'AI', '百炼', '通义'];
    for (const keyword of externalKeywords) {
      if (prdContent.includes(keyword)) {
        arch.externals.push({
          name: keyword,
          type: '外部服务',
          purpose: '集成'
        });
      }
    }

    // 去重
    arch.externals = [...new Map(arch.externals.map(e => [e.name, e])).values()];

    // 默认容器
    arch.containers = [
      { name: 'Web 应用', tech: 'Vue3/React', description: '前端界面' },
      { name: 'API 服务', tech: 'Node.js/Java', description: '后端接口' },
      { name: '数据库', tech: 'MySQL/MongoDB', description: '数据存储' }
    ];

    return arch;
  }

  /**
   * 从功能列表提取功能结构
   *
   * @param {Array} features - 功能列表
   * @returns {Object} - 结构数据 { modules: [] }
   */
  extractFunctionStructure(features) {
    if (!features || features.length === 0) {
      return { modules: [] };
    }

    // 按优先级分组
    const modules = [];

    // P0 功能为核心模块
    const p0Features = features.filter(f => f.priority === 'P0');
    const p1Features = features.filter(f => f.priority === 'P1');
    const p2Features = features.filter(f => f.priority === 'P2');

    if (p0Features.length > 0) {
      modules.push({
        id: 'core',
        name: '核心功能',
        features: p0Features.map((f, i) => ({
          id: `core_${i}`,
          name: f.name,
          priority: f.priority
        }))
      });
    }

    if (p1Features.length > 0) {
      modules.push({
        id: 'extended',
        name: '扩展功能',
        features: p1Features.map((f, i) => ({
          id: `ext_${i}`,
          name: f.name,
          priority: f.priority
        }))
      });
    }

    if (p2Features.length > 0) {
      modules.push({
        id: 'optional',
        name: '可选功能',
        features: p2Features.map((f, i) => ({
          id: `opt_${i}`,
          name: f.name,
          priority: f.priority
        }))
      });
    }

    return { modules };
  }

  /**
   * 功能结构转 Mermaid 代码
   *
   * @param {Object} structure - { modules: [] }
   * @returns {string} - Mermaid 代码
   */
  structureToMermaid(structure) {
    const { modules } = structure;

    let code = 'flowchart TB\n';

    for (const module of modules) {
      code += `    subgraph ${module.id}["${module.name}"]\n`;
      for (const feature of module.features) {
        const safeName = feature.name.replace(/"/g, "'");
        code += `        ${feature.id}["${safeName}<br/>${feature.priority}"]\n`;
      }
      code += '    end\n';
    }

    return code;
  }

  /**
   * 架构数据转 Mermaid C4 架构图
   *
   * @param {Object} arch - { system, users, externals, containers }
   * @returns {string} - Mermaid 代码
   */
  architectureToMermaid(arch) {
    const { system, users, externals, containers } = arch;

    let code = 'flowchart TB\n';

    // 系统边界
    const systemName = system.name || '系统';
    code += `    subgraph System["${systemName}"]\n`;

    // 容器（内部组件）
    if (containers && containers.length > 0) {
      for (const container of containers) {
        const safeName = container.name.replace(/"/g, "'");
        const tech = container.tech || '';
        const desc = container.description || '';
        code += `        ${container.name.toLowerCase().replace(/\s/g, '_')}["${safeName}<br/><small>${tech}</small><br/><small>${desc}</small>"]\n`;
      }
    } else {
      code += '        web["Web 应用<br/><small>Vue3/React</small>"]\n';
      code += '        api["API 服务<br/><small>Node.js/Java</small>"]\n';
      code += '        db["数据库<br/><small>MySQL/MongoDB</small>"]\n';
    }
    code += '    end\n\n';

    // 用户（外部）
    if (users && users.length > 0) {
      for (const user of users) {
        const safeName = user.name.replace(/"/g, "'");
        const userId = 'user_' + user.name.toLowerCase().replace(/\s/g, '_');
        code += `    ${userId}(["${safeName}<br/><small>用户</small>"])\n`;
        // 连接到第一个容器
        if (containers && containers.length > 0) {
          const firstContainer = containers[0].name.toLowerCase().replace(/\s/g, '_');
          code += `    ${userId} --> ${firstContainer}\n`;
        }
      }
    } else {
      code += '    user(["用户<br/><small>主要用户</small>"])\n';
      code += '    user --> web\n';
    }

    // 外部系统
    if (externals && externals.length > 0) {
      for (const external of externals) {
        const safeName = external.name.replace(/"/g, "'");
        const extId = 'ext_' + external.name.toLowerCase().replace(/\s/g, '_');
        code += `    ${extId}(["${safeName}<br/><small>${external.type || '外部系统'}</small>"])\n`;
        // 连接到 API 容器
        if (containers && containers.length > 1) {
          const apiContainer = containers.find(c => c.name.includes('API') || c.name.includes('服务'));
          if (apiContainer) {
            code += `    ${extId} --> ${apiContainer.name.toLowerCase().replace(/\s/g, '_')}\n`;
          }
        }
      }
    }

    // 内部连接
    if (containers && containers.length > 0) {
      // Web -> API
      const webContainer = containers.find(c => c.name.includes('Web') || c.name.includes('前端'));
      const apiContainer = containers.find(c => c.name.includes('API') || c.name.includes('服务') || c.name.includes('后端'));
      const dbContainer = containers.find(c => c.name.includes('数据库') || c.name.includes('DB') || c.name.includes('存储'));

      if (webContainer && apiContainer) {
        code += `    ${webContainer.name.toLowerCase().replace(/\s/g, '_')} --> ${apiContainer.name.toLowerCase().replace(/\s/g, '_')}\n`;
      }
      if (apiContainer && dbContainer) {
        code += `    ${apiContainer.name.toLowerCase().replace(/\s/g, '_')} --> ${dbContainer.name.toLowerCase().replace(/\s/g, '_')}\n`;
      }
    } else {
      code += '    web --> api\n';
      code += '    api --> db\n';
    }

    return code;
  }

  /**
   * 从 PRD 提取原型信息（用于 htmlPrototype）
   *
   * @param {Object} prd - PRD 数据
   * @returns {Object} - 原型数据
   */
  extractPrototypeData(prd) {
    const content = prd.content || '';
    const features = prd.features || [];

    // 提取产品名称
    const titleMatch = content.match(/^# (.+)$/m);
    const productName = titleMatch ? titleMatch[1].replace(/\s*PRD.*/i, '').trim() : '产品';

    // 提取侧边栏菜单
    const sidebar = features.map(f => f.name);

    // 提取主功能的输入输出
    const mainFeature = features[0] || {};
    const inputs = mainFeature.inputs || [];
    const outputs = mainFeature.outputs || [];

    // 表单字段
    const formFields = inputs.map(input => ({
      label: input.field,
      type: this.mapInputType(input.type),
      required: input.required,
      placeholder: `请输入${input.field}`,
      validation: input.validation
    }));

    // 表格列
    const tableColumns = outputs.map(output => ({
      field: output.field,
      label: output.description || output.field,
      example: output.example
    }));

    // 生成示例数据
    const sampleData = this.generateSampleData(outputs, mainFeature.name);

    return {
      productName,
      sidebar,
      formFields,
      tableColumns,
      sampleData
    };
  }

  /**
   * ⭐ v2.0 新增：生成 htmlPrototype 配置
   * 用于动态调用 htmlPrototype 技能
   *
   * @param {Object} prd - PRD 数据
   * @param {Object} designTokens - 设计系统
   * @returns {Object} - htmlPrototype 配置
   */
  generatePrototypeConfig(prd, designTokens) {
    const prototypeData = this.extractPrototypeData(prd);

    // 检测页面类型
    const pageTypes = this.detectPageTypesFromFeatures(prd.features || []);

    // 推断产品类型
    const productType = this.inferProductType(prd.content || '');

    // 构建页面描述
    const descriptions = this.buildPageDescriptions(prd.features || [], productType);

    return {
      // 基础信息
      productName: prototypeData.productName,
      productType: productType,

      // 页面配置
      pages: pageTypes.map(pageType => ({
        type: pageType,
        description: descriptions[pageType] || `创建一个${pageType}页面`,
        formFields: pageType === 'form' ? prototypeData.formFields : [],
        tableColumns: pageType === 'list' ? prototypeData.tableColumns : [],
        sampleData: prototypeData.sampleData
      })),

      // 设计系统
      designTokens: {
        colors: designTokens?.colors || {},
        typography: designTokens?.typography || {},
        spacing: designTokens?.spacing || {},
        borderRadius: designTokens?.borderRadius || {},
        shadows: designTokens?.shadows || {},
        effects: designTokens?.effects || {},
        style: this.getStyleRecommendation(productType)
      },

      // 输出配置
      output: {
        directory: 'prototypes',
        formats: ['html', 'png'],
        screenshot: true
      }
    };
  }

  /**
   * ⭐ v2.0 新增：从功能列表检测页面类型
   */
  detectPageTypesFromFeatures(features) {
    const pageTypes = new Set();

    // 默认列表页
    pageTypes.add('list');

    for (const feature of features) {
      const name = feature.name || '';
      const inputs = feature.inputs || [];

      // 表单页
      if (name.includes('提交') || name.includes('申请') || name.includes('注册') ||
          name.includes('填写') || inputs.length > 3) {
        pageTypes.add('form');
      }

      // 仪表盘
      if (name.includes('统计') || name.includes('分析') || name.includes('概览') ||
          name.includes('看板') || name.includes('仪表盘')) {
        pageTypes.add('dashboard');
      }

      // 登录页
      if (name.includes('登录') || name.includes('认证') || name.includes('权限')) {
        pageTypes.add('login');
      }

      // 详情页
      if (name.includes('详情') || name.includes('查看')) {
        pageTypes.add('detail');
      }
    }

    return Array.from(pageTypes).slice(0, 3);
  }

  /**
   * ⭐ v2.0 新增：推断产品类型
   */
  inferProductType(content) {
    if (!content) return 'default';

    if (content.includes('金融') || content.includes('理财') || content.includes('养老') || content.includes('贷款')) {
      return 'financial';
    }
    if (content.includes('电商') || content.includes('购物') || content.includes('商品') || content.includes('订单')) {
      return 'ecommerce';
    }
    if (content.includes('社交') || content.includes('社区') || content.includes('互动')) {
      return 'social';
    }
    if (content.includes('SaaS') || content.includes('管理') || content.includes('后台') || content.includes('系统')) {
      return 'saas';
    }
    if (content.includes('教育') || content.includes('学习') || content.includes('课程')) {
      return 'education';
    }
    if (content.includes('医疗') || content.includes('健康') || content.includes('问诊')) {
      return 'healthcare';
    }
    return 'default';
  }

  /**
   * ⭐ v2.0 新增：获取风格推荐
   */
  getStyleRecommendation(productType) {
    const styles = {
      financial: { name: 'Professional Trust', mood: '可靠、专业、安全', primaryStyle: 'Minimalism' },
      ecommerce: { name: 'Conversion Focused', mood: '活力、紧迫、行动导向', primaryStyle: 'Modern Clean' },
      social: { name: 'Friendly Engaging', mood: '活泼、亲和、社区感', primaryStyle: 'Playful Modern' },
      saas: { name: 'Clean Efficient', mood: '简洁、高效、专业', primaryStyle: 'Minimalism' },
      education: { name: 'Friendly Learning', mood: '友好、鼓励、清晰', primaryStyle: 'Modern Clean' },
      healthcare: { name: 'Calm Professional', mood: '安心、专业、清晰', primaryStyle: 'Minimalism' },
      default: { name: 'Modern Clean', mood: '现代、简洁、专业', primaryStyle: 'Minimalism' }
    };
    return styles[productType] || styles.default;
  }

  /**
   * ⭐ v2.0 新增：构建页面描述
   */
  buildPageDescriptions(features, productType) {
    const descriptions = {};
    const mainFeature = features[0] || {};

    // 列表页描述
    if (mainFeature.outputs && mainFeature.outputs.length > 0) {
      const columns = mainFeature.outputs.slice(0, 3).map(o => o.description || o.field).join('、');
      descriptions.list = `创建一个数据列表页，显示${columns}等信息，支持筛选、排序和分页`;
    } else {
      descriptions.list = `创建一个${mainFeature.name || '数据'}列表页，支持筛选和分页`;
    }

    // 表单页描述
    if (mainFeature.inputs && mainFeature.inputs.length > 0) {
      const fields = mainFeature.inputs.slice(0, 3).map(i => i.field).join('、');
      descriptions.form = `创建一个表单页，包含${fields}等输入字段，支持校验和提交`;
    }

    // 仪表盘描述
    descriptions.dashboard = `创建一个数据仪表盘，展示${mainFeature.name || '业务'}统计概览，包含数据卡片和趋势图`;

    // 登录页描述
    descriptions.login = `创建一个登录页，${productType === 'financial' ? '风格稳重专业' : '风格现代简洁'}`;

    // 详情页描述
    descriptions.detail = `创建一个${mainFeature.name || '数据'}详情页，展示完整信息`;

    return descriptions;
  }

  /**
   * 生成示例数据
   */
  generateSampleData(outputs, featureName) {
    if (featureName.includes('测算') || featureName.includes('养老')) {
      return [
        ['张先生', '35岁', '¥8,500', '2026-04-01', '已保存'],
        ['李女士', '42岁', '¥12,300', '2026-04-02', '已提交'],
        ['王先生', '28岁', '¥6,800', '2026-04-03', '已保存']
      ];
    }

    if (featureName.includes('推荐') || featureName.includes('产品')) {
      return [
        ['稳健型产品A', '年化4.5%', '低风险', '¥10,000', '查看'],
        ['平衡型产品B', '年化6.2%', '中风险', '¥5,000', '查看'],
        ['成长型产品C', '年化8.5%', '中高风险', '¥1,000', '查看']
      ];
    }

    // 默认示例
    return [
      ['示例数据1', '详情1', '2026-04-01', '状态1'],
      ['示例数据2', '详情2', '2026-04-02', '状态2'],
      ['示例数据3', '详情3', '2026-04-03', '状态3']
    ];
  }
}

module.exports = { AIDiagramExtractor };