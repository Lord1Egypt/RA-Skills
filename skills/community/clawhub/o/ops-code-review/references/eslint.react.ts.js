/**
 * 内置 ESLint 配置 for React + TypeScript
 * 用法: npx eslint src --no-config-lookup -c references/eslint.react.ts.js
 *
 * 规则覆盖:
 *   - 严重: no-undef, no-unused-vars (var), consistent-return
 *   - 警告: no-console, no-debugger, no-alert
 *   - React: hooks-dependencies, exhaustive-deps (需 eslint-plugin-react-hooks)
 *
 * 注意: 不含 tsc 类型检查（tsc --noEmit 需完整 node_modules + tsconfig，
 *       SVN 仓库通常不完整，会产生大量误报，故默认关闭）
 */
module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: "module",
    ecmaFeatures: { jsx: true },
  },
  env: {
    browser: true,
    es6: true,
    node: true,
  },
  plugins: ["@typescript-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
  ],
  rules: {
    // 严重
    "no-undef": "error",
    "consistent-return": "error",
    // 警告
    "no-console": "warn",
    "no-debugger": "warn",
    "no-alert": "warn",
    // TypeScript
    "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-explicit-any": "off",
  },
  ignorePatterns: [
    "node_modules/",
    "dist/",
    "build/",
    ".next/",
    "coverage/",
  ],
};
