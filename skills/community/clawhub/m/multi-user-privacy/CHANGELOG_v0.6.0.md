# Multi-User Privacy v0.6.0 更新说明

## 🆕 v0.6.0 (2026-03-11)

### Session 会话管理

**新增功能：**
- ✅ Session 检查（确保对话隔离）
- ✅ 用户专属 session 记录
- ✅ Session 不匹配警告
- ✅ Session 统计工具

**新增文件：**
- `scripts/session-guard.js` - Session 管理工具

**使用方式：**

```bash
# 查看 Session 统计
node scripts/session-guard.js stats

# 清空 Session 数据库
node scripts/session-guard.js clear
```

**集成到 privacy-guard：**
```javascript
const pg = require('./skills/multi-user-privacy/privacy-guard');

// 对话前自动检查 session
const result = pg.preCheck(context);

if (result.status === 'PASS') {
    console.log('✅ Session 检查通过');
} else {
    console.error('❌ Session 检查失败:', result.error);
}
```

---

## 📊 版本历史

### v0.5.0 - P2 改进完整版
- 异常行为检测
- 实时告警系统
- 配置热更新
- 性能优化

### v0.4.0 - 完整隔离
- 记忆文件物理隔离
- 配置统一管理
- 防绕过机制
- 自动注入启动

### v0.3.1 - 项目归属检查
- 项目权限管理
- 增强日志审计

### v0.3.0 - 基础功能
- 身份识别
- 记忆隔离
- 隐私检查

---

## 📋 Session 管理说明

### 问题背景

**当前问题：**
- 多个用户的对话消息可能混在同一个 session 中
- 导致 AI 无法正确区分用户身份
- 造成隐私泄露和上下文混淆

### 解决方案

**Session Guard 功能：**
1. 为每个用户创建专属 session 记录
2. 跟踪用户活动状态
3. 检查 session 匹配
4. Session 不匹配时发出警告

### 使用示例

**查看当前 Session 状态：**
```bash
node scripts/session-guard.js stats
```

**输出示例：**
```
📊 Session 统计:

总 Session 数：3

Session 列表:
  - ou_b96f5424607baf3a0455b55e0f4a2213: 150 条消息 (最后活跃：2026-03-11T08:00:00.000Z)
  - ou_ba3410ec9024501b3383141a5ba7bec4: 80 条消息 (最后活跃：2026-03-11T08:05:00.000Z)
  - ou_f5618661cbdcc6f3abb79571db7ec604: 20 条消息 (最后活跃：2026-03-10T15:00:00.000Z)
```

### 注意事项

**技能层面限制：**
- ✅ 可以记录 session 状态
- ✅ 可以检查 session 匹配
- ✅ 可以发出警告
- ⚠️ 无法控制消息路由（需要平台支持）

**建议：**
- 定期检查 session 统计
- 发现异常及时清空 session 数据库
- 向 OpenClaw 团队反馈 session 隔离需求

---

## 🔧 故障排查

### Session 不匹配警告

**现象：**
```
[SessionGuard] ⚠️ 检测到非管理员用户，请确保 session 隔离正确
```

**原因：**
- 多个用户的消息混在同一个 session 中

**解决方案：**
1. 查看 session 统计：`node scripts/session-guard.js stats`
2. 清空 session 数据库：`node scripts/session-guard.js clear`
3. 重新创建专属 session

### Session 数据库损坏

**现象：**
```
[SessionGuard] 加载 Session 数据库失败
```

**解决方案：**
```bash
# 清空并重建
node scripts/session-guard.js clear
```

---

## 📞 支持

- 文档：查看 SKILL.md
- 问题：提交 Issue
- 更新日志：查看本文件
