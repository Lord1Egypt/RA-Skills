# 演读 DECK · 换肤 = token-flip（不是重做）

给**已有 deck** 换主色时用这套。核心认知：两套主色的 `:root` **逐行结构完全一致、只有值不同**——所以换肤是一次**机械的 token 值映射**，引擎 CSS/JS 一字不动，内容一字不动。别重写、别让 subagent "参照着做一版"。

> 当前口径见 SKILL.md 第1.4节：**米白 = 全站默认**，国标走 V6 焰彩白，**暖黑/焰彩黑是存量历史态**——本文档现在主要服务于「存量黑版 → 米白」的收敛。
>
> 现成脚本：**`scripts/flip-暖黑到米白.py`**（映射抽自引擎模板 · 单遍替换 · 内建未覆盖色守卫 · 先读后写）。用法 `python3 scripts/flip-暖黑到米白.py <deck.html>...`；退出码 2 = 有未覆盖色，按 第2.6节 人工判断后再跑。

## 0. 动手前（这五步省过一次 9 期全毁）

1. **先查 git 有没有现成的目标态**——见 第0.5节，能取回就别转换。
2. **先 cp 备份**要改的文件。
3. flip 脚本**必须先读后写**（见 第3节 第 1 条，这是最贵的坑）。
4. flip 后 `stat -f%z` 查**每个文件大小非 0**。
5. flip 后跑**全谱残留 grep**（第2节），**=0 才算过**。

## 0.5 先问一句：git 里是不是躺着现成的？⭐ 省一整轮

演读 DECK 的 deck HTML **都在 git 里**（只有 `演读DECK/publish.py` 被 `.gitignore` 的 `*.py` 排除）。整站换过肤，就意味着**换肤前的版本还在历史里**。要换回某个旧主色时，先查：

```bash
git log --oneline --all -- <deck路径>                    # 哪次提交换的肤
git show <flip提交>^:<deck路径> | grep -oE -- '--bg:#[0-9a-f]*'   # 换肤前是什么色
git log --oneline <flip提交>..HEAD -- <deck路径>          # 换肤后还改过内容吗（0 = 可安全取回）
```

**换肤后 0 次提交 = 直接 `git show <flip提交>^:<路径>` 取回，精确、零转换风险**，比任何 flip 脚本都可靠。
2026-07-15 实战：偷师 4 期换肤前本就是米白、之后 0 改动 → 直接取回，全谱残留 grep=0 一次过；而算力 5 期换肤前是**暖黑**（不是米白），取回只能拿到暖黑，仍需一轮真转换。**先查再动，别默认要写脚本。**

## 0.6 ⚠️ 跨设计系统 ≠ 换肤，别硬套

本文档的 flip 只适用于**同一套设计系统的明暗两极**（V6焰彩白↔V6焰彩黑、暖黑↔米白——后两者同为 V2 黏土系统）。

**焰彩黑 → 米白 是跨系统**：主色紫 `#a855f7` vs 黏土 `#c15f3c`、字体 Mozilla VF vs Anthropic Sans，V6 的焰橙/焰粉在 V2 里根本没有对应色。硬套 token-flip 会出四不像。跨系统要走「先 git 取回同系统版本，再同系统 flip」，或老老实实重做。

## 1. 已验证的映射

### 1.1 V6 焰彩：白 ↔ 黑（两向互为精确逆运算）

| 语义 | 焰彩白 | 焰彩黑 |
|---|---|---|
| 底 | `#fbfaff` | `#170a30` |
| surface | `#ffffff` / `#f4eefc` / `#efe7fb` | `#241246` / `#231044` / `#2c1552` |
| 正文字 | `#1c0b3e` | `#f3eefe` |
| 主紫 | `#7c3aed` | `#a855f7` |
| 次紫 | `#6d28d9` | `#c084fc` |
| 蓝 | `#4f6ef0` | `#7c9bff` |
| 金 | `#c8620a` / `#e07a1a` | `#ffb454` / `#f0a13a` |
| warn | `#e0304f` | `#ff5c78` |
| 线 | `rgba(28,11,62,…` | `rgba(255,255,255,…` |
| 紫辉光 | `rgba(124,58,237,…` | `rgba(168,85,247,…` |
| grain | `multiply` `.02` | `screen` `.05` |
| body class | `class="light"` | `class="dark"` |

**黑白通用、不翻**：焰橙 `#ff8a3d`、焰粉 `#ff4f8b`、`--ok`、`--teal`。
**演示版与首页的 token 值不同，各写一份映射**，别共用一张表。

### 1.2 暖黑 / 米白（旧两套）

暖黑 `#161514` + 黏土 `#e08a5f` + 石板蓝 `#8fa6bd`；米白 `#faf9f5` + 黏土 `#c15f3c`。
亮底适配：网格线→极淡深色、卡片靠 `--shadow` 不靠辉光、幽灵号深色 `opacity:.05`、`.grain`→`multiply`。

## 2. 三条验收（缺一条都不算换完）

1. **全谱残留 grep = 0**：拿**旧主色整套调色板**（不只是 `--bg`）去 grep，包括 SVG 内联色。半成品最爱漏的就是图表里的 `#e08a5f`（暖黑黏土）、`#8fa6bd`（石板蓝）。有残留 → 补一轮「旧色→新色」映射再跑。
2. **封面截图**肉眼过一眼。
3. **线上 curl 验 token**：跟随 308（`/suanli/ep04.html` → `/suanli/ep04`），确认 `--bg` 和 `class` 是新值。

