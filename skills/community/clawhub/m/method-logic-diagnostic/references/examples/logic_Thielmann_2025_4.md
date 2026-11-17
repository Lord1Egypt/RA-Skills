# 片段类型：逻辑

## 原文片段

Whereas prior work has often relied on frequentist estimation using multiTree (Moshagen, 2010), we implemented the models in a Bayesian framework using the TreeBUGS package in R (Heck, Arnold, & Arnold, 2018). This offers several advantages: First, the Bayesian framework allows us to specify weakly informative prior distributions for the marginal probability d of dishonesty which is known to range between .20 and .40 (Abeler et al., 2019; Heck, Thielmann, Moshagen, & Hilbig, 2018). Second, we obtain (Bayesian) credible intervals (CIs) for the parameters that have a more intuitive interpretation than (frequentist) confidence intervals (Morey et al., 2016). Third, the posterior distribution of MPT parameters can easily be approximated via Markov chain Monte Carlo sampling (Heck, Arnold, & Arnold, 2018), which (a) provides a full description of uncertainty regarding all model parameters jointly and (b) facilitates the derivation of quantities that are of theoretical interest.

## 来源文献

Thielmann et al., 2025, Journal of Personality and Social Psychology

## 适配诊断点

方法选择先对比前人做法（Whereas prior work...），再以 First/Second/Third + (a)/(b) 枚举自身方案的三点优势，是"为什么选这个模型"的论证样板。
