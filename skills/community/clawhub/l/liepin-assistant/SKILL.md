---
name: liepin-assistant
description: |
  猎聘求职助手，封装 Liepin MCP 服务。用于搜索职位、查看 JD、投递简历、管理简历。

  **触发场景**：
  (1) 用户提到"猎聘"、"liepin"、"liepin求职"、"猎聘求职"、"猎聘助手"、"liepin助手"、"找工作"、"搜职位"、"投简历"、"查看简历"
  (2) 用户提供猎聘 token 并要求配置
  (3) 用户要搜索职位、查看 JD、投递岗位

  **必须配置凭证**。凭证获取：https://www.liepin.com/mcp/server → 登录 → 生成凭证。设置环境变量 LIEPIN_TOKEN（推荐）或运行 set-token.js 将 token 写入 config.json。
---

# 猎聘求职

## 快速使用

1. 配置 Token：用户发送「设置猎聘token xxx」
2. 搜索职位：说「搜前端职位」
3. 投递简历：确认后说「投递这个职位」

## Token 配置

### 方式一（推荐）：环境变量

**最安全**，token 不落地，只存在于当前进程环境：

```bash
export LIEPIN_TOKEN=<你的token>
```

### 方式二：配置文件

如果环境变量未设置，则回退到 config.json：

```bash
node scripts/set-token.js <token>
```

查看当前 token 状态：

```bash
node scripts/set-token.js --show
```

**清除已保存的 token：**

```bash
node scripts/set-token.js --clear
```

Token 获取方式：打开 https://www.liepin.com/mcp/server → 登录 → 生成凭证 → 复制 token（有效期 90 天）

---

## 工作流程

### 1. 搜索职位

关键词、地点均可选；jobKind 通常为 "2"（正式职位）：

```bash
node scripts/liepin-mcp.js user-search-job '{"jobName":"AI","address":"北京"}'
```

### 2. 投递职位

**jobId 必须是数字类型**（从搜索结果的职位ID获取），jobKind 从搜索结果获取（通常为 "2"）：

```bash
node scripts/liepin-mcp.js user-apply-job '{"jobId":81543059,"jobKind":"2"}'
```

### 3. 查看我的简历

```bash
node scripts/liepin-mcp.js my-resume '{}'
```

### 4. 补充简历信息

修改简历各项（基本信息、工作经历、教育经历、项目经历、求职期望、自我评价）：

```bash
# 修改基本信息
node scripts/liepin-mcp.js modify-resume-base-info '{"realName":"姓名","sex":"男","birthday":"19950101"}'
# 添加工作经历
node scripts/liepin-mcp.js add-work-exp '{"compName":"公司名","rwTitle":"职位名称","workStart":"202001","workEnd":"202312"}'
```

---

## 注意事项

- Token 有效期 90 天，过期后重新生成并配置
- 频率限制 60 次/分钟，搜索/投递共用配额
- 每次投递前先展示职位详情，用户确认后再投
- jobId 必须是**数字类型**（不是字符串），jobKind 为字符串
- 所有操作记录可在猎聘 App 查看
- **优先读取环境变量 `LIEPIN_TOKEN`**，未设置则回退到 config.json

## 错误排查

| 现象 | 原因 | 方案 |
|-----|------|-----|
| "token not configured" | 未设置过 token | 用户发送"设置猎聘token xxx" |
| "Request failed" | 网络问题 | 等待几秒重试 |
| errCode != 0 | 业务错误 | 查看返回的具体错误信息 |
