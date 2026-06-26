/**
 * 统一版本配置（唯一版本源）
 *
 * ⚠️ 不要手动编辑此文件！
 *
 * 发布新版本：
 *   python3 scripts/update_version.py 4.2.1 "修复 bug" "详细说明"
 *
 * 同步当前版本到所有文件：
 *   python3 scripts/update_version.py
 *
 * 代码中获取版本：
 *   const VERSION = require('./version');
 *   console.log(VERSION.full);  // "v4.2.0"
 */

module.exports = {
  // 当前版本号
  version: '5.1.0',

  // 发布日期
  releaseDate: '2026-04-20',

  // 技能名称
  name: 'PRD Workflow',

  // 完整版本字符串
  get full() {
    return `v${this.version}`;
  },

  // 带日期的完整版本
  get fullWithDate() {
    return `${this.name} ${this.full} (${this.releaseDate})`;
  },

  // 版本历史（用于生成文档）
  changelog: [
    {
      version: '5.1.0',
      date: '2026-04-20',
      type: 'feature',
      desc: 'Wiki增强 + AI驱动原型v6.1.0 + 设计系统持久化',
      detail: 'Wiki知识库智能集成（可选）+ 原型从模板渲染改为AI驱动（Chart.js CDN + JS校验）+ ui-ux-pro-max设计系统持久化'
    },
    {
      version: '5.0.0',
      date: '2026-04-15',
      type: 'feature',
      desc: '分段确认模式',
      detail: '引入 Superpowers 分段确认 + 任务细化理念'
    },
    {
      version: '4.2.5',
      date: '2026-04-07',
      type: 'fix',
      desc: 'postinstall 脚本添加 adm-zip 依赖检测',
      detail: '增加 Word 文档图片检查依赖 adm-zip 的自动检测和安装说明'
    },
    {
      version: '4.2.5',
      date: '2026-04-07',
      type: 'docs',
      desc: '更新使用说明',
      detail: '增加/skill 命令误区的详细说明，引导正确使用方式'
    },
    {
      version: '4.2.5',
      date: '2026-04-05',
      type: 'feature',
      desc: '验收标准 GWT 格式优化',
      detail: '需求拆解不再生成验收标准 + PRD 阶段按功能生成 GWT 格式 + COMPLETE-6 检查项'
    },
    {
      version: '4.2.5',
      date: '2026-04-05',
      type: 'feature',
      desc: '内容检查问答引导',
      detail: '13 项内容检查 + 问答引导修补 + AI 自动/用户指导/误报跳过三种处理方式'
    },
    {
      version: '4.2.5',
      date: '2026-04-05',
      type: 'feature',
      desc: '多页面原型系统',
      detail: '页面树推断 + 导航组件 + 路由注入 + 多端截图'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'feature',
      desc: '图片渲染服务',
      detail: 'Mermaid → PNG 自动渲染 + Word 导出嵌入图片 + 系统 Chrome 支持'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'feature',
      desc: '架构图表',
      detail: '系统架构图 + 功能框架图 + htmlPrototype 配置动态生成'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'feature',
      desc: 'AI 图表提取',
      detail: '流程图从 inputs/outputs 推断 + 原型布局动态生成'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'fix',
      desc: '依赖完善',
      detail: 'postinstall 自动安装 mermaid-cli + 截图方案优化'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'feature',
      desc: '模板库扩展',
      detail: '6 种页面类型 + 完整设计系统集成'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'feature',
      desc: '设计系统集成',
      detail: 'htmlPrototype 与 ui-ux-pro-max 协作'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'fix',
      desc: '可移植性',
      detail: '移除硬编码路径 + 动态路径检测 + 添加测试套件'
    },
    {
      version: '4.2.5',
      date: '2026-04-04',
      type: 'feature',
      desc: '质量提升',
      detail: '环境检查前置化 + 流程降级策略 + 进度反馈机制'
    },
    {
      version: '4.2.5',
      date: '2026-04-01',
      type: 'feature',
      desc: '迭代支持',
      detail: '版本管理 + 需求对比 + 回滚'
    },
    {
      version: '4.2.5',
      date: '2026-03-30',
      type: 'feature',
      desc: '真正集成',
      detail: '内置调用 6 个技能'
    },
    {
      version: '4.2.5',
      date: '2026-03-24',
      type: 'feature',
      desc: '初始版本',
      detail: '基础工作流'
    }
  ],

  /**
   * 生成 Markdown 版本历史表格
   */
  toMarkdownTable() {
    const lines = ['| 版本 | 日期 | 变更内容 |', '|------|------|---------|'];
    const icons = { feature: '🚀', fix: '🔧', docs: '📝' };

    this.changelog.forEach(item => {
      const icon = icons[item.type] || '📦';
      const bold = item.version === this.version ? '**' : '';
      lines.push(`| ${bold}${item.version.startsWith('v') ? '' : 'v'}${item.version}${bold} | ${bold}${item.date}${bold} | ${icon} **${item.desc}** - ${item.detail} |`);
    });

    return lines.join('\n');
  },

  /**
   * 获取最新版本信息
   */
  get latest() {
    return this.changelog[0];
  },

  /**
   * 获取指定版本信息
   */
  getVersion(version) {
    return this.changelog.find(item => item.version === version || `v${item.version}` === version);
  }
};
