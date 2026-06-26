/**
 * PRD 模板引擎 v3.0.0
 *
 * 基于功能模块化的 PRD 生成模板
 * 输出结构：需求概述 + 全局流程 + 功能章节（完整）+ 非功能需求
 *
 * v2.8.8 新增：AI 图表提取器集成
 * v2.8.9 新增：架构图、功能框架图 Mermaid 生成 + htmlPrototype 配置生成
 * v3.0.0 新增：图片渲染服务集成 + Word 导出增强
 */

const { AIDiagramExtractor } = require('./ai_diagram_extractor');

class PRDTemplate {
  constructor() {
    this.version = '4.2.5';
    this.extractor = new AIDiagramExtractor();
  }
  
  /**
   * 生成完整 PRD 文档
   */
  generatePRD(templateData) {
    let prd = '';
    
    // 文档头部
    prd += this.buildHeader(templateData);
    
    // 章节 1：需求概述
    prd += '\n## 1. 需求概述\n\n';
    prd += this.buildOverview(templateData.overview);
    
    // 章节 2：全局业务流程
    prd += '\n## 2. 全局业务流程\n\n';
    prd += this.buildGlobalFlow(templateData.globalFlow, templateData);
    
    // 章节 3-N：功能章节
    if (templateData.functions && templateData.functions.length > 0) {
      templateData.functions.forEach((func, index) => {
        prd += `\n## ${index + 3}. 功能${index + 1}：${func.name}\n\n`;
        prd += this.buildFunctionChapter(func, index + 1);
      });
    }
    
    // 章节 N+1：非功能需求
    prd += '\n## 非功能需求\n\n';
    prd += this.buildNonFunctional(templateData.nonFunctional);
    
    // 章节 N+2：附录
    prd += '\n## 附录\n\n';
    prd += this.buildAppendix(templateData.appendix);
    
    return prd;
  }
  
  /**
   * 构建文档头部
   */
  buildHeader(templateData) {
    const productName = templateData.overview?.productName || '产品需求文档';
    const version = templateData.version || 'v1.0';
    const date = new Date().toISOString().split('T')[0];
    
    return `# ${productName}

**文档版本**: ${version}  
**创建日期**: ${date}  
**产品负责人**: [待填写]  
**状态**: 草稿/评审中/已批准

---

## 📋 文档变更记录

| 版本 | 日期 | 变更内容 | 变更人 | 审核状态 |
|------|------|---------|--------|---------|
| ${version} | ${date} | 初始版本 | [姓名] | 草稿 |

---`;
  }
  
  /**
   * 构建需求概述
   */
  buildOverview(overview) {
    let content = '';
    
    // 1.1 产品定位
    content += '### 1.1 产品定位\n\n';
    content += `> ${overview.productPositioning || '待填写产品定位'}\n\n`;
    
    // 1.2 目标用户
    content += '### 1.2 目标用户\n\n';
    if (overview.targetUsers && overview.targetUsers.length > 0) {
      content += '| 用户类型 | 年龄段 | 收入水平 | 核心痛点 |\n';
      content += '|---------|-------|---------|---------|\n';
      overview.targetUsers.forEach(user => {
        content += `| ${user.type || '主要用户'} | ${user.ageRange || '-'} | ${user.incomeLevel || '-'} | ${user.painPoint || '-'} |\n`;
      });
    } else {
      content += '| 用户类型 | 年龄段 | 收入水平 | 核心痛点 |\n';
      content += '|---------|-------|---------|---------|\n';
      content += '| 主要用户 | 待填写 | 待填写 | 待填写 |\n';
    }
    content += '\n';
    
    // 1.3 业务目标
    content += '### 1.3 业务目标\n\n';
    if (overview.businessGoals && overview.businessGoals.length > 0) {
      content += '| 目标类型 | 目标描述 | 衡量指标 | 目标值 |\n';
      content += '|---------|---------|---------|-------|\n';
      overview.businessGoals.forEach(goal => {
        content += `| ${goal.type || '-'} | ${goal.description || '-'} | ${goal.metric || '-'} | ${goal.target || '-'} |\n`;
      });
    } else {
      content += '| 目标类型 | 目标描述 | 衡量指标 | 目标值 |\n';
      content += '|---------|---------|---------|-------|\n';
      content += '| 用户目标 | 待填写 | 待填写 | 待填写 |\n';
    }
    content += '\n';
    
    // 1.4 功能列表
    content += '### 1.4 功能列表\n\n';
    if (overview.functionList && overview.functionList.length > 0) {
      content += '| 功能编号 | 功能名称 | 优先级 | 预计工时 | 状态 |\n';
      content += '|---------|---------|-------|---------|------|\n';
      overview.functionList.forEach((func, index) => {
        content += `| F${String(index + 1).padStart(2, '0')} | ${func.name || '待填写'} | ${func.priority || 'P0'} | ${func.estimatedDays || '待评估'} | 待开发 |\n`;
      });
    } else {
      content += '| 功能编号 | 功能名称 | 优先级 | 预计工时 | 状态 |\n';
      content += '|---------|---------|-------|---------|------|\n';
      content += '| F01 | 待填写 | P0 | 待评估 | 待开发 |\n';
    }
    content += '\n';
    
    return content;
  }
  
