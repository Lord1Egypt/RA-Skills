# keplerjai-oss-uploader

将本地文件上传到阿里云 OSS，并输出 `bindHost` 下的可访问 URL。适用于 Agent / OpenClaw 技能场景。

规范参考：[OpenClaw Skills](https://docs.openclaw.ai/tools/skills)。

## 仓库内文件

| 文件 | 作用 |
|------|------|
| `SKILL.md` | OpenClaw 加载的精简技能说明（保持短小以降低加载成本） |
| `config.json` | 静态 OSS 参数（`staticOSS`：`endPoint`、`bucket`、`host`、`bindHost`、`uploadDir`、`base64Table`、`expireTime`、`objectLifecycleExpireDays`、`lifecycleRuleId` 等），**不含** AccessKey；脚本启动时会合并进环境（已有环境变量优先） |
| `config.example.env` | 必填密钥说明与可选变量注释 |
| `.env` | 可选：与 `config.example.env` 同键名；脚本启动时会自动加载（**已存在的环境变量不被覆盖**） |

## 路径与公开 URL

默认对象键为 **`{uploadDir}/YYYY/MM/{毫秒时间戳}_{安全文件名}.ext`**（按本机本地时区的年/月分目录；设 `KEPLERJAI_OSS_PATH_UTC=1` 时改为 UTC 年/月）。公开访问地址为 **`bindHost` + `/` + 对象键**（例如 `bindHost` 为 `https://cdn.example.com` 且 CDN 回源到该 bucket 时，即对外访问域名）。

## 安全（必读）

- **AccessKey 不得写入仓库、不得贴进 SKILL 或聊天**。仅通过环境变量或 OpenClaw `skills.entries` 的 `env` / SecretRef 注入（见官方 [Skills 文档](https://docs.openclaw.ai/tools/skills) 的 Environment injection）。
- 若密钥曾出现在聊天或日志中，请在阿里云 **立即轮换** AccessKey。

## 环境变量

复制 `config.example.env` 为本地 `.env`（已 gitignore），或在 OpenClaw 中配置同名变量：

| 变量 | 说明 |
|------|------|
| `KEPLERJAI_OSS_ACCESS_KEY_ID` | 阿里云 AccessKey ID（必填） |
| `KEPLERJAI_OSS_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret（必填） |
| `KEPLERJAI_OSS_ENDPOINT` | 如 `oss-cn-chengdu.aliyuncs.com`（无 `https://` 前缀） |
| `KEPLERJAI_OSS_BUCKET` | 如 `static-szxg` |
| `KEPLERJAI_OSS_HOST` | 可选；OSS 访问域名，如 `https://{bucket}.{endpoint}`；可由 `config.json` 的 `host` 注入 |
| `KEPLERJAI_OSS_UPLOAD_DIR` | 对象前缀目录，默认 `upload` |
| `KEPLERJAI_OSS_BIND_HOST` | 公开访问根，如 `https://cdn.example.com`（无末尾 `/`） |
| `KEPLERJAI_OSS_EXPIRE_TIME_MS` | 可选；与 `config.json` 的 `expireTime` 对齐（Post policy 等场景） |
| `KEPLERJAI_OSS_NAME_ALPHABET` | 可选；仅 `--flat` 模式：随机文件名字符表 |
| `KEPLERJAI_OSS_PATH_UTC` | 可选；`1`/`true` 时年/月按 UTC；默认本地时区 |
| `KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS` | 可选；与 `config.json` 的 `objectLifecycleExpireDays` 一致；用于 **PutBucketLifecycle**（脚本写入）时的过期天数 |
| `KEPLERJAI_OSS_LIFECYCLE_RULE_ID` | 可选；与 `config.json` 的 `lifecycleRuleId` 一致；合并写入时按该 ID **覆盖**同 ID 规则，其它规则保留 |
| `KEPLERJAI_OSS_SYNC_LIFECYCLE_ON_UPLOAD` | 可选；`1`/`true` 时，上传成功后自动调用 PutBucketLifecycle（与 `--sync-lifecycle` 等价） |
| `KEPLERJAI_OSS_CONFIG` | 可选；指向替代 `config.json` 的 JSON 文件路径 |

说明：`expireTime` 等多用于 **服务端直传/回调** 流程；本仓库脚本为 **服务端脚本直传**（AccessKey 仅在受控环境使用），脚本不实现 OSS 回调 HTTP 服务。

### 对象按「最后修改时间」过期删除（生命周期）

与阿里云 [生命周期规则](https://help.aliyun.com/zh/oss/user-guide/overview-13) 一致：对前缀 `{uploadDir}/` 配置 **Expiration.Days**，满 N 天后删除对象。实现方式：

1. **独立脚本**（推荐运维一次性执行）：`scripts/put_bucket_lifecycle.py` 内部使用 **oss2** `get_bucket_lifecycle` + `put_bucket_lifecycle`，按 `lifecycleRuleId` 与现有规则 **合并**（同 ID 覆盖）。需 RAM 策略包含 `oss:GetBucketLifecycle`、`oss:PutBucketLifecycle` 等。
2. **随上传写入**：`upload_to_oss.py` 加 `--sync-lifecycle`，或设置环境变量 `KEPLERJAI_OSS_SYNC_LIFECYCLE_ON_UPLOAD=1`（仍要求已配置 `objectLifecycleExpireDays` / `KEPLERJAI_OSS_OBJECT_LIFECYCLE_DAYS`）。

```bash
python scripts/put_bucket_lifecycle.py --dry-run
python scripts/put_bucket_lifecycle.py
```

若未执行上述脚本且未开 `--sync-lifecycle`，上传成功后仍会在 **stderr** 提示可如何写入生命周期。

## 依赖

在仓库根目录执行：

```bash
pip install -r requirements.txt
```

## 用法

上传（默认路径示例：`upload/2026/04/1712738400123_my-photo.png`，并打印 `public_url`）：

```bash
python scripts/upload_to_oss.py "/path/to/local/file.png"
```

仍使用「`upload/` + 随机文件名」扁平路径时加 `--flat`：

```bash
python scripts/upload_to_oss.py "/path/to/local/file.png" --flat
```

指定对象键（位于 bucket 内路径，不要前导 `/`）：

```bash
python scripts/upload_to_oss.py "/path/to/file.png" -k "upload/branding/logo.png"
```

仅查看将使用的 key 与 URL（不实际上传）：

```bash
python scripts/upload_to_oss.py "/path/to/file.png" --dry-run
```

上传并 **同步写入** bucket 生命周期（前缀 `uploadDir/`，天数来自 config / 环境变量）：

```bash
python scripts/upload_to_oss.py "/path/to/file.png" --sync-lifecycle
```

## Agent 行为指引

1. 确认用户已配置上述环境变量（或 OpenClaw `skills.entries["keplerjai-oss-uploader"].env`），**不要把密钥写进对话或 SKILL 正文**。
2. 需要上传时：在 shell 中设置好 env 后执行脚本；上传成功后把输出的 `public_url` 回传给用户。
3. 若用户要求固定路径，使用 `-k`；默认使用「年/月/时间戳_文件名」；若用户明确要求扁平随机名，加 `--flat`。
4. 若用户要在 OSS 侧自动过期删除：在确认 AccessKey 具备生命周期权限后，执行 `put_bucket_lifecycle.py` 或上传时加 `--sync-lifecycle`；**勿**在对话中暴露密钥。

## OpenClaw `openclaw.json` 示例（片段）

将 `env` 指向本机已导出变量或使用 SecretRef，勿明文长期保存 Secret：

```json
{
  "skills": {
    "entries": {
      "keplerjai-oss-uploader": {
        "enabled": true,
        "env": {
          "KEPLERJAI_OSS_ACCESS_KEY_ID": {
            "source": "env",
            "provider": "default",
            "id": "KEPLERJAI_OSS_ACCESS_KEY_ID"
          },
          "KEPLERJAI_OSS_ACCESS_KEY_SECRET": {
            "source": "env",
            "provider": "default",
            "id": "KEPLERJAI_OSS_ACCESS_KEY_SECRET"
          },
          "KEPLERJAI_OSS_ENDPOINT": "oss-cn-chengdu.aliyuncs.com",
          "KEPLERJAI_OSS_BUCKET": "static-szxg",
          "KEPLERJAI_OSS_HOST": "https://static-szxg.oss-cn-chengdu.aliyuncs.com",
          "KEPLERJAI_OSS_UPLOAD_DIR": "upload",
          "KEPLERJAI_OSS_BIND_HOST": "https://cdn.example.com"
        }
      }
    }
  }
}
```

（具体 SecretRef 写法以你本机 [Skills config](https://docs.openclaw.ai/tools/skills-config) 为准。）
