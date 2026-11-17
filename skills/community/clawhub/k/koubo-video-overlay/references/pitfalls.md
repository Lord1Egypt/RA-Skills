# 踩坑与解法（口播视频素材加工）

实际跑通样例工程时遇到的坑，按出现顺序记录。

## 1. 复制 node_modules 耗尽系统资源

`cp -r` 复制 Remotion 的 node_modules（几千个小文件）在 Git Bash/cygwin 下会触发大量 fork，耗尽系统资源：
- 表现：`cygheap read copy failed`、`fork: Resource temporarily unavailable`、`Win32 error 299`，连带其他进程（如转写）也报 `WinError 1450 系统资源不足`。
- **解法**：不复制 node_modules，用目录联接（junction）指向已有工程的依赖，瞬间完成：
  ```python
  import _winapi
  _winapi.CreateJunction(r'<已有Remotion工程>\node_modules', r'<新工程>\node_modules')
  ```
  残缺的副本可 `mv node_modules node_modules_partial` 先改名（瞬间），再建 junction。事后删 node_modules_partial。
- 没有现成依赖才 `npm ci`（慢，失败回退 npmmirror）。

## 2. PowerShell 按 GBK 读 UTF-8 脚本 → 解析失败

pipeline.ps1 含中文（路径 `本次素材\原片.mp4`、`成片`，或中文注释/字符串）时：
- 表现：`字符串缺少终止符`、`表达式或语句中包含意外的标记`，中文显示成乱码（`鎴愮墖`）。原因是 Windows PowerShell 按系统码页 GBK 读无 BOM 的 UTF-8 文件。
- **解法**：给 .ps1 加 UTF-8 BOM：
  ```python
  b=open('pipeline.ps1','rb').read()
  if not b.startswith(b'\xef\xbb\xbf'): open('pipeline.ps1','wb').write(b'\xef\xbb\xbf'+b)
  ```
  或干脆脚本里全用英文（注释/报错/输出文件名），仅保留必要的中文路径并加 BOM。样例脚本本身带 BOM 所以没事。

## 3. 内存不足，本地转写跑不动

FunASR SenseVoice + torch 加载需 >1–2GB 空闲内存。系统只剩 1GB 时：
- 表现：`DefaultCPUAllocator: not enough memory` 或 `WinError 1450`。
- **解法**：
  - 不要擅自关用户的应用（其他占内存的程序）。
  - 改用**口播稿字数比例估算时间轴**：各段字数 ÷ 总字数 × 总时长 = 各段起止秒。用户念的就是写好的稿子时，估算足够准。
  - 渲染后抽帧核对（看画面字幕是否对上），偏了改 `$TN` 重渲染。
  - 系统空闲后再转写求精确：`python -I transcribe_audio.py audio.wav out.txt zh`。

## 4. python 串到别的 venv

不带 `-I` 跑 python 可能加载到其他 agent 的 venv site-packages（torch/wcwidth），引发资源或版本问题。
- **解法**：跑脚本统一 `python -I`（隔离模式，忽略 PYTHONPATH 和用户 site）。注意 `-I` 也会忽略 `PYTHONIOENCODING`，所以编码靠脚本内 `open(...,encoding=...)` 或 `PYTHONUTF8=1`（但 -I 下 PYTHONUTF8 也失效，需脚本内处理）。

## 5. 原片只读属性

从样例复制来的 `本次素材\原片.mp4` 可能继承只读（`-r--r--r--`），cp 覆盖报 `Permission denied`。
- **解法**：先 `rm -f` 旧文件再 cp；或 `chmod u+w`。

## 6. Git Bash 下 robocopy 中文路径乱码

`robocopy "<含中文的路径>"` 在 Git Bash 里中文被转码乱码 + 路径参数失效（`无效参数 #3`）。
- **解法**：用 Git Bash 原生 `cp -r`（正确处理 UTF-8 路径），或 Python 文件操作。工程文件夹名尽量用英文避免编码问题。

## 7. ffmpeg 合成写法（不要改）

`work/composite.txt`：
- 多图叠加链：`[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v1]; [v1][2:v]overlay...[v2]; ...`，`eof_action=pass` 让叠加层结束后原片继续。
- 原声 `[0:a]volume=2.0[a]`：单独输出时 volume=2.0 补偿（若和音效 amix 则两边同时有声会减半，需先放大）。
- **不要** `amerge`、不要给 `amix` 加 `normalize`、不要 `tpad` 拉长原片。
- 字幕滤镜用相对路径 `ass=captions.ass`，ffmpeg 工作目录设在 `work`（绝对路径盘符冒号会拆断滤镜）。本流程原片自带字幕时不另烧字幕。
- 叠加序列输入：`-itsoffset <秒> -framerate 30 -start_number 0 -i frames/frame-%03d.png`，帧率与原片一致。

## 8. 时间轴估算法（无转写时）

1. 拿到口播稿（用户念的稿子），分段统计字数。
2. 各段累计字数 ÷ 总字数 × 视频总时长 = 各段边界秒。
3. 每张图对齐到「口播讲到对应内容」的那段起始秒（如讲 skill 的段落起点）。
4. 渲染后在每张图应出现的秒数抽帧，看画面自带字幕是否正是对应语句 → 验证卡点。
5. 偏差就改 pipeline.ps1 的 `$TN`，重渲染（只需重跑 ffmpeg 合成段时可跳过 Remotion 渲染）。

## 9. 验证与交付

- 抽帧：`ffmpeg -ss <秒> -i 成片.mp4 -frames:v 1 check.jpg`，多模态确认图在侧边、不挡主体、字幕对应。
- 核对原声时长 = 原片时长（ffprobe audio duration），确保没被截断。
- 交付：复制成片到工作区，`python -I -c "import os; os.startfile(r'<成片路径>')"` 打开默认播放器。

## 环境清单

Node.js + npm + ffmpeg + ffprobe + Google Chrome（`C:\Program Files\Google\Chrome\Application\chrome.exe`）。Remotion 4.0.539 + React 19。多模态/转写脚本在 social-account-doctor 工程（见对应 memory）。