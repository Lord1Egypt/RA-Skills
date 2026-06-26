# Smoke Test · IFQ Design Skills

一页说明：**如何快速验证 ClawHub-safe bundle 安装完整、脚本可读、安全面干净**。不是完整设计 QA，是 60 秒内跑完、任何发布级破损都能暴露的最小回归入口。

## 一行启动

```bash
# 在 ifq-design-skills 仓库根目录下
npm run validate
```

这个命令会顺序验证：

1. **模板索引一致性** — `assets/templates/INDEX.json` 里每一条 `file` 在磁盘上真实存在
2. **品牌资产齐备** — `assets/ifq-brand/logo.svg`、`logo-white.svg`、`mark.svg`、`icons/hand-drawn-icons.svg`、`ifq_brand.jsx` 全在
3. **手绘图标 sprite 可解析** — `hand-drawn-icons.svg` 的 `<symbol id="...">` 至少 24 条
4. **References 路由目标存在** — SKILL.md 里每个 `references/*.md` 指向都真实存在
5. **SKILL disclosure budget** — 根 `SKILL.md` 保持 500 行内，`metadata` 保持单行 JSON，并声明 First-Run Success Path
6. **关键脚本健康** — `scripts/*.mjs / *.js` 必须是文本、非空、结构正常
7. **authored 年份渲染** — IFQ authored stamp 必须渲染为真实年份，不能残留 `field note / 2026` 或年份占位符
8. **ClawHub manifest** — `clawhub.json` 与 `SKILL.md` 版本一致，summary / tags / docs / triggers / tool_map / quick commands 可解析
9. **Marketplace onboarding** — manifest 必须包含 marketplace 定位、first-run prompts、success evidence 和可检查 demo artifacts
10. **OpenClaw loader gates** — `metadata.openclaw.os`、`requires.bins/env/config`、plugins 与 workspace 权限声明必须和 manifest 对齐
11. **package 安全** — zero dependencies，zero install-time lifecycle hooks
12. **ClawHub cleanliness** — ignore manifest 排除 VCS、agent-local state、`.env`、`.well-known/`、个人资产索引和构建产物；若 manifest 声明 `contains_binary=false`，仓库内容不得含二进制资产
13. **script safety** — `scripts/script-safety-rules.json` deny-list 覆盖动态执行、进程创建和脚本侧外联原语
14. **secret hygiene** — deny-list 覆盖常见令牌、PAT、云访问标识和私钥块
15. **font loading** — Google Fonts 只能是 Tier B 非阻塞 + noscript fallback
16. **template runtime** — 默认可 fork 模板不依赖远程 JS/CSS runtime（Google Fonts 除外）
17. **remote runtime pinning** — HTML 资产里的远程 runtime 不能用 floating `@latest`
18. **eval suite** — 12 个模式都有回归场景、agent contract、路由 requiredReferences、preview/verify 命令和质量红线

退出码：`0` 成功 · `1` 失败（会打印第一条失败详情）。

当前仓库的最小 smoke 仅依赖 Node，无需 `npm install`，也不会触发网络访问。高敏感检测词放在 `scripts/script-safety-rules.json`，避免平台把自检代码误判成“读文件后外发”。

## 三种任务的最小验证剧本

如果你要验证**设计交付链**而不是只验证发布包，按下面的最小任务跑一次。ClawHub-safe bundle 负责 HTML 和协议；Playwright / ffmpeg / PDF / PPTX 自动化只在完整 GitHub 仓库中使用。

### ① 原型任务最小验证

```
任务：给 iPhone 15 Pro 做一个「相机 App 拍照瞬间」的高保真原型，1 屏即可。
验收：
- 使用 Starter Components 里的 AppPhone 状态管理器
- 图片素材必须来自 Wikimedia / Met / Unsplash，不能用纯色占位
- 交付前跑 Playwright 点击测试，至少 1 个可点击交互
```

预期耗时 3–5 分钟；失败通常意味着：占位图没替换 / AppPhone 没包 / 宿主 agent 没有浏览器截图能力。

### ② 动画任务最小验证

```
任务：5 秒 logo 起幕动画，1920×1080。ClawHub-safe bundle 交付 HTML motion source + 导出计划；完整 GitHub repo 再导出 MP4/GIF。
验收：
- 使用动画引擎（keyframe-based，非 CSS transition 堆叠）
- 导出后 gif ≤ 2 MB，palette 优化开启
- mp4 自动附加 BGM + fade in/out
```

预期耗时 6–10 分钟；MP4/GIF 导出请切到完整 GitHub repo。失败通常意味着：ffmpeg 没装 / Playwright 没装 chromium / BGM 文件缺失。

### ③ Deck 导出最小验证

```
任务：3 页 keynote HTML deck（封面 + 1 内容页 + 封底），同时导出 PDF 与 PPTX。
验收：
- 使用 slide-title.html 模板 + 两个自定义页
- PDF 文件 > 0 字节，页数 = 3
- PPTX 在 Keynote / PowerPoint 打开文字仍可编辑
```

预期耗时 4–8 分钟；PDF/PPTX 导出请切到完整 GitHub repo。失败通常意味着：`pptxgenjs` 或 `pdf-lib` 没装 / chromium 没装 / 字体加载失败。

## 依赖矩阵速查

ClawHub-safe bundle:

| 命令 | 依赖 |
|------|------|
| `npm run validate` | Node ≥ 18.17 |
| `npm run pack` | Node ≥ 18.17 |

完整 GitHub repo 的导出辅助：

| 脚本 | Node deps | Python deps | System |
|------|-----------|-------------|--------|
| `scripts/verify.py` | — | `playwright` | chromium |
| `scripts/render-video.js` | `playwright`, `sharp` | — | `ffmpeg`, chromium |
| `scripts/export_deck_pdf.mjs` | `playwright`, `pdf-lib` | — | chromium |
| `scripts/export_deck_pptx.mjs` | `playwright`, `pptxgenjs`, `sharp` | — | chromium |
| `scripts/export_deck_stage_pdf.mjs` | `playwright`, `pdf-lib` | — | chromium |
| `scripts/html2pptx.js` | `pptxgenjs`, `sharp` | — | — |

> **仅在需要导出时安装**：
> ```
> npm install            # full repo Node deps
> npx playwright install chromium
> pip install -r requirements.txt   # 仅当你要跑 verify.py
> brew install ffmpeg    # macOS；Debian/Ubuntu 用 apt install ffmpeg
> ```

## 失败排查清单

- `Error: browserType.launch: Executable doesn't exist` → `npx playwright install chromium`
- `ffmpeg: command not found` → `brew install ffmpeg`（macOS）/ `apt install ffmpeg`（Linux）
- `Cannot find module 'playwright'` → `npm install`
- `ModuleNotFoundError: No module named 'playwright'` → `pip install -r requirements.txt`
- INDEX.json 指向不存在文件 → 先运行 `npm run validate` 看第一条失败，再修或删索引
