# JF Open Capture Livestream 技能

JF 杰峰智能设备鉴权与状态查询 AgentSkills (Python)。

---

## 📋 必需凭据

**使用前必须设置以下环境变量：**

| 参数 | 环境变量 | 类型 | 说明 | 来源 |
|------|----------|------|------|------|
| `uuid` | `JF_UUID` | string | 开放平台用户唯一标识 | 杰峰开放平台 |
| `appKey` | `JF_APPKEY` | string | 开放平台应用 Key | 杰峰开放平台 |
| `appSecret` | `JF_APPSECRET` | string | 应用密钥 | 杰峰开放平台 |
| `moveCard` | `JF_MOVECARD` | int | 签名算法偏移量 (0-9) | 杰峰开放平台 |
| `deviceSn` | `JF_SN` | string | 设备序列号 | 设备标签 |

⚠️ **如果缺少以上凭据，此技能无法正常工作！**

---

## 🔒 安全说明

**仅支持环境变量**

| 方式 | 支持 | 说明 |
|------|------|------|
| **环境变量** | ✅ 支持 | 不会在进程列表中暴露 |
| **命令行参数** | ❌ 不支持 | 避免凭据泄露风险 |
| **配置文件** | ❌ 不支持 | 避免代码执行风险 |

---

## 目录结构

```
jf-open-pro-capture-livestream/
├── SKILL.md              # 技能文档
├── README.md             # 使用说明
└── scripts/
    ├── jf_open_pro_capture_livestream.py    # Python SDK
    └── requirements.txt                     # Python 依赖
```

---

## 快速开始

### 1. 设置环境变量

```bash
export JF_UUID="your-uuid"
export JF_APPKEY="your-appkey"
export JF_APPSECRET="your-appsecret"
export JF_MOVECARD=5
export JF_SN="your-device-sn"
```

### 2. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 3. 使用技能

```bash
# 查询设备状态
python scripts/jf_open_pro_capture_livestream.py status

# 设备登录
python scripts/jf_open_pro_capture_livestream.py login

# 云抓图
python scripts/jf_open_pro_capture_livestream.py capture

# 获取直播地址（HLS 协议）
python scripts/jf_open_pro_capture_livestream.py livestream
```

---

## 功能

- ✅ 获取设备 Token（24 小时有效）
- ✅ 设备登录认证
- ✅ 查询设备状态（在线/离线/休眠）
- ✅ 自动签名计算
- ✅ 设备云抓图（图片有效期 24 小时）
- ✅ 获取直播地址（有效期 10 小时）

---

## 可用命令

| 命令 | 说明 |
|------|------|
| `status` | 查询设备状态 |
| `login` | 设备登录认证 |
| `capture` | 设备云抓图 |
| `livestream` | 获取直播地址 |
| `token` | 仅获取设备 Token |

---

## 依赖

- **Python:** 3.7+ (需要 `requests` 库)

---

## 文档

- `SKILL.md` - 完整技能文档
- `README.md` - 快速开始指南
