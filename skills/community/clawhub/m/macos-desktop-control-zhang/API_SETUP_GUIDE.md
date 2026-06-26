# ClawHub API 配置指南

> **配置日期**: 2026-04-01  
> **平台状态**: 早期开发阶段

---

## 📋 ClawHub 平台现状

**当前状态**:
```
ClawHub 平台：早期开发阶段
技能上传：暂不可用
API 注册：暂不可用
统计功能：暂不可用
```

**官网信息**:
```
Popular skills
Most-downloaded, non-suspicious picks.
No skills yet. Be the first.
```

---

## 🔑 API Key 获取方式

### 方式 1: 等待平台开放（推荐）

**步骤**:
1. 访问 https://clawhub.com
2. 注册账号
3. 等待 API 功能开放
4. 创建应用获取 API Key

**现状**: ⏳ 平台还在开发中，API 暂未开放

---

### 方式 2: 使用本地模式（当前可用）

**说明**: 
- 不配置 API Key
- 仅使用本地功能
- 手动导出分享

**配置**:
```bash
# 无需配置
# 本地功能完全可用
```

---

## ⚙️ API 配置方法（平台开放后）

### 方法 1: 环境变量（推荐）

**步骤**:

1. **编辑 ~/.zshrc**:
```bash
nano ~/.zshrc
```

2. **添加 API Key**:
```bash
export CLAWHUB_API_KEY="your-api-key-here"
```

3. **保存并生效**:
```bash
source ~/.zshrc
```

4. **验证配置**:
```bash
echo $CLAWHUB_API_KEY
# 应该显示你的 API Key
```

---

### 方法 2: 脚本配置

**编辑 clawhub_sync.py**:
```bash
nano /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control/scripts/clawhub_sync.py
```

**修改**:
```python
# 找到这行（约第 25 行）
self.api_key = os.getenv('CLAWHUB_API_KEY', '')

# 修改为
self.api_key = "your-api-key-here"
```

**保存**: `Ctrl+O` → `Enter` → `Ctrl+X`

---

### 方法 3: 配置文件（推荐用于生产）

**创建配置文件**:
```bash
nano /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control/.env
```

**内容**:
```
CLAWHUB_API_KEY=your-api-key-here
CLAWHUB_API_BASE=https://clawhub.com/api/v1
SKILL_ID=macos-desktop-control
```

**修改脚本读取配置**:
```python
# 在 clawhub_sync.py 开头添加
from dotenv import load_dotenv
load_dotenv()
self.api_key = os.getenv('CLAWHUB_API_KEY', '')
```

---

## 🧪 测试同步

### 测试命令

```bash
cd /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control
python3 scripts/clawhub_sync.py
```

### 预期输出（配置 API 后）

```
🔄 开始 ClawHub 同步...
   时间：2026-04-01 00:12:xx

📥 下载远程记录...
✅ 下载成功：0 条记录

🔀 合并记录...
⏳ 查重并上传新记录...
✅ 上传成功：6 条新记录

📝 更新本地文件...
✅ 同步完成！上传 6 条新记录
```

---

## 📊 同步策略

### 智能同步规则

```python
# 每 6 小时同步一次
sync_interval_hours = 6

# 2 小时内有新记录则同步
check_interval_hours = 2

# 判断逻辑
if 距离上次同步 >= 6 小时:
    执行同步
elif 距离上次同步 >= 2 小时 and 有新记录:
    执行同步
else:
    跳过同步（节省 API 调用）
```

---

### 定时任务配置

**自动配置**:
```bash
cd /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control
bash scripts/setup_cron.sh
```

**手动配置**:
```bash
crontab -e

# 添加（每 6 小时同步）
0 0,6,12,18 * * * cd /path/to/macos-desktop-control && python3 scripts/clawhub_sync.py
```

**验证**:
```bash
crontab -l | grep clawhub
```

---

## 🎯 当前可用功能

### 无需 API（100% 可用）✅

| 功能 | 状态 | 说明 |
|------|------|------|
| **本地记录** | ✅ | 记录操作到 controlmemory.md |
| **借鉴次数** | ✅ | 自动增加借鉴次数 |
| **失败记录** | ✅ | 自动记录失败 |
| **质量评分** | ✅ | 自动计算评分 |
| **智能检索** | ✅ | 本地检索和排序 |
| **自然语言** | ✅ | 完整自然语言控制 |

### 需要 API（平台开放后）⏳

| 功能 | 状态 | 说明 |
|------|------|------|
| **上传记录** | ⏳ | 上传到 ClawHub |
| **下载记录** | ⏳ | 下载社区记录 |
| **社区共享** | ⏳ | 共享操作记录 |
| **统计查看** | ⏳ | 查看下载量等 |

---

## 📝 配置检查清单

### 当前配置（无 API）

- [x] 本地记录功能
- [x] 智能检索功能
- [x] 质量评分系统
- [x] 定时任务脚本
- [ ] ClawHub API Key（平台未开放）
- [ ] 云端同步（平台未开放）

### 平台开放后配置

- [ ] 注册 ClawHub 账号
- [ ] 创建应用
- [ ] 获取 API Key
- [ ] 配置环境变量
- [ ] 测试同步
- [ ] 配置定时任务
- [ ] 上传技能记录

---

## 🎊 总结

### 现阶段（平台开发中）

**推荐做法**:
```
✅ 使用本地功能
- 本地记录操作
- 本地智能检索
- 本地质量评分
- 无需 API Key
```

**配置状态**:
```
✅ 本地功能：100% 可用
⏳ 云端功能：等待平台开放
```

---

### 平台开放后

**配置步骤**:
1. 注册 ClawHub 账号
2. 获取 API Key
3. 配置环境变量
4. 测试同步
5. 配置定时任务

**预计时间**: 10 分钟

---

## 📞 获取帮助

### 问题排查

**问题 1: API Key 无效**
```
解决：检查 API Key 是否正确
     确认平台已开放 API
```

**问题 2: 同步失败**
```
解决：检查网络连接
     检查 API 端点是否正确
     查看详细错误日志
```

**问题 3: 定时任务不执行**
```
解决：检查 crontab 配置
     检查脚本路径
     查看 cron 日志
```

---

**配置指南创建日期**: 2026-04-01  
**平台状态**: 早期开发阶段  
**下次更新**: 平台开放 API 后
