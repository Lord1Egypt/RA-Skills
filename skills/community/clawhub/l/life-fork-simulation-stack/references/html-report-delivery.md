# HTML 报告交付流程

> Language scope: the bundled layout intentionally targets Simplified Chinese readers. Follow the user's chosen language in conversation. Use Chinese HTML only when requested; offer Markdown for other languages.

## 交付选择

默认在当前对话交付 Markdown。用户要求保存或导出 HTML 后，才生成文件。中文 HTML 包含固定中文标题；其他语言的用户可继续使用对应语言的 Markdown，或自愿选择中文 HTML。

文件可能包含个人经历。先说明保存位置和文件类型，使用中性文件名，仅使用当前任务已授权的目录。私人报告的公开发布、上传和转发需要额外授权；不要把生成文件和发送文件合并成一次动作。

## 单文件渲染

仅使用当前任务生成的 Markdown，或用户明确指定的一份报告。将示例中的路径替换成当前授权的准确路径，使用独立命令参数，避免把正文拼进命令。

```bash
python3 scripts/render_html_report.py input.md --html report.html
```

渲染器只读取选定输入、只写入选定输出，不查找父目录、历史报告或其他项目，不联网、不运行其他程序，也不安装依赖。输入、输出不能指向同一个文件；符号链接文件会被拒绝。已存在的输出默认保留，用户明确要求替换后才可使用 `--overwrite`。

执行前确认宿主允许运行本地脚本，并核验实际渲染器路径。文件工具不可用时，直接交付对话 Markdown，不安装工具或扩展权限。

## 当前报告检查

按 `report-quality-rubric.md` 和 `magic-score-rubric.md` 检查当前报告的结构、情景边界和内容具体度。这些检查在当前生成过程完成，无需包级自检或仓库扫描，也不需要保存额外日志。

渲染后仅检查本次生成的 HTML：

- 首屏包含报告名、用户问题、判词和下滑提示。
- 分叉图解释现实结果、假设结果和回补结果。
- 三种结果同时包含收益、代价与成立条件。
- 事件冲击卡含时间、生活场景、现实代价、情绪代价、误判点和验证动作。
- 30 天实验按四周安排低风险动作和现实反馈。
- 各视角解释和补充问题进入折叠层，用户界面不展示内部评分。
- 手机与电脑阅读时文字可读、卡片可展开。

打开报告只用于查看当前文件，遵循宿主的浏览器权限。留档、打印和分享按用户请求处理。
