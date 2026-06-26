# 爱马仕进化版 - 部署检查清单

## 部署前检查

- [ ] 确认 Node.js 版本 ≥ 16
- [ ] 确认 OpenClaw 已安装并可运行
- [ ] 备份当前配置
- [ ] 确认飞书 Channel 已配置

## 文件复制

- [ ] 复制所有 `.js` 文件到 `skills/sensen-pm-router/`
- [ ] 复制 `tasks/` 目录
- [ ] 复制 `rules/` 目录
- [ ] 复制 `corrections/` 目录
- [ ] 复制 `schedules/` 目录（如有）

## 验证测试

### 核心模块测试

- [ ] `test-task-store.js` - 任务存储
- [ ] `test-intent-router.js` - 意图路由
- [ ] `test-self-improving-v2.js` - 自改进

### 增强功能测试

- [ ] `test-frozen-memory.js` - 冻结记忆
- [ ] `test-patch-store.js` - 增量更新
- [ ] `test-enhanced-skill.js` - Skill 增强
- [ ] `test-fts-indexer.js` - 全文检索
- [ ] `test-progressive-disclosure.js` - 渐进披露
- [ ] `test-periodic-nudge.js` - 主动自检

### 智能化测试

- [ ] `test-auto-skill-generator.js` - 自动创建
- [ ] `test-llm-summarizer.js` - LLM 摘要
- [ ] `test-honcho-profiler.js` - 用户画像

### 系统集成测试

- [ ] `test-logger.js` - 日志系统
- [ ] `test-dag.js` - DAG 依赖
- [ ] `test-template.js` - 模板引擎
- [ ] `test-collaborator.js` - 协作调度
- [ ] `test-collab-visualizer.js` - 协作可视化
- [ ] `test-scheduler.js` - 定时调度

## 健康检查

- [ ] `openclaw gateway status` 正常
- [ ] 端口 18790 可访问
- [ ] 飞书消息可发送
- [ ] Cron 任务正常运行

## 回滚准备

- [ ] 备份位置确认
- [ ] 回滚脚本可用
- [ ] 备份文件完整性检查

---

## 升级 OpenClaw 后的检查清单

### 升级前

- [ ] 备份爱马仕配置到新目录
- [ ] 记录当前 OpenClaw 版本

### 升级中

- [ ] 执行 `npm update openclaw -g`
- [ ] 确认版本变化

### 升级后

- [ ] OpenClaw 基础功能正常
- [ ] Gateway 可启动
- [ ] Skills 可加载
- [ ] **爱马仕测试全部通过**
- [ ] Channel 集成正常
- [ ] Cron 任务正常

### 如有问题

- [ ] 检查 API 变化
- [ ] 更新相关模块
- [ ] 测试后重新部署

---

**完成所有检查后，爱马仕进化版即可投入使用。**

---

*检查清单版本: v1.0 | 更新: 2026-04-11*
