# 数据汇总、Reliability、Validity 与 Inaccuracy

## 先报告什么

如果是 task inventory 或其他 quantitative ratings，技术报告至少应包含：

- **Task**：任务陈述。
- **M / mean**：平均评分。
- **SD / standard deviation**：评分离散程度。
- **N**：该任务的有效 respondent 数。
- **SEM / standard error of the mean**：mean 的精确性指标。

解释时可以这样讲：

- mean 回答"平均来看这个任务得分多高"。
- SD 回答"respondents 之间分歧有多大"。
- N 回答"这个结果基于多少人"。
- SEM 回答"这个平均数有多精确"；SD 越大、N 越小，SEM 越大。

报告这些数据有助于使用者判断哪些任务重要、哪些评分稳定、哪些项目可能需要再核实。

## Reliability 与 Validity 的基本区别

- **Reliability**：数据中有多少 error 或 disagreement。重复测量或不同 judge 是否能得到相似结果。
- **Validity**：这些数字对当前目的是否有意义，能否支持想要的推论。例如 PAQ 维度能否预测 salary，task ratings 能否支持 training design。

先讲用途：

- reliability 低，说明基于数据做决定可能出错，可能需要重新收集或改进数据。
- validity 弱，说明即使数据一致，也未必能支持目标 HR 应用。

## Reliability：常见来源和方法

误差来源包括：

- human judgments：人对 time spent、importance、KSAO 等判断不同。
- specific item content：量表题项本身带来的误差。
- changes in job content over time：工作内容随时间变化。

### Interjudge agreement

Agreement 关注 judgments 是否相同。

**Percentage agreement**

- 计算方式：一致的 rating 数 / rating 总数。
- 优点：简单、容易沟通。
- 问题：可能因低变异或偶然一致而显得很高。
- 若使用，最好搭配 chance-corrected 方法，如 kappa。

**Kappa**

- 用于 categorical data。
- 比 percentage agreement 更好，因为会考虑 chance agreement。

**r(wg)**

- 用于一个 job、有多个 raters、连续型 rating scale 的情境。
- 比较 observed standard deviation 与随机作答时的 standard deviation。
- 如果 observed spread 比随机 spread 小，说明 raters agreement 较好。
- 注意：r(wg) 在低变异时也可能很高，严格说不完全是 psychometric reliability。

### Interjudge reliability

Reliability 不只是"数字相同"，还关心 true variance 与 error variance。

**Correlation coefficient r**

- 适合两个 raters 对多个 jobs 的连续评分。
- 若两个 analysts 对一组 jobs 的 spatial ability importance ratings 高相关，说明 reliability 较好。
- 缺点：可能忽略 raters 之间 mean level 差异；即使一个 rater 总是给高 1 分，相关仍可能很高。

**Intraclass correlation (ICC)**

- 适合处理多个 raters、多个 tasks，或需要考虑 raters mean differences 的情境。
- 可用于估计需要多少 raters 才能达到期望 reliability。
- 与 generalizability theory 相关。

### Internal consistency

Internal consistency 关注多个 items 是否共同测量同一结构。

**Split-half**

- 把量表 items 分成两半，各自求和，再计算两半相关。
- 问题是不同分半方式会产生不同估计。

**Alpha**

- 常见 reliability 指标，用于多个 respondents、多个 items 或多个 raters 总分。
- 适用于 items/raters 预期给出相似结果的情况。
- 如果预期 incumbents 和 supervisors 本来就会不同，应使用能处理这些差异的方法，如 ICC。

### Temporal stability

Temporal stability 关注同一对象在不同时间测量是否稳定。

例子：

- 1 月让 incumbents 评 tasks 的 importance/time spent。
- 6 月让同一批 incumbents 再评一次。
- 比较两次 mean ratings 的相关，判断 job analysis 数据是否跨时间稳定。

## Validity：常见分析技术

### Correlation and regression

**Correlation**

- 用一个数字总结两个变量的关系。
- 例：difficulty-to-learn ratings 与 training time to proficiency 的关系。

**Regression**

