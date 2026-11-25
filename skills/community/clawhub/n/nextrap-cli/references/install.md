# 安装 Nextrap CLI / Install Nextrap CLI

## 简体中文

安装 Skill 后，还需要单独安装 Nextrap CLI。已有可用的 CLI 时，直接用 `nextrap-cli --version` 核对版本。

1. 从 [官方发布页](https://github.com/nextrap-net/nextrap-cli/releases/latest) 下载与当前系统和 CPU 架构对应的包，以及同一版本的 `checksums.txt`。Apple 芯片选 `darwin_arm64`，Intel Mac 选 `darwin_amd64`。
2. 用 `checksums.txt` 核对安装包的 SHA-256，校验通过后解压。将程序放到当前用户目录，并把程序所在目录加入 `PATH`。Windows 保留 `nextrap-cli.exe` 文件名。macOS 和 Linux 如缺执行权限，运行 `chmod +x nextrap-cli`。
3. 在终端运行 `nextrap-cli --version`，确认名称为 `nextrap-cli`、渠道为 `stable`、分发版本为 `public`。需要首次认证时，在本机终端输入 API Key，详见 [认证说明](auth.md)。

用户明确要求代装时，Agent 可以按以上步骤安装到当前用户目录，并报告程序位置和版本检查结果。详细说明见 [官网 CLI 安装页](https://www.nextrap.net/developer#cli-install)。

## English

Install Nextrap CLI separately from this Skill. If you already have a working copy, check its version with `nextrap-cli --version`.

1. Download the archive for your operating system and CPU architecture, along with `checksums.txt` from the same [official release](https://github.com/nextrap-net/nextrap-cli/releases/latest). Choose `darwin_arm64` for Apple silicon or `darwin_amd64` for an Intel Mac.
2. Verify the archive's SHA-256 against `checksums.txt`, then extract it. Place the executable in a directory you own and add that directory to `PATH`. Keep the filename `nextrap-cli.exe` on Windows. On macOS or Linux, run `chmod +x nextrap-cli` if needed.
3. Run `nextrap-cli --version` and check that the name is `nextrap-cli`, the channel is `stable`, and the distribution is `public`. For first-time authentication, enter your API key in your local terminal. See [authentication](auth.md).

If the user asks you to install the CLI, follow these steps in their user directory and report the executable path and version check result.
