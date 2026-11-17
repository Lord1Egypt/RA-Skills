# OEF 查询功能 v3.0.0 安装工作流：open-fund-query

本工作流用于单独安装并初始化场外指数基金查询功能（open-fund-query）。安装时请按阶段执行；如果遇到异常，按对应阶段的处理方式给出原因和修复建议，不要跳过。

## 输入参数

- `apiKey`：必填。基金查询服务 API Key。安装脚本也支持不传入参数时交互式输入。
- `skillsDir`：可选。安装目录，默认 `~/.openclaw/workspace/skills`。也可以通过环境变量 `OPENCLAW_SKILLS_DIR` 覆盖。
- `--skip-api-verify`：可选。离线安装或网络受限时跳过接口连通性校验。

## API Key 与额度说明

安装前请准备基金查询服务 API Key。每位用户每日享有 500 次免费 API 接口调用额度；单次提问可能调用多个接口，额度按实际接口调用次数计算。

如需获取API Key，请在微信搜索“指数直通车”小程序，在「AI Skills」页面申请。更多说明可访问帮助文档：https://cdn.efunds.com.cn/eda/h5/itcenter/pd/ai-skills-doc/help.pdf

问题反馈或技术支持邮箱：indexhub@efunds.com.cn

一键安装命令：

```bash
./install.sh
```

离线或仅做本地配置校验：

```bash
./install.sh --skip-api-verify
```

只更新本机私有 key，不重新复制功能文件：

```bash
./install.sh --no-install --skip-api-verify
```

`--no-install` 仅适用于已经安装独立凭据文件版本的用户。若安装脚本检测到旧版 `config.py`，会在写入新 Key 前停止；请改用当前安装包的安装入口执行一次完整安装，不要使用 `--no-install`。

## 阶段 1：环境检测

检查项：

- 当前系统是否可运行 shell 脚本。
- 是否存在 `python3`。
- Python 版本是否不低于 3.8。
- 是否能创建或写入安装目录，默认 `~/.openclaw/workspace/skills`。

异常处理：

- 未找到 `python3`：安装 Python 3.8 或更高版本后重试。
- Python 版本过低：升级 Python 后重试。
- 安装目录不可写：修复目录所有权/权限，或使用 `--skills-dir` 指定可写目录。

## 阶段 2：安装包完整性检查

检查项：

- `open-fund-query/` 目录是否完整存在。
- `SKILL.md`、`config.py`、`guardrails.py` 和 `references/catalog-oef.md` 是否齐全。

异常处理：

- 目录或文件缺失：不要继续安装；重新解压安装包，或重新下载完整安装包。

## 阶段 3：初始化 API Key

执行内容：

- 从 `--api-key` 参数读取 key；如果未传入，则交互式隐藏输入。
- 安装日志只显示脱敏 key。

异常处理：

- key 为空：重新运行 `./install.sh` 并按提示隐藏输入。

## 阶段 4：安装并写入 API Key

执行内容：

- 将 `open-fund-query` 复制到目标安装目录。
- 将对应版本的 `config.py` 写入已安装功能目录。
- 将 API Key 写入独立凭据文件 `~/.config/index-hub/api_key`，目录权限设为 `0700`，文件权限设为 `0600`。
- 不修改 `~/.zshrc`、`~/.bash_profile`，也不把 Key 写入 `config.py`。
- 运行时可用 `INDEX_HUB_API_KEY` 临时覆盖凭据文件，并兼容旧变量 `ETF_API_KEY`。
- 从旧版本升级时，安装器不会自动修改 shell profile；如果旧安装器曾写入 `INDEX_HUB_API_KEY` 或 `ETF_API_KEY`，请在确认新版本查询正常后手动删除对应的 `export` 行。

异常处理：

- 复制失败：检查目标目录权限，或使用 `--skills-dir DIR`。
- 凭据文件写入失败：检查 HOME 目录、`~/.config/index-hub` 的所有权和写入权限。

## 阶段 5：能力校验

本地校验：

- `open-fund-query` 能正确加载本地配置，读取到 API Key。

接口连通性校验：

- 调用场外基金详情接口，使用示例代码 `006748`。

异常处理：

- 接口校验失败：检查网络、API Key 是否有效；离线环境可加 `--skip-api-verify` 先完成安装。
- 如果接口明确返回 API Key 无效或已过期，必须停止安装并要求更换有效 key。

## 阶段 6：完成确认

完成后输出：

- 安装目录。
- 可用功能：`open-fund-query`。