  /**
   * 构建全局业务流程
   * v2.8.9 增强：添加架构图和功能框架图
   */
  buildGlobalFlow(globalFlow, templateData) {
    let content = '';

    // 2.1 系统架构图（v2.8.9 新增）
    content += '### 2.1 系统架构图\n\n';
    // ⚠️ 修复：避免递归调用 generatePRD 导致栈溢出
    // 直接使用默认架构图，后续由 AI 填充章节时补充
    content += '```mermaid\n';
    content += 'flowchart TB\n';
    content += '    subgraph System["系统"]\n';
    content += '        web["Web 应用"]\n';
    content += '        api["API 服务"]\n';
    content += '        db["数据库"]\n';
    content += '    end\n';
    content += '    user(["用户"]) --> web\n';
    content += '    web --> api\n';
    content += '    api --> db\n';
    content += '```\n\n';

    // 2.2 功能框架图（v2.8.9 新增）
    content += '### 2.2 功能框架图\n\n';
    if (templateData && templateData.functions && templateData.functions.length > 0) {
      const structureData = this.extractor.extractFunctionStructure(templateData.functions);
      const structMermaid = this.extractor.structureToMermaid(structureData);
      content += '```mermaid\n' + structMermaid + '```\n\n';
    } else {
      content += '```mermaid\n';
      content += 'flowchart TB\n';
      content += '    subgraph core["核心功能"]\n';
      content += '        f1["功能 1<br/>P0"]\n';
      content += '    end\n';
      content += '    subgraph extended["扩展功能"]\n';
      content += '        f2["功能 2<br/>P1"]\n';
      content += '    end\n';
      content += '```\n\n';
    }

    // 2.3 主业务流程图
    content += '### 2.3 主业务流程图\n\n';
    if (globalFlow && globalFlow.mainFlowchart) {
      content += '```mermaid\n' + globalFlow.mainFlowchart + '\n```\n\n';
    } else {
      content += '```mermaid\n';
      content += 'flowchart TD\n';
      content += '    Start([用户打开 APP]) --> Step1[选择功能]\n';
      content += '    Step1 --> Step2[使用功能]\n';
      content += '    Step2 --> Step3[查看结果]\n';
      content += '    Step3 --> End([结束])\n';
      content += '```\n\n';
    }
    
    // 2.4 全局业务规则
    content += '### 2.4 全局业务规则\n\n';
    if (globalFlow && globalFlow.globalRules && globalFlow.globalRules.length > 0) {
      content += '| 规则编号 | 规则名称 | 规则描述 | 适用范围 |\n';
      content += '|---------|---------|---------|---------|\n';
      globalFlow.globalRules.forEach(rule => {
        content += `| ${rule.id || '-'} | ${rule.name || '-'} | ${rule.description || '-'} | ${rule.scope || '全部功能'} |\n`;
      });
    } else {
      content += '| 规则编号 | 规则名称 | 规则描述 | 适用范围 |\n';
      content += '|---------|---------|---------|---------|\n';
      content += '| GR-001 | 待填写 | 待填写 | 全部功能 |\n';
    }
    content += '\n';

    // 2.5 全局数据定义
    content += '### 2.5 全局数据定义\n\n';
    if (globalFlow && globalFlow.globalData && globalFlow.globalData.length > 0) {
      content += '| 数据项 | 类型 | 说明 | 取值范围 |\n';
      content += '|-------|------|------|---------|\n';
      globalFlow.globalData.forEach(data => {
        content += `| ${data.name || '-'} | ${data.type || '-'} | ${data.description || '-'} | ${data.range || '-'} |\n`;
      });
    } else {
      content += '| 数据项 | 类型 | 说明 | 取值范围 |\n';
      content += '|-------|------|------|---------|\n';
      content += '| 待填写 | 待填写 | 待填写 | 待填写 |\n';
    }
    content += '\n';

    return content;
  }
  
