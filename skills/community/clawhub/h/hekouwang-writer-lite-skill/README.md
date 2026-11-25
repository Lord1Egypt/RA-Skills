# hekouwang-writer-skill · 开发仓库

本仓库是**本地开发与构建仓库**，不是安装包。

同一份源码出两个写作技能产物：免费版 `hekouwang-writer-lite-skill` 与专业版 `hekouwang-writer-skill`；另有一个独立的按次体检客户端 `hekouwang-writer-check-paid`。命名规则见 [`STRUCTURE.md`](STRUCTURE.md) 第二节。

面向用户的页面在 [`docs/`](docs/index.html)（GitHub Pages 源 = 主仓 `docs/`）。日常推送主仓 `origin`；目录约定见 [`STRUCTURE.md`](STRUCTURE.md)。

## 两个写作技能产物

| 产物 | 名字 | 来源 | 许可 | 脚本 / 参考 |
|---|---|---|---|---|
| 免费版 | `hekouwang-writer-lite-skill` | 根目录 | MIT-0 | 4 / 8 |
| 专业版 | `hekouwang-writer-skill` | 根目录 + `edition/` | Proprietary | 11 / 20 |

免费版管表达（结构、句子、去 AI 味）。专业版在此基础上加证据纪律、数字对账、出处卡、修订对账、文体规范、长文写作与七套场景包。

## 三个渠道

| 渠道 | 产品 | 版本 | 说明 |
|---|---|---|---|
| 支付宝 SkillPay | 专业版 | 见 `edition/VERSION` | 订阅；11 脚本 / 20 参考 |
| ClawHub / GitHub | 免费版 | 同 `edition/VERSION` | MIT-0；4 脚本 / 8 参考 |
| 腾讯 SkillHub | 按次体检 | 线上 2.0.1 | 远端检查，不是专业版 11 脚本包 |

完整口径见 [`RELEASE.md`](RELEASE.md)：免费版与专业版同号，按次体检是独立版本线，三个渠道不要混用。

`build_paid_package.py` 负责组装专业版包：先拷根目录，再叠加 `edition/`，然后替换名称、描述与许可，删掉只对免费版成立的段落。

## 目录

| 路径 | 归属 | 用途 |
|---|---|---|
| `SKILL.md`、`scripts/`、`references/`、`examples/` | 主仓 | 免费版源码，也是专业版的底座 |
| `docs/` | 主仓 | 产品页与案例页源（GitHub Pages） |
| `materials/` | 主仓 | 货架物料（不进 Skill/ClawHub 安装包） |
| `STRUCTURE.md` | 主仓 | 本仓特例；组织标准见 `~/.user-agents/standards/hekouwang-skill-structure.md` |
| `edition/` | 独立本地仓 | 专业版增量与构建材料（无公开远程） |
| `roadmap/` | 独立本地仓 | 升级与作战地图：方案、执行计划与证据（无公开远程；勿与对外产品路线混淆） |
| `services/skillhub-402/` | 独立私有仓 | 402 服务与 SkillHub 按次客户端 |
| `dist/`、`archive/` | 不版控 | 构建产物（`dist/<version>/` 只留当前版 zip）与归档 |

## 开发命令

```bash
# 脚本自检
for f in scripts/*.py; do python3 "$f" --selftest || exit 1; done

# 升级版本（一次更新 6 个版本点）
python3 scripts/bump_version.py 2.0.7

# 校验 6 个版本点一致
python3 scripts/bump_version.py --check

# 构建专业版包（默认读 edition/VERSION，输出到 dist/<version>/）
python3 scripts/build_paid_package.py

# 指定版本或输出路径
python3 scripts/build_paid_package.py --version "$(cat edition/VERSION)" --out /tmp/writer-skill.zip

# 改过页面文案后，重建字体子集
bash scripts/subset-fonts.sh

# 本地预览产品页
python3 -m http.server 8788 --directory docs
```

## 发版检查

先看 [`RELEASE.md`](RELEASE.md) 的渠道与版本矩阵：免费版与专业版同号，按次体检是独立版本线。

1. **版本号同号**：跑 `python3 scripts/bump_version.py <version>` 更新 6 个版本点，再跑 `--check` 必须 PASS；6 个点由脚本统一更新，不要手改。
2. **商品文案先改仓库副本**：先比对 [`listing-skillpay.md`](listing-skillpay.md)，再改平台商品描述。顺序反了会以「描述与上传文件能力说明不一致」驳回。
3. **文件移动**：根目录只放免费内容，专业版内容放 `edition/`。移动后重建专业版包，确认两个版本各自无死链。
4. **构建后自检**：解压安装包，确认 `SKILL.md` 的 name、版本号、脚本数与 `_meta.json` 一致。
5. **页面文案改动**：重跑 `scripts/subset-fonts.sh`，否则新字会回退到苹方。
6. **商品文案 / README / 构建核对**：统一按专业版包 **11 脚本 / 20 参考**对账；构建时从 `edition/meta.paid.json` 覆盖 homepage / handoff，并拷贝 `edition/examples`。

## 文档指针

| 文件 | 用途 |
|---|---|
| [`RELEASE.md`](RELEASE.md) | 三个产品、三条版本线、渠道矩阵与发版规则 |
| [`scripts/bump_version.py`](scripts/bump_version.py) | 一次更新 6 个版本点；`--check` 校验一致 |
| [`SKILL.md`](SKILL.md) | 运行时入口与路由（免费版正文） |
| [`STRUCTURE.md`](STRUCTURE.md) | 目录结构、双版本命名与推送边界 |
| [`AGENTS.md`](AGENTS.md) | 改本仓库时的规则 |
| [`listing-skillpay.md`](listing-skillpay.md) | 支付宝商品文案副本与发版比对 |
| [`services/skillhub-402/client/SKILL.md`](services/skillhub-402/client/SKILL.md) | SkillHub 按次体检客户端说明 |
| [`CHANGELOG.md`](CHANGELOG.md) | 免费版 + 专业版变更记录 |

## 产品入口

- 产品页：<https://huiyonghkw.github.io/hekouwang-writer-lite-skill/>
- 售卖渠道与商品页链接不在仓库留存，统一在创作者后台维护

## 许可

- 免费版 `hekouwang-writer-lite-skill`：MIT-0，可用、可改、可商用、可再分发。
- 专业版 `hekouwang-writer-skill`：Proprietary，个人使用，不可转售或再分发。
- 更早版本的许可说明见公开仓历史中的 `LEGACY-MIT-0.md`，已发出的副本继续适用。

## 方法论来源（致谢）

本技能的规则组织、案例和检查脚本为原创实现或重写。以下来源用于说明方法出处：

- **kunlun-doc-write / doc-write**（昆仑增长）：WRITE 流程、每节核心句、边界声明
- **universal-writer**：出处铁律、修订模式、进度卡、风险告知格式
- **asd-ste100**（GitHub: danyuchn/asd-ste100-skill）：句法纪律、模态保留、一词一义
- **chenlin-credible-translate**（真笔翻译）：五轴心、禁止层 P1-P3、G1-G5、机械检查思路
- **dev-god**、**dev-expert**、**parenting-expert**、**tencent-docs**、**self-improving-agent**（SkillHub）：证据三分、三档机制、边界声明、场景路由、learnings 台账
- **zh-humanizer**、**khazix-writer**、**李诞写作心法**、**说人话**、**Humanizer-zh / qu-ai-wei**：文章模式与去 AI 味的写法参考
- **ASD-STE100 Issue 9**（2025-01）：受控语言标准本身
