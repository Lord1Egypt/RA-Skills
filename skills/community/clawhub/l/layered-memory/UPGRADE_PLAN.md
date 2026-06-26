# layered-memory 升级路线图

**当前版本**: v1.1.0  
**最后更新**: 2026-03-13 06:23 AM

---

## Phase 1: 性能优化 (v1.2.0) - 短期高价值

### 1.1 增量更新
- **问题**: 每次 `generate --all` 都重新处理所有文件，浪费 CPU
- **方案**: 
  - 记录每个文件的 `mtime` 和生成的 L0/L1 的 `mtime`
  - 只处理源文件比 L0/L1 更新的情况
  - 使用 `fs.stat` 或 watch 模式
- **收益**: 生成速度提升 80%+，适合大仓库

### 1.2 并发生成
- **问题**: 单线程顺序处理，无法利用多核
- **方案**:
  - 使用 `Promise.all` 或 `worker_threads`
  - 控制并发数（默认 4，可配置）
- **收益**: 4 核机器提速 ~3x

### 1.3 Config 实际支持
- **现状**: 有 `config.example.json` 但代码未读取
- **实现**:
  - `loadConfig()` 读取 `config.json` 或 `.layered-memory.json`
  - 支持 CLI 参数覆盖 `--max-tokens`, `--skip`, `--concurrency`
- **收益**: 用户可自定义行为，提升灵活性

### 1.4 进度与错误恢复
- 生成时显示百分比进度条（使用 `progress` 包或自定义）
- 某个文件失败时跳过并记录，不影响其他文件
- 维护模式生成报告（成功/失败数量）

---

## Phase 2: 智能化增强 (v1.3.0) - 中期价值

### 2.1 智能摘要算法
- **当前**: 简单截取前 N 行或章节
- **升级**: 
  - 使用 TF-IDF 提取关键词
  - 基于标题和首句判断重要性
  - L0 控制在 100 tokens，L1 控制在 1000 tokens
- **工具**: 可引入 `natural` 或 `node-textrank`

### 2.2 L0 关键词索引
- **问题**: L0 全文搜索效率低（每次都要解析 markdown）
- **方案**: 
  - 生成 L0 时同时生成 `.keywords.json`（倒排索引）
  - 搜索时先查索引，再读取对应 L0 内容
- **收益**: 搜索速度提升 10x，适合频繁查询

### 2.3 动态分层策略
- 不同文件类型使用不同策略：
  - `MEMORY.md` - 侧重任务总结
  - 日志文件 (`\d{4}-\d{2}-\d{2}.md`) - 侧重日期和标题
  - 文档 (`DOC.md`) - 侧重章节结构
- 可配置 `layers.strategies` 映射

---

## Phase 3: 服务化 (v2.0.0) - 长期生态

### 3.1 API 服务器
```bash
layered-memory serve --port 8080
```
- REST API:
  - `GET /layers?path=...&layer=l0`
  - `POST /generate` (触发生成)
  - `GET /search?q=...&layer=l1`
- 支持 CORS，允许多进程访问

### 3.2 Web UI
- 单页面应用展示分层结构
- 手动触发生成、查看统计
- 配置管理界面

### 3.3 Docker 支持
```dockerfile
FROM node:20-alpine
COPY . /app
RUN npm ci --only=production
EXPOSE 8080
CMD ["node", "index.js", "serve"]
```

### 3.4 监控与指标
- Prometheus metrics:
  - `layered_memory_generation_seconds`
  - `layered_memory_cache_hits_total`
  - `layered_memory_tokens_saved`
- 健康检查端点 `/health`

---

## 实施建议

**优先级排序 (ROI 最高 -> 最低)**:
1. ✅ Config 实际支持 (1-2 天)
2. ✅ 增量更新 (2-3 天)
3. ✅ 并发生成 (1-2 天)
4. ⏳ 进度显示 (0.5 天)
5. ⏳ L0 关键词索引 (3-4 天)
6. ⏳ 智能摘要 (5-7 天)
7. ⏳ API 服务器 (5-7 天)
8. ⏳ Web UI (7-10 天)

**第一个里程碑**: v1.2.0 (增量 + 并发 + config)  
**预期发布时间**: 1-2 周内

---

## 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 增量更新逻辑错误导致遗漏文件 | 中 | 高 | 添加单元测试 + dry-run 模式 |
| 并发导致 race condition | 中 | 中 | 使用锁文件或原子操作 |
| 智能摘要质量下降 | 低 | 中 | A/B 测试，保持回退机制 |
| API 服务器增加复杂度 | 低 | 低 | 保持核心库独立，serve 作为独立命令 |

---

**推荐行动**: 立即开始 v1.2.0 开发，先实现增量更新和并发。
