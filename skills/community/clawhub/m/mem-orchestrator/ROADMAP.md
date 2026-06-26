# ROADMAP

## 当前状态

这是一个**可用的白盒文件型记忆 skill 原型**。

它已经具备：
- 分层记忆目录
- summary-first recall
- 显式触发词与 `/` 命令
- gate / turn 流程
- daily / reflection / index
- 统一 CLI

---

## Phase 1：当前已完成

### 基础结构
- [x] memory 根目录初始化
- [x] topic cards
- [x] object directories
- [x] session-state
- [x] daily logs
- [x] reflection output
- [x] index generation

### 基础流程
- [x] gate
- [x] recall
- [x] write events
- [x] reflect
- [x] CLI 入口

### 白盒支持
- [x] README
- [x] skill README
- [x] architecture doc
- [x] object/topic 可读说明

---

## Phase 2：建议下一步

### 召回质量
- [ ] 更细的 scoring
- [ ] 更强的 suppression 规则
- [ ] 更稳定的 summary 更新
- [ ] 更好的 domain expansion

### 对象质量
- [ ] 更系统的 object template
- [ ] project/person/note 等类型的更明确 schema
- [ ] object merge 机制
- [ ] object rename / refactor 机制

### 反思质量
- [ ] 从 daily log 自动提炼 topic update
- [ ] 从 repeated event 提升 stable preference
- [ ] 更好的 relation inference
- [ ] stale memory 降权机制

---

## Phase 3：更深集成（暂缓）

### OpenClaw 工作流接入
- [ ] 把 turn 流程嵌到真实会话入口
- [ ] 自动注入 recall 输出到回答上下文
- [ ] 低频后台 reflect 调度

### 更强智能层
- [ ] 更强的语义召回
- [ ] 更自然的跨域联想
- [ ] 更智能的 durability 判定
- [ ] 更细粒度的用户偏好建模

---

## 当前 intentionally not done

这些不是忘了做，而是故意先不做：

- [ ] 向量数据库
- [ ] 黑盒 embedding pipeline
- [ ] 每条消息自动跑重 memory
- [ ] 大规模自动对象抽取
- [ ] 深度 OpenClaw 内核改动

理由：
- 优先验证白盒结构是否顺手
- 优先验证显式触发是否足够好用
- 优先保证可维护，而不是先堆复杂度
