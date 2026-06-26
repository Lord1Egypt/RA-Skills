# Tasks
- [x] Task 1: 基线梳理与风险映射
  - [x] SubTask 1.1: 对齐主技能、上传子技能、README、配置模板中的凭证字段定义差异
  - [x] SubTask 1.2: 梳理上传策略端点来源与覆盖路径，确认硬编码与环境变量优先级
  - [x] SubTask 1.3: 梳理请求日志默认值、开关行为与敏感字段脱敏覆盖范围

- [x] Task 2: 实现凭证与端点合规加固（保持兼容）
  - [x] SubTask 2.1: 统一凭证元信息文档与模板字段，补充历史字段兼容读取策略
  - [x] SubTask 2.2: 收敛上传策略端点配置，增加可信主机约束与结构化审计日志
  - [x] SubTask 2.3: 确保默认端点、覆盖端点与回退链路均不破坏上传成功路径

- [x] Task 3: 实现日志最小披露策略
  - [x] SubTask 3.1: 将请求日志默认调整为关闭，仅显式开启时输出
  - [x] SubTask 3.2: 扩展敏感字段脱敏规则，避免 token/策略/签名参数外泄
  - [x] SubTask 3.3: 保留调试可用性，输出必要排障上下文且避免明文请求体

- [x] Task 4: 回归验证与发布前检查
  - [x] SubTask 4.1: 回归验证搜索→生成→上传→报告主链路功能无损
  - [x] SubTask 4.2: 覆盖“默认配置、历史配置、自定义端点、调试日志开关”四类场景
  - [x] SubTask 4.3: 更新发布说明与安装注意事项，确保 ClawHub 审查信息可解释

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 2 and Task 3
