# 本地 Vlog 制作 / Local Vlog Production

从真实素材出发，先确认故事，再同轮拿到可读脚本和能播放的 HTML 选材页。可按章节逐条预览或串看已选镜头。换镜头、移段或改旁白后，可保存选择并生成下一版脚本和页面。本地工具也支持粗剪、精剪、字幕、封面和声音检查。

安装后先读 [首次使用](references/first-run.md)。技能安装目录与素材工作区分开；初始化不会覆盖既有工作区。日常直接向Agent提供主题目录与故事描述，先确认故事结构，再按分镜、粗剪、精剪阶段推进。仅对本作明确要求跳过故事确认时可越过该环节，并记录依据。

分镜固定核对两件事。事实更正要改到所有引用它的画面和文案，关键现场声要先留完整再定剪点。漏拍补叙、跨天地标接镜、反复事件支线和单张照片首尾呼应按当前素材选用。

从 1.0.0 升级的已有工作区可以直接用新版技能内的 `scripts/review_board.py` 处理现有作品。新建工作区后，同一个工具位于工作区 `tools/review_board.py`。

从旧版升级的既有工作区可直接运行新版技能目录的 `tools/qa.py --root <现有工作区> --input <成片> --out <新报告>`。选轨、超时和独立复查参数见[工具命令](assets/workspace/docs/工具命令.md)。

- [核心技能](SKILL.md)
- [脚本与选材同步](references/storyboard-review.md)
- [按需剪法，包括漏拍补叙、跨天地标、沿途支线与首尾呼应](references/optional-edits.md)
- [视觉参数](references/visual-presets.md)
- [技术架构](assets/workspace/技术架构.md)
- [使用指南模板](assets/workspace/使用指南.md)
- [第三方依赖](assets/workspace/THIRD_PARTY_NOTICES.md)
- [MIT-0许可](LICENSE.txt)
- [已执行的验证](references/validation.md)

递进蒙太奇仅对当前作品明确要求时启用。BGM以接收者已确认的基准为准，不重复降低已接受音轨。所有审阅、连续观看、实际试听和程序验证分别记录。

本发布版不附带字体、配乐、语音模型、真实素材或成片。字体可从原作者来源另行取得，按其OFL许可使用；不将第三方字体重许可为技能代码的许可。示例在本机生成，Windows以外平台尚需实际验证。
