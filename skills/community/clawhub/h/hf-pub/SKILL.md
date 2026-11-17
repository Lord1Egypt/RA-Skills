---
name: heartflow-pipeline
title: "心虫 HeartFlow — AGI第1层管线"
version: "6.4.0"
description: |-
  心虫(HeartFlow)是AI输出的辨别门禁层。AGI五层能力的第一层。
  零LLM依赖，纯规则引擎，45维文本辨别 + 12模块管线。
  
  npm: @yun520-1/heartflow
  GitHub: https://github.com/yun520-1/mark-heartflow-skill
---
## 用法

```js
const hf = require('@yun520-1/heartflow');
hf.checkInput('你好');   // pass/verify/rewrite/block
hf.checkDraft('草稿');    // 检测AI草稿
hf.checkOutput('回复');   // 检测AI输出（发出前）
```

## 管线

scope-check → premise-check → discriminate(45维) → gate → 
verifier → frame-check → output-gate → doubt-engine → 
error-memory → auto-rules → intent-anchor

## 安装

```bash
npm install @yun520-1/heartflow
```
