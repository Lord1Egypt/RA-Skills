# 接收者环境状态

当前为未检查。包内测试报告只证明打包电脑上的合成示例验证，不代表这台电脑已经可以执行。

先运行 tools/workspace.py doctor；确认Python、Pillow、NumPy、FFmpeg/ffprobe和libx264。缺失依赖按使用指南安装。faster-whisper模型、ExifTool、录音/AI配音及内置图像生成分别检查，缺失不伪称可用。

默认Windows优先，其他系统的文件路径已尽量可移植但需要重新验证。无需GPU；CPU渲染时间取决于片长、分辨率与效果。第一次检查和合成示例成功后，由Codex更新本文件，不预先标记真实素材已审阅或完整听过。
