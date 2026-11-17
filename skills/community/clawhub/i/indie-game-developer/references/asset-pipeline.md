# 游戏资源管线（Game Asset Pipeline）

> 子技能讲了"怎么画精灵/怎么写 Three.js"，但资源从生产到进游戏有一条独立链路：
> 精灵表打包、贴图压缩、音频转码、模型优化、引用对齐。断了任何一环，游戏要么
> 体积爆炸要么运行时缺资源。本篇是跨栈的资源管线 playbook，附命令、坑与清单。
> 脚本资源完整性校验见 [scripts/check_asset_refs.py](../scripts/check_asset_refs.py)。

## 1. 资源分类与格式选型

| 资源 | 推荐格式 | 避免 | 原因 |
|------|----------|------|------|
| 2D 精灵 | PNG-8/索引色（像素风）、PNG-32（透明） | 未压缩 BMP | 体积与透明 |
| 精灵表 | 单图 + `.json` 帧数据（TexturePacker/免费工具） | 多散图 | 绘制调用数 |
| 3D 模型 | `.glb`（二进制 glTF） | `.obj`/`.fbx` 裸用 | glb 含材质/动画且小 |
| 贴图 | KTX2/Basis（GPU 压缩）WebP | 全尺寸 PNG | 显存与体积 |
| 音频 | `.ogg`（Web）/ `.mp3`；SFX 短 `.wav` | 长音乐用 wav | 体积 |
| 字体 | `.ttf`/`.woff2`（子集化） | 全量字体 | 体积 |
| 图集 | 2048×2048 以内（移动兼容） | 4096 超大图 | 老 GPU 不支持 |

**铁律**：资源进游戏前必须过管线（压缩/打包/优化），原文件不进构建产物。

## 2. 精灵表与图集打包（命令）

像素风/2D 必做精灵表，把数十张散图合成一张，绘制调用从 N 降到 1：

```bash
# 用 free-ish 工具（示例命令，按本地安装调整）
# TexturePacker 免费版：texturepacker sprites/ --sheet atlas.png --data atlas.json --format json
# 或用 ImageMagick 拼图（无帧数据，需自管坐标）
montage sprites/*.png -tile 8x8 -geometry +0+0 atlas.png
# 校验图集尺寸为 2 的幂且 ≤2048
identify -format "%wx%h" atlas.png
```

Three.js 加载精灵表：用 `Texture` + `repeat`/`offset` 按帧切，或 `SpriteSheet` 工具。
关键：帧坐标用整数像素，避免子像素模糊（见 `pixel-art-studio` 硬边缘原则）。

## 3. 3D 模型优化（glb）

```bash
# glTF 验证与优化（gltf-transform，npm 全局）
npm i -g @gltf-transform/cli
gltf-transform optimize model.glb model.opt.glb --compress draco   # Draco 几何压缩
gltf-transform dedup model.glb model.dedup.glb                     # 去重
gltf-transform inspect model.glb                                   # 看面数/材质/纹理
```
优化目标：
- 面数：移动端单模型 ≤ 1–2 万面；桌面可更高但注意总数
- 纹理：≤2048²，KTX2 压缩；合并共享材质
- 动画：骨骼数克制，避免每顶点多骨骼
- Draw call：合并静态网格（静态合批），减少材质切换

## 4. 音频转码与触发

```bash
# 音乐转 ogg（更小），SFX 保持短 wav 或转 ogg
ffmpeg -i bgm.wav -c:a libvorbis -q:a 5 bgm.ogg
# Web 端：用户首次交互后 resume（浏览器自动播放限制）
#   audioCtx = new AudioContext(); btn.onclick = () => audioCtx.resume();
```
- 同时加载的音频数受限，长音乐用流式，SFX 用对象池
- 音量分轨（master/music/sfx）便于设置页调

## 5. 资源引用对齐（防"运行时缺图"）

最痛的 bug：代码引用了 `hero.png`，但文件改名成 `hero_02.png` → 运行时裂图/报错。
用 [scripts/check_asset_refs.py](../scripts/check_asset_refs.py) 在 CI 里扫源码引用并校验文件存在（见该脚本说明）。
约定：
- 资源路径集中放常量/清单，不散落魔法字符串
- 改名走全局替换 + 跑引用校验
- 资源清单（manifest）进版本控制，CI 校验完整性

## 6. 典型坑与规避

- **坑：散图直接进游戏**，数百 draw call 卡成幻灯片。*规避*：精灵表/图集合批。
- **坑：贴图全尺寸 PNG 塞显存**，低端机爆显存崩。*规避*：KTX2/WebP + 尺寸上限。
- **坑：glb 带未压缩纹理**，单个模型几十 MB。*规避*：Draco + 纹理压缩。
- **坑：音频未 resume**，Web 上静音且无报错。*规避*：首次交互 resume。
- **坑：引用字符串写错大小写**，Linux 服务器构建 OK、mac/Windows 本地裂图（大小写敏感）。*规避*：CI 跑引用校验（跨平台一致）。
- **坑：超大图集 4096**，老 Android GPU 不支持非 2 幂/超大图。*规避*：≤2048 且 2 的幂。