## 2.5 映射表从模板里抽，别手编；且必须**单遍同时替换** ⭐

**映射的唯一真相源 = 两套引擎模板的 `:root` 逐 token 对照**（同一个引擎、两个主题，key 一一对应）。用脚本 diff 出来，别凭记忆写色号：

```python
# 剥掉 /* 注释 */ 再解析 :root，逐 key 比对 deck-engine-暖黑 vs deck-engine-米白
```

实测暖黑 33 token / 米白 26 token，其中 **20 个值不同**（`--bg/--surface*/--line*/--text*/--read/--hot*/--hl0/--cool*/--ochre*/--warn`），4 个通用不翻（`--font/--serif/--mono/--brand`）；另 `--m-*`（9 张插画）暖黑独有、**`stroke='%23000'` 单色遮罩、不含主题色**（靠 CSS 着色，不用管）；`--shadow/--shadow2` 米白独有（亮底要投影），flip 时**要补进去**。

⚠️ **源集与目标集有交集 → 必须单遍替换**：`#f4f2eb` 既是源（暖黑 `--text` → `#1a1a18`）又是目标（暖黑 `--surface2` → `#f4f2eb`）。顺序 sed 会把前一条刚写出的颜色被后一条**再吃一次**，静默改错。正确做法是拼一个大 alternation 一次扫过：

```python
pat = re.compile('|'.join(re.escape(k) for k in sorted(MAP, key=len, reverse=True)), re.I)
out = pat.sub(lambda m: MAP[m.group(0).lower()], html)   # 单遍，绝不二次命中
```

## 2.6 图表内部色 ≠ 页面色：**脚本先扫「未覆盖色」并停下来** ⭐

token 映射只管**相对页面底色**的颜色。deck 里还有大量**图表内部色**，它们的对比度是相对自己所在的色块，**翻了反而坏**：

- `#19191a` 深字压在浅蓝柱 `#8fa6bd` 上 → 页面转亮底也得**留深**，翻了字就没了
- `#e8eef3` 浅字压在深柱上 → **留浅**
- 柱状填充（`#5e6b75`/`#a9714f`/`#8a7d70`）中间调 → 黑白底都成立，**别动**
- 语义色（如 Harness 里 MCP 的绿 `#8fbf9f`）有含义 → **别当装饰色翻**
- `#pmode` 讲者浮层（`#0c0d10`/`#ececf2`/`#9a9aac`…）、`.shell` 终端（`#1f1d1b`/`#0c0d10`）**刻意深底** → 不翻

所以 flip 脚本**必须内建一道守卫**：转换前先扫全部目标文件，报出「映射表未覆盖、又不在保留名单」的裸色，**有就退出让人判断**，别闷头转（2026-07-15 实测：算力 EP01 干净，其余 5 期共 **15 种**各自的图表色需人工过——守卫挡住了一次静默改坏）。

## 3. 血泪坑（都已解，别重踩）

1. ⚠️ **原地覆盖脚本必须先读后写**——最贵的一个坑，曾把 9 期**全写空**：
   ```python
   # ✗ src==dst 时，open(dst,'w') 先把文件截断成空，再 read 就读到空字符串
   open(dst,'w').write(flip(open(src).read()))
   # ✓ 先读进内存，再开写
   data = open(src).read()
   open(dst,'w').write(flip(data))
   ```
2. **`.shell` 终端组件不翻**：`#1f1d1b` / `#0c0d10` / `rgba(0,0,0,.2)` 是**刻意的深底代码块**（米白/焰彩白母本自身就 `.shell{background:#1f1d1b}`），亮底下也该是深的。只在 `--shadow` 行里翻 `rgba(0,0,0,`，其余深底放行。
3. **显式串先做**：`shadow` / `body 光晕` / `grain` 这类整串先替换，避免被后面的 bare-value 规则拆坏 alpha。
4. **grep 单行 minified 会漏**：subagent 输出常是单行 HTML，`grep -c "--bg:"` 按行匹配会误判。用 `grep -o`，或先 `wc -c` 看是不是空文件。
5. **半成品残留**：subagent 转版被中途停 → body SVG 内联色没转完。所以验收靠 第2节 第 1 条，不靠"它说它做完了"。
6. **截图坑 → 用 `--headless=new` + `--timeout`**（2026-07-15 修正）：deck 的 `.draw` 动画让 `--virtual-time-budget` 不收敛。旧 `--headless` 会**挂死且不写盘**（`timeout` 杀进程后目录里什么都没有；"杀了图其实已写盘"的旧说法**实测不成立**，别信）。可靠配方——**1.5 秒出图**：

   ```bash
   "$CHROME" --headless=new --disable-gpu --incognito --user-data-dir="$TMP/prof" \
     --window-size=1600,900 --hide-scrollbars \
     --virtual-time-budget=15000 --timeout=30000 \
     --screenshot="$TMP/cover.png" "file://$DECK"
   ```
   `--timeout` 让 Chrome 自己到点截图退出（退出码 0），不必外部 `pkill`。字体走 content-master-skill 绝对路径，`file://` 即可加载。
   ⚠️ 必带 `--incognito` + 独立 `--user-data-dir`，**别碰用户正在用的 Chrome**（见 memory `chrome-screenshot-isolated-incognito`）。
