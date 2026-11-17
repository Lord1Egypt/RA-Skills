# 片段类型：结构（在线实验任务设计与流失率操作化）

## 原文片段

> For each of the six paradigms that we chose to replicate, we created an MTurk HIT (Human Intelligence Task), which in our case was a Qualtrics survey that an MTurk Worker can work on and collect a reward for completing. We described all six HITs as "a simple anonymous survey that takes about 5 minutes to complete." For each HIT, we requested 100 participants and paid participants who completed the study a fixed 50 cents in compensation. We determined the 10-cents-per-minute rate in accordance with the recommendation by the Guideline for Academic Requesters Project, a joint effort by academic researchers and the MTurk-worker community. We allowed only MTurk workers residing in either the United States or Canada to take the HITs.
>
> In each replication experiment, participants first clicked a button to indicate their consent. When computing dropout rates, we took into account only participants who consented. These participants were then taken to a second page where they were invited to complete the task intended as an experimental manipulation in the original experiment. In our replication experiments, we only had participants complete the experimental manipulation (i.e., we skipped all the other steps in the original procedures, including manipulation checks and dependent variables). The manipulation task was followed by a very short demographic questionnaire. However, the participants did not know beforehand that the survey they consented to consisted of only the manipulation task and the demographic questionnaire.

## 来源文献

Zhou, H., & Fishbach, A. (2016), Study 1 Method. *The Pitfall of Experimenting on the Web: How Unattended Selective Attrition Leads to Surprising (Yet False) Research Conclusions.* Journal of Personality and Social Psychology, 111(4), 493-504.

## 适配诊断点

- 平台术语先定义再使用（MTurk HIT → "which in our case was a Qualtrics survey"），对跨领域读者友好。
- 每个实验参数都精确给出：任务描述原文（加引号）、请求人数（100）、报酬（50 cents）、报酬率依据（10-cents-per-minute，引用 Guideline for Academic Requesters Project）。
- 因变量（dropout rate）的操作化边界被显式界定："we took into account only participants who consented"，避免口径歧义。
- 关键的方法学透明度：说明省略了原实验的 manipulation checks 与 dependent variables（"i.e., we skipped ..."），并交代参与者不知情（"did not know beforehand"），这是掩盖程序细节的常见陷阱的反面范例。