  /**
   * 构建功能章节（核心）
   * v2.8.8: 增强 flowcharts 和 prototype 使用 AI 提取
   */
  buildFunctionChapter(feature, index) {
    let content = '';

    // 3.1 功能概述
    content += `### ${index}.1 功能概述\n\n`;
    content += '| 属性 | 说明 |\n';
    content += '|------|------|\n';
    content += `| **功能编号** | F${String(index).padStart(2, '0')} |\n`;
    content += `| **功能名称** | ${feature.name || '待填写'} |\n`;
    content += `| **优先级** | ${feature.priority || 'P0'} |\n`;
    content += `| **预计工时** | ${feature.estimatedDays || '待评估'} |\n`;
    content += `| **负责人** | [待填写] |\n`;
    content += '\n';

    // 3.2 用户场景
    content += `### ${index}.2 用户场景\n\n`;
    content += this.buildScenarios(feature.scenarios);

    // 3.3 业务流程（v2.8.8 增强：从 inputs/outputs 推断）
    content += `### ${index}.3 业务流程\n\n`;
    content += this.buildFlowcharts(feature.flowcharts, feature);

    // 3.4 业务规则
    content += `### ${index}.4 业务规则\n\n`;
    content += this.buildBusinessRules(feature.businessRules);

    // 3.5 输入输出定义
    content += `### ${index}.5 输入输出定义\n\n`;
    content += this.buildIODefinition(feature.inputs, feature.outputs);

    // 3.6 用户故事
    content += `### ${index}.6 用户故事\n\n`;
    content += this.buildUserStories(feature.userStories);

    // 3.7 验收标准
    content += `### ${index}.7 验收标准\n\n`;
    content += this.buildAcceptanceCriteria(feature.acceptanceCriteria);

    // 3.8 原型设计（v2.8.8 增强：从 inputs/outputs 生成布局）
    content += `### ${index}.8 原型设计\n\n`;
    content += this.buildPrototype(feature.prototype, feature);

    // 3.9 异常处理
    content += `### ${index}.9 异常处理\n\n`;
    content += this.buildExceptionHandling(feature.exceptions);

    return content;
  }
  
  /**
   * 构建用户场景
   */
  buildScenarios(scenarios) {
    if (!scenarios || scenarios.length === 0) {
      return '待补充用户场景\n\n';
    }
    
    let content = '';
    scenarios.forEach((scenario, index) => {
      content += `#### 场景${index + 1}：${scenario.name || '场景' + (index + 1)}\n\n`;
      content += `**用户**: ${scenario.user || '待填写'}\n\n`;
      content += `**目标**: ${scenario.goal || '待填写'}\n\n`;
      
      content += '**操作流程**:\n';
      if (scenario.steps && scenario.steps.length > 0) {
        scenario.steps.forEach((step, i) => {
          content += `${i + 1}. ${step}\n`;
        });
      } else {
        content += '1. 待填写\n';
      }
      content += '\n';
      
      content += `**期望结果**:\n${scenario.expectation || '待填写'}\n\n`;
      content += '---\n\n';
    });
    
    return content;
  }
  
