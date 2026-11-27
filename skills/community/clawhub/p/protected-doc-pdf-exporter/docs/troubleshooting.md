# 故障排除指南 (Troubleshooting Guide)

## 1. 登录会话未检测到或过期

### 现象
提示：`RuntimeError: Weboffice iframe context not found. Make sure user has logged in.`

### 解决方式
1. 打开宿主机安装的 Google Chrome 或 Microsoft Edge；
2. 访问目标文档链接，使用微信/企业微信扫码登录，确保在浏览器中能正常看到文档正文；
3. 重新运行导出命令即可（脚本会自动复用该会话，无需输入账号密码）。
4. 也可以使用 `--no-headless` 参数以可视化窗口运行，在弹出的窗口中直接扫码登录。

---

## 2. 导出路径权限受限 (Read-only file system)

### 现象
`OSError: [Errno 30] Read-only file system`

### 解决方式
目标路径位于只读挂载盘（如部分移动硬盘或特定虚拟目录），请将输出路径改为可写目录：
- `~/Downloads/document.pdf`
- `~/Desktop/document.pdf`

---

## 3. 页面瓦片拼缝与错位问题

### 原理
部分文档采用非标准纵横比或高 DPI 缩放。新版 `WeComWebofficeExtractor` 已采用**动态外接矩形与坐标映射算法**：
- 自动读取每个 Canvas Tile 的真实 CSS `left`、`top` 坐标与设备的物理像素比（ScaleX/ScaleY）；
- 自动计算最小包围矩形（`minX, minY, maxX, maxY`）并映射至最终输出画布；
- 拼缝处实现零错位、零重叠缝隙。

---

## 4. 指定页码范围过滤导出

使用 `--pages` 参数按需导出指定页码，节省时间与磁盘空间：
```bash
# 导出第 1 到第 5 页
python3 export_doc.py --url "..." -o out.pdf --pages "1-5"

# 导出第 1、第 3、第 5 至 8 页
python3 export_doc.py --url "..." -o out.pdf --pages "1,3,5-8"
```
