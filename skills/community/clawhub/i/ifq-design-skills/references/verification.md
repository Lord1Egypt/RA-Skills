# Verification：证据优先的输出验证流程

IFQ 的验证不是“随手看一眼没问题就算完”，而是**先定义什么算完成，再收集对应证据**。

一些 design-agent 原生环境（如 Claude.ai Artifacts、Codex App browser、OpenClaw browser plugin）有内置验证器。ClawHub-safe bundle 不内置 Playwright/Python/ffmpeg；这些属于完整 GitHub repo 的增强工具。默认先用宿主浏览器/截图能力，只有在完整 repo 和依赖都存在时才跑脚本化检查。

核心原则：

- 能截图就截图；不能截图时至少记录已用哪种宿主预览/静态检查
- 有交互就点主路径；没有交互时说明是静态交付
- 没有导出核对，不算已经导出
- 没有控制台检查，不要声称“零运行错误”

## 验证清单

每次产出 HTML 后，至少走一遍这套 evidence contract：

### 1. 浏览器渲染检查（必做）

最基础：**HTML能不能打开**？在macOS上：

```bash
open -a "Google Chrome" "/path/to/your/design.html"
```

或者用宿主浏览器截图。完整 GitHub repo 环境可用 Playwright 脚本截图（下一节）。

### 2. 控制台错误检查

HTML文件里最常见的问题是JS报错导致白屏。优先使用宿主浏览器的 console / network 面板。完整 GitHub repo 中如果存在 `scripts/verify.py`，再用 Playwright 跑一遍：

```bash
python <full-repo>/scripts/verify.py path/to/design.html
```

这个脚本会：
1. 用headless chromium打开HTML
2. 截图保存到项目目录
3. 抓取控制台错误
4. 报告status

ClawHub-safe bundle 没有这个 Python 脚本；不要在 ClawHub-only 环境里承诺它可运行。

### 3. 多视口检查

如果是响应式设计，抓多个 viewport。没有 Playwright 时，用宿主浏览器的设备模拟或手动 resize；完整 repo 可跑：

```bash
python verify.py design.html --viewports 1920x1080,1440x900,768x1024,375x667
```

### 4. 交互检查

Tweaks、动画、按钮切换——默认的静态截图看不到。**建议在宿主浏览器里点一遍主路径**。完整 repo 可用 Playwright 录屏：

```python
page.video.record('interaction.mp4')
```

### 5. 幻灯片逐页检查

Deck 类 HTML，一张张截；完整 repo 可用：

```bash
python verify.py deck.html --slides 10  # 截前10张
```

生成 `deck-slide-01.png`、`deck-slide-02.png`... 方便快速浏览。

## 验证层级

| 层级 | 环境 | 能证明什么 |
|---|---|---|
| Tier 0 | ClawHub-safe bundle + `npm run validate` | Skill 包健康：模板、manifest、安全、字体协议、脚本 deny-list |
| Tier 1 | 宿主浏览器/截图工具 | 单件 HTML 能打开、首屏可见、主交互可点、响应式不崩 |
| Tier 2 | 完整 GitHub repo + Playwright/ffmpeg/PDF/PPTX 依赖 | 控制台捕获、多 viewport 截图、视频/PDF/PPTX 衍生文件核对 |

## Playwright Setup（完整 GitHub repo）

首次使用需要：

```bash
# 如果还没装
npm install -g playwright
npx playwright install chromium

# 或者Python版
pip install playwright
playwright install chromium
```

如果用户已经全局安装 Playwright，直接用即可。不要在 ClawHub-safe bundle 里新增依赖或安装 hook。

## 截图最佳实践

### 截完整页面

```python
page.screenshot(path='full.png', full_page=True)
```

### 截viewport

```python
page.screenshot(path='viewport.png')  # 默认只截可见区域
```

### 截特定元素

```python
element = page.query_selector('.hero-section')
element.screenshot(path='hero.png')
```

### 高清截图

```python
page = browser.new_page(device_scale_factor=2)  # retina
```

### 等动画结束再截

```python
page.wait_for_timeout(2000)  # 等2秒让动画settle
page.screenshot(...)
```

## 把截图发给用户

### 本地截图直接打开

```bash
open screenshot.png
```

用户会在自己的 Preview/Figma/VSCode/浏览器 里看。

### 分享给远程协作者

如果需要给远程协作者看（比如 Slack/飞书/微信），使用当前宿主 agent 已授权的附件、MCP、对象存储或图床工具。不要假设用户本机存在某个私人脚本或上传账号。

## 验证出错时

### 页面白屏

控制台一定有错。先检查：

1. React+Babel script tag的integrity hash对不对（见`react-setup.md`）
2. 是不是`const styles = {...}`命名冲突
3. 跨文件的组件有没有export到`window`
4. JSX语法错误（babel.min.js不报错，换babel.js非压缩版）

### 动画卡

- 用Chrome DevTools Performance tab录一段
- 找layout thrashing（频繁的reflow）
- 动效优先用`transform`和`opacity`（GPU加速）

### 字体不对

- 检查`@font-face`的url是否可访问
- 检查fallback字体
- 中文字体加载慢：先显示fallback，加载完再切换

### 布局错位

- 检查`box-sizing: border-box`是否全局应用
- 检查`*  margin: 0; padding: 0`reset
- Chrome DevTools里打开gridlines看实际布局

## 验证=设计师的第二双眼

**永远要自己过一遍**。AI写代码时经常出现：

- 看起来对但interaction有bug
- 静态截图好但scroll时错位
- 宽屏好看但窄屏崩
- Dark mode忘了测
- Tweaks切换后某些组件没响应

**最后1分钟的验证可以省1小时的返工**。

## 常用验证脚本命令（完整 GitHub repo）

```bash
# 基础：打开+截图+抓错
python verify.py design.html

# 多viewport
python verify.py design.html --viewports 1920x1080,375x667

# 多slide
python verify.py deck.html --slides 10

# 输出到指定目录
python verify.py design.html --output ./screenshots/

# headless=false，打开真实浏览器给你看
python verify.py design.html --show
```
