# WPS Office 跨平台验证环境 — 经验手册

## 概述

WPS Office (Linux) 的渲染引擎比 LibreOffice 更接近 MS PowerPoint，
适合作为跨平台 PPTX 一致性的本地验证工具。

---

## 环境搭建

### 版本兼容性（关键教训）

| WPS 版本 | pywpsrpc 兼容性 | 备注 |
|---------|---------------|------|
| **11.1.0.x** (11719/11720/11723) | **兼容** | 推荐使用 |
| 12.1.x / 12.8.x (365) | **不兼容** | `getWppApplication` 返回 hr=-2147483640 |
| snap 10.x | 太旧 | 不支持 |

> **重要**: pywpsrpc 2.3.12 仅与 WPS 11.1.0.x 系列兼容。
> WPS 365 (v12.x) 修改了内部 RPC 协议，导致无法获取应用对象。

### 可靠的 deb 包来源

- GitHub 存档: https://github.com/peeweep/gentoo-go-deps/releases/tag/wps-office_11.1.0.11719
  - `wps-office_11.1.0.11719_amd64.deb` (~391MB)
  - 来自 Gentoo 社区存档，经过验证的官方 Kingsoft 包

### 安装步骤

```bash
# 1. 安装 WPS
sudo dpkg -i wps-office_11.1.0.11719_amd64.deb
sudo apt --fix-broken install -y  # 修复可能的依赖

# 2. 安装 pywpsrpc + Qt5 依赖
pip3 install pywpsrpc
sudo apt install -y libqt5xml5 libqt5gui5 xvfb xdotool scrot

# 3. 配置 EULA + 多组件模式
mkdir -p ~/.config/Kingsoft
cat >> ~/.config/Kingsoft/Office.conf << 'EOF'
[common]
AcceptedEULA=true

[wpsoffice]
Application%20Settings\AppComponentMode=prome_independ
Application%20Settings\AppComponentModeInstall=prome_independ
EOF
```

---

## CLI 使用经验

### 可靠方式: pywpsrpc + xvfb

```bash
xvfb-run --auto-servernum --server-args="-screen 0 1920x1080x24" \
    python3 wps_convert.py input.pptx output_dir png
```

### 不可靠方式（避免使用）

| 方式 | 问题 |
|-----|------|
| `wpp --convert-to pdf` | 超时/挂起，不会生成输出 |
| `wps --convert-to pdf` | 同上，CLI 转换功能不可靠 |
| Docker akkuman/headless-wps | 基础镜像缺 pip，安装 pywpsrpc 编译超时 |
| WPS 365 + pywpsrpc | RPC 协议不兼容 |

---

## pywpsrpc API 关键要点

### 正确的连接流程（v7.9 验证通过）

```python
import sys
from pywpsrpc.rpcwppapi import createWppRpcInstance, wppapi
from pywpsrpc.common import S_OK, QtApp

# 1. 初始化 Qt 事件循环（必须！否则 RPC 连接将失败）
qApp = QtApp(sys.argv)

# 2. 创建 RPC 实例（pywpsrpc 自动管理 WPS 进程启动）
hr, rpc = createWppRpcInstance()

# 3. 获取应用对象
hr, app = rpc.getWppApplication()

# 4. 获取 PID 用于退出时清理
hr, pid = rpc.getProcessPid()

# 5. 打开演示文稿（WithWindow=msoFalse 用于无窗口模式）
hr, pres = app.Presentations.Open(
    abs_path, ReadOnly=True,
    WithWindow=wppapi.MsoTriState.msoFalse
)

# 6. 退出时用 kill -9 PID（app.Quit 不可靠）
import subprocess
subprocess.call(f"kill -9 {pid}", shell=True)
```

> **关键教训**: 之前的版本手动启动 `wpp` 进程再尝试 `createWppRpcInstance`，
> 但缺少 `QtApp` 初始化导致 RPC 始终无法连接。官方示例
> (`examples/rpcwppapi/wpp_convert.py`) 明确要求 `QtApp(sys.argv)`。

### SaveAs 文件类型常量

| 常量 | 值 | 说明 |
|-----|---|------|
| ppSaveAsPNG | 18 | 批量导出为 Slide1.png, Slide2.png... |
| ppSaveAsPDF | 32 | 导出 PDF（可能在某些版本失败） |
| ppSaveAsJPG | 17 | 批量导出 JPG |

### 已知问题

- 退出时 segfault（exit code 139，正常现象，不影响输出文件）
- PDF 导出 `SaveAs(path, 32)` 可能返回 `hr=-2147417851`
- PNG 批量导出 `SaveAs(dir, 18)` 通常可靠
- **必须** `QtApp(sys.argv)` 初始化 Qt 事件循环，否则 RPC 无法工作
- **不要** 手动启动 `wpp` 进程，让 `createWppRpcInstance` 自动管理
- **必须** 用 `kill -9 PID` 清理进程，`app.Quit()` 不可靠且可能挂起

---

## 验证发现的典型问题

基于 WPS 渲染 v7.7 PPTX 的对比结果：

1. **文本框宽度不足** → 文字意外换行（如 "Defender" 的 r 被挤到第三行）
2. **单位文字被截断** → "127个" 变成 "127" + 换行 + "个"  
3. **引用文字过大** → Slide 5 文字换行过于频繁
4. **字体差异** → WPS 使用 Noto 而非 Arial 渲染 CJK 字符

这些问题与 Windows MS PPT 中观察到的一致，验证了 WPS 是有效的跨平台测试代理。

---

## 文件清单

- `scripts/wps_convert.py` — WPS 转换脚本（已验证可用）
- `WPS_TESTING.md` — 本文档
