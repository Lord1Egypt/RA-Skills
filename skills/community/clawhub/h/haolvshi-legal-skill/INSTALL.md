# 好律狮法律技能包安装说明

## 环境要求

- 人工智能工具支持 Agent Skills 或兼容的 `SKILL.md` 技能目录。
- 支持执行 shell 或 PowerShell、访问网络以及读写临时文件。
- 无需预装 Node.js；技能首次运行时会自动检查，缺少或版本过低时自动安装技能专用运行环境。

## 让人工智能助手安装

可以直接向支持技能安装的人工智能助手发送：

```text
请根据 https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/INSTALL.md
帮我安装“好律狮法律技能包”。
```

或者：

```text
请根据安装文档安装 @haolvshi-legal-skill。
```

## 命令行安装

```bash
npx skills add https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip --skill haolvshi-legal-skill
```

需要安装到指定人工智能工具时，按照 `skills` 命令显示的目标列表选择对应工具。

## 直接导入

从以下地址下载 zip 压缩包，在人工智能工具的技能管理页面中导入：

- `https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip`

WorkBuddy 导入时会读取技能根目录的 `_icon.png` 作为技能图标。本技能包已内置该文件，请保持它与 `SKILL.md` 位于同一层级，不要只复制 `assets/` 目录。

## 验证安装

进入技能目录后，macOS 或 Linux 执行：

```bash
sh scripts/bootstrap.sh --ensure
sh scripts/run.sh health
```

Windows 执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1 -Ensure
powershell -ExecutionPolicy Bypass -File scripts/run.ps1 health
```

返回 `ok=true` 且五项能力状态为 `true`，说明网络和基础配置正常。

然后可以测试：

```text
发生交通事故，帮我计算一下可以获得多少赔偿。
```

人工智能应调用“好律狮法律技能包”并展示“交通事故赔偿”计算项目。

## 可选配置

技能已经内置生产环境地址。部署测试环境时可以设置：

| 环境变量 | 用途 |
|---|---|
| `HAOLVSHI_API_BASE` | 接口根地址 |
| `HAOLVSHI_SITE_BASE` | 在线应用站点地址 |
| `HAOLVSHI_SITE_ROUTE_BASE` | 在线报告前端路由根路径，默认为空 |
| `HAOLVSHI_APP_ID` | 站点应用编号 |
| `HAOLVSHI_DEVICE_TYPE` | 设备类型 |
| `HAOLVSHI_STATE_DIR` | 本地临时任务目录 |
| `HAOLVSHI_REQUEST_TIMEOUT_MS` | 普通接口超时时间 |
| `HAOLVSHI_AUDIT_TIMEOUT_MS` | 合同审核超时时间 |

旧版 `LVPIN_*` 环境变量仍可兼容读取，建议新部署统一使用 `HAOLVSHI_*`。

客户端配置中不要放置服务端工作流密钥。

## 更新和卸载

通过原安装方式重新安装可以更新技能。卸载前可以执行：

```bash
sh scripts/run.sh cleanup
```

清理过期任务材料后，再从人工智能工具的技能目录中删除本技能。
