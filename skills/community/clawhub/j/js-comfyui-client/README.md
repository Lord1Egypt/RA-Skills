# js-comfyui-skill

通过 ComfyUI HTTP API 调用工作流：加载 JSON、修改 prompt / 参考图、提交队列、轮询并在本地保存生成的图片或视频。可作为独立仓库使用，也可放入 `.claude/skills/comfyui-client/` 供 Agent 技能引用。

## 前置条件

- [Node.js](https://nodejs.org/) 18+
- 已启动的 [ComfyUI](https://github.com/comfyanonymous/ComfyUI)（默认 `http://127.0.0.1:8188`）
- 工作流依赖的模型已安装到对应 ComfyUI

## 快速开始

```bash
git clone https://github.com/imjszhang/js-comfyui-skill.git
cd js-comfyui-skill
npm install
```

若已在本地有副本，直接进入目录执行 `npm install` 即可。

可选：复制环境变量模板并修改服务端地址（与命令行 `--server` 等价）。

```bash
cp .env.example .env   # Windows 可复制 .env.example 并重命名为 .env
```

## 使用示例

在项目根目录执行（工作流路径相对仓库根）：

```bash
node scripts/comfyUIClient.js \
  --workflow assets/workflows/image_z_image_turbo.json \
  --prompt "a beautiful landscape at sunset"
```

查看全部选项：

```bash
node scripts/comfyUIClient.js --help
# 或
npm run comfyui -- --help
```

## 目录说明

| 路径 | 说明 |
|------|------|
| `scripts/comfyUIClient.js` | 主脚本 |
| `assets/workflows/` | 内置示例工作流（Z-Image、Qwen 编辑、Wan 视频等） |
| `SKILL.md` | 面向 Agent 的完整技能说明（能力、节点 ID、排错等） |
| `references/workflow_paths.md` | 工作流路径速查 |

默认输出目录：`work_dir/comfyui_output/<会话名>/`（已在 `.gitignore` 中忽略，勿提交）。

## 许可证

MIT
