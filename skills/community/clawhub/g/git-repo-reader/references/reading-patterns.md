# 不同类型项目的阅读技巧

## 框架类项目（Framework/Library）

**代表：** React、Django、FastAPI、Spring Boot

**阅读重点：**
- **抽象层设计**：接口如何定义？扩展点在哪里？
- **生命周期管理**：初始化 → 运行 → 销毁的流程
- **插件/中间件机制**：如何让用户扩展功能？
- **配置体系**：默认配置 vs 用户自定义

**核心模块位置：**
- `core/`、`kernel/`、`foundation/` — 最底层抽象
- `middleware/`、`plugins/`、`extensions/` — 扩展机制
- `lifecycle/`、`bootstrap/`、`runtime/` — 生命周期

**快速评估：**
1. 看 `src/core` 或 `lib/` 目录下的接口定义
2. 找一个具体功能（如"路由"），追踪从用户调用到底层实现的完整链路
3. 看测试文件，了解框架的预期使用方式

---

## 工具类项目（CLI/Utility）

**代表：** ripgrep、jq、httpie、fzf、bat

**阅读重点：**
- **命令解析**：怎么把用户输入翻译成操作？
- **核心算法/逻辑**：这个工具最核心的功能是怎么实现的？
- **输出格式化**：结果怎么展示？支持哪些格式？
- **性能优化**：如果是高性能工具，看关键路径的优化手段

**核心模块位置：**
- `src/cli.rs`、`cmd/`、`commands/` — 命令解析
- `src/main.rs`、`__main__.py`、`index.js` — 入口和流程控制
- 以工具名命名的核心文件（如 `ripgrep` 的 `search.rs`）

**快速评估：**
1. 看 `--help` 输出对应哪些代码文件
2. 找一个简单命令，追踪从参数解析到执行的完整路径
3. 看 `README` 里的 benchmark 或性能声明对应的实现

---

## 算法/模型类项目（Algorithm/ML）

**代表：** transformers、scikit-learn、LLaMA.cpp、faiss

**阅读重点：**
- **算法实现**：核心算法的数学公式怎么翻译成代码？
- **数据结构**：用了哪些特殊的数据结构来优化？
- **训练/推理流程**：数据流是怎样的？
- **优化技巧**：量化、剪枝、并行、内存优化

**核心模块位置：**
- `model/`、`algorithms/`、`core/` — 核心算法
- `ops/`、`kernels/`、`cuda/` — 底层算子
- `data/`、`dataset/` — 数据处理和加载

**快速评估：**
1. 找论文或文档中的算法伪代码，对照代码实现
2. 看 `benchmarks/` 或 `tests/` 了解性能预期
3. 如果支持 GPU/CUDA，看 `kernels/` 里的实现

---

## 应用类项目（Application）

**代表：** GitLab、Bitwarden、Home Assistant、Nextcloud

**阅读重点：**
- **架构模式**：MVC？微服务？单体？事件驱动？
- **数据模型**：核心实体和它们的关系
- **API 设计**：REST/GraphQL/gRPC 的定义和使用
- **部署架构**：Docker？K8s？Serverless？
- **认证/授权**：安全模型是怎样的？

**核心模块位置：**
- `api/`、`routes/`、`controllers/` — 接口层
- `models/`、`entities/`、`schema/` — 数据模型
- `services/`、`usecases/`、`handlers/` — 业务逻辑
- `frontend/`、`ui/`、`web/` — 前端（如果是全栈）
- `deploy/`、`docker/`、`helm/` — 部署配置

**快速评估：**
1. 看 `docker-compose.yml` 了解服务组成
2. 看数据库 migration/schema 了解数据模型
3. 看 `api/` 目录下的路由定义了解功能全貌
4. 看 `README` 的 Development/Deployment 章节

---

## 基础设施类项目（Infrastructure/DevOps）

**代表：** Kubernetes、Terraform、Prometheus、Nginx

**阅读重点：**
- **控制循环（Control Loop）**：状态如何收敛到期望状态？
- **配置解析**：DSL/JSON/YAML 怎么被解析和验证？
- **插件/驱动架构**：如何适配不同的后端？
- **监控/遥测**：怎么暴露指标和状态？

**核心模块位置：**
- `controller/`、`operator/`、`scheduler/` — 控制逻辑
- `plugin/`、`driver/`、`provider/` — 适配层
- `config/`、`manifest/` — 配置定义和解析
- `metrics/`、`telemetry/`、`observability/` — 监控

**快速评估：**
1. 看 `examples/` 或 `docs/examples/` 了解典型配置
2. 看 `architecture.md` 或 `design.md` 了解高层设计
3. 找 controller/operator 的核心循环逻辑

---

## 通用速读策略

### 3分钟判断法

| 时间 | 做什么 | 产出 |
|------|--------|------|
| 0-30s | 看 README 标题 + 第一句描述 | 解决什么问题 |
| 30s-1m | 看 stars/forks + 最后更新时间 + 许可证 | 成熟度和可用性 |
| 1m-2m | 看 examples/Quick Start 代码 | 怎么用 |
| 2m-3m | 看目录结构，识别主要模块 | 技术栈和架构 |

### 值得深入的信号
- ⭐ > 1000 且近期活跃
- 解决了你当前的具体问题
- 技术栈与你的技术债/技术方向匹配
- 代码组织清晰，有测试覆盖
- 文档完整，有 examples

### 快速放弃的信号
- 许可证不兼容（如 GPL 限制商用）
- 半年以上无更新且 issues 堆积
- README 只有标题没有说明
- 没有测试，目录混乱
- 依赖过多且老旧
