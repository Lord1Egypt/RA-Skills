# llmfill skill（LLMFill Agent Skill）

将 [LLMFill](https://www.llmfill.com) 的 **Word 文档智能填写** 与 **知识库管理**
能力封装为 Agent Skill：上传 .docx 让 AI 自动填表并下载结果；建知识库、
传资料供填写时检索取答案。适用于 Claude Code / Claw 等 agent 应用。

> ⚠️ **隐私与数据外发**：本 skill 会把上传的 .docx 表单、知识库资料连同 API 令牌
> 发送到 `llmfill.com` 远程处理/存储。请勿上传机密、个人敏感数据、受监管或仅限
> 内网的文档，除非你已获得授权；API 令牌为长效明文凭据，注意防泄露（详见 SKILL.md）。

## 安装（SkillHub）

```bash
npx --yes clawhub@0.23.3 install llmfill@1.0.8    # 安装器与 skill 均锁定已审计版本
```

执行前可先做**完整性校验（fail-closed）**——从 npm registry 实时取 digest
与下方已知值比对，不匹配即中止、不执行 npx：

```bash
expected='sha512-VwM6FQrZVarFRDiEqG42npUeyCu/iLhPnpO+b7kKIGRXv+TA6Lb8pboHnIgT6cmjFEnW3j/pTbshWeDQMQ7QWQ=='
[ "$(npm view clawhub@0.23.3 dist.integrity)" = "$expected" ] \
  && npx --yes clawhub@0.23.3 install llmfill@1.0.8 \
  || echo 'clawhub@0.23.3 完整性校验失败，已中止安装'
```

> 供应链说明：安装器锁定 `clawhub@0.23.3`，skill 锁定 `llmfill@1.0.8`，二者均固定到
> 已审计的具体版本（`--yes` 跳过首次安装的交互确认，适配 agent 非交互场景）。
> 升级任一版本前请先核对新版本再更新此处版本号。注意：锁定版本不等于强制校验
> integrity；需要严格校验时，请先核对 npm registry digest 再执行。
> integrity（clawhub@0.23.3）：
`sha512-VwM6FQrZVarFRDiEqG42npUeyCu/iLhPnpO+b7kKIGRXv+TA6Lb8pboHnIgT6cmjFEnW3j/pTbshWeDQMQ7QWQ==`

## 快速开始

```bash
# 1. 首次配置（只填 API Key，服务地址内置；无 Python 见 references/curl-guide.md）
python scripts/llmfill.py config

# 2. 填一份表
python scripts/llmfill.py fill 表单.docx --json

# 3. 建知识库，填表时挂载
python scripts/llmfill.py kb create --name "资料库"
python scripts/llmfill.py kb upload <kb_id> 手册.pdf
python scripts/llmfill.py fill 表单.docx --kb <kb_id>
```

详见 `SKILL.md`（skill 入口）与 `examples/`。

## 特性

- **零依赖**：纯 Python 3.10+ 标准库，无需 pip install
- **端到端**：fill 命令内部完成 上传 -> 轮询 -> 下载 全流程
- **agent 友好**：全命令 `--json` 输出；`discover` 自动发现接口
- **统一错误**：网关级错误码（见 references/errors.md）

## 版本

- `1.0.8`：README 安装命令与版本说明对齐至 1.0.7（仅文档更新）。
- `1.0.7`：优化部分secrets的描述。
- `1.0.6`：`--token-env` 新增 secret 引用/掩码占位符识别（`store:xxx` / `***` 直接
  拒绝并引导用户本人配置，防 agent 平台 secrets 未注入时把占位符当令牌）；SKILL.md
  移除「用 secrets 中转令牌」的误导、明确 agent 场景由用户本人落 config.json；
  `--token-env` 定位为 shell/CI 等真实环境变量场景。
- `1.0.5`：`--token-env` 收紧为白名单变量名（防误读无关密钥）；令牌统一 aif_ 格式
  校验；远程验证通过才落盘；README 增加 fail-closed 完整性校验命令；curl 指南加
  agent 执行确认门。
- `1.0.4`：curl 指南改用 curl 配置文件注入令牌；文件删除接口补不可恢复警示；
  SKILL.md 增加机器可读权限声明；端点信任改为完整 origin 比较（修端口绕过）；
  安装命令锁定 skill 版本。
- `0.1.0`（beta）：首发。填写/知识库/检索/whoami/discover。

## 结构

```
skill-llmfill/
├── SKILL.md              # skill 入口（frontmatter: name/description）
├── scripts/
│   ├── llmfill.py        # 主 CLI
│   ├── api_client.py    # 统一 HTTP（X-Auth-Token、错误解析、multipart）
│   └── config.py        # ~/.llmfill/config.json 读写
├── references/           # 接口详解（渐进式披露）
├── examples/             # 端到端示例
└── tests/                # pytest（25 用例：配置/错误解析/multipart/轮询/CLI）
```

## 测试

```bash
python -m pytest tests/ -q
```