- 用 predictor variables 数值预测 outcome。
- 例：用 PAQ scores 预测 salary，适合 job evaluation。
- 多个 PAQ scales 同时预测 salary 时，就是 multiple regression。

### Factor analysis

Factor analysis 通常用于把大量 items 组合成更少、更有解释力的 scales。

例子：

- 把多个 PAQ items 组合成 problem-solving scale。
- 把多个 JCI items 组合成 arithmetic scale。

逻辑：

- 在大量 jobs 上测量多个 items。
- 计算 items 之间的 correlation matrix。
- 找出哪些 items 一起变化，形成 factors。

### Cluster analysis

Cluster analysis 常用于 grouping jobs。

逻辑：

- 用任务、KSAO、rating profiles 或 correlation matrix 表示 jobs 的相似性。
- 最相似的 jobs 先聚成群，再逐步形成更大 clusters。
- 研究者要从多个 cluster solutions 中判断哪个最有意义。

用途：

- job classification
- selection/training 中的 job grouping
- worker mobility 和 career ladder 分析

### Other multivariate techniques

- **MANOVA**：比较多个 job groups 在多个 dependent variables 上是否不同。
- **Canonical correlation**：处理两组多变量之间的关系。
- **Discriminant analysis**：dependent variable 是 categorical 时使用，例如预测 job 属于 professional、managerial、white-collar 或 blue-collar。

### Consequential validity

Consequential validity 关注 job analysis 是否真的增加了 HR intervention 的 effectiveness 或 efficiency。

换句话说，问题不是"我们做了 job analysis 吗"，而是：

- 基于 job analysis 的 selection test 是否比未基于 job analysis 的 test 更有效？
- 更详细的 job analysis 是否让 selection/training examination plan 更好？
- job analysis 数据通过怎样的推论过程转化为 HR 决策？

第 9 章指出这很重要但也很复杂，现有证据和方法仍有限。

## Inaccuracy / Bias：为什么要防

Job analysis 大量依赖 human judgment，而 human judgment 可能受社会和认知因素影响。

潜在来源可分为两大类：

- **Social sources**：来自社会环境、规范压力、自我呈现和利益相关性。
- **Cognitive sources**：来自信息处理限制、记忆限制和认知偏差。

研究发现的风险包括：

- ability statements 比 task statements 更容易受 self-presentation 影响。
- job satisfaction、organizational commitment、job involvement 等态度可能影响 task ratings，尤其是高 discretion tasks。
- 某些 personality requirements ratings 可能与 organizational culture 有关。
- 低 specificity、低 observability 的 descriptors（如 traits）更容易受个人 rater tendencies 影响，reliability 更低。
- self-serving bias 可出现在 competencies 或 physically demanding tasks 的 importance ratings 中。

## 降低 inaccuracy 的实务做法

回答用户时可用以下 mitigation checklist：

- 优先使用更具体、可观察的 descriptors，尤其在争议或高风险用途下。
- 对抽象 trait/KSAO 推论更谨慎；尽量用 task evidence 支撑。
- 使用多个 sources，如 incumbents、supervisors、experts、analysts，并比较差异。
- 训练 raters，让他们理解量表、目的和评分标准。
- 使用清楚 instructions 和标准化 response scales。
- pilot test 问卷和访谈提纲。
- 匿名收集问卷，减少 self-presentation 或政治压力。
- 报告 disagreement，而不是只报告 mean。
- 让 SMEs review 报告，核实内容并解释异常分歧。
- 把低 reliability 当作需要调查的信号：它可能是 error，也可能是真实 job variation。

## 教学时的简化解释

如果用户是初学者，可以这样分层讲：

1. **先讲描述统计**：平均数、标准差、样本数、标准误。
2. **再讲可靠性**：这些评分是不是稳定、一致。
3. **再讲效度**：这些评分能不能支持我们的目的。
4. **最后讲偏差**：为什么人的判断可能不准确，怎么降低风险。

如果用户问公式，只展开 mean、SD、SEM 的概念和直觉；若没有数据，不要凭空计算。
