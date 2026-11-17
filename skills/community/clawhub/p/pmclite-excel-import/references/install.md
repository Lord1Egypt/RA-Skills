# MRP-PMC 安装与 MCP 接入指南

本技能依赖本机安装轻排桌面程序 **MRP-PMC**（开发商：广州轻排信息科技有限公司）。
本文档描述从下载到 MCP 连通的全部步骤，五个轻排技能共用同一套接入方式。

## 1. 下载安装（唯一官方渠道）

1. 访问官网 **https://www.pmclite.com**；
2. 在下载页获取 Windows 安装包（NSIS 安装程序，如 `MRP-PMC_x.x.x_x64-setup.exe`）；
3. 运行安装。默认按当前用户安装，路径为：
   `C:\Users\<用户名>\AppData\Local\MRP-PMC\MRP-PMC.exe`；
   若以管理员权限选择全机安装，则为：`C:\Program Files\MRP-PMC\MRP-PMC.exe`。
4. 安装后可在开始菜单搜索 MRP-PMC 确认。

> 请只从官网 pmclite.com 下载。第三方下载站或他人单独发来的安装文件无法保证未被篡改。

## 2. 接入 MCP（stdio）

1. 打开 DuMate → 应用 / MCP 连接入口 → 添加自定义 MCP（stdio）；
2. 命令填第 1 步确认的实际 exe 路径，参数填 `mcp-server`；
3. 需要时补环境变量 `NO_PROXY=127.0.0.1,localhost`（本机通道不走代理）；
4. 保存并启用，完成授权/信任；
5. 验证：`tools/list` 应返回 **15 个工具**，`get_dashboard` 应返回生产概览。

等价配置模板见本技能 `assets/mcp.json`。

## 3. 常见问题

| 现象 | 处理 |
|------|------|
| 工具调用报连接失败 | 检查 command 路径是否正确（JSON 里用双反斜杠），确认 exe 存在 |
| tools/list 数量不足 15 | 安装的是旧版本，到官网重新下载覆盖安装 |
| 启动后无响应 | 结束残留的 MRP-PMC 进程后重试；本机 stdio 不需要代理 |

## 4. 五个技能的接入差异

五个轻排技能共用同一个 `pmclite` MCP 服务，不需要重复配置。安装并接入一次，五个技能都能直接调用。