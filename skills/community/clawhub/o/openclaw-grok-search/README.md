# openclaw-grok-search

一个基于 `grok-skill` 改编的跨平台联网搜索 Skill，面向 OpenClawd（龙虾）/Codex 场景，支持 Windows、macOS、Linux 在项目本地目录直接使用。

## 项目缘起

我最近在玩龙虾（OpenClawd），发现系统自带网络搜索比较鸡肋：

1. Brave API 申请要绑信用卡。
2. 免费版经常触发调用速率限制。
3. 可获取资源不稳定，检索覆盖也受限。

后来逛 L 站时发现了宝藏项目 `grok-skill`。本项目基于原始项目做了改编，重点增强了可移植性和跨平台兼容性。

原始项目参考：`grok-skill`（https://github.com/Frankieli123/grok-skill）

## 核心改造

1. 从 PowerShell 安装/配置改为 Python 脚本，兼容 Win/macOS/Linux。
2. 默认仅在项目下载目录内运行，不再强依赖 `~/.codex` 安装路径。
3. 保留 `grok_search.py` 的结构化 JSON 输出能力（`content` + `sources`）。
4. 保留可扩展参数：`--extra-body-json`、`--extra-headers-json`。

## 最近修复（2026-02-23）

为提升第三方 OpenAI 兼容中转站可用性，`scripts/grok_search.py` 已同步以下兼容增强：

1. SSE 回退解析：当中转站在 `stream=false` 下仍返回 `data: {...}` 分片时，自动拼接为标准 `chat.completion` 结构，避免 `json.loads` 直接失败。
2. 嵌入 JSON 提取：当模型输出为 `<think>...```json {...}```` 或“前置思考 + JSON”时，可提取最终 JSON，恢复 `content`/`sources` 结构化结果。
3. 解析兜底不破坏原行为：若本身就是标准 JSON 响应，仍走原路径，不影响既有使用方式。

## 快速开始

### 一、龙虾安装（OpenClaw）

在龙虾里直接让助手安装这个 skill：

- https://github.com/Stemmaker/openclaw-grok-search

可直接使用这句话：

```text
请帮我安装这里的 skill：https://github.com/Stemmaker/openclaw-grok-search
```

### 二、各大编程 CLI 安装（推荐）

```bash
npx skills add Stemmaker/openclaw-grok-search
```

### 三、手动安装（git clone）

```bash
git clone https://github.com/Stemmaker/openclaw-grok-search.git
cd openclaw-grok-search
```

然后在项目目录执行：

```bash
python scripts/configure.py
python scripts/grok_search.py --query "What changed in Python recently?"
```

## ⚙️ 配置说明

### 方式 A：交互式配置（推荐）

```bash
python scripts/configure.py
```

### 方式 B：手动编辑

编辑项目目录下的配置文件：

```
openclaw-grok-search/config.json
```

```json
{
  "base_url": "https://your-grok-endpoint.example",
  "api_key": "YOUR_API_KEY",
  "model": "grok-4.20-beta",
  "timeout_seconds": 60,
  "extra_body": {},
  "extra_headers": {}
}
```

| 字段 | 说明 |
|------|------|
| `base_url` | 你的 Grok API 端点地址 |
| `api_key` | 你的 API 密钥（**不要提交到 Git**） |
| `model` | 模型名称（如 `grok-4.20-beta`） |
| `timeout_seconds` | 请求超时时间（秒） |
| `extra_body` | 额外的请求体参数 |
| `extra_headers` | 额外的 HTTP 请求头 |

### 方式 C：环境变量

```bash
export GROK_BASE_URL="https://your-grok-endpoint.example"
export GROK_API_KEY="YOUR_API_KEY"
export GROK_MODEL="grok-4.20-beta"
```

## 公益中转站信息（第三方）

### 注册链接：

- https://ai.huan666.de/register?aff=eB8Z

### 站点特性：

1. 注册即送 10 刀。
2. `grok-4.20-beta` 每次搜索约消耗 0.01刀。
3. 若你有 [L 站](https://linux.do/t/topic/1627339)，可再领站点大佬红包 20 刀。
4. 新上线 `Claude Sonnet 4.6`（输入 2/M，输出 10/M）。
5. 每天签到可随机领金额。
6. 纯公益站，不能现金充值，只能使用L站的LDC充值，但是如果只使用grok搜索每天签到积分完全够用。

## 项目结构

```text
openclaw-grok-search/
├─ SKILL.md
├─ config.example.json
└─ scripts/
   ├─ configure.py
   └─ grok_search.py
```

## 隐私与安全

1. API Key 保存在本地配置文件中，请勿提交到公开仓库。
2. 建议把真实密钥写入 `config.local.json`，并加入忽略列表。
3. 第三方中转站属于外部服务，请注意账号和密钥安全。

## 开源协议

沿用上游项目协议（MIT）

## 作者

- 作者：橙家厨子
- 邮箱：tomography2308@163.com

## 求个 Star

如果这个项目对你有帮助，欢迎 Star 支持，也欢迎提 Issue / PR 一起完善。
