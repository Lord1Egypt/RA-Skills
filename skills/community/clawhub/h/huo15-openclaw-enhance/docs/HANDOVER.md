# HANDOVER — 龙虾增强包接手指南

> 读完 [CLAUDE.md](../CLAUDE.md) 再读这里即可接手。本文件只放**可移交**的项目知识；凭据明文不入库（只指路）。

## 1. 环境与依赖

| 项 | 要求 |
|---|---|
| Node | ≥ 18（开发实测 nvm v25.x） |
| 包管理 | npm（仓库带 package-lock.json） |
| openclaw | **peerDependency** `^2026.4.24`；本地开发另装 `npm i openclaw@latest --no-save` |
| 原生模块 | `better-sqlite3`（需编译；缺失时插件进 DB 降级模式不崩） |

```bash
git clone https://cnb.cool/huo15/ai/huo15-openclaw-enhance
npm install && npm i openclaw@latest --no-save
npx tsc --noEmit       # 应 exit 0
npm run build
```

## 2. 远端与凭据（不写明文，只指路）

- **origin**（cnb.cool 主）：URL 内置 token，`git push origin` 即用。
- **github**（镜像）：`git@github-zhaobod1:zhaobod1/huo15-openclaw-enhance.git`，走 SSH 别名 `github-zhaobod1`（`~/.ssh/config` 已配）。
- 发版常态：**双 remote 同步** `git push origin main && git push github main`（tag 同理）。
- npm / ClawHub / cnb token：见**主目录 `~/CLAUDE.md` §2**（账号私有）。换账号接手向负责人（job zhao / zhaobod1@163.com）索取。

## 3. 发布 SOP（完整）

```bash
# 0. 跨会话先对账（见 §5）
# 1. package.json：version bump；build.openclawVersion 改目标 runtime
#    ⚠️ compat.pluginApi(>=X) / peerDependencies.openclaw(^X) 保持 ranged，不要拔成精确版本
# 2. CHANGELOG.md 顶部加新版条目
npx tsc --noEmit                 # 必过
rm -rf dist && npm run build     # 删旧 dist 防残留（删过的模块产物会留在 dist）
git add -A
git commit -m "vX.Y.Z: ..."
git tag vX.Y.Z
git push origin main && git push github main
git push origin vX.Y.Z && git push github vX.Y.Z
npm publish
CLAWHUB_TOKEN=<token> clawhub publish "$(pwd)" --version X.Y.Z   # plugin 双发布，绝对路径
openclaw plugins install "$(pwd)"   # 装到本地
```

## 4. 当前状态（滚动更新）

- 版本：**v6.7.19**（去 model-router + 分享链接预览 + 适配 2026.6.10）。
- ⚠️ **历史校正**：v6.7.17 / v6.7.18 有 git 提交但**从未发过 npm**（npm 此前 latest = 6.7.16）。v6.7.19 发布会让 npm 直接 6.7.16 → 6.7.19，其代码已含 17/18。
- node_modules/openclaw 本地已升到 2026.6.10。

## 5. 跨会话开工对账 checklist（必跑）

```bash
git fetch origin
git log --oneline HEAD..origin/main   # 远端有本地没的
git log --oneline origin/main..HEAD   # 本地有远端没的
git status -uno
npm view @huo15/huo15-openclaw-enhance version   # npm latest（注意可能落后于 git）
grep -E '"version"' package.json; head -5 CHANGELOG.md
```

**最强信号**：`package.json.version` 已 bump 但 CHANGELOG 顶部不是该版本 / npm latest 落后于本地 git → 几乎一定是「做了一半被打断」，先补完再做新事。

> 工具回执故障期的特别警示：曾有会话在 harness 故障期「完成」了发布/文档/memory，事后核对 git/npm/磁盘发现**全没落盘**。故障期不要相信工具回执，恢复后必须 ground-truth 重新对账。

## 6. 待办 / 后续方向

- [ ] v6.7.19 的 clawhub 双发布（若发布时未做）
- [ ] README 功能模块表是「v5.6.0 全量」标注，已略过时，可择机重整
- [ ] 模块 tier 标注集中化（目前分散在各 register 处）

## 7. 关键文档索引

- [CLAUDE.md](../CLAUDE.md) — 接手第一入口、开发铁律
- [architecture.md](architecture.md) — 架构 / 36 模块清单 / 数据流
- [PRD.md](PRD.md) — 产品需求 / 非目标边界
- [decisions/](decisions/) — ADR（为什么非侵入、为什么去 model-router）
- [lessons/](lessons/) — 踩坑复盘（SDK 2026.6 TS2742 / 工具故障 fabricated 警示）
- [SELF_ITERATE.md](SELF_ITERATE.md) — 自我迭代 SOP
