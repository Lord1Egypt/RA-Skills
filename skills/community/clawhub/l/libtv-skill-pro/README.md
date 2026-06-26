# libtv-skill-pro

> 🎬 LibTV (liblib.tv) AI 视频/图像生成平台的 OpenClaw / ClawHub skill。Pro 版在 [@haofanwang/libtv-skill](https://clawhub.ai/haofanwang/libtv-skill) 基础上扩展高级工作流与功能矩阵层。

[![ClawHub](https://img.shields.io/badge/ClawHub-libtv--skill--pro-orange)](https://clawhub.ai/qiuxiangxiang/libtv-skill-pro)
[![GitHub stars](https://img.shields.io/github/stars/Qiuxiangxiang/libtv-skill-pro?style=social)](https://github.com/Qiuxiangxiang/libtv-skill-pro)
[![GitHub issues](https://img.shields.io/github/issues/Qiuxiangxiang/libtv-skill-pro)](https://github.com/Qiuxiangxiang/libtv-skill-pro/issues)
[![License](https://img.shields.io/badge/license-MIT--0-blue)](LICENSE)

## 是什么

让 Agent（OpenClaw / Claude Code / 其他 ClawHub-compatible 客户端）通过统一入口调用 LibTV 平台的 AI 创作能力：

- **生成**：文生图/视频、图生图/视频、首尾帧视频、音频驱动视频
- **编辑**：局部修改（"把纸船换成爱心"）、风格迁移、运镜调整
- **多模型路由**：Seedance 2.0 / Kling 3.0/O3 / Wan 2.6 / Nano Banana / Midjourney / Seedream 5.0 / Lib Nano Pro / GVLM 3.1
- **工作流**：批量并发、轮询监控、8 个预设模板（短剧/MV/角色设计/分镜...）、HTML 报告导出
- **dry-run 预览**：所有生成类命令支持 `--dry-run`，预览 prompt 不烧积分
- **结构化错误**：API 错误以 JSON 输出，Agent 程序化可处理

## 安装

### 方式 1：通过 ClawHub（推荐）

```bash
openclaw skills install libtv-skill-pro
```

### 方式 2：从这个仓库克隆

```bash
git clone https://github.com/Qiuxiangxiang/libtv-skill-pro.git ~/.agents/skills/libtv-skill-pro
```

## 快速开始

```bash
# 1. 拿 access key：https://www.liblib.tv → 用户中心 → API
export LIBTV_ACCESS_KEY=your_key_here

# 2. 看命令清单
python3 scripts/libtv.py --help

# 3. dry-run 预览（不烧积分）
python3 scripts/libtv.py model with lib-nano-pro \
  "白色短毛猫坐在窗台上" --ratio 1:1 --resolution 2K --dry-run

# 4. 真实生成 + 轮询 + 下载
python3 scripts/libtv.py model with lib-nano-pro "..." --ratio 1:1
python3 scripts/libtv.py poll SESSION_ID
python3 scripts/libtv.py download SESSION_ID --output-dir ~/Downloads/cat
```

完整示例见 [`examples/`](./examples/)（5 个递进难度的 case）。

## 命令地图

```
libtv.py flow      预设流程（故事脚本/角色三视图/首帧图生视频/音频生视频）
libtv.py node      节点能力（文本/图片/视频节点细分动作）
libtv.py edit      修饰器（风格/标记/聚焦/运镜/角色库）
libtv.py model     模型路由（list 已知模型 / with 指定模型生成）

libtv.py session   创建会话/发消息       libtv.py query   查询会话进展
libtv.py upload    上传图片/视频         libtv.py download 下载结果

libtv.py batch     并发批量任务          libtv.py monitor 实时监控
libtv.py poll      简化轮询              libtv.py template 预设工作流模板
libtv.py export    导出 HTML/MD/JSON     libtv.py history 会话历史
libtv.py project   项目管理
```

17 个独立脚本（`scripts/*.py`）仍可单独调用（向后兼容）。

## 跟原版的关系

| | @haofanwang/libtv-skill | @qiuxiangxiang/libtv-skill-pro |
|---|---|---|
| 基础脚本 | 6 个 | 6 个（保留原版） |
| 高级工作流 | — | 7 个（batch/monitor/poll/template/export/history/project） |
| LibTV 功能矩阵 | — | 4 个（flow/node/edit/model） |
| 统一入口 | — | libtv.py |
| dry-run 预览 | — | ✓ |
| 结构化错误 | — | ✓ |

如果你只需要"自然语言一句话路由"的极简体验，原版 6 脚本足够。Pro 版面向**批量、精细控制、Agent 程序化集成**场景。

## 测试

```bash
# 离线（5 秒，不烧积分，120 个用例）
bash tests/test_offline.sh && python3 tests/test_templates.py

# 在线（按开关计费）
ONLINE_SESSION=1 bash tests/test_online.sh    # ≈0 积分
ONLINE_IMAGE=1   bash tests/test_online.sh    # ≈14 积分
ONLINE_VIDEO=1   bash tests/test_online.sh    # ≈135 积分
```

详细测试矩阵见 [`tests/README.md`](./tests/README.md)。

## 贡献

发现 bug 或想加新功能：

1. Issue 描述场景 + 预期 vs 实际
2. PR 前请跑通 `bash tests/test_offline.sh && python3 tests/test_templates.py`
3. 新功能请同时在 `tests/` 加用例 + 在 `examples/` 加 case

## License

MIT-0（与原版一致）。

## 致谢

- [@haofanwang/libtv-skill](https://clawhub.ai/haofanwang/libtv-skill) — 原版基础架构
- [LibTV (liblib.tv)](https://www.liblib.tv) — AI 视频创作平台
- [ClawHub](https://clawhub.ai) — Agent skill 分发