  /**
   * 构建业务流程图
   * v2.8.8 增强：从 inputs/outputs 推断流程
   */
  buildFlowcharts(flowcharts, feature) {
    let content = '';

    // 主流程图
    content += '#### 主流程图\n\n';

    // 检查是否需要从 inputs/outputs 推断
    if (flowcharts && flowcharts.main && !this.isPlaceholderFlow(flowcharts.main)) {
      content += '```mermaid\n' + flowcharts.main + '\n```\n\n';
    } else if (feature && (feature.inputs || feature.outputs)) {
      // v2.8.8: 从 inputs/outputs 推断流程
      const flowData = this.extractor.inferFlow(
        feature.inputs || [],
        feature.outputs || [],
        feature.businessRules || [],
        feature.name || '功能'
      );
      const mermaidCode = this.extractor.flowToMermaid(flowData);
      content += '```mermaid\n' + mermaidCode + '```\n\n';
    } else {
      content += '```mermaid\n';
      content += 'flowchart TD\n';
      content += '    Start([开始]) --> Step1[处理]\n';
      content += '    Step1 --> End([结束])\n';
      content += '```\n\n';
    }

    // 子流程图
    if (flowcharts && flowcharts.sub && flowcharts.sub.length > 0) {
      flowcharts.sub.forEach((subflow, index) => {
        content += `#### 子流程${index + 1}\n\n`;
        content += '```mermaid\n' + subflow + '\n```\n\n';
      });
    }

    // 流程说明表
    content += '#### 流程说明表\n\n';
    content += '| 节点编号 | 节点名称 | 节点说明 | 输入 | 输出 | 异常处理 |\n';
    content += '|---------|---------|---------|------|------|---------|\n';
    content += '| Step1 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |\n';
    content += '\n';

    return content;
  }

  /**
   * 检查是否是占位符流程
   */
  isPlaceholderFlow(mermaidCode) {
    if (!mermaidCode) return true;
    // 检查是否是简单的占位符流程（只有 开始 -> 处理 -> 结束）
    const simplePattern = /Start\(\[开始\]\).*Step1\[处理\].*End\(\[结束\]\)/s;
    return simplePattern.test(mermaidCode);
  }
  
  /**
   * 构建业务规则
   */
  buildBusinessRules(rules) {
    if (!rules || rules.length === 0) {
      return '| 规则编号 | 规则名称 | 规则描述 | 校验逻辑 | 错误提示 |\n';
      content += '|---------|---------|---------|---------|---------|\n';
      content += '| BR-001 | 待填写 | 待填写 | 待填写 | 待填写 |\n\n';
    }
    
    let content = '';
    content += '| 规则编号 | 规则名称 | 规则描述 | 校验逻辑 | 错误提示 |\n';
    content += '|---------|---------|---------|---------|---------|\n';
    
    rules.forEach(rule => {
      content += `| ${rule.id || '-'} | ${rule.name || '-'} | ${rule.description || '-'} | ${rule.validation || '-'} | ${rule.error || '-'} |\n`;
    });
    
    content += '\n';
    return content;
  }
  
  /**
   * 构建输入输出定义
   */
  buildIODefinition(inputs, outputs) {
    let content = '';
    
    // 输入定义
    content += '#### 输入定义\n\n';
    content += '| 字段名 | 字段类型 | 必填 | 默认值 | 说明 | 校验规则 | 错误提示 |\n';
    content += '|-------|---------|------|-------|------|---------|---------|\n';
    
    if (inputs && inputs.length > 0) {
      inputs.forEach(input => {
        content += `| ${input.field || '-'} | ${input.type || '-'} | ${input.required ? '是' : '否'} | ${input.default || '无'} | ${input.description || '-'} | ${input.validation || '-'} | ${input.error || '-'} |\n`;
      });
    } else {
      content += '| 待填写 | 待填写 | 待填写 | 无 | 待填写 | 待填写 | 待填写 |\n';
    }
    content += '\n';
    
    // 输出定义
    content += '#### 输出定义\n\n';
    content += '| 字段名 | 字段类型 | 说明 | 示例 |\n';
    content += '|-------|---------|------|------|\n';
    
    if (outputs && outputs.length > 0) {
      outputs.forEach(output => {
        content += `| ${output.field || '-'} | ${output.type || '-'} | ${output.description || '-'} | ${output.example || '-'} |\n`;
      });
    } else {
      content += '| 待填写 | 待填写 | 待填写 | 待填写 |\n';
    }
    content += '\n';
    
    return content;
  }
  
