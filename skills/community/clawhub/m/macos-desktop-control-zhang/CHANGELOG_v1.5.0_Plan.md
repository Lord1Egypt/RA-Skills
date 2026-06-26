# macOS Desktop Control v1.5.0 - ControlMemory 方案

> **版本**: 1.5.0  
> **功能**: 操作行为记忆 + 共享学习系统  
> **状态**: 📋 方案设计  
> **创建日期**: 2026-03-31 23:23

---

## 🎯 核心目标

### 1. 快速掌握控制 App 的方法
- 记录所有成功的操作行为
- 形成可复用的操作模式
- 新用户快速上手

### 2. ControlMemory 文档系统
- 本地记忆库：`controlmemory.md`
- 云端共享：ClawHub
- 版本控制：Git

### 3. 社区协作学习
- 用户贡献成功操作
- 自动查重避免重复
- 每小时自动同步

---

## 📁 系统架构

```
┌─────────────────────────────────────────────────┐
│              用户操作层                          │
│  自然语言 → 解析 → 执行 → 成功/失败              │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│           ControlMemory 记录层                   │
│  成功操作 → 格式化 → 本地存储 → 等待同步          │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│            ClawHub 同步层                        │
│  定时同步 → 查重 → 上传/下载 → 合并              │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│            社区共享层                            │
│  所有用户 ← 下载 ← ClawHub 服务器 → 上传 → 所有用户
└─────────────────────────────────────────────────┘
```

---

## 📝 ControlMemory 文档格式

### 本地文件位置
```
~/.openclaw/workspace/skills/macos-desktop-control/controlmemory.md
```

### 文档结构

```markdown
# ControlMemory - macOS Desktop Control 操作记忆库

> **版本**: 1.5.0  
> **最后更新**: 2026-03-31 23:23  
> **贡献者**: 所有用户  
> **总记录数**: 0

---

## 📊 统计信息

| 应用 | 成功操作数 | 最后更新 | 贡献者 |
|------|-----------|---------|--------|
| Safari | 0 | - | - |
| Chrome | 0 | - | - |
| QQ | 0 | - | - |
| ... | ... | ... | ... |

---

## 🎯 操作记录

### Safari 浏览器

#### 打开 Safari
- **命令**: "打开 Safari"
- **执行**: `open -a "Safari"`
- **成功率**: 100%
- **备注**: 系统自带，100% 可靠
- **贡献者**: system
- **添加时间**: 2026-03-31

#### 关闭窗口
- **命令**: "关闭 Safari"
- **执行**: `osascript -e 'tell application "Safari" to quit'`
- **成功率**: 100%
- **备注**: 完全退出应用
- **贡献者**: system
- **添加时间**: 2026-03-31

### QQ

#### 打开 QQ
- **命令**: "打开 QQ"
- **执行**: `osascript -e 'tell application "QQ" to activate'`
- **成功率**: 100%
- **备注**: 需要登录状态
- **贡献者**: system
- **添加时间**: 2026-03-31

#### 发送消息
- **命令**: "用 QQ 给 {好友} 发消息 {内容}"
- **执行**: AppleScript + 手动确认
- **成功率**: 50-80%
- **备注**: UI 结构可能变化，需手动选择好友
- **贡献者**: system
- **添加时间**: 2026-03-31
- **限制**: 需要辅助功能权限

---

## 🔄 更新日志

### 2026-03-31
- 初始版本
- 添加基础操作记录
- 系统预置操作

### 2026-04-01
- （等待用户贡献）

---

## 📖 贡献指南

### 如何贡献新操作

1. **成功执行新操作**
   - 使用自然语言控制
   - 操作成功完成

2. **自动记录**
   - 系统自动记录到本地 controlmemory.md
   - 格式化为标准格式

3. **同步到 ClawHub**
   - 每小时自动同步
   - 查重后上传

4. **审核机制**
   - 社区审核
   - 通过后合并到主库

### 查重规则

以下情况视为重复：
- 命令相同
- 执行脚本相同
- 目标应用相同

以下情况视为新记录：
- 新的应用
- 新的操作方式
- 更高的成功率
- 更好的备注说明

---

## 🛠️ 技术实现

### 1. 操作记录模块

**文件**: `scripts/control_memory.py`

**功能**:
- 监听操作执行结果
- 格式化成功操作
- 写入本地 controlmemory.md

**示例代码**:
```python
class ControlMemory:
    def __init__(self):
        self.memory_file = Path.home() / ".openclaw" / "workspace" / "skills" / "macos-desktop-control" / "controlmemory.md"
    
    def record_success(self, command, script, app_name, notes=""):
        """记录成功操作"""
        record = {
            'command': command,
            'script': script,
            'app': app_name,
            'success_rate': '100%',
            'notes': notes,
            'contributor': get_user_id(),
            'timestamp': datetime.now()
        }
        
        # 查重
        if not self.is_duplicate(record):
            self.append_to_memory(record)
            self.sync_to_clawhub(record)
    
    def is_duplicate(self, record):
        """检查是否重复"""
        # 实现查重逻辑
        pass
    
    def sync_to_clawhub(self, record):
        """同步到 ClawHub"""
        # 实现同步逻辑
        pass
