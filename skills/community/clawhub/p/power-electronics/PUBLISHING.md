# 发布到 ClawHub（OpenClaw 技能市场）

本 Skill 发布名建议：`power-electronics`（与 `SKILL.md` 中 `name` 一致）。

公开页 URL 格式：**https://clawhub.ai/\<你的用户名\>/power-electronics**

---

## 一、发布前检查

- [ ] 文件夹根目录有 `SKILL.md`，含 `name` 和 `description`
- [ ] `name` 仅小写字母、数字、连字符（与目录名一致最佳）
- [ ] `scripts/` 无恶意代码（ClawHub 会安全扫描）
- [ ] 版本号在 frontmatter 的 `version` 字段（如 `1.3.0`）
- [ ] 本地测试脚本能运行：`python scripts/power_calc.py --help`

---

## 二、安装 ClawHub CLI

```bash
npm i -g clawhub
# 或
pnpm add -g clawhub
```

验证：

```bash
clawhub --help
```

---

## 三、登录 ClawHub

```bash
clawhub login
```

浏览器完成 GitHub 授权。无头环境可用：

```bash
clawhub login --device
```

查看当前账号：

```bash
clawhub whoami
```

**注意**：ClawHub 要求 GitHub 账号达到一定「账龄」才能上传（防 spam）。

---

## 四、发布单个 Skill（推荐首次）

在 Skill **父目录**执行（路径按你本机修改）：

```bash
cd "E:\0WorkNew\OpenClaw小龙虾\Skills\电力电子技术"

clawhub skill publish . \
  --slug power-electronics \
  --name "Power Electronics 电力电子" \
  --version 1.3.0 \
  --changelog "四大变换 + PFC/Flyback/LLC/QR/NPC + Simulink 模板"
```

常用选项：

| 选项 | 说明 |
|------|------|
| `--slug` | 公开 URL 中的技能名 |
| `--name` | 展示名称 |
| `--version` |  semver，首次可 1.0.0 |
| `--changelog` | 更新说明 |
| `--owner <org>` | 发布到组织（需权限） |

**预览（不上传）**：部分版本支持 `--dry-run`，以 CLI 帮助为准。

后续更新：修改文件后再次 `publish`，ClawHub 会自动递增 patch 版本（也可显式 `--version`）。

---

## 五、批量 sync（维护多个 Skill 时）

若技能放在统一目录 `skills/` 下：

```bash
clawhub sync --dry-run --all
clawhub sync --all
```

`sync` 会扫描含 `SKILL.md` 的子文件夹，只上传有变更的技能。

---

## 六、用户如何安装你的 Skill

他人安装（OpenClaw 侧）：

```bash
openclaw skills install @你的用户名/power-electronics
```

或 ClawHub 网站浏览后一键安装。

---

## 七、OpenClaw 本地 vs ClawHub

| 方式 | 路径 | 适用 |
|------|------|------|
| 本地 workspace | `%USERPROFILE%\.openclaw\workspace\skills\` | 自己开发调试 |
| ClawHub 安装 | 由 OpenClaw 下载到 workspace | 分享给别人 |
| 全局 managed | `%USERPROFILE%\.openclaw\skills\` | `--global` 安装 |

**发布到 ClawHub 不等于自动替换本地文件夹**；发布后他人通过 `@owner/slug` 安装。

---

## 八、GitHub Actions 自动发布（可选）

在 GitHub 仓库配置 secret `CLAWHUB_TOKEN`：

```bash
clawhub login --label "GitHub Actions"
gh secret set CLAWHUB_TOKEN --body "$(clawhub token)"
```

使用官方 workflow：`openclaw/clawhub/.github/workflows/skill-publish.yml`

详见：[OpenClaw Publishing 文档](https://docs.openclaw.ai/clawhub/publishing)

---

## 九、安全与审核

- ClawHub 对上传 Skill 做 VirusTotal / 静态扫描
- 安装前用户可查看 `SKILL.md` 和 `scripts/` 源码
- 本 Skill 仅调用 Python 标准库，无网络请求，便于审核

---

## 十、推荐发布流程（一步步）

```bash
# 1. 登录
clawhub login

# 2. 进入 skill 目录
cd "E:\0WorkNew\OpenClaw小龙虾\Skills\电力电子技术"

# 3. 本地验证
python scripts/power_calc.py --transform dc-dc --topology buck --vin 48 --vo 12 --io 5

# 4. 发布
clawhub skill publish . --slug power-electronics --name "Power Electronics 电力电子" --version 1.3.0 --changelog "Initial public release"

# 5. 打开页面确认
# https://clawhub.ai/<你的用户名>/power-electronics
```

官方文档：
- [ClawHub 概览](https://docs.openclaw.ai/clawhub/)
- [Publishing 发布指南](https://docs.openclaw.ai/clawhub/publishing)