  /**
   * 构建用户故事
   */
  buildUserStories(stories) {
    if (!stories || stories.length === 0) {
      return '| 故事编号 | 用户故事 | 优先级 | 验收标准 |\n';
      content += '|---------|---------|-------|---------|\n';
      content += '| US-001 | 作为用户，我希望... | P0 | 待填写 |\n\n';
    }
    
    let content = '';
    content += '| 故事编号 | 用户故事 | 优先级 | 验收标准 |\n';
    content += '|---------|---------|-------|---------|\n';
    
    stories.forEach((story, index) => {
      const storyId = `US-${String(index + 1).padStart(3, '0')}`;
      content += `| ${storyId} | ${story.content || story || '待填写'} | ${story.priority || 'P0'} | ${story.acceptance || '待填写'} |\n`;
    });
    
    content += '\n';
    return content;
  }
  
  /**
   * 构建验收标准 v3.1.0
   * 兼容两种格式：
   * 1. 字符串数组（GWT 格式）：["Given...When...Then...", ...]
   * 2. 对象数组（旧格式）：[{method, expected}, ...]
   */
  buildAcceptanceCriteria(criteria) {
    let content = '';
    
    // v3.1.0: 优先处理 GWT 字符串数组格式
    if (criteria && Array.isArray(criteria) && criteria.length > 0) {
      // 检查是否是 GWT 字符串数组
      const isGWTFormat = typeof criteria[0] === 'string' && criteria[0].includes('Given') && criteria[0].includes('When') && criteria[0].includes('Then');
      
      if (isGWTFormat) {
        content += '**验收标准（GWT 格式）**\n\n';
        criteria.forEach((ac, index) => {
          content += `${index + 1}. ${ac}\n`;
        });
        content += '\n---\n\n';
      }
    }
    
    // 功能验收（旧格式兼容）
    content += '#### 功能验收\n\n';
    content += '| 验收项 | 验收方法 | 预期结果 | 验收结果 |\n';
    content += '|-------|---------|---------|---------|\n';
    
    if (criteria && criteria.functional && criteria.functional.length > 0) {
      criteria.functional.forEach((item, index) => {
        content += `| 验收项${index + 1} | ${item.method || '待填写'} | ${item.expected || '待填写'} | □通过 □失败 |\n`;
      });
    } else if (!criteria || !Array.isArray(criteria) || criteria.length === 0) {
      // 只有在没有 GWT 格式时才显示空表格
      content += '| 验收项 1 | 待填写 | 待填写 | □通过 □失败 |\n';
    }
    content += '\n';
    
    // 性能验收
    content += '#### 性能验收\n\n';
    content += '| 指标 | 目标值 | 实测值 | 验收结果 |\n';
    content += '|------|-------|-------|---------|\n';
    content += '| 响应时间（P95） | < 2 秒 | | □通过 □失败 |\n';
    content += '| 并发用户数 | ≥ 1000 | | □通过 □失败 |\n';
    content += '\n';
    
    // 兼容性验收
    content += '#### 兼容性验收\n\n';
    content += '| 平台 | 版本 | 验收结果 |\n';
    content += '|------|------|---------|\n';
    content += '| iOS | 12+ | □通过 □失败 |\n';
    content += '| Android | 8+ | □通过 □失败 |\n';
    content += '| 微信浏览器 | 最新版 | □通过 □失败 |\n';
    content += '\n';
    
    return content;
  }
  
