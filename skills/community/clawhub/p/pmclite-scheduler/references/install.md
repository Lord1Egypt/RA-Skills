# MRP-PMC 安装与 MCP 接入指南（百度搭子）

本技能需要本机安装轻排桌面程序 **MRP-PMC**（开发商：广州轻排信息科技有限公司）。
本文档描述从下载到 MCP 连通的全部步骤。

## 1. 下载安装（唯一官方渠道）

1. 访问官网 **https://www.pmclite.com**；
2. 在下载页获取 Windows 安装包（NSIS 安装程序，如 `MRP-PMC_x.x.x_x64-setup.exe`）；
3. 运行安装。默认按当前用户安装，路径为：
   `C:\Users\<用户名>\AppData\Local\MRP-PMC\MRP-PMC.exe`；
   若以管理员权限选择全机安装，则为：
   `C:\Program Files\MRP-PMC\MRP-PMC.exe`。
4. 安装后可在开始菜单搜索 MRP-PMC 确认；右键快捷方式 → 打开文件位置，可得到准确路径。

> ⚠️ 请只从官网 pmclite.com 下载。不要使用搜索引擎结果中的第三方下载站，不要接受他人
> 单独发来的安装文件——无法保证未被篡改。

## 2. 在百度搭子中接入 MCP

百度搭子原生支持自定义 MCP 应用接入。按 stdio 方式填写：

1. 打开百度搭子 → 应用 / MCP 连接入口 → 添加自定义 MCP（stdio）；
2. 命令填第 1 步确认的实际 exe 路径，参数填 `mcp-server`；
3. 需要时补环境变量 `NO_PROXY=127.0.0.1,localhost`（本机通道不走代理）；
4. 保存并启用，完成授权/信任。

等价的配置文件写法（模板见本技能 `assets/mcp.json`）：

```json
{
  "mcpServers": {
    "pmclite": {
      "type": "stdio",
      "command": "C:\\Users\\<用户名>\\AppData\\Local\\MRP-PMC\\MRP-PMC.exe",
      "args": ["mcp-server"],
      "env": {
        "NO_PROXY": "127.0.0.1,localhost"
      }
    }
  }
}
```

5. 重启客户端（若界面要求），在 MCP 列表中确认 **pmclite** 为已连接；
6. 验证：调用 `get_dashboard` 应返回生产概览文本；`tools/list` 应返回 **15 个工具**。

其他支持 MCP stdio 的客户端（WorkBuddy、Claude Desktop 等）同理，只是配置文件位置不同。

## 3. 常见问题

| 现象 | 处理 |
|------|------|
| 工具调用报连接失败 | 检查 command 路径是否正确（JSON 里用 `\\` 双反斜杠）；确认 exe 存在 |
| tools/list 数量不足 15 | 安装的是旧版本安装包，请到官网重新下载最新版覆盖安装 |
| 启动后无响应 | 确认没有其它 MRP-PMC 进程残留（任务管理器结束后再试）；检查代理设置，本机 stdio 通道不需要代理（模板中的 `NO_PROXY` 即为此准备） |
| 数据在哪 | 与桌面端共用同一数据库（`%APPDATA%\com.dell.MRP-PMC\data.db`，加密存储），MCP 的查询与写入和桌面端完全一致 |
| 想先试功能 | 桌面端支持导入行业模板/演示数据，可先在副本数据上跑通再接入真实数据 |

## 4. 数据与隐私

- 所有业务数据（工单、库存、报工记录）保存在用户本机加密 SQLite 中；
- 技能通过本地 stdio 管道与 MRP-PMC 通信，不经过任何第三方服务器；
- 卸载程序不会删除业务数据库，重装后数据仍在。
