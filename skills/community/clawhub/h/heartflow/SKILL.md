---
name: heartflow
title: "HeartFlow — Rule-based AI Output Discriminator"
version: "6.4.1"
description: |-
  HeartFlow (心虫) is a rule-based text discrimination engine for AI output validation.
  12-module pipeline, 45 discrimination dimensions, zero LLM dependency.
  
  npm: @yun520-1/heartflow
---
## Quick start

```js
const hf = require('@yun520-1/heartflow');
hf.checkInput('text');     // pass/verify/rewrite/block
hf.checkDraft('text');     // check draft before completing
hf.checkOutput('text');    // check AI output before sending
```

## Pipeline

scope-check → premise-check → discriminate(45dim) → gate → verifier → frame-check → output-gate → doubt-engine → error-memory → auto-rules

## Install

```bash
npm install @yun520-1/heartflow
```
