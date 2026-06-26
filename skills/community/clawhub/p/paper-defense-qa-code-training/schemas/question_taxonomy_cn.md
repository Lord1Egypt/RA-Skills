# 论文答辩问题分类法

## 1. 贡献与故事线

- 这篇论文一句话贡献是什么？
- 它解决的问题为什么重要？
- 如果没有这篇论文，领域缺的是什么？
- 它的贡献是 problem、method、theory、benchmark、system 还是 empirical finding？
- 论文标题中的每个关键词分别对应方法中的哪一部分？

## 2. 相关工作与创新性

- 最接近的 prior work 是哪篇？
- 本文和 prior work 的差异是新问题、新约束、新机制，还是新组合？
- 为什么不是 obvious combination？
- 如果加入某个强 baseline，结论会不会变弱？
- 论文有没有遗漏关键相关工作？

## 3. 方法机制

- 输入、输出、中间状态分别是什么？
- 每个模块解决哪个 failure mode？
- 哪个模块是核心贡献？哪个是工程辅助？
- 方法训练和推理阶段是否一致？
- 方法依赖的隐藏假设是什么？
- 复杂度、内存、延迟、通信成本是多少？

## 4. 公式 / 理论

- 关键公式每一项的含义是什么？
- loss 的每个权重如何设置？
- 定理证明了什么，没有证明什么？
- 理论假设和真实实现是否匹配？
- 如果假设被违反，方法会怎样失败？

## 5. 实验设计

- 每个实验块试图回答什么问题？
- 数据集和 metric 是否匹配论文主张？
- baseline 是否覆盖最强对手？
- baseline 是否公平调参？
- 是否有多个 seed、方差、置信区间？
- 消融能否证明机制，还是只证明性能下降？
- 有无 stress test / OOD / robustness / failure cases？

## 6. 代码实现

- 主结果由哪个命令复现？
- 哪个 config 对应主表格？
- 数据预处理在哪里实现？
- 论文公式对应代码哪一段？
- 是否存在未写在论文里的 trick？
- 评估 metric 是否和论文定义一致？
- baseline 是否使用相同数据管线？

## 7. 训练过程

- optimizer、lr schedule、batch size、epoch/steps 是什么？
- 超参搜索空间是什么？如何选择最优超参？
- checkpoint 选择是否看了 test set？
- 混合精度、分布式训练、gradient clipping 是否影响结果？
- 多少个 seed？失败 run 是否记录？
- 需要多少 GPU 小时？是否和 baseline 成本可比？

## 8. 可复现性

- 是否给了 dependencies？
- 是否给了训练、评估脚本？
- 是否给了 pretrained weights？
- README 是否有精确命令和预期结果？
- 第三方是否可以不联系作者复现主结果？

## 9. 局限性与风险

- 最弱的 claim 是什么？
- 方法在哪些 setting 下会失败？
- 是否有伦理、隐私、公平性、安全或法律问题？
- 是否有数据污染或 benchmark overfitting 风险？
- 是否过度泛化到未测试场景？

## 10. 未来工作

- 最直接的 follow-up experiment 是什么？
- 哪个 hidden assumption 最值得攻击？
- 这个方法能迁移到哪个相邻领域？
- 什么新 benchmark 更能检验贡献？
- 如何把工程改进提升为科学问题？
