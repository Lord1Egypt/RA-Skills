# 故障排查指南

> 🖤 混合层级隔离架构 1.0 - 常见问题与解决方案

## 快速诊断流程

```
遇到问题
    │
    ├─ 1. 是配置问题？ → 运行 config-check.sh
    │
    ├─ 2. 是角色行为问题？ → 检查 SOUL.md
    │
    ├─ 3. 是技能调用问题？ → 检查技能安装
    │
    ├─ 4. 是沟通问题？ → 检查@提及
    │
    └─ 5. 仍无法解决？ → 查看详细排查步骤
```

## 常见问题

### 问题 1：墨墨越权执行 baoyu-* 技能

**症状**：
```
用户：@墨墨 生成一张图片
墨墨：好的，正在调用 baoyu-image-gen... ❌
```

**原因**：
- SOUL.md 未正确配置
- 墨墨未遵守约束
- 配置未生效

**解决方案**：

1. **检查 SOUL.md**
   ```bash
   cat ~/Documents/openclaw/agents/writer/SOUL.md | grep -i "baoyu"
   ```
   
   应该包含：
   ```markdown
   ❌ 禁止直接执行 baoyu-* 技能
   ```

2. **重新应用模板**
   ```bash
   cp templates/writer-soul-template.md \
      ~/Documents/openclaw/agents/writer/SOUL.md
   ```

3. **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

4. **测试验证**
   ```
   用户：@墨墨 生成一张图片
   预期：墨墨应该指派小媒，而不是自己执行
   ```

**预防措施**：
- 定期运行 `config-check.sh`
- 更新 SOUL.md 后备份
- 用户监督并及时纠正

---

### 问题 2：小媒无法访问 baoyu-* 技能

**症状**：
```
用户：@小媒 生成一张图片
小媒：抱歉，我无法调用图片生成技能... ❌
```

**原因**：
- 技能未安装
- 技能路径配置错误
- 权限问题

**解决方案**：

1. **检查技能是否存在**
   ```bash
   ls -la ~/Documents/openclaw/agents/writer/skills/ | grep baoyu
   # 或
   ls -la ~/.openclaw/skills/ | grep baoyu
   ```

2. **安装缺失技能**
   ```bash
   clawhub install baoyu-image-gen
   # 或其他 baoyu-* 技能
   ```

3. **检查技能权限**
   ```bash
   # 确保技能目录可读
   chmod -R 755 ~/Documents/openclaw/agents/writer/skills/baoyu-*
   ```

4. **验证技能加载**
   ```bash
   openclaw skills list | grep baoyu
   ```

**预防措施**：
- 安装架构时同时安装所有 baoyu-* 技能
- 定期更新技能
- 检查技能兼容性

---

### 问题 3：任务流转混乱

**症状**：
```
用户：帮我写文章并发布
墨墨：好的，我来写...（然后没有下文了）❌
小媒：我不知道要做什么... ❌
```

**原因**：
- 职责边界不清晰
- 沟通机制不完善
- 缺乏协调

**解决方案**：

1. **明确任务分解**
   ```
   墨墨应该：
   1. 接收任务
   2. 分解为：写作 + 配图 + 发布
   3. 指派小媒：配图
   4. 自己负责：写作
   5. 协调发布
   ```

2. **建立沟通机制**
   ```
   墨墨：@小媒 哥哥需要 3 张配图，请帮忙生成~
   小媒：收到！预计 10 分钟完成
   墨墨：好的，我等你完成后整合发布
   ```

3. **使用@提及**
   - 明确@对象
   - 说明任务详情
   - 设定预期时间

**预防措施**：
- 培训墨墨的任务分解能力
- 建立标准沟通模板
- 定期回顾改进

---

### 问题 4：紧急任务响应慢

**症状**：
```
用户：@小媒 紧急！马上要海报！
小媒：好的，我先问问墨墨... ❌
```

**原因**：
- 紧急流程未建立
- 小媒过度依赖墨墨
- 响应机制不清晰

**解决方案**：

1. **建立紧急通道**
   ```
   用户直接@小媒 → 小媒立即执行 → 事后同步墨墨
   ```

2. **明确紧急定义**
   - 包含"紧急"、"立刻"、"马上"等关键词
   - 时间要求<10 分钟
   - 允许简化流程

3. **小媒响应模板**
   ```
   收到！紧急任务优先处理！⚡
   预计 [X] 分钟完成
   完成后同步墨墨记录~
   ```

**预防措施**：
- 培训小媒识别紧急任务
- 建立紧急响应 SOP
- 定期演练

