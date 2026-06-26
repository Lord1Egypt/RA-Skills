# PC Control API 完整文档

## 环境信息
- 工具路径：`/mnt/d/openclawTool/`（WSL访问Windows D盘）
- 入口文件：`pc.py`（CLI）、`api.py`（HTTP服务）

## 启动API服务

```bash
cd /mnt/d/openclawTool && python api.py
```

服务运行在 `http://localhost:8080`，文档：`http://localhost:8080/docs`

---

## 屏幕

### 截图
```bash
python pc.py screenshot [--path 保存路径]
```
```bash
curl "http://localhost:8080/screenshot?path=my.png"
```

### 屏幕信息
```bash
python pc.py screen-info
```
```bash
curl "http://localhost:8080/screen-info"
```

---

## 剪贴板

### 读取
```bash
python pc.py clipboard read
```
```bash
curl "http://localhost:8080/clipboard/read"
```

### 写入
```bash
python pc.py clipboard write --text "内容"
```
```bash
curl -X POST "http://localhost:8080/clipboard/write" -H "Content-Type: application/json" -d '{"text":"内容"}'
```

---

## 键盘

### 按键
```bash
python pc.py key press enter
```
```bash
curl -X POST "http://localhost:8080/key/press" -H "Content-Type: application/json" -d '{"key":"enter"}'
```

### 输入文本
```bash
python pc.py key type --text "Hello World"
```
```bash
curl -X POST "http://localhost:8080/key/type" -H "Content-Type: application/json" -d '{"text":"Hello","interval":0.05}'
```

### 快捷键
```bash
python pc.py key hotkey --keys ctrl c
```
```bash
curl -X POST "http://localhost:8080/key/hotkey" -H "Content-Type: application/json" -d '{"keys":["ctrl","c"]}'
```

### 按下/松开
```bash
python pc.py key down ctrl
python pc.py key up ctrl
```

---

## 鼠标

### 移动
```bash
python pc.py mouse move 100 200 [--duration 0.5]
```
```bash
curl -X POST "http://localhost:8080/mouse/move" -H "Content-Type: application/json" -d '{"x":100,"y":200,"duration":0}'
```

### 点击/双击/右键
```bash
python pc.py mouse click 100 200
python pc.py mouse double 100 200
python pc.py mouse right 100 200
```
```bash
curl -X POST "http://localhost:8080/mouse/click" -H "Content-Type: application/json" -d '{"x":100,"y":200}'
```

### 拖拽
```bash
python pc.py mouse drag 300 400
```

### 滚轮
```bash
python pc.py mouse scroll 3
```
```bash
curl -X POST "http://localhost:8080/mouse/scroll" -H "Content-Type: application/json" -d '{"clicks":3}'
```

### 获取位置
```bash
python pc.py mouse position
```

---

## 进程

### 列表
```bash
python pc.py process list
```
```bash
curl "http://localhost:8080/process/list"
```

### 结束进程
```bash
python pc.py process kill notepad
```
```bash
curl -X POST "http://localhost:8080/process/kill" -H "Content-Type: application/json" -d '{"name":"notepad"}'
```

### 获取进程信息
```bash
python pc.py process get python
```

---

## 窗口

### 列表
```bash
python pc.py window list
```
```bash
curl "http://localhost:8080/window/list"
```

### 聚焦/最小化/最大化/关闭
```bash
python pc.py window focus "Notepad"
python pc.py window minimize "Notepad"
python pc.py window maximize "Notepad"
python pc.py window close "Notepad"
```

---

## 系统

```bash
python pc.py system info
python pc.py system displays
```

---

## 文件

```bash
python pc.py file read C:/test.txt
python pc.py file write C:/test.txt --content "内容"
python pc.py file list C:/
python pc.py file exists C:/test.txt
```

---

## Shell

```bash
python pc.py shell run "Get-Process" [--shell powershell|cmd] [--timeout 10]
```

```bash
curl -X POST "http://localhost:8080/shell/run" -H "Content-Type: application/json" \
  -d '{"command":"Get-Process","shell":"powershell","timeout":30}'
```

---

## 浏览器自动化

需先安装浏览器驱动（Firefox/Chrome/Edge）。

### 启动浏览器
```bash
curl -X POST "http://localhost:8080/browser/start" -H "Content-Type: application/json" \
  -d '{"browser":"firefox","headless":false}'
```

### 导航
```bash
curl -X POST "http://localhost:8080/browser/navigate" -H "Content-Type: application/json" \
  -d '{"url":"https://www.example.com"}'
```

### 点击/输入
```bash
curl -X POST "http://localhost:8080/browser/click" -H "Content-Type: application/json" \
  -d '{"text":"按钮文字"}'
curl -X POST "http://localhost:8080/browser/input" -H "Content-Type: application/json" \
  -d '{"index":0,"text_to_input":"内容"}'
```

### 截图/执行JS/滚动/刷新/前进/后退

---

## 返回格式

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

失败：
```json
{
  "success": false,
  "data": null,
  "error": "错误信息"
}
```
