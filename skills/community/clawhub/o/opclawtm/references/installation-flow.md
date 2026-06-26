# 安装与激活流程

> 你是 AI Agent，此文档指导你如何帮助用户完成 opclawtm 安装和激活。

---

## 流程步骤

### Step 1：检查用户环境

**执行命令：**
```bash
node --version
```

**判断结果：**
- 版本 ≥ v18.0.0 → 继续 Step 2
- 版本 < v18.0.0 → 告知用户需要升级 Node.js
- 命令失败 → Node.js 未安装，告知用户安装 Node.js

---

### Step 2：安装 opclawtm

**执行命令：**
```bash
npm install -g opclawtm
```

**判断结果：**
- 安装成功 → 继续 Step 3
- 网络错误 → 建议用户检查网络或使用镜像源
- 权限错误 → 建议用户使用管理员权限

---

### Step 3：验证安装

**执行命令：**
```bash
opclawtm --version
```

**判断结果：**
- 显示版本号（如 1.9.0）→ 安装成功，继续 Step 4
- 命令不存在 → npm 全局路径未配置，告知用户检查 PATH

---

### Step 4：试用激活

**执行命令：**
```bash
opclawtm trial-activate
```

**判断结果：**

| 输出内容 | 你的行动 |
|----------|----------|
| "已自动激活 3 天试用授权" | 告知用户激活成功，显示授权 Key 和有效期 |
| "该设备已使用过试用授权" | 告知用户：访问 https://opclawtm.com 购买授权，或抖音私信 1594204110 获取测试码 |
| 网络错误 | 建议用户检查网络连接 |

---

### Step 5：查看授权状态（可选）

**执行命令：**
```bash
opclawtm license-status
```

**向用户反馈：**
- 显示授权有效期
- 显示剩余天数

---

## 处理测试码

如果用户提供测试码（格式：TM-TEMP-XXXX-XXXX）：

**执行命令：**
```bash
opclawtm bind-license --key TM-TEMP-XXXX-XXXX
```

**判断结果：**
- 绑定成功 → 告知用户激活成功
- Key 无效 → 告知用户 Key 无效，需要重新获取

---

## 常见问题处理

| 问题 | 你的行动 |
|------|----------|
| npm install 失败 | 建议使用镜像：`npm install -g opclawtm --registry=https://registry.npmmirror.com` |
| 命令不存在 | 检查 npm 全局路径：`npm config get prefix`，告知用户添加到 PATH |
| 授权已过期 | 告知用户购买授权或获取测试码 |