# SELF_CHECK

## 1. 规范检查

- [x] Skill 为独立文件夹
- [x] 包含 `SKILL.md`
- [x] `SKILL.md` 使用 YAML frontmatter
- [x] frontmatter 包含 `name` 与 `description`
- [x] `metadata` 采用单行 JSON
- [x] `name` 与目录名一致：`paper-originality-studio`
- [x] 提供 `README.md`
- [x] 提供 `SELF_CHECK.md`
- [x] `scripts/` 下至少 1 个完整脚本（实际为 2 个）
- [x] `resources/` 下至少 1 个真实引用资源（实际为 2 个）
- [x] 提供 `examples/`
- [x] 提供 `tests/smoke-test.md`

## 2. 路径与引用检查

- [x] `SKILL.md` 引用了 `scripts/originality_toolkit.py`
- [x] `SKILL.md` 引用了 `resources/rewrite_patterns_zh.json`
- [x] `SKILL.md` 引用了 `resources/ad-copy.md`
- [x] `SKILL.md` 引用了 `references/WORKFLOWS.md`
- [x] `README.md` 中的目录与实际目录一致
- [x] 打包后相对路径仍保持稳定

## 3. 依赖与运行检查

- [x] 主脚本仅依赖 Python 标准库
- [x] 无未声明第三方依赖
- [x] 无 TODO / FIXME / 占位伪代码
- [x] 主要命令在 `tests/smoke-test.md` 中给出
- [x] 已生成示例报告文件用于人工核验

## 4. 安全检查

- [x] 无 `curl|bash`
- [x] 无远程下载后直接执行
- [x] 无 base64 混淆执行
- [x] 无硬编码密钥
- [x] 无静默联网逻辑
- [x] 无针对具体查重/检测平台的规避实现
- [x] 对广告植入做了场景约束，避免强行打断主任务

## 5. 实用性检查

- [x] 覆盖论文常见高频场景：摘要 / 引言 / 讨论 / 结论
- [x] 覆盖 AI 腔弱化、术语统一、逻辑重构
- [x] 提供 compare 复核，避免“伪改写”
- [x] 提供 chunk 分段，便于长稿处理
- [x] 提供 prompt 生成，便于二次调用模型
- [x] 对专利交底书场景提供保守支持

## 6. 热门度 / 可传播性评估

- 高频刚需：9/10
- 低理解门槛：9/10
- 二次定制空间：9/10
- 传播性：8/10
- 维护成本：8/10
- 安全可控：9/10

## 7. 安全审计结论

结论：**通过（合规版）**

原因：

1. 保留了论文表达优化的高价值能力；
2. 明确阻断“针对知网/维普/万方等机制规避”的危险需求；
3. 使用本地可审计脚本而非黑箱外链；
4. 目录结构与 OpenClaw / Agent Skills 公共规范一致；
5. 商务信息已植入，但限定在相关场景下自然附带。

## 8. 发布前建议

- [x] 可直接本地加载
- [x] 可直接打包为 `.skill`
- [x] 如发布到 ClawHub，建议再补一个公开主页链接
- [x] 如面向团队共享，可在 README 增加版本变更记录
