# 钉钉考勤集成 - 当前状态

## ✅ 已完成

| 功能 | 状态 | 说明 |
|------|------|------|
| 获取 Token | ✅ 成功 | App Token 正常获取 |
| 获取部门列表 | ✅ 成功 | 13 个部门 |
| 获取用户列表 | ✅ 成功 | 46 个用户 |
| 数据导出 | ✅ 成功 | JSON 格式保存 |

## ❌ 待开通权限

| 功能 | 状态 | 需要权限 |
|------|------|---------|
| 获取考勤组 | ❌ 权限未开通 | 考勤管理 |
| 获取打卡记录 | ❌ 权限未开通 | 考勤管理 |
| 获取考勤报表 | ❌ 权限未开通 | 考勤管理 |

---

## 📋 需要开通的权限

在钉钉开放平台后台添加以下权限：

### 考勤管理权限
- 获取打卡记录
- 获取考勤组
- 获取考勤报表

### 申请步骤
1. 访问 https://open-dev.dingtalk.com
2. 进入「应用开发」→「企业内部开发」
3. 找到你的企业内部应用（按应用名称搜索）
4. 点击「权限管理」
5. 点击「添加权限」
6. 搜索「考勤」并添加相关权限
7. 提交审批

---

## 📁 已获取的数据

**文件位置**: `data/attendance/attendance_20260414.json`

**数据内容**:
- 13 个部门
- 46 个员工（包含姓名和用户 ID）

**示例数据**:
```json
{
  "date": "2026-04-13",
  "totalDepartments": 13,
  "totalUsers": 46,
  "users": [
    {"userId": "024525676521834425", "name": "景合"},
    {"userId": "011619524836381958", "name": "郭大侠"},
    ...
  ]
}
```

---

## 🚀 使用方法

### 手动运行
```bash
cd keplerjai-dingtalk-attendance
node index.js
```

### 运行后
- 用户数据会保存到 `data/attendance/` 目录
- 文件名格式：`attendance_YYYYMMDD.json`

---

## ⏭️ 考勤权限开通后

权限开通并审批通过后，运行：
```bash
node index.js
```

脚本会自动获取：
- 考勤组信息
- 员工打卡记录
- 考勤报表

---

## 📊 应用信息

| 项目 | 值 |
|------|-----|
| AppKey | 见本地 `.env` |
| AgentId | 见本地 `.env` |
| AppId | 见本地 `.env` |
| 应用类型 | 企业内部开发 |
| 企业名称 | 成都景合亿家科技有限公司 |

---

## 🔧 配置文件

`.env`（示例）：
```env
DINGTALK_APP_KEY=你的 AppKey
DINGTALK_APP_SECRET=你的 AppSecret
DINGTALK_AGENT_ID=你的 agentId
DINGTALK_APP_ID=你的 appId
OUTPUT_DIR=./data/attendance
OUTPUT_FORMAT=json
```

---

更新时间：2026-04-14
