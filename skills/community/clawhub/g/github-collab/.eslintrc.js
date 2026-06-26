/**
 * ESLint Configuration
 * 
 * 严格的代码规范配置
 */

module.exports = {
  root: true,
  env: {
    node: true,
    es2021: true,
    jest: true
  },
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module'
  },
  extends: [
    'eslint:recommended',
    'plugin:jest/recommended'
  ],
  plugins: ['jest'],
  rules: {
    // 错误
    'no-console': 'warn',
    'no-debugger': 'error',
    'no-alert': 'error',
    
    // 严格模式
    'strict': ['error', 'global'],
    
    // 变量
    'no-unused-vars': ['error', { 
      vars: 'all',
      args: 'after-used',
      ignoreRestSiblings: false
    }],
    'no-useless-escape': 'error',
    'no-useless-concat': 'error',
    'no-useless-return': 'error',
    
    // 函数
    'no-useless-call': 'error',
    'no-useless-computed-key': 'error',
    'no-useless-rename': 'error',
    'require-await': 'error',
    
    // 语法
    'no-var': 'error',
    'prefer-const': 'error',
    'prefer-spread': 'error',
    'prefer-destructuring': ['error', {
      array: false,
      object: true
    }],
    'prefer-template': 'error',
    'prefer-reflect': 'error',
    'prefer-promise-reject-errors': 'error',
    
    // 样式
    'quotes': ['error', 'single', { allowTemplateLiterals: true }],
    'semi': ['error', 'always'],
    'comma-dangle': ['error', 'never'],
    'no-trailing-spaces': 'error',
    'eol-last': ['error', 'always'],
    'indent': ['error', 2, { SwitchCase: 1 }],
    'space-before-blocks': ['error', 'always'],
    'space-in-parens': ['error', 'never'],
    'keyword-spacing': ['error', { before: true, after: true }],
    'key-spacing': ['error', { beforeColon: false, afterColon: true }],
    'comma-spacing': ['error', { before: false, after: true }],
    'array-bracket-spacing': ['error', 'never'],
    'object-curly-spacing': ['error', 'always'],
    'func-call-spacing': ['error', 'never'],
    'space-infix-ops': 'error',
    'semi-spacing': ['error', { before: false, after: true }],
    'semi-style': ['error', 'last'],
    
    // 最佳实践
    'curly': ['error', 'all'],
    'eqeqeq': ['error', 'always', { null: 'ignore' }],
    'guard-for-in': 'error',
    'no-caller': 'error',
    'no-extend-native': 'error',
    'no-implied-eval': 'error',
    'no-iterator': 'error',
    'no-lone-blocks': 'error',
    'no-new-func': 'error',
    'no-new-wrappers': 'error',
    'no-proto': 'error',
    'no-return-assign': 'error',
    'no-self-assign': 'error',
    'no-self-compare': 'error',
    'no-sequences': 'error',
    'no-throw-literal': 'error',
    'no-unmodified-loop-condition': 'error',
    'no-unreachable-loop': 'error',
    'no-unused-expressions': 'error',
    'no-unused-labels': 'error',
    'no-useless-backreference': 'error',
    'no-useless-catch': 'error',
    'no-useless-constructor': 'error',
    'no-void': 'error',
    'no-with': 'error',
    'wrap-iife': ['error', 'any'],
    'yoda': ['error', 'never'],
    
    // 性能
    'no-bitwise': 'warn',
    
    // Node.js
    'no-process-env': 'off',
    'no-process-exit': 'off',
    'no-path-concat': 'error',
    'no-sync': 'warn',
    
    // Jest
    'jest/expect-expect': ['error', {
      assertFunctionNames: ['expect', 'assert']
    }],
    'jest/no-disabled-tests': 'error',
    'jest/no-focused-tests': 'error',
    'jest/no-identical-title': 'error',
    'jest/no-jasmine-globals': 'error',
    'jest/no-mocks-import': 'error',
    'jest/no-standalone-expect': 'error',
    'jest/no-test-prefixes': 'error',
    'jest/prefer-to-be': 'error',
    'jest/prefer-to-contain': 'error',
    'jest/prefer-to-have-length': 'error',
    'jest/valid-expect': 'error',
    'jest/valid-title': 'error'
  },
  settings: {
    jest: {
      version: 29
    }
  },
  ignorePatterns: [
    'node_modules/',
    'coverage/',
    'dist/',
    'build/',
    '.nyc_output/',
    '*.min.js',
    'vendor/',
    'fixtures/'
  ]
};