---

### 问题 5：配置检查失败

**症状**：
```bash
$ bash templates/config-check.sh
❌ FAIL: Writer SOUL.md 不存在
❌ FAIL: Media SOUL.md 不存在
```

**原因**：
- 模板未复制
- 路径不正确
- 文件被误删

**解决方案**：

1. **手动复制模板**
   ```bash
   # Writer
   cp templates/writer-soul-template.md \
      ~/Documents/openclaw/agents/writer/SOUL.md
   
   # Media
   cp templates/media-soul-template.md \
      ~/Documents/openclaw/agents/media/SOUL.md
   ```

2. **检查路径**
   ```bash
   # 确认 Agent 目录
   ls -la ~/Documents/openclaw/agents/
   
   # 如路径不同，调整命令
   ```

3. **重新运行检查**
   ```bash
   bash templates/config-check.sh
   ```

**预防措施**：
- 安装时立即复制模板
- 备份重要配置文件
- 定期检查配置

---

### 问题 6：Gateway 重启后配置丢失

**症状**：
```
重启前：墨墨正确指派小媒
重启后：墨墨直接执行 baoyu-* 技能 ❌
```

**原因**：
- SOUL.md 未正确保存
- 配置缓存问题
- Gateway 未正确重载

**解决方案**：

1. **验证 SOUL.md 内容**
   ```bash
   cat ~/Documents/openclaw/agents/writer/SOUL.md
   ```

2. **强制重载配置**
   ```bash
   openclaw gateway stop
   openclaw gateway start
   ```

3. **检查日志**
   ```bash
   tail -f /tmp/openclaw/openclaw-*.log | grep writer
   ```

4. **测试验证**
   ```
   用户：@墨墨 生成图片
   预期：墨墨指派小媒
   ```

**预防措施**：
- 修改配置后验证保存
- 重启后测试关键功能
- 保留配置备份

---

### 问题 7：多 Agent 路由错误

**症状**：
```
用户：@墨墨 生成图片
实际响应：小媒（而不是墨墨）❌
```

**原因**：
- openclaw.json 配置错误
- Agent ID 映射错误
- 路由规则混乱

**解决方案**：

1. **检查 openclaw.json**
   ```bash
   cat ~/.openclaw/openclaw.json | python3 -m json.tool
   ```
   
   应该包含：
   ```json
   {
     "channels": {
       "feishu": {
         "bots": [
           {
             "appId": "cli_xxx",
             "agentId": "writer"
           },
           {
             "appId": "cli_yyy",
             "agentId": "media"
           }
         ]
       }
     }
   }
   ```

2. **验证 Agent ID**
   - writer → 墨墨
   - media → 小媒

3. **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

**预防措施**：
- 修改配置前备份
- 使用 JSON 格式化工具验证
- 测试路由后再投入使用

---

## 高级排查

### 日志分析

**查看墨墨日志**：
```bash
tail -f /tmp/openclaw/openclaw-*.log | grep writer
```

**查看小媒日志**：
```bash
tail -f /tmp/openclaw/openclaw-*.log | grep media
```

**查看技能调用日志**：
```bash
tail -f /tmp/openclaw/openclaw-*.log | grep baoyu
```

### 性能诊断

**检查响应时间**：
```bash
# 查看消息处理时间
grep "receive message" /tmp/openclaw/openclaw-*.log | tail -20
```

**检查技能加载**：
```bash
openclaw skills list | grep -E "writer|media|baoyu"
```

### 内存和状态

**检查 Agent 状态**：
```bash
openclaw status
```

**检查会话状态**：
```bash
# 查看当前活跃会话
ls -la /tmp/openclaw/sessions/
```

---

## 联系支持

如以上方法无法解决问题：

1. **收集信息**
   - 问题描述
   - 错误日志
   - 配置片段（脱敏）
   - 复现步骤

2. **提交问题**
   - GitHub Issues
   - OpenClaw 社区
   - 水产市场反馈

3. **临时方案**
   - 回退到单 Agent 模式
   - 手动执行任务
   - 等待修复

---

## 故障排查清单

每次遇到问题，按此清单检查：

- [ ] 运行 `config-check.sh`
- [ ] 检查 SOUL.md 配置
- [ ] 验证技能安装
- [ ] 查看错误日志
- [ ] 测试基本功能
- [ ] 重启 Gateway
- [ ] 验证修复效果

---

**最后更新**: 2026-03-08  
**维护者**: OpenClaw 社区