  /**
   * 构建原型设计
   * v2.8.8 增强：从 inputs/outputs 生成布局
   */
  buildPrototype(prototype, feature) {
    let content = '';

    // 页面列表
    content += '#### 页面列表\n\n';
    content += '| 页面编号 | 页面名称 | 说明 | 优先级 | 原型文件 |\n';
    content += '|---------|---------|------|-------|---------|\n';

    if (prototype && prototype.pages && prototype.pages.length > 0) {
      prototype.pages.forEach((page, index) => {
        const pageId = `P${String(index + 1).padStart(2, '0')}`;
        content += `| ${pageId} | ${page.name || '待填写'} | ${page.description || '-'} | ${page.priority || 'P0'} | ${page.file || '-'} |\n`;
      });
    } else if (feature) {
      // v2.8.8: 从功能名称生成页面
      const pageId = 'P01';
      const pageName = `${feature.name || '功能'}页`;
      content += `| ${pageId} | ${pageName} | 主${feature.name || '功能'}页面 | P0 | prototypes/${(feature.name || 'feature').toLowerCase()}.html |\n`;
    } else {
      content += '| P01 | 待填写 | 待填写 | P0 | - |\n';
    }
    content += '\n';

    // 页面布局
    content += '#### 页面布局\n\n';

    // v2.8.8: 检查是否需要从 inputs/outputs 生成布局
    const isPlaceholderLayout = !prototype || !prototype.layout ||
      prototype.layout.includes('页面标题') ||
      prototype.layout.includes('内容区域');

    if (isPlaceholderLayout && feature && (feature.inputs || feature.outputs)) {
      // 从 inputs/outputs 生成布局
      const layoutData = this.extractor.generateLayout(
        feature.name || '功能',
        (feature.inputs || []).map(input => ({
          label: input.field,
          type: this.extractor.mapInputType(input.type),
          required: input.required
        })),
        (feature.outputs || []).map(output => ({
          field: output.field,
          label: output.description || output.field,
          example: output.example
        }))
      );
      content += layoutData + '\n\n';
    } else if (prototype && prototype.layout) {
      content += '```\n' + prototype.layout + '\n```\n\n';
    } else {
      content += '```\n';
      content += '┌─────────────────────────────────────────┐\n';
      content += '│  页面标题                                │\n';
      content += '├─────────────────────────────────────────┤\n';
      content += '│  内容区域                                │\n';
      content += '└─────────────────────────────────────────┘\n';
      content += '```\n\n';
    }

    // 交互说明
    content += '#### 交互说明\n\n';
    content += '| 元素 | 交互类型 | 交互说明 |\n';
    content += '|------|---------|---------|\n';

    // v2.8.8: 从 inputs 生成交互说明
    if (feature && feature.inputs && feature.inputs.length > 0) {
      feature.inputs.slice(0, 3).forEach(input => {
        content += `| ${input.field}输入框 | 输入 | ${input.validation || '输入' + input.field} |\n`;
      });
      content += `| 提交按钮 | 点击 | 校验通过后提交 |\n`;
    } else if (prototype && prototype.interactions && prototype.interactions.length > 0) {
      prototype.interactions.forEach(interaction => {
        content += `| ${interaction.element || '-'} | ${interaction.type || '-'} | ${interaction.description || '-'} |\n`;
      });
    } else {
      content += '| 待填写 | 待填写 | 待填写 |\n';
    }
    content += '\n';

    // 原型文件
    content += '#### 原型文件\n\n';

    // v2.8.8: 确保文件路径与功能名称一致
    if (feature) {
      const fileName = (feature.name || 'feature').toLowerCase();
      content += `- HTML 原型：prototypes/${fileName}.html\n`;
      content += `- PNG 截图：prototypes/${fileName}.png\n`;
    } else if (prototype && prototype.files) {
      content += `- HTML 原型：${prototype.files.html || '待生成'}\n`;
      content += `- PNG 截图：${prototype.files.png || '待生成'}\n`;
    } else {
      content += '- HTML 原型：prototypes/feature-1.html\n';
      content += '- PNG 截图：prototypes/feature-1.png\n';
    }
    content += '\n';
    
    return content;
  }
  
  /**
   * 构建异常处理
   */
  buildExceptionHandling(exceptions) {
    let content = '';
    
    content += '| 异常类型 | 触发条件 | 错误码 | 错误提示 | 处理方式 |\n';
    content += '|---------|---------|-------|---------|---------|\n';
    
    if (exceptions && exceptions.length > 0) {
      exceptions.forEach(exception => {
        content += `| ${exception.type || '-'} | ${exception.condition || '-'} | ${exception.code || '-'} | ${exception.message || '-'} | ${exception.handling || '-'} |\n`;
      });
    } else {
      content += '| 参数校验失败 | 参数超范围 | PARAM_ERROR | "参数校验失败，请检查输入" | 前端提示，阻止提交 |\n';
      content += '| 系统异常 | 服务器错误 | SYSTEM_ERROR | "系统繁忙，请稍后重试" | 后端捕获，返回错误 |\n';
    }
    content += '\n';
    
    return content;
  }
  
