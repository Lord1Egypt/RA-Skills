# 技术排障领域（tech-support）

## 识别特征
问题涉及：Bug定位、环境问题、性能优化、报错信息、代码调试、架构问题等。

## 任务类型
- bug-diagnosis：Bug分析定位
- environment-setup：环境安装配置
- performance-optimization：性能问题
- architecture-debugging：架构问题排查

## 必要槽位
| 槽位 | 说明 |
|------|------|
| environment | 运行环境 |
| error_message | 报错信息 |
| reproduction_steps | 复现步骤 |
| expected_behavior | 预期行为 |

## 常见缺失项
- 操作系统/服务器环境
- 完整报错日志
- 近期改动记录
- 是否能稳定复现

## 追问模板
1. "你当前的环境是本地、服务器、容器还是云环境？"
2. "报错信息能贴出关键内容吗？"
3. "这是新增功能时报错，还是原来正常现在异常？"

## Rewrite 模板
请以资深工程师视角，针对【{environment}】中出现的【{error_message}】问题，基于【{reproduction_steps}】进行排查，结合【{expected_behavior}】输出可能原因、验证步骤与修复建议。
