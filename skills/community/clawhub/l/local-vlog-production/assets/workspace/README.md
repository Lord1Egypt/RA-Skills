# 本地 Vlog 工作区

本目录由已安装的 `local-vlog-production` 技能初始化。阅读 [使用指南](使用指南.md) 后放入自己的素材。

素材 → 审阅和时间线 → 分镜 → 粗剪确认 → 精剪检查 → 成片、封面、短文案 → 确认锁定。

先运行 `python tools/workspace.py doctor`。中文字体需通过初始化参数提供或另行配置；配置好后运行 `python tools/make_demo.py` 生成合成示例，再运行 `tests/selftest.py` 检查基础制作链路。FFmpeg不在PATH时，自检参数须明确传入本机ffmpeg及ffprobe路径。

本目录不含作者私人素材或已接受声音。递进蒙太奇仅当前作品明确要求后启用。工具不会自动发布、删除或标记用户接受。

- [技术架构](技术架构.md)
- [工具命令](docs/工具命令.md)
- [时间线格式](docs/时间线格式.md)
- [精修与声音](docs/逐镜精修与声音.md)
- [第三方依赖](THIRD_PARTY_NOTICES.md)
