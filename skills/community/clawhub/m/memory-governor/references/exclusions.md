# Exclusions

## 什么不要记

以下内容默认不进入记忆系统：

- secret、token、密码、私钥
- 原始长日志、完整控制台输出、巨量抓取结果
- 两周内高概率失效的运行态
- 纯闲聊、无后续价值的对话碎片
- 无法验证的猜测
- 没有新信息的重复记录
- 只属于项目文档的问题，却被误写到全局记忆
- 为了“显得完整”而保留的噪声

## 判断原则

一条信息如果不能改善未来的：

- 判断
- 恢复
- 执行质量
- 协作一致性

那它大概率不该进记忆系统。

## 反例

这些看起来“像该记”，但通常不该记：

- 一整段终端报错原文
- 某次临时授权状态
- 某次短期实验的原始过程细节
- 没提炼的聊天记录摘抄

## 外部导入内容

新版 OpenClaw 支持把外部对话（例如 ChatGPT 历史）作为 Imported Insights 导入记忆体系。

治理立场：

- 导入内容**未经本宿主验证**，默认不能当成 canonical truth
- 它应被当作 `learning_candidates` 一类的低承诺输入，而不是直接进入 `long_term_memory` / `reusable_lessons` / 系统级规则
- 编译层（Memory Wiki、People Wiki、Memory Palace）可以索引它，但升格仍要走人工 review

判定顺序：

1. 先看这条导入内容是否真的能改善未来判断 / 恢复 / 执行 / 协作
2. 如果能，先进入 `learning_candidates`
3. 只有在跨任务重复验证后，才考虑升到 `reusable_lessons` 或更上层

不要：

- 把整段外部对话原样塞进 `long_term_memory`
- 因为“这是用户在别的平台说过的”就直接当成稳定偏好
- 让导入内容绕过候选层，被编译层直接当成长期事实

详见 [correction-pipeline.md](correction-pipeline.md) 和 [compiled-surfaces.md](compiled-surfaces.md)。

## 隐私 / 作用域边界

新版 OpenClaw 在 recall 层引入了访问控制（例如 Active Memory Filters 的 `allowedChatIds` / `deniedChatIds`）。

治理立场：

- 某些记忆天然带作用域（项目内、会话内、某个 agent 内）
- capture 时应在 target class 条目上记录 scope，而不是只依赖 recall 期过滤
- 编译层不得扩大一条已捕获记忆的 scope：项目内事实被编译进全局 People Wiki 页面，就是泄露，即使 target class 写对了

高风险类别：

- 跨会话导入的内容
- 群聊里出现的敏感信息
- 只对某个项目成立的局部事实

这些默认应带显式 scope，并在 review 时确认编译层没有越界。