  /**
   * 构建非功能需求
   */
  buildNonFunctional(nonFunctional) {
    let content = '';
    
    // 性能要求
    content += '### 性能要求\n\n';
    content += '| 指标 | 要求 | 说明 |\n';
    content += '|------|------|------|\n';
    
    if (nonFunctional && nonFunctional.performance && nonFunctional.performance.length > 0) {
      nonFunctional.performance.forEach(item => {
        content += `| ${item.metric || '-'} | ${item.requirement || '-'} | ${item.description || '-'} |\n`;
      });
    } else {
      content += '| 响应时间 | < 2 秒 | 95% 的请求响应时间 |\n';
      content += '| 并发用户 | ≥ 1000 | 同时在线用户数 |\n';
    }
    content += '\n';
    
    // 安全要求
    content += '### 安全要求\n\n';
    content += '| 要求 | 说明 |\n';
    content += '|------|------|\n';
    
    if (nonFunctional && nonFunctional.security && nonFunctional.security.length > 0) {
      nonFunctional.security.forEach(item => {
        content += `| ${item.requirement || '-'} | ${item.description || '-'} |\n`;
      });
    } else {
      content += '| 数据加密 | 用户输入数据加密传输（HTTPS） |\n';
      content += '| 权限控制 | 用户只能查看自己的数据 |\n';
    }
    content += '\n';
    
    // 兼容性要求
    content += '### 兼容性要求\n\n';
    content += '| 类型 | 要求 |\n';
    content += '|------|------|\n';
    
    if (nonFunctional && nonFunctional.compatibility && nonFunctional.compatibility.length > 0) {
      nonFunctional.compatibility.forEach(item => {
        content += `| ${item.type || '-'} | ${item.requirement || '-'} |\n`;
      });
    } else {
      content += '| 浏览器 | Chrome 80+、Safari 12+、微信浏览器 |\n';
      content += '| 操作系统 | iOS 12+、Android 8+ |\n';
    }
    content += '\n';
    
    // 可用性要求
    content += '### 可用性要求\n\n';
    content += '| 指标 | 要求 |\n';
    content += '|------|------|\n';
    
    if (nonFunctional && nonFunctional.availability && nonFunctional.availability.length > 0) {
      nonFunctional.availability.forEach(item => {
        content += `| ${item.metric || '-'} | ${item.requirement || '-'} |\n`;
      });
    } else {
      content += '| 系统可用性 | ≥ 99.9% |\n';
      content += '| 故障恢复时间 | < 30 分钟 |\n';
    }
    content += '\n';
    
    return content;
  }
  
  /**
   * 构建附录
   */
  buildAppendix(appendix) {
    let content = '';
    
    // 术语表
    content += '### 术语表\n\n';
    content += '| 术语 | 定义 |\n';
    content += '|------|------|\n';
    
    if (appendix && appendix.glossary && appendix.glossary.length > 0) {
      appendix.glossary.forEach(term => {
        content += `| ${term.term || '-'} | ${term.definition || '-'} |\n`;
      });
    } else {
      content += '| PRD | 产品需求文档 |\n';
      content += '| P0/P1/P2 | 优先级 0/1/2 |\n';
    }
    content += '\n';
    
    // 参考资料
    content += '### 参考资料\n\n';
    if (appendix && appendix.references && appendix.references.length > 0) {
      appendix.references.forEach(ref => {
        content += `- ${ref}\n`;
      });
    } else {
      content += '- 待填写\n';
    }
    content += '\n';
    
    // 审核签字
    content += '### 审核签字\n\n';
    content += '| 角色 | 姓名 | 签字 | 日期 |\n';
    content += '|------|------|------|------|\n';
    content += '| 产品负责人 | | | |\n';
    content += '| 开发负责人 | | | |\n';
    content += '| 测试负责人 | | | |\n';
    content += '\n';
    
    content += '---\n\n**文档结束**\n';
    
    return content;
  }
}

module.exports = { PRDTemplate };
