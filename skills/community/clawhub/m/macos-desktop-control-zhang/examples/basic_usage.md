# macOS Desktop Control - 使用示例

---

## 📸 截屏示例

### 基础截屏
```bash
# 全屏截图
bash scripts/screenshot.sh

# 选择区域截图
bash scripts/screenshot.sh -s

# 窗口截图
bash scripts/screenshot.sh -w

# 延迟 5 秒截图
bash scripts/screenshot.sh -d 5
```

### 保存到指定位置
```bash
bash scripts/screenshot.sh -o ~/Desktop/test.png
```

---

## 📋 进程管理示例

### 查看进程
```bash
# 显示图形界面应用
bash scripts/processes.sh -g

# 显示用户进程
bash scripts/processes.sh -u

# 显示所有进程
bash scripts/processes.sh -a

# 显示 CPU 占用前 10 的进程
bash scripts/processes.sh -t 10
```

### 搜索进程
```bash
# 搜索 Safari 进程
bash scripts/processes.sh -s Safari

# 搜索 Chrome 进程
bash scripts/processes.sh -s Chrome
```

### JSON 格式输出
```bash
bash scripts/processes.sh -j
```

---

## 💻 系统信息示例

### 简要信息
```bash
bash scripts/system_info.sh --short
```

### 详细信息
```bash
# 所有信息
bash scripts/system_info.sh -a

# 硬件信息
bash scripts/system_info.sh -h

# 软件信息
bash scripts/system_info.sh -s

# 磁盘信息
bash scripts/system_info.sh -d

# 内存信息
bash scripts/system_info.sh -m

# 网络信息
bash scripts/system_info.sh -n

# 电池信息
bash scripts/system_info.sh -b
```

---

## 📋 剪贴板示例

```bash
# 读取剪贴板
bash scripts/clipboard.sh get

# 写入剪贴板
bash scripts/clipboard.sh set "Hello World"

# 复制文件到剪贴板
bash scripts/clipboard.sh copy file.txt

# 粘贴到文件
bash scripts/clipboard.sh paste > output.txt

# 清空剪贴板
bash scripts/clipboard.sh clear
```

---

## 🖥️ 应用控制示例

```bash
# 打开应用
bash scripts/app_control.sh open Safari

# 关闭应用
bash scripts/app_control.sh close Safari

# 获取前端应用
bash scripts/app_control.sh front

# 列出所有应用
bash scripts/app_control.sh list

# 切换到应用
bash scripts/app_control.sh activate Safari

# 应用信息
bash scripts/app_control.sh info Safari
```

---

## 🖱️ 鼠标键盘控制（需要 pyautogui）

### 安装依赖
```bash
pip3 install --user pyautogui pyscreeze pillow psutil
```

### 鼠标控制
```bash
# 获取鼠标位置
python3 scripts/desktop_ctrl.py mouse position

# 点击坐标
python3 scripts/desktop_ctrl.py mouse click 100 100

# 移动鼠标
python3 scripts/desktop_ctrl.py mouse move 200 200

# 滚动
python3 scripts/desktop_ctrl.py mouse scroll 10
```

### 键盘控制
```bash
# 输入文字
python3 scripts/desktop_ctrl.py keyboard type "Hello World"

# 按键
python3 scripts/desktop_ctrl.py keyboard press enter

# 快捷键（Cmd+C）
python3 scripts/desktop_ctrl.py keyboard hotkey command c
```

### 截屏
```bash
python3 scripts/desktop_ctrl.py screenshot
```

### 进程管理
```bash
# 列出进程
python3 scripts/desktop_ctrl.py process list

# 结束进程
python3 scripts/desktop_ctrl.py process kill Safari
```

---

## 🔧 组合使用示例

### 示例 1: 系统状态报告
```bash
#!/bin/bash
echo "=== 系统状态报告 ==="
echo ""
bash scripts/system_info.sh --short
echo ""
echo "=== 运行的应用 ==="
bash scripts/processes.sh -g
echo ""
echo "=== 磁盘使用 ==="
bash scripts/system_info.sh -d
```

### 示例 2: 自动化工作流
```bash
#!/bin/bash
# 1. 截屏
bash scripts/screenshot.sh -d 3

# 2. 打开应用
bash scripts/app_control.sh open Safari

# 3. 等待 2 秒
sleep 2

# 4. 再截屏
bash scripts/screenshot.sh -w
```

### 示例 3: 监控脚本
```bash
#!/bin/bash
while true; do
    echo "=== $(date) ==="
    bash scripts/processes.sh -t 5
    sleep 60
done
```

---

## 🐛 故障排除

### 检查权限
```bash
bash scripts/check_permissions.sh
```

### 运行安装脚本
```bash
bash scripts/install.sh
```

---

**最后更新**: 2026-03-31