## 7. 收口清单

- [ ] 所有 PNG 已按用途选格式（索引色/透明），无 BMP
- [ ] 2D 精灵已打包成精灵表（绘制调用已合批）
- [ ] 3D 模型已 glb 化并 Draco/纹理压缩，面数在预算内
- [ ] 音频已转码（ogg/mp3），Web 端 resume 逻辑就位
- [ ] 字体已子集化，体积可控
- [ ] 资源路径集中管理，无散落魔法字符串
- [ ] 改资源名后跑了 [scripts/check_asset_refs.py](../scripts/check_asset_refs.py)，0 缺失引用
- [ ] 资源清单进版本控制，CI 校验完整性通过
- [ ] 图集尺寸 ≤2048 且为 2 的幂，移动端兼容

## 8. 资源命名与目录规范

约定先于工具，避免混乱：

```
assets/
  sprites/        2D 精灵（按角色/UI 分子目录）
  spritesheets/   打包后的图集 .png + .json
  models/         .glb（含动画）
  textures/       KTX2/WebP 贴图
  audio/
    bgm/          长音乐 .ogg
    sfx/          短音效 .ogg/.wav
  fonts/          子集化 .ttf/.woff2
  data/           关卡/配置 .json（资源清单）
```

命名规则：小写 + 下划线，`角色_动作_帧序列.png`；图集 `角色_atlas.png`；
版本不用文件名（走版本控制）；**跨平台大小写敏感**：全小写避免 mac/Win 本地 OK、Linux CI 裂图。

## 9. 体积预算表（手游/Web 硬约束）

| 平台 | 首包体积目标 | 显存/内存 | 纹理上限 |
|------|--------------|-----------|----------|
| Web(H5) | <10MB（首屏） | 视设备 | 单图 ≤2048² |
| 移动(低端) | <100MB | <512MB | 单图 ≤1024² |
| Steam/桌面 | <2GB 友好 | <2GB | 单图 ≤4096² |
| Steam Deck | 同桌面 | 共享内存严控 | 同桌面 |

超预算的缓解：资源按需加载（场景/关卡切时再拉）、CDN 分流、纹理压缩、音频流式。

## 10. CI 集成（确定性校验）

把资源管线固化进 CI，避免"我机器上能跑"：

```yaml
# .github/workflows/assets.yml（骨架）
on: [push]
jobs:
  asset-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/check_asset_refs.py --scan src/ --root .
      # 资源优化（按需）
      - run: npx @gltf-transform/cli optimize models/*.glb models/opt/
      # 体积门禁
      - run: du -sh dist/assets && [ $(du -sm dist/assets | cut -f1) -lt 200 ]
```

要点：引用完整性（check_asset_refs）+ 优化 + 体积门禁三步固化。

## 11. 工具清单（常用）

- 精灵表：TexturePacker（商业）/ 免费 `free-tex-packer` / 自写 montage
- 模型：Blender（导出 glb）、`@gltf-transform/cli`（优化）
- 纹理：`texpresso` / `toktx`（KTX2）、`imageoptim`（WebP）
- 音频：`ffmpeg`（转码）、`audacity`（剪辑）
- 字体：`fonttools`（子集化）
- 校验：[scripts/check_asset_refs.py](../scripts/check_asset_refs.py)（引用完整性，本项目自带）

## 12. 资源解耦（为可迁移性）

资源统一用引擎无关格式（glb / 精灵表 / 配置 JSON），业务逻辑与渲染解耦。
这样换引擎时主要重写渲染层，资源可复用（见 [references/decision-engine-tech.md](decision-engine-tech.md) §10）。

## 相关子技能与层次边界

> 本文属**资源管线方法层**（格式选型 / 精灵表 / glb / 音频 / 引用完整性）；具体的精灵生成与 3D 资产加载交给子技能。

- 像素美术精灵与 sprite sheet 生成 → [`skills/pixel-art-studio/SKILL.md`](../skills/pixel-art-studio/SKILL.md)
- Three.js 资源加载与引用对齐 → [`skills/game-developer/SKILL.md`](../skills/game-developer/SKILL.md)
- 引用完整性确定性校验 → [scripts/check_asset_refs.py](../scripts/check_asset_refs.py)
- 兄弟参考：引擎无关格式与迁移止损 → [references/decision-engine-tech.md](decision-engine-tech.md) §10
- 兄弟参考：运行时缺图根因排查 → [references/game-qa-perf.md](game-qa-perf.md) §6

