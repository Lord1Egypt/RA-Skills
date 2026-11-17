# 首次建立工作区

此技能包含流程、通用工具和文本模板，不包含字体、照片、音视频、模型或软件运行时。先确定一个新建或空的工作区目录，再初始化；现有个人作品目录不适合作为初始化目标。

## 1. 准备环境和可用字体

准备 Python 3.10 或更新版本（已测3.12）、包含 `libx264` 的 FFmpeg 及 ffprobe。依赖安装清单在 `assets/workspace/requirements-core.txt`；可选本地转写依赖在 `assets/workspace/requirements-asr.txt`，模型另行准备。不要把凭据、模型缓存或个人素材放入已安装的技能目录。

中文渲染需要由使用者明确提供有权使用的 TTF/OTF 文件。可从以下官方仓库自行取得字体并阅读许可；技能不自动下载、不安装到系统，也不把这些字体按本技能的 MIT-0 许可再分发：

- [得意黑 / Smiley Sans 官方仓库](https://github.com/atelier-anchor/smiley-sans)，查看仓库中的 [SIL Open Font License 1.1](https://github.com/atelier-anchor/smiley-sans/blob/main/LICENSE)。可用作正文或立体贴纸艺术字。
- [Ma Shan Zheng 的 Google Fonts 官方目录](https://github.com/google/fonts/tree/main/ofl/mashanzheng)，查看其 [OFL.txt](https://github.com/google/fonts/blob/main/ofl/mashanzheng/OFL.txt)。可用作笔刷风格文字的起点；字体本身不等于完成了文字页的纹理和构图设计。

也可选择使用者已有的其他中文字体。核对字体覆盖所需汉字，保留其来源与适用许可；再次分享工作区时，字体的权利和许可仍独立适用。

## 2. 运行初始化工具

让 Codex 定位本技能的实际安装目录。以下示例中的 `<技能目录>` 和 `<字体文件>` 都需替换为本机真实路径，不是可直接执行的字面文本：

```text
python "<技能目录>/scripts/init_workspace.py" --destination "<新工作区>" --body-font "<正文中文字体.ttf>" --title-font "<标题中文字体.ttf>"
```

目标目录也可直接作为位置参数传入，与 `--destination` 二选一。可只提供 `--body-font`，正文与艺术字先共同使用它；只提供 `--title-font` 也可，正文暂时使用同一字体。不提供字体仍可建立目录、盘点素材和整理脚本，但不能把文字渲染标为就绪。初始化后的 `initialization_report.json` 会记录字体路径、实际复制情况和待检查项目。

初始化工具只接受不存在或空的目标目录，拒绝符号链接、目录联接及其他重解析点；不会替换已有文件。它从技能的 `assets/workspace/` 复制工作区文本模板，从技能的 `tools/`、`tests/` 复制 Python 文件，并创建素材、作品和工作数据目录。显式提供的字体复制到新工作区的 `公共资源/字体/用户字体/`，同步更新公共样式和示例时间线中的字体引用。不会复制技能目录本身、自动下载资源、上传素材或修改原字体。

若初始化中途因磁盘或权限错误停止，保留已写入文件用于排查；请改用另一个新建或空目录重试，不要期望再次执行时覆盖原目录。

若先创建了无字体工作区，再补字体，让 Codex将合法字体放入工作区资源目录，更新 `公共资源/style.default.json` 的 `font_candidates`、`font_roles`、`fonts_ready` 和 `examples/演示时间线.json` 中的 `font` 引用；不要再次运行初始化工具覆盖工作区。

## 3. 在新工作区检查并生成演示

用 Codex 打开新工作区。先阅读根目录的 `AGENTS.md`、`使用指南.md`、`WORKFLOW.md` 和 `docs/工具命令.md`，安装核心 Python 依赖后执行：

```text
python tools/workspace.py doctor
python tools/make_demo.py
python tools/render_timeline.py --workspace-root . --timeline examples/演示时间线.json --validate-only
```

`workspace.py doctor` 会读取工作区 `environment.local.json` 中的实际可执行文件路径。`make_demo.py` 和 `tests/selftest.py` 不读取该配置：FFmpeg 不在系统路径中时，必须显式传入本机路径，例如 `python tools/make_demo.py --ffmpeg "<ffmpeg路径>"`，以及 `python tests/selftest.py --ffmpeg "<ffmpeg路径>" --ffprobe "<ffprobe路径>"`。其他工具按其帮助和 `docs/工具命令.md` 配置。不要把本机配置、字体、生成的演示媒体和测试缓存回传到公开技能包。

`make_demo.py` 在本机生成合成照片、动态图形和低电平测试音，用于验证文件引用和渲染器；它不是成片风格样片，也不代表实际审阅过用户素材。现成媒体没有随技能分发，所以不能在生成演示之前直接宣称示例时间线验证通过。

依赖、字体与生成的示例就绪后，按 `docs/工具命令.md` 渲染演示或运行 `tests/selftest.py`。技术测试不能代替连续看片和实际听音。工作区建好后仍使用已安装的 `local-vlog-production` 技能；若当前宿主没有自动发现它，明确调用该技能或让 Codex读取其实际 `SKILL.md`。无需把技能重复复制到工作区。

## 4. 开始真实作品

在 `素材/` 下建立主题子目录并放入原件，给 Codex 本次主题、故事描述和输出要求。标准顺序是：实际审阅与拍摄时间线 → 分镜 → 粗剪确认 → 精剪和视觉/声音检查 → 成片、封面与短文案 → 用户确认锁定。

原件保持只读。默认启用普通剪辑、照片斜落轻放、关键艺术字与静态文字页的适配流程；将重复题材组织成递进蒙太奇，只有当前作品得到明确要求时才启用。首次作品需建立使用者自己的音乐听感参考，不能以作者已接受但未分享的私人混音作为已验证标准。
