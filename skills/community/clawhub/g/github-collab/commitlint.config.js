/**
 * Commitlint Configuration
 * 
 * 约定式提交规范
 */

module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 100],
    'footer-max-line-length': [2, 'always', 100],
    
    'type-enum': [2, 'always', [
      'feat',     // 新功能
      'fix',      // Bug 修复
      'docs',     // 文档变更
      'style',    // 代码格式（不影响代码运行）
      'refactor', // 代码重构
      'perf',     // 性能优化
      'test',     // 测试相关
      'build',    // 构建系统或外部依赖变更
      'ci',       // CI 配置变更
      'chore',    // 其他变更
      'revert'    // 回滚
    ]],
    
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    
    'subject-empty': [2, 'never'],
    'subject-case': [2, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']],
    'subject-full-stop': [2, 'never', '.'],
    
    'body-leading-blank': [1, 'always'],
    'body-max-line-length': [2, 'always', 100],
    
    'footer-leading-blank': [1, 'always'],
    'footer-max-line-length': [2, 'always', 100]
  }
};
