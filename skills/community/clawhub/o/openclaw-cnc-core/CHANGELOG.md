# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-03-26

### Security
- 🛡️ Nginx反向代理防护
- 🔒 限流保护 (20次/分钟/IP)
- 📦 上传限制 (50MB)
- 🔐 安全头注入 (X-Frame-Options, X-Content-Type-Options)

### Changed
- README添加在线演示地址
- 演示地址改为80端口 (Nginx代理)

## [1.1.0] - 2026-03-26

### Added
- 多平台API适配器 (`core/config.py`)
- 支持 6 种 LLM 服务商
- 多平台适配文档 (`docs/PROVIDERS.md`)
- 本地模型支持 (Ollama)

### Changed
- 移除硬编码的 API 配置
- 支持环境变量配置
- 提高平台兼容性

### Supported Providers
| Provider | ID | API Key Required |
|----------|-----|------------------|
| DashScope | `dashscope` | Yes |
| OpenAI | `openai` | Yes |
| DeepSeek | `deepseek` | Yes |
| 智谱AI | `zhipu` | Yes |
| Moonshot | `moonshot` | Yes |
| Ollama (本地) | `local` | No |

## [1.0.0] - 2026-03-26

### Added
- 初始版本发布
- 核心报价引擎框架
- STEP图纸解析模块
- 风险控制模块
- 混合检索器
- 案例检索器
- 中英文文档

### Features
- 材料库管理框架
- 工时计算算法
- 报价单生成
- 风险预警

### Documentation
- README 中英文双语
- 部署指南
- API文档

### Contact
- 官网: https://openclaw.ai/cnc
- 邮箱: miscdd@163.com
- QQ: 849355070