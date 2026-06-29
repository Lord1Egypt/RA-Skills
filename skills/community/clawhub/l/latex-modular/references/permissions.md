# 权限说明

## 操作权限权重

| 操作 | 权限权重 | 说明 |
|------|---------|------|
| 读取 manifest/组件 | READ | 读取 components/ 目录和 manifest.json |
| 生成 .tex 文档 | WRITE | 调用 compose.py 输出 .tex 文件 |
| 编译验证 | EXECUTE | 调用系统 lualatex 编译 |
| 写入 body.txt | WRITE | 更新 components/body.txt |
| 操作组件库 | WRITE | 更新 components/ 下的组件文件 |
| 读取系统 LaTeX | READ | 调用系统 lualatex/latex 引擎 |

所有操作均为本地文件系统操作，不涉及网络或外部 API。
权限等级：LOW（不影响系统安全）。
