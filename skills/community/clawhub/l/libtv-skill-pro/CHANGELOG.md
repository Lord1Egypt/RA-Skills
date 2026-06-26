# Changelog

## [0.4.0] - 2026-05-14（即将发布）

**主题：公开推广就绪 + 架构升级**

### Added — 推广向
- `examples/` 5 个完整 case：生图 / 视频 / 编辑 / 多步链 / 批量
- `README.md`（GitHub 入口）+ `LICENSE`（MIT-0）+ `.gitignore`
- `CHANGELOG.md` 正式纳入版本管理
- 公开 GitHub 仓库（信任来源 / issue / PR）
- SKILL.md frontmatter description 精简到 ~400 字，前 300 字聚焦关键词（搜索能见度）
- SKILL.md 增加「快速开始 3 分钟跑通」段落 + 决策树 + LibTV access key 获取链接

### Added — 架构升级
- `libtv.py` 统一入口（dispatcher）—— Agent 只需记一个命令：`libtv.py {flow|node|edit|model|...}`
- `--dry-run` 标志（flow / node / edit / model）—— 预览将发送的 prompt，不调 API、不烧积分
- 结构化错误响应（`_common.APIError` + `safe_run` wrapper）—— 所有 API 错误以 JSON 写 stderr，含 kind / http_code / message / raw
- 错误 kind 枚举：INVALID_ACCESS_KEY / FORBIDDEN_OR_INSUFFICIENT_CREDITS / NOT_FOUND / TIMEOUT / RATE_LIMITED / SERVER_ERROR / NETWORK_ERROR / INTERRUPTED / UNKNOWN

### Fixed
- `change_project.py` 缺 argparse 导致 `--help` 直接调真 API（之前发版前发现的 bug）
- `_common.py` 不再在 import 时因缺 LIBTV_ACCESS_KEY 而 `sys.exit(1)`——改为延迟到首次实际调用 API 时抛 `APIError`，让 `--help` 在任何情况下都可用

### Changed
- 所有调 API 的脚本都接入 `safe_run(main)` wrapper
- frontmatter emoji 由 💬 改为 🎬（配合 film 图标）
- tests/test_offline.sh 增加 1b（libtv.py 入口）+ 1c（dry-run 验证）共 20 个新用例
- 总测试用例：73 离线 + 47 模板 = **120 全通**

### Cleanup
- 发布前清掉 workspace 的 `.clawhub/origin.json`（之前误发）
- `_meta.json` 不打包进发布

---

## [0.3.0] - 2026-05-13

**LibTV 功能矩阵层**（slug: libtv-skill-pro，fork-of @haofanwang/libtv-skill@1.0.3）

新增 4 个脚本覆盖 LibTV 画布上的完整功能矩阵：

- `flow.py` — LibTV 首页 4 个预设流程（story_script / character_views / keyframe_to_video / audio_to_video）
- `node.py` — 文本/图片/视频节点的细分动作（text_to_video_prompt / image_caption / text_to_music / image_to_image / image_upscale / first_last_frame / reference_video）
- `edit.py` — 节点修饰器（style / mark / focus / camera / character_lib）
- `model.py` — 模型路由（list 9 个已知模型 + with 显式指定模型+参数）

SKILL.md 第 13–16 节文档，新增「场景 8：按 LibTV 网页功能直接调用」工作流示例。

## [0.2.0] - 2026-05-13

**首发 libtv-skill-pro**（fork-of @haofanwang/libtv-skill@1.0.3）

在原版 6 个基础脚本之上扩展 7 个高级工作流脚本：

- `manage_project.py`（list/current/switch/use/remove/describe + `~/.libtv_projects.json` 本地项目记录）
- `batch_create.py`（并发批量任务）
- `monitor_session.py`（实时监控）
- `quick_poll.py`（简化轮询）
- `workflow_template.py`（8 个预设模板）
- `export_results.py`（导出 JSON / Markdown / HTML）
- `session_history.py`（会话历史管理）

行为增强：
- `create_session.py` / `change_project.py` 自动写入本地项目记录
- `_common.py`：`change_project()` 支持可选 `projectUuid` 参数
