# {{title}}

> 统计窗口：{{startTime}} ～ {{endTime}}（{{timeLabel}}）  
> 样本：{{recordCount}} 条录音转写  
> {{#if dimensionNotice}}{{dimensionNotice}}{{/if}}

---

## 执行摘要

{{executiveSummary}}

---

{{#if useTenDimensions}}
{{tenDimensionsContent}}
{{else}}
## 用户关注：{{userTheme}}

{{userThemeContent}}
{{/if}}

---

<footer>本页依据 ASR 转写生成，结论均来自录音文本证据。</footer>