```

---

### 2. ClawHub 同步模块

**文件**: `scripts/clawhub_sync.py`

**功能**:
- 定时同步（每小时）
- 下载最新记录
- 上传新记录
- 冲突解决

**同步流程**:
```
1. 检查本地新记录
2. 下载 ClawHub 最新记录
3. 合并（本地优先）
4. 查重
5. 上传新记录
6. 更新本地文档
```

**示例代码**:
```python
class ClawHubSync:
    def __init__(self):
        self.api_url = "https://clawhub.com/api/v1/skills/macos-desktop-control"
        self.sync_interval = 3600  # 1 小时
    
    def sync(self):
        """执行同步"""
        # 下载
        remote_records = self.download_records()
        
        # 合并
        merged = self.merge_records(remote_records)
        
        # 上传
        new_records = self.get_new_records()
        for record in new_records:
            if not self.is_duplicate_in_remote(record):
                self.upload_record(record)
        
        # 更新本地
        self.update_local_memory(merged)
```

---

### 3. 定时任务模块

**文件**: `scripts/scheduler.py`

**功能**:
- 每小时同步
- 自动备份
- 冲突通知

**配置**:
```python
# 使用系统 cron
0 * * * * cd /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control && python3 scripts/clawhub_sync.py

# 或使用 Python schedule 库
import schedule

schedule.every().hour.do(sync_to_clawhub)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🔐 权限和安全

### 权限要求

| 权限 | 用途 | 必需性 |
|------|------|--------|
| **文件读写** | 记录操作 | ⭐⭐⭐ 必需 |
| **网络访问** | ClawHub 同步 | ⭐⭐ 推荐 |
| **Git 操作** | 版本控制 | ⭐⭐ 推荐 |

### 安全措施

1. **用户匿名化**
   - 使用用户 ID 哈希
   - 不记录个人信息

2. **操作审核**
   - 社区审核机制
   - 恶意操作过滤

3. **版本控制**
   - Git 版本管理
   - 可回滚到任意版本

4. **本地优先**
   - 本地记录优先
   - 网络失败不影响使用

---

## 📊 数据格式

### 单条记录格式

```json
{
  "id": "uuid-v4",
  "app": "Safari",
  "command": "打开 Safari",
  "script": "open -a \"Safari\"",
  "success_rate": "100%",
  "notes": "系统自带，100% 可靠",
  "contributor": "user-hash-xxx",
  "timestamp": "2026-03-31T23:23:00+08:00",
  "verified": false,
  "votes": 0
}
```

### 查重算法

```python
def check_duplicate(new_record, existing_records):
    """查重算法"""
    for record in existing_records:
        # 完全匹配
        if (record['app'] == new_record['app'] and 
            record['command'] == new_record['command'] and
            record['script'] == new_record['script']):
            return True
        
        # 相似度匹配（可选）
        similarity = calculate_similarity(
            record['command'], 
            new_record['command']
        )
        if similarity > 0.9:
            return True
    
    return False
```

---

## 🎯 实施计划

### 阶段 1: 基础功能（2-3 小时）

- [ ] 创建 controlmemory.md 模板
- [ ] 实现操作记录模块
- [ ] 实现本地存储
- [ ] 测试记录功能

### 阶段 2: ClawHub 集成（3-4 小时）

- [ ] 研究 ClawHub API
- [ ] 实现同步模块
- [ ] 实现查重功能
- [ ] 测试同步功能

### 阶段 3: 定时任务（1 小时）

- [ ] 配置 cron 任务
- [ ] 实现自动备份
- [ ] 测试定时同步

### 阶段 4: 社区功能（2-3 小时）

- [ ] 实现贡献指南
- [ ] 实现审核机制
- [ ] 实现投票系统
- [ ] 文档完善

**总预计**: 8-11 小时

---

## 📈 预期效果

### 短期（1 周）
- 基础操作记录 100+ 条
- 活跃贡献者 10+ 人
- 文档完善度 80%

### 中期（1 月）
- 操作记录 500+ 条
- 覆盖主流应用 50+ 个
- 成功率统计完善

### 长期（3 月）
- 操作记录 2000+ 条
- 社区贡献者 100+ 人
- 成为 macOS 自动化标准

---

## 🎊 优势分析

### 对用户
- ✅ 快速学习控制方法
- ✅ 避免重复踩坑
- ✅ 社区互助学习

### 对开发者
- ✅ 收集真实使用数据
- ✅ 发现常见问题
- ✅ 持续优化技能

### 对社区
- ✅ 知识共享
- ✅ 集体智慧
- ✅ 生态繁荣

---

## 📝 总结

**可行性**: ✅ **95% 可实施**

**核心价值**:
1. 快速掌握控制 App 的方法
2. 集体智慧，避免重复造轮子
3. 社区协作，持续进化

**下一步**:
1. 确认方案
2. 开始实施阶段 1
3. 测试基础功能

---

**这个方案可以编写吗？** 

**答案**: ✅ **完全可以！** 

所有技术都已具备：
- ✅ Python 文件操作
- ✅ Markdown 格式化
- ✅ Git 版本控制
- ✅ HTTP API 调用
- ✅ Cron 定时任务
- ✅ 文本查重算法

**唯一不确定**: ClawHub API 的具体接口（需要调研）

**建议**: 先实施阶段 1（本地记录），再实施阶段 2（ClawHub 集成）

🦐
