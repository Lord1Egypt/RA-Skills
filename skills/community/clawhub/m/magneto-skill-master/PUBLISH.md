# 上架指引（GitHub + ClawHub / WorkBuddy 技能市场）

本目录已是一份可发布的 WorkBuddy 技能。下面两步即可开源上架。

## 第一步：推到 GitHub（公开仓库）

仓库名建议：`magneto-skill-master`（已与本技能 Slug 一致，兼容市场校验）。

- 在 https://github.com/new 新建 **Public** 仓库 `magneto-skill-master`（可不初始化 README）。
- 然后在本机执行（需要你自己的 GitHub 令牌 / `gh` 登录）：

```bash
cd <本目录>
git init -q
git add -A
git commit -q -m "feat: 万磁王技能万事通 v1.0.0"
git branch -M main
git remote add origin https://github.com/yehuzi2026/magneto-skill-master.git
git push -u origin main
```

> 若你已授权 WorkBuddy 的 GitHub 连接器具备建仓库权限，也可让 WorkBuddy 直接建仓库并推送。

## 第二步：发布到 ClawHub（WorkBuddy 官方技能市场）

1. 打开 https://clawhub.ai/ ，用 **GitHub 账号登录**。
2. 点击「发布技能 / Publish Skill」。
3. 选择「通过 GitHub 仓库导入」，填入：
   `https://github.com/yehuzi2026/magneto-skill-master`
   （或上传本目录打成的 `magneto-skill-master.zip`）
4. 填写信息：
   - 名称：万磁王技能万事通
   - 描述：（同 SKILL.md description）
   - 版本：v1.0.0
   - 标签：技能安装、标书、招投标、自动化、WorkBuddy
5. 提交审核（通常 1–3 个工作日）。审核通过后即出现在 ClawHub，其他用户可一键安装。

## 备注

- 市场要求 Slug 小写且 URL 安全，故开源版 `name` 用 `magneto-skill-master`；你本机的中文触发名 `万磁王技能万事通` 保持不变（仅本地生效）。
- 本技能路径已改为可移植写法（基于 `$HOME` + `cygpath`），其他用户克隆即可用。
